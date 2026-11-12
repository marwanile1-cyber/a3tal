#!/usr/bin/env python3
"""Publish unique 2027 Opel Corsa Topline+ Egypt price guide to CATEGORY 374.
Real exact MY2027 car photo from an authorized Egyptian dealer, not vector art;
GitHub -> A3tal Direct Bridge, inspect public post, featured, OG and homepage.
Stop if duplicate same-intent post detected or source/photo pricing cannot verify.
"""
import base64,hashlib,io,json,os,re,time,urllib.parse,urllib.request,urllib.error
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
SLUG="opel-corsa-2027-egypt-price-topline-after-increase"
URL=SITE+"/"+SLUG+"/"
TITLE="سعر أوبل كورسا 2027 في مصر بعد زيادة 50 ألف جنيه.. هل تستحق 1.3 مليون؟"
HTML=Path("data/editorial/opel-corsa-2027-egypt-price-after-october-increase-20261112.html")
CATEGORY=374
SOURCE_PHOTO="https://ellaithy.com.eg/wp-content/uploads/2026/11/1794376474_361_90456_opelcorsa2027toplineplusexterior.webp"
SOURCE_PAGE="https://ellaithy.com.eg/new-cars/opel-corsa-2027-topline-plus-ar/"
SOURCE_PHOTO_SHA256="3e0749a2b0c3d63b"
REPORT=Path("reports/opel-corsa-2027-egypt-price-discover-20261112.json")
REPORT.parent.mkdir(parents=True,exist_ok=True)

def get(path,authenticated=False,data=None,timeout=320):
    url=(API if authenticated else SITE)+path
    headers={"Accept":"application/json","Cache-Control":"no-store","User-Agent":"A3tal-Corsa27-EditorialPhotoQA/1.0"}
    if authenticated:
        if not KEY:raise RuntimeError("A3tal Direct Bridge secret missing")
        headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf-8")
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,data=raw,headers=headers,method="POST" if raw is not None else "GET")
    try:
        with urllib.request.urlopen(req,timeout=timeout) as f:return json.load(f)
    except urllib.error.HTTPError as exc:
        raise RuntimeError("HTTP "+str(exc.code)+" "+url+": "+exc.read(600).decode("utf8","replace")) from exc

def existing(slug):
    arr=get("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":slug,"per_page":10,
        "_fields":"id,status,slug,link,featured_media,categories,content,yoast_head_json"}))
    if len(arr)>1:raise RuntimeError("Duplicate exact permalink already exists")
    return arr[0] if arr else None

def collision_guard():
    for query in ("أوبل كورسا","Opel Corsa"):
        rows=get("/wp-json/wp/v2/search?"+urllib.parse.urlencode({"search":query,"per_page":80}))
        for item in rows:
            label=(item.get("title") or "").lower()
            if (("كورسا" in label or "corsa" in label) and
                (("سعر" in label or "أسعار" in label or "price" in label)) and
                ("2027" in label) and item.get("url")!=URL):
                raise RuntimeError("Existing 2027 Opel Corsa price intent: "+item.get("url",""))
    print("NO_CANNIBALIZATION_CORSА_2027_PRICE_INTENT",flush=True)

def fetch_photo():
    if not SOURCE_PHOTO.startswith("https://ellaithy.com.eg/wp-content/uploads/2026/11/"):
        raise RuntimeError("Photo source not approved")
    req=urllib.request.Request(SOURCE_PHOTO,headers={"User-Agent":"Mozilla/5.0","Accept":"image/webp,image/*"})
    with urllib.request.urlopen(req,timeout=75) as f:raw=f.read(8_000_000)
    digest=hashlib.sha256(raw).hexdigest()
    if not digest.startswith(SOURCE_PHOTO_SHA256):
        raise RuntimeError("Exact 2027 Corsa distributor photo changed: "+digest)
    with Image.open(io.BytesIO(raw)) as pic:
        pic.load()
        if pic.width<1600 or pic.height<900:raise RuntimeError("Corsa MY2027 real image not Discover sized")
        photo=pic.convert("RGB")
    print("EXACT_REAL_CORSА_2027_SOURCE_PHOTO_VERIFIED",photo.size,len(raw),digest[:16],flush=True)
    return photo

