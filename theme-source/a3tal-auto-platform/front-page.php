<?php get_header();
$lead=a3ap_query(['posts_per_page'=>5]);$lead_ids=[];$lead_posts=[];while($lead->have_posts()){$lead->the_post();$lead_posts[]=get_post();$lead_ids[]=get_the_ID();}wp_reset_postdata();
$market=a3ap_query(['cat'=>374,'posts_per_page'=>4,'post__not_in'=>$lead_ids]);
$buy=a3ap_query(['category__in'=>[22,21,20],'posts_per_page'=>4,'post__not_in'=>$lead_ids]);
$diag=a3ap_query(['category__in'=>[8,13,2,18],'posts_per_page'=>4,'post__not_in'=>$lead_ids]);
$service=a3ap_query(['cat'=>33,'posts_per_page'=>3]);
$care=a3ap_query(['category__in'=>[86,3,85],'posts_per_page'=>4]);
?>
<section class="ap-home-hero"><div class="ap-wrap">
  <div class="ap-home-intro"><div><span class="ap-pill">A3TAL AUTO PLATFORM</span><h1>كل قرار يخص عربيتك يبدأ من هنا.</h1><p>اعرف السعر والمواصفات، قارن قبل الشراء، افهم العطل، تابع الصيانة، ووصل لمركز الخدمة المناسب.</p></div>
  <form class="ap-global-search" method="get" action="<?php echo esc_url(home_url('/')); ?>"><input name="s" placeholder="ابحث باسم عربية، سعر، عطل، كود، قطعة غيار أو مركز خدمة"><button>بحث</button></form></div>
  <?php if($lead_posts): $hero=$lead_posts[0]; ?>
  <div class="ap-news-grid">
    <article class="ap-lead-story"><a class="ap-lead-media" href="<?php echo esc_url(get_permalink($hero)); ?>"><?php if(has_post_thumbnail($hero)){echo get_the_post_thumbnail($hero,'full',['loading'=>'eager','fetchpriority'=>'high']);}else{echo '<span class="ap-fallback">A3TAL</span>';} ?><span class="ap-lead-shade"></span><div class="ap-lead-copy"><?php $c=a3ap_primary_cat($hero); if($c): ?><span class="ap-kicker ap-kicker-light"><?php echo esc_html($c->name); ?></span><?php endif; ?><h2><?php echo esc_html(get_the_title($hero)); ?></h2><p><?php echo esc_html(a3ap_excerpt($hero,24)); ?></p></div></a></article>
    <div class="ap-headlines"><?php foreach(array_slice($lead_posts,1) as $p) a3ap_compact($p->ID); ?></div>
  </div><?php endif; ?>
</div></section>

<section class="ap-paths-section"><div class="ap-wrap"><div class="ap-section-title"><div><span class="ap-overline">ابدأ حسب هدفك</span><h2>مش كل زائر داخل الموقع لنفس السبب</h2></div></div>
<div class="ap-paths">
<a class="ap-path ap-path-blue" href="<?php echo esc_url(a3ap_cat_link(374)); ?>"><span>01</span><h3>عايز أشتري عربية</h3><p>أسعار، مواصفات، فئات، مراجعات ومقارنات قبل الحجز.</p><b>ابدأ من السوق ←</b></a>
<a class="ap-path ap-path-cyan" href="<?php echo esc_url(home_url('/choose-your-car/')); ?>"><span>02</span><h3>عايز أعرف عربيتي</h3><p>اختار الماركة والموديل للوصول للمحتوى المرتبط بسيارتك.</p><b>اختار سيارتك ←</b></a>
<a class="ap-path ap-path-amber" href="<?php echo esc_url(a3ap_cat_link(8)); ?>"><span>03</span><h3>عندي مشكلة أو عطل</h3><p>ابدأ من العرض أو النظام، ثم انتقل للتشخيص والاختبارات.</p><b>شخّص المشكلة ←</b></a>
<a class="ap-path ap-path-green" href="<?php echo esc_url(a3ap_cat_link(33)); ?>"><span>04</span><h3>بدور على خدمة</h3><p>مراكز خدمة، توكيلات، قطع غيار ومعلومات صيانة عملية.</p><b>افتح دليل الخدمات ←</b></a>
</div></div></section>

