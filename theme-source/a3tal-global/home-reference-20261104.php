<?php
/**
 * A3TAL HOME EXACT REFERENCE 2026-11-04
 * Literal source-design layout and image crops; data-oriented WordPress links.
 * Vehicle photos taken from generated UI concept are illustrative, not factory photographs.
 */
defined('ABSPATH') || exit;
$ref_count = 0;
$home_ref_cards = post_type_exists('a3_car') ? new WP_Query([
 'post_type'=>'a3_car','post_status'=>'publish','posts_per_page'=>4,
 'orderby'=>'modified','order'=>'DESC','no_found_rows'=>true,'ignore_sticky_posts'=>true
]) : null;
$home_latest_guides = new WP_Query([
 'post_type'=>'post','post_status'=>'publish','category__in'=>[8,13,2,18],
 'posts_per_page'=>3,'orderby'=>'date','order'=>'DESC','ignore_sticky_posts'=>true,'no_found_rows'=>true
]);
$home_latest_review = new WP_Query([
 'post_type'=>'post','post_status'=>'publish','cat'=>22,
 'posts_per_page'=>1,'orderby'=>'date','order'=>'DESC','ignore_sticky_posts'=>true,'no_found_rows'=>true
]);

// Reuse existing, already stable homepage car query; avoid extra home data scans.
$home_new_reference = post_type_exists('a3_car_ref') ? get_posts([
 'post_type'=>'a3_car_ref','post_status'=>'publish','numberposts'=>6,
 'orderby'=>'modified','order'=>'DESC'
]) : [];
if (post_type_exists('a3_car_ref')) {
    $ref_stats = wp_count_posts('a3_car_ref');
    $ref_count = isset($ref_stats->publish) ? (int) $ref_stats->publish : 0;
}
?>
<div class="a3tal-reference-page" dir="rtl">
<section class="hero"><div class="wrap"><div class="red-sticker">دليلك الشامل<br>لعالم السيارات</div><div class="hero-copy"><h1><em>أعطال.كوم</em> | دليلك الشامل للسيارات في مصر</h1><p>أسعار السيارات ومواصفاتها ومقارنتها، الأعطال والصيانة وقطع الغيار ومراكز الخدمة، ودليل الموتوسيكلات والسكوتر.</p><div class="hero-mobile-scene" role="img" aria-label="صورة تصميمية لسيارة حمراء في المدينة"></div><form class="hero-search" method="get" action="https://a3tal.com/" id="searchForm"><label for="query" class="sr">ابحث في الموقع</label><input id="query" name="s" placeholder="ابحث عن أي سيارة .. (اسم السيارة / الموديل)" required><button aria-label="ابدأ البحث" type="submit">⌕</button></form><div class="search-modes" role="group" aria-label="طرق البحث"><button data-mode="car" class="active">🚘 البحث بالموديل</button><button data-mode="code">⚙ بحث بالكود</button><button data-mode="compare">⚖ مقارنة سيارات</button><button data-mode="spec">▤ دليل المواصفات</button></div></div></div></section>
<section class="quickarea" aria-label="أقسام وأدلة أعطال.كوم">
  <div class="wrap">
    <nav class="service-tiles a3tal-hub-tiles" aria-label="أهم قواعد البيانات والأدلة">
      <a class="hub-card hub-card-visual" href="https://a3tal.com/car-reference/"><img class="hub-visual" loading="eager" decoding="async" width="360" height="180" src="https://a3tal.com/wp-content/uploads/2026/11/a3tal-ref-20261104-service-specs.webp" alt="" aria-hidden="true"><strong>مواصفات السيارات</strong><small>موديلات وماركات</small></a>
      <a class="hub-card hub-card-visual" href="https://a3tal.com/dtc/"><img class="hub-visual" loading="eager" decoding="async" width="360" height="180" src="https://a3tal.com/wp-content/uploads/2026/11/a3tal-ref-20261104-service-dtc.webp" alt="" aria-hidden="true"><strong>مكتبة الأعطال</strong><small>أكواد وتشخيص</small></a>
      <a class="hub-card hub-card-visual" href="https://a3tal.com/motorcycles/"><img class="hub-visual" loading="eager" decoding="async" width="360" height="180" src="https://a3tal.com/wp-content/uploads/2026/10/tvs-raider-125-egypt.webp" alt="" aria-hidden="true"><strong>الموتوسيكلات</strong><small>موديلات وسكوتر</small></a>
      <a class="hub-card hub-card-visual" href="https://a3tal.com/parts/"><img class="hub-visual" loading="eager" decoding="async" width="360" height="180" src="https://a3tal.com/wp-content/uploads/2026/10/a3tal-egypt-parts-market-20261026-hero-original-20261025-1024x576.webp" alt="" aria-hidden="true"><strong>قطع الغيار</strong><small>أدلة وبيانات</small></a>
      <a class="hub-card hub-card-visual" href="https://a3tal.com/maintenance-schedules/"><img class="hub-visual" loading="eager" decoding="async" width="360" height="180" src="https://a3tal.com/wp-content/uploads/2026/11/a3tal-ref-20261104-service-maintenance.webp" alt="" aria-hidden="true"><strong>جداول الصيانة</strong><small>مواعيد ومتابعة</small></a>
      <a class="hub-card hub-card-visual" href="https://a3tal.com/service-centers/"><img class="hub-visual" loading="eager" decoding="async" width="360" height="180" src="https://a3tal.com/wp-content/uploads/2026/10/a3tal-authorized_hero-real-photograph-20261022-1024x576.webp" alt="" aria-hidden="true"><strong>مراكز الخدمة</strong><small>دليل المراكز</small></a>
    </nav>
  </div>
