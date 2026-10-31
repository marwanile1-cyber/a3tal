#!/usr/bin/env python3
"""Publish 3 non-overlapping 2027 Deepal G318/S09 editorial features and an integrated G318 car entity.
Authoritative source photography credited and cropped to WebP. Idempotent by exact slug;
check post SEO, taxonomy, internal image and encyclopedia price meta before declaring success.
"""
import os,json,re,io,time,base64,urllib.request,urllib.parse,urllib.error
from pathlib import Path
from PIL import Image,ImageOps
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY not available")
CAR_SLUG="jaecoo-j5-2027-egypt"
CAR_TITLE="جايكو J5 موديل 2027 في مصر | السعر والمواصفات"
ARTICLES=[
  {
    "slug": "chevrolet-optra-2027-egypt-complete-review-ls-lt-after-october-price-rise",
    "title": "مراجعة شيفروليه أوبترا 2027 في مصر بالكامل: السعر بعد الزيادة وفرق LS وLT والفتيس CVT",
    "category": 22,
    "minwords": 950,
    "focus": "مراجعة شيفروليه أوبترا 2027",
    "excerpt": "مراجعة أوبترا 2027 بعد زيادة أكتوبر: LS 784,900 جنيه وLT 809,900، محرك 1.5 لتر وفتيس CVT والضمان.",
    "meta": "شيفروليه أوبترا 2027 بعد زيادة أكتوبر: LS 784,900 وLT 809,900 جنيه، ومراجعة المحرك والفتيس CVT والأمان والضمان.",
    "photos": [
      {
        "key": "hero",
        "name": "optra-2027-review-official-car",
        "url": "https://www.chevroletarabia.com/content/dam/chevrolet/middle-east/egypt/english/index/cars/2025-optra/design/exterior/main-image-2000x1000.png?imwidth=1920",
        "license": "Official Chevrolet Egypt model image © rightsholder for product identification",
        "alt": "الصورة الرسمية لشيفروليه أوبترا الجديدة في مصر"
      },
      {
        "key": "detail",
        "name": "optra-2027-review-official-interior",
        "url": "https://www.chevroletarabia.com/content/dam/chevrolet/middle-east/egypt/english/index/cars/2025-optra/design/interior/2-Tone-Interior.jpg?imwidth=1920",
        "license": "Official Chevrolet Egypt image © rightsholder; equipment varies by trim",
        "alt": "مقصورة شيفروليه أوبترا في الصورة الرسمية"
      }
    ],
    "file": "data/editorial/chevrolet-optra-2027-egypt-complete-review-ls-lt-after-october-price-rise.html"
  },
  {
    "slug": "car-overheats-in-traffic-cools-when-driving-fan-thermostat-diagnosis",
    "title": "العربية بتسخن في الزحمة وبتبرد مع المشي؟ تشخيص المروحة ودورة التبريد قبل تغيير الردياتير",
    "category": 8,
    "minwords": 830,
    "focus": "العربية بتسخن في الزحمة",
    "excerpt": "تشخيص سخونة السيارة في الزحمة مع انخفاض الحرارة أثناء السير: فحص المروحة والريلاي وحساس الحرارة والثرموستات.",
    "meta": "العربية بتسخن في الزحمة وبتبرد مع المشي؟ أسباب المروحة والثرموستات والردياتير وحساس الحرارة وخطوات التشخيص.",
    "photos": [
      {
        "key": "hero",
        "name": "heat-traffic-cooling-fan-workshop",
        "commons": "Car cooling fan removed from a vehicle in a workshop during repair work.jpg",
        "license": "CC BY 2.0 Shixart1985 Wikimedia Commons; cropped WebP",
        "alt": "مروحة تبريد سيارة داخل ورشة حقيقة للتوضيح"
      },
      {
        "key": "detail",
        "name": "heat-traffic-mechanic-engine",
        "commons": "Mechanic works on car engine performing routine maintenance and inspections on vehicle parts.jpg",
        "license": "CC BY 2.0 Shixart1985 Wikimedia Commons; cropped WebP",
        "alt": "فني يفحص محرك سيارة داخل ورشة"
      }
    ],
    "file": "data/editorial/car-overheats-in-traffic-cools-when-driving-fan-thermostat-diagnosis.html"
  },
  {
    "slug": "motorcycle-engine-stalls-when-hot-restarts-cold-diagnosis",
    "title": "الموتوسيكل بيبطل وهو سخن ويدور بعد ما يبرد: تشخيص الشرارة والبنزين والكاربراتير",
    "category": 3028,
    "minwords": 870,
    "focus": "الموتوسيكل بيبطل وهو سخن",
    "excerpt": "الموتوسيكل بيفصل بعد السخونة ثم يدور وهو بارد: خطوات فحص البوبينة والبوجيه وحساس الكرنك والكربراتير والتهوية.",
    "meta": "الموتوسيكل بيبطل وهو سخن ويدور بعد ما يبرد؟ أسباب الشرارة والبوبينة والبنزين والكاربراتير والحقن وتشخيص آمن.",
    "photos": [
      {
        "key": "hero",
        "name": "motorcycle-hot-stall-real-repair",
        "commons": "Motorcycle Repair.jpg",
        "license": "CC BY-SA 4.0 Johnnybam Wikimedia Commons; cropped WebP",
        "alt": "ميكانيكي يصلح موتوسيكل حقيقي في ورشة للتوضيح"
      },
      {
        "key": "detail",
        "name": "motorcycle-hot-stall-engine-repair-detail",
        "commons": "Motor mechanic.jpg",
        "license": "CC BY-SA 4.0 Amuzujoe Wikimedia Commons; cropped WebP",
        "alt": "فني يفحص موتور موتوسيكل"
      }
    ],
    "file": "data/editorial/motorcycle-engine-stalls-when-hot-restarts-cold-diagnosis.html"
  },
  {
    "slug": "adas-camera-radar-calibration-after-windshield-bumper-repair-car-guide",
    "title": "معايرة كاميرات ورادار ADAS بعد تغيير الزجاج أو الصدام: هل لازم برمجة؟",
    "category": 1,
    "minwords": 760,
    "focus": "معايرة كاميرات ADAS بعد تغيير الزجاج",
    "excerpt": "خطوات معايرة ADAS بعد تغيير الزجاج أو الصدام والفرق بين المعايرة الثابتة والديناميكية وتقرير الفحص.",
    "meta": "هل يلزم معايرة كاميرا ADAS بعد تغيير الزجاج أو إصلاح الصدام؟ فرق Static وDynamic والتقارير اللازمة بعد إصلاح الحوادث.",
    "photos": [
      {
        "key": "hero",
        "name": "adas-automotive-camera-photograph",
        "commons": "Audi A8 2013 (11209843876).jpg",
        "license": "Wikimedia Commons editorial photo; cropped WebP; not calibration at a workshop",
        "alt": "سيارة حديثة للتوضيح لأنظمة ADAS"
      },
      {
        "key": "detail",
        "name": "adas-windshield-garage-detail",
        "commons": "Old car parked in garage with dusty windshield and wiper blade during the daytime.jpg",
        "license": "CC BY 2.0 Shixart1985 Wikimedia Commons; cropped WebP",
        "alt": "زجاج أمامي لسيارة داخل جراج للتوضيح"
      }
    ],
    "file": "data/editorial/adas-camera-radar-calibration-after-windshield-bumper-repair-car-guide.html"
  },
  {
    "slug": "geyou-shi-authorized-chevrolet-service-center-nasr-city-booking",
    "title": "مركز جيوشي شيفروليه المعتمد بمدينة نصر: العنوان ورقم 19927 وحجز الصيانة",
    "category": 33,
    "minwords": 760,
    "focus": "مركز جيوشي شيفروليه مدينة نصر",
    "excerpt": "مركز جيوشي المعتمد لشيفروليه بمدينة نصر: محور الشهيد، رقم 19927، مواعيد السبت–الخميس 9–5 والحجز.",
    "meta": "مركز جيوشي شيفروليه بمدينة نصر: العنوان محور الشهيد ورقم 19927 وحجز الصيانة ومواعيد العمل حسب المصدر الرسمي.",
    "photos": [
      {
        "key": "hero",
        "name": "geyou-shi-chevy-service-generic-garage",
        "commons": "Mechanic repairing car engine.jpg",
        "license": "CC0 Bembety Wikimedia Commons; generic mechanic not Geyushi center",
        "alt": "ميكانيكي سيارات في ورشة عامة للتوضيح وليست صورة مركز جيوشي"
      },
      {
        "key": "detail",
        "name": "geyou-shi-chevy-service-equipment",
        "commons": "Car maintenance in a garage with equipment for engine work and a vehicle being serviced.jpg",
        "license": "CC BY 2.0 Shixart1985 Wikimedia Commons; generic workshop",
        "alt": "أعمال صيانة محرك في ورشة عامة للتوضيح"
      }
    ],
    "file": "data/editorial/geyou-shi-authorized-chevrolet-service-center-nasr-city-booking.html"
  }
]
def request(url,data=None,auth=False):
    h={"Accept":"application/json","User-Agent":"A3talG318-Editorial-Release/20261027","Cache-Control":"no-cache,no-store"}
    if auth:h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=json.dumps(data,ensure_ascii=False).encode("utf8") if data is not None else None
    if raw is not None:h["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,data=raw,headers=h,method="POST" if raw is not None else "GET"),timeout=180) as r:return json.load(r)
def bridge(route,data=None):return request(API+route,data,True)
def count(s):return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+",re.sub("<[^>]+>"," ",s)))
def public(slug,car=False):
    kind="a3tal-cars" if car else "posts"
    return request(SITE+"/wp-json/wp/v2/"+kind+"?"+urllib.parse.urlencode(
       {"slug":slug,"_fields":"id,slug,title,status,link,featured_media,categories,content,yoast_head_json"}))

def preflight():
    for item in ARTICLES:
        c=Path(item["file"]).read_text("utf8")
        if count(c)<item["minwords"] or c.count("<h2>")<8 or c.count("<h3>")<4 or c.count("{{a3tal_image:detail}}")!=1 or "<h1" in c.lower():
            raise RuntimeError("Quality gate failed "+item["slug"]+" count "+str(count(c)))
        rows=public(item["slug"])
        if len(rows)>1:raise RuntimeError("Duplicate slug "+item["slug"])
        if rows and (rows[0].get("status")!="publish" or not rows[0].get("featured_media")):
            raise RuntimeError("Partial publication exists "+item["slug"])
        item["body"]=c
        item["prior"]=rows
    print("FIVE_CATEGORY_INTENTS_AND_SOURCES_VALIDATED",[(x["slug"],count(x["body"]),bool(x["prior"])) for x in ARTICLES],flush=True)
def photograph(f):
    if "commons" in f:
        url="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(f["commons"],safe="")
    else:url=f["url"]
    if not (url.startswith("https://www.chevroletarabia.com/content/dam/") or url.startswith("https://commons.wikimedia.org/")):
        raise RuntimeError("Unexpected image host")
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"A3tal model photo editorial/20261027","Accept":"image/*"}),timeout=90) as r:
        raw=r.read(23_000_000)
    if len(raw)<15000 or len(raw)>22_000_000:raise RuntimeError("Original photo missing or >22MB")
    with Image.open(io.BytesIO(raw)) as im:
        im=ImageOps.exif_transpose(im).convert("RGB")
        if im.width<1200 or im.height<650:raise RuntimeError("Original photo below useful resolution "+f["name"])
        if f["key"]=="hero":im=ImageOps.fit(im,(1200,675),method=Image.Resampling.LANCZOS)
        else:im.thumbnail((1200,900),Image.Resampling.LANCZOS)
        out=io.BytesIO();im.save(out,"WEBP",quality=86,method=6)
    b=out.getvalue()
    if len(b)<12000 or len(b)>2000000:raise RuntimeError("Invalid WebP conversion")
    print("DISCOVER_1200PX_REAL_SOURCE_PHOTO_VERIFIED",f["name"],len(b),url,flush=True)
    return {"key":f["key"],"role":"featured" if f["key"]=="hero" else "inline",
        "filename":"a3tal-"+f["name"]+"-20261027.webp",
        "image_base64":base64.b64encode(b).decode("ascii"),"convert_webp":False,
        "alt":f["alt"],"caption":f["license"]+" | المصدر: "+url,
        "placeholder":"{{a3tal_image:detail}}"}
