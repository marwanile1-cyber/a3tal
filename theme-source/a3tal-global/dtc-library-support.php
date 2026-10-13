<?php
/** Independent DTC experience using published A3tal content. */
if (!defined('ABSPATH')) exit;

define('A3G_DTC_VERSION', '1.0.0');
if (is_file(get_template_directory() . '/dtc-model-links.php')) {
    require_once get_template_directory() . '/dtc-model-links.php';
}

function a3g_dtc_codes_in_title($post_id) {
    $post = get_post((int)$post_id);
    if (!$post) return [];
    $text = wp_strip_all_tags($post->post_title) . ' ' . $post->post_name;
    preg_match_all('/(?<![A-Z0-9])([PBCU][0-9][0-9A-F]{3})(?![A-Z0-9])/i', $text, $matches);
    $codes = array_map('strtoupper', $matches[1] ?? []);
    $meta = strtoupper(trim((string)get_post_meta($post->ID, '_a3_dtc_code', true)));
    if (preg_match('/^[PBCU][0-9][0-9A-F]{3}$/D', $meta)) array_unshift($codes, $meta);
    return array_values(array_unique($codes));
}

function a3g_dtc_current_code($post_id = 0) {
    $codes = a3g_dtc_codes_in_title($post_id ?: get_the_ID());
    return $codes[0] ?? '';
}

function a3g_dtc_is_comment_target($post_id) {
    $post = get_post((int)$post_id);
    if (!$post || $post->post_status !== 'publish' || $post->post_password !== '') return false;
    if ($post->post_type === 'a3_dtc') return true;
    return $post->post_type === 'post' && has_category(2, $post->ID) && (bool)a3g_dtc_codes_in_title($post->ID);
}

function a3g_dtc_is_library() {
    if (is_admin()) return false;
    if (is_post_type_archive('a3_dtc')) return true;
    if (is_singular('a3_dtc')) return !post_password_required(get_queried_object_id());
    return is_singular('post') && a3g_dtc_is_comment_target(get_queried_object_id());
}

/** The original guide remains the discussion/content owner; no article moves. */
function a3g_dtc_content_id($post_id) {
    $post_id = (int)$post_id;
    if (get_post_type($post_id) !== 'a3_dtc') return $post_id;
    $code = a3g_dtc_current_code($post_id);
    foreach (a3g_related_post_ids($post_id) as $related_id) {
        if (get_post_type($related_id) === 'post' && a3g_dtc_is_comment_target($related_id) && in_array($code, a3g_dtc_codes_in_title($related_id), true)) return (int)$related_id;
    }
    return $post_id;
}

/** Deduplicate records and legacy guides by code, with explicit records first. */
function a3g_dtc_catalog() {
    $cached = get_transient('a3g_dtc_catalog_v1');
    if (is_array($cached)) return $cached;
    $entries = [];
    $records = get_posts(['post_type'=>'a3_dtc','post_status'=>'publish','posts_per_page'=>-1,'orderby'=>'title','order'=>'ASC','no_found_rows'=>true]);
    $guides = get_posts(['post_type'=>'post','post_status'=>'publish','category'=>2,'posts_per_page'=>-1,'orderby'=>'modified','order'=>'DESC','no_found_rows'=>true]);
    foreach (array_merge($records, $guides) as $post) {
        if ($post->post_password !== '') continue;
        foreach (a3g_dtc_codes_in_title($post->ID) as $code) {
            if (isset($entries[$code])) continue;
            $category = (string)get_post_meta($post->ID, '_a3_dtc_system', true);
            if ($category === '') {
                $category = ['P'=>'المحرك وناقل الحركة','B'=>'الهيكل والمقصورة','C'=>'الشاسيه والفرامل','U'=>'الشبكات والاتصالات'][$code[0]];
            }
            $entries[$code] = ['code'=>$code,'title'=>get_the_title($post->ID),'url'=>get_permalink($post->ID),'id'=>(int)$post->ID,'category'=>$category,'excerpt'=>a3g_excerpt($post->ID, 22)];
        }
    }
    ksort($entries);
    $entries = array_values($entries);
    set_transient('a3g_dtc_catalog_v1', $entries, 10 * MINUTE_IN_SECONDS);
    return $entries;
}

