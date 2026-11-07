#!/usr/bin/env python3
"""Inject one highly relevant link from each existing main guide to each new November 7 article.
Preserve every old URL, post category, Yoast and featured image. Revision guarded.
"""
import json,os,urllib.request
SITE="https://a3tal.com"; BRIDGE=SITE+"/wp-json/a3tal-direct/v1"; KEY=os.environ.get("A3TAL_API_KEY","")
ROWS=[
(81076,"car-ac-complete-maintenance-guide",85294,"car-ac-musty-smell-first-start-diagnosis",
 'لو تكييف العربية بيطلع ريحة عفن عند أول تشغيل، ابدأ من <a href="https://a3tal.com/car-ac-musty-smell-first-start-diagnosis/">تشخيص رائحة الرطوبة وفلتر المقصورة وصرف المبخر</a> بدل شحن الفريون عشوائيًا.'),
(81930,"p0507-high-idle-rpm-diagnosis",85298,"car-stalls-after-throttle-body-cleaning-idle-relearn",
 'لو الموتور بيفصل أو سلانسية العربية بتتلخبط تحديدًا <strong>بعد تنظيف بوابة الهواء</strong>، راجع <a href="https://a3tal.com/car-stalls-after-throttle-body-cleaning-idle-relearn/">دليل فحص الفيش والتسريب وإعادة تعلم الخمول</a>.'),
(83151,"motorcycle-maintenance-schedule-guide",85302,"motorcycle-hard-gear-shifting-clutch-cable-diagnosis",
 'لو نقلات الموتوسيكل تقيلة أو الحياد مش بيدخل بسهولة، شوف <a href="https://a3tal.com/motorcycle-hard-gear-shifting-clutch-cable-diagnosis/">تشخيص سلك الدبرياج والدواسة والفتيس قبل فك المحرك</a>.'),
(80581,"hyundai-elantra-suspension-maintenance-guide",85306,"hyundai-elantra-ad-eps-warning-heavy-steering",
 'لو عندك <strong>إلنترا AD</strong> ولمبة EPS منورة والدركسيون تقيل، راجع <a href="https://a3tal.com/hyundai-elantra-ad-eps-warning-heavy-steering/">دليل فحص الباور الكهربائي وتحذير EPS الخاص بجيل AD</a> قبل تغيير الاسكترا.')
]
def call(path,payload=None):
 if not KEY:raise RuntimeError("Missing scoped Bridge secret")
 headers={"Accept":"application/json","X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Cache-Control":"no-store","User-Agent":"A3tal-Nov07-Context-Links"}
 raw=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf8")
 if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
 request=urllib.request.Request(BRIDGE+path,data=raw,headers=headers,method="POST" if raw is not None else "GET")
 with urllib.request.urlopen(request,timeout=120) as r:return json.load(r)
for old_id,old_slug,new_id,new_slug,description in ROWS:
 new=call("/post/"+str(new_id))
 url=SITE+"/"+new_slug+"/"
 if new.get("status")!="publish" or new.get("slug")!=new_slug or new.get("link")!=url or not new.get("featured_media"):
  raise RuntimeError("New guide not fully live "+new_slug)
 old=call("/post/"+str(old_id))
 if old.get("status")!="publish" or old.get("slug")!=old_slug or old.get("link")!=SITE+"/"+old_slug+"/" or not old.get("featured_media"):
  raise RuntimeError("Unexpected existing source "+old_slug)
 content=old.get("content","")
 if not isinstance(content,str) or len(content)<1800:raise RuntimeError("Suspicious source length "+old_slug)
 if url in content:
  print("NOV07_INTERNAL_LINK_ALREADY_PRESENT",old_slug,url,flush=True);continue
 patch=content.rstrip()+"\n<p><strong>دليل تشخيص متخصص:</strong> "+description+"</p>"
 result=call("/update-post",{"id":old_id,"content":patch,"expected_modified_gmt":old["modified_gmt"]})
 if result.get("error") or result.get("ok") is False:raise RuntimeError("Bridge declined link update "+old_slug)
 after=call("/post/"+str(old_id))
 if after.get("slug")!=old_slug or after.get("status")!="publish" or after.get("featured_media")!=old.get("featured_media") or url not in after.get("content",""):
  raise RuntimeError("Unexpected hub identity or link readback "+old_slug)
 print("NOV07_CONTEXT_LINK_VERIFIED",old["link"],url,flush=True)
print("A3TAL_NOV07_FOUR_INBOUND_LINKS_COMPLETE",flush=True)
