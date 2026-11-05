<?php
/**
 * Template: smart, source-aware fault triage (not an AI medical-style certainty engine).
 * Dedicated URL /fault-diagnosis/; anonymous inputs remain client-side only.
 * Original diagnostic articles retain their independent intent and canonical URLs.
 */
defined('ABSPATH') || exit;
get_header();
$fd_css = get_template_directory().'/fault-diagnoser-20261106.css';
?>
<?php if (is_readable($fd_css)): ?><style id="a3fd-inline-style"><?php readfile($fd_css); ?></style><?php endif; ?>
<main id="a3fd" dir="rtl">
  <div class="a3fd-wrap">
    <nav class="a3fd-crumb" aria-label="مسار التصفح"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a> / مشخّص الأعطال الذكي</nav>
    <header class="a3fd-hero">
      <span class="a3fd-kicker">A3TAL DIAGNOSTICS / نسخة فنية تفاعلية</span>
      <h1>مشخّص الأعطال الذكي للسيارات والموتوسيكلات</h1>
      <p>بدل ما تغيّر قطع غيار بالتجربة: اختَر العَرَض، جاوب على أسئلة بسيطة، واعرف مستوى الخطورة وترتيب الفحوصات المطلوبة قبل زيارة الورشة. النتيجة استرشادية وليست تشخيصًا نهائيًا.</p>
      <div class="a3fd-chips"><span>20 عَرَضًا مبدئيًا</span><span>سلامتك أولًا</span><span>بدون تسجيل</span><span>بدون تخمين أسعار</span></div>
    </header>
    <div id="a3fd-app" class="a3fd-layout">
      <section class="a3fd-workspace" aria-label="أداة فرز الأعطال التفاعلية">
        <section class="a3fd-block" aria-labelledby="a3fd-vehicle-title">
          <h2 id="a3fd-vehicle-title" class="a3fd-title"><span class="a3fd-number">1</span>نوع المركبة</h2>
          <div id="a3fd-vehicles" class="a3fd-choices" role="group" aria-label="اختر نوع المركبة"></div>
          <div class="a3fd-models">
            <label class="a3fd-inputlabel" for="a3fd-model">الماركة والموديل (اختياري)<input id="a3fd-model" type="text" maxlength="70" autocomplete="off" placeholder="مثال: نيسان صني N17"></label>
            <label class="a3fd-inputlabel" for="a3fd-year">سنة الصنع (اختياري)<input id="a3fd-year" type="number" min="1970" max="2030" step="1" placeholder="مثال: 2021"></label>
          </div>
          <p class="a3fd-muted">اسم الموديل يُضاف لملخص الفني فقط؛ لا يعني أن أسباب الأعطال أو أسعار القطع مؤكدة لهذا الجيل دون فحص.</p>
        </section>
        <section class="a3fd-block" aria-labelledby="a3fd-category-title">
          <h2 id="a3fd-category-title" class="a3fd-title"><span class="a3fd-number">2</span>حدد نوع الشكوى</h2>
          <div id="a3fd-cats" class="a3fd-choices a3fd-categories" role="group" aria-label="فئات الأعراض"></div>
        </section>
        <section class="a3fd-block" aria-labelledby="a3fd-symptom-title">
          <h2 id="a3fd-symptom-title" class="a3fd-title"><span class="a3fd-number">3</span>اختَر العَرَض الأقرب</h2>
          <div id="a3fd-symptoms" class="a3fd-choices" role="group" aria-label="الأعراض المتاحة"></div>
        </section>
        <section class="a3fd-block" aria-labelledby="a3fd-danger-title">
          <h2 id="a3fd-danger-title" class="a3fd-title"><span class="a3fd-number">4</span>تأكد من علامات الخطر أولًا</h2>
          <div id="a3fd-danger" class="a3fd-danger" role="radiogroup" aria-label="علامات الخطر"></div>
          <div id="a3fd-notice" class="a3fd-notice" role="alert" aria-live="polite"><strong>لو ظهرت لمبة زيت حمراء أو سخونة شديدة أو ضعف فرامل أو تسريب وقود، أوقف المركبة بأمان.</strong></div>
        </section>
        <section class="a3fd-block" aria-labelledby="a3fd-questions-title">
          <h2 id="a3fd-questions-title" class="a3fd-title"><span class="a3fd-number">5</span>جاوب على سؤالين لتضييق الأسباب</h2>
          <div id="a3fd-questions" aria-live="polite"><p>اختَر العَرَض عشان تظهر الأسئلة.</p></div>
        </section>
        <section id="a3fd-report" aria-label="نتيجة فرز الأعطال" aria-live="polite" hidden></section>
      </section>
      <aside class="a3fd-sidebar" aria-label="إرشادات السلامة والمصادر">
        <div class="a3fd-sidebar-card">
          <h2>مهم قبل ما تبدأ</h2>
          <p>الأداة لا تشخّص القطعة التالفة، ولا تحل محل جهاز فحص أو ميكانيكي مؤهل. لو العربية أو الموتوسيكل في مكان خطر، الأولوية للوصول إلى مكان آمن وطلب المساعدة.</p>
          <ul>
            <li>لمبة ضغط زيت حمراء أثناء التشغيل أو حرارة في الأحمر: توقف بأمان وأطفئ المحرك.</li>
            <li>ضعف شديد في الفرامل أو فقد السيطرة: لا تواصل السير.</li>
            <li>تسريب وقود أو دخان أو شرر: ابتعد عن مصادر الاشتعال ولا تُجرّب التشغيل.</li>
            <li>لا تفتح غطاء مياه ساخنًا، ولا تلمس سيورًا أو أجزاء دوارة.</li>
          </ul>
        </div>
        <div class="a3fd-sidebar-card">
          <h2>من أين تأتي التوصيات؟</h2>
          <p>منطق الفرز مبني على قواعد سلامة وتحليل أعراض، والروابط تشير إلى الأدلة المنشورة على أعطال.كوم. يُراجع دليل المالك للموديل الصحيح دائمًا.</p>
          <a href="https://www.theaa.com/breakdown-cover/advice/dashboard-warning-lights" rel="nofollow noopener" target="_blank">مرجع تحذيرات العدادات من AA</a>
          <a href="<?php echo esc_url(home_url('/dtc/')); ?>">مكتبة أكواد أعطال السيارات DTC</a>
          <a href="<?php echo esc_url(home_url('/service-centers/')); ?>">دليل مراكز الخدمة</a>
          <a href="<?php echo esc_url(home_url('/car-tools/#maintenance-cost')); ?>">حاسبة تقدير فاتورة الورشة</a>
        </div>
        <div class="a3fd-sidebar-card">
          <h2>هل الأداة بتحفظ بياناتك؟</h2>
          <p>لا. اختيارك وإجاباتك واسم الموديل تبقى داخل المتصفح في هذه الجلسة ولا نرسلها إلى خادم للتشخيص. نسخ الملخص اختياري ويحدث بضغطة منك.</p>
        </div>
      </aside>
    </div>
    <section class="a3fd-footer-copy" aria-labelledby="a3fd-how">
      <h2 id="a3fd-how">إزاي تستخدم مشخّص الأعطال بصورة صحيحة؟</h2>
      <p>ابدأ بنوع المركبة، ثم اختَر الشكوى التي تستطيع ملاحظتها بنفسك مثل صوت أو رائحة أو لمبة عدادات. الأسئلة التالية تساعد في ترتيب الفحوصات المحتملة من الأبسط إلى الأكثر تخصصًا، لكنها لا تعطي نسبة مؤكدة لسبب معين. التحذيرات المتعلقة بالسلامة تأتي قبل أي مقارنة للتكلفة.</p>
      <h2>هل النتيجة تعني أن المركبة آمنة للقيادة؟</h2>
      <p>لا. حتى إذا ظهرت نتيجة «يحتاج فحصًا قريبًا»، فهي ليست شهادة أمان أو إذنًا بالقيادة. وفي حالات لمبة ضغط الزيت أو الحرارة الشديدة أو ضعف الفرامل أو الوقود المتسرب، يجب التوقف بأمان وطلب المساعدة.</p>
      <h2>ليه مش بنعرض سعرًا تلقائيًا لكل عطل؟</h2>
      <p>لأن سعر القطعة والمصنعية في مصر يتوقف على الجيل والمحرك والقطعة الأصلية أو البديلة وتاريخ عرض السعر. إظهار أرقام من غير مصدر قد يدفع الزائر لتغيير قطعة غير لازمة. بعد تأكيد التشخيص، استخدم <a href="<?php echo esc_url(home_url('/car-tools/#maintenance-cost')); ?>">حاسبة تكلفة الصيانة</a> لمقارنة بنود عروض الورش.</p>
    </section>
  </div>
</main>
<?php $fd_js=get_template_directory().'/assets/js/fault-diagnoser-20261106.js'; ?>
<?php if (is_readable($fd_js)): ?><script id="a3fd-inline-script" data-no-defer="1" data-no-optimize="1" data-no-delay="1"><?php readfile($fd_js); ?></script><?php endif; ?>
<?php get_footer(); ?>
