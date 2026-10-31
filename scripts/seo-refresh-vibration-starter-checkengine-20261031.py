#!/usr/bin/env python3
"""Revision-safe SEO improvements for three existing a3tal.com high-impression diagnostics.
GitHub + A3tal Direct Bridge only. No new posts, no URL/media/category changes.
"""
import os, json, re, time, urllib.parse, urllib.request
SITE="https://a3tal.com"
BRIDGE=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
ROWS=[
 {"id":79,"kind":"vibration","cover":81992,"slug":"%d8%b1%d8%ac%d8%a9-%d9%81%d9%8a-%d8%a7%d9%84%d8%b3%d9%8a%d8%a7%d8%b1%d8%a9-%d8%b9%d9%84%d9%89-%d8%b3%d8%b1%d8%b9%d8%a9-80-%d8%a3%d9%88-100-%d8%a3%d9%88-120","last":"2026-10-03T13:13:47",
  "seo_title":"رجة السيارة على سرعة 80 و100 و120: الأسباب والفحص | أعطال",
  "desc":"رجة السيارة على سرعة 80 أو 100 أو 120؟ اعرف الفرق بين الترصيص وتلف الإطار واعوجاج الجنط والكوبلن، ومتى يجب التوقف وفحص الإطارات فورًا."},
 {"id":80524,"kind":"starter","cover":80525,"slug":"bad-starter-motor-symptoms-repair-guide","last":"2026-10-09T00:41:02",
  "seo_title":"المارش بيكتك ومش بيدور؟ الفرق بين المارش والبطارية | أعطال",
  "desc":"المارش مش بيدور أو بيعمل تكة؟ الفرق بين التكة الواحدة والتكتكة السريعة، وفحص البطارية والأرضي وهبوط الجهد قبل شراء مارش جديد."},
 {"id":81039,"kind":"checkengine","cover":81040,"slug":"what-to-do-when-check-engine-light-is-on","last":"2026-10-09T00:39:56",
  "seo_title":"لمبة Check Engine منورة أو بتومض؟ الأسباب ومتى توقف | أعطال",
  "desc":"لمبة Check Engine ثابتة أم بتومض؟ اعرف متى يمكن الوصول للورشة بحذر، ومتى توقف العربية فورًا، وأهمية قراءة أكواد P0300 والميسفاير قبل مسحها."},
]
MARK="a3tal-diagnostic-refresh-20261031"
def api(url,payload=None):
    headers={"Accept":"application/json","Cache-Control":"no-cache,no-store","User-Agent":"A3tal-Diagnostic-Ctr-Refresh/20261031","X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY}
    blob=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
    if blob is not None: headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,headers=headers,data=blob,method="POST" if blob is not None else "GET")
    with urllib.request.urlopen(req,timeout=120) as r:return json.load(r)
def post(pid):return api(BRIDGE+"/post/"+str(pid))
def public(pid):
    url=SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?"+urllib.parse.urlencode({"_fields":"id,title,slug,modified_gmt,status,link,featured_media,yoast_head_json","check":"20261031"})
    return api(url)
def sid(kind): return MARK+"-"+kind
def insert_before_first_h2(raw,block):
    matches=list(re.finditer(r"<h2(?:\s[^>]*)?>",raw,re.I))
    if len(matches)<4:raise RuntimeError("Diagnostic post has too few headings for safe patch")
    off=matches[0].start()
    return raw[:off]+block+"\n"+raw[off:]