</section>
<!-- A3TAL-EGYPT-BRANDS-20261108-BEGIN -->
<section class="brands-bar a3egy-brands" id="egypt-car-brands" aria-labelledby="a3egy-brands-heading">
 <div class="wrap">
  <div class="a3egy-section-heading"><div><small>اختار ماركتك</small><h2 id="a3egy-brands-heading">ابحث عن سيارتك</h2><p>افتح صفحة الماركة لتشوف الأسعار والموديلات والأعطال والمواصفات الفنية المنشورة عنها.</p></div><a class="a3egy-all" href="https://a3tal.com/cars/#cg-brands">كل الماركات ←</a></div>
  <nav class="a3egy-brands-grid" aria-label="ماركات السيارات في مصر">
   <a class="a3egy-brand" data-brand="toyota" href="https://a3tal.com/cars/?brand=toyota" aria-label="تصفح دليل تويوتا في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار تويوتا" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">TOYOTA</strong><span class="a3egy-brand-arabic">تويوتا</span></a>
   <a class="a3egy-brand" data-brand="hyundai" href="https://a3tal.com/cars/?brand=hyundai" aria-label="تصفح دليل هيونداي في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار هيونداي" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">HYUNDAI</strong><span class="a3egy-brand-arabic">هيونداي</span></a>
   <a class="a3egy-brand" data-brand="chevrolet" href="https://a3tal.com/cars/?brand=chevrolet" aria-label="تصفح دليل شيفروليه في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار شيفروليه" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">CHEVROLET</strong><span class="a3egy-brand-arabic">شيفروليه</span></a>
   <a class="a3egy-brand" data-brand="kia" href="https://a3tal.com/cars/?brand=kia" aria-label="تصفح دليل كيا في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار كيا" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">KIA</strong><span class="a3egy-brand-arabic">كيا</span></a>
   <a class="a3egy-brand" data-brand="nissan" href="https://a3tal.com/cars/?brand=nissan" aria-label="تصفح دليل نيسان في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار نيسان" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">NISSAN</strong><span class="a3egy-brand-arabic">نيسان</span></a>
   <a class="a3egy-brand" data-brand="mg" href="https://a3tal.com/cars/?brand=mg" aria-label="تصفح دليل إم جي في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار إم جي" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">MG</strong><span class="a3egy-brand-arabic">إم جي</span></a>
   <a class="a3egy-brand" data-brand="chery" href="https://a3tal.com/cars/?brand=chery" aria-label="تصفح دليل شيري في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار شيري" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">CHERY</strong><span class="a3egy-brand-arabic">شيري</span></a>
   <a class="a3egy-brand" data-brand="geely" href="https://a3tal.com/cars/?brand=geely" aria-label="تصفح دليل جيلي في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار جيلي" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">GEELY</strong><span class="a3egy-brand-arabic">جيلي</span></a>
   <a class="a3egy-brand" data-brand="jetour" href="https://a3tal.com/cars/?brand=jetour" aria-label="تصفح دليل جيتور في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار جيتور" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">JETOUR</strong><span class="a3egy-brand-arabic">جيتور</span></a>
   <a class="a3egy-brand" data-brand="jaecoo" href="https://a3tal.com/cars/?brand=jaecoo" aria-label="تصفح دليل جايكو في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار جايكو" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">JAECOO</strong><span class="a3egy-brand-arabic">جايكو</span></a>
   <a class="a3egy-brand" data-brand="byd" href="https://a3tal.com/cars/?brand=byd" aria-label="تصفح دليل بي واي دي في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار بي واي دي" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">BYD</strong><span class="a3egy-brand-arabic">بي واي دي</span></a>
   <a class="a3egy-brand" data-brand="renault" href="https://a3tal.com/cars/?brand=renault" aria-label="تصفح دليل رينو في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار رينو" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">RENAULT</strong><span class="a3egy-brand-arabic">رينو</span></a>
   <a class="a3egy-brand" data-brand="opel" href="https://a3tal.com/cars/?brand=opel" aria-label="تصفح دليل أوبل في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار أوبل" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">OPEL</strong><span class="a3egy-brand-arabic">أوبل</span></a>
   <a class="a3egy-brand" data-brand="suzuki" href="https://a3tal.com/cars/?brand=suzuki" aria-label="تصفح دليل سوزوكي في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار سوزوكي" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">SUZUKI</strong><span class="a3egy-brand-arabic">سوزوكي</span></a>
   <a class="a3egy-brand" data-brand="skoda" href="https://a3tal.com/cars/?brand=skoda" aria-label="تصفح دليل سكودا في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار سكودا" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">SKODA</strong><span class="a3egy-brand-arabic">سكودا</span></a>
   <a class="a3egy-brand" data-brand="changan" href="https://a3tal.com/cars/?brand=changan" aria-label="تصفح دليل شانجان في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار شانجان" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">CHANGAN</strong><span class="a3egy-brand-arabic">شانجان</span></a>
   <a class="a3egy-brand" data-brand="haval" href="https://a3tal.com/cars/?brand=haval" aria-label="تصفح دليل هافال في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار هافال" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">HAVAL</strong><span class="a3egy-brand-arabic">هافال</span></a>
   <a class="a3egy-brand" data-brand="gac" href="https://a3tal.com/cars/?brand=gac" aria-label="تصفح دليل جي إيه سي في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار جي إيه سي" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">GAC</strong><span class="a3egy-brand-arabic">جي إيه سي</span></a>
   <a class="a3egy-brand" data-brand="deepal" href="https://a3tal.com/cars/?brand=deepal" aria-label="تصفح دليل ديبال في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار ديبال" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">DEEPAL</strong><span class="a3egy-brand-arabic">ديبال</span></a>
   <a class="a3egy-brand" data-brand="soueast" href="https://a3tal.com/cars/?brand=soueast" aria-label="تصفح دليل سوإيست في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار سوإيست" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">SOUEAST</strong><span class="a3egy-brand-arabic">سوإيست</span></a>
   <a class="a3egy-brand" data-brand="dongfeng" href="https://a3tal.com/cars/?brand=dongfeng" aria-label="تصفح دليل دونج فينج في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار دونج فينج" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">DONGFENG</strong><span class="a3egy-brand-arabic">دونج فينج</span></a>
   <a class="a3egy-brand" data-brand="baic" href="https://a3tal.com/cars/?brand=baic" aria-label="تصفح دليل بايك في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار بايك" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">BAIC</strong><span class="a3egy-brand-arabic">بايك</span></a>
   <a class="a3egy-brand" data-brand="kgm" href="https://a3tal.com/cars/?brand=kgm" aria-label="تصفح دليل كي جي إم في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار كي جي إم" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">KGM</strong><span class="a3egy-brand-arabic">كي جي إم</span></a>
   <a class="a3egy-brand" data-brand="ford" href="https://a3tal.com/cars/?brand=ford" aria-label="تصفح دليل فورد في مصر"><span class="a3egy-brand-logo-wrap"><img class="a3egy-brand-logo" alt="شعار فورد" width="124" height="49" loading="lazy" decoding="async"></span><strong class="a3egy-brand-name-fallback" dir="ltr" lang="en">FORD</strong><span class="a3egy-brand-arabic">فورد</span></a>
  </nav>
 </div>
