#!/usr/bin/env python3
"""Publish 3 original Egypt automotive symptom guides using A3tal Direct Bridge.
Category 11 suspension, 13 electrical, 8 mechanical.
Use different original editorial featured WebP compositions made by this publisher
from licensed CC BY 2.0 or CC0 real photographs, with visible photo attribution.
No WordPress generic AI-vector artwork or external publishing bridge.
Never overwrite existing posts or invent diagnosis/parts prices. Public SEO QA.
"""
import base64, hashlib, html as htmlmod, io, json, os, re, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from PIL import Image,ImageOps,ImageFilter,ImageEnhance,ImageDraw,ImageFont
BASE="https://a3tal.com"
API=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
FOLDER=Path("data/editorial/20261110-faults")
SLUGS=[
"steering-wheel-off-center-after-wheel-alignment-causes-fix",
"power-window-rolls-back-down-when-closing-anti-pinch-reset",
"engine-oil-level-rising-fuel-dilution-coolant-diagnosis"]
OUT=Path("reports/three-technical-fault-articles-20261110.json")
OUT.parent.mkdir(parents=True,exist_ok=True)
RESULTS=[]

def request(path,auth=False,payload=None,timeout=320):
    url=(API if auth else BASE)+path
    h={"Accept":"application/json","Cache-Control":"no-store","User-Agent":"A3tal-3-OriginalFaults-20261110"}
    if auth:
        if not KEY:raise RuntimeError("Missing A3tal Direct Bridge secret")
        h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf-8")
    if raw:h["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,raw,headers=h,method="POST" if raw else "GET")
    try:
        with urllib.request.urlopen(req,timeout=timeout) as resp:return json.load(resp)
    except urllib.error.HTTPError as e:
        raise RuntimeError("REST HTTP "+str(e.code)+" "+url+" "+e.read(400).decode("utf8","replace")) from e

def exact(slug):
    arr=request("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({
        "slug":slug,"_fields":"id,status,slug,title,link,featured_media,categories,content,yoast_head_json","per_page":6}))
    if len(arr)>1:raise RuntimeError("Duplicate slug exists "+slug)
    return arr[0] if arr else None

def photo_download(p):
    name=p["file"]
    if not re.fullmatch(r"File:[A-Za-z0-9_. -]+\.jpe?g",name,re.I):
        raise RuntimeError("Untrusted photo file name")
    if not p["url"].startswith("https://commons.wikimedia.org/wiki/File:"):
        raise RuntimeError("Unapproved CC image attribution URI")
    file_name=name.split(":",1)[1].replace(" ","_")
    url="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(file_name)
    r=urllib.request.Request(url,headers={"User-Agent":"A3talResearch/1.0 (photographic editorial car-diagnostics illustrations; contact https://a3tal.com/)","Accept":"image/jpeg,image/*"})
    with urllib.request.urlopen(r,timeout=75) as f:
        src=f.read(20_000_000)
    if len(src)<40000:raise RuntimeError("Photo bytes too small "+name)
    with Image.open(io.BytesIO(src)) as im:
        im.load()
        if im.width<1500 or im.height<1200:raise RuntimeError("Photo too small "+repr(im.size))
        real=ImageOps.exif_transpose(im).convert("RGB")
    print("CC_LICENSED_REAL_PHOTO_VERIFIED",name,real.size,hashlib.sha256(src).hexdigest()[:16],p["license"],flush=True)
    return real

