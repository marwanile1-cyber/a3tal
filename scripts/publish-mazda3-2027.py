#!/usr/bin/env python3
"""Publish Mazda3 2027 editorial via the approved A3tal Direct Bridge; no WPWriter."""
import os, json, base64, time, io, re, sys
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps, ImageDraw

API = "https://a3tal.com/wp-json/a3tal-direct/v1"
SECRET = os.environ.get("A3TAL_API_KEY", "")
DATA = json.loads(Path("publish-payloads/mazda-3-2027-egypt.json").read_text(encoding="utf-8"))
if not SECRET: raise SystemExit("Missing A3TAL_API_KEY secret")
HEADERS = {"X-A3tal-Key": SECRET, "Authorization": "Bearer " + SECRET, "User-Agent": "A3tal-Editorial-Publisher/1.0"}

def request(path, payload=None, method=None, protected=True, retries=4):
    url = API + path if path.startswith("/") else path
    h = dict(HEADERS if protected else {"User-Agent": "Mozilla/5.0 (A3tal.com editorial)"})
    body = None
    if payload is not None:
        body = json.dumps(payload,ensure_ascii=False).encode("utf-8")
        h["Content-Type"] = "application/json"
    for i in range(retries):
        try:
            req=Request(url,data=body,headers=h,method=method or ("POST" if body else "GET"))
            with urlopen(req,timeout=180) as r:
                raw=r.read()
                if url.startswith(API): return json.loads(raw)
                return raw
        except Exception as e:
            print(f"request attempt {i+1}/{retries} {path.split('?')[0]}: {type(e).__name__}: {str(e)[:170]}",flush=True)
            if i == retries-1: raise
            time.sleep(8 * (i+1))

def original_image(url):
    raw=request(url,protected=False)
    img=Image.open(io.BytesIO(raw)).convert("RGB")
    print(f"Verified official Mazda image: {img.size} {url}",flush=True)
    if img.width < 600 or img.height < 350: raise RuntimeError("Too-small official Mazda source")
    return img

def frame(im, size=(1600,900), tone=1.04):
    im=ImageOps.fit(im,size,method=Image.Resampling.LANCZOS,centering=(0.5,0.48))
    im=ImageEnhance.Contrast(im).enhance(tone)
    im=ImageEnhance.Color(im).enhance(1.06)
    return im

def media_payload(im, filename, title, alt, role, placeholder=None):
    out=io.BytesIO()
    im.save(out,format="WEBP",quality=84,method=6)
    result={"filename":filename,"title":title,"alt":alt,"role":role,"convert_webp":False,"image_base64":base64.b64encode(out.getvalue()).decode("ascii")}
    if placeholder: result["placeholder"]=placeholder
    print(f"Prepared {filename}: {im.size}, {len(out.getvalue())} bytes",flush=True)
    return result