</section>
<!-- A3TAL-EGYPT-BRANDS-20261108-END -->
<!-- A3TAL-EGYPT-HOME-PRICES-20261108-BEGIN -->
<section class="a3egy-price-section" id="egypt-car-prices" aria-labelledby="a3egy-price-heading">
 <div class="wrap">
  <div class="a3egy-section-heading"><div><small>دليل الشراء في مصر</small><h2 id="a3egy-price-heading">أسعار السيارات الجديدة في مصر</h2><p>آخر مقالات الأسعار المنشورة، مع بيانات الموديل والفئات وتاريخ التحديث داخل كل مقال.</p></div><a class="a3egy-all" href="https://a3tal.com/cars/">عرض كل الأسعار ←</a></div>
  <div class="a3egy-price-grid">
  <?php if($home_ref_cards && $home_ref_cards->posts): ?>
    <?php foreach($home_ref_cards->posts as $car):
      $car_id=(int)$car->ID;
      $car_img=get_the_post_thumbnail_url($car_id,'medium_large');
      $price_post_id=(int)get_post_meta($car_id,'_a3_primary_price_post_id',true);
      $price_href=($price_post_id && get_post_status($price_post_id)==='publish') ? get_permalink($price_post_id) : get_permalink($car_id);
      $price_display=function_exists('a3cp_vehicle_price') ? a3cp_vehicle_price($car_id) : '';
    ?>
    <article class="a3egy-price-card"><a href="<?php echo esc_url($price_href); ?>">
      <?php if($car_img): ?><img loading="lazy" decoding="async" src="<?php echo esc_url($car_img); ?>" alt="<?php echo esc_attr(get_the_title($car_id)); ?>"><?php else: ?><div class="a3egy-photo-placeholder">دليل أسعار السيارات</div><?php endif; ?>
      <span class="a3egy-price-copy"><strong><?php echo esc_html(get_the_title($car_id)); ?></strong>
      <small><?php echo $price_display ? esc_html($price_display).' · ' : ''; ?>السعر والفئات والمواصفات ←</small></span>
    </a></article>
    <?php endforeach; ?>
  <?php else: ?><p>تصفح جميع موديلات وأسعار السيارات المنشورة في الدليل.</p><?php endif; ?>
  </div>
  <div class="a3egy-market-quick">
  <strong>سيارات منتشرة في مصر:</strong>
  <a href="https://a3tal.com/cars/?brand=nissan">نيسان صني</a>
  <a href="https://a3tal.com/cars/?brand=hyundai">هيونداي أكسنت</a>
  <a href="https://a3tal.com/cars/?brand=chevrolet">شيفروليه أوبترا</a>
  <a href="https://a3tal.com/cars/?brand=mg">MG5</a>
  <a href="https://a3tal.com/cars/?brand=chery">شيري أريزو 5</a>
  <a href="https://a3tal.com/cars/?brand=byd">BYD F3</a>
  <a href="https://a3tal.com/cars/?brand=geely">جيلي كول راي</a>
  <a href="https://a3tal.com/cars/?brand=jetour">جيتور X70</a>
  </div>
 </div>
