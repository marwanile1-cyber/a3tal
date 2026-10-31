#!/usr/bin/env python3
"""Guarded in-place diagnostic cross-link repair for P0172 P0430 P0301-4.
Uses only A3tal Direct Bridge via GitHub Actions, no new WP posts or media.
Maintains original title, slug, permalink, featured_media, Yoast SEO and canonical.
"""
import os, json, re, time, urllib.parse, urllib.request
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
MARK="a3tal-rich-bank2-single-misfire-crosscodes-20261031"
PAGES=[
 {"id":83443,"type":"rich","slug":"p0172-system-too-rich-bank1-diagnosis","last":"2026-10-10T11:05:26","cover":83445},
 {"id":83054,"type":"bank2","slug":"p0430-catalyst-efficiency-bank-2","last":"2026-10-03T14:51:10","cover":83056},
 {"id":82366,"type":"single","slug":"p0301-p0302-p0303-p0304-cylinder-misfire","last":"2026-09-21T12:17:10","cover":82367}
]
RICH=(
'<section id="'+MARK+'-rich" dir="rtl" class="a3tal-diagnostic-crosscodes">'
'<h2>كود P0172 مع P0300 أو P0420: بأي عطل تبدأ؟</h2>'
'<p>وجود خليط غني في Bank 1 مع اختلال الاحتراق أو كفاءة المحول الحفاز لا يعني شراء رشاشات أو علبة بيئة فورًا. سجل الأكواد وFreeze Frame، ثم قارن تصحيحات الوقود في وضع Closed Loop ومؤشرات الميسفاير تحت ظروف العطل. اقرأ النمط قبل اختيار القطعة.</p>'
'<div class="g-table-wrap"><table><thead><tr><th>الأعراض والأكواد</th><th>اتجاه الفحص الأول</th></tr></thead><tbody>'
'<tr><td>P0172 مع <a href="https://a3tal.com/فك-لغز-كود-العطل-p0300-في-شيفروليه-دليل-التش/">P0300</a> ورعشة</td><td>حدد شدة الميسفاير وسلامة القيادة، ثم افحص ضغط الوقود والرشاشات والإشعال قبل تفسير Fuel Trim وحده</td></tr>'
'<tr><td>P0172 مع <a href="https://a3tal.com/p0420-catalyst-efficiency-bank-1/">P0420</a></td><td>اعالج سبب الخليط الغني أولًا ثم افحص العادم وCatalyst Monitor؛ تغيير المحول قبل تصحيح الاحتراق قد يعيد العطل</td></tr>'
'<tr><td>بوجيه مبلول بنزين وصعوبة تشغيل</td><td>قارن الشرارة بعمل الرشاش وضغط الوقود؛ <a href="https://a3tal.com/spark-plug-wet-with-fuel-diagnosis/">دليل البوجيه المبلول</a> يفصل الاحتمالات</td></tr>'
'<tr><td>تصحيحات سالبة دون رعشة قوية</td><td>راجع <a href="https://a3tal.com/stft-ltft-fuel-trim-diagnosis/">STFT وLTFT</a> في السلانسيه والحمل، وبيانات ECT وMAF وEVAP قبل الاستبدال</td></tr>'
'</tbody></table></div>'
'<p>إذا كانت لمبة Check Engine تومض مع رعشة شديدة أو توجد رائحة بنزين قوية، توقف بأمان واطلب الفحص. الأرقام والحدود الدقيقة تُؤخذ من تعليمات المحرك المحدد؛ لا توجد قراءة Fuel Trim واحدة تثبت تلف رشاش.</p>'
'</section>'
)
BANK2=(
'<section id="'+MARK+'-bank2" dir="rtl" class="a3tal-diagnostic-crosscodes">'
'<h2>إذا ظهر P0430 مع أكواد الخليط أو الميسفاير: ما ترتيب الإصلاح؟</h2>'
'<p><strong>P0430 يخص Bank 2</strong>، بينما P0420 يخص Bank 1؛ ولا يثبت أي منهما بمفرده انسداد علبة البيئة أو تلف حساس الأكسجين. يجب تحديد البنك ومكان الحساس من بيانات المحرك قبل القياس.</p>'
'<div class="g-table-wrap"><table><thead><tr><th>الأكواد المصاحبة</th><th>الفحص المقدم على تغيير Catalyst</th></tr></thead><tbody>'
'<tr><td><a href="https://a3tal.com/فك-لغز-كود-العطل-p0300-في-شيفروليه-دليل-التش/">P0300</a> أو <a href="https://a3tal.com/p0301-p0302-p0303-p0304-cylinder-misfire/">P0301–P0304</a></td><td>شخّص الاحتراق والشرارة والحقن وضغط الأسطوانات أولًا؛ الميسفاير الشديد قد يسخن المحول ويُتلفه</td></tr>'
'<tr><td><a href="https://a3tal.com/p0171-system-too-lean-bank-1-diagnosis/">P0171</a> أو <a href="https://a3tal.com/p0172-system-too-rich-bank1-diagnosis/">P0172</a></td><td>هذه أكواد Bank 1؛ لا تنقل نتيجتها تلقائيًا إلى Bank 2. قارن Fuel Trim لكل بنك وابحث عن سبب مشترك أو عطل مستقل</td></tr>'
'<tr><td>P0430 وحده بعد استقرار أداء المحرك</td><td>افحص تسريب العادم وحساسات O2/A/F وشروط Catalyst Monitor، وراجع نشرات الخدمة قبل الاستبدال</td></tr>'
'<tr><td>P0430 و<a href="https://a3tal.com/p0420-catalyst-efficiency-bank-1/">P0420</a> معًا</td><td>ابدأ بالأسباب المؤثرة في البنكيْن مثل التغذية أو تسريب العادم ثم اختبر كل بنك، لا تفترض تلقائيًا تلف محفزين</td></tr>'
'</tbody></table></div>'
'<p>توضح <a href="https://www.walkerexhaust.com/support/tech-tips/diagnosing-catalytic-converter-issues.html" rel="noopener noreferrer">إرشادات Walker الفنية لتشخيص المحول الحفاز</a> أهمية إصلاح أكواد المحرك والتسريب قبل استبدال المحول. راجع أيضًا <a href="https://a3tal.com/stft-ltft-fuel-trim-diagnosis/">شرح Fuel Trim</a> لتفسير قراءة كل Bank.</p>'
'</section>'
)
SINGLE=(
'<section id="'+MARK+'-single" dir="rtl" class="a3tal-diagnostic-crosscodes">'
'<h2>كود Misfire لسلندر محدد: متى تفحص البوجيه ومتى تراجع الخليط؟</h2>'
'<p>عند ظهور P0301 أو P0302 أو P0303 أو P0304، لا يكفي رقم السلندر لإدانة الكويل. اقرأ Freeze Frame، وحدد ترتيب الأسطوانات من بيانات الصانع، ثم افحص حالة البوجيه والفيشة وسلوك العطل قبل أي استبدال. يُجرى اختبار تبديل الكويل بين الأسطوانات بواسطة فني مع مراعاة متطلبات السلامة.</p>'
'<div class="g-table-wrap"><table><thead><tr><th>الملاحظة</th><th>ما الفحص التالي؟</th></tr></thead><tbody>'
'<tr><td>كود الميسفاير انتقل لسلندر آخر بعد تبديل كويلين متماثلين</td><td>يزيد الاشتباه في الكويل الذي انتقل معه العطل، مع التأكد من الفيشة والبوجيه والظروف نفسها</td></tr>'
'<tr><td>الكود ثابت في السلندر نفسه رغم سلامة الإشعال</td><td>افحص البخاخ والتسريب قرب مجرى السحب وضغط الأسطوانة قبل تغيير مزيد من الكويلات</td></tr>'
'<tr><td>البوجيه <a href="https://a3tal.com/spark-plug-wet-with-fuel-diagnosis/">مبلول بالبنزين</a></td><td>لا تفترض أن الرشاش تالف؛ قد تكون الشرارة مفقودة أو أن الرشاش يسرب أو توجد مشكلة ميكانيكية</td></tr>'
'<tr><td>أكثر من سلندر مع <a href="https://a3tal.com/فك-لغز-كود-العطل-p0300-في-شيفروليه-دليل-التش/">P0300</a> أو <a href="https://a3tal.com/p0172-system-too-rich-bank1-diagnosis/">P0172</a></td><td>ابدأ بالأسباب المشتركة: الهواء والوقود والإشعال والتوقيت، واقرأ تصحيحات الوقود بدقة</td></tr>'
'</tbody></table></div>'
'<p>توقف بأمان إذا كانت لمبة المحرك تومض مع رعشة قوية. لا تجرِ اختبار تعطيل كويل أو فصل رشاش والمحرك يعمل دون إجراء المصنع؛ ذلك قد يضر المحول الحفاز أو المكونات الكهربائية. انظر <a href="https://a3tal.com/what-to-do-when-check-engine-light-is-on/">متى تتوقف عند وميض Check Engine</a>.</p>'
'</section>'
)
BLOCK={"rich":RICH,"bank2":BANK2,"single":SINGLE}
def http(url,payload=None):
    headers={"Accept":"application/json","Cache-Control":"no-cache,no-store",
        "User-Agent":"A3tal-CrossCode-Misfire-Rich-Bank2/20261031",
        "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY}
    data=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
    if data is not None:headers["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=headers,
           method="POST" if data is not None else "GET"),timeout=100) as response:return json.load(response)
