#!/usr/bin/env python3
import sys
from faster_whisper import WhisperModel

audio = sys.argv[1] if len(sys.argv) > 1 else "A1.wav"
model_size = sys.argv[2] if len(sys.argv) > 2 else "tiny"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
_, info = model.transcribe(audio, beam_size=1, vad_filter=True, language=None)
print(f"{audio}\tlang={info.language}\tprob={info.language_probability:.3f}\tdur={info.duration:.2f}s")
