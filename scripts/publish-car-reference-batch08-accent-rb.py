#!/usr/bin/env python3
"""Publish five brochure-backed Hyundai Accent RB Egypt car-reference pages.
Uses photos already published by A3tal in its Accent RB review; composites are
uniquely cropped editorial WebP covers, NOT new independently generated photos.
No invented oil capacities or pressure values. Idempotent and URL guarded.
"""
import base64, io, json, os, re, time
from html import escape
from pathlib import Path
import requests
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"data/car-reference/batch-08-hyundai-accent-rb-egypt-20251103.json").read_text(encoding="utf8"))
BASE="https://a3tal.com"
HDR={"X-A3tal-Key":os.environ["A3TAL_API_KEY"],"Content-Type":"application/json"}
SESSION=requests.Session()
SESSION.headers["User-Agent"]="A3tal-Accent-RB-Egypt-Brochure-Batch08/1.0"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
MEDIA=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
RESULTS=[]
REPORT=ROOT/"accent-rb-batch08-audit.json"
MODEL=DATA["model"]
ITEMS=[("model",MODEL,"hyundai")]+[("spec",row,"hyundai/"+MODEL["slug"]) for row in DATA["items"]]
PALETTE={"model":(51,146,190),"tire-specs":(25,143,173),"engine-specs":(92,132,169),
         "dimensions":(116,145,153),"safety-specs":(146,122,125)}
SOURCES=[DATA["photo_source"]["preferred"],DATA["photo_source"]["secondary"],
         DATA["photo_source"]["tertiary"]]

def get(url,**kw):
    for n in range(3):
        try:
            r=SESSION.get(url,timeout=60,**kw)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if n==2:raise
            time.sleep(3+3*n)

def post(url,data):
    for n in range(3):
        try:
            r=SESSION.post(url,headers=HDR,json=data,timeout=160)
            if r.status_code>=500:raise requests.RequestException("HTTP "+str(r.status_code))
            if not r.ok:raise RuntimeError("Rejected "+str(r.status_code)+" "+r.text[:300])
            return r.json()
        except requests.RequestException:
            if n==2:raise
            time.sleep(4+4*n)

def existing(slug):
    posts=get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":20}).json()
    return [p for p in posts if p.get("slug")==slug and p.get("status")=="publish"]

def find_photographs():
    imgs=[]
    for url in SOURCES:
        try:
            r=get(url,headers={"Accept":"image/webp,image/jpeg,image/png,*/*"})
            if len(r.content)<28000:raise RuntimeError("image too small")
            im=Image.open(io.BytesIO(r.content)).convert("RGB")
            if im.width<1100 or im.height<650:raise RuntimeError("photo too small "+str(im.size))
            imgs.append((im,url))
            print("OWNED ACCENT PHOTO OK",url,im.size,flush=True)
        except Exception as e:
            print("PHOTO SOURCE NOT AVAILABLE",url,str(e)[:190],flush=True)
    if not imgs:raise RuntimeError("No suitable image on A3tal to use; publication stopped")
    return imgs

