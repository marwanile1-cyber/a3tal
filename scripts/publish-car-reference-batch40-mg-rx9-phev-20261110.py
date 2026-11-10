#!/usr/bin/env python3
"""Batch40: publish five original MG RX9 PHEV Egypt technical-reference pages.

Only A3tal Direct Bridge and the car-reference importer are used.
Every article uses a different pair of actual MG RX9 PHEV manufacturer photos at native source size; no blurry upscaling.
Fail closed if official photo cannot be downloaded; never substitute vector or fake car art. Never overwrite existing posts, verify public canonical and OG.
"""
import base64,hashlib,io,json,os,re,time
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageEnhance,ImageFilter
from html import escape
import requests

ROOT=Path(__file__).resolve().parents[1]
DB=json.loads((ROOT/"data/car-reference/batch-40-mg-rx9-phev-egypt.json").read_text("utf-8"))
ROWS=DB["rows"]
BASE="https://a3tal.com"
MODEL=DB["model_slug"]
BRAND="mg"
REPORT=ROOT/"reports/batch40-mg-rx9-phev-live-audit.json"
REPORT.parent.mkdir(parents=True,exist_ok=True)
S=requests.Session()
S.headers.update({"User-Agent":"A3tal-Tech-Reference-Batch40/1.0"})
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY required")
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
ROOT_URL=BASE+"/car-reference/mg/"+MODEL+"/"
CAP=min(len(ROWS),max(1,int(os.environ.get("A3CR_BATCH40_LIMIT","5"))))
PHOTO_URLS=[
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-55-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-57-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-58-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-59-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-60-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-84-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-34-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-42-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-70-1.webp",
 "https://www.mgmotor.com.eg/wp-content/uploads/2026/06/MG_RX9-High-Res-71-1.webp",
]
assert len(PHOTO_URLS)==len(set(PHOTO_URLS))==10
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
    # Exact image URLs observed in the official MG Motor Egypt RX9 PHEV model gallery.
    from urllib.parse import urlsplit
    if url not in PHOTO_URLS or urlsplit(url).hostname!="www.mgmotor.com.eg":
        raise RuntimeError("Not an approved MG Motor Egypt RX9 PHEV photo URL "+url)
    raw=get(url).content
    if len(raw)<12000:raise RuntimeError("Official MG RX9 PHEV gallery photo too small "+url)
    orig=Image.open(io.BytesIO(raw))
    if orig.mode=="RGBA":
        # Some manufacturer 360-degree real car renders use transparency.
        canvas=Image.new("RGBA",orig.size,(235,241,245,255))
        canvas.alpha_composite(orig)
        im=canvas.convert("RGB")
    else:
        im=orig.convert("RGB")
    if im.width<800 or im.height<600:raise RuntimeError("Too-small genuine OEM image "+str(im.size)+" "+url)
    print("MG_RX9_PHEV_VERIFIED_REAL_PHOTO",url,str(im.size),flush=True)
    return im

def cover(pair,index):
    """1600x900 photo diptych: two different genuine MG RX9 PHEV pictures.
    Each photo is downscaled or kept at native resolution. Never upscale.
    The blurred atmospheric backdrop is decorative; photo panels stay sharp.
    """
    W,H=1600,900
    if len(pair)!=2:raise RuntimeError("Need two independent original MG photos")
    left,right=pair
    if left.width<800 or left.height<600 or right.width<800 or right.height<600:
        raise RuntimeError("Manufacturer images must each be at least 800x600")
    if hashlib.sha256(left.tobytes()).digest()==hashlib.sha256(right.tobytes()).digest():
        raise RuntimeError("Two photos for a featured image must be different")
    bg=ImageOps.fit(left,(W,H),method=Image.Resampling.LANCZOS)
    bg=ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(35))).enhance(.62)
    frame_w,frame_h=776,582
    for i,pic in enumerate(pair):
        tile=ImageOps.fit(pic,(frame_w,frame_h),method=Image.Resampling.LANCZOS)
        if pic.width<tile.width or pic.height<tile.height:
            raise RuntimeError("No upscaling of primary real-car photo")
        x=16+i*792
        y=159
        bg.paste(tile,(x,y))
    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    draw=ImageDraw.Draw(overlay)
    draw.rounded_rectangle((1375,836,1578,874),radius=8,fill=(7,20,35,170))
    for font_path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                      "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(font_path).exists():
            draw.text((1393,841),"A3TAL.COM",font=ImageFont.truetype(font_path,20),fill=(255,255,255,240))
            break
    final=Image.alpha_composite(bg.convert("RGBA"),overlay).convert("RGB")
    buf=io.BytesIO()
    final.save(buf,"WEBP",quality=90,method=6)
    data=buf.getvalue()
    if len(data)<24000 or data[:4]!=b"RIFF" or data[8:12]!=b"WEBP":
        raise RuntimeError("Featured true-WebP photo composition QA failed")
    return data

