#!/usr/bin/env python3
"""Update existing MG reference brand hub in place after legacy ZS release.
Preserve brand page ID, featured attachment, canonical and original URL.
"""
import json, os, re, time
from pathlib import Path
import requests

BASE="https://a3tal.com"
KEY=os.environ["A3TAL_API_KEY"]
S=requests.Session()
S.headers["User-Agent"]="A3tal-MG-Brand-Hub-Cohesion/1.0"
REPORT=Path("car-reference-mg-brand-hub-result.json")
HUB=BASE+"/car-reference/mg/"
MG5=BASE+"/car-reference/mg/mg5-egypt/"
ZS=BASE+"/car-reference/mg/zs-legacy-4at-egypt/"
GT=BASE+"/car-reference/mg/mg-gt-15t-egypt/"
MG7=BASE+"/car-reference/mg/mg7-15-turbo-egypt/"
PRICE=BASE+"/mg-zs-price-egypt/"
HTML="""<p>دليل المواصفات الفنية لسيارات MG في أعطال.كوم يعرض البيانات الفنية من نشرات MG Motor Egypt الرسمية، مع فصل الأجيال والفئات وأنواع الفتيس. يشمل MG5 وMG ZS الجيل السابق وMG GT تيربو وMG7، من غير تكرار صفحات الأسعار أو أعطال السيارات الموجودة بالموقع.</p>
<h2>اختر موديل MG</h2>
<p><a href="https://a3tal.com/car-reference/mg/mg5-egypt/">مواصفات MG5 في مصر</a> تشمل محرك 1.5 لتر وCVT ومقاسات الجنوط والأمان. <a href="https://a3tal.com/car-reference/mg/zs-legacy-4at-egypt/">دليل MG ZS القديمة</a> يوضح فتيس 4AT والإطارات وأبعاد الجيل السابق. <a href="https://a3tal.com/car-reference/mg/mg-gt-15t-egypt/">دليل MG GT تيربو</a> يغطي محرك 170 حصانًا وناقل WDCT ومقاس الكاوتش. <a href="https://a3tal.com/car-reference/mg/mg7-15-turbo-egypt/">دليل MG7 في مصر</a> يعرض محرك 185 حصانًا وفروق تجهيز Luxury وTrophy.</p>
<h2>لا تنقل مواصفات سيارة إلى الأخرى</h2>
<p>تختلف MG5 المزودة بناقل CVT عن MG GT وMG7 ذواتي القابض المزدوج الرطب. كما أن MG ZS القديمة بناقل 4 سرعات وتانك 48 لترًا تختلف عن New MG ZS ذات CVT وتانك 45 لترًا. وتختلف الوسائد وأنظمة مساعدة السائق بين MG7 Luxury وTrophy. يجب مطابقة الفئة والجيل ورقم الشاسيه عند شراء القطع أو تنفيذ الصيانة.</p>
<h2>متى تستفيد من هذا القسم؟</h2>
<p>استخدم صفحات الدليل لمعرفة مقاس الكاوتش والأبعاد والأرقام الفنية قبل الصيانة. أما <a href="https://a3tal.com/mg-zs-price-egypt/">سعر MG ZS والجيلين</a> و<a href="https://a3tal.com/mg7-price-egypt-specs-2026/">أسعار ومراجعة MG7</a> و<a href="https://a3tal.com/mg-5-cvt-transmission-problems-guide/">أعطال فتيس MG5</a> فلها مقالات متخصصة. لا تُعد أسعار السيارات وتوافر فئاتها حقائق ثابتة من نشرات المواصفات وحدها.</p>
<h2>المصادر والاحتياطات</h2>
<p>تحتفظ الشركة بحق تعديل التجهيزات، وقد يختلف رقم بين النسخة الورقية والصفحة الحية كما في سعة تانك MG GT. لذلك نوضح الاختلاف عند وجوده بدل وضع قيمة غير محسومة، ويظل كتيب سيارة المالك هو المرجع النهائي للإجراءات الفنية.</p>"""

def get_page(url,**kw):
    error=None
    for attempt in range(5):
        try:
            r=S.get(url,timeout=55,**kw)
            if r.status_code in (408,429,500,502,503,504,520,521,522,523,524):
                raise requests.RequestException("Transient HTTP "+str(r.status_code))
            r.raise_for_status()
            return r
        except requests.RequestException as exc:
            error=exc
            if attempt<4:time.sleep(4*(attempt+1))
    raise RuntimeError("Hub REST lookup retries exhausted "+url+" "+str(error))

