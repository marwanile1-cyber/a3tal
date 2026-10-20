#!/usr/bin/env python3
"""Guarded WordPress repair for MANUALLY rated <=80 next-20 posts only.
Supports full replacement of unsafe posts with backup artifact, or addition of
researched sections to safe original bodies. Preserves slug, status, featured
image, WordPress SEO metadata (only content field is changed). No >80 writes.
"""
import glob,html,json,os,re,time,urllib.parse,urllib.request,hashlib
from pathlib import Path
from editorial_minimum_words import count_editorial_words,require_minimum
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY secret required")
ROOT=Path(__file__).resolve().parent.parent
MANIFEST_FILES=sorted(glob.glob(str(ROOT/"data/expansions/egypt-quality80-20261020-batch15-*.json")))
if not MANIFEST_FILES:raise RuntimeError("No quality80 batch15 source manuscripts found")
manifests=[json.loads(Path(p).read_text("utf-8")) for p in MANIFEST_FILES]
paths={x["audit_path"] for x in manifests}
if len(paths)!=1 or any(x.get("minimum_after_repair")!=1500 for x in manifests):raise RuntimeError("Invalid uniform quality audit/word floor")
audit=json.loads((ROOT/next(iter(paths))).read_text("utf-8"))
audited={int(x["id"]):x for x in audit["reviewed"]}
if len(audited)!=20 or audit.get("counts",{}).get("needs_repair")!=10:raise RuntimeError("Wrong batch 11-30 score report")
items=[x for m in manifests for x in m["articles"]]
if len({x["pid"] for x in items})!=len(items):raise RuntimeError("Duplicate pid in manuscripts")
allowed={80462,80644,80456,80581,80313,80321,80936,80494,80923,80471}
if len(items)>10 or any(int(x["pid"]) not in allowed for x in items):raise RuntimeError("Article is not one of ten eligible IDs")
for e in items:
    r=audited.get(int(e["pid"]))
    if not r or r["score"]>80 or r["decision"]!="repair" or r["slug"]!=e["slug"]:
        raise RuntimeError("Non-approved or passing-grade post cannot be edited")
    if e.get("mode") not in ("replace_unsafe_original","append_researched_expansion"):
        raise RuntimeError("Missing explicit safety rewrite/append mode")
    if e["html"].count(e["marker"])!=1 or count_editorial_words(e["html"])<950:
        raise RuntimeError("Insufficient substantive corrective text "+e["slug"])
    for evidence in e.get("required_sources",[]):
        if evidence not in e["html"]:raise RuntimeError("Required source or internal doc absent "+e["slug"]+" "+evidence)
    print("MANUAL_QUALITY_APPROVED",e["pid"],r["score"],e["slug"],"mode",e["mode"],flush=True)
def fetch(url,auth=True,raw=False):
    url=url if url.startswith("http") else API+url
    url=urllib.parse.quote(url,safe=":/?&=%#@+,;")
    h={"User-Agent":"A3tal-Batch15-Safety-Repair/1.0","Accept":"application/json,text/html,*/*","Cache-Control":"no-store"}
    if auth:h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    for n in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=h),timeout=100) as r:buf=r.read().decode("utf-8","replace")
            return buf if raw else json.loads(buf)
        except Exception as exc:
            if n==3:raise
            print("READ_RETRY",n,str(exc)[:150],flush=True);time.sleep(4*(n+1))
def publish(obj):
    req=urllib.request.Request(API+"/update-post",data=json.dumps(obj,ensure_ascii=False).encode("utf-8"),method="POST",headers={
       "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","User-Agent":"A3tal-Batch15-Safety-Repair/1.0"})
    with urllib.request.urlopen(req,timeout=140) as r:return json.load(r)
def identity_match(a,b):
    return urllib.parse.unquote(str(a).rstrip("/"))==urllib.parse.unquote(str(b).rstrip("/"))
