#!/usr/bin/env node
/**
 * retime.mjs — TIMINGS.json 기반으로 프레임 타이밍을 재조정하고 재렌더합니다.
 *
 * 사용법:
 *   1) TIMINGS.json 의 각 프레임 start/end 초를 수정하세요.
 *   2) node retime.mjs           # 기본: 재빌드 + check + 렌더 실행
 *   3) node retime.mjs --no-render  # 렌더는 건너뛰고 빌드만 (미리보기용)
 *   4) node retime.mjs --dry-run     # 실제 파일 수정 없이 계산 결과만 출력
 *
 * 동작:
 *   - assets/voice/A1.wav 를 새 boundaries 로 다시 자름 → assets/voice/NN.wav
 *   - STORYBOARD.md 의 각 프레임 duration 을 새 값으로 업데이트
 *   - 각 compositions/frames/NN-*.html 의 root/clip data-duration 재계산
 *   - audio_meta.json 재작성
 *   - assemble-index → transitions inject → check → snapshot → render
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, resolve, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const PROJECT = HERE;
const args = process.argv.slice(2);
const NO_RENDER = args.includes("--no-render");
const DRY = args.includes("--dry-run");

function die(msg) {
  console.error(`✗ retime: ${msg}`);
  process.exit(1);
}

const TIMINGS = JSON.parse(readFileSync(join(PROJECT, "TIMINGS.json"), "utf8"));
const SRC_WAV = join(PROJECT, TIMINGS.source_wav || "assets/voice/A1.wav");
if (!existsSync(SRC_WAV)) die(`source wav not found: ${SRC_WAV}`);

/* 1. sanity + duration compute */
const frames = TIMINGS.frames.map((f, i) => {
  if (typeof f.start !== "number" || typeof f.end !== "number") die(`frame ${i + 1} missing start/end`);
  if (f.end <= f.start) die(`frame ${i + 1} (${f.id}) has end (${f.end}) <= start (${f.start})`);
  return { ...f, duration: +(f.end - f.start).toFixed(3), idx: i + 1 };
});
for (let i = 1; i < frames.length; i++) {
  const prevEnd = frames[i - 1].end;
  if (Math.abs(frames[i].start - prevEnd) > 0.001) {
    console.warn(`⚠  frame ${i + 1} start ${frames[i].start}s ≠ prev end ${prevEnd}s (gap or overlap)`);
  }
}
const total = frames[frames.length - 1].end;
console.log(`◆ retime: ${frames.length} frame(s), total ${total.toFixed(3)}s`);
frames.forEach((f) => console.log(`  ${String(f.idx).padStart(2)} ${f.id.padEnd(22)} ${f.start.toFixed(3)}s → ${f.end.toFixed(3)}s   (${f.duration}s)`));

/* 2. split A1.wav into per-frame WAVs (ffmpeg) */
function splitWav(f) {
  const outRel = `assets/voice/${String(f.idx).padStart(2, "0")}.wav`;
  const outAbs = join(PROJECT, outRel);
  if (DRY) {
    console.log(`  (dry) ffmpeg cut -> ${outRel}`);
    return outRel;
  }
  mkdirSync(dirname(outAbs), { recursive: true });
  const r = spawnSync(
    "ffmpeg",
    ["-y", "-loglevel", "error", "-i", SRC_WAV, "-ss", String(f.start), "-to", String(f.end), "-c:a", "pcm_s16le", "-ar", "24000", "-ac", "1", outAbs],
    { stdio: ["ignore", "inherit", "inherit"] },
  );
  if (r.status !== 0) die(`ffmpeg failed for frame ${f.idx}`);
  return outRel;
}
console.log("· splitting A1.wav …");
frames.forEach((f) => (f._wav = splitWav(f)));

