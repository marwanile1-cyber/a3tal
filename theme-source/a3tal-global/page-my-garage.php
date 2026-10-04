<?php
/**
 * Template for the private My A3tal Garage dashboard.
 */
if (defined('A3CP_DIR') && file_exists(A3CP_DIR . 'my-garage.php')) {
    require A3CP_DIR . 'my-garage.php';
    return;
}
get_header();
?>
<section class="g-error"><div class="g-wrap"><span>MY A3TAL GARAGE</span><h1>سيارتي غير متاحة مؤقتًا</h1><p>طبقة A3tal Core Platform غير محمّلة حاليًا.</p></div></section>
<?php get_footer(); ?>
