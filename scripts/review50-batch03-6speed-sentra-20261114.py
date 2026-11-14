#!/usr/bin/env python3
"""A3tal third human50 batch: repair GM 6AT fluid generalization and Sentra invented price/service claims.
Preserve the original inline Sentra photo verbatim and every featured image; do not modify URL/categories.
Sources: GM/ATSG, ZF Aftermarket, Nissan Egypt dealer/official customer service.
"""
import importlib.util,re,time
spec=importlib.util.spec_from_file_location("b","scripts/review-human-seo-geo-egypt-three-20261114.py")
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
ROWS=[
  {
    "id": 81155,
    "slug": "6-speed-automatic-transmission-cars-dexron-vi-oil",
    "mod": "2026-07-04T09:32:56",
    "cover": 81156,
    "title": "الفتيس الأوتوماتيك 6 سرعات: هل كل الأنواع تستخدم Dexron VI؟",
    "seo": "زيت الفتيس 6 غيار: Dexron VI ومواصفات كل ناقل | أعطال",
    "desc": "هل كل فتيس أوتوماتيك 6 غيارات يحتاج Dexron VI؟ الفرق بين نواقل GM وZF وAisin، ومواعيد تغيير الزيت وتشخيص النتشة والتسريب قبل الصيانة.",
    "kw": "زيت فتيس 6 غيار Dexron VI",
    "kind": "six",
    "html": "<p><strong>هل كل فتيس أوتوماتيك 6 غيارات يستخدم زيت Dexron VI؟</strong> لا. عدد السرعات لا يحدد مواصفة الزيت: بعض نواقل جنرال موتورز من عائلة 6T30/6T40 تحتاج <strong>DEXRON-VI</strong>، لكن نواقل أخرى بست سرعات من شركات ZF أو Aisin أو هيونداي وكيا قد تحتاج سوائل مختلفة. القرار الصحيح يبدأ بكود الفتيس ورقم الشاسيه VIN ومواصفة المصنع، وليس باسم السيارة أو عدد نقلاتها فقط.</p>\n<p>مثلًا، يوضح <a href=\"https://atsg.gtautopro.com/bulletins/16/16-10.pdf\" rel=\"noopener noreferrer\">مرجع ATSG الفني لإجراءات 6T30/40/45/50 من GM</a> استخدام Dexron VI وضبط مستوى السائل بدرجة الحرارة وإجراء محدد، بينما تشير <a href=\"https://aftermarket.zf.com/en/aftermarket-portal/faq/faq-oils/\" rel=\"noopener noreferrer\">ZF Aftermarket</a> إلى الالتزام بالسوائل والإجراءات المعتمدة لنواقلها. حتى داخل GM لا تعني ست أو ثماني سرعات المواصفة نفسها.</p>\n<h2>كيف تحدد نوع الفتيس الست سرعات الموجود في عربيتك؟</h2>\n<p>اطلب رقم VIN، وسنة الموديل والسوق ونوع المحرك، ثم ابحث عن كود الناقل في دليل الخدمة أو على بيانات القطعة. لا تعتمد على عبارة «فتيس أوبل 6 سرعات» أو «فتيس أمريكي 6 غيار»؛ نفس العلامة تستخدم عائلات ناقل مختلفة حسب السنوات. وجود Torque Converter لا يعني أن كل تصميم يستخدم سائلًا واحدًا.</p>\n<h2>أمثلة مهمة لاختيار زيت فتيس 6 غيار</h2>\n<div style=\"overflow-x:auto\"><table><thead><tr><th>الناقل أو العائلة</th><th>ما الذي يجب التأكد منه؟</th><th>تحذير</th></tr></thead><tbody>\n<tr><td>GM 6T30/40/45/50 في تطبيقات معنية</td><td>DEXRON-VI وفق مرجع الخدمة لهذا الناقل</td><td>مستوى السائل يحتاج إجراءً ودرجة حرارة؛ لا تعتمد على عدد العلب وحده</td></tr>\n<tr><td>ZF 6HP وتطبيقات ZF أخرى</td><td>السائل المسموح به في قائمة ZF الخاصة بالكود</td><td>لا تضع Dexron VI افتراضًا لمجرد وجود ست سرعات</td></tr>\n<tr><td>Aisin / Toyota 6AT</td><td>مواصفة ATF ورقم الناقل حسب VIN وكتالوج السيارة</td><td>بعض النواقل تستخدم Toyota WS أو مواصفات أخرى، ولا يعمّم ذلك على كل Aisin</td></tr>\n<tr><td>Hyundai / Kia 6AT</td><td>كود الناقل ومواصفة المصنع المحددة</td><td>لا تعتبر كل ATF-SP أو Dexron متبادلًا</td></tr>\n<tr><td>أي 6DCT أو ناقل مختلف</td><td>نوع القوابض ونظام التزييت والناقل الفعلي</td><td>الـDCT ليس Torque Converter تقليديًا؛ قد تتطلب سوائل وخدمة مختلفة</td></tr>\n</tbody></table></div>\n<p>ذكر سيارة في جدول سوقي أو إعلان لا يثبت نوع الفتيس ولا مواصفته، حتى إن كانت قوة المحرك وسنة الإنتاج متشابهتين.</p>\n<h2>هل Dexron VI متوافق مع كل Dexron القديم؟</h2>\n<p>مواصفة DEXRON-VI صُممت لتطبيقات محددة من GM، لكن عبارة «متوافق رجعيًا» لا تعطي إذنًا باستعماله في ناقل يطلب CVT Fluid أو ATF آخر أو زيت DCT. حتى عند وجود توصيات انتقال بين مواصفات من الشركة، يجب مراجعة دليل الخدمة أو نشرة GM لناقل السيارة المحدد. لون الزيت الأحمر لا يعني أنه DEXRON-VI.</p>\n<h2>كل كام يتغير زيت الفتيس 6 غيار؟</h2>\n<p><strong>لا يوجد جدول «كل 40–50 ألف كم» يناسب جميع نواقل 6AT.</strong> بعض الشركات لديها فترات خدمة حسب المسافة أو ظروف القيادة الشاقة، وأخرى تستخدم برامج صيانة أو فحوصًا مختلفة. اتبع كتيب المصنع وكود الناقل، ولا تعتبر تجاوز 80 ألف كيلومتر دليلًا على أن تغيير الزيت سيدمر الفتيس؛ قيّم الحالة قبل أي خدمة.</p>\n<h2>الغيار الجزئي أم الغسيل الكامل؟</h2>\n<p>تغيير الزيت الجزئي Drain & Fill يبدل جزءًا من السائل، أما الاستبدال الأوسع أو الغسيل فيحتاج معدات وإجراءً يناسب الناقل. لا تستخدم إضافات أو منظفات غير معتمدة. قبل تغيير الزيت افحص التسريب ودرجة الحرارة والأكواد والتاريخ، لأن مشكلة نتشة قد تأتي من قواعد أو حساسات أو Valve Body أو تآكل داخلي وليس من الزيت وحده. المزيد في <a href=\"https://a3tal.com/automatic-transmission-fluid-change-guide-risks/\">دليل تغيير زيت الفتيس ومخاطر الغسيل</a>.</p>\n<h2>علامات الفحص قبل تغيير أي قطعة</h2>\n<div style=\"overflow-x:auto\"><table><thead><tr><th>العرض</th><th>ابدأ بفحص</th></tr></thead><tbody>\n<tr><td>تأخير اختيار D أو R</td><td>مستوى الزيت بالطريقة الصحيحة والتسريب والقواعد وأكواد TCM</td></tr>\n<tr><td>نتشة أثناء النقل</td><td>ظروف ظهورها وحرارة الناقل وجهد التغذية وضغط التحكم وسلوك المحرك</td></tr>\n<tr><td>ارتفاع RPM من دون زيادة سرعة</td><td>انزلاق محتمل بالناقل أو مشكلة بالمحرك حسب الفحص؛ لا تحكم من العرض وحده</td></tr>\n<tr><td>سخونة متكررة أو تحذير فتيس</td><td>التبريد ومستوى السائل والكود؛ توقف في مكان آمن عند فقد الحركة</td></tr>\n</tbody></table></div>\n<h2>سعر زيت فتيس 6 غيار في مصر</h2>\n<p>لا يوجد «سعر واحد لزيت فتيس الست غيارات» لأن السوائل والأحجام ومصادر البيع مختلفة. لإعداد مقايسة اطلب الكود ورقم الزيت وسعة العبوة وكمية الصرف والفلتر والجوان والمصنعية والضريبة مكتوبة؛ أي ثمن غير مربوط بمنتج وتاريخ لا يُنشر هنا كسعر رسمي. اقرأ <a href=\"https://a3tal.com/transmission-fluid-change-prices-types-egypt-2026/\">العوامل المؤثرة في تكلفة تغيير زيت الفتيس</a>، ولتطبيق محدد راجع <a href=\"https://a3tal.com/chevrolet-optra-transmission-fluid-price-egypt/\">أنواع زيت فتيس أوبترا حسب الجيل</a> بدل تعميم الزيت.</p>\n<h2>الأسئلة الشائعة عن الفتيس 6 غيار</h2>\n<h3>هل كل أوتوماتيك 6 غيار DEXRON-VI؟</h3><p>لا، المعيار يخص تطبيقات معينة حسب المصنع وكود الناقل. عدد السرعات وحده لا يحدد السائل.</p>\n<h3>هل زيت CVT ينفع لفتيس 6AT؟</h3><p>لا تستخدم سوائل CVT في ناقل تقليدي إلا لو وردت موافقة صريحة، وهو أمر لا يُستنتج من عدد السرعات أو شكل الزيت.</p>\n<h3>هل الغسيل الكامل يعالج أي نتشة؟</h3><p>لا. قد تكون النتشة من دائرة التحكم أو القواعد أو مشكلة ميكانيكية. التشخيص قبل قرار الخدمة أكثر أمانًا.</p>"
  },
  {
    "id": 81062,
    "slug": "nissan-sentra-maintenance-schedule-service-centers",
    "mod": "2026-10-01T23:23:16",
    "cover": 81063,
    "title": "جدول صيانة نيسان سنترا في مصر: CVT والتكاليف ومراكز الخدمة",
    "seo": "جدول صيانة نيسان سنترا: CVT ومراكز الخدمة | أعطال",
    "desc": "دليل صيانة نيسان سنترا في مصر: الفحص كل 10 آلاف كم أو 6 أشهر حسب تعليمات الخدمة، زيت CVT حسب VIN، مراكز نيسان المعتمدة وتكاليف بدون أرقام تخمينية.",
    "kw": "جدول صيانة نيسان سنترا",
    "kind": "sentra",
    "html": "<p><strong>جدول صيانة نيسان سنترا في مصر</strong> لا يتحدد من قائمة أسعار عامة تتكرر على كل الموديلات. البداية هي تحديد سنة السيارة ورقم الشاسيه VIN والمحرك وكود ناقل الحركة، ثم مطابقة البنود مع كتيب المالك وجدول الوكيل المصري. توضح شبكة نيسان المعتمدة في مصر أن المراجعة الدورية العامة تتم <strong>كل 10,000 كم أو 6 أشهر، أيهما أقرب</strong>، لكن هذا لا يعني أن تغيير زيت الفتيس أو سائل التبريد أو البوجيهات مطلوب في كل زيارة بنفس الفاصل.</p>\n<p>المرجع: <a href=\"https://en.nissan-eltarek.com/owners/service-portfolio\" rel=\"noopener noreferrer\">توجيهات الصيانة لدى موزع نيسان الرسمي الطارق</a>، و<a href=\"https://ar.nissan.com.eg/owners/maintenance-and-repair.html\" rel=\"noopener noreferrer\">نيسان مصر عن الصيانة والضمان</a>. مواعيد استبدال كل بند تُقرأ من خطة السيارة نفسها، خاصة في السيارات الأقدم أو الوارد الخاص.</p>\n<h2>جدول فحص نيسان سنترا دون مواعيد استبدال مختلقة</h2>\n<div style=\"overflow-x:auto\"><table><thead><tr><th>البند</th><th>ما يراجع في الصيانة</th><th>متى يتغير؟</th></tr></thead><tbody>\n<tr><td>زيت المحرك وفلتره</td><td>المستوى واللزوجة والموافقة والتسريب</td><td>حسب كتيب VIN والفترة الزمنية أو المسافة</td></tr>\n<tr><td>فلتر الهواء والتكييف</td><td>حالة العنصر وتدفق الهواء والغبار</td><td>حسب الجدول أو حالته وظروف الاستخدام</td></tr>\n<tr><td>الفرامل</td><td>سمك التيل والطنابير والخراطيم والسائل</td><td>بناءً على القياس والفترة المقررة</td></tr>\n<tr><td>الفتيس الأوتوماتيك/CVT</td><td>تسريب وحرارة وأكواد وتاريخ الخدمة</td><td>وفق كود الناقل ومواصفة السائل وجدول الصيانة</td></tr>\n<tr><td>التبريد والسيور</td><td>مستوى السائل وحالة الخراطيم والأحزمة</td><td>حسب النوع والفترات المعتمدة للمحرك</td></tr>\n<tr><td>العفشة والإطارات</td><td>الخلوص والتآكل والضغط والزوايا عند الحاجة</td><td>قطع العفشة تُستبدل عند التلف المؤكد، لا كل زيارة</td></tr>\n</tbody></table></div>\n<p>خطة الصيانة الدورية تعني الفحص وتسجيل النتائج وتغيير البنود المستحقة؛ لا تحول كل سطر «فحص» إلى «شراء قطعة جديدة». بعض السيارات تُخدم في ظروف استخدام قاسية مثل الغبار والرحلات القصيرة، وتحتاج تطبيق الجدول المخصص لهذه الظروف في دليل السيارة.</p>\n<h2>زيت فتيس نيسان سنترا CVT: هل دائمًا NS-3؟</h2>\n<p>معظم نسخ سنترا المحلية الشائعة مزودة بناقل CVT، لكن لا ننقل المواصفة من سيارة أو سنة إلى أخرى. حدد نوع الناقل من VIN ودليل المالك؛ في تطبيقات معينة قد يكون Nissan CVT Fluid NS-3 صحيحًا، لكن استخدام زيت أوتوماتيك 4AT مثل Matic S أو DEXRON-VI افتراضًا في CVT قد يسبب ضررًا. لا تعتمد على لون الزيت أو تسمية «نيسان أوتوماتيك». لو هناك نتشة أو ونة أو تأخير، افحص الأكواد والحرارة والمستوى والإجراء الصحيح قبل تغيير مخ الفتيس.</p>\n<p>لمزيد من الفروق اقرأ <a href=\"https://a3tal.com/automatic-transmission-fluid-change-guide-risks/\">متى يكون تغيير زيت الفتيس مناسبًا؟</a> و<a href=\"https://a3tal.com/nissan-sunny-transmission-fluid-matic-s-price-specs/\">لماذا زيت صني 4AT ليس زيت CVT؟</a>. لا يُجزم أن كل فتيس سنترا يحتاج تغييرًا عند 60 ألف أو 80 ألف أو 100 ألف من دون جدول كود الناقل.</p>\n<h2>أسعار صيانة نيسان سنترا في مصر: ما المؤكد؟</h2>\n<p><strong>لا تتوفر في هذه المراجعة قائمة رسمية محدثة من نيسان مصر</strong> تثبت أسعار 2,800–3,500 أو 12,000–15,000 جنيه لكل زيارة. لذلك أزلنا الأرقام القديمة التي كانت تُعرض كتكلفة شاملة للقطع والضريبة من غير فاتورة أو مستند. يختلف السعر حسب سنة السيارة وبنود الزيارة ومواصفة الزيت والقطع وأجور المركز والضريبة.</p>\n<div style=\"overflow-x:auto\"><table><thead><tr><th>البند في مقايسة الصيانة</th><th>التفصيل المطلوب قبل الموافقة</th></tr></thead><tbody>\n<tr><td>الزيت والفلاتر</td><td>العلامة والمواصفة والكمية ورقم القطعة وسعر كل بند</td></tr>\n<tr><td>البوجيهات والتيل</td><td>رقم الجزء وحالة القطع ونوع البديل وضمانه</td></tr>\n<tr><td>سائل الفتيس</td><td>كود CVT ومواصفة NS/رقم المنتج وكمية التعبئة وإجراء ضبط المستوى</td></tr>\n<tr><td>المصنعية</td><td>أجر الخدمة والقياس والفحص والضريبة منفصلًا</td></tr>\n</tbody></table></div>\n<h2>أين تجد مركز صيانة نيسان سنترا معتمدًا؟</h2>\n<p>استخدم <a href=\"https://ar.nissan.com.eg/find-a-dealer.html\" rel=\"noopener noreferrer\">أداة البحث الرسمية عن مراكز خدمة نيسان في مصر</a> بدل الاعتماد على رقم هاتف قديم أو عنوان من مقال، واختر «مركز خدمة» ثم المدينة. ويمكن الاتصال بخدمة عملاء نيسان مصر على <strong>16244</strong> وفق <a href=\"https://ar.nissan.com.eg/owners/peace-of-mind/customer-service.html\" rel=\"noopener noreferrer\">صفحة الاتصال الرسمية</a> للتأكد من اعتماد المركز وتوفر قطع الغيار وتكلفة الكشف والحجز. لا يدعي موقع أعطال.كوم أن له مركز خدمة نيسان معتمدًا أو صلة تشغيل رسمية بالوكيل.</p>\n<h2>متى تقلق من صفارة الفرامل أو رجّة الفتيس؟</h2>\n<p>صوت صفارة الفرامل لا يعني أن خرط الطنابير هو العلاج؛ افحص سمك التيل وطبيعة الخامة وحالة سطح القرص والتثبيت والغبار. أما نتشة أو تحذير فتيس فابدأ بقراءة كود TCM وفحص السائل والمبرد والقواعد والبرمجة الخاصة بناقل السيارة. إذا فقدت الفرامل قدرتها أو فقدت السيارة الحركة على طريق سريع، توقف بأمان واستعن بمركز متخصص.</p>\n<h2>كيف تحتفظ بسجل صيانة مفيد لنيسان سنترا؟</h2>\n<p>سجل كل زيارة بتاريخها وعدّادها، وأرقام القطع ومواصفات الزيوت والكمية والفاتورة والتقرير. احتفظ بملاحظات التآكل والتسريب والأكواد قبل وبعد الإصلاح. ده يوفر وقتًا وتكلفة عند تشخيص عطل متكرر ويساعد في فحص السيارة قبل البيع.</p>\n<h2>أسئلة شائعة</h2>\n<h3>هل صيانة سنترا كل 10 آلاف كم؟</h3><p>تذكر شبكة الموزع المعتمد فاصلًا عامًا 10 آلاف كم أو 6 أشهر، لكن بعض البنود لها فترات استبدال مختلفة حسب سنة السيارة وظروف استخدامها.</p>\n<h3>هل أغير زيت CVT عند 100 ألف كم؟</h3><p>القرار يعتمد على جدول خدمة ناقل السيارة الفعلي ورقم VIN والظروف ونتائج الفحص؛ لا توجد قاعدة واحدة لكل سنة أو جيل.</p>\n<h3>هل أي مركز مكتوب عنه في الإنترنت معتمد من نيسان؟</h3><p>لا. التأكد من الاعتماد يتم من موقع نيسان مصر أو خدمة العملاء 16244، وليس من وصف تسويقي أو نتيجة بحث قديمة.</p>\n<h3>هل تبديل التيل وخرط الطنابير مطلوبان عند أي صفارة؟</h3><p>لا. صوت الفرامل يحتاج فحص قياسات التيل والقرص والتركيب والتلوث والظروف قبل تحديد الإصلاح.</p>"
  }
]
MARK="a3tal-third50-tech-20261114"
def verify_old(t,p,pub):
 if (int(p.get("id",0)),p.get("slug"),p.get("status"),p.get("type"),int(p.get("featured_media") or 0))!=(
   t["id"],t["slug"],"publish","post",t["cover"]):
   raise RuntimeError("Article identity status or media drift")
 if not p.get("modified_gmt","").startswith(t["mod"]):
   raise RuntimeError("Original article modified since audit")
 yo=pub.get("yoast_head_json") or {}
 if yo.get("canonical")!=b.SITE+"/"+t["slug"]+"/" or not yo.get("og_image") or (yo.get("robots") or {}).get("index")=="noindex":
   raise RuntimeError("Canonical, OG and robots mismatch")
 if len(p.get("content",""))<4500:raise RuntimeError("Original article unexpectedly short")
 return yo
