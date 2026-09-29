<?php get_header(); while(have_posts()):the_post(); ?>
<section class="ap-article-head"><div class="ap-wrap ap-article-head-inner"><div class="ap-breadcrumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a> / <?php the_title(); ?></div><h1><?php the_title(); ?></h1></div></section>
<div class="ap-wrap ap-page-shell"><main class="ap-article"><?php if(has_post_thumbnail()): ?><figure class="ap-featured"><?php the_post_thumbnail('full'); ?></figure><?php endif; ?><div class="ap-entry"><?php the_content(); ?></div></main></div>
<?php endwhile; get_footer(); ?>
