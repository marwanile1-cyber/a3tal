#!/usr/bin/env python3
"""Publish the source-checked 2025 Hyundai Tucson NX4e reference cluster.

Safety:
- Every technical value is from the linked official Hyundai owner's manual.
- Photos are new unique page compositions made from already owned on-site Tucson
  photographic artwork, NOT falsely presented as brand-new generated photographs.
- No unpublished records or empty indexable URLs.
- No duplication of previous brand/make/model records.
- Post status, featured photo, canonical and OG image are checked live.
"""
import base64
import io
import json
import os
import re
import time
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"data/car-reference/batch-05-hyundai-tucson-nx4e-2025.json").read_text(encoding="utf8"))
SITE="https://a3tal.com"
BRIDGE=SITE+"/wp-json/a3tal-direct/v1/upload-image-data"
API=SITE+"/wp-json/a3tal-car-reference/v1/upsert"
KEY=os.environ["A3TAL_API_KEY"]
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
S=requests.Session()
S.headers["User-Agent"]="A3tal-Tucson-NX4e-Technical-References/1.0"
REPORT=ROOT/"tucson-nx4e-batch05-results.json"
DONE=[]
MODEL=DATA["model"]
ROWS=[("model",MODEL,"hyundai")]+[("spec",r,"hyundai/"+MODEL["slug"]) for r in DATA["items"]]
PALETTE={"model":(49,174,227),"engine-oil":(49,187,212),
        "transmission-oil":(223,158,78),"tire-specs":(96,205,188),
        "coolant":(68,171,235),"brake-fluid":(231,112,100),
        "differential-oil":(219,164,78),"transfer-case-oil":(151,141,245)}
TOPICS={"engine-oil":"زيت المحرك","transmission-oil":"زيت فتيس DCT",
        "tire-specs":"مقاس وضغط الكاوتش","coolant":"دورة تبريد المحرك",
        "brake-fluid":"سائل الفرامل","differential-oil":"زيت الدفرنس الخلفي",
        "transfer-case-oil":"زيت علبة النقل"}

