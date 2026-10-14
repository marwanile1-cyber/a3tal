<?php
if (!defined('ABSPATH')) exit;
get_header('dtc');
while (have_posts()): the_post();
  $dtc_original_post = $GLOBALS['post'];
  $dtc_id = get_the_ID();
  $dtc_code = a3g_dtc_current_code($dtc_id);
  $dtc_content_id = a3g_dtc_content_id($dtc_id);
  $dtc_content_post = get_post($dtc_content_id);
  if (!$dtc_content_post || $dtc_content_post->post_status !== 'publish') {
    $dtc_content_id = $dtc_id;
    $dtc_content_post = $dtc_original_post;
  }
  $dtc_library_url = get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/');
  $dtc_title = get_the_title($dtc_id);
  $dtc_system = (string) get_post_meta($dtc_id, '_a3_dtc_system', true);
  $dtc_scope = (string) get_post_meta($dtc_id, '_a3_code_scope', true);
  $dtc_manufacturer = (string) get_post_meta($dtc_id, '_a3_manufacturer', true);
  $dtc_advice = (string) get_post_meta($dtc_id, '_a3_drive_advice', true);
  $dtc_source = (string) get_post_meta($dtc_id, '_a3_source_url', true);
  $dtc_checked = (string) get_post_meta($dtc_id, '_a3_source_checked_at', true);
  $dtc_scope_labels = ['generic' => 'عام OBD-II', 'manufacturer' => 'خاص بالشركة المصنعة'];
  $dtc_excerpt = trim(wp_strip_all_tags((string) get_post_field('post_excerpt', $dtc_id)));
  $GLOBALS['post'] = $dtc_content_post;
  setup_postdata($dtc_content_post);
  $dtc_body = apply_filters('the_content', $dtc_content_post->post_content);
  $GLOBALS['post'] = $dtc_original_post;
  setup_postdata($dtc_original_post);
  $dtc_toc = [];
  $dtc_heading_index = 0;
  $dtc_body = preg_replace_callback('/<h([23])\b([^>]*)>(.*?)<\/h\1>/is', static function ($match) use (&$dtc_toc, &$dtc_heading_index, $dtc_content_id) {
    $dtc_heading_index++;
    $attributes = $match[2];
    $heading_text = trim(html_entity_decode(wp_strip_all_tags($match[3]), ENT_QUOTES, 'UTF-8'));
    if ($heading_text === '') return $match[0];
    if (preg_match('/\bid\s*=\s*(["\'])(.*?)\1/is', $attributes, $id_match)) {
      $heading_id = html_entity_decode($id_match[2], ENT_QUOTES, 'UTF-8');
    } else {
      $heading_id = 'dtc-guide-' . $dtc_content_id . '-' . $dtc_heading_index;
      $attributes .= ' id="' . esc_attr($heading_id) . '"';
    }
    $dtc_toc[] = ['id' => $heading_id, 'title' => $heading_text, 'level' => (int) $match[1]];
    return '<h' . $match[1] . $attributes . '>' . $match[3] . '</h' . $match[1] . '>';
  }, $dtc_body);
  $dtc_sidebar_toc = array_values(array_filter($dtc_toc, static function ($heading) { return $heading['level'] === 2; }));
  if (!$dtc_sidebar_toc) $dtc_sidebar_toc = $dtc_toc;
  $dtc_related_entries = array_values(array_filter(a3g_dtc_catalog(), static function ($entry) use ($dtc_code, $dtc_id, $dtc_content_id) {
    return (int) $entry['id'] !== $dtc_id && (int) $entry['id'] !== $dtc_content_id && $entry['code'] !== $dtc_code && substr($entry['code'], 0, 1) === substr($dtc_code, 0, 1);
  }));
  $dtc_related_entries = array_slice($dtc_related_entries, 0, 3);
  $dtc_share_url = get_permalink($dtc_id);
  $dtc_share_title = $dtc_code ? 'دليل تشخيص كود ' . $dtc_code . ' بالعربي | أعطال.كوم' : get_the_title($dtc_id);
  $dtc_video_links = preg_split('/[\\r\\n,]+/', (string) get_post_meta($dtc_content_id, '_a3_dtc_video_urls', true), -1, PREG_SPLIT_NO_EMPTY);
  $dtc_video_links = array_values(array_filter(array_map('trim', (array)$dtc_video_links), static function ($url) {
    $parts = wp_parse_url($url);
    return is_array($parts) && ($parts['scheme'] ?? '') === 'https' &&
      in_array(strtolower($parts['host'] ?? ''), ['youtube.com','www.youtube.com','m.youtube.com','youtu.be'], true);
  }));
  $dtc_promos = a3g_dtc_promo_ids([$dtc_id, $dtc_content_id], 3);
