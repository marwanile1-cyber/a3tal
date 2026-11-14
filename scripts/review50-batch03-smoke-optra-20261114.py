#!/usr/bin/env python3
"""A3tal third batch human repair: exhaust smoke diagnostic and Optra AC/electrics.
Protect original photo media, exact slugs, statuses, featured image and Yoast canonical.
Fact-check 2026 sources: RAC and DENSO technical diagnostics, Chevrolet Egypt specs.
"""
import importlib.util,re,time
s=importlib.util.spec_from_file_location("base","scripts/review-human-seo-geo-egypt-three-20261114.py")
base=importlib.util.module_from_spec(s);s.loader.exec_module(base)
TARGETS=[
  {
    "id": 80969,
    "slug": "car-exhaust-smoke-colors-causes",
    "mod": "2026-10-01T23:23:17",
    "cover": 80970,
    "kind": "smoke",
    "title": "ألوان دخان الشكمان: الأبيض والأسود والأزرق والتشخيص الصحيح",
    "seo": "ألوان دخان الشكمان: الأبيض والأسود والأزرق | أعطال",
    "desc": "ماذا يعني دخان الشكمان الأبيض أو الأزرق أو الأسود؟ الفرق بين بخار الماء ونقص التبريد واحتراق الزيت وغنى الخليط، ومتى توقف السيارة وتفحصها.",
    "kw": "ألوان دخان الشكمان",
    "html": "<p><strong>ألوان دخان الشكمان</strong> تساعد في ترتيب احتمالات العطل، لكنها ليست تشخيصًا نهائيًا. الأبيض الخفيف بعد تشغيل محرك بارد قد يكون بخار ماء طبيعيًا، بينما الأبيض الكثيف المستمر مع نقص سائل تبريد يحتاج فحصًا. الأزرق قد يشير لاحتراق زيت، والأسود غالبًا يرتبط بزيادة الوقود أو نقص الهواء، مع اختلاف المحرك البنزين عن الديزل.</p>\n<p>ينصح <a href=\"https://www.rac.co.uk/drive/advice/know-how/engine-smoking-why-its-happening-and-what-to-do/\" rel=\"noopener noreferrer\">دليل RAC البريطاني لألوان الدخان، المحدث في أكتوبر 2026</a> بتسجيل وقت ظهور الدخان ولونه ورائحته وعلاقته بالسخونة والحمل بدل الحكم من صورة أو لون منفصل. كما يشرح <a href=\"https://www.autoexpress.co.uk/car-news/102502/car-exhaust-smoke-what-do-the-different-kinds-and-colours-of-smoke-mean\" rel=\"noopener noreferrer\">Auto Express</a> الفرق بين التكثف ومشكلات الزيت والتبريد.</p>\n<h2>جدول ألوان دخان الشكمان وما يجب فحصه</h2>\n<div style=\"overflow-x:auto\"><table><thead><tr><th>اللون/العرض</th><th>أسباب محتملة</th><th>كيف تبدأ؟</th></tr></thead><tbody>\n<tr><td>بخار أبيض خفيف في الصباح ويختفي</td><td>تكاثف مياه في الشكمان</td><td>راقب اختفاءه بعد التسخين وعدم نقص التبريد</td></tr>\n<tr><td>أبيض كثيف ومستمر بعد التسخين</td><td>احتراق سائل تبريد محتمل أو وقود غير محترق في بعض الديزل</td><td>مستوى التبريد واختبار ضغط الدورة وBlock Test حسب الأعراض</td></tr>\n<tr><td>أزرق أو رمادي مزرق</td><td>زيت يدخل غرفة الاحتراق أو مسار العادم</td><td>راقب استهلاك الزيت وPCV والصبابات والشنابر والتيربو إن وجد</td></tr>\n<tr><td>أسود في محرك بنزين</td><td>خليط غني أو هواء غير كافٍ واحتراق غير كامل</td><td>Fuel Trim وMAF/MAP والرشاشات وضغط الوقود</td></tr>\n<tr><td>أسود في محرك ديزل</td><td>سخام ووقود/هواء وEGR/بوست وDPF بحسب الحالة</td><td>أكواد المنظومة وفحص البوست والعادم قبل تغيير أجزاء</td></tr>\n</tbody></table></div>\n<h2>الدخان الأبيض: بخار ماء أم جوان وش سلندر؟</h2>\n<p>التكاثف يكون شائعًا في الجو البارد أو بعد مشاوير قصيرة، وقد يتلاشى بعد سخونة العادم. أما الدخان الأبيض الكثيف المستمر مع انخفاض مستوى سائل التبريد أو سخونة غير معتادة فيحتاج فحصًا، لكن لا يكفي اللون وحده للموافقة على فك وش السلندر. اطلب ضغط دورة التبريد وقياس غازات الاحتراق في السائل وفحص تسريب الأسطوانات عند اللزوم. لا تفتح غطاء القربة أو الردياتير والمحرك ساخن.</p>\n<h2>الدخان الأزرق: هل يحتاج المحرك عمرة؟</h2>\n<p>ظهور دخان أزرق بعد تشغيل بارد أو بعد رفع القدم من البنزين أو أثناء التسارع يفيد في تحديد موضع الاشتباه، لكنه لا يكفي للحكم على الشنابر. قد تكون المشكلة من جلود الصبابات أو PCV أو تلف تيربو أو تآكل جدران الأسطوانات أو تسريب زيت إلى العادم. افحص مستوى الزيت واستهلاكه والتسريب الخارجي، ثم Compression/Leak-down عند الحاجة قبل اتخاذ قرار «عمرة». راجع <a href=\"https://a3tal.com/engine-compression-leakdown-test-guide/\">اختبار كبس وتسريب الأسطوانات</a>.</p>\n<h2>الدخان الأسود: ماذا يعني في البنزين والديزل؟</h2>\n<p>في محركات البنزين يشير عادة إلى احتراق غني، وقد يتأثر برشاش يسرّب أو حساس أو ضغط وقود أو مشكلة في الهواء الداخل. أما الديزل فيختلف بسبب تكون السخام ونظم الحقن والشحن وDPF. لا تنصح بقطع غيار أو «مشوار طريق سريع» لتجديد DPF قبل معرفة حالة الفلتر والأكواد ودرجة الحرارة؛ بعض أعطال الفلتر تجعل الاستمرار خطرًا أو تزيد التلف.</p>\n<h2>هل الدخان الرمادي له معنى محدد؟</h2>\n<p>الرمادي وصف غير دقيق بالعين المجردة وقد يتداخل مع الأزرق أو الأبيض حسب الضوء والوقود والحرارة. سجل الرائحة والتوقيت ومدى استهلاك الزيت أو نقص سائل التبريد والأكواد، لأن اللون وحده لا يمكن أن يثبت سببًا واحدًا.</p>\n<h2>متى تتوقف عن القيادة؟</h2>\n<p>أوقف المحرك في مكان آمن إذا كان الدخان كثيفًا على نحو جديد، أو صاحبه سخونة عالية أو تحذير ضغط زيت أو فقد قدرة واضح، ولا تكمل مشوارًا لاختبار «هل الدخان هيروح». إذا رأيت دخانًا من حجرة المحرك أو رائحة حريق، ابتعد عن السيارة واطلب مساعدة الطوارئ المحلية؛ هذا يختلف عن بخار ماء خفيف في العادم.</p>\n<h2>كيف تساعد الفني على تشخيص الدخان؟</h2>\n<ol><li>حدد هل الدخان من العادم أم من أسفل الكبوت.</li><li>سجّل اللون والمدة وهل يظهر عند التشغيل أو الدعس أو التهدئة.</li><li>راجع مستوى الزيت والتبريد والمحرك بارد دون فتح أجزاء ساخنة.</li><li>سجّل أكواد DTC وFreeze Frame قبل مسحها.</li><li>اطلب فحوصًا مناسبة للعَرَض بدل تغيير جوان أو تيربو من لون الدخان فقط.</li></ol>\n<p>لتحديد سبب السخونة أو التبريد راجع <a href=\"https://a3tal.com/nissan-sunny-engine-common-faults/\">طرق فحص دورة التبريد والمحرك</a>، ولأسباب لون العادم مع التيربو راجع <a href=\"https://a3tal.com/p0299-turbo-underboost-chinese-cars-fix-egypt-2026/\">فحص تسريب البوست والتيربو</a>.</p>\n<h2>أسئلة شائعة</h2>\n<h3>هل الدخان الأبيض صباحًا يعني تلف الجوان؟</h3><p>لا؛ قد يكون بخار ماء، خاصة إذا اختفى بعد التسخين ولم يظهر نقص تبريد. عند استمرار الدخان أو السخونة افحص دورة التبريد.</p>\n<h3>هل الدخان الأزرق يعني تغيير شنابر فورًا؟</h3><p>لا، أسباب الزيت تشمل PCV والصبابات والشنابر والتيربو. حدد السبب باختبارات قبل فك المحرك.</p>\n<h3>هل الدخان الأسود معناه بخاخات فقط؟</h3><p>لا؛ ابحث أيضًا في الهواء الداخل والحساسات والضغط والبوست ونظام العادم حسب نوع المحرك.</p>"
  },
  {
    "id": 80593,
    "slug": "chevrolet-optra-electrical-ac-problems",
    "mod": "2026-09-20T15:56:12",
    "cover": 80594,
    "kind": "optra",
    "title": "أعطال كهرباء وتكييف شيفروليه أوبترا: الفحص حسب الجيل",
    "seo": "أعطال كهرباء وتكييف أوبترا: الحساسات والكمبروسر | أعطال",
    "desc": "أعطال كهرباء وتكييف شيفروليه أوبترا: الفرق بين القديمة ونيو أوبترا CVT، فحص حساس الكرنك والبطارية والكمبروسر والمروحة قبل شراء قطع.",
    "kw": "أعطال كهرباء شيفروليه أوبترا",
    "html": "<p><strong>أعطال كهرباء وتكييف شيفروليه أوبترا</strong> لازم تُفحص حسب سنة السيارة وجيلها وكود محركها؛ «أوبترا» القديمة ليست نفس <strong>أوبترا 2026</strong> الجديدة التي تطرحها شيفروليه مصر بمحرك 1.5 لتر وناقل <strong>CVT</strong> حسب <a href=\"https://www.chevroletarabia.com/eg-ar/cars/optra/specs\" rel=\"noopener noreferrer\">مواصفات شيفروليه الرسمية</a>. ضعف التبريد أو تأخر التشغيل أو ظهور لمبة المحرك عَرَض، وليس دليلًا على تلف كمبروسر أو حساس بعينه.</p>\n<h2>خريطة أعراض كهرباء أوبترا قبل تغيير القطع</h2>\n<div style=\"overflow-x:auto\"><table><thead><tr><th>العرض</th><th>ابدأ بفحص</th><th>ما لا يمكن الجزم به</th></tr></thead><tbody>\n<tr><td>المارش لا يدور أو يدور ببطء</td><td>بطارية 12V، القواطيش، الأرضي، الريلاي، دائرة المارش</td><td>ليس «حساس كرنك» تلقائيًا</td></tr>\n<tr><td>المارش يدور والمحرك لا يبدأ التشغيل</td><td>أكواد ECM، إشارة CKP/CMP، ضغط الوقود، إشعال وموانع التشغيل</td><td>لا تغيير حساس قبل قياس الإشارة</td></tr>\n<tr><td>التكييف هواء ضعيف من الفتحات</td><td>فلتر المقصورة والمروحة وبوابات الهواء</td><td>ليس بالضرورة نقص فريون</td></tr>\n<tr><td>الهواء قوي لكنه دافئ</td><td>شحنة وسيط التبريد، المراوح، المكثف، أمر الكمبروسر والضغوط</td><td>ليس بالضرورة تلف كباس</td></tr>\n<tr><td>التكييف بارد أثناء الحركة وساخن في الوقوف</td><td>مروحة المكثف وتدفق الهواء وحرارة التشغيل</td><td>لا تقرر زيادة فريون من الأعراض فقط</td></tr>\n<tr><td>لمبة ABS أو EPS</td><td>أكواد الوحدة والجهد والحساسات والأسلاك</td><td>لا تنقل وصف نظام هيدروليك من أوبترا قديمة لكل الجديدة</td></tr>\n</tbody></table></div>\n<h2>حساس الكرنك والكامة: كيف تتأكد؟</h2>\n<p>توقف المحرك وهو ساخن أو فقده للإشارة قد يثير الاشتباه في CKP، لكنه قد يكون نتيجة عطل وقود أو كهرباء أو أرضي أو كنترول. استخدم بيانات RPM أثناء التدوير وقياس إشارة الحساس والتغذية والضفيرة ضمن ظروف العطل، ثم حدد رقم القطعة مطابقًا لـVIN. قطع الغيار المقلدة مخاطرة، لكن ليس صحيحًا أن كل قطعة غير معبأة في علبة GM تدمر الكمبيوتر؛ الجودة والتوافق والمصدر هي الأساس.</p>\n<h2>تكييف أوبترا لا يبرد: هل تغيير Control Valve كفاية؟</h2>\n<p><strong>لا يوجد إصلاح واحد يناسب كل الأجيال.</strong> بعض الكمبروسرات Variable Displacement قد تحتوي صمام تحكم قابلًا للفحص أو الاستبدال حسب التصميم، وأخرى بها قابض كهربائي أو نظام تحكم مختلف. ضعف ضغط الشحن قد يحدث من نقص الفريون بسبب تسريب أو تعطل مروحة المكثف أو حساس الضغط أو مشكلة الكمبروسر الداخلية. تبديل Control Valve قبل التأكد من الضغوط ودائرة الأمر وحالة الزيت والتلوث قد لا يصلح العطل.</p>\n<p>يحدد <a href=\"https://www.densoautoparts.com/reference-ac-compressor-troubleshooting/\" rel=\"noopener noreferrer\">دليل DENSO الفني لتشخيص كمبروسر السيارة، مارس 2026</a> تسلسلًا يبدأ بوصف الشكوى ثم المراوح والضغوط والمكونات ونشرات الخدمة والاختبارات، بدل استبدال الكمبروسر مباشرة. لا تفك خطوط التبريد أو تطلق الفريون في الجو؛ إجراء الاستعادة والشحن يحتاج معدات وفنيًا مؤهلًا.</p>\n<h2>هل كل أوبترا تستخدم نفس حساس MAP وTPS والبوابة؟</h2>\n<p>لا. قد تختلف مواقع الحساسات وعددها وتصميم البوابة بين الجيل والمحرك ونظام الحقن. اقرأ كود DTC من وحدة التحكم نفسها، ثم قارِن Live Data بمواصفات المصنع. مثلاً P0335 يتحدث عن دائرة موضع الكرنك، وP0105 عن أداء دائرة ضغط المنفولد في تطبيقات معينة، وP0300 عن Misfire؛ ليست قائمة قطع للشراء.</p>\n<h2>أوبترا القديمة ونيو أوبترا: لماذا الفرق مهم؟</h2>\n<p>تجهيزات التوجيه والفتيس والتحكم في التكييف تختلف، ولا يجوز استخدام كهربائي توصيلات الجيل القديم في سيارة حديثة من غير مخطط. قبل شراء كمبروسر أو ECU أو تغيير زيت ناقل الحركة راجع سنة السيارة وVIN وكود القطعة. لتشخيص الفتيس راجع <a href=\"https://a3tal.com/chevrolet-optra-transmission-problems-guide/\">الفرق بين فتيس أوبترا القديمة والجديدة</a>، ولأكواد التحكم راجع <a href=\"https://a3tal.com/chevrolet-optra-dtc-codes-encyclopedia/\">دليل أكواد أعطال أوبترا</a>.</p>\n<h2>متى لا تستمر في القيادة؟</h2>\n<p>توقف بأمان إذا ظهرت رائحة احتراق كهربائي أو دخان أو ارتفاع حرارة أو تحذير شحن مع ضعف الأنوار، ولا تستمر في رحلة طويلة لفحص «العطل على الطريق». نقص تبريد التكييف وحده لا يعني تغيير مجموعة كاملة، لكن رائحة غازات العادم داخل المقصورة أو دخان الأسلاك تستدعي إيقاف المركبة والفحص.</p>\n<h2>ما بيانات السيارة التي تطلبها الورشة؟</h2>\n<ol><li>رقم VIN وكود المحرك وسنة الموديل وفئة السيارة.</li><li>وصف توقيت العطل: بارد أم ساخن، أثناء الوقوف أم التسارع؟</li><li>الأكواد المسجلة وFreeze Frame والجهد والقراءات الحية.</li><li>تاريخ تغيير البطارية أو التكييف أو تنظيف البوابة.</li><li>مقايسة مكتوبة برقم القطعة ونتيجة الاختبار قبل أي استبدال.</li></ol>\n<h2>الأسئلة الشائعة</h2>\n<h3>هل تغيير صمام الكمبروسر يصلح التكييف دائمًا؟</h3><p>لا؛ قد يكون العطل من التسريب أو التحكم أو المراوح أو ضغط الدورة أو الكمبروسر نفسه. يجب معرفة نوع الكمبروسر وقياس الدائرة.</p>\n<h3>هل P0335 يعني تغيير حساس الكرنك؟</h3><p>لا. اختبر إشارة الحساس والتغذية والضفيرة والتزامن وأكواد الأعطال المصاحبة قبل شراء جزء.</p>\n<h3>هل كمبروسر أوبترا القديمة يركب في الجديدة؟</h3><p>لا تفترض التوافق؛ الكود والفيشة والتثبيت ونوع وسيط التبريد وتصميم الدائرة قد تختلف، ولا بد من مطابقة رقم القطعة.</p>"
  }
]
MARK="a3tal-third50-tech2-20261114"
def newcontent(t,original):
 old_images=re.findall(r"<img\b[^>]*>",original,re.I)
 # If original has media, preserve exact original figure or image in place
 fig=re.findall(r"<figure\b[^>]*>[\s\S]*?</figure>",original,re.I)
 if len(old_images)>1 or len(fig)>1:raise RuntimeError("Unreviewed inline media layout")
 body=t["html"]
 if old_images:
  if fig and len(re.findall(r"<img\b",fig[0],re.I))==1:pic=fig[0]
  elif not fig:pic='<figure class="a3tal-kept-original-inline">'+old_images[0]+'</figure>'
  else:raise RuntimeError("Photo wrapper not understood")
  anchor="<h2>جدول ألوان دخان الشكمان وما يجب فحصه</h2>" if t["kind"]=="smoke" else "<h2>خريطة أعراض كهرباء أوبترا قبل تغيير القطع</h2>"
  if body.count(anchor)!=1:raise RuntimeError("Original image placement changed")
  body=body.replace(anchor,pic+"\n"+anchor,1)
 if len(re.findall(r"<img\b",body,re.I))!=len(old_images):raise RuntimeError("Original photo count would change")
 if body.count("<h2>")<5 or body.count('<a href="')<3 or len(body)<3200:raise RuntimeError("Human rewrite quality check")
 return '<section id="'+MARK+'-'+t["kind"]+'" dir="rtl">'+body+'</section>'

