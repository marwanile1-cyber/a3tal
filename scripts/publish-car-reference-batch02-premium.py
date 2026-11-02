#!/usr/bin/env python3
"""A3tal image-gated batch 02: upgrade seven documented Kia drafts to live.
All imagery is newly composed from the existing ChatGPT-made photographic Kia
master assets already approved and held in this repository. No vector-only art.
Never overwrites an already published post; every live URL and image is verified.
"""
import base64
import io
import json
import os
import re
import time
from html import escape
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/car-reference/batch-02-kia-image-gated-drafts.json"
PHOTOS = ROOT / "assets/car-reference-replacements"
BASE = "https://a3tal.com"
KEY = os.environ["A3TAL_API_KEY"]
BRIDGE = BASE + "/wp-json/a3tal-direct/v1"
UPSERT = BASE + "/wp-json/a3tal-car-reference/v1/upsert"
S = requests.Session()
S.headers["User-Agent"] = "A3tal-Reference-Batch02-Premium/1.0"
HEAD = {"X-A3tal-Key": KEY, "Content-Type": "application/json"}
REPORT = ROOT / "car-reference-batch02-premium-report.json"
RESULTS = []

# A source photo is one of the five ChatGPT-created high-quality Kia editorials
# already installed and reviewed; the resulting page-specific artwork is distinct.
DESIGNS = {
  "cerato-ivt-smartstream-16": ("cerato-bd-2023.webp","كيا سيراتو 2023","زيت فتيس IVT","6.7 L","SP-CVT",(38,188,236),0),
  "cerato-brake-fluid-dot4": ("cerato-engine-oil-16-mpi.webp","كيا سيراتو 2023","سائل الفرامل","DOT 4 LV","0.7–0.8 L",(236,100,91),1),
  "seltos-coolant-16-tgdi": ("seltos-sp2-2023.webp","كيا سيلتوس 2023","سائل تبريد محرك 1.6 تيربو","7.0 L","سعة نظام التبريد",(32,191,188),0),
  "seltos-awd-rear-differential-oil": ("seltos-sp2-2023.webp","كيا سيلتوس AWD","زيت الدفرنس الخلفي","0.5 L","SAE 75W/85",(225,152,78),1),
  "sportage-awd-rear-differential-oil": ("sportage-nq5-2023.webp","كيا سبورتاج NQ5","زيت الدفرنس الخلفي","0.53–0.63 L","SAE 75W/85",(225,162,71),0),
  "sportage-coolant-25-gdi": ("sportage-nq5-2023.webp","كيا سبورتاج 2023","تبريد محرك 2.5 GDI","9.1 L","سعة دورة التبريد",(50,190,210),1),
  "sportage-diesel-adblue-20": ("sportage-nq5-2023.webp","كيا سبورتاج ديزل","محلول AdBlue 2.0","14 L","ISO 22241",(86,167,245),2)
}
def font(name, size):
    candidates={
      "ar": ["/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
      "en": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    }[name]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p,size)
    raise RuntimeError("Missing font " + name)