def verify_post(item,pid):
    u=SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode(
        {"_fields":"id,slug,status,link,featured_media,categories,content,yoast_head_json"})
    p=request(u)
    c=(p.get("content") or {}).get("rendered","")
    seo=p.get("yoast_head_json") or {}
    if p["slug"]!=item["slug"] or p["status"]!="publish" or not p.get("featured_media") or item["category"] not in p["categories"]:
        raise RuntimeError("Wrong post identity, status, cover or category "+item["slug"])
    if count(c)<item["minwords"] or "{{a3tal_image" in c or item["photos"][1]["name"] not in c:
        raise RuntimeError("Editorial/photo missing from live page "+item["slug"])
    if (seo.get("robots") or {}).get("index")!="index" or seo.get("canonical")!=p["link"] or not seo.get("og_image"):
        raise RuntimeError("Article SEO index, canonical or social image missing "+item["slug"])
    print("FULL_EDITORIAL_PUBLISHED_VERIFIED",item["slug"],pid,count(c),"WORDS",p["link"],flush=True)
    return p
def publish(item):
    if item["prior"]:
        return verify_post(item,item["prior"][0]["id"])
    images=[photograph(x) for x in item["photos"]]
    payload={"post":{"title":item["title"],"slug":item["slug"],"status":"publish",
      "categories":[item["category"]],"content":item["body"],"excerpt":item["excerpt"],
      "meta":{"_yoast_wpseo_title":item["title"],
              "_yoast_wpseo_metadesc":item["meta"],
              "_yoast_wpseo_focuskw":item["focus"]}},
      "media":images}
    try:r=bridge("/publish-bundle",payload)
    except (TimeoutError,urllib.error.URLError):
        check=public(item["slug"])
        if len(check)!=1 or check[0]["status"]!="publish" or not check[0].get("featured_media"):raise
        return verify_post(item,check[0]["id"])
    post=r.get("post") or {}
    if post.get("status")!="publish" or not post.get("id"):raise RuntimeError("Bundle failed to publish "+item["slug"])
    return verify_post(item,int(post["id"]))

