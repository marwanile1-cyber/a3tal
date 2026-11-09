#!/usr/bin/env python3
"""Batch35: publish five original Geely Emgrand Egypt technical-reference pages.

Only A3tal Direct Bridge and the car-reference importer are used.
Every article gets a separate original WebP technical drawing, not fake photos.
Never overwrite existing posts, verify public canonical and OG.
"""
import base64,hashlib,io,json,os,re,time
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageEnhance,ImageFilter
from html import escape
import requests

ROOT=Path(__file__).resolve().parents[1]
DB=json.loads((ROOT/"data/car-reference/batch-35-geely-emgrand-egypt.json").read_text("utf-8"))
ROWS=DB["rows"]
BASE="https://a3tal.com"
MODEL=DB["model_slug"]
BRAND="geely"
REPORT=ROOT/"reports/batch35-emgrand-live-audit.json"
REPORT.parent.mkdir(parents=True,exist_ok=True)
S=requests.Session()
S.headers.update({"User-Agent":"A3tal-Tech-Reference-Batch35/1.0"})
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY required")
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
ROOT_URL=BASE+"/car-reference/geely/"+MODEL+"/"
CAP=min(len(ROWS),max(1,int(os.environ.get("A3CR_BATCH35_LIMIT","5"))))
LABELS=["MODEL 2026","1.5D ENGINE","6AT NOT CVT","WHEELBASE & TRUNK","SUSPENSION EPB"]
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

def vector_art(index):
    """Create five distinct original model-neutral technical line diagrams."""
    im=Image.new("RGB",(660,520),(19,39,58))
    d=ImageDraw.Draw(im)
    a=ACCENTS[index]
    ink=(217,233,243)
    for x in range(0,660,40):d.line((x,0,x,520),fill=(39,62,78))
    for y in range(0,520,40):d.line((0,y,660,y),fill=(39,62,78))
    d.rounded_rectangle((28,30,632,490),radius=26,outline=a,width=6)
    if index==0:
        d.line([(80,318),(130,240),(215,208),(437,208),(527,294),(578,318)],fill=ink,width=11,joint="curve")
        d.line((80,319,578,319),fill=a,width=10)
        for x in [182,474]:
            d.ellipse((x-57,318,x+57,432),fill=(19,39,58),outline=ink,width=11)
            d.ellipse((x-23,352,x+23,398),outline=a,width=8)
    elif index==1:
        d.rounded_rectangle((89,112,575,386),radius=25,outline=ink,width=9)
        for x in [123,237,351,465]:
            d.rounded_rectangle((x,175,x+75,295),radius=14,outline=a,width=8)
            d.line((x+37,296,x+37,350),fill=ink,width=8)
        d.text((213,423),"1.5 DVVT",font=namefont(34),fill=ink)
    elif index==2:
        for x in [210,450]:
            d.ellipse((x-92,167,x+92,360),outline=a,width=14)
            d.ellipse((x-44,216,x+44,312),outline=ink,width=7)
        d.line((210,168,450,168),fill=ink,width=12)
        d.line((210,360,450,360),fill=ink,width=12)
        d.text((257,412),"CVT",font=namefont(44),fill=ink)
    elif index==3:
        d.line((106,254,550,254),fill=ink,width=10)
        for x in [193,473]:d.ellipse((x-35,270,x+35,340),outline=a,width=9)
        d.line((88,378,570,378),fill=a,width=8)
        for x in [90,568]:d.line((x,360,x,397),fill=a,width=7)
        d.text((233,413),"4532 mm",font=namefont(34),fill=ink)
    else:
        d.line((88,415,583,415),fill=ink,width=12)
        d.line([(136,409),(280,341),(427,409)],fill=a,width=14)
        for j in range(7):
            y=108+j*39
            d.line((305 + (48 if j%2 else -48),y,305 + (-48 if j%2 else 48),y+39),fill=ink,width=10)
        d.text((407,205),"EPS",font=namefont(42),fill=a)
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
    d.text((132,282),"GEELY EMGRAND",font=namefont(64),fill=(251,252,255))
    d.text((134,372),LABELS[index],font=namefont(42),fill=color)
    d.text((134,462),"EGYPT  |  1.5D / 6AT",font=namefont(28),fill=(197,215,229))
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
            r=get(url,params={"a3_batch35_audit":str(time.time_ns())},
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
    if len(parent)!=1 or parent[0].get("link","").rstrip("/")!=BASE+"/car-reference/geely":
        raise RuntimeError("Existing Geely brand parent not uniquely verified")
    assert len(ROWS)==5 and len({r["slug"] for r in ROWS})==5
    for i,row in enumerate(ROWS[:CAP]):
        slug=row["slug"]
        kind=row["kind"]
        base=BASE+"/car-reference/geely/"
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
        im=vector_art(i)
        picture=cover(im,i)
        fname="a3tal-pseo-b35-emgrand-"+slug+".webp"
        media=post(UPLOAD,{"filename":fname,"image_base64":base64.b64encode(picture).decode(),
                           "convert_webp":False,"title":row["title"],"alt":row["title"]+" - أعطال.كوم"})
        image_id=int(media.get("media_id") or 0)
        if image_id<1 or not str(media.get("url","")).endswith(".webp"):
            raise RuntimeError("Photo upload not verified")
        data={"kind":kind,"market":"Egypt / Geely Emgrand 2026 OEM 6AT",
              "years":"المواصفات الرسمية المدققة 2026-11-09",
              "engine":"Geely Emgrand 1.5D 1499cc 120HP 152Nm / 6AT",
              "category":row["category"],"reviewed_at":"2026-11-09",
              "facts":[{"label":f[0],"value":f[1]} for f in row["facts"]],
              "sources":[{"title":"Geely Egypt Emgrand Official","url":u} for u in row["sources"]]}
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
                         "image_file":fname,"visual_source":"original technical vector authored for A3tal","status":"published",
                         "og_verified":True,"canonical_verified":True})
        print("BATCH35_PUBLIC_ARTICLE_AND_OG_VERIFIED",url,flush=True)
    after=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    if after.get("drafts")!=0:raise RuntimeError("Unexpected draft count")
    if after.get("published",0)<health["published"]+sum(x["status"]=="published" for x in PROGRESS):
        raise RuntimeError("Published count did not increase")
    print("BATCH35_GEELY_EMGRAND_COMPLETE",len(PROGRESS),after["published"],flush=True)

if __name__=="__main__":
    try:main()
    finally:
        REPORT.write_text(json.dumps({"batch":33,"rows":PROGRESS},ensure_ascii=False,indent=2),"utf-8")
