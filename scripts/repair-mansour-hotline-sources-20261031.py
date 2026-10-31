#!/usr/bin/env python3
"""Patch existing Mansour multi-brand hotline page with official branch classification sources."""
import json, os, urllib.request, urllib.parse, time
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
PID=79964
SLUG="%d8%a7%d9%84%d8%af%d9%84%d9%8a%d9%84-%d8%a7%d9%84%d8%b4%d8%a7%d9%85%d9%84-%d8%a3%d8%b1%d9%82%d8%a7%d9%85-%d9%85%d8%b1%d8%a7%d9%83%d8%b2-%d8%ae%d8%af%d9%85%d8%a9-%d8%a7%d9%84%d9%85%d9%86%d8%b5%d9%88"
EXPECTED_DATE="2026-10-08T00:08:40"
FEATURED=82887
MARKER="A3TAL-MANSOUR-SERVICE-SEO-20261031-V1"
def request(url, body=None, auth=False):
    headers={"Accept":"application/json","User-Agent":"A3tal-Mansour-Guarded-Correction/20261031","Cache-Control":"no-cache,no-store"}
    if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=json.dumps(body,ensure_ascii=False).encode("utf-8") if body is not None else None
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,headers=headers,data=raw,method="POST" if raw is not None else "GET")
    with urllib.request.urlopen(req,timeout=120) as response:return json.load(response)
def wp():
    return request(SITE+"/wp-json/wp/v2/posts/"+str(PID)+"?"+urllib.parse.urlencode({
        "_fields":"id,slug,status,link,modified_gmt,featured_media,content,yoast_head_json",
        "seo_check":"20261031"}))
old=wp()
if (old["id"],old["slug"],old["status"],old["featured_media"])!=(PID,SLUG,"publish",FEATURED):
    raise RuntimeError("Post identity or featured image mismatch")
text=old["content"]["rendered"]
if MARKER in text:
    print("MANSOUR_ALREADY_UPDATED",old["link"],flush=True)
    raise SystemExit(0)
if old["modified_gmt"]!=EXPECTED_DATE:
    raise RuntimeError("Post edited since audit: stop, no overwrite")
if len(text)<11000 or "منصور" not in text or text.count("<h2")<8:
    raise RuntimeError("Unexpected original content")
before_seo=old.get("yoast_head_json") or {}
if not before_seo.get("og_image") or before_seo.get("robots",{}).get("index")=="noindex":
    raise RuntimeError("Original OG or index metadata invalid")
