#!/usr/bin/env node
// Split the pre-recorded narration.wav into per-frame WAV slices using the
// TIME markers taken from SCRIPT.md (soft guides). Produces:
//   assets/voice/01.wav .. 07.wav
// and audio_meta.json that assemble-index.mjs consumes.

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const HERE = dirname(new URL(import.meta.url).pathname);
const ROOT = resolve(HERE, "..");
const WAV_IN = join(ROOT, "public/narration.wav");
const OUT_DIR = join(ROOT, "assets/voice");
const META_OUT = join(ROOT, "audio_meta.json");

// Boundaries in seconds derived from SCRIPT.md **Time:** guides.
// The 7 spoken frames; frame 8 is silent outro appended after last slice.
// Boundaries derived from detected sentence-end silence gaps in narration.wav.
// Silence detection points (RMS < 0.02 for >0.25s):
//   3.05, 8.25, 22.15, 32.85, 47.75  → F1/F2/F3/F4 ends and F6 end.
// F5→F6 boundary has no strong pause; split proportionally on character count.
const CUTS = [
  { frame: 1, start: 0.0,  end: 3.15  },
  { frame: 2, start: 3.15, end: 8.30  },
  { frame: 3, start: 8.30, end: 22.20 },
  { frame: 4, start: 22.20, end: 32.90 },
  { frame: 5, start: 32.90, end: 39.75 },
  { frame: 6, start: 39.75, end: 47.85 },
  { frame: 7, start: 47.85, end: 55.30 },
];

function parseWav(buf) {
  if (buf.toString("ascii", 0, 4) !== "RIFF") throw new Error("not RIFF");
  if (buf.toString("ascii", 8, 12) !== "WAVE") throw new Error("not WAVE");
  let pos = 12;
  let fmt = null, dataStart = 0, dataSize = 0;
  while (pos < buf.length - 8) {
    const id = buf.toString("ascii", pos, pos + 4);
    const size = buf.readUInt32LE(pos + 4);
    if (id === "fmt ") {
      fmt = {
        format: buf.readUInt16LE(pos + 8),
        channels: buf.readUInt16LE(pos + 10),
        sampleRate: buf.readUInt32LE(pos + 12),
        byteRate: buf.readUInt32LE(pos + 16),
        blockAlign: buf.readUInt16LE(pos + 20),
        bitsPerSample: buf.readUInt16LE(pos + 22),
      };
    } else if (id === "data") {
      dataStart = pos + 8;
      dataSize = size;
      break;
    }
    pos += 8 + size;
  }
  if (!fmt) throw new Error("no fmt chunk");
  if (!dataStart) throw new Error("no data chunk");
  return { fmt, dataStart, dataSize };
}

function writeWavSlice(outPath, fmt, samples) {
  const dataSize = samples.length;
  const buf = Buffer.alloc(44 + dataSize);
  buf.write("RIFF", 0, "ascii");
  buf.writeUInt32LE(36 + dataSize, 4);
  buf.write("WAVE", 8, "ascii");
  buf.write("fmt ", 12, "ascii");
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(fmt.format, 20);
  buf.writeUInt16LE(fmt.channels, 22);
  buf.writeUInt32LE(fmt.sampleRate, 24);
  buf.writeUInt32LE(fmt.byteRate, 28);
  buf.writeUInt16LE(fmt.blockAlign, 30);
  buf.writeUInt16LE(fmt.bitsPerSample, 32);
  buf.write("data", 36, "ascii");
  buf.writeUInt32LE(dataSize, 40);
  samples.copy(buf, 44);
  writeFileSync(outPath, buf);
}

const raw = readFileSync(WAV_IN);
const { fmt, dataStart, dataSize } = parseWav(raw);
const bytesPerSecond = fmt.sampleRate * fmt.blockAlign;
const totalSeconds = dataSize / bytesPerSecond;
console.log(
  `narration: ${totalSeconds.toFixed(3)}s @ ${fmt.sampleRate}Hz ${fmt.channels}ch ${fmt.bitsPerSample}-bit`,
);

mkdirSync(OUT_DIR, { recursive: true });
const voices = [];
for (const cut of CUTS) {
  const startByte = dataStart + Math.floor(cut.start * bytesPerSecond / fmt.blockAlign) * fmt.blockAlign;
  const endByte = dataStart + Math.floor(cut.end * bytesPerSecond / fmt.blockAlign) * fmt.blockAlign;
  const slice = raw.slice(startByte, Math.min(endByte, dataStart + dataSize));
  const outPath = join(OUT_DIR, `${String(cut.frame).padStart(2, "0")}.wav`);
  writeWavSlice(outPath, fmt, slice);
  const duration = slice.length / bytesPerSecond;
  voices.push({
    frame: cut.frame,
    path: `assets/voice/${String(cut.frame).padStart(2, "0")}.wav`,
    duration_s: Number(duration.toFixed(3)),
    words: [],
  });
  console.log(`  frame ${cut.frame}: ${duration.toFixed(3)}s → ${outPath}`);
}

const meta = {
  tts_provider: "prerecorded",
  voice_id: "user-supplied",
  bgm: null,
  bgm_pending: false,
  voices,
  sfx: [],
  total_duration_s: voices.reduce((s, v) => s + v.duration_s, 0),
};
writeFileSync(META_OUT, JSON.stringify(meta, null, 2));
console.log(`✓ audio_meta.json written: ${voices.length} voice slices, total ${meta.total_duration_s.toFixed(2)}s`);
