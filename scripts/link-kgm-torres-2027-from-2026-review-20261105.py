#!/usr/bin/env python3
"""Precisely link the existing 2026 Torres review to published 2027 model, preserving its intent."""
import json,os,urllib.request,urllib.parse
SITE="https://a3tal.com"
BRIDGE=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
OLD_ID=81019
OLD_SLUG="ssangyong-kgm-torres-2026-review"
NEW_ID=85271
NEW_SLUG="kgm-torres-2027-egypt-price-trims-8speed"
NEW=SITE+"/"+NEW_SLUG+"/"
NOTE='<p><strong>تحديث 5 نوفمبر 2026:</strong> طرحت KGM مصر موديل <strong>توريس 2027 الفيس ليفت</strong> رسميًا بسعر يبدأ من <strong>1,650,000 جنيه</strong>، مع فتيس AISIN من 8 سرعات وعزم 300 نيوتن متر. المعلومات أدناه خاصة بموديل 2026؛ راجع <a href="'+NEW+'">أسعار ومواصفات KGM توريس 2027 وفروق الفئات الخمس</a> إذا كنت تبحث عن النسخة الجديدة.</p>'
def call(path,data=None):
 if not KEY:raise RuntimeError("Missing bridge credential")
 headers={"Accept":"application/json","User-Agent":"A3tal-Torres-Model-Year-Link-20261105","Cache-Control":"no-store","X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY}
 raw=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf-8")
 if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
 req=urllib.request.Request(BRIDGE+path,data=raw,headers=headers,method="POST" if raw is not None else "GET")
 with urllib.request.urlopen(req,timeout=140) as f:return json.load(f)
def main():
 new=call("/post/"+str(NEW_ID))
 if new.get("status")!="publish" or new.get("slug")!=NEW_SLUG or new.get("link")!=NEW or not new.get("featured_media"):
  raise RuntimeError("New model page not confirmed live")
 old=call("/post/"+str(OLD_ID))
 oldurl=SITE+"/"+OLD_SLUG+"/"
 if old.get("status")!="publish" or old.get("slug")!=OLD_SLUG or old.get("link")!=oldurl:
  raise RuntimeError("Existing 2026 review unexpected: refusing write")
 body=old.get("content")
 if not isinstance(body,str) or len(body)<3000:raise RuntimeError("Existing review unexpectedly short")
 if NEW in body:
  print("ALREADY_LINKED_2026_TO_2027",oldurl,NEW,flush=True);return
 updated=NOTE+"\n"+body
 result=call("/update-post",{"id":OLD_ID,"content":updated,"expected_modified_gmt":old["modified_gmt"]})
 if result.get("id")!=OLD_ID or result.get("slug")!=OLD_SLUG or NEW not in result.get("content",""):
  raise RuntimeError("Failed 2026 review link update validation")
 if result.get("featured_media")!=old.get("featured_media"):raise RuntimeError("Existing featured image unexpectedly changed")
 print("TORRES_YEAR_LINK_VERIFIED",oldurl,NEW,flush=True)
if __name__=="__main__":main()
