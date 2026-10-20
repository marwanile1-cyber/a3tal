#!/usr/bin/env python3
"""Revision-guarded replacement of 166-word US-spec BMW X5 xDrive50e post
with Egypt-specific manufacturer-sourced G05 PHEV diagnostic encyclopedia."""
import json,os,re,urllib.parse,urllib.request,urllib.error
from pathlib import Path
PID=80907
REST="https://a3tal.com/wp-json/a3tal-direct/v1"
SITE="https://a3tal.com"
SLUG="bmw-x5-2026-hybrid-specs-problems-maintenance"
REV="2026-10-01T12:20:11+00:00"
FEATURED=80908
FILE=Path("data/repairs/egypt-bmw-x5-xdrive50e-g05-20261020.html")
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY: raise RuntimeError("Missing private bridge secret")

def request(path,body=None,secure=True):
    headers={"Accept":"application/json","User-Agent":"A3tal-Egypt-X5-Editorial-QA/20261020",
             "Cache-Control":"no-store"}
    if secure:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    payload=None
    if body is not None:
        payload=json.dumps(body,ensure_ascii=False).encode("utf-8")
        headers["Content-Type"]="application/json"
    url=path if path.startswith("https://") else REST+path
    with urllib.request.urlopen(urllib.request.Request(url,data=payload,headers=headers),timeout=100) as r:return json.load(r)

def wc(value):
    return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+",re.sub(r"<[^>]*>"," ",value)))

def identity(item):
    if int(item.get("id",0))!=PID or item.get("status")!="publish" or \
       urllib.parse.unquote(item.get("slug",""))!=SLUG or \
       not item.get("link","").startswith(SITE+"/"):
        raise RuntimeError("Post identity/status/slug mismatch")

def main():
    fresh=FILE.read_text("utf-8").strip()
    if wc(fresh)<1500:raise RuntimeError("Encyclopedic minimum missing")
    if "<h1" in fresh.lower():raise RuntimeError("Duplicate H1")
    for required in ["BMW X5 xDrive50e","489 حصان","25.7","700 نيوتن",
                     "الجهد العالي","bmw-egypt.com","bmwgroup.com"]:
        if required not in fresh:raise RuntimeError("Missing model-specific evidence")
    original=request("/post/"+str(PID))
    identity(original)
    if original.get("type")!="post" or original.get("modified_gmt")!=REV:
        raise RuntimeError("Article changed since review, abort with no write")
    if int(original.get("featured_media") or 0)!=FEATURED:
        raise RuntimeError("Cover changed, abort")
    text=original.get("content") or ""
    if "xDrive50e" not in text or "483" not in text or "44" not in text:
        raise RuntimeError("Unexpected old USA-based original content, abort")
    title="BMW X5 xDrive50e في مصر: المواصفات والشحن وأعطال الهايبرد"
    body={
      "id":PID,"expected_modified_gmt":REV,
      "title":title,"content":fresh,
      "excerpt":"دليل BMW X5 xDrive50e G05 في مصر: 489 حصانًا و700 نيوتن متر وبطارية 25.7 كيلوواط ساعة، الشحن والمدى وفرق الجيل، وتشخيص الهايبرد عالي الجهد بأمان.",
      "meta":{
        "_yoast_wpseo_focuskw":"BMW X5 xDrive50e في مصر",
        "_yoast_wpseo_title":"BMW X5 xDrive50e: المواصفات والشحن والأعطال في مصر",
        "_yoast_wpseo_metadesc":"موسوعة BMW X5 xDrive50e G05 في مصر: المواصفات الرسمية 489 حصانًا، الشحن والمدى والبطارية، تشخيص أعطال الهايبرد وفحص المستعمل بأمان."
      }
    }
    updated=request("/update-post",body)
    identity(updated)
    if int(updated.get("featured_media") or 0)!=FEATURED:
        raise RuntimeError("Cover changed during update")
    live=request(SITE+"/wp-json/wp/v2/posts/"+str(PID)+"?_fields=id,slug,status,link,featured_media,content,yoast_head_json",secure=False)
    identity(live)
    if int(live.get("featured_media") or 0)!=FEATURED:
        raise RuntimeError("Featured media changed on live")
    rendered=(live.get("content") or {}).get("rendered","")
    actual_wc=wc(rendered)
    if actual_wc<1500 or "489 حصان" not in rendered or "الجهد العالي" not in rendered:
        raise RuntimeError("Live article missing reviewed technical detail")
    robots=(live.get("yoast_head_json") or {}).get("robots") or {}
    if robots.get("index")=="noindex":
        raise RuntimeError("Unexpected noindex on repaired page")
    print("BMW_X5_PHEV_ENCYCLOPEDIA_PUBLISHED",PID,"WORDS",actual_wc,
          "SLUG_AND_FEATURED_PRESERVED",flush=True)

if __name__=="__main__":
    main()
