<?php
/** Shared A3tal navigation, diagnostic summaries and search improvements. */
if (!defined('ABSPATH')) exit;
add_filter('body_class', static function($classes) {
    $classes[] = 'a3tal-ux-20261031';
    return $classes;
});

function a3g_ux_original_guide_id($post_id) {
    $post_id = (int) $post_id;
    if (get_post_type($post_id) !== 'a3_dtc' || !function_exists('a3g_dtc_content_id')) return $post_id;
    $original = (int) a3g_dtc_content_id($post_id);
    return $original && get_post_status($original) === 'publish' ? $original : $post_id;
}

/** Extract an existing explanation, never generate a diagnosis from the code alone. */
function a3g_ux_dtc_summary($post_id, $code = '') {
    $manual = trim(wp_strip_all_tags((string) get_post_field('post_excerpt', $post_id)));
    if ($manual !== '' && !preg_match('/^(?:الإجابة السريعة|لو الكود على البنك الثاني)/u', $manual)) {
        return wp_trim_words($manual, 42, '…');
    }
    $html = (string) get_post_field('post_content', $post_id);
    $html = preg_replace('~<(aside|nav|figure|table|script|style)\b[^>]*>.*?</\1>~is', '', $html);
    preg_match_all('~<p\b[^>]*>(.*?)</p>~is', $html, $paragraphs);
    foreach ($paragraphs[1] ?? [] as $paragraph) {
        $text = trim(html_entity_decode(wp_strip_all_tags(strip_shortcodes($paragraph)), ENT_QUOTES, 'UTF-8'));
        $length = function_exists('mb_strlen') ? mb_strlen($text, 'UTF-8') : strlen($text);
        if ($length < 85 || ($code !== '' && stripos($text, $code) === false)) continue;
        if (preg_match('/^(?:لو |إذا كنت تبحث|راجع |للمزيد|مصدر|آخر تحديث)/u', $text)) continue;
        return wp_trim_words($text, 42, '…');
    }
    return $manual !== '' ? wp_trim_words($manual, 42, '…') : '';
}

/** Exclude only linked mirror records before SQL pagination; unique codes remain. */
function a3g_ux_mirror_ids() {
    $cached = get_transient('a3g_ux_search_mirrors_v1');
    if (is_array($cached)) return $cached;
    $ids = [];
    $records = get_posts(['post_type'=>'a3_dtc', 'post_status'=>'publish', 'posts_per_page'=>-1, 'no_found_rows'=>true]);
    foreach ($records as $record) {
        if (a3g_ux_original_guide_id($record->ID) !== (int) $record->ID) $ids[] = (int) $record->ID;
    }
    set_transient('a3g_ux_search_mirrors_v1', $ids, HOUR_IN_SECONDS);
    return $ids;
}
function a3g_ux_clear_search_cache($post_id = 0) {
    if (!$post_id || in_array(get_post_type($post_id), ['post','a3_dtc'], true)) delete_transient('a3g_ux_search_mirrors_v1');
}
add_action('save_post', 'a3g_ux_clear_search_cache');
add_action('deleted_post', static function() { delete_transient('a3g_ux_search_mirrors_v1'); });
add_action('updated_post_meta', static function($meta_id, $post_id, $key) {
    if (in_array($key, ['_a3_related_post_ids','_a3_dtc_code'], true)) a3g_ux_clear_search_cache($post_id);
}, 10, 3);
add_action('added_post_meta', static function($meta_id, $post_id, $key) {
    if (in_array($key, ['_a3_related_post_ids','_a3_dtc_code'], true)) a3g_ux_clear_search_cache($post_id);
}, 10, 3);
add_action('pre_get_posts', static function($query) {
    if (is_admin() || !$query->is_main_query() || !$query->is_search()) return;
    $excluded = array_map('absint', (array) $query->get('post__not_in'));
    $query->set('post__not_in', array_values(array_unique(array_merge($excluded, a3g_ux_mirror_ids()))));
    $phrase = trim((string) $query->get('s'));
    if (!preg_match('/^[PBCU][0-9][0-9A-F]{3}$/iD', $phrase) || !function_exists('a3g_dtc_catalog')) return;
    foreach (a3g_dtc_catalog() as $entry) {
        if (strtoupper((string) ($entry['code'] ?? '')) !== strtoupper($phrase)) continue;
        $query->set('a3tal_ux_exact_code_id', a3g_ux_original_guide_id((int) $entry['id']));
        break;
    }
}, 30);
add_filter('posts_orderby', static function($orderby, $query) {
    if (is_admin() || !$query->is_main_query() || !$query->is_search()) return $orderby;
    $id = (int) $query->get('a3tal_ux_exact_code_id');
    if (!$id) return $orderby;
    global $wpdb;
    return 'CASE WHEN ' . $wpdb->posts . '.ID = ' . $id . ' THEN 0 ELSE 1 END' . ($orderby ? ', ' . $orderby : '');
}, 30, 2);

