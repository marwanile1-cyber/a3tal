<?php
get_header();

$hero_q=a3g_query(['cat'=>374,'posts_per_page'=>1]);
$hero_id=0;$hero_img_id=0;
if($hero_q->have_posts()){ $hero_q->the_post(); $hero_id=get_the_ID(); $hero_img_id=get_post_thumbnail_id($hero_id); }
wp_reset_postdata();

$faults=a3g_query(['category__in'=>[8,13,2,18],'posts_per_page'=>4]);

/* A3TAL-HOME-RECENT-VEHICLES-AND-ARTICLES-20261022
 * Vehicle entities are NOT the same as editorial buying guides. Show both,
 * label them separately, and sort actual car profiles by their last update.
 * New category-374 prices and category-22 reviews appear automatically. */
$cars=new WP_Query([
  'post_type'=>'a3_car',
  'post_status'=>'publish',
  'posts_per_page'=>4,
  'orderby'=>'modified',
  'order'=>'DESC',
  'ignore_sticky_posts'=>true,
  'no_found_rows'=>true,
]);
$car_editorials=new WP_Query([
  'post_type'=>'post',
  'post_status'=>'publish',
  'category__in'=>[374,22,21],
  'posts_per_page'=>4,
  'orderby'=>'date',
  'order'=>'DESC',
  'ignore_sticky_posts'=>true,
  'no_found_rows'=>true,
]);
$moto_articles=new WP_Query([
  'post_type'=>'post',
  'post_status'=>'publish',
  'cat'=>3028,
  'posts_per_page'=>3,
  'orderby'=>'date',
  'order'=>'DESC',
  'ignore_sticky_posts'=>true,
  'no_found_rows'=>true,
]);
$home_editorial_ids = wp_list_pluck($car_editorials->posts, 'ID');
$prices=a3g_query(['cat'=>374,'posts_per_page'=>4,'post__not_in'=>$home_editorial_ids]);
$home_seen_posts=array_values(array_unique(array_merge($home_editorial_ids,wp_list_pluck($prices->posts,'ID'),wp_list_pluck($faults->posts,'ID'),wp_list_pluck($moto_articles->posts,'ID'))));
$news=a3g_query(['posts_per_page'=>4,'post__not_in'=>$home_seen_posts]);
$motos=new WP_Query(['post_type'=>'a3_motorcycle','post_status'=>'publish','posts_per_page'=>3,'ignore_sticky_posts'=>true]);
$dtcs=new WP_Query(['post_type'=>'a3_dtc','post_status'=>'publish','posts_per_page'=>4,'ignore_sticky_posts'=>true]);
$parts=new WP_Query(['post_type'=>'a3_part','post_status'=>'publish','posts_per_page'=>4,'ignore_sticky_posts'=>true]);
$listings=new WP_Query(['post_type'=>'a3_listing','post_status'=>'publish','posts_per_page'=>3,'ignore_sticky_posts'=>true]);
$centers=new WP_Query(['post_type'=>'a3_service_center','post_status'=>'publish','posts_per_page'=>3,'ignore_sticky_posts'=>true]);
$showrooms=new WP_Query(['post_type'=>'a3_showroom','post_status'=>'publish','posts_per_page'=>3,'ignore_sticky_posts'=>true]);

$ref_archive=post_type_exists('a3_car_ref')?(get_post_type_archive_link('a3_car_ref')?:home_url('/car-reference/')):home_url('/car-reference/');
$ref_published=0;
if(post_type_exists('a3_car_ref')){
  $ref_count_obj=wp_count_posts('a3_car_ref');
  $ref_published=(int)($ref_count_obj->publish??0);
}
$ref_examples=[
  ['path'=>'chevrolet/captiva-2026-egypt','brand'=>'CHEVROLET · 2026','short'=>'شيفروليه كابتيفا 2026','note'=>'المحرك والفتيس والإطارات والمقاعد'],
  ['path'=>'mg/mg-gt-15t-egypt','brand'=>'MG · GT','short'=>'MG GT تيربو','note'=>'الفتيس والمقاسات والتجهيزات'],
  ['path'=>'mg/mg7-15-turbo-egypt','brand'=>'MG · MG7','short'=>'MG7 تيربو','note'=>'الفروق بين Luxury وTrophy'],
];
$ref_brands=['mg'=>'إم جي','chevrolet'=>'شيفروليه','kia'=>'كيا','nissan'=>'نيسان','hyundai'=>'هيونداي'];