function a3g_dtc_clear_catalog($post_id) {
    if (in_array(get_post_type($post_id), ['post','a3_dtc'], true)) delete_transient('a3g_dtc_catalog_v1');
}
add_action('save_post', 'a3g_dtc_clear_catalog');
add_action('deleted_post', static function() { delete_transient('a3g_dtc_catalog_v1'); });
add_action('trashed_post', 'a3g_dtc_clear_catalog');
add_action('untrashed_post', 'a3g_dtc_clear_catalog');

function a3g_dtc_promo_ids($exclude = [], $limit = 3) {
    $posts = get_posts(['post_type'=>'post','post_status'=>'publish','category__in'=>[374,22,21],'post__not_in'=>array_map('absint', (array)$exclude),'posts_per_page'=>max(1,min(6,(int)$limit)),'orderby'=>'modified','order'=>'DESC','meta_query'=>[['key'=>'_thumbnail_id','compare'=>'EXISTS']],'no_found_rows'=>true]);
    return array_map(static function($post) { return (int)$post->ID; }, $posts);
}

function a3g_dtc_recent_discussions($limit = 3) {
    $ids = [];
    foreach (a3g_dtc_catalog() as $entry) $ids[] = a3g_dtc_content_id($entry['id']);
    $ids = array_values(array_unique($ids));
    if (!$ids) return [];
    return get_comments(['post__in'=>$ids,'status'=>'approve','type'=>'comment','number'=>max(1,min(6,(int)$limit)),'orderby'=>'comment_date_gmt','order'=>'DESC']);
}

add_filter('template_include', static function($template) {
    if (!a3g_dtc_is_library()) return $template;
    $name = is_post_type_archive('a3_dtc') ? 'dtc-library-archive.php' : 'dtc-library-single.php';
    $file = get_template_directory() . '/' . $name;
    return is_file($file) ? $file : $template;
}, 99);

add_filter('body_class', static function($classes) {
    if (a3g_dtc_is_library()) $classes[] = 'a3g-dtc-library';
    return $classes;
});

add_action('wp_enqueue_scripts', static function() {
    if (!a3g_dtc_is_library()) return;
    wp_enqueue_style('a3g-dtc-library', get_template_directory_uri().'/dtc-library.css', ['a3g-style'], A3G_DTC_VERSION);
    // The global garage only runs on the archive. Version by file modification to avoid stale cached UI.
    if (is_post_type_archive('a3_dtc')) {
        $gg_css = get_template_directory() . '/dtc-world-garage.css';
        $gg_js = get_template_directory() . '/assets/js/dtc-world-garage.js';
        if (is_file($gg_css)) wp_enqueue_style('a3g-global-garage', get_template_directory_uri() . '/dtc-world-garage.css', ['a3g-dtc-library'], (string)filemtime($gg_css));
        $gg_logo_pack = get_template_directory() . '/assets/js/dtc-brand-logos.generated.js';
        $gg_logo_dependencies = [];
        if (is_file($gg_logo_pack)) {
            wp_enqueue_script('a3g-global-brand-logos', get_template_directory_uri() . '/assets/js/dtc-brand-logos.generated.js', [], (string)filemtime($gg_logo_pack), true);
            $gg_logo_dependencies = ['a3g-global-brand-logos'];
        }
        if (is_file($gg_js)) wp_enqueue_script('a3g-global-garage', get_template_directory_uri() . '/assets/js/dtc-world-garage.js', $gg_logo_dependencies, (string)filemtime($gg_js), true);
    }
});

// Search/filter and discussion-page variants keep the original canonical URL.
function a3g_dtc_is_variant() {
    return (is_post_type_archive('a3_dtc') && (!empty($_GET['code']) || !empty($_GET['family']) || !empty($_GET['dtc_page'])))
        || (a3g_dtc_is_library() && is_singular() && !empty($_GET['dcpage']));
}
add_filter('wpseo_robots', static function($robots) {
    if (a3g_dtc_is_variant()) return 'noindex, follow';
    return $robots;
}, 110);
add_filter('wp_robots', static function($robots) {
    if (a3g_dtc_is_variant()) {
        unset($robots['index']);
        $robots['noindex'] = true;
        $robots['follow'] = true;
    }
    return $robots;
}, 110);
add_filter('wpseo_canonical', static function($canonical) {
    if (a3g_dtc_is_variant()) return is_post_type_archive('a3_dtc') ? get_post_type_archive_link('a3_dtc') : get_permalink(get_queried_object_id());
    return $canonical;
}, 110);

require_once __DIR__ . '/dtc-discussions.php';