/** These terms already exist; offer a brand only if a record or a published guide supports it. */
function a3g_ux_directory_guides($brand = '', $location = '') {
    static $all = null;
    if ($all === null) $all = get_posts(['post_type'=>'post','post_status'=>'publish','category'=>33,'posts_per_page'=>200,'orderby'=>'modified','order'=>'DESC','no_found_rows'=>true]);
    $aliases = ['hyundai'=>['هيونداي','هيونداى'],'kia'=>['كيا'],'toyota'=>['تويوتا'],'chery'=>['شيري','شيرى'],'chevrolet'=>['شيفروليه'],'skoda'=>['سكودا'],'fiat'=>['فيات'],'jetour'=>['جيتور'],'geely'=>['جيلي','جيلى'],'byd'=>['بي واي دي'],'mg'=>['إم جي','ام جي'],'opel'=>['أوبل','اوبل'],'peugeot'=>['بيجو'],'renault'=>['رينو'],'nissan'=>['نيسان'],'changan'=>['شانجان'],'haval'=>['هافال'],'soueast'=>['ساوايست','ساو إيست','ساو ايست'],'jaecoo'=>['جايكو'],'deepal'=>['ديبال'],'bmw'=>['بي إم دبليو'],'mercedes'=>['مرسيدس']];
    $term = $brand !== '' ? get_term_by('slug', $brand, 'a3_brand') : null;
    $needles = $term && !is_wp_error($term) ? [$term->name, urldecode($term->slug)] : [];
    if ($brand !== '' && !$needles) return [];
    foreach ($aliases as $slug => $names) {
        if ($term && (strtolower($term->slug) === $slug || in_array($term->name, $names, true))) $needles = array_merge($needles, [$slug], $names);
    }
    return array_values(array_filter($all, static function($post) use ($needles, $location) {
        if ($post->post_password !== '') return false;
        if ($needles) {
            $matches = false;
            foreach ($needles as $needle) {
                if (preg_match('/(?<![\p{L}\p{N}])' . preg_quote($needle, '/') . '(?![\p{L}\p{N}])/iu', $post->post_title)) { $matches = true; break; }
            }
            if (!$matches) return false;
        }
        if ($location !== '') {
            $text = wp_strip_all_tags($post->post_title . ' ' . $post->post_content);
            if (function_exists('mb_stripos') ? mb_stripos($text, $location, 0, 'UTF-8') === false : stripos($text, $location) === false) return false;
        }
        return true;
    }));
}

/** Homepage sharing uses the current lead car photo, with matching size and MIME. */
function a3g_ux_home_image() {
    static $image = null;
    if ($image !== null) return $image;
    $posts = get_posts(['post_type'=>'post','post_status'=>'publish','cat'=>374,'posts_per_page'=>1,'meta_key'=>'_thumbnail_id','no_found_rows'=>true]);
    $id = $posts ? (int) get_post_thumbnail_id($posts[0]->ID) : 0;
    $source = $id ? wp_get_attachment_image_src($id, 'full') : false;
    $image = $source ? ['url'=>$source[0],'width'=>(int)$source[1],'height'=>(int)$source[2],'type'=>(string)get_post_mime_type($id)] : [];
    return $image;
}
foreach (['wpseo_opengraph_image','wpseo_twitter_image'] as $filter) add_filter($filter, static function($url) {
    if (!is_front_page()) return $url;
    $image = a3g_ux_home_image();
    return $image['url'] ?? $url;
}, 150);
foreach (['width','height','type'] as $field) add_filter('wpseo_opengraph_image_' . $field, static function($original) use ($field) {
    if (!is_front_page()) return $original;
    $image = a3g_ux_home_image();
    return $image[$field] ?? $original;
}, 150);

add_action('wp_enqueue_scripts', static function() {
    $root = get_template_directory();
    $deps = ['a3g-style'];
    if (function_exists('a3g_dtc_is_library') && a3g_dtc_is_library()) $deps[] = 'a3g-dtc-library';
    if (is_file($root . '/ux-improvements-20261031.css')) wp_enqueue_style('a3g-ux-20261031', get_template_directory_uri() . '/ux-improvements-20261031.css', $deps, (string)filemtime($root . '/ux-improvements-20261031.css'));
    if (is_file($root . '/assets/js/ux-improvements-20261031.js')) wp_enqueue_script('a3g-ux-20261031', get_template_directory_uri() . '/assets/js/ux-improvements-20261031.js', [], (string)filemtime($root . '/assets/js/ux-improvements-20261031.js'), true);
}, 120);

/** AdSense's documented per-link opt-out keeps code navigation uninterrupted. */
add_filter('the_content', static function($html) {
    if (!function_exists('a3g_dtc_is_library') || !a3g_dtc_is_library() || !class_exists('WP_HTML_Tag_Processor')) return $html;
    $tags = new WP_HTML_Tag_Processor($html);
    $host = (string) wp_parse_url(home_url('/'), PHP_URL_HOST);
    while ($tags->next_tag('A')) {
        $href = (string) $tags->get_attribute('href');
        if ($href === '') continue;
        $target_host = (string) wp_parse_url($href, PHP_URL_HOST);
        if ($href[0] === '#' || ($href[0] === '/' && substr($href, 0, 2) !== '//') || $target_host === $host) $tags->set_attribute('data-google-vignette', 'false');
    }
    return $tags->get_updated_html();
}, 200);
