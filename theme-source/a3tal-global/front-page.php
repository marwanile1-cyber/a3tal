<?php
get_header();

$hero_q=a3g_query(['cat'=>374,'posts_per_page'=>1]);
$hero_id=0;$hero_img='';
if($hero_q->have_posts()){ $hero_q->the_post(); $hero_id=get_the_ID(); $hero_img=get_the_post_thumbnail_url($hero_id,'full'); }
wp_reset_postdata();

$prices=a3g_query(['cat'=>374,'posts_per_page'=>4,'post__not_in'=>$hero_id?[$hero_id]:[]]);
$reviews=a3g_query(['category__in'=>[22,21],'posts_per_page'=>3]);
$faults=a3g_query(['category__in'=>[8,13,2,18],'posts_per_page'=>4]);
$care=a3g_query(['category__in'=>[86,3,85],'posts_per_page'=>4]);
$service=a3g_query(['cat'=>33,'posts_per_page'=>3]);
$news=a3g_query(['posts_per_page'=>4,'post__not_in'=>$hero_id?[$hero_id]:[]]);
?>
<main class="g-home">

<section class="g-hero-section">
  <div class="g-wrap">
    <div class="g-hero" <?php if($hero_img): ?>style="background-image:linear-gradient(90deg,rgba(5,14,24,.94) 0%,rgba(5,14,24,.72) 44%,rgba(5,14,24,.26) 100%),url('<?php echo esc_url($hero_img); ?>')"<?php endif; ?>>
      <div class="g-hero-content">
        <span class="g-hero-eyebrow">A3TAL AUTOMOTIVE</span>
        <h1>كل ما يخص عالم السيارات</h1>
        <p>ابحث، قارن، اكتشف، افهم الأعطال، واتخذ قرارك على الطريق الصحيح.</p>

        <div class="g-hero-tabs" role="navigation" aria-label="اختصارات البحث">
          <a class="is-active" href="<?php echo esc_url(a3g_cat_link(374)); ?>"><?php echo a3g_icon('car'); ?><span>ابحث عن سيارة</span></a>
          <a href="<?php echo esc_url(a3g_cat_link(8)); ?>"><?php echo a3g_icon('wrench'); ?><span>اعرف العطل</span></a>
          <a href="<?php echo esc_url(a3g_cat_link(21)); ?>"><?php echo a3g_icon('compare'); ?><span>قارن بين سيارتين</span></a>
          <a href="<?php echo esc_url(a3g_cat_link(33)); ?>"><?php echo a3g_icon('pin'); ?><span>ابحث عن مركز خدمة</span></a>
        </div>

        <form class="g-hero-search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
          <div class="g-search-field"><?php echo a3g_icon('search'); ?><input type="search" name="s" placeholder="ابحث عن ماركة، موديل، عطل أو كلمة مفتاحية..." aria-label="بحث"></div>
          <button type="submit"><?php echo a3g_icon('search'); ?><span>بحث</span></button>
        </form>
      </div>
      <?php if($hero_id): ?><a class="g-hero-story" href="<?php echo esc_url(get_permalink($hero_id)); ?>"><span>الأحدث</span><strong><?php echo esc_html(get_the_title($hero_id)); ?></strong></a><?php endif; ?>
    </div>

    <div class="g-quick-grid">
      <a href="<?php echo esc_url(add_query_arg('s','SUV',home_url('/'))); ?>"><?php echo a3g_icon('car'); ?><span>SUV</span></a>
      <a href="<?php echo esc_url(add_query_arg('s','سيدان',home_url('/'))); ?>"><?php echo a3g_icon('car'); ?><span>سيدان</span></a>
      <a href="<?php echo esc_url(add_query_arg('s','سيارات هجينة',home_url('/'))); ?>"><?php echo a3g_icon('leaf'); ?><span>السيارات الهجينة</span></a>
      <a href="<?php echo esc_url(add_query_arg('s','سيارات كهربائية',home_url('/'))); ?>"><?php echo a3g_icon('bolt'); ?><span>السيارات الكهربائية</span></a>
      <a href="<?php echo esc_url(a3g_cat_link(3)); ?>"><?php echo a3g_icon('wrench'); ?><span>الصيانة</span></a>
      <a href="<?php echo esc_url(a3g_cat_link(2)); ?>"><?php echo a3g_icon('gear'); ?><span>أكواد الأعطال</span></a>
    </div>
  </div>
</section>

<section class="g-section">
  <div class="g-wrap">
    <div class="g-section-head"><div><span>السوق</span><h2>أحدث أسعار السيارات</h2></div><a href="<?php echo esc_url(a3g_cat_link(374)); ?>">عرض جميع الأسعار</a></div>
    <div class="g-price-grid"><?php while($prices->have_posts()){$prices->the_post();a3g_price_card();}wp_reset_postdata(); ?></div>
  </div>
</section>

<section class="g-section g-section-soft">
  <div class="g-wrap">
    <div class="g-section-head"><div><span>تجارب حقيقية</span><h2>مراجعات وتجارب القيادة</h2></div><a href="<?php echo esc_url(a3g_cat_link(22)); ?>">عرض جميع المراجعات</a></div>
    <div class="g-review-grid"><?php while($reviews->have_posts()){$reviews->the_post();a3g_card(get_the_ID(),'g-review-card');}wp_reset_postdata(); ?></div>
  </div>
