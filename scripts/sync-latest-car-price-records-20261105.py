#!/usr/bin/env python3
"""One-time audited entity linking for verified November 2026 Egypt car price stories.

Creates (or checks) source-backed, noindex car catalogue records, each tied to its
own existing canonical editorial price guide and actual featured image.
Never overwrites unrelated vehicle records or fabricates a new indexed SEO article.
"""
import json,os,urllib.parse,urllib.request
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types

m=types.ModuleType("a3tal_bridge_vehicle_linker")
SourceFileLoader(m.__name__,"scripts/deploy-dtc-library.py").exec_module(m)
Bridge=m.Bridge
BASE="https://a3tal.com"
CARS=[
 {"slug":"kgm-torres-2027-egypt","brand":"kgm","brand_name":"KGM","title":"KGM توريس 2027 في مصر","post_id":85271,"post_slug":"kgm-torres-2027-egypt-price-trims-8speed","media":85272,"price_min":1650000,"price_max":2075000,"notes":"خمس فئات مصرية مع موتور 163 حصانًا وناقل AISIN من 8 سرعات؛ تفاصيل التجهيزات والأسعار المتغيرة في الدليل الأصلي."},
 {"slug":"renault-boreal-2027-egypt","brand":"renault","brand_name":"Renault","title":"رينو بوريال 2027 في مصر","post_id":84943,"post_slug":"renault-boreal-2027-egypt-price-trims","media":84944,"price_min":1470000,"price_max":1690000,"notes":"موديل بوريال المطروح في مصر بفئات Evolution وTechno وIconic. راجع تفاصيل الأسعار المؤرخة والفتيس والمواصفات بالمقال الأصلي."},
 {"slug":"jetour-t2-idm-4x4-2027-egypt","brand":"jetour","brand_name":"Jetour","title":"جيتور T2 i-DM 4x4 موديل 2027 في مصر","post_id":85078,"post_slug":"jetour-t2-idm-4x4-2027-egypt-price-specs","media":85079,"price_min":2300000,"price_max":2300000,"notes":"نسخة T2 i-DM بالدفع الرباعي التي أعلن عنها في نوفمبر 2026 بسعر 2.3 مليون جنيه، مختلفة عن نسخة T2 الأخرى."}
]
def public(path):
 req=urllib.request.Request(BASE+path,headers={"Accept":"application/json","Cache-Control":"no-store","User-Agent":"A3tal-Linked-Cars-20261105/1.0"})
 with urllib.request.urlopen(req,timeout=55) as f:return json.load(f)
def exact_record(slug):
 rows=public("/wp-json/wp/v2/a3tal-cars?"+urllib.parse.urlencode({"slug":slug,"per_page":10,"_fields":"id,slug,title,link,featured_media,status"}))
 if len(rows)>1:raise RuntimeError("Multiple car records for "+slug)
 return rows[0] if rows else None
def validate_sources():
 for c in CARS:
  p=public("/wp-json/wp/v2/posts/"+str(c["post_id"])+"?_fields=id,slug,status,featured_media,link,content,yoast_head_json")
  canonical=BASE+"/"+c["post_slug"]+"/"
  html=(p.get("content") or {}).get("rendered","")
  if (p.get("status")!="publish" or p.get("slug")!=c["post_slug"] or p.get("featured_media")!=c["media"]
      or p.get("link")!=canonical or (p.get("yoast_head_json") or {}).get("canonical")!=canonical
      or ("2027" not in html or not (str(c["price_min"]) in html or f'{c["price_min"]:,}' in html))):
   raise RuntimeError("Source guide failed identity/price/media/canonical QA: "+c["slug"])
  old=exact_record(c["slug"])
  if old and (old.get("status")!="publish" or old.get("featured_media")!=c["media"]):
   raise RuntimeError("Existing record cannot be silently changed: "+c["slug"])
  c["existing"]=old
  print("PRICE_SOURCE_VERIFIED",c["post_id"],canonical,"existing_car",old["id"] if old else 0,flush=True)
def brand_term(slug):
 rows=public("/wp-json/wp/v2/a3_brand?"+urllib.parse.urlencode({"slug":slug,"_fields":"id,name,slug"}))
 if len(rows)>1:raise RuntimeError("Duplicate brand slug: "+slug)
 return rows[0] if rows else None
