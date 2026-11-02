#!/usr/bin/env python3
"""Replace only the 5 approved Kia featured images using A3tal Direct Bridge.

Requires incoming/a3tal-kia-image-replacements.zip with exactly 5 named WebP
files. This script never edits post content, URLs or SEO metadata directly.
"""
import base64
import io
import json
import os
import sys
import time
import zipfile
from pathlib import Path
import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "incoming" / "a3tal-kia-image-replacements.zip"
WP = "https://a3tal.com"
BRIDGE = WP + "/wp-json/a3tal-direct/v1"
API_KEY = os.environ["A3TAL_API_KEY"].strip()
HEADERS = {"X-A3tal-Key": API_KEY, "Content-Type": "application/json"}
MAP = {
    "kia.webp": ("kia", "دليل المواصفات الفنية لسيارات كيا"),
    "cerato-bd-2023.webp": ("cerato-bd-2023", "دليل مواصفات كيا سيراتو 2023 BD"),
    "seltos-sp2-2023.webp": ("seltos-sp2-2023", "دليل مواصفات كيا سيلتوس 2023 SP2"),
    "sportage-nq5-2023.webp": ("sportage-nq5-2023", "دليل مواصفات كيا سبورتاج 2023 NQ5"),
    "cerato-engine-oil-16-mpi.webp": ("engine-oil-16-mpi", "كمية زيت سيراتو 2023 محرك 1.6 MPI"),
}
session = requests.Session()
session.headers.update({"User-Agent": "A3tal-Kia-Featured-Replacement/1.0"})
results = []


def fetch_json(url, params=None):
    r = session.get(url, params=params, timeout=50, headers={"Cache-Control": "no-cache"})
    r.raise_for_status()
    return r.json()


def post(path, payload):
    r = session.post(BRIDGE + path, json=payload, headers=HEADERS, timeout=130)
    if not r.ok:
        raise RuntimeError("Bridge rejected " + path + " HTTP " + str(r.status_code) + ": " + r.text[:260])
    return r.json()


def record(slug):
    posts = fetch_json(WP + "/wp-json/wp/v2/car-reference-records", {"slug": slug, "per_page": 20})
    posts = [p for p in posts if p.get("slug") == slug and p.get("status") == "publish"]
    if len(posts) != 1:
        raise RuntimeError(f"Expected one live record for {slug}, found {len(posts)}")
    return posts[0]


def verify_image(raw, name):
    if len(raw) < 25_000:
        raise RuntimeError(f"Suspiciously small image {name}")
    image = Image.open(io.BytesIO(raw))
    image.verify()
    image = Image.open(io.BytesIO(raw))
    if image.format != "WEBP" or image.width < 1000 or image.height < 560:
        raise RuntimeError("Expected WebP >= 1000x560 " + name)


def check_page(item, filename):
    url = item["link"]
    for attempt in range(6):
        r = session.get(url, timeout=55, params={"a3cr_visual_review": str(int(time.time()))})
        if not r.ok:
            time.sleep(3)
            continue
        html = r.text.lower()
        expected = filename.lower()
        # Yoast meta and the actual get_post_thumbnail() should reference new image.
        if expected in html and 'og:image' in html and f'property="og:image"' in html:
            return True
        time.sleep(5)
    return False


def main():
    if not BUNDLE.is_file():
        raise SystemExit("Missing reviewed ZIP at " + str(BUNDLE))
    with zipfile.ZipFile(BUNDLE) as archive:
        names = archive.namelist()
        if sorted(names) != sorted(MAP):
            raise SystemExit("Expected exactly the five image filenames: " + ", ".join(MAP))
        data = {name: archive.read(name) for name in names}
    for name, raw in data.items():
        verify_image(raw, name)

    # Preflight every WordPress target and preserve the original featured ids.
    pages = {}
    for name, (slug, _) in MAP.items():
        p = record(slug)
        if not p.get("link", "").startswith(WP + "/car-reference/kia/"):
            raise RuntimeError("Unexpected URL for " + slug)
        pages[name] = p
        print("Preflight", name, "post", p["id"], "current featured", p["featured_media"], flush=True)
    print("Five verified targets. Updating only featured attachments.", flush=True)

    try:
        for name, (slug, alt) in MAP.items():
            page = pages[name]
            media = post("/upload-image-data", {
                "post_id": page["id"],
                "filename": "a3tal-kia-2026-new-" + name,
                "image_base64": base64.b64encode(data[name]).decode("ascii"),
                "convert_webp": False,
                "title": alt,
                "alt": alt
            })
            new_media = int(media.get("media_id") or 0)
            if not new_media or not str(media.get("url", "")).endswith(".webp"):
                raise RuntimeError("Media upload returned no valid WebP id for " + name)
            answer = post("/set-featured-image", {"post_id": page["id"], "media_id": new_media})
            if int(answer.get("featured_media", 0)) != new_media:
                raise RuntimeError("Featured attachment mismatch for " + name)
            updated = record(slug)
            if int(updated.get("featured_media", 0)) != new_media:
                raise RuntimeError("REST post featured mismatch for " + name)
            verified = check_page(updated, "a3tal-kia-2026-new-" + name)
            if not verified:
                raise RuntimeError("OG/image HTML verification failed for " + updated["link"])
            entry = {"post_id": page["id"], "url": page["link"], "new_featured_id": new_media, "old_featured_id": page["featured_media"], "image": media.get("url"), "verified": True}
            results.append(entry)
            print("REPLACED VERIFIED", entry["url"], "media", new_media, flush=True)
    finally:
        (ROOT / "a3tal-kia-images-replacement-report.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    assert len(results) == 5
    print("SUCCESS: all five existing pages use the new image + og:image", flush=True)


if __name__ == "__main__":
    main()
