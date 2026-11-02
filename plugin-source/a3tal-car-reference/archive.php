<?php
defined('ABSPATH')||exit;
get_header();
$q=isset($_GET['q'])?sanitize_text_field(wp_unslash($_GET['q'])):'';
$posts=get_posts(['post_type'=>A3tal_Car_Reference_Engine::TYPE,'post_status'=>'publish','numberposts'=>60]+($q?['s'=>$q]:['post_parent'=>0,'orderby'=>'title','order'=>'ASC']));
?>
<main class="a3cr-wrap" dir="rtl">
<nav class="a3cr-crumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a> / دليل المواصفات الفنية</nav>
<header class="a3cr-hero"><p>A3TAL CAR REFERENCE</p><h1>دليل المواصفات الفنية للسيارات</h1><p>المقاسات والسعات والزيوت والبيانات الفنية حسب الماركة والموديل والمحرك، مع مراجعة المصادر قبل النشر.</p>
<form method="get" action="<?php echo esc_url(get_post_type_archive_link(A3tal_Car_Reference_Engine::TYPE)); ?>"><label class="screen-reader-text" for="a3cr-q">اسم السيارة</label><input id="a3cr-q" name="q" type="search" placeholder="ابحث باسم الماركة أو الموديل" value="<?php echo esc_attr($q); ?>"><button>بحث</button></form></header>
<section><h2>الأقسام الفنية</h2><div class="a3cr-grid a3cr-kinds">
<?php foreach(['زيت المحرك','زيت ناقل الحركة','مقاسات الإطارات','البطاريات','البوجيهات','الفلاتر','المساحات','الفيوزات'] as $label): ?><div class="a3cr-tile"><strong><?php echo esc_html($label); ?></strong><small>بحسب الموديل والمحرك</small></div><?php endforeach; ?>
</div></section>
<section><h2><?php echo $q?'نتائج البحث':'الماركات المتاحة'; ?></h2><div class="a3cr-grid">
<?php if(!$posts): ?><p class="a3cr-empty">الصفحات الفنية قيد مراجعة البيانات والمصادر. يمكن تصفح <a href="<?php echo esc_url(home_url('/cars/')); ?>">دليل السيارات</a> و<a href="<?php echo esc_url(home_url('/dtc/')); ?>">مكتبة أكواد الأعطال</a> حاليًا.</p><?php endif; ?>
<?php foreach($posts as $item) A3tal_Car_Reference_Engine::card($item); ?></div></section>
</main>
<?php get_footer(); ?>