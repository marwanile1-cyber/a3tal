<?php get_header(); while(have_posts()): the_post(); ?>
<section class="g-article-hero g-page-hero"><div class="g-wrap g-article-head">
  <div class="g-breadcrumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a><span>›</span><?php the_title(); ?></div>
  <h1><?php the_title(); ?></h1>
</div></section>
<div class="g-wrap g-page-shell"><main class="g-article-card"><?php if(has_post_thumbnail()): ?><figure class="g-featured"><?php the_post_thumbnail('full'); ?></figure><?php endif; ?><div class="g-entry"><?php the_content(); ?></div></main></div>
<?php endwhile; get_footer(); ?>