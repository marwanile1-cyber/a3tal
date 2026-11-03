#!/usr/bin/env python3
"""MG5 Egypt: six non-cannibalising specification pages via Direct Bridge.

Figures come from MG Motor Egypt model/trim pages and 2025 brochure.
Illustrations are original editorial compositions from an existing A3tal-owned
MG5 image, not separately generated car photographs. Live page is mandatory:
URL, featured image, Yoast og:image and canonical must all pass.
"""
import base64, io, json, os, re, time, hashlib
from html import escape
from pathlib import Path
import requests
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"data/car-reference/batch-09-mg5-egypt-official-20261103.json").read_text(encoding="utf8"))
BASE="https://a3tal.com"
KEY=os.environ["A3TAL_API_KEY"]
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
SESSION=requests.Session()
SESSION.headers["User-Agent"]="A3tal-MG5-Verified-Reference-Batch09/1.0"
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
REPORT=ROOT/"car-reference-batch09-mg5-results.json"
DONE=[]
ROWS=[("brand",DATA["brand"],""),("model",DATA["model"],"mg")]+[("spec",r,"mg/mg5-egypt") for r in DATA["items"]]
COLORS={"brand":(176,69,60),"model":(146,77,70),
        "tire-specs":(40,147,168),"engine-specs":(182,129,75),
        "dimensions":(90,144,177),"safety-specs":(107,154,135)}
TOPICS={"tire-specs":"مقاسات كاوتش MG5","engine-specs":"مواصفات محرك MG5",
        "dimensions":"سعة الوقود والشنطة","safety-specs":"وسائل الأمان حسب الفئة"}
assert len(ROWS)==6 and len(DATA["items"])==4

