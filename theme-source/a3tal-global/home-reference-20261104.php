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
      <a class="hub-card" href="https://a3tal.com/car-reference/"><span class="hub-number" aria-hidden="true">01</span><strong>مواصفات السيارات</strong><small>موديلات وماركات</small></a>
      <a class="hub-card" href="https://a3tal.com/dtc/"><span class="hub-number" aria-hidden="true">02</span><strong>مكتبة الأعطال</strong><small>أكواد وتشخيص</small></a>
      <a class="hub-card" href="https://a3tal.com/motorcycles/"><span class="hub-number" aria-hidden="true">03</span><strong>الموتوسيكلات</strong><small>موديلات وسكوتر</small></a>
      <a class="hub-card" href="https://a3tal.com/parts/"><span class="hub-number" aria-hidden="true">04</span><strong>قطع الغيار</strong><small>أدلة وبيانات</small></a>
      <a class="hub-card" href="https://a3tal.com/maintenance-schedules/"><span class="hub-number" aria-hidden="true">05</span><strong>جداول الصيانة</strong><small>مواعيد ومتابعة</small></a>
      <a class="hub-card" href="https://a3tal.com/service-centers/"><span class="hub-number" aria-hidden="true">06</span><strong>مراكز الخدمة</strong><small>دليل المراكز</small></a>
    </nav>
  </div>
</section>
<section class="brands-bar"><div class="wrap brands-grid"><div class="brand-heading"><span>╱</span> تصفّح حسب<br>الماركة</div><a class="brand" href="https://a3tal.com/cars/?brand=geely" aria-label="جيلي"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-geely.webp')); ?>" alt="جيلي"></a><a class="brand" href="https://a3tal.com/?s=تويوتا" aria-label="تويوتا"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-toyota.webp')); ?>" alt="تويوتا"></a><a class="brand" href="https://a3tal.com/cars/?brand=kia" aria-label="كيا"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-kia.webp')); ?>" alt="كيا"></a><a class="brand" href="https://a3tal.com/cars/?brand=hyundai" aria-label="هيونداي"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-hyundai.webp')); ?>" alt="هيونداي"></a><a class="brand" href="https://a3tal.com/car-reference/nissan/" aria-label="نيسان"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-nissan.webp')); ?>" alt="نيسان"></a><a class="brand" href="https://a3tal.com/car-reference/mg/" aria-label="إم جي"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-mg.webp')); ?>" alt="MG"></a><a class="brand" href="https://a3tal.com/car-reference/chevrolet/" aria-label="شيفروليه"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-chevrolet.webp')); ?>" alt="شيفروليه"></a><a class="brand" href="https://a3tal.com/cars/?brand=byd" aria-label="بي واي دي"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-byd.webp')); ?>" alt="BYD"></a><a class="allbrands" href="https://a3tal.com/car-reference/">عرض كل الماركات ‹</a></div></section>
<div class="wrap"><section class="catalog"><div class="panel cars-panel"><div class="panel-title"><h2>أحدث موديلات السيارات</h2><a href="https://a3tal.com/cars/">عرض جميع الموديلات ←</a></div><div class="car-grid">
<?php if($home_ref_cards && $home_ref_cards->have_posts()): ?>
<?php while($home_ref_cards->have_posts()):$home_ref_cards->the_post();
$home_car_img=get_the_post_thumbnail_url(get_the_ID(),'medium_large');
if(!$home_car_img)$home_car_img=content_url('/uploads/2026/11/a3tal-ref-20261104-service-specs.webp');
?>
<a class="carcard" href="<?php the_permalink(); ?>">
<img loading="eager" decoding="async" width="320" height="180" src="<?php echo esc_url($home_car_img); ?>" alt="<?php echo esc_attr(get_the_title()); ?>">
<strong><?php echo esc_html(get_the_title()); ?></strong>
<small>أسعار ومواصفات • <?php echo esc_html(get_the_modified_date('Y/m/d')); ?></small>
<span class="btn">الأسعار والمواصفات ←</span></a>
<?php endwhile;wp_reset_postdata(); ?>
<?php else: ?>
<a class="carcard" href="https://a3tal.com/car-reference/mg/mg7-15-turbo-egypt/"><img width="320" height="180" loading="eager" src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-model-mg7.webp')); ?>" alt="تصميم توضيحي لسيارة MG7"><strong>MG7</strong><small>دليل المواصفات</small><span class="btn">عرض المواصفات ←</span></a>
<a class="carcard" href="https://a3tal.com/car-reference/chevrolet/captiva-2026-egypt/"><img width="320" height="180" loading="eager" src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-model-chevrolet-captiva.webp')); ?>" alt="تصميم توضيحي لشيفروليه كابتيفا"><strong>شيفروليه كابتيفا</strong><small>دليل المواصفات</small><span class="btn">عرض المواصفات ←</span></a>
<?php endif; ?>
</div></div><aside class="panel tools-panel"><h2>⚒ أدوات مهمة لكل مالك سيارة</h2><div class="toolgrid"><a href="https://a3tal.com/dtc/"><span>⚙</span>معرفة كود العطل</a><a href="https://a3tal.com/?s=صيانة"><span>▦</span>معلومات تكلفة الصيانة</a><a href="https://a3tal.com/?s=استهلاك+الوقود"><span>⛽</span>معلومات استهلاك الوقود</a><a href="https://a3tal.com/?s=مقاسات+الإطارات"><span>◉</span>مقاسات الإطارات</a><a href="https://a3tal.com/parts/"><span>⚙</span>دليل قطع الغيار</a><a href="https://a3tal.com/maintenance-schedules/"><span>▣</span>جدول الصيانة</a></div></aside></section>
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