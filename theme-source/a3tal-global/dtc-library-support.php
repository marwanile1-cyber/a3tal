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
/**
 * Consistent display taxonomy for verified diagnostic code families.
 * This deliberately does not mutate editorial terms or infer OEM-specific meanings.
 */
function a3g_dtc_standard_system($code, $stored = '') {
    $fallback = ['P'=>'المحرك وناقل الحركة','B'=>'الهيكل والمقصورة','C'=>'الشاسيه والفرامل','U'=>'الشبكات والاتصالات'];
    if (preg_match('/^P03(?:3[5-9]|4[0-9])$/', $code)) return 'المحرك / حساسات عمود الكرنك والكامات CKP-CMP';
    if (preg_match('/^P017[0-5]$/', $code)) return 'المحرك / خليط الوقود والهواء Fuel Trim';
    if (preg_match('/^P03A[0-8]$/', $code)) return 'المحرك / حساس ضغط الأسطوانة';
    if (in_array($code, ['P0420','P0430'], true)) return 'المحرك / المحول الحفاز والانبعاثات';
    if ($code === 'P0700') return 'ناقل الحركة / نظام التحكم TCM';
    if ($code === 'P0011') return 'المحرك / توقيت عمود الكامات VVT';
    return trim($stored) !== '' ? trim($stored) : ($fallback[substr($code,0,1)] ?? 'أنظمة السيارة');
}

/** Filter the unified catalog without limiting results to the current page. */
function a3g_dtc_filter_catalog($catalog, $query = '', $family = '') {
    $query = trim(preg_replace('/\\s+/u', ' ', (string)$query));
    $family = strtoupper((string)$family);
    if (!in_array($family, ['P','B','C','U'], true)) $family = '';
    if (function_exists('mb_strlen') && mb_strlen($query, 'UTF-8') > 80) return [];
    if (!function_exists('mb_strlen') && strlen($query) > 240) return [];
    $compact = strtoupper(preg_replace('/\\s+/u', '', $query));
    return array_values(array_filter($catalog, static function ($entry) use ($query, $compact, $family) {
        if ($family !== '' && substr($entry['code'],0,1) !== $family) return false;
        if ($query === '') return true;
        if (strpos($entry['code'], $compact) === 0) return true;
        $text = (string)($entry['search_text'] ?? $entry['title'] . ' ' . $entry['category']);
        if (function_exists('mb_stripos')) return mb_stripos($text, $query, 0, 'UTF-8') !== false;
        return stripos($text, $query) !== false;
    }));
}

function a3g_dtc_ajax_lookup() {
    $raw = isset($_GET['q']) && is_string($_GET['q']) ? wp_unslash($_GET['q']) : '';
    $query = sanitize_text_field(a3g_dtc_digits($raw));
    $family = isset($_GET['family']) && is_string($_GET['family']) ? sanitize_text_field(wp_unslash($_GET['family'])) : '';
    $matches = a3g_dtc_filter_catalog(a3g_dtc_catalog(), $query, $family);
    $results = [];
    foreach (array_slice($matches, 0, 12) as $entry) {
        $results[] = [
            'code' => $entry['code'],
            'title' => $entry['title'],
            'url' => $entry['url'],
            'system' => $entry['category']
        ];
    }
    wp_send_json_success(['total'=>count($matches), 'results'=>$results]);
}
add_action('wp_ajax_a3g_dtc_lookup', 'a3g_dtc_ajax_lookup');
add_action('wp_ajax_nopriv_a3g_dtc_lookup', 'a3g_dtc_ajax_lookup');

