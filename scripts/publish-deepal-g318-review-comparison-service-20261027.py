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
CAR_SLUG="deepal-g318-2027-egypt"
CAR_TITLE="ديبال G318 موديل 2027 في مصر | السعر والمواصفات"
ARTICLES=[
 {"slug":"deepal-g318-2027-egypt-full-review-prices-ownership",
  "title":"مراجعة ديبال G318 موديل 2027 في مصر بالكامل: السعر والفئات والأداء والعفشة والعيوب",
  "file":"data/editorial/deepal-g318-2027-egypt-full-review-20261027.html",
  "category":22,"minwords":2200,"focus":"مراجعة ديبال G318 موديل 2027",
  "excerpt":"مراجعة ديبال G318 2027 في مصر: Premium بسعر 2,135,000 جنيه وAdventure بـ2,285,000 جنيه؛ تحليل الأداء والبطارية والعفشة والأمان والصيانة والشراء.",
  "meta":"مراجعة ديبال G318 2027 كاملة: السعر من 2.135 إلى 2.285 مليون جنيه، مقارنة الفئتين، 316 كيلوواط، بطارية 35.07، ومميزات وعيوب الاستخدام.",
  "photos":[
   {"key":"hero","name":"g318-review-exterior","url":"https://deepal-eg.com/media/products/main_banner__car_page_1920___980__eItcJgM.png","license":"Manufacturer product photography © Deepal Egypt; editorial model identification","alt":"صورة رسمية لطراز ديبال G318 موديل 2027 من موقع ديبال مصر، التصميم الخارجي"},
   {"key":"detail","name":"g318-review-interior","url":"https://deepal-eg.com/media/products/interior_interactive_1980x1080_7BIPH9R.png","license":"Manufacturer product photography © Deepal Egypt; editorial model identification","alt":"صورة رسمية داخلية لسيارة Deepal G318 وتوزيع مقصورة القيادة"}
  ]},
 {"slug":"deepal-g318-vs-s09-egypt-2027-comparison",
  "title":"مقارنة ديبال G318 وS09 في مصر 2027: فرق السعر والمقاعد والمدى وأيهما تستحق؟",
  "file":"data/editorial/deepal-g318-vs-s09-2027-egypt-comparison-20261027.html",
  "category":21,"minwords":1950,"focus":"مقارنة ديبال G318 وS09",
  "excerpt":"مقارنة G318 وS09 في مصر: يبدأ سعر الأولى 2.135 مليون والثانية 2.85 مليون، فرق 715 ألف جنيه؛ خمسة مقاعد أم ستة والبطارية والتعليق والصيانة.",
  "meta":"مقارنة ديبال G318 وS09 موديل 2027: فرق 715 ألف جنيه بين أول فئتين، مساحة 5 أو 6 مقاعد، بطاريات 35.07 و40.18، وتوصيات الشراء.",
  "photos":[
   {"key":"hero","name":"g318-vs-s09-compare-exterior","url":"https://deepal-eg.com/media/products/1920_x_1113_v2_g318_copy.png","license":"Manufacturer product photography © Deepal Egypt; editorial comparison G318","alt":"ديبال G318 في مقارنة مع S09، صورة G318 الأصلية من الوكيل"},
   {"key":"detail","name":"g318-vs-s09-compare-s09","url":"https://deepal-eg.com/media/products/Home_Banner_2_1.jpg.jpeg","license":"Manufacturer product photography © Deepal Egypt; editorial comparison S09","alt":"الصورة الرسمية لسيارة ديبال S09 بستة مقاعد من ديبال مصر ضمن المقارنة"}
  ]},
 {"slug":"deepal-egypt-official-service-centers-2026-booking-branches",
  "title":"مراكز خدمة ديبال مصر المعتمدة: العناوين والحجز والصيانة وضمان G318 وS09",
  "file":"data/editorial/deepal-egypt-official-centers-service-booking-20261027.html",
  "category":33,"minwords":1750,"focus":"مراكز خدمة ديبال مصر",
  "excerpt":"فروع ديبال مصر المنشورة رسميًا في أبو رواش والعامرية والسويس والمنيا وأسيوط، رقم 15050، وكيف تتأكد من مركز الخدمة والحجز والضمان.",
  "meta":"مراكز ديبال مصر: فروع أبو رواش والعامرية والسويس والمنيا وأسيوط وأرقام الحجز ومواعيد 9–5، الفرق بين الخدمة والمعرض وضمان G318 وS09.",
  "photos":[
   {"key":"hero","name":"deepal-service-guide-hero","commons":"Car lift in an auto repair shop with vehicles and tools present.jpg","license":"CC BY 2.0, Shixart1985, Wikimedia Commons; not a Deepal Egypt site","alt":"ورشة سيارات حقيقية خارج مصر للتوضيح فقط وليست فرع ديبال في مصر"},
   {"key":"detail","name":"deepal-service-guide-detail","commons":"Car repair in an auto shop with tools and equipment present on the floor and a partially disassembled vehicle on a lift.jpg","license":"CC BY 2.0, Shixart1985, Wikimedia Commons; not a Deepal Egypt site","alt":"صورة فوتوغرافية عامة لورشة خارج مصر، وليست صورة مركز خدمة ديبال"}
  ]}
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
        if count(c)<item["minwords"] or c.count("<table")<(1 if item["category"]==33 else 2) or c.count("<h3>")<5 or c.count("{{a3tal_image:detail}}")!=1:
            raise RuntimeError("Editorial depth/visual/comparison gate failed "+item["slug"]+" "+str(count(c)))
        if "<h1" in c.lower() or not c.count("https://a3tal.com/"):
            raise RuntimeError("Article internal link or duplicate heading incorrect")
        found=public(item["slug"])
        if len(found)>1:raise RuntimeError("Duplicate exact blog slug")
        if found and (found[0]["status"]!="publish" or not found[0].get("featured_media")):
            raise RuntimeError("Existing partial post requires manual review "+item["slug"])
        item["body"]=c
        item["prior"]=found
    # Search published/draft content for distinct intended article slugs, not generic Deepal name.
    for topic in ("G318 وS09","مراجعة ديبال G318","مراكز خدمة ديبال مصر"):
        r=bridge("/search-posts?"+urllib.parse.urlencode({"search":topic,"limit":80}))
        for x in r.get("items",[]):
            name=x.get("slug","")
            if name in [y["slug"] for y in ARTICLES]:continue
            title=x.get("title","")
            if topic in title and name not in [y["slug"] for y in ARTICLES]:
                raise RuntimeError("Existing exact overlapping editorial article at "+name)
    cars=public(CAR_SLUG,True)
    if len(cars)>1:raise RuntimeError("Duplicate G318 model")
    if cars and (cars[0]["title"]["rendered"]!=CAR_TITLE or cars[0]["status"]!="publish"):
        raise RuntimeError("Existing car identity conflict")
    print("SOURCE_ARTICLES_PREFLIGHT_VERIFIED",[(x["slug"],count(x["body"]),len(x["prior"])) for x in ARTICLES], "prior_cars",len(cars),flush=True)
    return cars
def photograph(f):
    if "commons" in f:
        url="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(f["commons"],safe="")
    else:url=f["url"]
    if not (url.startswith("https://deepal-eg.com/media/products/") or url.startswith("https://commons.wikimedia.org/")):
        raise RuntimeError("Unexpected image host")
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"A3tal model photo editorial/20261027","Accept":"image/*"}),timeout=90) as r:
        raw=r.read(23_000_000)
    if len(raw)<15000 or len(raw)>22_000_000:raise RuntimeError("Original photo missing or >22MB")
    with Image.open(io.BytesIO(raw)) as im:
        im=ImageOps.exif_transpose(im).convert("RGB")
        if im.width<950 or im.height<600:raise RuntimeError("Original photo below useful resolution "+f["name"])
        if f["key"]=="hero":im=ImageOps.fit(im,(1200,675),method=Image.Resampling.LANCZOS)
        else:im.thumbnail((1200,900),Image.Resampling.LANCZOS)
        out=io.BytesIO();im.save(out,"WEBP",quality=86,method=6)
    b=out.getvalue()
    if len(b)<12000 or len(b)>2000000:raise RuntimeError("Invalid WebP conversion")
    print("VERIFIED_REAL_SOURCE_PHOTO",f["name"],len(b),url,flush=True)
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
def car_record(review,comparison,centers,prior):
    body=Path("data/editorial/deepal-g318-2027-egypt-encyclopedia-20261027.html").read_text("utf8")
    if count(body)<1550 or len(body)<10000 or body.count("<h2>")<9:raise RuntimeError("G318 car model must be substantial")
    if prior:
        record=prior[0]
        if record["title"]["rendered"]!=CAR_TITLE or record["status"]!="publish":raise RuntimeError("Unexpected existing car")
        if not record.get("featured_media"):raise RuntimeError("Existing car lacks cover")
        print("EXISTING_G318_CAR_RECORD",record["id"],record["link"],flush=True)
        return record
    meta={"_a3_year":"2027","_a3_price_min":"2135000","_a3_price_max":"2285000",
          "_a3_currency":"EGP","_a3_engine_cc":"1500","_a3_power_hp":"424","_a3_torque_nm":"575",
          "_a3_transmission":"Electric drive","_a3_fuel":"REEV","_a3_drivetrain":"4WD","_a3_seats":"5",
          "_a3_source_url":"https://deepal-eg.com/ar/models/deepal-g318/",
          "_a3_source_checked_at":"2026-10-27",
          "_a3_related_post_ids":",".join(map(str,[review["id"],comparison["id"],centers["id"]])),
          "_yoast_wpseo_meta-robots-noindex":"2"}
    r=bridge("/admin",{"op":"platform_entity_upsert","type":"a3_car","title":CAR_TITLE,"slug":CAR_SLUG,
        "status":"publish","content":body,
        "excerpt":"ديبال G318 2027 في مصر: Premium من 2,135,000 وAdventure حتى 2,285,000 جنيه، 5 مقاعد وبطارية 35.07 كيلوواط/ساعة ودفع رباعي REEV.",
        "featured_media":review["featured_media"],
        "taxonomies":{"a3_brand":["deepal"],"a3_market":["egypt"],"a3_car_body":["suv"]},
        "meta":meta,"confirm":True,"dangerous":True})
    row=r.get("result") or {}
    if not r.get("ok") or not row.get("id"):raise RuntimeError("No successful car insert confirmation")
    car=public(CAR_SLUG,True)
    if len(car)!=1 or car[0]["status"]!="publish" or car[0]["id"]!=int(row["id"]) or car[0]["featured_media"]!=review["featured_media"]:
        raise RuntimeError("G318 car post not persisted correctly")
    pid=car[0]["id"]
    for key,expected in meta.items():
        m=bridge("/admin?"+urllib.parse.urlencode({"op":"post_meta","post_id":pid,"key":key}))
        if str((m.get("result") or {}).get(key,"")).strip()!=expected:
            raise RuntimeError("G318 car meta mismatch "+key)
    print("NEW_G318_CAR_CATALOG_RECORD_VERIFIED",pid,"PRICE",meta["_a3_price_min"],meta["_a3_price_max"],
          "RELATED",[review["id"],comparison["id"],centers["id"]],"URL",car[0]["link"],flush=True)
    return car[0]
def main():
    prior=preflight()
    data={}
    for a in ARTICLES:
        data[a["slug"]]=publish(a)
        time.sleep(2)
    car_record(data[ARTICLES[0]["slug"]],data[ARTICLES[1]["slug"]],data[ARTICLES[2]["slug"]],prior)
    print("G318_FULL_REVIEW_COMPARISON_VERIFIED_SERVICE_GUIDE_AND_CAR_CATALOG_RELEASE_COMPLETE",flush=True)
if __name__=="__main__":main()
