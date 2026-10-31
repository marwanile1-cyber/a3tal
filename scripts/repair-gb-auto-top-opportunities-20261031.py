#!/usr/bin/env python3
"""Safely update two existing high-impression GB Auto pages, preserving exact URLs and media.
One-shot GitHub Actions deployment. Guard live edit timestamps before every mutation.
"""
import json, os, re, urllib.parse, urllib.request, time
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
TAG="A3TAL-GB-AUTO-SEO-20261031-V1"
TARGETS={
  81102: {
    "slug":"ghabbour-auto-maintenance-booking-numbers-branches",
    "modified_gmt":"2026-10-08T00:08:39",
    "featured_media":82888,
  },
  79943:{
    "slug":"%d8%af%d9%84%d9%8a%d9%84%d9%83-%d8%a7%d9%84%d8%b4%d8%a7%d9%85%d9%84-%d8%a3%d9%81%d8%b6%d9%84-%d9%85%d8%b1%d8%a7%d9%83%d8%b2-%d8%ae%d8%af%d9%85%d8%a9-%d8%ba%d8%a8%d9%88%d8%b1-%d8%a3%d9%88%d8%aa%d9%88",
    "modified_gmt":"2026-10-08T00:08:44",
    "featured_media":79944,
  }
}
def get(url, auth=False):
    headers={"Accept":"application/json","User-Agent":"A3tal-GB-Auto-SEO-RevisionGuard/20261031","Cache-Control":"no-cache,no-store"}
    if auth: headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=90) as response:
        return json.load(response)
def publish(body):
    data=json.dumps(body,ensure_ascii=False).encode("utf-8")
    req=urllib.request.Request(API+"/update-post",data=data,headers={
        "Accept":"application/json","Content-Type":"application/json; charset=utf-8",
        "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,
        "User-Agent":"A3tal-GB-Auto-SEO-RevisionGuard/20261031"},method="POST")
    with urllib.request.urlopen(req,timeout=120) as response: return json.load(response)
def wp(pid):
    fields="id,slug,modified_gmt,status,link,featured_media,content,yoast_head_json"
    return get(SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode({"_fields":fields,"_a3tal_audit":"20261031"}))
def validate_original(pid, record, allow_already=False):
    if record["id"]!=pid or record["slug"]!=TARGETS[pid]["slug"] or record["status"]!="publish":
        raise RuntimeError("Post ID/slug/publication identity mismatch: "+str(pid))
    if record["featured_media"]!=TARGETS[pid]["featured_media"]:
        raise RuntimeError("Original featured media changed: "+str(pid))
    content=record["content"]["rendered"]
    if len(content)<4000 or "غبور" not in content or not content.count("<h2"):
        raise RuntimeError("Unexpected original post length or structure: "+str(pid))
    if TAG in content and allow_already:
        print("ALREADY_PUBLISHED",pid,record["link"],flush=True)
        return None
    if TAG in content:
        raise RuntimeError("Duplicate marker in original article: "+str(pid))
    if record["modified_gmt"]!=TARGETS[pid]["modified_gmt"]:
        raise RuntimeError("Concurrent edit detected; abort instead of overwriting: "+str(pid)+": "+str(record["modified_gmt"]))
    seo=record.get("yoast_head_json") or {}
    if seo.get("canonical") and seo["canonical"].rstrip("/")!=record["link"].rstrip("/"):
        raise RuntimeError("Unexpected canonical before update: "+str(pid))
    if not seo.get("og_image"):
        raise RuntimeError("Original post has no social featured image: "+str(pid))
    return content