?>
<main class="g-home g-home-platform">

<!-- PREVIEW ONLY: encyclopedia homepage V4, never deploy without review -->
<section class="g-ency-hero" aria-labelledby="g-ency-title">
  <div class="g-wrap g-ency-hero-grid">
    <div class="g-ency-copy">
      <span class="g-ency-eyebrow">موسوعة السيارات والمعلومات الفنية</span>
      <h1 id="g-ency-title">موسوعة السيارات في مصر.<br><span>كل ما يخص عربيتك في مكان واحد.</span></h1>
      <p>من المواصفات والأسعار إلى أكواد الأعطال وخطوات الصيانة. اعرف معلومات عربيتك قبل شراء قطعة أو اتخاذ قرار.</p>
      <div class="g-ency-search" data-home="<?php echo esc_url(home_url('/')); ?>" data-reference="<?php echo esc_url($ref_archive); ?>" data-dtc="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>">
        <div class="g-ency-tabs" role="tablist" aria-label="نوع البحث">
          <button type="button" role="tab" aria-selected="true" data-ency-search="car">اسم السيارة</button>
          <button type="button" role="tab" aria-selected="false" data-ency-search="reference">المواصفات الفنية</button>
          <button type="button" role="tab" aria-selected="false" data-ency-search="fault">كود العطل</button>
          <button type="button" role="tab" aria-selected="false" data-ency-search="price">الأسعار</button>
        </div>
        <form role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
          <label class="g-sr-only" for="g-ency-search-input">ابحث في موسوعة أعطال</label>
          <input id="g-ency-search-input" type="search" name="s" placeholder="ابحث باسم الماركة أو الموديل" required autocomplete="off">
          <button type="submit">ابحث ←</button>
        </form>
      </div>
      <div class="g-ency-actions">
        <a data-google-vignette="false" class="g-ency-primary" href="<?php echo esc_url($ref_archive); ?>">استكشف دليل المواصفات الفنية ←</a>
        <a data-google-vignette="false" class="g-ency-secondary" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">تصفح موسوعة السيارات</a>
      </div>
    </div>
    <div class="g-ency-photo">
      <?php if($hero_img_id): echo wp_get_attachment_image($hero_img_id,'large',false,['loading'=>'eager','fetchpriority'=>'high','decoding'=>'async','alt'=>'','sizes'=>'(max-width:980px) 100vw, (max-width:1280px) 42vw, 550px']); endif; ?>
      <div class="g-ency-photo-caption">أعطال.كوم | معرفة من أول اختيار العربية لحد صيانتها</div>
      <?php if($ref_published>0): ?><div class="g-ency-ref-count"><strong><?php echo esc_html(number_format_i18n($ref_published)); ?></strong><small>صفحات مواصفات فنية منشورة</small></div><?php endif; ?>
    </div>
  </div>
</section>
<div class="g-wrap g-ency-quick-outer">
  <nav class="g-ency-quick" aria-label="المداخل الرئيسية لموسوعة السيارات">
    <a data-google-vignette="false" href="<?php echo esc_url($ref_archive); ?>"><span class="g-ency-q-icon"><?php echo a3g_icon('gear'); ?></span><span><b>مواصفات سيارتك</b><small>محركات ومقاسات وتجهيزات</small></span></a>
    <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><span class="g-ency-q-icon"><?php echo a3g_icon('warning'); ?></span><span><b>تشخيص الأعطال</b><small>أكواد OBD-II وخطوات الفحص</small></span></a>
    <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>"><span class="g-ency-q-icon"><?php echo a3g_icon('car'); ?></span><span><b>الأسعار والموديلات</b><small>الفئات والمواصفات</small></span></a>
    <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>"><span class="g-ency-q-icon"><?php echo a3g_icon('calendar'); ?></span><span><b>جداول الصيانة</b><small>العداد والمستلزمات</small></span></a>
  </nav>
</div>

