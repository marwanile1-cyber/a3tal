<?php get_header(); while(have_posts()):the_post();
$code=a3cp_field('_a3_dtc_code');$system=a3cp_field('_a3_dtc_system');$severity=a3cp_field('_a3_severity');$scope=a3cp_field('_a3_code_scope');$manufacturer=a3cp_field('_a3_manufacturer');$advice=a3cp_field('_a3_drive_advice');$source=a3cp_field('_a3_source_url');$checked=a3cp_field('_a3_source_checked_at');$related=a3g_related_post_ids();
$sev_labels=['low'=>'منخفضة','medium'=>'متوسطة','high'=>'مرتفعة','critical'=>'حرجة'];
$scope_labels=['generic'=>'عام OBD-II','manufacturer'=>'خاص بالشركة المصنعة'];
?>
<section class="g-dtc-single-hero">
  <div class="g-wrap g-dtc-single-grid">
    <div>
      <div class="g-breadcrumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a><span>›</span><a href="<?php echo esc_url(get_post_type_archive_link('a3_dtc')); ?>">أكواد DTC</a></div>
      <span>A3TAL DTC</span>
      <h1><?php echo esc_html($code?:get_the_title()); ?></h1>
      <h2><?php the_title(); ?></h2>
      <?php if(has_excerpt()): ?><p><?php echo esc_html(get_the_excerpt()); ?></p><?php endif; ?>
    </div>
    <aside>
      <div><small>النظام</small><strong><?php echo esc_html($system?:'غير محدد'); ?></strong></div>
      <div><small>درجة الخطورة</small><strong><?php echo esc_html($sev_labels[$severity]??'غير محددة'); ?></strong></div>
      <div><small>نوع الكود</small><strong><?php echo esc_html($scope_labels[$scope]??'غير محدد'); ?></strong></div>
      <?php if($manufacturer): ?><div><small>الشركة</small><strong><?php echo esc_html($manufacturer); ?></strong></div><?php endif; ?>
    </aside>
  </div>
</section>

<main class="g-wrap g-dtc-single-main">
  <?php if($advice): ?><div class="g-dtc-drive-note"><b>هل يمكن الاستمرار في القيادة؟</b><p><?php echo esc_html($advice); ?></p></div><?php endif; ?>
  <article class="g-vehicle-panel g-entry"><?php the_content(); ?></article>
  <?php if($source||$checked): ?><div class="g-source-note"><span><?php if($checked): ?>آخر مراجعة للمصدر: <?php echo esc_html($checked); ?><?php endif; ?></span><?php if($source): ?><a href="<?php echo esc_url($source); ?>" rel="nofollow noopener" target="_blank">فتح المصدر الفني</a><?php endif; ?></div><?php endif; ?>
  <?php if($related): $rq=new WP_Query(['post_type'=>'post','post_status'=>'publish','post__in'=>$related,'orderby'=>'post__in','posts_per_page'=>12]); if($rq->have_posts()): ?>
  <section class="g-vehicle-panel"><div class="g-section-head"><div><span>من أعطال.كوم</span><h2>شرح وتشخيصات مرتبطة</h2></div></div><div class="g-news-grid"><?php while($rq->have_posts()):$rq->the_post();a3g_card();endwhile;wp_reset_postdata(); ?></div></section>
  <?php endif; endif; ?>
</main>
<?php endwhile; get_footer(); ?>