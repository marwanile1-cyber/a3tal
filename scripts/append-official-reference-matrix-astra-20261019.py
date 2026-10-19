#!/usr/bin/env python3
"""Ground two previously source-light diagnostic guides using verified official resources.
Identity, permalink, hero and existing technical sections are preserved.
"""
import os,re,json,urllib.request,html,time
BASE="https://a3tal.com";ROOT=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY")
if not KEY:raise RuntimeError("Missing bridge key")
RECORDS={
  80836:("hyundai-matrix-fault-codes-dtc-dictionary","A3TAL_MATRIX_OBD_EPA_SOURCE_20261019",
  """<section class="a3tal-editorial-source" aria-label="مرجع قراءة كود OBD"><h2>مرجع موثوق لفهم لمبة Check Engine</h2><p>تشرح <a href="https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1009Z15.TXT" target="_blank" rel="noopener noreferrer">وكالة حماية البيئة الأمريكية EPA في وثيقة شرح تشخيص OBD</a> أن الكمبيوتر يحتفظ برمز يوضح نوع الخلل المكتشف، وأن وميض لمبة المحرك يرتبط في بعض الحالات بتقطيع شديد قد يضر بالمحول الحفاز. هذه وثيقة عامة لشرح نظام OBD وليست كتالوج صيانة هيونداي ماتريكس؛ لذلك تظل قيم الجهد والمقاومة وأرقام القطع حسب سنة السيارة ودليل محركها.</p></section>"""),
  80853:("opel-astra-j-fault-codes-dtc-dictionary","A3TAL_ASTRA_MANUAL_SOURCE_20261019",
  """<section class="a3tal-editorial-source" aria-label="كتيب أوبل أسترا J"><h2>كيف تتحقق من معنى رسالة الشاشة في كتيب السيارة؟</h2><p>تنشر <a href="https://www.vauxhall.co.uk/owners/information-and-safety/owners-manuals.html" target="_blank" rel="noopener noreferrer">فوكسهول، العلامة الشقيقة لأوبل، مكتبة رسمية لكتيبات المالك بحسب سنة السيارة</a>، وبها أدلة Astra قديمة وحديثة. اختر سنة الإنتاج والفئة وكتيبها الصحيح عند مراجعة رسائل العدادات؛ لا تفترض أن كودًا في دليل نسخة بريطانية يطابق جميع التجهيزات المصرية دون مراجعة وحدة السيارة وأكواد OBD المسجلة بالفعل.</p></section>""")
}
def api(endpoint,data=None):
    payload=json.dumps(data,ensure_ascii=False).encode() if data is not None else None
    h={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Accept":"application/json","User-Agent":"A3talReferenceFinalizer/1.0"}
    if payload is not None:h["Content-Type"]="application/json"
    req=urllib.request.Request(ROOT+endpoint,headers=h,data=payload)
    with urllib.request.urlopen(req,timeout=100) as x:return json.load(x)
def verify_public(slug,mark):
    for z in range(3):
        if z:time.sleep(5)
        r=urllib.request.Request(BASE+"/"+slug+"/?sourceqa="+str(int(time.time())),headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(r,timeout=45) as x:body=x.read().decode("utf-8","replace")
        if "مرجع موثوق" in body or "كيف تتحقق من معنى رسالة الشاشة" in body:
            if 'a3tal-original-diagnostic-flow-b' not in body:raise RuntimeError("Image unexpectedly disappeared "+slug)
            return
    raise RuntimeError("Source reference not visible "+slug)
def main():
    for pid,(slug,mark,section) in RECORDS.items():
        x=api("/post/"+str(pid))
        if x.get("slug")!=slug or x.get("status")!="publish" or not x.get("featured_media"):raise RuntimeError("Identity failed "+slug)
        if mark in x.get("content",""):
            verify_public(slug,mark);print("ALREADY_SOURCE_CONFIRMED",slug,flush=True);continue
        if not x.get("content","").count("a3tal-original-diagnostic-flow-b"):raise RuntimeError("Reviewed diagram not present "+slug)
        body=x["content"]
        pos=re.search(r'<h2\b[^>]*>\s*الخلاصة\s*</h2>',body,re.I)
        if not pos:raise RuntimeError("Conclusion missing "+slug)
        insert="<!-- "+mark+" -->\n"+section+"\n"
        new=body[:pos.start()]+insert+body[pos.start():]
        y=api("/post/"+str(pid))
        if y.get("modified_gmt")!=x.get("modified_gmt") or y.get("content")!=body:raise RuntimeError("Concurrent edit "+slug)
        try:api("/update-post",{"id":pid,"content":new,"expected_modified_gmt":x["modified_gmt"]})
        except Exception as err:
            if mark not in api("/post/"+str(pid)).get("content",""):raise RuntimeError("Write uncertain, don't repeat "+slug) from err
        z=api("/post/"+str(pid))
        if z.get("content","").count(mark)!=1 or z.get("featured_media")!=x.get("featured_media"):raise RuntimeError("Readback failed "+slug)
        verify_public(slug,mark)
        print("OFFICIAL_REFERENCE_PUBLISHED",BASE+"/"+slug+"/",flush=True)
    print("TWO_OFFICIAL_REFERENCES_VERIFIED",flush=True)
if __name__=="__main__":main()
