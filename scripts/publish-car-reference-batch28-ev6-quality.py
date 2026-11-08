#!/usr/bin/env python3
"""Publish source-grounded high-quality Kia EV6 Electric Egypt PSEO with unique substantive editorial content.

Use only GitHub Actions -> A3tal Direct Bridge; do not call WPWriter.
1 model hub + 6 differentiated non-overlapping detailed technical guides; Kia brand hub preserved.
Every page has an individually composed, photographic 1600x900 WebP based on
real Kia Egypt manufacturer photographs; copyright remains with the manufacturer.
Never guess workshop oil capacities or use conflicting official fuel figures.
Stop on any source/photo/SEO check failure and keep the output audit.
"""
import base64, hashlib, io, json, os, re, time
from html import escape
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat
import requests

ROOT=Path(__file__).resolve().parents[1]
DB=json.loads((ROOT/"data/car-reference/batch-28-kia-ev6-egypt-quality.json").read_text(encoding="utf8"))
FAMILY=os.environ.get("A3CR_FAMILY","captiva")
GROUP=next((x for x in DB["clusters"] if x["key"]==FAMILY),None)
if GROUP is None:raise RuntimeError("Unknown cluster: "+FAMILY)
BASE="https://a3tal.com"
S=requests.Session()
S.headers.update({"User-Agent":"A3tal-Reference-Batch12-Official-Photo/1.0"})
AUTH={"X-A3tal-Key":os.environ["A3TAL_API_KEY"],"Content-Type":"application/json"}
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
REPORT=ROOT/("car-reference-batch28-"+FAMILY+"-audit.json")
MODE=GROUP["model"]
ITEMS=[("brand",{"slug":GROUP["brand"],"title":GROUP["brand_title"],"engine":MODE["engine"],"sources":GROUP["brand_sources"],"intro":GROUP["brand_intro"],"detail":GROUP["brand_detail"],"warning":GROUP["brand_warning"]},""),("model",MODE,GROUP["brand"])]+[("spec",p,GROUP["brand"]+"/"+MODE["slug"]) for p in GROUP["specs"]]
PROGRESS=[]
CATEGORY_NAMES={"engine-specs":"المحرك وناقل الحركة","tire-specs":"الإطارات والجنوط","dimensions":"الأبعاد والقياسات","seating":"المقاعد والشنطة","safety-specs":"الفرامل والأمان","infotainment":"التجهيزات والتكنولوجيا","adas-specs":"مساعدات القيادة","parking-tech":"أنظمة الركن","hybrid-powertrain":"مجموعة الدفع الهجينة","hybrid-battery":"بطارية النظام الهجين","charging":"شحن البطارية","charging-devices":"شحن الأجهزة","performance":"التسارع والأداء","fuel-specs":"استهلاك الوقود وخزان البنزين","trim-features":"فروق الفئات","exterior-specs":"التجهيزات الخارجية","interior-specs":"المقصورة والتكييف","capacity":"الحمولة والمقاعد","safety-tech":"أنظمة الثبات","chassis-specs":"التعليق والشاسيه","hybrid-range":"مدى القيادة","infotainment-chip":"المعالج الرقمي","offroad":"قدرات القيادة الوعرة","cargo-fuel":"الأمتعة وخزان الوقود","braking-tech":"الفرامل والثبات","luggage-volume":"حجم الأمتعة","transmission-specs":"ناقل الحركة"}
ACCENTS={"kia-ev6":(93,151,185),"mg-newzs":(75,163,197),"geely-starray":(98,164,190),"jetour-t2-idm-4wd":(91,154,200),"chery-tiggo9-phev":(135,151,179),"renault-boreal":(187,136,77),"opel-frontera":(180,138,87)}
MARK_NAMES={"kia-ev6":"KIA EV6 ELECTRIC EGYPT","mg-newzs":"MG NEW ZS 1.5 CVT","geely-starray":"GEELY STARRAY 1.5T","jetour-t2-idm-4wd":"JETOUR T2 i-DM 4WD","chery-tiggo9-phev":"CHERY TIGGO9 PHEV","renault-boreal":"RENAULT BOREAL 2027","opel-frontera":"OPEL FRONTERA 2027"}
assert len(DB["clusters"])==1 and len(ITEMS)==8
assert len({p["slug"] for _,p,_ in ITEMS})==len(ITEMS)

def get(url, **kwargs):
    for n in range(4):
        try:
            r=S.get(url,timeout=70,**kwargs)
            r.raise_for_status()
            return r
        except requests.RequestException as exc:
            if n==3:raise
            print("GET retry",n,url,str(exc)[:110],flush=True)
            time.sleep(3*(n+1))

