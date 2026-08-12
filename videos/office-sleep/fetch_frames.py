#!/usr/bin/env python3
"""Fetch Unsplash backgrounds for office-sleep video, per frames.json."""
from __future__ import annotations
import argparse, contextlib, io, json, os, sys, time
from pathlib import Path
import requests
from PIL import Image

REPO_ROOT = Path("/home/user/First")
UNSPLASH_SEARCH = "https://api.unsplash.com/search/photos"

def search_unsplash(query, orientation, access_key):
    r = requests.get(
        UNSPLASH_SEARCH,
        params={"query": query, "orientation": orientation, "per_page": 5},
        headers={"Accept-Version": "v1", "Authorization": f"Client-ID {access_key}"},
        timeout=30,
    )
    r.raise_for_status()
    results = r.json().get("results") or []
    if not results:
        raise RuntimeError(f"no results: {query!r}")
    return results[0]

def trigger_download(photo, access_key):
    location = (photo.get("links") or {}).get("download_location")
    if not location: return
    with contextlib.suppress(requests.RequestException):
        requests.get(location, headers={"Authorization": f"Client-ID {access_key}"}, timeout=15)

def fetch_and_fit(photo, size):
    urls = photo.get("urls") or {}
    url = urls.get("full") or urls.get("regular")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    tw, th = size
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    resized = img.resize((int(sw*scale), int(sh*scale)), Image.LANCZOS)
    x0 = (resized.width - tw) // 2
    y0 = (resized.height - th) // 2
    return resized.crop((x0, y0, x0+tw, y0+th))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(REPO_ROOT/"videos/office-sleep/frames.json"))
    parser.add_argument("--skip-existing", action="store_true", default=True)
    args = parser.parse_args()

    ak = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not ak:
        print("UNSPLASH_ACCESS_KEY not set", file=sys.stderr); return 2

    cfg = json.loads(Path(args.config).read_text())
    size = tuple(cfg.get("image_size", [1920, 1080]))
    out_dir = REPO_ROOT / cfg["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    manifest_path = out_dir / "manifest.json"
    existing = {}
    if manifest_path.exists():
        for e in json.loads(manifest_path.read_text()).get("frames", []):
            existing[e["id"]] = e

    for i, frame in enumerate(cfg["frames"]):
        fid = frame["id"]
        query = frame["query"]
        out_path = out_dir / f"{fid}.jpg"
        if args.skip_existing and out_path.exists() and fid in existing:
            print(f"  skip {fid} (exists)")
            manifest.append(existing[fid])
            continue
        try:
            photo = search_unsplash(query, frame.get("orientation", "landscape"), ak)
            trigger_download(photo, ak)
            img = fetch_and_fit(photo, size)
            img.save(out_path, "JPEG", quality=88, optimize=True)
            user = photo.get("user") or {}
            entry = {
                "id": fid,
                "paragraphs": frame.get("paragraphs"),
                "query": query,
                "image": str(out_path.relative_to(REPO_ROOT)),
                "photographer": user.get("name"),
                "photographer_url": (user.get("links") or {}).get("html"),
                "photo_url": (photo.get("links") or {}).get("html"),
                "unsplash_id": photo.get("id"),
            }
            manifest.append(entry)
            print(f"  [{i+1:2d}/{len(cfg['frames'])}] {fid}  <-  {query!r}")
        except Exception as e:
            print(f"  FAILED {fid}: {e}", file=sys.stderr)
            # Save partial manifest and exit so we can retry
            manifest_path.write_text(json.dumps({"frames": manifest}, ensure_ascii=False, indent=2))
            return 1
        # Rate limit: Unsplash free = 50/hr. Add small delay.
        time.sleep(0.2)

    manifest_path.write_text(json.dumps({"frames": manifest}, ensure_ascii=False, indent=2))
    print(f"wrote {manifest_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
