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
BODY="""<p>دليل المواصفات الفنية لسيارات هيونداي على أعطال.كوم يجمع بيانات الزيوت والسوائل ومقاسات الإطارات من أدلة المالك الرسمية. يغطي حاليًا إلنترا CN7 2025 وتوسان NX4e 2025، مع فصل المحرك ونوع ناقل الحركة وسوق السيارة حتى لا تُنسب مواصفة نسخة إلى أخرى.</p>
<h2>اختر الموديل المناسب</h2>
<p><a href="https://a3tal.com/car-reference/hyundai/elantra-cn7-2025/">دليل هيونداي إلنترا CN7 موديل 2025</a> يعرض بيانات المحركات وفتيس AT وIVT والزيوت والتبريد والفرامل ومقاسات الإطارات. أما <a href="https://a3tal.com/car-reference/hyundai/tucson-nx4e-2025/">دليل توسان NX4e موديل 2025</a> فيفصل محرك 1.6 تيربو وDCT والإطارات والسوائل وأجزاء الدفع الرباعي عندما تكون موجودة.</p>
<h2>كيف تتأكد من الرقم الصحيح؟</h2>
<p>اختر الجيل أولًا، ثم طابق كود المحرك والفتيس ونظام الجر مع كتالوج سيارتك. يذكر الدليل أحيانًا لزوجة مخصصة لمصر والشرق الأوسط تختلف عن لزوجة أسواق أخرى، ولا يعني وجود المحرك في جدول دولي طرحه في كل فئات مصر.</p>
<h2>فرق دليل المواصفات عن مقالات الأسعار والأعطال</h2>
<p>الصفحات هنا للإجابة عن السعات والمقاسات وتصنيفات السوائل قبل الصيانة. صفحات أسعار السيارات والمراجعات ومراكز الخدمة ومكتبة أكواد الأعطال تؤدي أغراضًا مختلفة، ويُرجع إليها عندما يحتاج القارئ إلى قرار شراء أو تشخيص عطل بدل تكرار المعلومات الفنية.</p>"""
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
    if not check1.ok or not check2.ok:raise RuntimeError("A linked model is not live")
    new={
      "title":"دليل المواصفات الفنية لسيارات هيونداي",
      "slug":"hyundai","kind":"brand","parent_path":"",
      "status":"publish","allow_update_published":True,"featured_image_id":old["featured_media"],
      "content":BODY,
      "excerpt":"بيانات صيانة موثقة لهيونداي إلنترا CN7 وتوسان NX4e 2025، تشمل الزيوت والفتيس والإطارات وفق كتالوج الشركة.",
      "data":{"kind":"brand","market":"أدلة مالك هيونداي الرسمية؛ مصر والشرق الأوسط حيث وردا صراحة",
              "years":"2025","engine":"","category":"",
              "reviewed_at":"2026-11-03","facts":[],
              "sources":[
                {"title":"كتالوج إلنترا CN7 2025","url":"https://ownersmanual.hyundai.com/full_webhelp/CN7/2025/en_GN/id8a19b15b80e.html"},
                {"title":"كتالوج توسان NX4e 2025","url":"https://ownersmanual.hyundai.com/full_webhelp/NX4e/2025/en_GN/idcd4ca75644f.html"}]},
      "meta_title":"دليل مواصفات هيونداي 2025: إلنترا وتوسان | أعطال.كوم",
      "meta_description":"دليل هيونداي الفني لإلنترا CN7 وتوسان NX4e 2025: الزيوت والفتيس والتبريد ومقاسات الكاوتش من كتالوج الشركة الرسمي."
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
        if (response.ok and "tucson-nx4e-2025" in h and "elantra-cn7-2025" in h and
            "أدلة مالك هيونداي الرسمية" in h and "noindex" not in h[:15000].lower()):
            break
        if i==5:raise RuntimeError("Hub live HTML verification failed")
        time.sleep(3)
    after=SESSION.get(BASE+"/wp-json/wp/v2/car-reference-records",
        params={"slug":"hyundai","per_page":2},timeout=45).json()
    post=next(x for x in after if x["slug"]=="hyundai")
    if int(post["id"])!=int(old["id"]) or int(post["featured_media"])!=int(old["featured_media"]):
        raise RuntimeError("Hub post/image ID changed unexpectedly")
    result={"url":old["link"],"post_id":old["id"],"featured_id":old["featured_media"],
        "links_verified":["elantra-cn7-2025","tucson-nx4e-2025"],"status":"updated"}
    Path("hyundai-hub-cohesion-audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf8")
    print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=="__main__":
    run()
