#!/usr/bin/env python3
"""Publish Nissan Sunny N17 Egypt car reference pages under WordPress.

Only verified figures from Nissan Egypt. The page that would cannibalise an
existing Nissan transmission guide is intentionally absent. Uses original
editorial layouts composed from a vehicle photo previously uploaded to the
user's own a3tal.com media library. These images are not new ImageGen photos.
"""
import base64,io,json,os,re,time
from html import escape
from pathlib import Path

import requests
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageFilter

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"data/car-reference/batch-06-nissan-sunny-n17-egypt-20261103.json").read_text(encoding="utf8"))
BASE="https://a3tal.com"
AUTH={"X-A3tal-Key":os.environ["A3TAL_API_KEY"],"Content-Type":"application/json"}
S=requests.Session()
S.headers["User-Agent"]="A3tal-Nissan-Sunny-N17-Reference-20261103/1.0"
POST_URL=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
MEDIA_URL=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
OUT=ROOT/"sunny-n17-batch06-result.json"
DONE=[]
BRAND=DATA["brand"]; MODEL=DATA["model"]
QUEUE=[("brand",BRAND,""),("model",MODEL,"nissan")]+[("spec",row,"nissan/sunny-n17-egypt") for row in DATA["items"]]
COLORS={"brand":(47,175,219),"model":(71,189,212),"tire-specs":(48,191,161),"engine-specs":(72,153,230),"dimensions":(233,150,69)}
TOPICS={"tire-specs":"مقاس كاوتش نيسان صني","engine-specs":"بيانات محرك 1.5","dimensions":"خزان الوقود والأبعاد"}
assert len(DATA["items"])==3 and len(QUEUE)==5
assert DATA["intent_collision_excluded"][0]["slug"]=="sunny-n17-manual-vs-auto-egypt"

def f(size,arabic=False):
    names=(["/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        if arabic else ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"])
    for path in names:
        if Path(path).is_file():return ImageFont.truetype(path,size)
    raise RuntimeError("Font unavailable")

def get(url,**kwargs):
    for k in range(3):
        try:
            r=S.get(url,timeout=50,**kwargs)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if k==2:raise
            time.sleep(3+k*3)

def post(url,body):
    for k in range(4):
        try:
            r=S.post(url,json=body,headers=AUTH,timeout=145)
            if r.status_code>=500:raise requests.RequestException("Server HTTP "+str(r.status_code))
            if not r.ok:raise RuntimeError("HTTP "+str(r.status_code)+" "+r.text[:250])
            return r.json()
        except requests.RequestException:
            if k==3:raise
            time.sleep(3+3*k)

def current(slug):
    data=get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":20}).json()
    return [x for x in data if x.get("slug")==slug and x.get("status")=="publish"]

def photo():
    x=DATA["image_source"]
    urls=[x["preferred"],x["fallback"],x["fallback_2"]]
    for url in urls:
        try:
            rr=get(url,headers={"Accept":"image/webp,image/jpeg,image/png,*/*"})
            if len(rr.content)<20000:raise RuntimeError("Source filesize")
            im=Image.open(io.BytesIO(rr.content)).convert("RGB")
            if im.width<950 or im.height<550:raise RuntimeError("Image dimension "+str(im.size))
            print("NISSAN OWNED PHOTO",url,"resolution",im.size,flush=True)
            return im,url
        except Exception as e:
            print("Photo rejected",url,str(e)[:160],flush=True)
    raise RuntimeError("No verified Nissan photo. No publishing.")

def cover(master,kind,row,i):
    label=row["title"]
    metric=(
      "NISSAN" if kind=="brand" else
      "SUNNY N17" if kind=="model" else row["metric"]
    )
    detail=(
      "SERVICE REFERENCE" if kind=="brand" else
      "EGYPT  /  OFFICIAL DATA" if kind=="model" else row["subtitle"]
    )
    accent=COLORS[row.get("category",kind)]
    im=Image.new("RGB",(1600,900),(7,20,34))
    crop=(0.43,0.48) if i%2 else (0.50,0.53)
    main=ImageOps.fit(master,(1480,900),method=Image.Resampling.LANCZOS,centering=crop)
    main=main.filter(ImageFilter.UnsharpMask(radius=1.4,percent=135,threshold=3))
    im.paste(main,(-210+(i%3)*48,0))
    layer=Image.new("RGBA",im.size,(0,0,0,0))
    painter=ImageDraw.Draw(layer)
    for x in range(450,1600,3):
        alpha=min(255,int(22+(x-450)*230/1150))
        painter.rectangle((x,0,x+3,900),fill=(3,15,30,alpha))
    painter.rectangle((0,0,1600,98),fill=(4,13,25,232))
    painter.rectangle((0,822,1600,900),fill=(4,13,25,240))
    painter.rounded_rectangle((960,275,1542,695),radius=30,fill=(12,30,48,232),outline=(*accent,245),width=4)
    painter.rectangle((968,211,1535,219),fill=(*accent,230))
    for radius in (60,90,120):
        painter.ellipse((1390-radius,760-radius,1390+radius,760+radius),outline=(*accent,25),width=2)
    c=Image.alpha_composite(im.convert("RGBA"),layer)
    d=ImageDraw.Draw(c)
    d.text((73,54),"A3TAL  /  NISSAN SUNNY N17",font=f(26),fill=(231,243,251))
    d.text((1500,408),metric,font=f(60 if len(metric)>11 else 86),anchor="ra",fill=(249,251,253))
    d.text((1490,516),detail[:27],font=f(27),anchor="ra",fill=accent)
    topic=TOPICS.get(row.get("category"),"المواصفات الفنية الرسمية")
    d.text((1492,618),topic,font=f(31,True),anchor="ra",direction="rtl",fill=(219,235,244))
    d.text((1500,869),"A3TAL.COM",font=f(27),anchor="ra",fill=(226,240,249))
    out=io.BytesIO()
    c.convert("RGB").save(out,"WEBP",quality=89,method=5)
    if out.tell()<60000:raise RuntimeError("Too small photo output")
    return out.getvalue()

