#!/usr/bin/env python3
"""A3tal Egypt editorial correction batch03: Xpander A/C, gearbox, motorcycle parts.
Read-before-write through GitHub + A3tal Direct Bridge. Preserves post ID,
URL, categories, tags, original featured image and original OG image.
No new articles, no generic overwrite, no made-up intervals, no media deletion.
"""
import importlib.util
import re
import time
from collections import Counter

spec=importlib.util.spec_from_file_location("a3tal_human", "scripts/review-human-seo-geo-egypt-three-20261114.py")
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

MARK="a3tal-human-batch03-20261114"
ROWS=[
 {"id":80930,"slug":"mitsubishi-xpander-electrical-ac-problems-smart-key",
  "date":"2026-02-08T19:42:24","cover":80931,"kind":"ac",
  "check":["تكييف إكسباندر","ريموت البصمة","شحن الفريون"],
  "title":"أعطال تكييف وكهرباء ميتسوبيشي إكسباندر: التبريد والبصمة والبطارية",
  "seo":"أعطال تكييف وكهرباء إكسباندر: خطوات الفحص | أعطال",
  "desc":"تكييف ميتسوبيشي إكسباندر ضعيف أو البصمة لا تستجيب؟ تعرف على فحص المروحة والفريون والريموت وبطارية 12 فولت قبل تغيير القطع.",
  "kw":"أعطال تكييف ميتسوبيشي إكسباندر",
  "links":[
    "https://a3tal.com/mitsubishi-xpander-fault-codes-dtc-guide/",
    "https://a3tal.com/أعطال-التكييف-في-السيارات/",
    "https://a3tal.com/mitsubishi-xpander-gearbox-cvt-suspension-problems/"
  ]},
 {"id":80926,"slug":"mitsubishi-xpander-gearbox-cvt-suspension-problems",
  "date":"2026-02-08T19:37:04","cover":80927,"kind":"gear",
  "check":["فتيس إكسباندر","العفشة","ضغط الإطارات"],
  "title":"أعطال فتيس وعفشة ميتسوبيشي إكسباندر: تشخيص النتشة والخبط",
  "seo":"أعطال فتيس وعفشة إكسباندر: نتشة وخبط | أعطال",
  "desc":"دليل فحص فتيس ميتسوبيشي إكسباندر الأوتوماتيك أو CVT حسب الموديل، وأسباب النتشة وخبط العفشة والفرامل وضغط الإطارات الصحيح.",
  "kw":"أعطال فتيس ميتسوبيشي إكسباندر",
  "links":[
    "https://a3tal.com/mitsubishi-xpander-engine-performance-fuel-pump-faults/",
    "https://a3tal.com/mitsubishi-xpander-electrical-ac-problems-smart-key/",
    "https://a3tal.com/mitsubishi-xpander-fault-codes-dtc-guide/"
  ]},
 {"id":83152,"slug":"motorcycle-genuine-vs-aftermarket-parts",
  "date":"2026-10-08T15:07:32","cover":83341,"kind":"parts",
  "check":["Aftermarket","رقم القطعة","الفرامل"],
  "title":"قطع غيار الموتوسيكل: الفرق بين الأصلي وOEM وAftermarket قبل الشراء",
  "seo":"قطع غيار الموتوسيكل: الأصلي وOEM والبديل | أعطال",
  "desc":"تشتري قطع غيار موتوسيكل أصلية أم بديلة؟ افهم الفرق بين Genuine وOEM وAftermarket، وطابق رقم القطعة والمقاس والمصدر قبل التركيب.",
  "kw":"قطع غيار الموتوسيكل",
  "links":[
    "https://a3tal.com/motorcycle-maintenance-schedule-guide/",
    "https://a3tal.com/motorcycle-chain-slack-tightening-maintenance-guide/"
  ]},
]

