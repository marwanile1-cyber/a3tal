#!/usr/bin/env python3
"""Improve existing 2027 Chevrolet Optra review to 1600+ words while preserving WebP photo, URL, OG, cover, and category."""
import json,os,re,urllib.request,urllib.parse
from pathlib import Path
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
ID=84750
SLUG="chevrolet-optra-2027-egypt-complete-review-ls-lt-after-october-price-rise"
def req(url,body=None,auth=False):
    h={"Accept":"application/json","User-Agent":"A3tal-Optra-Complete-Review-Release/20261031"}
    if auth:h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=json.dumps(body,ensure_ascii=False).encode("utf8") if body is not None else None
    if raw:h["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,data=raw,headers=h,method="POST" if raw else "GET"),timeout=110) as r:return json.load(r)
def wp():return req(SITE+"/wp-json/wp/v2/posts/"+str(ID)+"?"+urllib.parse.urlencode({"_fields":"id,slug,status,categories,link,content,featured_media,yoast_head_json"}))
def count(s):return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+",re.sub("<[^>]*>"," ",s)))
old=wp()
if old["slug"]!=SLUG or old["status"]!="publish" or 22 not in old["categories"] or not old.get("featured_media"):
    raise RuntimeError("Existing Optra review identity/status/category/cover failed")
current=(old["content"] or {}).get("rendered","")
updated=Path("data/editorial/"+SLUG+".html").read_text("utf8")
if count(updated)<1600 or updated.count("{{a3tal_image:detail}}")!=1:
    raise RuntimeError("Expanded deep Optra editorial content incomplete")
if count(current)>=1600 and "مصفوفة قرار الشراء" in current:
    print("OPTRA_2027_REVIEW_ALREADY_ENRICHED",count(current),old["link"],flush=True)
    raise SystemExit(0)
if count(current)<900:raise RuntimeError("Original current review unexpectedly short")
match=re.search(r'<figure\b[^>]*>[\s\S]*?optra-2027-review-official-interior[\s\S]*?</figure>',current,re.I)
if not match:
    match=re.search(r'<img\b[^>]*optra-2027-review-official-interior[^>]*>',current,re.I)
if not match:raise RuntimeError("Preserving existing exact Optra cabin photo failed")
updated=updated.replace("{{a3tal_image:detail}}",match.group(0))
r=req(API+"/update-post",{"id":ID,"slug":SLUG,"status":"publish","content":updated},True)
live=wp()
body=live["content"]["rendered"]
seo=live.get("yoast_head_json") or {}
if (live["slug"],live["status"],live["featured_media"])!=(SLUG,"publish",old["featured_media"]):
    raise RuntimeError("Wrong post/media after review update")
if count(body)<1600 or "مصفوفة قرار الشراء" not in body or "optra-2027-review-official-interior" not in body:
    raise RuntimeError("Review content or cabin photo lost")
if seo.get("robots",{}).get("index")!="index" or seo.get("canonical")!=live["link"] or not seo.get("og_image"):
    raise RuntimeError("Optra review index/canonical/social photo regressed")
print("EXPANDED_OPTRA_REVIEW_WITH_CAR_EXACT_IMAGES_CANONICAL_AND_INDEX_VERIFIED",count(body),"WORDS",live["link"],flush=True)
