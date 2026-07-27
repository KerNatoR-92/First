#!/usr/bin/env python3
"""Silence-gap-aware caption timing.

Reads narration.wav (A1 + A2), detects silence gaps within each audio segment,
and matches sentence boundaries to the largest gaps. This gives noticeably
better sync than pure character-count proportional distribution."""
import json, re, struct, wave

A1_END = 42.759
A2_END = 117.117

S1 = [
    "여러분은 평일과 주말에 각각 몇 시에 잠드시나요?",
    "평일에는 출근 때문에 억지로 일찍 일어나고,",
    "주말에는 밀린 잠을 보충하느라 점심때까지 자는 분들이 많습니다.",
    "야근이나 회식이 있는 날에는 새벽에 잠들고,",
    "다음 날 중요한 일정이 있으면 평소보다 일찍 일어나기도 합니다.",
    "이렇게 하루하루 자는 시간이 달라지면",
    "우리는 충분히 잤다고 생각해도 계속 피곤할 수 있습니다.",
    "오늘은 직장인에게 필요한 수면 시간은 몇 시간인지,",
    "규칙적으로 잠을 자면 무엇이 좋아지는지,",
    "반대로 수면 시간이 불규칙하면 어떤 문제가 생기는지 알아보겠습니다.",
    "그리고 잠들기 어려운 분들에게 도움이 될 수 있는",
    "음식과 성분, 생활 습관도 함께 이야기해 보겠습니다.",
]
S2 = [
    "성인은 일반적으로 하루에 최소 7시간 이상의 수면이 필요합니다.",
    "개인차는 있지만 대부분의 성인은",
    "약 7시간에서 9시간 정도 잠을 자는 것이 좋습니다.",
    "하지만 모든 사람에게 적용되는 절대적인 취침 시간이",
    "따로 정해져 있는 것은 아닙니다.",
    "중요한 것은 자신이 일어나야 하는 시간에서",
    "필요한 수면 시간을 거꾸로 계산하는 것입니다.",
    "예를 들어 아침 7시에 일어나야 하는 사람이라면",
    "밤 10시부터 12시 사이에는 잠들 수 있도록 준비하는 것이 좋습니다.",
    "7시간을 자려면 자정 전에 잠들어야 하고,",
    "8시간을 자려면 밤 11시,",
    "9시간을 자려면 밤 10시쯤 잠들어야 합니다.",
    "여기서 중요한 점은 침대에 들어가는 시간이 아니라",
    "실제로 잠드는 시간을 기준으로 계산해야 한다는 것입니다.",
    "평소 잠드는 데 30분 정도 걸린다면",
    "목표 취침 시간보다 30분 정도 일찍 침대에 들어가는 것이 좋습니다.",
    "그리고 수면 시간만큼 중요한 것이",
    "매일 비슷한 시간에 자고 일어나는 것입니다.",
    "주말이라고 해서 평일보다 서너 시간 늦게 자고 일어나면",
    "우리 몸은 매주 작은 시차 적응을 반복하게 됩니다.",
    "따라서 주말에도 기상 시간 차이를",
    "가능하면 한두 시간 이내로 유지하는 것이 좋습니다.",
]

def load_wav_rms(path, window_ms=20):
    """Return (rms_series, hop_seconds) — per-window RMS amplitude."""
    with wave.open(path, "rb") as w:
        assert w.getsampwidth() == 2 and w.getnchannels() == 1
        fr = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    samples = struct.unpack(f"<{n}h", raw)
    hop = int(fr * window_ms / 1000)
    rms = []
    for i in range(0, len(samples) - hop, hop):
        chunk = samples[i:i+hop]
        s = sum(x*x for x in chunk) / len(chunk)
        rms.append(s ** 0.5)
    return rms, hop / fr  # rms per window, seconds per hop

