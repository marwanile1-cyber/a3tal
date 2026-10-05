<?php
$searched_code=strtoupper(preg_replace('/[^A-Z0-9]/i','',(string)get_query_var('code')));
$legacy_match_q=null;
$legacy_match_count=0;
$legacy_exact_id=0;
if($searched_code!==''){
  $legacy_match_q=new WP_Query([
    'post_type'=>'post',
    'post_status'=>'publish',
    'cat'=>2,
    's'=>$searched_code,
    'posts_per_page'=>12,
    'ignore_sticky_posts'=>true,
  ]);
  $legacy_match_count=(int)$legacy_match_q->found_posts;
  if($legacy_match_q->posts){
    foreach($legacy_match_q->posts as $legacy_post){
      $legacy_slug=(string)$legacy_post->post_name;
      $legacy_title=(string)$legacy_post->post_title;
      if(stripos($legacy_title,$searched_code)!==false || stripos($legacy_slug,strtolower($searched_code))!==false){
        $legacy_exact_id=(int)$legacy_post->ID;
        break;
      }
    }
  }
}
get_header(); ?>
<section class="g-platform-archive-hero g-dtc-archive-hero">
  <div class="g-wrap">
    <span>A3TAL DTC LIBRARY</span>
    <h1>مرجع أكواد أعطال السيارات OBD-II</h1>
    <p>ابحث بالكود مباشرة للوصول إلى المعنى والأعراض والأسباب وخطوات التشخيص قبل تغيير أي قطعة.</p>
    <form class="g-dtc-search" method="get">
      <input type="text" name="code" value="<?php echo esc_attr($searched_code); ?>" placeholder="اكتب الكود مثل P0420" maxlength="8" autocomplete="off">
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
    <?php if($legacy_match_count>0): ?>
      <div class="g-platform-empty g-dtc-legacy-hit"><?php echo a3g_icon('search'); ?><h2>وجدنا شرحًا منشورًا للكود <?php echo esc_html($searched_code); ?></h2><p>الكود لم يُضف بعد كصفحة مرجعية منظمة، لكن الشرح الفني الموجود على أعطال متاح مباشرة بالأسفل.</p></div>
    <?php else: ?>
      <div class="g-platform-empty"><?php echo a3g_icon('gear'); ?><h2>لم نجد شرحًا منشورًا للكود <?php echo esc_html($searched_code?:'المطلوب'); ?></h2><p>راجع كتابة الكود، أو تصفح شروحات أكواد الأعطال المتاحة في المكتبة.</p></div>
    <?php endif; ?>
  <?php endif; ?>

  <?php if($legacy_match_count>0): ?>
    <section class="g-legacy-bridge g-dtc-search-results">
      <?php if($legacy_exact_id): ?>
        <div class="g-section-head"><div><span>النتيجة الأقرب</span><h2>شرح الكود <?php echo esc_html($searched_code); ?></h2><p>ابدأ بالشرح المطابق للكود، ثم راجع النتائج المرتبطة فقط إذا احتجت تفاصيل إضافية.</p></div></div>
        <div class="g-news-grid g-dtc-exact-grid"><?php a3g_card($legacy_exact_id,'g-legacy-card g-dtc-exact-card'); ?></div>
      <?php endif; ?>

      <?php if($legacy_match_count>($legacy_exact_id?1:0)): ?>
        <div class="g-section-head g-dtc-related-head"><div><span>نتائج مرتبطة</span><h2>شروحات أخرى مرتبطة بـ <?php echo esc_html($searched_code); ?></h2></div><div class="g-legacy-count"><?php echo esc_html(number_format_i18n($legacy_match_count-($legacy_exact_id?1:0))); ?> نتيجة</div></div>
        <div class="g-news-grid g-legacy-grid">
          <?php while($legacy_match_q->have_posts()):$legacy_match_q->the_post();if(get_the_ID()===$legacy_exact_id)continue;a3g_card(get_the_ID(),'g-legacy-card');endwhile;wp_reset_postdata(); ?>
        </div>
      <?php else: wp_reset_postdata(); endif; ?>
    </section>
  <?php endif; ?>
  <?php
  $legacy_exclude=a3g_entity_related_post_ids('a3_dtc');
  if($legacy_exact_id)$legacy_exclude[]=$legacy_exact_id;
  $legacy_exclude=array_values(array_unique(array_map('intval',$legacy_exclude)));
  a3g_legacy_section(
    [2],
    'كل شروحات أكواد الأعطال',
    'شروحات تفصيلية لأكواد OBD-II تشمل المعنى والأعراض والأسباب وخطوات التشخيص قبل تغيير القطع.',
    18,
    $legacy_exclude,
    2
  );
  ?>
</main>
<?php get_footer(); ?>