def post(url,payload):
    for n in range(4):
        try:
            r=S.post(url,headers=AUTH,json=payload,timeout=180)
            if r.status_code>=500:raise requests.RequestException("Transient "+str(r.status_code))
            if not r.ok:raise RuntimeError("HTTP "+str(r.status_code)+" "+r.text[:340])
            return r.json()
        except requests.RequestException:
            if n==3:raise
            time.sleep(4+4*n)

def records(slug):
    r=get(BASE+"/wp-json/wp/v2/car-reference-records",
          params={"slug":slug,"per_page":20})
    return [p for p in r.json() if p.get("slug")==slug and p.get("status")=="publish"]

def font(size):
    for fn in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",):
        if Path(fn).exists():return ImageFont.truetype(fn,size)
    return ImageFont.load_default()

_PHOTO_CHOICE={}
_PHOTO_USED=set()
def download_photo(index=0):
    if index in _PHOTO_CHOICE:
        return _PHOTO_CHOICE[index]
    candidates=GROUP["photos"]
    for shift in range(len(candidates)):
        url=candidates[(index+shift)%len(candidates)]
        if url in _PHOTO_USED and len(_PHOTO_USED)<len(candidates):
            continue
        if not url.startswith("https://www.kia.com.eg/img/ev6/"):
            continue
        if url.rsplit(".",1)[-1].lower() not in ("webp","avif"):
            continue
        try:
            raw=get(url).content
            if len(raw)<10000:raise RuntimeError("Invalid or tiny photographic file "+str(len(raw)))
            image=Image.open(io.BytesIO(raw)).convert("RGB")
            print("SOURCE_PHOTO_AUDIT",index,len(raw),image.size,url,flush=True)
            if min(image.size)<550 or max(image.size)<900:
                raise RuntimeError("Source below real-photograph dimensions "+str(image.size))
            stat=ImageStat.Stat(image.resize((64,64)))
            if max(stat.stddev)<18:
                raise RuntimeError("Low-detail or blank image")
            _PHOTO_CHOICE[index]=(image,url)
            _PHOTO_USED.add(url)
            print("KIA_EV6_REAL_OFFICIAL_PHOTO_OK",index,image.size,url,flush=True)
            return image,url
        except Exception as err:
            print("SKIP_PHOTO_CANDIDATE",index,url,type(err).__name__,str(err)[:130],flush=True)
    # If an official image is below the publication threshold, use the already verified
    # official hero rather than turning a low-resolution thumbnail into an artificial 4K file.
    for cached in _PHOTO_CHOICE.values():
        if cached[0].width>=1000:
            print("OFFICIAL_EV6_HERO_REUSED_WITH_DIFFERENT_EDITORIAL_COMPOSITION",index,flush=True)
            _PHOTO_CHOICE[index]=cached
            return cached
    raise RuntimeError("No verified EV6 manufacturer photo for page index "+str(index))

