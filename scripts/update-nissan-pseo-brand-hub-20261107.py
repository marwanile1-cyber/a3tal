#!/usr/bin/env python3
"""Refresh the existing Nissan PSEO brand hub, preserving its media, ID and canonical.
Uses GitHub Actions -> A3tal Direct Bridge exclusively.
"""
import json, os, re, time
from html import escape
from pathlib import Path
import requests

BASE="https://a3tal.com"
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"car-reference-b21-nissan-brand-hub-update-audit.json"
S=requests.Session()
S.headers.update({"User-Agent":"A3tal-PSEO-Nissan-hub-Quality/1.0"})
KEY=os.environ["A3TAL_API_KEY"]
MODELS=[
 ("sunny-n17-egypt","صني N17","دليل مواصفات المحرك، الكاوتش والشنطة لخدمة ملاك صني N17."),
 ("magnite-2026-egypt","ماجنايت 2026","محرك 1.0 تيربو وناقل CVT والتجهيزات الخاصة بالنسخة المصرية."),
 ("qashqai-j12-egypt-petrol-epower","قشقاي الجديدة J12","فصل بيانات البنزين 1332 سي سي عن منظومة e-POWER وتجهيزات كل فئة."),
 ("juke-10-digt-dct-egypt","جوك 1.0 تيربو","محرك DIG-T وناقل DCT ومقاسات الإطارات والأمان."),
 ("xtrail-epower-e4orce-egypt","إكس تريل e-POWER","مقارنة القوة والدفع بين Acenta Premium وTekna e-4ORCE."),
 ("sentra-16-xtronic-premium-egypt","سنترا 1.6 Premium","محرك 1598 سي سي وفتيس Xtronic CVT والكاوتش والأبعاد والفرامل.")
]
URLS=[(BASE+"/car-reference/nissan/"+slug+"/",title,summary) for slug,title,summary in MODELS]
REST=BASE+"/wp-json/wp/v2/car-reference-records"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
current=S.get(REST,params={"slug":"nissan","per_page":10},timeout=60).json()
current=[r for r in current if r.get("slug")=="nissan" and r.get("status")=="publish"]
assert len(current)==1,"Brand not uniquely published"
old=current[0]
assert old["id"]==85084 and old["featured_media"]>0
assert old["link"].rstrip("/")==BASE+"/car-reference/nissan"
assert "صني" in old["content"]["rendered"]
for url,_,_ in URLS:
    r=S.get(url,timeout=45)
    r.raise_for_status()
    assert r.url.split("?")[0].rstrip("/")==url.rstrip("/"),("URL mismatch",url)
    assert "canonical" in r.text.lower(),("No canonical",url)
rows=[]
for url,title,summary in URLS:
    rows.append("<tr><th scope='row'><a href='"+escape(url,quote=True)+"'>"+escape(title)+"</a></th><td>"+escape(summary)+"</td></tr>")
