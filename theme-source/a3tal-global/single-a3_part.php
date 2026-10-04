<?php get_header(); while(have_posts()):the_post();
$orig=get_the_terms(get_the_ID(),'a3_part_origin');$origin=($orig&&!is_wp_error($orig))?$orig[0]:null;
$cats=get_the_terms(get_the_ID(),'a3_part_category');$cat=($cats&&!is_wp_error($cats))?$cats[0]:null;
$pn=(string)get_post_meta(get_the_ID(),'_a3_part_number',true);$oem=(string)get_post_meta(get_the_ID(),'_a3_oem_number',true);$maker=(string)get_post_meta(get_the_ID(),'_a3_part_manufacturer',true);
$min=(float)get_post_meta(get_the_ID(),'_a3_price_min',true);$max=(float)get_post_meta(get_the_ID(),'_a3_price_max',true);$cur=(string)get_post_meta(get_the_ID(),'_a3_currency',true);
$source=(string)get_post_meta(get_the_ID(),'_a3_source_url',true);$checked=(string)get_post_meta(get_the_ID(),'_a3_source_checked_at',true);
$ids=array_filter(array_map('absint',preg_split('/[^0-9]+/',(string)get_post_meta(get_the_ID(),'_a3_vehicle_entity_ids',true))));
?>
<section class="g-part-single-hero"><div class="g-wrap g-part-single-grid">
  <div>
    <div class="g-breadcrumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a><span>›</span><a href="<?php echo esc_url(get_post_type_archive_link('a3_part')); ?>">قطع الغيار</a></div>
    <div class="g-part-badges"><?php if($origin): ?><span><?php echo esc_html($origin->name); ?></span><?php endif; ?><?php if($cat): ?><span><?php echo esc_html($cat->name); ?></span><?php endif; ?></div>
    <h1><?php the_title(); ?></h1>
    <?php if($maker): ?><p>الشركة المصنعة: <strong><?php echo esc_html($maker); ?></strong></p><?php endif; ?>
    <div class="g-part-hero-numbers"><?php if($pn): ?><span><small>رقم القطعة</small><b><?php echo esc_html($pn); ?></b></span><?php endif; ?><?php if($oem): ?><span><small>OEM</small><b><?php echo esc_html($oem); ?></b></span><?php endif; ?></div>
    <?php if($min>0||$max>0): ?><div class="g-part-hero-price">تقريبًا <strong><?php echo esc_html(number_format_i18n($min>0?$min:$max,0)); ?><?php if($max>0&&$max!=$min): ?> – <?php echo esc_html(number_format_i18n($max,0)); ?><?php endif; ?> <?php echo esc_html($cur); ?></strong></div><?php endif; ?>
  </div>
  <div class="g-part-single-image"><?php if(has_post_thumbnail()){the_post_thumbnail('full',['loading'=>'eager']);}else{echo '<span class="g-fallback">A3TAL PARTS</span>';} ?></div>
</div></section>

<main class="g-wrap g-part-single-main">
  <?php if($ids): ?><section class="g-vehicle-panel"><div class="g-section-head"><div><span>FITMENT</span><h2>المركبات المتوافقة</h2></div><a href="<?php echo esc_url(home_url('/my-garage/')); ?>">تحقق من سيارتي</a></div><div class="g-fitment-grid"><?php foreach($ids as $id): if(get_post_status($id)!=='publish')continue; ?><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo a3g_icon('car'); ?><span><?php echo esc_html(get_the_title($id)); ?></span></a><?php endforeach; ?></div></section><?php endif; ?>
  <article class="g-vehicle-panel g-entry"><?php the_content(); ?></article>
  <section class="g-vehicle-panel g-part-buy-box"><div><span>BUY SMARTER</span><h2>تدور على مكان يبيعها؟</h2><p>شوف الموزعين الرسميين والبائعين الموثقين والمستقلين داخل دليل قطع الغيار.</p></div><a href="<?php echo esc_url(get_post_type_archive_link('a3_parts_vendor')); ?>">أماكن بيع قطع الغيار</a></section>
  <?php if($source||$checked): ?><div class="g-source-note"><span><?php if($checked): ?>آخر مراجعة: <?php echo esc_html($checked); ?><?php endif; ?></span><?php if($source): ?><a href="<?php echo esc_url($source); ?>" target="_blank" rel="nofollow noopener">فتح المصدر</a><?php endif; ?></div><?php endif; ?>
</main>
<?php endwhile;get_footer(); ?>