def make_art(slug):
    filename, car, topic, metric, descriptor, accent, variant=DESIGNS[slug]
    photo=Image.open(PHOTOS / filename).convert("RGB")
    if photo.width < 1100:
        raise RuntimeError("Master photograph too small for " + slug)
    if variant == 2:
        photo=ImageOps.mirror(photo)
    # Recompose the car scene: source title banners cropped out, never replayed.
    left=photo.crop((0,220,785,676))
    left=ImageOps.fit(left,(1220,780),Image.Resampling.LANCZOS,centering=(0.50,0.48))
    left=left.filter(ImageFilter.UnsharpMask(radius=1.7,percent=135,threshold=3))
    canvas=Image.new("RGB",(1600,900),(5,17,30))
    canvas.paste(left,(-95,96))
    overlay=Image.new("RGBA",(1600,900))
    d=ImageDraw.Draw(overlay)
    for x in range(470,1600,4):
        alpha=min(253,47+int(211*(x-470)/1130))
        d.rectangle((x,0,x+4,900),fill=(5,18,33,alpha))
    d.rectangle((0,0,1600,108),fill=(4,13,26,242))
    d.rectangle((0,785,1600,900),fill=(4,13,26,240))
    x1,y1,x2,y2=1023,294,1537,623
    d.rounded_rectangle((x1,y1,x2,y2),radius=29,fill=(15,34,52,240),outline=(*accent,242),width=4)
    d.rectangle((x2-16,y1+3,x2,y2-3),fill=(*accent,250))
    d.rectangle((1010,166,1537,171),fill=(*accent,255))
    # Small, non-distracting original technical circles.
    for r in (66,86,110):
        d.ellipse((1370-r,710-r,1370+r,710+r),outline=(*accent,32),width=3)
    canvas=Image.alpha_composite(canvas.convert("RGBA"),overlay)
    t=ImageDraw.Draw(canvas)
    arabic=font("ar",48)
    arabic_sm=font("ar",39)
    t.text((1523,77),car,font=arabic,fill=(248,251,255),anchor="ra",direction="rtl")
    t.text((1523,225),topic,font=arabic_sm,fill=(210,229,239),anchor="ra",direction="rtl")
    latin_size=69 if len(metric)>9 else 94
    t.text((1492,415),metric,font=font("en",latin_size),fill=(252,254,255),anchor="ra")
    # Descriptor can be Arabic or Latin; avoid mixing digits into Arabic font.
    if re.search(r"[A-Za-z]",descriptor):
        t.text((1491,545),descriptor,font=font("en",38),fill=(*accent,),anchor="ra")
    else:
        t.text((1491,545),descriptor,font=font("ar",34),fill=(*accent,),anchor="ra",direction="rtl")
    t.text((1523,844),"A3TAL.COM  /  CAR REFERENCE",font=font("en",26),fill=(226,235,241),anchor="ra")
    t.text((70,55),"KIA  /  SERVICE DATA",font=font("en",23),fill=(215,237,248))
    out=io.BytesIO()
    canvas.convert("RGB").save(out,"WEBP",quality=87,method=5)
    return out.getvalue()

def req(url, payload, timeout=160):
    for attempt in range(3):
        r=S.post(url,headers=HEAD,json=payload,timeout=timeout)
        if r.status_code >= 500 and attempt < 2:
            time.sleep(4*(attempt+1))
            continue
        if not r.ok:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:280]}")
        return r.json()
    raise RuntimeError("Retries exhausted")

def existing_public(slug):
    r=S.get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":20},timeout=45)
    r.raise_for_status()
    return [p for p in r.json() if p.get("slug")==slug and p.get("status")=="publish"]

def entry(row, source, media_id):
    content=(
        "<p>"+escape(row["intro"])+"</p>"
        "<h2>المواصفات الرسمية لنسخة السيارة</h2><p>"+escape(row["detail"])+"</p>"
        "<h2>متى تختلف القيمة بين الفئات؟</h2><p>"+escape(row["warning"])+"</p>"
        "<h2>مراجعة المعلومات قبل الصيانة</h2>"
        "<p>ابدأ بمطابقة رمز المحرك ونوع ناقل الحركة والجيل وسوق السيارة مع دليل المالك. "
        "الأرقام المعروضة مواصفات للنسخة الواردة في الدليل؛ وقد تختلف كمية التعبئة الفعلية بعد التفريغ الجزئي. "
        "راجع إجراءات القياس الفنية لدى مركز خدمة مختص قبل إضافة السوائل أو شراء قطع الغيار.</p>"
        "<p><strong>المصدر:</strong> <a href='"+escape(source,quote=True)+
        "' rel='nofollow noopener noreferrer'>دليل المالك الرسمي لكيا لسنة 2023، جدول السوائل والسعات</a>.</p>"
    )
    data={"kind":"spec",
      "market":"النسخة الواردة في دليل كيا 2023؛ الشرق الأوسط ومصر عندما يذكرهما المصدر",
      "years":"2023","engine":row["engine"],"category":row["category"],
      "reviewed_at":"2026-11-02",
      "facts":[{"label":k,"value":v} for k,v in row["facts"]],
      "sources":[{"title":"دليل المالك الرسمي لكيا "+row["model"]+" 2023","url":source}]}
    return {"kind":"spec","slug":row["slug"],"title":row["title"],
      "parent_path":"kia/"+row["model"],"status":"publish",
      "featured_image_id":media_id,"content":content,
      "excerpt":"المواصفات الفنية الرسمية والسعات حسب المحرك والناقل من دليل كيا 2023.",
      "data":data,
      "meta_title":row["title"]+" | أعطال.كوم",
      "meta_description":("تفاصيل "+row["title"]+" حسب دليل كيا الرسمي 2023؛ السعة والمواصفة والمحرك والتنبيهات قبل الصيانة.")[:155]}

