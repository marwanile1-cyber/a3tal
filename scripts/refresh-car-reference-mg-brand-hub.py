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
PRICE=BASE+"/mg-zs-price-egypt/"
HTML="""<p>دليل مواصفات سيارات MG في أعطال.كوم يجمع البيانات الفنية المستندة إلى نشرات MG Motor Egypt الرسمية. يضم حاليًا MG5 السيدان، وMG ZS الجيل السابق بمحرك 1.5 لتر وناقل أوتوماتيك تقليدي 4 سرعات. نعرض المقاسات والأبعاد وتجهيزات الأمان حسب الفئة، دون خلط بيانات الأجيال المختلفة.</p>
<h2>اختر موديل MG المناسب</h2>
<p>ابدأ من <a href="https://a3tal.com/car-reference/mg/mg5-egypt/">دليل مواصفات MG5 في مصر</a> لمعرفة مقاسات الإطارات وبيانات المحرك وفتيس CVT والسعات وتجهيزات السلامة. أما <a href="https://a3tal.com/car-reference/mg/zs-legacy-4at-egypt/">دليل MG ZS القديمة في مصر</a> فيشرح ناقل 4AT ومقاسات إطارات 16 و17 بوصة وسعة تانك 48 لترًا وتجهيزات الفئات وفق كتالوج 2023.</p>
<h2>MG ZS القديمة ليست New MG ZS</h2>
<p>الجيل التقليدي في دليل الشركة القديم يستخدم ناقل أوتوماتيك 4 سرعات وخزان وقود سعة 48 لترًا. أما New MG ZS المعروضة أيضًا في السوق المصري فتستخدم CVT وخزان 45 لترًا ومقاس إطارات مختلفًا. لا تُنقل بيانات السعة أو الإطارات أو سوائل الفتيس بين الجيلين. وفي ZS القديمة ذاتها قد تختلف مقاسات الإطارات وتجهيزات الوسائد الهوائية حسب الفئة وسنة النشرة.</p>
<h2>الفرق بين المواصفات والأسعار والأعطال</h2>
<p>هذا الدليل مرجع للمقاسات والسعات قبل الشراء أو الصيانة، بينما <a href="https://a3tal.com/mg-zs-price-egypt/">مقال سعر MG ZS في مصر ومقارنة الجيلين</a> يشرح الأسعار والشراء، و<a href="https://a3tal.com/mg-5-cvt-transmission-problems-guide/">مقال أعطال CVT في MG5</a> يتناول التشخيص. لن ننشئ هنا صفحات أخرى تستهدف نية البحث نفسها.</p>
<h2>كيف تستخدم البيانات بشكل صحيح؟</h2>
<p>راجع سنة الإنتاج ونوع ناقل الحركة والفئة وبلد السيارة، واطلب التأكد من رقم الشاسيه أو كتالوج المالك عند اختيار قطع الغيار أو الزيوت. نشرات الشركة تمثل نسخة وتاريخ إصدار محددين ولا تضمن استمرار كل الفئات أو التجهيزات للبيع اليوم.</p>"""

def get_page(url,**kw):
    r=S.get(url,timeout=50,**kw)
    r.raise_for_status()
    return r

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
    for url in (MG5,ZS,PRICE):
        if not get_page(url).ok:raise RuntimeError("Existing internal page unavailable "+url)
    record={
      "kind":"brand","slug":"mg","title":"دليل المواصفات الفنية لسيارات MG في مصر",
      "parent_path":"","status":"publish","allow_update_published":True,
      "featured_image_id":image,"content":HTML,
      "excerpt":"مواصفات MG5 وMG ZS الجيل السابق في مصر: المحركات والفتيس ومقاسات الكاوتش والأمان من مصادر الوكيل الرسمية.",
      "data":{"kind":"brand","market":"مصر - نشرات MG Motor Egypt الرسمية",
        "years":"MG5 حسب النشرة؛ ZS الجيل السابق وفق كتالوج 2023",
        "engine":"","category":"","reviewed_at":"2026-11-04",
        "facts":[],"sources":[
          {"title":"MG5 - النشرة المحلية","url":"https://www.mgmotor.com.eg/wp-content/uploads/2025/10/MG5-Amended-Brochure.pdf"},
          {"title":"MG ZS الجيل السابق - نشرة 2023","url":"https://www.mgmotor.com.eg/wp-content/uploads/2023/03/MG-ZS.pdf"},
          {"title":"New ZS - فصل المواصفات","url":"https://www.mgmotor.com.eg/model/new-zs/?pp=0"}]},
      "meta_title":"دليل مواصفات MG في مصر: MG5 وZS القديمة | أعطال.كوم",
      "meta_description":"مواصفات MG5 وMG ZS الجيل السابق في مصر من نشرات الوكيل: المقاسات والمحرك والفتيس والأبعاد والفرامل وتجهيزات الأمان."
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
            if ("href=\""+MG5+"\"" not in text and "mg5-egypt" not in text) or "zs-legacy-4at-egypt" not in text:
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
      "linked_models":[MG5,ZS],"unchanged_permalink":True,
      "unchanged_featured_image":True,"verified":True}
    REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf8")
    print("UPDATED MG HUB VERIFIED",json.dumps(result,ensure_ascii=False),flush=True)

if __name__=="__main__":main()
