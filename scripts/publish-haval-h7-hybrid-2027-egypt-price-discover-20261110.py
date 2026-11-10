#!/usr/bin/env python3
"""Publish a one-off verifiable Haval H7 HEV 2027 Egypt buying guide.
Use exclusively GitHub Actions -> A3tal Direct Bridge; exact 2027 price
from live dealer and November price list. Original editorial compositions
of REAL manufacturer H7 Black Edition photos. No invented SUV illustration.
Fail closed on duplicate search intent, image, category, OG or canonical QA.
"""
import base64, io, json, os, re, urllib.parse, urllib.request, urllib.error, time
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
SLUG="haval-h7-hybrid-2027-egypt-price-ultra-black"
URL=SITE+"/"+SLUG+"/"
TITLE="سعر هافال H7 هايبرد 2027 في مصر بعد زيادة نوفمبر.. هل تستحق 1.795 مليون؟"
FILE=Path("data/editorial/haval-h7-hybrid-2027-egypt-prices-20261110.html")
CATEGORY=374
PHOTO_COVER=[
 "https://greatwall.eg/media/car-performance-images/performance_black_edition_H7.jpg"
]
PHOTO_DETAIL=[
 "https://greatwall.eg/media/extDesignImages/h7_black_edition_exterior_.jpg",
 "https://greatwall.eg/media/extDesignImages/h7_black_edition_exterior_1.jpg"
]
REPORT=Path("reports/haval-h7-price-2027-20261110-publish-qa.json")
REPORT.parent.mkdir(parents=True,exist_ok=True)

def req(path,auth=False,data=None,timeout=250):
    headers={"Accept":"application/json","User-Agent":"A3tal-Haval-H7-2027-Discover/20261110","Cache-Control":"no-store"}
    if auth:
        if not KEY:raise RuntimeError("Missing A3TAL_API_KEY: cannot use A3tal Direct Bridge")
        headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf-8")
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    target=(API if auth else SITE)+path
    request=urllib.request.Request(target,data=raw,headers=headers,method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(request,timeout=timeout) as f:return json.load(f)
    except urllib.error.HTTPError as e:
        msg=e.read(700).decode("utf-8","replace")
        raise RuntimeError("HTTP "+str(e.code)+" "+target+" "+msg) from e

def duplicate_guard():
    hits=req("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({
        "slug":SLUG,"_fields":"id,title,slug,status,link,featured_media,content,yoast_head_json","per_page":5
    }))
    if len(hits)>1:raise RuntimeError("Multiple posts with exact Haval H7 slug")
    if hits:
        p=hits[0];html=(p.get("content") or {}).get("rendered","")
        seo=p.get("yoast_head_json") or {}
        og=(seo.get("og_image") or [{}])[0].get("url","")
        if p.get("status")=="publish" and p.get("link")==URL and p.get("featured_media") and "1,795,000" in html and "haval-h7-2027" in og and seo.get("canonical")==URL:
            print("ALREADY_PUBLISHED_WITH_FEATURED_AND_PRICE",p["id"],URL,flush=True)
            return p
        raise RuntimeError("Existing Haval H7 slug needs reconciliation; refusing overwrite")
    for term in ("هافال H7","Haval H7","هافال اتش 7"):
        hits=req("/search-posts?"+urllib.parse.urlencode({"search":term,"limit":100}),auth=True)
        for post in hits.get("items",[]):
            name=(str(post.get("title",""))+" "+str(post.get("slug",""))).lower()
            matched=("هافال" in name or "haval" in name) and (
              bool(re.search(r"(?<![a-z0-9])h7(?![a-z0-9])",name)) or "اتش 7" in name)
            if matched:raise RuntimeError("Existing same-intent Haval H7 price post found: "+name[:120])
    return None