</section>
<!-- A3TAL-EGYPT-HOME-PRICES-20261108-END -->
<!-- A3TAL-EGYPT-HOME-PSEO-20261108-BEGIN -->
<section class="a3egy-reference-section" id="egypt-pseo" aria-labelledby="a3egy-reference-heading">
 <div class="wrap">
  <div class="a3egy-section-heading"><div><small>موسوعة المواصفات الفنية</small><h2 id="a3egy-reference-heading"><?php echo esc_html(number_format_i18n($ref_count)); ?> صفحة مواصفات فنية منشورة</h2><p>المحركات والفتيس والمقاسات والعفشة والأمان، حسب الماركة والموديل والفئة.</p></div><a class="a3egy-all" href="https://a3tal.com/car-reference/">الدليل الفني كاملًا ←</a></div>
  <div class="a3egy-reference-grid">
  <?php foreach($home_new_reference as $ref_entry): ?>
    <a class="a3egy-reference-card" href="<?php echo esc_url(get_permalink($ref_entry)); ?>">
    <?php $img=get_the_post_thumbnail_url($ref_entry->ID,'medium');if($img): ?><img loading="lazy" decoding="async" src="<?php echo esc_url($img); ?>" alt="<?php echo esc_attr(get_the_title($ref_entry)); ?>"><?php endif; ?>
    <strong><?php echo esc_html(get_the_title($ref_entry)); ?></strong><span>عرض المواصفات ←</span></a>
  <?php endforeach; ?>
 </div>