# The published original at 81102 has a table that already describes seven
# passenger-car brands. Add a dated, verified two-brand amendment before it.
HOTLINE_INSERT=(
  "<!-- "+TAG+" -->\n"
  "<section dir=\"rtl\" aria-label=\"تحديث وسائل تواصل غبور\" "
  "style=\"border:1px solid #cbd5e1;border-right:4px solid #0ea5e9;padding:16px;"
  "margin:20px 0;border-radius:10px;background:#f8fafc\">\n"
  "<h3 style=\"margin-top:0\">تحديث رسمي: لي أوتو وآيكار ضمن علامات جي بي أوتو</h3>\n"
  "<p>بجانب أرقام هيونداي وشيري ومازدا وهافال وشانجان وديبال وجينيسيس الموضحة أدناه، "
  "تظهر الآن <strong>لي أوتو (Li Auto)</strong> و<strong>آيكار (iCAUR)</strong> ضمن خيارات "
  "علامات سيارات الركوب لدى GB Auto. راجع وسيلة الاتصال الخاصة بكل علامة قبل الحجز.</p>\n"
  "<div style=\"overflow-x:auto;width:100%\"><table style=\"width:100%;min-width:450px;border-collapse:collapse\">"
  "<thead><tr><th scope=\"col\">العلامة</th><th scope=\"col\">رقم التواصل</th>"
  "<th scope=\"col\">المصدر والخدمة</th></tr></thead><tbody>"
  "<tr><td>لي أوتو Li Auto</td><td><strong>15156</strong></td>"
  "<td><a href=\"https://liauto-eg.com/contact-us/\">صفحة التواصل الرسمية</a> "
  "(الرقم مذكور بجوار واتساب؛ لا تفترض أنه خط اتصال صوتي للحجز)</td></tr>"
  "<tr><td>آيكار iCAUR</td><td><strong>17833</strong></td>"
  "<td><a href=\"https://icaur-eg.com/landing/ar/\">الموقع الرسمي وحجز الصيانة</a></td></tr>"
  "</tbody></table></div>\n"
  "<p>تنبيه: <a href=\"https://gb-auto.com/en/after_sales/\">محدد مراكز GB Auto الرسمي</a> "
  "يضم أيضًا معارض بيع، ولا يعني ظهور العلامة في شبكة المجموعة أن كل فرع يصلح كل موديل. "
  "تأكد من المركز والتوقيت وتوافر الخدمة قبل التوجه. تمت مراجعة المصادر في 31 أكتوبر 2026.</p>"
  "</section>\n"
)
def update_hotline(original):
    needle="<h2>أرقام حجز صيانة غبور حسب علامة السيارة</h2>"
    if original.count(needle)!=1:raise RuntimeError("Expected booking table heading exactly once")
    return original.replace(needle,HOTLINE_INSERT+needle,1)

SERVICE_HEADING='<h2 style="color: #c00">ما الخدمات التي قد تجدها في مراكز GB Auto؟</h2>'
SAFE_SERVICES=(
    SERVICE_HEADING+"\n<!-- "+TAG+" -->\n"
    "<p>تختلف الخدمات الفعلية حسب العلامة والفرع والموديل؛ فلا يعني وجود اسم غبور "
    "على لافتة معرض أنه مركز صيانة مجهز لكل الإصلاحات. استخدم "
    "<a href=\"https://gb-auto.com/en/after_sales/\">محدد مراكز الخدمة الرسمي</a> "
    "واختر العلامة المطلوبة، ثم أكد بالمكالمة نوع الخدمة وقطع الغيار والموعد.</p>\n"
    "<ul><li>الصيانة الدورية: تحقق من جدول موديلك ومن استقبال المركز له.</li>"
    "<li>تشخيص الأعطال: تأكد من توافر الفني والجهاز المناسبين للمنظومة.</li>"
    "<li>السمكرة والدهان: ليست خدمة موجودة بالضرورة في كل فرع.</li>"
    "<li>قطع الغيار: طابق رقم القطعة مع الشاسيه قبل الشراء.</li>"
    "<li>الضمان والمساعدة على الطريق: اسأل العلامة رسميًا عن شروط التغطية وآلية الدعم.</li>"
    "</ul>"
)
REPLACEMENTS={
 "فروع مثل أبو رواش، العبور، القطامية تتميز بتوفر أجهزة فحص وبرمجة أشمل وكثافة فنيين، بينما الفروع الأصغر تناسب الصيانات الدورية البسيطة.":
 "قد تختلف التجهيزات وعدد الفنيين ونطاق الخدمات بين الفروع؛ لا توجد قاعدة موثقة تُصنف كل فرع كبير باعتباره أفضل. ابدأ بمحدد المراكز الرسمي، ثم تأكد أن الموقع يستقبل موديلك ونوع الإصلاح المطلوب.",
 "نعم، عبر الخط الساخن 16661 أو عبر مواقع وكلاء غبور أوتو، ويحصل الحاجزين مقدمًا على أولوية الخدمة وسرعة التنفيذ.":
 "يفضل الحجز مسبقًا عبر رقم العلامة أو موقعها الرسمي، لكن لا يمكن ضمان أولوية أو موعد تسليم ثابت لجميع الفروع. اطلب تأكيد الفرع والموعد ونوع الخدمة قبل الذهاب.",
 "في الحالات الدورية غالبًا لا يستغرق الأمر أكثر من ساعات، أما لو عطل مفاجئ أو سمكرة فيحتاج أكثر من يوم حسب جدول الأحمال في المركز.":
 "تختلف المدة بحسب بنود الصيانة وقطع الغيار وحجم العمل داخل المركز. اطلب موعد تسليم تقديريًا بعد فحص السيارة، ولا تعتمد على مدة موحدة لجميع الفروع.",
 "الضمانات تغطي الأعطال المصنعية وأي صيانة أو تغييرات داخل الضمان، بشرط وجود الفاتورة وسجل الصيانة في المراكز المعتمدة.":
 "يغطي الضمان ما تنص عليه وثائق الضمان الرسمية الخاصة بالموديل مع الاستثناءات والحدود المحددة، ولا يعني أن جميع الأعطال أو البنود الاستهلاكية مجانية. اطلب نتيجة فحص وقرار تغطية مكتوبًا."
}
def update_branches(original):
    pattern=re.escape(SERVICE_HEADING)+r"\s*<ul>[\s\S]*?</ul>"
    updated,num=re.subn(pattern,SAFE_SERVICES,original,count=1)
    if num!=1:raise RuntimeError("Expected original unverified service bullet list once")
    for old,new in REPLACEMENTS.items():
        if updated.count(old)!=1:raise RuntimeError("FAQ precondition missing or duplicate: "+old[:25])
        updated=updated.replace(old,new,1)
    return updated

