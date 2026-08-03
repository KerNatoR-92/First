#!/usr/bin/env python3
"""Fetch narration-matched background images per frame from Unsplash.

Reads scripts/frames.json (a list of frames with per-frame search queries),
downloads one photo per frame, resizes to the target size, and writes:
  - frames/<id>.jpg      (background image, ready to drop into HyperFrames)
  - frames/manifest.json (all frames with photographer credit + source URLs)

Runtime requires UNSPLASH_ACCESS_KEY.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
from pathlib import Path

import requests
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
UNSPLASH_SEARCH = "https://api.unsplash.com/search/photos"


def search_unsplash(query: str, orientation: str, access_key: str) -> dict:
    r = requests.get(
        UNSPLASH_SEARCH,
        params={"query": query, "orientation": orientation, "per_page": 5},
        headers={
            "Accept-Version": "v1",
            "Authorization": f"Client-ID {access_key}",
        },
        timeout=30,
    )
    r.raise_for_status()
    results = r.json().get("results") or []
    if not results:
        raise RuntimeError(f"no Unsplash results for query: {query!r}")
    return results[0]


def trigger_download(photo: dict, access_key: str) -> None:
    location = (photo.get("links") or {}).get("download_location")
    if not location:
        return
    with contextlib.suppress(requests.RequestException):
        requests.get(
            location,
            headers={"Authorization": f"Client-ID {access_key}"},
            timeout=15,
        )


def fetch_and_fit(photo: dict, size: tuple[int, int]) -> Image.Image:
    urls = photo.get("urls") or {}
    url = urls.get("full") or urls.get("regular")
    if not url:
        raise RuntimeError("Unsplash result has no usable image URL")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    img = Image.open(io.BytesIO(r.content)).convert("RGB")

    target_w, target_h = size
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    resized = img.resize((int(src_w * scale), int(src_h * scale)), Image.LANCZOS)
    x0 = (resized.width - target_w) // 2
    y0 = (resized.height - target_h) // 2
    return resized.crop((x0, y0, x0 + target_w, y0 + target_h))


def process_frame(frame: dict, size: tuple[int, int], out_dir: Path, access_key: str) -> dict:
    query = frame["query"]
    orientation = frame.get("orientation", "landscape")

    photo = search_unsplash(query, orientation, access_key)
    trigger_download(photo, access_key)
    img = fetch_and_fit(photo, size)

    out_path = out_dir / f"{frame['id']}.jpg"
    img.save(out_path, "JPEG", quality=88, optimize=True)

    user = photo.get("user") or {}
    return {
        "id": frame["id"],
        "audio": frame.get("audio"),
        "start": frame.get("start"),
        "end": frame.get("end"),
        "narration": frame.get("narration"),
        "query": query,
        "image": str(out_path.relative_to(REPO_ROOT)),
        "photographer": user.get("name"),
        "photographer_url": (user.get("links") or {}).get("html"),
        "photo_url": (photo.get("links") or {}).get("html"),
        "unsplash_id": photo.get("id"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "scripts" / "frames.json"),
        help="Path to frames.json",
    )
    args = parser.parse_args()

    access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not access_key:
        print("error: UNSPLASH_ACCESS_KEY is not set", file=sys.stderr)
        return 2

    config = json.loads(Path(args.config).read_text())
    size = tuple(config.get("image_size", [1920, 1080]))
    out_dir = REPO_ROOT / config.get("output_dir", "frames")
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for frame in config["frames"]:
        try:
            entry = process_frame(frame, size, out_dir, access_key)
            manifest.append(entry)
            print(f"wrote {entry['image']}  <-  {frame['query']!r}")
        except Exception as e:
            print(f"failed frame {frame.get('id')!r}: {e}", file=sys.stderr)
            return 1

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps({"frames": manifest}, indent=2, ensure_ascii=False))
    print(f"wrote {manifest_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
