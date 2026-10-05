<?php
get_header();

$hero_q=a3g_query(['cat'=>374,'posts_per_page'=>1]);
$hero_id=0;$hero_img='';
if($hero_q->have_posts()){ $hero_q->the_post(); $hero_id=get_the_ID(); $hero_img=get_the_post_thumbnail_url($hero_id,'full'); }
wp_reset_postdata();

$prices=a3g_query(['cat'=>374,'posts_per_page'=>4,'post__not_in'=>$hero_id?[$hero_id]:[]]);
$reviews=a3g_query(['category__in'=>[22,21],'posts_per_page'=>3]);
$faults=a3g_query(['category__in'=>[8,13,2,18],'posts_per_page'=>4]);
$news=a3g_query(['posts_per_page'=>4,'post__not_in'=>$hero_id?[$hero_id]:[]]);

$home_car_slugs=['byd-sealion-6-ev-2027','haval-v7-egypt','opel-frontera-egypt','geely-monjaro-em-i-egypt','xpeng-g7-super-reev-egypt','chery-tiggo-9-egypt'];
$home_car_ids=[];
foreach($home_car_slugs as $slug){
  $p=get_page_by_path($slug,OBJECT,'a3_car');
  if($p instanceof WP_Post)$home_car_ids[]=(int)$p->ID;
}
$cars=new WP_Query([
  'post_type'=>'a3_car',
  'post_status'=>'publish',
  'posts_per_page'=>6,
  'post__in'=>$home_car_ids,
  'orderby'=>'post__in',
  'ignore_sticky_posts'=>true,
]);
$motos=new WP_Query(['post_type'=>'a3_motorcycle','post_status'=>'publish','posts_per_page'=>3,'ignore_sticky_posts'=>true]);
$dtcs=new WP_Query(['post_type'=>'a3_dtc','post_status'=>'publish','posts_per_page'=>4,'ignore_sticky_posts'=>true]);
$parts=new WP_Query(['post_type'=>'a3_part','post_status'=>'publish','posts_per_page'=>4,'ignore_sticky_posts'=>true]);
$listings=new WP_Query(['post_type'=>'a3_listing','post_status'=>'publish','posts_per_page'=>3,'ignore_sticky_posts'=>true]);
$centers=new WP_Query(['post_type'=>'a3_service_center','post_status'=>'publish','posts_per_page'=>3,'ignore_sticky_posts'=>true]);
$showrooms=new WP_Query(['post_type'=>'a3_showroom','post_status'=>'publish','posts_per_page'=>3,'ignore_sticky_posts'=>true]);
?>
<main class="g-home g-home-platform">

