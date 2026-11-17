#!/usr/bin/env python3
"""One-shot, revision-safe human editorial improvement for seven existing A3tal posts.

Reads the actual WordPress original via A3tal Direct Bridge on every run.
Never creates a new article, changes URL, canonical, thumbnail or schema.
Article authorship remains the real WordPress editorial team; expert biographies
are informative and do not falsely claim that a named engineer reviewed content.
"""
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

SITE = "https://a3tal.com"
API = SITE + "/wp-json/a3tal-direct/v1"
KEY = os.environ.get("A3TAL_API_KEY", "")
ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "data/seo-human-seven-20261117.json").read_text(encoding="utf-8"))
MARK = CONFIG["tag"]
if not KEY:
    raise SystemExit("A3TAL_API_KEY is not configured")
if len(CONFIG["cases"]) != 7 or len({c["id"] for c in CONFIG["cases"]}) != 7:
    raise SystemExit("Expected seven distinct existing posts")


def get_json(url, *, authorized=False, body=None, timeout=120):
    headers = {"Accept": "application/json", "User-Agent": "A3talEditorialSevenSafe/20261117",
               "Cache-Control": "no-cache"}
    if authorized:
        headers["X-A3tal-Key"] = KEY
        headers["Authorization"] = "Bearer " + KEY
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    if data is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def bridge_post(pid):
    return get_json(API + "/post/" + str(pid), authorized=True)


def public_post(pid):
    fields = "id,slug,status,link,featured_media,yoast_head_json,modified_gmt"
    return get_json(SITE + "/wp-json/wp/v2/posts/" + str(pid) + "?" +
                    urllib.parse.urlencode({"_fields": fields, "_a3tal_check": MARK}))


def canonicalize(url):
    u = urllib.parse.urlsplit(url)
    return u.scheme.lower() + "://" + u.netloc.lower() + urllib.parse.unquote(u.path).rstrip("/")


def slug_norm(slug):
    return urllib.parse.unquote(str(slug)).rstrip("/").lower()


def assert_original(case, original, public):
    pid = case["id"]
    if original.get("id") != pid or public.get("id") != pid:
        raise RuntimeError("ID changed for " + str(pid))
    if original.get("status") != "publish" or public.get("status") != "publish":
        raise RuntimeError("Not currently published: " + str(pid))
    if slug_norm(original.get("slug")) != slug_norm(case["slug"]):
        raise RuntimeError("Bridge slug mismatch: " + str(pid))
    if slug_norm(public.get("slug")) != slug_norm(case["slug"]):
        raise RuntimeError("Public slug mismatch: " + str(pid))
    if not original.get("featured_media") or original.get("featured_media") != public.get("featured_media"):
        raise RuntimeError("Cover changed or missing: " + str(pid))
    seo = public.get("yoast_head_json") or {}
    if (seo.get("robots") or {}).get("index") == "noindex":
        raise RuntimeError("Unexpected noindex: " + str(pid))
    if not seo.get("canonical") or canonicalize(seo["canonical"]) != canonicalize(public["link"]):
        raise RuntimeError("Unexpected canonical: " + str(pid))
    if not seo.get("og_image"):
        raise RuntimeError("Missing original og:image: " + str(pid))
    if len(original.get("content", "")) < 4500 or not original.get("modified_gmt"):
        raise RuntimeError("Source too short or missing revision: " + str(pid))
    if original["content"].lower().count("<h2") < 2:
        raise RuntimeError("Original article has unexpected structure: " + str(pid))
    return seo


def answer_box(case):
    q = html.escape(case["question"])
    a = html.escape(case["answer"])
    label = html.escape(case["label"])
    return (
        '\n<section class="a3tal-answer-first-seven" id="' + MARK + '-' + str(case["id"]) +
        '" dir="rtl" aria-label="إجابة مباشرة" style="margin:0 0 22px;padding:16px 18px;'
        'border-right:4px solid #145b79;background:#f5f9fc;border-radius:9px">'
        '<h2 style="font-size:1.18em;margin:0 0 9px;color:#123047">' + q + '</h2>'
        '<p style="margin:0 0 8px">' + a + '</p>'
        '<div class="a3tal-answer-practical" style="margin-top:10px">' +
        case["detail"] + '</div></section>\n'
    )


