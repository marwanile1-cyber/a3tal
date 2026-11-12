#!/usr/bin/env python3
"""Jetour T1 Egypt batch42: five original PSEO technical-reference guides.
Original 2026 Egypt manufacturer 1.5T-7DCT facts, genuine exact-model photos.
GitHub -> A3tal Direct Bridge + reference importer only. Fail closed. No vectors.
"""
import base64,hashlib,io,json,os,re,time
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageEnhance,ImageFilter
import requests
ROOT=Path(__file__).resolve().parents[1]
DB=json.loads((ROOT/"data/car-reference/batch-42-jetour-t1-egypt.json").read_text("utf8"))
ROWS=DB["rows"]
BASE="https://a3tal.com"
MODEL=DB["model_slug"]
BRAND="jetour"
GALLERY="https://jetouregypt.com/models/T1/new_assets/images/carModel/t1/"
PHOTO_GROUPS=[
 ["7_1.jpg"],["5-2.jpg"],["5-3.jpg"],["5-4.jpg"],
 ["4-1.jpg","4-2.jpg","7_2.jpg"]
]
DIM={"7_1.jpg":(1920,960),"5-2.jpg":(1920,1036),"5-3.jpg":(1920,1036),"5-4.jpg":(1920,1036),
     "4-1.jpg":(854,350),"4-2.jpg":(854,350),"7_2.jpg":(454,875)}
REPORT=ROOT/"reports/batch42-jetour-t1-live-audit.json"
REPORT.parent.mkdir(exist_ok=True,parents=True)
S=requests.Session()
S.headers.update({"User-Agent":"A3tal-PSEO-T1-Batch42/1.0"})
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3tal Bridge API secret unavailable")
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
ROOT_URL=BASE+"/car-reference/jetour/"+MODEL+"/"
CAP=min(len(ROWS),max(1,int(os.environ.get("A3CR_BATCH42_LIMIT","5"))))
PROGRESS=[]

def get(url,**kw):
    for n in range(4):
        try:
            r=S.get(url,timeout=80,**kw)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if n==3:raise
            time.sleep(3*(n+1))

def post(url,payload):
    for n in range(4):
        try:
            r=S.post(url,json=payload,headers=HEAD,timeout=210)
            if r.status_code>=500:raise requests.RequestException("Transient "+str(r.status_code))
            if not r.ok:raise RuntimeError("Bridge HTTP "+str(r.status_code)+" "+r.text[:400])
            return r.json()
        except requests.RequestException:
            if n==3:raise
            time.sleep(4*(n+1))

def existing(slug):
    r=get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":20})
    return [p for p in r.json() if p.get("slug")==slug and p.get("status")=="publish"]

def read_real_photo(name):
    if name not in DIM:raise RuntimeError("Image not in verified official Jetour T1 gallery "+name)
    url=GALLERY+name
    raw=get(url).content
    if len(raw)<45000:raise RuntimeError("Source photograph too small "+url)
    with Image.open(io.BytesIO(raw)) as origin:
        origin.load()
        im=origin.convert("RGB")
    if im.size!=DIM[name]:raise RuntimeError("Actual model photo dimensions changed "+name+" "+str(im.size))
    print("EXACT_JETOUR_T1_OEM_PHOTO",name,im.size,hashlib.sha256(raw).hexdigest()[:12],flush=True)
    return im

