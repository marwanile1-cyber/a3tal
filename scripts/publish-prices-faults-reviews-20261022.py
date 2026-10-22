#!/usr/bin/env python3
"""Publish three independently researched Egypt auto-directory encyclopedia posts
with real, licensed Wikimedia Commons camera photographs, cropped/encoded WebP.
Idempotent by exact immutable slug; no replacements or invented centers/photos.
"""
import base64
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

SITE = "https://a3tal.com"
API = SITE + "/wp-json/a3tal-direct/v1"
KEY = os.environ.get("A3TAL_API_KEY", "")
if not KEY:
    raise RuntimeError("Missing A3TAL_API_KEY, refusing publication")

ROOT = "data/editorial/prices-faults-reviews-20261022"
CREDIT = "الصور لورش أو صالات عرض حقيقية خارج مصر، توضيحية وليست لمواقع الشركات المذكورة."
IMG = {
  "price_hero": {
    "url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Chang'an%20Eado%20Plus%20facelift%2002%20China%202023-04-10.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Chang'an_Eado_Plus_facelift_02_China_2023-04-10.jpg",
    "author": "Navigator84",
    "license": "CC BY-SA 4.0",
    "alt": "صورة حقيقية لإيدو بلس 2023 خارج مصر وليست تأكيدًا لتجهيز نسخة مصر 2026"
  },
  "price_detail": {
    "url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Changan%20Eado%20Plus%20012.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Changan_Eado_Plus_012.jpg",
    "author": "JustAnotherCarDesigner",
    "license": "CC BY-SA 4.0",
    "alt": "صورة حقيقية لإيدو بلس خارج مصر للمقارنة البصرية"
  },
  "review_hero": {
    "url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/2026%20Suzuki%20Dzire%20GL%20in%20Arctic%20White%20Pearl%2001.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:2026_Suzuki_Dzire_GL_in_Arctic_White_Pearl_01.jpg",
    "author": "Haysnawri10",
    "license": "CC BY-SA 4.0",
    "alt": "سوزوكي ديزاير 2026 في السعودية فئة GL وليس صورة فئة GLX المصرية"
  },
  "review_detail": {
    "url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/2026%20Suzuki%20Dzire%20GL%20in%20Arctic%20White%20Pearl%2002.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:2026_Suzuki_Dzire_GL_in_Arctic_White_Pearl_02.jpg",
    "author": "Haysnawri10",
    "license": "CC BY-SA 4.0",
    "alt": "صورة حقيقية ثانية لسوزوكي ديزاير 2026 مصورة خارج مصر"
  },
  "fault_hero": {
    "url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Car%20battery.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Car_battery.jpg",
    "author": "Azorbli",
    "license": "CC BY-SA 4.0",
    "alt": "فني يفحص بطارية عربية فوتوغرافيًا للتوضيح لا تشخيص سيارة بعينها"
  },
  "fault_detail": {
    "url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/All%20multimeters.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:All_multimeters.jpg",
    "author": "Ecomponents",
    "license": "CC BY-SA 4.0",
    "alt": "صورة حقيقية لعدادات قياس كهرباء فنية لفهم تشخيص تسريب البطارية"
  }
}
POSTS = [
  {
    "title": "سعر شانجان إيدو بلس 2026 في مصر: Elite وPremium وFlagship والفرق بين الأسعار",
    "slug": "changan-eado-plus-2026-egypt-prices-trims-official",
    "file": "changan-eado-plus-2026-prices.html",
    "categories": [
      374
    ],
    "excerpt": "أسعار شانجان إيدو بلس 2026: Elite 1,049,000 وPremium 1,100,000 وFlagship 1,200,000 جنيه بالقوائم المتاحة، مع اختلاف صفحة الوكيل.",
    "seo_title": "سعر شانجان إيدو بلس 2026 | الفئات والمواصفات في مصر",
    "seo_description": "أسعار شانجان إيدو بلس 2026 Elite وPremium وFlagship في مصر، محرك 1.5 تيربو 178 حصان وفتيس 7DCT، مع توضيح اختلاف قوائم الأسعار.",
    "focus": "سعر شانجان ايدو بلس 2026",
    "image_keys": [
      "price_hero",
      "price_detail"
    ],
    "insert_before": "<h2>لماذا قد تجد إيدو بلس"
  },
  {
    "title": "مراجعة سوزوكي ديزاير 2026 في مصر: المحرك والفتيس والأمان وهل تستحق؟",
    "slug": "suzuki-dzire-2026-egypt-review-real-specs-pros-cons",
    "file": "suzuki-dzire-2026-review.html",
    "categories": [
      22
    ],
    "excerpt": "مراجعة تحريرية لسوزوكي ديزاير 2026 في مصر بمحرك Z12E ثلاثي الأسطوانات والفتيس والأمان وسعر GLX، دون ادعاء تجربة قيادة.",
    "seo_title": "مراجعة سوزوكي ديزاير 2026 في مصر | المميزات والعيوب",
    "seo_description": "تقييم سوزوكي ديزاير 2026 في مصر: محرك 1.2 ثلاثي الأسطوانات ونوع الفتيس والتجهيزات والأمان والسعر ونقاط الفحص قبل الشراء.",
    "focus": "مراجعة سوزوكي ديزاير 2026",
    "image_keys": [
      "review_hero",
      "review_detail"
    ],
    "insert_before": "<h2>الشكل الخارجي:"
  },
  {
    "title": "بطارية السيارة بتفضى وهي واقفة: أسباب تسريب الكهرباء وطريقة التشخيص",
    "slug": "car-battery-drains-overnight-while-parked-parasitic-draw-diagnosis",
    "file": "car-battery-discharges-while-parked-diagnostic.html",
    "categories": [
      13
    ],
    "excerpt": "لماذا تفضى بطارية السيارة وهي متوقفة؟ الفرق بين ضعف البطارية والدينامو وسحب Parasitic Draw، تشخيص الوحدات والفيوزات والسلامة.",
    "seo_title": "بطارية السيارة بتفضى وهي واقفة | تشخيص سحب الكهرباء",
    "seo_description": "أسباب تفريغ بطارية العربية وهي مقفولة: البطارية والدينامو والكاميرا وParasitic Draw، وفحص الكهرباء بعد نوم الوحدات.",
    "focus": "بطارية العربية بتفضى وهي واقفة",
    "image_keys": [
      "fault_hero",
      "fault_detail"
    ],
    "insert_before": "<h2>كيف تفرق بين بطارية"
  }
]