<section class="g-ency-path-section" aria-labelledby="g-ency-path-title">
  <div class="g-wrap">
    <div class="g-ency-section-head"><div><span class="g-ency-kicker">بوابتك لمعلومات السيارات</span><h2 id="g-ency-path-title">اختار اللي محتاج تعرفه</h2><p>كل معلومة ليها مكان واضح، مع روابط بين المواصفات والأعطال والصيانة والموديلات.</p></div></div>
    <div class="g-ency-paths">
      <a class="g-ency-path" data-google-vignette="false" href="<?php echo esc_url($ref_archive); ?>"><strong>الدليل الفني للسيارات</strong><p>مواصفات المحرك والكاوتش والأبعاد وبيانات الموديلات.</p><span>افتح الدليل ←</span></a>
      <a class="g-ency-path" data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><strong>مكتبة أكواد الأعطال</strong><p>معاني الأكواد وأعراضها وأسبابها وخطوات التشخيص.</p><span>ابدأ التشخيص ←</span></a>
      <a class="g-ency-path" data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>"><strong>دليل السيارات والأسعار</strong><p>الموديلات والفئات والأسعار والمقارنات قبل الشراء.</p><span>استكشف السيارات ←</span></a>
      <a class="g-ency-path" data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>"><strong>الصيانة الدورية</strong><p>جداول ومعلومات صيانة المركبات حسب الموديل.</p><span>شوف جدول الصيانة ←</span></a>
      <a class="g-ency-path" data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_part','/parts/')); ?>"><strong>قطع الغيار والمقاسات</strong><p>معلومات القطع والمستلزمات ومصادر الشراء.</p><span>افتح دليل القطع ←</span></a>
      <a class="g-ency-path" data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>"><strong>مراكز الصيانة والخدمة</strong><p>دليل المراكز ومعلومات الاتصال والخدمات المنشورة.</p><span>شوف المراكز ←</span></a>
    </div>
  </div>
</section>

<?php if($ref_published>0): ?>
<section class="g-ency-reference" aria-labelledby="g-ency-reference-title">
  <div class="g-wrap">
    <div class="g-ency-section-head"><div><span class="g-ency-kicker">مرجع فني موثق</span><h2 id="g-ency-reference-title">دليل المواصفات الفنية للسيارات</h2><p>معلومات محددة للموديل والسوق والفئة، من مصادر معلنة ومراجعة.</p></div><a data-google-vignette="false" href="<?php echo esc_url($ref_archive); ?>">تصفح الدليل بالكامل ←</a></div>
    <div class="g-ency-ref-hero">
      <div><span class="eyebrow">CAR TECHNICAL REFERENCE</span><h3>قبل ما تغير قطعة، اعرف مواصفات عربيتك الصحيحة.</h3><p>المحرك، ناقل الحركة، الإطارات، الأبعاد وتجهيزات الأمان. بيانات فنية مع تنبيهات الفروق بين الموديلات والسنوات والفئات.</p><a data-google-vignette="false" class="g-ency-primary" href="<?php echo esc_url($ref_archive); ?>">افتح الدليل الفني ←</a></div>
      <div class="g-ency-ref-counter"><strong><?php echo esc_html(number_format_i18n($ref_published)); ?></strong><small>صفحات فنية منشورة</small></div>
    </div>
    <div class="g-ency-ref-models">
    <?php foreach($ref_examples as $item):
      $record=get_page_by_path($item['path'],OBJECT,'a3_car_ref');
      if(!$record||$record->post_status!=='publish')continue; ?>
      <a class="g-ency-model" data-google-vignette="false" href="<?php echo esc_url(get_permalink($record)); ?>">
        <div class="g-ency-model-thumb"><?php if(has_post_thumbnail($record->ID)) echo get_the_post_thumbnail($record->ID,'medium_large',['loading'=>'lazy','decoding'=>'async']); ?></div>
        <div class="g-ency-model-copy"><small><?php echo esc_html($item['brand']); ?></small><b><?php echo esc_html($item['short']); ?></b><span><?php echo esc_html($item['note']); ?> ←</span></div>
      </a>
    <?php endforeach; ?>
    </div>
    <nav class="g-ency-brands" aria-label="ماركات دليل المواصفات الفنية">
    <?php foreach($ref_brands as $slug=>$name):
      $brand=get_page_by_path($slug,OBJECT,'a3_car_ref');
      if(!$brand||$brand->post_status!=='publish')continue; ?>
      <a data-google-vignette="false" href="<?php echo esc_url(get_permalink($brand)); ?>"><?php echo esc_html($name); ?></a>
    <?php endforeach; ?>
    </nav>
  </div>