def editorial_photo(group,index):
    """1600x900 WebP from sharp native factory photos; backdrop only may be blurred."""
    W,H=1600,900
    if index<4:
        if len(group)!=1:raise RuntimeError("Invalid one-photo cover")
        photo=group[0]
        if photo.width<1800 or photo.height<900:raise RuntimeError("Low-quality main T1 photo")
        base=ImageOps.fit(photo,(W,H),method=Image.Resampling.LANCZOS)
        base=ImageEnhance.Brightness(base.filter(ImageFilter.GaussianBlur(28))).enhance(.74)
        foreground=ImageOps.contain(photo,(min(W,photo.width),min(H,photo.height)),method=Image.Resampling.LANCZOS)
        if foreground.width>photo.width or foreground.height>photo.height:
            raise RuntimeError("Refusing to upscale car source")
        base.paste(foreground,((W-foreground.width)//2,(H-foreground.height)//2))
    else:
        if len(group)!=3:raise RuntimeError("Three different official T1 photos are required")
        left1,left2,portrait=group
        if left1.size!=(854,350) or left2.size!=(854,350) or portrait.size!=(454,875):
            raise RuntimeError("No source upscale permitted for Jetour original-photo collage")
        base=ImageOps.fit(left1,(W,H),method=Image.Resampling.LANCZOS)
        base=ImageEnhance.Brightness(base.filter(ImageFilter.GaussianBlur(38))).enhance(.47)
        base.paste(left1,(28,83))
        base.paste(left2,(28,450))
        base.paste(portrait,(1023,12))
    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    d.rounded_rectangle((1382,837,1575,874),radius=8,fill=(11,29,40,160))
    fp="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if Path(fp).is_file():
        d.text((1401,842),"A3TAL.COM",font=ImageFont.truetype(fp,20),fill=(255,255,255,245))
    final=Image.alpha_composite(base.convert("RGBA"),overlay).convert("RGB")
    buff=io.BytesIO()
    final.save(buff,"WEBP",quality=90,method=6)
    binary=buff.getvalue()
    if len(binary)<16000 or binary[:4]!=b"RIFF" or binary[8:12]!=b"WEBP":
        raise RuntimeError("Actual automotive photograph WebP verification failed")
    return binary

def live_qa(url,title,imagefile):
    reason=""
    for n in range(8):
        try:
            r=get(url,params={"batch42_check":str(time.time_ns())},headers={"Cache-Control":"no-cache"})
            h=r.text
            if r.url.split("?")[0].rstrip("/")!=url.rstrip("/"):raise RuntimeError("Unexpected URL redirect")
            if title not in h:raise RuntimeError("Article title not visible")
            if imagefile not in h:raise RuntimeError("Uploaded OEM photo not visible")
            og=re.search(r'<meta[^>]+property=["\\\']og:image["\\\'][^>]*>',h,re.I)
            if not og or imagefile not in og.group(0):raise RuntimeError("Wrong og:image")
            canonical=re.search(r'<link[^>]+rel=["\\\']canonical["\\\'][^>]*>',h,re.I)
            if not canonical or url.rstrip("/") not in canonical.group(0):
                raise RuntimeError("Wrong canonical URL")
            if re.search(r'<meta[^>]+name=["\\\']robots["\\\'][^>]*noindex',h[:24000],re.I):
                raise RuntimeError("Page is noindex")
            return True
        except Exception as err:
            reason=str(err)
            time.sleep(3)
    raise RuntimeError("Public 200 and Yoast QA failed "+url+" "+reason)

def main():
    if DB.get("batch")!=42 or DB.get("brand")!="jetour" or MODEL!="t1-15t-7dct-egypt-2026":
        raise RuntimeError("Wrong model/batch metadata")
    if len(ROWS)!=5 or len({r["slug"] for r in ROWS})!=5:
        raise RuntimeError("Exactly five original PSEO intents required")
    health=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    if not health.get("ok") or health.get("published",0)<450:
        raise RuntimeError("Previously published 450-page corpus not healthy")
    parent=existing(BRAND)
    if len(parent)!=1 or parent[0].get("link","").rstrip("/")!=BASE+"/car-reference/jetour":
        raise RuntimeError("Jetour brand archive is not verified")
    # Every original photo is preflight checked before even one media upload.
    photo_groups=[[read_real_photo(name) for name in g] for g in PHOTO_GROUPS[:CAP]]
    print("JETOUR_T1_SEVEN_EXACT_EGYPT_OEM_IMAGES_VALIDATED",len(photo_groups),flush=True)
    for i,row in enumerate(ROWS[:CAP]):
        kind=row["kind"]
        slug=row["slug"]
        url=BASE+"/car-reference/jetour/"+(slug+"/" if kind=="model" else MODEL+"/"+slug+"/")
        pre=existing(slug)
        if pre:
            if len(pre)!=1 or pre[0].get("link","").rstrip("/")!=url.rstrip("/"):
                raise RuntimeError("Slug collision on existing technical-reference record "+slug)
            print("T1_ALREADY_PUBLISHED",url,flush=True)
            PROGRESS.append({"slug":slug,"url":url,"status":"existing"})
            continue
        if kind=="spec":
            model=existing(MODEL)
            if len(model)!=1 or model[0].get("link","").rstrip("/")!=ROOT_URL.rstrip("/"):
                raise RuntimeError("Exact T1 model hub was not published")
        cover=editorial_photo(photo_groups[i],i)
        fname="a3tal-pseo-b42-jetour-t1-real-"+slug+".webp"
        media=post(UPLOAD,{"filename":fname,"image_base64":base64.b64encode(cover).decode(),
                          "convert_webp":False,"title":row["title"],"alt":row["title"]+" - أعطال.كوم"})
        media_id=int(media.get("media_id") or 0)
        if media_id<1 or not media.get("url","").endswith(".webp"):
            raise RuntimeError("OEM featured photo attachment was not confirmed")
        structured={"kind":kind,"market":"Egypt / Jetour T1 1.5T / 7DCT FWD, July 2026",
            "years":"مواصفات الوكيل المصري إصدار يوليو 2026، مراجعة 2026-11-12",
            "engine":"Jetour T1 1.5T / 184HP / 290Nm / 7DCT FWD",
            "category":row["category"],"reviewed_at":"2026-11-12",
            "facts":[{"label":a,"value":b} for a,b in row["facts"]],
            "sources":[{"title":"Jetour Egypt official July 2026","url":link} for link in row["sources"]]}
        payload={"kind":kind,"slug":slug,"title":row["title"],
            "parent_path":BRAND if kind=="model" else BRAND+"/"+MODEL,
            "featured_image_id":media_id,"status":"publish",
            "content":row["rich_html"],"excerpt":row["meta_description"],
            "meta_title":row["title"]+" | أعطال.كوم",
            "meta_description":row["meta_description"],"data":structured}
        result=post(UPSERT,{"items":[payload]})
        outcome=result.get("results") or []
        if len(outcome)!=1 or not outcome[0].get("ok") or outcome[0].get("status")!="publish":
            raise RuntimeError("Car-reference Bridge publish failed "+repr(result)[:500])
        if outcome[0].get("url","").rstrip("/")!=url.rstrip("/"):
            raise RuntimeError("Unexpected nested permalink "+repr(outcome))
        live_qa(url,row["title"],fname)
        PROGRESS.append({"slug":slug,"url":url,"status":"published","photo_urls":[GALLERY+name for name in PHOTO_GROUPS[i]],"featured_image":media["url"],"canonical_verified":True,"og_verified":True})
        print("BATCH42_T1_PUBLIC_ARTICLE_OG_CANONICAL_PASSED",url,flush=True)
    after=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    if after.get("drafts")!=0:raise RuntimeError("New drafts unexpectedly present")
    if after.get("published",0)<health["published"]+sum(x["status"]=="published" for x in PROGRESS):
        raise RuntimeError("Car-reference live count did not increase as expected")
    print("BATCH42_JETOUR_T1_2026_PUBLISHED",len(PROGRESS),after["published"],flush=True)

if __name__=="__main__":
    try:main()
    finally:
        REPORT.write_text(json.dumps({"batch":42,"rows":PROGRESS},ensure_ascii=False,indent=2),"utf8")
