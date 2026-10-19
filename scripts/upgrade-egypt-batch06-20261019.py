#!/usr/bin/env python3
"""Existing-post editorial repairs via Direct Bridge. Strict preflight, no permalink/meta changes.
No retry of uncertain writes; idempotency with original editorial marker.
"""
import json,os,re,time,html,urllib.request,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE="https://a3tal.com";API=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY")
if not KEY:raise RuntimeError("No A3TAL_API_KEY")
MANIFEST=json.loads((ROOT/"data/expansions/egypt-editorial-batch06-20261019.json").read_text(encoding="utf-8"))
if MANIFEST.get("batch")!="egypt-editorial-quality-batch06":raise RuntimeError("Wrong manifest")
def wc(src):return len(re.findall(r"[\w\u0600-\u06ff]+",html.unescape(re.sub(r"<[^>]+>"," ",src))))
def req(url,payload=None,auth=False):
    h={"Accept":"application/json","Cache-Control":"no-store","User-Agent":"A3tal-Egypt-Editorial-Repair-02/1.0"}
    if auth:h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=None
    if payload is not None:h["Content-Type"]="application/json";data=json.dumps(payload,ensure_ascii=False).encode()
    request=urllib.request.Request(url,data=data,headers=h)
    with urllib.request.urlopen(request,timeout=120) as r:return json.load(r)
def public(pid):return req(BASE+"/wp-json/wp/v2/posts/"+str(pid)+"?_fields=id,slug,status,link,featured_media")
def source(pid):return req(API+"/post/"+str(pid),auth=True)
def live_check(slug,heading,old_image):
    url=BASE+"/"+slug+"/"
    for attempt in range(3):
        if attempt:time.sleep(7)
        try:
            h={"Accept":"text/html","User-Agent":"Mozilla/5.0 (A3tal-Editorial-QA/1.0)","Cache-Control":"no-cache"}
            with urllib.request.urlopen(urllib.request.Request(url+"?qa="+str(int(time.time())),headers=h),timeout=40) as r:body=r.read().decode("utf-8","replace")
            text=" ".join(html.unescape(re.sub(r"<[^>]+>"," ",body)).split())
            if heading not in text:raise RuntimeError("New diagnostic section missing")
            if not re.search(r'<meta[^>]+property=["\x27]og:image',body,re.I):raise RuntimeError("OG image missing")
            if 'content="noindex' in body:raise RuntimeError("Noindex")
            if 'class="g-table-wrap"' not in body:raise RuntimeError("No responsive table")
            if wc(body)<680:raise RuntimeError("Unexpectedly short rendered output")
            if 'rel="canonical"' not in body:raise RuntimeError("Missing canonical")
            return
        except Exception as e:
            print("READ_PUBLIC_RETRY",slug,type(e).__name__,str(e)[:120],flush=True)
    raise RuntimeError("Cannot independently verify live content of "+slug)
def main():
    plans=[]
    for row in MANIFEST["articles"]:
        pid=row["pid"];slug=row["slug"];marker=row["marker"];extra=row["html"]
        pp=public(pid);src=source(pid)
        if pp.get("id")!=pid or pp.get("slug")!=slug or pp.get("status")!="publish":raise RuntimeError("Public wrong post "+slug)
        if pp.get("link","").rstrip("/")!=BASE+"/"+slug:raise RuntimeError("Existing URL changed "+slug)
        if not pp.get("featured_media"):raise RuntimeError("Existing featured image missing "+slug)
        if src.get("slug")!=slug or src.get("status")!="publish" or src.get("type")!="post":raise RuntimeError("Direct bridge post mismatch "+slug)
        if int(src.get("featured_media") or 0)!=int(pp["featured_media"]):raise RuntimeError("Featured changed before preflight "+slug)
        content=src.get("content","")
        if not isinstance(content,str) or wc(content)<80:raise RuntimeError("Original body unexpected "+slug)
        if extra.count(marker)!=1 or extra.count("<table")!=1 or wc(extra)<500:
            raise RuntimeError("Insufficient custom reviewed editorial content "+slug)
        if marker in content:
            if wc(content)<650:raise RuntimeError("Existing marker but thin "+slug)
            plans.append((row,src,None,pp["featured_media"]))
            continue
        if wc(content)>900:raise RuntimeError("Someone already expanded this article, halt "+slug)
        conclusions=list(re.finditer(r'<h2\b[^>]*>\s*الخلاصة\s*</h2>',content,re.I))
        if len(conclusions)!=1:raise RuntimeError("Original conclusion not exactly one "+slug)
        idx=conclusions[0].start()
        revised=content[:idx]+"\n"+extra+"\n"+content[idx:]
        if revised.replace("\n"+extra+"\n","",1)!=content:raise RuntimeError("Original body not preserved "+slug)
        if wc(revised)<680:raise RuntimeError("Article still too thin "+slug)
        plans.append((row,src,revised,pp["featured_media"]))
        print("PREPARED",slug,"from",wc(content),"to",wc(revised),flush=True)
    print("BATCH06_PREFLIGHT_OK",len(plans),flush=True)
    for row,src,revised,featured in plans:
        slug=row["slug"];pid=row["pid"];marker=row["marker"];heading=row["heading"]
        if revised is None:
            live_check(slug,heading,featured);print("ALREADY_VERIFIED",slug,flush=True);continue
        check=source(pid)
        if check.get("modified_gmt")!=src.get("modified_gmt") or check.get("content")!=src.get("content"):
            raise RuntimeError("Concurrent change, abort "+slug)
        try:
            output=req(API+"/update-post",{"id":pid,"content":revised,"expected_modified_gmt":src["modified_gmt"]},auth=True)
        except Exception as error:
            latest=source(pid)
            if marker not in latest.get("content",""):raise RuntimeError("Write not verifiable; never blind retry "+slug) from error
        latest=source(pid)
        if latest.get("content","").count(marker)!=1 or latest.get("status")!="publish" or latest.get("slug")!=slug:
            raise RuntimeError("Post mutation mismatch "+slug)
        if int(latest.get("featured_media") or 0)!=int(featured):raise RuntimeError("Featured changed "+slug)
        live_check(slug,heading,featured)
        print("PUBLISHED_VERIFIED",BASE+"/"+slug+"/","words",wc(latest.get("content","")),flush=True)
        time.sleep(2)
    print("EGYPT_BATCH06_COMPLETE",flush=True)
if __name__=="__main__":main()
