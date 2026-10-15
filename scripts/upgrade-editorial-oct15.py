#!/usr/bin/env python3
"""One-time expansion of four already-published non-DTC guides. No new posts or media."""
import json,os,re,time,urllib.request,urllib.parse,html
from pathlib import Path

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
SECRET=os.getenv("A3TAL_API_KEY","")
if not SECRET:raise SystemExit("Missing A3TAL_API_KEY secret")
ITEMS=[
("mg5-new-egypt-prices-trims-2026-october","data/expansions/oct15-mg5-price.html"),
("mg5-vs-nissan-sunny-egypt-buying-comparison","data/expansions/oct15-mg5-sunny.html"),
("steering-wheel-vibrates-when-braking-diagnosis","data/expansions/oct15-brake-judder.html"),
("motorcycle-chain-slack-tightening-maintenance-guide","data/expansions/oct15-motorcycle-chain.html")
]
def http(path,body=None,secure=True):
    url=path if path.startswith("https://") else API+path
    h={"User-Agent":"A3tal-DeepEditorial/2026-10-15","Accept":"application/json,*/*"}
    if secure:h.update({"X-A3tal-Key":SECRET,"Authorization":"Bearer "+SECRET})
    data=None if body is None else json.dumps(body,ensure_ascii=False).encode("utf-8")
    if data is not None:h["Content-Type"]="application/json"
    req=urllib.request.Request(url,headers=h,data=data)
    with urllib.request.urlopen(req,timeout=120) as response:
        raw=response.read()
    return json.loads(raw) if secure else raw
def get_public(slug):
    url=SITE+"/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":slug,"_fields":"id,slug,status,featured_media,link,yoast_head_json"})
    records=json.loads(http(url,secure=False))
    if len(records)!=1 or records[0].get("status")!="publish":
        raise RuntimeError("Expected exactly one published article: "+slug)
    return records[0]
def words(content):
    t=re.sub(r"<[^>]*>"," ",content)
    return len(re.findall(r"[\w\u0600-\u06FF]+",html.unescape(t)))
def merged(text,extra):
    if not any(s in text for s in ("<h2>الأسئلة", "<h2>أسئلة سريعة")):
        raise RuntimeError("Could not locate FAQs for editorial insertion; stop")
    i=min([text.find(s) for s in ("<h2>الأسئلة","<h2>أسئلة سريعة") if s in text])
    return text[:i]+"\n"+extra+"\n"+text[i:]
def audit_public(slug,featured):
    link=SITE+"/"+slug+"/"
    for attempt in range(5):
        if attempt:time.sleep(9)
        try:
            record=get_public(slug)
            if int(record.get("featured_media") or 0)!=featured:raise RuntimeError("Lost featured media")
            raw=http(link+"?audit="+str(int(time.time())),secure=False).decode("utf-8","replace")
            if "og:image" not in raw or "a3tal-editorial-"+slug not in raw:
                raise RuntimeError("Featured image or og:image not correct")
            if "noindex" in raw.lower():raise RuntimeError("Public article has noindex")
            print("LIVE_AUDIT_OK",link,"featured",featured,flush=True)
            return link
        except Exception as e:print("AUDIT_WAIT",slug,str(e)[:120],flush=True)
    raise RuntimeError("Could not verify live article: "+slug)
def main():
    status=http("/status")
    if not status.get("ok"):raise RuntimeError("A3tal Direct Bridge not available")
    print("EDITORIAL_REBUILD_BRIDGE",status.get("version"),flush=True)
    results=[]
    for slug,path in ITEMS:
        post=get_public(slug)
        pid=post["id"]
        featured=int(post.get("featured_media") or 0)
        if not featured:raise RuntimeError("Existing post has no cover: "+slug)
        current=http("/post/"+str(pid))
        original=current.get("content","")
        if not isinstance(original,str) or len(original)<2500:raise RuntimeError("Cannot inspect full live content; no write")
        if current.get("status")!="publish" or int(current.get("featured_media") or 0)!=featured:
            raise RuntimeError("Original publication state changed")
        extra=Path(path).read_text(encoding="utf-8")
        match=re.search(r"<!-- (A3TAL-ENCYCLOPEDIC-EXPANSION-[A-Z0-9-]+) -->",extra)
        if not match:raise RuntimeError("Missing unique review marker")
        marker=match.group(1)
        if marker in original:
            print("ALREADY_ENRICHED",slug,words(original),flush=True)
            results.append({"slug":slug,"words":words(original),"url":audit_public(slug,featured),"already":True})
            continue
        new=merged(original,extra)
        print("DEEP_CONTENT_CHECK",slug,"before",words(original),"added",words(extra),"after",words(new),flush=True)
        if words(new)<1650 or words(extra)<1100:
            raise RuntimeError("Encyclopedic depth check failed: "+slug)
        if len(re.findall(r"<h2\b",new))<10:raise RuntimeError("Missing substantive sections: "+slug)
        # Single guarded live mutation only. Read latest original, then preserve all previous blocks.
        try:
            result=http("/update-post",{"id":pid,"content":new})
            print("UPDATE_BRIDGE_RESPONSE",slug,str(result)[:650],flush=True)
        except Exception as e:
            print("WRITE_AMBIGUOUS_CHECK_LIVE_BEFORE_RETRY",slug,str(e)[:200],flush=True)
            raise
        if result.get("ok") is False:raise RuntimeError("Bridge explicitly rejected the update")
        actual=http("/post/"+str(pid))
        updated=actual.get("content","")
        if marker not in updated:
            raise RuntimeError("Updated article did not retain review marker: "+slug)
        if words(updated)<1650 or actual.get("status")!="publish" or int(actual.get("featured_media") or 0)!=featured:
            raise RuntimeError("Updated article depth or cover failed: "+slug)
        link=audit_public(slug,featured)
        results.append({"slug":slug,"words":words(updated),"url":link,"already":False})
        print("ENCYCLOPEDIC_ARTICLE_VERIFIED",json.dumps(results[-1],ensure_ascii=False),flush=True)
    print("ENCYCLOPEDIC_REBUILD_ALL",json.dumps(results,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
