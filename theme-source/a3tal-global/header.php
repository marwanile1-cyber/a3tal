<?php
$g_header_ticker_q = a3g_query(['posts_per_page'=>8]);
$g_header_ticker_items = [];
while($g_header_ticker_q->have_posts()){
  $g_header_ticker_q->the_post();
  $g_header_ticker_items[] = ['title'=>get_the_title(),'url'=>get_permalink()];
}
wp_reset_postdata();
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<header class="g-header">
  <div class="g-wrap g-header-row">
    <a class="g-brand" href="<?php echo esc_url(home_url('/')); ?>" aria-label="أعطال.كوم"><?php a3g_logo(); ?></a>
    <nav class="g-main-nav g-platform-nav" aria-label="القائمة الرئيسية">
      <div class="g-nav-item"><a href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">السيارات</a><div class="g-nav-drop"><a href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">قاعدة السيارات</a><a href="<?php echo esc_url(a3g_cat_link(374)); ?>">الأسعار</a><a href="<?php echo esc_url(a3g_cat_link(22)); ?>">المراجعات</a></div></div>
      <div class="g-nav-item"><a href="<?php echo esc_url(a3g_platform_link('a3_motorcycle','/motorcycles/')); ?>">الموتوسيكلات</a><div class="g-nav-drop"><a href="<?php echo esc_url(a3g_platform_link('a3_motorcycle','/motorcycles/')); ?>">الموديلات والأسعار</a><a href="<?php echo esc_url(add_query_arg('s','موتوسيكل',home_url('/'))); ?>">المحتوى</a></div></div>
      <div class="g-nav-item"><a href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>">الأعطال والأكواد</a><div class="g-nav-drop"><a href="<?php echo esc_url(a3g_cat_link(8)); ?>">أعطال وحلول</a><a href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>">أكواد DTC</a><a href="<?php echo esc_url(a3g_cat_link(13)); ?>">كهرباء السيارات</a></div></div>
      <div class="g-nav-item"><a href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>">الصيانة وقطع الغيار</a><div class="g-nav-drop"><a href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>">جداول الصيانة</a><a href="<?php echo esc_url(a3g_platform_link('a3_part','/parts/')); ?>">قطع الغيار</a><a href="<?php echo esc_url(a3g_platform_link('a3_parts_vendor','/parts-stores/')); ?>">أماكن بيع القطع</a><a href="<?php echo esc_url(a3g_cat_link(3)); ?>">الزيوت والصيانة</a></div></div>
      <div class="g-nav-item"><a href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>">الخدمات</a><div class="g-nav-drop"><a href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>">مراكز الخدمة</a><a href="<?php echo esc_url(a3g_platform_link('a3_showroom','/car-showrooms/')); ?>">معارض السيارات</a><a href="<?php echo esc_url(a3g_platform_link('a3_parts_vendor','/parts-stores/')); ?>">بائعو قطع الغيار</a></div></div>
      <div class="g-nav-item"><a href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>">السوق</a><div class="g-nav-drop"><a href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>">سيارات للبيع</a><a href="<?php echo esc_url(home_url('/my-garage/')); ?>">بيع سيارتي</a><a href="<?php echo esc_url(a3g_platform_link('a3_showroom','/car-showrooms/')); ?>">المعارض</a></div></div>
      <a href="<?php echo esc_url(a3g_cat_link(21)); ?>">قارن</a>
      <a class="g-mycar-link" href="<?php echo esc_url(home_url('/my-garage/')); ?>"><?php echo a3g_icon('car'); ?><span>سيارتي</span></a>
    </nav>
    <div class="g-head-tools">
      <a class="g-head-loc" href="<?php echo esc_url(a3g_cat_link(33)); ?>"><?php echo a3g_icon('pin'); ?><span>مصر والخليج</span></a>
      <a class="g-head-search" href="<?php echo esc_url(home_url('/?s=')); ?>" aria-label="البحث"><?php echo a3g_icon('search'); ?></a>
      <button class="g-menu-toggle" type="button" aria-expanded="false" aria-label="فتح القائمة"><?php echo a3g_icon('menu'); ?></button>
    </div>
  </div>
  <?php if($g_header_ticker_items): ?>
  <div class="g-newsbar" aria-label="آخر أخبار ومقالات أعطال.كوم">
    <div class="g-wrap g-newsbar-row">
      <span class="g-newsbar-label"><i></i>آخر الأخبار</span>
      <div class="g-newsbar-viewport" data-a3tal-news-ticker>
        <div class="g-newsbar-track">
          <div class="g-newsbar-group">
            <?php foreach($g_header_ticker_items as $item): ?>
              <a href="<?php echo esc_url($item['url']); ?>"><b></b><?php echo esc_html($item['title']); ?></a>
            <?php endforeach; ?>
          </div>
          <div class="g-newsbar-group" aria-hidden="true">
            <?php foreach($g_header_ticker_items as $item): ?>
              <a tabindex="-1" href="<?php echo esc_url($item['url']); ?>"><b></b><?php echo esc_html($item['title']); ?></a>
            <?php endforeach; ?>
          </div>
        </div>
      </div>
    </div>
  </div>
  <?php endif; ?>
  <nav class="g-mobile-menu" aria-label="قائمة الجوال">
    <a href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">السيارات</a>
    <a href="<?php echo esc_url(a3g_platform_link('a3_motorcycle','/motorcycles/')); ?>">الموتوسيكلات والسكوتر</a>
    <a href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>">أكواد الأعطال DTC</a>
    <a href="<?php echo esc_url(a3g_cat_link(8)); ?>">الأعطال والتشخيص</a>
    <a href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>">جداول الصيانة</a>
    <a href="<?php echo esc_url(a3g_platform_link('a3_part','/parts/')); ?>">قطع الغيار</a>
    <a href="<?php echo esc_url(a3g_platform_link('a3_parts_vendor','/parts-stores/')); ?>">أماكن بيع قطع الغيار</a>
    <a href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>">مراكز الخدمة</a>
    <a href="<?php echo esc_url(a3g_platform_link('a3_showroom','/car-showrooms/')); ?>">معارض السيارات</a>
    <a href="<?php echo esc_url(a3g_platform_link('a3_listing','/cars-for-sale/')); ?>">سيارات للبيع</a>
    <a href="<?php echo esc_url(a3g_cat_link(21)); ?>">المقارنات</a>
    <a href="<?php echo esc_url(home_url('/my-garage/')); ?>">سيارتي</a>
  </nav>
</header>