def content(kind,row):
    if kind=="brand":
        return (
          "<p>يجمع دليل المواصفات الفنية لنيسان في أعطال.كوم المعلومات التي يحتاجها مالك السيارة عند اختيار الإطارات وفهم المحرك والأبعاد وقطع الصيانة. "
          "نبدأ بنيسان صني N17 المنتشرة في مصر، مع إسناد الأرقام المنشورة إلى صفحة نيسان مصر بدل استخدام أرقام من كتالوجات أسواق أخرى.</p>"
          "<h2>الموديلات المتاحة في الدليل</h2>"
          "<p>ابدأ من <a href='https://a3tal.com/car-reference/nissan/sunny-n17-egypt/'>دليل نيسان صني N17 في مصر</a>، "
          "ثم اختر المقاس أو بيانات المحرك أو السعات المطلوبة. عند اختلاف سنة الإنتاج أو فئة السيارة يجب التأكد من رقم الشاسيه والكتالوج الخاص بها.</p>"
          "<h2>ما الفرق بين دليل المواصفات وصفحات الأعطال؟</h2>"
          "<p>هذا القسم يشرح الأرقام والمقاسات المطلوبة قبل الشراء أو الصيانة؛ أما تشخيص النتشة والأكواد والأعراض "
          "فيُراجع عبر <a href='https://a3tal.com/nissan-sunny-gearbox-problems-guide/'>دليل فتيس نيسان صني</a> "
          "والأقسام المتخصصة الأخرى. لا نكرر شرح الأعطال في صفحات المقاسات.</p>"
        )
    if kind=="model":
        return (
          "<p>هذه الصفحة المرجعية لسيارات نيسان صني N17 المعروضة في السوق المصري. تعرض نيسان مصر محركًا سعة 1498 سم³، "
          "مع خيار يدوي وفئات أوتوماتيك تقليدية أربع سرعات ومقاس كاوتش 185/65 R15، وتوضح الأبعاد وسعة خزان الوقود والشنطة.</p>"
          "<h2>اختيار المعلومة المناسبة</h2>"
          "<p>تختلف فئات صني في التجهيزات ونوع الجنط وناقل الحركة. اختر البيانات من الصفحة الفنية المتخصصة، "
          "ولا تنسَ أن الفئة والجيل والسوق وسنة الإنتاج قد تغيّر بعض البنود. الأرقام المحلية من صفحة نيسان مصر "
          "هي نقطة البداية، بينما ملصقات السيارة ودليل المالك المرجع النهائي في إجراءات الصيانة.</p>"
          "<h2>معلومات الفتيس وأسعار السيارة</h2>"
          "<p>لأن الموقع يحتوي بالفعل على <a href='https://a3tal.com/nissan-sunny-gearbox-problems-guide/'>"
          "شرح مستقل لنوع فتيس صني ومشكلاته</a>، لا نعيد إنشاء صفحة بنفس نية البحث داخل هذا الدليل. "
          "محتوى هذا القسم يركز على المقاسات والسعات، بينما أسعار الفئات والمراجعات لها صفحاتها الحالية.</p>"
        )
    return (
       "<p>"+escape(row["intro"])+"</p>"
       "<h2>شرح القيم المنشورة من نيسان مصر</h2><p>"+escape(row["detail"])+"</p>"
       "<h2>ما الذي يجب مطابقته قبل الشراء أو الصيانة؟</h2>"
       "<p>"+escape(row["warning"])+"</p>"
       "<h2>نطاق هذه المواصفات</h2>"
       "<p>المعلومات تخص صني N17 كما ترد في صفحة الإصدارات والمواصفات الخاصة بنيسان مصر، ولا يُفترض مطابقتها "
       "لصني N16 الأقدم أو سيارات نيسان أخرى أو نسخ صني الموردة لأسواق خارج مصر. عند شراء قطعة غيار، "
       "استعن برقم الشاسيه ومقاس القطعة الأصلي بدل الاعتماد على اسم السيارة وحده.</p>"
       "<p>المرجع الأصلي: <a href='"+escape(row["source"],quote=True)+
       "' rel='noopener nofollow noreferrer'>نيسان مصر - مواصفات صني الرسمية</a>.</p>"
    )

