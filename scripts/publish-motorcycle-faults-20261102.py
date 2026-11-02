#!/usr/bin/env python3
"""Publish two narrowly-scoped motorcycle fault guides with original editorial WebP photo treatments.
Uses responsibly attributed Creative Commons photography and guarded A3tal Direct Bridge posting.
"""
import base64,io,json,os,re,time,urllib.request,urllib.parse,urllib.error
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance,ImageFilter,ImageDraw,ImageFont

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
CAT=3028
IMAGES = {
 "engine":{
    "cover":{"name":"Man working on motorcycle engine while using a screwdriver.jpg","author":"Shixart1985","license":"CC BY 2.0",
             "alt":"فني يفحص محرك موتوسيكل باستخدام مفك داخل مشهد صيانة حقيقي أثناء تشخيص الدخان الأزرق وفقد الزيت"},
    "detail":{"name":"Motorcycle Repair.jpg","author":"Johnnybam","license":"CC BY-SA 4.0",
              "alt":"ميكانيكي يعمل على فحص وصيانة محرك موتوسيكل في ورشة حقيقية قبل اتخاذ قرار فك المحرك"}
 },
 "brakes":{
    "cover":{"name":"Brembo p4-32 Caliper.jpg","author":"Sinank56","license":"CC BY-SA 4.0",
              "alt":"لقطة فوتوغرافية حقيقية لكاليبر فرامل أمامي في موتوسيكل Ducati، توضح مكان القطعة عند فحص الفرامل القافشة"},
    "detail":{"name":"Yamaha SR400 2014 Front Wheel.JPG","author":"Khaosaming","license":"CC BY-SA 4.0",
              "alt":"العجلة الأمامية وديسك الفرامل الفعلي في موتوسيكل Yamaha SR400 من أجل توضيح فحص مجموعة الفرامل"}
 }
}
ITEMS=[
 {"slug":"motorcycle-blue-smoke-exhaust-oil-burning-diagnosis",
  "title":"الموتوسيكل بيطلع دخان أزرق وبينقص زيت؟ أسباب الشنابر وكاوتش الصباب والتشخيص",
  "file":"data/editorial/motorcycle-blue-exhaust-smoke-oil-loss-20261102.html",
  "excerpt":"دخان أزرق من شكمان الموتوسيكل مع نقص زيت؟ اعرف الفرق بين تآكل الشنابر وكاوتش الصباب وزيادة الزيت، وكيف يُفحص محرك 4T قبل الفك.",
  "focus":"الموتوسيكل بيطلع دخان أزرق",
  "meta":"أسباب الدخان الأزرق من شكمان الموتوسيكل ونقص زيت المحرك: الشنابر، كاوتش الصباب، تهوية الكارتير، وجدول تشخيص قبل فتح الموتور.",
  "search":["دخان أزرق الموتوسيكل","دخان ازرق الموتوسيكل"],
  "facts":["كاوتش الصباب","الشنابر","2T","4T","{{a3tal_image:detail}}"],
  "photos":"engine"
 },
 {"slug":"motorcycle-brakes-dragging-wheel-hot-caliper-diagnosis",
  "title":"فرامل الموتوسيكل بتقفش والعجلة بتسخن؟ أسباب الكاليبر والتيل والماستر",
  "file":"data/editorial/motorcycle-brakes-dragging-wheel-hot-20261102.html",
  "excerpt":"فرامل الموتوسيكل بتقفش والعجلة بتسخن؟ اعرف علامات احتكاك الديسك المستمر وأسباب الكاليبر والماستر والتيل والطنبورة ومتى توقف القيادة فورًا.",
  "focus":"فرامل الموتوسيكل بتقفش",
  "meta":"فرامل الموتوسيكل بتقفش والعجلة بتسخن بعد الفرملة؟ أسباب تعليق الكاليبر وتيل الديسك والماستر والطنبورة وخطوات الفحص الآمن.",
  "search":["فرامل الموتوسيكل بتقفش","العجلة بتسخن موتوسيكل"],
  "facts":["الكاليبر","الماستر","الطنبورة","{{a3tal_image:detail}}"],
  "photos":"brakes"
 }
]