def getbrand():
    r=get_page(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":"mg","per_page":20})
    v=[p for p in r.json() if p.get("slug")=="mg" and p.get("status")=="publish"]
    if len(v)!=1 or v[0].get("link","").rstrip("/")!=HUB.rstrip("/"):
        raise RuntimeError("MG brand hub missing or slug collision")
    return v[0]

def main():
    before=getbrand()
    image=int(before.get("featured_media") or 0)
    if not image:raise RuntimeError("Brand hub has no featured image, fail closed")
    for url in (MG5,ZS,GT,MG7,PRICE):
        if not get_page(url).ok:raise RuntimeError("Existing internal page unavailable "+url)
    record={
      "kind":"brand","slug":"mg","title":"دليل المواصفات الفنية لسيارات MG في مصر",
      "parent_path":"","status":"publish","allow_update_published":True,
      "featured_image_id":image,"content":HTML,
      "excerpt":"دليل MG5 وMG ZS القديمة وMG GT وMG7 في مصر: المحركات والفتيس ومقاسات الكاوتش والأمان من المصادر الرسمية.",
      "data":{"kind":"brand","market":"مصر - نشرات MG Motor Egypt الرسمية",
        "years":"نشرات كل موديل رسمية؛ MG ZS القديمة وفق كتالوج 2023",
        "engine":"","category":"","reviewed_at":"2026-11-04",
        "facts":[],"sources":[
          {"title":"MG5 - النشرة المحلية","url":"https://www.mgmotor.com.eg/wp-content/uploads/2025/10/MG5-Amended-Brochure.pdf"},
          {"title":"MG ZS الجيل السابق - نشرة 2023","url":"https://www.mgmotor.com.eg/wp-content/uploads/2023/03/MG-ZS.pdf"},
          {"title":"New ZS - فصل المواصفات","url":"https://www.mgmotor.com.eg/model/new-zs/?pp=0"},
          {"title":"MG GT - النشرة المصرية","url":"https://www.mgmotor.com.eg/wp-content/uploads/2025/12/MG-GT-Brochure-Compressed.pdf"},
          {"title":"MG7 - النشرة المصرية","url":"https://www.mgmotor.com.eg/wp-content/uploads/2025/08/MG7-Brochure-Jul-25-Amended.pdf"}]},
      "meta_title":"دليل مواصفات MG مصر: MG5 وZS وGT وMG7 | أعطال.كوم",
      "meta_description":"موسوعة مواصفات MG5 وMG ZS القديمة وMG GT وMG7 في مصر: المحرك والفتيس والإطارات والأبعاد والأمان من مصادر الوكيل الرسمية."
    }
    r=S.post(BASE+"/wp-json/a3tal-car-reference/v1/upsert",
      headers={"X-A3tal-Key":KEY,"Content-Type":"application/json"},
      json={"items":[record]},timeout=140)
    r.raise_for_status()
    d=r.json()
    results=d.get("results") or []
    if len(results)!=1 or not results[0].get("ok") or results[0].get("status")!="publish":
        raise RuntimeError("Hub update rejected "+str(d)[:300])
    for k in range(7):
        try:
            page=get_page(HUB,params={"mg_brand_qa":str(time.time_ns())},headers={"Cache-Control":"no-cache"})
            text=page.text
            if any(part not in text for part in ("mg5-egypt","zs-legacy-4at-egypt","mg-gt-15t-egypt","mg7-15-turbo-egypt")):
                raise RuntimeError("Links not visible")
            if "New MG ZS" not in text:raise RuntimeError("No generation separation")
            if not re.search(r'<link[^>]*rel=["\x27]canonical["\x27][^>]*href=["\x27]'+re.escape(HUB.rstrip("/"))+r'/?["\x27]',text,re.I):
                raise RuntimeError("Wrong canonical")
            if "noindex" in text[:16000].lower():raise RuntimeError("Hub noindex")
            if not re.search(r'<meta[^>]*property=["\x27]og:image["\x27]',text,re.I):
                raise RuntimeError("Missing OG")
            break
        except Exception:
            if k==6:raise
            time.sleep(4)
    after=getbrand()
    if int(after["id"])!=int(before["id"]) or int(after["featured_media"])!=image:
        raise RuntimeError("Existing brand post id or photo changed")
    result={"url":HUB,"post_id":before["id"],"photo_id":image,
      "linked_models":[MG5,ZS,GT,MG7],"unchanged_permalink":True,
      "unchanged_featured_image":True,"verified":True}
    REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf8")
    print("UPDATED MG HUB VERIFIED",json.dumps(result,ensure_ascii=False),flush=True)

if __name__=="__main__":main()
