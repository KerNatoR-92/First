#!/usr/bin/env python3
import json, sys, time
from pathlib import Path
from faster_whisper import WhisperModel

MODEL = "large-v3"
FILES = ["A1.wav", "A2.wav"]
OUT_DIR = Path("scripts/out")


def to_dict(seg):
    return {
        "id": seg.id,
        "start": seg.start,
        "end": seg.end,
        "text": seg.text,
        "avg_logprob": seg.avg_logprob,
        "no_speech_prob": seg.no_speech_prob,
        "words": [
            {"start": w.start, "end": w.end, "word": w.word, "probability": w.probability}
            for w in (seg.words or [])
        ],
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"loading {MODEL} (cpu, int8)...", flush=True)
    t0 = time.time()
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")
    print(f"loaded in {time.time()-t0:.1f}s", flush=True)

    for f in FILES:
        if not Path(f).exists():
            print(f"skip {f} (missing)", flush=True); continue
        print(f"transcribing {f}...", flush=True)
        t0 = time.time()
        segments, info = model.transcribe(
            f,
            beam_size=5,
            word_timestamps=True,
            vad_filter=True,
            language=None,
        )
        seg_list = [to_dict(s) for s in segments]
        out = {
            "audio": f,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "model": MODEL,
            "segments": seg_list,
        }
        out_path = OUT_DIR / (Path(f).stem + ".json")
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
        print(f"  {f}: lang={info.language} ({info.language_probability:.2f}), "
              f"{len(seg_list)} segments, {time.time()-t0:.1f}s -> {out_path}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
