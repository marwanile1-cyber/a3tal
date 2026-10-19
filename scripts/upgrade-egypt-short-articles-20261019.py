#!/usr/bin/env python3
"""Carefully enrich five existing Egypt articles, preserving IDs, slugs and Yoast.
Uses only A3tal Direct Bridge. A failed update is never blindly retried.
"""
import json, os, re, time, html, urllib.parse, urllib.request
from pathlib import Path

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:
    raise SystemExit("A3TAL_API_KEY is missing")
TARGETS=[
 ("kia-sportage-dct-gearbox-overheating-problems",80886,"data/expansions/egypt-20261019-kia-sportage-dct.html","A3TAL-ENCYCLOPEDIA-WEAK-20261019-KIA-DCT"),
 ("kia-sportage-fault-codes-dtc-full-list-guide",80898,"data/expansions/egypt-20261019-kia-sportage-dtc.html","A3TAL-ENCYCLOPEDIA-WEAK-20261019-KIA-DTC"),
 ("mg-5-electrical-screen-tpms-problems",80684,"data/expansions/egypt-20261019-mg5-electrical.html","A3TAL-ENCYCLOPEDIA-WEAK-20261019-MG5-ELECTRICAL"),
 ("renault-megane-suspension-steering-problems",80705,"data/expansions/egypt-20261019-renault-megane-steering.html","A3TAL-ENCYCLOPEDIA-WEAK-20261019-MEGANE-STEERING"),
 ("hyundai-tucson-nx4-fault-codes-dtc-dictionary",80752,"data/expansions/egypt-20261019-tucson-dtc.html","A3TAL-ENCYCLOPEDIA-WEAK-20261019-TUCSON-DTC"),
]

def get(path, auth=True, raw=False, tries=3):
    url=path if path.startswith("https://") else API+path
    url=urllib.parse.quote(url,safe=":/?&=%#@+,;")
    headers={"User-Agent":"A3tal-Encyclopedia-Guarded-20261019/1.0","Accept":"application/json,text/html,*/*","Cache-Control":"no-store"}
    if auth:
        headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers=headers)
            with urllib.request.urlopen(req,timeout=110) as r:
                b=r.read()
            return b.decode("utf-8","replace") if raw else json.loads(b)
        except Exception as exc:
            if i==tries-1: raise
            print("RETRY_READ",type(exc).__name__,str(exc)[:120],flush=True)
            time.sleep(5*(i+1))

def post(path, data):
    payload=json.dumps(data,ensure_ascii=False).encode("utf-8")
    req=urllib.request.Request(API+path,headers={
        "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,
        "Content-Type":"application/json; charset=utf-8",
        "User-Agent":"A3tal-Encyclopedia-Guarded-20261019/1.0"
    },data=payload,method="POST")
    with urllib.request.urlopen(req,timeout=135) as r:
        return json.load(r)

def wc(text):
    clean=html.unescape(re.sub(r"<[^>]*>"," ",text))
    return len(re.findall(r"[\w\u0600-\u06ff]+",clean,re.UNICODE))

def identity(slug,pid):
    endpoint=SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode({
        "_fields":"id,slug,status,link,featured_media",})
    r=get(endpoint,auth=False)
    if r.get("id")!=pid or r.get("slug")!=slug or r.get("status")!="publish":
        raise RuntimeError("Identity mismatch for "+slug)
    if int(r.get("featured_media") or 0)<=0:
        raise RuntimeError("Missing featured image: "+slug)
    if r.get("link","").rstrip("/")!=SITE+"/"+slug:
        raise RuntimeError("Published canonical slug mismatch: "+slug)
    return r

def file_data(path, marker):
    t=Path(path).read_text(encoding="utf-8")
    if t.count(marker)!=1 or "<h2>" not in t or wc(t)<700:
        raise RuntimeError("Expansion editorial depth or marker invalid: "+path)
    if len(re.findall(r"<table\b",t))!=1:
        raise RuntimeError("Expected one helpful responsive table per article "+path)
    return t

def merge(original,extra):
    matches=list(re.finditer(r"<h2\b[^>]*>\s*الخلاصة\s*</h2>",original,re.I))
    if len(matches)!=1:raise RuntimeError("Original conclusion heading no longer unique")
    at=matches[0].start()
    return original[:at]+"\n"+extra+"\n"+original[at:]

