# فحص قابلية الفهرسة لأعطال.كوم: 16 نوفمبر 2026

**النطاق:** مراجعة قراءة فقط خلال أزمة تحديث Google November 2026 Core Update. **لا تغيير في صفحات الموقع، أو Redirects، أو Yoast، أو ملفات Sitemap.**

## النتيجة

- **Google Search Console الفعلي:** تعذر استخراج تقرير Page Indexing لأن اتصال GSC Wizard رفض الوصول بانتهاء الاشتراك. **ليس لدينا رقم رسمي جديد لصفحات Google Indexed أو Crawled/Discovered not indexed**؛ لا يجوز استنتاجه من هذا التقرير.
- **فحص خريطة الموقع الحية:** 11 ملف XML، مجموع 1409 إدخالات، و1408 عناوين فريدة، لأن الرئيسية مذكورة مرتين في post/page sitemap. **صفر** روابط تحتوي Fragment/Query/KSA Path في الإدخالات.
- **زحف كامل سابق يوم 15 نوفمبر:** جميع 1408 عنوانًا استجابت 200، بلا noindex في السايت ماب ضمن نطاق ذلك الزحف. [سجل الفحص](https://github.com/marwanile1-cyber/a3tal/actions/runs/43701521420).
- **فحص تفصيلي حي:** عينة 154 صفحة كلها HTTP 200، Canonical صحيح، لا noindex أو تحويل. ثلاث صفحات سيارات (Deepal S09، Deepal G318، Jaecoo J5 موديل 2027) تفتقد وصف Meta؛ ليست مشكلة فهرسة حتمية. [سجل XML](https://github.com/marwanile1-cyber/a3tal/actions/runs/43773379575).
- **مراجعة الصفحات المهمة:** 32 عنوانًا من قائمة الأداء التاريخية يتحولون إلى **30 رابطًا نهائيًا مختلفًا**؛ كل العناوين النهائية والـCanonical تظهر داخل السايت ماب، بلا noindex أو أخطاء HTTP. وُجد تحويلان قائمان: Jetour T2 maintenance spare parts إلى maintenance schedule، وToyota Corolla spare parts maintenance إلى maintenance prices؛ مصدر كل تحويل **غير موجود** في السايت ماب (صحيح). [سجل مقارنة GSC priorities مع السايت ماب](https://github.com/marwanile1-cyber/a3tal/actions/runs/43774862180).

## ما لا يثبته الفحص

الفحص الخارجي يؤكد أن الصفحات **قابلة للزحف والفهرسة** تقنيًا، ولا يثبت أن Google **فهرستها فعليًا** أو أن ترتيبها لم يتراجع.

لا يثبت أن 0 صفحة من الموقع مستبعدة من Google Index، ولا أن هبوط نوفمبر سببه/ليس سببه تحديث جوجل، ولا يقدم تقارير Crawl Stats.

## القرار الآمن

1. لا نضيف 301 أو نغير السايت ماب أو نحذف صفحات بسبب الهبوط.
2. نحافظ على وقف النشر الجماعي أثناء تحديث Google.
3. نستخرج من Search Console: **Indexing > Pages > Export** مع أقسام Indexed وNot indexed ومبررات الاستبعاد، ثم نراجع أعلى 20 عنوانًا من الحالات **Crawled - currently not indexed** و**Discovered - currently not indexed** ومقارنة أعمارها وأهميتها وجودتها.
4. نراجع **Settings > Crawl stats** لرصد 5xx، تأخيرات DNS/Hosting، ومعدل استجابة Googlebot، مع مقارنة أيام 10–16 نوفمبر.
5. نصحح تكرار الرئيسية في خرائط XML وMeta Description للصفحات الثلاث بصورة منفصلة ومنخفضة الأولوية **بعد** انتهاء الحالة الحرجة، ومن دون تعديل URLs أو صورها.

## الأدلة

- [GitHub Action: زحف كل URLs](https://github.com/marwanile1-cyber/a3tal/actions/runs/43701521420)
- [GitHub Action: فحص ملف XML وعينة 154 صفحة](https://github.com/marwanile1-cyber/a3tal/actions/runs/43773379575)
- [GitHub Action: 32 رابطًا ذا أولوية، 30 هدفًا نهائيًا](https://github.com/marwanile1-cyber/a3tal/actions/runs/43774862180)
- [نص برنامج فحص العناوين](https://github.com/marwanile1-cyber/a3tal/blob/main/scripts/audit-a3tal-priority-indexability-readonly-20261116.py)