def generate_image(src,role):
    # Unique A3tal editorial crop and colour grade of *actual* photographed 2027 car.
    # Strict native dimensions; no generic vector, synthetic design or advertising text.
    target=(1600,900) if role=="featured" else (1400,900)
    W,H=target
    if src.width<W or src.height<H:raise RuntimeError("Refusing to upscale Corsa MY2027 photo")
    centering=(0.53,0.50) if role=="featured" else (0.43,0.48)
    image=ImageOps.fit(src,target,method=Image.Resampling.LANCZOS,centering=centering)
    image=ImageEnhance.Contrast(image).enhance(1.045)
    image=ImageEnhance.Color(image).enhance(1.025)
    buf=io.BytesIO()
    image.save(buf,format="WEBP",quality=89,method=6)
    data=buf.getvalue()
    if not 38_000<len(data)<2_000_000 or data[:4]!=b"RIFF" or data[8:12]!=b"WEBP":
        raise RuntimeError("Discover featured image is not true large sharp WebP")
    return data

def media(src,role):
    fname="a3tal-opel-corsa-2027-discover-"+role+"-real-car.webp"
    image=generate_image(src,role)
    return {"key":role,"role":role,
      "filename":fname,"image_base64":base64.b64encode(image).decode("ascii"),
      "convert_webp":False,
      "alt":("أوبل كورسا 2027 توب لاين بلس في مصر، صورة السيارة الحقيقية" if role=="featured"
            else "تفاصيل التصميم الخارجي لأوبل كورسا Topline+ موديل 2027"),
      "caption":"صورة حقيقية للسيارة من الليثي أوتو، بتكوين تحريري خاص بأعطال.كوم. المصدر: "+SOURCE_PAGE,
      "placeholder":"{{a3tal_image:detail}}"}

def verify_post(pid,expected_feature):
    r=get("/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode(
      {"_fields":"id,status,slug,link,featured_media,categories,content,yoast_head_json"}))
    seo=r.get("yoast_head_json") or {}
    robots=seo.get("robots") or {}
    og=(seo.get("og_image") or [{}])[0].get("url","")
    content=(r.get("content") or {}).get("rendered","")
    checks={
      "status":r.get("status")=="publish","url":r.get("link")==URL,"slug":r.get("slug")==SLUG,
      "category":CATEGORY in r.get("categories",[]),
      "featured":r.get("featured_media")==expected_feature and bool(expected_feature),
      "og_real_image":"a3tal-opel-corsa-2027-discover-featured-real-car.webp" in og,
      "canonical":seo.get("canonical")==URL,
      "indexable":robots.get("index")!="noindex",
      "inline_image":"a3tal-opel-corsa-2027-discover-inline-real-car.webp" in content,
      "content":content.count("<h2")>=9 and "1,300,000" in content and "Topline" in content,
      "no_placeholder":"{{a3tal_image:" not in content
    }
    if not all(checks.values()):raise RuntimeError("PUBLIC_POST_QA_FAILED "+repr(checks))
    return {"id":pid,"url":URL,"featured":expected_feature,"og_image":og,
            "category":CATEGORY,"canonical":seo.get("canonical"),"checks":checks}

def homepage_check():
    specs=[(SITE+"/","a3egy-price-grid","a3egy-market-quick"),
           (SITE+"/cars/","cg-latest-price-articles","cg-popular")]
    for uri,start,end in specs:
        seen=False
        for n in range(9):
            query="?corsa_2027_publish_check=20261112_"+str(n)
            request=urllib.request.Request(uri+query,headers={
                "User-Agent":"Mozilla/5.0 (A3tal Discover featured-price-article QA)",
                "Cache-Control":"no-cache"})
            with urllib.request.urlopen(request,timeout=60) as res:
                raw=res.read(3_000_000).decode("utf-8","replace")
            a=raw.find(start)
            b=raw.find(end,a+len(start)) if a>=0 else -1
            # Use fixed section markers, not footer/sidebar links.
            block=raw[a:b] if a>=0 and b>a else ""
            haslink=SLUG in block
            hasphoto="a3tal-opel-corsa-2027-discover-featured-real-car" in block
            print("CORSА_PRICE_GRID_QA",uri,"card",haslink,"image",hasphoto,"sectionBytes",len(block),flush=True)
            if haslink and hasphoto:seen=True;break
            time.sleep(8)
        if not seen:raise RuntimeError("Homepage or /cars/ section missing actual new Corsa price card+photo: "+uri)
    print("CORSА_ARTICLE_VISIBLE_HOME_AND_CARS_WITH_ACTUAL_PHOTO",flush=True)

