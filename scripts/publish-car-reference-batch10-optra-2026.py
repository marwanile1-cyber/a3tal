#!/usr/bin/env python3
"""Chevrolet Optra 2026: five non-duplicated technical pages via Direct Bridge.

Figures come from Chevrolet Egypt's official new Optra 2026 brochure.
Illustrations are original editorial compositions from an existing A3tal-owned
Optra 2026 image, not separately generated car photographs. Live page is mandatory:
URL, featured image, Yoast og:image and canonical must all pass.
"""
import base64, io, json, os, re, time, hashlib
from html import escape
from pathlib import Path
import requests
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"data/car-reference/batch-10-chevrolet-optra-egypt-2026.json").read_text(encoding="utf8"))
BASE="https://a3tal.com"
KEY=os.environ["A3TAL_API_KEY"]
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
SESSION=requests.Session()
SESSION.headers["User-Agent"]="A3tal-Chevrolet-Optra-Verified-Batch10/1.0"
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
REPORT=ROOT/"car-reference-batch10-optra-results.json"
DONE=[]
ROWS=[("brand",DATA["brand"],""),("model",DATA["model"],"chevrolet")]+[("spec",r,"chevrolet/optra-2026-egypt") for r in DATA["items"]]
COLORS={"brand":(188,84,70),"model":(162,94,85),"engine-specs":(170,137,87),
        "dimensions":(74,149,186),"safety-specs":(88,155,150)}
TOPICS={"engine-specs":"محرك أوبترا الجديدة","dimensions":"سعة الوقود والشنطة","safety-specs":"أنظمة الأمان في أوبترا"}
assert len(ROWS)==5 and len(DATA["items"])==3

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
            print("A3TAL OPTRA PHOTOGRAPHY INPUT",source,im.size,flush=True)
            return im,source
        except Exception as exc:
            print("Rejected image source",str(exc)[:170],flush=True)
    raise RuntimeError("No suitable owned Optra photograph: abort publishing")

def cover(im,kind,row,index):
    accent=COLORS.get(row.get("category",kind),(64,147,170))
    width,height=1600,900
    # Large actual Optra 2026 imagery without oversized text or generic vector car.
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
    label.text((66,816),"OPTRA  /  EGYPT SERVICE REFERENCE",font=font(25),fill=(244,249,250))
    out=io.BytesIO()
    src.convert("RGB").save(out,"WEBP",quality=89,method=5)
    if out.tell()<65000:raise RuntimeError("Rejected cover output "+row["slug"])
    return out.getvalue()

def brand_html():
    return (
      "<p>يضم دليل المواصفات الفنية لشيفروليه في أعطال.كوم بيانات المحركات وناقلات الحركة "
      "والأبعاد ووسائل السلامة المستندة إلى مصادر شيفروليه مصر الرسمية. نبدأ بأوبترا الجديدة "
      "موديل 2026 بفئتي LS وLT، دون خلط بينها وبين أوبترا الأجيال الأقدم.</p>"
      "<h2>الموديلات المتاحة حاليًا</h2>"
      "<p>يقدم <a href='https://a3tal.com/car-reference/chevrolet/optra-2026-egypt/'>"
      "دليل أوبترا الجديدة 2026</a> معلومات المحرك 1485 سم³ وناقل CVT وسعة الوقود "
      "والشنطة والأبعاد وأنظمة الأمان. يجب اختيار المواصفة المطابقة لجيل السيارة وسنة الإنتاج.</p>"
      "<h2>الفرق عن صفحات الأعطال والأسعار</h2>"
      "<p>تلك الصفحات مرجع للمواصفات فقط، بينما "
      "<a href='https://a3tal.com/chevrolet-optra-transmission-problems-guide/'>"
      "مشاكل فتيس أوبترا</a> و<a href='https://a3tal.com/chevrolet-optra-2026-egypt/'>"
      "مراجعة أوبترا في مصر</a> لهما صفحات قائمة مخصصة لنية بحث مختلفة.</p>"
    )