/* 3. rewrite STORYBOARD.md durations */
const sbPath = join(PROJECT, "STORYBOARD.md");
let sb = readFileSync(sbPath, "utf8");
frames.forEach((f) => {
  const anchor = new RegExp(`(src: compositions/frames/${f.id}\\.html)`, "m");
  if (!anchor.test(sb)) console.warn(`⚠  ${f.id}: src anchor not found in STORYBOARD.md`);
});
// Replace duration line inside each frame block: naive block detection by src anchor
for (const f of frames) {
  const re = new RegExp(`(- src: compositions/frames/${f.id}\\.html)`);
  // Find the frame section (from previous "## Frame" to next "## Frame")
  const idx = sb.indexOf(`compositions/frames/${f.id}.html`);
  if (idx < 0) continue;
  const headerStart = sb.lastIndexOf("## Frame", idx);
  const nextHeader = sb.indexOf("\n## Frame", idx);
  const end = nextHeader < 0 ? sb.length : nextHeader;
  const block = sb.slice(headerStart, end);
  const newBlock = block.replace(/- duration:\s*[\d.]+s?/m, `- duration: ${f.duration}s`);
  sb = sb.slice(0, headerStart) + newBlock + sb.slice(end);
}
if (!DRY) writeFileSync(sbPath, sb);
console.log("· updated STORYBOARD.md durations");

/* 4. rewrite frame HTMLs — root + inner .clip data-duration + timeline sync */
for (const f of frames) {
  const fp = join(PROJECT, "compositions", "frames", `${f.id}.html`);
  if (!existsSync(fp)) {
    console.warn(`⚠  ${f.id}.html not found — skipping`);
    continue;
  }
  let html = readFileSync(fp, "utf8");
  const d = f.duration;
  // 1) root data-duration
  html = html.replace(
    new RegExp(`(data-composition-id="${f.id}"[^>]*?data-duration=")[\\d.]+(")`, "g"),
    `$1${d}$2`,
  );
  // 2) every direct clip child under root that had a full-duration span: match values
  //    NOTE: transitions inject may extend these later, so set them to `d` here.
  html = html.replace(
    /(data-start="0"\s+data-duration=")[\d.]+(")/g,
    `$1${d}$2`,
  );
  if (!DRY) writeFileSync(fp, html);
}
console.log("· updated frame HTMLs (root + inner clip durations)");

/* 5. rewrite audio_meta.json */
const meta = {
  bgm: null,
  voices: frames.map((f) => ({
    frame: f.idx,
    path: f._wav,
    duration_s: f.duration,
    words: [],
  })),
  sfx: [],
};
if (!DRY) writeFileSync(join(PROJECT, "audio_meta.json"), JSON.stringify(meta, null, 2));
console.log("· rewrote audio_meta.json");

/* 6. reassemble + transitions + check + snapshot + render */
function run(cmd, argv, label) {
  if (DRY) {
    console.log(`  (dry) ${label}: ${cmd} ${argv.join(" ")}`);
    return 0;
  }
  console.log(`· ${label}`);
  const r = spawnSync(cmd, argv, { cwd: PROJECT, stdio: "inherit" });
  return r.status;
}

const SKILL = "/root/.claude/skills/faceless-explainer/scripts";
if (run("node", [`${SKILL}/assemble-index.mjs`, "--storyboard", "./STORYBOARD.md", "--hyperframes", "."], "assemble-index") !== 0) die("assemble-index failed");
// The assembler restores the CDN gsap src — swap back to local vendor
if (!DRY) {
  const idxPath = join(PROJECT, "index.html");
  const idx = readFileSync(idxPath, "utf8").replace(
    /<script src="https:\/\/cdn\.jsdelivr\.net\/npm\/gsap@[\d.]+\/dist\/gsap\.min\.js"[^>]*><\/script>/,
    '<script src="vendor/gsap.min.js"></script>',
  );
  writeFileSync(idxPath, idx);
}
if (run("node", [`${SKILL}/transitions.mjs`, "inject", "--storyboard", "./STORYBOARD.md", "--hyperframes", "."], "transitions inject") !== 0) die("transitions inject failed");
if (run("npx", ["hyperframes", "check"], "hyperframes check") !== 0) console.warn("⚠  check reported issues — see output above");

if (NO_RENDER) {
  console.log("◆ retime: build complete (--no-render). To render: node retime.mjs");
} else {
  // Take snapshots at each frame midpoint
  const mids = frames.map((f) => (f.start + f.end) / 2).map((n) => n.toFixed(3)).join(",");
  run("npx", ["hyperframes", "snapshot", "--at", mids], "snapshot");
  if (run("npx", ["hyperframes", "render", "--skill=faceless-explainer", "--quality", "high", "--output", "renders/video.mp4"], "render") !== 0) die("render failed");
  console.log("◆ retime: renders/video.mp4 ready");
}