</section>
<!-- A3TAL-EGYPT-HOME-PSEO-20261108-END -->
<!-- A3TAL-EGYPT-BRAND-LOGO-ASSET-20261108 -->
<link rel="stylesheet" href="<?php echo esc_url(get_template_directory_uri().'/egypt-home-brand-logos-20261108.css?ver=20261108.3'); ?>">
<script src="<?php echo esc_url(get_template_directory_uri().'/assets/js/egypt-home-brand-logos-20261108.js'); ?>" defer></script>
<div class="wrap"><section class="catalog"><div class="panel cars-panel"><div class="panel-title"><h2>أحدث موديلات السيارات</h2><a href="https://a3tal.com/cars/">عرض جميع الموديلات ←</a></div><div class="car-grid">
<?php if($home_ref_cards && $home_ref_cards->have_posts()): ?>
<?php while($home_ref_cards->have_posts()):$home_ref_cards->the_post();
$home_car_img=get_the_post_thumbnail_url(get_the_ID(),'medium_large');
if(!$home_car_img)$home_car_img=content_url('/uploads/2026/11/a3tal-ref-20261104-service-specs.webp');
$home_main_post_id=(int)get_post_meta(get_the_ID(),'_a3_primary_price_post_id',true);
$home_main_post_url=($home_main_post_id && get_post_type($home_main_post_id)==='post' && get_post_status($home_main_post_id)==='publish') ? get_permalink($home_main_post_id) : get_permalink();
?>
<a class="carcard" href="<?php echo esc_url($home_main_post_url); ?>">
<img loading="eager" decoding="async" width="320" height="180" src="<?php echo esc_url($home_car_img); ?>" alt="<?php echo esc_attr(get_the_title()); ?>">
<strong><?php echo esc_html(get_the_title()); ?></strong>
<small>أسعار ومواصفات • <?php echo esc_html(get_the_modified_date('Y/m/d')); ?></small>
<span class="btn">الأسعار والمواصفات ←</span></a>
<?php endwhile;wp_reset_postdata(); ?>
<?php else: ?>
<a class="carcard" href="https://a3tal.com/car-reference/mg/mg7-15-turbo-egypt/"><img width="320" height="180" loading="eager" src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-model-mg7.webp')); ?>" alt="تصميم توضيحي لسيارة MG7"><strong>MG7</strong><small>دليل المواصفات</small><span class="btn">عرض المواصفات ←</span></a>
<a class="carcard" href="https://a3tal.com/car-reference/chevrolet/captiva-2026-egypt/"><img width="320" height="180" loading="eager" src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-model-chevrolet-captiva.webp')); ?>" alt="تصميم توضيحي لشيفروليه كابتيفا"><strong>شيفروليه كابتيفا</strong><small>دليل المواصفات</small><span class="btn">عرض المواصفات ←</span></a>
<?php endif; ?>
</div></div><aside class="panel tools-panel"><h2>⚒ أدوات مهمة لكل مالك سيارة</h2><div class="toolgrid"><a href="https://a3tal.com/fault-diagnosis/"><span>⚙</span>مشخّص الأعطال الذكي</a><a href="https://a3tal.com/car-tools/#maintenance-cost"><span>▦</span>احسب تكلفة الصيانة</a><a href="https://a3tal.com/car-tools/#fuel-use"><span>⛽</span>احسب استهلاك البنزين</a><a href="https://a3tal.com/car-tires-prices-egypt-2026/"><span>◉</span>دليل مقاسات الكاوتش</a><a href="https://a3tal.com/parts/"><span>⚙</span>دليل قطع الغيار</a><a href="https://a3tal.com/maintenance-schedules/"><span>▣</span>جدول الصيانة</a></div></aside></section>
<section class="lower"><div class="panel maint-feature"><h2>▮ دليل الصيانة الدورية</h2><a href="https://a3tal.com/maintenance-schedules/"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-maintenance-feature.webp')); ?>" alt="صيانة سيارة كما في التصميم المرجعي"></a></div><div class="panel"><h2>▮ أحدث المقالات والتحليلات</h2><div class="article-list">
<?php if($home_latest_guides->have_posts()): ?>
<?php while($home_latest_guides->have_posts()):$home_latest_guides->the_post();
$guide_img=get_the_post_thumbnail_url(get_the_ID(),'medium');
if(!$guide_img)$guide_img=content_url('/uploads/2026/11/a3tal-ref-20261104-article-brakes.webp');
?>
<a href="<?php the_permalink(); ?>"><img loading="lazy" decoding="async" width="220" height="130" src="<?php echo esc_url($guide_img); ?>" alt="<?php echo esc_attr(get_the_title()); ?>"><strong><?php echo esc_html(get_the_title()); ?></strong></a>
<?php endwhile;wp_reset_postdata(); ?>
<?php endif; ?>
</div></div><div class="panel"><h2>▮ أحدث المراجعات</h2><?php if($home_latest_review->have_posts()):$home_latest_review->the_post();
$review_img=get_the_post_thumbnail_url(get_the_ID(),'medium_large');
if(!$review_img)$review_img=content_url('/uploads/2026/11/a3tal-ref-20261104-review-tucson.webp');
?>
<a class="review-card" href="<?php the_permalink(); ?>"><img loading="lazy" decoding="async" width="360" height="180" src="<?php echo esc_url($review_img); ?>" alt="<?php echo esc_attr(get_the_title()); ?>"><strong><?php echo esc_html(get_the_title()); ?></strong>
<?php wp_reset_postdata(); ?>
<?php else: ?>
<a class="review-card" href="<?php echo esc_url(a3g_cat_link(22)); ?>"><img loading="lazy" decoding="async" width="360" height="180" src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-review-tucson.webp')); ?>" alt="مراجعات السيارات"><strong>تصفح مراجعات السيارات</strong>
<?php endif; ?>
</a></div></section></div>
<section class="facts" aria-label="ملخص أقسام الموسوعة"><div class="wrap stats"><span><strong>أعطال.كوم</strong><br>موسوعة السيارات العربية</span><span><strong><?php echo esc_html(number_format_i18n($ref_count)); ?></strong><br>صفحة مواصفات فنية منشورة</span><span>أعطال وأكواد وتشخيص<br><em>معلومات منظمة للبحث</em></span><span>مواصفات وصيانة<br>دليل متكامل للسيارات</span></div></section>
<nav class="dock" aria-label="روابط سريعة للموبايل"><a class="active" href="https://a3tal.com/"><b>⌂</b>الرئيسية</a><a href="https://a3tal.com/car-reference/"><b>▤</b>الدليل</a><a href="https://a3tal.com/dtc/"><b>⚙</b>الأعطال</a><a href="https://a3tal.com/maintenance-schedules/"><b>◇</b>الصيانة</a><a href="https://a3tal.com/?s=مقارنة"><b>⋯</b>المزيد</a></nav>