<section class="g-hero-section g-platform-home-hero">
  <div class="g-wrap">
    <div class="g-hero g-hero-platform" <?php if($hero_img): ?>style="background-image:linear-gradient(90deg,rgba(5,14,24,.96) 0%,rgba(5,14,24,.77) 46%,rgba(5,14,24,.25) 100%),url('<?php echo esc_url($hero_img); ?>')"<?php endif; ?>>
      <div class="g-hero-content">
        <span class="g-hero-eyebrow">A3TAL AUTOMOTIVE PLATFORM</span>
        <h1>كل ما يخص عالم السيارات والموتوسيكلات</h1>
        <p>من الشراء والمقارنة إلى التشخيص والصيانة وقطع الغيار ومراكز الخدمة والبيع. مركبتك كلها في مكان واحد.</p>

        <form class="g-hero-search g-universal-search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
          <div class="g-search-field"><?php echo a3g_icon('search'); ?><input type="search" name="s" placeholder="ابحث عن سيارة، موتوسيكل، عطل، كود P0420، قطعة غيار أو مركز خدمة..." aria-label="بحث شامل"></div>
          <button type="submit"><?php echo a3g_icon('search'); ?><span>بحث</span></button>
        </form>

        <div class="g-hero-action-row">
          <a href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>"><?php echo a3g_icon('car'); ?><span><b>ابحث عن سيارة</b><small>أسعار ومواصفات ومراجعات</small></span></a>
          <a href="<?php echo esc_url(a3g_platform_link('a3_motorcycle','/motorcycles/')); ?>"><?php echo a3g_icon('motorcycle'); ?><span><b>الموتوسيكلات</b><small>سكوتر وموتوسيكل ومقارنات</small></span></a>
          <a href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><?php echo a3g_icon('gear'); ?><span><b>فسّر كود عطل</b><small>مرجع DTC عربي</small></span></a>
          <a href="<?php echo esc_url(home_url('/my-garage/')); ?>"><?php echo a3g_icon('car'); ?><span><b>سيارتي</b><small>الصيانة والعداد والسجل</small></span></a>
        </div>
      </div>
    </div>

    <div class="g-platform-launcher">
      <a href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('car'); ?></span><b>السيارات</b><small>الموديلات والأسعار</small></a>
      <a href="<?php echo esc_url(a3g_platform_link('a3_motorcycle','/motorcycles/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('motorcycle'); ?></span><b>الموتوسيكلات</b><small>السكوتر والموتوسيكل</small></a>
      <a href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('warning'); ?></span><b>أكواد الأعطال</b><small>P / B / C / U</small></a>
      <a href="<?php echo esc_url(a3g_cat_link(8)); ?>"><span class="g-launch-icon"><?php echo a3g_icon('brain'); ?></span><b>تشخيص الأعطال</b><small>الأعراض والحلول</small></a>
      <a href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('calendar'); ?></span><b>جداول الصيانة</b><small>حسب الموديل والعداد</small></a>
      <a href="<?php echo esc_url(a3g_platform_link('a3_part','/parts/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('gear'); ?></span><b>قطع الغيار</b><small>OEM وAftermarket</small></a>
      <a href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('wrench'); ?></span><b>مراكز الخدمة</b><small>معتمد وموثّق ومستقل</small></a>
      <a href="<?php echo esc_url(a3g_platform_link('a3_showroom','/car-showrooms/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('store'); ?></span><b>معارض السيارات</b><small>رسمي وموثّق وخاص</small></a>
      <a href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>"><span class="g-launch-icon"><?php echo a3g_icon('tag'); ?></span><b>سوق السيارات</b><small>بيع وشراء المستعمل</small></a>
      <a href="<?php echo esc_url(a3g_cat_link(21)); ?>"><span class="g-launch-icon"><?php echo a3g_icon('compare'); ?></span><b>المقارنات</b><small>مقارنات منشورة قبل الشراء</small></a>
    </div>
  </div>
</section>

<?php if($cars->have_posts()): ?>
<section class="g-section g-home-cars-section">
  <div class="g-wrap">
    <div class="g-section-head">
      <div>
        <span>A3TAL CARS DATABASE</span>
        <h2>سيارات مضافة حديثًا</h2>
        <p>سعر ومواصفات أساسية موثقة لكل موديل، مع رابط للمراجعة الكاملة والتفاصيل قبل الشراء.</p>
      </div>
      <a href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">عرض كل السيارات</a>
    </div>
    <div class="g-platform-grid g-home-car-grid">
      <?php while($cars->have_posts()):$cars->the_post();a3g_platform_card();endwhile;wp_reset_postdata(); ?>
    </div>
  </div>
</section>
<?php endif; ?>

<section class="g-section g-home-os-section">
  <div class="g-wrap">
    <div class="g-home-os">
      <div class="g-home-os-copy">
        <span>MY A3TAL GARAGE</span>
        <h2>خلي أعطال يتابع مركبتك معاك</h2>
        <p>أضف سيارتك أو موتوسيكلك مرة واحدة. حدّث العداد، سجل الصيانة، اعرف اللي قرب ميعاده، دور على القطع المناسبة، ولو قررت تبيعها اعرضها من نفس الملف.</p>
        <div class="g-home-os-actions"><a class="is-primary" href="<?php echo esc_url(home_url('/my-garage/')); ?>">افتح سيارتي</a><a href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>">شوف جداول الصيانة</a></div>
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

<section class="g-section g-section-soft g-home-dtc-zone">
  <div class="g-wrap">
    <div class="g-dtc-command">
      <div class="g-dtc-command-copy">
        <span>A3TAL DTC</span>
        <h2>لمبة Check Engine منوّرة؟ اكتب الكود.</h2>
        <p>مرجع عربي لأكواد OBD-II: معنى الكود، الأعراض، الأسباب، درجة الخطورة، وطريقة التشخيص قبل تغيير أي قطعة.</p>
        <form method="get" action="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><input name="code" maxlength="8" placeholder="P0420"><button type="submit"><?php echo a3g_icon('search'); ?><span>فسّر الكود</span></button></form>
        <div class="g-dtc-letters"><span><b>P</b> Powertrain</span><span><b>B</b> Body</span><span><b>C</b> Chassis</span><span><b>U</b> Network</span></div>
      </div>
      <div class="g-dtc-command-side">
        <?php if($dtcs->have_posts()): ?>
          <?php while($dtcs->have_posts()):$dtcs->the_post();$code=(string)get_post_meta(get_the_ID(),'_a3_dtc_code',true); ?>
            <a href="<?php the_permalink(); ?>"><b><?php echo esc_html($code?:get_the_title()); ?></b><span><?php echo esc_html(wp_trim_words(get_the_title(),8)); ?></span></a>
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

