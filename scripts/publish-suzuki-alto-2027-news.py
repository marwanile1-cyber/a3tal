#!/usr/bin/env python3
"""Publish a verified Arabic price report on a3tal.com using the existing Direct Bridge.

Images are real licensed Wikimedia Commons photos of the modern Alto K10,
credited inline. Post remains draft until featured and inline media are verified.
No paid app or WPWriter post credit is used.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = "https://a3tal.com/wp-json/a3tal-direct/v1"
KEY = os.environ.get("A3TAL_API_KEY", "")
STORY = json.loads(Path("data/news-suzuki-alto-2027-egypt.json").read_text(encoding="utf-8"))
LAST = 0
if not KEY:
    raise SystemExit("A3TAL_API_KEY GitHub secret is missing")


def pause():
    global LAST
    seconds = max(0, 23 - (time.monotonic() - LAST))
    if seconds:
        time.sleep(seconds)
    LAST = time.monotonic()


def bridge(path, data=None, *, retries=3):
    query = json.dumps(data, ensure_ascii=False).encode("utf-8") if data is not None else None
    header = {
        "X-A3tal-Key": KEY,
        "Authorization": "Bearer " + KEY,
        "User-Agent": "A3tal-Content-Publisher/2.0 (https://a3tal.com)",
        "Accept": "application/json",
        "Cache-Control": "no-store",
    }
    if query is not None:
        header["Content-Type"] = "application/json"
    for attempt in range(retries if data is None else 1):
        pause()
        req = urllib.request.Request(ROOT + path, data=query, headers=header)
        try:
            with urllib.request.urlopen(req, timeout=80) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if data is None and exc.code in (429, 502, 503, 504, 520, 522, 524) and attempt < retries - 1:
                print("Transient GET:", exc.code, "waiting...", flush=True)
                time.sleep(32 * (attempt + 1))
                continue
            raise RuntimeError(f"Bridge {path} returned HTTP {exc.code}") from None
        except (TimeoutError, urllib.error.URLError) as exc:
            if data is None and attempt < retries - 1:
                time.sleep(30 * (attempt + 1))
                continue
            raise RuntimeError(f"Bridge {path} interrupted: {type(exc).__name__}") from None


def lookup():
    params = urllib.parse.urlencode({"search": "سوزوكي ألتو 2027", "limit": 60})
    matches = bridge("/search-posts?" + params)["items"]
    selected = [item for item in matches if item["slug"] == STORY["slug"]]
    if len(selected) > 1:
        raise RuntimeError("Multiple posts have matching canonical slug; refusing edits")
    return selected[0] if selected else None


def ensure_post():
    item = lookup()
    if item:
        print("Found existing article:", item["id"], item["status"], flush=True)
        return item["id"]
    payload = {
        "title": STORY["title"], "type": "post", "slug": STORY["slug"],
        "content": STORY["content"], "excerpt": STORY["excerpt"],
        "status": "draft", "categories": STORY["categories"], "tags": STORY["tags"],
        "meta": {
            "_yoast_wpseo_title": STORY["seo_title"],
            "_yoast_wpseo_metadesc": STORY["meta_description"],
            "_yoast_wpseo_focuskw": STORY["focus_keyword"],
        },
    }
    try:
        created = bridge("/create-post", payload)
        print("Created draft:", created["id"], flush=True)
        return created["id"]
    except RuntimeError:
        # A failed HTTP response to a POST is ambiguous. Resolve remotely,
        # don't replay blindly, to avoid duplicate news posts.
        for i in range(4):
            time.sleep(40 * (i + 1))
            existing = lookup()
            if existing:
                print("Recovered created article from search:", existing["id"], flush=True)
                return existing["id"]
        raise


def fetch_wikimedia(name):
    file_key = name.replace(" ", "_")
    thumb = hashlib.md5(file_key.encode("utf-8")).hexdigest()
    quoted = urllib.parse.quote(file_key)
    urls = [
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/{thumb[0]}/{thumb[:2]}/{quoted}/1200px-{quoted}",
        "https://commons.wikimedia.org/wiki/Special:Redirect/file/" + quoted + "?width=1200",
    ]
    for url in urls:
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={
                    "User-Agent": "A3talCarNews/1.0 (editorial; https://a3tal.com/)",
                    "Accept": "image/jpeg,image/webp,*/*",
                })
                with urllib.request.urlopen(req, timeout=55) as resp:
                    data = resp.read()
                if len(data) < 10_000 or len(data) > 12_000_000 or data[:2] != b"\xff\xd8":
                    raise RuntimeError(f"Unexpected remote photo data length/type: {len(data)}")
                print("Licensed Wikimedia image downloaded:", name, len(data), flush=True)
                return data
            except Exception as err:
                print("Licensed photo fetch retry", name, attempt+1, type(err).__name__, flush=True)
                time.sleep(7 * (attempt + 1))
    raise RuntimeError("Unable to retrieve verified licensed photo: " + name)


def upload_image(image, post_id):
    jpeg = fetch_wikimedia(image["file"])
    payload = {
        "post_id": post_id, "title": image["alt"],
        "filename": image["name"].replace(".webp", ".jpg"),
        "image_base64": base64.b64encode(jpeg).decode("ascii"),
        "convert_webp": True, "max_width": 1200, "max_height": 850,
        "quality": 82, "alt": image["alt"],
        "caption": "الصورة: Vis M / Wikimedia Commons، ترخيص CC BY-SA 4.0",
        "set_featured": image["role"] == "featured",
    }
    # Mutation is deliberately attempted once. Lost response may have created media:
    # stop rather than blindly duplicating uploads.
    result = bridge("/upload-image-data", payload)
    print("MEDIA UPLOADED:", image["role"], result["media_id"], result["url"], flush=True)
    if result["mime"] != "image/webp":
        print("INFO: Server image editor did not convert to WebP; file remains a valid image", flush=True)
    return result


def publish():
    post_id = ensure_post()
    current = bridge(f"/post/{post_id}")
    if current["status"] == "publish" and current["featured_media"] and \
       "{{A3TAL_ALTO_IMAGE_SIDE}}" not in current["content"] and \
       "/wp-content/uploads/" in current["content"]:
        print("ALREADY COMPLETE:", current["link"], "featured=", current["featured_media"], flush=True)
        return
    images = STORY["image_files"]
    # A resumed partial run will reuse a previously set featured attachment.
    feat = current["featured_media"] or 0
    if not feat:
        feat = upload_image(images[0], post_id)["media_id"]
    else:
        print("Reusing existing featured image:", feat, flush=True)
    # Do not use the same image for a side angle; obtain unique licensed photo.
    if "{{A3TAL_ALTO_IMAGE_SIDE}}" in current["content"]:
        inline = upload_image(images[1], post_id)
        content = current["content"].replace(
            "{{A3TAL_ALTO_IMAGE_SIDE}}",
            '<figure class="wp-block-image size-full"><img src="' + inline["url"] +
            '" alt="' + images[1]["alt"] +
            '" loading="lazy" decoding="async"><figcaption>سوزوكي ألتو K10 - تصوير Vis M، CC BY-SA 4.0 (صورة إرشادية للشكل)</figcaption></figure>',
        )
    else:
        content = current["content"]
    if not feat or "{{A3TAL_ALTO_IMAGE_SIDE}}" in content:
        raise RuntimeError("Missing featured or inline photo; article must remain draft")
    updated = bridge("/update-post", {
        "id": post_id, "content": content, "title": STORY["title"],
        "excerpt": STORY["excerpt"], "slug": STORY["slug"],
        "status": "publish", "featured_media": int(feat),
        "categories": STORY["categories"],
        "meta": {
            "_yoast_wpseo_title": STORY["seo_title"],
            "_yoast_wpseo_metadesc": STORY["meta_description"],
            "_yoast_wpseo_focuskw": STORY["focus_keyword"],
        },
    })
    if updated["status"] != "publish" or not updated["featured_media"]:
        raise RuntimeError("Article not confirmed published with a featured image")
    print("SUCCESS:", updated["link"], "ID=",post_id, "featured=",updated["featured_media"], flush=True)
    time.sleep(22)
    checked = bridge(f"/post/{post_id}")
    if checked["status"] != "publish" or checked["featured_media"] != feat or \
       "{{A3TAL_ALTO_IMAGE_SIDE}}" in checked["content"] or \
       "<figure" not in checked["content"]:
        raise RuntimeError("Post readback failed after publishing")
    print("READBACK PASS: post is published, featured media set, inline photo present", flush=True)


if __name__ == "__main__":
    publish()
