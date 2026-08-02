#!/usr/bin/env python3
"""Generate NVIDIA-styled thumbnails for audio files using Unsplash imagery."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
import wave
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
UNSPLASH_SEARCH = "https://api.unsplash.com/search/photos"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# NVIDIA design tokens (from DESIGN.md)
GREEN = (118, 185, 0)
INK = (0, 0, 0)
WHITE = (255, 255, 255)
MUTE = (167, 167, 167)


def audio_duration_seconds(path: Path) -> float | None:
    try:
        with contextlib.closing(wave.open(str(path), "rb")) as w:
            frames = w.getnframes()
            rate = w.getframerate()
            return frames / float(rate) if rate else None
    except (wave.Error, FileNotFoundError):
        return None


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return ""
    m, s = divmod(int(round(seconds)), 60)
    return f"{m}:{s:02d}"


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
        raise RuntimeError(f"No Unsplash results for query: {query!r}")
    return results[0]


def trigger_download(photo: dict, access_key: str) -> None:
    # Per Unsplash API guidelines: ping the download_location endpoint.
    location = (photo.get("links") or {}).get("download_location")
    if not location:
        return
    with contextlib.suppress(requests.RequestException):
        requests.get(
            location,
            headers={"Authorization": f"Client-ID {access_key}"},
            timeout=15,
        )


def fetch_image(photo: dict, size: tuple[int, int]) -> Image.Image:
    url = (photo.get("urls") or {}).get("regular") or (photo.get("urls") or {}).get("full")
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


def bottom_gradient(size: tuple[int, int]) -> Image.Image:
    w, h = size
    grad = Image.new("L", (1, h), 0)
    for y in range(h):
        t = max(0.0, (y - h * 0.35) / (h * 0.65))
        grad.putpixel((0, y), int(255 * (t ** 1.6) * 0.85))
    alpha = grad.resize((w, h))
    overlay = Image.new("RGBA", (w, h), INK + (0,))
    overlay.putalpha(alpha)
    return overlay


def compose_thumbnail(
    photo_img: Image.Image,
    title: str,
    subtitle: str,
    size: tuple[int, int],
    credit: str,
) -> Image.Image:
    w, h = size
    canvas = photo_img.copy().convert("RGBA")
    canvas.alpha_composite(bottom_gradient((w, h)))

    draw = ImageDraw.Draw(canvas)

    # Green corner square (NVIDIA signature motif). 2px radius on the whole system, but
    # the corner-square is intentionally sharp — draw as a solid square.
    square = max(12, int(w * 0.015))
    pad = max(24, int(w * 0.03))
    draw.rectangle(
        [(pad, pad), (pad + square, pad + square)],
        fill=GREEN,
    )

    # Eyebrow badge: "AUDIO" pill in NVIDIA green.
    eyebrow_font = ImageFont.truetype(FONT_BOLD, max(14, int(h * 0.028)))
    eyebrow_text = "AUDIO"
    tb = draw.textbbox((0, 0), eyebrow_text, font=eyebrow_font)
    bx = pad + square + max(12, int(w * 0.012))
    by = pad + (square - (tb[3] - tb[1])) // 2 - tb[1]
    draw.text((bx, by), eyebrow_text, font=eyebrow_font, fill=GREEN)

    # Title — display-xl weight (48px scaled to canvas).
    title_font = ImageFont.truetype(FONT_BOLD, max(48, int(h * 0.12)))
    title_y = int(h * 0.62)
    draw.text((pad, title_y), title, font=title_font, fill=WHITE)

    # Subtitle — duration + optional caption.
    sub_font = ImageFont.truetype(FONT_BOLD, max(18, int(h * 0.035)))
    tb = draw.textbbox((0, 0), title, font=title_font)
    sub_y = title_y + (tb[3] - tb[1]) + max(8, int(h * 0.02))
    draw.text((pad, sub_y), subtitle, font=sub_font, fill=GREEN)

    # Credit line, bottom-right, muted.
    if credit:
        credit_font = ImageFont.truetype(FONT_REG, max(11, int(h * 0.02)))
        ctb = draw.textbbox((0, 0), credit, font=credit_font)
        cx = w - pad - (ctb[2] - ctb[0])
        cy = h - pad - (ctb[3] - ctb[1])
        draw.text((cx, cy), credit, font=credit_font, fill=MUTE)

    return canvas.convert("RGB")


def process_item(item: dict, size: tuple[int, int], out_dir: Path, access_key: str) -> Path:
    audio_name = item["audio"]
    audio_path = REPO_ROOT / audio_name
    query = item.get("query") or Path(audio_name).stem
    orientation = item.get("orientation", "landscape")
    title = item.get("title") or Path(audio_name).stem

    duration = audio_duration_seconds(audio_path)
    dur_str = format_duration(duration)
    subtitle = f"{dur_str} • {query}" if dur_str else query

    photo = search_unsplash(query, orientation, access_key)
    trigger_download(photo, access_key)
    photo_img = fetch_image(photo, size)

    author = ((photo.get("user") or {}).get("name")) or "Unsplash"
    credit = f"Photo: {author} / Unsplash"

    thumb = compose_thumbnail(photo_img, title, subtitle, size, credit)
    out_path = out_dir / f"{Path(audio_name).stem}.jpg"
    thumb.save(out_path, "JPEG", quality=88, optimize=True)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "scripts" / "thumbnails.json"),
        help="Path to thumbnails.json config",
    )
    args = parser.parse_args()

    access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not access_key:
        print("error: UNSPLASH_ACCESS_KEY is not set", file=sys.stderr)
        return 2

    config = json.loads(Path(args.config).read_text())
    size = tuple(config.get("size", [1280, 720]))
    out_dir = REPO_ROOT / config.get("output_dir", "thumbnails")
    out_dir.mkdir(parents=True, exist_ok=True)

    for item in config["items"]:
        try:
            path = process_item(item, size, out_dir, access_key)
            print(f"wrote {path.relative_to(REPO_ROOT)}")
        except Exception as e:
            print(f"failed {item.get('audio')!r}: {e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