def human_content(t,raw):
 image_tags=re.findall(r"<img\b[^>]*>",raw,re.I)
 if t["kind"]=="six":
  if image_tags:raise RuntimeError("Unexpected six-speed original inline images")
  if "Dexron VI" not in raw or "40,000" not in raw:
   raise RuntimeError("Original six-speed claims changed since human review")
  body=t["html"]
 else:
  if len(image_tags)!=1 or "2,800" not in raw or "مركز خدمة أعطال" not in raw:
    raise RuntimeError("Sentra source differs: media or inaccurate price claims gone")
  figures=re.findall(r"<figure\b[^>]*>[\s\S]*?</figure>",raw,re.I)
  if len(figures)==1 and len(re.findall(r"<img\b",figures[0],re.I))==1:
   image=figures[0]
  elif not figures:
   image='<figure class="a3tal-legacy-media">'+image_tags[0]+'</figure>'
  else:raise RuntimeError("Unknown original Sentra image wrapper")
  anchor="<h2>زيت فتيس نيسان سنترا CVT: هل دائمًا NS-3؟</h2>"
  if t["html"].count(anchor)!=1:raise RuntimeError("Media slot changed")
  body=t["html"].replace(anchor,image+"\n"+anchor,1)
 if body.count("<h2>")<6 or body.count('<a href="')<3 or len(body)<4500:
   raise RuntimeError("Human rewrite missing structure or sources")
 if len(re.findall(r"<img\b",body,re.I))!=len(image_tags):
   raise RuntimeError("Original inline picture count changed")
 return '<section id="'+MARK+'-'+t["kind"]+'" dir="rtl">'+body+'</section>'