def main():
 todo=[]
 for t in TARGETS:
  old=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
  if MARK+"-"+t["kind"] in old.get("content",""):
   print("THIRD50_ALREADY_REVIEWED",t["id"],flush=True);continue
  if (int(old.get("id",0)),old.get("slug"),old.get("status"),old.get("type"),int(old.get("featured_media") or 0))!=(
    t["id"],t["slug"],"publish","post",t["cover"]):
    raise RuntimeError("Post identity/cover status mismatch")
  if not old["modified_gmt"].startswith(t["mod"]):raise RuntimeError("Post modified since audit")
  yo=pub.get("yoast_head_json") or {}
  if yo.get("canonical")!=base.SITE+"/"+t["slug"]+"/" or not yo.get("og_image") or (yo.get("robots") or {}).get("index")=="noindex":
    raise RuntimeError("SEO/OG preflight mismatch")
  content=newcontent(t,old["content"])
  todo.append((t,old,pub,content))
  print("THIRD50_REPAIR2_PREFLIGHT",t["id"],len(old["content"]),len(content),flush=True)
 print("THIRD50_REPAIR2_ALL_PREFLIGHTS_PASS",len(todo),flush=True)
 for t,old,pub,content in todo:
  current=base.bridge_post(t["id"])
  if current["modified_gmt"]!=old["modified_gmt"] or current["content"]!=old["content"]:
   raise RuntimeError("Concurrent modification stop")
  meta={"_yoast_wpseo_title":t["seo"],"_yoast_wpseo_metadesc":t["desc"],"_yoast_wpseo_focuskw":t["kw"],
    "_yoast_wpseo_opengraph-title":t["seo"],"_yoast_wpseo_opengraph-description":t["desc"],
    "_yoast_wpseo_twitter-title":t["seo"],"_yoast_wpseo_twitter-description":t["desc"]}
  try:base.req("/update-post",{"id":t["id"],"expected_modified_gmt":current["modified_gmt"],"title":t["title"],"content":content,"meta":meta})
  except Exception as err:
   if MARK+"-"+t["kind"] not in base.bridge_post(t["id"])["content"]:
    raise RuntimeError("No confirmed update; do not retry") from err
  new=base.bridge_post(t["id"]);np=base.public_post(t["id"]);yo=np.get("yoast_head_json") or {}
  if (new.get("slug"),new.get("status"),new.get("title"),int(new.get("featured_media") or 0))!=(
    t["slug"],"publish",t["title"],t["cover"]):
    raise RuntimeError("Post title/slug/status/cover drift")
  if content.count('id="'+MARK+"-"+t["kind"]+'"')!=1 or new["content"].count('id="'+MARK+"-"+t["kind"]+'"')!=1:
    raise RuntimeError("Human rewritten article not live")
  if yo.get("canonical")!=pub["yoast_head_json"]["canonical"] or (
      yo.get("robots") or {}).get("index")=="noindex" or yo.get("description")!=t["desc"] or (
      yo.get("og_image") or [{}])[0].get("url")!=(pub["yoast_head_json"].get("og_image") or [{}])[0].get("url"):
    raise RuntimeError("Yoast canonical/index/OG failed")
  print("THIRD50_REPAIR2_LIVE_VERIFIED",t["id"],new["link"],flush=True)
  time.sleep(1)
 print("A3TAL_THIRD50_REPAIR2_DONE",flush=True)
if __name__=="__main__":main()
