#!/usr/bin/env python3
"""Idempotent depth and UX overhaul of 9 published A3tal articles.
No new posts, slugs, dates, categories, featured images, focus keywords,
canonical tags or existing paragraphs removed. Every change gets readback QA.
"""
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
SECRET=os.environ.get("A3TAL_API_KEY","")
if not SECRET:raise SystemExit("Missing configured A3TAL_API_KEY")
DATA=Path("data/editorial-oct-18-2026.json")
EXPECTED={
 "jetour-x70-plus-ckd-2027-egypt-price-luxury":84039,
 "suzuki-alto-vs-proton-saga-2027-egypt-city-car":84042,
 "opel-frontera-egypt-family-review-third-row-2026":84045,
 "car-jerks-on-first-move-after-stop-diagnosis":84048,
 "dashboard-lights-dim-with-ac-on-charging-system":84051,
 "when-to-replace-car-cabin-air-filter-symptoms":84054,
 "fuel-pump-low-pressure-how-to-test-before-replacement":84072,
 "scooter-stalls-when-hot-causes-ignition-fuel":84076,
 "how-to-verify-authorized-car-service-center-egypt":84077
}
MIN_WORDS={
 "suzuki-alto-vs-proton-saga-2027-egypt-city-car":1950,
 "opel-frontera-egypt-family-review-third-row-2026":1950,
}
MARKER_RE=re.compile(r"<!--\s*(A3TAL-ENCYCLOPEDIC-EXPANSION-OCT18-[A-Z0-9-]+)\s*-->")
def words(text):
    clean=html.unescape(re.sub(r"<[^>]+>"," ",text))
    return len([w for w in clean.split() if re.search(r"[\w\u0600-\u06ff]",w)])
def request(url,body=None,auth=True,retries=3):
    target=url if url.startswith("https://") else API+url
    target=urllib.parse.quote(target,safe=":/?&=%#@+,;")
    headers={"User-Agent":"A3tal-Encyclopedic-Revision-20261018/1.0",
             "Accept":"application/json,text/html,*/*","Cache-Control":"no-cache"}
    if auth:headers.update({"X-A3tal-Key":SECRET,"Authorization":"Bearer "+SECRET})
    encoded=None if body is None else json.dumps(body,ensure_ascii=False).encode("utf-8")
    if encoded is not None:headers["Content-Type"]="application/json"
    # POST writes are non-retriable because they may have succeeded before a timeout.
    attempts=1 if encoded is not None else retries
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(urllib.request.Request(target,headers=headers,data=encoded),timeout=145) as r:
                data=r.read()
            return json.loads(data) if auth else data
        except Exception as exc:
            if attempt==attempts-1:raise
            print("READ_RETRY",type(exc).__name__,str(exc)[:150],flush=True)
            time.sleep(6*(attempt+1))
def public_post(slug):
    endpoint=SITE+"/wp-json/wp/v2/posts?"+urllib.parse.urlencode({
        "slug":slug,"per_page":3,"_fields":"id,slug,status,link,featured_media"})
    records=json.loads(request(endpoint,auth=False))
    if len(records)!=1 or records[0].get("status")!="publish":
        raise RuntimeError("Expected exactly one published target: "+slug)
    if int(records[0].get("id") or 0)!=EXPECTED[slug]:
        raise RuntimeError("Post identifier no longer matches reviewed release: "+slug)
    return records[0]
def combine(original,addition):
    headings=("<h2>الأسئلة الشائعة</h2>","<h2>أسئلة شائعة</h2>")
    locs=[original.find(s) for s in headings if s in original]
    if len(locs)!=1:raise RuntimeError("FAQs insertion marker changed; abort rather than overwrite body")
    idx=locs[0]
    return original[:idx]+"\n"+addition+"\n"+original[idx:]