def entry(kind,row,parent,media):
    source=(DATA["sources"][0] if kind!="spec" else row["source"])
    data={"kind":kind,"market":"مصر - بيانات نيسان مصر الرسمية",
       "years":"الجيل N17، راجع سنة إنتاج السيارة", "engine":row.get("engine",""),
       "category":row.get("category",""),"reviewed_at":"2026-11-03",
       "facts":[{"label":a,"value":b} for a,b in row.get("facts",[])],
       "sources":[{"title":"صفحة نيسان مصر: إصدارات صني ومواصفاتها","url":source}]}
    return {
       "title":row["title"],"slug":row["slug"],"kind":kind,"parent_path":parent,
       "featured_image_id":media,"status":"publish","data":data,
       "content":content(kind,row),
       "excerpt":"بيانات صني N17 الفنية من نيسان مصر، وفق الفئة المحلية مع التنبيه لاختلاف سنة الإنتاج.",
       "meta_title":row["title"]+" | أعطال.كوم",
       "meta_description":("تعرف على "+row["title"]+" بالرجوع إلى بيانات نيسان مصر الرسمية، مع شرح الفروق والنصائح اللازمة قبل صيانة السيارة.")[:155]
    }

def verify(url,name,title):
    for k in range(6):
        try:
            rr=get(url,params={"sunny_quality_check":str(time.time_ns())},
                headers={"Cache-Control":"no-cache"})
            if rr.url.split("?")[0].rstrip("/")!=url.rstrip("/"):raise RuntimeError("redirect")
            html=rr.text
            if title not in html:raise RuntimeError("title")
            if name not in html:raise RuntimeError("featured image missing")
            og=re.search(r'<meta[^>]*property=["\x27]og:image["\x27][^>]*content=["\x27]([^"\x27]+)',html,re.I)
            if not og or name not in og.group(1):raise RuntimeError("og:image")
            ca=re.search(r'<link[^>]*rel=["\x27]canonical["\x27][^>]*href=["\x27]([^"\x27]+)',html,re.I)
            if not ca or ca.group(1).rstrip("/")!=url.rstrip("/"):raise RuntimeError("canonical")
            if "noindex" in html[:14000].lower():raise RuntimeError("noindex")
            return
        except Exception as e:
            if k==5:raise RuntimeError("Live QA "+url+" "+str(e))
            time.sleep(3)

def main():
    assert len(QUEUE)==5
    count=max(1,min(5,int(os.getenv("A3CR_LIMIT","1"))))
    master,source=photo()
    print("Pilot cap",count,"source",source,flush=True)
    try:
        for i,(kind,row,parent) in enumerate(QUEUE[:count]):
            slug=row["slug"]
            path=(parent+"/"+slug).strip("/")
            url=BASE+"/car-reference/"+path+"/"
            old=current(slug)
            if old:
                if len(old)!=1 or old[0]["link"].rstrip("/")!=url.rstrip("/"):
                    raise RuntimeError("Slug collision "+slug)
                DONE.append({"slug":slug,"url":url,"status":"existing"})
                print("SKIP live",url,flush=True)
                continue
            art=cover(master,kind,row,i)
            fn="a3tal-sunny-n17-editorial-"+slug+".webp"
            m=post(MEDIA_URL,{"filename":fn,"image_base64":base64.b64encode(art).decode("ascii"),
                "title":row["title"],"alt":row["title"]+" - تصميم تحريري لأعطال.كوم",
                "convert_webp":False})
            photoid=int(m.get("media_id") or 0)
            if not photoid:raise RuntimeError("No uploaded media id")
            payload=entry(kind,row,parent,photoid)
            try:
                res=post(POST_URL,{"items":[payload]})
            except requests.RequestException:
                # No duplicate after uncertain connection reset.
                old=current(slug)
                if len(old)==1 and old[0]["link"].rstrip("/")==url.rstrip("/"):
                    res={"results":[{"ok":True,"url":url,"status":"publish","id":old[0]["id"]}]}
                else:res=post(POST_URL,{"items":[payload]})
            records=res.get("results") or []
            if len(records)!=1 or not records[0].get("ok") or records[0].get("status")!="publish":
                raise RuntimeError("Rejected WordPress record "+slug+" "+str(records)[:270])
            if records[0].get("url","").rstrip("/")!=url.rstrip("/"):
                raise RuntimeError("WordPress permalink mismatch "+slug)
            verify(url,fn,row["title"])
            DONE.append({"slug":slug,"url":url,"status":"published",
                  "photo_id":photoid,"photo_url":m.get("url"),"verified":True})
            print("LIVE VERIFIED",url,"image_id",photoid,flush=True)
    finally:
        OUT.write_text(json.dumps({"image_master":source,"records":DONE},ensure_ascii=False,indent=2),encoding="utf8")
    assert len(DONE)==count
    print("COMPLETE",len(DONE),flush=True)

if __name__=="__main__": main()
