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
 {"slug":"jaecoo-j5-2027-egypt-full-review-price-trims",
  "title":"مراجعة جايكو J5 موديل 2027 في مصر بالكامل: السعر وفرق Urban وElite والعيوب",
  "file":"data/editorial/jaecoo-j5-2027-egypt-full-review-price-20261027.html",
  "category":22,"minwords":2200,"focus":"مراجعة جايكو J5 موديل 2027 في مصر",
  "excerpt":"مراجعة جايكو J5 موديل 2027 بعد إطلاق 26 أكتوبر: Urban بـ1,195,000 جنيه وElite بـ1,325,000 جنيه، المواصفات والأمان والفتيس CVT والضمان والصيانة.",
  "meta":"مراجعة جايكو J5 2027 بالكامل: Urban بسعر 1.195 مليون وElite بـ1.325 مليون، فرق 130 ألف جنيه، المحرك 1.5 تيربو والأمان والعيوب.",
  "photos":[
   {"key":"hero","name":"jaecoo-j5-2027-discover-review-exterior","url":"https://omodajaecoo-dubai.ae/wp-content/uploads/2025/08/jaecoo-j5-exterior1-2153x1095-1.webp","license":"Official JAECOO Dubai dealer model promotional photograph; editorial identification only © respective owner, not photographed in Egypt","alt":"صورة جايكو J5 الخارجية من موزع جايكو الرسمي بدبي توضح تصميم الموديل؛ صورة تعريفية وليست تجربة قيادة"},
   {"key":"detail","name":"jaecoo-j5-review-official-cabin","url":"https://omodajaecoo-dubai.ae/wp-content/uploads/2025/08/jaecoo-j5-interior1-1824x1027-1.webp","license":"Official JAECOO Dubai dealer cabin promotional photograph © respective owner; configurations may vary in Egyptian trims","alt":"مقصورة سيارة جايكو J5 وشاشة الترفيه ومكان القيادة في صورة ترويجية للموديل من موزع رسمي"}
  ]},
 {"slug":"jaecoo-j5-vs-kia-seltos-2027-egypt-price-comparison",
  "title":"مقارنة جايكو J5 وكيا سيلتوس 2027 في مصر: هل توفر 175 ألف جنيه وتكسب تجهيزات؟",
  "file":"data/editorial/jaecoo-j5-vs-kia-seltos-2027-comparison-20261027.html",
  "category":21,"minwords":1950,"focus":"مقارنة جايكو J5 وكيا سيلتوس 2027",
  "excerpt":"مقارنة جايكو J5 وكيا سيلتوس 2027: فرق سعر البداية 174,900 جنيه، محرك 1.5 تيربو CVT مقابل سيلتوس 1.5 IVT و1.4 DCT، الأمان والضمان.",
  "meta":"مقارنة جايكو J5 وكيا سيلتوس 2027: فرق 174,900 جنيه، قوة المحركات، 4 أو 6 وسائد هوائية، العفشة الخلفية والصيانة وأفضل فئة للشراء.",
  "photos":[
   {"key":"hero","name":"jaecoo-j5-vs-kia-seltos-discover-comparison","url":"https://omodajaecoo-dubai.ae/wp-content/uploads/2025/08/jaecoo-j5-exterior2-2153x1095-1.webp","license":"Jaecoo J5 official distributor Dubai promotion; authentic Jaecoo J5, not a composite car photograph","alt":"صورة خارجية رسمية لسيارة جايكو J5 في مقارنة سعرها مع كيا سيلتوس موديل 2027 بمصر"},
   {"key":"detail","name":"kia-seltos-egypt-official-comparison","url":"https://kia.com.eg/uploads/models/685a94e5a94661750766821.jpg","license":"Official Kia Egypt The Seltos model page, © Kia Egypt; local vehicle identification","alt":"صورة كيا سيلتوس الرسمية من موقع كيا مصر ضمن المقارنة مع جايكو J5"}
  ]},
 {"slug":"jaecoo-egypt-agent-service-centers-maintenance-2026",
  "title":"توكيل جايكو مصر ومراكز الخدمة المعتمدة: الضمان والحجز والصيانة وأسعار القطع",
  "file":"data/editorial/jaecoo-egypt-agent-service-maintenance-20261027.html",
  "category":33,"minwords":1900,"focus":"توكيل جايكو مصر ومراكز الخدمة المعتمدة",
  "excerpt":"وكيل جايكو مصر عز العرب السويدي: حقيقة الفروع المعتمدة، ضمان السيارة والمحرك، عرض الصيانة لأول 150 عميلًا وكيف تحصل على مركز رسمي وسعر قطع J5.",
  "meta":"توكيل جايكو مصر عز العرب السويدي: دليل مراكز الخدمة والتحقق من الفروع، ضمان J5 سبع سنوات وضمان المحرك، الحجز وعرض الصيانة المحدود.",
  "photos":[
   {"key":"hero","name":"jaecoo-agent-repair-workshop-discover","commons":"Car lift in an auto repair shop with vehicles and tools present.jpg","license":"CC BY 2.0, Shixart1985, Wikimedia Commons; generic real repair shop, not JAECOO Egypt","alt":"صورة فوتوغرافية لورشة صيانة سيارات حقيقية خارج مصر، ولا تمثل مركز جايكو معتمدًا"},
   {"key":"detail","name":"jaecoo-agent-workshop-detail","commons":"Car repair in an auto shop with tools and equipment present on the floor and a partially disassembled vehicle on a lift.jpg","license":"CC BY 2.0, Shixart1985, Wikimedia Commons; not a Jaecoo branch","alt":"مركز صيانة سيارات عام في صورة توضيحية، وليس أحد فروع جايكو مصر"}
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
    for topic in ("جايكو J5 وكيا سيلتوس","مراجعة جايكو J5","توكيل جايكو مصر"):
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
    if not (url.startswith("https://omodajaecoo-dubai.ae/wp-content/uploads/") or url.startswith("https://kia.com.eg/uploads/models/") or url.startswith("https://commons.wikimedia.org/")):
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
def car_record(review,comparison,centers,prior):
    body=Path("data/editorial/jaecoo-j5-2027-egypt-encyclopedia-20261027.html").read_text("utf8")
    if count(body)<1500 or len(body)<10000 or body.count("<h2>")<9:raise RuntimeError("G318 car model must be substantial")
    if prior:
        record=prior[0]
        if record["title"]["rendered"]!=CAR_TITLE or record["status"]!="publish":raise RuntimeError("Unexpected existing car")
        if not record.get("featured_media"):raise RuntimeError("Existing car lacks cover")
        print("EXISTING_JAECOO_J5_CAR_RECORD",record["id"],record["link"],flush=True)
        return record
    meta={"_a3_year":"2027","_a3_price_min":"1195000","_a3_price_max":"1325000",
          "_a3_currency":"EGP","_a3_engine_cc":"1500","_a3_power_hp":"157","_a3_torque_nm":"250",
          "_a3_transmission":"CVT","_a3_fuel":"Petrol","_a3_drivetrain":"FWD","_a3_seats":"5",
          "_a3_source_url":"https://almalnews.com/2143603/",
          "_a3_source_checked_at":"2026-10-27",
          "_a3_related_post_ids":",".join(map(str,[review["id"],comparison["id"],centers["id"]])),
          "_yoast_wpseo_meta-robots-noindex":"2"}
    r=bridge("/admin",{"op":"platform_entity_upsert","type":"a3_car","title":CAR_TITLE,"slug":CAR_SLUG,
        "status":"publish","content":body,
        "excerpt":"جايكو J5 2027 مصر: Urban بـ1,195,000 وElite بـ1,325,000 جنيه، بنزين 1.5 تيربو وCVT، خمس مقاعد.",
        "featured_media":review["featured_media"],
        "taxonomies":{"a3_brand":["jaecoo"],"a3_market":["egypt"],"a3_car_body":["suv"]},
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
    print("NEW_JAECOO_J5_CAR_CATALOG_RECORD_VERIFIED",pid,"PRICE",meta["_a3_price_min"],meta["_a3_price_max"],
          "RELATED",[review["id"],comparison["id"],centers["id"]],"URL",car[0]["link"],flush=True)
    return car[0]
def main():
    prior=preflight()
    data={}
    for a in ARTICLES:
        data[a["slug"]]=publish(a)
        time.sleep(2)
    # The Jaecoo brand debuted in Egypt on Oct 26 and doesn't yet exist in this car taxonomy.
    # The bridge refuses assigning a nonexistent brand; safely create only the exact slug.
    brands=request(SITE+"/wp-json/wp/v2/a3_brand?"+urllib.parse.urlencode({"slug":"jaecoo","_fields":"id,name,slug"}))
    if not brands:
        res=bridge("/admin",{"op":"term_upsert","taxonomy":"a3_brand","name":"JAECOO","slug":"jaecoo"})
        if not (res.get("ok") and (res.get("result") or {}).get("term_id")):
            raise RuntimeError("Jaecoo brand term creation not confirmed")
        print("NEW_JAECOO_BRAND_TERM_VERIFIED",res["result"]["term_id"],flush=True)
    else:
        print("EXISTING_JAECOO_BRAND_TERM",brands[0]["id"],flush=True)
    car_record(data[ARTICLES[0]["slug"]],data[ARTICLES[1]["slug"]],data[ARTICLES[2]["slug"]],prior)
    print("JAECOO_J5_FULL_REVIEW_COMPARISON_AGENT_GUIDE_AND_CAR_CATALOG_RELEASE_COMPLETE",flush=True)
if __name__=="__main__":main()
