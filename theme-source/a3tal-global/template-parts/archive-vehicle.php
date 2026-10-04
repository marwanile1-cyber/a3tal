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
  <?php else: ?>
    <div class="g-platform-empty">
      <span><?php echo $is_moto?'🏍️':'🚘'; ?></span>
      <h2>لا توجد نتائج منشورة بهذه الفلاتر حاليًا</h2>
      <p>نحن لا ننشر مركبة داخل قاعدة البيانات قبل مراجعة بياناتها ومصدرها. غيّر الفلاتر أو عد لاحقًا بعد إضافة البيانات الموثقة.</p>
      <a href="<?php echo esc_url(get_post_type_archive_link($type)); ?>">مسح الفلاتر</a>
    </div>
  <?php endif; ?>
</main>
<?php get_footer(); ?>
