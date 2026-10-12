#!/usr/bin/env python3
"""One-shot production DTC interaction smoke test with moderated test comment.

Reads live page and WordPress queue. Leaves a clearly labeled test comment
pending for the site editor to delete. Never approves/publishes comments.
"""
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE = "https://a3tal.com"
PAGE = BASE + "/dtc/p0172/"
KEY = os.getenv("A3TAL_API_KEY", "")
if not KEY:
    raise SystemExit("Bridge key unavailable")


def http(url, params=None, bridge=False):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36",
        "Accept": "text/html,application/json;q=0.9,*/*;q=0.5",
        "Origin": BASE,
        "Referer": PAGE,
        "Cache-Control": "no-cache",
    }
    if bridge:
        headers["X-A3tal-Key"] = KEY
        headers["Authorization"] = "Bearer " + KEY
    body = None
    if params is not None:
        if bridge:
            headers["Content-Type"] = "application/json"
            body = json.dumps(params, ensure_ascii=False).encode("utf-8")
        else:
            headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            body = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=35) as res:
        return res.read().decode("utf-8")


def retry_read(url, bridge_payload=None):
    for n in range(3):
        try:
            return http(url, bridge_payload, bridge=bridge_payload is not None)
        except urllib.error.HTTPError as err:
            if err.code not in (403, 429, 502, 503, 504, 520, 522, 524) or n == 2:
                raise
            print("Read blocked transiently", err.code, "retrying", flush=True)
            time.sleep(12 * (n + 1))


def main():
    body = retry_read(PAGE + "?qa=" + uuid.uuid4().hex)
    if 'id="dtc-discussion"' not in body:
        raise RuntimeError("DTC discussion element is missing")
    match = re.search(r'<section[^>]*id="dtc-discussion"[^>]*data-post-id="(\d+)"', body)
    if not match:
        raise RuntimeError("Cannot extract WordPress discussion target")
    post_id = int(match.group(1))
    print("Discussion target", post_id, flush=True)

    for platform, required in {
        "WhatsApp": ("api.whatsapp.com/send?", "d-share-wa"),
        "Facebook": ("facebook.com/sharer/", "d-share-fb"),
        "X": ("twitter.com/intent/tweet?", "d-share-x"),
        "Copy": ("data-dtc-copy=", "d-share-copy"),
    }.items():
        if not all(part in body for part in required):
            raise RuntimeError("Missing share control: " + platform)
        print("Share control present:", platform, flush=True)

    first_page = re.search(r'<a[^>]+class="[^"]*d-share-wa[^"]*"[^>]+href="([^"]+)"', body)
    if not first_page:
        raise RuntimeError("WhatsApp share link is missing")
    share_href = html.unescape(first_page.group(1))
    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(share_href).query)
    shared_text = parsed.get("text", [""])[0]
    if "/dtc/p0172/" not in shared_text:
        print("QUALITY ISSUE: share buttons point to the original guide instead of the DTC detail URL", flush=True)
    else:
        print("Share destinations correctly use DTC code detail permalink", flush=True)

    visitor = uuid.uuid4().hex + "dtcsmoke"
    ajax = BASE + "/wp-admin/admin-ajax.php"
    # The WordPress handler intentionally reads submitted form fields from POST.
    raw_token = http(ajax, {"action": "a3g_dtc_token",
                            "post_id": str(post_id), "visitor": visitor})
    try:
        token = json.loads(raw_token)
    except json.JSONDecodeError:
        # Do not log response bodies other than tiny, non-sensitive diagnostics;
        # typical blocked-ajax responses are "0" or WAF HTML.
        print("Anonymous token endpoint returned non-JSON; length:", len(raw_token),
              "prefix:", repr(raw_token[:100]), flush=True)
        raise RuntimeError("Anonymous token endpoint returned non-JSON") from None
    if token.get("success") is not True:
        raise RuntimeError("Anonymous challenge endpoint failed")
    values = token.get("data", {})
    if not values.get("nonce") or not values.get("challenge"):
        raise RuntimeError("Anonymous challenge/nonce is missing")
    print("Anonymous token endpoint succeeded without a login", flush=True)
    time.sleep(3)

    marker = "A3TAL-DTC-QA-" + uuid.uuid4().hex[:10]
    comment = "اختبار تقني مؤقت لنظام تعليقات مكتبة أعطال، للمراجعة والحذف من لوحة ووردبريس. " + marker
    payload = {
        "action": "a3g_dtc_comment",
        "post_id": str(post_id),
        "visitor": visitor,
        "_ajax_nonce": values["nonce"],
        "challenge": values["challenge"],
        "alias": "اختبار تقني أعطال",
        "comment": comment,
        "comment_parent": "0",
        "website": "",
    }
    # Mutating form submission happens exactly once; do not blindly replay.
    response = json.loads(http(ajax, payload))
    if response.get("success") is not True:
        raise RuntimeError("Anonymous form returned error " +
                           str(response.get("data", {}).get("code", "unknown")))
    print("Anonymous comment accepted by AJAX; checking WordPress moderation queue", flush=True)
    time.sleep(4)

    listing = json.loads(retry_read(BASE + "/wp-json/a3tal-direct/v1/admin",
                                 {"op": "comments", "post_id": post_id,
                                  "status": "hold", "limit": 100}))
    if not listing.get("ok") or not isinstance(listing.get("result"), list):
        raise RuntimeError("WordPress moderation list unavailable")
    found = [c for c in listing["result"] if marker in c.get("content", "")]
    if len(found) != 1 or str(found[0].get("approved")) != "0":
        raise RuntimeError("Anonymous comment was not confirmed pending review")
    print("PASS: test comment", found[0]["id"], "is pending moderator approval; never publicly approved.", flush=True)
    print("TEST MARKER: " + marker, flush=True)
    print("QA COMPLETE: inspect/delete this test comment from WordPress > Comments", flush=True)


if __name__ == "__main__":
    main()
