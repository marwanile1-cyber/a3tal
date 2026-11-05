#!/usr/bin/env python3
"""Publish two differentiated A3tal PSEO symptom articles through Direct Bridge.

Reuse the proven guarded uploader: no unverified writes, live duplicate check,
category check, linked-source media attributions, canonical/OG/index checks.
"""
import importlib.util
from pathlib import Path

module_path=Path("scripts/publish-pseo-symptoms-20261105.py")
spec=importlib.util.spec_from_file_location("a3tal_verified_pseo_publisher", module_path)
pub=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)

pub.POSTS=[
 {
  "slug":"kia-sportage-nq5-reverse-camera-black-screen",
  "file":"data/editorial/pseo-20261105/kia-sportage-nq5-reverse-camera-black-screen.html",
  "title":"كاميرا الرجوع في كيا سبورتاج NQ5 شاشة سوداء؟ خطوات فحص R والفيش قبل التغيير",
  "excerpt":"كاميرا سبورتاج NQ5 لا تظهر عند الرجوع؟ تعرف على الفرق بين الشاشة السوداء وعدم الانتقال لعرض R وعطل الضفيرة والعدسة قبل شراء كاميرا جديدة.",
  "focus":"كاميرا الرجوع كيا سبورتاج NQ5 مش شغالة",
  "category":"كهربا",
  "checks":["سبورتاج NQ5","الكاميرا","{{a3tal_image:detail}}"],
  "dedup":["سبورتاج NQ5 كاميرا الرجوع","سبورتاج كاميرا سوداء"],
  "match":["سبورتاج","كاميرا","الرجوع"],
  "photo":[
   [("Kia Sportage (NQ5) in White, rear left.jpg","Benespit","CC BY-SA 4.0"),
    ("2023 Kia Sportage (NQ5) in White, rear right.jpg","Benespit","CC BY-SA 4.0")],
   [("Kia Sportage Hybrid 30th Edition NQ5 HEV Green (1).jpg","Damian B Oh","CC BY-SA 4.0"),
    ("Kia Sportage Hybrid 30th Edition NQ5 HEV Green (6).jpg","Damian B Oh","CC BY-SA 4.0")]
  ],
  "alt":[
   "الجزء الخلفي الحقيقي من كيا سبورتاج NQ5 لتحديد منطقة كاميرا الرجوع لا توثيقًا لعطل بعينه",
   "المقصورة الحقيقية لسبورتاج NQ5 من فئة مختلفة توضح موقع الشاشة وواجهة العرض حسب التجهيز"
  ]
 },
 {
  "slug":"hyundai-elantra-hd-abs-light-after-wheel-bearing",
  "file":"data/editorial/pseo-20261105/hyundai-elantra-hd-abs-light-after-wheel-bearing.html",
  "title":"لمبة ABS في إلنترا HD بعد تغيير رمان بلي العجل؟ فحص الحساس والإشارة",
  "excerpt":"بعد تغيير رمان البلي في إلنترا HD نورت لمبة ABS؟ خطوات قراءة كود العجلة والفيشة والضفيرة وحساس السرعة قبل تغيير وحدة ABS.",
  "focus":"لمبة ABS إلنترا HD بعد تغيير رمان بلي",
  "category":"كهربا",
  "checks":["إلنترا HD","رمان بلي","{{a3tal_image:detail}}"],
  "dedup":["إلنترا HD ABS رمان بلي","ABS إلنترا HD بعد تغيير البلي"],
  "match":["إلنترا","ABS","رمان"],
  "photo":[
   [("2006-2010 Hyundai Elantra (HD) SX sedan 01.jpg","OSX","Public domain"),
    ("2006-2009 Hyundai Elantra (HD) SX sedan 01.jpg","OSX","Public domain")],
   [("Brake calipers.jpg","Alison Cassidy","CC BY-SA 3.0"),
    ("HYUNDAI ELANTRA (HD) China (79).jpg","Dinkun Chen","CC BY-SA 4.0")]
  ],
  "alt":[
   "هيونداي إلنترا الجيل HD صورة حقيقية توضيحية لفحص أضواء نظام ABS بعد صيانة العجلة",
   "صورة حقيقية لمكونات الفرامل توضح منطقة العمل قرب حساس سرعة العجلة ولا تمثل قطعة إلنترا الأصلية"
  ]
 }
]

if __name__=="__main__":
    pub.main()
    print("A3TAL_PSEO_BATCH02_20261105_COMPLETE",flush=True)
