#!/usr/bin/env python3
"""Fact-checked Renault Boreal 2027 Egypt guide: safe single-post publish via A3tal Direct Bridge."""
import base64, io, json, os, re, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
SLUG="renault-boreal-2027-egypt-price-trims"
URL=SITE+"/"+SLUG+"/"
TITLE="سعر رينو بوريال 2027 في مصر يبدأ من 1.47 مليون جنيه.. هل تستحق الشراء؟"
PATH=Path("data/editorial/renault-boreal-2027-price-egypt-20261102.html")
COVER_SOURCES=[
 "https://renault-mediaroom-prensa.s3.amazonaws.com/18073/R_BOREAL_2K_16X9_P01B.jpg",
 "https://renault-mediaroom-prensa.s3.amazonaws.com/18073/conversions/R_BOREAL_2K_16X9_P01B-sd.jpg",
 "https://media.renault.com/wp-content/uploads/2026/06/d579e51d9848cfe1847fbb0487554546-l.jpg.webp"
]
DETAIL_SOURCES=[
 "https://renault-mediaroom-prensa.s3.amazonaws.com/18135/DSC00255-1.jpg",
 "https://renault-mediaroom-prensa.s3.amazonaws.com/18135/conversions/DSC00255-1-sd.jpg",
 "https://media.renault.com/wp-content/uploads/2026/06/af4b829cb8fe0dadc0d17295790d4252-m.jpg.webp"
]

def jget(path,auth=False,data=None):
    head={"Accept":"application/json","User-Agent":"A3tal-Editorial-Renault-Boreal-2027","Cache-Control":"no-cache,no-store"}
    if auth:
        if not KEY:raise RuntimeError("A3TAL_API_KEY is missing")
        head["X-A3tal-Key"]=KEY
        head["Authorization"]="Bearer "+KEY
    payload=None
    if data is not None:
        payload=json.dumps(data,ensure_ascii=False).encode("utf-8")
        head["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request((API if auth else SITE)+path,data=payload,headers=head,method="POST" if payload is not None else "GET")
    try:
        with urllib.request.urlopen(req,timeout=210) as f:return json.load(f)
    except urllib.error.HTTPError as ex:
        detail=ex.read(700).decode("utf-8","replace")
        raise RuntimeError("Bridge or public API HTTP "+str(ex.code)+": "+detail) from ex

def confirm_no_duplicate():
    rows=jget("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":SLUG,"_fields":"id,slug,status,link,featured_media,content"}))
    if len(rows)>1:raise RuntimeError("Duplicate exact slug detected")
    if rows:
        item=rows[0]
        if item.get("status")=="publish" and item.get("featured_media") and "1,470,000" in (item.get("content") or {}).get("rendered",""):
            print("ALREADY_PUBLISHED",item["id"],item["link"],flush=True)
            return item
        raise RuntimeError("Existing draft/incomplete matching slug: manual review")
    for term in ("بوريال","Boreal"):
        results=jget("/search-posts?"+urllib.parse.urlencode({"search":term,"limit":100}),auth=True)
        for row in results.get("items",[]):
            name=(row.get("title","")+" "+row.get("slug","")).lower()
            if "boreal" in name or "بوريال" in name:
                raise RuntimeError("Pre-existing intent page detected: "+str(row))
    return None

def read_press_photo(urls):
    for url in urls:
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; A3talEditorial/1.0; +https://a3tal.com/)","Accept":"image/avif,image/webp,image/jpeg,image/*"})
            with urllib.request.urlopen(req,timeout=45) as f:
                raw=f.read(9_000_001)
            if len(raw)>9_000_000 or len(raw)<15_000:continue
            with Image.open(io.BytesIO(raw)) as im:
                im.load()
                if im.width<700 or im.height<390:continue
                return im.convert("RGB"),url
        except Exception as ex:
            print("PRESS_IMAGE_SOURCE_FAILED",url.rsplit("/",1)[-1],type(ex).__name__,flush=True)
    raise RuntimeError("Cannot retrieve valid official Renault Boreal press photo; publication stopped")

def process_photo(urls,role,alt,name,caption,target):
    im,source=read_press_photo(urls)
    # A3tal editorial crop & tonal grade; preserve the real model geometry and press photo provenance.
    im=ImageOps.exif_transpose(im)
    out=ImageOps.fit(im,target,method=Image.Resampling.LANCZOS,centering=(.5,.48))
    out=ImageEnhance.Contrast(out).enhance(1.045)
    out=ImageEnhance.Color(out).enhance(1.035)
    out=ImageEnhance.Sharpness(out).enhance(1.06)
    b=io.BytesIO();out.save(b,"WEBP",quality=86,method=6,exif=b"")
    raw=b.getvalue()
    if not 30_000<len(raw)<1_600_000:raise RuntimeError("Image WebP size out of range")
    print("RENAULT_PRESS_PHOTO_PREPARED",name,len(raw),source,flush=True)
    return {
        "key":role,"role":"featured" if role=="cover" else "inline",
        "filename":name,"image_base64":base64.b64encode(raw).decode("ascii"),"convert_webp":False,
        "alt":alt,"caption":caption+" | الصورة: Renault Media Room، معالجة تحريرية خاصة بأعطال.كوم",
        "placeholder":"{{a3tal_image:detail}}"
    }