def main():
    status=request("/status")
    print("Bridge:",status.get("version"),flush=True)
    if not status.get("ok"): raise SystemExit("Bridge health failed")

    matches=request("/search-posts?"+urlencode({"search":"مازدا 3","limit":100,"status":"any"})).get("items",[])
    same=[x for x in matches if x.get("slug")==DATA["post"]["slug"]]
    overlaps=[x for x in matches if "2027" in (x.get("title") or "") and ("مازدا" in (x.get("title") or ""))]
    print("Mazda 3 existing candidates:",json.dumps(matches,ensure_ascii=False)[:2500],flush=True)
    if overlaps and not same:
        raise SystemExit("Existing Mazda 2027 post(s) need review before publishing to avoid cannibalization: "+json.dumps(overlaps,ensure_ascii=False))
    post=dict(DATA["post"])
    if same:
        print("Updating exact-slug existing article; no duplicate.",same[0]["id"],flush=True)
        post["id"]=same[0]["id"]

    try:
        categories=request("/admin?"+urlencode({"op":"terms","taxonomy":"category","limit":"500"}))
        terms=categories.get("result",[]) if isinstance(categories,dict) else []
        print("Candidate categories:",[(t.get("id"),t.get("name")) for t in terms if any(w in t.get("name","") for w in ("السيارات","أخبار","اسعار","أسعار"))][:40],flush=True)
        exact=["اسعار السيارات الجديدة","أسعار السيارات الجديدة","أسعار السيارات","أخبار السيارات"]
        chosen=next((t for name in exact for t in terms if t.get("name","").strip()==name),None)
        if not chosen:
            chosen=next((t for t in terms if "أسعار السيارات" in t.get("name","") or "اسعار السيارات" in t.get("name","")),None)
        if chosen:
            post["categories"]=[int(chosen["id"])]
            print("Selected category:",chosen["id"],chosen["name"],flush=True)
        else:
            print("No confirmed dedicated price category; using existing editorial category 374",flush=True)
            post["categories"]=[374]
    except Exception as e:
        print("Category lookup unavailable; use established price-category id 374:",type(e).__name__,str(e)[:120],flush=True)
        post["categories"]=[374]

    src=DATA["sources"]
    sedan=original_image(src["hero"][0])
    hatch=original_image(src["hero"][1])
    hero=Image.new("RGB",(1600,900))
    hero.paste(frame(sedan,(800,900)),(0,0))
    hero.paste(frame(hatch,(800,900)),(800,0))
    hero=ImageEnhance.Contrast(hero).enhance(1.08)
    exterior=frame(original_image(src["exterior"]))
    interior=frame(original_image(src["interior"]))
    media=[
        media_payload(hero,"mazda-3-2027-egypt-sedan-hatchback-a3tal.webp","مازدا 3 موديل 2027 السيدان والهاتشباك في مصر","مازدا 3 سيدان وهاتشباك في مقارنة بصرية لسعر موديل 2027 في مصر","featured"),
        media_payload(exterior,"mazda-3-2027-egypt-exterior-a3tal.webp","مازدا 3 من الخارج في مراجعة الأسعار","مازدا 3 من الخارج في صورة من معرض مازدا الرسمي للسيارة","inline","{{a3tal_image:exterior}}"),
        media_payload(interior,"mazda-3-egypt-interior-a3tal.webp","مقصورة مازدا 3 وتجهيزات القيادة","صورة توضيحية لمقصورة مازدا 3 من مواد مازدا الرسمية وتجهيزات قد تختلف حسب الفئة","inline","{{a3tal_image:interior}}")
    ]
    print("Submitting one guarded publish bundle with three WEBP media items...",flush=True)
    published=request("/publish-bundle",{"post":post,"media":media})
    obj=published.get("post",{})
    postid=obj.get("id")
    print("RESULT:",json.dumps({"ok":published.get("ok"),"id":postid,"status":obj.get("status"),"link":obj.get("link"),"featured_media":obj.get("featured_media"),"media":{k:{"media_id":v.get("media_id"),"url":v.get("url"),"width":v.get("width"),"height":v.get("height")} for k,v in published.get("media",{}).items()}},ensure_ascii=False),flush=True)
    if not published.get("ok") or obj.get("status")!="publish" or not postid or not obj.get("featured_media"):
        raise SystemExit("Publish bundle did not return a published article with featured media")
    check=request("/post/"+str(postid))
    images=published["media"]
    assert check.get("status")=="publish"
    assert check.get("featured_media")==images["image_1"]["media_id"] if "image_1" in images else check.get("featured_media")==next(iter(images.values()))["media_id"]
    assert "{{a3tal_image:" not in check.get("content",""),"Unresolved image placeholder"
    assert len(re.findall(r"<img\b",check.get("content","")) )>=2,"Internal article images missing"
    assert check.get("meta",{}).get("_yoast_wpseo_metadesc"),"Yoast meta missing"
    print("BRIDGE VERIFIED:",json.dumps({"id":postid,"link":check.get("link"),"status":check.get("status"),"featured_media":check.get("featured_media"),"inline_images":len(re.findall(r"<img\b",check.get("content","")))},ensure_ascii=False),flush=True)

    url=check["link"]
    for wait in (0,10,20,35):
        if wait: time.sleep(wait)
        try:
            page=request(url+"?editorial_check="+str(int(time.time())),protected=False,retries=2).decode("utf-8","replace")
            og=re.search(r'<meta[^>]*(?:property|name)=["\x27]og:image["\x27][^>]*>',page,re.I)
            hero_url=images["image_1"]["url"] if "image_1" in images else next(iter(images.values()))["url"]
            if not og or hero_url not in og.group(0):
                raise RuntimeError("og:image does not match expected featured image")
            if "مازدا 3" not in page: raise RuntimeError("Missing Mazda 3 title in public HTML")
            print("PUBLIC HTML VERIFIED: HTTP 200, Mazda title and matching og:image, URL:",url,flush=True)
            return
        except Exception as e:
            print("Public verification retry:",type(e).__name__,str(e)[:240],flush=True)
    raise SystemExit("Article published in WordPress but CDN/public og:image still unverified; inspect live cache")

if __name__=="__main__":
    main()