def private(id):return http(API+"/post/"+str(id))
def public(id):
    url=SITE+"/wp-json/wp/v2/posts/"+str(id)+"?"+urllib.parse.urlencode({
        "_fields":"id,title,slug,modified_gmt,status,link,featured_media,yoast_head_json",
        "verify":"20261031-crosscode"})
    return http(url)
def patch(original,p):
    if MARK in original:return None
    heads=list(re.finditer(r"<h2(?:\s[^>]*)?>",original,re.I))
    if len(original)<5800 or len(heads)<8:
        raise RuntimeError("Article structure changed from audit "+p["type"])
    i=heads[0].start()
    combined=original[:i]+BLOCK[p["type"]]+"\n"+original[i:]
    if combined.count('id="'+MARK+'-'+p["type"]+'"')!=1 or len(combined)-len(original)<1400:
        raise RuntimeError("Cross-code section injection did not pass size or unique marker")
    return combined
plan=[]
for p in PAGES:
    a=private(p["id"]);b=public(p["id"])
    if (a["id"],a["status"],a["slug"],a["featured_media"])!=(p["id"],"publish",p["slug"],p["cover"]):
        raise RuntimeError("Original slug/media/status changed "+str(p["id"]))
    if b["modified_gmt"]!=p["last"]:
        raise RuntimeError("Changed since audited; do not overwrite newer editor version "+str(p["id"]))
    oldseo=b["yoast_head_json"]
    if not oldseo.get("og_image") or oldseo.get("robots",{}).get("index")=="noindex" or not oldseo.get("canonical"):
        raise RuntimeError("Unsafe original SEO state "+str(p["id"]))
    new=patch(a["content"],p)
    if new is None:
        print("RICH_BANK2_MISFIRE_ALREADY_DONE",p["id"],flush=True)
        continue
    plan.append((p,a,b,new))
    print("RICH_BANK2_MISFIRE_PREFLIGHT_OK",p["id"],len(a["content"]),len(new),flush=True)
