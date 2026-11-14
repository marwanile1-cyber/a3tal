#!/usr/bin/env python3
"""Noindex only the off-topic luxury watch sales page on the automotive site.
Keep the sales landing page published and reachable to direct-link visitors.
Set Yoast's own post meta, force one safe Yoast indexable refresh, verify public
meta and that live content, product photos and contact remain unaffected.
Do NOT unpublish, trash, delete, redirect or change any automotive page.
"""
import json,os,time,re,requests
from pathlib import Path
BASE="https://a3tal.com"
API=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","").strip()
PAGE_ID=86067
SLUG="jacob-co-watch-offer"
URL=BASE+"/"+SLUG+"/"
REPORT=Path("reports/watch-offtopic-noindex-20261114.json")
REPORT.parent.mkdir(parents=True,exist_ok=True)
META="_yoast_wpseo_meta-robots-noindex"
S=requests.Session()
S.headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"User-Agent":"A3tal-OffTopic-IndexProtection-20261114"})
def api(endpoint,method="GET",payload=None,params=None):
    res=S.request(method,API+endpoint,json=payload,params=params,timeout=70)
    if not res.ok:raise RuntimeError("Bridge HTTP "+str(res.status_code)+" "+res.text[:450])
    return res.json()
def admin(op,**args):
    raw=api("/admin",method="POST",payload={"op":op,**args})
    if raw.get("ok") is not True:raise RuntimeError("Bridge admin operation "+op+" failed "+str(raw)[:200])
    return raw["result"]
def live():
    r=requests.get(URL,headers={"Cache-Control":"no-cache","User-Agent":"Mozilla/5.0"},timeout=50,
       params={"verify_nidx":str(time.time_ns())})
    if r.status_code!=200:raise RuntimeError("Landing stopped serving HTTP 200")
    text=r.text
    tags=re.findall(r'<meta[^>]+name=["\\\']robots["\\\'][^>]*>',text,re.I)
    has_noindex=any("noindex" in tag.lower() for tag in tags)
    if 'a3tal-watch-landing' not in text or "24,000" not in text or "watch-videos" not in text or "wa.me/" not in text:
        raise RuntimeError("Sales landing content changed unexpectedly")
    return {"noindex":has_noindex,"tags":tags[:4],"published":True,"content_ok":True}
def main():
    if not KEY:raise RuntimeError("Bridge secret is required")
    p=requests.get(BASE+"/wp-json/wp/v2/pages",params={"slug":SLUG,"_fields":"id,status,slug,link"},timeout=35).json()
    if len(p)!=1 or p[0].get("id")!=PAGE_ID or p[0].get("status")!="publish" or p[0].get("link")!=URL:
        raise RuntimeError("Existing WordPress item identity or status changed; refusing edit")
    old=admin("post_meta",post_id=PAGE_ID,key=META).get(META)
    if isinstance(old,(dict,list)):raise RuntimeError("Unexpected Yoast meta format")
    if old not in ("","0","1",None):
        raise RuntimeError("Unexpected existing Yoast robots directive "+repr(old))
    original=live()
    if original["noindex"] and old=="1":
        print("ALREADY_NOINDEX_WATCH_LANDING_VERIFIED",URL,flush=True)
        return
    admin("post_meta_set",post_id=PAGE_ID,meta={META:"1"},confirm=True)
    # Recompute Yoast indexable metadata with one safe no-content edit.
    updated=api("/update-post",method="POST",payload={"id":PAGE_ID})
    if updated.get("status")!="publish" or updated.get("slug")!=SLUG:raise RuntimeError("No-op Yoast refresh changed published page")
    try:
        admin("cache_flush",confirm=True)
    except RuntimeError as e:
        print("WARN_CACHE_FLUSH",str(e),flush=True)
    final=None
    for attempt in range(6):
        final=live()
        if final["noindex"]:break
        time.sleep(6)
    REPORT.write_text(json.dumps({"page_id":PAGE_ID,"url":URL,"before":original,"after":final,
      "original_meta":old,"after_noindex":final["noindex"]},ensure_ascii=False,indent=2),"utf8")
    if not final["noindex"]:raise RuntimeError("Public robots noindex missing, needs live review; report saved")
    # Strong verification: Yoast public REST API includes index='noindex'
    resp=requests.get(BASE+"/wp-json/wp/v2/pages",params={"slug":SLUG,"_fields":"id,yoast_head_json"},timeout=40).json()
    robots=(resp[0].get("yoast_head_json") or {}).get("robots") or {}
    if robots.get("index")!="noindex":raise RuntimeError("Yoast internal robots JSON not yet rebuilt: "+str(robots))
    # Non-indexable posts typically disappear from sitemap after Yoast indexable regeneration.
    sm=requests.get(BASE+"/page-sitemap.xml",timeout=40,headers={"Cache-Control":"no-cache"})
    in_sm=SLUG in sm.text
    print("WATCH_SITEMAP_REMOVED",not in_sm,flush=True)
    print("WATCH_SALES_200_PRESERVED_PUBLIC_NOINDEX_VERIFIED",URL,flush=True)
    if in_sm:print("NOTICE_SITEMAP_STILL_CACHED_RECHECK_YOAST_INDEXABLE",flush=True)
if __name__=="__main__":main()
