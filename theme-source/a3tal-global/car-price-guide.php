<?php
/**
 * A3tal car pricing discovery page.
 * Existing /cars/ archive, model permalinks and editorial category URLs stay unchanged.
 * Published data only: no fabricated price, availability or timestamp.
 */
if (!defined('ABSPATH')) exit;
$cg_url = get_post_type_archive_link('a3_car') ?: home_url('/cars/');
$cg_car_ids = get_posts([
  'post_type'=>'a3_car','post_status'=>'publish','posts_per_page'=>-1,
  'fields'=>'ids','no_found_rows'=>true,'suppress_filters'=>false
]);
$cg_brands = $cg_car_ids ? get_terms([
  'taxonomy'=>'a3_brand','object_ids'=>$cg_car_ids,'hide_empty'=>true,
  'orderby'=>'name','order'=>'ASC'
]) : [];
if (is_wp_error($cg_brands)) $cg_brands = [];
$cg_markets = $cg_car_ids ? get_terms(['taxonomy'=>'a3_market','object_ids'=>$cg_car_ids,'hide_empty'=>true]) : [];
if (is_wp_error($cg_markets)) $cg_markets = [];
$cg_bodies = $cg_car_ids ? get_terms(['taxonomy'=>'a3_car_body','object_ids'=>$cg_car_ids,'hide_empty'=>true]) : [];
if (is_wp_error($cg_bodies)) $cg_bodies = [];
$cg_search = isset($_GET['car_search']) && is_string($_GET['car_search']) ? trim(sanitize_text_field(wp_unslash($_GET['car_search']))) : '';
$cg_search = function_exists('mb_substr') ? mb_substr($cg_search,0,85) : substr($cg_search,0,85);
$cg_brand = get_query_var('brand');
$cg_market = get_query_var('market');
$cg_body = get_query_var('vehicle_type');
$cg_year = get_query_var('year');
$cg_archive_filtered = $cg_search !== '' || isset($_GET['brand']) || isset($_GET['market']) || isset($_GET['vehicle_type']) || isset($_GET['year']);
// WordPress interprets ?s= as a global site search and may swap this archive
// for index.php. Use a scoped, paginated vehicle-only search instead.
$cg_listing = $GLOBALS['wp_query'];
if ($cg_search !== '') {
  $cg_tax_query = ['relation'=>'AND'];
  foreach (['brand'=>'a3_brand','market'=>'a3_market','vehicle_type'=>'a3_car_body'] as $param=>$taxonomy) {
    $raw = isset($_GET[$param]) && is_string($_GET[$param]) ? sanitize_title(wp_unslash($_GET[$param])) : '';
    if ($raw !== '') $cg_tax_query[] = ['taxonomy'=>$taxonomy,'field'=>'slug','terms'=>[$raw]];
  }
  $cg_args = [
    'post_type'=>'a3_car','post_status'=>'publish','s'=>$cg_search,
    'posts_per_page'=>20,'paged'=>max(1,(int)get_query_var('paged')),
    'orderby'=>'date','order'=>'DESC',
    'ignore_sticky_posts'=>true
  ];
  if (count($cg_tax_query)>1) $cg_args['tax_query']=$cg_tax_query;
  if (isset($_GET['year']) && is_scalar($_GET['year'])) {
    $requested_year=absint($_GET['year']);
    if($requested_year>=1950 && $requested_year<=2100)
      $cg_args['meta_query']=[['key'=>'_a3_year','value'=>(string)$requested_year,'compare'=>'=']];
  }
  $cg_listing = new WP_Query($cg_args);
}
$cg_all = $cg_listing->posts ?? [];
$cg_top = array_slice($cg_all,0,6);
$cg_more = array_slice($cg_all,6);
$cg_hero_ids = get_posts([
  'post_type'=>'a3_car','post_status'=>'publish','posts_per_page'=>7,
  'fields'=>'ids','no_found_rows'=>true,'meta_query'=>[['key'=>'_thumbnail_id','compare'=>'EXISTS']]
]);
$cg_hero_ids = array_slice($cg_hero_ids,0,3);
$cg_price_updates = new WP_Query([
  'post_type'=>'post','post_status'=>'publish','cat'=>374,'posts_per_page'=>5,
  'orderby'=>'date','order'=>'DESC','no_found_rows'=>true,'ignore_sticky_posts'=>true
]);
// Scoped assets: only the cars archive, never motorcycle, DTC or posts.
wp_enqueue_style('a3tal-car-price-guide',get_template_directory_uri().'/car-price-guide.css',[], '1.0.0');
wp_enqueue_script('a3tal-car-price-logos',get_template_directory_uri().'/car-price-brand-logos.js',[], '1.0.0',true);
wp_enqueue_script('a3tal-car-price-guide',get_template_directory_uri().'/car-price-guide.js',['a3tal-car-price-logos'],'1.0.0',true);
// Fix the unhelpful default archive SEO title, without changing any URLs.
add_filter('wpseo_title',static function($title){return is_post_type_archive('a3_car')?'أسعار السيارات في مصر | الموديلات والمواصفات وأحدث التحديثات | أعطال.كوم':$title;},120);
add_filter('wpseo_metadesc',static function($desc){return is_post_type_archive('a3_car')?'تصفح أسعار السيارات الجديدة في مصر حسب الماركة والموديل والسنة، واستعرض المواصفات والفئات وأحدث تحديثات الأسعار والمقارنات المنشورة على أعطال.كوم.':$desc;},120);
add_filter('wpseo_opengraph_title',static function($title){return is_post_type_archive('a3_car')?'أسعار السيارات في مصر | دليل أعطال.كوم':$title;},120);
add_filter('document_title_parts',static function($parts){if(is_post_type_archive('a3_car'))$parts['title']='أسعار السيارات في مصر | دليل أعطال.كوم';return $parts;},120);
if ($cg_archive_filtered) {
  add_filter('wpseo_robots',static function($robots){return is_post_type_archive('a3_car')?'noindex, follow':$robots;},120);
}
// Present only published price metadata from the original vehicle record.
$cg_render_card = static function($car) {
  $id = (int)$car->ID;
  $brand = a3g_first_term($id,'a3_brand');
  $year = (string)get_post_meta($id,'_a3_year',true);
  $price = function_exists('a3cp_vehicle_price') ? a3cp_vehicle_price($id) : '';
  $checked = get_post_meta($id,'_a3_source_checked_at',true);
  $href = get_permalink($id);
  ?>
  <article class="cg-car-card">
    <a class="cg-car-photo" href="<?php echo esc_url($href); ?>" aria-label="<?php echo esc_attr('عرض تفاصيل '.get_the_title($id)); ?>">
      <?php if (has_post_thumbnail($id)) echo get_the_post_thumbnail($id,'medium_large',['loading'=>'lazy','decoding'=>'async','alt'=>get_the_title($id)]); else echo '<span class="cg-photo-empty">A3TAL CARS</span>'; ?>
      <?php if ($year): ?><span class="cg-year-badge"><?php echo esc_html($year); ?></span><?php endif; ?>
    </a>
    <div class="cg-car-info">
      <div class="cg-car-meta"><?php if($brand): ?><span><?php echo esc_html($brand); ?></span><?php endif; ?><span>سيارة جديدة</span></div>
      <h3><a href="<?php echo esc_url($href); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3>
      <?php if ($price): ?><p class="cg-price" dir="auto"><?php echo esc_html($price); ?></p><?php else: ?><p class="cg-no-price">السعر قيد المراجعة</p><?php endif; ?>
      <?php if($checked): ?><small class="cg-checked">آخر مراجعة: <?php echo esc_html($checked); ?></small><?php endif; ?>
      <a class="cg-car-more" href="<?php echo esc_url($href); ?>">الأسعار والمواصفات <span aria-hidden="true">←</span></a>
    </div>
  </article>
  <?php
};
get_header();
?>
<main class="cg-guide" id="car-prices-guide" dir="rtl">
  <section class="cg-hero" aria-labelledby="cg-title">
    <div class="cg-hero-cars" aria-hidden="true">
      <?php foreach($cg_hero_ids as $h_id): ?>
        <div class="cg-hero-photo"><?php echo get_the_post_thumbnail($h_id,'large',['loading'=>'eager','decoding'=>'async','alt'=>'']); ?></div>
      <?php endforeach; ?>
    </div>
    <div class="cg-hero-shade"></div>
    <div class="cg-container cg-hero-content">
      <span class="cg-eyebrow">A3TAL CAR PRICES • EGYPT</span>
      <h1 id="cg-title">أسعار السيارات في مصر</h1>
      <p>دليل السيارات الجديدة والمواصفات والفئات والمقارنات، من بيانات الموديلات والمقالات المنشورة بالفعل على أعطال.كوم.</p>
      <form class="cg-search" role="search" action="<?php echo esc_url($cg_url); ?>" method="get">
        <label class="screen-reader-text" for="cg-car-search">ابحث عن سيارة أو موديل</label>
        <input type="search" id="cg-car-search" name="car_search" placeholder="ابحث عن سيارة... تويوتا، كيا، جيلي، نيسان" value="<?php echo esc_attr($cg_search); ?>" maxlength="85">
        <button type="submit" aria-label="ابحث في دليل السيارات"><?php echo a3g_icon('search'); ?><span>ابحث</span></button>
      </form>
      <nav class="cg-quick" aria-label="التنقل في دليل السيارات">
        <a class="is-active" href="#cg-popular"><?php echo a3g_icon('car'); ?><span>جديدة</span></a>
        <a href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>"><?php echo a3g_icon('car'); ?><span>مستعملة</span></a>
        <a href="#cg-all"><?php echo a3g_icon('search'); ?><span>مواصفات</span></a>
        <a href="#cg-brands"><?php echo a3g_icon('menu'); ?><span>الماركات</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(21)); ?>"><?php echo a3g_icon('car'); ?><span>مقارنة</span></a>
      </nav>
    </div>
  </section>

  <div class="cg-container">
    <section class="cg-brands cg-surface" id="cg-brands" aria-labelledby="cg-brands-title">
      <div class="cg-section-heading"><div><span class="cg-kicker">تصفح السيارات</span><h2 id="cg-brands-title">تصفح حسب الماركة</h2></div><a href="#cg-filters">كل الماركات والفلاتر ←</a></div>
      <?php if ($cg_brands): ?>
      <div class="cg-brands-grid">
        <?php foreach(array_slice($cg_brands,0,18) as $term): ?>
          <a class="cg-brand" data-brand-name="<?php echo esc_attr($term->name); ?>" href="<?php echo esc_url(add_query_arg('brand',$term->slug,$cg_url)); ?>">
            <span class="cg-brand-icon" aria-hidden="true"><?php echo esc_html(function_exists('mb_substr') ? mb_substr($term->name,0,2) : substr($term->name,0,2)); ?></span>
            <span class="cg-brand-name"><?php echo esc_html($term->name); ?></span>
          </a>
        <?php endforeach; ?>
      </div>
      <?php else: ?><p>الماركات هتظهر هنا بمجرد نشر موديل مرتبط بماركة.</p><?php endif; ?>
    </section>

    <div class="cg-discovery-layout">
      <aside class="cg-news cg-surface" id="cg-news" aria-labelledby="cg-news-title">
        <div class="cg-section-heading"><div><span class="cg-kicker">من غرفة الأخبار</span><h2 id="cg-news-title">أحدث تحديثات الأسعار</h2></div></div>
        <?php if($cg_price_updates->have_posts()): ?>
        <div class="cg-news-list"><?php while($cg_price_updates->have_posts()):$cg_price_updates->the_post(); ?>
          <article class="cg-news-row">
            <a class="cg-news-image" href="<?php the_permalink(); ?>"><?php if(has_post_thumbnail())the_post_thumbnail('thumbnail',['loading'=>'lazy','decoding'=>'async']); ?></a>
            <div><h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3><time datetime="<?php echo esc_attr(get_the_date('c')); ?>"><?php echo esc_html(get_the_date('j F Y')); ?></time></div>
          </article>
        <?php endwhile;wp_reset_postdata(); ?></div>
        <?php endif; ?>
        <a class="cg-secondary-link" href="<?php echo esc_url(a3g_cat_link(374)); ?>">كل أخبار وأسعار السيارات ←</a>
      </aside>

      <div class="cg-models-col">
        <section class="cg-surface cg-models-section" id="cg-popular" aria-labelledby="cg-popular-title">
          <div class="cg-section-heading"><div><span class="cg-kicker">موديلات منشورة ومعلومات فعلية</span><h2 id="cg-popular-title">أحدث السيارات في الدليل</h2></div><span class="cg-total"><?php echo esc_html(number_format_i18n((int)$cg_listing->found_posts)); ?> نتيجة</span></div>
          <?php if($cg_top): ?><div class="cg-cars-grid"><?php foreach($cg_top as $car){$cg_render_card($car);} ?></div><?php else: ?><p class="cg-empty">مفيش موديلات مطابقة للفلاتر دي حاليًا. جرّب مسح الفلاتر أو اسم موديل تاني.</p><?php endif; ?>
        </section>
      </div>
    </div>

    <section class="cg-benefits" aria-label="مميزات دليل السيارات">
      <div><span class="cg-benefit-symbol">↗</span><strong>تحديثات السوق</strong><small>مقالات الأسعار المنشورة</small></div>
      <div><span class="cg-benefit-symbol">⇄</span><strong>مقارنات السيارات</strong><small>مواصفات وتجهيزات</small></div>
      <div><span class="cg-benefit-symbol">▤</span><strong>المواصفات والفئات</strong><small>تفاصيل موثقة عند توفرها</small></div>
      <div><span class="cg-benefit-symbol">🚘</span><strong>جديدة ومستعملة</strong><small>دليل الموديلات وسوق السيارات</small></div>
      <div><span class="cg-benefit-symbol">✓</span><strong>أسعار قيد المراجعة</strong><small>تاريخ التحقق عند توفره</small></div>
    </section>

    <section class="cg-surface cg-all" id="cg-all" aria-labelledby="cg-all-title">
      <div class="cg-section-heading"><div><span class="cg-kicker">قائمة الموديلات</span><h2 id="cg-all-title">كل السيارات والفئات المتاحة</h2><p>استخدم الفلاتر لتضييق النتائج. روابط السيارات القديمة محفوظة بدون تعديل.</p></div><a href="<?php echo esc_url($cg_url); ?>">إعادة ضبط البحث ←</a></div>
      <form class="cg-filter" id="cg-filters" method="get" action="<?php echo esc_url($cg_url); ?>">
        <label>اسم السيارة<input name="car_search" type="search" maxlength="85" value="<?php echo esc_attr($cg_search); ?>" placeholder="موديل أو ماركة"></label>
        <label>الماركة<select name="brand"><option value="">كل الماركات</option><?php foreach($cg_brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected($cg_brand,$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
        <label>السوق<select name="market"><option value="">كل الأسواق</option><?php foreach($cg_markets as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected($cg_market,$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
        <label>الهيكل<select name="vehicle_type"><option value="">كل الأنواع</option><?php foreach($cg_bodies as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected($cg_body,$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
        <label>سنة الموديل<input type="number" name="year" min="1950" max="2100" value="<?php echo esc_attr($cg_year ? absint($cg_year) : ''); ?>" placeholder="2027"></label>
        <button type="submit">تطبيق الفلاتر</button>
      </form>
      <?php if($cg_more): ?><div class="cg-cars-grid cg-cars-rest"><?php foreach($cg_more as $car){$cg_render_card($car);} ?></div><?php endif; ?>
      <?php if($cg_top): ?><div class="cg-pagination"><?php if($cg_search !== ''):
            echo paginate_links([
              'total'=>max(1,(int)$cg_listing->max_num_pages),
              'current'=>max(1,(int)get_query_var('paged')),
              'prev_text'=>'السابق','next_text'=>'التالي',
              'add_args'=>['car_search'=>$cg_search]
            ]);
          else:
            the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']);
          endif; ?></div><?php endif; ?>
    </section>

    <section class="cg-guides" aria-labelledby="cg-guide-links">
      <div class="cg-section-heading"><div><span class="cg-kicker">خطوتك التالية</span><h2 id="cg-guide-links">اختار عربيتك بمعلومات أوضح</h2></div></div>
      <div class="cg-guide-links">
        <a href="<?php echo esc_url(a3g_cat_link(374)); ?>"><b>أخبار الأسعار</b><span>آخر التغييرات المنشورة في السوق المصري ←</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(22)); ?>"><b>مراجعات السيارات</b><span>تفاصيل القيادة والتجهيزات ←</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(21)); ?>"><b>مقارنات قبل الشراء</b><span>قارن السيارات المتقاربة ←</span></a>
        <a href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>"><b>السيارات المستعملة</b><span>إعلانات السيارات المنشورة ←</span></a>
      </div>
    </section>
    <p class="cg-disclaimer">الأسعار المعروضة مأخوذة من سجلات السيارات المنشورة على أعطال.كوم وقد تتغير لدى الوكيل أو المعرض. راجع تاريخ المراجعة والمصدر وصفحة السيارة قبل اتخاذ قرار شراء. أسعار المستعمل تختلف حسب الحالة وسنة الصنع والمسافة المقطوعة.</p>
  </div>
</main>
<?php get_footer(); ?>
