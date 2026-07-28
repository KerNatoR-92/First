"""Generate word-level timestamp JSON for A1.wav and A2.wav using faster-whisper."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUTS = ["A1.wav", "A2.wav"]
DEFAULT_OUT_DIR = ROOT / "data"


def transcribe(model: WhisperModel, audio_path: Path) -> dict:
    segments_iter, info = model.transcribe(
        str(audio_path),
        language="ko",
        word_timestamps=True,
        vad_filter=True,
        beam_size=5,
    )

    segments = []
    words = []
    for seg in segments_iter:
        seg_words = []
        for w in seg.words or []:
            entry = {
                "word": w.word,
                "start": round(float(w.start), 3),
                "end": round(float(w.end), 3),
                "probability": round(float(w.probability), 4),
            }
            seg_words.append(entry)
            words.append(entry)
        segments.append(
            {
                "id": seg.id,
                "start": round(float(seg.start), 3),
                "end": round(float(seg.end), 3),
                "text": seg.text,
                "words": seg_words,
            }
        )

    return {
        "audio": audio_path.name,
        "language": info.language,
        "language_probability": round(float(info.language_probability), 4),
        "duration": round(float(info.duration), 3),
        "segments": segments,
        "words": words,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="*", default=DEFAULT_INPUTS)
    parser.add_argument("--model", default="small")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)

    for name in args.inputs:
        audio_path = (ROOT / name) if not Path(name).is_absolute() else Path(name)
        if not audio_path.exists():
            raise FileNotFoundError(audio_path)
        print(f"[transcribe] {audio_path.name}")
        result = transcribe(model, audio_path)
        out_path = args.out_dir / f"{audio_path.stem}.words.json"
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"[transcribe] -> {out_path} ({len(result['words'])} words)")


if __name__ == "__main__":
    main()