<section class="g-section">
  <div class="g-wrap">
    <div class="g-section-head"><div><span>السوق</span><h2>أحدث أسعار السيارات</h2></div><a href="<?php echo esc_url(a3g_cat_link(374)); ?>">عرض جميع الأسعار</a></div>
    <div class="g-price-grid"><?php while($prices->have_posts()){$prices->the_post();a3g_price_card();}wp_reset_postdata(); ?></div>
  </div>
</section>

<section class="g-section g-home-moto-section">
  <div class="g-wrap">
    <div class="g-home-moto-head">
      <div><span>A3TAL MOTO</span><h2>عالم الموتوسيكلات والسكوتر</h2><p>أسعار ومواصفات وأعطال وصيانة وقطع غيار للموتوسيكل، لأن السوق المصري مش عربيات بس.</p></div>
      <a href="<?php echo esc_url(a3g_platform_link('a3_motorcycle','/motorcycles/')); ?>">دخول عالم الموتوسيكلات</a>
    </div>
    <?php if($motos->have_posts()): ?>
      <div class="g-platform-grid"><?php while($motos->have_posts()):$motos->the_post();a3g_platform_card();endwhile;wp_reset_postdata(); ?></div>
    <?php else: ?>
      <div class="g-moto-teaser-grid">
        <a href="<?php echo esc_url(add_query_arg('vehicle_type','scooter',a3g_platform_link('a3_motorcycle','/motorcycles/'))); ?>"><span><?php echo a3g_icon('motorcycle'); ?></span><b>سكوتر</b><small>عملي للمدينة والتنقل اليومي</small></a>
        <a href="<?php echo esc_url(add_query_arg('vehicle_type','commuter',a3g_platform_link('a3_motorcycle','/motorcycles/'))); ?>"><span><?php echo a3g_icon('motorcycle'); ?></span><b>اقتصادي</b><small>استهلاك وتشغيل يومي</small></a>
        <a href="<?php echo esc_url(add_query_arg('vehicle_type','sport',a3g_platform_link('a3_motorcycle','/motorcycles/'))); ?>"><span><?php echo a3g_icon('bolt'); ?></span><b>رياضي</b><small>أداء وتجهيزات ومقارنات</small></a>
        <a href="<?php echo esc_url(add_query_arg('vehicle_type','electric',a3g_platform_link('a3_motorcycle','/motorcycles/'))); ?>"><span><?php echo a3g_icon('bolt'); ?></span><b>كهربائي</b><small>بطارية ومدى وشحن</small></a>
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
        <a href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>">استكشف جداول الصيانة ←</a>
      </div>

      <div class="g-home-module g-module-parts">
        <div class="g-home-module-head"><span>A3TAL PARTS</span><h2>قطع الغيار وأماكن بيعها</h2></div>
        <div class="g-parts-origin-list"><span>OEM أصلي</span><span>OES</span><span>Aftermarket</span><span>بديل اقتصادي</span><span>استيراد</span></div>
        <p>رقم القطعة، التوافق مع السيارة، البدائل، السعر المرجعي، وأماكن الشراء الرسمية أو الموثقة أو المستقلة.</p>
        <div class="g-module-links"><a href="<?php echo esc_url(a3g_platform_link('a3_part','/parts/')); ?>">كتالوج القطع</a><a href="<?php echo esc_url(a3g_platform_link('a3_parts_vendor','/parts-stores/')); ?>">أماكن البيع</a></div>
      </div>

      <div class="g-home-module g-module-market">
        <div class="g-home-module-head"><span>A3TAL MARKET</span><h2>بيع سيارتك من ملفها</h2></div>
        <div class="g-market-mini"><span>صور واضحة</span><span>الموقع</span><span>سجل الصيانة</span><span>العداد</span></div>
        <p>لو سيارتك موجودة في My Garage، بياناتها الأساسية تنتقل للإعلان بدل ما تعيد إدخالها من الصفر.</p>
        <div class="g-module-links"><a href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>">سيارات للبيع</a><a href="<?php echo esc_url(home_url('/my-garage/')); ?>">بيع سيارتي</a></div>
      </div>
    </div>
  </div>
</section>

