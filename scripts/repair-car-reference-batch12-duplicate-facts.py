#!/usr/bin/env python3
"""Remove only redundant inline facts tables from Batch 12 reference specs.
The existing A3tal WordPress single.php already prints the exact same facts.
The only write API used is the authorized A3tal Direct Bridge post update.
"""
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://a3tal.com"
KEY = os.environ["A3TAL_API_KEY"]
LIMIT = int(os.environ.get("A3CR_REPAIR_LIMIT", "1"))
DATA = json.loads(Path("data/car-reference/batch-12-18-technical-references-20261104.json").read_text(encoding="utf8"))
SPECS = []
for group in DATA["clusters"]:
    for spec in group["specs"]:
        url = f"{BASE}/car-reference/{group['brand']}/{group['model']['slug']}/{spec['slug']}/"
        SPECS.append((spec, url))
assert len(SPECS) == 15
assert 1 <= LIMIT <= 15

INLINE = re.compile(
    r'<div\b(?=[^>]*class=["\x27]a3tal-responsive-table["\x27])[^>]*>\s*<table\b[^>]*>\s*<tbody\b[^>]*>.*?</tbody>\s*</table>\s*</div>',
    re.DOTALL | re.IGNORECASE,
)

def request(url, payload=None, authenticated=False):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf8")
    headers = {"User-Agent": "A3tal-Batch12-DuplicateFactsRepair/1.0", "Cache-Control": "no-cache"}
    if authenticated:
        headers["X-A3tal-Key"] = KEY
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method="POST" if data is not None else "GET", headers=headers)
    last = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=80) as resp:
                return resp.read().decode("utf8", errors="replace")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 504, 520, 522, 524):
                raise
            last = e
            if attempt < 4:
                time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Request retries exhausted: {url} {last}")

def read_public(spec):
    q = urllib.parse.urlencode({"slug": spec["slug"], "per_page": 10})
    records = json.loads(request(BASE + "/wp-json/wp/v2/car-reference-records?" + q))
    records = [r for r in records if r.get("slug") == spec["slug"] and r.get("status") == "publish"]
    if len(records) != 1:
        raise RuntimeError("Expected exactly one live record " + spec["slug"])
    return records[0]

def read_bridge(post_id):
    return json.loads(request(
        BASE + "/wp-json/a3tal-direct/v1/post/" + str(post_id),
        authenticated=True,
    ))

def verify_live(url, title, image):
    issue = ""
    for i in range(10):
        try:
            page = request(url + "?a3tal_facts_clean=" + str(time.time_ns()))
            if title not in html.unescape(page):
                raise ValueError("title missing")
            if page.count('class="a3cr-table"') != 1:
                raise ValueError("expected one default facts table")
            if "a3tal-responsive-table" in page:
                raise ValueError("old inline facts table still visible")
            canon = re.search(r'<link\b[^>]*rel=["\x27]canonical["\x27][^>]*>', page, re.I)
            if not canon or url.rstrip("/") not in html.unescape(canon.group(0)):
                raise ValueError("canonical changed")
            og = re.findall(r'<meta\b[^>]*property=["\x27]og:image["\x27][^>]*>', page, re.I)
            if not og or not any(image in html.unescape(tag) for tag in og):
                raise ValueError("featured OG image changed")
            if re.search(r'<meta\b[^>]*name=["\x27]robots["\x27][^>]*noindex', page, re.I):
                raise ValueError("unexpected noindex")
            return
        except Exception as e:
            issue = str(e)
            if i < 9:
                time.sleep(5)
    raise RuntimeError(f"Live page QC failed: {url}: {issue}")

for spec, url in SPECS[:LIMIT]:
    public = read_public(spec)
    assert public["link"].rstrip("/") == url.rstrip("/"), "unexpected URL"
    assert html.unescape(re.sub(r"<[^>]*>", "", public["title"]["rendered"])).strip() == spec["title"], "title changed"
    image_id = int(public.get("featured_media") or 0)
    assert image_id > 0, "featured image missing"
    image_info = (public.get("yoast_head_json") or {}).get("og_image") or []
    assert image_info and image_info[0].get("url"), "OG missing"
    image_url = image_info[0]["url"]
    item = read_bridge(public["id"])
    assert item["type"] == "a3_car_ref" and item["status"] == "publish", "wrong post type/status"
    assert item["slug"] == spec["slug"] and item["link"].rstrip("/") == url.rstrip("/"), "wrong bridge record"
    assert item["featured_media"] == image_id, "image IDs disagree"
    raw = item["content"]
    matches = list(INLINE.finditer(raw))
    if len(matches) == 1:
        found = matches[0]
        body = found.group(0)
        # Only delete a table verified to contain this page's exact sourced data values.
        for label, value in spec["facts"]:
            if html.escape(str(label)) not in body or html.escape(str(value)) not in body:
                raise RuntimeError("Facts in inline table diverged from reviewed source: " + spec["slug"])
        revised = raw[:found.start()] + raw[found.end():]
        assert revised and revised != raw and not INLINE.search(revised)
        result = json.loads(request(
            BASE + "/wp-json/a3tal-direct/v1/update-post",
            payload={
                "id": public["id"],
                "content": revised,
                "expected_modified_gmt": item["modified_gmt"],
            },
            authenticated=True,
        ))
        assert result["id"] == public["id"] and result["content"] == revised, "Bridge content differs"
        assert result["featured_media"] == image_id, "image changed"
        assert result["meta"] == item["meta"], "SEO metadata changed"
        print("UPDATED", spec["slug"], "id", public["id"], flush=True)
    elif len(matches) == 0 and 'a3tal-responsive-table' not in raw:
        print("ALREADY CLEAN", spec["slug"], "id", public["id"], flush=True)
    else:
        raise RuntimeError("Ambiguous/repeated inline facts tables: " + spec["slug"] + " excerpt=" + repr(raw[max(0, raw.find("a3tal-responsive-table")-100):raw.find("a3tal-responsive-table")+500]))
    now = read_bridge(public["id"])
    assert "a3tal-responsive-table" not in now["content"], "inline table still persisted"
    assert now["featured_media"] == image_id and now["meta"] == item["meta"], "post changed unexpectedly"
    verify_live(url, spec["title"], image_url)
    print("LIVE SINGLE FACTS TABLE VERIFIED", url, flush=True)

health = json.loads(request(BASE + "/wp-json/a3tal-car-reference/v1/health"))
assert health["ok"] and health["published"] == 108 and health["drafts"] == 0, health
print("SUCCESS", json.dumps({"processed": LIMIT, "total_specs_in_batch": len(SPECS),
                           "published": health["published"], "drafts": health["drafts"]}))
