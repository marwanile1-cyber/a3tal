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
<?php while(have_posts()):the_post();$status=a3g_directory_status();$phone=a3cp_field('_a3_phone');$address=a3cp_field('_a3_address');$checked=a3cp_field('_a3_source_checked_at'); ?>
<article class="g-directory-card">
<a class="g-directory-media" href="<?php the_permalink(); ?>"><?php if(has_post_thumbnail()){the_post_thumbnail('large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL</span>';} ?></a>
<div class="g-directory-body"><?php if($status): ?><span class="g-directory-badge g-status-<?php echo esc_attr($status->slug); ?>"><?php echo esc_html($status->name); ?></span><?php endif; ?><h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3><?php if($address): ?><p><?php echo esc_html($address); ?></p><?php endif; ?><div><?php if($phone): ?><span>☎ <?php echo esc_html($phone); ?></span><?php endif; ?><?php if($checked): ?><small>تحقق: <?php echo esc_html($checked); ?></small><?php endif; ?></div><a class="g-platform-more" href="<?php the_permalink(); ?>">عرض التفاصيل ←</a></div>
</article>
<?php endwhile; ?></div><div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
<?php else: ?><div class="g-platform-empty"><span><?php echo $is_showroom?'🏢':'🔧'; ?></span><h2>لا توجد بيانات منشورة بهذه الفلاتر حاليًا</h2><p>لا تظهر الأنشطة في الدليل إلا بعد إضافة بياناتها وحالة التحقق بوضوح.</p></div><?php endif; ?>
</main><?php get_footer(); ?>