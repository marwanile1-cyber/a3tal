#!/usr/bin/env python3
"""A3tal Hyundai CN7 2025 reference batch.
Publishes only source-checked Hyundai data with a unique WebP editorial cover for
each page. It re-composes photography from the user's OWN A3tal website.
One model across regional trim variants; never claim all engines sold in Egypt.
Protects live pages and checks actual current featured photo and Yoast og:image.
"""
import base64, io, json, os, re, sys, time, hashlib
from html import escape
from pathlib import Path
from urllib.parse import urlparse
import requests
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/"data/car-reference/batch-04-hyundai-cn7-2025-official.json").read_text(encoding="utf-8"))
BASE="https://a3tal.com"
API=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
BRIDGE=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
KEY=os.environ["A3TAL_API_KEY"]
HEAD={"Content-Type":"application/json","X-A3tal-Key":KEY}
S=requests.Session()
S.headers["User-Agent"]="A3tal-Hyundai-CN7-Editorial-2026-11-03/1.0"
REPORT=ROOT/"car-reference-batch04-hyundai-publishing.json"
RESULTS=[]
STAMP="2026-11-03"
PATHS=[
 ("brand",{"slug":CONFIG["brand"]["slug"],"title":CONFIG["brand"]["title"]},""),
 ("model",{"slug":CONFIG["model"]["slug"],"title":CONFIG["model"]["title"]},"hyundai")
]+[("spec",r,"hyundai/elantra-cn7-2025") for r in CONFIG["items"]]
COLORS={
 "brand":(58,175,230),"model":(67,189,220),
 "engine-oil":(68,191,224),"tire-specs":(91,198,184),
 "transmission-oil":(232,153,76),"coolant":(50,178,222),
 "brake-fluid":(226,121,109)
}

