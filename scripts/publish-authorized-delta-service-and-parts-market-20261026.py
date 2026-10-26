#!/usr/bin/env python3
"""Publish October 2026 verified authorized Kia Delta service centers and SKU-grounded car-parts prices through GitHub -> A3tal Direct Bridge.
Guard exact slug + search intent, preserve existing WordPress entries, use authentic
licensed photographic images and confirm live SEO, category, inline and featured WebP.
"""
import base64,io,json,os,re,time,urllib.parse,urllib.request,urllib.error
from pathlib import Path
from PIL import Image,ImageOps

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY missing; refusing publication")
ARTICLES=[
{"slug":"kia-authorized-service-centers-delta-mansoura-tanta-mahalla-egypt",
 "title":"مراكز خدمة كيا المعتمدة في الدلتا: المنصورة وطنطا والمحلة بالأرقام والعناوين",
 "file":"data/editorial/kia-authorized-service-delta-mansoura-tanta-mahalla-20261026.html",
 "category":33,"query":["مراكز كيا معتمدة الدلتا المنصورة طنطا المحلة","كيا عيسى كارز ابوشادي الجندي","مراكز خدمة كيا في الدلتا"],
 "excerpt":"دليل مراكز كيا المعتمدة في الدلتا: عيسى كارز المنصورة وأبوشادي موتورز طنطا والجندي المحلة، الأرقام الرسمية والحجز والتأكد من الضمان.",
 "seo_title":"مراكز كيا المعتمدة في الدلتا | المنصورة وطنطا والمحلة",
 "meta":"عناوين وأرقام مراكز كيا المعتمدة بالدلتا: عيسى كارز المنصورة 01001772910، أبوشادي طنطا 01224922245، الجندي المحلة 01288888228.",
 "kw":"مراكز خدمة كيا المعتمدة في الدلتا",
 "images":[
  {"role":"featured","name":"kia-delta-verified-service-hero","file":"Car lift in an auto repair shop with vehicles and tools present.jpg","author":"Shixart1985","license":"CC BY 2.0","alt":"ورشة خدمة سيارات حقيقية عامة خارج مصر، لا تمثل مركز كيا محددا في المنصورة أو طنطا أو المحلة"},
  {"role":"inline","name":"kia-delta-verified-service-detail","file":"Car repair in an auto shop with tools and equipment present on the floor and a partially disassembled vehicle on a lift.jpg","author":"Shixart1985","license":"CC BY 2.0","alt":"فني صيانة وورشة حقيقية للتوضيح، وليست صور مراكز كيا الدلتا المسماة"}
 ]},
{"slug":"egypt-car-spare-parts-price-update-october-2026-verified-skus",
 "title":"أسعار قطع غيار السيارات في مصر أكتوبر 2026: أمثلة موثقة من شانجان وهيونداي وتغييرات السوق",
 "file":"data/editorial/egypt-car-spare-parts-prices-october-2026-verified-market-update.html",
 "category":85,"query":["تحديث اسعار قطع الغيار اكتوبر 2026","قطع غيار شانجان هيونداي اسعار اكتوبر","تغيرات اسعار قطع الغيار مصر 2026"],
 "excerpt":"رصد 26 أكتوبر 2026 لأسعار قطع غيار منشورة رسميًا من شانجان وعروض تيل إلنترا AD من متجر مستقل، مع الفصل بين فروق المنتجات والزيادات الحقيقية.",
 "seo_title":"أسعار قطع غيار السيارات أكتوبر 2026 | مصدر وسعر ورقم قطعة",
 "meta":"أسعار قطع غيار مصر 26 أكتوبر 2026: فلتر زيت شانجان 100، سير 1140، بوجيهات 1834، وعروض تيل النترا AD مع روابط الموردين وتحركات السوق.",
 "kw":"أسعار قطع غيار السيارات في مصر أكتوبر 2026",
 "images":[
  {"role":"featured","name":"egypt-parts-market-20261026-hero","file":"Car parts shop in Baku.jpg","author":"ChanisCaucasi","license":"CC BY 4.0","alt":"متجر قطع غيار سيارات حقيقي في باكو لتوضيح التسعير وليس موردًا داخل مصر"},
  {"role":"inline","name":"egypt-parts-market-20261026-detail","file":"Auto Spare Parts Shop on the Roadside.jpg","author":"Johnnybam","license":"CC BY-SA 4.0","alt":"صورة فوتوغرافية لمحل قطع غيار حقيقي خارج مصر، لا تمثل أي متجر مصري ورد بالمقال"}
 ]}
]
def request(url,data=None,auth=False):
    headers={"Accept":"application/json","User-Agent":"A3tal Editorial Mechanical Electrical/2026-10-25","Cache-Control":"no-cache,no-store"}
    if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    payload=None
    if data is not None:
        payload=json.dumps(data,ensure_ascii=False).encode("utf-8")
        headers["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,data=payload,headers=headers,method="POST" if payload is not None else "GET"),timeout=210) as response:
        return json.load(response)
def bridge(route,data=None):
    return request(API+route,data,True)
def count_words(content):
    return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+",re.sub("<[^>]+>"," ",content)))
def existing_slug(slug):
    # The authenticated Bridge search covers posts, pages and drafts; exact slug is checked in results.
    r=bridge("/search-posts?"+urllib.parse.urlencode({"search":slug.replace("-"," "),"limit":100}))
    all=list(r.get("items",[]))
    # public exact lookup gives published content media and SEO for idempotency
    url=SITE+"/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":slug,"_fields":"id,slug,status,link,featured_media,content"})
    try:
        public=request(url)
    except urllib.error.HTTPError as e:
        if e.code!=403:raise
        public=[]
    return all,[x for x in public if x.get("slug")==slug]