HTML={
"ac":r"""
<section id="a3tal-human-batch03-20261114-ac" dir="rtl">
<p><strong>أعطال تكييف وكهرباء ميتسوبيشي إكسباندر</strong> لا تبدأ دائمًا من الكمبروسر أو البطارية. لو التكييف ضعيف، افحص هل الهواء الخارج من الفتحات قليل أصلًا، أم تدفقه طبيعي لكنه غير بارد. ولو ظهرت رسالة Key not detected، ابدأ بفحص حالة ريموت المفتاح وبطارية 12 فولت وظروف ظهور الرسالة قبل شراء وحدة بصمة جديدة.</p>
<p>حدد سنة الإنتاج وفئة إكسباندر وسوقها ورقم الشاسيه VIN؛ تجهيزات المكيف الخلفي ونظام الدخول والتشغيل قد تختلف بين نسخة وأخرى. لا نعتبر شكاوى ملاك خارج مصر دليلًا على عيب منتشر في كل السيارات المصرية.</p>
<h2>إكسباندر التكييف ضعيف: من أين تبدأ؟</h2>
<div style="overflow-x:auto"><table>
<thead><tr><th scope="col">العرض</th><th scope="col">أول فحص عملي</th><th scope="col">ما الذي لا نستنتجه من العرض وحده؟</th></tr></thead>
<tbody>
<tr><td>الهواء ضعيف من الفتحات</td><td>فلتر المقصورة، مروحة النفخ، بوابات الهواء ومدخل السحب</td><td>ليس دليلًا على نقص الفريون</td></tr>
<tr><td>هواء قوي لكنه دافئ</td><td>المراوح والمكثف وأوامر الكمبروسر وضغوط وسيط التبريد لدى فني</td><td>لا يعني أن الكمبروسر يحتاج تغييرًا</td></tr>
<tr><td>يبرد أثناء الحركة ويضعف في الوقوف</td><td>مروحة المكثف وتدفق الهواء وحرارة التشغيل</td><td>لا تحكم على الشحنة من هذه العلامة فقط</td></tr>
<tr><td>الهواء الأمامي بارد والخلفي ضعيف</td><td>إعدادات ومروحة ومجاري توزيع الهواء الخلفية بحسب الفئة</td><td>لا تفترض وجود عطل في وحدة تبريد خلفية بكل نسخة</td></tr>
</tbody></table></div>
<p>نظافة المكثف مفيدة عند تراكم الأتربة، لكن يُنظَّف والمحرك متوقف وبطريقة لا تثني الزعانف أو ترش الوصلات الكهربائية بضغط مؤذٍ. الفحص الكامل لدائرة التبريد يتطلب معدات وخبرة، ولا يُفك خط الفريون في المنزل.</p>
<h2>هل فريون إكسباندر يحتاج شحنًا كل سنتين؟</h2>
<p><strong>لا يوجد موعد ثابت لشحن الفريون كل سنتين إذا كانت الدائرة سليمة.</strong> التكييف دائرة مغلقة؛ عند نقص الشحنة ينبغي البحث عن التسريب وإصلاحه، ثم شحن النوع والكمية المقررين على ملصق السيارة أو في دليل الخدمة. الشحن العشوائي أو المبالغة في الكمية قد يضعف الأداء ويضر المكونات. للمقارنة اقرأ <a href="https://a3tal.com/أعطال-التكييف-في-السيارات/">تشخيص ضعف تكييف السيارات</a>.</p>
<h2>البصمة لا تتعرف على المفتاح أو تظهر Key not detected</h2>
<p>ابدأ بتجربة المفتاح الاحتياطي إن توفر، وراجع رسالة العدادات وظروفها: هل تتكرر في كل مكان؟ هل يظهر معها ضعف عام في الكهرباء؟ قد تكون المشكلة بطارية الريموت أو موضعه أو بطارية السيارة 12 فولت أو مستقبل الإشارة أو أسلاك النظام. لا تفترض مقاس بطارية الريموت CR2032 أو تغييرها سنويًا لكل الإصدارات؛ ارجع إلى دليل المالك للسيارة والمفتاح الفعلي.</p>
<p>تختلف طريقة التشغيل عند ضعف بطارية المفتاح حسب نظام Keyless المجهز في الفئة. استخدم الخطوات المبيّنة في كتيب المالك ولا تجرب توصيل أسلاك أو تجاوز نظام منع التشغيل. إذا بقي العطل بعد الاختبارات الأولية، تحتاج الورشة قراءة وحدة KOS والأكواد الكهربائية بأداة متوافقة.</p>
<h2>ضعف بطارية إكسباندر أو لمبة شحن: فحص قبل الاستبدال</h2>
<p>البطارية ليست لها مدة عمر واحدة مضمونة. الزحام والحرارة وتاريخ الشحن والرحلات القصيرة وطريقة الاستخدام تؤثر في حالتها. قِس جهد البطارية بعد الراحة، ثم جهد الشحن تحت الأحمال لدى فني، وافحص القواطيش والأرضي وتسريب التيار إن كان الشحن سليمًا والبطارية تفرغ أثناء التوقف.</p>
<p>لا تُركب لمبات أو أحمالًا كهربائية إضافية من غير تقييم الفيوزات ومقطع السلك والتوصيلات. خطأ في تركيب ملحق يمكن أن يسبب سخونة أو أعطالًا بالدوائر، لكنه لا يثبت تلقائيًا تلف وحدة ETACS.</p>
<h2>هل تشغيل التكييف والسيارة أسرع من 80 كم/س يضر الكمبروسر؟</h2>
<p>لا توجد قاعدة فنية عامة تلزم سائق إكسباندر بإطفاء التكييف فوق سرعة معينة قبل تشغيله. أنظمة التكييف مصممة للعمل أثناء القيادة مع تحكمات وحمايات بحسب التصميم. إذا سمعت صوتًا غير عادي أو ظهر فقد تبريد مفاجئ، افحص النظام بدل استخدام سرعة 80 كم/س كحد صيانة مفترض.</p>
<h2>متى تتوقف عن استخدام السيارة حتى الفحص؟</h2>
<p>إذا ظهرت رائحة احتراق كهربائي أو دخان أو سخونة غير معتادة أو تحذير شحن مع ضعف متزايد في الأنوار، اركن في مكان آمن ولا تستمر في الرحلة قبل التقييم. ضعف التبريد وحده ليس عطلًا ميكانيكيًا يستوجب تغيير كمبروسر فورًا.</p>
<h2>مراجع وروابط مفيدة لمالك إكسباندر</h2>
<p>تتيح ميتسوبيشي <a href="https://www.mitsubishi-motors.co.th/en/after-sales/promotion-and-other-services/owner-manual" rel="noopener noreferrer">أدلة مالك رسمية لطرازات إكسباندر</a>، وكذلك <a href="https://microsite.mitsubishi-motors.co.id/owner-manual/" rel="noopener noreferrer">فهرس أدلة إكسباندر حسب السنة</a>. هذه الأدلة لأسواقها المعلنة، وتُستخدم لمراجعة مبدأ التشغيل لا لإثبات تطابق نسخة مصر دون VIN. لمعرفة رموز الأعطال راجع <a href="https://a3tal.com/mitsubishi-xpander-fault-codes-dtc-guide/">دليل أكواد إكسباندر</a>، ولمشاكل الفتيس والعفشة راجع <a href="https://a3tal.com/mitsubishi-xpander-gearbox-cvt-suspension-problems/">فحص فتيس وعفشة إكسباندر</a>.</p>
<h2>أسئلة شائعة عن كهرباء وتكييف إكسباندر</h2>
<h3>هل ضعف تكييف الصف الثالث يعني نقص فريون؟</h3>
<p>ليس بالضرورة. قارن تدفق الهواء وإعدادات المروحة الخلفية حسب الفئة أولًا، ثم افحص منظومة التبريد إن كان الهواء قويًا لكنه لا يبرد.</p>
<h3>هل أغيّر البطارية لأن عمرها تجاوز سنتين؟</h3>
<p>ليس العمر وحده دليلًا. اختبار البطارية والشحن والتوصيلات يساعد على تحديد ما إذا كانت تحتاج استبدالًا.</p>
<h3>هل يمكن مسح رسالة البصمة ويختفي العطل؟</h3>
<p>المسح لا يصلح عطل التغذية أو المستقبل. سجّل الرسالة والأكواد وظروف ظهورها ثم اختبر السبب.</p>
</section>
""",
"gear":r"""
<section id="a3tal-human-batch03-20261114-gear" dir="rtl">
<p><strong>أعطال فتيس وعفشة ميتسوبيشي إكسباندر</strong> لازم تتشخّص بناءً على سنة السيارة ونوع الفتيس والأعراض الفعلية. نتشة عند التحرك لا تعني فورًا تلف الفتيس، وخبطة على مطب لا تعني أن المساعدين انتهوا. ابدأ بمراجعة بيانات السيارة ورقم الشاسيه VIN وتاريخ الصيانة، ثم اطلب فحصًا يحدد السبب بدل تغيير أجزاء بالتجربة.</p>
<p>بعض إصدارات إكسباندر في أسواق وسنوات معينة مزودة بأوتوماتيك تقليدي، وأخرى بناقل CVT. لا تنقل زيت فتيس أو مواعيد خدمة أو نصائح قيادة من واحدة للتانية اعتمادًا على اسم إكسباندر وحده. دليل المالك والوكيل بحسب VIN هما المرجع.</p>
<h2>هل فتيس إكسباندر 4AT أم CVT؟</h2>
<p>السنة والسوق والفئة هي التي تحسم نوع ناقل الحركة. لا يعتبر سلوك الـRPM أو شكل عصا الفتيس إثباتًا كافيًا؛ افحص بيانات السيارة أو كود ناقل الحركة في سجلات الخدمة. ناقل CVT له مواصفات سائل وإجراءات صيانة مختلفة عن الأوتوماتيك التقليدي، ولا يستخدم زيت ATF عام لكل النسخ.</p>
<h2>إكسباندر بتنتش بين R وD: ما أول فحص؟</h2>
<div style="overflow-x:auto"><table>
<thead><tr><th scope="col">العرض</th><th scope="col">ما يجب فحصه</th><th scope="col">ملحوظة</th></tr></thead>
<tbody>
<tr><td>تأخير واضح عند اختيار D أو R</td><td>مستوى ومواصفة سائل الناقل بالطريقة الصحيحة، قواعد المحرك والفتيس والأكواد</td><td>طريقة قياس الزيت ليست واحدة في كل ناقل</td></tr>
<tr><td>نتشة عند التسارع أو التهدئة</td><td>ظروف ظهورها، البرمجة والأكواد والتغذية والاحتراق والقواعد</td><td>قد يكون العَرَض من المحرك لا من الفتيس</td></tr>
<tr><td>تحذير فتيس أو سخونة مع فقد حركة</td><td>التوقف الآمن وقراءة وحدة TCM وفحص الناقل لدى مختص</td><td>تجنب اختبار الحمل المتكرر أو إجبار السيارة على الحركة</td></tr>
<tr><td>ونة أو رجة مع سرعة الطريق</td><td>الإطارات وبلي العجل والكبالن وناقل الحركة حسب ظهور الصوت</td><td>ليست كل ونة من CVT</td></tr>
</tbody></table></div>
<p>لا تكرر النقل بعنف من D إلى R والسيارة تتحرك، ولا تستخدم قراءة كود عام لتحديد قطعة قبل فحص الوحدة المعنية. لو فيه تقطيع موتور عند النقل أو ضعف سحب، راجع <a href="https://a3tal.com/mitsubishi-xpander-engine-performance-fuel-pump-faults/">فحص محرك وطلمبة بنزين إكسباندر</a> قبل نسبة العرض للفتيس.</p>
<h2>هل زيت فتيس إكسباندر يتغير كل 40 إلى 60 ألف كم؟</h2>
<p><strong>مافيش رقم واحد آمن لكل سيارات إكسباندر.</strong> جدول تغيير الزيت ونوع السائل وإجراء ضبط المستوى ونمط الاستخدام القاسي يختلفون حسب الناقل وسنة الإنتاج. اطلب من مركز الخدمة المواصفة والفترة الصحيحتين كتابة مع VIN، ولا تقبل إدخال زيت «متعدد الاستخدام» في CVT من غير إثبات مطابقته.</p>
<h2>خبط أو تزييق في عفشة إكسباندر على المطبات</h2>
<p>وصلة الميزان وجلب المقصات وقواعد المساعدين والمفاصل والمساعد نفسه قد تصدر أصواتًا متشابهة. سجّل هل الصوت أمامي أم خلفي، وعلى مطب صغير أم مع الفرامل، وهل هناك أثر حادث أو تعديل في الجنط. افحص تثبيت الأجزاء والخلوص وتحميل الجلب على رافعة آمنة، ولا ترش سيليكون لتغطية صوت باعتباره إصلاحًا.</p>
<h2>ضغط كاوتش إكسباندر مع الحمولة</h2>
<p>لا تطبق 32 PSI للراحة أو 35 PSI للحمولة من دون الرجوع إلى ملصق ضغط الإطارات على السيارة نفسها. الضغط الصحيح قد يختلف بين الأمام والخلف ومع الحمولة ومقاس الإطار المعتمد. استخدم ضغط الإطارات الباردة المكتوب لنسختك، ولا تعالج إحساس الخبط بخفض الضغط عشوائيًا.</p>
<h2>تآكل التيل ورعشة الفرامل: هل يلزم خرط الطنابير؟</h2>
<p>عمر تيل الفرامل ليس 25 ألف كيلومتر ثابتًا؛ يتأثر بالزحام والحمولة وطريقة القيادة ونوع التيل. عند رعشة الفرامل، افحص الإطارات والتثبيت وحالة الأقراص والسمك والاعوجاج واحتكاك الكاليبر أولًا. خرط القرص أو تغييره لا يُقرر من الإحساس وحده؛ يجب القياس مقابل الحدود المعتمدة للطراز.</p>
<h2>متى تمنعك الأعراض من استكمال الطريق؟</h2>
<p>رجة شديدة، فقد استجابة الدركسيون أو الفرامل، صوت احتكاك معدني قوي، أو تسريب سائل واضح من ناقل الحركة أو الفرامل تستوجب توقفًا آمنًا وفحصًا قبل السفر. لا تختبر ثبات سيارة بها خلوص مشكوك فيه على سرعة عالية.</p>
<h2>مراجع وروابط تشخيص إكسباندر</h2>
<p>راجع <a href="https://microsite.mitsubishi-motors.co.id/owner-manual/" rel="noopener noreferrer">مكتبة ميتسوبيشي الرسمية لأدلة إكسباندر حسب السنة والفئة</a> بوصفها مرجعًا لنسخ السوق الذي تصدر فيه، لا بديلاً عن كتيب مصر. لأكواد المحرك والناقل تابع <a href="https://a3tal.com/mitsubishi-xpander-fault-codes-dtc-guide/">دليل الأكواد</a>، ولأعطال البطارية والتكييف راجع <a href="https://a3tal.com/mitsubishi-xpander-electrical-ac-problems-smart-key/">كهرباء وتكييف إكسباندر</a>.</p>
<h2>أسئلة شائعة عن فتيس وعفشة إكسباندر</h2>
<h3>هل فتيس الـCVT في إكسباندر أعطاله أكثر دائمًا؟</h3>
<p>مفيش حكم عام من دون بيانات موثقة للسنة والسوق والصيانة. الفحص وتاريخ الاستخدام ونوع الناقل أهم من الانطباعات.</p>
<h3>هل الدبدبة من العفشة طبيعية لأنها سبعة ركاب؟</h3>
<p>اختلاف الراحة حسب الوزن والمقاس وارد، لكن صوت خبط جديد أو خلوص ظاهر يحتاج فحصًا؛ لا تعتبره صفة ثابتة لكل إكسباندر.</p>
<h3>هل ضبط الزوايا يصلح أي خبط؟</h3>
<p>لا. الزوايا تعالج محاذاة العجلات ضمن الحدود المسموحة، أما الجلب والروابط المتهالكة فتحتاج إصلاح السبب أولًا.</p>
</section>
""",
"parts":r"""
<section id="a3tal-human-batch03-20261114-parts" dir="rtl">
<p><strong>قطع غيار الموتوسيكل الأصلية أم البديلة؟</strong> مش كل قطعة Aftermarket وحشة، ومش كل علبة عليها لوجو معروف أصلية. الاختيار الصحيح يبدأ بالموديل وسنة الإنتاج ورقم القطعة ومواصفتها، ثم مصدر موثوق وفاتورة وضمان واضح. في أجزاء الفرامل والتوجيه والعجلات، التوافق والسلامة أهم من فرق السعر.</p>
<p>مصطلحات Genuine وOEM وOES وAftermarket أحيانًا بيستخدمها البائعون بمعانٍ مختلطة. لا تدفع ثمن «أصلي وكالة» لمجرد أن البائع كتب OEM على الإعلان؛ اطلب دليل منشأ القطعة ورقمها وتوافقها مع موتوسيكل العميل نفسه.</p>
<h2>الفرق بين Genuine وOEM وAftermarket</h2>
<div style="overflow-x:auto"><table>
<thead><tr><th scope="col">المصطلح</th><th scope="col">المقصود عادة</th><th scope="col">ما الذي يثبت أنه مناسب؟</th></tr></thead>
<tbody>
<tr><td>Genuine / أصلي معتمد من ماركة الدراجة</td><td>قطعة تُباع ضمن قنوات الشركة أو علامتها وبترقيمها</td><td>رقم القطعة والفاتورة ومصدر بيع رسمي مطابق</td></tr>
<tr><td>OEM / مورّد تجهيز أصلي</td><td>مصنّع قد يورد مكونات لشركة مركبات، لكن المصطلح وحده لا يثبت أن نفس القطعة للموديل</td><td>الشركة المصنعة والرقم الفني وبيانات المطابقة</td></tr>
<tr><td>OES</td><td>تسمية سوقية لقطع أو مورّدين بجودة أو منشأ قريب من شبكة التجهيز الأصلي</td><td>لا يكفي الاسم؛ يلزم إثبات المرجع والمواصفات</td></tr>
<tr><td>Aftermarket / بديل</td><td>قطعة من منتج مستقل، جودتها تتفاوت</td><td>مواصفات وملاءمة موثقة وسمعة الشركة والضمان</td></tr>
<tr><td>مجهولة أو مقلدة</td><td>مصدر أو بيانات غير قابلة للتحقق أو شعار مزور</td><td>تجنبها خصوصًا في المكونات المؤثرة في السلامة</td></tr>
</tbody></table></div>
<p>حتى إن صنعت شركة معروفة قطعًا لتجهيز مصنع دراجات، فهذا لا يعني أن كل منتجاتها البديلة مطابقة لنفس رقم القطعة. الأفضل التأكد بالكتالوج الرسمي للموديل وليس بالتخمين من شكل أو فيشة مشابهة.</p>
<h2>إزاي تتأكد إن القطعة راكبة على موتوسيكلك؟</h2>
<ol>
<li>اكتب الشركة والموديل وسنة الإنتاج ونسخة المحرك، ورقم الشاسيه إن لزم لتحديد التوافق.</li>
<li>استخرج رقم القطعة من كتالوج قطع الغيار أو دليل الصيانة المعتمد، لا من صورة منتج مشابه.</li>
<li>اطلب من البائع رقم الشركة المصنّعة والمواصفة والضمان والفاتورة وإمكانية الاسترجاع إذا لم تطابق.</li>
<li>راجع أبعاد القطعة والفيش والتثبيت والمواد مع فني مؤهل قبل التركيب، خصوصًا في الفرامل والتوجيه.</li>
<li>احتفظ ببيانات الفاتورة والتغليف ورقم الدفعة عند توفره لحين التأكد من أداء القطعة.</li>
</ol>
<p>كمثال لطريقة البحث الصحيحة، تتيح <a href="https://www.yamaha-motor.eu/ie/en/service-support/genuine-parts/parts-catalogue/" rel="noopener noreferrer">ياماها كتالوجًا رسميًا لقطع الغيار بحسب الموديل ورسوم التوضيح</a>. هذه الطريقة مفيدة للتعلّم، لكنها لا تجعل رقم ياماها مناسبًا لدراجة من علامة أخرى.</p>
<h2>إيه قطع الغيار اللي ماينفعش تخاطر فيها؟</h2>
<p>تيل الفرامل وأقراصها وخرطوم الفرامل والإطارات ومسامير العجل وبيضة المقود وأجزاء التوجيه كلها تؤثر في الأمان. لا تشتريها من مصدر مجهول حتى لو المقاس الظاهري قريب، ولا تجرّب تغيير مواصفات تيل أو خرطوم على الطريق. عند ظهور ضعف فرامل أو ارتخاء توجيه بعد الإصلاح، توقف عن القيادة إلى أن تُراجع الورشة التركيب والتوافق.</p>
<p>تذكّر قائمة <a href="https://msf-usa.org/documents/library/t-clocs-pre-ride-inspection-checklist/" rel="noopener noreferrer">فحص الموتوسيكل T-CLOCS من Motorcycle Safety Foundation</a> للفرامل والعجلات والتوجيه قبل الركوب، بغض النظر عن نوع قطع الغيار المستخدمة.</p>
<h2>هل شراء البديل الأرخص يوفّر فلوس فعلًا؟</h2>
<p>قارن تكلفة القطعة والتركيب وإمكانية الإرجاع واحتمال تكرار الإصلاح. بديل موثوق ومطابق قد يكون خيارًا مناسبًا لقطع كثيرة، لكن جزءًا غير واضح المصدر قد يكلّفك فكًا وتركيبًا مرتين، أو يعرّضك لخطر لو أثر في الفرامل أو العجل.</p>
<h2>هل القطعة الصينية تنفع بدل الأصلية؟</h2>
<p>مكان التصنيع وحده لا يحكم على الجودة. بعض قطع الغيار مصنّعة في الصين وفق مواصفات صارمة، وأخرى لا تملك بيانات اختبار موثوقة. الأهم هو الشركة الفعلية، وملاءمة القطعة، ومواصفاتها، ومصدرها، وإمكان الرجوع لها عند ظهور عيب.</p>
<h2>قبل تغيير السلسلة أو التيل</h2>
<p>لو هتغيّر مجموعة السلسلة والتروس، استخدم <a href="https://a3tal.com/motorcycle-chain-slack-tightening-maintenance-guide/">دليل فحص شد السلسلة وتآكل التروس</a> لتفهم ما الذي يستدعي الاستبدال فعلًا. ولأن مواعيد تغيير القطع تختلف حسب الاستخدام، راجع <a href="https://a3tal.com/motorcycle-maintenance-schedule-guide/">جدول صيانة الموتوسيكل</a> وكتالوج طرازك بدل تركيب قطع لمجرد تجاوز رقم كيلومترات عشوائي.</p>
<h2>أسئلة شائعة عن قطع غيار الموتوسيكل</h2>
<h3>هل كلمة OEM على الإعلان دليل الأصالة؟</h3>
<p>لا. اطلب رقم القطعة والمنتج والمصدر والفاتورة. مصطلحات السوق قد تُستخدم بشكل غير دقيق.</p>
<h3>هل ينفع أشتري قطعة حسب سعة المحرك فقط؟</h3>
<p>لا. دراجتان بسعة 150 سي سي قد تختلفان في المحرك والفيش والتثبيت والأبعاد، فلا تُثبت الملاءمة إلا ببيانات الطراز والجزء.</p>
<h3>إمتى أرجع القطعة للبائع؟</h3>
<p>عند اختلاف الرقم أو المقاس أو الفيشة أو ظهور خلل في الجودة قبل الاستخدام، احتفظ بالتغليف والفاتورة واتبع سياسة الاسترجاع المتفق عليها.</p>
</section>
"""
}

