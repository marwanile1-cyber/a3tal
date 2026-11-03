#!/usr/bin/env python3
"""Refresh the existing Hyundai brand hub after Tucson NX4e cluster release.
No new page; preserves existing slug, post id, image, and child hierarchy.
"""
import json,os,re,time
from pathlib import Path
import requests

BASE="https://a3tal.com"
URL=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
API_KEY=os.environ["A3TAL_API_KEY"]
SESSION=requests.Session()
SESSION.headers["User-Agent"]="A3tal-Hyundai-Brand-Cohesion/1.0"
BODY="""<p>دليل المواصفات الفنية لسيارات هيونداي في أعطال.كوم يجمع بيانات الصيانة والمقاسات من أدلة المالك والنشرات الرسمية المصرية. يغطي حاليًا إلنترا CN7 2025 وتوسان NX4e 2025 وأكسنت RB المصرية، مع فصل كل جيل ومحرك وناقل حركة عن غيره.</p>
<h2>اختر موديل هيونداي</h2>
<p><a href="https://a3tal.com/car-reference/hyundai/elantra-cn7-2025/">إلنترا CN7 موديل 2025</a> تشمل زيوت المحركات ونواقل AT وIVT والإطارات والتبريد والفرامل. <a href="https://a3tal.com/car-reference/hyundai/tucson-nx4e-2025/">توسان NX4e موديل 2025</a> تشمل مواصفات التيربو وDCT والإطارات والتبريد وأنظمة الدفع الرباعي حيث توجد. <a href="https://a3tal.com/car-reference/hyundai/accent-rb-egypt-2025/">أكسنت RB المصرية</a> تشمل مقاسات الإطارات حسب الفئة، والمحرك والأبعاد والفرامل وتجهيزات ABS والوسائد الهوائية.</p>
<h2>اختر الفئة قبل اختيار المقاس</h2>
<p>في أكسنت RB يختلف مقاس الإطار بين فئات جنط 14 وجنط 16، وتختلف تجهيزات ABS والوسائد الهوائية بين الفئات. وفي توسان تختلف سعة السوائل باختلاف المحرك ونوع الناقل ونظام AWD. طابق الفئة والكود وسنة السيارة قبل الاعتماد على أي رقم.</p>
<h2>ما الفرق عن صفحات الأسعار والأعطال؟</h2>
<p>هذا القسم مختص بالبيانات الفنية والجداول التي يحتاجها المالك قبل الصيانة. صفحات الأسعار والمراجعات والأعطال الموجودة بالموقع تؤدي أغراضًا مختلفة، ولا نكررها لمجرد إنشاء عنوان جديد. تخضع المواصفات للمصدر الأصلي وسوق السيارة وليس للاسم التجاري فقط.</p>"""
def run():
    p=SESSION.get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":"hyundai","per_page":2},timeout=45)
    p.raise_for_status()
    rows=[x for x in p.json() if x.get("slug")=="hyundai" and x.get("status")=="publish"]
    assert len(rows)==1
    old=rows[0]
    assert old.get("featured_media",0)>0
    assert old["link"]==BASE+"/car-reference/hyundai/"
    check1=SESSION.get(BASE+"/car-reference/hyundai/elantra-cn7-2025/",timeout=50)
    check2=SESSION.get(BASE+"/car-reference/hyundai/tucson-nx4e-2025/",timeout=50)
    check3=SESSION.get(BASE+"/car-reference/hyundai/accent-rb-egypt-2025/",timeout=50)
    if not check1.ok or not check2.ok or not check3.ok:raise RuntimeError("A linked model is not live")
    new={
      "title":"دليل المواصفات الفنية لسيارات هيونداي",
      "slug":"hyundai","kind":"brand","parent_path":"",
      "status":"publish","allow_update_published":True,"featured_image_id":old["featured_media"],
      "content":BODY,
      "excerpt":"بيانات موثقة لهيونداي إلنترا CN7 وتوسان NX4e وأكسنت RB في مصر، تشمل الزيوت والمقاسات والفرامل حسب الموديل.",
      "data":{"kind":"brand","market":"أدلة هيونداي الرسمية ونشرة غبور لأكسنت RB المصرية",
              "years":"2025","engine":"","category":"",
              "reviewed_at":"2026-11-03","facts":[],
              "sources":[
                {"title":"كتالوج إلنترا CN7 2025","url":"https://ownersmanual.hyundai.com/full_webhelp/CN7/2025/en_GN/id8a19b15b80e.html"},
                {"title":"كتالوج توسان NX4e 2025","url":"https://ownersmanual.hyundai.com/full_webhelp/NX4e/2025/en_GN/idcd4ca75644f.html"},
                {"title":"نشرة أكسنت RB في مصر - غبور","url":"https://hyundai-egypt.net/wp-content/uploads/2024/05/Accent-RB_NEW-Final.pdf"}]},
      "meta_title":"دليل مواصفات هيونداي: إلنترا وتوسان وأكسنت RB | أعطال.كوم",
      "meta_description":"دليل مواصفات هيونداي الفنية لإلنترا CN7 وتوسان NX4e وأكسنت RB في مصر: المحركات والزيوت والفتيس ومقاسات الكاوتش والفرامل."
    }
    result=SESSION.post(URL,json={"items":[new]},headers={"X-A3tal-Key":API_KEY,"Content-Type":"application/json"},timeout=140)
    result.raise_for_status()
    j=result.json()
    items=j.get("results") or []
    if len(items)!=1 or not items[0].get("ok") or items[0].get("status")!="publish":
        raise RuntimeError("Hub refresh rejected "+repr(j)[:350])
    for i in range(6):
        response=SESSION.get(BASE+"/car-reference/hyundai/",params={"verify_hub":str(time.time_ns())},timeout=45)
        h=response.text
        if (response.ok and "tucson-nx4e-2025" in h and "elantra-cn7-2025" in h and "accent-rb-egypt-2025" in h and
            "أدلة هيونداي الرسمية ونشرة غبور" in h and "noindex" not in h[:15000].lower()):
            break
        if i==5:raise RuntimeError("Hub live HTML verification failed")
        time.sleep(3)
    after=SESSION.get(BASE+"/wp-json/wp/v2/car-reference-records",
        params={"slug":"hyundai","per_page":2},timeout=45).json()
    post=next(x for x in after if x["slug"]=="hyundai")
    if int(post["id"])!=int(old["id"]) or int(post["featured_media"])!=int(old["featured_media"]):
        raise RuntimeError("Hub post/image ID changed unexpectedly")
    result={"url":old["link"],"post_id":old["id"],"featured_id":old["featured_media"],
        "links_verified":["elantra-cn7-2025","tucson-nx4e-2025","accent-rb-egypt-2025"],"status":"updated"}
    Path("hyundai-hub-cohesion-audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf8")
    print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=="__main__":
    run()