</section>

<section class="g-section">
  <div class="g-wrap g-duo-grid">
    <div class="g-feature-box g-compare-box">
      <div class="g-box-head"><div><span>قرار أسرع</span><h2>قارن بين السيارات</h2></div><a href="<?php echo esc_url(a3g_cat_link(21)); ?>">ابدأ المقارنة</a></div>
      <div class="g-compare-visual">
        <div class="g-compare-car"><?php echo a3g_icon('car'); ?><span>السيارة الأولى</span></div>
        <b>VS</b>
        <div class="g-compare-car"><?php echo a3g_icon('car'); ?><span>السيارة الثانية</span></div>
      </div>
      <p>قارن المواصفات والتجهيزات ونقاط القوة والضعف قبل الحجز.</p>
    </div>

    <div class="g-feature-box g-fault-box">
      <div class="g-box-head"><div><span>تشخيص ذكي</span><h2>أعطال شائعة وأكواد الأعطال</h2></div><a href="<?php echo esc_url(a3g_cat_link(8)); ?>">عرض جميع الأعطال</a></div>
      <div class="g-fault-icons">
        <a href="<?php echo esc_url(a3g_cat_link(8)); ?>"><?php echo a3g_icon('gear'); ?><span>أعطال المحرك</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(13)); ?>"><?php echo a3g_icon('bolt'); ?><span>أعطال الكهرباء</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(2)); ?>"><?php echo a3g_icon('gear'); ?><span>أكواد DTC</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(18)); ?>"><?php echo a3g_icon('wrench'); ?><span>التكييف</span></a>
      </div>
      <form class="g-mini-search" method="get" action="<?php echo esc_url(home_url('/')); ?>"><input name="s" placeholder="ابحث عن عطل أو كود مثل P0171"><button><?php echo a3g_icon('search'); ?>بحث</button></form>
    </div>
  </div>
</section>

<section class="g-section g-section-soft">
  <div class="g-wrap g-duo-grid g-duo-bottom">
    <div class="g-feature-box">
      <div class="g-box-head"><div><span>العناية بسيارتك</span><h2>جداول الصيانة والزيوت وقطع الغيار</h2></div><a href="<?php echo esc_url(a3g_cat_link(3)); ?>">عرض المزيد</a></div>
      <div class="g-tool-grid">
        <a href="<?php echo esc_url(a3g_cat_link(86)); ?>"><?php echo a3g_icon('calendar'); ?><span>جداول الصيانة</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(3)); ?>"><?php echo a3g_icon('oil'); ?><span>زيوت المحرك</span></a>
        <a href="<?php echo esc_url(a3g_cat_link(85)); ?>"><?php echo a3g_icon('filter'); ?><span>قطع الغيار</span></a>
        <a href="<?php echo esc_url(add_query_arg('s','فلاتر السيارة',home_url('/'))); ?>"><?php echo a3g_icon('filter'); ?><span>الفلاتر</span></a>
      </div>
      <div class="g-care-feed"><?php while($care->have_posts()){$care->the_post();a3g_compact();}wp_reset_postdata(); ?></div>
    </div>

    <div class="g-feature-box g-service-box">
      <div class="g-box-head"><div><span>دليل موثوق</span><h2>مراكز الخدمة المعتمدة</h2></div><a href="<?php echo esc_url(a3g_cat_link(33)); ?>">عرض جميع المراكز</a></div>
      <form class="g-mini-search" method="get" action="<?php echo esc_url(home_url('/')); ?>"><input name="s" value="" placeholder="ابحث عن مدينة، ماركة أو مركز خدمة"><button><?php echo a3g_icon('search'); ?>بحث</button></form>
      <div class="g-map-visual"><span class="g-map-road r1"></span><span class="g-map-road r2"></span><i class="p1"><?php echo a3g_icon('pin'); ?></i><i class="p2"><?php echo a3g_icon('pin'); ?></i><i class="p3"><?php echo a3g_icon('pin'); ?></i></div>
      <div class="g-service-feed"><?php while($service->have_posts()){$service->the_post();a3g_compact();}wp_reset_postdata(); ?></div>
    </div>
  </div>
</section>

<section class="g-section">
  <div class="g-wrap">
    <div class="g-section-head"><div><span>الجديد الآن</span><h2>آخر الأخبار والترند</h2></div><a href="<?php echo esc_url(home_url('/')); ?>">عرض المزيد</a></div>
    <div class="g-news-grid"><?php while($news->have_posts()){$news->the_post();a3g_card(get_the_ID(),'g-news-card');}wp_reset_postdata(); ?></div>

    <div class="g-trust-strip">
      <div><?php echo a3g_icon('gear'); ?><span><strong>محتوى متخصص</strong><small>من فريق أعطال.كوم</small></span></div>
      <div><?php echo a3g_icon('car'); ?><span><strong>صور وتجارب حقيقية</strong><small>عرض واضح وسهل المقارنة</small></span></div>
      <div><?php echo a3g_icon('pin'); ?><span><strong>مراكز خدمة</strong><small>بيانات منظمة وسهلة الوصول</small></span></div>
      <div><?php echo a3g_icon('bolt'); ?><span><strong>معلومات محدثة</strong><small>مراجعة دورية للأسعار والمواصفات</small></span></div>
    </div>
  </div>
</section>

</main>
<?php get_footer(); ?>
