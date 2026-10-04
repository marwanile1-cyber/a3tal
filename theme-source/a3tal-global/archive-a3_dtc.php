<?php get_header(); ?>
<section class="g-platform-archive-hero g-dtc-archive-hero">
  <div class="g-wrap">
    <span>A3TAL DTC LIBRARY</span>
    <h1>مرجع أكواد أعطال السيارات OBD-II</h1>
    <p>ابحث بالكود مباشرة للوصول إلى المعنى والأعراض والأسباب وخطوات التشخيص قبل تغيير أي قطعة.</p>
    <form class="g-dtc-search" method="get">
      <input type="text" name="code" value="<?php echo esc_attr((string)get_query_var('code')); ?>" placeholder="اكتب الكود مثل P0420" maxlength="8" autocomplete="off">
      <button type="submit"><?php echo a3g_icon('search'); ?><span>بحث عن الكود</span></button>
    </form>
    <div class="g-dtc-family-links">
      <span><b>P</b> المحرك وناقل الحركة</span>
      <span><b>B</b> الهيكل والمقصورة</span>
      <span><b>C</b> الشاسيه والفرامل</span>
      <span><b>U</b> الشبكات والاتصالات</span>
    </div>
  </div>
</section>

<main class="g-wrap g-platform-archive">
  <div class="g-platform-archive-head"><div><span>مرجع تشخيصي</span><h2>أكواد الأعطال المنشورة</h2></div><b><?php global $wp_query; echo esc_html(number_format_i18n((int)$wp_query->found_posts)); ?> كود</b></div>
  <?php if(have_posts()): ?>
  <div class="g-dtc-grid">
    <?php while(have_posts()):the_post();
      $code=a3cp_field('_a3_dtc_code');$sys=a3cp_field('_a3_dtc_system');$sev=a3cp_field('_a3_severity');
      $sev_labels=['low'=>'منخفضة','medium'=>'متوسطة','high'=>'مرتفعة','critical'=>'حرجة'];
    ?>
    <article class="g-dtc-card">
      <a href="<?php the_permalink(); ?>">
        <div class="g-dtc-code"><?php echo esc_html($code?:get_the_title()); ?></div>
        <?php if($sys): ?><span><?php echo esc_html($sys); ?></span><?php endif; ?>
        <h3><?php the_title(); ?></h3>
        <p><?php echo esc_html(a3g_excerpt(get_the_ID(),18)); ?></p>
        <footer><small>الخطورة: <?php echo esc_html($sev_labels[$sev]??'غير محددة'); ?></small><b>التفاصيل ←</b></footer>
      </a>
    </article>
    <?php endwhile; ?>
  </div>
  <div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
  <?php else: ?>
  <div class="g-platform-empty"><span>⚙️</span><h2>لم نجد هذا الكود في قاعدة البيانات المنشورة بعد</h2><p>لن نملأ المرجع بتفسيرات غير مراجعة. سيتم نشر الأكواد بعد التحقق من تعريفها ومصادرها الفنية.</p></div>
  <?php endif; ?>
  <?php
  $legacy_exclude=a3g_entity_related_post_ids('a3_dtc');
  a3g_legacy_section(
    [2],
    'شروحات أكواد الأعطال الموجودة بالفعل',
    'الـ68 مقال DTC الحاليين فضلوا على روابطهم الأصلية، والمرجع الجديد بيجمعهم بدل ما يخلق نسخ منافسة لهم.',
    18,
    $legacy_exclude,
    2
  );
  ?>
</main>
<?php get_footer(); ?>