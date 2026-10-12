#!/usr/bin/env python3
"""Correct only El Dawly Zagazig article contact details via authenticated A3tal Bridge.

Never log API credentials, private response bodies, or entire article text.
The update is idempotent and preserves all metadata, slug and featured media.
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://a3tal.com"
POST_ID = 83472
SLUG = "el-dawly-car-service-zagazig"
OLD_PHONE = "01009406505"
OLD_TEL = "tel:+201009406505"
NEW_PHONE_A = "01001288414"
NEW_PHONE_B = "01227008997"
TEL_A = "tel:+201001288414"
TEL_B = "tel:+201227008997"
OLD_ADDRESS = "طريق بنها – الزقازيق، شرويدة، الزقازيق"
NEW_ADDRESS = "الزقازيق، أول طريق أبو حماد، الشوبك"
READ_TRANSIENT = {429, 502, 503, 504, 520, 522, 524}

KEY = os.environ.get("A3TAL_API_KEY", "")
if not KEY:
    sys.exit("A3TAL_API_KEY is not set")


def bridge_request(method, path, payload=None, retry_read=True):
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"X-A3tal-Key": KEY, "Authorization": "Bearer " + KEY,
               "Accept": "application/json", "Cache-Control": "no-store",
               "User-Agent": "A3tal-El-Dawly-Contact-Correction/1.0"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(BASE + "/wp-json/a3tal-direct/v1" + path,
                                     data=body, method=method, headers=headers)
    attempts = 4 if retry_read and method == "GET" else 1
    for index in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=55) as response:
                data = json.load(response)
            if not isinstance(data, dict):
                raise RuntimeError("Unexpected response format from WordPress")
            return data
        except urllib.error.HTTPError as exc:
            if method == "GET" and exc.code in READ_TRANSIENT and index < attempts - 1:
                print("WordPress read temporarily unavailable, retrying after cooldown:", exc.code, flush=True)
                time.sleep(30 * (index + 1))
                continue
            raise RuntimeError("Bridge HTTP error: " + str(exc.code)) from None
        except (TimeoutError, urllib.error.URLError, json.JSONDecodeError) as exc:
            if method == "GET" and index < attempts - 1:
                print("WordPress read interrupted; waiting before retry", flush=True)
                time.sleep(30 * (index + 1))
                continue
            raise RuntimeError("Bridge transport/read error") from None


def assert_identity(post):
    if post.get("id") != POST_ID or post.get("slug") != SLUG or post.get("status") != "publish" or post.get("type") != "post":
        raise RuntimeError("Post identity/status changed; refusing to modify")
    if not (post.get("link") or "").rstrip("/").endswith("/" + SLUG):
        raise RuntimeError("Unexpected permalink; refusing to modify")


def verify(post):
    assert_identity(post)
    body = post.get("content")
    if not isinstance(body, str):
        raise RuntimeError("Missing published body")
    if not all(value in body for value in (NEW_ADDRESS, NEW_PHONE_A, NEW_PHONE_B, TEL_A, TEL_B)):
        raise RuntimeError("New contact data incomplete")
    if any(value in body for value in (OLD_PHONE, OLD_TEL, OLD_ADDRESS)):
        raise RuntimeError("Stale contact detail is still present")
    # Ensure every displayed phone has a clickable tel: counterpart.
    if body.count(TEL_A) < 3 or body.count(TEL_B) < 3:
        raise RuntimeError("Expected header, contact table, and footer phone links not complete")
    return True


def corrected_content(body):
    if OLD_PHONE not in body and OLD_ADDRESS not in body:
        if all(v in body for v in (NEW_PHONE_A, NEW_PHONE_B, NEW_ADDRESS, TEL_A, TEL_B)):
            return None
        raise RuntimeError("Existing contact information differs from the reviewed original")
    if OLD_PHONE not in body or OLD_ADDRESS not in body:
        raise RuntimeError("Only part of the original contact information matches; manual review needed")
    if body.count(OLD_ADDRESS) != 1 or body.count(OLD_TEL) < 3:
        raise RuntimeError("Original address or telephone link layout changed; refusing unreviewed edit")
    body = body.replace(OLD_ADDRESS, NEW_ADDRESS)
    body = body.replace(OLD_TEL, TEL_A).replace(OLD_PHONE, NEW_PHONE_A)
    # The three existing clickable first-number anchors have matching
    # visual styles in the article's header, table, and closing CTA.
    pattern = re.compile(r'<a\b[^>]*href=(["' + "'" + r'])' + re.escape(TEL_A) + r'\1[^>]*>.*?</a>', flags=re.I | re.S)
    count = 0

    def add_second(match):
        nonlocal count
        primary = match.group(0)
        secondary = primary.replace(TEL_A, TEL_B, 1).replace(NEW_PHONE_A, NEW_PHONE_B)
        secondary = secondary.replace("اتصل بالمركز:", "الرقم الثاني:")
        secondary = secondary.replace("اتصل الآن:", "الرقم الثاني:")
        count += 1
        return primary + " " + secondary

    body = pattern.sub(add_second, body)
    if count != 3:
        raise RuntimeError("Expected 3 contact links, found " + str(count))
    return body


def main():
    original = bridge_request("GET", f"/post/{POST_ID}")
    assert_identity(original)
    original_content = original.get("content")
    if not isinstance(original_content, str):
        raise RuntimeError("WordPress returned missing content")
    new_content = corrected_content(original_content)
    if new_content is None:
        verify(original)
        print("Already corrected and verified: article", POST_ID, flush=True)
        return
    # Refetch just before updating, to avoid overwriting an intervening edit.
    current = bridge_request("GET", f"/post/{POST_ID}")
    assert_identity(current)
    if hashlib.sha256(current["content"].encode("utf-8")).digest() != hashlib.sha256(original_content.encode("utf-8")).digest():
        raise RuntimeError("Concurrent editorial change detected; stop to protect the article")
    print("Patching contact fields only for article", POST_ID, flush=True)
    failed = None
    try:
        result = bridge_request("POST", "/update-post", {"id": POST_ID, "content": new_content}, retry_read=False)
        assert_identity(result)
    except Exception as err:
        failed = err
        print("Write response interrupted; confirming published result by safe readback", flush=True)
    time.sleep(8)
    updated = bridge_request("GET", f"/post/{POST_ID}")
    try:
        verify(updated)
    except RuntimeError:
        if failed:
            raise RuntimeError("Contact correction not verified: " + str(failed)) from None
        raise
    if updated["featured_media"] != original["featured_media"]:
        raise RuntimeError("Featured image changed unexpectedly")
    if updated["title"] != original["title"]:
        raise RuntimeError("Title changed unexpectedly")
    print("SUCCESS: both phone numbers and new address verified in all three contact locations", flush=True)
    print("Post:", updated["link"], flush=True)
    print("Featured image kept:", updated["featured_media"], flush=True)


if __name__ == "__main__":
    main()