def jget(path, auth=False, data=None):
    headers={"Accept":"application/json","User-Agent":"A3tal-Motorcycle-Faults-20261102","Cache-Control":"no-store"}
    if auth:
        if not KEY:raise RuntimeError("Missing A3TAL_API_KEY")
        headers["X-A3tal-Key"]=KEY
        headers["Authorization"]="Bearer "+KEY
    raw=None
    if data is not None:
        raw=json.dumps(data,ensure_ascii=False).encode("utf-8")
        headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request((API if auth else SITE)+path,headers=headers,data=raw,method="POST" if data is not None else "GET")
    with urllib.request.urlopen(req,timeout=270) as f:return json.load(f)

def exact_post(item):
    exact=jget("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":item["slug"],"_fields":"id,slug,link,status,featured_media,content"}))
    if len(exact)>1:raise RuntimeError("Duplicate slug found; stop")
    if exact:
        old=exact[0]
        if old.get("status")=="publish" and old.get("featured_media") and old["slug"]==item["slug"] and "a3tal_image" not in (old.get("content") or {}).get("rendered",""):
            print("ALREADY_PUBLISHED",old["id"],old["link"],flush=True)
            return old
        raise RuntimeError("Existing incomplete post has exact slug; reconcile rather than create duplicate")
    # Only check matches with this narrow intent. Broad terms like engine should not block educational hubs.
    for term in item["search"]:
        results=jget("/search-posts?"+urllib.parse.urlencode({"search":term,"limit":100}),auth=True)
        for q in results.get("items",[]):
            name=(q.get("title","")+" "+q.get("slug","")).casefold()
            if item["photos"]=="engine" and ("دخان أزرق" in name or "دخان ازرق" in name) and ("موتوسيكل" in name or "motorcycle" in name):
                raise RuntimeError("Near-duplicate existing intent page: "+str(q))
            if item["photos"]=="brakes" and ("فرامل" in name or "brakes" in name) and ("قفش" in name or "drag" in name or "تسخن" in name):
                raise RuntimeError("Near-duplicate existing brake-drag page: "+str(q))
    return None

def commons_photo(spec):
    name=spec["name"]
    enc=urllib.parse.quote(name, safe="")
    links=[
      "https://commons.wikimedia.org/wiki/Special:Redirect/file/"+enc+"?width=1920",
      "https://commons.wikimedia.org/wiki/Special:FilePath/"+enc+"?width=1920",
      "https://commons.wikimedia.org/wiki/Special:Redirect/file/"+enc
    ]
    for url in links:
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"A3talEditorialPhotography/1.0 (https://a3tal.com; licensed credited reuse)","Accept":"image/jpeg,image/png,image/webp,image/*"})
            with urllib.request.urlopen(req,timeout=65) as f:raw=f.read(18_000_000)
            if not 20_000<len(raw)<18_000_000:continue
            with Image.open(io.BytesIO(raw)) as original:
                original.load()
                if original.width<950 or original.height<700:continue
                im=ImageOps.exif_transpose(original).convert("RGB")
                print("LICENSED_SOURCE_READY",name,im.size,spec["author"],spec["license"],flush=True)
                return im
        except Exception as e:
            print("SOURCE_RETRY",name,type(e).__name__,flush=True)
    raise RuntimeError("Required licensed source photo inaccessible: "+name)

def image_record(item,role,size):
    spec=IMAGES[item["photos"]][role]
    im=commons_photo(spec)
    w,h=size
    # Keep photographic subject: distinctive editorial crop and grading, without artificial smoke,
    # text banners, infographics or generic rendered components.
    photo=ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=(0.50,0.47))
    photo=ImageEnhance.Color(photo).enhance(.91 if item["photos"]=="engine" else .96)
    photo=ImageEnhance.Contrast(photo).enhance(1.09)
    photo=ImageEnhance.Sharpness(photo).enhance(1.08)
    # Small unobtrusive byline mark only.
    overlay=Image.new("RGBA",size,(0,0,0,0))
    draw=ImageDraw.Draw(overlay)
    draw.rounded_rectangle((w-171,h-51,w-21,h-16),radius=8,fill=(8,22,30,126))
    try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",16)
    except OSError:font=ImageFont.load_default()
    draw.text((w-158,h-45),"A3tal.com",font=font,fill=(255,255,255,235))
    image=Image.alpha_composite(photo.convert("RGBA"),overlay).convert("RGB")
    out=io.BytesIO()
    image.save(out,"WEBP",quality=87,method=6)
    raw=out.getvalue()
    if not 65_000<len(raw)<2_500_000:raise RuntimeError("Invalid edited photo size: "+str(len(raw)))
    link="https://commons.wikimedia.org/wiki/File:"+urllib.parse.quote(spec["name"].replace(" ","_"),safe="()_")
    cap=("صورة فوتوغرافية توضيحية حقيقية لموضع الفحص، وليست تصويرًا لحالة العطل المحددة. "
         "التصوير: "+spec["author"]+"، رخصة "+spec["license"]+"؛ قصّ وتعديل لوني خاص بمقال أعطال.كوم. "
         "المصدر: "+link)
    return {
       "key":role,"role":"featured" if role=="cover" else "inline",
       "filename":"a3tal-"+item["slug"]+"-original-"+role+".webp",
       "image_base64":base64.b64encode(raw).decode("ascii"),
       "convert_webp":False,"alt":spec["alt"],"caption":cap,
       "placeholder":"{{a3tal_image:detail}}"
    }

