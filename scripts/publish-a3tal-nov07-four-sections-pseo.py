#!/usr/bin/env python3
"""A3tal 2026-11-07: four distinct editorial articles including model-specific PSEO.
Protected bridge, comprehensive duplicate/featured/OG/Yoast checks; no WPWriter.
Licensed photos are subject-specific and attributed, not claimed as AI-original.
"""
import types
from pathlib import Path
original=Path("scripts/publish-pseo-symptoms-20261105.py")
code=original.read_text("utf-8")
needle='category_map={"عفشة":(11,"نظام التعليق"),"ميكانيكا":(9,"مشاكل المحرك"),"كهربا":(13,"أعطال كهربائية")}'
assert code.count(needle)==1, "Publisher category map changed"
code=code.replace(needle,needle.replace('{"عفشة":','{"موتوسيكلات":(3028,"دليل الموتوسيكلات"),"عفشة":'),1)
publisher=types.ModuleType("a3tal_guarded_publish_nov07")
publisher.__file__=str(original)
exec(compile(code,str(original),"exec"),publisher.__dict__)
publisher.POSTS=[
 {
  "slug":"car-ac-musty-smell-first-start-diagnosis",
  "file":"data/editorial/20261107/car-ac-musty-smell-first-start-diagnosis.html",
  "title":"ريحة عفن من تكييف العربية أول ما يشتغل؟ الفلتر وصرف المبخر قبل التعقيم",
  "excerpt":"ريحة رطوبة من تكييف السيارة أول التشغيل أو بعد ركنة؟ اعرف الفرق بين فلتر المقصورة وصرف المبخر ومياه الموكيت ومتى تحتاج تنظيف متخصص.",
  "focus":"ريحة عفن من تكييف العربية",
  "category":"تكييف",
  "checks":["ريحة رطوبة","فلتر التكييف","{{a3tal_image:detail}}"],
  "dedup":["ريحة عفن من تكييف العربية","ريحة رطوبة التكييف أول تشغيل"],
  "match":["ريحة","تكييف","عفن"],
  "photo":[
    [("A dirty cabin filter.jpg","UnifiedFunctionality","CC BY-SA 4.0")],
    [("Filtro abitacolo.JPG","A7N8X","CC BY-SA 4.0")]
  ],
  "alt":[
    "صورة حقيقية لفلتر تكييف مقصورة متسخ يساعد على تشخيص رائحة الرطوبة عند بداية تشغيل التكييف",
    "مقارنة فوتوغرافية لفلتر مقصورة مستعمل وآخر جديد لمعرفة تأثير الأتربة والرطوبة"
  ]
 },
 {
  "slug":"car-stalls-after-throttle-body-cleaning-idle-relearn",
  "file":"data/editorial/20261107/car-stalls-after-throttle-body-cleaning-idle-relearn.html",
  "title":"العربية بتفصل بعد تنظيف بوابة الهواء؟ فحص السلانسية والتعلم والفيش",
  "excerpt":"الموتور بيفصل على السلانسية أو RPM بيعلى بعد تنظيف بوابة الهواء؟ خطوات فحص الخرطوم والفيش وإجراء Idle Relearn الصحيح قبل تغيير البوابة.",
  "focus":"العربية بتفصل بعد تنظيف بوابة الهواء",
  "category":"ميكانيكا",
  "checks":["بوابة الهواء","Idle Relearn","{{a3tal_image:detail}}"],
  "dedup":["بتفصل بعد تنظيف بوابة الهواء","سلانسية بعد تنظيف البوابة"],
  "match":["تنظيف","بوابة","بعد"],
  "photo":[
   [("Car engine part shows details of throttle body and surrounding components during a repair in a garage.jpg","Shixart1985","CC BY 2.0")],
   [("Throttle and Engine Inlet.jpg","Musay16","CC BY-SA 4.0")]
  ],
  "alt":[
    "صورة فوتوغرافية حقيقية لفني يفحص بوابة الهواء بالمحرك بعد عملية التنظيف",
    "تفاصيل حقيقية لبوابة الهواء ومدخل المحرك لتوضيح احتمال فصل السيارة بسبب الخمول أو التسريب"
  ]
 },
 {
  "slug":"motorcycle-hard-gear-shifting-clutch-cable-diagnosis",
  "file":"data/editorial/20261107/motorcycle-hard-gear-shifting-clutch-cable-diagnosis.html",
  "title":"دواسة غيارات الموتوسيكل تقيلة؟ فحص سلك الدبرياج والحياد قبل فتح الفتيس",
  "excerpt":"الغيارات تقيلة في الموتوسيكل أو الحياد N مش بيدخل؟ اعرف دور Freeplay وسلك الدبرياج والزيت ووصلة الغيارات وخطوات التشخيص قبل فتح الموتور.",
  "focus":"دواسة غيارات الموتوسيكل تقيلة",
  "category":"موتوسيكلات",
  "checks":["دواسة غيارات","Freeplay","{{a3tal_image:detail}}"],
  "dedup":["دواسة غيارات الموتوسيكل تقيلة","الموتوسيكل نقلات الغيار صعبة"],
  "match":["الموتوسيكل","غيارات","تقيلة"],
  "photo":[
    [("Motorcycle clutch.jpg","Gérard Delafond","CC BY-SA 3.0")],
    [("Gearbox.jpg","Gérard Delafond","CC BY-SA 3.0")]
  ],
  "alt":[
    "صورة حقيقية لمجموعة دبرياج موتوسيكل توضح مكونًا من أسباب صعوبة نقل الغيارات",
    "صورة فوتوغرافية حقيقية لفتيس موتوسيكل ياماها مفكوك توضح منطقة التروس والتعشيق"
  ]
 },
 {
  "slug":"hyundai-elantra-ad-eps-warning-heavy-steering",
  "file":"data/editorial/pseo-20261107/hyundai-elantra-ad-eps-warning-heavy-steering.html",
  "title":"لمبة EPS في هيونداي إلنترا AD والدركسيون تقيل؟ فحص الباور قبل تغيير الاسكترا",
  "excerpt":"الدركسيون في إلنترا AD بقى تقيل مع لمبة EPS؟ فحص التغذية والأرضي وأكواد EPS، وتوضيح استدعاء أمريكي محدود لا يشمل كل سيارات مصر.",
  "focus":"لمبة EPS إلنترا AD والدركسيون تقيل",
  "category":"كهربا",
  "checks":["إلنترا AD","EPS","{{a3tal_image:detail}}"],
  "dedup":["إلنترا AD EPS تقيل","لمبة EPS إلنترا AD"],
  "match":["إلنترا","AD","EPS"],
  "photo":[
    [("2017 Hyundai Elantra (AD) front 3.25.18.jpg","Kevauto","CC BY-SA 4.0")],
    [("2017 Hyundai Elantra (AD) Elite sedan (2017-12-09) 01.jpg","EurovisionNim","CC BY-SA 4.0")]
  ],
  "alt":[
    "هيونداي إلنترا AD موديل 2017 بصورة فوتوغرافية حقيقية لتوضيح السيارة المعنية بعطل EPS",
    "صورة حقيقية ثانية لإلنترا AD من تجهيز خارجي مختلف ضمن شرح تشخيص ثقل الدركسيون"
  ]
 }
]
if __name__=="__main__":
 publisher.main()
 print("A3TAL_NOV07_FOUR_ARTICLES_COMPLETE",flush=True)
