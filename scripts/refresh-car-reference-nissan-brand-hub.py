#!/usr/bin/env python3
"""Refresh the existing Nissan brand hub after Tucson NX4e cluster release.
No new page; preserves existing slug, post id, image, and child hierarchy.
"""
import json,os,re,time
from pathlib import Path
import requests

BASE="https://a3tal.com"
URL=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
API_KEY=os.environ["A3TAL_API_KEY"]
SESSION=requests.Session()
SESSION.headers["User-Agent"]="A3tal-Nissan-Brand-Cohesion/1.0"
BODY="""<p>دليل المواصفات الفنية لسيارات نيسان في أعطال.كوم يضم أرقام المقاسات والمحركات والسعات قبل الشراء والصيانة. نغطي نيسان صني N17 ونيسان ماجنايت 2026 بمواصفات السوق المصري، مع فصل كل موديل عن الآخر وعدم خلط بيانات أسواق مختلفة.</p>
<h2>اختر موديل نيسان</h2>
<p><a href="https://a3tal.com/car-reference/nissan/sunny-n17-egypt/">دليل صني N17 في مصر</a> يشرح المحرك ومقاس الكاوتش وسعة الخزان والشنطة والأبعاد، و<a href="https://a3tal.com/car-reference/nissan/magnite-2026-egypt/">دليل ماجنايت 2026 في مصر</a> يعرض محرك 1.0 تيربو CVT وإطارات 195/60R16 والسعات المحلية.</p>
<h2>لماذا تختلف المواصفات بين البلدان؟</h2>
<p>قد تُباع السيارة باسم واحد مع اختلافات في السوق أو الفئة، مثل سعة خزان الوقود. يظهر في مُهيّئ نيسان مصر أن سعة ماجنايت 36 لترًا، بينما توجد أرقام مختلفة في كتالوجات دول أخرى. لذلك نستخدم مصدر نيسان مصر المحلي، وننصح بمطابقة الكتالوج مع رقم الشاسيه.</p>
<h2>ما الفرق بين الدليل وصفحات الأعطال والأسعار؟</h2>
<p>هنا نجيب عن المقاسات والسعات والبيانات الفنية فقط. موضوعات سعر ماجنايت ومشكلات فتيس CVT واعتماديته موجودة في مقالات مستقلة، ولا نكرر نية بحثها. قبل أي صيانة، يُرجع إلى ملصقات السيارة ودليل المالك الأصلي.</p>"""
def run():
    p=SESSION.get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":"nissan","per_page":2},timeout=45)
    p.raise_for_status()
    rows=[x for x in p.json() if x.get("slug")=="nissan" and x.get("status")=="publish"]
    assert len(rows)==1
    old=rows[0]
    assert old.get("featured_media",0)>0
    assert old["link"]==BASE+"/car-reference/nissan/"
    check1=SESSION.get(BASE+"/car-reference/nissan/sunny-n17-egypt/",timeout=50)
    check2=SESSION.get(BASE+"/car-reference/nissan/magnite-2026-egypt/",timeout=50)
    if not check1.ok or not check2.ok:raise RuntimeError("A linked model is not live")
    new={
      "title":"دليل المواصفات الفنية لسيارات نيسان",
      "slug":"nissan","kind":"brand","parent_path":"",
      "status":"publish","allow_update_published":True,"featured_image_id":old["featured_media"],
      "content":BODY,
      "excerpt":"دليل صني N17 وماجنايت 2026 في مصر: المحرك والمقاسات والوقود والأبعاد من نيسان الرسمية.",
      "data":{"kind":"brand","market":"مواصفات نيسان مصر الرسمية",
              "years":"حسب الموديل","engine":"","category":"",
              "reviewed_at":"2026-11-03","facts":[],
              "sources":[
                {"title":"صني N17 - نيسان مصر","url":"https://ar.nissan.com.eg/vehicles/new/sunny/versions-and-specs.html"},
                {"title":"ماجنايت - مُهيّئ نيسان مصر","url":"https://ar-eg.magniteconfigurator.com/eg/ar/configure/magnite-1-0t-visia-cvt?activeCam=exterior&ext=RCA"}]},
      "meta_title":"دليل مواصفات نيسان مصر: صني وماجنايت | أعطال.كوم",
      "meta_description":"مواصفات نيسان صني N17 وماجنايت 2026 في مصر: المحركات ومقاسات الكاوتش وسعات البنزين والأمتعة."
    }
    result=SESSION.post(URL,json={"items":[new]},headers={"X-A3tal-Key":API_KEY,"Content-Type":"application/json"},timeout=140)
    result.raise_for_status()
    j=result.json()
    items=j.get("results") or []
    if len(items)!=1 or not items[0].get("ok") or items[0].get("status")!="publish":
        raise RuntimeError("Hub refresh rejected "+repr(j)[:350])
    for i in range(6):
        response=SESSION.get(BASE+"/car-reference/nissan/",params={"verify_hub":str(time.time_ns())},timeout=45)
        h=response.text
        if (response.ok and "magnite-2026-egypt" in h and "sunny-n17-egypt" in h and
            "مواصفات نيسان مصر الرسمية" in h and "noindex" not in h[:15000].lower()):
            break
        if i==5:raise RuntimeError("Hub live HTML verification failed")
        time.sleep(3)
    after=SESSION.get(BASE+"/wp-json/wp/v2/car-reference-records",
        params={"slug":"nissan","per_page":2},timeout=45).json()
    post=next(x for x in after if x["slug"]=="nissan")
    if int(post["id"])!=int(old["id"]) or int(post["featured_media"])!=int(old["featured_media"]):
        raise RuntimeError("Hub post/image ID changed unexpectedly")
    result={"url":old["link"],"post_id":old["id"],"featured_id":old["featured_media"],
        "links_verified":["sunny-n17-egypt","magnite-2026-egypt"],"status":"updated"}
    Path("nissan-hub-cohesion-audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf8")
    print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=="__main__":
    run()
