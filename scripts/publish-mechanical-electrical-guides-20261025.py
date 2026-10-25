#!/usr/bin/env python3
"""Publish exactly two new original diagnostic guides through GitHub -> A3tal Direct Bridge.
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
{"slug":"clutch-pedal-sinks-floor-hydraulic-master-slave-diagnosis","title":"دواسة الدبرياج بتغوص تحت ومش بترجع؟ تشخيص الماستر والسلندر قبل تغيير الطقم",
 "file":"data/editorial/clutch-pedal-sinks-to-floor-hydraulic-diagnosis-20261025.html",
 "category":8,"query":["دواسة الدبرياج بتغوص","الدبرياج مش بترجع","الماستر والسلندر","clutch pedal sinks floor"],
 "excerpt":"الدبرياج بيغوص للأرض ومش بيرجع أو الغيار مش بيعشق؟ دليل يفرق بين ماستر الدبرياج والسلندر والهواء والسلك وتلف طقم الاحتكاك.",
 "seo_title":"دواسة الدبرياج بتغوص ومش بترجع | الأسباب والتشخيص",
 "meta":"أسباب هبوط دواسة الدبرياج وعدم رجوعها: فحص الماستر العلوي والسلندر والتسريب ودخول الهواء ومتى لا يجوز القيادة أو تغيير الطقم.",
 "kw":"دواسة الدبرياج بتغوص ومش بترجع",
 "images":[
  {"role":"featured","name":"clutch-hero","file":"Brake fluid reservoir in Škoda Fabia I.jpg","author":"Frettie","license":"CC BY 3.0","alt":"صورة حقيقية لخزان سائل فرامل سيارة سكودا فابيا الأول الذي يغذي دائرة دبرياج هيدروليكية؛ توضيحية وليست عطلًا موثقًا"},
  {"role":"inline","name":"clutch-detail","file":"M5OD transmission, input.jpg","author":"J.C. Fields / Typhoon","license":"CC BY-SA 3.0","alt":"صورة حقيقية لبلية الفصل والسلندر الهيدروليكي المركزي داخل جرس فتيس مانيوال Mazda M5OD"}
 ]},
{"slug":"car-electricity-cuts-off-over-bumps-dashboard-restarts","title":"كهرباء العربية بتقطع مع المطبات والعدادات بتطفي؟ تشخيص القطاش والأرضي والضفيرة",
 "file":"data/editorial/car-electrical-power-cuts-over-bumps-20261025.html",
 "category":13,"query":["الكهرباء بتقطع مع المطبات","العدادات بتطفي","الكهرباء بتقطع","car electricity cuts off over bumps"],
 "excerpt":"لو كهرباء العربية بتقطع مع المطب والعدادات أو الشاشة تطفي، اتعرف على فحص قطاش البطارية ونقاط الأرضي والضفيرة والريلاي.",
 "seo_title":"كهرباء العربية بتقطع مع المطبات | أسباب فصل العداد",
 "meta":"أسباب تقطيع كهرباء السيارة عند المطبات وإطفاء العدادات: قطاش البطارية، الأرضي، الضفيرة، علبة الفيوزات والـECU، وخطوات الفحص الآمن.",
 "kw":"كهرباء العربية بتقطع مع المطبات",
 "images":[
  {"role":"featured","name":"electric-hero","file":"Mechanic working on a car battery.jpg","author":"Kwamitsey","license":"CC BY 4.0","alt":"صورة فوتوغرافية حقيقية لفني يفحص بطارية سيارة داخل ورشة؛ صورة توضيحية لفحص الكهرباء"},
  {"role":"inline","name":"electric-detail","file":"Wires and connections inside a vehicle's electronic control unit during repair in a garage setting.jpg","author":"Shixart1985","license":"CC BY 2.0","alt":"فني كهرباء سيارات يفحص ضفيرة ووصلات وحدة تحكم إلكترونية داخل ورشة حقيقية"}
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
    print("PRECHECK_COMPLETE duplicate-safe, two independent intents",flush=True)
    for article,content,already in ready:
        if not already:publish(article,content)
        time.sleep(3)
    print("MECHANICAL_AND_ELECTRICAL_RELEASE_VERIFIED_COMPLETE",flush=True)
if __name__=="__main__":main()