def f(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",):
        if Path(p).is_file():return ImageFont.truetype(p,size)
    raise RuntimeError("No font")

def render_cover(photo,kind,row,index):
    # Photo fills majority of frame. No huge numerals or advertising copy.
    im=Image.new("RGB",(1600,900),(15,24,32))
    focus=[(0.47,0.47),(0.53,0.49),(0.60,0.55),(0.50,0.46),(0.46,0.58)][index]
    pic=ImageOps.fit(photo,(1600,900),method=Image.Resampling.LANCZOS,centering=focus)
    pic=pic.filter(ImageFilter.UnsharpMask(radius=1.2,percent=118,threshold=3))
    im.paste(pic,(0,0))
    layer=Image.new("RGBA",im.size,(0,0,0,0))
    d=ImageDraw.Draw(layer)
    # Minimal photographic editorial treatment keeps subject clear.
    for y in range(550,900,4):
        a=int(174*(y-550)/350)
        d.rectangle((0,y,1600,y+4),fill=(6,17,27,a))
    d.rounded_rectangle((55,55,214,88),radius=7,fill=(5,21,34,185))
    accent=PALETTE[row.get("category",kind)]
    d.rectangle((55,866,1545,872),fill=(*accent,210))
    im=Image.alpha_composite(im.convert("RGBA"),layer)
    t=ImageDraw.Draw(im)
    # A compact provenance mark, no oversized inaccurate vehicle-spec text.
    t.text((68,62),"A3TAL.COM",font=f(17),fill=(244,248,251))
    name="HYUNDAI ACCENT RB · EGYPT 2025"
    t.text((65,817),name,font=f(27),fill=(247,249,250))
    out=io.BytesIO()
    im.convert("RGB").save(out,"WEBP",quality=90,method=5)
    if out.tell()<60000:raise RuntimeError("Image quality gate failed "+row["slug"])
    return out.getvalue()

def content(kind,row):
    if kind=="model":
        return (
         "<p>دليل المواصفات الفنية لهيونداي أكسنت RB المجمعة في مصر، وفق نشرة غبور الرسمية للسيارة "
         "التي تعرض محرك 1.6 لتر بناقل أوتوماتيك أربع سرعات. تعرض الصفحات التابعة المقاسات الفعلية "
         "للإطارات حسب فئة الجنط، ومواصفات المحرك، وسعات الوقود والأمتعة وأبعاد السيارة، وفروق تجهيزات الفرامل والأمان.</p>"
         "<h2>اختيار الصفحة حسب الخدمة</h2>"
         "<p>قبل شراء كاوتش جديد، حدّد هل سيارتك بجنط 14 بوصة أم 16 بوصة. ولتحديد قطعة غيار أو "
         "معلومات الفتيس، طابق كود المحرك ونوع الناقل وسنة الإنتاج. جدول الفئات مهم أيضًا لأن تجهيز "
         "ABS والوسائد الهوائية لا يأتي بالطريقة نفسها في جميع الفئات بالنشرة.</p>"
         "<h2>ما الفرق بين الدليل والمراجعة؟</h2>"
         "<p>توجد <a href='https://a3tal.com/hyundai-accent-rb-2026-review-egypt/'>"
         "مراجعة أكسنت RB في مصر</a> للمميزات والعيوب وقرار الشراء. "
         "أما الصفحات هنا فتختص بالمقاسات والأرقام الفنية المطلوبة قبل الصيانة، ولا تكرر أسعار السيارة أو تقييمها.</p>"
         "<h2>حدود النشرة الرسمية</h2>"
         "<p>تستند هذه البيانات إلى النشرة المنشورة لدى هيونداي مصر التي تعرض تجهيزات GL وSR و"
         "DAB-ABS وDAB-ABS PLUS وHighline. تأكد من مطابقة الفئة الفعلية عند الاختلاف بين "
         "سنوات الإنتاج أو السيارات المستخدمة أو المعدلة.</p>"
        )
    return (
      "<p>"+escape(row["intro"])+"</p>"
      "<h2>"+escape(row["factGroup"])+" في النشرة الرسمية</h2><p>"+escape(row["detail"])+"</p>"
      "<h2>قبل الشراء أو الصيانة</h2><p>"+escape(row["warning"])+"</p>"
      "<h2>لماذا ينبغي التأكد من الفئة؟</h2>"
      "<p>هذه الأرقام مستخرجة من نشرة أكسنت RB المصرية، وليست بيانات لجميع أجيال هيونداي "
      "أكسنت أو نسخها المستوردة. بعض التجهيزات تختلف بين GL وSR وDAB-ABS وHighline. "
      "يُرجع إلى ملصقات السيارة ورقم الشاسيه وكتيب المالك عند شراء الإطارات أو أجزاء الفرامل. "
      "وبخلاف النشرة، لا نفترض أرقام زيت محرك أو زيت فتيس أو ضغط إطارات غير منشورة.</p>"
      "<p><strong>المصدر:</strong> <a href='"+escape(row["source"],quote=True)+
      "' rel='noopener nofollow noreferrer'>نشرة مواصفات أكسنت RB الرسمية من هيونداي مصر</a>.</p>"
    )

def entry(kind,row,parent,media_id):
    source=DATA["model"]["source"] if kind=="model" else row["source"]
    facts=[{"label":x,"value":y} for x,y in row.get("facts",[])]
    data={"kind":kind,"market":"مصر - نشرة هيونداي أكسنت RB المحلية",
      "years":"نشرة طراز 2025؛ مراجعة فئة وسنة السيارة الفعلية",
      "engine":row.get("engine",MODEL["engine"]),"category":row.get("category",""),
      "reviewed_at":"2026-11-03","facts":facts,
      "sources":[{"title":"النشرة الفنية الرسمية: أكسنت RB - غبور وهيونداي مصر","url":source}]}
    return {"title":row["title"],"slug":row["slug"],"kind":kind,"parent_path":parent,
      "status":"publish","featured_image_id":media_id,"content":content(kind,row),"data":data,
      "excerpt":"مواصفات أكسنت RB بمصر من نشرة غبور: كاوتش ومحرك وأبعاد وفروق الأمان حسب الفئة.",
      "meta_title":row["title"]+" | أعطال.كوم",
      "meta_description":("تعرف على "+row["title"]+" بالرجوع إلى نشرة أكسنت RB الرسمية في مصر، مع فروق الفئات والتنبيهات الفنية.")[:155]}

def check_live(url,filename,title):
    for n in range(7):
        try:
            r=get(url,params={"accent_audit":str(time.time_ns())},headers={"Cache-Control":"no-cache"})
            if r.url.split("?")[0].rstrip("/")!=url.rstrip("/"):raise RuntimeError("unexpected redirect")
            html=r.text
            if title not in html or filename not in html:raise RuntimeError("title/featured not visible")
            og=re.search(r'<meta[^>]+property=["\x27]og:image["\x27][^>]+content=["\x27]([^"\x27]+)',html,re.I)
            if not og or filename not in og.group(1):raise RuntimeError("wrong OG")
            c=re.search(r'<link[^>]+rel=["\x27]canonical["\x27][^>]+href=["\x27]([^"\x27]+)',html,re.I)
            if not c or c.group(1).rstrip("/")!=url.rstrip("/"):raise RuntimeError("wrong canonical")
            if "noindex" in html[:14000].lower():raise RuntimeError("noindex")
            return True
        except Exception as e:
            if n==6:raise RuntimeError("Live verification failed "+url+" "+str(e))
            time.sleep(3)

def main():
    assert len(DATA["items"])==4 and len(ITEMS)==5
    assert len({x["slug"] for kind,x,parent in ITEMS})==5
    limit=max(1,min(5,int(os.getenv("A3CR_LIMIT","1"))))
    hyundai=existing("hyundai")
    if len(hyundai)!=1 or hyundai[0]["link"].rstrip("/")!=BASE+"/car-reference/hyundai":
        raise RuntimeError("Hyundai brand does not exist; abort")
    photos=find_photographs()
    try:
        for i,(kind,row,parent) in enumerate(ITEMS[:limit]):
            slug=row["slug"]
            url=BASE+"/car-reference/"+parent+"/"+slug+"/"
            found=existing(slug)
            if found:
                if len(found)!=1 or found[0]["link"].rstrip("/")!=url.rstrip("/"):
                    raise RuntimeError("Conflicting slug "+slug)
                RESULTS.append({"slug":slug,"url":url,"status":"already-live"})
                print("SKIP existing",url,flush=True)
                continue
            photo,master_url=photos[i%len(photos)]
            bytes_=render_cover(photo,kind,row,i)
            filename="a3tal-accent-rb-egypt-2025-"+slug+".webp"
            media=post(MEDIA,{"filename":filename,"image_base64":base64.b64encode(bytes_).decode("ascii"),
                "title":row["title"],"alt":row["title"]+" - تصميم فني لأعطال.كوم",
                "convert_webp":False})
            image_id=int(media.get("media_id") or 0)
            if not image_id:raise RuntimeError("No uploaded media id "+slug)
            payload=entry(kind,row,parent,image_id)
            try:
                output=post(UPSERT,{"items":[payload]})
            except requests.RequestException:
                # Do not duplicate after uncertain network loss.
                preexisting=existing(slug)
                if len(preexisting)==1 and preexisting[0]["link"].rstrip("/")==url.rstrip("/"):
                    output={"results":[{"ok":True,"status":"publish","url":url,"id":preexisting[0]["id"]}]}
                else:output=post(UPSERT,{"items":[payload]})
            records=output.get("results") or []
            if len(records)!=1 or not records[0].get("ok") or records[0].get("status")!="publish":
                raise RuntimeError("WordPress did not publish "+slug+" "+str(records)[:240])
            if records[0]["url"].rstrip("/")!=url.rstrip("/"):
                raise RuntimeError("Wrong permalink: "+records[0]["url"])
            check_live(url,filename,row["title"])
            RESULTS.append({"slug":slug,"status":"published","url":url,
                "image":media.get("url"),"featured_id":image_id,"photo_master":master_url,
                "og_verified":True,"canonical_verified":True})
            print("PUBLISHED VERIFIED",url,"image",image_id,flush=True)
    finally:
        REPORT.write_text(json.dumps({"results":RESULTS},ensure_ascii=False,indent=2),encoding="utf8")
    assert len(RESULTS)==limit
    print("COMPLETE",len(RESULTS),"ACCENT RB RECORDS",flush=True)

if __name__=="__main__":main()
