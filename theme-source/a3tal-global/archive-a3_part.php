<?php
get_header();
$brands=get_terms(['taxonomy'=>'a3_brand','hide_empty'=>false]);
$markets=get_terms(['taxonomy'=>'a3_market','hide_empty'=>false]);
$origins=get_terms(['taxonomy'=>'a3_part_origin','hide_empty'=>false]);
$cats=get_terms(['taxonomy'=>'a3_part_category','hide_empty'=>false]);
?>
<section class="g-commerce-hero g-parts-hero">
  <div class="g-wrap">
    <span>A3TAL PARTS</span>
    <h1>قطع الغيار المناسبة لمركبتك</h1>
    <p>ابحث برقم القطعة أو الماركة أو النوع، وقارن بين الأصلي وOES وAftermarket والبدائل الاقتصادية والاستيراد قبل الشراء.</p>
    <form class="g-commerce-filter" method="get">
      <label><small>الماركة</small><select name="brand"><option value="">كل الماركات</option><?php foreach($brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('brand'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small>نوع القطعة</small><select name="part_origin"><option value="">كل الأنواع</option><?php foreach($origins as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('part_origin'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small>التصنيف</small><select name="part_category"><option value="">كل التصنيفات</option><?php foreach($cats as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('part_category'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small>السوق</small><select name="market"><option value="">كل الأسواق</option><?php foreach($markets as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('market'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <button type="submit"><?php echo a3g_icon('search'); ?><span>بحث</span></button>
    </form>
    <div class="g-part-trust-row">
      <span><b>OEM</b> أصلي</span><span><b>OES</b> مورد أصلي</span><span><b>AM</b> Aftermarket</span><span><b>IMP</b> استيراد</span>
    </div>
  </div>
</section>

<main class="g-wrap g-commerce-main">
  <div class="g-commerce-head">
    <div><span>PARTS CATALOG</span><h2>كتالوج قطع الغيار</h2></div>
    <div class="g-commerce-actions"><a href="<?php echo esc_url(get_post_type_archive_link('a3_parts_vendor')); ?>">أماكن بيع القطع</a><a href="<?php echo esc_url(home_url('/my-garage/')); ?>">هل تناسب سيارتي؟</a></div>
  </div>

  <?php if(have_posts()): ?><div class="g-parts-grid">
  <?php while(have_posts()):the_post();
    $orig=get_the_terms(get_the_ID(),'a3_part_origin');$origin=($orig&&!is_wp_error($orig))?$orig[0]:null;
    $pn=(string)get_post_meta(get_the_ID(),'_a3_part_number',true);
    $oem=(string)get_post_meta(get_the_ID(),'_a3_oem_number',true);
    $maker=(string)get_post_meta(get_the_ID(),'_a3_part_manufacturer',true);
    $min=(float)get_post_meta(get_the_ID(),'_a3_price_min',true);$max=(float)get_post_meta(get_the_ID(),'_a3_price_max',true);$cur=(string)get_post_meta(get_the_ID(),'_a3_currency',true);
  ?>
    <article class="g-part-card">
      <a class="g-part-media" href="<?php the_permalink(); ?>"><?php if(has_post_thumbnail()){the_post_thumbnail('large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL PARTS</span>';} ?></a>
      <div class="g-part-body">
        <div class="g-part-badges"><?php if($origin): ?><span><?php echo esc_html($origin->name); ?></span><?php endif; ?><?php if($maker): ?><span><?php echo esc_html($maker); ?></span><?php endif; ?></div>
        <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
        <div class="g-part-numbers"><?php if($pn): ?><small>رقم القطعة <b><?php echo esc_html($pn); ?></b></small><?php endif; ?><?php if($oem): ?><small>OEM <b><?php echo esc_html($oem); ?></b></small><?php endif; ?></div>
        <?php if($min>0||$max>0): ?><strong class="g-part-price"><?php echo esc_html(number_format_i18n($min>0?$min:$max,0)); ?><?php if($max>0&&$max!=$min): ?> – <?php echo esc_html(number_format_i18n($max,0)); ?><?php endif; ?> <?php echo esc_html($cur); ?></strong><?php endif; ?>
        <a class="g-platform-more" href="<?php the_permalink(); ?>">التوافق والتفاصيل ←</a>
      </div>
    </article>
  <?php endwhile; ?></div><div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
  <?php else: ?><div class="g-platform-empty"><span>⚙️</span><h2>الكتالوج لسه بيتعبّى ببيانات موثقة</h2><p>مش هنحط أرقام قطع وأسعار من الذاكرة. كل قطعة هتنزل مرتبطة بمصدر ومركبات متوافقة.</p></div><?php endif; ?>
</main>
<?php get_footer(); ?>