def font(n, ar=False):
    paths=(["/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if ar else
           ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"])
    for p in paths:
        if Path(p).exists():return ImageFont.truetype(p,n)
    raise RuntimeError("Font missing")

def get(url, **kw):
    for attempt in range(3):
        try:
            r=SESSION.get(url,timeout=65,**kw)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if attempt==2:raise
            time.sleep(3+attempt*3)

def send(url, payload):
    for attempt in range(3):
        try:
            r=SESSION.post(url,json=payload,headers=HEAD,timeout=160)
            if r.status_code>=500:raise requests.RequestException("backend "+str(r.status_code))
            if not r.ok:raise RuntimeError("REST request rejected "+str(r.status_code)+" "+r.text[:260])
            return r.json()
        except requests.RequestException:
            if attempt==2:raise
            time.sleep(5+attempt*5)

def find_post(slug):
    records=get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":20}).json()
    return [p for p in records if p.get("slug")==slug and p.get("status")=="publish"]

def photo():
    sources=[DATA["photos"]["primary"]]
    for source in sources:
        try:
            r=get(source,headers={"Accept":"image/webp,image/jpeg,image/png,*/*"})
            if len(r.content)<30000:raise RuntimeError("Not a viable photo")
            im=Image.open(io.BytesIO(r.content)).convert("RGB")
            if im.width<1200 or im.height<670:raise RuntimeError("Low original resolution "+str(im.size))
            print("A3TAL MG5 PHOTOGRAPHY INPUT",source,im.size,flush=True)
            return im,source
        except Exception as exc:
            print("Rejected image source",str(exc)[:170],flush=True)
    raise RuntimeError("No owned high-quality MG5 photo: abort publish")

def cover(im,kind,row,index):
    accent=COLORS.get(row.get("category",kind),(64,147,170))
    width,height=1600,900
    # Large actual MG5 imagery without oversized text or generic vector car.
    # Every page gets a separately composed crop and tonal treatment.
    focus=[(0.50,0.47),(0.52,0.53),(0.42,0.51),(0.57,0.46),
           (0.46,0.57),(0.55,0.54)][index]
    src=ImageOps.fit(im,(1600,900),method=Image.Resampling.LANCZOS,centering=focus)
    if index%3==1:src=ImageEnhance.Contrast(src).enhance(1.07)
    if index%3==2:src=ImageEnhance.Color(src).enhance(0.93)
    src=src.filter(ImageFilter.UnsharpMask(radius=1.2,percent=115,threshold=3))
    overlay=Image.new("RGBA",(width,height))
    painter=ImageDraw.Draw(overlay)
    for y in range(610,900,3):
        a=int(155*(y-610)/290)
        painter.rectangle((0,y,width,y+3),fill=(4,14,24,a))
    painter.rounded_rectangle((48,47,230,90),radius=12,fill=(4,14,27,164))
    painter.rectangle((50,858,1550,863),fill=(*accent,190))
    src=Image.alpha_composite(src.convert("RGBA"),overlay)
    label=ImageDraw.Draw(src)
    label.text((63,61),"A3TAL.COM",font=font(18),fill=(246,249,252))
    label.text((66,816),"MG5  /  EGYPT SERVICE REFERENCE",font=font(25),fill=(244,249,250))
    out=io.BytesIO()
    src.convert("RGB").save(out,"WEBP",quality=89,method=5)
    if out.tell()<65000:raise RuntimeError("Rejected cover output "+row["slug"])
    return out.getvalue()

def brand_html():
    return (
      "<p>يقدم دليل مواصفات MG في أعطال.كوم أرقامًا فنية موثقة من موقع إم جي مصر "
      "ونشرات الشركة الرسمية، بدل الاعتماد على منشورات عامة تخلط بين السيارات والفئات والأسواق. "
      "تبدأ المجموعة بسيارة MG5 السيدان المتاحة بمصر، وتفصل المقاسات وتجهيزات الأمان والمحرك والأبعاد.</p>"
      "<h2>اختر السيارة ثم المواصفة</h2>"
      "<p>يمكن الوصول إلى <a href='https://a3tal.com/car-reference/mg/mg5-egypt/'>دليل MG5 في مصر</a> "
      "لاختيار مقاس الكاوتش الصحيح أو معرفة سعة الوقود والشنطة وأرقام المحرك أو فرق وسائل السلامة. "
      "تختلف الفئات Classic وComfort وLuxury، ولا يجوز تعميم تجهيز Luxury على كل النسخ.</p>"
      "<h2>ما الفرق بين دليل المواصفات وأعطال MG5؟</h2>"
      "<p>هنا تُعرض المواصفات الرقمية قبل شراء القطع أو الصيانة، بينما الشروحات المتخصصة مثل "
      "<a href='https://a3tal.com/mg-5-cvt-transmission-problems-guide/'>مشكلات فتيس CVT</a> "
      "و<a href='https://a3tal.com/mg-5-maintenance-prices-guide-2026/'>تكلفة الصيانة</a> "
      "تُراجع في المقالات الموجودة بالفعل، حتى لا تتكرر الصفحات بنفس نية البحث.</p>"
    )
def model_html():
    return (
      "<p>هذه الصفحة تجمع البيانات الفنية لسيارة MG5 المعروضة في مصر وفق النشرة الرسمية من "
      "إم جي موتورز مصر. المحرك المعلن 1.5 لتر بقوة 120 حصانًا والعزم 150 نيوتن متر مع CVT، "
      "وتختلف مقاسات الإطارات وتجهيزات السلامة والشاشات بحسب الفئة.</p>"
      "<h2>ابدأ بالمعلومة المطلوبة</h2>"
      "<p>اختر صفحة <strong>مقاسات الإطارات</strong> لمعرفة الفرق بين 15 و16 بوصة، وصفحة "
      "<strong>المحرك</strong> لبيانات القدرة والفتيس، وصفحة <strong>الوقود والأبعاد</strong> "
      "لسعة التانك والشنطة، أو صفحة <strong>وسائل الأمان</strong> لمقارنة الوسائد والفرامل الإلكترونية. "
      "تتوافر التفاصيل في روابط الصفحات المرتبطة أسفل الدليل.</p>"
      "<h2>اختلاف الفئات والسوق</h2>"
      "<p>تصف صفحة الشركة فئات Classic وComfort وLuxury، وتعرض النشرة الفنية بعض المقارنات "
      "بين Comfort وLuxury. توافر الفئة فعليًا لدى الوكيل يتغير، لذا لا يُفهم وجودها "
      "في كتالوج المواصفات على أنه تأكيد لتوافرها للبيع الآن.</p>"
      "<h2>مقالات MG5 الأخرى على أعطال</h2>"
      "<p>للبحث عن الأسعار أو التجارب والمراجعات راجع "
      "<a href='https://a3tal.com/mg5-new-egypt-prices-trims-2026-october/'>دليل سعر MG5</a> "
      "أو <a href='https://a3tal.com/mg5-vs-nissan-sunny-egypt-buying-comparison/'>"
      "مقارنتها بنيسان صني</a>. هذه الصفحة مخصصة للأرقام الفنية.</p>"
    )
def spec_html(row):
    sources=row["sources"]
    return (
      "<p>"+escape(row["intro"])+"</p>"
      "<h2>المواصفات الرسمية بالتفصيل</h2><p>"+escape(row["detail"])+"</p>"
      "<h2>متى لا ينطبق هذا الرقم على السيارة؟</h2><p>"+escape(row["warning"])+"</p>"
      "<h2>التحقق قبل شراء القطع أو الصيانة</h2>"
      "<p>طابق تجهيزات السيارة وسنة الإنتاج والفئة مع النشرة المحلية ومُلصق السيارة، "
      "ولا تنقل بيانات نسخة MG5 من سوق آخر إلى نسخة مصر دون التأكد من المحرك "
      "ونوع الناقل. الأرقام المعروضة بيانات للتعريف والمقارنة، وليست تعليمات "
      "بإضافة سوائل أو تعديل أنظمة سلامة. تُراجع إجراءات الصيانة في كتيب المالك الأصلي.</p>"
      "<p><strong>المصدر:</strong> <a href='"+escape(sources[0],quote=True)+
      "' rel='nofollow noopener noreferrer'>إم جي مصر: النشرة أو صفحة المواصفات الرسمية</a>.</p>"
    )

def entry(kind,row,parent,featured):
    ref=DATA["sources"]["official"]
    sources=([ref,DATA["sources"]["brochure"]] if kind!="spec" else row["sources"])
    facts=[{"label":k,"value":v} for k,v in row.get("facts",[])]
    data={"kind":kind,
          "market":"مصر - مواصفات MG Motor Egypt المنشورة، الفئات حسب النشرة",
          "years":"حسب نشرة الشركة أكتوبر 2025 والصفحات الرسمية المحدثة",
          "engine":row.get("engine","MG5 - 1.5L CVT"),"category":row.get("category",""),
          "reviewed_at":"2026-11-03","facts":facts,
          "sources":[{"title":"MG Motor Egypt - مواصفات MG5 الرسمية",
                      "url":url} for url in sources]}
    return {
      "kind":kind,"slug":row["slug"],"title":row["title"],
      "parent_path":parent,"status":"publish","featured_image_id":featured,
      "content":brand_html() if kind=="brand" else model_html() if kind=="model" else spec_html(row),
      "excerpt":"المواصفات الفنية المحلية لـMG5، مع الفصل بين الفئات والمصادر الرسمية.",
      "data":data,"meta_title":row["title"]+" | أعطال.كوم",
      "meta_description":("تعرف على "+row["title"]+" من بيانات إم جي مصر الرسمية، مع اختلاف الفئات وتنبيهات مهمة قبل الصيانة.")[:155]
    }

def verify_live(url,filename,title):
    for n in range(7):
        try:
            r=get(url,params={"mg5_reference_qa":str(time.time_ns())},
                  headers={"Cache-Control":"no-cache"})
            if r.url.split("?")[0].rstrip("/")!=url.rstrip("/"):raise RuntimeError("redirect")
            html=r.text
            if title not in html or filename not in html:raise RuntimeError("featured/title missing")
            og=re.search(r'<meta[^>]*property=["\x27]og:image["\x27][^>]*content=["\x27]([^"\x27]+)',html,re.I)
            if not og or filename not in og.group(1):raise RuntimeError("og:image")
            ca=re.search(r'<link[^>]*rel=["\x27]canonical["\x27][^>]*href=["\x27]([^"\x27]+)',html,re.I)
            if not ca or ca.group(1).rstrip("/")!=url.rstrip("/"):raise RuntimeError("canonical")
            if "noindex" in html[:14000].lower():raise RuntimeError("noindex")
            return True
        except Exception as e:
            if n==6:raise RuntimeError("MG5 live verification failed "+url+" "+str(e))
            time.sleep(3)

def main():
    assert len(ROWS)==6 and len(DATA["items"])==4
    assert len({r["slug"] for kind,r,parent in ROWS})==6
    limit=max(1,min(6,int(os.getenv("A3CR_LIMIT","1"))))
    photo_source,original=photo()
    print("MG5 PHOTO MASTER",original,"sha",hashlib.sha256(photo_source.tobytes()).hexdigest()[:16],flush=True)
    try:
        for index,(kind,row,parent) in enumerate(ROWS[:limit]):
            slug=row["slug"]
            url=BASE+"/car-reference/"+(parent+"/"+slug if parent else slug)+"/"
            live=find_post(slug)
            if live:
                if len(live)!=1 or live[0]["link"].rstrip("/")!=url.rstrip("/"):
                    raise RuntimeError("Conflicting published slug "+slug)
                DONE.append({"slug":slug,"url":url,"status":"existing"})
                print("SKIP live",url,flush=True)
                continue
            if kind!="brand":
                expected_parent="mg" if kind=="model" else "mg5-egypt"
                parent_slug=parent.split("/")[-1]
                if parent_slug!=expected_parent or len(find_post(parent_slug))!=1:
                    raise RuntimeError("Parent record not yet live for "+slug)
            raw=cover(photo_source,kind,row,index)
            filename="a3tal-mg5-egypt-reference-"+slug+".webp"
            m=send(UPLOAD,{"filename":filename,"image_base64":base64.b64encode(raw).decode("ascii"),
                     "title":row["title"],"alt":row["title"]+" - تصميم تحريري لأعطال.كوم",
                     "convert_webp":False})
            media_id=int(m.get("media_id") or 0)
            if not media_id or not str(m.get("url","")).endswith(".webp"):
                raise RuntimeError("Media upload did not return WebP "+slug)
            payload=entry(kind,row,parent,media_id)
            try:
                result=send(UPSERT,{"items":[payload]})
            except requests.RequestException:
                # Remote WP may have committed successfully before disconnect.
                old=find_post(slug)
                if len(old)==1 and old[0]["link"].rstrip("/")==url.rstrip("/"):
                    result={"results":[{"ok":True,"status":"publish","id":old[0]["id"],"url":url}]}
                else:result=send(UPSERT,{"items":[payload]})
            records=result.get("results") or []
            if len(records)!=1 or not records[0].get("ok") or records[0].get("status")!="publish":
                raise RuntimeError("Publishing rejected "+slug+" "+repr(records)[:350])
            if records[0].get("url","").rstrip("/")!=url.rstrip("/"):
                raise RuntimeError("Unexpected permalink "+str(records[0].get("url")))
            verify_live(url,filename,row["title"])
            DONE.append({"slug":slug,"status":"published","url":url,
                         "media_id":media_id,"photo_url":m["url"],"canonical_og_checked":True})
            print("PUBLISHED AND VERIFIED",url,media_id,flush=True)
    finally:
        REPORT.write_text(json.dumps({"photo_master":original,"records":DONE},
                  ensure_ascii=False,indent=2),encoding="utf8")
    assert len(DONE)==limit
    print("COMPLETE",len(DONE),"MG5 records",flush=True)

if __name__=="__main__": main()