<script id="a3tal-v5-home-interactions" data-no-defer="1" data-no-optimize="1" data-no-delay="1">
(function(){
  function init(){
    var root=document.querySelector('.a3tal-reference-page:not(.a3r-site-header)');
    if(!root || root.dataset.a3talV5Bound==='1')return;
    root.dataset.a3talV5Bound='1';
    var modes={
      car:{target:'https://a3tal.com/',name:'s',placeholder:'ابحث باسم السيارة أو الموديل'},
      code:{target:'https://a3tal.com/dtc/',name:'code',placeholder:'مثال: P0420'},
      compare:{target:'https://a3tal.com/',name:'s',placeholder:'ابحث عن مقارنة بين سيارتين'},
      spec:{target:'https://a3tal.com/car-reference/',name:'q',placeholder:'ابحث عن مواصفات الموديل'}
    };
    root.addEventListener('click',function(e){
      var button=e.target.closest('button[data-mode]');
      if(!button || !root.contains(button))return;
      var mode=modes[button.dataset.mode];
      var form=root.querySelector('#searchForm'),input=root.querySelector('#query');
      if(!mode || !form || !input)return;
      root.querySelectorAll('[data-mode]').forEach(function(el){el.classList.remove('active');});
      button.classList.add('active');
      form.action=mode.target;
      input.name=mode.name;
      input.placeholder=mode.placeholder;
      input.value='';
      input.focus();
    });
    var menu=document.querySelector('.a3r-site-header #menuToggle');
    var nav=document.querySelector('.a3r-site-header .desktop-nav');
    if(menu && nav)menu.addEventListener('click',function(){
      var opened=nav.classList.toggle('is-open');
      menu.setAttribute('aria-expanded',String(opened));
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
</script>
</div>