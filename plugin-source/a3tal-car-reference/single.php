<?php
defined('ABSPATH')||exit;
get_header();$post=get_queried_object();$data=A3tal_Car_Reference_Engine::data($post->ID);
$children=get_posts(['post_type'=>A3tal_Car_Reference_Engine::TYPE,'post_status'=>'publish','post_parent'=>$post->ID,'numberposts'=>100,'orderby'=>'title','order'=>'ASC']);
?>
<main class="a3cr-wrap" dir="rtl">
<nav class="a3cr-crumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a> / <a href="<?php echo esc_url(get_post_type_archive_link(A3tal_Car_Reference_Engine::TYPE)); ?>">دليل المواصفات</a>
<?php foreach(array_reverse(get_post_ancestors($post)) as $id): ?> / <a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a><?php endforeach; ?></nav>
<article class="a3cr-article"><h1><?php echo esc_html(get_the_title($post)); ?></h1>
<?php if(has_excerpt($post)): ?><p><?php echo esc_html(get_the_excerpt($post)); ?></p><?php endif; ?>
<?php if(has_post_thumbnail($post)): ?><figure><?php echo get_the_post_thumbnail($post,'large',['loading'=>'eager']); ?></figure><?php endif; ?>
<?php if(!empty($data['years'])||!empty($data['market'])||!empty($data['engine'])): ?><div class="a3cr-grid">
<?php foreach(['market'=>'السوق','years'=>'السنوات','engine'=>'المحرك'] as $key=>$label): if(empty($data[$key]))continue; ?><div class="a3cr-tile"><small><?php echo esc_html($label); ?></small><strong><?php echo esc_html($data[$key]); ?></strong></div><?php endforeach; ?></div><?php endif; ?>
<?php // Inline verified-facts tables are authored in some reference records; do not render the same fact rows twice. ?>
<?php if(!empty($data['facts']) && strpos((string)$post->post_content,'a3tal-responsive-table')===false): ?><section><h2>جدول المواصفات</h2><div class="a3cr-table"><table><tbody>
<?php foreach($data['facts'] as $fact): ?><tr><th scope="row"><?php echo esc_html($fact['label']); ?></th><td><?php echo esc_html($fact['value']); ?></td></tr><?php endforeach; ?>
</tbody></table></div></section><?php endif; ?>
<div class="a3cr-content"><?php echo apply_filters('the_content',$post->post_content); ?></div>
<?php if($children): ?><section><h2>الصفحات المرتبطة</h2><div class="a3cr-grid"><?php foreach($children as $item)A3tal_Car_Reference_Engine::card($item); ?></div></section><?php endif; ?>
<?php if(!empty($data['sources'])): ?><section class="a3cr-sources"><h2>المصادر</h2><ul><?php foreach($data['sources'] as $s): ?><li><a href="<?php echo esc_url($s['url']); ?>" rel="noopener nofollow noreferrer" target="_blank"><?php echo esc_html($s['title']); ?></a></li><?php endforeach; ?></ul>
<?php if(!empty($data['reviewed_at'])): ?><p>آخر مراجعة: <?php echo esc_html($data['reviewed_at']); ?></p><?php endif; ?></section><?php endif; ?>
<p class="a3cr-note">تختلف المواصفات حسب المحرك والسوق وسنة الإنتاج. راجع دليل المالك وملصق السيارة قبل شراء القطع أو تغيير السوائل.</p>
</article></main>
<?php get_footer(); ?>