<section class="ap-section"><div class="ap-wrap"><div class="ap-section-title"><div><span class="ap-overline">السوق الآن</span><h2>أسعار ومواصفات السيارات الجديدة</h2><p>أحدث الأسعار والموديلات والفئات المنشورة على أعطال.كوم.</p></div><a class="ap-section-link" href="<?php echo esc_url(a3ap_cat_link(374)); ?>">كل الأسعار ←</a></div><div class="ap-card-grid"><?php while($market->have_posts()){$market->the_post();a3ap_card();}wp_reset_postdata(); ?></div></div></section>

<section class="ap-section ap-soft"><div class="ap-wrap"><div class="ap-split-title"><div><span class="ap-overline">قبل ما تدفع</span><h2>مراجعات، مقارنات ودليل شراء</h2><p>المهم مش مين أرخص. المهم إيه الأنسب لاستخدامك وميزانيتك وتكلفة امتلاكك.</p></div><div class="ap-mini-links"><a href="<?php echo esc_url(a3ap_cat_link(22)); ?>">المراجعات</a><a href="<?php echo esc_url(a3ap_cat_link(21)); ?>">المقارنات</a><a href="<?php echo esc_url(a3ap_cat_link(20)); ?>">المستعمل</a></div></div><div class="ap-card-grid"><?php while($buy->have_posts()){$buy->the_post();a3ap_card();}wp_reset_postdata(); ?></div></div></section>

<section class="ap-diagnostic-zone"><div class="ap-wrap ap-diagnostic-grid"><div class="ap-diagnostic-copy"><span class="ap-pill">DIAGNOSTIC LAB</span><h2>العربية بتقولك حاجة. افهمها قبل ما تغيّر قطع.</h2><p>ابحث بالعرض أو كود DTC أو النظام. أعطال.كوم يفصل بين العرض والسبب والاختبار والإصلاح.</p><form class="ap-diag-search" method="get" action="<?php echo esc_url(home_url('/')); ?>"><input name="s" placeholder="مثال: P0420، العربية بتنتش، ونة مع السرعة"><button>ابدأ التشخيص</button></form><div class="ap-diag-links"><a href="<?php echo esc_url(a3ap_cat_link(8)); ?>">ميكانيكا</a><a href="<?php echo esc_url(a3ap_cat_link(13)); ?>">كهرباء</a><a href="<?php echo esc_url(a3ap_cat_link(2)); ?>">DTC</a><a href="<?php echo esc_url(a3ap_cat_link(18)); ?>">التكييف</a></div></div><div class="ap-diag-feed"><?php while($diag->have_posts()){$diag->the_post();a3ap_compact();}wp_reset_postdata(); ?></div></div></section>

<section class="ap-section"><div class="ap-wrap"><div class="ap-section-title"><div><span class="ap-overline">خدمة وصيانة</span><h2>صيانة، قطع غيار ومراكز خدمة</h2><p>من جدول الصيانة وحتى اختيار مكان الخدمة أو قطعة الغيار.</p></div></div><div class="ap-service-layout"><div class="ap-service-feature"><div class="ap-service-icon">⌖</div><span class="ap-overline">دليل المراكز</span><h3>وصل لمركز الخدمة أو التوكيل المناسب</h3><p>صفحات مراكز الخدمة والتوكيلات جزء أساسي من المنصة، وليست ذيلًا في الفوتر.</p><a class="ap-action" href="<?php echo esc_url(a3ap_cat_link(33)); ?>">استكشف مراكز الخدمة ←</a></div><div class="ap-service-list"><?php while($service->have_posts()){$service->the_post();a3ap_compact();}wp_reset_postdata(); ?></div></div>
<div class="ap-card-grid ap-care-grid"><?php while($care->have_posts()){$care->the_post();a3ap_card();}wp_reset_postdata(); ?></div></div></section>

<section class="ap-tools-strip"><div class="ap-wrap ap-tools-grid"><a href="<?php echo esc_url(a3ap_cat_link(2790)); ?>"><b>المرور والتراخيص</b><span>غرامات، إجراءات ومعلومات مهمة للسائق.</span></a><a href="<?php echo esc_url(a3ap_cat_link(85)); ?>"><b>قطع الغيار</b><span>أسعار، بدائل ونصائح قبل الشراء.</span></a><a href="<?php echo esc_url(a3ap_cat_link(86)); ?>"><b>جداول الصيانة</b><span>مواعيد الصيانة وما يتم فحصه وتغييره.</span></a><a href="<?php echo esc_url(a3ap_cat_link(2)); ?>"><b>أكواد DTC</b><span>مرجع تقني داخل المنصة، مش المنصة كلها.</span></a></div></section>
<?php get_footer(); ?>
