#!/usr/bin/env python3
"""Batch 15 REAL PSEO publisher for /car-reference/{brand}/{model}/{spec}/.

Uses proven batch 12 image/upsert/SEO-verification publisher, with a dedicated
thirty-record, source-matched engine and maintenance dataset across five verified existing model hubs.
Never publishes regular blog posts and never creates duplicate model pages.
"""
from pathlib import Path
import os,types
oldpath=Path("scripts/publish-car-reference-batch12-18-pages.py")
src=oldpath.read_text("utf-8")
def change(a,b):
 global src
 if src.count(a)!=1:
  raise RuntimeError("Batch12 safety template drift for "+a[:70])
 src=src.replace(a,b,1)
change('data/car-reference/batch-12-18-technical-references-20261104.json',
       'data/car-reference/batch-15-technical-specs-official-20261107.json')
change('car-reference-batch12-', 'car-reference-batch15-')
change('ACCENTS={"captiva":(87,148,176),"mg-gt":(198,103,83),"mg7":(81,148,126)}',
       'ACCENTS={"cerato-bd-technical":(70,160,192),"seltos-sp2-technical":(78,157,190),"sportage-nq5-technical":(81,148,188),"elantra-cn7-technical":(79,159,199),"tucson-nx4e-technical":(75,154,208)}')
change('MARK_NAMES={"captiva":"CHEVROLET CAPTIVA 2026","mg-gt":"MG GT 1.5T","mg7":"MG7 1.5T"}',
       'MARK_NAMES={"cerato-bd-technical":"KIA CERATO BD 2023","seltos-sp2-technical":"KIA SELTOS SP2 2023","sportage-nq5-technical":"KIA SPORTAGE NQ5 2023","elantra-cn7-technical":"HYUNDAI ELANTRA CN7 2025","tucson-nx4e-technical":"HYUNDAI TUCSON NX4e 2025"}')
change('assert len(DB["clusters"])==3 and len(ITEMS)==6',
       'assert len(DB["clusters"])==5 and 2<=len(ITEMS)<=8')
change('assert len({p["slug"] for _,p,_ in ITEMS})==6',
       'assert len({p["slug"] for _,p,_ in ITEMS})==len(ITEMS)')
change('cap=max(1,min(6,int(os.getenv("A3CR_LIMIT","1"))))',
       'cap=min(len(ITEMS),max(1,int(os.getenv("A3CR_LIMIT","6"))))')
change('"a3tal-b12-"+FAMILY+"-"+slug+".webp"',
       '"a3tal-b15-"+FAMILY+"-"+slug+".webp"')
change('seed=[(0.44,0.49),(0.5,0.5),(0.54,0.52),(0.47,0.55),(0.51,0.43),(0.58,0.47)][i]', 'seed=[(0.44,0.49),(0.5,0.5),(0.54,0.52),(0.47,0.55),(0.51,0.43),(0.58,0.47)][i%6]')
change('"reviewed_at":"2026-11-04"',
       '"reviewed_at":"2026-11-07"')
# The source script generates standalone visible HTML with one specific data table;
# improve the distinct practical usage per specification, without changing published model hubs.
change('def spec_content(row):\n    return (',
'''CATEGORY_NAMES.update({"bulb-specs":"لمبات السيارة حسب تجهيز الفانوس",
    "fuse-specs":"جدول أمبيرات الفيوزات",
    "safety-specs":"وسائل الأمان النشطة والسلبية",
    "trim-features":"فروق فئات التجهيز",
    "exterior-specs":"الجنوط والإضاءة الخارجية","interior-specs":"تجهيزات المقصورة والمقاعد","chassis-specs":"نظام التعليق والشاسيه","ac-refrigerant":"فريون التكييف وزيت الكمبروسر","fuel-tank":"سعة تانك الوقود","brake-fluid":"سائل الفرامل","coolant":"سعة دورة التبريد","dimensions":"أبعاد الهيكل ومقاساته","transmission-oil":"مواصفات زيت الفتيس","engine-oil":"كمية زيت المحرك"})
def spec_content(row):
    return (''')
change('''"<h2>الجيل والفئة والسوق الصحيح</h2>"
      "<p>هذه البيانات محددة''',
'''"<h2>أخطاء شائعة عند استخدام جدول المواصفات</h2>"
      "<p>الاسم التجاري وحده لا يثبت مطابقة قطعة الغيار أو وجود الميزة في كل فئة؛ "
      "تجنّب نقل تجهيزات الفئة الأعلى أو مواصفات سوق مختلف إلى السيارة المعنية. "
      "عند شكّ في الفانوس أو الفيوز أو تجهيز إلكتروني، طابق الملصق والقطعة الفعلية "
      "ووثيقة الشركة، ولا تلجأ للتجربة بتوصيل أجزاء مختلفة.</p>"
      "<h2>الجيل والفئة والسوق الصحيح</h2>"
      "<p>هذه البيانات محددة''')
# Add description of why verified record exists instead of generic short teaser.
change('''"excerpt":"مواصفات فنية موثقة من المصدر الرسمي للموديل المصري، مع اختلاف الفئات وتنبيهات الصيانة.",''',
''' "excerpt":(row.get("intro","")[:165] if kind=="spec" else "دليل المواصفات الفنية الرسمية لهذا الموديل، مع فروق المحرك والفئة والسوق."),''')
# Correct the batch trace name without changing underlying post content.
change('print("COMPLETE",FAMILY,len(PROGRESS),flush=True)',
       'print("A3TAL_CAR_REFERENCE_BATCH15_COMPLETE",FAMILY,len(PROGRESS),flush=True)')
module=types.ModuleType("a3tal_real_pseo_batch13")
module.__file__=str(oldpath)
exec(compile(src,str(oldpath),"exec"),module.__dict__)
if __name__=="__main__":
 module.main()
