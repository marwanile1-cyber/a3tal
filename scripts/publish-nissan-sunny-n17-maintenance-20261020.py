#!/usr/bin/env python3
"""Revision-guarded Nissan Sunny N17 Egypt repair, exact 4AT manual context.
Never changes the existing permalink, cover or content of another model."""
import json,os,re,urllib.parse,urllib.request
from pathlib import Path
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
PID=80395
SLUG="جدول-صيانة-نيسان-صني-2026"
REV="2026-10-08T15:00:22+00:00"
COVER=80396
SOURCE=Path("data/repairs/egypt-nissan-sunny-n17-maintenance-20261020.html")
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY not configured")
def call(url,body=None,auth=True):
    endpoint=url if url.startswith("http") else API+url
    headers={"Accept":"application/json","User-Agent":"A3tal-Sunny-4AT-Official-Quality/1.0","Cache-Control":"no-store"}
    if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=None
    if body is not None:
        data=json.dumps(body,ensure_ascii=False).encode()
        headers["Content-Type"]="application/json"
    with urllib.request.urlopen(urllib.request.Request(endpoint,data=data,headers=headers),timeout=100) as r:return json.load(r)
def count(s):
    return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+",re.sub(r"<[^>]*>"," ",s)))
def ident(v):
    if int(v.get("id",0))!=PID or v.get("status")!="publish" or \
       urllib.parse.unquote(v.get("slug",""))!=SLUG or \
       not v.get("link","").startswith(SITE+"/"):
       raise RuntimeError("Publication identity mismatch")
def main():
    new=SOURCE.read_text("utf-8").strip()
    if count(new)<1500:raise RuntimeError("Minimum 1500 editorial words absent")
    if "<h1" in new.lower():raise RuntimeError("Post body cannot have extra H1")
    for marker in ("فتيسًا أوتوماتيكيًا بأربع سرعات","نيسان صني N17","4AT","16244",
                   "لا تفتح غطاء","nissan.com.eg/vehicles/new/sunny"):
        if marker not in new:raise RuntimeError("Critical technical or safety QA marker missing: "+marker)
    old=call("/post/"+str(PID))
    ident(old)
    if old.get("type")!="post" or old.get("modified_gmt")!=REV:
        raise RuntimeError("Revision conflict, no write")
    if int(old.get("featured_media") or 0)!=COVER:
        raise RuntimeError("Hero image changed, abort")
    prior=old.get("content") or ""
    if "صيانة نيسان صني" not in prior or "CVT" not in prior:
        raise RuntimeError("Original reviewed text changed, abort")
    updated=call("/update-post",{
        "id":PID,"expected_modified_gmt":REV,
        "title":"صيانة نيسان صني N17 في مصر: جدول الفحص والفتيس 4AT والزيوت",
        "content":new,
        "excerpt":"دليل صيانة نيسان صني المصرية N17 بمواصفات نيسان الرسمية: ناقل 4AT مقابل المانيوال، زيت المحرك والفتيس، التبريد والفرامل، المراكز وخطة الفحص الآمن.",
        "meta":{
           "_yoast_wpseo_focuskw":"جدول صيانة نيسان صني 2026",
           "_yoast_wpseo_title":"صيانة نيسان صني N17: جدول الفحص وفتيس 4AT والزيوت",
           "_yoast_wpseo_metadesc":"دليل صيانة نيسان صني في مصر: جدول فحص عملي، زيت المحرك والفتيس 4AT والتبريد والفرامل، وروابط نيسان الرسمية لمواعيد الخدمة."
        }
    })
    ident(updated)
    if int(updated.get("featured_media") or 0)!=COVER:
        raise RuntimeError("Featured media mismatch")
    pub=call(SITE+"/wp-json/wp/v2/posts/"+str(PID)+"?_fields=id,slug,status,link,featured_media,content,yoast_head_json",auth=False)
    ident(pub)
    if int(pub.get("featured_media") or 0)!=COVER:raise RuntimeError("Cover identity changed")
    rendered=(pub.get("content") or {}).get("rendered","")
    words=count(rendered)
    if words<1500 or "4AT" not in rendered or "16244" not in rendered:
        raise RuntimeError("Public article body verification failed")
    if ((pub.get("yoast_head_json") or {}).get("robots") or {}).get("index")=="noindex":
        raise RuntimeError("Noindex introduced, investigate")
    print("SUNNY_N17_4AT_OFFICIAL_REPAIR_VERIFIED",PID,"WORDS",words,"SLUG_COVER_PRESERVED",flush=True)
if __name__=="__main__":main()
