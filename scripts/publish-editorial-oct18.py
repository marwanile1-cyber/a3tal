#!/usr/bin/env python3
"""Publish nine original, categorised auto guides with real photos through A3tal Direct Bridge.
Exactly one publish mutation per new article; never blindly replay ambiguous writes.
Source media are photos, original cover cropping with no text or screenshots.
"""
import base64,io,json,os,re,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance,ImageDraw

BASE="https://a3tal.com"
API=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
DATA=Path("data/editorial-oct-18-2026.json")
if not KEY:raise SystemExit("Missing A3TAL_API_KEY")

def get(url,payload=None,auth=True):
    url=url if url.startswith("https://") else API+url
    # WordPress filenames can contain Arabic characters. HTTP request paths must be ASCII.
    url=urllib.parse.quote(url,safe=":/?&=%#@+,;")
    headers={"User-Agent":"A3talIndependentEditorial20261018/1.0","Accept":"application/json,text/html,image/*,*/*","Cache-Control":"no-cache"}
    if auth: headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf-8")
    if data is not None:headers["Content-Type"]="application/json"
    # Writes must never be retried blindly when a CDN drops the response.
    attempts=1 if data is not None else 3
    for i in range(attempts):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=headers),timeout=125) as resp:
                body=resp.read()
            return json.loads(body) if auth else body
        except Exception as exc:
            if i==attempts-1:raise
            print("READ_RETRY",i+1,type(exc).__name__,str(exc)[:140],flush=True)
            time.sleep(7*(i+1))

def wp_post(slug):
    url=BASE+"/wp-json/wp/v2/posts?"+urllib.parse.urlencode({
        "slug":slug,"per_page":3,"_fields":"id,slug,status,link,featured_media"})
    rows=json.loads(get(url,auth=False))
    if len(rows)>1:raise RuntimeError("Duplicate slug detected: "+slug)
    return rows[0] if rows else None

def cover(article):
    imgs=[]
    for url in article["photos"]:
        data=get(url,auth=False)
        img=Image.open(io.BytesIO(data))
        img.load()
        if img.width<500 or img.height<350:raise RuntimeError("Photo source too small: "+url)
        # If one source is taller than wide still use a photographic crop, not synthetic art.
        if len(article["photos"])==1:
            img=ImageOps.fit(img.convert("RGB"),(1600,900),method=Image.Resampling.LANCZOS)
        else:
            img=ImageOps.fit(img.convert("RGB"),(800,900),method=Image.Resampling.LANCZOS)
        imgs.append(img)
    if len(imgs)==1:final=imgs[0]
    elif len(imgs)==2:
        final=Image.new("RGB",(1600,900))
        for i,img in enumerate(imgs):final.paste(img,(800*i,0))
        ImageDraw.Draw(final).rectangle([797,0,803,900],fill=(228,231,234))
    else:raise RuntimeError("Unsupported number of photo sources")
    final=ImageEnhance.Contrast(final).enhance(1.035)
    out=io.BytesIO()
    final.save(out,format="WEBP",quality=83,method=6)
    raw=out.getvalue()
    if not 18000<len(raw)<2300000:raise RuntimeError("Bad featured WebP length")
    filename="a3tal-editorial-20261018-"+article["slug"]+".webp"
    print("WEBP_PHOTOGRAPH_READY",article["slug"],len(raw),flush=True)
    return {"filename":filename,"title":article["title"],"alt":article["title"]+" - صورة فوتوغرافية توضيحية",
            "role":"featured","convert_webp":False,
            "image_base64":base64.b64encode(raw).decode("ascii")}

def validate(article):
    html=article["html"]
    if len(html)<3500 or html.count("<h2>")<5 or html.count("<h3>")<3:
        raise RuntimeError("Editorial depth missing: "+article["slug"])
    if not re.fullmatch(r"[a-z0-9-]{15,110}",article["slug"]):raise RuntimeError("Unsafe slug")
    if article["category_id"] not in [374,21,22,8,13,3,85,3028,33]:
        raise RuntimeError("Unknown verified category")
    if not 1<=len(article["photos"])<=2:raise RuntimeError("Photo requirement missing")
    if article["html"].count("<a href=")<2:raise RuntimeError("Missing contextual links")