content=(
 "<p>يضم دليل نيسان في أعطال.كوم الموديلات التي تتوفر لها بيانات فنية محددة للسوق المصري، "
 "من صني وسنترا إلى ماجنايت وقشقاي وجوك وإكس تريل. لا تنطبق مواصفات أي موديل على الآخر تلقائيًا؛ "
 "كما تختلف الأرقام داخل الاسم الواحد عند تغير المحرك أو الجيل أو الفئة. اختر الطراز أولًا، "
 "ثم انتقل إلى صفحة المحرك أو الكاوتش أو الأمان أو السعات التي تجيب عن سؤالك.</p>"
 "<h2>اختر موديل نيسان والمعلومة المطلوبة</h2>"
 "<div class='a3tal-responsive-table' style='overflow-x:auto'><table><thead><tr>"
 "<th scope='col'>الموديل</th><th scope='col'>ماذا ستجد في دليله؟</th></tr></thead><tbody>"
 +"".join(rows)+"</tbody></table></div>"
 "<h2>قبل طلب قطعة غيار أو اختيار مقاس كاوتش</h2>"
 "<p>اسم السيارة وحده ليس رقم قطعة. طابق سنة الإنتاج والفئة ومواصفة المحرك ورقم الشاسيه، "
 "ثم راجع الملصق وكتالوج المالك. مثلاً قشقاي البنزين ليست قشقاي e-POWER، وفتيس سنترا Xtronic CVT "
 "ليس فتيس جوك DCT. كذلك قد يختلف مقاس الكاوتش داخل موديل واحد وفق فئته. "
 "تشرح الصفحات المستقلة هذه الفروق بمراجعها دون وصف معدات غير مؤكدة.</p>"
 "<h2>المواصفات الفنية ليست أسعارًا ولا تشخيصًا للأعطال</h2>"
 "<p>هذا القسم مخصص للمقاسات والأبعاد وتجهيزات المصنع والسعات الفنية. "
 "أسعار السيارات وقطع الغيار تتغير، وأسباب الأعراض الميكانيكية تحتاج فحصًا مستقلاً؛ "
 "لذلك لا نخلط نية بحث الأسعار أو التشخيص مع صفحات المواصفات. "
 "ما لم يُذكر رقم أو تجهيز صراحة في المصدر المصري فلا نقدمه باعتباره حقيقة لكل الفئات.</p>"
 "<h2>كيف نراجع المصادر؟</h2>"
 "<p>المرجع الأساسي لكل صفحة هو موقع نيسان مصر أو نشرة الشركة للطراز المحدد. "
 "عند التعارض بين سوقين نختار البيانات المحلية ونذكر الفئة بوضوح، "
 "وعند نقص معلومة مهمة لا نخمن مقادير سوائل الصيانة أو أرقام قطع الغيار. "
 "لمتابعة موديلات أخرى ارجع إلى <a href='https://a3tal.com/car-reference/'>الدليل العام للمواصفات الفنية</a>.</p>"
 "<p><a href='https://en.nissan.com.eg/vehicles/new.html' rel='nofollow noopener'>مصدر الشركة: نيسان مصر</a></p>"
)
payload={
 "kind":"brand","slug":"nissan","allow_update_published":True,"title":"دليل المواصفات الفنية لسيارات نيسان",
 "status":"publish","parent_path":"","featured_image_id":old["featured_media"],
 "content":content,
 "excerpt":"دليل مواصفات نيسان في مصر: صني وسنترا وماجنايت وقشقاي وجوك وإكس تريل، مع روابط المحرك والكاوتش والأبعاد والأمان لكل موديل.",
 "meta_title":"مواصفات سيارات نيسان في مصر: 6 موديلات | أعطال.كوم",
 "meta_description":"دليل فني لسيارات نيسان مصر: صني وسنترا وماجنايت وقشقاي وجوك وإكس تريل. روابط مواصفات المحركات والكاوتش والأبعاد والفرامل حسب الموديل.",
 "data":{"kind":"brand","market":"مصر","years":"بحسب الموديل والفئة","engine":"موديلات نيسان المصرية","reviewed_at":"2026-11-07","sources":[{"title":"نيسان مصر - السيارات الجديدة","url":"https://en.nissan.com.eg/vehicles/new.html"}]}
}
r=S.post(UPSERT,headers={"X-A3tal-Key":KEY,"Content-Type":"application/json"},json={"items":[payload],"allow_update_published":True},timeout=180)
r.raise_for_status()
ans=r.json(); res=ans.get("results") or []
assert len(res)==1 and res[0].get("ok") and res[0].get("status")=="publish",ans
assert res[0].get("url","").rstrip("/")==old["link"].rstrip("/"),ans
success=False
for attempt in range(8):
    html=S.get(old["link"],params={"a3tal_audit":str(time.time_ns())},headers={"Cache-Control":"no-cache"},timeout=45).text
    if all('/nissan/'+slug+'/' in html for slug,_,_ in MODELS) and "canonical" in html.lower():
        success=True
        break
    time.sleep(4)
assert success,"Hub updated but six direct model links not yet visible"
now=S.get(REST,params={"slug":"nissan","per_page":2},timeout=45).json()
assert len(now)==1 and now[0]["id"]==old["id"] and now[0]["featured_media"]==old["featured_media"]
REPORT.write_text(json.dumps({"ok":True,"brand_url":old["link"],"brand_id":old["id"],"preserved_image_id":old["featured_media"],"models":[u for u,_,_ in URLS]},ensure_ascii=False,indent=2),encoding="utf8")
print("SIX_NISSAN_MODEL_HUB_LINKS_LIVE_AND_MEDIA_PRESERVED",flush=True)