def public_verify(slug,marker):
    url=SITE+"/"+slug+"/"
    for attempt in range(4):
        if attempt:time.sleep(8)
        try:
            result=get(url+"?a3talc="+str(int(time.time())),auth=False,raw=True)
            headings={
                "A3TAL-ENCYCLOPEDIA-WEAK-20261019-KIA-DCT":"ما الذي يجب تحديده قبل تشخيص فتيس كيا سبورتاج؟",
                "A3TAL-ENCYCLOPEDIA-WEAK-20261019-KIA-DTC":"كيف تقرأ كود عطل كيا سبورتاج دون الوقوع في تشخيص خاطئ؟",
                "A3TAL-ENCYCLOPEDIA-WEAK-20261019-MG5-ELECTRICAL":"قبل فحص كهرباء MG5: حدد العَرَض والتجهيز",
                "A3TAL-ENCYCLOPEDIA-WEAK-20261019-MEGANE-STEERING":"خريطة تشخيص صوت الطقطقة في رينو ميجان",
                "A3TAL-ENCYCLOPEDIA-WEAK-20261019-TUCSON-DTC":"كيف تحدد معنى كود توسان NX4 حسب المحرك والفتيس؟",
            }
            plain=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",result)))
            if headings[marker] not in plain:
                raise RuntimeError("Updated editorial heading not visible")
            if "<meta property=\"og:image\"" not in result and 'property="og:image"' not in result:
                raise RuntimeError("Open Graph image missing")
            if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex',result,re.I):
                raise RuntimeError("Unexpected noindex")
            if wc(result)<800:raise RuntimeError("Rendered text unexpectedly short")
            return
        except Exception as e:
            print("PUBLIC_RECHECK",slug,type(e).__name__,str(e)[:140],flush=True)
    raise RuntimeError("No public verification for "+slug)

def main():
    plans=[]
    # Read-before-write preflight for all targets prevents partial mutation
    # when one source identity or editorial expansion is wrong.
    for slug,pid,path,marker in TARGETS:
        p=identity(slug,pid)
        row=get("/post/"+str(pid))
        if int(row.get("id",0))!=pid or row.get("slug")!=slug or row.get("type")!="post" or row.get("status")!="publish":
            raise RuntimeError("Bridge post identity mismatch for "+slug)
        if int(row.get("featured_media") or 0)!=int(p["featured_media"]):
            raise RuntimeError("Featured image changed since public identity check "+slug)
        body=row.get("content","")
        if not isinstance(body,str) or wc(body)<60:raise RuntimeError("Unexpected missing original body "+slug)
        extra=file_data(path,marker)
        if marker in body:
            if wc(body)<800:raise RuntimeError("Already marked but not substantive "+slug)
            plans.append((slug,pid,marker,row,None,p["featured_media"]))
            continue
        if wc(body)>900:raise RuntimeError("Original article expanded by someone else, stop: "+slug)
        combined=merge(body,extra)
        if wc(combined)<800:raise RuntimeError("Insufficient revised content "+slug)
        if combined.replace("\n"+extra+"\n","",1)!=body:
            raise RuntimeError("Preservation guard failed "+slug)
        plans.append((slug,pid,marker,row,combined,p["featured_media"]))
        print("PREPARED",slug,"original_words",wc(body),"revised_words",wc(combined),flush=True)
    print("ALL_FIVE_PRECHECKS_PASSED",len(plans),flush=True)
    for slug,pid,marker,row,combined,featured in plans:
        if combined is None:
            public_verify(slug,marker)
            print("ALREADY_DONE",slug,flush=True)
            continue
        reread=get("/post/"+str(pid))
        if reread.get("modified_gmt")!=row.get("modified_gmt") or reread.get("content")!=row.get("content"):
            raise RuntimeError("Concurrent change: "+slug)
        try:
            result=post("/update-post",{"id":pid,"content":combined,"expected_modified_gmt":row["modified_gmt"]})
        except Exception as e:
            recovered=get("/post/"+str(pid))
            if marker not in recovered.get("content",""):
                raise RuntimeError("Write unconfirmed; do not auto retry "+slug) from e
            print("RECOVERED_WRITE_AFTER_TIMEOUT",slug,flush=True)
        else:
            if result.get("ok") is False:raise RuntimeError("Bridge explicitly refused "+slug)
        after=get("/post/"+str(pid))
        if after.get("content","").count(marker)!=1 or after.get("slug")!=slug or after.get("status")!="publish":
            raise RuntimeError("Readback content or identity mismatch "+slug)
        if int(after.get("featured_media") or 0)!=int(featured):
            raise RuntimeError("Featured image changed "+slug)
        if wc(after["content"])<800:raise RuntimeError("Revision too short after WordPress processing "+slug)
        public_verify(slug,marker)
        print("LIVE_ENCYCLOPEDIA_UPDATED",slug,"words",wc(after["content"]),SITE+"/"+slug+"/",flush=True)
        time.sleep(2)
    print("EGYPT_SHORT_ARTICLES_BATCH01_FIVE_COMPLETE",flush=True)

if __name__=="__main__":
    main()