def audit_live(url,title,image):
    error=None
    for attempt in range(7):
        try:
            r=get(url,params={"a3_batch40_audit":str(time.time_ns())},
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
    if not health.get("ok") or health.get("published",0)<440:
        raise RuntimeError("Existing 440-page reference corpus not healthy: "+repr(health))
    parent=existing(BRAND)
    if len(parent)!=1 or parent[0].get("link","").rstrip("/")!=BASE+"/car-reference/mg":
        raise RuntimeError("Existing MG brand parent not uniquely verified")
    assert len(ROWS)==5 and len({r["slug"] for r in ROWS})==5
    # Fail before publishing anything if any official photo cannot be verified.
    PRECHECK_PHOTOS=[exact_model_photo(url) for url in PHOTO_URLS[:2*CAP]]
    for i,row in enumerate(ROWS[:CAP]):
        slug=row["slug"]
        kind=row["kind"]
        base=BASE+"/car-reference/mg/"
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
        pair=PRECHECK_PHOTOS[2*i:2*i+2]
        picture=cover(pair,i)
        fname="a3tal-pseo-b40-mg-rx9-phev-real-"+slug+".webp"
        media=post(UPLOAD,{"filename":fname,"image_base64":base64.b64encode(picture).decode(),
                           "convert_webp":False,"title":row["title"],"alt":row["title"]+" - أعطال.كوم"})
        image_id=int(media.get("media_id") or 0)
        if image_id<1 or not str(media.get("url","")).endswith(".webp"):
            raise RuntimeError("Photo upload not verified")
        data={"kind":kind,"market":"Egypt / MG RX9 PHEV 1.5T plug-in hybrid",
              "years":"جدول الفئات الرسمي في مصر؛ مراجعة 2026-11-10",
              "engine":"MG RX9 PHEV 1.5T + 24.7kWh / 295HP / 390Nm / DHT",
              "category":row["category"],"reviewed_at":"2026-11-10",
              "facts":[{"label":f[0],"value":f[1]} for f in row["facts"]],
              "sources":[{"title":"MG Motor Egypt RX9 PHEV Official","url":u} for u in row["sources"]]}
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
                         "image_file":fname,"photo_source_pair":PHOTO_URLS[2*i:2*i+2],"visual_source":"original MG Motor Egypt RX9 PHEV photographic gallery image","status":"published",
                         "og_verified":True,"canonical_verified":True})
        print("BATCH40_PUBLIC_ARTICLE_AND_OG_VERIFIED",url,flush=True)
    after=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    if after.get("drafts")!=0:raise RuntimeError("Unexpected draft count")
    if after.get("published",0)<health["published"]+sum(x["status"]=="published" for x in PROGRESS):
        raise RuntimeError("Published count did not increase")
    print("BATCH40_MG_RX9_PHEV_COMPLETE",len(PROGRESS),after["published"],flush=True)

if __name__=="__main__":
    try:main()
    finally:
        REPORT.write_text(json.dumps({"batch":40,"rows":PROGRESS},ensure_ascii=False,indent=2),"utf-8")
