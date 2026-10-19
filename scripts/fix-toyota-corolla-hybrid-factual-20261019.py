#!/usr/bin/env python3
"""Fix stale assertion that Corolla Hybrid is import-only: Toyota Egypt lists official brochure.
No unverified current price/availability claims; preserve same post and SEO media.
"""
import os,re,json,urllib.request,time
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
BASE="https://a3tal.com"
KEY=os.environ.get("A3TAL_API_KEY")
if not KEY:raise RuntimeError("No key")
PID=80764;SLUG="toyota-corolla-electrical-hybrid-screen-problems"
MARK="A3TAL_TOYOTA_HYBRID_FACTCHECK_20261019"
INTRO=(
'<p><strong>تويوتا كورولا في مصر</strong> تُعرض بفئات بنزين 1.6، '
'وتدرج تويوتا مصر أيضًا <a href="https://toyota.com.eg/storage/49557/Corolla-2026-Brochure.pdf" target="_blank" rel="noopener noreferrer">'
'كتيب كورولا Hybrid الرسمي</a> ونسخة هايبرد ضمن صفحة اختيار الموديلات. '
'لذلك لا يصح الادعاء أن جميع سيارات كورولا هايبرد في مصر مستوردة بصورة فردية، '
'ولا الجزم بتوافرها الفوري أو سعرها اليوم لمجرد نشر الكتيب. '
'تختلف منظومات بطارية الجر والتبريد والإلكترونيات بين البنزين والهايبرد، '
'وتحدد سنة الصنع ورقم الهيكل وكتيب التجهيز طريقة الفحص الصحيحة.</p>'
)
def api(ep,payload=None):
    h={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Accept":"application/json","User-Agent":"A3tal-Corolla-Official-FactCheck/1.0"}
    b=None
    if payload is not None:b=json.dumps(payload,ensure_ascii=False).encode();h["Content-Type"]="application/json"
    with urllib.request.urlopen(urllib.request.Request(ROOT+ep,data=b,headers=h),timeout=120) as r:return json.load(r)
def verify_public():
    for i in range(3):
        if i:time.sleep(7)
        with urllib.request.urlopen(urllib.request.Request(BASE+"/"+SLUG+"/?factcheck="+str(int(time.time())),headers={"User-Agent":"Mozilla/5.0","Cache-Control":"no-store"}),timeout=40) as r:s=r.read().decode("utf-8","replace")
        if "Corolla-2026-Brochure.pdf" in s and "لا يصح الادعاء" in s:return
    raise RuntimeError("Official factcheck not visible")
def main():
    p=api("/post/"+str(PID))
    if p.get("slug")!=SLUG or p.get("status")!="publish" or not p.get("featured_media"):raise RuntimeError("Bad identity")
    body=p.get("content","")
    if MARK in body:verify_public();print("ALREADY_FACT_CHECKED");return
    # Preserve all other sections; only the two confirmed stale clauses are rewritten.
    pattern=r'<p\b[^>]*>[^<]*<strong>تويوتا كورولا الحالية في مصر</strong>.*?</p>'
    m=list(re.finditer(pattern,body,re.I|re.S))
    if len(m)!=1:raise RuntimeError("Old summary not unique, refusing edit "+str(len(m)))
    changed=body[:m[0].start()]+"<!-- "+MARK+" -->\n"+INTRO+body[m[0].end():]
    phrase="كورولا البنزين المصرية ونسخ Hybrid المستوردة"
    if changed.count(phrase)!=1:raise RuntimeError("Outdated conclusion not unique")
    changed=changed.replace(phrase,"كورولا البنزين ونسخ Hybrid المتاحة في كتيبات تويوتا مصر أو المستوردة حسب رقم الهيكل",1)
    fresh=api("/post/"+str(PID))
    if fresh.get("content")!=body or fresh.get("modified_gmt")!=p.get("modified_gmt"):raise RuntimeError("Concurrent edit")
    try:api("/update-post",{"id":PID,"content":changed,"expected_modified_gmt":p["modified_gmt"]})
    except Exception as e:
        if MARK not in api("/post/"+str(PID)).get("content",""):raise RuntimeError("Write uncertain") from e
    after=api("/post/"+str(PID))
    if after.get("content","").count(MARK)!=1 or after.get("featured_media")!=p["featured_media"]:raise RuntimeError("Validation failed")
    verify_public();print("COROLLA_HYBRID_OFFICIAL_EGYPT_FACTCHECK_LIVE",BASE+"/"+SLUG+"/",flush=True)
if __name__=="__main__":main()
