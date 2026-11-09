#!/usr/bin/env python3
"""Batch37: publish five original Chery Tiggo 4 Pro Turbo Egypt technical-reference pages.

Only A3tal Direct Bridge and the car-reference importer are used.
Every article uses a distinct photo from Chery Egypt Tiggo 4 Pro official model gallery.
Fail closed if official photo cannot be downloaded; never substitute vector or fake car art. Never overwrite existing posts, verify public canonical and OG.
"""
import base64,hashlib,io,json,os,re,time
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageEnhance,ImageFilter
from html import escape
import requests

ROOT=Path(__file__).resolve().parents[1]
DB=json.loads((ROOT/"data/car-reference/batch-37-chery-tiggo4pro-turbo-egypt.json").read_text("utf-8"))
ROWS=DB["rows"]
BASE="https://a3tal.com"
MODEL=DB["model_slug"]
BRAND="chery"
REPORT=ROOT/"reports/batch37-tiggo4pro-live-audit.json"
REPORT.parent.mkdir(parents=True,exist_ok=True)
S=requests.Session()
S.headers.update({"User-Agent":"A3tal-Tech-Reference-Batch37/1.0"})
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY required")
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
ROOT_URL=BASE+"/car-reference/chery/"+MODEL+"/"
CAP=min(len(ROWS),max(1,int(os.environ.get("A3CR_BATCH37_LIMIT","5"))))
PHOTO_URLS=[
 "https://www.chery-eg.com/media/ModelsBanner/image00001.jpeg",
 "https://www.chery-eg.com/media/performanceBanners/Performance-Banner--1720--600-px.jpg",
 "https://www.chery-eg.com/media/intDesignImages/Large-interior-exterior-banner--1720--600-px.jpg",
 "https://www.chery-eg.com/media/ModelsBanner/Mobile_Banner_final_1.png",
 "https://www.chery-eg.com/media/images/TIGGO_4_PRO_car_img_2026-09-03_133831.203775.png",
]
assert len(PHOTO_URLS)==len(set(PHOTO_URLS))==5
PROGRESS=[]

def get(url,**kw):
    for attempt in range(4):
        try:
            r=S.get(url,timeout=75,**kw)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if attempt==3:raise
            time.sleep(3*(attempt+1))

def post(url,payload):
    for attempt in range(4):
        try:
            r=S.post(url,json=payload,headers=HEAD,timeout=180)
            if r.status_code>=500:raise requests.RequestException("Transient HTTP "+str(r.status_code))
            if not r.ok:raise RuntimeError("HTTP "+str(r.status_code)+" "+r.text[:300])
            return r.json()
        except requests.RequestException:
            if attempt==3:raise
            time.sleep(4*(attempt+1))

def existing(slug):
    resp=get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":30})
    return [p for p in resp.json() if p.get("slug")==slug and p.get("status")=="publish"]