def find_silence_gaps(rms, hop_s, thresh_frac=0.12, min_gap_s=0.30):
    """Return list of {"start":s, "end":e, "len":l}. Filters out sub-300ms
    breath pauses; only real sentence-boundary pauses survive."""
    if not rms:
        return []
    sorted_r = sorted(rms)
    top = sorted_r[int(len(sorted_r)*0.8):]
    ref = sum(top)/len(top) if top else 1.0
    thresh = ref * thresh_frac
    gaps = []
    i = 0
    n = len(rms)
    while i < n:
        if rms[i] < thresh:
            j = i
            while j < n and rms[j] < thresh:
                j += 1
            gap_len = (j - i) * hop_s
            if gap_len >= min_gap_s:
                gaps.append({"start": i*hop_s, "end": j*hop_s, "len": gap_len})
            i = j
        else:
            i += 1
    return gaps

def align(lines, rms, hop_s, t0, t1):
    """Monotone-DP alignment of detected pauses to sentence boundaries.

    We need N-1 boundaries (onsets of sentences 1..N-1) inside [0, t1-t0].
    K real pauses are detected. Assign each pause monotonically to some
    boundary slot j; any slot not covered by a pause is char-weight
    interpolated between neighboring anchor pauses (or segment ends)."""
    n = len(lines)
    seg_dur = t1 - t0
    B = n - 1  # boundary slots
    gaps = find_silence_gaps(rms, hop_s)
    interior = [g for g in gaps if 0.15 < g["start"] and g["end"] < seg_dur - 0.15]
    K = len(interior)
    gap_ends = [g["end"] for g in interior]

    weights = [len(re.sub(r"\s", "", x)) for x in lines]
    total = sum(weights)
    cum = 0
    prop = []  # proportional target for boundary j (j = 0..B-1 = end of sentence j)
    for w in weights[:-1]:
        cum += w
        prop.append(seg_dur * (cum / total))

    # Monotone DP: assign K gaps to K slots (subset of 0..B-1), minimize
    # sum |gap_ends[i] - prop[slot_i]|, keeping slot_i strictly increasing.
    # dp[k][j] = min cost of assigning first k gaps into first j slots.
    INF = float("inf")
    K2 = min(K, B)  # can assign at most B gaps
    # We'll use K2 gaps (the "closest" set). But which K2? Try all — the best
    # DP subset with |gaps| <= B is what we want. Use full K but bound by B.
    dp = [[INF]*(B+1) for _ in range(K+1)]
    parent = [[None]*(B+1) for _ in range(K+1)]
    for j in range(B+1):
        dp[0][j] = 0
    for k in range(1, K+1):
        for j in range(1, B+1):
            # option A: skip slot j
            if dp[k][j-1] < dp[k][j]:
                dp[k][j] = dp[k][j-1]
                parent[k][j] = (k, j-1, None)
            # option B: assign gap k-1 to slot j-1
            cand = dp[k-1][j-1] + abs(gap_ends[k-1] - prop[j-1])
            if cand < dp[k][j]:
                dp[k][j] = cand
                parent[k][j] = (k-1, j-1, j-1)
    # Reconstruct: assignment[j] = gap_end or None
    assignment = [None]*B
    k, j = K, B
    while k > 0 and j > 0:
        prev = parent[k][j]
        if prev is None:
            break
        pk, pj, slot = prev
        if slot is not None:
            assignment[slot] = gap_ends[k-1]
        k, j = pk, pj

    # Fill in interpolated boundaries between anchor pauses using char weights.
    # Anchor list: (slot_index, time). Segment boundaries: (-1, 0.0), (B, seg_dur).
    anchors = [(-1, 0.0)]
    for j, a in enumerate(assignment):
        if a is not None:
            anchors.append((j, a))
    anchors.append((B, seg_dur))

    onsets = [None]*B
    for a in range(len(anchors)-1):
        j0, t_a = anchors[a]
        j1, t_b = anchors[a+1]
        if j1 == j0 + 1:
            continue  # no gaps between
        # sentences to distribute: indices (j0+1)..j1 inclusive (their ends fall between)
        # For slot j (j0 < j < j1), sentence j is the (j+1)-th sentence (0-indexed),
        # whose end = weight_sentence_j+1... wait let me be careful.
        # Boundary slot j = end of sentence j (0-indexed). Between anchors we have
        # sentences (j0+1)..j1 (both inclusive) whose weights control interpolation.
        seg_weights = [weights[s] for s in range(j0+1, j1+1)]
        seg_total = sum(seg_weights) or 1
        cumw = 0
        for s_idx, w in enumerate(seg_weights[:-1]):
            cumw += w
            slot_j = j0 + 1 + s_idx
            onsets[slot_j] = t_a + (t_b - t_a) * (cumw / seg_total)
    # Fill anchor onsets
    for j, a in enumerate(assignment):
        if a is not None:
            onsets[j] = a

    LEAD = 0.05
    onsets_full = [0.0] + onsets + [seg_dur]
    result = []
    for i, text in enumerate(lines):
        start_local = max(0.0, onsets_full[i] - LEAD)
        end_local = onsets_full[i+1] - 0.05
        if i == n - 1:
            end_local = seg_dur - 0.25
        s_abs = round(t0 + start_local, 3)
        e_abs = round(t0 + end_local, 3)
        result.append({"text": text, "start": s_abs, "end": e_abs,
                       "duration": round(e_abs - s_abs, 3),
                       "anchored": assignment[i] is not None if i < B else False})
    return result

