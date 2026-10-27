#!/usr/bin/env python3
"""Flush WordPress page cache only after direct proven JAECOO_J5 indexability; then QA canonical URL.
Uses site's existing authenticated A3tal Direct Bridge cache_flush operation.
"""
import os,json,urllib.request,urllib.parse,time,re
URL="https://a3tal.com/cars/jaecoo-j5-2027-egypt/"
KEY=os.environ["A3TAL_API_KEY"]
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (A3tal Seo Cache QA)","Cache-Control":"no-cache, no-store","Pragma":"no-cache"}),timeout=55) as resp:
        return resp.read(2000000).decode("utf8","replace")
def robots(h):
    m=re.findall(r'<meta[^>]+name=["\x27]robots["\x27][^>]*>',h,re.I)
    return m[:4]
def run():
    fresh=fetch(URL+"?a3tal_jaecoo_j5_verification=20261027")
    if "index, follow" not in fresh or "noindex, follow" in fresh:
        raise RuntimeError("Fresh JAECOO_J5 source not indexable, refusing cache clear")
    print("PRE_PURGE_LIVE_CAR_SOURCE_INDEX_VERIFIED",robots(fresh),flush=True)
    payload=json.dumps({"op":"cache_flush","confirm":True,"dangerous":True}).encode("utf8")
    headers={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json",
            "Accept":"application/json","User-Agent":"A3tal-JAECOO_J5-Cache-Flush/20261027"}
    with urllib.request.urlopen(urllib.request.Request("https://a3tal.com/wp-json/a3tal-direct/v1/admin",
            data=payload,headers=headers,method="POST"),timeout=80) as r:result=json.load(r)
    if not result.get("ok"):raise RuntimeError("WordPress refused cache flush")
    print("WP_CACHE_FLUSH_CONFIRMED",result.get("result"),flush=True)
    for attempt in range(5):
        raw=fetch(URL)
        rules=robots(raw)
        if ('content="index, follow' in raw or "content='index, follow" in raw) and "noindex, follow" not in raw:
            if 'https://a3tal.com/cars/jaecoo-j5-2027-egypt/' not in raw:
                raise RuntimeError("Canonical URL missing after purge")
            print("NORMAL_CANONICAL_JAECOO_J5_PAGE_INDEX_FOLLOW_CACHE_REFRESHED",URL,rules,flush=True)
            return
        print("STILL_CACHED_OLD_ROBOTS",attempt+1,rules,flush=True)
        time.sleep(7)
    raise RuntimeError("Origin indexable, but plain canonical URL still stale with noindex due to external cache")
if __name__=="__main__":run()
