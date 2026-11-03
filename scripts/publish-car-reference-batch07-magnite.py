#!/usr/bin/env python3
"""Publish Nigerian? No: Nissan Magnite 2026 Egypt technical car references.

Only Nissan Egypt's configurator figures, with a market-specific 36 litre
fuel tank. Existing Magnite price, CVT and fluid articles are not duplicated. Uses original
editorial layouts composed from a vehicle photo previously uploaded to the
user's own a3tal.com media library. These images are not new ImageGen photos.
"""
import base64,io,json,os,re,time
from html import escape
from pathlib import Path

import requests
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageFilter

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"data/car-reference/batch-07-nissan-magnite-egypt-20261103.json").read_text(encoding="utf8"))
BASE="https://a3tal.com"
AUTH={"X-A3tal-Key":os.environ["A3TAL_API_KEY"],"Content-Type":"application/json"}
S=requests.Session()
S.headers["User-Agent"]="A3tal-Nissan-Magnite-Egypt-Reference-20261103/1.0"
POST_URL=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
MEDIA_URL=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
OUT=ROOT/"magnite-batch07-result.json"
DONE=[]
MODEL=DATA["model"]
QUEUE=[("model",MODEL,"nissan")]+[("spec",row,"nissan/"+MODEL["slug"]) for row in DATA["items"]]
COLORS={"model":(71,189,212),"tire-specs":(48,191,161),"engine-specs":(72,153,230),"dimensions":(233,150,69)}
TOPICS={"tire-specs":"مقاسات إطارات ماجنايت","engine-specs":"محرك ماجنايت 1.0 تيربو","dimensions":"خزان الوقود والأبعاد"}
assert len(DATA["items"])==3 and len(QUEUE)==4
assert DATA["brand_existing"]=="nissan"
assert "فتيس CVT ماجنايت واعتماديته" in DATA["nonduplication"]["excluded"]

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
    x=DATA["photo_source"]
    urls=[x["preferred"],x["fallback"]]
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
      "MAGNITE" if kind=="model" else row["metric"]
    )
    detail=(
      "EGYPT  /  1.0 TURBO CVT" if kind=="model" else row["subtitle"]
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
    d.text((73,54),"A3TAL  /  NISSAN MAGNITE",font=f(26),fill=(231,243,251))
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
    if kind=="model":
        return (
          "<p>يقدم دليل نيسان ماجنايت 2026 مواصفات نسخة 1.0 تيربو CVT المعروضة رسميًا في مصر، "
          "وليس بيانات محرك طبيعي السحب أو ناقل يدوي من أسواق أخرى. تعرض الصفحات المرتبطة الإطارات "
          "ومواصفات المحرك وسعات الوقود والأمتعة والأبعاد مع مصدر الشركة المصرية لكل رقم.</p>"
          "<h2>تجهيزات النسخة المصرية</h2>"
          "<p>تعرض نيسان مصر محرك 999 سم³ تيربو بقوة 74 كيلوواط وعزم 152 نيوتن متر، "
          "ودفعًا أماميًا مع CVT، ومقاس كاوتش 195/60R16. الاختلاف بين الفئات قد يشمل نوع الجنط "
          "وبعض تجهيزات الأمان والإضاءة والمقصورة، ولذلك لا نفترض تطابق كل التجهيزات.</p>"
          "<h2>لماذا تختلف سعة خزان الوقود عن أرقام متداولة؟</h2>"
          "<p>في مُهيّئ ماجنايت الخاص بنيسان مصر تظهر سعة الخزان 36 لترًا والطول 3999 مم؛ "
          "وتذكر نشرات لأسواق أخرى سعات وأبعادًا مختلفة. نلتزم هنا ببيانات السوق المصري "
          "وننصح بالرجوع إلى كتيب السيارة الأصلي إذا اختلفت سنة الإنتاج.</p>"
          "<h2>مقالات أخرى بدون تكرار نية البحث</h2>"
          "<p>معلومات أسعار وتوافر السيارة موجودة في <a href='https://a3tal.com/nissan-magnite-price-egypt/'>مقال الأسعار</a>، "
          "ومعلومات الاعتمادية في <a href='https://a3tal.com/nissan-magnite-cvt-turbo-reliability/'>دليل فتيس CVT والتيربو</a>. "
          "هذه الصفحة مخصصة للأرقام الفنية وليست بديلًا عن تلك المقالات.</p>"
        )
    extra=(
       "<p>توضيح بخصوص اختلاف الأسواق: قد تجد رقم خزان 40 لترًا في كتالوج نيسان بدولة أخرى، "
       "لكن البيانات المنشورة هنا من مُهيّئ نيسان مصر الذي يذكر 36 لترًا.</p>"
       if row["category"]=="dimensions" else ""
    )
    return (
       "<p>"+escape(row["intro"])+"</p>"
       "<h2>شرح القيم المنشورة من نيسان مصر</h2><p>"+escape(row["detail"])+"</p>"
       "<h2>ما الذي يجب مطابقته قبل شراء القطعة أو إجراء الصيانة؟</h2>"
       "<p>"+escape(row["warning"])+"</p>"
       +extra+
       "<h2>ما الفرق بين هذه الصفحة ودليل الصيانة؟</h2>"
       "<p>الجدول يشرح القيم الخاصة بسيارات ماجنايت في التكوين المصري المعروض رسميًا، "
       "ولا يعني أن أي نسخة مستوردة من سوق مختلف لها نفس التجهيزات. عند شراء إطار أو قطع غيار "
       "أو تغيير سائل، راجع ملصق السيارة ورقم الشاسيه ودليل المالك الأصلي.</p>"
       "<p>المرجع: <a href='"+escape(row["source"],quote=True)+
       "' rel='noopener nofollow noreferrer'>مُهيّئ نيسان ماجنايت الرسمي في مصر</a>.</p>"
    )

def entry(kind,row,parent,media):
    source=DATA["sources"][0] if kind=="model" else row["source"]
    data={"kind":kind,"market":"نيسان مصر - نسخة ماجنايت 1.0 تيربو CVT",
       "years":"2026","engine":row.get("engine","1.0 Turbo CVT 2WD"),
       "category":row.get("category",""),"reviewed_at":"2026-11-03",
       "facts":[{"label":a,"value":b} for a,b in row.get("facts",[])],
       "sources":[{"title":"مواصفات نيسان ماجنايت الرسمية - مهيّئ نيسان مصر","url":source}]}
    return {
       "title":row["title"],"slug":row["slug"],"kind":kind,"parent_path":parent,
       "featured_image_id":media,"status":"publish","data":data,
       "content":content(kind,row),
       "excerpt":"مواصفات ماجنايت مصر 2026 من بيانات نيسان الرسمية، مع اختلاف التجهيزات والأسواق.",
       "meta_title":row["title"]+" | أعطال.كوم",
       "meta_description":("تعرف على "+row["title"]+" وفق بيانات نيسان مصر الرسمية، مع التنبيه إلى فروق الفئات والأسواق.")[:155]
    }

def verify(url,name,title):
    for k in range(6):
        try:
            rr=get(url,params={"magnite_quality_check":str(time.time_ns())},
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
    assert len(QUEUE)==4
    count=max(1,min(4,int(os.getenv("A3CR_LIMIT","1"))))
    brand=current("nissan")
    if len(brand)!=1 or brand[0]["link"].rstrip("/")!=BASE+"/car-reference/nissan":
        raise RuntimeError("Expected existing Nissan parent not found")
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
            fn="a3tal-nissan-magnite-editorial-"+slug+".webp"
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