def ensure_brand(b,c):
 if brand_term(b):
  print("BRAND_EXISTS",b,flush=True);return
 try:
  r=c.request({"op":"term_upsert","taxonomy":"a3_brand","slug":b,"name":next(x["brand_name"] for x in CARS if x["brand"]==b),"confirm":True},write=True)
  print("BRAND_CREATED",b, r.get("term_id",""),flush=True)
 except RuntimeError as error:
  # Mutations are never blindly repeated. Verify whether a response was lost.
  if not brand_term(b):raise
  print("BRAND_WRITE_READBACK_CONFIRMED",b,flush=True)
 if not brand_term(b):raise RuntimeError("Brand missing after write: "+b)
def record_payload(c):
 slug=c["slug"];url=BASE+"/"+c["post_slug"]+"/"
 body=('<p>'+c["notes"]+'</p><p><strong>السعر الرسمي المسجل وقت المراجعة: '
       +f'{c["price_min"]:,}'+' جنيه'
       +(f' إلى {c["price_max"]:,} جنيه' if c["price_max"]!=c["price_min"] else '')
       +'.</strong> تاريخ التحقق: 5 نوفمبر 2026.</p>'
       +'<p>هذا سجل بيانات لتصفح الموديلات وليس مقال أسعار جديدًا. '
       +'<a href="'+url+'">افتح دليل سعر ومواصفات '+c["title"]+' الكامل والمصدر</a>. '
       +'تحقق من السعر الحالي لدى الوكيل قبل الشراء.</p>')
 return {"op":"platform_entity_upsert","type":"a3_car","title":c["title"],"slug":slug,"status":"publish",
         "content":body,"excerpt":"سجل موديل مرتبط بالمقال المنشور والتحقق التاريخي للأسعار؛ التفاصيل الكاملة في الدليل الأصلي.",
         "taxonomies":{"a3_brand":[c["brand"]],"a3_market":["egypt"],"a3_car_body":["suv"]},
         "featured_media":c["media"],
         "meta":{"_a3_year":2027,"_a3_price_min":c["price_min"],"_a3_price_max":c["price_max"],
                 "_a3_related_post_ids":str(c["post_id"]),
                 "_a3_primary_price_post_id":str(c["post_id"]),
                 "_a3_source_checked_at":"2026-11-05",
                 "_a3_source_url":url,"_a3_entity_stub":"1",
                 "_yoast_wpseo_meta-robots-noindex":"1"},
         "confirm":True,"dangerous":True}
def verify(c):
 p=exact_record(c["slug"])
 if not p or not p.get("featured_media")==c["media"] or p.get("status")!="publish":
  raise RuntimeError("Linked model missing/without cover: "+c["slug"])
 if c.get("existing") and p["id"]!=c["existing"]["id"]:
  raise RuntimeError("Existing model record ID changed")
 link=p.get("link","")
 if link!=BASE+"/cars/"+c["slug"]+"/":raise RuntimeError("Unexpected model permalink "+link)
 # Existing A3tal car template owns robots. These are intentionally non-indexed,
 # leaving the substantive price article as the only indexable landing page.
 print("MODEL_RECORD_LIVE_VERIFIED",p["id"],link,"SOURCE_ARTICLE",c["post_id"],flush=True)
def main():
 if not os.getenv("A3TAL_API_KEY"):raise RuntimeError("Missing GitHub-scoped bridge credential")
 validate_sources()
 api=Bridge()
 for b in dict.fromkeys(x["brand"] for x in CARS):ensure_brand(b,api)
 for c in CARS:
  if c.get("existing"):
   # Idempotency: verify stored related post relationship instead of replacing unknown content.
   raw=api.request({"op":"post_meta","post_id":c["existing"]["id"],"key":"_a3_primary_price_post_id"})
   if str(raw.get("_a3_primary_price_post_id",""))!=str(c["post_id"]):
    raise RuntimeError("Existing car has a different primary article; manual review: "+c["slug"])
   print("MODEL_ALREADY_LINKED",c["slug"],flush=True)
  else:
   try:
    result=api.request(record_payload(c),write=True)
    print("MODEL_RECORD_CREATED",c["slug"],result.get("id"),flush=True)
   except RuntimeError:
    if not exact_record(c["slug"]):raise
    print("AMBIGUOUS_RECORD_WRITE_READBACK",c["slug"],flush=True)
  verify(c)
 print("A3TAL_THREE_LATEST_CAR_ARTICLE_LINKS_COMPLETE",flush=True)
if __name__=="__main__":main()
