<?php
if (!defined('ABSPATH')) exit;
$dtc_library_url = get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/');
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class('a3g-dtc-library'); ?>>
<?php wp_body_open(); ?>
<a class="d-skip-link" href="#dtc-main">انتقل إلى المحتوى</a>
<header class="d-header">
  <div class="d-wrap d-header-row">
    <a class="d-brand" data-google-vignette="false" href="<?php echo esc_url(home_url('/')); ?>" aria-label="أعطال.كوم — الرئيسية">
      <?php a3g_logo(); ?>
      <span class="d-brand-sub">مكتبة أكواد الأعطال</span>
    </a>
    <nav class="d-nav" aria-label="تنقل دليل أعطال">
      <a data-google-vignette="false" href="<?php echo esc_url($dtc_library_url); ?>" <?php if (is_post_type_archive('a3_dtc')) echo 'aria-current="page"'; ?>>مكتبة الأكواد</a>
      <a data-google-vignette="false" href="<?php echo esc_url($dtc_library_url . '#dtc-community'); ?>">الأسئلة والتجارب</a>
      <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>">السيارات</a>
      <a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>">مراكز الخدمة</a>
    </nav>
    <a class="d-return" data-google-vignette="false" href="<?php echo esc_url(home_url('/?s=')); ?>">البحث في أعطال</a>
  </div>
</header>