def render(photo,i,row):
    width,height=1600,900
    seed=[(0.44,0.49),(0.5,0.5),(0.54,0.52),(0.47,0.55),(0.51,0.43),(0.58,0.47)][i%6]
    # Preserve the vehicle when the owned photo is extra-wide or square.
    if photo.width / photo.height > 2.1 or photo.width / photo.height < 1.35:
        blurred=ImageOps.fit(photo,(width,height),method=Image.Resampling.LANCZOS,centering=seed)
        blurred=blurred.filter(ImageFilter.GaussianBlur(radius=22))
        main=ImageOps.contain(photo,(1550,820),method=Image.Resampling.LANCZOS)
        picture=blurred
        picture.paste(main,((width-main.width)//2,(height-main.height)//2))
    else:
        picture=ImageOps.fit(photo,(width,height),method=Image.Resampling.LANCZOS,centering=seed)
    if i%3==1:picture=ImageEnhance.Contrast(picture).enhance(1.07)
    if i%3==2:picture=ImageEnhance.Color(picture).enhance(1.06)
    picture=picture.filter(ImageFilter.UnsharpMask(radius=1.25,percent=110,threshold=3))
    overlay=Image.new("RGBA",(width,height),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    for y in range(705,900,4):
        alpha=int(160*(y-705)/195)
        d.rectangle((0,y,width,y+4),fill=(7,17,26,alpha))
    accent=ACCENTS[FAMILY]
    d.rounded_rectangle((54,47,226,92),radius=10,fill=(8,19,29,175))
    d.rectangle((58,852,1540,857),fill=(*accent,208))
    out=Image.alpha_composite(picture.convert("RGBA"),overlay)
    t=ImageDraw.Draw(out)
    t.text((70,57),"A3TAL.COM",font=font(20),fill=(248,249,251))
    t.text((68,800),MARK_NAMES[FAMILY]+"  /  OFFICIAL SPECIFICATIONS",
           font=font(24),fill=(247,249,251))
    buffer=io.BytesIO()
    out.convert("RGB").save(buffer,"WEBP",quality=88,method=5)
    v=buffer.getvalue()
    if len(v)<28000 or len(v)>3000000:raise RuntimeError("Bad WebP quality "+row["slug"]+": "+str(len(v)))
    return v

def facts_html(facts):
    lines=[]
    for a,b in facts:
        lines.append("<tr><th scope='row'>"+escape(str(a))+"</th><td>"+escape(str(b))+"</td></tr>")
    return '<div class="a3tal-responsive-table" style="overflow-x:auto"><table><tbody>'+"".join(lines)+"</tbody></table></div>"

def brand_content(row):
    return ("<p>"+escape(row["intro"])+"</p><h2>اختيار الموديل</h2><p>"+escape(row["detail"])+"</p><h2>حدود المرجع</h2><p>"+escape(row["warning"])+"</p><p>مصدر المواصفات: <a href=\'"+escape(row["sources"][0],quote=True)+"\' rel=\'nofollow noopener noreferrer\'>المصدر المرجعي</a>.</p>")

def model_content():
    name=MODE["title"]
    return (
      "<p>"+escape(MODE["intro"])+"</p>"
      "<h2>مواصفات "+escape(MARK_NAMES[FAMILY])+" الأساسية</h2>"
      "<p>"+escape(MODE["detail"])+"</p>"
      "<h2>ما الذي يغطيه الدليل الفني؟</h2>"
      "<p>تتفرع من الصفحة موضوعات مستقلة عن المحرك، ونوع ناقل الحركة، ومقاس الإطارات، "
      "والأبعاد، ووسائل الأمان، وتجهيزات المقصورة عندما تختلف نية البحث. "
      "تُعرض جداول البيانات بجانب شرح استخدام الأرقام ومتى تختلف بحسب فئة السيارة وسوقها، "
      "بدون تحويلها إلى صفحات سعر أو مراجعات مكررة.</p>"
      "<h2>قبل شراء الإطار أو تنفيذ الصيانة</h2>"
      "<p>"+escape(MODE["warning"])+"</p>"
      "<p>المصدر الفني: <a href='"+escape(MODE["sources"][0],quote=True)+
      "' rel='noopener noreferrer nofollow'>المواصفات المنشورة لهذا الموديل</a>.</p>"
    )

def spec_content(row):
    return (
      "<p>"+escape(row["intro"])+"</p>"
      "<h2>"+CATEGORY_NAMES.get(row["category"],"المواصفات الفنية")+" وفق المصدر الرسمي</h2>"
      +facts_html(row["facts"])+
      "<p>"+escape(row["detail"])+"</p>"
      "<h2>ماذا ينبغي التأكد منه قبل الشراء أو الصيانة؟</h2>"
      "<p>"+escape(row["warning"])+"</p>"
      "<h2>الجيل والفئة والسوق الصحيح</h2>"
      "<p>هذه البيانات محددة لموديل السيارة المذكور في العنوان وبحسب نشرة الشركة "
      "في السوق المصري. لا تنقل أرقام موديل أقدم أو فئة أعلى إلى سيارتك دون التأكد "
      "من رقم الشاسيه وتجهيز الفئة وملصقات السيارة وكتيب المالك. "
      "صفحات المواصفات ليست بديلًا عن خطوات الفحص ومستوى السوائل في دليل الورشة.</p>"
      "<p><strong>المرجع:</strong> <a href='"+escape(row["sources"][0],quote=True)+
      "' rel='nofollow noopener noreferrer'>كتالوج ومواصفات الشركة المصنعة</a>.</p>"
    )

def payload(kind,row,parent,photo_id):
    src=row["sources"]
    return {"kind":kind,"slug":row["slug"],"title":row["title"],
      "parent_path":parent,"featured_image_id":photo_id,"status":"publish",
      "content":(row.get("rich_html") or (brand_content(row) if kind=="brand" else model_content() if kind=="model" else spec_content(row))),
      "excerpt":"مواصفات فنية موثقة من المصدر الرسمي للموديل المصري، مع اختلاف الفئات وتنبيهات الصيانة.",
      "meta_title":row["title"]+" | أعطال.كوم",
      "meta_description":(row.get("meta_description") or ("مواصفات "+row["title"]+" والجداول الفنية التي تهم المالك."))[:155],
      "data":{"kind":kind,"market":"مصر - مرجع مُحدد المصدر والفئة",
        "years":"إصدار المرجع وتاريخ المراجعة 2026-11-08",
        "engine":row.get("engine",MODE["engine"]),
        "category":row.get("category",""),
        "reviewed_at":"2026-11-08",
        "facts":[{"label":a,"value":b} for a,b in row.get("facts",[])],
        "sources":[{"title":"المرجع الفني المنشور","url":u} for u in src]}}

def verify(url,filename,title):
    failure=None
    for k in range(8):
        try:
            r=get(url,params={"a3tal_batch12_audit":str(time.time_ns())},
                  headers={"Cache-Control":"no-cache"})
            if r.url.split("?")[0].rstrip("/")!=url.rstrip("/"):raise ValueError("permalink redirect")
            html=r.text
            if title not in html or filename not in html:raise ValueError("title or visible featured photo missing")
            tags=re.findall(r"<meta\b[^>]*>",html,re.I)
            og=[x for x in tags if re.search(r"\bproperty=['\"]og:image['\"]",x,re.I)]
            if not og or filename not in og[0]:raise ValueError("wrong og:image")
            canon=re.findall(r'<link\b[^>]*rel=["\x27]canonical["\x27][^>]*>',html,re.I)
            if not canon or url.rstrip("/") not in canon[0]:raise ValueError("wrong canonical")
            if "noindex" in html[:15000].lower():raise ValueError("unexpected noindex")
            return
        except Exception as e:
            failure=e
            if k<7:time.sleep(4)
    raise RuntimeError("SEO verification failed "+url+" "+str(failure))

def main():
    cap=min(len(ITEMS),max(1,int(os.getenv("A3CR_LIMIT","12"))))
    brand=records(GROUP["brand"])
    if brand and (len(brand)!=1 or brand[0]["link"].rstrip("/")!=BASE+"/car-reference/"+GROUP["brand"]):
        raise RuntimeError("Unexpected brand collision: "+GROUP["brand"])
    master,origin=download_photo()
    print("Publishing",FAMILY,"cap",cap,"source",origin,flush=True)
    try:
        for i,(kind,row,parent) in enumerate(ITEMS[:cap]):
            slug=row["slug"]
            url=BASE+"/car-reference/"+(parent+"/" if parent else "")+slug+"/"
            old=records(slug)
            if old:
                if len(old)!=1 or old[0].get("link","").rstrip("/")!=url.rstrip("/"):
                    raise RuntimeError("Slug collision: "+slug)
                PROGRESS.append({"slug":slug,"url":url,"status":"already-published"})
                print("SKIP VERIFIED EXISTING SLUG",url,flush=True)
                continue
            if kind=="spec":
                parent_post=records(MODE["slug"])
                if len(parent_post)!=1 or parent_post[0]["link"].rstrip("/")!=(BASE+"/car-reference/"+GROUP["brand"]+"/"+MODE["slug"]):
                    raise RuntimeError("Model parent not published: "+MODE["slug"])
            photo_i,photo_src=download_photo(max(0,i-1))
            raw=render(photo_i,i,row)
            filename="a3tal-b28-"+FAMILY+"-"+slug+".webp"
            media=post(UPLOAD,{"filename":filename,
                "image_base64":base64.b64encode(raw).decode("ascii"),
                "convert_webp":False,"title":row["title"],
                "alt":row["title"]+" - دليل أعطال.كوم"})
            mid=int(media.get("media_id") or 0)
            if mid<1 or not str(media.get("url","")).endswith(".webp"):
                raise RuntimeError("Image upload failed "+slug+" "+repr(media)[:160])
            record=payload(kind,row,parent,mid)
            try:
                response=post(UPSERT,{"items":[record]})
            except requests.RequestException:
                # WP may already have saved it before a dropped connection.
                found=records(slug)
                if len(found)==1 and found[0].get("link","").rstrip("/")==url.rstrip("/"):
                    response={"results":[{"ok":True,"status":"publish","id":found[0]["id"],"url":url}]}
                else:response=post(UPSERT,{"items":[record]})
            outcomes=response.get("results") or []
            if len(outcomes)!=1 or not outcomes[0].get("ok") or outcomes[0].get("status")!="publish":
                raise RuntimeError("Upsert failed "+slug+" "+repr(response)[:300])
            if outcomes[0].get("url","").rstrip("/")!=url.rstrip("/"):
                raise RuntimeError("Wrong published URL "+slug+" "+str(outcomes[0].get("url")))
            verify(url,filename,row["title"])
            PROGRESS.append({"slug":slug,"status":"published","url":url,
                "image_url":media["url"],"photo_source":photo_src,"photo_id":mid,"og_image_verified":True,
                "canonical_verified":True})
            print("PUBLISHED PHOTO AND SEO VERIFIED",url,flush=True)
    finally:
        REPORT.write_text(json.dumps({"family":FAMILY,"original_photo":origin,
            "rows":PROGRESS},ensure_ascii=False,indent=2),encoding="utf8")
    if len(PROGRESS)!=cap:
        raise RuntimeError("Expected "+str(cap)+" processed rows, found "+str(len(PROGRESS)))
    print("A3TAL_REAL_PSEO_BATCH17_COMPLETE",FAMILY,len(PROGRESS),flush=True)

if __name__=="__main__":main()