def review(t,live,public):
    if (int(live.get("id",0)),live.get("slug"),live.get("status"),live.get("type"),int(live.get("featured_media") or 0))!=(
        t["id"],t["slug"],"publish","post",t["cover"]):
        raise RuntimeError("Post identity changed; stop: "+t["slug"])
    if (public.get("slug"),public.get("status"),int(public.get("featured_media") or 0))!=(
        t["slug"],"publish",t["cover"]):
        raise RuntimeError("Public identity changed: "+t["slug"])
    if not live.get("modified_gmt","").startswith(t["date"]):
        raise RuntimeError("Post edited since human audit: "+t["slug"])
    if not live.get("content") or not (1600<len(live["content"])<20000):
        raise RuntimeError("Unexpected original length: "+t["slug"])
    for sign in t["check"]:
        if sign not in base.readable_markup(live["content"]):
            raise RuntimeError("Original content topic changed: "+sign)
    if re.search(r"<(?:img|figure)\b",live["content"],re.I):
        raise RuntimeError("Inline media found. Refuse overwrite without preservation plan: "+t["slug"])
    seo=public.get("yoast_head_json") or {}
    if (seo.get("canonical")!=base.SITE+"/"+t["slug"]+"/" or
        (seo.get("robots") or {}).get("index")=="noindex" or
        not seo.get("og_image")):
        raise RuntimeError("Unexpected canonical/index/OG state: "+t["slug"])
    h=HTML[t["kind"]]
    if h.count('id="'+MARK+"-"+t["kind"]+'"')!=1 or h.count("<h2>")<5:
        raise RuntimeError("Unsafe new human-reviewed body")
    if any(u not in h for u in t["links"]):
        raise RuntimeError("Missing verified internal URL")
    if not (2500<len(h)<14000):
        raise RuntimeError("Unexpected authored length")
    return h