def photo(urls,min_w,min_h):
    for u in urls:
        if not u.startswith("https://greatwall.eg/media/"):raise RuntimeError("Unapproved source host")
        try:
            q=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 (A3tal / exact-model official visual QA)","Accept":"image/jpeg,image/png,image/*"})
            with urllib.request.urlopen(q,timeout=70) as f:b=f.read(12_000_000)
            if len(b)<45000:raise RuntimeError("JPEG too small in bytes")
            with Image.open(io.BytesIO(b)) as src:
                src.load()
                if src.width<min_w or src.height<min_h:raise RuntimeError("Photo resolution below minimum "+str(src.size))
                out=ImageOps.exif_transpose(src).convert("RGB")
                print("VERIFIED_REAL_HAVAL_H7_BLACK_EDITION",u,src.size,flush=True)
                return out,u
        except Exception as e:print("PHOTO_CANDIDATE_REJECTED",u.rsplit("/",1)[-1],type(e).__name__,str(e)[:130],flush=True)
    raise RuntimeError("No adequate exact-model Haval H7 photo; publication stopped")

def frame(im,role):
    if role=="cover":
        W,H=1600,900
        if im.width<W or im.height<H:raise RuntimeError("Featured photo cannot be upscaled")
        pic=ImageOps.fit(im,(W,H),method=Image.Resampling.LANCZOS,centering=(.51,.50))
        pic=ImageEnhance.Contrast(pic).enhance(1.05)
        pic=ImageEnhance.Color(pic).enhance(1.035)
    else:
        W,H=1400,900
        back=ImageOps.fit(im,(W,H),method=Image.Resampling.LANCZOS)
        back=ImageEnhance.Brightness(back.filter(ImageFilter.GaussianBlur(28))).enhance(.69)
        inset=ImageOps.contain(im,(min(W-24,im.width),min(H-24,im.height)),method=Image.Resampling.LANCZOS)
        back.paste(inset,((W-inset.width)//2,(H-inset.height)//2))
        pic=back
    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    d.rounded_rectangle((W-206,H-57,W-21,H-17),radius=11,fill=(12,27,41,145))
    try:f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",19)
    except OSError:f=ImageFont.load_default()
    d.text((W-180,H-46),"A3TAL.COM",font=f,fill=(255,255,255,245))
    pic=Image.alpha_composite(pic.convert("RGBA"),overlay).convert("RGB")
    buff=io.BytesIO();pic.save(buff,"WEBP",quality=90,method=6)
    raw=buff.getvalue()
    if not 45_000<len(raw)<2_400_000 or raw[:4]!=b"RIFF" or raw[8:12]!=b"WEBP":
        raise RuntimeError("Real official-photo WebP output failed QA")
    return raw

def make_media(role,pic,source):
    binary=frame(pic,role)
    fname="a3tal-haval-h7-2027-"+role+"-official-photo-original-editorial.webp"
    alt=("هافال H7 هايبرد 2027 Ultra Black Edition من الصور الرسمية للوكيل، "
         +("صورة بارزة" if role=="cover" else "تفاصيل التصميم الخارجي"))
    return {"key":role,"role":"featured" if role=="cover" else "inline",
       "filename":fname,"image_base64":base64.b64encode(binary).decode("ascii"),
       "convert_webp":False,"alt":alt,
       "caption":"صورة حقيقية من موقع هافال مصر الرسمي، بتكوين ومعالجة تحريرية خاصة لأعطال.كوم. المصدر: "+source,
       "placeholder":"{{a3tal_image:detail}}"}

def live_qa(pid,media_id):
    result=req("/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode(
        {"_fields":"id,title,slug,link,status,featured_media,categories,content,yoast_head_json"}))
    seo=result.get("yoast_head_json") or {}
    content=(result.get("content") or {}).get("rendered","")
    og=(seo.get("og_image") or [{}])[0].get("url","")
    robots=seo.get("robots") or {}
    if result.get("status")!="publish" or result.get("slug")!=SLUG or result.get("link")!=URL:
        raise RuntimeError("Public URL or publication status incorrect")
    if result.get("featured_media")!=media_id or CATEGORY not in result.get("categories",[]):
        raise RuntimeError("Featured image or category 374 was not assigned")
    if seo.get("canonical")!=URL or robots.get("index")=="noindex":
        raise RuntimeError("Yoast canonical or indexability wrong")
    if "haval-h7-2027-cover-official-photo-original-editorial.webp" not in og:
        raise RuntimeError("Missing real H7 model featured OG image "+og)
    if "haval-h7-2027-detail-official-photo-original-editorial.webp" not in content:
        raise RuntimeError("Inline official H7 photo not visible")
    if "{{a3tal_image:" in content or "1,795,000" not in content or "530" not in content:
        raise RuntimeError("Unreplaced photo placeholder or missing current specs")
    if len(re.findall(r"<h2[ >]",content))<8:raise RuntimeError("Article subheadings missing")
    record={"post_id":pid,"url":URL,"featured_media":media_id,"og_image":og,"canonical":seo.get("canonical"),"status":"publish","category":CATEGORY,"prices_current":True,"real_exact_model_photo":True}
    REPORT.write_text(json.dumps(record,ensure_ascii=False,indent=2),"utf-8")
    print("HAVAL_H7_2027_PUBLISHED_WITH_REAL_MODEL_COVER_AND_OG",json.dumps(record,ensure_ascii=False),flush=True)

def main():
    if not KEY:raise RuntimeError("A3tal bridge credential unavailable")
    html=FILE.read_text("utf8")
    if len(html)<7200 or html.count("<h2>")<8 or html.count("<table>")<2 or "1,795,000" not in html or "{{a3tal_image:detail}}" not in html:
        raise RuntimeError("Price, authoring or inline-media quality gate failed")
    if duplicate_guard():return
    cat=req("/wp-json/wp/v2/categories/374")
    if "السيارات" not in cat.get("name",""):raise RuntimeError("Unexpected WP price category")
    # Check current official manufacturer pricing even if the sourced 2026 spec PDF is stale.
    official=urllib.request.urlopen(urllib.request.Request("https://greatwall.eg/en/model/h7-hev/",headers={"User-Agent":"Mozilla/5.0"}),timeout=50).read(2_000_000).decode("utf-8","ignore")
    if "1,795,000" not in official and "1795000" not in official:raise RuntimeError("Haval Egypt live page no longer confirms 1,795,000 EGP")
    cover,coverurl=photo(PHOTO_COVER,1600,900)
    detail,detailurl=photo(PHOTO_DETAIL,1000,650)
    if coverurl==detailurl:raise RuntimeError("Duplicate cover/detail image")
    media=[make_media("cover",cover,coverurl),make_media("detail",detail,detailurl)]
    meta={
     "_yoast_wpseo_title":"سعر هافال H7 هايبرد 2027 في مصر بعد زيادة نوفمبر | أعطال.كوم",
     "_yoast_wpseo_metadesc":"سعر هافال H7 موديل 2027 في مصر 1,795,000 جنيه بعد زيادة 30 ألفًا. مواصفات Ultra Black Edition الهجينة 240 حصانًا وتجهيزاتها وهل تستحق الشراء؟",
     "_yoast_wpseo_focuskw":"سعر هافال H7 2027 في مصر",
     "_yoast_wpseo_canonical":URL,
     "_yoast_wpseo_opengraph-title":TITLE,
     "_yoast_wpseo_opengraph-description":"هافال H7 هايبرد 2027 أصبحت بـ1.795 مليون جنيه بعد زيادة نوفمبر. تفاصيل السعر وتجهيزات Ultra Black Edition وأهم ما يجب التأكد منه قبل الشراء.",
     "_yoast_wpseo_twitter-title":TITLE,
     "_yoast_wpseo_twitter-description":"هافال H7 2027 HEV: 1.795 مليون جنيه، منظومة 240 حصانًا، سعر نوفمبر والمواصفات وأهم فرق عن V7."
    }
    post={"type":"post","status":"publish","slug":SLUG,"title":TITLE,"content":html,
       "categories":[CATEGORY],
       "excerpt":"سعر هافال H7 هايبرد موديل 2027 وصل إلى 1,795,000 جنيه بعد زيادة 30 ألفًا في نوفمبر. مواصفات Ultra Black Edition وهل تستحق الشراء؟",
       "meta":meta}
    try:response=req("/publish-bundle",auth=True,data={"post":post,"media":media},timeout=320)
    except (TimeoutError,urllib.error.URLError):
        print("AMBIGUOUS_BRIDGE_POST_VERIFY_ONLY",flush=True)
        rows=req("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":SLUG,"_fields":"id,status,link,featured_media"}))
        if len(rows)!=1 or rows[0].get("status")!="publish" or not rows[0].get("featured_media"):raise
        response={"post":rows[0]}
    p=response.get("post") or {}
    if not p.get("id") or p.get("status")!="publish" or p.get("slug")!=SLUG or not p.get("featured_media"):
        raise RuntimeError("A3tal bridge did not confirm exact published article with featured photo: "+repr(response)[:400])
    live_qa(p["id"],p["featured_media"])

if __name__=="__main__":
    main()
