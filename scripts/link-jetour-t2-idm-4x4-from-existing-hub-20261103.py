#!/usr/bin/env python3
"""Non-destructive update to legacy Jetour T2 2027 hub. Link newly announced 4x4 PHEV page."""
import json,os,urllib.request,urllib.parse
ROOT="https://a3tal.com"
API=ROOT+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
ID=81139
HUB=ROOT+"/jetour-t2-egypt-review-specs-price/"
NEW=ROOT+"/jetour-t2-idm-4x4-2027-egypt-price-specs/"
NOTE='<p><strong>تحديث 3 نوفمبر 2026:</strong> أطلق الوكيل فئة <strong>جيتور T2 i-DM 4x4 موديل 2027</strong> بسعر 2,300,000 جنيه، وبطارية 43.24 كيلووات/ساعة وقوة مجمعة معلنة نحو 600 حصان. هذه نسخة مختلفة عن T2 i-DM السابقة ذات السعر 2,150,000 جنيه. تعرف على <a href="'+NEW+'">سعر ومواصفات جيتور T2 i-DM 4x4 الجديدة والفرق بين الفئتين</a>، وتابع هنا دليل العائلة العام.</p>'
def call(path,method="GET",payload=None):
  h={"User-Agent":"A3tal-Jetour-Internal-Link-20261103","Accept":"application/json","X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Cache-Control":"no-store"}
  raw=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf8")
  if raw is not None:h["Content-Type"]="application/json"
  req=urllib.request.Request(API+path,headers=h,method=method,data=raw)
  with urllib.request.urlopen(req,timeout=140) as f:return json.load(f)
def main():
  if not KEY:raise RuntimeError("Missing bridge credential")
  # A positive live check ensures we never link to an un-published draft.
  req=urllib.request.Request(ROOT+"/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":"jetour-t2-idm-4x4-2027-egypt-price-specs","_fields":"id,status,link,featured_media"}))
  with urllib.request.urlopen(req,timeout=45) as f:published=json.load(f)
  if len(published)!=1 or published[0]["status"]!="publish" or not published[0]["featured_media"]:raise RuntimeError("New variant page is not fully published")
  post=call("/post/"+str(ID))
  if post["slug"]!="jetour-t2-egypt-review-specs-price" or post["status"]!="publish" or post["link"]!=HUB:
    raise RuntimeError("Unexpected hub post; no mutation")
  content=post["content"]
  if NEW in content:
    print("HUB_ALREADY_LINKED",HUB,flush=True);return
  if len(content)<4000:raise RuntimeError("Hub content unexpectedly short")
  updated=NOTE+"\n"+content
  result=call("/update-post",method="POST",payload={"id":ID,"content":updated,"expected_modified_gmt":post["modified_gmt"]})
  if result.get("id")!=ID or result.get("slug")!="jetour-t2-egypt-review-specs-price" or NEW not in result.get("content",""):
    raise RuntimeError("Post update did not preserve hub content/link")
  if result.get("featured_media")!=post.get("featured_media"):raise RuntimeError("Hub featured media changed")
  print("HUB_LINK_PUBLISHED",HUB,NEW,flush=True)
if __name__=="__main__":main()
