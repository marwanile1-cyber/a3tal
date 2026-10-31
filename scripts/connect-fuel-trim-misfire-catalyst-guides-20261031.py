#!/usr/bin/env python3
"""Add concise, source-grounded cross-code diagnostic decisions to 3 existing a3tal posts.
Preserve post IDs, URLs, titles, original bodies, images, Yoast canonicals and indexability.
Runs through GitHub Actions + A3tal Direct Bridge only, not WPWriter.
"""
import os,json,re,time,urllib.request,urllib.parse
SITE="https://a3tal.com"
BRIDGE=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
STAMP="a3tal-fuel-misfire-catalyst-navigation-20261031"
PAGES=[
 {"id":82264,"kind":"p0171","last":"2026-09-20T13:33:05",
  "slug":"p0171-system-too-lean-bank-1-diagnosis","cover":81374},
 {"id":81382,"kind":"fueltrim","last":"2026-09-06T11:59:31",
  "slug":"stft-ltft-fuel-trim-diagnosis","cover":81383},
 {"id":81336,"kind":"p0420","last":"2026-10-03T13:13:43",
  "slug":"p0420-catalyst-efficiency-bank-1","cover":81337},
]
P0171=(
'<section id="'+STAMP+'-p0171" dir="rtl" class="a3tal-diagnostic-crosscodes">'
'<h2>إذا ظهر P0171 مع كود آخر، من أين يبدأ التشخيص؟</h2>'
'<p>احفظ الأكواد الحالية والمعلقة وبيانات Freeze Frame قبل المسح. معنى P0171 هو أن تصحيح الوقود في Bank 1 وصل إلى حد يعتبره الكمبيوتر خليطًا فقيرًا؛ لكنه لا يحدد قطعة واحدة. ترتيب الفحص يتغير إذا ظهر معه كود آخر:</p>'
'<div class="g-table-wrap"><table><thead><tr><th>الكود أو النمط المصاحب</th><th>أول فحص منطقي</th></tr></thead><tbody>'
'<tr><td>P0171 وتصحيح وقود موجب أكثر على السلانسيه</td><td>تسريب سحب الهواء وخراطيم PCV وجوانات السحب، ثم مقارنة القراءات بزيادة RPM</td></tr>'
'<tr><td><a href="https://a3tal.com/فك-لغز-كود-العطل-p0300-في-شيفروليه-دليل-التش/">P0300 مع P0171</a></td><td>تأكد من الميسفاير وشدته، ثم افحص أسباب الخليط الفقير والإشعال والوقود، بدل تغيير الكويلات عشوائيًا</td></tr>'
'<tr><td><a href="https://a3tal.com/p0420-catalyst-efficiency-bank-1/">P0420 مع P0171</a></td><td>شخّص الخليط الفقير وتسريب العادم وأداء المحرك قبل الحكم على علبة البيئة</td></tr>'
'<tr><td><a href="https://a3tal.com/p0172-system-too-rich-bank1-diagnosis/">P0172</a> يظهر بدلًا من P0171 في ظروف أخرى</td><td>قارن Freeze Frame وحالة Closed Loop والقراءات الحية واحتمال انحراف حساس أو اضطراب تغذية الوقود؛ لا تعتبرهما سببًا واحدًا ثابتًا</td></tr>'
'</tbody></table></div>'
'<p>لشرح طريقة قراءة التصحيحات بدل الحكم من رقم منفرد، راجع <a href="https://a3tal.com/stft-ltft-fuel-trim-diagnosis/">دليل STFT وLTFT</a>. إذا ظهرت لمبة Check Engine وامضة مع رعشة قوية، توقف بأمان بدل مواصلة التجربة على الطريق.</p>'
'</section>'
)
FUELTRIM=(
'<section id="'+STAMP+'-fueltrim" dir="rtl" class="a3tal-diagnostic-crosscodes">'
'<h2>من قراءة STFT وLTFT إلى دليل كود العطل الصحيح</h2>'
'<p>لا تحدد القراءة الواحدة القطعة التالفة، وبعض السيارات لا تسمح بتفسير Fuel Trim بدقة خارج وضع Closed Loop. بعد تسجيل Freeze Frame ومقارنة السلانسيه بحمل مناسب، استخدم النمط مع الكود لتحديد المقال الذي تحتاجه:</p>'
'<div class="g-table-wrap"><table><thead><tr><th>القراءة والكود</th><th>اتجاه التشخيص التالي</th></tr></thead><tbody>'
'<tr><td>تصحيحات موجبة مستمرة + <a href="https://a3tal.com/p0171-system-too-lean-bank-1-diagnosis/">P0171</a></td><td>تسريب فاكيوم، PCV، الهواء المقاس، ضغط الوقود حسب نمط Idle مقابل الحمل</td></tr>'
'<tr><td>تصحيحات سالبة مستمرة + <a href="https://a3tal.com/p0172-system-too-rich-bank1-diagnosis/">P0172</a></td><td>رشاش يسرب، ضغط وقود مرتفع، MAF/ECT وEVAP حسب بيانات السيارة</td></tr>'
'<tr><td>رعشة قوية + <a href="https://a3tal.com/فك-لغز-كود-العطل-p0300-في-شيفروليه-دليل-التش/">P0300</a></td><td>ابدأ بسلامة القيادة وعدّادات Misfire إن توفرت، ثم الإشعال والوقود والضغط الميكانيكي</td></tr>'
'<tr><td><a href="https://a3tal.com/p0420-catalyst-efficiency-bank-1/">P0420</a> مع أكواد خليط أو ميسفاير</td><td>أصلح العطل الأساسي واختبر العادم قبل تغيير Catalyst</td></tr>'
'</tbody></table></div>'
'<p><strong>مهم:</strong> يختلف تفسير التصحيحات حسب استراتيجية التحكم وحالة الوقود وحمل المحرك. القيم الإرشادية لا تُعد حدود فشل عامة لجميع الماركات، ولا يغني الجدول عن مواصفات المصنع.</p>'
'</section>'
)
P0420=(
'<section id="'+STAMP+'-p0420" dir="rtl" class="a3tal-diagnostic-crosscodes">'
'<h2>ترتيب تشخيص P0420 إذا ظهر مع P0171 أو P0172 أو P0300</h2>'
'<p>كود P0420 يصف كفاءة المحول الحفاز في Bank 1، وليس انسداد العادم بحد ذاته. ظهور كود احتراق أو خليط مع P0420 يغيّر ترتيب الإصلاح؛ لأن المشكلة السابقة قد تؤثر في كفاءة المحول وتُسبب تكرار تلفه إذا استُبدل دون علاج السبب.</p>'
'<div class="g-table-wrap"><table><thead><tr><th>الكود المصاحب</th><th>الفحص الذي يسبق شراء علبة البيئة</th></tr></thead><tbody>'
'<tr><td><a href="https://a3tal.com/فك-لغز-كود-العطل-p0300-في-شيفروليه-دليل-التش/">P0300</a> أو Misfire</td><td>تشخيص الاشتعال والوقود والضغط الميكانيكي؛ الوميض مع رعشة قوية يستدعي التوقف الآمن</td></tr>'
'<tr><td><a href="https://a3tal.com/p0171-system-too-lean-bank-1-diagnosis/">P0171</a> خليط فقير</td><td>تسريب هواء أو عادم، ضغط الوقود، MAF ومصححات Fuel Trim</td></tr>'
'<tr><td><a href="https://a3tal.com/p0172-system-too-rich-bank1-diagnosis/">P0172</a> خليط غني</td><td>الرشاشات وضغط البنزين والهواء المقاس والـEVAP، مع فحص أي وقود غير محترق</td></tr>'
'<tr><td>P0420 وحده بعد استقرار عمل المحرك</td><td>افحص تسريب العادم وإشارات حساسات الأكسجين واختبار Catalyst Monitor قبل الحكم على المحول</td></tr>'
'</tbody></table></div>'
'<p>راجع <a href="https://a3tal.com/stft-ltft-fuel-trim-diagnosis/">قراءة STFT وLTFT</a>، والفرق مع <a href="https://a3tal.com/p0430-catalyst-efficiency-bank-2/">P0430 في Bank 2</a>. مرجع فني: <a href="https://guides.innova.com/codes/p0420" rel="noopener noreferrer">Innova: تشخيص P0420</a>. لا تحكم على المحول أو الحساس من مسح الكود وعودة اللمبة وحدهما.</p>'
'</section>'
)
BLOCKS={"p0171":P0171,"fueltrim":FUELTRIM,"p0420":P0420}
def fetch(url,payload=None):
    headers={"Accept":"application/json","Cache-Control":"no-cache,no-store",
             "User-Agent":"A3tal-Fuel-Misfire-Catalyst-Guides/20261031",
             "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY}
    raw=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,data=raw,headers=headers,
            method="POST" if raw is not None else "GET"),timeout=120) as r:return json.load(r)
