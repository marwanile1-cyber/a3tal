#!/usr/bin/env python3
"""Fact-checked, surgical copy QA: distinguish Nov 17 editorial/phone checks
from older branch lists and September price snapshots. No URL/media/schema changes.
"""
import html, json, os, re, time, urllib.request
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
TAG="A3TAL-20261117-DATE-EDITORIAL-QA-V1"
if not KEY:raise SystemExit("Missing A3TAL_API_KEY")

PLANS={
79964:[
("آخر مراجعة: سبتمبر 2026.","آخر مراجعة لأرقام التواصل من المصادر الرسمية: 17 نوفمبر 2026. عناوين الفروع وساعاتها تُؤكد مباشرةً من محدد كل علامة قبل الزيارة."),
("تحديث رسمي – 20 سبتمبر 2026:","بيانات رسمية منشورة سابقًا، وأُعيد التحقق من أرقامها يوم 17 نوفمبر 2026:"),
("الأرقام المؤكدة من المواقع الرسمية بتاريخ 31 أكتوبر 2026:","أرقام خُصصت للعلامات وأُعيد التحقق منها عبر المواقع الرسمية في 17 نوفمبر 2026:"),
("آخر تحديث: سبتمبر 2026.","آخر تحديث تحريري: 17 نوفمبر 2026. تمت مطابقة أرقام خدمة العملاء مع المواقع الرسمية في هذا التاريخ، ولم تتم إعادة فحص جميع الفروع واحدًا واحدًا.")
],
80401:[
("تحديث 20 سبتمبر 2026:","معلومة منشورة في سبتمبر، وأُعيد التحقق من الرقم الرسمي يوم 17 نوفمبر 2026:"),
("آخر مراجعة للأرقام والعناوين: 31 أكتوبر 2026","آخر تحقق من الخط الساخن: 17 نوفمبر 2026. آخر مراجعة تفصيلية لقائمة الفروع والعناوين: 31 أكتوبر 2026.")
],
80669:[
("آخر تحديث فعلي: أغسطس 2026.","آخر تحديث تحريري: 17 نوفمبر 2026. تمت مطابقة رقم 19112 وصفحة حجز الصيانة مع موقع سكودا الرسمي، بينما تعود المراجعة التفصيلية للفروع إلى أغسطس 2026؛ تحقق من حالة الفرع ونوع الخدمة قبل التوجه.")
],
80266:[
("آخر مراجعة للأسعار: 19 سبتمبر 2026.","آخر مراجعة فعلية لأسعار الجداول: 19 سبتمبر 2026. تم تحسين شرح المقال يوم 17 نوفمبر 2026 دون تحديث أسعار البيع؛ الأرقام التالية رصد سابق وليست تسعيرة مؤكدة اليوم."),
("راجعنا الأسعار المعروضة حاليًا للمقاسات الأكثر بحثًا في السوق المصري.","تم رصد أسعار بعض المقاسات الشائعة في السوق المصري في التاريخ المذكور، وقد تغيرت بعدها."),
("أفضل طريقة لمقارنة أسعار الكاوتش في مصر 2027 هي","أفضل طريقة لمقارنة أسعار الكاوتش في مصر هي")
],
80534:[
("تحديث 20 سبتمبر 2026:","بيانات سبق نشرها في سبتمبر، وأُعيد التحقق من الخط الساخن والضمان بالموقع الرسمي يوم 17 نوفمبر 2026:")
],
80056:[]
}
ALL=[79964,80401,79,80669,80266,80534,80056]
def req(path,body=None):
    headers={"Accept":"application/json","User-Agent":"curl/8.5.0","Cache-Control":"no-cache",
             "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY}
    data=None if body is None else json.dumps(body,ensure_ascii=False).encode("utf-8")
    if data is not None:headers["Content-Type"]="application/json; charset=utf-8"
    request=urllib.request.Request(API+path,data=data,headers=headers,method="POST" if data else "GET")
    with urllib.request.urlopen(request,timeout=145) as r:return json.load(r)
def post(pid):return req("/post/"+str(pid))
def verify_identity(pid,before,after):
    keys=("id","slug","status","featured_media","title","type")
    for k in keys:
        if before.get(k)!=after.get(k):
            raise RuntimeError(f"Critical identity or media modified {pid} field {k}")
    oldlinks=re.findall(r'<a\b[^>]*href="([^"]+)"',before["content"],re.I)
    newlinks=re.findall(r'<a\b[^>]*href="([^"]+)"',after["content"],re.I)
    if oldlinks!=newlinks:raise RuntimeError("Unexpected links change "+str(pid))
    if before["content"].count("<img")!=after["content"].count("<img"):
        raise RuntimeError("Inline image dropped "+str(pid))
def transform(pid,content):
    if TAG in content:return None
    if "a3tal-answer-first-seven" not in content:raise RuntimeError("Expected prior revision missing "+str(pid))
    output=content
    for old,new in PLANS.get(pid,[]):
        ct=output.count(old)
        if ct!=1:
            raise RuntimeError(f"Unsafe date edit {pid}, expected exactly one {old!r}, got {ct}")
        output=output.replace(old,new,1)
    if pid==80266:
        comments=list(re.finditer(r'<!--([\s\S]*?)-->',output))
        target=[m for m in comments if "SEO Title" in m.group(1) and "2027" in m.group(1)]
        if len(target)!=1:raise RuntimeError("Expected one obsolete SEO drafting comment in tire article")
        m=target[0];output=output[:m.start()]+output[m.end():]
    if pid==80534:
        comments=list(re.finditer(r'<!--([\s\S]*?)-->',output))
        target=[m for m in comments if "SEO Title" in m.group(1) and "مراكز صيانة" in m.group(1)]
        if len(target)!=1:raise RuntimeError("Expected one Soueast editorial-only comment")
        m=target[0];output=output[:m.start()]+output[m.end():]
    if pid==80056:
        nav=output.find('<nav aria-label="breadcrumb">')
        if not (70<nav<1200 and "body { font-family:" in output[:nav]
                and ".highlight { font-weight: bold;" in output[:nav]):
            raise RuntimeError("Unsafe clutch CSS prefix: stop without deleting content")
        # The initial plain-text stylesheet is visible as text, not CSS.
        output=output[nav:]
        nav_match=re.match(r'<nav aria-label="breadcrumb">\s*(?:&nbsp;\s*){1,3}</nav>\s*',output)
        if nav_match:output=output[nav_match.end():]
        if "body { font-family:" in output[:400]:raise RuntimeError("Visible CSS remains")
    if pid==80534:
        # Remove authoring-only notes about future images. No actual <img> is touched.
        output=re.sub(r'<!--\s*الصورة الداخلية\s+[123][\s\S]*?-->',"",output)
    if pid in (79964,80401,80669,80266,80534):
        # Distinguish editorial update from source validation at the end.
        pass
    if pid==79:
        # No stale dates in this article; no content changes needed.
        if output!=content:raise RuntimeError("Untouched vibration page somehow changed")
        return None
    if output==content:raise RuntimeError("Expected a correction but no change "+str(pid))
    return output

def main():
    plans=[];snapshots={}
    for pid in ALL:
        before=post(pid)
        if before.get("id")!=pid or before.get("status")!="publish" or not before.get("featured_media"):
            raise RuntimeError("Unsafe original "+str(pid))
        snapshots[pid]=before
        content=transform(pid,before.get("content") or "")
        if content is None:print("QA_UNCHANGED_OR_ALREADY_DONE",pid,before.get("link"),flush=True);continue
        if content.count("<img")!=before["content"].count("<img"):
            raise RuntimeError("Preflight image count differs "+str(pid))
        if re.findall(r'<a\b[^>]*href="([^"]+)"',content,re.I) != re.findall(r'<a\b[^>]*href="([^"]+)"',before["content"],re.I):
            raise RuntimeError("Preflight link change "+str(pid))
        if len(content) < len(before["content"])-1800:
            raise RuntimeError("Too much content removed "+str(pid))
        print("COPY_QA_PREFLIGHT",pid,"old",len(before["content"]),"new",len(content),flush=True)
        plans.append((pid,content))
    print("COPY_QA_PREFLIGHTS_COMPLETE",len(plans),flush=True)
    for pid,new in plans:
        before=snapshots[pid]
        latest=post(pid)
        if latest["modified_gmt"]!=before["modified_gmt"] or latest["content"]!=before["content"]:
            raise RuntimeError("Concurrent edit, stopped "+str(pid))
        result=req("/update-post",{"id":pid,"expected_modified_gmt":before["modified_gmt"],"content":new})
        if result.get("ok") is False or result.get("error"):
            raise RuntimeError("Bridge declined "+str(pid))
        final=post(pid)
        verify_identity(pid,before,final)
        if final["content"]!=new:raise RuntimeError("Published content differs "+str(pid))
        print("COPY_QA_PUBLISHED_AND_VERIFIED",pid,final.get("link"),flush=True)
    print("COPY_QA_COMPLETE",len(plans),flush=True)
if __name__=="__main__":main()
