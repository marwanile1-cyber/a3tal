<?php
/**
 * A3TAL HOME EXACT REFERENCE 2026-11-04
 * Literal source-design layout and image crops; data-oriented WordPress links.
 * Vehicle photos taken from generated UI concept are illustrative, not factory photographs.
 */
defined('ABSPATH') || exit;
$ref_count = 0;
if (post_type_exists('a3_car_ref')) {
    $ref_stats = wp_count_posts('a3_car_ref');
    $ref_count = isset($ref_stats->publish) ? (int) $ref_stats->publish : 0;
}
?>
<div class="a3tal-reference-page" dir="rtl">
<section class="hero"><div class="wrap"><div class="red-sticker">دليلك الشامل<br>لعالم السيارات</div><div class="hero-copy"><h1><em>أعطال</em> موسوعة سيارات عربية</h1><p>مواصفات · أعطال وحلول · صيانة · أسعار · مراجعات · مقارنات</p><div class="hero-mobile-scene" role="img" aria-label="صورة تصميمية لسيارة حمراء في المدينة"></div><form class="hero-search" method="get" action="https://a3tal.com/" id="searchForm"><label for="query" class="sr">ابحث في الموقع</label><input id="query" name="s" placeholder="ابحث عن أي سيارة .. (اسم السيارة / الموديل)" required><button aria-label="ابدأ البحث" type="submit">⌕</button></form><div class="search-modes" role="group" aria-label="طرق البحث"><button data-mode="car" class="active">🚘 البحث بالموديل</button><button data-mode="code">⚙ بحث بالكود</button><button data-mode="compare">⚖ مقارنة سيارات</button><button data-mode="spec">▤ دليل المواصفات</button></div></div></div></section>
<section class="quickarea"><div class="wrap"><nav class="service-tiles" aria-label="أقسام موسوعة السيارات"><a href="https://a3tal.com/car-reference/" aria-label="دليل المواصفات الفنية"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-service-specs.webp')); ?>" alt="دليل المواصفات"></a><a href="https://a3tal.com/?s=مقارنة" aria-label="مقارنات السيارات"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-service-comparison.webp')); ?>" alt="مقارنات السيارات"></a><a href="https://a3tal.com/dtc/" aria-label="الأعطال والأكواد"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-service-dtc.webp')); ?>" alt="الأعطال والأكواد"></a><a href="https://a3tal.com/maintenance-schedules/" aria-label="الصيانة الدورية"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-service-maintenance.webp')); ?>" alt="الصيانة الدورية"></a><a href="https://a3tal.com/?s=تجهيزات" aria-label="تجهيزات وراحة"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-service-cabin.webp')); ?>" alt="تجهيزات وراحة"></a><a href="https://a3tal.com/?s=إطارات" aria-label="الإطارات"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-service-tires.webp')); ?>" alt="الإطارات"></a><a href="https://a3tal.com/?s=استهلاك الوقود" aria-label="استهلاك الوقود"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-service-fuel.webp')); ?>" alt="استهلاك الوقود"></a></nav></div></section>
<section class="brands-bar"><div class="wrap brands-grid"><div class="brand-heading"><span>╱</span> تصفّح حسب<br>الماركة</div><a class="brand" href="https://a3tal.com/car-reference/" aria-label="جيلي"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-geely.webp')); ?>" alt="جيلي"></a><a class="brand" href="https://a3tal.com/car-reference/" aria-label="تويوتا"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-toyota.webp')); ?>" alt="تويوتا"></a><a class="brand" href="https://a3tal.com/car-reference/kia/" aria-label="كيا"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-kia.webp')); ?>" alt="كيا"></a><a class="brand" href="https://a3tal.com/car-reference/hyundai/" aria-label="هيونداي"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-hyundai.webp')); ?>" alt="هيونداي"></a><a class="brand" href="https://a3tal.com/car-reference/nissan/" aria-label="نيسان"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-nissan.webp')); ?>" alt="نيسان"></a><a class="brand" href="https://a3tal.com/car-reference/mg/" aria-label="إم جي"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-mg.webp')); ?>" alt="MG"></a><a class="brand" href="https://a3tal.com/car-reference/chevrolet/" aria-label="شيفروليه"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-chevrolet.webp')); ?>" alt="شيفروليه"></a><a class="brand" href="https://a3tal.com/car-reference/" aria-label="بي واي دي"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-brand-byd.webp')); ?>" alt="BYD"></a><a class="allbrands" href="https://a3tal.com/car-reference/">عرض كل الماركات ‹</a></div></section>
<div class="wrap"><section class="catalog"><div class="panel cars-panel"><div class="panel-title"><h2>أحدث السيارات في دليل المواصفات</h2><a href="https://a3tal.com/car-reference/">عرض جميع الموديلات ←</a></div><div class="car-grid"><a class="carcard" href="https://a3tal.com/car-reference/mg/mg7-15-turbo-egypt/"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-model-mg7.webp')); ?>" alt="صورة MG7 توضيحية من التصميم المرجعي"><strong>MG7</strong><small>الموديل في الدليل</small><span class="btn">المواصفات الكاملة ←</span></a><a class="carcard" href="https://a3tal.com/car-reference/chevrolet/captiva-2026-egypt/"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-model-chevrolet-captiva.webp')); ?>" alt="صورة شيفروليه كابتيفا توضيحية من التصميم المرجعي"><strong>شيفروليه كابتيفا</strong><small>موديل 2026</small><span class="btn">المواصفات الكاملة ←</span></a><a class="carcard" href="https://a3tal.com/?s=هيونداي+توسان"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-model-hyundai-tucson.webp')); ?>" alt="سيارة SUV في التصميم المرجعي"><strong>هيونداي توسان</strong><small>مواصفات ومراجعات</small><span class="btn">اقرأ المزيد ←</span></a><a class="carcard" href="https://a3tal.com/?s=تويوتا+كورولا"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-model-toyota-corolla.webp')); ?>" alt="سيارة سيدان في التصميم المرجعي"><strong>تويوتا كورولا</strong><small>مواصفات ومراجعات</small><span class="btn">اقرأ المزيد ←</span></a></div></div><aside class="panel tools-panel"><h2>⚒ أدوات مهمة لكل مالك سيارة</h2><div class="toolgrid"><a href="https://a3tal.com/dtc/"><span>⚙</span>معرفة كود العطل</a><a href="https://a3tal.com/?s=صيانة"><span>▦</span>معلومات تكلفة الصيانة</a><a href="https://a3tal.com/?s=استهلاك+الوقود"><span>⛽</span>معلومات استهلاك الوقود</a><a href="https://a3tal.com/?s=مقاسات+الإطارات"><span>◉</span>مقاسات الإطارات</a><a href="https://a3tal.com/?s=فلتر+الهواء"><span>⚙</span>دليل قطع الغيار</a><a href="https://a3tal.com/maintenance-schedules/"><span>▣</span>جدول الصيانة</a></div></aside></section>
<section class="lower"><div class="panel maint-feature"><h2>▮ دليل الصيانة الدورية</h2><a href="https://a3tal.com/maintenance-schedules/"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-maintenance-feature.webp')); ?>" alt="صيانة سيارة كما في التصميم المرجعي"></a></div><div class="panel"><h2>▮ أحدث المقالات والتحليلات</h2><div class="article-list"><a href="https://a3tal.com/?s=الفرامل"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-article-brakes.webp')); ?>" alt="فرامل السيارة"><strong>علامات تآكل تيل الفرامل</strong></a><a href="https://a3tal.com/?s=البطارية"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-article-battery.webp')); ?>" alt="بطارية سيارة"><strong>أسباب ضعف البطارية</strong></a><a href="https://a3tal.com/?s=زيت+المحرك"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-article-oil.webp')); ?>" alt="زيت المحرك"><strong>اختيار زيت المحرك</strong></a></div></div><div class="panel"><h2>▮ أحدث المراجعات</h2><a class="review-card" href="https://a3tal.com/?s=توسان+2026"><img src="<?php echo esc_url(content_url('/uploads/2026/11/a3tal-ref-20261104-review-tucson.webp')); ?>" alt="سيارة من التصميم المرجعي"><strong>مراجعات السيارات ومواصفاتها</strong></a></div></section></div>
<section class="facts" aria-label="ملخص أقسام الموسوعة"><div class="wrap stats"><span><strong>أعطال.كوم</strong><br>موسوعة السيارات العربية</span><span><strong><?php echo esc_html(number_format_i18n($ref_count)); ?></strong><br>صفحة مواصفات فنية منشورة</span><span>أعطال وأكواد وتشخيص<br><em>معلومات منظمة للبحث</em></span><span>مواصفات وصيانة<br>دليل متكامل للسيارات</span></div></section>
<nav class="dock" aria-label="روابط سريعة للموبايل"><a class="active" href="https://a3tal.com/"><b>⌂</b>الرئيسية</a><a href="https://a3tal.com/car-reference/"><b>▤</b>الدليل</a><a href="https://a3tal.com/dtc/"><b>⚙</b>الأعطال</a><a href="https://a3tal.com/maintenance-schedules/"><b>◇</b>الصيانة</a><a href="https://a3tal.com/?s=مقارنة"><b>⋯</b>المزيد</a></nav>

<script id="a3tal-v5-home-interactions">
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