</section>
<?php endif; ?>

<section class="g-section g-section-soft g-home-dtc-zone g-ency-home-dtc-zone">
  <div class="g-wrap">
    <div class="g-dtc-command">
      <div class="g-dtc-command-copy">
        <span>مكتبة أكواد الأعطال</span>
        <h2>لمبة Check Engine منوّرة؟ اكتب الكود.</h2>
        <p>مرجع عربي لأكواد OBD-II: معنى الكود، الأعراض، الأسباب، درجة الخطورة، وطريقة التشخيص قبل تغيير أي قطعة.</p>
        <form role="search" method="get" action="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><label class="g-sr-only" for="home-dtc-code">كود العطل</label><input id="home-dtc-code" name="code" maxlength="8" placeholder="P0420" aria-label="اكتب كود العطل" dir="ltr" autocomplete="off" autocapitalize="characters" spellcheck="false" required><button type="submit"><?php echo a3g_icon('search'); ?><span>فسّر الكود</span></button></form>
        <div class="g-dtc-letters"><span><b>P</b> Powertrain</span><span><b>B</b> Body</span><span><b>C</b> Chassis</span><span><b>U</b> Network</span></div>
      </div>
      <div class="g-dtc-command-side">
        <?php if($dtcs->have_posts()): ?>
          <?php while($dtcs->have_posts()):$dtcs->the_post();$code=(string)get_post_meta(get_the_ID(),'_a3_dtc_code',true); ?>
            <a data-google-vignette="false" href="<?php echo esc_url(get_permalink(a3g_ux_original_guide_id(get_the_ID()))); ?>"><b><?php echo esc_html($code?:get_the_title()); ?></b><span><?php echo esc_html(wp_trim_words(get_the_title(),8)); ?></span></a>
          <?php endwhile;wp_reset_postdata(); ?>
        <?php else: ?>
          <div class="g-dtc-preview-card"><b>P0420</b><span>كفاءة المحول الحفاز</span><small>مثال لشكل صفحة الكود داخل مرجع أعطال</small></div>
          <div class="g-dtc-preview-card"><b>P0171</b><span>خليط فقير Bank 1</span><small>أعراض + أسباب + تشخيص</small></div>
          <div class="g-dtc-preview-card"><b>P0300</b><span>Misfire متعدد</span><small>تشخيص قبل تغيير القطع</small></div>
        <?php endif; ?>
      </div>
    </div>
  </div>
</section>


<?php if($cars->have_posts() || $car_editorials->have_posts()): ?>
<section class="g-section g-home-cars-section" aria-labelledby="g-home-cars-heading">
  <div class="g-wrap">
    <div class="g-section-head">
      <div>
        <span>دليل السيارات</span>
        <h2 id="g-home-cars-heading">جديد السيارات على أعطال</h2>
        <p>أسعار ومراجعات حديثة، ومواصفات تساعدك على المقارنة واختيار السيارة المناسبة.</p>
      </div>
      <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">عرض موسوعة السيارات</a>
    </div>

    <?php if($car_editorials->have_posts()): ?>
    <div class="g-home-cars-editorials" aria-labelledby="g-home-cars-editorials-heading">
      <div class="g-home-cars-subhead">
        <div>
          <h3 id="g-home-cars-editorials-heading">أحدث الأسعار والمراجعات</h3>
          <p>اقرأ أحدث الأسعار والفروق بين الفئات والمميزات والعيوب قبل الشراء.</p>
        </div>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(374)); ?>">كل أسعار السيارات</a>
      </div>
      <div class="g-news-grid g-home-car-editorial-grid">
        <?php while($car_editorials->have_posts()):$car_editorials->the_post();a3g_card(get_the_ID(),'g-home-car-editorial-card');endwhile;wp_reset_postdata(); ?>
      </div>
    </div>
    <?php endif; ?>

    <?php if($cars->have_posts()): ?>
    <div class="g-home-cars-profiles" aria-labelledby="g-home-cars-profiles-heading">
      <div class="g-home-cars-subhead">
        <div>
          <h3 id="g-home-cars-profiles-heading">سيارات مضافة أو محدثة حديثًا</h3>
          <p>اختر الموديل للوصول إلى مواصفاته وأسعاره والمراجعات المرتبطة به.</p>
        </div>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">كل الموديلات</a>
      </div>
      <div class="g-platform-grid g-home-car-grid">
        <?php while($cars->have_posts()):$cars->the_post();a3g_platform_card();endwhile;wp_reset_postdata(); ?>
      </div>
    </div>
    <?php endif; ?>
  </div>