for p,a,b,new in plan:
    current=private(p["id"])
    if current["modified_gmt"]!=a["modified_gmt"]:
        raise RuntimeError("Concurrent WordPress update detected "+str(p["id"]))
    response=http(API+"/update-post",{"id":p["id"],"content":new,
                                     "expected_modified_gmt":current["modified_gmt"]})
    if response.get("error") or response.get("ok") is False:
        raise RuntimeError("Bridge rejected update "+str(p["id"])+str(response)[:220])
    confirmed=None
    for attempt in range(6):
        w=private(p["id"]);j=public(p["id"])
        if MARK+"-"+p["type"] in w["content"]:
            confirmed=(w,j);break
        time.sleep(2)
    if confirmed is None:raise RuntimeError("Updated content not visible "+str(p["id"]))
    w,j=confirmed
    after=j["yoast_head_json"];before=b["yoast_head_json"]
    if (w["slug"],w["status"],w["featured_media"])!=(p["slug"],"publish",p["cover"]):
        raise RuntimeError("Slug or cover changed "+str(p["id"]))
    if (after.get("canonical")!=before.get("canonical")
       or after.get("description")!=before.get("description")
       or after.get("title")!=before.get("title")
       or after.get("og_image",[{}])[0].get("url")!=before.get("og_image",[{}])[0].get("url")
       or after.get("robots",{}).get("index")=="noindex"):
        raise RuntimeError("Unexpected change to original Yoast/canonical/OG/image "+str(p["id"]))
    print("RICH_BANK2_MISFIRE_LIVE_VERIFIED",p["id"],w["link"],"featured_media",w["featured_media"],flush=True)
print("A3TAL_RICH_BANK2_SINGLE_MISFIRE_TRIO_COMPLETE",flush=True)