# Preflight BOTH pages before any writes.
originals={}
for pid in TARGETS:
    record=wp(pid)
    content=validate_original(pid,record,allow_already=True)
    if content is not None:
        originals[pid]=(record, update_hotline(content) if pid==81102 else update_branches(content))
        print("PREFLIGHT_OK",pid,len(content),len(originals[pid][1]),flush=True)

for pid in TARGETS:
    if pid not in originals:continue
    previous,new_content=originals[pid]
    # Just-in-time guard makes an intervening WordPress edit a hard failure.
    refreshed=wp(pid)
    if refreshed["modified_gmt"]!=previous["modified_gmt"]:
        raise RuntimeError("Concurrent edit since preflight: "+str(pid))
    body={"id":pid,"slug":TARGETS[pid]["slug"],"content":new_content}
    if pid==81102:
        body["meta"]={"_yoast_wpseo_metadesc":
          "رقم توكيل غبور وحجز الصيانة: 16661 لهيونداي وشيري ومازدا، 15050 لهافال وشانجان وديبال، 17020 لجينيسيس، 15156 للي أوتو و17833 لآيكار."}
    response=publish(body)
    if response.get("error") or response.get("ok") is False:
        raise RuntimeError("Bridge returned failure on "+str(pid)+": "+str(response)[:350])
    # Allow WordPress/cache a short moment; never declare success on status alone.
    verified=None
    for attempt in range(5):
        live=wp(pid)
        if TAG in live["content"]["rendered"]:
            verified=live
            break
        time.sleep(3)
    if verified is None:raise RuntimeError("Live public content did not reflect update: "+str(pid))
    if (verified["slug"],verified["status"],verified["featured_media"])!=(
       TARGETS[pid]["slug"],"publish",TARGETS[pid]["featured_media"]):
        raise RuntimeError("Live URL/status/cover changed unexpectedly: "+str(pid))
    before_seo=previous.get("yoast_head_json") or {}
    after_seo=verified.get("yoast_head_json") or {}
    if after_seo.get("canonical")!=before_seo.get("canonical"):
        raise RuntimeError("Canonical changed unexpectedly: "+str(pid))
    if not after_seo.get("og_image"):
        raise RuntimeError("OG cover missing after update: "+str(pid))
    if after_seo.get("robots",{}).get("index")=="noindex":
        raise RuntimeError("Unexpected noindex after update: "+str(pid))
    print("LIVE_VERIFIED",pid,verified["link"],"featured",verified["featured_media"],
          "canonical",after_seo.get("canonical"),flush=True)
print("GB_AUTO_EXISTING_POSTS_SEO_UPDATES_COMPLETE",flush=True)