FIRST_HEADING="<h2>الخط الساخن لتوكيل منصور حسب العلامة</h2>"
if text.count(FIRST_HEADING)!=1:raise RuntimeError("First hotline heading changed")
INTRO=(
  "<!-- "+MARKER+" -->\n"
  "<aside dir=\"rtl\" style=\"border-right:4px solid #0ea5e9;background:#f8fafc;"
  "border-radius:8px;padding:14px 18px;margin:16px 0\">"
  "<p><strong>الأرقام المؤكدة من المواقع الرسمية بتاريخ 31 أكتوبر 2026:</strong> "
  "رقم خدمة عملاء <a href=\"https://www.chevroletarabia.com/eg-ar/contact-us\">شيفروليه</a> "
  "و<a href=\"https://www.mgmotor.com.eg/faqs/?lang=ar\">MG</a> "
  "و<a href=\"https://www.opelegypt.net/ar/tools/contact.html\">أوبل</a> هو <strong>16424</strong>، "
  "بينما رقم التواصل المنشور على <a href=\"https://www.peugeot-eg.com/ar/\">بيجو مصر</a> "
  "هو <strong>16674</strong>. الرقم لا يثبت أن الفرع المطلوب مركز صيانة؛ "
  "اختيار الفرع يعتمد على العلامة والخدمة.</p>"
  "<p>للتأكد من عنوان الخدمة قبل التحرك استخدم "
  "<a href=\"https://www.opelegypt.net/ar/tools/opel-locate-dealer.html\">محدد أوبل الرسمي</a> "
  "أو <a href=\"https://www.mgmotor.com.eg/locations-showrooms/?lang=ar\">محدد MG الرسمي</a>، "
  "مع اختيار تبويب «مراكز الخدمة» بدل «المعارض» عند البحث عن صيانة.</p>"
  "</aside>\n"
)
updated=text.replace(FIRST_HEADING,INTRO+FIRST_HEADING,1)
fixes={
    "<p>في MG مثلًا يظهر موقع الشيخ زايد ضمن شبكة العلامة، ويعرض رقمًا خاصًا بالموقع هو <strong>16423</strong> حاليًا.</p>":
    "<p>في محدد MG الرسمي يظهر موقع الشيخ زايد ضمن <strong>المعارض</strong>، ويعرض الرقم الخاص بالموقع <strong>16423</strong>. لا تتعامل مع هذا العنوان على أنه مركز صيانة MG إلا إذا ظهر ضمن تبويب مراكز الخدمة أو أكد الوكيل ذلك.</p>",
    "<p>منصور لديها وجود في بني غالب بأسيوط، وهو من المواقع المهمة لخدمة الصعيد.</p>":
    "<p>تختلف صفة موقع منصور في بني غالب حسب العلامة: يصنفه محدد MG الرسمي ضمن <strong>المعارض</strong>، بينما يدرجه محدد أوبل ضمن <strong>مبيعات وخدمات ما بعد البيع</strong>. عند الحجز، حدد علامتك والخدمة المطلوبة ولا تعتمد على اسم الفرع وحده.</p>",
    "<p>شبكة MG الرسمية مثلًا تعرض Mansour – Assuit (Bani Ghaleb) ضمن مواقع العلامة.</p>":
    "<p>مصادر التحقق: <a href=\"https://www.mgmotor.com.eg/locations-showrooms/?lang=ar\">تصنيف فروع MG الرسمي</a> و<a href=\"https://www.opelegypt.net/ar/tools/opel-locate-dealer.html\">تصنيف فروع أوبل الرسمي</a>. أكد استقبال موديلك قبل زيارة الموقع.</p>"
}
for a,b in fixes.items():
    if updated.count(a)!=1:raise RuntimeError("Expected original branch description exactly once: "+a[:70])
    updated=updated.replace(a,b,1)
if len(updated)<len(text) or MARKER not in updated:raise RuntimeError("New content validation failed")
if wp()["modified_gmt"]!=old["modified_gmt"]:
    raise RuntimeError("Concurrent update detected before writing")
print("MANSOUR_PREFLIGHT_OK",len(text),len(updated),flush=True)
resp=request(API+"/update-post",{"id":PID,"slug":SLUG,"content":updated,
  "meta":{"_yoast_wpseo_metadesc":
      "توكيل منصور الخط الساخن: 16424 لشيفروليه وMG وأوبل، و16674 لبيجو. روابط رسمية للفروع والفرق بين المعارض ومراكز الصيانة."}},True)
if resp.get("ok") is False or resp.get("error"):
    raise RuntimeError("Bridge refused update: "+str(resp)[:280])
verified=None
for _ in range(5):
    live=wp()
    if MARKER in live["content"]["rendered"]:
        verified=live;break
    time.sleep(3)
if verified is None:raise RuntimeError("Live public post missing verified patch")
if (verified["id"],verified["slug"],verified["status"],verified["featured_media"])!=(PID,SLUG,"publish",FEATURED):
    raise RuntimeError("Post/cover changed after update")
after_seo=verified.get("yoast_head_json") or {}
if after_seo.get("canonical")!=before_seo.get("canonical") or not after_seo.get("og_image") or after_seo.get("robots",{}).get("index")=="noindex":
    raise RuntimeError("Canonical/OG/index regression after update")
print("MANSOUR_LIVE_VERIFIED",verified["link"],verified["featured_media"],flush=True)
