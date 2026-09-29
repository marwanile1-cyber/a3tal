<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0B1220">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<header class="a3-site-header">
  <div class="a3-container a3-header-row">
    <a class="a3-brand" href="<?php echo esc_url(home_url('/')); ?>">
      <span class="a3-brand-mark">أ</span>
      <span class="a3-brand-copy"><strong>أعطال.كوم</strong><small>افهم العطل قبل تغيير القطعة</small></span>
    </a>
    <nav class="a3-main-nav" aria-label="القائمة الرئيسية">
      <?php wp_nav_menu(['theme_location'=>'primary','container'=>false,'fallback_cb'=>'a3du_menu_fallback','depth'=>1]); ?>
    </nav>
    <div class="a3-header-actions">
      <a class="a3-icon-btn" href="<?php echo esc_url(a3du_search_url('')); ?>" aria-label="البحث">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
      </a>
      <button class="a3-icon-btn a3-menu-toggle" type="button" aria-label="القائمة" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
  <nav class="a3-mobile-menu" aria-label="قائمة الموبايل"><?php a3du_menu_fallback(); ?></nav>
</header>