def get_json(url, body=None, authorized=True):
    h={"Accept":"application/json",
       "User-Agent":"A3tal-Egypt-VerifiedServiceDirectory/2026-10-20",
       "Cache-Control":"no-cache, no-store"}
    if authorized:
        h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=None
    if body is not None:
        data=json.dumps(body,ensure_ascii=False).encode("utf-8")
        h["Content-Type"]="application/json"
    request=urllib.request.Request(url,data=data,headers=h)
    with urllib.request.urlopen(request,timeout=210) as response:
        return json.load(response)

def count_words(raw):
    return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+",re.sub("<[^>]+>"," ",raw)))

def fetch_image(key, size):
    item=IMG[key]
    # Only download real, CC-licensed camera photos whose original Commons
    # source and author have been checked in advance.
    if not item["url"].startswith("https://commons.wikimedia.org/wiki/Special:Redirect/file/"):
        raise RuntimeError("Unverified image host")
    req=urllib.request.Request(item["url"],headers={
      "User-Agent":"A3tal-Editorial/1.0 (source: https://a3tal.com; CC credits in published post)",
      "Accept":"image/jpeg,image/*"
    })
    with urllib.request.urlopen(req,timeout=55) as response:
        original=response.read(9_000_000)
        mime=response.headers.get("Content-Type","")
    if len(original)<6000 or len(original)>8_000_000:
        raise RuntimeError("Unexpected image byte count")
    with Image.open(io.BytesIO(original)) as im:
        im=ImageOps.exif_transpose(im).convert("RGB")
        if im.width<700 or im.height<550:
            raise RuntimeError("Image resolution below photographic standard")
        if size[0]==1200 and size[1]==675:
            im=ImageOps.fit(im,size,method=Image.Resampling.LANCZOS,centering=(.5,.5))
        else:
            im.thumbnail(size,Image.Resampling.LANCZOS)
        buff=io.BytesIO()
        im.save(buff,format="WEBP",quality=86,method=6)
    photo=buff.getvalue()
    if len(photo)<15_000 or len(photo)>1_500_000:
        raise RuntimeError("Transcoded photo out of range")
    print("REAL_LICENSED_PHOTO_READY",key,len(photo),item["license"],flush=True)
    return {
        "key":"hero" if key.endswith("_hero") else "detail",
        "role":"featured" if key.endswith("_hero") else "inline",
        "filename":"a3tal-"+key+"-real-photograph-20261022.webp",
        "image_base64":base64.b64encode(photo).decode("ascii"),
        "convert_webp":False,
        "alt":item["alt"],
        "caption":f"صورة فوتوغرافية توضيحية حقيقية، ليست للمراكز المذكورة. تصوير: {item['author']}، {item['license']}، المصدر: Wikimedia Commons.",
        "placeholder":"{{a3tal_image:detail}}"
    }

