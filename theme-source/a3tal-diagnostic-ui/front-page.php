<?php get_header(); ?>
<section class="a3-hero">
  <div class="a3-container a3-hero-grid">
    <div>
      <span class="a3-eyebrow">A3tal Diagnostic UI</span>
      <h1>إيه المشكلة اللي ظهرت في عربيتك؟</h1>
      <p>ابدأ من كود العطل أو العرض الذي ظهر في السيارة، ثم انتقل إلى الأسباب والاختبارات المنطقية قبل التفكير في تغيير أي قطعة.</p>
      <form class="a3-search-shell" role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
        <input type="search" name="s" placeholder="اكتب كود العطل أو العرض… مثال: P0420، العربية بتنتش، لمبة البطارية" aria-label="ابحث عن العطل">
        <button class="a3-btn a3-btn-primary" type="submit">بحث وتشخيص</button>
      </form>
      <div class="a3-shortcuts">
        <a class="a3-shortcut" href="<?php echo esc_url(a3du_search_url('P0')); ?>">عندي كود عطل</a>
        <a class="a3-shortcut" href="<?php echo esc_url(a3du_search_url('العربية')); ?>">عندي عَرَض</a>
        <a class="a3-shortcut a3-open-car" href="#">اختار عربيتي</a>
        <a class="a3-shortcut" href="<?php echo esc_url(a3du_search_url('توقف عن القيادة')); ?>">مشكلة طارئة</a>
      </div>
    </div>
    <div class="a3-scanner">
      <div class="a3-scanner-head"><span>OBD-II DIAGNOSTIC</span><span class="a3-live"><span class="a3-live-dot"></span> Connected</span></div>
      <div class="a3-code">P0420</div>
      <div class="a3-code-label">Catalyst System Efficiency Below Threshold · Bank 1</div>
      <div class="a3-scan-grid">
        <div class="a3-scan-stat"><small>Severity</small><strong style="color:#FBBF24">Medium</strong></div>
        <div class="a3-scan-stat"><small>System</small><strong>Emissions</strong></div>
        <div class="a3-scan-stat"><small>First check</small><strong>Freeze Frame</strong></div>
        <div class="a3-scan-stat"><small>Rule</small><strong>Test before replace</strong></div>
      </div>
    </div>
  </div>
</section>

<div class="a3-carbar-wrap">
  <div class="a3-container">
    <div class="a3-carbar">
      <div class="a3-carbar-icon">◈</div>
      <div class="a3-carbar-copy"><strong id="a3-car-title">عربيتي: لم يتم الاختيار</strong><span id="a3-car-subtitle">اختيار السيارة يجهز الموقع لعرض محتوى أكثر ارتباطًا بموديلك.</span></div>
      <button class="a3-open-car" type="button">أضف عربيتك</button>
    </div>
  </div>
</div>

<section class="a3-section">
  <div class="a3-container">
    <div class="a3-section-head">
      <div><span class="a3-eyebrow" style="color:#0284C7;background:#E0F2FE">ابدأ من المشكلة</span><h2>اختار النظام اللي فيه العطل</h2><p>بدل ما نرمي عشرين مقالًا في وشك، ابدأ من الجزء الذي ظهرت فيه المشكلة.</p></div>
    </div>
    <div class="a3-systems">
      <?php
      $systems=[
        ['المحرك','تقطيع، حرارة، دخان، استهلاك زيت أو ضعف سحب','محرك'],
        ['الفتيس','نتشة، تأخير نقلات، تعليق أو صوت غير طبيعي','فتيس'],
        ['الكهرباء','دينامو، فيوزات، دوائر، أعطال تشغيل','كهرباء'],
        ['الفرامل','صفير، رعشة، دواسة، ABS ولمبات تحذير','فرامل'],
        ['التكييف','ضعف تبريد، كمبروسر، فريون أو أصوات','تكييف'],
        ['العادم','دخان، شكمان، كاتاليزر وانبعاثات','عادم'],
        ['الحساسات','O2، MAF، MAP، كرنك، كام وحساسات أخرى','حساس'],
        ['البطارية والشحن','بطارية، دينامو، ضعف شحن وصعوبة تشغيل','بطارية'],
      ];
      foreach($systems as $i=>$s): ?>
        <a class="a3-system-card" href="<?php echo esc_url(a3du_search_url($s[2])); ?>">
          <span class="a3-system-icon"><?php echo esc_html(str_pad((string)($i+1),2,'0',STR_PAD_LEFT)); ?></span>
          <h3><?php echo esc_html($s[0]); ?></h3><p><?php echo esc_html($s[1]); ?></p>
        </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="a3-section" style="padding-top:0">
  <div class="a3-container">
    <div class="a3-dtc-panel">
      <div>
        <span class="a3-eyebrow" style="color:#0284C7;background:#E0F2FE">DTC Finder</span>
        <h2>معاك كود Check Engine؟</h2>
        <p style="color:#64748B;margin:0">اكتب الكود كما ظهر على جهاز الفحص. الكود بداية التشخيص وليس حكمًا مباشرًا بتلف قطعة.</p>
        <form class="a3-dtc-form" method="get" action="<?php echo esc_url(home_url('/')); ?>">
          <input type="text" name="s" maxlength="7" placeholder="P _ _ _ _" aria-label="كود DTC">
          <button class="a3-btn a3-btn-primary">افتح الكود</button>
        </form>
        <div class="a3-chip-row">
          <?php foreach(['P0420','P0300','P0171','P0455'] as $code): ?><a class="a3-chip" href="<?php echo esc_url(a3du_search_url($code)); ?>"><?php echo esc_html($code); ?></a><?php endforeach; ?>
        </div>
      </div>
      <div class="a3-dtc-art">
        <small style="color:#64748B;font-weight:800">DIAGNOSTIC PRINCIPLE</small>
        <strong>CODE ≠ PART</strong>
        <ul><li>اقرأ Freeze Frame.</li><li>افحص الظروف التي سجل فيها الكود.</li><li>اختبر الدائرة أو النظام قبل استبدال القطعة.</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="a3-section" style="background:#fff;border-block:1px solid #E2E8F0">
  <div class="a3-container">
    <div class="a3-section-head"><div><span class="a3-eyebrow" style="color:#0284C7;background:#E0F2FE">أحدث التشخيصات</span><h2>مقالات تساعدك توصل للسبب</h2><p>المحتوى الحالي في أعطال.كوم يظهر تلقائيًا هنا، لكن داخل واجهة تشخيصية بدل قائمة مقالات تقليدية.</p></div></div>
    <div class="a3-post-grid">
      <?php $q=new WP_Query(['post_type'=>'post','post_status'=>'publish','posts_per_page'=>6,'ignore_sticky_posts'=>true]); if($q->have_posts()): while($q->have_posts()):$q->the_post(); a3du_post_card(); endwhile; wp_reset_postdata(); else: ?>
      <p>لا توجد مقالات منشورة.</p>
      <?php endif; ?>
    </div>
  </div>
</section>
<?php get_footer(); ?>
