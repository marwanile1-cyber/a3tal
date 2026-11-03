#!/usr/bin/env python3
"""Publish a new Jetour T2 i-DM 4x4 2027 Egypt-specific page through A3tal Direct Bridge.
No generic T2 page is replaced. Guard SEO duplication and verify 2 unique WebP graphics
built exclusively for this page from images hosted by the manufacturer.
"""
import base64,io,json,os,urllib.request,urllib.parse,urllib.error,re
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance,ImageFilter,ImageDraw,ImageFont

ROOT="https://a3tal.com"
API=ROOT+"/wp-json/a3tal-direct/v1"
SECRET=os.environ.get("A3TAL_API_KEY","")
SLUG="jetour-t2-idm-4x4-2027-egypt-price-specs"
URL=ROOT+"/"+SLUG+"/"
TITLE="سعر جيتور T2 i-DM 4x4 موديل 2027 في مصر.. 600 حصان وفرق 150 ألف جنيه"
PATH=Path("data/editorial/jetour-t2-idm-4x4-2027-egypt-price-launch-20261103.html")
CAT=374

OFFICIAL=[
 "https://jetourglobal.com/new-static/images/vehicles/cars/T2iDM/p1_1.png",
 "https://jetourglobal.com/new-static/images/vehicles/cars/T2iDM/p1_2.png",
 "https://jetourglobal.com/new-static/images/vehicles/cars/T2iDM/p1_3.png",
 "https://jetourglobal.com/new-static/images/vehicles/cars/T2iDM/p2_1.png",
 "https://jetourglobal.com/new-static/images/vehicles/cars/T2iDM/p2_2.png",
 "https://jetourglobal.com/new-static/images/vehicles/cars/T2iDM/p2_3.png",
 "https://jetourglobal.com/new-static/images/vehicles/cars/T2iDM/p4_1.png",
 "https://jetourglobal.com/new-static/images/vehicles/cars/T2iDM/p4_2.png",
 "https://jetouregypt.com/models/T2-i-DM-4x4/new_assets/img/october_digital_ad_t2_idm_1920x1080_english.png"
]

def jreq(path,protected=False,data=None):
    headers={"Accept":"application/json","User-Agent":"A3tal-Jetour-Launch-Editorial-20261103","Cache-Control":"no-cache,no-store"}
    if protected:
        if not SECRET:raise RuntimeError("Missing bridge credential")
        headers["X-A3tal-Key"]=SECRET
        headers["Authorization"]="Bearer "+SECRET
    raw=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf8")
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    request=urllib.request.Request((API if protected else ROOT)+path,headers=headers,data=raw,method="POST" if data is not None else "GET")
    with urllib.request.urlopen(request,timeout=300) as f:return json.load(f)

def safe_intent():
    exact=jreq("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":SLUG,"_fields":"id,slug,status,link,featured_media,content"}))
    if len(exact)>1:raise RuntimeError("Multiple posts with identical canonical slug")
    if exact:
        old=exact[0]
        if old.get("status")=="publish" and old.get("featured_media") and "43.24" in (old.get("content") or {}).get("rendered",""):
            print("ALREADY_PUBLISHED",old["id"],old["link"],flush=True);return old
        raise RuntimeError("Existing incomplete page requires reconciliation, not duplication")
    items=jreq("/search-posts?"+urllib.parse.urlencode({"search":"T2 i-DM 4x4","limit":100}),protected=True)
    for x in items.get("items",[]):
        title=(x.get("title","")+" "+x.get("slug","")).lower()
        if "4x4" in title and ("t2" in title or "جيتور" in title):
            raise RuntimeError("An existing exact 4x4 intent page exists: "+str(x))
    return None

def get_brand_media(candidates):
    for url in candidates:
        try:
            headers={"User-Agent":"Mozilla/5.0 (compatible; A3tal-Editorial/1.0; +https://a3tal.com/)","Accept":"image/png,image/jpeg,image/webp,image/*"}
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=50) as f:
                raw=f.read(14_000_000)
            if len(raw)<25_000 or len(raw)>14_000_000:continue
            with Image.open(io.BytesIO(raw)) as src:
                src.load()
                if src.width<900 or src.height<490:continue
                im=ImageOps.exif_transpose(src).convert("RGB")
                print("MANUFACTURER_MEDIA_SOURCE",url,im.size,flush=True)
                return im,url
        except Exception as exc:print("MEDIA_SOURCE_FAILED",url.rsplit("/",1)[-1],type(exc).__name__,flush=True)
    raise RuntimeError("Manufacturer photography could not be loaded for this post")

def make_unique_art(role,im,size,alt,source):
    w,h=size
    # This page's one-off edited editorial photo: crop, subtle grading, clean Discover
    # composition and discrete site identifier. No fabricated exterior/interior hardware.
    result=ImageOps.fit(im,size,Image.Resampling.LANCZOS,centering=(.50,.47))
    result=ImageEnhance.Contrast(result).enhance(1.075)
    result=ImageEnhance.Color(result).enhance(1.04)
    result=ImageEnhance.Sharpness(result).enhance(1.065)
    # Dark-toned translucent bottom accent without headlines, claims or prices.
    overlay=Image.new("RGBA",size,(0,0,0,0))
    draw=ImageDraw.Draw(overlay)
    draw.rounded_rectangle((w-188,h-53,w-25,h-17),radius=9,fill=(15,28,42,132))
    try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",17)
    except Exception:font=ImageFont.load_default()
    draw.text((w-169,h-45),"A3tal.com",font=font,fill=(248,248,248,240))
    result=Image.alpha_composite(result.convert("RGBA"),overlay).convert("RGB")
    b=io.BytesIO();result.save(b,"WEBP",quality=87,method=6)
    image=b.getvalue()
    if not 35_000<len(image)<2_500_000:raise RuntimeError("Invalid output WebP")
    return {
       "key":role,"role":"featured" if role=="cover" else "inline",
       "filename":"a3tal-jetour-t2-idm-4x4-2027-egypt-exclusive-"+role+".webp",
       "image_base64":base64.b64encode(image).decode("ascii"),"convert_webp":False,
       "alt":alt,"caption":"معالجة وتكوين تحريري حصري لأعطال.كوم من مادة صور جيتور الرسمية للطراز. مصدر الصورة: "+source+". قد تختلف بعض التفاصيل المرئية بين الأسواق.",
       "placeholder":"{{a3tal_image:detail}}"
    }

