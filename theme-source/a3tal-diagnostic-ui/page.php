<?php get_header(); while(have_posts()):the_post(); ?>
<section class="a3-page-hero"><div class="a3-container"><div class="a3-breadcrumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a> / <?php the_title(); ?></div></div></section>
<div class="a3-container a3-article-layout" style="grid-template-columns:minmax(0,900px)">
  <article class="a3-article"><h1><?php the_title(); ?></h1><?php if(has_post_thumbnail()): ?><div class="a3-featured"><?php the_post_thumbnail('full'); ?></div><?php endif; ?><div class="a3-entry"><?php the_content(); ?></div></article>
</div>
<?php endwhile; get_footer(); ?>
