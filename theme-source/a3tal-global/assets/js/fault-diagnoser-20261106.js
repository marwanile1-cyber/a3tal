/* A3tal fault triage v1: deterministic, human-reviewed rules, no API or personal data.
 * Source-backed safety rules outrank suspected causes and any price discussion.
 */
(function(){
"use strict";
const root=document.getElementById("a3fd-app"); if(!root)return;
const categories=[
 ["lights","لمبات العدادات","زيت، حرارة، محرك، بطارية، ABS"],
 ["sounds","أصوات","صوت خبط أو صرير أو احتكاك"],
 ["smells","روائح","بنزين، حريق، عادم"],
 ["leaks","تسريب سوائل","نقط أسفل السيارة أو الموتوسيكل"],
 ["vibrations","اهتزازات","رعشة أو هزة في القيادة"],
 ["power","التشغيل والأداء","عدم دوران أو ضعف سحب أو فصل"],
 ["climate","التكييف","ضعيف أو لا يبرد"]
];
const guides={
 dtc:["مكتبة أكواد DTC","https://a3tal.com/dtc/"],
 workshop:["دليل مراكز الخدمة","https://a3tal.com/service-centers/"],
 cost:["احسب عرض المصنعية وقطع الغيار","https://a3tal.com/car-tools/#maintenance-cost"],
 cooling:["تشخيص ارتفاع الحرارة في الزحمة","https://a3tal.com/car-overheats-in-traffic-cools-when-driving-fan-thermostat-diagnosis/"],
 battery:["فحص شحن أكسنت RB كمثال موديل محدد","https://a3tal.com/hyundai-accent-rb-battery-light-when-ac-on/"],
 drain:["فحص سحب البطارية لأسترا J كمثال","https://a3tal.com/opel-astra-j-battery-drains-overnight-diagnosis/"],
 abs:["لمبة ABS بعد صيانة البلي: إلنترا HD","https://a3tal.com/hyundai-elantra-hd-abs-light-after-wheel-bearing/"],
 brakes:["تكة أول فرملة بعد الرجوع: خطوات الفحص","https://a3tal.com/brake-clunk-first-stop-after-reversing-diagnosis/"],
 wander:["فحص العفشة عند عوم السيارة","https://a3tal.com/car-floating-wandering-highway-suspension-diagnosis/"],
 cold:["تشخيص النتشة على البارد","https://a3tal.com/car-hesitates-cold-start-fine-when-warm/"],
 ac:["ضعف تكييف صني N17 عند الوقوف","https://a3tal.com/nissan-sunny-n17-ac-weak-at-idle/"],
 motorbrake:["الموتوسيكل وفرامل العجلة الساخنة","https://a3tal.com/motorcycle-brakes-dragging-wheel-hot-caliper-diagnosis/"],
 motorsmoke:["دخان أزرق بالموتوسيكل وفقد الزيت","https://a3tal.com/motorcycle-blue-smoke-exhaust-oil-burning-diagnosis/"]
};
function q(title,opts){return {title,opts};}
function cause(name,check,tier,signals){return {name,check,tier,signals:signals||[]};}
function item(id,vehicle,category,title,detail,level,questions,causes,links,stops){
 return {id,vehicle,category,title,detail,level,questions,causes,links:links||["dtc"],stops:stops||[]};
}
const cases=[
 item("oil",["car","bike"],"lights","لمبة ضغط الزيت الحمراء مضيئة","أثناء تشغيل المحرك، لا مجرد إضاءة اختبار قبل التشغيل.","stop",
  [q("هل تستمر اللمبة والمحرك يعمل؟",["نعم","ظهرت لثوانٍ وقت تشغيل الكونتاكت فقط","مش متأكد"]),q("هل يوجد تسريب زيت أو خبط جديد؟",["نعم","لا","لم أتحقق"])],
  [cause("نقص زيت أو تسريب","بعد إيقاف المحرك بأمان، يفحص الفني المستوى والتسريبات وفق دليل المركبة.",0,["0:0","1:0"]),cause("حساس ضغط أو ضفيرة","قياس ضغط الزيت الفعلي أولًا قبل اتهام الحساس.",1,["0:1"]),cause("مشكلة فعلية في ضغط التزييت","فحص الضغط بمعدة مناسبة وفق مواصفات المحرك؛ لا تُعد التشغيل لاختبار الصوت.",2,["0:0","1:0"])],["dtc"],["0:0","0:2"]),
 item("temp",["car","bike"],"lights","مؤشر الحرارة في الأحمر أو بخار","ارتفاع الحرارة الشديد قد يتلف المحرك.","stop",
  [q("إمتى ارتفعت الحرارة؟",["في الوقوف والزحام","أثناء السير السريع","في كل الحالات"]),q("هل لاحظت نقص سائل أو بخارًا؟",["نعم","لا","مش متأكد"])],
  [cause("نقص سائل تبريد أو تسريب","الفحص بعد أن يبرد النظام؛ لا تفتح غطاء الردياتير وهو ساخن.",0,["1:0"]),cause("مروحة التبريد ودائرتها","يفحص الفني عمل المروحة والفيوز والريلاي والحساس بلا لمس أجزاء متحركة.",1,["0:0"]),cause("ثرموستات أو طرمبة مياه أو انسداد","اختبار دورة التبريد وضغطها بعد التوقف والبرودة.",2,["0:1","0:2"])],["cooling","dtc"]),
 item("check",["car","bike"],"lights","لمبة فحص المحرك (Check Engine)","اللمبة الصفراء ثابتة أم تومض؟","caution",
  [q("اللمبة شكلها إيه أثناء التشغيل؟",["ثابتة","بتومض/تقطع","مش متأكد"]),q("هل العربية بترعش أو قوتها قلت بوضوح؟",["نعم","لا","مش متأكد"])],
  [cause("غطاء الوقود أو تسريب بخار تبخير","راجع إحكام الغطاء فقط إذا لا توجد رائحة وقود أو تسريب.",0,["0:0","1:1"]),cause("مشكلة خليط/حساس/هواء","قراءة الأكواد والبيانات الحية قبل تغيير حساس.",1,["0:0"]),cause("اختلال احتراق أو إشعال","فحص الأعطال وأسباب فقد الاشتعال فورًا خاصة عند وميض اللمبة.",2,["0:1","1:0"])],["dtc"],["0:1"]),
 item("charge",["car","bike"],"lights","لمبة البطارية أثناء السير","قد يكون الشحن متوقفًا أو ضعيفًا.","urgent",
  [q("متى ظهرت اللمبة؟",["مع التكييف أو حمل كهربائي","من بداية الحركة","تظهر وتختفي"]),q("هل الأنوار ضعفت أو انطفأت أجهزة؟",["نعم","لا","مش متأكد"])],
  [cause("سير المجموعة أو توصيل/طرف بطارية","فحص بصري آمن بعد التوقف دون الاقتراب من سير أو مراوح.",0,["0:1","1:0"]),cause("ضعف شحن الدينامو أو منظّم الجهد","قياس الشحن والحمل في ورشة مختصة.",1,["0:0","1:0"]),cause("خلل بدائرة الشحن أو أرضي","اختبار هبوط الجهد والفيش حسب مخطط الموديل.",2,["0:2"])],["battery","dtc"]),
 item("abs",["car"],"lights","لمبة ABS الصفراء","قد يتوقف نظام منع الانغلاق بينما تبقى وظيفة الفرامل الأساسية حسب الحالة.","caution",
  [q("ظهرت اللمبة بعد صيانة عجلة أو بلي؟",["نعم","لا","مش متأكد"]),q("هل الفرامل غير طبيعية أو لمبة فرامل حمراء معها؟",["نعم","لا","مش متأكد"])],
  [cause("فيشة أو حساس سرعة عجلة","قراءة كود العجلة وفحص التوصيلات القريبة من الإصلاح.",0,["0:0"]),cause("حلقة قراءة سرعة أو بلي غير مطابق","مقارنة سرعة العجلات في البيانات الحية وفحص القطعة.",1,["0:0"]),cause("خلل دائرة ABS أو تغذية","فحص الفيوز والوحدة بعد قراءة كود ABS المتخصص.",2,["0:1"])],["abs","dtc"],["1:0"]),
 item("brake",["car","bike"],"lights","لمبة الفرامل الحمراء أو ضعف الدواسة","نظام الفرامل من معدات السلامة المباشرة.","stop",
  [q("هل الدواسة/الذراع غير طبيعي أو الفرامل ضعيفة؟",["نعم","لا","مش متأكد"]),q("هل يوجد سائل فرامل متسرب أو مستوى منخفض؟",["نعم","لا","مش متأكد"])],
  [cause("فرامل اليد/مفتاح تنبيه","قد تكون الإشارة بسيطة لكن لا يُعتمد على ذلك قبل التأكد من سلامة الفرامل.",0,["0:1","1:1"]),cause("مستوى سائل/تسريب/تيل","فحص الفرامل دون قيادة تجريبية عند ضعفها.",1,["1:0"]),cause("دائرة هيدروليكية/ماستر/كاليبر","فحص احترافي قبل إعادة السيارة للطريق.",2,["0:0"])],["brakes","motorbrake"]),
 item("knock",["car","bike"],"sounds","خبط معدني من المحرك","صوت متزامن مع دوران المحرك يحتاج تقييمًا جادًا.","urgent",
  [q("الصوت شديد ويزيد مع الدعس؟",["نعم","خفيف ومتقطع","مش متأكد"]),q("هل لمبة الزيت أو الحرارة ظهرت؟",["نعم","لا","مش متأكد"])],
  [cause("صفيحة أو ملحق خارجي مرتخٍ","تمييز مصدر الصوت بالفحص في الورشة بدون الاقتراب من أجزاء دوارة.",0,["0:1"]),cause("توقيت احتراق/زيت غير مناسب","مراجعة البيانات والضغط والزيت قبل تغيير أجزاء.",1,["0:1"]),cause("تلف ميكانيكي داخلي","اختبار ضغط/زيت وتشخيص متخصص؛ لا تشغّل المحرك عند خبط قوي.",2,["0:0","1:0"])],["dtc"],["0:0","1:0"]),
 item("brakenoise",["car","bike"],"sounds","صرير أو احتكاك عند الفرملة","فرق مهم بين صرير متقطع واحتكاك معدني مستمر.","caution",
  [q("نوع الصوت؟",["احتكاك معدني مستمر","صرير قصير وقت الفرملة","تكة واحدة بعد تغيير اتجاه السير"]),q("هل قوة الفرملة قلت أو المركبة بتحدف؟",["نعم","لا","مش متأكد"])],
  [cause("أتربة/سطح التيل","تفتيش بصري لعناصر الفرامل قبل شراء قطع.",0,["0:1"]),cause("تيل أو كلبسات تثبيت أو كاليبر","فحص سمك التيل والمشابك والدلايل.",1,["0:2"]),cause("احتكاك معدن أو تلف بالطنابير","إيقاف الاستخدام وفحص فوري إذا الصوت مستمر.",2,["0:0","1:0"])],["brakes","motorbrake"],["0:0","1:0"]),
 item("clunk",["car"],"sounds","طقة من ناحية العفشة أو العجل","الصوت عند المطبات أو الفرملة أو تغيير الاتجاه.","caution",
  [q("بتسمع الطقة إمتى؟",["مع المطبات","أول فرملة بعد الرجوع","مع لف الدركسيون"]),q("هل الدركسيون غير مستقر أو فيه عوم واضح؟",["نعم","لا","مش متأكد"])],
  [cause("تيش ميزان أو كلبسات التيل","اختيار الفحص حسب توقيت الصوت، وليس تغيـير القطع عشوائيًا.",0,["0:0","0:1"]),cause("جلب مقص/مفاصل/بطاحات","فحص الخلوص في ورشة مؤهلة.",1,["0:0","1:0"]),cause("كوبلن أو مشكلة توجيه","فحص الدركسيون والمفاصل خاصة لو الصوت مع اللف.",2,["0:2","1:0"])],["brakes","wander"],["1:0"]),
 item("fuel",["car","bike"],"smells","رائحة بنزين قوية أو وقود متسرب","احتمال اشتعال لا يُختبر بتشغيل المحرك.","stop",
  [q("هل الرائحة قوية أو تشاهد بقعة وقود؟",["نعم","خفيفة ومتقطعة","مش متأكد"]),q("هل الرائحة قرب المحرك أو الخزان؟",["قرب المحرك","قرب الخزان","مش متأكد"])],
  [cause("غطاء خزان أو وصلة بخار","يفحص الفني الإحكام بعيدًا عن مصادر الاشتعال.",0,["1:1"]),cause("خرطوم أو وصلة وقود","تحديد موضع التسريب دون تشغيل أو شرر.",1,["0:0"]),cause("مضخة/حاقن/خط ضغط","فحص ضغط الوقود في ورشة مجهزة بعد تأمين المركبة.",2,["1:0"])],["workshop"]),
 item("burn",["car","bike"],"smells","رائحة حريق أو بلاستيك/كهرباء","قد تشير لسخونة أسلاك أو أجزاء فرامل.","stop",
  [q("هل هناك دخان أو شرر؟",["نعم","لا","مش متأكد"]),q("هل تظهر الرائحة مع تشغيل الكهرباء أو الفرملة؟",["كهرباء","فرملة","مش متأكد"])],
  [cause("سلك/فيشة أو فيوز يسخن","فحص دائرة الكهرباء بعد فصل التشغيل بأمان، لا لمس الأسلاك الساخنة.",1,["1:0"]),cause("فرامل قافشة أو تيل ساخن","فحص حرارة الكاليبر ومكابس الفرامل بعد أن تبرد.",1,["1:1"]),cause("تسريب على أجزاء ساخنة","كشف المصدر في الورشة بعيدًا عن لهب أو شرر.",2,["0:0"])],["motorbrake","workshop"]),
 item("exhaust",["car"],"smells","رائحة عادم داخل الصالون","العادم قد يحتوي أول أكسيد الكربون السام.","stop",
  [q("هل الرائحة داخل المقصورة أثناء تشغيل المحرك؟",["نعم","عند فتح الشنطة فقط","مش متأكد"]),q("هل يوجد صداع أو دوخة عند الركوب؟",["نعم","لا","مش متأكد"])],
  [cause("تسريب ماسورة/جوان عادم","فحص عادم كامل وعدم تشغيل المحرك في مكان مغلق.",1,["0:0"]),cause("عزل الشنطة أو تهوية المقصورة","فحص مسار دخول العادم للصالون.",1,["0:1"]),cause("تسريب بمجمع العادم","فحص احترافي بعد إيقاف المركبة وتهوية الركاب.",2,["1:0"])],["workshop"]),
 item("leak",["car","bike"],"leaks","بقع أو سوائل تحت المركبة","نوع السائل ومكانه يغيّران مستوى الخطر.","caution",
  [q("تعتقد السائل إيه؟",["بنزين أو سائل فرامل","زيت أو سائل ملون","مياه شفافة بعد التكييف"]),q("هل الكمية كبيرة أو المستوى بينقص؟",["نعم","لا","مش متأكد"])],
  [cause("مياه تكثيف التكييف","لو مياه شفافة بعد التكييف وبدون مؤشرات أخرى، قد تكون طبيعية.",0,["0:2"]),cause("جلدة/خرطوم أو تسريب دورة","تحديد نوع السائل قبل فك أي قطعة.",1,["0:1"]),cause("تسريب وقود/فرامل خطير","إيقاف المركبة فورًا إذا كان السائل وقودًا أو فرامل.",2,["0:0","1:0"])],["cooling","workshop"],["0:0"]),
 item("steer",["car"],"vibrations","رعشة في الدركسيون أثناء السير","قد تكون مرتبطة بسرعة معينة أو فرملة.","caution",
  [q("الرعشة بتحصل إمتى؟",["على سرعة محددة","أثناء الفرملة","طول الوقت"]),q("هل في فقد تحكم أو العربية بتحدف بشدة؟",["نعم","لا","مش متأكد"])],
  [cause("ضغط إطارات أو ترصيص/اعوجاج جنط","فحص الإطار والجنط والترصيص أولًا.",0,["0:0"]),cause("طنابير/فرامل","فحص هبوط قوة الفرامل والطنابير عند ظهورها مع الفرملة.",1,["0:1"]),cause("مفاصل توجيه أو عفشة","مراجعة خلوص المقصات والبيضة والوصلة.",2,["0:2","1:0"])],["wander","brakes"],["1:0"]),
 item("idle",["car","bike"],"vibrations","اهتزاز أو نتشة والمحرك واقف","الاهتزاز قد يأتي من احتراق غير منتظم أو قواعد المحرك.","caution",
  [q("الرعشة بتحصل إمتى؟",["على البارد فقط","بعد السخونة","باستمرار"]),q("هل لمبة المحرك بتومض أو فيه تقطيع شديد؟",["نعم","لا","مش متأكد"])],
  [cause("فلتر هواء/اتساخ خانق","فحص مجرى الهواء وبيانات الحساسات، لا تنظيفًا عشوائيًا.",0,["0:0"]),cause("بوجيه/موبينة أو خليط وقود","قراءة أكواد فقد الاشتعال إن وجدت قبل شراء قطعة.",1,["1:0"]),cause("قاعدة محرك أو مشكلة ميكانيكية","فحص القواعد والضغط إذا اهتزاز مستمر.",2,["0:2"])],["cold","dtc"],["1:0"]),
 item("nostart",["car","bike"],"power","المحرك لا يدور أو لا يشتغل","فرّق بين عدم دوران المارش وبين الدوران دون تشغيل.","caution",
  [q("عند محاولة التشغيل، إيه اللي بيحصل؟",["المارش لا يدور","المارش يدور لكن المحرك لا يشتغل","بيشتغل ويفصل"]),q("هل الأنوار ضعيفة أو البطارية فضيت؟",["نعم","لا","مش متأكد"])],
  [cause("بطارية/أطراف/أرضي","فحص الجهد والتوصيلات بواسطة فني، دون توصيل عشوائي.",0,["0:0","1:0"]),cause("فيوز/ريلاي/مارش أو إشارة تشغيل","فحص دائرة الأمر وفق موديل المركبة.",1,["0:0"]),cause("وقود/شرارة/حساس توقيت","تشخيص عند دوران المحرك بدون اشتعال، مع قراءة الأكواد.",2,["0:1","0:2"])],["drain","dtc"]),
 item("weak",["car","bike"],"power","ضعف سحب أو فقد قوة مفاجئ","الأسباب تتراوح بين مدخل الهواء وإدارة المحرك وأنظمة الأمان.","caution",
  [q("الضعف ظهر إزاي؟",["تدريجي","مفاجئ مع رعشة","بعد صيانة"]),q("هل لمبة المحرك بتومض أو في سخونة؟",["نعم","لا","مش متأكد"])],
  [cause("فلتر هواء أو مشكلة وقود بسيطة","مراجعة الفلاتر وجدول الصيانة أولًا إذا لا توجد علامة خطر.",0,["0:0"]),cause("حساس/ضغط وقود/شحن تيربو","قراءة بيانات حساسات وضغط/هواء مناسب لنوع المحرك.",1,["0:2"]),cause("فقد اشتعال أو مشكلة فتيس/محرك","فحص عاجل عند رعشة شديدة أو تحذير وامض.",2,["0:1","1:0"])],["cold","dtc"],["1:0"]),
 item("ac",["car"],"climate","التكييف ضعيف أو مش بيبرد","الأسباب تختلف إذا كان الضعف في الوقوف فقط أو طوال الوقت.","caution",
  [q("الهواء مش بارد إمتى؟",["في الزحمة والوقوف","طول الوقت","التبريد ضعيف مع سرعات المروحة"]),q("هل مؤشر حرارة المحرك يرتفع أيضًا؟",["نعم","لا","مش متأكد"])],
  [cause("فلتر تكييف/اتساخ مكثف أو عائق هواء","فحص تدفق الهواء والتنظيف الآمن قبل إضافة فريون.",0,["0:2"]),cause("مراوح مكثف أو دائرة تشغيل","مراجعة دورة المراوح وضغط التشغيل لدى فني تكييف.",1,["0:0","1:0"]),cause("تسريب غاز/كومبروسر أو حساس","اختبار الضغط والتسريب، لا تعبئة غاز دون كشف السبب.",2,["0:1"])],["ac","cooling"],["1:0"]),
 item("bikestall",["bike"],"power","الموتوسيكل بيفصل بعد ما يسخن","إذا بيفصل أثناء السير فالموقف قد يعرّض السائق للخطر.","urgent",
  [q("هل يفصل وهو ماشي ويرجع يشتغل بعد ما يبرد؟",["نعم","بيفصل وهو واقف فقط","مش متأكد"]),q("هل فيه لمبة تحذير أو دخان أو حرارة زائدة؟",["نعم","لا","مش متأكد"])],
  [cause("فيشة/حساس حراري أو مشكلة كهرباء","فحص الإشارات والتوصيلات عند الحرارة التشغيلية في ورشة.",0,["0:0"]),cause("تغذية وقود أو تهوية الخزان","فحص مضخة/كربراتير أو حقن حسب الموديل.",1,["0:1"]),cause("إشعال/فقد ضغط/سخونة محرك","فحص نظام الإشعال والتبريد والضغط قبل التغيير.",2,["1:0"])],["motorsmoke","dtc"],["1:0"]),
 item("bikebrake",["bike"],"sounds","عجلة الموتوسيكل قافشة أو الفرامل سخنة","انحشار الفرامل قد يسبب فقد السيطرة.","stop",
  [q("هل العجلة بتمسك أو الفرامل مش بترجع؟",["نعم","صرير بدون قفشة واضحة","مش متأكد"]),q("هل في ريحة حريق أو دخان من العجلة؟",["نعم","لا","مش متأكد"])],
  [cause("سلك/ذراع فرامل أو رجوع غير سليم","فحص ضبط الفرامل بعد أن تبرد تمامًا.",0,["0:1"]),cause("تيل/كاليبر أو بستم عالق","فحص ميكانيكي وهيدروليكي، لا لمس كاليبر ساخن.",1,["0:0"]),cause("ماستر/خرطوم يحتفظ بالضغط","اختبار متخصص قبل إعادة الموتوسيكل للطريق.",2,["1:0"])],["motorbrake"])
];
const danger=[
 ["none","لا، مفيش علامة خطيرة واضحة"],
 ["oil","لمبة زيت حمراء أو سخونة شديدة/بخار"],
 ["brakes","فرامل ضعيفة جدًا أو فقد السيطرة"],
 ["fuel","تسريب بنزين أو رائحة وقود شديدة أو دخان/شرر"],
 ["unsure","مش متأكد من سلامة المركبة"]
];
const catEl=root.querySelector("#a3fd-cats");
const caseEl=root.querySelector("#a3fd-symptoms");
const questionEl=root.querySelector("#a3fd-questions");
const reportEl=root.querySelector("#a3fd-report");
const noticeEl=root.querySelector("#a3fd-notice");
const vehicleEl=root.querySelector("#a3fd-vehicles");
const dangerEl=root.querySelector("#a3fd-danger");
const modelEl=root.querySelector("#a3fd-model");
const yearEl=root.querySelector("#a3fd-year");
const state={vehicle:"car",cat:"lights",id:null,answers:[],danger:"none"};
const make=(tag,className,text)=>{const e=document.createElement(tag);if(className)e.className=className;if(text!==undefined)e.textContent=text;return e;};
function addLink(parent,key){
 const entry=guides[key];if(!entry)return;
 const a=make("a","a3fd-link",entry[0]);a.href=entry[1];a.rel="noopener";parent.append(a);
}
function choiceButton(text,active,fn){
 const b=make("button","a3fd-choice"+(active?" is-selected":""),text);
 b.type="button";b.setAttribute("aria-pressed",active?"true":"false");b.addEventListener("click",fn);return b;
}
function getCase(){return cases.find(c=>c.id===state.id)||null;}
function emergency(){return state.danger!=="none"&&state.danger!=="unsure";}
function stopReason(c){
 if(emergency())return true;
 if(!c)return false;
 if(c.level==="stop")return true;
 return c.stops.some(s=>{const [idx,opt]=s.split(":").map(Number);return state.answers[idx]===opt;});
}
function renderVehicle(){
 vehicleEl.replaceChildren();
 [["car","سيارة"],["bike","موتوسيكل أو سكوتر"]].forEach(([id,label])=>{
  vehicleEl.append(choiceButton(label,state.vehicle===id,()=>{
   state.vehicle=id;state.cat="lights";state.id=null;state.answers=[];reportEl.hidden=true;
   renderAll();
  }));
 });
}
function renderCats(){
 catEl.replaceChildren();
 categories.filter(c=>cases.some(s=>s.category===c[0]&&s.vehicle.includes(state.vehicle))).forEach(c=>{
  const btn=choiceButton(c[1],state.cat===c[0],()=>{
    state.cat=c[0];state.id=null;state.answers=[];reportEl.hidden=true;
    renderCats();renderCases();renderQuestions();renderSafety();
  });
  btn.classList.add("a3fd-cat");
  const small=make("small","",c[2]);btn.append(small);catEl.append(btn);
 });
}
function renderCases(){
 caseEl.replaceChildren();
 const available=cases.filter(c=>c.vehicle.includes(state.vehicle)&&c.category===state.cat);
 available.forEach(c=>{
  caseEl.append(choiceButton(c.title,state.id===c.id,()=>{
   state.id=c.id;state.answers=[];reportEl.hidden=true;renderCases();renderQuestions();renderSafety();
   questionEl.scrollIntoView({behavior:"smooth",block:"nearest"});
  }));
 });
}
function renderSafety(){
 const c=getCase();const immediate=stopReason(c);
 noticeEl.className="a3fd-notice"+(immediate?" a3fd-alert":"");
 noticeEl.replaceChildren();
 noticeEl.append(make("strong","",immediate?"أولوية سلامة: توقف بأمان":"قبل التشخيص: راقب علامات الخطر"));
 noticeEl.append(make("p","",immediate?
  "أوقف المركبة في مكان آمن، وأطفئ المحرك عند وجود حرارة شديدة أو لمبة ضغط زيت حمراء أو تسريب وقود. لا تواصل القيادة أو تُجرّب التشغيل لتأكيد العطل. عند وجود دخان أو حريق ابتعد واتصل بالطوارئ أو المساعدة المختصة.":
  "لو ظهرت لمبة ضغط زيت حمراء أثناء تشغيل المحرك، أو سخونة شديدة، أو ضعف فرامل، أو تسريب وقود، تعامل معها كحالة توقف حتى لو اخترت عَرَضًا آخر."));
}
function renderQuestions(){
 questionEl.replaceChildren();
 const c=getCase();
 if(!c){questionEl.append(make("p","a3fd-muted","اختَر العَرَض من فوق عشان تظهر أسئلة تضيق الاحتمالات."));return;}
 questionEl.append(make("h3","",c.title));
 questionEl.append(make("p","a3fd-muted",c.detail));
 c.questions.forEach((question,i)=>{
  const field=make("fieldset","a3fd-field");
  const legend=make("legend","",String(i+1)+". "+question.title);field.append(legend);
  question.opts.forEach((option,idx)=>{
   const label=make("label","a3fd-option"+(state.answers[i]===idx?" is-chosen":""));
   const input=make("input");input.type="radio";input.name="a3fd-q"+i;input.value=idx;
   input.checked=state.answers[i]===idx;
   input.addEventListener("change",()=>{
    state.answers[i]=idx;reportEl.hidden=true;renderQuestions();renderSafety();
    if(state.answers.every(a=>Number.isInteger(a))&&state.answers.length===c.questions.length){
      const btn=questionEl.querySelector("#a3fd-show");
      if(btn)btn.focus({preventScroll:true});
    }
   });
   label.append(input,make("span","",option));field.append(label);
  });
  questionEl.append(field);
 });
 const btn=make("button","a3fd-main-button","اعرض خطوات الفحص");
 btn.id="a3fd-show";btn.type="button";btn.disabled=!state.answers.every(a=>Number.isInteger(a))||state.answers.length!==c.questions.length;
 btn.addEventListener("click",showReport);questionEl.append(btn);
}
function ranked(c){
 return c.causes.map((cause,index)=>{
  let score=0;cause.signals.forEach(s=>{const [i,a]=s.split(":").map(Number);if(state.answers[i]===a)score+=3;});
  return {...cause,score,index};
 }).sort((a,b)=>b.score-a.score||a.tier-b.tier||a.index-b.index);
}
function showReport(){
 const c=getCase();if(!c||state.answers.length!==c.questions.length)return;
 const dangerStop=stopReason(c);
 const urgency=dangerStop?"stop":state.danger==="unsure"||c.level==="urgent"?"urgent":"caution";
 reportEl.hidden=false;reportEl.replaceChildren();
 const card=make("div","a3fd-result-card");
 const badge=make("span","a3fd-risk a3fd-risk-"+urgency,
  urgency==="stop"?"توقف بأمان ولا تواصل القيادة":urgency==="urgent"?"تجنب القيادة لحين التقييم":"يحتاج فحصًا قريبًا؛ لا يمكن ضمان أمان القيادة");
 card.append(badge);
 card.append(make("h2","",c.title));
 const model=modelEl.value.trim().slice(0,70),year=yearEl.value.trim().slice(0,4);
 const context=make("p","a3fd-muted","نوع المركبة: "+(state.vehicle==="car"?"سيارة":"موتوسيكل/سكوتر")+
 (model?" | الموديل المكتوب: "+model:"")+(year?" | السنة: "+year:""));
 card.append(context);
 if(dangerStop){
  card.append(make("p","a3fd-critical","الإجراء الأول: اختر مكانًا آمنًا للتوقف وأبعد الركاب عن الخطر. لا تستكمل القيادة أو تفك أجزاء ساخنة/مضغوطة. اطلب نقل المركبة أو فحصًا مناسبًا. إذا كان هناك حريق، ابتعد واتصل بالطوارئ."));
 }else if(urgency==="urgent"){
  card.append(make("p","a3fd-critical","الإجراء الأول: لا تعتمد على اختبار قيادة لتأكيد المشكلة. توجّه للفحص بطريقة آمنة، واطلب مساعدة أو نقلًا إذا ظهرت علامات خطر أو تعذر التحكم."));
 }else{
  card.append(make("p","a3fd-muted","دي خطوة فرز أولية وليست تصريحًا بالقيادة. إذا زادت الأعراض أو ظهرت علامة خطر، توقف في مكان آمن."));
 }
 card.append(make("h3","","ترتيب الفحوصات المقترحة حسب إجاباتك"));
 card.append(make("p","a3fd-muted","هذه احتمالات للفحص، مش نسب تشخيص ولا حكم على قطعة تالفة. الخطورة مقدمة دائمًا على توفير التكلفة."));
 const list=make("ol","a3fd-causes");
 ranked(c).forEach(item=>{
  const li=make("li","");li.append(make("strong","",item.name));li.append(make("p","",item.check));
  li.append(make("small","",["فحص مبدئي","فحص متوسط","فحص متخصص"][item.tier]));
  list.append(li);
 });
 card.append(list);
 const cost=make("section","a3fd-cost");
 cost.append(make("h3","","تكلفة الإصلاح في مصر"));
 cost.append(make("p","","مافيش مدى سعري مؤكد للحالة دي قبل تحديد الموديل والقطعة ونتيجة الفحص. احصل على عرض مكتوب يفصل سعر القطعة عن المصنعية والضريبة وتاريخ التسعير، وبعدها استخدم حاسبة التكلفة. مش هنخترع أرقام لمجرد ملء المربع."));
 addLink(cost,"cost");card.append(cost);
 const qlist=make("section","a3fd-qa");
 qlist.append(make("h3","","ملخص تعطيه للفني"));
 const summary=[c.title].concat(c.questions.map((x,i)=>x.title+" "+x.opts[state.answers[i]]));
 summary.forEach(line=>qlist.append(make("p","",line)));
 card.append(qlist);
 const refs=make("section","a3fd-related");refs.append(make("h3","","أدلة فنية مرتبطة"));
 const wrap=make("div","a3fd-links");
 [...new Set(c.links.concat(["workshop"]))].forEach(key=>addLink(wrap,key));
 refs.append(wrap);
 refs.append(make("p","a3fd-muted","روابط بعض الموديلات أمثلة تشخيصية فقط، ولا تعني تطابق قطعها أو مواصفاتها مع مركبتك."));
 card.append(refs);
 const btns=make("div","a3fd-actions");
 const copy=make("button","a3fd-secondary","انسخ ملخص الحالة للفني");copy.type="button";
 copy.addEventListener("click",async()=>{
  const text=[c.title,context.textContent,urgency==="stop"?"توقف ولا تواصل القيادة":"يحتاج فحصًا",...summary.slice(1),...ranked(c).map(x=>x.name+" : "+x.check)].join("\n");
  try{await navigator.clipboard.writeText(text);copy.textContent="تم نسخ الملخص";}catch(e){copy.textContent="النسخ غير متاح في المتصفح؛ استخدم تحديد النص";}
 });
 const reset=make("button","a3fd-secondary","ابدأ تشخيص عَرَض آخر");reset.type="button";reset.addEventListener("click",()=>{
   state.id=null;state.answers=[];reportEl.hidden=true;renderCases();renderQuestions();renderSafety();root.scrollIntoView({behavior:"smooth"});
 });
 btns.append(copy,reset);card.append(btns);reportEl.append(card);
 reportEl.scrollIntoView({behavior:"smooth",block:"start"});
 root.dataset.lastRisk=urgency;
}
function renderDanger(){
 dangerEl.replaceChildren();
 danger.forEach(([id,label])=>{
  const el=make("label","a3fd-danger-option");
  const input=make("input");input.type="radio";input.name="a3fd-emergency";
  input.value=id;input.checked=state.danger===id;
  input.addEventListener("change",()=>{
    state.danger=id;reportEl.hidden=true;renderSafety();renderDanger();
    const c=getCase();
    if(c&&state.answers.length===c.questions.length&&state.answers.every(Number.isInteger))showReport();
  });
  el.append(input,make("span","",label));dangerEl.append(el);
 });
}
function renderAll(){renderVehicle();renderCats();renderCases();renderQuestions();renderDanger();renderSafety();}
renderAll();root.dataset.ready="1";root.dataset.scenarioCount=String(cases.length);
})();
