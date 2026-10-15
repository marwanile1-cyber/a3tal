<?php
if (!defined('ABSPATH')) exit;
$dtc_catalog = a3g_dtc_catalog();
$dtc_library_url = get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/');
$dtc_query_code = get_query_var('code', '');
$dtc_raw_code = isset($_GET['code']) && is_string($_GET['code']) ? wp_unslash($_GET['code']) : (is_string($dtc_query_code) ? $dtc_query_code : '');
$dtc_search = trim(preg_replace('/\s+/u', ' ', sanitize_text_field(a3g_dtc_digits($dtc_raw_code))));
$dtc_valid_search = function_exists('mb_strlen') ? mb_strlen($dtc_search, 'UTF-8') <= 80 : strlen($dtc_search) <= 240;
$dtc_family = isset($_GET['family']) && is_string($_GET['family']) ? strtoupper(sanitize_text_field(wp_unslash($_GET['family']))) : '';
if (!in_array($dtc_family, ['P', 'B', 'C', 'U'], true)) $dtc_family = '';
$dtc_families = [
  'P' => ['المحرك وناقل الحركة', 'Powertrain'],
  'B' => ['الهيكل والمقصورة', 'Body'],
  'C' => ['الشاسيه والفرامل', 'Chassis'],
  'U' => ['الشبكات والاتصالات', 'Network'],
];
$dtc_matches = $dtc_valid_search ? a3g_dtc_filter_catalog($dtc_catalog, $dtc_search, $dtc_family) : [];
$dtc_total = count($dtc_matches);
$dtc_pages = max(1, (int) ceil($dtc_total / 18));
$dtc_page = isset($_GET['dtc_page']) && is_scalar($_GET['dtc_page']) ? max(1, absint($_GET['dtc_page'])) : 1;
$dtc_page = min($dtc_page, $dtc_pages);
$dtc_entries = array_slice($dtc_matches, ($dtc_page - 1) * 18, 18);
$dtc_sample = array_slice($dtc_catalog, 0, 2);
$dtc_recent = a3g_dtc_recent_discussions(3);
$dtc_promos = a3g_dtc_promo_ids([], 3);
get_header('dtc');
?>
<main id="dtc-main">
  <section class="d-hero">
    <div class="d-wrap d-hero-grid">
      <div class="d-hero-copy">
        <p class="d-eyebrow">مكتبة أكواد أعطال السيارات OBD-II</p>
        <h1>كل كود له حكاية.<br><span>اعرف تبدأ منين.</span></h1>
        <p class="d-hero-description">افهم معنى العطل، رتّب خطوات الفحص، واستفد من تجارب الناس قبل ما تغيّر أي قطعة.</p>
        <form class="d-search" action="<?php echo esc_url($dtc_library_url); ?>#dtc-codes" method="get" role="search" aria-label="البحث في أكواد الأعطال" data-dtc-search>
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg>
          <label class="screen-reader-text" for="dtc-code-search">كود العطل</label>
          <input id="dtc-code-search" type="text" name="code" value="<?php echo esc_attr($dtc_search); ?>" placeholder="ابحث بالكود أو اسم الحساس، مثل P0172 أو حساس الكامة" maxlength="80" autocomplete="off" autocapitalize="characters" spellcheck="false" dir="ltr">
          <?php if ($dtc_family): ?><input type="hidden" name="family" value="<?php echo esc_attr($dtc_family); ?>"><?php endif; ?>
          <button type="submit">فسّر الكود</button>
        </form>
        <div class="d-search-hint"><span>جرّب:</span><?php foreach ($dtc_sample as $dtc_example): ?><a href="<?php echo esc_url($dtc_example['url']); ?>" dir="ltr"><?php echo esc_html($dtc_example['code']); ?></a><?php endforeach; ?><span>شارك باسم مستعار، دون حساب</span></div>
      </div>
      <div class="d-scanner" aria-hidden="true">
        <div class="d-scanner-top"><span>OBD · DIAGNOSTICS</span><span class="d-scanner-dot">READ · UNDERSTAND</span></div>
        <div class="d-scanner-screen"><span class="d-scanner-code"><?php echo esc_html($dtc_sample ? $dtc_sample[0]['code'] : 'OBD-II'); ?></span><div class="d-scan-wave"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><p>الكود بداية التشخيص.<br>الفحص هو اللي يحدد السبب.</p></div>
        <div class="d-scanner-bottom"><span>A3TAL / DTC LIBRARY</span><i></i></div>
      </div>
    </div>
  </section>
  <?php /* Global marque discovery is additive: the existing indexed DTC list remains intact. */ ?>
  <?php if (is_file(get_template_directory() . '/dtc-world-garage.php')) require get_template_directory() . '/dtc-world-garage.php'; ?>
  <nav class="d-families" aria-label="مجموعات أكواد الأعطال"><div class="d-wrap d-families-grid">
    <?php foreach ($dtc_families as $dtc_letter => $dtc_names): ?>
      <a class="d-family<?php echo $dtc_family === $dtc_letter ? ' is-active' : ''; ?>" href="<?php echo esc_url(add_query_arg('family', $dtc_letter, $dtc_library_url) . '#dtc-codes'); ?>" <?php if ($dtc_family === $dtc_letter) echo 'aria-current="true"'; ?>><span class="d-family-letter" dir="ltr"><?php echo esc_html($dtc_letter); ?></span><span><strong><?php echo esc_html($dtc_names[0]); ?></strong><small lang="en" dir="ltr"><?php echo esc_html($dtc_names[1]); ?></small></span></a>
    <?php endforeach; ?>
  </div></nav>
  <div class="d-wrap d-main">
    <section id="dtc-codes" aria-labelledby="dtc-codes-title">
      <div class="d-section-heading"><div><p class="d-kicker"><?php echo $dtc_search !== '' || $dtc_family !== '' ? 'نتائج البحث والتصفح' : 'مكتبة أعطال الحالية'; ?></p><h2 id="dtc-codes-title"><?php echo $dtc_search !== '' ? 'نتائج البحث عن ' . esc_html($dtc_search) : ($dtc_family ? esc_html($dtc_families[$dtc_family][0]) : 'ابدأ من الكود اللي عندك'); ?></h2><p><?php echo esc_html(number_format_i18n($dtc_total)); ?> شرحًا متاحًا<?php if ($dtc_pages > 1): ?> · صفحة <?php echo esc_html(number_format_i18n($dtc_page)); ?> من <?php echo esc_html(number_format_i18n($dtc_pages)); ?><?php endif; ?></p></div><?php if ($dtc_search !== '' || $dtc_family !== ''): ?><a class="d-text-link" href="<?php echo esc_url($dtc_library_url . '#dtc-codes'); ?>">كل الأكواد <span aria-hidden="true">←</span></a><?php endif; ?></div>
      <div class="d-code-grid">
        <?php foreach ($dtc_entries as $dtc_entry): ?>
          <article class="d-code-card"><a href="<?php echo esc_url($dtc_entry['url']); ?>"><div class="d-code-card-top"><b class="d-code" dir="ltr"><?php echo esc_html($dtc_entry['code']); ?></b><span class="d-card-arrow" aria-hidden="true">←</span></div><h3><?php echo esc_html($dtc_entry['title']); ?></h3><?php if (!empty($dtc_entry['excerpt'])): ?><p><?php echo esc_html($dtc_entry['excerpt']); ?></p><?php endif; ?><span class="d-code-category"><?php echo esc_html(!empty($dtc_entry['category']) ? $dtc_entry['category'] : $dtc_families[substr($dtc_entry['code'], 0, 1)][0]); ?></span></a></article>
        <?php endforeach; ?>
        <?php if (!$dtc_entries): ?><div class="d-empty"><span class="d-empty-code" dir="ltr"><?php echo esc_html($dtc_search ?: ($dtc_family ?: 'OBD-II')); ?></span><h3><?php echo $dtc_valid_search ? 'لا يوجد شرح منشور مطابق حاليًا' : 'عبارة البحث طويلة جدًا'; ?></h3><p><?php echo $dtc_valid_search ? 'جرّب رقم الكود أو اسم الحساس بالعربية أو الإنجليزية، أو تصفح الشروحات المتاحة.' : 'اختصر عبارة البحث إلى 80 حرفًا كحد أقصى.'; ?></p><a class="d-button" href="<?php echo esc_url($dtc_library_url . '#dtc-codes'); ?>">تصفح المكتبة</a></div><?php endif; ?>
      </div>
      <?php if ($dtc_pages > 1): ?><nav class="d-pagination" aria-label="صفحات أكواد الأعطال"><?php if ($dtc_page > 1): ?><a class="d-button d-button-quiet" rel="prev" href="<?php echo esc_url(add_query_arg(['code' => $dtc_search ?: false, 'family' => $dtc_family ?: false, 'dtc_page' => $dtc_page - 1], $dtc_library_url) . '#dtc-codes'); ?>">الصفحة السابقة</a><?php endif; ?><span><?php echo esc_html(number_format_i18n($dtc_page)); ?> / <?php echo esc_html(number_format_i18n($dtc_pages)); ?></span><?php if ($dtc_page < $dtc_pages): ?><a class="d-button d-button-quiet" rel="next" href="<?php echo esc_url(add_query_arg(['code' => $dtc_search ?: false, 'family' => $dtc_family ?: false, 'dtc_page' => $dtc_page + 1], $dtc_library_url) . '#dtc-codes'); ?>">الصفحة التالية</a><?php endif; ?></nav><?php endif; ?>
    </section>
    <section id="dtc-community" class="d-community" aria-labelledby="dtc-community-title">
      <div class="d-community-intro"><span class="d-community-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M16 3H5a2 2 0 0 0-2 2v11l4-3h9a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2Z"/><path d="M8 17v1a2 2 0 0 0 2 2h7l4 3V10a2 2 0 0 0-2-2"/></svg></span><p class="d-kicker">الأسئلة وتجارب الإصلاح</p><h2 id="dtc-community-title">نفس الكود.<br>تجارب مختلفة.</h2><p>احكي اللي بيحصل في عربيتك، واسأل الناس اللي مرّت بالتجربة. افتح صفحة الكود وشارك باسم مستعار، من غير حساب.</p><a class="d-text-link" href="#dtc-codes">اختَر الكود وشارك تجربتك <span aria-hidden="true">←</span></a></div>
      <div class="d-community-feed">
        <?php if ($dtc_recent): foreach ($dtc_recent as $dtc_comment): $dtc_comment_code = a3g_dtc_current_code((int) $dtc_comment->comment_post_ID); ?><a class="d-recent-comment" href="<?php echo esc_url(a3g_dtc_comment_url($dtc_comment)); ?>"><span class="d-mini-code" dir="ltr"><?php echo esc_html($dtc_comment_code ?: 'DTC'); ?></span><span><strong><?php echo esc_html(wp_trim_words(wp_strip_all_tags($dtc_comment->comment_content), 22)); ?></strong><small><?php echo esc_html($dtc_comment->comment_author); ?> · <?php echo esc_html(get_comment_date(get_option('date_format'), $dtc_comment)); ?></small></span></a><?php endforeach; else: ?><div class="d-community-empty"><span class="d-community-lines" aria-hidden="true"><i></i><i></i><i></i></span><h3>تجربتك ممكن تساعد غيرك</h3><p>عندك سؤال أو وصلت لسبب العطل؟ شاركه داخل صفحة الكود مع نوع السيارة والأعراض وما تم فحصه.</p><a class="d-button d-button-quiet" href="#dtc-codes">ابدأ من مكتبة الأكواد</a></div><?php endif; ?>
      </div>
    </section>
    <?php if ($dtc_promos): ?><section class="d-editorial" aria-labelledby="dtc-editorial-title"><div class="d-section-heading"><div><p class="d-kicker">من مقالات أعطال</p><h2 id="dtc-editorial-title">كمّل رحلتك مع أعطال</h2><p>أسعار السيارات ومراجعات تساعدك تختار</p></div><a class="d-text-link" href="<?php echo esc_url(a3g_cat_link(22)); ?>">المزيد من المقالات <span aria-hidden="true">←</span></a></div><div class="d-article-grid"><?php foreach ($dtc_promos as $dtc_promo_id): if (!has_post_thumbnail($dtc_promo_id)) continue; ?><article class="d-article-card"><a href="<?php echo esc_url(get_permalink($dtc_promo_id)); ?>"><div class="d-article-image"><?php echo get_the_post_thumbnail($dtc_promo_id, 'medium_large', ['loading' => 'lazy', 'decoding' => 'async']); ?></div><div class="d-article-body"><span class="d-kicker">من مقالات أعطال</span><h3><?php echo esc_html(get_the_title($dtc_promo_id)); ?></h3><span class="d-article-tail">اقرأ المقال <span aria-hidden="true">←</span></span></div></a></article><?php endforeach; ?></div></section><?php endif; ?>
  </div>
</main>
<?php get_footer('dtc'); ?>
