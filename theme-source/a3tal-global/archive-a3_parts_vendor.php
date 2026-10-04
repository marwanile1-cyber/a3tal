<?php
get_header();
$brands=get_terms(['taxonomy'=>'a3_brand','hide_empty'=>false]);
$markets=get_terms(['taxonomy'=>'a3_market','hide_empty'=>false]);
$statuses=get_terms(['taxonomy'=>'a3_vendor_status','hide_empty'=>false]);
?>
<section class="g-commerce-hero g-vendor-hero"><div class="g-wrap">
  <span>A3TAL PARTS STORES</span>
  <h1>أماكن بيع قطع الغيار</h1>
  <p>دليل منظم للموزعين الرسميين والبائعين الموثقين والمحلات المستقلة، مع الماركات والسوق ووسائل التواصل.</p>
  <form class="g-commerce-filter" method="get">
    <label><small>الماركة</small><select name="brand"><option value="">كل الماركات</option><?php foreach($brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('brand'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
    <label><small>السوق</small><select name="market"><option value="">كل الأسواق</option><?php foreach($markets as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('market'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
    <label><small>حالة البائع</small><select name="vendor_status"><option value="">كل الحالات</option><?php foreach($statuses as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('vendor_status'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
    <button type="submit"><?php echo a3g_icon('search'); ?><span>بحث</span></button>
  </form>
</div></section>

<main class="g-wrap g-commerce-main">
  <div class="g-commerce-head"><div><span>DIRECTORY</span><h2>دليل بائعي قطع الغيار</h2></div><a href="<?php echo esc_url(get_post_type_archive_link('a3_part')); ?>">تصفح القطع نفسها</a></div>
  <?php if(have_posts()): ?><div class="g-vendor-grid">
  <?php while(have_posts()):the_post();
    $status=get_the_terms(get_the_ID(),'a3_vendor_status');$st=($status&&!is_wp_error($status))?$status[0]:null;
    $phone=(string)get_post_meta(get_the_ID(),'_a3_phone',true);$addr=(string)get_post_meta(get_the_ID(),'_a3_address',true);$delivery=(bool)get_post_meta(get_the_ID(),'_a3_delivery_available',true);$checked=(string)get_post_meta(get_the_ID(),'_a3_source_checked_at',true);
  ?>
    <article class="g-vendor-card">
      <a class="g-vendor-media" href="<?php the_permalink(); ?>"><?php if(has_post_thumbnail()){the_post_thumbnail('large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL PARTS</span>';} ?></a>
      <div class="g-vendor-body"><?php if($st): ?><span class="g-vendor-badge g-vendor-<?php echo esc_attr($st->slug); ?>"><?php echo esc_html($st->name); ?></span><?php endif; ?><h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3><?php if($addr): ?><p><?php echo esc_html($addr); ?></p><?php endif; ?><div class="g-vendor-meta"><?php if($phone): ?><span>☎ <?php echo esc_html($phone); ?></span><?php endif; ?><?php if($delivery): ?><span>🚚 توصيل متاح</span><?php endif; ?><?php if($checked): ?><small>تحقق: <?php echo esc_html($checked); ?></small><?php endif; ?></div><a class="g-platform-more" href="<?php the_permalink(); ?>">عرض التفاصيل ←</a></div>
    </article>
  <?php endwhile; ?></div><div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
  <?php else: ?><div class="g-platform-empty"><span>🧰</span><h2>الدليل لسه بيتراجع ويتوثق</h2><p>أي بائع هيظهر هنا بحالة واضحة: رسمي، موثّق من أعطال، أو مستقل.</p></div><?php endif; ?>
</main><?php get_footer(); ?>