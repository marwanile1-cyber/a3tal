<?php
/**
 * A3tal Global Garage. Real bidirectional vehicle/diagnostic guide discovery.
 * Separate "verified for this specific vehicle" from generic OBD explanations.
 */
if (!defined('ABSPATH')) exit;

function a3g_gg_codes_for_vehicle(int $vehicle_id): array {
    if (get_post_type($vehicle_id) !== 'a3_car') return [];
    $raw = strtoupper((string)get_post_meta($vehicle_id, '_a3_verified_dtc_codes', true));
    preg_match_all('/\b[PBCU][0-9][0-9A-F]{3}\b/', $raw, $matches);
    $source = trim((string)get_post_meta($vehicle_id, '_a3_verified_dtc_source', true));
    $source_url = esc_url_raw($source);
    // Never assert that any code is model-specific without an editorial reference.
    if (!$source_url || !preg_match('#^https://#', $source_url)) return [];
    return array_values(array_unique($matches[0]));
}

function a3g_gg_vehicle_index(): array {
    $ids = get_posts(['post_type'=>'a3_car','post_status'=>'publish','posts_per_page'=>150,
       'fields'=>'ids','orderby'=>'date','order'=>'DESC','no_found_rows'=>true]);
    $result = [];
    foreach ($ids as $id) {
        $terms = get_the_terms($id,'a3_brand');
        $brand = ($terms && !is_wp_error($terms)) ? (string)$terms[0]->name : '';
        $result[] = [
            'id'=>(int)$id,'brand'=>$brand,'title'=>get_the_title($id),
            'year'=>(int)get_post_meta($id,'_a3_year',true),
            'url'=>get_permalink($id),
            'verified_codes'=>a3g_gg_codes_for_vehicle((int)$id)
        ];
    }
    return $result;
}

function a3g_gg_verified_vehicle_for_code(string $code): array {
    $result = [];
    foreach (a3g_gg_vehicle_index() as $car) {
        if (in_array($code,$car['verified_codes'],true)) $result[] = $car;
    }
    return $result;
}
function a3g_gg_guide_entries(int $limit = 12): array {
    if (!function_exists('a3g_dtc_catalog')) return [];
    $catalog = a3g_dtc_catalog();
    // Feature recent researched full guides; avoid short legacy multi-code stubs.
    $filtered = [];
    foreach ($catalog as $item) {
       if (get_post_type((int)$item['id']) !== 'a3_dtc') continue;
       if (!preg_match('/^P[0-9][0-9A-F]{3}$/',$item['code'])) continue;
       $post = get_post((int)$item['id']);
       if (!$post || strlen(wp_strip_all_tags($post->post_content)) < 1200) continue;
       $filtered[] = ['code'=>$item['code'],'title'=>$item['title'],'url'=>$item['url']];
    }
    return array_slice($filtered, -$limit);
}

add_action('wp_enqueue_scripts', static function() {
    if (!is_singular('a3_car') && !is_singular('a3_dtc') && !is_post_type_archive('a3_dtc')) return;
    $file = get_template_directory().'/dtc-model-links.css';
    if (is_file($file)) wp_enqueue_style('a3g-dtc-model-links',get_template_directory_uri().'/dtc-model-links.css',[],(string)filemtime($file));
}, 30);

add_action('wp_footer', static function() {
    if (!is_post_type_archive('a3_dtc')) return;
    $payload = [
       'cars'=>a3g_gg_vehicle_index(),
       'guides'=>array_map(static function($x) {
         return ['code'=>$x['code'],'title'=>$x['title'],'url'=>$x['url']];
       }, a3g_dtc_catalog())
    ];
    echo '<script type="application/json" id="a3tal-gg-data">'.wp_json_encode($payload,JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT).'</script>';
}, 1);

function a3g_gg_diagnostics_section(int $vehicle_id): string {
    if (get_post_type($vehicle_id) !== 'a3_car') return '';
    $found = a3g_gg_codes_for_vehicle($vehicle_id);
    $catalog = function_exists('a3g_dtc_catalog') ? a3g_dtc_catalog() : [];
    $map = [];foreach($catalog as $entry) $map[$entry['code']]=$entry;
    $source = esc_url((string)get_post_meta($vehicle_id,'_a3_verified_dtc_source',true));
    $title = get_the_title($vehicle_id);
    ob_start(); ?>
    <section class="gg-related" id="a3tal-vehicle-diagnostics" aria-labelledby="gg-related-title">
      <span class="gg-related-eyebrow">A3TAL GLOBAL GARAGE</span>
      <h2 id="gg-related-title">دليل تشخيص الأعطال للسيارة: <?php echo esc_html($title); ?></h2>
      <p>ابدأ بالكود الذي قرأه جهاز OBD-II أو بعرض المشكلة. الأكواد العامة أدلة لفهم الفحص وليست قائمة بأعطال شائعة مؤكدة لهذه السيارة. راجع سنة التصنيع ونوع المحرك قبل اتخاذ قرار الإصلاح.</p>
      <?php if ($found): ?>
        <h3>أكواد مرتبطة بهذه السيارة بمصدر فني</h3>
        <div class="gg-related-grid"><?php foreach($found as $code):if(empty($map[$code]))continue;?>
         <a href="<?php echo esc_url($map[$code]['url']); ?>"><b dir="ltr"><?php echo esc_html($code);?></b><span><?php echo esc_html($map[$code]['title']);?></span></a>
        <?php endforeach; ?></div>
        <p class="gg-related-source"><a rel="nofollow noopener" target="_blank" href="<?php echo $source; ?>">المصدر الفني لتوثيق انطباق الكود على هذه السيارة</a></p>
      <?php else: ?>
        <p class="gg-related-note">لم نتحقق بعد من أعطال مميزة لهذا الجيل والمحرك؛ لذلك لا نعرض ادعاءات غير موثقة.</p>
      <?php endif; ?>
      <h3>ابدأ من شروحات الأكواد العامة المنشورة</h3>
      <div class="gg-related-grid">
        <?php foreach(a3g_gg_guide_entries(12) as $entry): ?>
        <a href="<?php echo esc_url($entry['url']);?>"><b dir="ltr"><?php echo esc_html($entry['code']);?></b><span><?php echo esc_html(wp_trim_words($entry['title'],10,'…'));?></span></a>
        <?php endforeach;?>
      </div>
      <a class="gg-related-all" href="<?php echo esc_url(get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/')); ?>">تصفح جميع أكواد الأعطال وابحث بكود سيارتك ←</a>
    </section>
    <?php return (string)ob_get_clean();
}
add_filter('the_content',static function($content){
    if (!is_singular('a3_car') || !in_the_loop() || !is_main_query()) return $content;
    $id = (int)get_the_ID();
    return $content.a3g_gg_diagnostics_section($id);
},22);

add_filter('the_content',static function($content) {
    if (!is_singular('a3_dtc') || !in_the_loop() || !is_main_query())return $content;
    $code = function_exists('a3g_dtc_current_code')?a3g_dtc_current_code(get_the_ID()):'';
    $cars = a3g_gg_verified_vehicle_for_code($code);
    if (!$cars) return $content;
    $html = '<section class="gg-dtc-cars"><h2>سيارات ثبت ارتباطها بهذا الكود في مراجع فنية</h2><ul>';
    foreach($cars as $car) {
      $html .= '<li><a href="'.esc_url($car['url']).'">'.esc_html($car['title']).'</a></li>';
    }
    return $content.$html.'</ul><p>ينطبق الوصف فقط على الأجيال والمحركات المذكورة في المصادر، ولا يثبت وحده تلف جزء معين.</p></section>';
},28);
