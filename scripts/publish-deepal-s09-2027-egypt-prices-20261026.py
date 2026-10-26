#!/usr/bin/env python3
"""Safely publish a Deepal S09 2027 launch price guide AND an integrated car encyclopedia entity.
Exact source manufacturer promotional images credited (not CC), no invented test drive.
One-time article/vehicle slugs. No blind retries, verify permalink/media/index/metadata.
"""
import base64,io,json,os,re,time,urllib.request,urllib.parse,urllib.error
from pathlib import Path
from PIL import Image,ImageOps

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("Refusing publication without A3TAL_API_KEY")
SLUG="deepal-s09-2027-egypt-price-premium-signature-reev"
CAR_SLUG="deepal-s09-2027-egypt"
TITLE="سعر ديبال S09 موديل 2027 في مصر: Premium وSignature وهل فرق 250 ألف جنيه يستحق؟"
CAR_TITLE="ديبال S09 موديل 2027 في مصر | الأسعار والمواصفات"
ROOT=Path("data/editorial/deepal-s09-2027-egypt-price-trims-reev-20261026.html")
SOURCES=[
  {"name":"s09-official-exterior","url":"https://deepal-eg.com/media/products/Home_Banner_2_1.jpg.jpeg",
   "alt":"صورة تعريفية رسمية من ديبال مصر لسيارة Deepal S09 الزرقاء من الأمام والجانب، وليست تجربة قيادة مصرية","role":"featured"},
  {"name":"s09-official-interior","url":"https://deepal-eg.com/media/products/Interior_Panoramic_1.78_1.jpg",
   "alt":"الصورة الترويجية الرسمية لمقصورة ديبال S09 بشاشتين أماميتين كما يعرضها موقع ديبال مصر","role":"inline"},
]
def req(url,body=None,auth=False):
    h={"Accept":"application/json","User-Agent":"A3tal-DeepalS09-LaunchEditorial/2026-10-26","Cache-Control":"no-cache,no-store"}
    if auth:h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=json.dumps(body,ensure_ascii=False).encode("utf8") if body is not None else None
    if data is not None:h["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=h,method="POST" if data is not None else "GET"),timeout=210) as r:return json.load(r)
def wp(path):return req(SITE+path)
def bridge(path,body=None):return req(API+path,body,True)
def count_words(c):return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+",re.sub("<[^>]+>"," ",c)))
def posts_exact(slug,typ="posts"):
    q=urllib.parse.urlencode({"slug":slug,"_fields":"id,slug,title,status,link,featured_media,content,categories,yoast_head_json"})
    return wp("/wp-json/wp/v2/"+typ+"?"+q)
def safe_check():
    body=ROOT.read_text("utf-8")
    if count_words(body)<2500 or body.count("<table")<3 or body.count("<h3>")<8 or "<h1" in body.lower():
        raise RuntimeError("Long-form depth/sections/table/H1 preflight failure")
    if body.count("{{a3tal_image:detail}}")!=1 or not all(x in body for x in [
        "2,850,000","3,100,000","250 ألف","595","637","NEDC","WLTP","Signature",
        "https://deepal-eg.com/ar/models/deepal-s09/","https://a3tal.com/cars/deepal-s07-2026-egypt/"]):
        raise RuntimeError("Critical facts and source/intent quality preflight failure")
    if any(s in body for s in ["{{a3tal_image:hero}}","<!-- TODO","lorem ipsum"]):
        raise RuntimeError("Unresolved placeholders")
    # Authenticated indexed title search catches drafts and hidden duplicate titles.
    scan=bridge("/search-posts?"+urllib.parse.urlencode({"search":"ديبال S09","limit":100}))
    for row in scan.get("items",[]):
        title=(row.get("title") or "").lower()
        slug=row.get("slug") or ""
        if (("s09" in title or "s09" in slug) and
            (("سعر" in title or "price" in slug) and slug!=SLUG)):
            raise RuntimeError("S09 duplicate price intent at existing slug: "+str(row))
    existing=posts_exact(SLUG)
    if len(existing)>1:raise RuntimeError("Multiple posts have same exact slug")
    car=posts_exact(CAR_SLUG,"a3tal-cars")
    if len(car)>1:raise RuntimeError("Multiple vehicle records have same exact slug")
    if car and car[0].get("title",{}).get("rendered","").strip()!=CAR_TITLE:
        raise RuntimeError("Refusing to modify an existing different vehicle identity")
    print("PRECHECK_UNIQUE_PRICE_INTENT",count_words(body),"words","existing_post",len(existing),"existing_car",len(car),flush=True)
    return body,existing,car
def process_image(src):
    url=src["url"]
    if not url.startswith("https://deepal-eg.com/media/products/"):
        raise RuntimeError("Only verified local manufacturer model image asset URLs allowed")
    # The assets are manufacturer-owned promotional images used for model identification.
    # Do not claim Creative Commons rights or third-party photography provenance.
    request=urllib.request.Request(url,headers={"User-Agent":"A3tal-Editorial/2026-10-26 (exact manufacturer image sourced https://deepal-eg.com/ar/models/deepal-s09/)","Accept":"image/jpeg,image/png,image/*"})
    with urllib.request.urlopen(request,timeout=80) as r:
        mime=r.headers.get("Content-Type","")
        raw=r.read(15_000_000)
    if not 30000<len(raw)<14_000_000 or not mime.startswith("image/"):
        raise RuntimeError("Manufacturer photo resolution/MIME failed")
    with Image.open(io.BytesIO(raw)) as im:
        im=ImageOps.exif_transpose(im).convert("RGB")
        if im.width<950 or im.height<490:raise RuntimeError("Low resolution manufacturer S09 photo")
        if src["role"]=="featured":
            im=ImageOps.fit(im,(1200,675),method=Image.Resampling.LANCZOS,centering=(.5,.5))
        else:
            im.thumbnail((1200,900),Image.Resampling.LANCZOS)
        out=io.BytesIO();im.save(out,format="WEBP",quality=88,method=6)
    b=out.getvalue()
    if not 12000<len(b)<2000000:raise RuntimeError("WebP output unexpected")
    print("OFFICIAL_MODEL_IMAGE_READY",src["name"],"bytes",len(b),"source",url,flush=True)
    return {"key":"hero" if src["role"]=="featured" else "detail",
      "role":src["role"],"filename":"a3tal-"+src["name"]+"-deepal-egypt-source-20261026.webp",
      "image_base64":base64.b64encode(b).decode("ascii"),"convert_webp":False,
      "alt":src["alt"],"caption":"صورة تعريفية أصلية منشورة على موقع ديبال مصر الرسمي لطراز S09. © أصحاب الحقوق/ديبال، للاستخدام التحريري. المصدر: "+url,
      "placeholder":"{{a3tal_image:detail}}"}
def get_post(pid):
    fields=urllib.parse.urlencode({"_fields":"id,slug,status,type,link,featured_media,categories,content,yoast_head_json"})
    return wp("/wp-json/wp/v2/posts/"+str(pid)+"?"+fields)
def verify_post(pid):
    live=get_post(pid)
    rendered=(live.get("content") or {}).get("rendered","")
    seo=live.get("yoast_head_json") or {}
    if (live["slug"],live["status"])!=(SLUG,"publish") or not live.get("featured_media") or 374 not in live.get("categories",[]):
        raise RuntimeError("Article slug, status, category or cover drift")
    if count_words(rendered)<2500 or "{{a3tal_image" in rendered or "s09-official-interior" not in rendered:
        raise RuntimeError("Article content insufficient or exact S09 interior missing")
    if "2,850,000" not in rendered or "3,100,000" not in rendered:
        raise RuntimeError("Prices not actually rendered")
    if (seo.get("robots") or {}).get("index")=="noindex" or seo.get("canonical")!=live["link"]:
        raise RuntimeError("Article canonical or noindex error")
    if not seo.get("og_image"):raise RuntimeError("Article missing OG image")
    print("LIVE_PRICE_GUIDE_VERIFIED",pid,count_words(rendered),"words","FEATURED",live["featured_media"],"URL",live["link"],flush=True)
    return live
def create_post(body,exists):
    if exists:
        row=exists[0]
        if row.get("status")!="publish" or not row.get("featured_media"):
            raise RuntimeError("Existing exact article but partial: manual reconciliation needed")
        return verify_post(row["id"])
    photos=[process_image(x) for x in SOURCES]
    # Vehicle encyclopedia permalink is created after this article.
    body += '\n<p>للمعلومات الفنية المركزة والربط مع الموسوعة، راجع <a href="'+SITE+'/cars/'+CAR_SLUG+'/">بطاقة ديبال S09 موديل 2027 في موسوعة السيارات</a>.</p>'
    payload={"post":{"title":TITLE,"slug":SLUG,"status":"publish","categories":[374],
        "content":body,
        "excerpt":"ديبال S09 2027 رسميًا في مصر: Premium بـ2,850,000 جنيه وSignature بـ3,100,000 جنيه. الفرق بين الفئتين، بطارية 40.18 ك.و.س، المدى والتعليق الهوائي والصيانة.",
        "meta":{"_yoast_wpseo_title":"سعر ديبال S09 2027 في مصر | الفئات والمواصفات",
                "_yoast_wpseo_metadesc":"سعر ديبال S09 موديل 2027 في مصر: Premium بـ2.85 مليون وSignature بـ3.1 مليون، مقارنة الفرق 250 ألف جنيه، المدى، REEV، الضمان.",
                "_yoast_wpseo_focuskw":"سعر ديبال S09 2027 في مصر"}},
      "media":photos}
    try:
        result=bridge("/publish-bundle",payload)
    except (TimeoutError,urllib.error.URLError) as e:
        print("AMBIGUOUS_PUBLISH_VERIFY_NOT_RETRY",type(e).__name__,flush=True)
        rows=posts_exact(SLUG)
        if not rows or rows[0].get("status")!="publish" or not rows[0].get("featured_media"):raise
        result={"post":{"id":rows[0]["id"],"status":"publish"}}
    post=result.get("post") or {}
    if post.get("status")!="publish" or not post.get("id"):raise RuntimeError("Bundle did not acknowledge publication")
    return verify_post(int(post["id"]))
def ensure_car(live,existing):
    if existing:
        car=existing[0]
        if car.get("status")!="publish" or not car.get("featured_media") or car["featured_media"]!=live["featured_media"]:
            raise RuntimeError("Existing car entity inconsistent with article cover; manual inspection required")
        print("EXISTING_VEHICLE_ENTITY_VERIFIED",car["id"],car["link"],flush=True)
        return
    brief=('<p>ديبال S09 موديل 2027 في مصر سيارة SUV فاخرة بستة مقاعد 2+2+2، بمنظومة دفع كهربائية '
           'ممتدة المدى REEV ومحرك بنزين 1.5 تيربو لتوليد الكهرباء ومحركين كهربائيين للدفع الرباعي. '
           'سعر Premium المعلن 2,850,000 جنيه وسعر Signature هو 3,100,000 جنيه، بتاريخ 26 أكتوبر 2026. '
           'قدرة المحركات القصوى وفق ديبال مصر 362 كيلوواط وبطارية 40.18 كيلوواط/ساعة. '
           'تختلف تقارير العزم بين 595 و637 نيوتن متر؛ لا نحسم المواصفة قبل كتالوج الوكيل.'
           '</p><p>لقراءة الفئات والتجهيزات والفرق بين معايير المدى والتعليق الهوائي والضمان، '
           '<a href="'+live["link"]+'">اطلع على دليل أسعار ديبال S09 الكامل</a>. '
           'المصدر: <a href="https://deepal-eg.com/ar/models/deepal-s09/">ديبال مصر</a>.</p>')
    payload={"op":"platform_entity_upsert","type":"a3_car","slug":CAR_SLUG,"title":CAR_TITLE,
            "status":"publish","featured_media":live["featured_media"],"content":brief,
            "excerpt":"ديبال S09 2027 في مصر: 6 مقاعد REEV، فئتان من 2,850,000 إلى 3,100,000 جنيه وفق إطلاق أكتوبر 2026.",
            "meta":{"_a3_year":"2027","_a3_price_min":"2850000","_a3_price_max":"3100000",
               "_a3_currency":"EGP","_a3_engine_cc":"1500","_a3_power_hp":"485",
               "_a3_fuel":"REEV","_a3_transmission":"Electric drive",
               "_a3_drivetrain":"AWD","_a3_seats":"6",
               "_a3_source_url":"https://deepal-eg.com/ar/models/deepal-s09/",
               "_a3_source_checked_at":"2026-10-26"},
            "confirm":True,"dangerous":True}
    result=bridge("/admin",payload)
    if not result.get("ok") or not (result.get("result") or {}).get("id"):
        raise RuntimeError("No confirmation of car entity upsert")
    rows=posts_exact(CAR_SLUG,"a3tal-cars")
    if len(rows)!=1 or rows[0].get("slug")!=CAR_SLUG or rows[0].get("status")!="publish" or rows[0].get("featured_media")!=live["featured_media"]:
        raise RuntimeError("New car entity live readback failure")
    for key,value in (("_a3_price_min","2850000"),("_a3_price_max","3100000"),
                      ("_a3_year","2027"),("_a3_source_checked_at","2026-10-26")):
        m=bridge("/admin?"+urllib.parse.urlencode({"op":"post_meta","post_id":rows[0]["id"],"key":key}))
        found=str((m.get("result") or {}).get(key,"")).strip()
        if found!=value:raise RuntimeError("New car metadata mismatch "+key+" = "+repr(found))
    print("LIVE_VEHICLE_ENTRY_VERIFIED",rows[0]["id"],"FEATURED",rows[0]["featured_media"],"URL",rows[0]["link"],flush=True)
def main():
    body,exists,car=safe_check()
    live=create_post(body,exists)
    ensure_car(live,car)
    print("DEEPAL_S09_PRICE_ARTICLE_AND_CAR_MODEL_VERIFIED_COMPLETE",flush=True)
if __name__=="__main__":main()
