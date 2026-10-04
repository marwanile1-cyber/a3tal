<?php
get_header();
$brands=get_terms(['taxonomy'=>'a3_brand','hide_empty'=>false]);
$markets=get_terms(['taxonomy'=>'a3_market','hide_empty'=>false]);
$conditions=get_terms(['taxonomy'=>'a3_listing_condition','hide_empty'=>false]);
?>
<section class="g-commerce-hero g-market-hero"><div class="g-wrap">
  <span>A3TAL MARKET</span>
  <h1>سيارات للبيع من ملاكها</h1>
  <p>سوق سيارات مبني على بيانات المركبة داخل أعطال، مع عداد وصيانة وسجل ملكية عندما يختار البائع مشاركته.</p>
  <div class="g-market-hero-actions"><a href="<?php echo esc_url(home_url('/my-garage/')); ?>">بيع سيارتي من الجراج</a><a href="<?php echo esc_url(get_post_type_archive_link('a3_showroom')); ?>">معارض السيارات</a></div>
  <form class="g-commerce-filter" method="get">
    <label><small>الماركة</small><select name="brand"><option value="">كل الماركات</option><?php foreach($brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('brand'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
    <label><small>السوق</small><select name="market"><option value="">كل الأسواق</option><?php foreach($markets as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('market'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
    <label><small>الحالة</small><select name="listing_condition"><option value="">كل الحالات</option><?php foreach($conditions as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('listing_condition'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
    <button type="submit"><?php echo a3g_icon('search'); ?><span>بحث</span></button>
  </form>
</div></section>

<main class="g-wrap g-commerce-main">
  <div class="g-commerce-head"><div><span>USED CARS</span><h2>أحدث السيارات المعروضة</h2></div><a href="<?php echo esc_url(home_url('/my-garage/')); ?>">+ أضف سيارتك</a></div>
  <?php if(have_posts()): ?><div class="g-listing-grid">
  <?php while(have_posts()):the_post();
    $price=(float)get_post_meta(get_the_ID(),'_a3_listing_price',true);$cur=(string)get_post_meta(get_the_ID(),'_a3_listing_currency',true);$km=(int)get_post_meta(get_the_ID(),'_a3_listing_mileage_km',true);$year=(int)get_post_meta(get_the_ID(),'_a3_listing_year',true);$loc=(string)get_post_meta(get_the_ID(),'_a3_listing_location',true);$cond=get_the_terms(get_the_ID(),'a3_listing_condition');$condition=($cond&&!is_wp_error($cond))?$cond[0]:null;
  ?>
    <article class="g-listing-card">
      <a class="g-listing-media" href="<?php the_permalink(); ?>"><?php if(has_post_thumbnail()){the_post_thumbnail('large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL MARKET</span>';} ?><?php if($condition): ?><span class="g-listing-condition"><?php echo esc_html($condition->name); ?></span><?php endif; ?></a>
      <div class="g-listing-body"><h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3><?php if($price>0): ?><strong><?php echo esc_html(number_format_i18n($price,0).' '.$cur); ?></strong><?php endif; ?><div class="g-listing-facts"><?php if($year): ?><span><?php echo esc_html($year); ?></span><?php endif; ?><?php if($km): ?><span><?php echo esc_html(number_format_i18n($km).' كم'); ?></span><?php endif; ?><?php if($loc): ?><span><?php echo esc_html($loc); ?></span><?php endif; ?></div><a class="g-platform-more" href="<?php the_permalink(); ?>">تفاصيل السيارة ←</a></div>
    </article>
  <?php endwhile; ?></div><div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
  <?php else: ?><div class="g-platform-empty"><span>🏷️</span><h2>السوق لسه بيفتح أبوابه</h2><p>أول الإعلانات هتدخل من My Garage للمراجعة قبل النشر، بدل مهرجان الإعلانات المكررة والمجهولة المعتاد.</p><a href="<?php echo esc_url(home_url('/my-garage/')); ?>">اذهب إلى سيارتي</a></div><?php endif; ?>
<?php a3g_legacy_section(
  [374,22],
  'محتوى يساعدك قبل شراء المستعمل',
  'لحد ما تبدأ إعلانات السوق الفعلية، أسعار السيارات ومراجعاتها الحالية تظهر هنا بروابطها الأصلية بدل صفحة خالية.',
  12,
  [],
  374
); ?>
</main><?php get_footer(); ?>