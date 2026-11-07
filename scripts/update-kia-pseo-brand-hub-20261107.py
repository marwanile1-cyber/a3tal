#!/usr/bin/env python3
"""Add verified Sorento Egypt links to the existing Kia PSEO hub without deleting existing content."""
import json, os, time, re
from pathlib import Path
from html import escape
import requests

BASE="https://a3tal.com"
REST=BASE+"/wp-json/wp/v2/car-reference-records"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"car-reference-b24-kia-hub-update-audit.json"
KEY=os.environ["A3TAL_API_KEY"]
client=requests.Session()
client.headers["User-Agent"]="A3tal-Kia-Hub-Editorial-Update/1.0"
models=[
 ("cerato-bd-2023","كيا سيراتو BD 2023","ملفات زيت المحرك والفتيس وسوائل التبريد والإضاءة والكاوتش الخاصة بجيل BD"),
 ("seltos-sp2-2023","كيا سيلتوس SP2 2023","فصل مواصفات محركات وفتيس ودفع العجلات في الجيل SP2 حسب دليل الخدمة"),
 ("sportage-nq5-2023","كيا سبورتاج NQ5 2023","مراجع فنية للزيوت والفرامل والتبريد والإطارات ومقاسات المحرك"),
 ("sorento-hev-topline-egypt","كيا سورينتو هايبرد Topline في مصر","نسخة 1.6 تيربو HEV بقوة 230 حصان، 6AT ودفع أمامي مع صفحات فنية مستقلة")
]
links=[(BASE+"/car-reference/kia/"+slug+"/",title,summary) for slug,title,summary in models]
response=client.get(REST,params={"slug":"kia","per_page":2},timeout=45)
response.raise_for_status()
items=[r for r in response.json() if r.get("slug")=="kia" and r.get("status")=="publish"]
assert len(items)==1, "Existing Kia manufacturer hub not found unambiguously"
old=items[0]
assert old["id"]==84884 and int(old["featured_media"])==84955, "Preserve manufacturer hub identity and photo"
assert old["link"].rstrip("/")==BASE+"/car-reference/kia"
for url,_,_ in links:
    r=client.get(url,timeout=45)
    r.raise_for_status()
    assert r.url.split("?")[0].rstrip("/")==url.rstrip("/"),("Wrong model link",url)
old_content=old["content"]["rendered"]
assert "دليل كيا" in old_content and "دليل المالك" in old_content
if "/sorento-hev-topline-egypt/" in old_content:
    print("KIA_HUB_ALREADY_LINKS_SORENTO_VERIFIED")
    REPORT.write_text(json.dumps({"ok":True,"already_updated":True,"id":old["id"],"photo_id":old["featured_media"]},ensure_ascii=False),encoding="utf8")
    raise SystemExit(0)
rows=[]
for url,title,summary in links:
    rows.append("<tr><th scope='row'><a href='"+escape(url,quote=True)+"'>"+escape(title)+"</a></th><td>"+escape(summary)+"</td></tr>")