def font(n,arabic=False):
    xs=(
      ["/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
      if arabic else ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    )
    for f in xs:
        if Path(f).exists():return ImageFont.truetype(f,n)
    raise RuntimeError("font unavailable")

def request_post(url,body):
    for attempt in range(4):
        try:
            r=S.post(url,headers=HEAD,json=body,timeout=145)
            if r.status_code >=500: raise requests.exceptions.RequestException("server "+str(r.status_code))
            if not r.ok: raise RuntimeError("HTTP "+str(r.status_code)+" "+r.text[:300])
            return r.json()
        except (requests.exceptions.RequestException,ValueError) as e:
            if attempt==3:raise
            time.sleep(3+attempt*3)
    raise RuntimeError("post failure")

def get_posts(slug):
    for attempt in range(3):
        try:
            r=S.get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":30},timeout=50)
            r.raise_for_status()
            return [x for x in r.json() if x.get("slug")==slug]
        except requests.exceptions.RequestException:
            if attempt==2:raise
            time.sleep(2+attempt*2)

def image_master():
    imgs=[]
    for u in (CONFIG["image_source"]["preferred"],CONFIG["image_source"]["fallback"]):
        try:
            r=S.get(u,timeout=55,headers={"Accept":"image/webp,image/jpeg,image/png,*/*"})
            r.raise_for_status()
            if len(r.content)<15000: raise RuntimeError("image too small in bytes")
            im=Image.open(io.BytesIO(r.content)).convert("RGB")
            if min(im.size)<460 or max(im.size)<850: raise RuntimeError("image resolution too low "+str(im.size))
            print("SOURCE OK",urlparse(u).path[-60:],"pixels",im.size,flush=True)
            return im,u
        except Exception as e:
            print("SOURCE candidate rejected:",str(e)[:190],flush=True)
            continue
    raise RuntimeError("No acceptable image from the site's already published, owned Hyundai photos. Not publishing without photography.")

def cover(master,kind,row,order):
    title=row["title"]
    key=row["slug"]
    accent=COLORS.get(row.get("category",kind),(57,183,221))
    angle=(order%3)
    # Different grade, car photo placement and content-specific technical focus
    canvas=Image.new("RGB",(1600,900),(8,20,33))
    src=ImageOps.fit(master,(1330,800),method=Image.Resampling.LANCZOS,centering=(0.45+0.04*angle,0.50))
    src=src.filter(ImageFilter.UnsharpMask(radius=1.7,percent=135,threshold=2))
    canvas.paste(src,(-130+38*angle,92))
    overlay=Image.new("RGBA",(1600,900),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    for x in range(420,1600,3):
        mix=(x-420)/1180
        alpha=min(255,int(46+211*mix))
        d.rectangle((x,0,x+3,900),fill=(3+int(4*mix),14+int(6*mix),28+int(8*mix),alpha))
    d.rectangle((0,0,1600,102),fill=(5,15,30,237))
    d.rectangle((0,826,1600,900),fill=(5,15,30,244))
    d.rounded_rectangle((958,284,1545,690),radius=32,fill=(13,34,52,227),outline=(*accent,255),width=4)
    d.rectangle((972,214,1544,221),fill=(*accent,248))
    for r in (50,76,100):
        d.ellipse((1250-r,765-r,1250+r,765+r),outline=(*accent,25),width=2)
    d.ellipse((1465,743,1484,762),fill=(*accent,210))
    # Distinct high-res typography, no promos and no unverified data on the cover.
    canvas=Image.alpha_composite(canvas.convert("RGBA"),overlay)
    t=ImageDraw.Draw(canvas)
    t.text((73,57),"HYUNDAI  /  TECHNICAL REFERENCE",font=font(23),fill=(221,236,249))
    if kind=="brand":
        main="HYUNDAI";unit="TECHNICAL CAR DATA";ar="دليل المواصفات الفنية"
    elif kind=="model":
        main="ELANTRA CN7";unit="MODEL YEAR 2025";ar="الزيوت والمقاسات حسب المحرك"
    else:
        main=str(row.get("metric","CN7 2025"))
        unit=str(row.get("subtitle","OWNER MANUAL 2025"))
        ar={
          "engine-oil":"كمية زيت المحرك",
          "tire-specs":"مقاس وضغط الإطارات",
          "transmission-oil":"مواصفات زيت الفتيس",
          "coolant":"سعة دورة التبريد",
          "brake-fluid":"مواصفة سائل الفرامل"
        }.get(row.get("category"),"مواصفات فنية موثقة")
    t.text((1501,384),main,font=font(65 if len(main)>11 else 91),fill=(246,251,254),anchor="ra")
    t.text((1495,491),unit[:26],font=font(34),fill=accent,anchor="ra")
    try:
        t.text((1498,601),ar,font=font(33,True),fill=(212,230,238),anchor="ra",direction="rtl")
    except Exception:
        t.text((1498,601),"OFFICIAL SERVICE DATA",font=font(26),fill=(212,230,238),anchor="ra")
    t.text((1510,867),"A3TAL.COM",font=font(26),fill=(230,240,248),anchor="ra")
    b=io.BytesIO()
    canvas.convert("RGB").save(b,"WEBP",quality=90,method=5)
    result=b.getvalue()
    if len(result)<65000: raise RuntimeError("Poor photo composition: "+str(len(result)))
    return result

def html_content(kind,row):
    if kind=="brand":
        return (
           "<p>يقدم دليل هيونداي في أعطال.كوم المواصفات الفنية الخاصة بالزيوت والسعات والإطارات وسوائل أنظمة السيارة. "
           "القيم مستخرجة من أدلة المالك الأصلية، وتختلف بحسب سنة الإصدار وكود المحرك ونوع ناقل الحركة والسوق.</p>"
           "<h2>اختيار الموديل والمحرك</h2>"
           "<p>ابدأ بتحديد السيارة والجيل، ثم اختر المحرك ونظام نقل الحركة. "
           "لا تعمم سعة فتيس IVT على أوتوماتيك AT أو كمية زيت محرك Smartstream على D-CVVT؛ فقد تتغير البيانات داخل الجيل نفسه.</p>"
           "<h2>التحقق من مواصفات السوق المصري</h2>"
           "<p>الكتالوج العالمي يذكر الشرق الأوسط بما فيه مصر في مواضع محددة. "
           "مع ذلك قد لا تتوافر كل نسخة محرك أو تجهيز في مصر، لذا تُراجع البيانات على ملصقات السيارة ودليلها المرتبط برقم الشاسيه.</p>"
        )
    if kind=="model":
        return (
           "<p>يجمع هذا الدليل البيانات الفنية المتنوعة لهيونداي إلنترا CN7 موديل 2025 وفق نسخة دليل المالك الرسمي لعام 2025، "
           "ويفصل المحركات Smartstream G1.6 و1.6 D-CVVT، وأنواع ناقل الحركة AT وIVT، وسعات السوائل والمقاسات.</p>"
           "<h2>كيف تختار صفحة المواصفة الصحيحة؟</h2>"
           "<p>تحقق من كود المحرك وحروف ناقل الحركة على السيارة قبل اختيار الكمية أو مواصفة الزيت. "
           "بعض الخيارات المذكورة في الدليل الدولي قد لا تُطرح في السوق المصري بنفس التجهيزات.</p>"
           "<h2>الفرق بين دليل المواصفات وجدول الصيانة</h2>"
           "<p>هذا القسم يوضح <strong>ما السعة أو المواصفة المطلوبة؟</strong>، ولا يكرر "
           "مواعيد الصيانة الدورية أو أسعار السيارات الموجودة في مقالات أعطال الأخرى. "
           "ارجع إلى جدول الصيانة الخاص بسوق سيارتك لمعرفة موعد تغيير السوائل.</p>"
        )
    return (
      "<p>"+escape(row["intro"])+"</p>"
      "<h2>مواصفات النسخة المحددة</h2><p>"+escape(row["detail"])+"</p>"
      "<h2>متى يختلف الرقم؟</h2><p>"+escape(row["warning"])+"</p>"
      "<h2>التحقق قبل الصيانة</h2>"
      "<p>طابق سنة الطراز وكود المحرك ونوع ناقل الحركة مع كتالوج السيارة ولوحة البيانات. "
      "الكمية المرجعية للنظام ليست بالضرورة كمية التعبئة في صيانة جزئية. "
      "الأولوية دائماً لتعليمات القياس ومستوى السائل الصادرة عن الشركة المصنعة.</p>"
      "<p>المصدر: <a href='"+escape(row["source"],quote=True)+
      "' rel='nofollow noopener noreferrer'>دليل مالك هيونداي إلنترا CN7 لعام 2025: جدول المواصفات الرسمي</a>.</p>"
    )

def entry(kind,row,parent,media):
    if kind=="brand":
        source=CONFIG["brand"]["url"]; facts=[]; engine=""
    elif kind=="model":
        source=CONFIG["model"]["source"];facts=[];engine=""
    else:
        source=row["source"];facts=[{"label":a,"value":b} for a,b in row["facts"]];engine=row["engine"]
    data={"kind":kind,"market":CONFIG["market"],"years":"2025" if kind!="brand" else "حسب سنة إصدار الدليل",
          "engine":engine,"category":row.get("category",""),
          "reviewed_at":STAMP,"facts":facts,
          "sources":[{"title":"دليل هيونداي الرسمي "+("2025" if kind!="brand" else ""), "url":source}]}
    return {"title":row["title"],"slug":row["slug"],"kind":kind,
      "parent_path":parent,"status":"publish","featured_image_id":media,
      "content":html_content(kind,row),
      "excerpt":"معلومات فنية من دليل مالك هيونداي الرسمي حسب نوع المحرك والتجهيز والسوق.",
      "data":data,"meta_title":row["title"]+" | أعطال.كوم",
      "meta_description":("تعرف على "+row["title"]+" من كتالوج هيونداي الرسمي، مع السعات والمقاسات والفروق بين المحركات وملاحظات السلامة.")[:155]}

def check(url,image_name,title):
    for attempt in range(6):
        try:
            r=S.get(url,params={"verify_hyundai_cn7":str(time.time_ns())},timeout=60,headers={"Cache-Control":"no-cache"})
            r.raise_for_status()
            page=r.text
            if r.url.split("?")[0].rstrip("/")!=url.rstrip("/"):raise RuntimeError("redirected")
            if title not in page:raise RuntimeError("no title")
            if image_name not in page:raise RuntimeError("image not in content")
            found=re.search(r'<meta[^>]+property=["\x27]og:image["\x27][^>]+content=["\x27]([^"\x27]+)',page,re.I)
            if not found or image_name not in found.group(1):raise RuntimeError("wrong OG image")
            canon=re.search(r'<link[^>]+rel=["\x27]canonical["\x27][^>]+href=["\x27]([^"\x27]+)',page,re.I)
            if not canon or canon.group(1).rstrip("/")!=url.rstrip("/"):raise RuntimeError("wrong canonical")
            if "noindex" in page[:15000].lower():raise RuntimeError("noindex")
            return True
        except Exception as exc:
            if attempt==5:raise
            time.sleep(3)

def main():
    assert len(CONFIG["items"])==7
    assert len(PATHS)==9
    assert len({r["slug"] for k,r,p in PATHS})==len(PATHS)
    cap=max(1,min(9,int(os.getenv("A3CR_LIMIT","1"))))
    master,original_url=image_master()
    print("SOURCE IMAGE:",original_url,"source hash",hashlib.sha256(master.tobytes()).hexdigest()[:14],flush=True)
    try:
        for order,(kind,row,parent) in enumerate(PATHS[:cap]):
            slug=row["slug"]
            path=parent+"/"+slug if parent else slug
            expected=BASE+"/car-reference/"+path+"/"
            current=[p for p in get_posts(slug) if p["status"]=="publish"]
            if current:
                if len(current)!=1 or current[0]["link"].rstrip("/")!=expected.rstrip("/"):
                    raise RuntimeError("Duplicate or incorrect existing path for "+slug)
                print("SKIP existing live",expected,flush=True)
                RESULTS.append({"slug":slug,"url":expected,"status":"already-live"})
                continue
            raw=cover(master,kind,row,order)
            filename="a3tal-hyundai-cn7-premium-"+slug+".webp"
            media_result=request_post(BRIDGE,{
              "image_base64":base64.b64encode(raw).decode("ascii"),
              "filename":filename,"convert_webp":False,
              "title":row["title"],"alt":row["title"]+" - تصميم فني حصري لأعطال.كوم"})
            media=int(media_result.get("media_id") or 0)
            if not media:raise RuntimeError("No uploaded media id for "+slug)
            response=request_post(API,{"items":[entry(kind,row,parent,media)]})
            items=response.get("results") or []
            if len(items)!=1 or not items[0].get("ok") or items[0].get("status")!="publish":
                raise RuntimeError("Post was not accepted "+slug+" "+str(items)[:250])
            newurl=items[0]["url"]
            if newurl.rstrip("/")!=expected.rstrip("/"):raise RuntimeError("Wrong permalink "+newurl)
            check(expected,filename,row["title"])
            print("LIVE VERIFIED",expected,"featured",media,flush=True)
            RESULTS.append({"slug":slug,"url":newurl,"featured_media":media,
                "image":media_result.get("url"),"status":"published","canonical_og_checked":True})
    finally:
        REPORT.write_text(json.dumps({"source_url":original_url,"results":RESULTS},ensure_ascii=False,indent=2),encoding="utf-8")
    assert len(RESULTS)==cap
    print("COMPLETE",len(RESULTS),flush=True)

if __name__=="__main__": main()
