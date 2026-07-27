"""Quick language detection using faster-whisper tiny model."""
import sys
from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")
for path in sys.argv[1:]:
    segments, info = model.transcribe(path, beam_size=1, vad_filter=False)
    # Consume generator so info is finalized
    list(segments)
    print(f"{path}\tlang={info.language}\tprob={info.language_probability:.3f}\tdur={info.duration:.2f}s")
