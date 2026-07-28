# scripts/

Whisper transcription pipeline for A1.wav / A2.wav.

## Prereqs

```bash
apt-get update && apt-get install -y ffmpeg
pip install faster-whisper
```

The remote environment blocks HuggingFace / Azure CDN by policy, so the
`WhisperModel(...)` call in `transcribe.py` cannot fetch its weights until
`huggingface.co` and `cdn-lfs.huggingface.co` are added to the environment's
egress allowlist.

## Run

```bash
python3 scripts/detect_lang.py A1.wav tiny   # smoke-test model download
python3 scripts/transcribe.py                # large-v3, word timestamps
```

Output: `scripts/out/A1.json`, `scripts/out/A2.json` with `segments[].words[]`
(each word carries `start`, `end`, `probability`).
