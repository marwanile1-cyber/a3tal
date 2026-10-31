<?php
$type=get_query_var('post_type');$is_showroom=$type==='a3_showroom';$title=$is_showroom?'معارض السيارات':'مراكز الخدمة';
$directory_ids=get_posts(['post_type'=>$type,'post_status'=>'publish','posts_per_page'=>-1,'fields'=>'ids','no_found_rows'=>true]);
$brands=$directory_ids?get_terms(['taxonomy'=>'a3_brand','hide_empty'=>true,'object_ids'=>$directory_ids]):[];
$markets=$directory_ids?get_terms(['taxonomy'=>'a3_market','hide_empty'=>true,'object_ids'=>$directory_ids]):[];
$statuses=$directory_ids?get_terms(['taxonomy'=>'a3_directory_status','hide_empty'=>true,'object_ids'=>$directory_ids]):[];
$guide_brand = sanitize_text_field((string)get_query_var('brand'));
$guide_location = sanitize_text_field((string)get_query_var('location'));
$directory_guides = !$is_showroom ? a3g_ux_directory_guides($guide_brand, $guide_location) : [];
if (!$is_showroom) {
  $guide_terms = get_terms(['taxonomy'=>'a3_brand','hide_empty'=>false]);
  $brand_options = [];
  foreach (is_wp_error($brands) ? [] : $brands as $term) $brand_options[$term->term_id] = $term;
  if (!is_wp_error($guide_terms)) foreach ($guide_terms as $term) {
    if (!isset($brand_options[$term->term_id]) && a3g_ux_directory_guides($term->slug)) $brand_options[$term->term_id] = $term;
  }
  $brands = array_values($brand_options);
  usort($brands, static function($a, $b) { return strcasecmp($a->name, $b->name); });
}
get_header(); ?>
<section class="g-platform-archive-hero g-directory-hero"><div class="g-wrap">
<span><?php echo $is_showroom?'A3TAL SHOWROOMS':'A3TAL SERVICE DIRECTORY'; ?></span>
<h1><?php echo esc_html($title); ?></h1>
<p><?php echo $is_showroom?'ابحث عن المعارض حسب السوق والماركة وحالة التحقق، مع فصل واضح بين المعتمد رسميًا والموثّق والمستقل.':'دليل مراكز الخدمة حسب الماركة والسوق وحالة الاعتماد والخدمات المتاحة.'; ?></p>
<form class="g-platform-filter" method="get">
<label><small>الماركة</small><select name="brand"><option value="">كل الماركات</option><?php foreach($brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('brand'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
<label><small>السوق</small><select name="market"><option value="">كل الأسواق</option><?php foreach($markets as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('market'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
<label><small>اعتماد المركز</small><select name="directory_status"><option value="">كل الحالات</option><?php foreach($statuses as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('directory_status'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
<label><small>المحافظة أو المدينة</small><input type="search" name="location" value="<?php echo esc_attr((string)get_query_var('location')); ?>" placeholder="مثال: القاهرة أو الإسكندرية"></label>
<button type="submit"><?php echo a3g_icon('search'); ?><span>بحث</span></button>
</form>
<?php if($guide_brand || $guide_location || get_query_var('market') || get_query_var('directory_status')): ?><a data-google-vignette="false" class="g-directory-reset" data-google-vignette="false" href="<?php echo esc_url(get_post_type_archive_link($type)); ?>">مسح الفلاتر وعرض كل النتائج</a><?php endif; ?>
</div></section>

<main class="g-wrap g-platform-archive">
<div class="g-platform-archive-head"><div><span>دليل أعطال</span><h2><?php echo $is_showroom?'اكتشف المعارض':'اختر مركز الخدمة'; ?></h2></div><b><?php global $wp_query; echo esc_html(number_format_i18n((int)$wp_query->found_posts)); ?> <?php echo $is_showroom?'معرضًا':'مركزًا مسجلًا'; ?></b></div>
<?php if(!$is_showroom): ?>
<section class="g-service-brand-hubs" aria-label="اختصارات أدلة التوكيلات ومراكز الصيانة" style="margin:20px 0 26px;padding:18px;border:1px solid #cbd5e1;border-radius:14px;background:#f8fafc">
<h2 style="margin:0 0 8px;color:#0b1220;font-size:21px">ابحث عن مركز الخدمة حسب ماركة السيارة</h2>
<p style="margin:0 0 14px;color:#475569">النتائج المنظمة أدناه تخص سجلات مراكز محددة داخل الدليل، وليست كل فروع التوكيلات في مصر. لعرض المزيد من الفروع ووسائل الحجز، افتح دليل العلامة ثم تأكد من الاعتماد والخدمة من الوكيل قبل الذهاب.</p>
<nav aria-label="أدلة الخدمة حسب العلامة" style="display:flex;flex-wrap:wrap;gap:10px">
<?php
$quick_hubs=[
  [81102,'غبور: الخط الساخن والحجز'],
  [79964,'منصور: الفروع والتواصل'],
  [80401,'جيتور: المراكز المعتمدة'],
  [81239,'كيا: الصيانة المعتمدة'],
  [79958,'هيونداي: التوكيل والصيانة'],
  [79924,'دليل مراكز الصيانة في مصر']
];
foreach($quick_hubs as $quick_hub):
  if(get_post_status((int)$quick_hub[0])!=='publish') continue;
?>
<a data-google-vignette="false" href="<?php echo esc_url(get_permalink((int)$quick_hub[0])); ?>" style="display:inline-flex;align-items:center;justify-content:center;flex:1 1 170px;min-height:44px;padding:10px 12px;background:white;border:1px solid #cbd5e1;border-radius:9px;text-decoration:none;color:#0b1220;font-weight:700"><?php echo esc_html($quick_hub[1]); ?></a>
<?php endforeach; ?>
</nav>
</section>
<?php endif; ?>
<?php if(have_posts()): ?><div class="g-directory-grid">
<?php while(have_posts()):the_post();$status=a3g_directory_status();$phone=a3cp_field('_a3_phone');$address=a3cp_field('_a3_address');$checked=a3cp_field('_a3_source_checked_at');$map_query=$is_showroom?(a3cp_field('_a3_maps_query')?:$address):$address;$map_url=$map_query?'https://www.google.com/maps/search/?api=1&query='.rawurlencode($map_query):''; ?>
<article class="g-directory-card">
<a data-google-vignette="false" class="g-directory-media" href="<?php the_permalink(); ?>"><?php if(has_post_thumbnail()){the_post_thumbnail('large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL</span>';} ?></a>
<div class="g-directory-body"><?php if($status): ?><span class="g-directory-badge g-status-<?php echo esc_attr($status->slug); ?>"><?php echo esc_html($status->name); ?></span><?php endif; ?><h3><a data-google-vignette="false" href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3><?php if($address): ?><p><?php echo esc_html($address); ?></p><?php endif; ?><div class="g-directory-mini-meta"><?php if($phone): ?><span>☎ <?php echo esc_html($phone); ?></span><?php endif; ?><?php if($checked): ?><small>تحقق: <?php echo esc_html($checked); ?></small><?php endif; ?></div><?php if($is_showroom): ?><div class="g-directory-card-actions"><?php if($phone): ?><a data-google-vignette="false" href="tel:<?php echo esc_attr(preg_replace('/[^0-9+]/','',$phone)); ?>">اتصال</a><?php endif; ?><?php if($map_url): ?><a data-google-vignette="false" href="<?php echo esc_url($map_url); ?>" rel="nofollow noopener" target="_blank">الخريطة</a><?php endif; ?><a data-google-vignette="false" href="<?php the_permalink(); ?>">كل التفاصيل</a></div><?php else: ?><div class="g-directory-card-actions"><?php if($phone && preg_match('/^\+?[0-9\s()\-]{3,24}$/',trim($phone))): ?><a data-google-vignette="false" data-a3tal-action="call" href="tel:<?php echo esc_attr(preg_replace('/[^0-9+]/','',$phone)); ?>">اتصال</a><?php endif; ?><?php if($map_url): ?><a data-google-vignette="false" data-a3tal-action="map" href="<?php echo esc_url($map_url); ?>" rel="nofollow noopener" target="_blank">الموقع</a><?php endif; ?><a data-google-vignette="false" href="<?php the_permalink(); ?>">التفاصيل</a></div><?php endif; ?></div>
</article>
<?php endwhile; ?></div><div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
<?php else: ?><div class="g-platform-empty"><?php echo a3g_icon($is_showroom?'store':'wrench'); ?><h2>لا توجد نتائج منظمة بهذه الفلاتر حاليًا</h2><p><?php echo $is_showroom?'جرّب تغيير الفلاتر أو تصفح أدلة المعارض المنشورة بالأسفل.':'تصفح أدلة مراكز الخدمة المنشورة بالأسفل للوصول إلى الفروع والمعلومات المتاحة الآن.'; ?></p></div><?php endif; ?>
<?php if(!$is_showroom): ?>
  <section class="g-legacy-bridge g-guide-results" aria-labelledby="service-guides-heading">
    <div class="g-section-head"><div><span>من مكتبة أعطال</span><h2 id="service-guides-heading"><?php echo $guide_brand || $guide_location ? 'أدلة مرتبطة باختيارك' : 'أدلة مراكز الخدمة المتاحة'; ?></h2><p>أدلة منشورة للفروع ووسائل الحجز؛ راجع اعتماد الفرع والخدمة المطلوبة داخل كل دليل قبل الزيارة.</p></div><b><?php echo esc_html(number_format_i18n(count($directory_guides))); ?> دليل ومقال</b></div>
    <?php if($directory_guides): ?><div class="g-news-grid g-legacy-grid"><?php foreach(array_slice($directory_guides,0,16) as $guide) a3g_card((int)$guide->ID,'g-legacy-card'); ?></div>
    <?php else: ?><p>لا يوجد دليل منشور مطابق للعلامة والمدينة المختارتين حاليًا. جرّب إزالة المدينة أو تغيير العلامة.</p><?php endif; ?>
    <div class="g-legacy-more"><a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(33)); ?>">تصفح كل أدلة مراكز الخدمة</a></div>
  </section>
<?php else: ?>
  <?php
    $guide_cat=get_category_by_slug('car-showrooms-guide');
    if($guide_cat):
      $guide_q=a3g_query(['cat'=>(int)$guide_cat->term_id,'posts_per_page'=>8]);
      if($guide_q->have_posts()):
  ?>
    <section class="g-showroom-guides">
      <div class="g-section-head">
        <div><span>BUYER INTELLIGENCE</span><h2>دليل الشراء من معارض السيارات</h2><p>مش مجرد عناوين فروع. هنا هتعرف تختار المعرض، تفهم العرض، تحجز Test Drive، وتقفل الحجز والاستلام من غير مفاجآت.</p></div>
        <a data-google-vignette="false" href="<?php echo esc_url(get_category_link($guide_cat)); ?>">كل أدلة المعارض</a>
      </div>
      <div class="g-showroom-guide-grid">
        <?php while($guide_q->have_posts()):$guide_q->the_post();a3g_card(get_the_ID(),'g-showroom-guide-card');endwhile;wp_reset_postdata(); ?>
      </div>
    </section>
  <?php endif; endif; ?>

  <?php a3g_legacy_section(
    [374,22],
    'قبل زيارة المعرض: الأسعار والمراجعات الحالية',
    'قارن السعر والمواصفات والمراجعة قبل ما تروح المعرض، وكل صفحة تفضل على رابطها الأصلي.',
    12,
    [],
    374
  ); ?>
<?php endif; ?>
</main><?php get_footer(); ?>