def main():
 plan=[]
 for t in ROWS:
  old=b.bridge_post(t["id"]);pub=b.public_post(t["id"])
  if MARK+"-"+t["kind"] in old.get("content",""):
   print("THIRD50_TECH_ALREADY",t["id"],flush=True);continue
  verify_old(t,old,pub)
  body=human_content(t,old["content"])
  plan.append((t,old,pub,body))
  print("THIRD50_TECH_PREFLIGHT",t["id"],len(old["content"]),len(body),flush=True)
 print("THIRD50_TECH_ALL_PREFLIGHTS_PASS",len(plan),flush=True)
 for t,old,pub0,body in plan:
  now=b.bridge_post(t["id"])
  if now.get("modified_gmt")!=old.get("modified_gmt") or now.get("content")!=old.get("content"):
   raise RuntimeError("Concurrent edit before write")
  meta={"_yoast_wpseo_title":t["seo"],"_yoast_wpseo_metadesc":t["desc"],"_yoast_wpseo_focuskw":t["kw"],
        "_yoast_wpseo_opengraph-title":t["seo"],"_yoast_wpseo_opengraph-description":t["desc"],
        "_yoast_wpseo_twitter-title":t["seo"],"_yoast_wpseo_twitter-description":t["desc"]}
  try:
   b.req("/update-post",{"id":t["id"],"expected_modified_gmt":now["modified_gmt"],"title":t["title"],"content":body,"meta":meta})
  except Exception as err:
   if MARK+"-"+t["kind"] not in b.bridge_post(t["id"]).get("content",""):
    raise RuntimeError("Unconfirmed write, no retry") from err
  after=b.bridge_post(t["id"]);pub=b.public_post(t["id"]);seo=pub.get("yoast_head_json") or {}
  if (after.get("slug"),after.get("status"),after.get("title"),int(after.get("featured_media") or 0))!=(
     t["slug"],"publish",t["title"],t["cover"]):
     raise RuntimeError("Article slug/status/cover/title changed")
  if after["content"].count('id="'+MARK+"-"+t["kind"]+'"')!=1 or seo.get("description")!=t["desc"]:
     raise RuntimeError("New article or Yoast meta not saved")
  if seo.get("canonical")!=pub0["yoast_head_json"]["canonical"] or (
    seo.get("robots") or {}).get("index")=="noindex" or (
    seo.get("og_image") or [{}])[0].get("url")!=(pub0["yoast_head_json"].get("og_image") or [{}])[0].get("url"):
     raise RuntimeError("Canonical, index or featured OG changed")
  if t["kind"]=="sentra" and len(re.findall(r"<img\b",after["content"],re.I))!=1:
     raise RuntimeError("Original inline Sentra photo disappeared")
  print("THIRD50_TECH_LIVE_VERIFIED",t["id"],after.get("link"),flush=True)
  time.sleep(1)
 print("THIRD50_TECH_REPAIRS_COMPLETE",flush=True)
if __name__=="__main__":main()
