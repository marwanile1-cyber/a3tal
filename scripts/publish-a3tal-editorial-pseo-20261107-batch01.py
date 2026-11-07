#!/usr/bin/env python3
"""Publish two distinctive automotive diagnoses with verified A3tal Direct Bridge.

Photo sources are real freely-licensed Wikimedia Commons images, individually
selected and attributed; their site-specific edits are not generated-original.
All WordPress writes have slug/intent guards, Yoast/OG/image/canonical checks.
"""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("a3tal_guarded_20261107","scripts/publish-pseo-symptoms-20261105.py")
pub=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)
pub.POSTS=[
 {
  "slug":"car-fuse-keeps-blowing-short-circuit-diagnosis",
  "file":"data/editorial/car-fuse-keeps-blowing-short-circuit-diagnosis-20261107.html",
  "title":"فيوز العربية بيحرق كل ما تغيّره؟ طريقة فحص القفلة من غير تكبير الأمبير",
  "excerpt":"فيوز السيارة بيحرق فور تغييره أو عند تشغيل التكييف والزجاج؟ تعرف على أسباب القفلة والحمل الزائد وكيف يفحص الفني الدائرة بأمان قبل تغيير أي قطعة.",
  "focus":"فيوز العربية بيحرق كل ما تغيّره",
  "category":"كهربا",
  "checks":["فيوز العربية","أمبير","{{a3tal_image:detail}}"],
  "dedup":["فيوز العربية بيحرق","فيوز السيارة يفصل باستمرار"],
  "match":["فيوز","بيحرق"],
  "photo":[
   [("Close view of a car fuse box showing various fuses and wires in a vehicle's engine compartment.jpg","Shixart1985","CC BY 2.0"),("Understanding car fuse box components and their arrangement in a vehicle engine bay at midday.jpg","Shixart1985","CC BY 2.0")],
   [("Car fuses intact and broken.JPG","Cqdx","CC BY-SA 3.0"),("Closeup of the car fuses.jpg","Shixart1985","CC BY 2.0")]
  ],
  "alt":[
   "صورة فوتوغرافية حقيقية لعلبة فيوزات السيارة توضح مكان اختبار الفيوز الذي يحترق باستمرار",
   "صورة فوتوغرافية لفيوزات سيارات سليمة ومحترقة للمقارنة البصرية دون استنتاج سبب القفلة"
  ]
 },
 {
  "slug":"hyundai-tucson-nx4-dual-zone-ac-one-side-hot",
  "file":"data/editorial/pseo-20261107/hyundai-tucson-nx4-dual-zone-ac-one-side-hot.html",
  "title":"تكييف هيونداي توسان NX4 بارد من ناحية وساخن من الثانية؟ SYNC وبوابة الخلط",
  "excerpt":"ناحية تبرد وناحية تسخن في تكييف توسان NX4؟ ابدأ بزر SYNC ثم اختبر بوابة خلط الهواء وحساساتها قبل شحن الفريون أو فك التابلوه.",
  "focus":"تكييف توسان NX4 بارد من ناحية وساخن من ناحية",
  "category":"تكييف",
  "checks":["توسان NX4","SYNC","{{a3tal_image:detail}}"],
  "dedup":["تكييف توسان NX4 ناحية سخنة","توسان NX4 تكييف بارد ناحية"],
  "match":["توسان","تكييف","ناحية"],
  "photo":[
   [("Hyundai Tucson NX4 1.6 GLS HEV - interior view.jpg","Ethan Llamas","CC BY-SA 4.0"),("HYUNDAI TUCSON HYBRID (NX4) CHINA VERSION INTERIOR.jpg","Dinkun Chen","CC BY-SA 4.0")],
   [("Hyundai Tucson Inspiration NX4 Gray Interior (2).jpg","Damian B Oh","CC BY-SA 4.0"),("Hyundai Tucson Inspiration NX4 Gray Interior (1).jpg","Damian B Oh","CC BY-SA 4.0")]
  ],
  "alt":[
   "مقصورة هيونداي توسان NX4 الحقيقية لتوضيح لوحة التحكم في التكييف ثنائي المناطق بحسب الفئة",
   "صورة حقيقية لتفاصيل مقصورة توسان NX4 تُظهر منطقة التحكم بالهواء وتوزيعه"
  ]
 }
]
if __name__=="__main__":
 pub.main()
 print("A3TAL_EDITORIAL_NOV07_BATCH01_COMPLETE",flush=True)
