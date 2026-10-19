#!/usr/bin/env python3
"""Rebuild Opel Insignia DTC manually rated 58/100 with OEM Vauxhall variants and multi-module safe diagnostic workflows.
Do not change their permalinks, existing content, hero media, Yoast meta,
status, canonical, or their other links. Stop on concurrent edits.
"""
import html,json,os,re,time,urllib.parse,urllib.request
from pathlib import Path
from editorial_minimum_words import count_editorial_words,require_minimum

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY")
if not KEY:raise RuntimeError("A3TAL_API_KEY is required")
MANIFEST=json.loads((Path(__file__).resolve().parent.parent/"data/expansions/egypt-editorial-quality80-batch06-insignia-dtc-20261020.json").read_text("utf-8"))
if MANIFEST.get("minimum_after_repair")!=1500:raise RuntimeError("Missing editorial quality-80 acceptance policy")
AUDIT=json.loads((Path(__file__).resolve().parent.parent/MANIFEST["audit_path"]).read_text("utf-8"))
if AUDIT.get("threshold_repair_if_score_lte")!=80:raise RuntimeError("Quality review threshold changed")
REVIEWED={x["slug"]:x for x in AUDIT["reviewed"]}
expected={"opel-insignia-fault-codes-dtc-dictionary"}
if {x["slug"] for x in MANIFEST["articles"]}!=expected:raise RuntimeError("Unreviewed post in publication manifest")
for article in MANIFEST["articles"]:
    item=REVIEWED.get(article["slug"])
    if not item or item["score"]>80 or item["decision"]!="repair" or item["pid"]!=article["pid"]:
        raise RuntimeError("A >80 score or unreviewed post must NOT be edited: "+article["slug"])
    print("MANUAL_QUALITY_SCORE_APPROVED",article["slug"],item["score"],flush=True)
def get(url, auth=True, raw=False):
    url=url if url.startswith("http") else API+url
    url=urllib.parse.quote(url,safe=":/?&=%#@+,;")
    headers={"User-Agent":"A3tal-1500-Editorial-Repair/1.0","Accept":"application/json,text/html,*/*","Cache-Control":"no-store"}
    if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    for n in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=75) as r:
                buf=r.read().decode("utf-8","replace")
            return buf if raw else json.loads(buf)
        except Exception as e:
            if n==2:raise
            print("RETRY_READ",str(e)[:100],flush=True)
            time.sleep(5*(n+1))
def post(path,obj):
    data=json.dumps(obj,ensure_ascii=False).encode()
    h={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json",
       "User-Agent":"A3tal-1500-Editorial-Repair/1.0"}
    req=urllib.request.Request(API+path,headers=h,data=data,method="POST")
    with urllib.request.urlopen(req,timeout=140) as r:return json.load(r)
def live_verify(e,featured):
    slug=e["slug"];pid=e["pid"]
    rest=get(SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode({
      "_fields":"id,slug,status,link,featured_media,content,yoast_head_json"}),auth=False)
    if rest.get("slug")!=slug or rest.get("status")!="publish" or rest.get("link","").rstrip("/")!=SITE+"/"+slug:
        raise RuntimeError("Live identity unexpectedly changed "+slug)
    if int(rest.get("featured_media") or 0)!=featured:
        raise RuntimeError("Live featured media changed "+slug)
    actual=(rest.get("content") or {}).get("rendered","")
    count=require_minimum(actual,slug)
    if e["heading"] not in html.unescape(re.sub("<[^>]*>"," ",actual)):
        raise RuntimeError("New section not visible in public WordPress content "+slug)
    page=get(SITE+"/"+slug+"/?1500-review="+str(int(time.time())),auth=False,raw=True)
    if e["heading"] not in html.unescape(re.sub("<[^>]*>"," ",page)):
        raise RuntimeError("New heading absent from actual page "+slug)
    if not re.search(r'<meta[^>]+property=["\x27]og:image',page,re.I):
        raise RuntimeError("Social/featured image missing "+slug)
    if re.search(r'<meta[^>]*name=["\x27]robots["\x27][^>]*noindex',page,re.I):
        raise RuntimeError("Unexpected noindex "+slug)
    if 'rel="canonical"' not in page:raise RuntimeError("Canonical absent "+slug)
    for source in ("GML_10970043_Insignia_Spec","vauxhall.co.uk/owners/information-and-safety/owners-manuals","opel-insignia-electrical-intellilux-screen-problems"):
        if source not in actual:
            raise RuntimeError("New verified OEM source is absent from live content: "+slug+" "+source)
    print("QUALITY80_REPAIR_VERIFIED_LIVE",SITE+"/"+slug+"/","words",count,"featured",featured,flush=True)