</section>
<?php endif; ?>

<section class="g-section g-home-os-section">
  <div class="g-wrap">
    <div class="g-home-os">
      <div class="g-home-os-copy">
        <span>جراج أعطال</span>
        <h2>خلي أعطال يتابع مركبتك معاك</h2>
        <p>أضف سيارتك أو موتوسيكلك مرة واحدة. حدّث العداد، سجل الصيانة، اعرف اللي قرب ميعاده، دور على القطع المناسبة، ولو قررت تبيعها اعرضها من نفس الملف.</p>
        <div class="g-home-os-actions"><a data-google-vignette="false" class="is-primary" href="<?php echo esc_url(home_url('/my-garage/')); ?>">افتح سيارتي</a><a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>">شوف جداول الصيانة</a></div>
      </div>
      <div class="g-home-os-dashboard">
        <div class="g-os-car-head"><span><?php echo a3g_icon('car'); ?></span><div><small>سيارتي</small><strong>جراج رقمي كامل</strong></div><b>مثال توضيحي</b></div>
        <div class="g-os-meter"><div><span>عداد المركبة</span><strong>87,450 <small>كم</small></strong></div><i style="--p:72%"></i></div>
        <div class="g-os-services">
          <span class="is-due"><i></i><b>زيت المحرك</b><small>مستحق الآن</small></span>
          <span class="is-soon"><i></i><b>فلتر الهواء</b><small>قريبًا</small></span>
          <span class="is-ok"><i></i><b>سائل الفرامل</b><small>لاحقًا</small></span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="g-section">
  <div class="g-wrap">
    <div class="g-section-head"><div><span>السوق</span><h2>أحدث أسعار السيارات</h2></div><a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(374)); ?>">عرض جميع الأسعار</a></div>
    <div class="g-price-grid"><?php while($prices->have_posts()){$prices->the_post();a3g_price_card();}wp_reset_postdata(); ?></div>
  </div>
</section>

<section class="g-section g-home-moto-section">
  <div class="g-wrap">
    <div class="g-home-moto-head">
      <div><span>A3TAL MOTO</span><h2>عالم الموتوسيكلات والسكوتر</h2><p>أسعار ومواصفات وأعطال وصيانة وقطع غيار للموتوسيكل، لأن السوق المصري مش عربيات بس.</p></div>
      <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_motorcycle','/motorcycles/')); ?>">دخول عالم الموتوسيكلات</a>
    </div>
    <?php if($moto_articles->have_posts()): ?>
      <div class="g-section-head g-home-moto-articles-head">
        <div><span>أحدث المقالات</span><h3>جديد دليل الموتوسيكلات والسكوتر</h3></div>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(3028)); ?>">عرض كل مقالات الموتوسيكلات</a>
      </div>
      <div class="g-news-grid"><?php while($moto_articles->have_posts()):$moto_articles->the_post();a3g_card(get_the_ID(),'g-news-card');endwhile;wp_reset_postdata(); ?></div>
    <?php endif; ?>
    <?php if($motos->have_posts()): ?>
      <div class="g-section-head g-home-moto-models-head"><div><span>قاعدة الموديلات</span><h3>أحدث موديلات الموتوسيكلات</h3></div></div>
      <div class="g-platform-grid"><?php while($motos->have_posts()):$motos->the_post();a3g_platform_card();endwhile;wp_reset_postdata(); ?></div>
    <?php else: ?>
      <div class="g-moto-teaser-grid">
        <a data-google-vignette="false" href="<?php echo esc_url(add_query_arg('vehicle_type','scooter',a3g_platform_link('a3_motorcycle','/motorcycles/'))); ?>"><span><?php echo a3g_icon('motorcycle'); ?></span><b>سكوتر</b><small>عملي للمدينة والتنقل اليومي</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(add_query_arg('vehicle_type','commuter',a3g_platform_link('a3_motorcycle','/motorcycles/'))); ?>"><span><?php echo a3g_icon('motorcycle'); ?></span><b>اقتصادي</b><small>استهلاك وتشغيل يومي</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(add_query_arg('vehicle_type','sport',a3g_platform_link('a3_motorcycle','/motorcycles/'))); ?>"><span><?php echo a3g_icon('bolt'); ?></span><b>رياضي</b><small>أداء وتجهيزات ومقارنات</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(add_query_arg('vehicle_type','electric',a3g_platform_link('a3_motorcycle','/motorcycles/'))); ?>"><span><?php echo a3g_icon('bolt'); ?></span><b>كهربائي</b><small>بطارية ومدى وشحن</small></a>
      </div>
    <?php endif; ?>
  </div>