<section class="g-section">
  <div class="g-wrap">
    <div class="g-section-head"><div><span>تجارب وقرار شراء</span><h2>مراجعات ومقارنات السيارات</h2></div><a href="<?php echo esc_url(a3g_cat_link(22)); ?>">عرض جميع المراجعات</a></div>
    <div class="g-review-grid"><?php while($reviews->have_posts()){$reviews->the_post();a3g_card(get_the_ID(),'g-review-card');}wp_reset_postdata(); ?></div>
  </div>
</section>

<section class="g-section g-section-soft">
  <div class="g-wrap g-home-places-wrap">
    <div class="g-section-head"><div><span>A3TAL PLACES</span><h2>مراكز الخدمة والمعارض</h2></div><a href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>">استكشف الدليل</a></div>
    <div class="g-home-places-grid">
      <a class="g-place-mega" href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>"><span><?php echo a3g_icon('wrench'); ?></span><div><b>مراكز الخدمة</b><small>معتمد رسميًا، موثّق من أعطال، ومستقل</small></div></a>
      <a class="g-place-mega" href="<?php echo esc_url(a3g_platform_link('a3_showroom','/car-showrooms/')); ?>"><span><?php echo a3g_icon('store'); ?></span><div><b>معارض السيارات</b><small>رسمي، موثّق، وخاص</small></div></a>
      <a class="g-place-mega" href="<?php echo esc_url(a3g_platform_link('a3_parts_vendor','/parts-stores/')); ?>"><span><?php echo a3g_icon('gear'); ?></span><div><b>بائعو قطع الغيار</b><small>رسمي، موثّق، ومستقل</small></div></a>
    </div>
  </div>
</section>

<section class="g-section">
  <div class="g-wrap g-duo-grid">
    <div class="g-feature-box g-compare-box">
      <div class="g-box-head"><div><span>قرار أسرع</span><h2>مقارنات السيارات</h2></div><a href="<?php echo esc_url(a3g_cat_link(21)); ?>">تصفح المقارنات</a></div>
      <div class="g-compare-visual"><div class="g-compare-car"><?php echo a3g_icon('car'); ?><span>مقارنات حسب الفئة</span></div><b>VS</b><div class="g-compare-car"><?php echo a3g_icon('compare'); ?><span>فروق المواصفات</span></div></div>
      <p>تصفح مقارنات منشورة بين سيارات متقاربة في السعر أو الاستخدام قبل قرار الشراء.</p>
    </div>
    <div class="g-feature-box g-fault-box">
      <div class="g-box-head"><div><span>الأعطال والتشخيص</span><h2>ابدأ من العَرَض أو من الكود</h2></div><a href="<?php echo esc_url(a3g_cat_link(8)); ?>">كل الأعطال</a></div>
      <div class="g-fault-icons">
        <a href="<?php echo esc_url(a3g_cat_link(8)); ?>"><?php echo a3g_icon('gear'); ?><span>المحرك</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(13)); ?>"><?php echo a3g_icon('bolt'); ?><span>الكهرباء</span></a>
        <a href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>"><?php echo a3g_icon('gear'); ?><span>DTC</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(18)); ?>"><?php echo a3g_icon('wrench'); ?><span>التكييف</span></a>
      </div>
      <div class="g-fault-feed"><?php while($faults->have_posts()){$faults->the_post();a3g_compact();}wp_reset_postdata(); ?></div>
    </div>
  </div>
</section>

<section class="g-section g-section-soft">
  <div class="g-wrap">
    <div class="g-section-head"><div><span>الجديد الآن</span><h2>آخر الأخبار والترند</h2></div><a href="<?php echo esc_url(home_url('/')); ?>">عرض المزيد</a></div>
    <div class="g-news-grid"><?php while($news->have_posts()){$news->the_post();a3g_card(get_the_ID(),'g-news-card');}wp_reset_postdata(); ?></div>
    <div class="g-trust-strip g-trust-platform">
      <div><?php echo a3g_icon('gear'); ?><span><strong>محتوى متخصص</strong><small>تشخيص ومعلومات منظمة</small></span></div>
      <div><?php echo a3g_icon('car'); ?><span><strong>قاعدة مركبات</strong><small>سيارات وموتوسيكلات</small></span></div>
      <div><?php echo a3g_icon('pin'); ?><span><strong>خدمات وسوق</strong><small>مراكز ومعارض وقطع غيار</small></span></div>
      <div><?php echo a3g_icon('calendar'); ?><span><strong>ملكية وصيانة</strong><small>جراج وسجل وتذكيرات</small></span></div>
    </div>
  </div>
</section>

</main>
<?php get_footer(); ?>