new=(
 "<h2>اختيار موديل كيا حسب الجيل ونوع منظومة الحركة</h2>"
 "<p>تختلف أدلة الموديلات القديمة عن صفحات المواصفات المحلية المعلنة لدى الوكيل. "
 "صيانة سيراتو BD وسيلتوس SP2 وسبورتاج NQ5 مرتبطة بسنة الإنتاج ورمز المحرك ونوع ناقل الحركة. "
 "أما سورينتو Topline HEV المعروضة في مصر، فهي منظومة هجينة 1.6 Turbo GDI وناقل أوتوماتيك 6 سرعات بدفع أمامي، "
 "ولها روابط مستقلة عن مواصفات سيارات كيا الأخرى.</p>"
 "<div class='a3tal-responsive-table' style='overflow-x:auto'><table><thead><tr><th>الموديل</th><th>المحتوى المتاح</th></tr></thead><tbody>"
 +"".join(rows)+"</tbody></table></div>"
 "<h2>قبل الاعتماد على رقم زيت أو قطعة غيار</h2>"
 "<p>ابدأ برقم الشاسيه ورمز المحرك وسنة الإنتاج والفئة، ثم راجع دليل الخدمة الأصلي. "
 "لا تنقل كمية زيت فتيس DCT من سبورتاج إلى سورينتو HEV ذات ناقل 6AT، ولا تتعامل مع الفئة الهجينة كسيارة بنزين فقط؛ "
 "بعض أنظمة الجهد العالي تحتاج إجراءات عزل وخبرة متخصصة.</p>"
 "<h2>ملاحظة مهمة على بيانات سورينتو الهجينة</h2>"
 "<p>تذكر <a href='https://www.kia.com.eg/ar/models/specifications/The_Sorento' rel='nofollow noopener'>صفحة المواصفات الرسمية</a> "
 "سعة خزان 67 لترًا، بينما تذكر <a href='https://www.kia.com.eg/ar/models/The_Sorento' rel='nofollow noopener'>صفحة عرض الموديل</a> "
 "76 لترًا؛ لذلك لا ننشر رقمًا نهائيًا على أنه مؤكد لكل سيارة من دون مطابقة بيانات الفئة ورقم الشاسيه أو تأكيد الوكيل. "
 "الهدف من الدليل توضيح المواصفات والتحفظات المؤثرة في قرار المالك، لا تجميع أرقام دون مراجعتها.</p>"
)
payload={
 "kind":"brand","slug":"kia","title":old["title"]["rendered"],
 "status":"publish","parent_path":"","featured_image_id":old["featured_media"],
 "allow_update_published":True,"content":old_content+"\n"+new,
 "excerpt":"دليل موديلات كيا ومواصفاتها الفنية: سيراتو BD وسيلتوس SP2 وسبورتاج NQ5 وسورينتو هايبرد المصرية.",
 "meta_title":"دليل مواصفات كيا في مصر | أعطال.كوم",
 "meta_description":"دليل مواصفات كيا وسوائل الصيانة حسب الجيل والمحرك: سيراتو BD وسيلتوس SP2 وسبورتاج NQ5 وسورينتو هايبرد Topline في مصر.",
 "data":{"kind":"brand","market":"مصر - تختلف أدلة الصيانة بحسب الجيل","years":"حسب الموديل وسنة الإنتاج","engine":"محركات وفئات مختلفة","reviewed_at":"2026-11-07","sources":[{"title":"كيا مصر - سورينتو Topline","url":"https://www.kia.com.eg/ar/models/specifications/The_Sorento"}]}
}
r=client.post(UPSERT,headers={"X-A3tal-Key":KEY},json={"items":[payload],"allow_update_published":True},timeout=180)
r.raise_for_status()
data=r.json();out=data.get("results") or []
assert len(out)==1 and out[0].get("ok") and out[0].get("status")=="publish",data
assert out[0].get("url","").rstrip("/")==old["link"].rstrip("/"),data
validated=False
for attempt in range(8):
    page=client.get(old["link"],params={"a3tal_kia_hub_audit":str(time.time_ns())},headers={"Cache-Control":"no-cache"},timeout=45)
    html=page.text
    if all("/car-reference/kia/"+slug+"/" in html for slug,_,_ in models) and "canonical" in html.lower() and "/uploads/" in html:
        validated=True
        break
    time.sleep(4)
assert validated, "Kia model hub not updated or image missing"
now=client.get(REST,params={"slug":"kia","per_page":2},timeout=45).json()
assert len(now)==1 and now[0]["id"]==84884 and now[0]["featured_media"]==old["featured_media"]
REPORT.write_text(json.dumps({"ok":True,"brand":old["link"],"id":84884,"media_preserved":old["featured_media"],"links":[u for u,_,_ in links]},ensure_ascii=False,indent=2),encoding="utf8")
print("KIA_HUB_FOUR_MODELS_LINKED_WITH_PHOTO_AND_CANONICAL_PRESERVED",flush=True)
