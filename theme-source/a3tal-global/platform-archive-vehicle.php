<?php
if (!defined('ABSPATH')) exit;
$type=$a3g_vehicle_type??get_query_var('post_type');
$is_moto=$type==='a3_motorcycle';
$title=$is_moto?'الموتوسيكلات والسكوتر':'السيارات';
$subtitle=$is_moto?'أسعار ومواصفات ومراجعات وصيانة الموتوسيكلات والسكوتر في مكان واحد.':'اكتشف السيارات حسب الماركة والسوق والسنة ونوع الهيكل، مع الأسعار والمواصفات والمحتوى المرتبط.';
$type_tax=$is_moto?'a3_motorcycle_type':'a3_car_body';
$brands=get_terms(['taxonomy'=>'a3_brand','hide_empty'=>false]);
$markets=get_terms(['taxonomy'=>'a3_market','hide_empty'=>false]);
$types=get_terms(['taxonomy'=>$type_tax,'hide_empty'=>false]);
?>
<?php get_header(); ?>
<section class="g-platform-archive-hero">
  <div class="g-wrap">
    <span><?php echo $is_moto?'A3TAL MOTORCYCLES':'A3TAL CARS'; ?></span>
    <h1><?php echo esc_html($title); ?></h1>
    <p><?php echo esc_html($subtitle); ?></p>
    <form class="g-platform-filter" method="get">
      <label><small>الماركة</small><select name="brand"><option value="">كل الماركات</option><?php foreach($brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('brand'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small>السوق</small><select name="market"><option value="">كل الأسواق</option><?php foreach($markets as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('market'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small><?php echo $is_moto?'النوع':'نوع الهيكل'; ?></small><select name="vehicle_type"><option value="">كل الأنواع</option><?php foreach($types as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('vehicle_type'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small>سنة الموديل</small><input type="number" min="1950" max="2100" name="year" value="<?php echo esc_attr((string)get_query_var('year')); ?>" placeholder="2026"></label>
      <button type="submit"><?php echo a3g_icon('search'); ?><span>فلترة</span></button>
    </form>
  </div>
</section>

<main class="g-wrap g-platform-archive">
  <div class="g-platform-archive-head">
    <div><span>قاعدة بيانات أعطال</span><h2><?php echo $is_moto?'اختر الموتوسيكل المناسب':'اختر السيارة المناسبة'; ?></h2></div>
    <b><?php global $wp_query; echo esc_html(number_format_i18n((int)$wp_query->found_posts)); ?> نتيجة</b>
  </div>

  <?php if(have_posts()): ?>
    <div class="g-platform-grid">
      <?php while(have_posts()):the_post();a3g_platform_card();endwhile; ?>
    </div>
    <div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
  <?php elseif($is_moto): ?>
    <div class="g-platform-empty">
      <span>🏍️</span>
      <h2>لا توجد نتائج منشورة بهذه الفلاتر حاليًا</h2>
      <p>غيّر الفلاتر أو ارجع للقائمة الكاملة للموتوسيكلات المنشورة.</p>
      <a href="<?php echo esc_url(get_post_type_archive_link($type)); ?>">مسح الفلاتر</a>
    </div>
  <?php else: ?>
    <div class="g-platform-bridge-note">
      <span>🚘</span>
      <div><h2>قاعدة السيارات المنظمة بتتبني من المحتوى الموجود</h2><p>بدل ما نعمل صفحات جديدة تنافس مقالات الموقع القديمة، بنربط الأسعار والمراجعات والمقارنات الحالية هنا ونحوّل أهم الموديلات تدريجيًا إلى بيانات منظمة.</p></div>
    </div>
  <?php endif; ?>

  <?php if(!$is_moto): ?>
    <?php a3g_legacy_section([374],'أسعار السيارات الجديدة','كل صفحات الأسعار الحالية تفضل على روابطها الأصلية وتظهر هنا داخل قسم السيارات.',8,[],374); ?>
    <?php a3g_legacy_section([22],'مراجعات السيارات','مراجعات وتجارب الشراء الموجودة بالفعل، من غير إنشاء نسخ جديدة لنفس النية.',6,[],22); ?>
    <?php a3g_legacy_section([21],'مقارنات بين السيارات','المقارنات الحالية مرتبطة بقسم السيارات بدل ما تفضل معزولة في تصنيف منفصل.',6,[],21); ?>
  <?php endif; ?>
</main>
<?php get_footer(); ?>
