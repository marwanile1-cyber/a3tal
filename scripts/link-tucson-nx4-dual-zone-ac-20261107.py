#!/usr/bin/env python3
"""Bidirectional contextual links for published Tucson NX4 HVAC PSEO article.

One new dedicated symptom URL and two already-published Tucson model hubs.
Requires exact ID/slug/status, unchanged cover, revision token and live readback.
"""
import os,json,urllib.request,urllib.parse,time
SITE="https://a3tal.com"; API=SITE+"/wp-json/a3tal-direct/v1"; KEY=os.getenv("A3TAL_API_KEY","")
NEW=SITE+"/hyundai-tucson-nx4-dual-zone-ac-one-side-hot/"
PARENTS=[
 {"id":80744,"slug":"hyundai-tucson-nx4-electrical-screen-battery-problems",
  "add":'<p><strong>تحديث تشخيص أنظمة المقصورة:</strong> لو التكييف في توسان NX4 بارد من ناحية وساخن من ناحية الراكب، راجع <a href="'+NEW+'">خطوات فحص SYNC وبوابة خلط التكييف في توسان NX4</a> بدل تغيير الشاشة أو شحن الفريون بلا قياس.</p>'},
 {"id":84008,"slug":"hyundai-tucson-2027-prices-egypt",
  "add":'<p><strong>فحص التكييف قبل الاستلام:</strong> في الفئات التي تدعم Dual Zone جرّب تساوي حرارة الجانبين، واقرأ <a href="'+NEW+'">تشخيص اختلاف تبريد جهتي تكييف توسان NX4</a> إن لاحظت فرقًا واضحًا رغم تشغيل SYNC.</p>'},
 {"id":85284,"slug":"hyundai-tucson-nx4-dual-zone-ac-one-side-hot",
  "add":'<p>إذا كنت تختبر سيارة مستعملة أو تريد معرفة الأجزاء الكهربائية المرتبطة بالشاشة في NX4، راجع <a href="https://a3tal.com/hyundai-tucson-nx4-electrical-screen-battery-problems/">دليل كهرباء وشاشات توسان NX4</a> و<a href="https://a3tal.com/hyundai-tucson-2027-prices-egypt/">دليل فئات وأسعار توسان في مصر</a>، مع اختلاف تجهيزات السنوات والفئات.</p>'}
]
def req(path,payload=None):
 if not KEY:raise RuntimeError("A3TAL_API_KEY missing")
 h={"User-Agent":"A3tal-Nov07-Tucson-Context-Looking/1.0","Accept":"application/json","Cache-Control":"no-store","X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY}
 data=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf-8")
 if data is not None:h["Content-Type"]="application/json; charset=utf-8"
 with urllib.request.urlopen(urllib.request.Request(API+path,data=data,headers=h,method="POST" if data is not None else "GET"),timeout=140) as r:return json.load(r)
def main():
 new=req("/post/85284")
 if new.get("link")!=NEW or new.get("status")!="publish" or not new.get("featured_media"):raise RuntimeError("PSEO page missing")
 for row in PARENTS:
  old=req("/post/"+str(row["id"]))
  if old.get("id")!=row["id"] or old.get("slug")!=row["slug"] or old.get("status")!="publish" or not old.get("featured_media"):
   raise RuntimeError("Unsafe hub identity or featured media "+row["slug"])
  content=old.get("content","")
  if not isinstance(content,str) or len(content)<2800:raise RuntimeError("Parent post unexpectedly short")
  anchor=(NEW if row["id"]!=85284 else "https://a3tal.com/hyundai-tucson-nx4-electrical-screen-battery-problems/")
  if anchor in content:
   print("TUCSON_CONTEXT_ALREADY_LINKED",old["link"],flush=True);continue
  before=old.get("modified_gmt")
  newcontent=content.rstrip()+"\n"+row["add"]
  response=req("/update-post",{"id":row["id"],"expected_modified_gmt":before,"content":newcontent})
  if response.get("error") or response.get("ok") is False:raise RuntimeError("Bridge rejected link "+row["slug"])
  checked=req("/post/"+str(row["id"]))
  if checked.get("slug")!=row["slug"] or checked.get("status")!="publish" or checked.get("featured_media")!=old.get("featured_media") or anchor not in checked.get("content",""):
   raise RuntimeError("Link verification failed "+row["slug"])
  print("TUCSON_CONTEXT_LINK_VERIFIED",checked["link"],anchor,flush=True)
 print("A3TAL_TUCSON_CONTEXT_LINKS_NOV07_COMPLETE",flush=True)
if __name__=="__main__":main()