</section>

<section class="g-section g-section-soft">
  <div class="g-wrap">
    <div class="g-home-ownership-grid">
      <div class="g-home-module g-module-maintenance">
        <div class="g-home-module-head"><span>العناية بالمركبة</span><h2>صيانة تتحرك مع عدادك</h2></div>
        <div class="g-maintenance-mini-timeline">
          <span><b>10K</b><small>زيت + فحص</small></span><i></i><span><b>20K</b><small>فلاتر</small></span><i></i><span><b>40K</b><small>سوائل وفحص</small></span><i></i><span><b>90K</b><small>صيانة كبرى</small></span>
        </div>
        <p>جداول حسب الموديل، مع فترات مختلفة للاستخدام العادي والشاق، ومواصفات السوائل وأرقام القطع عند توفرها.</p>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>">استكشف جداول الصيانة ←</a>
      </div>

      <div class="g-home-module g-module-parts">
        <div class="g-home-module-head"><span>A3TAL PARTS</span><h2>قطع الغيار وأماكن بيعها</h2></div>
        <div class="g-parts-origin-list"><span>OEM أصلي</span><span>OES</span><span>Aftermarket</span><span>بديل اقتصادي</span><span>استيراد</span></div>
        <p>رقم القطعة، التوافق مع السيارة، البدائل، السعر المرجعي، وأماكن الشراء الرسمية أو الموثقة أو المستقلة.</p>
        <div class="g-module-links"><a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_part','/parts/')); ?>">كتالوج القطع</a><a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_parts_vendor','/parts-stores/')); ?>">أماكن البيع</a></div>
      </div>

      <div class="g-home-module g-module-market">
        <div class="g-home-module-head"><span>A3TAL MARKET</span><h2>بيع سيارتك من ملفها</h2></div>
        <div class="g-market-mini"><span>صور واضحة</span><span>الموقع</span><span>سجل الصيانة</span><span>العداد</span></div>
        <p>لو سيارتك موجودة في My Garage، بياناتها الأساسية تنتقل للإعلان بدل ما تعيد إدخالها من الصفر.</p>
        <div class="g-module-links"><a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>">سيارات للبيع</a><a data-google-vignette="false" href="<?php echo esc_url(home_url('/my-garage/')); ?>">بيع سيارتي</a></div>
      </div>
    </div>
  </div>
</section>

<section class="g-section g-section-soft">
  <div class="g-wrap g-home-places-wrap">
    <div class="g-section-head"><div><span>A3TAL PLACES</span><h2>مراكز الخدمة والمعارض</h2></div><a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>">استكشف الدليل</a></div>
    <div class="g-home-places-grid">
      <a data-google-vignette="false" class="g-place-mega" href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>"><span><?php echo a3g_icon('wrench'); ?></span><div><b>مراكز الخدمة</b><small>معتمد رسميًا، موثّق من أعطال، ومستقل</small></div></a>
      <a data-google-vignette="false" class="g-place-mega" href="<?php echo esc_url(a3g_platform_link('a3_showroom','/car-showrooms/')); ?>"><span><?php echo a3g_icon('store'); ?></span><div><b>معارض السيارات</b><small>رسمي، موثّق، وخاص</small></div></a>
      <a data-google-vignette="false" class="g-place-mega" href="<?php echo esc_url(a3g_platform_link('a3_parts_vendor','/parts-stores/')); ?>"><span><?php echo a3g_icon('gear'); ?></span><div><b>بائعو قطع الغيار</b><small>رسمي، موثّق، ومستقل</small></div></a>
    </div>
  </div>
