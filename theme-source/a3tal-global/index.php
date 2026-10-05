<?php get_header(); ?>
<?php if(is_singular('post')): while(have_posts()): the_post();
$cat=a3g_primary_cat(); $diag=a3g_is_diagnostic(); $vehicle_entity=a3g_related_vehicle_entity(get_the_ID()); ?>
<section class="g-article-hero">
  <div class="g-wrap g-article-head">
    <div class="g-breadcrumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a><?php if($cat): ?> <span>›</span> <a href="<?php echo esc_url(get_category_link($cat)); ?>"><?php echo esc_html($cat->name); ?></a><?php endif; ?></div>
    <?php if($cat): ?><span class="g-article-tag"><?php echo esc_html($cat->name); ?></span><?php endif; ?>
    <h1><?php the_title(); ?></h1>
    <p><?php echo esc_html(a3g_excerpt(get_the_ID(),28)); ?></p>
    <div class="g-article-meta"><span>آخر تحديث: <?php echo esc_html(get_the_modified_date('j F Y')); ?></span><span><?php echo esc_html(a3g_read_time()); ?> دقائق قراءة</span><span class="g-article-views"><?php echo a3g_icon('eye'); ?><b data-a3-views><?php echo esc_html(a3g_views_label()); ?></b></span><span>فريق أعطال.كوم</span></div>
  </div>
</section>
<div class="g-wrap g-article-layout">
  <main class="g-article-card">
    <?php if(has_post_thumbnail()): ?><figure class="g-featured"><?php the_post_thumbnail('full',['loading'=>'eager','fetchpriority'=>'high']); ?></figure><?php endif; ?>
    <?php if($diag): ?><div class="g-diagnostic-note"><strong>قاعدة أعطال:</strong><span>ابدأ بالأعراض والفحص والقياسات قبل تغيير أي قطعة.</span></div><?php endif; ?>
    <?php if($vehicle_entity):
      $ve_id=(int)$vehicle_entity->ID;
      $ve_price=function_exists('a3cp_vehicle_price')?a3cp_vehicle_price($ve_id):'';
    ?>
      <aside class="g-related-model-box">
        <div><small>ملف الموديل على أعطال</small><strong><?php echo esc_html(get_the_title($ve_id)); ?></strong><?php if($ve_price): ?><span><?php echo esc_html($ve_price); ?></span><?php endif; ?></div>
        <a href="<?php echo esc_url(get_permalink($ve_id)); ?>">المواصفات والبيانات المنظمة ←</a>
      </aside>
    <?php endif; ?>
    <div class="g-entry"><?php the_content(); ?></div>
  </main>
  <aside class="g-article-side">
    <div class="g-side-box"><h3>في هذا المقال</h3><ul><?php foreach(a3g_toc() as $it): ?><li><a href="#<?php echo esc_attr($it['id']); ?>"><?php echo esc_html($it['t']); ?></a></li><?php endforeach; ?></ul></div>
    <div class="g-side-box g-side-dark"><span>A3TAL</span><h3>ابحث داخل أعطال.كوم</h3><p>سعر سيارة، كود عطل، صيانة أو مركز خدمة.</p><form method="get" action="<?php echo esc_url(home_url('/')); ?>"><input name="s" placeholder="اكتب ما تبحث عنه"><button><?php echo a3g_icon('search'); ?></button></form></div>
  </aside>
</div>
<?php endwhile; else: ?>
<section class="g-archive-head"><div class="g-wrap">
  <span><?php echo is_search()?'بحث أعطال.كوم':'محتوى أعطال.كوم'; ?></span>
  <h1><?php if(is_search()){echo 'نتائج البحث عن: '.esc_html(get_search_query());}elseif(is_archive()){the_archive_title();}else{echo 'أحدث المحتوى';} ?></h1>
  <?php if(is_archive() && get_the_archive_description()): ?><p><?php echo wp_kses_post(get_the_archive_description()); ?></p><?php endif; ?>
</div></section>
<div class="g-wrap g-archive-grid"><?php if(have_posts()): while(have_posts()): the_post(); a3g_card(); endwhile; else: ?><div class="g-empty">لا توجد نتائج مطابقة حاليًا.</div><?php endif; ?></div>
<?php endif; get_footer(); ?>