def main():
    plans=[]
    for e in MANIFEST["articles"]:
        slug=e["slug"];pid=e["pid"];marker=e["marker"]
        rest=get(SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?_fields=id,slug,status,featured_media,link",auth=False)
        if rest.get("id")!=pid or rest.get("slug")!=slug or rest.get("status")!="publish":
            raise RuntimeError("Post identity mismatch "+slug)
        if rest.get("link","").rstrip("/")!=SITE+"/"+slug or not rest.get("featured_media"):
            raise RuntimeError("Unverified URL or hero "+slug)
        src=get("/post/"+str(pid))
        if src.get("type")!="post" or src.get("status")!="publish" or src.get("slug")!=slug:
            raise RuntimeError("Bridge identity mismatch "+slug)
        featured=int(rest["featured_media"])
        if int(src.get("featured_media") or 0)!=featured:raise RuntimeError("Featured race "+slug)
        body=src.get("content","")
        if not isinstance(body,str) or count_editorial_words(body)<80:
            raise RuntimeError("Old article missing expected depth "+slug)
        if e["html"].count(marker)!=1 or count_editorial_words(e["html"])<750:
            raise RuntimeError("Additional research not substantive "+slug)
        if marker in body:
            require_minimum(body,slug)
            plans.append((e,src,None,featured))
            continue
        if count_editorial_words(body)>=1500:
            print("ALREADY_1500_BUT_NOT_MARKED",slug,"preserving",flush=True)
            plans.append((e,src,None,featured))
            continue
        # Insert before the existing final conclusion and preserve ALL old copy.
        conclusion=list(re.finditer(r"<h2\b[^>]*>\s*الخلاصة\s*</h2>",body,re.I))
        if len(conclusion)!=1:raise RuntimeError("Expected exactly one existing final conclusion "+slug)
        pos=conclusion[0].start()
        add="\n"+e["html"]+"\n"
        combined=body[:pos]+add+body[pos:]
        if combined.replace(add,"",1)!=body:raise RuntimeError("Original body not preserved "+slug)
        count=require_minimum(combined,slug)
        plans.append((e,src,combined,featured))
        print("READY_1500",slug,"old",count_editorial_words(body),"new",count,flush=True)
    print("PRECHECK_ALL_1500_REBUILDS",len(plans),flush=True)
    for e,src,combined,featured in plans:
        slug=e["slug"];pid=e["pid"]
        if combined is not None:
            fresh=get("/post/"+str(pid))
            if fresh.get("modified_gmt")!=src.get("modified_gmt") or fresh.get("content")!=src.get("content"):
                raise RuntimeError("Concurrent editorial change: "+slug)
            try:post("/update-post",{"id":pid,"content":combined,"expected_modified_gmt":src["modified_gmt"]})
            except Exception as error:
                latest=get("/post/"+str(pid))
                if e["marker"] not in latest.get("content",""):
                    raise RuntimeError("Write uncertain; no blind retry "+slug) from error
            saved=get("/post/"+str(pid))
            if saved.get("slug")!=slug or saved.get("status")!="publish" or int(saved.get("featured_media") or 0)!=featured:
                raise RuntimeError("Post identity, status or media changed "+slug)
            require_minimum(saved.get("content",""),slug)
        live_verify(e,featured)
        time.sleep(2)
    print("QUALITY80_BATCH06_INSIGNIA_DTC_LIVE_ACCEPTED",len(plans),flush=True)
if __name__=="__main__":main()