VIBRATION=(
'<section id="'+sid("vibration")+'" class="a3tal-diagnostic-safety" dir="rtl">'
'<h2>هل رجة العربية على سرعة 80 أو 100 خطيرة؟</h2>'
'<p><strong>لا تختبر الرجة بتجاوز السرعة القانونية.</strong> لو الرجة شديدة أو زادت فجأة، أو ظهر انتفاخ في جنب الإطار، أو شعر السائق بأن الدركسيون فقد ثباته، أوقف السيارة في مكان آمن وافحصها قبل استكمال الطريق. الإطار الذي به انتفاخ أو تلف ظاهر لا يكفي ترصيصه أو نقله للخلف، بل يجب تقييم استبداله.</p>'
'<p>لو الرجة تظهر عند نطاق سرعة محدد والسيارة مستقرة دون علامات خطر، يبدأ الفني بفحص <strong>ضغط الإطارات الباردة حسب ملصق السيارة</strong> وتآكلها وثبات الجنوط والعجل، ثم ترصيص العجلات الأربع. استمرار الرجة رغم الترصيص يستدعي قياس اعوجاج الجنط والإطار (Runout) وفحص <strong>Road Force Variation</strong> عندما يتوفر الجهاز المناسب. ضبط الزوايا ليس بديلًا عن فحص اتزان العجل.</p>'
'<p>لو الرجة مرتبطة بالفرامل تحديدًا فاقرأ <a href="https://a3tal.com/steering-wheel-vibrates-when-braking-diagnosis/">رعشة الدركسيون عند الفرامل</a>. أما الرجة والسيارة واقفة على D فلها <a href="https://a3tal.com/car-vibration-in-drive-at-idle-diagnosis/">تشخيص مستقل لقواعد المحرك والميسفاير</a>، وليست بالضرورة مشكلة ترصيص.</p>'
'<p><strong>مرجع فني:</strong> <a href="https://www.nhtsa.gov/vehicle-safety/tires" rel="noopener noreferrer">تعليمات سلامة الإطارات والترصيص من NHTSA</a>.</p>'
'</section>'
)
STARTER=(
'<section id="'+sid("starter")+'" class="a3tal-diagnostic-safety" dir="rtl">'
'<h2>المارش بيكتك ولا يدور: كيف تحدد أول فحص؟</h2>'
'<p><strong>التكتكة السريعة المتكررة</strong> تضع البطارية وكابلاتها والقواطيش والأرضي في بداية الفحص. أما <strong>تكة واحدة دون دوران</strong> فلا تؤكد تلف المارش؛ يجب التأكد من البطارية تحت الحمل وهبوط الجهد في كابلي الموجب والأرضي ودائرة الـSolenoid. إذا كان المارش يدور بسرعة طبيعية لكن المحرك لا يشتغل، انتقل لتشخيص الوقود والإشعال بدل شراء مارش جديد.</p>'
'<p><strong>إمتى توقف المحاولة؟</strong> عند سماع طحن متكرر أو شم رائحة احتراق أو ظهور دخان؛ لا تكرر تشغيل المارش. قياس هبوط الجهد أثناء سحب التيار العالي وفحص أطراف المارش من عمل الفني المؤهل، مع تأمين السيارة على P أو N وفرامل الانتظار. لا تقصر أطراف المارش أو تطرق جسمه باعتبارها طريقة تشخيص آمنة.</p>'
'<p>ابدأ من <a href="https://a3tal.com/car-ground-voltage-drop-test/">اختبار أرضي السيارة Voltage Drop</a>، '
'ولو لا يصل أمر تشغيل راجع <a href="https://a3tal.com/ignition-switch-failure-symptoms-diagnosis/">أعراض تلف الكونتاكت</a>. ولو البطارية تضعف بعد التشغيل راجع <a href="https://a3tal.com/bad-alternator-symptoms-testing-guide/">أعطال الدينامو</a>.</p>'
'<p><strong>مرجع فني:</strong> <a href="https://www.aaa.com/autorepair/articles/14-reasons-why-your-car-wont-start" rel="noopener noreferrer">دليل AAA لتشخيص عدم تشغيل السيارة</a>.</p>'
'</section>'
)
CHECK_ENGINE=(
'<section id="'+sid("checkengine")+'" class="a3tal-diagnostic-safety" dir="rtl">'
'<h2>لمبة Check Engine بتومض: توقف ولا تكمّل؟</h2>'
'<p><strong>إذا كانت اللمبة تومض أثناء القيادة</strong>، خفف الحمل فورًا وابحث عن مكان آمن للتوقف، خصوصًا مع رعشة أو تقطيع أو فقدان سحب. الوميض قد يشير إلى Misfire يمكن أن يضر المحول الحفاز؛ لا تستمر في المشوار على أمل أن تختفي اللمبة. اطلب مساعدة فنية أو سطحة عند استمرار الوميض أو عدم انتظام عمل المحرك. إذا كانت ثابتة ولا توجد علامات خطورة، تجنب الحمل الشديد وافحص السيارة قريبًا بدل تجاهل التحذير.</p>'
'<p>قبل مسح اللمبة، احفظ <strong>Stored/Pending Codes</strong> وFreeze Frame إن توفر. كود <a href="https://a3tal.com/p0300-random-misfire/">P0300</a> يرتبط باختلال احتراق عشوائي، بينما <a href="https://a3tal.com/p0301-p0302-p0303-p0304-cylinder-misfire/">P0301 إلى P0304</a> تحدد السلندر الذي رصد الكمبيوتر فيه الاختلال، لكنها لا تثبت وحدها أن الكويل أو البوجيه تالف. راجع أيضًا <a href="https://a3tal.com/car-dashboard-warning-lights-meaning/">معاني لمبات التابلوه الأخرى</a> إذا ظهر تحذير زيت أو حرارة.</p>'
'<p><strong>مرجع فني:</strong> <a href="https://www.aaa.com/autorepair/articles/safety/the-check-engine-light-common-causes-and-how-to-fix-it" rel="noopener noreferrer">شرح AAA للفرق بين اللمبة الثابتة والوامضة</a>.</p>'
'</section>'
)
BLOCK={"vibration":VIBRATION,"starter":STARTER,"checkengine":CHECK_ENGINE}
def build(item,raw):
    kind=item["kind"]
    if sid(kind) in raw:return None
    if len(raw)<5000 or raw.count("<h2")<5:raise RuntimeError("Unexpected pre-existing content length/layout: "+kind)
    body=insert_before_first_h2(raw,BLOCK[kind])
    # Correct action text that could understate a flashing engine warning.
    if kind=="checkengine":
        old="خفف الحمل والسرعة وتجنب القيادة القوية، وتوقف بأمان إذا كان المحرك يهتز بشدة أو ظهرت تحذيرات حرارة أو ضغط زيت."
        if old in body:
            body=body.replace(old,"خفف الحمل وتوقف في مكان آمن إذا استمر الوميض أو كانت هناك رعشة أو فقد قوة؛ لا تكمل المشوار قبل الفحص.",1)
    if kind=="starter":
        old="قبل أن تطلب الونش، جرب هذه الحيل التي نستخدمها في الورش:"
        if old in body:
            body=body.replace(old,"قبل تغيير المارش، اطلب فحص هذه النقاط بالترتيب، وتُجرى قياسات التيار العالي لدى فني مؤهل:",1)
    if body.count('id="'+sid(kind)+'"')!=1:raise RuntimeError("Duplicate marker in updated text: "+kind)
    if len(body)<len(raw)+700:raise RuntimeError("Insufficient new useful content: "+kind)
    return body
