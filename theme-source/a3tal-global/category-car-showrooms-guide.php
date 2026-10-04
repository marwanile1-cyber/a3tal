<?php
get_header();

$paged=max(1,(int)get_query_var('paged'));
?>
<section class="g-showroom-editorial-hero">
  <div class="g-wrap">
    <span>SHOWROOM BUYER INTELLIGENCE</span>
    <h1>دليل معارض السيارات</h1>
    <p>أدلة عملية قبل الحجز والتمويل وتجربة القيادة والاستلام، مرتبطة بدليل المعارض الموثق في أعطال.كوم.</p>
    <div class="g-showroom-editorial-actions">
      <a href="<?php echo esc_url(home_url('/car-showrooms/')); ?>">استكشف المعارض الموثقة</a>
      <a href="<?php echo esc_url(home_url('/cars/')); ?>">أسعار ومراجعات السيارات</a>
    </div>
  </div>
</section>

<main class="g-wrap g-showroom-editorial-main">
  <?php if(have_posts()): ?>
    <div class="g-showroom-editorial-grid">
      <?php $card_index=0; while(have_posts()):the_post(); $card_index++;
        $id=get_the_ID();
        $image=get_the_post_thumbnail_url($id,'large');
        if(!$image){
          $image=get_template_directory_uri().'/assets/images/hero-fallback.webp';
        }
        $image_bust=add_query_arg('a3v','20261004-3',$image);
      ?>
      <article class="g-showroom-editorial-card">
        <a
          class="g-showroom-editorial-media"
          href="<?php the_permalink(); ?>"
          style="background-image:linear-gradient(180deg,rgba(4,12,20,.03),rgba(4,12,20,.22)),url('<?php echo esc_url($image_bust); ?>')"
          aria-label="<?php echo esc_attr(get_the_title()); ?>"
        >
          <img
            src="<?php echo esc_url($image_bust); ?>"
            alt="<?php echo esc_attr(get_post_meta(get_post_thumbnail_id($id),'_wp_attachment_image_alt',true) ?: get_the_title()); ?>"
            width="1000"
            height="667"
            loading="eager"
            decoding="async"
          >
          <span class="g-showroom-editorial-number"><?php echo esc_html(str_pad((string)$card_index,2,'0',STR_PAD_LEFT)); ?></span>
        </a>
        <div class="g-showroom-editorial-body">
          <div class="g-showroom-editorial-kicker">دليل معارض السيارات</div>
          <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
          <p><?php echo esc_html(a3g_excerpt($id,22)); ?></p>
          <div class="g-showroom-editorial-meta">
            <span><?php echo esc_html(a3g_read_time($id)); ?> دقائق قراءة</span>
            <span>آخر تحديث <?php echo esc_html(get_the_modified_date('j F Y',$id)); ?></span>
          </div>
          <a class="g-showroom-editorial-read" href="<?php the_permalink(); ?>">اقرأ الدليل كاملًا ←</a>
        </div>
      </article>
      <?php endwhile; ?>
    </div>

    <div class="g-platform-pagination">
      <?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?>
    </div>
  <?php else: ?>
    <div class="g-platform-empty"><span>🚘</span><h2>لا توجد أدلة منشورة حاليًا</h2></div>
  <?php endif; ?>

  <section class="g-showroom-editorial-directory">
    <div>
      <span>LIVE DIRECTORY</span>
      <h2>مش محتوى وبس: عندنا دليل معارض حي</h2>
      <p>ادخل على الفروع الموثقة وشوف الهاتف والعنوان والخريطة وحالة الاعتماد ومصدر التحقق، بدل البحث بين عشر صفحات متفرقة.</p>
    </div>
    <a href="<?php echo esc_url(home_url('/car-showrooms/')); ?>">فتح دليل المعارض</a>
  </section>
</main>
<?php get_footer(); ?>