# --- run ---
rms1, hop1 = load_wav_rms("public/A1.wav")
rms2, hop2 = load_wav_rms("public/A2.wav")

# Diagnostic: report detected gaps in each segment
gaps1 = find_silence_gaps(rms1, hop1)
gaps2 = find_silence_gaps(rms2, hop2)
print(f"A1: {len(rms1)} windows, {len(gaps1)} silence gaps ≥300ms")
for i, g in enumerate(gaps1[:20]):
    print(f"  gap {i:02d}: end={g['end']:.2f}s  length={g['len']*1000:.0f}ms")
print(f"A2: {len(rms2)} windows, {len(gaps2)} silence gaps ≥300ms")
for i, g in enumerate(gaps2[:30]):
    print(f"  gap {i:02d}: end={g['end']:.2f}s  length={g['len']*1000:.0f}ms")

cap1 = align(S1, rms1, hop1, 0.0, A1_END)
cap2 = align(S2, rms2, hop2, A1_END, A2_END)
captions = cap1 + cap2

# Scene groups — rescale for new A1 length (42.76s instead of 45.76s)
scenes = [
    {"id": "s1-question",   "start": 0.0,   "end": 5.5,   "bg": "window-moon"},
    {"id": "s2-weekly",     "start": 5.5,   "end": 18.5,  "bg": "bed-alarm"},
    {"id": "s3-lateshift",  "start": 18.5,  "end": 27.0,  "bg": "laptop-glow"},
    {"id": "s4-tired",      "start": 27.0,  "end": 33.5,  "bg": "timeline-drift"},
    {"id": "s5-topic-intro","start": 33.5,  "end": A1_END,"bg": "title-fade"},
    {"id": "s6-need-hours", "start": A1_END,"end": 57.5,  "bg": "number-focus"},
    {"id": "s7-no-absolute","start": 57.5,  "end": 71.5,  "bg": "reverse-calc"},
    {"id": "s8-example-7am","start": 71.5,  "end": 89.5,  "bg": "clock-hands"},
    {"id": "s9-real-vs-bed","start": 89.5,  "end": 101.5, "bg": "bed-latency"},
    {"id": "s10-consist",   "start": 101.5, "end": A2_END,"bg": "weekly-grid"},
]

out = {
    "narration": "public/narration.wav",
    "narration_duration": A2_END,
    "a1_end": A1_END,
    "captions": captions,
    "scenes": scenes,
}
with open("timings.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print()
print(f"Captions: {len(captions)}  Scenes: {len(scenes)}  Total: {A2_END}s")
for i, c in enumerate(captions):
    anch = "●" if c.get("anchored") else "○"
    print(f"  #{i+1:02d} {anch} {c['start']:>6.2f} → {c['end']:>6.2f}  ({c['duration']:>5.2f}s)  {c['text'][:44]}")
