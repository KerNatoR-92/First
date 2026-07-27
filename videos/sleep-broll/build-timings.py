#!/usr/bin/env python3
"""Compute per-caption timings from Korean script, proportional to char count
within each audio segment (A1=45.76s, A2=74.36s)."""
import json, re, sys

A1_END = 45.760
A2_END = 120.118

# Section 1 (in A1, 0 to A1_END)
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
# Section 2 (in A2, A1_END to A2_END)
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

def hangul_chars(s):
    # Count non-space chars as speaking units
    return len(re.sub(r"[\s]", "", s))

def spread(lines, t0, t1, lead_head=0.15, lead_tail=0.3):
    """Distribute lines proportionally to char count over [t0, t1].
    lead_head: reveal caption slightly before spoken syllable starts.
    lead_tail: keep last caption on until near t1."""
    weights = [hangul_chars(x) for x in lines]
    total_w = sum(weights)
    window = t1 - t0
    # Track cumulative fraction, then compute onsets
    onsets = [t0]
    cum = 0
    for w in weights[:-1]:
        cum += w
        onsets.append(t0 + window * (cum / total_w))
    onsets.append(t1)  # sentinel
    # Convert to (start, end) with lead
    result = []
    for i, text in enumerate(lines):
        s = max(t0, onsets[i] - lead_head)
        e = onsets[i+1] - 0.05  # tiny gap before next
        if i == len(lines) - 1:
            e = t1 - lead_tail
        result.append({"text": text, "start": round(s, 3), "end": round(e, 3),
                       "duration": round(e - s, 3)})
    return result

cap1 = spread(S1, 0.0, A1_END)
cap2 = spread(S2, A1_END, A2_END)
captions = cap1 + cap2

# Scene groups (background macro-scenes)
scenes = [
    {"id": "s1-question",   "start": 0.0,   "end": 5.5,    "bg": "window-moon"},
    {"id": "s2-weekly",     "start": 5.5,   "end": 18.5,   "bg": "bed-alarm"},
    {"id": "s3-lateshift",  "start": 18.5,  "end": 28.5,   "bg": "laptop-glow"},
    {"id": "s4-tired",      "start": 28.5,  "end": 35.5,   "bg": "timeline-drift"},
    {"id": "s5-topic-intro","start": 35.5,  "end": 45.76,  "bg": "title-fade"},
    {"id": "s6-need-hours", "start": 45.76, "end": 60.0,   "bg": "number-focus"},
    {"id": "s7-no-absolute","start": 60.0,  "end": 74.0,   "bg": "reverse-calc"},
    {"id": "s8-example-7am","start": 74.0,  "end": 92.0,   "bg": "clock-hands"},
    {"id": "s9-real-vs-bed","start": 92.0,  "end": 104.0,  "bg": "bed-latency"},
    {"id": "s10-consist",   "start": 104.0, "end": 120.118,"bg": "weekly-grid"},
]

out = {
    "narration": "public/narration.wav",
    "narration_duration": A2_END,
    "captions": captions,
    "scenes": scenes,
}
with open("timings.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# Print summary
print(f"Captions: {len(captions)}  Scenes: {len(scenes)}  Total: {A2_END}s")
for i, c in enumerate(captions):
    print(f"  #{i+1:02d}  {c['start']:>6.2f} → {c['end']:>6.2f}  ({c['duration']:>5.2f}s)  {c['text'][:40]}")
