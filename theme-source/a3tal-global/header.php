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
    <nav class="g-main-nav" aria-label="القائمة الرئيسية">
      <a href="<?php echo esc_url(a3g_cat_link(374)); ?>">أسعار السيارات</a>
      <a href="<?php echo esc_url(a3g_cat_link(22)); ?>">مراجعات</a>
      <a href="<?php echo esc_url(a3g_cat_link(21)); ?>">مقارنات</a>
      <a href="<?php echo esc_url(a3g_cat_link(8)); ?>">أعطال وحلول</a>
      <a href="<?php echo esc_url(a3g_cat_link(3)); ?>">الصيانة</a>
      <a href="<?php echo esc_url(a3g_cat_link(33)); ?>">مراكز الخدمة</a>
      <a href="<?php echo esc_url(home_url('/?s=أخبار+السيارات')); ?>">أخبار السيارات</a>
    </nav>
    <div class="g-head-tools">
      <a class="g-head-loc" href="<?php echo esc_url(a3g_cat_link(33)); ?>"><?php echo a3g_icon('pin'); ?><span>مصر والخليج</span></a>
      <a class="g-head-search" href="<?php echo esc_url(home_url('/?s=')); ?>" aria-label="البحث"><?php echo a3g_icon('search'); ?></a>
      <button class="g-menu-toggle" type="button" aria-expanded="false" aria-label="فتح القائمة"><?php echo a3g_icon('menu'); ?></button>
    </div>
  </div>
  <nav class="g-mobile-menu" aria-label="قائمة الجوال">
    <a href="<?php echo esc_url(a3g_cat_link(374)); ?>">أسعار السيارات</a>
    <a href="<?php echo esc_url(a3g_cat_link(22)); ?>">المراجعات</a>
    <a href="<?php echo esc_url(a3g_cat_link(21)); ?>">المقارنات</a>
    <a href="<?php echo esc_url(a3g_cat_link(8)); ?>">الأعطال الميكانيكية</a>
    <a href="<?php echo esc_url(a3g_cat_link(13)); ?>">كهرباء السيارات</a>
    <a href="<?php echo esc_url(a3g_cat_link(2)); ?>">أكواد الأعطال DTC</a>
    <a href="<?php echo esc_url(a3g_cat_link(3)); ?>">الصيانة والزيوت</a>
    <a href="<?php echo esc_url(a3g_cat_link(33)); ?>">مراكز الخدمة</a>
  </nav>
</header>