def model_html():
    return (
      "<p>توثق هذه الصفحة مواصفات شيفروليه أوبترا الجديدة 2026 للسوق المصري كما يوردها "
      "الكتالوج الرسمي. المحرك 1485 سم³ بقدرة 98 حصانًا وعزم 140 نيوتن متر "
      "مع ناقل CVT، وتختلف بعض التجهيزات الخارجية والداخلية بين LS وLT.</p>"
      "<h2>اختر المواصفة المطلوبة</h2>"
      "<p>توجد صفحات منفصلة للمحرك وناقل الحركة، ولسعة خزان الوقود والشنطة والأبعاد، "
      "ولأنظمة الأمان مثل ABS وESC والوسائد الهوائية. تظهر روابط الصفحات المرتبطة أسفل "
      "الدليل، والهدف تقديم جداول دقيقة للمالك دون تكرار محتوى الأسعار.</p>"
      "<h2>الفرق بين أوبترا الجديدة والقديمة</h2>"
      "<p>لا يكفي الاسم التجاري لاختيار سائل فتيس أو قطعة غيار. الأرقام تخص موديل 2026 "
      "كما تعرضه شيفروليه مصر، ولا تُنقل لأوبترا الأقدم دون كتالوج مطابق.</p>"
      "<h2>مقالات مخصصة للأعطال والشراء</h2>"
      "<p>لمعلومات الشراء راجع <a href='https://a3tal.com/chevrolet-optra-2026-egypt/'>"
      "دليل أوبترا في مصر</a>، وللتشخيص راجع "
      "<a href='https://a3tal.com/chevrolet-optra-transmission-problems-guide/'>"
      "مقال مشاكل فتيس أوبترا</a>.</p>"
    )

def spec_html(row):
    sources=row["sources"]
    return (
      "<p>"+escape(row["intro"])+"</p>"
      "<h2>المواصفات الرسمية بالتفصيل</h2><p>"+escape(row["detail"])+"</p>"
      "<h2>متى لا ينطبق هذا الرقم على السيارة؟</h2><p>"+escape(row["warning"])+"</p>"
      "<h2>التحقق قبل شراء القطع أو الصيانة</h2>"
      "<p>طابق تجهيزات السيارة وسنة الإنتاج والفئة مع النشرة المحلية ومُلصق السيارة، "
      "ولا تنقل بيانات نسخة أوبترا 2026 من سوق آخر إلى نسخة مصر دون التأكد من المحرك "
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
          "market":"مصر - مواصفات Chevrolet Egypt المنشورة، الفئات حسب النشرة",
          "years":"كتالوج شيفروليه أوبترا المصرية موديل 2026",
          "engine":row.get("engine","MG5 - 1.5L CVT"),"category":row.get("category",""),
          "reviewed_at":"2026-11-03","facts":facts,
          "sources":[{"title":"شيفروليه مصر - مواصفات أوبترا 2026 الرسمية",
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
            r=get(url,params={"optra_reference_qa":str(time.time_ns())},
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
            if n==6:raise RuntimeError("Optra live verification failed "+url+" "+str(e))
            time.sleep(3)

def main():
    assert len(ROWS)==5 and len(DATA["items"])==3
    assert len({r["slug"] for kind,r,parent in ROWS})==6
    limit=max(1,min(5,int(os.getenv("A3CR_LIMIT","1"))))
    photo_source,original=photo()
    print("OPTRA PHOTO MASTER",original,"sha",hashlib.sha256(photo_source.tobytes()).hexdigest()[:16],flush=True)
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
                expected_parent="chevrolet" if kind=="model" else "optra-2026-egypt"
                parent_slug=parent.split("/")[-1]
                if parent_slug!=expected_parent or len(find_post(parent_slug))!=1:
                    raise RuntimeError("Parent record not yet live for "+slug)
            raw=cover(photo_source,kind,row,index)
            filename="a3tal-optra-2026-egypt-reference-"+slug+".webp"
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
    print("COMPLETE",len(DONE),"Optra 2026 records",flush=True)

if __name__=="__main__": main()
