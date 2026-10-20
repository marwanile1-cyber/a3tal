#!/usr/bin/env python3
"""Link the published Arrizo 5 vehicle record to its existing maintenance guide.
No new posts, URL changes, article rewrites, or model-year guesses.
"""
import importlib.util
import json
import urllib.parse
import urllib.request
import re

spec = importlib.util.spec_from_file_location("bridge", "scripts/deploy-dtc-library.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

BASE = "https://a3tal.com"
CAR_ID = 83383
CAR_SLUG = "chery-arrizo-5-egypt"
ARTICLE_SLUG = "chery-arrizo-5-2026-egypt"

def public_json(path):
    req = urllib.request.Request(
        BASE + path,
        headers={"User-Agent":"A3tal-Verified-Link-20261020/1.0","Accept":"application/json"},
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)

def read_ids(bridge_client):
    payload = bridge_client.request(
        {"op":"post_meta","post_id":CAR_ID,"key":"_a3_related_post_ids"}
    )
    raw = payload.get("_a3_related_post_ids", [])
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    return list(dict.fromkeys(int(item) for item in re.findall(r"\d+", str(raw)) if int(item)>0))

def main():
    client = bridge.Bridge()
    status = client.request({"op":"site_info"})
    if status.get("active_theme") != "a3tal-global":
        raise RuntimeError("Wrong active theme; no write attempted")

    car = public_json(f"/wp-json/wp/v2/a3tal-cars/{CAR_ID}?_fields=id,slug,status,title")
    if (int(car.get("id",0)) != CAR_ID or
            car.get("slug") != CAR_SLUG or
            car.get("status") != "publish"):
        raise RuntimeError("Arrizo 5 entity identity/status mismatch; abort")

    query = urllib.parse.urlencode({
        "slug":ARTICLE_SLUG,
        "_fields":"id,slug,title,status,link",
        "per_page":2,
    })
    matches = public_json("/wp-json/wp/v2/posts?" + query)
    if not isinstance(matches,list) or len(matches)!=1:
        raise RuntimeError("Expected one published maintenance article by exact slug")
    article = matches[0]
    title = article.get("title",{}).get("rendered","")
    if (article.get("slug") != ARTICLE_SLUG or
            article.get("status") != "publish" or
            "صيانة شيري أريزو 5" not in title):
        raise RuntimeError("Unexpected article content or status; abort")
    article_id = int(article["id"])
    if article_id <= 0:
        raise RuntimeError("Invalid article id")
    before = read_ids(client)
    if article_id in before:
        print("ARRIZO5_ALREADY_LINKED",CAR_ID,article_id,flush=True)
        return
    # Re-read before mutation and preserve every existing curated relationship.
    current = read_ids(client)
    if current != before:
        raise RuntimeError("Concurrent related metadata edit; abort")
    updated = current + [article_id]
    target = ",".join(map(str, updated))
    try:
        client.request({
            "op":"post_meta_set",
            "post_id":CAR_ID,
            "meta":{"_a3_related_post_ids":target},
            "confirm":True,
            "dangerous":True,
        },write=True)
    except RuntimeError as exc:
        print("ARRIZO5_WRITE_READBACK_CHECK",str(exc),flush=True)
    final = read_ids(client)
    if final != updated:
        raise RuntimeError(f"Readback mismatch; expected {updated}, got {final}")
    print("ARRIZO5_RELATED_LINK_CONFIRMED",CAR_ID,article_id,article["link"],flush=True)

if __name__=="__main__":
    main()