def main():
    planned=[]
    for t in ROWS:
        live=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
        if MARK+"-"+t["kind"] in live.get("content",""):
            print("ALREADY_APPLIED",live.get("link"),flush=True)
            continue
        updated=review(t,live,pub)
        planned.append((t,live,pub,updated))
        print("BATCH03_PREFLIGHT",t["id"],t["slug"],"original_len",len(live["content"]),"reviewed_len",len(updated),flush=True)
    print("BATCH03_ALL_PREFLIGHTS_PASS",len(planned),flush=True)
    for t,before,before_public,updated in planned:
        reread=base.bridge_post(t["id"])
        if reread["content"]!=before["content"] or reread["modified_gmt"]!=before["modified_gmt"]:
            raise RuntimeError("Concurrent content edit; do not overwrite: "+t["slug"])
        meta={
            "_yoast_wpseo_title":t["seo"],
            "_yoast_wpseo_metadesc":t["desc"],
            "_yoast_wpseo_focuskw":t["kw"],
            "_yoast_wpseo_opengraph-title":t["seo"],
            "_yoast_wpseo_opengraph-description":t["desc"],
            "_yoast_wpseo_twitter-title":t["seo"],
            "_yoast_wpseo_twitter-description":t["desc"],
        }
        try:
            base.req("/update-post",{
                "id":t["id"],"expected_modified_gmt":reread["modified_gmt"],
                "content":updated,"title":t["title"],"meta":meta,
            })
        except Exception as ex:
            after_timeout=base.bridge_post(t["id"])
            if MARK+"-"+t["kind"] not in after_timeout.get("content",""):
                raise RuntimeError("Write unconfirmed; don't auto-retry "+t["slug"]) from ex
        after=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
        seo=pub.get("yoast_head_json") or {}
        if (after.get("slug"),after.get("status"),after.get("type"),int(after.get("featured_media") or 0))!=(
            t["slug"],"publish","post",t["cover"]):
            raise RuntimeError("Identity/featured changed after write: "+t["slug"])
        if after.get("title")!=t["title"] or seo.get("description")!=t["desc"]:
            raise RuntimeError("Title/Yoast description not saved: "+t["slug"])
        if after["content"].count('id="'+MARK+"-"+t["kind"]+'"')!=1:
            raise RuntimeError("Expected unique update marker not saved")
        if any(u not in after["content"] for u in t["links"]):
            raise RuntimeError("Actual internal links missing: "+t["slug"])
        if seo.get("canonical")!=before_public["yoast_head_json"]["canonical"]:
            raise RuntimeError("Canonical changed unexpectedly")
        if (seo.get("robots") or {}).get("index")=="noindex":
            raise RuntimeError("Indexed page turned noindex")
        old_og=(before_public["yoast_head_json"].get("og_image") or [{}])[0].get("url")
        new_og=(seo.get("og_image") or [{}])[0].get("url")
        if old_og!=new_og:
            raise RuntimeError("Featured OG image changed")
        print("BATCH03_LIVE_VERIFIED",t["id"],after["link"],"cover",t["cover"],"og",new_og,flush=True)
        time.sleep(2)
    print("A3TAL_BATCH03_THREE_HUMAN_ARTICLES_COMPLETE",flush=True)

if __name__=="__main__":
    main()
