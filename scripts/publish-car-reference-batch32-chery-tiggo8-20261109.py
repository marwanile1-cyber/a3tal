#!/usr/bin/env python3
"""Batch32: publish five original Chery Tiggo 8 Egypt technical-reference pages.

Only A3tal Direct Bridge and a3tal-car-reference importer are used.
No updates to existing posts, no counterfeit workshop specifications.
Each page gets a distinct original 1600x900 infographic composition based
on official Chery Egypt media, with OG, canonical, indexability verified.
"""
import base64,hashlib,io,json,os,re,time
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageEnhance,ImageFilter
from html import escape
import requests

ROOT=Path(__file__).resolve().parents[1]
DB=json.loads((ROOT/"data/car-reference/batch-32-chery-tiggo8-egypt.json").read_text("utf-8"))
ROWS=DB["rows"]
BASE="https://a3tal.com"
MODEL=DB["model_slug"]
BRAND="chery"
REPORT=ROOT/"reports/batch32-tiggo8-live-audit.json"
REPORT.parent.mkdir(parents=True,exist_ok=True)
S=requests.Session()
S.headers.update({"User-Agent":"A3tal-Tech-Reference-Batch32/1.0"})
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY required")
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
ROOT_URL=BASE+"/car-reference/chery/"+MODEL+"/"
CAP=min(len(ROWS),max(1,int(os.environ.get("A3CR_BATCH32_LIMIT","5"))))
LABELS=["MODEL OVERVIEW","1.5T ENGINE","6DCT WET","DIMENSIONS","SUSPENSION"]
ACCENTS=[(26,156,211),(227,85,44),(92,179,177),(175,124,211),(224,166,49)]
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

def photograph(url):
    if not url.startswith("https://www.chery-eg.com/media/"):
        raise ValueError("Photo is not from audited Egyptian manufacturer host")
    raw=get(url).content
    if len(raw)<9000:raise RuntimeError("Source photo too small "+url)
    im=Image.open(io.BytesIO(raw)).convert("RGB")
    if max(im.size)<450 or min(im.size)<260:raise RuntimeError("Source photo dimensions too small "+str(im.size))
    return im

def cover(im,index):
    W,H=1600,900
    color=ACCENTS[index]
    c=Image.new("RGB",(W,H),(11,27,45))
    d=ImageDraw.Draw(c)
    # Exclusive editorial geometry and diagram elements, not a fake model photo.
    for y in range(H):
        k=y/H
        d.line((0,y,W,y),fill=(int(10+13*k),int(24+15*k),int(43+19*k)))
    for x in range(0,W,80):
        d.line((x,0,x,H),fill=(28,47,64),width=1)
    for y in range(0,H,80):
        d.line((0,y,W,y),fill=(28,47,64),width=1)
    d.rounded_rectangle((48,50,1550,849),radius=33,outline=(69,97,117),width=3)
    d.rounded_rectangle((67,75,1532,822),radius=27,fill=(17,37,57))
    d.rounded_rectangle((840,115,1500,760),radius=28,fill=(27,49,70))
    photo=ImageOps.contain(im,(625,520),method=Image.Resampling.LANCZOS)
    if photo.width<400:
        photo=photo.resize((min(620,int(photo.width*1.5)),min(480,int(photo.height*1.5))),Image.Resampling.LANCZOS)
    offset=(852+(640-photo.width)//2,155+(535-photo.height)//2)
    c.paste(photo,offset)
    d=ImageDraw.Draw(c)
    d.rectangle((88,126,99,743),fill=color)
    d.text((135,145),"A3TAL.COM  /  TECHNICAL REFERENCE",font=namefont(23),fill=(210,228,240))
    d.text((132,282),"CHERY TIGGO 8",font=namefont(64),fill=(251,252,255))
    d.text((134,372),LABELS[index],font=namefont(42),fill=color)
    d.text((134,462),"EGYPT  |  1.5T / 6DCT",font=namefont(28),fill=(197,215,229))
    for i in range(5):
        y=596+i*31
        d.rounded_rectangle((138+i*78,y,192+i*78,y+8),radius=4,fill=color if i<=index else (83,102,121))
    d.text((132,777),"SOURCE-VERIFIED  •  2026",font=namefont(19),fill=(191,211,227))
    out=io.BytesIO()
    c.save(out,"WEBP",quality=88,method=6)
    data=out.getvalue()
    if len(data)<18000 or data[:4]!=b"RIFF" or data[8:12]!=b"WEBP":
        raise RuntimeError("Generated cover failed quality gate")
    return data

def audit_live(url,title,image):
    error=None
    for attempt in range(7):
        try:
            r=get(url,params={"a3_batch32_audit":str(time.time_ns())},
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
    if not health.get("ok") or health.get("published",0)<400:
        raise RuntimeError("Existing 400 page reference corpus not healthy: "+repr(health))
    parent=existing(BRAND)
    if len(parent)!=1 or parent[0].get("link","").rstrip("/")!=BASE+"/car-reference/chery":
        raise RuntimeError("Existing Chery brand parent not uniquely verified")
    assert len(ROWS)==5 and len({r["slug"] for r in ROWS})==5
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
        im=photograph(row["image"])
        picture=cover(im,i)
        fname="a3tal-pseo-b32-tiggo8-"+slug+".webp"
        media=post(UPLOAD,{"filename":fname,"image_base64":base64.b64encode(picture).decode(),
                           "convert_webp":False,"title":row["title"],"alt":row["title"]+" - أعطال.كوم"})
        image_id=int(media.get("media_id") or 0)
        if image_id<1 or not str(media.get("url","")).endswith(".webp"):
            raise RuntimeError("Photo upload not verified")
        data={"kind":kind,"market":"Egypt / Chery GB Auto official Tiggo 8 base model",
              "years":"المواصفات الرسمية المدققة 2026-11-09",
              "engine":"Chery Tiggo 8 base 1.5T / 6 speed Wet DCT",
              "category":row["category"],"reviewed_at":"2026-11-09",
              "facts":[{"label":f[0],"value":f[1]} for f in row["facts"]],
              "sources":[{"title":"Chery Egypt Tiggo 8 Official","url":u} for u in row["sources"]]}
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
                         "image_file":fname,"photo_source":row["image"],"status":"published",
                         "og_verified":True,"canonical_verified":True})
        print("BATCH32_PUBLIC_ARTICLE_AND_OG_VERIFIED",url,flush=True)
    after=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    if after.get("drafts")!=0:raise RuntimeError("Unexpected draft count")
    if after.get("published",0)<health["published"]+sum(x["status"]=="published" for x in PROGRESS):
        raise RuntimeError("Published count did not increase")
    print("BATCH32_CHERY_TIGGO8_COMPLETE",len(PROGRESS),after["published"],flush=True)

if __name__=="__main__":
    try:main()
    finally:
        REPORT.write_text(json.dumps({"batch":32,"rows":PROGRESS},ensure_ascii=False,indent=2),"utf-8")