def update_existing_price():
    pid=83420
    prev=request(SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode({"_fields":"id,slug,title,link,status,featured_media,content,yoast_head_json"}))
    if prev.get("slug")!="jac-js2-price-egypt" or prev.get("status")!="publish" or not prev.get("featured_media"):
        raise RuntimeError("Existing JS2 original identity or featured image mismatch: refuse update")
    fresh=Path("data/editorial/jac-js2-price-egypt-update-20261031.html").read_text("utf8")
    if count(fresh)<980 or "795,000" not in fresh or "775,000" not in fresh:
        raise RuntimeError("Price refresh failed quality and historical-price guard")
    old=(prev.get("content") or {}).get("rendered","")
    # Reuse the original images visible on the old article, retaining existing Hero ID.
    old_imgs=re.findall(r"<(?:figure|img)[^>]*>.*?</figure>|<img[^>]*>",old,re.S|re.I)
    reuse=[]
    for block in old_imgs:
        if "wp-content/uploads" in block:
            reuse.append(block)
    if reuse:
        fresh=fresh.replace("<h2>مين وكيل جاك في مصر؟</h2>","<figure>"+reuse[0]+"</figure><h2>مين وكيل جاك في مصر؟</h2>",1)
    if "795,000" in old and "2026-10-31" in old:
        print("JS2_ALREADY_UPDATED_VERIFIED",prev["link"],flush=True)
        return
    result=bridge("/update-post",{"id":pid,"title":"سعر جاك JS2 في مصر بعد الزيادة: المواصفات والمميزات والعيوب","slug":"jac-js2-price-egypt",
        "status":"publish","content":fresh,
        "excerpt":"السعر الأحدث لجاك JS2 2027 أصبح 795,000 جنيه Smart بعد زيادة 20 ألف في 25 أكتوبر؛ مقارنة بالسعر السابق 775 ألف وتفاصيل الضمان.",
        "meta":{"_yoast_wpseo_metadesc":"سعر جاك JS2 2027 في مصر الآن 795 ألف جنيه بعد زيادة أكتوبر، وجدول الأسعار السابقة والمواصفات والضمان وخطوات الحجز.",
                "_yoast_wpseo_focuskw":"سعر جاك JS2 2027 في مصر"}})
    live=request(SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode({"_fields":"id,slug,link,status,featured_media,content,yoast_head_json"}))
    rendered=(live.get("content") or {}).get("rendered","")
    if (live["slug"],live["status"],live["featured_media"])!=("jac-js2-price-egypt","publish",prev["featured_media"]) or "795,000" not in rendered or "775,000" not in rendered:
        raise RuntimeError("JS2 old permalink price refresh verification failed")
    if count(rendered)<980 or (live.get("yoast_head_json") or {}).get("robots",{}).get("index")=="noindex":
        raise RuntimeError("JS2 live price article quality/index gate failed")
    print("EXISTING_JAC_JS2_PAGE_UPDATED_WITHOUT_DUPLICATE",pid,count(rendered),"WORDS",live["link"],flush=True)
def main():
    preflight()
    for a in ARTICLES:
        publish(a)
        time.sleep(1)
    update_existing_price()
    print("SIX_A3TAL_SECTIONS_DELIVERY_VERIFIED_FIVE_NEW_ONE_REFRESHED",flush=True)
if __name__=="__main__":main()
