<?php get_header(); ?>
<?php if(is_singular('post')): while(have_posts()):the_post(); ?>
<section class="a3-page-hero">
  <div class="a3-container">
    <div class="a3-breadcrumb"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a> / <?php echo esc_html(get_the_title()); ?></div>
  </div>
</section>
<div class="a3-container a3-article-layout">
  <article class="a3-article">
    <span class="a3-eyebrow" style="color:#0284C7;background:#E0F2FE">تشخيص وصيانة</span>
    <h1><?php the_title(); ?></h1>
    <div class="a3-article-meta">
      <span>تمت المراجعة: <?php echo esc_html(get_the_modified_date('j F Y')); ?></span>
      <span><?php echo esc_html(a3du_read_time()); ?> دقائق قراءة</span>
      <span>فريق أعطال.كوم</span>
    </div>
    <section class="a3-summary">
      <h2>الخلاصة السريعة</h2>
      <div class="a3-summary-grid">
        <div class="a3-summary-item"><small>درجة الخطورة</small><strong><?php echo esc_html(a3du_article_meta('a3tal_severity','راجع تفاصيل الحالة')); ?></strong></div>
        <div class="a3-summary-item"><small>هل يمكن القيادة؟</small><strong><?php echo esc_html(a3du_article_meta('a3tal_drive','يعتمد على الأعراض')); ?></strong></div>
        <div class="a3-summary-item"><small>أول فحص</small><strong><?php echo esc_html(a3du_article_meta('a3tal_first_check','ابدأ بالفحص والتشخيص')); ?></strong></div>
        <div class="a3-summary-item"><small>قبل تغيير القطع</small><strong><?php echo esc_html(a3du_article_meta('a3tal_before_replace','اختبر السبب المحتمل')); ?></strong></div>
      </div>
    </section>
    <?php if(has_post_thumbnail()): ?><div class="a3-featured"><?php the_post_thumbnail('full',['loading'=>'eager','fetchpriority'=>'high']); ?></div><?php endif; ?>
    <div class="a3-entry"><?php the_content(); ?></div>
  </article>
  <aside class="a3-sidebar">
    <div class="a3-side-card a3-toc"><h3>في هذا المقال</h3><ul>
      <?php foreach(a3du_toc() as $item): ?><li><a href="#<?php echo esc_attr($item['id']); ?>"><?php echo esc_html($item['title']); ?></a></li><?php endforeach; ?>
    </ul></div>
    <div class="a3-side-card"><h3>قاعدة أعطال.كوم</h3><p style="font-size:13px;color:#64748B;margin:0">لا تعتبر كود العطل دليلًا مباشرًا على تلف قطعة. اختبر النظام أولًا.</p></div>
  </aside>
</div>
<?php endwhile; else: ?>
<section class="a3-archive-head"><div class="a3-container">
  <?php if(is_search()): ?><h1>نتائج البحث: <?php echo esc_html(get_search_query()); ?></h1>
  <?php elseif(is_archive()): ?><h1><?php the_archive_title(); ?></h1>
  <?php else: ?><h1>أحدث محتوى أعطال.كوم</h1><?php endif; ?>
</div></section>
<div class="a3-container a3-archive-grid">
  <?php if(have_posts()): while(have_posts()):the_post(); a3du_post_card(); endwhile; else: ?><p>لا توجد نتائج مطابقة.</p><?php endif; ?>
</div>
<?php endif; ?>
<?php get_footer(); ?>