def editorial_webp(im,index,kind):
    """Original photographic collage, no misleading car model or large overprint.
    Every original photo is kept readable; bg is defocused same photograph.
    """
    W,H=(1600,900) if kind=="featured" else (1350,900)
    bg=ImageOps.fit(im,(W,H),method=Image.Resampling.LANCZOS,centering=(.5,.43))
    bg=ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(30))).enhance(.58)
    if kind=="featured":
        # Use lens-style panel occupying >=80% of frame; keep details sharp.
        margin=22; target=(W-2*margin,H-2*margin)
        fg=ImageOps.fit(im,target,method=Image.Resampling.LANCZOS,centering=(.5,.48))
        bg.paste(fg,(margin,margin))
        # Editorial accent: thin colored vertical rail, no text overlay on car.
        draw=ImageDraw.Draw(bg,"RGBA")
        draw.rectangle((margin,margin,margin+8,H-margin),fill=(182,32,49,245))
        draw.rectangle((margin,H-margin-8,W-margin,H-margin),fill=(14,36,60,160))
        # Small unobtrusive text site signature, original styling.
        draw.rounded_rectangle((W-181,H-67,W-33,H-31),radius=8,fill=(9,22,41,160))
        try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",17)
        except OSError:font=ImageFont.load_default()
        draw.text((W-164,H-57),"A3TAL.COM",font=font,fill=(255,255,255,250))
    else:
        fore=ImageOps.contain(im,(min(W-30,im.width),min(H-30,im.height)),method=Image.Resampling.LANCZOS)
        bg.paste(fore,((W-fore.width)//2,(H-fore.height)//2))
    dst=io.BytesIO()
    bg.save(dst,format="WEBP",quality=87,method=6)
    val=dst.getvalue()
    if len(val)<20000 or val[:4]!=b"RIFF" or val[8:12]!=b"WEBP":
        raise RuntimeError("Real WebP editorial creation failed")
    return val

def make_media(p,photo,index,kind):
    name="a3tal-20261110-"+["alignment","window","engine-oil"][index]+"-"+kind+"-original-editorial.webp"
    label=p["hero"]+" | تصوير توضيحي مع معالجة تحريرية من أعطال.كوم"
    caption="صورة فوتوغرافية مرخّصة للموضوع، تصميم تحريري: أعطال.كوم. المصور: "+p["photo"]["author"]+"، الرخصة "+p["photo"]["license"]+"، المصدر: "+p["photo"]["url"]
    return {"key":kind,"role":kind,"filename":name,
     "image_base64":base64.b64encode(editorial_webp(photo,index,kind)).decode("ascii"),
     "convert_webp":False,"alt":label,"caption":caption,
     "placeholder":"{{a3tal_image:inline}}"}

def verify(p,pid,feature,index):
    r=request("/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode(
        {"_fields":"id,title,slug,status,link,featured_media,categories,content,yoast_head_json"}))
    want=BASE+"/"+p["slug"]+"/"
    content=(r.get("content") or {}).get("rendered","")
    seo=r.get("yoast_head_json") or {}
    og=(seo.get("og_image") or [{}])[0].get("url","")
    robots=seo.get("robots") or {}
    fname="a3tal-20261110-"+["alignment","window","engine-oil"][index]+"-featured-original-editorial.webp"
    inline="a3tal-20261110-"+["alignment","window","engine-oil"][index]+"-inline-original-editorial.webp"
    checks={
        "url":r.get("link")==want,"status":r.get("status")=="publish","slug":r.get("slug")==p["slug"],
        "category":p["category"] in r.get("categories",[]),
        "featured":r.get("featured_media")==feature and bool(feature),
        "og":fname in og,"canonical":seo.get("canonical")==want,
        "indexable":robots.get("index")!="noindex","inline":inline in content,
        "content":len(re.findall(r"<h2(?: |>)",content))>=7 and len(content)>4500,
        "no_placeholder":"{{a3tal_image:" not in content
    }
    if not all(checks.values()):raise RuntimeError("LIVE_PUBLIC_POST_QA_FAILED "+repr(checks)+" "+want)
    return {"post_id":pid,"category":p["category"],"url":want,"featured_media":feature,
            "og_image":og,"canonical":seo["canonical"],"cover_size":"1600x900 WebP",
            "inline_image":inline,"checks":checks}

def process(slug,index):
    p=json.loads((FOLDER/(slug+".json")).read_text("utf8"))
    if p["slug"]!=slug or p["category"] not in [11,13,8]:raise RuntimeError("Post identity mismatch")
    content=p["html"]
    if content.count("<h2>")<7 or len(content)<5000 or len(re.findall(r"[\u0600-\u06FF]+",re.sub(r"<[^>]+>"," ",content)))<650:
        raise RuntimeError("Editorial thin/invalid content "+slug)
    if p["source"] not in content or "https://a3tal.com/fault-diagnosis/" not in content:raise RuntimeError("Required source missing")
    existing=exact(slug)
    if existing:
        # Idempotent restart. Only accept a matching published post with photo and canonical.
        if existing.get("status")!="publish" or not existing.get("featured_media"):
            raise RuntimeError("Slug exists but not a validated published article")
        q=verify(p,existing["id"],existing["featured_media"],index)
        print("ALREADY_PUBLISHED_VERIFIED",q["url"],flush=True)
        return q
    category=request("/wp-json/wp/v2/categories/"+str(p["category"])+"?_fields=id,name")
    if category.get("id")!=p["category"]:raise RuntimeError("Wrong category")
    source_img=photo_download(p["photo"])
    media=[make_media(p,source_img,index,"featured"),make_media(p,source_img,index,"inline")]
    credit=p["featured_caption"]
    # Attribution visibly in article body for CC BY and CC0 photos.
    content=content.replace("</h2>","</h2>",1)+(
        '<p><small>حقوق الصورة: <a href="'+p["photo"]["url"]+'" rel="nofollow noopener noreferrer">'+p["photo"]["author"]+
        '</a>، '+p["photo"]["license"]+
        '، تصميم ومعالجة الغلاف: أعطال.كوم.</small></p>')
    content=content.replace("</p>\n<h2>",'</p>\n<figure>{{a3tal_image:inline}}</figure>\n<h2>',1)
    url=BASE+"/"+slug+"/"
    seo={
     "_yoast_wpseo_title":p["title"]+" | أعطال.كوم",
     "_yoast_wpseo_metadesc":p["meta"],
     "_yoast_wpseo_focuskw":p["focus"],
     "_yoast_wpseo_canonical":url,
     "_yoast_wpseo_opengraph-title":p["title"],
     "_yoast_wpseo_opengraph-description":p["meta"],
     "_yoast_wpseo_twitter-title":p["title"],
     "_yoast_wpseo_twitter-description":p["meta"]
    }
    post={"type":"post","status":"publish","slug":slug,"title":p["title"],"content":content,
        "categories":[p["category"]],"excerpt":p["excerpt"],"meta":seo}
    response=request("/publish-bundle",auth=True,payload={"post":post,"media":media})
    r=response.get("post") or {}
    if not r.get("id") or r.get("slug")!=slug or r.get("status")!="publish" or not r.get("featured_media"):
        raise RuntimeError("Bridge returned incomplete post "+repr(r)[:330])
    proof=verify(p,r["id"],r["featured_media"],index)
    print("NEW_FAULT_ARTICLE_PUBLISHED_LIVE_QA_SUCCESS",proof["url"],flush=True)
    return proof

def main():
    if not KEY:raise RuntimeError("A3tal Direct Bridge key missing")
    for i,slug in enumerate(SLUGS):
        try:
            RESULTS.append(process(slug,i))
            OUT.write_text(json.dumps({"verified":RESULTS,"completed":len(RESULTS)},ensure_ascii=False,indent=2),"utf8")
        except Exception:
            OUT.write_text(json.dumps({"verified":RESULTS,"failure_slug":slug},ensure_ascii=False,indent=2),"utf8")
            raise
    print("A3TAL_THREE_FAULT_ARTICLES_FULLY_PUBLISHED",len(RESULTS),flush=True)

if __name__=="__main__":main()
