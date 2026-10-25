#!/usr/bin/env python3
"""Publish three original encyclopedia guides: suspension, parts and an official Kia-authorized center through GitHub -> A3tal Direct Bridge.
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
{"slug":"suspension-knock-after-replacing-shock-absorbers-diagnosis",
 "title":"العفشة بتخبط بعد تغيير المساعدين؟ تشخيص البطاحة والتثبيت ومسمار الميزان",
 "file":"data/editorial/suspension-clunk-after-new-shocks-struts-20261025.html",
 "category":11,"query":["بعد تغيير المساعدين","العفشة بتخبط بعد تغيير","مساعد جديد بيخبط","suspension knock new shocks"],
 "excerpt":"صوت خبط بعد تغيير المساعدين؟ دليل عملي لمراجعة مسامير التثبيت والبطاحات والبلية والسوستة ومسمار الميزان قبل شراء مساعدين جديدة.",
 "seo_title":"العفشة بتخبط بعد تغيير المساعدين | تشخيص بدون تخمين",
 "meta":"العفشة بتخبط بعد تركيب مساعدين جديدة؟ الأسباب وخطوات فحص البطاحة والبلية والجلب وتياش الميزان والتربيط، ومعايير Monroe الفنية.",
 "kw":"العفشة بتخبط بعد تغيير المساعدين",
 "images":[
  {"role":"featured","name":"shock-clunk-hero","file":"Radius rod sway bar.jpg","author":"RB30DE","license":"Public Domain","alt":"صورة فوتوغرافية حقيقية لقضيب اتزان وعفشة أمامية MacPherson؛ توضيحية ليست لموديل محدد"},
  {"role":"inline","name":"shock-clunk-detail","file":"Front suspension of Toyota Land Cruiser J60.jpg","author":"Pittigrilli","license":"CC BY-SA 4.0","alt":"صورة فوتوغرافية للعفشة الأمامية في تويوتا لاند كروزر J60، توضيحية لفروق أنظمة التعليق"}
 ]},
{"slug":"buy-correct-car-spare-parts-vin-oem-oes-aftermarket-egypt",
 "title":"شراء قطع غيار السيارة برقم الشاسيه VIN: الفرق بين الأصلي وOES وAftermarket",
 "file":"data/editorial/buy-car-spare-parts-using-vin-oem-oes-aftermarket-egypt-20261025.html",
 "category":85,"query":["قطع غيار برقم الشاسيه","قطع غيار OEM OES","رقم قطعة الغيار VIN","spare parts VIN OEM"],
 "excerpt":"تشتري قطع غيار من غير مقاسات غلط؟ شرح VIN ورقم القطعة OE والفروق بين Genuine وOEM وOES وAftermarket والفاتورة والضمان في مصر.",
 "seo_title":"شراء قطع غيار برقم الشاسيه VIN | الأصلي وOEM والبدائل",
 "meta":"كيف تشتري قطع الغيار برقم الشاسيه VIN؟ مطابقة أرقام OE، الفرق بين الأصلي وOES وAftermarket، وتحديد التوافق والضمان قبل الدفع.",
 "kw":"شراء قطع غيار برقم الشاسيه VIN",
 "images":[
  {"role":"featured","name":"spareparts-vin-hero","file":"Car parts shop in Baku.jpg","author":"ChanisCaucasi","license":"CC BY 4.0","alt":"متجر حقيقي لقطع غيار السيارات في باكو أذربيجان، توضيحي وليس محلًا في مصر"},
  {"role":"inline","name":"spareparts-vin-detail","file":"Auto Spare Parts Shop on the Roadside.jpg","author":"Johnnybam","license":"CC BY-SA 4.0","alt":"صورة توضيحية لمحل قطع غيار حقيقي في نيجيريا، وليست متجرًا مصريًا"}
 ]},
{"slug":"kia-benha-authorized-service-korean-center-address-phone",
 "title":"مركز خدمة كيا المعتمد في بنها: السنتر الكوري، العنوان والتليفون والحجز",
 "file":"data/editorial/kia-authorized-service-benha-korean-center-20261025.html",
 "category":33,"query":["السنتر الكوري بنها","كيا بنها مركز معتمد","كيا بنها السنتر الكوري","kia benha korean center"],
 "excerpt":"السنتر الكوري كيا بنها المعتمد: طريق مصر إسكندرية الزراعي خلف مصنع توشيبا، رقم 01002165317، ومواعيد 8 إلى 4:30 حسب كيا مصر.",
 "seo_title":"مركز كيا بنها المعتمد | السنتر الكوري العنوان والرقم",
 "meta":"مركز السنتر الكوري كيا بنها المعتمد رسميًا: العنوان خلف مصنع توشيبا على الطريق الزراعي، رقم 01002165317، مواعيد العمل والحجز والضمان.",
 "kw":"مركز خدمة كيا المعتمد في بنها",
 "images":[
  {"role":"featured","name":"kia-benha-illustrative-hero","file":"Car lift in an auto repair shop with vehicles and tools present.jpg","author":"Shixart1985","license":"CC BY 2.0","alt":"صورة فوتوغرافية لورشة سيارات عامة خارج مصر، ليست صورة السنتر الكوري أو مركز كيا بنها"},
  {"role":"inline","name":"kia-benha-illustrative-detail","file":"Car repair in an auto shop with tools and equipment present on the floor and a partially disassembled vehicle on a lift.jpg","author":"Shixart1985","license":"CC BY 2.0","alt":"ورشة صيانة سيارات حقيقية خارج مصر للتوضيح، لا تمثل داخل مركز السنتر الكوري كيا بنها"}
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
    with urllib.request.urlopen(req,timeout=70) as resp: raw=resp.read(11_000_000)
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
    print("PRECHECK_COMPLETE duplicate-safe, three independent intents",flush=True)
    for article,content,already in ready:
        if not already:publish(article,content)
        time.sleep(3)
    print("SUSPENSION_PARTS_SERVICE_RELEASE_VERIFIED_COMPLETE",flush=True)
if __name__=="__main__":main()
