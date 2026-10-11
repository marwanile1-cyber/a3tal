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
    <a class="d-brand" href="<?php echo esc_url($dtc_library_url); ?>" aria-label="رئيسية دليل أعطال">
      <span class="d-brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m13-5h3a2 2 0 0 1 2 2v3M3 16v3a2 2 0 0 0 2 2h3m8 0h3a2 2 0 0 0 2-2v-3M3 12h18"/><path d="m7 9 2 6 3-7 3 7 2-6"/></svg></span>
      <span><span class="d-brand-name">دليل أعطال<span>.</span></span><span class="d-brand-sub" lang="en" dir="ltr">THE DTC LIBRARY</span></span>
    </a>
    <nav class="d-nav" aria-label="تنقل دليل أعطال">
      <a href="<?php echo esc_url($dtc_library_url); ?>" <?php if (is_post_type_archive('a3_dtc')) echo 'aria-current="page"'; ?>>مكتبة الأكواد</a>
      <a href="<?php echo esc_url($dtc_library_url . '#dtc-community'); ?>">الأسئلة والتجارب</a>
    </nav>
    <a class="d-return" href="<?php echo esc_url(home_url('/')); ?>">أعطال.كوم <span aria-hidden="true">↖</span></a>
  </div>
</header>