def font(size,ar=False):
    choices=(["/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if ar
             else ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"])
    for path in choices:
        if Path(path).is_file():
            return ImageFont.truetype(path,size)
    raise RuntimeError("Font not available")

def with_retry_get(url,**kwargs):
    for n in range(4):
        try:
            result=S.get(url,timeout=60,**kwargs)
            result.raise_for_status()
            return result
        except requests.RequestException:
            if n==3:raise
            time.sleep(3+n*3)

def existing(slug):
    records=with_retry_get(SITE+"/wp-json/wp/v2/car-reference-records",
        params={"slug":slug,"per_page":20}).json()
    return [p for p in records if p.get("slug")==slug and p.get("status")=="publish"]

def source_photo():
    for url in (DATA["image_source"]["preferred"],DATA["image_source"]["fallback"]):
        try:
            r=with_retry_get(url,headers={"Accept":"image/webp,image/jpeg,image/png,*/*"})
            if len(r.content)<22000:raise RuntimeError("Source pixels insufficient")
            im=Image.open(io.BytesIO(r.content)).convert("RGB")
            if im.width<900 or im.height<540:raise RuntimeError("Source aspect/size insufficient "+str(im.size))
            print("APPROVED OWNED SITE PHOTO",url,im.size,flush=True)
            return im,url
        except Exception as e:
            print("Source rejected",url,str(e)[:130],flush=True)
    raise RuntimeError("No suitable owned photo. Stop before publishing.")

def cover(master,kind,row,index):
    """Technical editorial photo, never the old neon-line technical drawings."""
    key=row["slug"]
    accent=PALETTE[row.get("category",kind)]
    c=Image.new("RGB",(1600,900),(7,18,32))
    # Rotate / crop source in different ways so every page has unique composition.
    lens=[(0.39,0.52),(0.45,0.50),(0.52,0.54),(0.43,0.43)][index%4]
    src=ImageOps.fit(master,(1400,840),method=Image.Resampling.LANCZOS,centering=lens)
    if index % 3 == 2:src=src.filter(ImageFilter.UnsharpMask(radius=1.5,percent=140,threshold=3))
    c.paste(src,(-150+(index%3)*30,60))
    layer=Image.new("RGBA",c.size,(0,0,0,0))
    d=ImageDraw.Draw(layer)
    for x in range(365,1600,3):
        alpha=min(255,int(18+236*(x-365)/1235))
        d.rectangle((x,0,x+3,900),fill=(4,17,32,alpha))
    d.rectangle((0,0,1600,112),fill=(6,20,36,232))
    d.rectangle((0,810,1600,900),fill=(6,20,36,244))
    d.rounded_rectangle((940,270,1538,703),radius=31,fill=(11,29,46,232),outline=(*accent,254),width=3)
    d.rectangle((959,206,1534,213),fill=(*accent,254))
    for rad in (50,76,102):
        d.ellipse((1420-rad,762-rad,1420+rad,762+rad),outline=(*accent,27),width=3)
    c=Image.alpha_composite(c.convert("RGBA"),layer)
    t=ImageDraw.Draw(c)
    t.text((70,68),"HYUNDAI  /  TUCSON NX4e",font=font(26),fill=(232,245,252))
    metric=row.get("metric","TUCSON NX4e")
    if len(metric)>12:sz=58
    elif len(metric)>9:sz=72
    else:sz=97
    t.text((1496,404),metric,font=font(sz),fill=(255,255,255),anchor="ra")
    topic=TOPICS.get(row.get("category"),"دليل المواصفات الفنية")
    t.text((1492,527),topic,font=font(35,True),fill=accent,anchor="ra",direction="rtl")
    subtitle=str(row.get("subtitle","MY 2025 / OWNER MANUAL"))
    if re.search(r"[\u0600-\u06ff]",subtitle):
        t.text((1493,616),subtitle[:34],font=font(26,True),fill=(210,230,238),anchor="ra",direction="rtl")
    else:
        t.text((1493,616),subtitle[:34],font=font(26),fill=(210,230,238),anchor="ra")
    t.text((1490,868),"A3TAL.COM  ·  SERVICE REFERENCE",font=font(23),fill=(228,240,249),anchor="ra")
    raw=io.BytesIO()
    c.convert("RGB").save(raw,"WEBP",quality=88,method=5)
    if raw.tell()<70000:raise RuntimeError("Poor cover quality "+key+" bytes "+str(raw.tell()))
    return raw.getvalue()

def post_json(url,data):
    for n in range(4):
        try:
            r=S.post(url,json=data,headers=HEAD,timeout=145)
            if r.status_code>=500:raise requests.RequestException("server "+str(r.status_code))
            if not r.ok:raise RuntimeError(f"Rejected {r.status_code}: {r.text[:260]}")
            return r.json()
        except requests.RequestException:
            if n==3:raise
            time.sleep(4+n*4)

def model_html():
    return (
      "<p>هذا القسم مرجع فني لهيونداي توسان NX4e المحدثة وفق دليل المالك الدولي لعام 2025. "
      "يعرض بيانات السوائل، سعات المحركات، مقاسات وضغط الإطارات، والفرق بين أنظمة الجر وناقلات الحركة. "
      "توجد مواصفات للشرق الأوسط تشمل مصر صراحة في دليل الشركة، لكن توافر كل محرك أو فئة محليًا يجب التأكد منه.</p>"
      "<h2>ما هي نسخة السيارة المناسبة؟</h2>"
      "<p>تختلف كمية ونوع زيت المحرك Smartstream 1.6 T-GDi عن G2.0 وG2.5، "
      "كما يختلف فتيس DCT عن الأوتوماتيك AT، ولا توجد منظومة دفرنس خلفي AWD في كل النسخ. "
      "اختر صفحة مواصفات تطابق رقم المحرك ونوع الفتيس وليس مجرد اسم توسان.</p>"
      "<h2>الفرق بين هذا الدليل وأسعار توسان</h2>"
      "<p>الصفحات هنا تجيب عن مقاسات وسعات السوائل والقطع التي يحتاجها المالك وقت الصيانة. "
      "أما أسعار السيارة وفئاتها وتقييمها فموجودة في <a href='https://a3tal.com/hyundai-tucson-2027-prices-egypt/'>"
      "دليل الأسعار</a>، و<a href='https://a3tal.com/used-hyundai-tucson-prices-egypt-2026/'>سوق المستعمل</a>. "
      "ولا تُنقل تجهيزات موديل 2027 إلى نسخة 2025 دون مستند.</p>"
      "<h2>المصدر ومعنى مواصفات الشرق الأوسط</h2>"
      "<p>دليل هيونداي يدرج مصر ضمن تعريفه لأسواق الشرق الأوسط عند الحديث عن الزيوت. "
      "اتبع كتيب السيارة الخاصة بك عند اختلاف سنة الإصدار أو رقم الشاسيه أو السوق.</p>"
    )

def spec_html(row):
    src=escape(row["source"],quote=True)
    return (
        "<p>"+escape(row["intro"])+"</p>"
        "<h2>أهم الأرقام والمواصفات</h2><p>"+escape(row["detail"])+"</p>"
        "<h2>هل تنطبق على جميع فئات توسان؟</h2>"
        "<p>"+escape(row["warning"])+"</p>"
        "<h2>قبل شراء الزيت أو إجراء الصيانة</h2>"
        "<p>طابق سنة الموديل وكود المحرك ونوع الفتيس ونظام الجر مع ملصق السيارة ودليل المالك. "
        "القيم المرجعية لا تعني أن كل صيانة جزئية تتطلب تعبئة السعة الكاملة، ولا يجوز خلط السوائل أو تجاوز "
        "المستوى الصحيح. عند الشك تُرجع خطوات القياس إلى مركز صيانة مختص.</p>"
        "<p>المصدر المعتمد: <a href='"+src+"' rel='nofollow noopener noreferrer'>"
        "جدول المواصفات في دليل مالك هيونداي توسان NX4e 2025</a>.</p>"
    )

def entry(kind,row,parent,media):
    data={"kind":kind,"market":"إصدار 2025 عالمي، مع بيانات مصر والشرق الأوسط عندما يحددها دليل هيونداي",
          "years":"2025","engine":row.get("engine","NX4e Facelift"),
          "category":row.get("category",""),
          "reviewed_at":"2026-11-03",
          "facts":[{"label":k,"value":v} for k,v in row.get("facts",[])],
          "sources":[{"title":"دليل المالك الرسمي لهيونداي توسان NX4e موديل 2025",
                      "url":row.get("source",MODEL["source"])}]}
    return {"title":row["title"],"slug":row["slug"],"kind":kind,"parent_path":parent,
      "status":"publish","featured_image_id":media,
      "content":model_html() if kind=="model" else spec_html(row),
      "excerpt":"مواصفات فنية موثقة من دليل هيونداي الرسمي؛ يجب مطابقة المحرك والفئة والسوق قبل الصيانة.",
      "data":data,
      "meta_title":row["title"]+" | أعطال.كوم",
      "meta_description":("مواصفات "+row["title"]+" طبقًا لكتيب هيونداي الرسمي 2025: السعات والمقاسات والنقاط المهمة قبل صيانة السيارة.")[:155]}

def check_live(url, filename, title):
    for n in range(7):
        try:
            r=with_retry_get(url,params={"tucson_audit":str(time.time_ns())},
                             headers={"Cache-Control":"no-cache"})
            if r.url.split("?")[0].rstrip("/")!=url.rstrip("/"):raise RuntimeError("redirect")
            h=r.text
            if title not in h:raise RuntimeError("title")
            if filename not in h:raise RuntimeError("featured photo")
            image=re.search(r'<meta[^>]*property=["\x27]og:image["\x27][^>]*content=["\x27]([^"\x27]+)',h,re.I)
            if not image or filename not in image.group(1):raise RuntimeError("og:image")
            canonical=re.search(r'<link[^>]*rel=["\x27]canonical["\x27][^>]*href=["\x27]([^"\x27]+)',h,re.I)
            if not canonical or canonical.group(1).rstrip("/")!=url.rstrip("/"):raise RuntimeError("canonical")
            if "noindex" in h[:15000].lower():raise RuntimeError("noindex")
            return True
        except Exception as e:
            if n==6:raise RuntimeError("Failed verify "+url+" "+str(e))
            time.sleep(4)

def main():
    assert len(DATA["items"])==7 and len(ROWS)==8
    assert len({r["slug"] for k,r,p in ROWS})==8
    limit=max(1,min(8,int(os.getenv("A3CR_LIMIT","1"))))
    photo,source=source_photo()
    print("TUCSON PHOTO SOURCE",source,flush=True)
    try:
        for index,(kind,row,parent) in enumerate(ROWS[:limit]):
            slug=row["slug"]
            target=SITE+"/car-reference/"+parent+"/"+slug+"/"
            old=existing(slug)
            if old:
                if len(old)!=1 or old[0]["link"].rstrip("/")!=target.rstrip("/"):
                    raise RuntimeError("Existing conflict: "+slug)
                DONE.append({"slug":slug,"url":target,"status":"already-live"})
                print("SKIP existing",target,flush=True)
                continue
            art=cover(photo,kind,row,index)
            filename="a3tal-hyundai-tucson-nx4e-2025-"+slug+".webp"
            media=post_json(BRIDGE,{
              "filename":filename,"image_base64":base64.b64encode(art).decode("ascii"),
              "convert_webp":False,"title":row["title"],
              "alt":row["title"]+" - تصميم فني خاص بموسوعة أعطال.كوم"})
            media_id=int(media.get("media_id") or 0)
            if not media_id or not media.get("url","").endswith(".webp"):
                raise RuntimeError("Failed uploaded photo id "+slug)
            payload=entry(kind,row,parent,media_id)
            # Connection may be lost after WordPress saves a post; re-check slug
            # before resubmitting to avoid duplicates.
            try:
                result=post_json(API,{"items":[payload]})
            except requests.RequestException:
                found=existing(slug)
                if len(found)==1 and found[0]["link"].rstrip("/")==target.rstrip("/"):
                    result={"results":[{"ok":True,"status":"publish","id":found[0]["id"],"url":target}]}
                else:result=post_json(API,{"items":[payload]})
            records=result.get("results") or []
            if len(records)!=1 or not records[0].get("ok") or records[0].get("status")!="publish":
                raise RuntimeError("Publishing not accepted: "+str(records)[:350])
            actual=records[0].get("url","")
            if actual.rstrip("/")!=target.rstrip("/"):raise RuntimeError("Unexpected permalink "+actual)
            check_live(target,filename,row["title"])
            DONE.append({"slug":slug,"url":target,"status":"published",
                "featured_media":media_id,"image":media["url"],"verified":True})
            print("PUBLISHED AND VERIFIED",target,flush=True)
    finally:
        REPORT.write_text(json.dumps({"photo_master":source,"results":DONE},ensure_ascii=False,indent=2),encoding="utf8")
    if len(DONE)!=limit:raise RuntimeError("Only "+str(len(DONE))+" of "+str(limit)+" entries handled")
    print("COMPLETE",len(DONE),"TUCSON RECORDS",flush=True)

if __name__=="__main__":
    main()