def main():
    if not SECRET:raise RuntimeError("Protected GitHub action secret is missing")
    html=PATH.read_text(encoding="utf-8").strip()
    if len(html)<11000 or html.count("<h2>")<9 or html.count("<table")<2:
        raise RuntimeError("Incomplete editorial document")
    for must in ("2,300,000","2,150,000","150 ألف","43.24","600 حصان","915","910","1300","{{a3tal_image:detail}}"):
        if must not in html:raise RuntimeError("Critical facts/nuance missing: "+must)
    if safe_intent():return
    cat=jreq("/wp-json/wp/v2/categories/"+str(CAT))
    if "اسعار السيارات" not in cat["name"] and "أسعار السيارات" not in cat["name"]:
        raise RuntimeError("Price-and-model category changed")
    # Use original vehicle media supplied by manufacturer, with exclusive crops/grades,
    # not unrelated stock photos or screenshots from competitors.
    cover,coverurl=get_brand_media(OFFICIAL[:3]+OFFICIAL[8:])
    try:detail,detailurl=get_brand_media(OFFICIAL[3:8])
    except RuntimeError:
        detail,detailurl=get_brand_media(OFFICIAL[1:3])
    images=[
      make_unique_art("cover",cover,(1600,900),"جيتور T2 i-DM 4x4 موديل 2027 الهجينة من زاوية خارجية في صورة تحريرية حصرية لأعطال.كوم",coverurl),
      make_unique_art("detail",detail,(1400,840),"تفاصيل تصميم جيتور T2 i-DM الجديدة في صورة تحريرية مخصصة لمقارنة النسخة الرباعية",detailurl)
    ]
    data={
      "post":{
        "type":"post","title":TITLE,"slug":SLUG,"status":"publish",
        "content":html,"excerpt":"سعر جيتور T2 i-DM 4x4 موديل 2027 في مصر 2.3 مليون جنيه. مقارنة مع i-DM العادية وفرق 150 ألف، مواصفات بطارية 43.24 كيلووات وقوة 600 حصان والضمان.",
        "categories":[CAT],
        "meta":{
            "_yoast_wpseo_title":"سعر جيتور T2 i-DM 4x4 موديل 2027 في مصر والمواصفات | أعطال.كوم",
            "_yoast_wpseo_metadesc":"جيتور T2 i-DM 4x4 موديل 2027 في مصر بسعر 2.3 مليون جنيه. 600 حصان، بطارية 43.24 كيلووات، الفرق عن i-DM العادية وهل تستحق 150 ألف زيادة؟",
            "_yoast_wpseo_focuskw":"سعر جيتور T2 i-DM 4x4 2027",
            "_yoast_wpseo_canonical":URL,
            "_yoast_wpseo_opengraph-title":TITLE,
            "_yoast_wpseo_opengraph-description":"سعر جيتور T2 i-DM 4x4 الجديدة 2.3 مليون جنيه، مع مقارنة الفئات والمدى والبطارية وشروط الشراء.",
            "_yoast_wpseo_twitter-title":TITLE,
            "_yoast_wpseo_twitter-description":"أحدث جيتور T2 i-DM 4x4 في مصر بسعر رسمي 2.3 مليون جنيه وتفاصيل الدفع الرباعي."
        }
      },
      "media":images
    }
    try:
       response=jreq("/publish-bundle",protected=True,data=data)
    except (TimeoutError,urllib.error.URLError):
       rows=jreq("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":SLUG,"_fields":"id,slug,status,featured_media,link"}))
       if len(rows)!=1 or rows[0].get("status")!="publish" or not rows[0].get("featured_media"):raise
       response={"post":rows[0]}
    post=response.get("post") or {}
    if post.get("status")!="publish" or post.get("slug")!=SLUG or not post.get("featured_media"):
       raise RuntimeError("Bridge has not confirmed published post with cover")
    public=jreq("/wp-json/wp/v2/posts/"+str(post["id"])+"?"+urllib.parse.urlencode({"_fields":"id,slug,status,link,featured_media,content,categories,yoast_head_json"}))
    seo=public.get("yoast_head_json") or {}
    body=(public.get("content") or {}).get("rendered","")
    og=(seo.get("og_image") or [{}])[0].get("url","")
    if (public.get("status")!="publish" or public.get("link")!=URL or public.get("featured_media")!=post.get("featured_media")
        or CAT not in public.get("categories",[]) or "{{a3tal_image" in body or "exclusive-detail" not in body
        or "exclusive-cover" not in og or seo.get("canonical")!=URL
        or (seo.get("robots") or {}).get("index")=="noindex"):
        raise RuntimeError("Live canonical/OG/indexable image validation failed")
    print("PUBLISHED_VERIFIED",post["id"],URL,"FEATURED",post["featured_media"],"OG",og,flush=True)

if __name__=="__main__":main()