def existing(slug):
    endpoint=SITE+"/wp-json/wp/v2/posts?slug="+urllib.parse.quote(slug,safe="")+"&_fields=id,slug,status,link,featured_media,content"
    records=get_json(endpoint,authorized=False)
    return [r for r in records if r.get("slug")==slug]

def publish(entry):
    slug=entry["slug"]
    originals=existing(slug)
    if len(originals)>1:raise RuntimeError("Duplicate slug already exists: "+slug)
    if originals:
        row=originals[0]
        if row.get("status")=="publish" and row.get("featured_media") and count_words(row.get("content",{}).get("rendered",""))>=1500:
            print("ALREADY_PUBLISHED_VERIFIED",slug,row["id"],row["link"],flush=True)
            return
        raise RuntimeError("Partial or draft existing slug, manual reconciliation needed: "+slug)
    content=(Path(ROOT)/entry["file"]).read_text("utf-8")
    n=count_words(content)
    if n<1500 or "<h1" in content.lower():
        raise RuntimeError("Article failed originality/length/H1 gate: "+slug)
    if content.count("<table")<2 or "<h3" not in content or "commons.wikimedia.org" not in content:
        raise RuntimeError("Article lacks decision tables, FAQ, or real media attribution")
    needle=entry["insert_before"]
    if content.count(needle)!=1:raise RuntimeError("Unable to place factual inline photograph")
    content=content.replace(needle,"{{a3tal_image:detail}}\n"+needle)
    photos=[fetch_image(k,(1200,675) if k.endswith("_hero") else (1200,850)) for k in entry["image_keys"]]
    payload={"post":{
        "title":entry["title"],"slug":slug,"content":content,
        "excerpt":entry["excerpt"],"categories":entry["categories"],"status":"publish",
        "meta":{
            "_yoast_wpseo_title":entry["seo_title"],
            "_yoast_wpseo_metadesc":entry["seo_description"],
            "_yoast_wpseo_focuskw":entry["focus"]
        }},"media":photos}
    response=get_json(API+"/publish-bundle",body=payload)
    post=response.get("post") or {}
    if post.get("status")!="publish" or not post.get("id"):
        raise RuntimeError("Bundle returned no published WordPress post: "+slug)
    article_id=int(post["id"])
    # Query origin's REST representation, not a success banner only.
    endpoint=SITE+"/wp-json/wp/v2/posts/"+str(article_id)+"?_fields=id,slug,status,link,featured_media,categories,content,yoast_head_json"
    live=get_json(endpoint,authorized=False)
    rendered=live.get("content",{}).get("rendered","")
    count=count_words(rendered)
    if live["slug"]!=slug or live["status"]!="publish" or count<1500:
        raise RuntimeError("Live article quality/identity readback failure: "+slug)
    if not live.get("featured_media"):
        raise RuntimeError("Real photograph not assigned as featured image: "+slug)
    if "{{a3tal_image:" in rendered or "a3tal-"+entry["image_keys"][1] not in rendered:
        raise RuntimeError("Real inline photo placeholder not replaced: "+slug)
    y=live.get("yoast_head_json") or {}
    if (y.get("robots") or {}).get("index")=="noindex":
        raise RuntimeError("SEO noindex unexpected")
    if not (y.get("canonical") or "").startswith(SITE+"/"):
        raise RuntimeError("SEO canonical not set to own site")
    print("ARTICLE_PUBLISHED_AND_LIVE_VERIFIED",article_id,"WORDS",count,
          "COVER",live["featured_media"],"MEDIA",len(response.get("media") or []),
          "CATEGORIES",live.get("categories"),"URL",live.get("link"),flush=True)

def main():
    for post in POSTS:
        publish(post)
        time.sleep(3)
    print("OCT22_PRICES_FAULTS_REVIEWS_VERIFIED_COMPLETE",flush=True)

if __name__=="__main__":
    main()