</section>

<section class="g-section">
  <div class="g-wrap g-duo-grid">
    <div class="g-feature-box g-compare-box">
      <div class="g-box-head"><div><span>قرار أسرع</span><h2>مقارنات السيارات</h2></div><a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(21)); ?>">تصفح المقارنات</a></div>
      <div class="g-compare-visual"><div class="g-compare-car"><?php echo a3g_icon('car'); ?><span>مقارنات حسب الفئة</span></div><b>VS</b><div class="g-compare-car"><?php echo a3g_icon('compare'); ?><span>فروق المواصفات</span></div></div>
      <p>تصفح مقارنات منشورة بين سيارات متقاربة في السعر أو الاستخدام قبل قرار الشراء.</p>
    </div>
    <div class="g-feature-box g-fault-box">
      <div class="g-box-head"><div><span>الأعطال والتشخيص</span><h2>ابدأ من العَرَض أو من الكود</h2></div><a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(8)); ?>">كل الأعطال</a></div>
      <div class="g-fault-icons">
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(8)); ?>"><?php echo a3g_icon('gear'); ?><span>المحرك</span></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(13)); ?>"><?php echo a3g_icon('bolt'); ?><span>الكهرباء</span></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><?php echo a3g_icon('gear'); ?><span>DTC</span></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(18)); ?>"><?php echo a3g_icon('wrench'); ?><span>التكييف</span></a>
      </div>
      <div class="g-fault-feed"><?php while($faults->have_posts()){$faults->the_post();a3g_compact();}wp_reset_postdata(); ?></div>
    </div>
  </div>
</section>

<section class="g-section g-section-soft">
  <div class="g-wrap">
    <div class="g-section-head"><div><span>الجديد الآن</span><h2>موضوعات أخرى من أعطال</h2></div><a data-google-vignette="false" href="<?php echo esc_url(home_url('/')); ?>">عرض المزيد</a></div>
    <div class="g-news-grid"><?php while($news->have_posts()){$news->the_post();a3g_card(get_the_ID(),'g-news-card');}wp_reset_postdata(); ?></div>
    <div class="g-trust-strip g-trust-platform">
      <div><?php echo a3g_icon('gear'); ?><span><strong>محتوى متخصص</strong><small>تشخيص ومعلومات منظمة</small></span></div>
      <div><?php echo a3g_icon('car'); ?><span><strong>قاعدة مركبات</strong><small>سيارات وموتوسيكلات</small></span></div>
      <div><?php echo a3g_icon('pin'); ?><span><strong>خدمات وسوق</strong><small>مراكز ومعارض وقطع غيار</small></span></div>
      <div><?php echo a3g_icon('calendar'); ?><span><strong>ملكية وصيانة</strong><small>جراج وسجل وتذكيرات</small></span></div>
    </div>
  </div>
</section>

<nav class="g-v3-mobile-dock" aria-label="التنقل السريع على الجوال">
  <a data-google-vignette="false" href="<?php echo esc_url(home_url('/')); ?>" aria-current="page"><?php echo a3g_icon('car'); ?><span>الرئيسية</span></a>
  <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(8)); ?>"><?php echo a3g_icon('wrench'); ?><span>الأعطال</span></a>
  <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>"><?php echo a3g_icon('car'); ?><span>السيارات</span></a>
  <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(374)); ?>"><?php echo a3g_icon('tag'); ?><span>الأسعار</span></a>
  <a data-google-vignette="false" href="<?php echo esc_url($ref_archive); ?>"><?php echo a3g_icon('gear'); ?><span>المواصفات</span></a>
</nav>

</main>
<?php get_footer(); ?>