def verify(url, image_url, expected_title):
    for attempt in range(7):
        try:
            x=S.get(url,params={"v":str(int(time.time()))},timeout=55)
            if not x.ok:
                raise RuntimeError("Page HTTP "+str(x.status_code))
            if x.url.split("?")[0].rstrip("/") != url.rstrip("/"):
                raise RuntimeError("Unexpected redirect to "+x.url)
            html=x.text
            if expected_title not in html: raise RuntimeError("Title missing")
            if image_url.split("/")[-1].lower() not in html.lower():raise RuntimeError("New image missing in HTML")
            if "noindex" in html[:10000].lower():raise RuntimeError("Noindex on published page")
            if not re.search(r'<meta[^>]+property=["\x27]og:image["\x27][^>]+content=["\x27][^"\x27]*'+re.escape(image_url.split("/")[-1])+r'[^"\x27]*',html,re.I):
                raise RuntimeError("og:image not using page-specific image")
            if not re.search(r'<link[^>]+rel=["\x27]canonical["\x27][^>]+href=["\x27]'+re.escape(url.rstrip("/"))+r'/?["\x27]',html,re.I):
                raise RuntimeError("Wrong canonical")
            return True
        except Exception as exc:
            if attempt == 6: raise
            time.sleep(4)
    return False

def main():
    manifest=json.loads(MANIFEST.read_text(encoding="utf8"))
    rows=manifest["items"]
    assert len(rows)==7 and len({r["slug"] for r in rows})==7
    assert set(DESIGNS)=={r["slug"] for r in rows}
    for f in {x[0] for x in DESIGNS.values()}:
        assert (PHOTOS/f).is_file(), "Missing previously approved premium photo "+f
    limit=max(1,min(7,int(os.getenv("A3CR_LIMIT","7"))))
    print("Publishing cap:",limit,flush=True)
    try:
        for row in rows[:limit]:
            slug=row["slug"]
            old=existing_public(slug)
            if old:
                print("SKIP already published:",old[0]["link"],flush=True)
                RESULTS.append({"slug":slug,"status":"already-published","url":old[0]["link"]})
                continue
            raw=make_art(slug)
            if len(raw)<55000:
                raise RuntimeError("Image quality gate: output image too small for "+slug)
            filename="a3tal-kia-premium-"+slug+".webp"
            upload=req(BRIDGE+"/upload-image-data",{
                "image_base64":base64.b64encode(raw).decode("ascii"),
                "filename":filename,"title":row["title"],"alt":row["title"]+" - تصميم خاص بأعطال.كوم",
                "convert_webp":False
            })
            media=int(upload.get("media_id") or 0)
            if not media:raise RuntimeError("No media id for "+slug)
            data=entry(row,manifest["models"][row["model"]],media)
            result=req(UPSERT,{"items":[data]})
            records=result.get("results") or []
            if not records or not records[0].get("ok") or records[0].get("status")!="publish":
                raise RuntimeError("Publishing failed "+slug+": "+str(records)[:350])
            url=records[0]["url"]
            verify(url,upload["url"],row["title"])
            RESULTS.append({"slug":slug,"status":"published","post_id":records[0]["id"],"url":url,
                            "image_id":media,"image_url":upload["url"],"og_checked":True})
            print("PUBLISHED AND VERIFIED",slug,url,"image_id",media,flush=True)
    finally:
        REPORT.write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2),encoding="utf8")
    print("Finished",len(RESULTS),"records",flush=True)

if __name__=="__main__":
    main()