def namefont(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"):
        if Path(p).is_file():return ImageFont.truetype(p,sz)
    return ImageFont.load_default()

def exact_model_photo(url):
    # Exact image URLs observed in the official Chery Egypt Tiggo 4 Pro model gallery.
    from urllib.parse import urlsplit
    if url not in PHOTO_URLS or urlsplit(url).hostname!="www.chery-eg.com":
        raise RuntimeError("Not an approved official Chery Tiggo 4 Pro image URL "+url)
    raw=get(url).content
    if len(raw)<12000:raise RuntimeError("Official Tiggo4 Pro Turbo image too small "+url)
    orig=Image.open(io.BytesIO(raw))
    if orig.mode=="RGBA":
        # Some manufacturer 360-degree real car renders use transparency.
        canvas=Image.new("RGBA",orig.size,(235,241,245,255))
        canvas.alpha_composite(orig)
        im=canvas.convert("RGB")
    else:
        im=orig.convert("RGB")
    if im.width<550 or im.height<280:raise RuntimeError("Too-small OEM image "+str(im.size)+" "+url)
    print("CHERY_TIGGO4PRO_VERIFIED_REAL_PHOTO",url,str(im.size),flush=True)
    return im

def cover(photo,index):
    # Photo-first 1600x900 editorial crop, NEVER generic vector art or fake car.
    # Preserve the entire authentic car frame in the centered contain layer.
    W,H=1600,900
    base=ImageOps.fit(photo,(W,H),method=Image.Resampling.LANCZOS)
    base=base.filter(ImageFilter.GaussianBlur(28))
    base=ImageEnhance.Brightness(base).enhance(0.8)
    inset=ImageOps.contain(photo,(W-32,H-32),method=Image.Resampling.LANCZOS)
    base.paste(inset,((W-inset.width)//2,(H-inset.height)//2))
    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    d.rounded_rectangle((1377,834,1574,874),radius=9,fill=(9,28,42,135))
    for fp in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
               "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(fp).exists():
            d.text((1400,840),"A3TAL.COM",font=ImageFont.truetype(fp,20),fill=(255,255,255,235))
            break
    base=Image.alpha_composite(base.convert("RGBA"),overlay).convert("RGB")
    out=io.BytesIO()
    base.save(out,"WEBP",quality=88,method=6)
    result=out.getvalue()
    if len(result)<18000 or result[:4]!=b"RIFF" or result[8:12]!=b"WEBP":
        raise RuntimeError("Featured image failed photographic WebP gate")
    return result

def audit_live(url,title,image):
    error=None
    for attempt in range(7):
        try:
            r=get(url,params={"a3_batch37_audit":str(time.time_ns())},
                  headers={"Cache-Control":"no-cache"})
            h=r.text
            if r.url.split("?")[0].rstrip("/")!=url.rstrip("/"):raise RuntimeError("URL redirect")
            if title not in h or image not in h:raise RuntimeError("Headline or image absent")
            m=re.search(r'<meta[^>]+property=["\x27]og:image["\x27][^>]*>',h,re.I)
            if not m or image not in m.group(0):raise RuntimeError("OG image incorrect")
            c=re.search(r'<link[^>]+rel=["\x27]canonical["\x27][^>]*>',h,re.I)
            if not c or url.rstrip("/") not in c.group(0):raise RuntimeError("Canonical incorrect")
            if re.search(r'<meta[^>]+name=["\x27]robots["\x27][^>]*noindex',h[:20000],re.I):
                raise RuntimeError("Unexpected noindex")
            return True
        except Exception as exc:
            error=str(exc)
            time.sleep(3)
    raise RuntimeError("Public QA failed "+url+" "+str(error))

def main():
    health=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    if not health.get("ok") or health.get("published",0)<425:
        raise RuntimeError("Existing 425-page reference corpus not healthy: "+repr(health))
    parent=existing(BRAND)
    if len(parent)!=1 or parent[0].get("link","").rstrip("/")!=BASE+"/car-reference/chery":
        raise RuntimeError("Existing Chery brand parent not uniquely verified")
    assert len(ROWS)==5 and len({r["slug"] for r in ROWS})==5
    # Fail before publishing anything if any official photo cannot be verified.
    PRECHECK_PHOTOS=[exact_model_photo(url) for url in PHOTO_URLS[:CAP]]
    for i,row in enumerate(ROWS[:CAP]):
        slug=row["slug"]
        kind=row["kind"]
        base=BASE+"/car-reference/chery/"
        url=base+(slug+"/" if kind=="model" else MODEL+"/"+slug+"/")
        prev=existing(slug)
        if prev:
            if len(prev)!=1 or prev[0]["link"].rstrip("/")!=url.rstrip("/"):
                raise RuntimeError("Slug collision or wrong nested URL "+slug)
            PROGRESS.append({"slug":slug,"url":url,"status":"existing"})
            print("ALREADY_PUBLISHED",url,flush=True)
            continue
        if kind=="spec":
            model=existing(MODEL)
            if len(model)!=1 or model[0]["link"].rstrip("/")!=ROOT_URL.rstrip("/"):
                raise RuntimeError("Model hub not yet published")
        im=PRECHECK_PHOTOS[i]
        picture=cover(im,i)
        fname="a3tal-pseo-b37-tiggo4pro-real-"+slug+".webp"
        media=post(UPLOAD,{"filename":fname,"image_base64":base64.b64encode(picture).decode(),
                           "convert_webp":False,"title":row["title"],"alt":row["title"]+" - أعطال.كوم"})
        image_id=int(media.get("media_id") or 0)
        if image_id<1 or not str(media.get("url","")).endswith(".webp"):
            raise RuntimeError("Photo upload not verified")
        data={"kind":kind,"market":"Egypt / Chery Tiggo 4 Pro Turbo 1.5 CVT",
              "years":"جدول الفئات الرسمي في مصر؛ مراجعة 2026-11-09",
              "engine":"Chery Tiggo 4 Pro Turbo 1.5T / 145HP / 210Nm / CVT",
              "category":row["category"],"reviewed_at":"2026-11-09",
              "facts":[{"label":f[0],"value":f[1]} for f in row["facts"]],
              "sources":[{"title":"Chery Egypt Tiggo 4 Pro Turbo Official","url":u} for u in row["sources"]]}
        payload={"kind":kind,"slug":slug,"title":row["title"],
                 "parent_path":BRAND if kind=="model" else BRAND+"/"+MODEL,
                 "featured_image_id":image_id,"status":"publish",
                 "content":row["rich_html"],"excerpt":row["meta_description"],
                 "meta_title":row["title"]+" | أعطال.كوم",
                 "meta_description":row["meta_description"],"data":data}
        result=post(UPSERT,{"items":[payload]})
        outcomes=result.get("results") or []
        if len(outcomes)!=1 or not outcomes[0].get("ok") or outcomes[0].get("status")!="publish":
            raise RuntimeError("WordPress upsert failed "+repr(result)[:400])
        if outcomes[0].get("url","").rstrip("/")!=url.rstrip("/"):
            raise RuntimeError("Canonical destination changed "+repr(outcomes))
        audit_live(url,row["title"],fname)
        PROGRESS.append({"slug":slug,"url":url,"image":media["url"],
                         "image_file":fname,"photo_source":PHOTO_URLS[i],"visual_source":"official real Tiggo 4 Pro photo from Chery Egypt gallery","status":"published",
                         "og_verified":True,"canonical_verified":True})
        print("BATCH37_PUBLIC_ARTICLE_AND_OG_VERIFIED",url,flush=True)
    after=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    if after.get("drafts")!=0:raise RuntimeError("Unexpected draft count")
    if after.get("published",0)<health["published"]+sum(x["status"]=="published" for x in PROGRESS):
        raise RuntimeError("Published count did not increase")
    print("BATCH37_CHERY_TIGGO4PRO_COMPLETE",len(PROGRESS),after["published"],flush=True)

if __name__=="__main__":
    try:main()
    finally:
        REPORT.write_text(json.dumps({"batch":37,"rows":PROGRESS},ensure_ascii=False,indent=2),"utf-8")
