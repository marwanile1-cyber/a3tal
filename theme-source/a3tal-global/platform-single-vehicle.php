<?php
if (!defined('ABSPATH')) exit;
$type=get_post_type();
$is_moto=$type==='a3_motorcycle';
$brand=a3g_first_term(get_the_ID(),'a3_brand');
$market=a3g_first_term(get_the_ID(),'a3_market');
$shape=a3g_first_term(get_the_ID(),$is_moto?'a3_motorcycle_type':'a3_car_body');
$year=a3cp_field('_a3_year');
$price=function_exists('a3cp_vehicle_price')?a3cp_vehicle_price():'';
$source=a3cp_field('_a3_source_url');
$checked=a3cp_field('_a3_source_checked_at');
$related=a3g_related_post_ids();
?>
<?php get_header(); while(have_posts()):the_post(); ?>
<section class="g-vehicle-hero">
  <div class="g-wrap g-vehicle-hero-grid">
    <div class="g-vehicle-copy">
      <div class="g-breadcrumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a><span>›</span><a href="<?php echo esc_url(get_post_type_archive_link($type)); ?>"><?php echo $is_moto?'الموتوسيكلات':'السيارات'; ?></a></div>
      <div class="g-vehicle-tags"><?php if($brand): ?><span><?php echo esc_html($brand); ?></span><?php endif; ?><?php if($shape): ?><span><?php echo esc_html($shape); ?></span><?php endif; ?><?php if($market): ?><span><?php echo esc_html($market); ?></span><?php endif; ?></div>
      <h1><?php the_title(); ?></h1>
      <?php if(has_excerpt()): ?><p><?php echo esc_html(get_the_excerpt()); ?></p><?php endif; ?>
      <div class="g-vehicle-price-row"><?php if($price): ?><strong><?php echo esc_html($price); ?></strong><?php endif; ?><?php if($checked): ?><small>آخر مراجعة للبيانات: <?php echo esc_html($checked); ?></small><?php endif; ?></div>
    </div>
    <div class="g-vehicle-image"><?php if(has_post_thumbnail()){the_post_thumbnail('full',['loading'=>'eager','fetchpriority'=>'high']);}else{echo '<span class="g-fallback">A3TAL</span>';} ?></div>
  </div>
</section>

<nav class="g-vehicle-tabs"><div class="g-wrap"><a href="#overview">نظرة عامة</a><a href="#specs">المواصفات</a><a href="#details">التفاصيل</a><?php if($related): ?><a href="#related">مقالات مرتبطة</a><?php endif; ?></div></nav>

<main class="g-wrap g-vehicle-main">
  <section id="overview" class="g-vehicle-panel">
    <div class="g-section-head"><div><span>A3TAL DATA</span><h2>بيانات <?php echo $is_moto?'الموتوسيكل':'السيارة'; ?></h2></div></div>
    <div id="specs" class="g-spec-grid">
      <?php
      $specs=[
        'سنة الموديل'=>$year,
        'الماركة'=>$brand,
        ($is_moto?'النوع':'الهيكل')=>$shape,
        'سعة المحرك'=>a3cp_field('_a3_engine_cc')?a3cp_field('_a3_engine_cc').' CC':'',
        'القوة'=>a3cp_field('_a3_power_hp')?a3cp_field('_a3_power_hp').($is_moto?' PS':' HP'):'',
        'العزم'=>a3cp_field('_a3_torque_nm')?a3cp_field('_a3_torque_nm').' Nm':'',
        'ناقل الحركة'=>a3cp_field('_a3_transmission'),
        'الوقود'=>a3cp_field('_a3_fuel'),
        'نظام الجر'=>a3cp_field('_a3_drivetrain'),
      ];
      if($is_moto){
        $specs['بلد العلامة / المنشأ المرجعي']=a3cp_field('_a3_origin_country');
        $specs['التبريد']=a3cp_field('_a3_cooling');
        $specs['الفرامل الأمامية']=a3cp_field('_a3_front_brake');
        $specs['الفرامل الخلفية']=a3cp_field('_a3_rear_brake');
        $specs['نوع الإطارات']=a3cp_field('_a3_tyre_type');
        $specs['سعة الخزان']=a3cp_field('_a3_tank_l')?a3cp_field('_a3_tank_l').' لتر':'';
        $specs['الوزن']=a3cp_field('_a3_weight_kg')?a3cp_field('_a3_weight_kg').' كجم':'';
        $specs['الاستخدام الأنسب']=a3cp_field('_a3_use_case');
        $specs['الضمان']=a3cp_field('_a3_warranty');
      }else{
        $specs['المقاعد']=a3cp_field('_a3_seats');
      }
      foreach($specs as $label=>$value): if($value==='')continue; ?>
        <div><small><?php echo esc_html($label); ?></small><strong><?php echo esc_html($value); ?></strong></div>
      <?php endforeach; ?>
    </div>
    <?php if($source): ?><div class="g-source-note"><span>المصدر المرجعي للبيانات</span><a href="<?php echo esc_url($source); ?>" rel="nofollow noopener" target="_blank">فتح المصدر</a></div><?php endif; ?>
  </section>

  <section id="details" class="g-vehicle-panel g-entry"><?php the_content(); ?></section>

  <?php if($related): $rq=new WP_Query(['post_type'=>'post','post_status'=>'publish','post__in'=>$related,'orderby'=>'post__in','posts_per_page'=>12]); if($rq->have_posts()): ?>
  <section id="related" class="g-vehicle-panel">
    <div class="g-section-head"><div><span>من أعطال.كوم</span><h2>مقالات مرتبطة</h2></div></div>
    <div class="g-news-grid"><?php while($rq->have_posts()):$rq->the_post();a3g_card();endwhile;wp_reset_postdata(); ?></div>
  </section>
  <?php endif; endif; ?>
</main>
<?php endwhile; get_footer(); ?>
