#!/usr/bin/env python3
"""One-off, safeguarded Geely EX5 EM-R launch price article. Live via GitHub -> A3tal Bridge.
Authentic CC BY-SA 4.0 images are explicitly EX5 EM-i illustrative photos; never masquerade as EM-R.
"""
import base64,io,json,os,re,time,urllib.parse,urllib.request,urllib.error
from pathlib import Path
from PIL import Image,ImageOps

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
PATH=Path("data/editorial/geely-ex5-em-r-price-egypt-20261025.html")
SLUG="geely-ex5-em-r-egypt-price-trims-reev"
TITLE="سعر جيلي EX5 EM-R في مصر: 3 فئات من 1.35 إلى 1.6 مليون جنيه وهل تستحق؟"
IMAGE_SPECS=[
 {"name":"hero","file":"Geely EX5 EM-i 1.5 Max PHEV 2026 (1).jpg",
  "alt":"صورة حقيقية من الفلبين لجيلي EX5 EM-i للتوضيح، وليست صورة موثقة لنسخة EM-R المصرية"},
 {"name":"detail","file":"Geely EX5 EM-i 1.5 Max PHEV 2026 (2).jpg",
  "alt":"زاوية أخرى فوتوغرافية لسيارة Geely EX5 EM-i المشابهة بالاسم، لا تؤكد مواصفات EX5 EM-R"}
]
def jget(path,protected=False,data=None):
    head={"Accept":"application/json","User-Agent":"A3tal-Editorial-EX5-EMR/2026-10-25","Cache-Control":"no-cache,no-store"}
    if protected:
        head.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    payload=None
    if data is not None:
        payload=json.dumps(data,ensure_ascii=False).encode("utf-8")
        head["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request((API if protected else SITE)+path,headers=head,data=payload,method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req,timeout=210) as f:return json.load(f)
def wordpress_list(type,**q):
    return jget("/wp-json/wp/v2/"+type+"?"+urllib.parse.urlencode(q))
def words(content):
    return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+",re.sub("<[^>]*>"," ",content)))
def image(spec):
    filename=spec["file"]
    quote=urllib.parse.quote(filename,safe="")
    url="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+quote
    req=urllib.request.Request(url,headers={"User-Agent":"A3tal Editorial (https://a3tal.com; licensed CC BY-SA 4.0 images with attribution)","Accept":"image/jpeg,image/*"})
    with urllib.request.urlopen(req,timeout=70) as f:
        raw=f.read(9_000_000)
    with Image.open(io.BytesIO(raw)) as im:
        im=ImageOps.exif_transpose(im).convert("RGB")
        if min(im.width,im.height)<850:raise RuntimeError("Photo is not high-resolution")
        if spec["name"]=="hero":
            im=ImageOps.fit(im,(1200,675),method=Image.Resampling.LANCZOS,centering=(.5,.5))
        else:
            im.thumbnail((1200,900),Image.Resampling.LANCZOS)
        out=io.BytesIO()
        im.save(out,"WEBP",quality=86,method=6)
    data=out.getvalue()
    if not 15_000<len(data)<1_500_000:raise RuntimeError("WebP byte size out of range")
    source="https://commons.wikimedia.org/wiki/File:"+filename.replace(" ","_")
    print("LICENSED_PHOTO_READY",spec["name"],len(data),source,flush=True)
    return {"key":spec["name"],"role":"featured" if spec["name"]=="hero" else "inline",
            "filename":"a3tal-geely-ex5-emr-ex5-emi-illustrative-"+spec["name"]+"-20261025.webp",
            "image_base64":base64.b64encode(data).decode("ascii"),
            "convert_webp":False,
            "alt":spec["alt"],
            "caption":"صورة توضيحية حقيقية لسيارة EX5 EM-i وليس EX5 EM-R المصرية. تصوير: Captainmorlypogi1959، رخصة CC BY-SA 4.0، نسخة WebP مقتصة. المصدر: "+source,
            "placeholder":"{{a3tal_image:detail}}"}
def check_duplicate():
    # Exact slug check plus distinct content search across published posts, pages, cars.
    hits=[]
    # The production WAF blocks some public REST search query strings from Actions.
    # Use the authenticated Direct Bridge post/page search, not an unverified skip.
    for token in ("EX5 EM-R","EX5 EMR","جيلي EX5"):
        result=jget("/search-posts?"+urllib.parse.urlencode({"search":token,"limit":100}),protected=True)
        for r in result.get("items",[]):
            title=r.get("title","")
            if ("em-r" in (title+" "+r.get("slug","")).lower()
                or "emr" in (title+" "+r.get("slug","")).lower()
                or "إي إم آر" in title):
                hits.append({"type":r.get("type","post"),"slug":r["slug"],"id":r["id"],"link":r["link"]})
    rows=wordpress_list("a3tal-cars",per_page=100,_fields="id,slug,title,link,status")
    if not isinstance(rows,list) or len(rows)<26:
        raise RuntimeError("Car encyclopedia inventory cannot be verified")
    for r in rows:
        t=(r.get("title") or {}).get("rendered","")
        if "em-r" in (t+" "+r.get("slug","")).lower() or "emr" in (t+" "+r.get("slug","")).lower():
            hits.append({"type":"a3tal-cars","slug":r["slug"],"id":r["id"],"link":r["link"]})
    unique={(r["type"],r["id"]):r for r in hits}
    exact=wordpress_list("posts",slug=SLUG,per_page=5,_fields="id,slug,status,featured_media,content,link,yoast_head_json")
    if len(exact)>1:raise RuntimeError("Duplicate exact slug unexpectedly")
    for r in unique.values():
        if r["slug"]!=SLUG:raise RuntimeError("Another existing EM-R resource: "+str(r))
    if exact:
        p=exact[0]
        if p["status"]=="publish" and p.get("featured_media") and words((p.get("content") or {}).get("rendered",""))>=1500:
            print("ALREADY_PUBLISHED_VERIFIED",p["id"],p["link"],flush=True)
            return p["id"]
        raise RuntimeError("Existing slug draft or incomplete: reconcile without duplicate")
    # Related links must be publicly live for proper internal linking.
    for route in ("cars/deepal-s07-2026-egypt/","cars/geely-monjaro-em-i-egypt/","cars/"):
        req=urllib.request.Request(SITE+"/"+route,headers={"User-Agent":"A3tal-Editorial-Preflight"})
        with urllib.request.urlopen(req,timeout=40) as response:
            if response.status!=200:raise RuntimeError("Related link not live "+route)
    return None
def main():
    if not KEY:raise RuntimeError("Missing A3TAL_API_KEY")
    source=PATH.read_text("utf8")
    if words(source)<1700 or source.count("<table")<2 or "<h1" in source.lower() or source.count("{{a3tal_image:detail}}")!=1:
        raise RuntimeError("Editorial depth, tables or photo placeholder failed")
    if not all(x in source for x in ("1,350,000","1,500,000","1,600,000","18.4","29.8","EX5 EM-i")):
        raise RuntimeError("Critical fact/variant disclaimer missing")
    old=check_duplicate()
    if old:return
    photos=[image(x) for x in IMAGE_SPECS]
    payload={"post":{"title":TITLE,"slug":SLUG,"type":"post","status":"publish",
        "content":source,"categories":[374],
        "excerpt":"سعر جيلي EX5 EM-R في مصر بعد طرح أكتوبر 2026: 1.35 و1.5 و1.6 مليون جنيه لثلاث فئات، مع شرح REEV والبطارية والفروق قبل الحجز.",
        "meta":{"_yoast_wpseo_title":"سعر جيلي EX5 EM-R في مصر | الفئات والبطارية والمدى",
                "_yoast_wpseo_metadesc":"سعر جيلي EX5 EM-R بمصر من 1.35 إلى 1.6 مليون جنيه: مقارنة الفئات الثلاث، بطاريات 18.4 و29.8 كيلوواط/ساعة، مدى REEV، والشراء.",
                "_yoast_wpseo_focuskw":"سعر جيلي EX5 EM-R في مصر"}},"media":photos}
    try:
        result=jget("/publish-bundle",protected=True,data=payload)
    except (TimeoutError,urllib.error.URLError) as exc:
        # Never blind-retry a write after a timeout, check whether WordPress committed it.
        print("AMBIGUOUS_WRITE_VERIFY_ONLY",type(exc).__name__,flush=True)
        rows=wordpress_list("posts",slug=SLUG,_fields="id,slug,status,link,featured_media,content")
        if not rows or rows[0].get("status")!="publish" or not rows[0].get("featured_media"):
            raise
        result={"post":{"id":rows[0]["id"],"status":"publish"},"media":[]}
    item=result.get("post") or {}
    if item.get("status")!="publish" or not item.get("id"):
        raise RuntimeError("No published post acknowledgement")
    pid=int(item["id"])
    live=jget("/wp-json/wp/v2/posts/"+str(pid)+"?_fields=id,slug,status,link,featured_media,categories,content,yoast_head_json")
    rendered=(live.get("content") or {}).get("rendered","")
    seo=live.get("yoast_head_json") or {}
    if live["slug"]!=SLUG or live["status"]!="publish" or not live.get("featured_media") or 374 not in live.get("categories",[]):
        raise RuntimeError("Production slug/category/media status mismatch")
    if words(rendered)<1700 or "{{a3tal_image" in rendered:
        raise RuntimeError("Content or inline photo not rendered")
    if "a3tal-geely-ex5-emr-ex5-emi-illustrative-detail" not in rendered:
        raise RuntimeError("Distinct photo missing in published body")
    if (seo.get("robots") or {}).get("index")=="noindex":raise RuntimeError("Unexpected noindex")
    if seo.get("canonical")!=live.get("link"):raise RuntimeError("Canonical differs from exact post URL")
    print("ARTICLE_PUBLISHED_VERIFIED",pid,"WORDS",words(rendered),"FEATURED",live["featured_media"],"URL",live["link"],flush=True)
if __name__=="__main__":main()