def verify_public(slug,marker,featured,updated_words):
    url=SITE+"/"+slug+"/"
    for i in range(5):
        if i:time.sleep(12)
        try:
            p=public_post(slug)
            if int(p.get("featured_media") or 0)!=featured:
                raise RuntimeError("Featured media changed")
            body=request(url+"?a3tal_editorial_audit="+str(int(time.time())),auth=False).decode("utf-8","replace")
            if marker not in body:raise RuntimeError("New content marker not yet visible")
            if re.search(r'<meta[^>]+name=["\x27]robots["\x27][^>]+noindex',body,re.I):
                raise RuntimeError("Noindex present")
            if "og:image" not in body:raise RuntimeError("Social image tag absent")
            print("EXPANDED_PUBLIC_VERIFIED",slug,updated_words,url,flush=True)
            return
        except Exception as exc:
            print("PUBLIC_RECHECK",slug,type(exc).__name__,str(exc)[:135],flush=True)
    raise RuntimeError("Updated content not publicly verifiable: "+slug)
def main():
    info=request("/status")
    if not info.get("ok"):raise RuntimeError("A3tal Direct Bridge unavailable")
    items=json.loads(DATA.read_text(encoding="utf-8"))["items"]
    if len(items)!=9 or {a["slug"] for a in items}!=set(EXPECTED):raise RuntimeError("Release identities changed")
    results=[]
    for item in items:
        slug=item["slug"]
        p=public_post(slug)
        pid=int(p["id"]);featured=int(p.get("featured_media") or 0)
        if not featured:raise RuntimeError("Target post lacks featured media: "+slug)
        detail=request("/post/"+str(pid))
        original=detail.get("content","")
        if not isinstance(original,str) or len(original)<2800 or detail.get("status")!="publish":
            raise RuntimeError("Invalid live content state: "+slug)
        if int(detail.get("featured_media") or 0)!=featured:
            raise RuntimeError("Featured image differs between bridge and public")
        path=Path("data/expansions")/("oct18-"+slug+".html")
        extra=path.read_text(encoding="utf-8")
        match=MARKER_RE.search(extra)
        if not match or len(MARKER_RE.findall(extra))!=1:raise RuntimeError("Unique marker missing")
        marker=match.group(1)
        min_words=MIN_WORDS.get(slug,1500)
        if marker in original:
            if words(original)<min_words:raise RuntimeError("Marker exists but article too short")
            print("ALREADY_ENRICHED",slug,words(original),flush=True)
            results.append({"slug":slug,"words":words(original),"already":True})
            continue
        if words(extra)<900:raise RuntimeError("Expansion lacks deep technical content: "+slug)
        merged=combine(original,extra)
        count=words(merged)
        if count<min_words or len(re.findall(r"<h2\b",merged))<10:
            raise RuntimeError(f"Not deep enough: {slug} {count} words")
        if not all(fragment in merged for fragment in [original[:250],original[-250:]]):
            raise RuntimeError("Existing content would be lost")
        print("CONTENT_DEPTH",slug,"before",words(original),"added",words(extra),"after",count,flush=True)
        # The exact POST ID is pinned. Only its content is changed, preserving metadata.
        try:
            result=request("/update-post",{"id":pid,"content":merged})
        except Exception as exc:
            print("WRITE_RESPONSE_UNKNOWN_DO_NOT_RETRY",slug,type(exc).__name__,str(exc)[:145],flush=True)
            raise
        if isinstance(result,dict) and result.get("ok") is False:
            raise RuntimeError("Bridge rejected article update: "+slug)
        after=request("/post/"+str(pid))
        final=after.get("content","")
        if marker not in final or words(final)<min_words or after.get("status")!="publish":
            raise RuntimeError("Live content readback mismatch: "+slug)
        if int(after.get("featured_media") or 0)!=featured:
            raise RuntimeError("Readback featured image changed: "+slug)
        if not all(fragment in final for fragment in [original[:250],original[-250:]]):
            raise RuntimeError("Original content not preserved on server: "+slug)
        verify_public(slug,marker,featured,words(final))
        results.append({"slug":slug,"words":words(final),"already":False})
        print("ENCYCLOPEDIC_UPGRADE_COMPLETE",slug,words(final),flush=True)
    print("OCT18_ALL_NINE_DEPTH_RESULTS",json.dumps(results,ensure_ascii=False),flush=True)
if __name__=="__main__":
    main()