def bridge(id): return fetch(BRIDGE+"/post/"+str(id))
def public(id):
    return fetch(SITE+"/wp-json/wp/v2/posts/"+str(id)+"?"+
       urllib.parse.urlencode({"_fields":"id,title,modified_gmt,status,slug,featured_media,link,yoast_head_json", "_q":"20261031-2"}))
def edit_body(h,kind):
    if STAMP in h:return None
    heads=list(re.finditer(r"<h2(?:\s[^>]*)?>",h,re.I))
    if len(heads)<8 or len(h)<5500:raise RuntimeError("Existing longform layout not as expected "+kind)
    idx=heads[0].start()
    updated=h[:idx]+BLOCKS[kind]+"\n"+h[idx:]
    if updated.count('id="'+STAMP+"-"+kind+'"')!=1:raise RuntimeError("Duplicate snippet marker "+kind)
    if len(updated)-len(h)<1300 or updated.count("<h2")!=h.count("<h2")+1:raise RuntimeError("Bad patch size or headings "+kind)
    return updated
plans=[]
for p in PAGES:
    raw=bridge(p["id"]); pub=public(p["id"])
    if (raw["id"],raw["status"],raw["slug"],raw["featured_media"])!=(p["id"],"publish",p["slug"],p["cover"]):
        raise RuntimeError("WordPress identity changed "+str(p["id"]))
    if pub["modified_gmt"]!=p["last"]:raise RuntimeError("Editor changed article since audited "+str(p["id"]))
    seo=pub.get("yoast_head_json") or {}
    if seo.get("robots",{}).get("index")=="noindex" or not seo.get("canonical") or not seo.get("og_image"):
        raise RuntimeError("Original SEO state unsafe "+str(p["id"]))
    new=edit_body(raw["content"],p["kind"])
    if new is None:print("CROSSCODE_ALREADY_PUBLISHED",p["id"],flush=True);continue
    plans.append((p,raw,pub,new))
    print("CROSSCODE_PREFLIGHT_OK",p["id"],"existing",len(raw["content"]),"new",len(new),flush=True)