/** SEO metadata and graph for the canonical DTC collection only. */
function a3g_dtc_archive_seo_data() {
    return [
        'title' => 'مكتبة أكواد أعطال السيارات (OBD-II DTC) وتفسيرها بالعربي | أعطال.كوم',
        'description' => 'مرجع عربي لتفسير أكواد أعطال السيارات P وB وC وU: معنى الكود والأعراض ودرجة الخطورة عند توثيقها، وخطوات الفحص قبل تغيير القطع.'
    ];
}
add_filter('wpseo_title', static function($title) {
    return is_post_type_archive('a3_dtc') ? a3g_dtc_archive_seo_data()['title'] : $title;
}, 120);
add_filter('wpseo_metadesc', static function($description) {
    return is_post_type_archive('a3_dtc') ? a3g_dtc_archive_seo_data()['description'] : $description;
}, 120);
add_filter('wpseo_opengraph_title', static function($title) {
    return is_post_type_archive('a3_dtc') ? a3g_dtc_archive_seo_data()['title'] : $title;
}, 120);
add_filter('wpseo_opengraph_desc', static function($description) {
    return is_post_type_archive('a3_dtc') ? a3g_dtc_archive_seo_data()['description'] : $description;
}, 120);
add_filter('document_title_parts', static function($parts) {
    if (is_post_type_archive('a3_dtc')) $parts['title'] = a3g_dtc_archive_seo_data()['title'];
    return $parts;
}, 120);
add_action('wp_head', static function() {
    if (!is_post_type_archive('a3_dtc') || a3g_dtc_is_variant()) return;
    $url = get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/');
    $catalog = a3g_dtc_catalog();
    $items = [];
    foreach (array_slice($catalog, 0, 18) as $index => $entry) {
        $items[] = [
            '@type' => 'ListItem',
            'position' => $index + 1,
            'item' => [
                '@type' => 'DefinedTerm',
                'termCode' => $entry['code'],
                'name' => $entry['title'],
                'url' => $entry['url'],
                'description' => $entry['category']
            ]
        ];
    }
    $graph = [
        '@context' => 'https://schema.org',
        '@graph' => [
            [
                '@type' => 'CollectionPage',
                '@id' => $url . '#webpage',
                'url' => $url,
                'name' => a3g_dtc_archive_seo_data()['title'],
                'description' => a3g_dtc_archive_seo_data()['description'],
                'mainEntity' => ['@id' => $url . '#dtc-itemlist']
            ],
            [
                '@type' => 'ItemList',
                '@id' => $url . '#dtc-itemlist',
                'name' => 'أكواد الأعطال المنشورة',
                'numberOfItems' => count($items),
                'itemListElement' => $items
            ]
        ]
    ];
    echo '<script type="application/ld+json">' . wp_json_encode($graph, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) . '</script>' . "\n";
}, 20);

function a3g_dtc_catalog() {
    $cached = get_transient('a3g_dtc_catalog_v2');
    if (is_array($cached)) return $cached;
    $entries = [];
    $records = get_posts(['post_type'=>'a3_dtc','post_status'=>'publish','posts_per_page'=>-1,'orderby'=>'title','order'=>'ASC','no_found_rows'=>true]);
    $guides = get_posts(['post_type'=>'post','post_status'=>'publish','category'=>2,'posts_per_page'=>-1,'orderby'=>'modified','order'=>'DESC','no_found_rows'=>true]);
    foreach (array_merge($records, $guides) as $post) {
        if ($post->post_password !== '') continue;
        foreach (a3g_dtc_codes_in_title($post->ID) as $code) {
            if (isset($entries[$code])) continue;
            $category = a3g_dtc_standard_system($code, (string)get_post_meta($post->ID, '_a3_dtc_system', true));
            $excerpt = a3g_excerpt($post->ID, 22);
            $focus = get_post_meta($post->ID, '_yoast_wpseo_focuskw', true);
            $focus = is_string($focus) ? $focus : '';
            $entries[$code] = [
                'code' => $code,
                'title' => get_the_title($post->ID),
                'url' => get_permalink($post->ID),
                'id' => (int)$post->ID,
                'category' => $category,
                'excerpt' => $excerpt,
                'search_text' => implode(' ', [$code, get_the_title($post->ID), $category, $excerpt, $focus])
            ];
        }
    }
    ksort($entries);
    $entries = array_values($entries);
    set_transient('a3g_dtc_catalog_v2', $entries, 10 * MINUTE_IN_SECONDS);
    return $entries;
}

function a3g_dtc_clear_catalog($post_id) {
    if (in_array(get_post_type($post_id), ['post','a3_dtc'], true)) delete_transient('a3g_dtc_catalog_v2');
}
add_action('save_post', 'a3g_dtc_clear_catalog');
add_action('deleted_post', static function() { delete_transient('a3g_dtc_catalog_v2'); });
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
        $search_js = get_template_directory() . '/assets/js/dtc-live-search.js';
        $search_css = get_template_directory() . '/assets/css/dtc-live-search.css';
        if (is_file($search_css)) wp_enqueue_style('a3g-dtc-live-search', get_template_directory_uri() . '/assets/css/dtc-live-search.css', ['a3g-dtc-library'], (string)filemtime($search_css));
        if (is_file($search_js)) {
            wp_enqueue_script('a3g-dtc-live-search', get_template_directory_uri() . '/assets/js/dtc-live-search.js', [], (string)filemtime($search_js), true);
            wp_localize_script('a3g-dtc-live-search', 'a3talDtcLookup', ['endpoint' => admin_url('admin-ajax.php')]);
        }
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
