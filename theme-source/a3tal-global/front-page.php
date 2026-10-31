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
?>
<main class="g-home g-home-platform">

<!-- A3TAL-EXPERIENCE-V3-20261022: editorial-first, fast, accessible homepage hero -->
<section class="g-hero-section g-platform-home-hero g-v3-intro" aria-labelledby="g-v3-main-title">
  <div class="g-wrap">
    <div class="g-hero g-hero-platform g-v3-hero">
      <?php if($hero_img_id): ?>
        <?php echo wp_get_attachment_image($hero_img_id,'large',false,[
          'class'=>'g-hero-bg',
          'alt'=>'',
          'loading'=>'eager',
          'fetchpriority'=>'high',
          'decoding'=>'async',
          'sizes'=>'(max-width: 767px) 100vw, (max-width: 1280px) 92vw, 1240px',
        ]); ?>
      <?php endif; ?>
      <div class="g-v3-hero-inner">
        <div class="g-hero-content g-v3-hero-copy">
          <span class="g-hero-eyebrow"><i aria-hidden="true"></i> A3TAL | موسوعة السيارات</span>
          <h1 id="g-v3-main-title">موسوعة أعطال السيارات وأكواد التشخيص والأسعار ومراكز الصيانة</h1>
          <p class="g-v3-hero-lead">افهم كود العطل وحدّد خطوات الفحص، أو ابحث عن أسعار ومواصفات سيارتك ومراكز صيانتها. ابدأ بالكود أو اسم الموديل أو المشكلة التي تواجهك.</p>
          <form class="g-hero-search g-universal-search g-v3-search" role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
            <label class="g-search-field" for="g-v3-site-search"><?php echo a3g_icon('search'); ?><input id="g-v3-site-search" type="search" name="s" autocomplete="off" placeholder="اكتب موديل سيارة، سعر، عطل، كود P0420..." aria-label="ابحث عن سيارة أو سعر أو عطل"></label>
            <button type="submit"><?php echo a3g_icon('search'); ?><span>ابحث</span></button>
          </form>
          <div class="g-v3-search-examples" aria-label="عمليات بحث شائعة">
            <span>ابدأ مثلًا بـ</span>
            <a data-google-vignette="false" href="<?php echo esc_url(add_query_arg('s','P0420',home_url('/'))); ?>">P0420</a>
            <a data-google-vignette="false" href="<?php echo esc_url(add_query_arg('s','بطارية السيارة',home_url('/'))); ?>">البطارية</a>
            <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(374)); ?>">أسعار السيارات</a>
          </div>
        </div>
        <aside class="g-v3-hero-journeys" aria-label="اختر ما تبحث عنه">
          <div class="g-v3-journeys-title"><span>اختر وجهتك</span><strong>ابدأ من هنا</strong></div>
          <a data-google-vignette="false" class="g-v3-journey" href="<?php echo esc_url(a3g_cat_link(8)); ?>">
            <span class="g-v3-journey-icon"><?php echo a3g_icon('wrench'); ?></span>
            <span class="g-v3-journey-copy"><b>شخّص عطل العربية</b><small>الأعراض والأسباب وخطوات الفحص</small></span>
            <span class="g-v3-journey-arrow" aria-hidden="true">←</span>
          </a>
          <a data-google-vignette="false" class="g-v3-journey" href="<?php echo esc_url(a3g_cat_link(374)); ?>">
            <span class="g-v3-journey-icon"><?php echo a3g_icon('tag'); ?></span>
            <span class="g-v3-journey-copy"><b>اعرف سعر عربية</b><small>الفئات والمواصفات والمقارنات</small></span>
            <span class="g-v3-journey-arrow" aria-hidden="true">←</span>
          </a>
          <a data-google-vignette="false" class="g-v3-journey" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">
            <span class="g-v3-journey-icon"><?php echo a3g_icon('car'); ?></span>
            <span class="g-v3-journey-copy"><b>اختار سيارتك</b><small>كل ما يخص الموديل في ملف واحد</small></span>
            <span class="g-v3-journey-arrow" aria-hidden="true">←</span>
          </a>
          <div class="g-v3-journeys-foot">
            <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>">مكتبة أكواد DTC <?php echo a3g_icon('gear'); ?></a>
            <a data-google-vignette="false" href="<?php echo esc_url(home_url('/my-garage/')); ?>">جراجي <?php echo a3g_icon('car'); ?></a>
          </div>
        </aside>
      </div>
    </div>
    <div class="g-v3-explorer" aria-label="استكشف أقسام أعطال">
      <div class="g-v3-explorer-head">
        <div><span>اكتشف المزيد</span><h2>كل خدمات السيارات بين إيديك</h2></div>
        <span class="g-v3-explorer-note">من أول المعلومة لحد الصيانة والشراء</span>
      </div>
      <nav class="g-platform-launcher g-v3-launcher" aria-label="أقسام موسوعة أعطال">
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('car'); ?></span><b>موسوعة السيارات</b><small>الموديلات والمواصفات</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('warning'); ?></span><b>أكواد الأعطال</b><small>معنى الكود والتشخيص</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_motorcycle','/motorcycles/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('motorcycle'); ?></span><b>الموتوسيكلات</b><small>الموديلات والأعطال</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('wrench'); ?></span><b>مراكز الخدمة</b><small>المعتمد والمستقل</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_showroom','/car-showrooms/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('store'); ?></span><b>معارض السيارات</b><small>أماكن بيع السيارات</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('calendar'); ?></span><b>جداول الصيانة</b><small>حسب العداد والموديل</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_part','/parts/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('gear'); ?></span><b>قطع الغيار</b><small>المقاسات والأكواد</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('tag'); ?></span><b>سوق السيارات</b><small>مستعمل وبيع وشراء</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(21)); ?>"><span class="g-launch-icon"><?php echo a3g_icon('compare'); ?></span><b>مقارنات السيارات</b><small>قرار شراء أذكى</small></a>
        <a data-google-vignette="false" href="<?php echo esc_url(home_url('/my-garage/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('car'); ?></span><b>جراجي</b><small>العداد وسجل الصيانة</small></a>
      </nav>
    </div>
  </div>
</section>

<section class="g-section g-section-soft g-home-dtc-zone">
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
  <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>"><?php echo a3g_icon('pin'); ?><span>الخدمات</span></a>
</nav>

</main>
<?php get_footer(); ?>
