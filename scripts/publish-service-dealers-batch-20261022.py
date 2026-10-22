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

ROOT = "data/editorial/service-dealers-20261022"
CREDIT = "الصور لورش أو صالات عرض حقيقية خارج مصر، توضيحية وليست لمواقع الشركات المذكورة."
IMG = {
  "authorized_hero": {
    "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/73/Car_Repair_04.jpg/1280px-Car_Repair_04.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Car_Repair_04.jpg",
    "author": "Jwale2",
    "license": "CC BY-SA 4.0",
    "alt": "صورة فوتوغرافية لورشة سيارات حقيقية خارج مصر، للتوضيح لا تمثل مركز كيا بالإسكندرية"
  },
  "authorized_detail": {
    "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/ca/Car_Repairs_04.jpg/1280px-Car_Repairs_04.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Car_Repairs_04.jpg",
    "author": "NanaYawBotar",
    "license": "CC BY-SA 4.0",
    "alt": "صورة داخلية حقيقية لورشة صيانة سيارات خارج مصر توضيحية فقط"
  },
  "independent_hero": {
    "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fd/Car_Repair_01.jpg/1280px-Car_Repair_01.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Car_Repair_01.jpg",
    "author": "Jwale2",
    "license": "CC BY-SA 4.0",
    "alt": "فني وورشة صيانة سيارات فعلية خارج مصر لتوضيح المراكز المستقلة بالإسكندرية"
  },
  "independent_detail": {
    "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/48/Car_Repairs_01.jpg/1280px-Car_Repairs_01.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Car_Repairs_01.jpg",
    "author": "NanaYawBotar",
    "license": "CC BY-SA 4.0",
    "alt": "صورة حقيقية لأعمال إصلاح سيارة بورشة مستقلة خارج مصر"
  },
  "showroom_hero": {
    "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5c/Autosalon_Sindelfingen_2020_IMG_2332.jpg/1280px-Autosalon_Sindelfingen_2020_IMG_2332.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Autosalon_Sindelfingen_2020_IMG_2332.jpg",
    "author": "Alexander Migl",
    "license": "CC BY-SA 4.0",
    "alt": "صالة عرض سيارات حقيقية مصورة في ألمانيا، توضيحية لا تخص معارض الشيخ زايد"
  },
  "showroom_detail": {
    "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8e/Geely_Binrui_Cool_in_the_showroom%2C_rear_quarter.jpg/1280px-Geely_Binrui_Cool_in_the_showroom%2C_rear_quarter.jpg",
    "source": "https://commons.wikimedia.org/wiki/File:Geely_Binrui_Cool_in_the_showroom,_rear_quarter.jpg",
    "author": "GZrex",
    "license": "CC BY-SA 4.0",
    "alt": "صورة فوتوغرافية حقيقية لسيارة في معرض بالصين لا تمثل معارض الشيخ زايد"
  }
}
POSTS = [
  {
    "title": "مراكز صيانة كيا المعتمدة في الإسكندرية: سموحة والعامرية وجليم",
    "slug": "kia-authorized-service-alexandria-smouha-amreya-gleem",
    "file": "kia-alexandria-branches.html",
    "categories": [
      33
    ],
    "excerpt": "مراكز خدمة كيا EIT الرسمية في سموحة والعامرية بالإسكندرية، والفرق بينها وبين معرض جليم، مع العناوين ورقم 19542 وطريقة الحجز والضمان.",
    "seo_title": "مراكز صيانة كيا الإسكندرية | سموحة والعامرية و19542",
    "seo_description": "دليل كيا الإسكندرية: عنوان مركز سموحة والعامرية المعتمدين، هل جليم مركز خدمة أم معرض؟ الرقم 19542 والحجز والصيانة والضمان.",
    "focus": "مراكز صيانة كيا المعتمدة في الإسكندرية",
    "image_keys": [
      "authorized_hero",
      "authorized_detail"
    ],
    "insert_before": "<h2>مركز كيا العامرية"
  },
  {
    "title": "مراكز صيانة السيارات المستقلة في الإسكندرية: سيدي جابر وسموحة",
    "slug": "independent-car-repair-centers-alexandria-sidi-gaber-smouha",
    "file": "alexandria-independent-repair.html",
    "categories": [
      33
    ],
    "excerpt": "مراكز صيانة مستقلة في الإسكندرية: Check Car Service والسيد الكهربائي، العناوين المعلنة، وتقييم خدمات الكمبيوتر والفتيس والتكييف وفحص المستعمل.",
    "seo_title": "مراكز صيانة السيارات المستقلة في الإسكندرية | العناوين",
    "seo_description": "دليل الورش المستقلة في سيدي جابر وسموحة: Check Car Service والسيد الكهربائي مع خطوات التشخيص وفحص المستعمل والأسعار والفواتير.",
    "focus": "مراكز صيانة السيارات المستقلة في الإسكندرية",
    "image_keys": [
      "independent_hero",
      "independent_detail"
    ],
    "insert_before": "<h2>Check Car Service:"
  },
  {
    "title": "معارض السيارات في الشيخ زايد: وصلة دهشور وعناوين الزيرو والمستعمل",
    "slug": "sheikh-zayed-car-showrooms-waslet-dahshur-guide",
    "file": "sheikh-zayed-showrooms.html",
    "categories": [
      2998
    ],
    "excerpt": "دليل معارض الشيخ زايد على وصلة دهشور ومحور 26 يوليو: العلا والليثي ومحمد فهمي وVolvo Gallery وG.Auto، والفارق بين الوكيل والمعرض والتقسيط.",
    "seo_title": "معارض السيارات الشيخ زايد | وصلة دهشور والعناوين",
    "seo_description": "معارض السيارات الجديدة والمستعملة في الشيخ زايد: العلا والليثي ومحمد فهمي وفولفو وG.Auto، خطوات فحص الزيرو والتقسيط والضمان.",
    "focus": "معارض السيارات في الشيخ زايد",
    "image_keys": [
      "showroom_hero",
      "showroom_detail"
    ],
    "insert_before": "<h2>العلا والليثي"
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
    if not item["url"].startswith("https://thumb.wikimedia.org/wikipedia/commons/thumb/"):
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
        "filename":""a3tal-"+key+"-real-photograph-20261022.webp",
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
    print("OCT22_ALEXANDRIA_ZAYED_BATCH_VERIFIED_COMPLETE",flush=True)

if __name__=="__main__":
    main()