def verify_live(e,featured):
    id=e["pid"];slug=e["slug"]
    pub=fetch(SITE+"/wp-json/wp/v2/posts/"+str(id)+"?_fields=id,slug,status,link,featured_media,content",auth=False)
    if pub["id"]!=id or not identity_match(pub["slug"],slug) or not identity_match(pub["link"],SITE+"/"+slug) or pub["status"]!="publish":
        raise RuntimeError("Live identity changed for "+slug)
    if int(pub.get("featured_media") or 0)!=featured:raise RuntimeError("Original featured media changed")
    body=(pub.get("content") or {}).get("rendered","")
    words=require_minimum(body,slug)
    if e["heading"] not in html.unescape(re.sub("<[^>]+>"," ",body)):raise RuntimeError("Heading missing public REST "+slug)
    for s in e.get("required_sources",[]):
        if s not in body:raise RuntimeError("Source disappeared in public REST "+slug+" "+s)
    live=fetch(SITE+"/"+slug+"/?q80="+str(int(time.time())),auth=False,raw=True)
    if e["heading"] not in html.unescape(re.sub("<[^>]+>"," ",live)):raise RuntimeError("Missing article heading from page "+slug)
    if not re.search(r"rel=[\"']canonical[\"']",live,re.I):raise RuntimeError("Canonical missing "+slug)
    if re.search(r'<meta[^>]*name=["\x27]robots["\x27][^>]*noindex',live,re.I):raise RuntimeError("Noindex unexpectedly set "+slug)
    if not re.search(r'<meta[^>]*property=["\x27]og:image',live,re.I):raise RuntimeError("Featured/OG image missing "+slug)
    print("QUALITY80_NEXT20_REPAIR_VERIFIED_LIVE",SITE+"/"+slug+"/","words",words,"featured",featured,flush=True)
    return words
def main():
    backup=ROOT/"diagnostics"/"quality80-next20-20261020-backup"
    backup.mkdir(parents=True,exist_ok=True)
    plan=[]
    for e in items:
        pid=e["pid"];slug=e["slug"]
        pub=fetch(SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?_fields=id,slug,status,featured_media,link",auth=False)
        if pub["id"]!=pid or not identity_match(pub["slug"],slug) or not identity_match(pub["link"],SITE+"/"+slug) or pub["status"]!="publish":
            raise RuntimeError("Current public identity wrong "+slug)
        featured=int(pub.get("featured_media") or 0)
        if featured<=0:raise RuntimeError("Original featured image absent "+slug)
        src=fetch("/post/"+str(pid))
        if src.get("type")!="post" or src.get("status")!="publish" or not identity_match(src.get("slug",""),slug):
            raise RuntimeError("Bridge source identity mismatch "+slug)
        if int(src.get("featured_media") or 0)!=featured:raise RuntimeError("Bridge media mismatch "+slug)
        old=src.get("content") or ""
        if not isinstance(old,str) or count_editorial_words(old)<80:raise RuntimeError("Unexpected original body "+slug)
        (backup/(str(pid)+"-original.html")).write_text(old,"utf-8")
        if e["marker"] in old:
            new=None
            require_minimum(old,slug)
        elif e["mode"]=="replace_unsafe_original":
            new=e["html"]
        else:
            markers=list(re.finditer(r"<h2\b[^>]*>\s*الخلاصة\s*</h2>",old,re.I))
            if len(markers)!=1:raise RuntimeError("Expected original conclusion before append "+slug)
            pos=markers[-1].start()
            new=old[:pos]+"\n"+e["html"]+"\n"+old[pos:]
            if old not in new and new.replace("\n"+e["html"]+"\n","",1)!=old:
                raise RuntimeError("Preserve all old copy for nonunsafe post "+slug)
        new_words=count_editorial_words(new if new is not None else old)
        if new_words<1500:raise RuntimeError("Not encyclopedic: "+slug+" words "+str(new_words))
        plan.append((e,src,new,featured))
        print("READY_1500",slug,"old",count_editorial_words(old),"new",new_words,flush=True)
    print("PRECHECK_ALL_NEXT20",len(plan),"all old HTML archived to job artifact",flush=True)
    for e,src,new,featured in plan:
        slug=e["slug"];pid=e["pid"]
        if new is not None:
            latest=fetch("/post/"+str(pid))
            if latest.get("modified_gmt")!=src.get("modified_gmt") or latest.get("content")!=src.get("content"):
                raise RuntimeError("Concurrent editor changed article "+slug)
            try:
                publish({"id":pid,"content":new,"expected_modified_gmt":src["modified_gmt"]})
            except Exception as exc:
                after=fetch("/post/"+str(pid))
                if e["marker"] not in (after.get("content") or ""):
                    raise RuntimeError("Write uncertain, STOP no blind retry "+slug) from exc
            saved=fetch("/post/"+str(pid))
            if not identity_match(saved.get("slug",""),slug) or saved.get("status")!="publish" or int(saved.get("featured_media") or 0)!=featured:
                raise RuntimeError("Post slug/status/hero corrupted "+slug)
            require_minimum(saved.get("content",""),slug)
        verify_live(e,featured)
        time.sleep(2)
    print("QUALITY80_NEXT20_BATCH15_COMPLETED",len(items),flush=True)
if __name__=="__main__":main()
