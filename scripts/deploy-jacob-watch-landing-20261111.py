#!/usr/bin/env python3
"""Deploy one isolated luxury-watch WordPress page using A3tal Direct Bridge.
No automotive theme, homepage, or menu changes.
"""
from __future__ import annotations

import base64
import io
import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "watch-offer"
TEMPLATE = ROOT / "theme-source" / "a3tal-global" / "page-jacob-watch-offer.php"
REPORT = ROOT / "reports" / "watch-offer" / "publish-qa.json"
BASE = "https://a3tal.com/wp-json/a3tal-direct/v1"
SLUG = "jacob-co-watch-offer"
KEY = os.environ.get("A3TAL_API_KEY", "").strip()
if not KEY:
    raise SystemExit("Missing A3TAL_API_KEY secret")

S = requests.Session()
S.headers.update({
    "X-A3tal-Key": KEY, "Authorization": f"Bearer {KEY}",
    "User-Agent": "A3talWatchLandingDeploy/1.0",
})
MEDIA = {
    "hero": ("watch-premium-hero-master.png", "watch-skeleton-premium-design-20261111.webp",
             "صورة دعائية فنية توضيحية للتصميمين"),
    "steel": ("watch-studio-two-variants-master.png", "watch-oil-pump-inspired-steel-studio-20261111.webp",
              "صورة ستوديو توضيحية للساعة الفضية"),
    "gold": ("watch-studio-two-variants-master.png", "watch-opera-inspired-rose-gold-studio-20261111.webp",
             "صورة ستوديو توضيحية للساعة الذهبية"),
    "box": ("watch-box-original.jpg", "watch-original-wooden-presentation-box-20261111.webp",
            "صورة فعلية للبوكس الخشبي"),
}
TITLE = "ساعة جاكوب اند كو هاي كوبي في مصر | السعر والصور والفيديو"
META = {
    "_yoast_wpseo_title": "ساعة جاكوب اند كو هاي كوبي في مصر | سعر 24,000 جنيه",
    "_yoast_wpseo_metadesc": "ساعة جاكوب اند كو هاي كوبي في مصر بتصميمي Oil Pump وOpera Godfather. صور احترافية و3 فيديوهات حقيقية، بسعر 24,000 جنيه والكمية 6 قطع فقط. للحجز 01025036151.",
    "_yoast_wpseo_focuskw": "ساعة جاكوب اند كو هاي كوبي",
}

def api(method: str, path: str, *, params=None, data=None, timeout=150):
    response = S.request(method, BASE + path, params=params, json=data, timeout=timeout)
    try:
        payload = response.json()
    except Exception:
        raise RuntimeError(f"Bridge {method} {path}: unexpected HTTP {response.status_code}: "
                           f"{response.text[:220]}")
    if not response.ok or (isinstance(payload, dict) and payload.get("ok") is False):
        raise RuntimeError(f"Bridge {method} {path}: HTTP {response.status_code}: "
                           f"{str(payload)[:700]}")
    return payload

def admin_read(op: str, **params):
    result = api("GET", "/admin", params={"op": op, **params})
    return result.get("result", result)

def admin_write(op: str, **params):
    result = api("POST", "/admin", data={"op": op, "confirm": True, **params})
    if result.get("ok") is False:
        raise RuntimeError(f"Admin {op} returned failure")
    return result.get("result", result)

def optimized_image(filename: str, key: str):
    path = ASSETS / filename
    if not path.is_file():
        raise FileNotFoundError(f"Missing source image: {path}")
    with Image.open(path) as source:
        photo = source.convert("RGB")
        if key == "hero":
            photo.thumbnail((1600, 1080), resample=Image.Resampling.LANCZOS)
        elif key in ("steel", "gold"):
            w, h = photo.size
            if key == "steel":
                photo = photo.crop((0, 0, int(w * 0.492), h))
            else:
                photo = photo.crop((int(w * 0.508), 0, w, h))
            photo.thumbnail((900, 1200), resample=Image.Resampling.LANCZOS)
        else:
            photo = ImageOps.fit(photo, (1000, 1000), method=Image.Resampling.LANCZOS)
        output = io.BytesIO()
        photo.save(output, "WEBP", quality=88, method=6)
        return output.getvalue()

def find_page():
    res = api("GET", "/search-posts", params={"search": "Jacob & Co", "status": "any", "limit": 90})
    items = res.get("items", [])
    exact = [p for p in items if p.get("slug") == SLUG]
    if len(exact) > 1:
        raise RuntimeError(f"More than one existing page for slug {SLUG}")
    return exact[0] if exact else None