def preflight(article):
    c=Path(article["file"]).read_text("utf-8")
    if count_words(c)<1800 or c.count("<table")<2 or "<h1" in c.lower() or c.count("{{a3tal_image:detail}}")!=1:
        raise RuntimeError("Editorial gate failed "+article["slug"]+" "+str(count_words(c)))
    if "<a href=\"https://a3tal.com/" not in c or "<h3>" not in c or "commons.wikimedia.org" not in c:
        raise RuntimeError("Internal link, FAQ or photo attribution missing "+article["slug"])
    found={}
    for q in article["query"]:
        r=bridge("/search-posts?"+urllib.parse.urlencode({"search":q,"limit":100}))
        for x in r.get("items",[]):
            # Avoid over-restricting general articles; exact title and exact slug matter.
            norm=lambda s:" ".join(s.lower().replace("؟"," ").replace(":"," ").split())
            title=norm(x.get("title",""))
            if x.get("slug")==article["slug"] or title==norm(article["title"]):
                found[x["id"]]=x
    all,public=existing_slug(article["slug"])
    for x in all:
        if x.get("slug")==article["slug"]:found[x["id"]]=x
    if len(found)>1:raise RuntimeError("Duplicate post identity: "+str(found))
    if found:
        old=list(found.values())[0]
        if old["slug"]!=article["slug"]:raise RuntimeError("Existing exact title at other slug: "+str(old))
        if len(public)==1 and public[0].get("featured_media") and count_words(public[0].get("content",{}).get("rendered",""))>=1800:
            print("ALREADY_LIVE_VERIFIED",article["slug"],old["id"],flush=True)
            return None,True
        # May be published but public REST blocked; do not create duplicate.
        raise RuntimeError("Exact slug already exists but publication state needs manual review: "+str(old))
    if len(public)==1:
        if public[0].get("featured_media") and count_words(public[0].get("content",{}).get("rendered",""))>=1800:
            print("ALREADY_LIVE_VERIFIED",article["slug"],public[0]["id"],flush=True)
            return None,True
        raise RuntimeError("Partially published slug: manual review "+article["slug"])
    return c,False