def publish(item):
    body=Path(item["file"]).read_text("utf-8").strip()
    if len(body)<8500 or body.count("<h2>")<8 or body.count("<h3>")<5 or body.count("<table")<1:
        raise RuntimeError("Article editorial quality validation failed: "+item["slug"])
    for fact in item["facts"]:
        if fact not in body:raise RuntimeError("Critical editorial detail missing "+fact)
    existing=exact_post(item)
    if existing:return
    imgs=[
      image_record(item,"cover",(1600,900)),
      image_record(item,"detail",(1400,840))
    ]
    slug=item["slug"];url=SITE+"/"+slug+"/"
    post={
      "title":item["title"],"slug":slug,"type":"post","status":"publish",
      "content":body,"categories":[CAT],"excerpt":item["excerpt"],
      "meta":{
        "_yoast_wpseo_title":item["title"]+" | أعطال.كوم",
        "_yoast_wpseo_metadesc":item["meta"],
        "_yoast_wpseo_focuskw":item["focus"],
        "_yoast_wpseo_canonical":url,
        "_yoast_wpseo_opengraph-title":item["title"],
        "_yoast_wpseo_opengraph-description":item["meta"],
        "_yoast_wpseo_twitter-title":item["title"],
        "_yoast_wpseo_twitter-description":item["meta"]
      }
    }
    try:
        res=jget("/publish-bundle",auth=True,data={"post":post,"media":imgs})
    except (TimeoutError,urllib.error.URLError):
        print("AMBIGUOUS_WRITE_VERIFY_ONLY",slug,flush=True)
        matches=jget("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":slug,"_fields":"id,status,link,featured_media"}))
        if len(matches)!=1 or matches[0].get("status")!="publish" or not matches[0].get("featured_media"):raise
        res={"post":matches[0]}
    info=res.get("post") or {}
    if info.get("status")!="publish" or info.get("slug")!=slug or not info.get("featured_media"):
        raise RuntimeError("Bridge did not confirm successful published article: "+slug)
    live=jget("/wp-json/wp/v2/posts/"+str(info["id"])+"?"+urllib.parse.urlencode({"_fields":"id,slug,status,link,featured_media,categories,content,yoast_head_json"}))
    rendered=(live.get("content") or {}).get("rendered","")
    seo=live.get("yoast_head_json") or {}
    og=(seo.get("og_image") or [{}])[0].get("url","")
    if (live.get("link")!=url or live.get("status")!="publish" or
        live.get("featured_media")!=info.get("featured_media") or CAT not in live.get("categories",[]) or
        "{{a3tal_image" in rendered or "original-detail" not in rendered or
        "original-cover" not in og or seo.get("canonical")!=url or
        (seo.get("robots") or {}).get("index")=="noindex"):
        raise RuntimeError("Published post failed full media/SEO QA: "+slug)
    print("PUBLISHED_VERIFIED",live["id"],url,"FEATURED",live["featured_media"],"OG",og,flush=True)

def main():
    if not KEY:raise RuntimeError("Protected A3TAL_API_KEY absent")
    for item in ITEMS:publish(item)
    print("MOTORCYCLE_FAULT_PAIR_COMPLETED",flush=True)
if __name__=="__main__":main()