def main():
    if not KEY:raise RuntimeError("A3tal Direct Bridge key absent")
    body=HTML.read_text("utf-8")
    if len(body)<8_000 or body.count("<h2>")<8 or body.count("<table>")!=2 or "1,300,000" not in body or "{{a3tal_image:detail}}" not in body:
        raise RuntimeError("Original price editorial not complete")
    prev=existing(SLUG)
    if not prev:
        collision_guard()
        cat=get("/wp-json/wp/v2/categories/374?_fields=id,name")
        if cat.get("id")!=374 or "السيارات" not in cat.get("name",""):
            raise RuntimeError("Price article category incorrect")
        src=fetch_photo()
        images=[media(src,"featured"),media(src,"inline")]
        meta={
          "_yoast_wpseo_title":"سعر أوبل كورسا 2027 في مصر بعد زيادة 50 ألف | أعطال.كوم",
          "_yoast_wpseo_metadesc":"سعر أوبل كورسا 2027 Topline+ في مصر 1,300,000 جنيه بعد زيادة 50 ألفًا. المواصفات والمحرك 130 حصان والفتيس والتجهيزات وهل تستحق الشراء.",
          "_yoast_wpseo_focuskw":"سعر أوبل كورسا 2027 في مصر",
          "_yoast_wpseo_canonical":URL,
          "_yoast_wpseo_opengraph-title":TITLE,
          "_yoast_wpseo_opengraph-description":"أوبل كورسا 2027 بقت بـ1.3 مليون جنيه بعد زيادة 50 ألفًا. السعر الرسمي ومواصفات Topline+ وتجهيزات الشراء.",
          "_yoast_wpseo_twitter-title":TITLE
        }
        post={"type":"post","status":"publish","slug":SLUG,"title":TITLE,
          "content":body,"categories":[CATEGORY],
          "excerpt":"سعر أوبل كورسا 2027 في مصر وصل إلى 1,300,000 جنيه بعد زيادة 50 ألف. تفاصيل فئة Topline+ والمواصفات والضمان والمقارنة مع فرونتيرا.",
          "meta":meta}
        result=get("/publish-bundle",authenticated=True,data={"post":post,"media":images},timeout=350)
        prev=result.get("post") or {}
        if prev.get("status")!="publish" or prev.get("slug")!=SLUG or not prev.get("id") or not prev.get("featured_media"):
            raise RuntimeError("A3tal Direct Bridge did not confirm complete publication: "+repr(prev)[:250])
    else:
        print("CORSА_2027_ARTICLE_ALREADY_EXISTS_QA_ONLY",prev.get("id"),flush=True)
        if prev.get("status")!="publish" or not prev.get("featured_media"):
            raise RuntimeError("Existing post is unverified; refusing duplicate")
    record=verify_post(prev["id"],prev["featured_media"])
    REPORT.write_text(json.dumps({"article":record,"homepage_checked":False},ensure_ascii=False,indent=2),"utf-8")
    print("CORSА_ARTICLE_PUBLIC_CANONICAL_IMAGE_VERIFIED",URL,flush=True)
    homepage_check()
    REPORT.write_text(json.dumps({"article":record,"homepage_checked":True,
       "discover_image_size":"1600x900 WEBP","source":SOURCE_PAGE},ensure_ascii=False,indent=2),"utf-8")
    print("CORSА_PRICE_2027_PUBLISHED_DISCOVER_AND_HOME_VERIFIED",URL,flush=True)

if __name__=="__main__":main()