def author_card(case):
    name = html.escape(case["expert"])
    role = html.escape(case["role"])
    return (
        '\n<section class="a3tal-author-note" dir="rtl" aria-label="فريق إعداد المقال"'
        ' style="margin:24px 0;padding:17px;border:1px solid #d6e2eb;'
        'border-radius:9px;background:#fff">'
        '<h2 style="font-size:1.12em;margin:0 0 8px">عن إعداد هذا المقال</h2>'
        '<p style="margin:0 0 9px"><strong>إعداد: فريق تحرير أعطال.كوم.</strong> '
        'نقدم معلومات تساعد مالك العربية على فهم الخدمة أو المشكلة،'
        ' مع الرجوع للمصادر الفنية والرسمية الموضحة داخل المقال.</p>'
        '<p style="margin:0"><strong>من الخبراء المتخصصين في فريق الموقع: '
        + name + '.</strong> ' + role + '</p></section>\n'
    )


def remove_visible_css_clutch(original):
    # The old clutch post contains stylesheet source literally printed to visitors,
    # NOT an actual <style> tag. Remove ONLY the known visibly broken paragraph.
    pattern = (r'<p>\s*body\s*\{\s*font-family:.*?'
               r'\.highlight\s*\{\s*font-weight:\s*bold;.*?\}\s*</p>')
    patched, count = re.subn(pattern, "", original, count=1, flags=re.I | re.S)
    if count != 1 or "body { font-family:" in patched[:1000]:
        raise RuntimeError("Clutch printed CSS did not match the reviewed original")
    return patched


def insert_answer(original, case):
    pid = case["id"]
    block = answer_box(case)
    if pid == 80056:
        original = remove_visible_css_clutch(original)
        marker = '<div class="a3tal-intro">'
        if original.count(marker) != 1:
            raise RuntimeError("Clutch content structure changed")
        return original.replace(marker, block + marker, 1)
    if pid in (79964, 80401, 80534):
        # Root article tag. Keep existing quick hotline boxes and internal links.
        match = re.search(r"<article\b[^>]*>", original, flags=re.I)
        if not match or match.start() > 950:
            raise RuntimeError("Expected root article was not found: " + str(pid))
        return original[:match.end()] + block + original[match.end():]
    if pid == 80266:
        marker = '<div class="a3tal-tire-prices-2027"'
        match = re.search(re.escape(marker) + r"[^>]*>", original)
        if not match:
            raise RuntimeError("Tires original layout changed")
        return original[:match.end()] + block + original[match.end():]
    if pid == 80669:
        match = re.search(r'<div\s+style="direction:\s*rtl;[^"]*">', original)
        if not match or match.start() > 500:
            raise RuntimeError("Skoda original layout changed")
        return original[:match.end()] + block + original[match.end():]
    if pid == 79:
        article = re.search(r'<article\b[^>]*>', original, flags=re.I)
        if article and article.start() < 800:
            return original[:article.end()] + block + original[article.end():]
        container = re.search(r'<div\b[^>]*class="[^"]*a3tal[^"]*"[^>]*>', original, flags=re.I)
        if container and container.start() < 1100:
            return original[:container.end()] + block + original[container.end():]
        # A plain legacy article with no container: place before its first body paragraph.
        match = re.search(r'<p\b[^>]*>', original, flags=re.I)
        if match and match.start() < 450:
            return original[:match.start()] + block + original[match.start():]
        raise RuntimeError("Unrecognized vibration page structure")
    raise RuntimeError("Unapproved post ID for insertion")


