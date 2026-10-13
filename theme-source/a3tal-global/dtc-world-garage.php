<?php
/**
 * A3TAL Global Garage discovery panel.
 * Browse-only layer: never generates thin brand/model permalinks or DTC claims.
 */
if (!defined('ABSPATH')) exit;
$garage_dtc_url = get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/');
$garage_cars_url = get_post_type_archive_link('a3_car') ?: home_url('/');
?>
<section class="gg-world" id="global-garage" aria-labelledby="gg-heading" dir="rtl">
  <div class="d-wrap">
    <div class="gg-intro">
      <span class="gg-kicker">A3TAL GLOBAL GARAGE <span aria-hidden="true">✦</span> الموسوعة العربية</span>
      <h2 id="gg-heading">اختار عربيتك. <span>واكتشف طريق التشخيص.</span></h2>
      <p>تصفح الماركات حسب المنشأ، ثم اختَر الموديل. الموديلات المعروضة دليل للتصفح وليست ادعاءً بأن كل الأعطال موثقة لها.</p>
      <div class="gg-highlights" aria-label="مميزات المكتبة"><span>ماركات عالمية</span><span>موديلات متعددة</span><span>أكواد OBD-II</span><span>روابط للأدلة المنشورة</span></div>
    </div>
    <div class="gg-shell" data-gg-garage data-dtc-url="<?php echo esc_url($garage_dtc_url); ?>" data-cars-url="<?php echo esc_url($garage_cars_url); ?>">
      <div class="gg-toolbar">
        <div><span class="gg-step">01 / 03</span><h3>اختر بلد المنشأ</h3><p>التصنيف حسب أصل العلامة التجارية، وليس بلد تجميع السيارة.</p></div>
        <label class="gg-brand-search"><span class="screen-reader-text">ابحث عن ماركة أو موديل</span><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/></svg><input type="search" id="gg-find" placeholder="ابحث: كيا، BMW، تويوتا، إلنترا…" autocomplete="off"></label>
      </div>
      <div class="gg-region-grid" role="group" aria-label="بلد المنشأ">
        <button class="gg-region is-active" type="button" data-origin="all" aria-pressed="true"><span class="gg-region-symbol">◎</span><strong>كل الماركات</strong><small>تصفح عالمي</small></button>
        <button class="gg-region" type="button" data-origin="jp" aria-pressed="false"><span class="gg-region-symbol">日</span><strong>ياباني</strong><small>Japan</small></button>
        <button class="gg-region" type="button" data-origin="kr" aria-pressed="false"><span class="gg-region-symbol">한</span><strong>كوري</strong><small>Korea</small></button>
        <button class="gg-region" type="button" data-origin="cn" aria-pressed="false"><span class="gg-region-symbol">中</span><strong>صيني</strong><small>China</small></button>
        <button class="gg-region" type="button" data-origin="in" aria-pressed="false"><span class="gg-region-symbol">IN</span><strong>هندي</strong><small>India</small></button>
        <button class="gg-region" type="button" data-origin="eu" aria-pressed="false"><span class="gg-region-symbol">EU</span><strong>أوروبي</strong><small>Europe</small></button>
        <button class="gg-region" type="button" data-origin="us" aria-pressed="false"><span class="gg-region-symbol">US</span><strong>أمريكي</strong><small>USA</small></button>
        <button class="gg-region" type="button" data-origin="other" aria-pressed="false"><span class="gg-region-symbol">✧</span><strong>منشأ آخر</strong><small>بقية العالم</small></button>
      </div>
      <div class="gg-divider"></div>
      <div class="gg-section-title"><div><span class="gg-step">02 / 03</span><h3>اختر الماركة</h3><p id="gg-brand-count" aria-live="polite">استعرض الماركات المتاحة</p></div><button type="button" class="gg-clear" data-gg-reset>إعادة الاختيار ↶</button></div>
      <div class="gg-brand-grid" id="gg-brands" role="group" aria-label="ماركات السيارات"></div>
      <p class="gg-empty" id="gg-brands-empty" hidden>لم نعثر على ماركة مطابقة. جرّب الاسم بالعربية أو الإنجليزية.</p>
      <div class="gg-divider"></div>
      <div class="gg-section-title"><div><span class="gg-step">03 / 03</span><h3>اختر الموديل</h3><p id="gg-model-desc" aria-live="polite">اختَر الماركة أولاً لعرض موديلاتها المتاحة.</p></div></div>
      <div class="gg-model-grid" id="gg-models" role="group" aria-label="موديلات الماركة"><div class="gg-placeholder">حدد ماركتك من البطاقات بالأعلى لعرض الموديلات.</div></div>
      <div class="gg-selected" id="gg-selected" hidden>
        <div><span class="gg-kicker">السيارة المختارة</span><strong id="gg-selected-name"></strong><p>اختَر سنة الصنع والمحرك داخل دليل السيارة عند توفره؛ اختلاف الجيل والمحرك يغيّر خطوات الفحص.</p></div>
        <div class="gg-selected-actions"><a id="gg-search-model" href="<?php echo esc_url($garage_cars_url); ?>">ابحث عن أدلة هذه السيارة ←</a><a href="<?php echo esc_url($garage_dtc_url . '#dtc-codes'); ?>">دليل أكواد الأعطال ↗</a></div>
      </div>
      <div class="gg-diagnostics" id="gg-diagnostics" hidden aria-live="polite">
        <div class="gg-diagnostics-header"><div><span class="gg-step">DIAGNOSTICS / التشخيص</span><h3>شروحات الأكواد المتاحة</h3><p id="gg-diagnostics-description">هذه أكواد عامة منشورة؛ لا نعتبرها أعطالاً مؤكدة للموديل المختار.</p></div><a href="<?php echo esc_url($garage_dtc_url); ?>">كل الأكواد ←</a></div>
        <div class="gg-diagnostics-grid" id="gg-diagnostics-grid"></div>
      </div>
      <p class="gg-coverage-note">هذه واجهة تصفح أولية قابلة للتوسع. ظهور الماركة أو الموديل لا يعني وجود دليل عطل خاص به بعد. تفاصيل الأعطال تُربط بالمراجع الفنية عند مراجعتها، دون تكرار محتوى الأكواد العامة.</p>
    </div>
  </div>
</section>