def photograph(d):
    filename=d["file"]
    url="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(filename,safe="")
    req=urllib.request.Request(url,headers={"User-Agent":"A3tal Editorial/1.0 (credit in body: https://a3tal.com)","Accept":"image/jpeg,image/*"})
    with urllib.request.urlopen(req,timeout=70) as resp: raw=resp.read(22_000_000)
    with Image.open(io.BytesIO(raw)) as im:
        im=ImageOps.exif_transpose(im).convert("RGB")
        if min(im.width,im.height)<700:raise RuntimeError("Insufficient authentic photo resolution: "+filename)
        if d["role"]=="featured":im=ImageOps.fit(im,(1200,675),method=Image.Resampling.LANCZOS)
        else: im.thumbnail((1200,900),Image.Resampling.LANCZOS)
        out=io.BytesIO();im.save(out,"WEBP",quality=85,method=6)
    data=out.getvalue()
    if not 15000<len(data)<1600000:raise RuntimeError("Photo output size unexpectedly small or large")
    src="https://commons.wikimedia.org/wiki/File:"+filename.replace(" ","_")
    print("REAL_PHOTO_READY",d["name"],len(data),d["license"],src,flush=True)
    return {"key":"hero" if d["role"]=="featured" else "detail",
            "role":d["role"],"filename":"a3tal-"+d["name"]+"-original-20261025.webp",
            "image_base64":base64.b64encode(data).decode("ascii"),"convert_webp":False,
            "alt":d["alt"],"caption":"صورة فوتوغرافية توضيحية من Wikimedia Commons؛ تصوير: "+d["author"]+"؛ الترخيص "+d["license"]+"؛ تم القص والتحويل إلى WebP. المصدر: "+src,
            "placeholder":"{{a3tal_image:detail}}"}
def publish(article,content):
    photos=[photograph(i) for i in article["images"]]
    payload={"post":{"title":article["title"],"slug":article["slug"],"content":content,"status":"publish","categories":[article["category"]],
          "excerpt":article["excerpt"],
          "meta":{"_yoast_wpseo_title":article["seo_title"],
                  "_yoast_wpseo_metadesc":article["meta"],"_yoast_wpseo_focuskw":article["kw"]}},
          "media":photos}
    try:
        result=bridge("/publish-bundle",payload)
    except (urllib.error.URLError,TimeoutError) as e:
        print("AMBIGUOUS_WRITE_NO_RETRY",type(e).__name__,flush=True)
        # No blind resend, verify exact slug.
        rows=request(SITE+"/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":article["slug"],"_fields":"id,status,featured_media"}))
        if not rows or rows[0].get("status")!="publish" or not rows[0].get("featured_media"):raise
        result={"post":rows[0]}
    post=result.get("post") or {}
    if not post.get("id") or post.get("status")!="publish":raise RuntimeError("Bundle publish missing post ID")
    pid=int(post["id"])
    live=request(SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?_fields=id,slug,status,link,featured_media,categories,content,yoast_head_json")
    body=(live.get("content") or {}).get("rendered","")
    yoast=live.get("yoast_head_json") or {}
    if live.get("slug")!=article["slug"] or live.get("status")!="publish" or article["category"] not in live.get("categories",[]) or not live.get("featured_media"):
        raise RuntimeError("Published identity, image or taxonomy failed")
    if count_words(body)<1800 or "{{a3tal_image" in body or "a3tal-"+article["images"][1]["name"] not in body:
        raise RuntimeError("Published content or photo replacement incomplete")
    if (yoast.get("robots") or {}).get("index")=="noindex" or yoast.get("canonical")!=live.get("link"):
        raise RuntimeError("SEO indexing or canonical failed")
    if not (yoast.get("og_image") or []):raise RuntimeError("No og image")
    print("ARTICLE_PUBLISHED_LIVE_VERIFIED",pid,"WORDS",count_words(body),"FEATURED",live["featured_media"],"CATEGORY",article["category"],"URL",live["link"],flush=True)
def main():
    ready=[]
    for article in ARTICLES:
        c,already=preflight(article)
        ready.append((article,c,already))
    print("PRECHECK_COMPLETE duplicate-safe, two independent intents",flush=True)
    for article,content,already in ready:
        if not already:publish(article,content)
        time.sleep(3)
    print("DELTA_AUTHORIZED_SERVICE_AND_PRICE_SNAPSHOT_PUBLISHED_VERIFIED",flush=True)
if __name__=="__main__":main()