def build_content(case, old):
    pid = case["id"]
    if MARK + "-" + str(pid) in old:
        return None
    result = insert_answer(old, case)
    card = author_card(case)
    closing = result.lower().rfind("</article>")
    if closing < 0:
        closing = result.lower().rfind("</div>")
    if closing < 0:
        raise RuntimeError("Missing outer wrapper to append author note")
    result = result[:closing] + card + result[closing:]
    if result.count('id="' + MARK + "-" + str(pid) + '"') != 1:
        raise RuntimeError("Duplicate or missing update marker")
    if result.count('class="a3tal-author-note"') != 1:
        raise RuntimeError("Author section did not insert")
    if result.count("<img") != old.count("<img"):
        raise RuntimeError("Inline image count changed")
    if result.count("<a ") < old.count("<a "):
        raise RuntimeError("Existing internal or external links dropped")
    if len(result) < len(old) - 1600:
        raise RuntimeError("Unexpected content loss")
    if len(case["meta"]) < 65 or len(case["meta"]) > 220:
        raise RuntimeError("Unreviewed meta description length")
    return result


def update(case, before, old_seo, new_content):
    pid = case["id"]
    latest = bridge_post(pid)
    if latest.get("modified_gmt") != before["modified_gmt"] or latest.get("content") != before["content"]:
        raise RuntimeError("Concurrent WordPress edit detected: " + str(pid))
    payload = {
        "id": pid,
        "expected_modified_gmt": latest["modified_gmt"],
        "content": new_content,
        "meta": {"_yoast_wpseo_metadesc": case["meta"]},
    }
    response = get_json(API + "/update-post", authorized=True, body=payload, timeout=160)
    if response.get("error") or response.get("ok") is False:
        raise RuntimeError("Bridge declined update: " + str(pid))
    after = bridge_post(pid)
    if MARK + "-" + str(pid) not in after.get("content", ""):
        raise RuntimeError("Live update marker absent: " + str(pid))
    if (after.get("slug"), after.get("status"), after.get("featured_media")) != (
            before.get("slug"), "publish", before.get("featured_media")):
        raise RuntimeError("Slug/status/featured image changed: " + str(pid))
    if after["content"].count('class="a3tal-author-note"') != 1:
        raise RuntimeError("Published author bio absent: " + str(pid))
    if after["content"].count("<img") != before["content"].count("<img"):
        raise RuntimeError("Published inline image count changed: " + str(pid))
    for attempt in range(4):
        pp = public_post(pid)
        so = pp.get("yoast_head_json") or {}
        if so.get("description") == case["meta"]:
            if canonicalize(so.get("canonical", "")) != canonicalize(old_seo.get("canonical", "")):
                raise RuntimeError("Canonical changed in public HTML: " + str(pid))
            if pp.get("featured_media") != before.get("featured_media"):
                raise RuntimeError("Public image changed: " + str(pid))
            if (so.get("robots") or {}).get("index") == "noindex":
                raise RuntimeError("New noindex appeared: " + str(pid))
            before_og = (old_seo.get("og_image") or [{}])[0].get("url")
            after_og = (so.get("og_image") or [{}])[0].get("url")
            if before_og != after_og:
                raise RuntimeError("og:image changed: " + str(pid))
            print("A3TAL_SEVEN_PUBLISHED_AND_CHECKED", pid, pp.get("link"), flush=True)
            return
        time.sleep(3)
    raise RuntimeError("Yoast meta verification failed: " + str(pid))


def main():
    plans = []
    for case in CONFIG["cases"]:
        original, public = bridge_post(case["id"]), public_post(case["id"])
        seo = assert_original(case, original, public)
        revised = build_content(case, original["content"])
        if revised is None:
            print("ALREADY_UPDATED", case["id"], public.get("link"), flush=True)
            continue
        plans.append((case, original, seo, revised))
        print("PREFLIGHT_OK", case["id"], len(original["content"]), len(revised), flush=True)
    print("SEVEN_PREFLIGHTS_COMPLETE", len(plans), flush=True)
    for case, original, seo, revised in plans:
        update(case, original, seo, revised)
    print("A3TAL_SEVEN_UPDATES_VERIFIED", flush=True)


if __name__ == "__main__":
    main()