preflight=[]
for item in ROWS:
    live=post(item["id"])
    public_live=public(item["id"])
    if (live["id"],live["status"],live["slug"],live["featured_media"])!=(item["id"],"publish",item["slug"],item["cover"]):
        raise RuntimeError("Bridge live identity changed "+str(item["id"]))
    if public_live["modified_gmt"]!=item["last"]:raise RuntimeError("Existing post modified since audit "+str(item["id"]))
    canonical=public_live["yoast_head_json"].get("canonical")
    og=public_live["yoast_head_json"].get("og_image")
    if not canonical or not og or public_live["yoast_head_json"].get("robots",{}).get("index")=="noindex":
        raise RuntimeError("Original OG/index canonical integrity bad "+str(item["id"]))
    content=build(item,live["content"])
    if content is None:
        print("ALREADY_APPLIED",item["id"],live["link"],flush=True)
        continue
    preflight.append((item,live,public_live,content))
    print("DIAGNOSTIC_PREFLIGHT_OK",item["id"],len(live["content"]),len(content),flush=True)
for item,previous,previous_pub,content in preflight:
    latest=post(item["id"])
    if latest["modified_gmt"]!=previous["modified_gmt"]:
        raise RuntimeError("Concurrent WordPress revision; abort "+str(item["id"]))
    response=api(BRIDGE+"/update-post",{
        "id":item["id"],"slug":item["slug"],"expected_modified_gmt":latest["modified_gmt"],
        "content":content,
        "meta":{
            "_yoast_wpseo_title":item["seo_title"],
            "_yoast_wpseo_metadesc":item["desc"],
            "_yoast_wpseo_focuskw":("رجة السيارة على سرعة 80" if item["kind"]=="vibration" else
                                    "مارش السيارة لا يعمل" if item["kind"]=="starter" else
                                    "لمبة Check Engine"),
            "_yoast_wpseo_opengraph-title":item["seo_title"],
            "_yoast_wpseo_opengraph-description":item["desc"],
            "_yoast_wpseo_twitter-title":item["seo_title"],
            "_yoast_wpseo_twitter-description":item["desc"]
        }
    })
    if response.get("error") or response.get("ok") is False:
        raise RuntimeError("Bridge declined update "+str(item["id"])+str(response)[:180])
    confirmed=None
    for attempt in range(5):
        w=post(item["id"]);p=public(item["id"])
        if sid(item["kind"]) in w["content"] and p["yoast_head_json"].get("title")==item["seo_title"]:
            confirmed=(w,p);break
        time.sleep(3)
    if confirmed is None:raise RuntimeError("Published marker or SEO title missing "+str(item["id"]))
    w,p=confirmed
    if (w["slug"],w["status"],w["featured_media"])!=(item["slug"],"publish",item["cover"]):
        raise RuntimeError("Post slug/status/cover changed unexpectedly "+str(item["id"]))
    beforeseo=previous_pub["yoast_head_json"];afterseo=p["yoast_head_json"]
    if (afterseo.get("canonical")!=beforeseo.get("canonical") or
        afterseo.get("robots",{}).get("index")=="noindex" or
        afterseo.get("og_image",[{}])[0].get("url")!=beforeseo.get("og_image",[{}])[0].get("url") or
        afterseo.get("description")!=item["desc"] or afterseo.get("og_description")!=item["desc"]):
        raise RuntimeError("SEO guard failed after update "+str(item["id"]))
    print("DIAGNOSTIC_LIVE_VERIFIED",item["id"],w["link"],"image",w["featured_media"],"canonical",afterseo["canonical"],flush=True)
print("A3TAL_DIAGNOSTIC_TRIO_UPDATES_COMPLETE",flush=True)