def verify(article,id_,featured,link):
    for pause in [0,12,24,36]:
        if pause:time.sleep(pause)
        try:
            row=wp_post(article["slug"])
            if not row or int(row["id"])!=id_ or row["status"]!="publish" or int(row["featured_media"])!=featured:
                raise RuntimeError("Published REST article/cover mismatch")
            page=get(link+"?a3tal_check="+str(int(time.time())),auth=False).decode("utf-8","replace")
            if article["title"] not in page or "og:image" not in page:
                raise RuntimeError("Public HTML title/OG missing")
            if "a3tal-editorial-20261018-"+article["slug"] not in page:
                raise RuntimeError("New article featured cover not exposed")
            if re.search(r'<meta[^>]*name=["\x27]robots["\x27][^>]*noindex',page,re.I):
                raise RuntimeError("Public post unexpectedly noindexed")
            print("PUBLISHED_AND_PUBLICLY_VERIFIED",link,"ID",id_,"WEBP",featured,flush=True)
            return
        except Exception as exc:
            print("PUBLIC_QA_RECHECK",article["slug"],type(exc).__name__,str(exc)[:140],flush=True)
    raise RuntimeError("Public verification failed: "+article["slug"])

def main():
    batch=json.loads(DATA.read_text(encoding="utf-8"))
    items=batch["items"]
    if len(items)!=9 or len({a["slug"] for a in items})!=9:
        raise RuntimeError("Expected nine distinct articles")
    st=get("/status")
    if not st.get("ok"):raise RuntimeError("Bridge unavailable")
    print("BRIDGE_READY",st.get("version"),flush=True)
    results=[]
    for index,article in enumerate(items,1):
        validate(article)
        print("ARTICLE_START",index,article["slug"],flush=True)
        existing=wp_post(article["slug"])
        if existing:
            if existing.get("status")!="publish" or not existing.get("featured_media"):
                raise RuntimeError("Manual review required for partial existing article: "+article["slug"])
            print("ARTICLE_ALREADY_PUBLISHED",existing["link"],flush=True)
            results.append({"slug":article["slug"],"link":existing["link"],"reused":True})
            continue
        image=cover(article)
        payload={"title":article["title"],"slug":article["slug"],
            "type":"post","status":"publish","excerpt":article["excerpt"],
            "content":article["html"],"categories":[article["category_id"]],
            "meta":{"_yoast_wpseo_title":article["title"],
                    "_yoast_wpseo_metadesc":article["meta"],
                    "_yoast_wpseo_focuskw":article["focus"],
                    "_yoast_wpseo_canonical":BASE+"/"+article["slug"]+"/",
                    "_yoast_wpseo_opengraph-title":article["title"],
                    "_yoast_wpseo_opengraph-description":article["meta"]}}
        try:
            result=get("/publish-bundle",{"post":payload,"media":[image]})
        except Exception as exc:
            # A successful mutation may have a lost response. Never create the same slug twice.
            print("AMBIGUOUS_WRITE_CHECK_STATUS_BEFORE_RETRY",article["slug"],type(exc).__name__,str(exc)[:190],flush=True)
            raise
        post=result.get("post") or {}
        id_=int(post.get("id") or 0)
        featured=int(post.get("featured_media") or 0)
        if not result.get("ok") or not id_ or post.get("status")!="publish" or not featured:
            raise RuntimeError("Publish acknowledgement incomplete: "+article["slug"])
        link=post.get("link") or BASE+"/"+article["slug"]+"/"
        verify(article,id_,featured,link)
        results.append({"slug":article["slug"],"link":link,"category_id":article["category_id"]})
        print("ARTICLE_COMPLETE",len(results),"/",len(items),flush=True)
    print("EDITORIAL_OCT18_FINAL_LINKS",json.dumps(results,ensure_ascii=False),flush=True)
    if len(results)!=9:raise RuntimeError("Batch incomplete")

if __name__=="__main__":
    main()