for p,original,before,new in plans:
    livebefore=bridge(p["id"])
    if livebefore["modified_gmt"]!=original["modified_gmt"]:
        raise RuntimeError("Concurrent WordPress editor conflict "+str(p["id"]))
    response=fetch(BRIDGE+"/update-post",{"id":p["id"],
      "expected_modified_gmt":livebefore["modified_gmt"],"content":new})
    if response.get("error") or response.get("ok") is False:
        raise RuntimeError("Bridge rejected post update "+str(p["id"])+str(response)[:250])
    verified=None
    for i in range(5):
        a=bridge(p["id"]);b=public(p["id"])
        if STAMP+"-"+p["kind"] in a["content"]:verified=(a,b);break
        time.sleep(3)
    if not verified:raise RuntimeError("Updated guide not visible "+str(p["id"]))
    a,b=verified
    oldseo=before["yoast_head_json"];newseo=b["yoast_head_json"]
    if ((a["slug"],a["status"],a["featured_media"])!=(p["slug"],"publish",p["cover"])
        or newseo.get("canonical")!=oldseo.get("canonical")
        or newseo.get("og_image",[{}])[0].get("url")!=oldseo.get("og_image",[{}])[0].get("url")
        or newseo.get("robots",{}).get("index")=="noindex"
        or newseo.get("title")!=oldseo.get("title")
        or newseo.get("description")!=oldseo.get("description")):
        raise RuntimeError("SEO integrity changed after posting "+str(p["id"]))
    print("CROSSCODE_LIVE_VERIFIED",p["id"],a["link"],"image",a["featured_media"],flush=True)
print("A3TAL_FUEL_MISFIRE_CATALYST_CROSSCODE_DONE",flush=True)
