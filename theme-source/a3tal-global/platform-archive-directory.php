<?php
$type=get_query_var('post_type');$is_showroom=$type==='a3_showroom';$title=$is_showroom?'معارض السيارات':'مراكز الخدمة';$brands=get_terms(['taxonomy'=>'a3_brand','hide_empty'=>false]);$markets=get_terms(['taxonomy'=>'a3_market','hide_empty'=>false]);$statuses=get_terms(['taxonomy'=>'a3_directory_status','hide_empty'=>false]);
get_header(); ?>
<section class="g-platform-archive-hero g-directory-hero"><div class="g-wrap">
<span><?php echo $is_showroom?'A3TAL SHOWROOMS':'A3TAL SERVICE DIRECTORY'; ?></span>
<h1><?php echo esc_html($title); ?></h1>
<p><?php echo $is_showroom?'ابحث عن المعارض حسب السوق والماركة وحالة التحقق، مع فصل واضح بين المعتمد رسميًا والموثّق والمستقل.':'دليل مراكز الخدمة حسب الماركة والسوق وحالة الاعتماد والخدمات المتاحة.'; ?></p>
<form class="g-platform-filter" method="get">
<label><small>الماركة</small><select name="brand"><option value="">كل الماركات</option><?php foreach($brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('brand'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
<label><small>السوق</small><select name="market"><option value="">كل الأسواق</option><?php foreach($markets as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('market'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
<label><small>الحالة</small><select name="directory_status"><option value="">كل الحالات</option><?php foreach($statuses as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('directory_status'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
<button type="submit"><?php echo a3g_icon('search'); ?><span>بحث</span></button>
</form></div></section>

<main class="g-wrap g-platform-archive">
<div class="g-platform-archive-head"><div><span>A3TAL DIRECTORY</span><h2><?php echo $is_showroom?'اكتشف المعارض':'اختر مركز الخدمة'; ?></h2></div><b><?php global $wp_query; echo esc_html(number_format_i18n((int)$wp_query->found_posts)); ?> نتيجة</b></div>
<?php if(have_posts()): ?><div class="g-directory-grid">
<?php while(have_posts()):the_post();$status=a3g_directory_status();$phone=a3cp_field('_a3_phone');$address=a3cp_field('_a3_address');$checked=a3cp_field('_a3_source_checked_at');$map_query=$is_showroom?(a3cp_field('_a3_maps_query')?:$address):$address;$map_url=$map_query?'https://www.google.com/maps/search/?api=1&query='.rawurlencode($map_query):''; ?>
<article class="g-directory-card">
<a class="g-directory-media" href="<?php the_permalink(); ?>"><?php if(has_post_thumbnail()){the_post_thumbnail('large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL</span>';} ?></a>
<div class="g-directory-body"><?php if($status): ?><span class="g-directory-badge g-status-<?php echo esc_attr($status->slug); ?>"><?php echo esc_html($status->name); ?></span><?php endif; ?><h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3><?php if($address): ?><p><?php echo esc_html($address); ?></p><?php endif; ?><div class="g-directory-mini-meta"><?php if($phone): ?><span>☎ <?php echo esc_html($phone); ?></span><?php endif; ?><?php if($checked): ?><small>تحقق: <?php echo esc_html($checked); ?></small><?php endif; ?></div><?php if($is_showroom): ?><div class="g-directory-card-actions"><?php if($phone): ?><a href="tel:<?php echo esc_attr(preg_replace('/[^0-9+]/','',$phone)); ?>">اتصال</a><?php endif; ?><?php if($map_url): ?><a href="<?php echo esc_url($map_url); ?>" rel="nofollow noopener" target="_blank">الخريطة</a><?php endif; ?><a href="<?php the_permalink(); ?>">كل التفاصيل</a></div><?php else: ?><a class="g-platform-more" href="<?php the_permalink(); ?>">عرض التفاصيل ←</a><?php endif; ?></div>
</article>
<?php endwhile; ?></div><div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
<?php else: ?><div class="g-platform-empty"><?php echo a3g_icon($is_showroom?'store':'wrench'); ?><h2>لا توجد نتائج منظمة بهذه الفلاتر حاليًا</h2><p><?php echo $is_showroom?'جرّب تغيير الفلاتر أو تصفح أدلة المعارض المنشورة بالأسفل.':'تصفح أدلة مراكز الخدمة المنشورة بالأسفل للوصول إلى الفروع والمعلومات المتاحة الآن.'; ?></p></div><?php endif; ?>
<?php if(!$is_showroom): ?>
  <?php a3g_legacy_section(
    [33],
    'أدلة مراكز الخدمة المتاحة',
    'أدلة وفروع مراكز الخدمة المنشورة على أعطال، مع العناوين ووسائل التواصل والمعلومات المتاحة لكل مركز.',
    16,
    [],
    33
  ); ?>
<?php else: ?>
  <?php
    $guide_cat=get_category_by_slug('car-showrooms-guide');
    if($guide_cat):
      $guide_q=a3g_query(['cat'=>(int)$guide_cat->term_id,'posts_per_page'=>8]);
      if($guide_q->have_posts()):
  ?>
    <section class="g-showroom-guides">
      <div class="g-section-head">
        <div><span>BUYER INTELLIGENCE</span><h2>دليل الشراء من معارض السيارات</h2><p>مش مجرد عناوين فروع. هنا هتعرف تختار المعرض، تفهم العرض، تحجز Test Drive، وتقفل الحجز والاستلام من غير مفاجآت.</p></div>
        <a href="<?php echo esc_url(get_category_link($guide_cat)); ?>">كل أدلة المعارض</a>
      </div>
      <div class="g-showroom-guide-grid">
        <?php while($guide_q->have_posts()):$guide_q->the_post();a3g_card(get_the_ID(),'g-showroom-guide-card');endwhile;wp_reset_postdata(); ?>
      </div>
    </section>
  <?php endif; endif; ?>

  <?php a3g_legacy_section(
    [374,22],
    'قبل زيارة المعرض: الأسعار والمراجعات الحالية',
    'قارن السعر والمواصفات والمراجعة قبل ما تروح المعرض، وكل صفحة تفضل على رابطها الأصلي.',
    12,
    [],
    374
  ); ?>
<?php endif; ?>
</main><?php get_footer(); ?>