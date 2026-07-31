#!/bin/bash
# Concat all segment renders into videos/final/video-full.mp4
# Add new segments here as they're built.
set -e

cd "$(dirname "$0")/.."
mkdir -p videos/final

SEGMENTS=(
  "videos/sleep-schedule-guide/renders/video.mp4"
  "videos/sleep-schedule-guide-a2/renders/video.mp4"
  # add A3, A4... here
)

# Build filter graph for concat
n=${#SEGMENTS[@]}
inputs=()
maps=""
for i in "${!SEGMENTS[@]}"; do
  inputs+=("-i" "${SEGMENTS[$i]}")
  maps+="[${i}:v][${i}:a]"
done

ffmpeg -y -hide_banner -loglevel error "${inputs[@]}" \
  -filter_complex "${maps}concat=n=${n}:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k \
  videos/final/video-full.mp4

echo "✓ concat → videos/final/video-full.mp4"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 videos/final/video-full.mp4 | awk '{printf "  duration: %.2fs\n", $1}'
ls -lh videos/final/video-full.mp4 | awk '{print "  size:", $5}'
