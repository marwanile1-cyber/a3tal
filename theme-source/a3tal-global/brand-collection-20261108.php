<?php
/**
 * A3tal Egypt car-brand overview inside the existing /cars/?brand=slug archive.
 * Includes published editorial posts and the existing PSEO brand tree, in addition
 * to the car-price records rendered by car-price-guide.php. No synthetic content.
 * The query-filter archive remains noindex/follow to avoid duplicate SEO intent.
 */
defined('ABSPATH') || exit;
if (empty($cg_brand_selected) || empty($cg_brand_slug)) return;
// Use WordPress native title search; avoid intrusive SQL filters on live archives.
$brand_page = 1;
if (isset($_GET['brand_articles_page']) && is_scalar($_GET['brand_articles_page'])) {
    $brand_page = min(500,max(1,absint(wp_unslash($_GET['brand_articles_page']))));
}
$brand_editorial = new WP_Query([
    'post_type'=>'post','post_status'=>'publish',
    's'=>$cg_brand_selected['search'],
    'search_columns'=>['post_title'],
    'posts_per_page'=>12,'paged'=>$brand_page,'orderby'=>'date','order'=>'DESC',
    'ignore_sticky_posts'=>true
]);
$brand_ref_root = null;
if (post_type_exists('a3_car_ref')) {
    $found=get_page_by_path($cg_brand_slug,OBJECT,'a3_car_ref');
    if ($found instanceof WP_Post && $found->post_status==='publish') $brand_ref_root=$found;
}
$brand_models=[];
if ($brand_ref_root) {
    $brand_models=get_posts([
        'post_type'=>'a3_car_ref','post_status'=>'publish',
        'post_parent'=>$brand_ref_root->ID,'posts_per_page'=>10,
        'orderby'=>'modified','order'=>'DESC'
    ]);
}
?>
<section class="cg-brand-collection cg-surface" aria-labelledby="cg-brand-content-title" id="all-brand-content">
 <div class="cg-section-heading">
   <div><span class="cg-kicker">كل ما نُشر عن الماركة</span>
   <h2 id="cg-brand-content-title"><?php echo esc_html('دليل '. $cg_brand_selected['name'].' في أعطال.كوم'); ?></h2>
   <p>الأسعار والموديلات بالأعلى، ثم المواصفات والأعطال والصيانة والمقارنات المنشورة بالفعل.</p></div>
 </div>
 <?php if ($brand_ref_root): ?>
 <div class="cg-brand-reference">
  <div><span>دليل PSEO الفني</span><h3><?php echo esc_html('مواصفات وموديلات '.$cg_brand_selected['name']); ?></h3>
  <p>تصفح الدليل الفني ومواصفات كل موديل من قاعدة بيانات أعطال.</p></div>
  <a href="<?php echo esc_url(get_permalink($brand_ref_root)); ?>">جميع المواصفات الفنية ←</a>
 </div>
 <?php if($brand_models): ?>
 <div class="cg-brand-model-links">
   <?php foreach($brand_models as $model): ?>
   <a href="<?php echo esc_url(get_permalink($model)); ?>"><?php echo esc_html(get_the_title($model)); ?> <span aria-hidden="true">←</span></a>
   <?php endforeach; ?>
 </div>
 <?php endif; ?>
 <?php endif; ?>
 <div class="cg-brand-editorial-heading">
  <h3><?php echo esc_html('أحدث المقالات والأعطال والصيانة عن '.$cg_brand_selected['name']); ?></h3>
  <span><?php echo esc_html(number_format_i18n((int)$brand_editorial->found_posts)); ?> مقال منشور مطابق للماركة</span>
 </div>
 <?php if ($brand_editorial->have_posts()): ?>
 <div class="cg-brand-editorial-list">
  <?php while($brand_editorial->have_posts()):$brand_editorial->the_post(); ?>
  <article><a href="<?php the_permalink(); ?>">
  <?php if(has_post_thumbnail()):the_post_thumbnail('thumbnail',['loading'=>'lazy','decoding'=>'async']);endif; ?>
  <span><strong><?php echo esc_html(get_the_title()); ?></strong><small><?php echo esc_html(get_the_date('j F Y')); ?></small></span>
  </a></article>
  <?php endwhile; wp_reset_postdata(); ?>
 </div>
 <?php if($brand_editorial->max_num_pages>1): ?>
 <nav class="cg-brand-pagination" aria-label="صفحات مقالات الماركة">
  <?php if($brand_page>1): ?><a href="<?php echo esc_url(add_query_arg(['brand'=>$cg_brand_slug,'brand_articles_page'=>$brand_page-1],$cg_url)); ?>">← الأحدث</a><?php endif; ?>
  <span><?php echo esc_html('صفحة '.$brand_page.' من '.(int)$brand_editorial->max_num_pages); ?></span>
  <?php if($brand_page<$brand_editorial->max_num_pages): ?><a href="<?php echo esc_url(add_query_arg(['brand'=>$cg_brand_slug,'brand_articles_page'=>$brand_page+1],$cg_url)); ?>">المزيد من المقالات ←</a><?php endif; ?>
 </nav>
 <?php endif; ?>
 <?php else: ?>
 <p class="cg-empty">لا توجد مقالات إضافية مطابقة لهذه الماركة في العناوين المنشورة حاليًا. يمكنك متابعة موديلاتها ودليل المواصفات بالأعلى.</p>
 <?php endif; ?>
 <p class="cg-brand-note">يعرض هذا القسم المقالات التي تذكر الماركة أو موديلاتها المحددة في العنوان، ولا يخلطها بمقالات العلامات الأخرى. صفحات الأسعار الفنية مرتبطة بأقسامها الأصلية، مع الحفاظ على روابطها الحالية.</p>
</section>
