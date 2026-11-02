#!/usr/bin/env python3
"""Quality-first update of existing Kia model hub pages. No new thin URLs, no image changes."""
import json, os, sys, time
from pathlib import Path
from html import escape
from urllib.parse import quote
import requests
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"data/car-reference/batch-01-kia-verified-2026-11-02.json").read_text(encoding="utf8"))
base="https://a3tal.com"
bridge=base+"/wp-json/a3tal-direct/v1"
session=requests.Session()
key=os.environ["A3TAL_API_KEY"]
headers={"X-A3tal-Key":key,"Authorization":"Bearer "+key}
marker="A3TAL-KIA-MODEL-COMPARE-20261102"
notes={
"cerato-bd-2023":(
"دليل سيراتو BD حسب المحرك والفتيس",
"يوضح دليل كيا لسيراتو BD أن سنة الطراز وحدها لا تكفي لاختيار سائل الصيانة. يوجد اختلاف بين محرك 1.6 MPI ومحرك 2.0 MPI ونسخة 1.6 تيربو وSmartstream G1.6. كما تتغير مواصفة الناقل بين المانيوال والأوتوماتيك وDCT، ومن الخطأ اختيار زيت ناقل الحركة بناء على تشابه الاسم أو السعة فقط.",
"عند مراجعة سعة الزيت، استخدم الرقم المرتبط باسم المحرك المكتوب في دليل السيارة. كما أن سعة ناقل الحركة الكلية المنشورة في الدليل لا تعني أن الكمية نفسها ستخرج أثناء التغيير الجزئي. في دورة التبريد قد تتغير السعة بحسب نوع الفتيس حتى مع المحرك نفسه. المعلومات هنا مخصصة لنسخ المحركات الواردة في دليل المالك، ولا تعني أن كل الفئات كانت معروضة في مصر."
),
"seltos-sp2-2023":(
"دليل سيلتوس SP2 حسب فئة المحرك وناقل الحركة",
"تظهر سيلتوس SP2 في دليل 2023 بأكثر من اختيار للمحرك وناقل الحركة، منها 1.6 MPI و1.6 تيربو و2.0 MPI، مع اختلاف بين الفتيس اليدوي والأوتوماتيك وIVT. لذلك يجب تحديد المحرك ونظام الدفع واسم الفتيس قبل البحث عن سعة زيت أو شراء سائل ناقل الحركة.",
"لا تخلط بين سائل الناقل IVT من مواصفة SP-CVT1 وبين ATF SP4M-1 المخصص للناقل الأوتوماتيكي التقليدي. وفي سيارات الدفع الرباعي قد تختلف كميات سوائل علبة النقل والدفرنس عن الدفع الأمامي. راجع الأسواق التي يذكرها الدليل بجوار درجة اللزوجة؛ لأن توصية السوق المصري والشرق الأوسط لا تطابق دائمًا مواصفات دول أخرى."
),
"sportage-nq5-2023":(
"مواصفات سبورتاج NQ5 بحسب نظام الحركة",
"يشمل دليل سبورتاج NQ5 لعام 2023 عدة محركات، من ضمنها Smartstream G1.6 تيربو وG2.0 وG2.5 بنزين وD2.0 ديزل. تختلف سعة زيت المحرك والتصنيف الموصى به، وتختلف كذلك سوائل AT وDCT، لذلك لا يصح نشر مواصفة واحدة باعتبارها مناسبة لجميع نسخ سبورتاج.",
"افحص كود المحرك ونوع ناقل الحركة ومواصفات السوق قبل اختيار زيت الصيانة. إذا كان الناقل DCT، فلا تستخدم مواصفات ATF التابعة للفتيس الأوتوماتيكي التقليدي. كذلك السعة الكلية المسجلة في الدليل لا تعني كمية التغيير الجزئي. ولنسخ الديزل توجد تصنيفات مختلفة بحسب وجود فلتر جزيئات الديزل DPF. تحت كل بند رابط منفصل يوضح المواصفة الدقيقة والسياق."
)
}
def get(url):
 r=session.get(url,headers={**headers,"Cache-Control":"no-cache"},timeout=50)
 r.raise_for_status();return r.json()
def post(body):
 r=session.post(bridge+"/update-post",headers={**headers,"Content-Type":"application/json"},json=body,timeout=80)
 if not r.ok:raise RuntimeError(f"update-post HTTP {r.status_code}: {r.text[:400]}")
 return r.json()
def make_block(model,items):
 slug=model["slug"]; title,lead,advice=notes[slug]
 rows=[]
 for s in items:
  facts=s.get("facts",[])
  primary=facts[0] if facts else None
  if not primary:continue
  link=f"{base}/car-reference/kia/{slug}/{s['slug']}/"
  rows.append("<tr><th scope='row'><a href='"+escape(link)+"'>"+escape(s["title"])+"</a></th><td>"+escape(primary[0])+"</td><td>"+escape(primary[1])+"</td></tr>")
 assert len(rows)>=5
 return ("<!-- "+marker+" -->\n"+
 "<section class='a3cr-compare-audit' aria-label='"+escape(title)+"'>"
 "<h2>"+escape(title)+"</h2>"
 "<p>"+escape(lead)+"</p>"
 "<div class='a3cr-table' style='overflow-x:auto;-webkit-overflow-scrolling:touch'>"
 "<table><thead><tr><th>الدليل المتخصص</th><th>البند</th><th>القيمة المذكورة في الدليل</th></tr></thead><tbody>"+''.join(rows)+"</tbody></table></div>"
 "<h2>خطوات التحقق قبل الصيانة</h2><p>"+escape(advice)+"</p>"
 "<p><strong>المصدر:</strong> <a rel='nofollow noopener' href='"+escape(model['ref'])+"'>دليل المالك الرسمي لكيا "+escape(model["family"])+" 2023</a>."
 " جميع القيم مرتبطة بنسخة المحرك والفتيس المذكورة في صفحة كل بند، وليست بديلًا عن دليل السيارة المحددة.</p>"
 "</section>")
def main():
 report=[]
 for model in manifest["models"]:
  slug=model["slug"]
  data=get(base+"/wp-json/wp/v2/car-reference-records?slug="+quote(slug))
  pages=[p for p in data if p.get("slug")==slug and p.get("status")=="publish"]
  assert len(pages)==1,slug
  page=pages[0];pid=page["id"]; old=get(bridge+"/post/"+str(pid))
  assert old.get("type")=="a3_car_ref" and old.get("status")=="publish"
  assert old.get("featured_media"),"Hub missing featured image"
  if "a3cr-compare-audit" in old["content"]:
   report.append({"slug":slug,"result":"skipped-already-enhanced","url":page["link"]})
   continue
  items=[s for s in manifest["specs"] if s["model"]==slug]
  block=make_block(model,items)
  fresh=old["content"]+"\n\n"+block
  result=post({"id":pid,"content":fresh,"expected_modified_gmt":old["modified_gmt"]})
  assert result["id"]==pid and result["status"]=="publish"
  live=session.get(page["link"],params={"a3cr_qa":str(int(time.time()))},timeout=45).text
  if notes[slug][0] not in live or "<table" not in live or "og:image" not in live:
   raise RuntimeError("Live HTML post-update check failed for "+slug)
  report.append({"slug":slug,"result":"updated","url":page["link"],"rows":len(items),"featured_media":old["featured_media"]})
  print("ENHANCED",slug, len(items),"technical rows",flush=True)
 (ROOT/"car-reference-hub-audit-20261102.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
 print("RESULT",json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
