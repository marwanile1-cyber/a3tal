#!/usr/bin/env python3
"""Stage 7 cited Kia technical drafts. NEVER publishes without reviewed premium photos."""
import os,json,requests,time
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
payload=json.loads((ROOT/"data/car-reference/batch-02-kia-image-gated-drafts.json").read_text(encoding="utf8"))
BASE="https://a3tal.com"
KEY=os.environ["A3TAL_API_KEY"]
URL=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
session=requests.Session()
def entry(row):
 data={
  "kind":"spec","market":"النسخ الواردة في دليل كيا الرسمي لعام 2023؛ تحقق من السوق والمحرك",
  "years":"2023","engine":row["engine"],"category":row["category"],
  "reviewed_at":"2026-11-02",
  "facts":[{"label":k,"value":v} for k,v in row["facts"]],
  "sources":[{"title":"دليل المالك الرسمي لكيا "+row["model"]+" 2023","url":payload["models"][row["model"]]}]
 }
 content=(
 "<p>"+escape(row["intro"])+"</p>"
 "<h2>ما الذي توضحه هذه المواصفات؟</h2>"
 "<p>"+escape(row["detail"])+"</p>"
 "<h2>متى تختلف الأرقام أو المواصفة؟</h2>"
 "<p>"+escape(row["warning"])+"</p>"
 "<p>المصدر الأساسي: <a href='"+escape(payload["models"][row["model"]])+"' rel='nofollow noopener noreferrer'>"
 "جدول المواد والسعات في دليل المالك الرسمي لكيا لعام 2023</a>. قبل الصيانة، طابق المحرك ونوع الفتيس "
 "ومواصفات التجهيز والسوق، ولا تعتبر القيم هنا بديلًا عن دليل سيارتك المحددة.</p>"
 )
 return {
  "title":row["title"],"slug":row["slug"],"kind":"spec",
  "parent_path":"kia/"+row["model"],"status":"draft",
  "content":content,"excerpt":"بيانات صيانة فنية حسب دليل المالك الرسمي. لم تنشر بعد لحين اعتماد الصورة والمراجعة التحريرية.",
  "data":data,"meta_title":row["title"]+" | أعطال.كوم",
  "meta_description":"دليل فني عن "+row["title"]+"، السعات والمواصفة الرسمية والتنبيهات اللازمة قبل الصيانة."
 }
def main():
 rows=payload["items"]
 assert payload["status"]=="draft"
 assert len(rows)==7
 assert len({r["slug"] for r in rows})==7
 assert all(len(r["facts"])>=3 for r in rows)
 records=[entry(r) for r in rows]
 report=[]
 for i in range(0,len(records),7):
  response=session.post(URL,headers={"X-A3tal-Key":KEY,"Content-Type":"application/json"},json={"items":records[i:i+7]},timeout=140)
  response.raise_for_status()
  body=response.json()
  for source,record in zip(records[i:i+7],body.get("results",[])):
   if not record.get("ok") or record.get("status")!="draft":
    raise RuntimeError("Failed to create safe draft "+source["slug"]+": "+repr(record))
   report.append({"status":"draft","slug":source["slug"],"id":record["id"],"url":record["url"]})
   print("DRAFT",record["id"],source["title"],flush=True)
 assert len(report)==7
 (ROOT/"car-reference-batch02-draft-results.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
 print("All 7 source-backed drafts created. No new published pages.")
if __name__=="__main__":main()
