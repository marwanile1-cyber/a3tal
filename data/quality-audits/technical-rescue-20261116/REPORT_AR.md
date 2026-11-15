# تقرير الاستمرار في إنقاذ أعطال.كوم - 16 نوفمبر 2026

**النطاق:** تشخيص فني أثناء Google November 2026 Core Update، وتطبيق إصلاحين محدودين فقط على روابط داخلية مؤكدة العطل. لا تعديل جماعي للمحتوى ولا تغيير Slugs أو Redirects أو Sitemap أو فهرسة.

## 1. حالة Google Search Console

- تعذر الحصول على تقارير **Google Page Indexing** و**Googlebot Crawl Stats** من API المتصل: GSC Wizard يرفض الاستدعاءات لانتهاء الاشتراك، وWindsor.ai لا يتضمن خاصية a3tal.com.
- لا يجوز اختلاق عدد الصفحات المفهرسة أو أخطاء زحف Googlebot. نتائج الفحص الخارجي لا تعوض تقارير جوجل الأصلية.

## 2. ما أثبته الزحف

- **فحص كامل سابق 15 نوفمبر:** 11 ملف Sitemap، **1408 URL فريد**، HTTP 200 لجميع الروابط ضمن الفحص، ولا صفحات noindex داخل XML. توجد حالة تكرار وحيدة للرئيسية بين خريطتي post وpage. [السجل](https://github.com/marwanile1-cyber/a3tal/actions/runs/43701521420).
- **فحص أهم الصفحات:** 32 URL تاريخيًا تؤدي إلى 30 عنوانًا نهائيًا مختلفًا؛ الـ30 موجودة في Sitemap، بلا اختلاف Canonical أو noindex. رابطا مصدر Jetour T2 وToyota Corolla المحولان **غير موجودين في Sitemap**، كما ينبغي. [السجل](https://github.com/marwanile1-cyber/a3tal/actions/runs/43774862180).
- **الروابط خارج XML:** عُثر على 80 هدفًا من زحف الموقع (بعد استبعاد CDN/WP pagination وما شابه اختُبر **78 URL**)؛ الاستجابات **76 HTTP 200 + 2 HTTP 404**. من الـ78، **41 noindex**: 26 صفحة /cars/ مساعدة، و6 /dtc/ مساعدة، و9 أخرى (تتضمن صفحتي 404). **لا يُفترض أن noindex خطأ في الصفحات المستبعدة عمدًا**. [السجل](https://github.com/marwanile1-cyber/a3tal/actions/runs/43775359346).
- في الزحف السابق 128 عنوانًا لم يكن لديها **روابط واردة من متن/المحتوى الرئيسي ضمن نطاق فحص الأداة** (منها 24 تصنيفًا)، و458 عنوانًا بروابط واردة ضعيفة حسب معيار الأداة؛ لا يعني ذلك غياب جميع أنواع الروابط أو إثبات عقوبة Google.

## 3. إصلاحات تمت على الموقع بنجاح: روابط 404 فقط

| المصدر | الرابط الخاطئ | الرابط الصحيح | النتيجة |
|---|---|---|---|
| [بطارية السيارة مع حر السعودية](https://a3tal.com/car-battery-heat-saudi-summer-voltage-test-before-replace/) | /car-battery-drains-when-parked-diagnosis/ | [تشخيص تفريغ البطارية بالملتيميتر](https://a3tal.com/car-battery-parasitic-draw-diagnosis/) | تم استبدال href واحد والتحقق من بقاء الصورة والـSEO |
| [سير المجموعة أم سير الكاتينة](https://a3tal.com/serpentine-belt-squealing-vs-timing-belt-replacement/) | /صيانة-دورية-للسيارة/ | [دليل جداول صيانة السيارات](https://a3tal.com/maintenance-schedules/) | تم استبدال href واحد والتحقق من بقاء الصورة والـSEO |

- نفذ الإصلاح عبر **GitHub + A3tal Direct Bridge** في المقالين المنشورين فقط (Post IDs: 86139 و86155).
- تم التحقق من حفظ المحتوى النهائي وعدم تغيير العنوان، الصورة البارزة، SEO title/description، Canonical أو og:image.
- لا تحويل 301 جديد، لا تعديل في مواد التشخيص أو الأسعار أو نصوص العناوين.
- [سجل الإصلاح والتحقق الناجح](https://github.com/marwanile1-cyber/a3tal/actions/runs/43775816646).

## 4. قياس استجابة السيرفر وسرعة الهاتف (GitHub Actions، 16 نوفمبر)

- تم اختبار `/`، `/cars/`، `/dtc/` ثلاث مرات لكل مسار من GitHub runner؛ كل الاستجابات **HTTP 200** مع LiteSpeed cache hit. في القياسات التسع بلغ TTFB نحو **0.14-0.53 ثانية**. هذه اختبارات نقطة واحدة، **ليست** Googlebot Crawl Stats أو ضمان عدم وجود 5xx على مدار اليوم.
- **Lighthouse موبايل، اختباران متتاليان:** Performance **75/100 ثم 76/100**، و**LCP = 5.8 ثانية** في الاختبارين، وFCP 2.6 ثم 2.3 ثانية، وTBT 0ms، وCLS 0.
- عنصر LCP هو **صورة الهيرو للموبايل** `img.hero-mobile-scene`، وهي مجهزة بـ `loading="eager"` و`fetchpriority="high"`. التقرير يشير إلى **تأخير كبير بين وصول الصورة ورسمها** في أحد تحليلات Lighthouse. ينبغي إعادة التحقق في ظروف ثابتة من الـCSS والتحميل والرسم؛ لا نفترض أن حجم الصورة وحده السبب.
- **هذا اختبار Lighthouse معملي**، وليس حقل Core Web Vitals/CrUX الحقيقي. لا يصح الادعاء أنه دليل مباشر على سقوط ترتيب Google أو أن التغيير الأخير تسبب به.
- راجع [Lighthouse + HTTP timing run](https://github.com/marwanile1-cyber/a3tal/actions/runs/43775977790).

## 5. ترتيب القرارات

1. **تم:** إصلاح الرابطين المعطوبين.
2. **أولوية تقنية تالية:** تحليل سبب LCP المرتفع في الصفحة الرئيسية وتجربة مستقلة لعزل أثر CSS الخاص بالـmobile hero و`decoding="async"` في نسخة اختبار، قبل أي تعديل حي أو purge كاش.
3. **فحص تحريري لاحق:** استكمال قائمة 128 صفحة قليلة الروابط الواردة واختيار الصفحات ذات قيمة البحث الحقيقية فقط، مع عدم تنفيذ ربط جماعي.
4. **عند توفر GSC:** اطلب تصدير **Indexing > Pages** و`Settings > Crawl stats` لتأكيد أسباب الاستبعاد واستجابة Googlebot، ثم قارن أداء Pages وQueries في فترات متساوية بعد استقرار التحديث.
5. **المؤجل:** 301 جماعي، تعديل Meta لـ50 صفحة، دمج Cannibalization بلا استعلامات، تفعيل Product/FAQ schema بدون تحقق أهلية.

## مصادر الإثبات
- [تقرير Sitemap](https://github.com/marwanile1-cyber/a3tal/actions/runs/43773379575)
- [زحف SEO شامل](https://github.com/marwanile1-cyber/a3tal/actions/runs/43701521420)
- [خارج Sitemap و404](https://github.com/marwanile1-cyber/a3tal/actions/runs/43775359346)
- [إصلاح رابطين](https://github.com/marwanile1-cyber/a3tal/actions/runs/43775816646)
- [Lighthouse موبایل](https://github.com/marwanile1-cyber/a3tal/actions/runs/43775977790)
