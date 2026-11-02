#!/usr/bin/env python3
"""Publish six user-value Kia tire/brake/AWD references. Only sources verified
against Kia manuals. Each article gets its own premium WebP photographic art.
Pilot first; subsequent reruns are idempotent, never duplicate pages.
"""
import base64
import importlib.util
import json
import os
import re
import time
from html import escape
from pathlib import Path

import requests

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/"data/car-reference/batch-03-kia-tires-safety-awd-20261102.json").read_text(encoding="utf-8"))
source=importlib.util.spec_from_file_location("premium_kia",ROOT/"scripts/publish-car-reference-batch02-premium.py")
p=importlib.util.module_from_spec(source)
source.loader.exec_module(p)
SITE="https://a3tal.com"
HEAD={"X-A3tal-Key":os.environ["A3TAL_API_KEY"],"Content-Type":"application/json"}
SESSION=requests.Session()
RESULTS=[]
REPORT=ROOT/"kia-reference-batch03-published-images.json"

def get_record(slug):
    r=SESSION.get(SITE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":20},timeout=45)
    r.raise_for_status()
    return [x for x in r.json() if x.get("slug")==slug]

def publish_entry(row,photo_id):
    model=CONFIG["models"][row["model"]]
    facts=[{"label":l,"value":v} for l,v in row["facts"]]
    details = "<ul>"+ "".join("<li><strong>"+escape(l)+"</strong>: "+escape(v)+"</li>" for l,v in row["facts"]) +"</ul>"
    is_tires=row["category"]=="tire-specs"
    title2="مقاسات الإطارات وضغط الهواء" if is_tires else "المواصفة الفنية بحسب التجهيز"
    content=(
      "<p>"+escape(row["intro"])+"</p>"
      "<h2>"+title2+"</h2>"
      "<p>"+escape(row["detail"])+"</p>"
      "<h2>متى تختلف المواصفة عن سيارة أخرى؟</h2>"
      "<p>"+escape(row["warning"])+"</p>"
      "<h2>قبل شراء القطعة أو بدء الصيانة</h2>"
      "<p>راجع سنة الطراز، وفئة المحرك، ونوع ناقل الحركة، وملصق السيارة أو دليل المالك. "
      "إذا كانت تجهيزات السيارة مختلفة عن النسخة الواردة بالدليل فلا تعتمد على هذه الأرقام وحدها. "
      "القيم المعروضة مرجع للمقارنة والتحقق، وليست بديلًا عن إجراءات الفحص الفني.</p>"
      "<p><strong>المرجع الرسمي:</strong> <a href='"+escape(model["source"],quote=True)+
      "' rel='nofollow noopener noreferrer'>جدول المواصفات في دليل كيا "+escape(model["name"])+"</a>.</p>"
    )
    return {
      "title":row["title"],"slug":row["slug"],"kind":"spec",
      "parent_path":"kia/"+row["model"],"status":"publish","featured_image_id":photo_id,
      "content":content,
      "excerpt":"بيانات فنية دقيقة من دليل المالك الرسمي لكيا 2023، مع التنبيهات المهمة عند اختلاف الفئة والسوق.",
      "data":{"kind":"spec","years":"2023","engine":row["engine"],"category":row["category"],
       "market":"نسخة دليل كيا الرسمي 2023؛ تحقق من الملصق والفئة والسوق",
       "reviewed_at":"2026-11-02","facts":facts,
       "sources":[{"title":"دليل المالك الرسمي "+model["name"],"url":u} for u in row["sources"]]},
      "meta_title":row["title"]+" | أعطال.كوم",
      "meta_description":("تعرف على "+row["title"]+" وفق دليل المالك الرسمي لكيا؛ المقاسات والسعات والتنبيهات المهمة حسب نسخة السيارة.")[:155]
    }

def photo_design(row):
    m=CONFIG["models"][row["model"]]
    t,number,desc=row["visual"]
    if row["category"]=="tire-specs":
        desc="15 / 16 / 17" if "cerato" in row["model"] else ("16 / 17 / 18" if "seltos" in row["model"] else "17 / 18 / 19")
    accent={"tire-specs":(47,191,227),"brake-fluid":(228,98,85),"transfer-case-oil":(241,171,82)}[row["category"]]
    num=0 if row["category"]=="tire-specs" else (1 if row["category"]=="brake-fluid" else 2)
    # Distinct technical art per page, retaining the correct Kia vehicle model.
    p.DESIGNS[row["slug"]]=(m["hero"],m["name"],t,number,desc,accent,num)
    b=p.make_art(row["slug"])
    if len(b)<50000: raise RuntimeError("Low-resolution artwork rejected "+row["slug"])
    return b

def main():
    assert len(CONFIG["items"])==6
    assert len({x["slug"] for x in CONFIG["items"]})==6
    cap=max(1,min(6,int(os.getenv("A3CR_LIMIT","6"))))
    print("Kia reference premium batch3 cap",cap,flush=True)
    try:
      for row in CONFIG["items"][:cap]:
        slug=row["slug"]
        model=CONFIG["models"][row["model"]]
        live=[x for x in get_record(slug) if x.get("status")=="publish"]
        expected=SITE+"/car-reference/kia/"+row["model"]+"/"+slug+"/"
        if live:
            if len(live)!=1 or live[0].get("link","").rstrip("/")!=expected.rstrip("/"):
                raise RuntimeError("Existing conflicting URL "+slug)
            print("SKIP already live",expected,flush=True)
            RESULTS.append({"slug":slug,"url":expected,"status":"existing"})
            continue
        # Preserve only documents whose original manufacturer reference is accessible.
        src=SESSION.get(model["source"],timeout=45)
        if not src.ok or "كيا" not in src.text and "الإطارات" not in src.text and "سائل" not in src.text and "مواد التشحيم" not in src.text:
            raise RuntimeError("Manufacturer source not accessible for "+slug)
        raw=photo_design(row)
        filename="a3tal-kia-guide-2023-"+slug+".webp"
        media=p.req(p.BRIDGE+"/upload-image-data",{"filename":filename,
           "image_base64":base64.b64encode(raw).decode("ascii"),
           "title":row["title"],"alt":row["title"]+" - تصميم حصري لموسوعة أعطال.كوم",
           "convert_webp":False})
        media_id=int(media.get("media_id") or 0)
        if not media_id or not media.get("url","").endswith(".webp"):
            raise RuntimeError("Image upload missing ID/URL "+slug)
        entry=publish_entry(row,media_id)
        try:
            response=p.req(p.UPSERT,{"items":[entry]})
        except requests.RequestException:
            # A dropped connection can happen after WordPress committed the post.
            # Recheck the stable slug before retrying, preventing duplicates.
            time.sleep(3)
            after=[x for x in get_record(slug) if x.get("status")=="publish"]
            if len(after)==1 and after[0].get("link","").rstrip("/")==expected.rstrip("/"):
                response={"results":[{"ok":True,"status":"publish","id":after[0]["id"],"url":expected}]}
            else:
                response=p.req(p.UPSERT,{"items":[entry]})
        results=response.get("results") or []
        if len(results)!=1 or not results[0].get("ok") or results[0].get("status")!="publish":
            raise RuntimeError("Upsert failed "+slug+" "+repr(results)[:300])
        real_url=results[0].get("url","")
        if real_url.rstrip("/") != expected.rstrip("/"):
            raise RuntimeError("Unexpected permalink "+real_url+" expected "+expected)
        p.verify(expected,media["url"],row["title"])
        print("PUBLISHED PHOTO VERIFIED",slug,real_url,media_id,flush=True)
        RESULTS.append({"slug":slug,"status":"published","post_id":results[0]["id"],
                        "url":real_url,"image_url":media["url"],"media_id":media_id,
                        "canonical_checked":True,"og_image_checked":True})
    finally:
      REPORT.write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2),encoding="utf-8")
    assert len(RESULTS)==cap
    print("BATCH COMPLETE",len(RESULTS),flush=True)

if __name__=="__main__":
    main()