def main():
    if not KEY:raise RuntimeError("GitHub Actions protected A3TAL_API_KEY missing")
    article=PATH.read_text("utf-8").strip()
    if len(article)<11500 or article.count("<h2>")<10 or article.count("<table")<2:
        raise RuntimeError("Article depth/structure validation failed")
    for needle in ("1,470,000","1,570,000","1,690,000","Wet DCT","28 أكتوبر 2026","{{a3tal_image:detail}}","150 حصان"):
        if needle not in article:raise RuntimeError("Missing verified fact or image marker: "+needle)
    current=confirm_no_duplicate()
    if current:return
    images=[
        process_photo(COVER_SOURCES,"cover","رينو بوريال 2027 الجديدة في مصر بلون أزرق مخضر من الأمام في صورة رسمية","a3tal-renault-boreal-2027-egypt-hero-20261102.webp","رينو بوريال 2027 - صورة صحفية للطراز",(1600,900)),
        process_photo(DETAIL_SOURCES,"detail","رينو بوريال SUV الجديدة في عرض رينو الصحفي من الواجهة الأمامية بتصميم المصابيح LED","a3tal-renault-boreal-2027-egypt-detail-20261102.webp","عرض السيارة رينو بوريال وتفاصيل التصميم الأمامي",(1400,840))
    ]
    post={"title":TITLE,"slug":SLUG,"type":"post","status":"publish","content":article,"categories":[374],
        "excerpt":"سعر رينو بوريال 2027 في مصر بعد الإطلاق الرسمي: 1.47 و1.57 و1.69 مليون جنيه. مقارنة Evolution وTechno وIconic، موتور 150 حصان وفتيس Wet DCT وهل تستحق؟",
        "meta":{
          "_yoast_wpseo_title":"سعر رينو بوريال 2027 في مصر والفئات والمواصفات | أعطال.كوم",
          "_yoast_wpseo_metadesc":"أسعار رينو بوريال 2027 في مصر تبدأ من 1.47 مليون جنيه. قارن Evolution وTechno وIconic، المحرك والفتيس والشاشات والأمان وتعرف على الفئة الأنسب.",
          "_yoast_wpseo_focuskw":"سعر رينو بوريال 2027 في مصر",
          "_yoast_wpseo_canonical":URL,
          "_yoast_wpseo_opengraph-title":TITLE,
          "_yoast_wpseo_opengraph-description":"سعر رينو بوريال 2027 يبدأ من 1.47 مليون جنيه. المواصفات والفرق بين فئات Evolution وTechno وIconic وأهم معلومات الشراء."
       }}
    try:
        result=jget("/publish-bundle",auth=True,data={"post":post,"media":images})
    except (TimeoutError,urllib.error.URLError) as ex:
        print("AMBIGUOUS_PUBLISH_WRITE_VERIFY_ONLY",type(ex).__name__,flush=True)
        found=jget("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":SLUG,"_fields":"id,status,link,featured_media"}))
        if len(found)!=1 or found[0].get("status")!="publish" or not found[0].get("featured_media"):raise
        result={"post":found[0],"media":{}}
    p=result.get("post") or {}
    if p.get("status")!="publish" or p.get("slug")!=SLUG or not p.get("featured_media"):
        raise RuntimeError("Bridge did not confirm publish and featured image")
    pid=p["id"]
    live=jget("/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode({"_fields":"id,slug,status,link,featured_media,categories,content,yoast_head_json"}))
    if live.get("link")!=URL or live.get("featured_media")!=p.get("featured_media") or 374 not in live.get("categories",[]):
        raise RuntimeError("Canonical, categories or featured media mismatch")
    rendered=(live.get("content") or {}).get("rendered","")
    if "a3tal-renault-boreal-2027-egypt-detail" not in rendered or "{{a3tal_image" in rendered:
        raise RuntimeError("Inline custom WebP image missing")
    yoast=live.get("yoast_head_json") or {}
    if yoast.get("canonical")!=URL or (yoast.get("robots") or {}).get("index")=="noindex":
        raise RuntimeError("Canonical / robots indexability mismatch")
    cover=(yoast.get("og_image") or [{}])[0].get("url","")
    if "a3tal-renault-boreal-2027-egypt-hero" not in cover:
        raise RuntimeError("Featured / OpenGraph image mismatch: "+cover)
    print("PUBLISHED_VERIFIED",pid,URL,"COVER",live["featured_media"],"OG",cover,flush=True)
if __name__=="__main__":main()