?>
<main id="dtc-main" class="d-wrap d-main d-single-main">
  <nav class="d-breadcrumb" aria-label="مسار الصفحة"><a href="<?php echo esc_url($dtc_library_url); ?>">دليل أعطال</a><span aria-hidden="true">/</span><a href="<?php echo esc_url($dtc_library_url . '#dtc-codes'); ?>">مكتبة الأكواد</a><span aria-hidden="true">/</span><span dir="ltr" aria-current="page"><?php echo esc_html($dtc_code ?: $dtc_title); ?></span></nav>
  <header class="d-detail-hero">
    <div class="d-detail-copy"><p class="d-eyebrow">افهم الكود. رتّب الفحص.</p><h1><?php echo esc_html($dtc_title); ?></h1><?php if ($dtc_excerpt): ?><p class="d-detail-excerpt"><?php echo esc_html($dtc_excerpt); ?></p><?php endif; ?><div class="d-detail-meta"><?php if ($dtc_system): ?><span><?php echo esc_html($dtc_system); ?></span><?php endif; ?><?php if (isset($dtc_scope_labels[$dtc_scope])): ?><span><?php echo esc_html($dtc_scope_labels[$dtc_scope]); ?></span><?php endif; ?><?php if ($dtc_manufacturer): ?><span><?php echo esc_html($dtc_manufacturer); ?></span><?php endif; ?><a href="#dtc-discussion">الأسئلة والتجارب <span aria-hidden="true">↓</span></a></div></div>
    <?php if ($dtc_code): ?><b class="d-detail-code" dir="ltr"><?php echo esc_html($dtc_code); ?></b><?php endif; ?>
  </header>
  <?php if (has_post_thumbnail($dtc_id) && (bool)preg_match('/^A3TAL-DTC-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-(?:5|10)$/', (string)get_post_meta($dtc_id, '_a3_dtc_batch', true))): ?>
  <figure class="d-dtc-featured" aria-label="رسم توضيحي لمكونات النظام">
    <?php echo get_the_post_thumbnail($dtc_id, 'large', ['loading'=>'eager','decoding'=>'async','fetchpriority'=>'high']); ?>
    <figcaption>صورة تشخيصية توضيحية من تصميم أعطال.كوم، وليست مخطط توصيلات خاصًا بموديل معين.</figcaption>
  </figure>
  <?php endif; ?>
  <section class="d-share" aria-label="مشاركة دليل الكود">
    <div class="d-share-intro"><strong>الشرح نفعك؟ شاركه مع صاحب عربية عنده نفس الكود</strong><small>مشاركة مباشرة من غير تسجيل دخول</small></div>
    <div class="d-share-actions">
      <a class="d-share-btn d-share-wa" target="_blank" rel="noopener noreferrer nofollow" href="<?php echo esc_url('https://api.whatsapp.com/send?text='.rawurlencode($dtc_share_title.' '.$dtc_share_url)); ?>">واتساب</a>
      <a class="d-share-btn d-share-fb" target="_blank" rel="noopener noreferrer nofollow" href="<?php echo esc_url('https://www.facebook.com/sharer/sharer.php?u='.rawurlencode($dtc_share_url)); ?>">فيسبوك</a>
      <a class="d-share-btn d-share-x" target="_blank" rel="noopener noreferrer nofollow" href="<?php echo esc_url('https://twitter.com/intent/tweet?text='.rawurlencode($dtc_share_title).'&url='.rawurlencode($dtc_share_url)); ?>">X / تويتر</a>
      <button class="d-share-btn d-share-copy" type="button" data-dtc-copy="<?php echo esc_attr($dtc_share_url); ?>">نسخ الرابط</button>
    </div>
    <span class="d-share-feedback" aria-live="polite"></span>
  </section>
  <div class="d-detail-layout">
    <div class="d-detail-content">
      <?php if ($dtc_advice): ?><aside class="d-drive-note"><span class="d-note-icon" aria-hidden="true"><?php echo a3g_icon('warning'); ?></span><div><h2>هل يمكن الاستمرار في القيادة؟</h2><p><?php echo esc_html($dtc_advice); ?></p></div></aside><?php endif; ?>
      <article class="d-guide d-panel" aria-label="شرح الكود وخطوات التشخيص">
        <div class="d-guide-meta"><span>آخر تحديث للمقال: <?php echo esc_html(get_the_modified_date(get_option('date_format'), $dtc_content_id)); ?></span><?php if ($dtc_content_id !== $dtc_id): ?><a href="<?php echo esc_url(get_permalink($dtc_content_id)); ?>">المقال الأصلي على أعطال <span aria-hidden="true">↗</span></a><?php endif; ?></div>
        <div class="d-entry"><?php echo $dtc_body; ?></div>
        <?php if ($dtc_source || $dtc_checked): ?><footer class="d-source-note"><?php if ($dtc_checked): ?><span>آخر مراجعة للمصدر: <?php echo esc_html($dtc_checked); ?></span><?php endif; ?><?php if ($dtc_source): ?><a href="<?php echo esc_url($dtc_source); ?>" target="_blank" rel="nofollow noopener">المصدر الفني <span aria-hidden="true">↗</span></a><?php endif; ?></footer><?php endif; ?>
      </article>
      <?php if ($dtc_video_links): ?><section class="d-videos d-panel" aria-labelledby="dtc-videos-title">
        <span class="d-kicker">فيديوهات تشخيص مرتبطة</span><h2 id="dtc-videos-title">شاهد خطوات الفحص على يوتيوب</h2>
        <p>روابط خارجية مختارة للفهم والتوضيح. تحقق من تطابق السيارة والمحرك قبل تطبيق أي إجراء.</p>
        <ul><?php foreach (array_slice($dtc_video_links, 0, 5) as $dtc_video_url): ?><li><a href="<?php echo esc_url($dtc_video_url); ?>" rel="nofollow noopener noreferrer" target="_blank">شاهد الفيديو على YouTube <span aria-hidden="true">↗</span></a></li><?php endforeach; ?></ul>
      </section><?php endif; ?>
      <?php a3g_dtc_render_discussion($dtc_content_id); ?>
    </div>
    <aside class="d-sidebar" aria-label="تنقل وأكواد أخرى">
      <div class="d-sidebar-sticky">
        <?php if ($dtc_sidebar_toc): ?><nav class="d-sidebar-box d-toc" aria-label="محتويات شرح الكود"><h2>في هذا الدليل</h2><?php foreach (array_slice($dtc_sidebar_toc, 0, 24) as $dtc_heading): ?><a class="<?php echo $dtc_heading['level'] === 3 ? 'd-toc-sub' : ''; ?>" href="<?php echo esc_url('#' . rawurlencode($dtc_heading['id'])); ?>"><?php echo esc_html($dtc_heading['title']); ?></a><?php endforeach; ?><a class="d-toc-discussion" href="#dtc-discussion">الأسئلة وتجارب الإصلاح <span aria-hidden="true">↓</span></a></nav><?php endif; ?>
        <div class="d-sidebar-box d-sidebar-question"><span class="d-kicker">عندك نفس الكود؟</span><h2>احكي تفاصيل عربيتك</h2><p>اكتب الأعراض وما تم فحصه، وشارك السؤال أو نتيجة الإصلاح باسم مستعار.</p><a class="d-button" href="#dtc-discussion">اسأل وشارك تجربتك</a></div>
        <form class="d-sidebar-box d-small-search" action="<?php echo esc_url($dtc_library_url); ?>#dtc-codes" method="get" role="search" aria-label="ابحث عن كود آخر" data-dtc-search><label for="dtc-other-code">ابحث عن كود آخر</label><div><input id="dtc-other-code" name="code" type="text" placeholder="P0420" maxlength="12" dir="ltr" autocomplete="off" autocapitalize="characters" spellcheck="false"><button type="submit" aria-label="البحث عن الكود"><?php echo a3g_icon('search'); ?></button></div></form>
      </div>
    </aside>
  </div>
  <?php if ($dtc_related_entries): ?><section class="d-editorial" aria-labelledby="dtc-related-title"><div class="d-section-heading"><div><p class="d-kicker">من نفس مجموعة الأكواد</p><h2 id="dtc-related-title">أكواد أخرى في المكتبة</h2></div><a class="d-text-link" href="<?php echo esc_url($dtc_library_url); ?>">كل الأكواد <span aria-hidden="true">←</span></a></div><div class="d-code-grid"><?php foreach ($dtc_related_entries as $dtc_entry): ?><article class="d-code-card"><a href="<?php echo esc_url($dtc_entry['url']); ?>"><div class="d-code-card-top"><b class="d-code" dir="ltr"><?php echo esc_html($dtc_entry['code']); ?></b><span class="d-card-arrow" aria-hidden="true">←</span></div><h3><?php echo esc_html($dtc_entry['title']); ?></h3><?php if (!empty($dtc_entry['category'])): ?><span class="d-code-category"><?php echo esc_html($dtc_entry['category']); ?></span><?php endif; ?></a></article><?php endforeach; ?></div></section><?php endif; ?>
  <?php if ($dtc_promos): ?><section class="d-editorial" aria-labelledby="dtc-single-editorial-title"><div class="d-section-heading"><div><p class="d-kicker">من مقالات أعطال</p><h2 id="dtc-single-editorial-title">اكتشف السيارات مع أعطال</h2><p>مراجعات وأسعار من محتوى الموقع</p></div></div><div class="d-article-grid"><?php foreach ($dtc_promos as $dtc_promo_id): if (!has_post_thumbnail($dtc_promo_id)) continue; ?><article class="d-article-card"><a href="<?php echo esc_url(get_permalink($dtc_promo_id)); ?>"><div class="d-article-image"><?php echo get_the_post_thumbnail($dtc_promo_id, 'medium_large', ['loading' => 'lazy', 'decoding' => 'async']); ?></div><div class="d-article-body"><span class="d-kicker">من مقالات أعطال</span><h3><?php echo esc_html(get_the_title($dtc_promo_id)); ?></h3><span class="d-article-tail">اقرأ المقال <span aria-hidden="true">←</span></span></div></a></article><?php endforeach; ?></div></section><?php endif; ?>
</main>
<?php endwhile; get_footer('dtc'); ?>