def main():
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {"slug": SLUG, "price_egp": 24000, "stock_quantity": 6, "phone": "01025036151"}
    try:
        active_theme = admin_read("site_info").get("active_theme")
        assert active_theme == "a3tal-global", f"Unexpected active theme {active_theme!r}"
        report["active_theme"] = active_theme

        # Apply the one new template, without touching shared theme files or menus.
        live_path = "themes/a3tal-global/page-jacob-watch-offer.php"
        body = {"path": live_path, "content": TEMPLATE.read_text(encoding="utf-8"),
                "dangerous": True}
        try:
            original = admin_read("file_read", path=live_path)
            if original.get("sha256"):
                body["expected_sha256"] = original["sha256"]
        except RuntimeError as exc:
            if "404" not in str(exc) and "file_missing" not in str(exc):
                raise
        saved = admin_write("file_write", **body)
        report["template_sha256"] = saved.get("sha256")
        print("WATCH_TEMPLATE_DEPLOYED", live_path, flush=True)

        match = find_page()
        if match:
            page_id = match["id"]
            prior = api("GET", f"/post/{page_id}")
            assert prior.get("type") == "page", "Existing item is not a page"
            # Refuse to overwrite any unrelated post with a coincidental slug.
            existing_template = admin_read("post_meta", post_id=page_id,
                                           key="_wp_page_template")
            cur = existing_template.get("_wp_page_template", "")
            if cur not in ("", "default", "page-jacob-watch-offer.php"):
                raise RuntimeError(f"Conflicting page template: {cur}")
            print("EXISTING_PAGE", page_id, flush=True)
        else:
            created = api("POST", "/create-post", data={
                "type": "page", "title": TITLE, "slug": SLUG,
                "status": "draft",
                "content": "<p>صفحة عرض ساعات بتصميم مستوحى من Jacob & Co.</p>",
                "meta": META,
            })
            page_id = int(created["id"])
            print("DRAFT_PAGE_CREATED", page_id, flush=True)

        urls = {}
        for name, (source_name, dest_name, alt) in MEDIA.items():
            raw = optimized_image(source_name, name)
            media = api("POST", "/upload-image-data", timeout=220, data={
                "post_id": page_id, "filename": dest_name, "title": alt, "alt": alt,
                "image_base64": base64.b64encode(raw).decode("ascii"),
                "convert_webp": False,
                "set_featured": name == "hero",
            })
            url = str(media["url"])
            assert url.startswith("https://a3tal.com/"), url
            urls[name] = url
            report[f"{name}_image"] = {"url": url, "media_id": media["media_id"],
                                       "bytes": len(raw)}
            print("PRODUCT_PHOTO_UPLOADED", name, media["media_id"], flush=True)

        admin_write("post_meta_set", post_id=page_id, meta={
            "_wp_page_template": "page-jacob-watch-offer.php",
            "_a3tal_watch_gallery": urls,
        })
        updated = api("POST", "/update-post", data={
            "id": page_id, "title": TITLE, "slug": SLUG,
            "content": "<p>صفحة عرض ساعات بتصميم مستوحى من Jacob & Co.</p>",
            "status": "publish", "meta": META,
        })
        assert updated.get("status") == "publish", updated
        page_url = str(updated.get("link", ""))
        assert page_url.startswith("https://a3tal.com/"), page_url
        report["page_id"] = page_id
        report["url"] = page_url

        # Live QA: actual page must show the custom landing, contact and images.
        import time
        checks = {}
        for attempt in range(5):
            res = requests.get(page_url, timeout=35,
                               headers={"User-Agent": "Mozilla/5.0"})
            body = res.text
            checks = {
                "http_200": res.status_code == 200,
                "landing_template": 'a3tal-watch-landing' in body,
                "price_24000": '24,000' in body,
                "stock_six": '6 قطع' in body,
                "phone": '01025036151' in body,
                "silver_image": urls["steel"] in body,
                "gold_image": urls["gold"] in body,
                "box_image": urls["box"] in body,
                "contact_whatsapp": 'wa.me/201025036151' in body,
                "mobile_style": "@media(max-width:720px)" in body,
            }
            if all(checks.values()):
                break
            time.sleep(5)
        report["public_qa"] = checks
        if not all(checks.values()):
            raise RuntimeError("Public QA missing: " + ", ".join(k for k, v in checks.items() if not v))
        print("WATCH_LANDING_LIVE_VERIFIED", page_url, flush=True)
        print("PUBLIC_QA", json.dumps(checks, ensure_ascii=False), flush=True)
    except Exception as exc:
        report["error"] = str(exc)
        raise
    finally:
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                          encoding="utf-8")
if __name__ == "__main__":
    main()
