<?php
/**
 * Plugin Name: A3tal Direct Bridge
 * Description: Secure administrator-grade REST bridge for managing A3tal.com content, SEO, media, users, plugins, themes, settings and wp-content from trusted AI clients.
 * Version: 3.1.0
 * Author: A3tal.com
 * Update URI: https://github.com/marwanile1-cyber/a3tal
 */

if (!defined('ABSPATH')) {
    exit;
}

final class A3tal_Direct_Bridge {
    const OPTION_KEY = 'a3tal_direct_bridge_api_key';
    const REDIRECTS_KEY = 'a3tal_direct_bridge_redirects';
    const BACKUPS_KEY = 'a3tal_direct_bridge_backups';
    const NS = 'a3tal-direct/v1';

    public static function init() {
        add_action('rest_api_init', [__CLASS__, 'register_routes']);
        add_action('admin_menu', [__CLASS__, 'admin_menu']);
        add_action('admin_init', [__CLASS__, 'register_settings']);
        add_action('template_redirect', [__CLASS__, 'maybe_redirect'], 0);
        add_action('wp_enqueue_scripts', [__CLASS__, 'enqueue_mobile_ux_patch'], 99);
    }

    public static function enqueue_mobile_ux_patch() {
        $css = <<<'CSS'
/* A3tal Pro mobile UX patch */
.a3-entry-content{min-width:0}
.a3-entry-content table{display:block!important;width:100%!important;max-width:100%!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;white-space:nowrap;touch-action:pan-x;overscroll-behavior-inline:contain;scrollbar-width:thin}
.a3-entry-content th,.a3-entry-content td{min-width:120px;vertical-align:top}
@media (max-width:560px){
body.search .a3-post-grid{grid-template-columns:1fr!important;gap:14px!important}
body.search .a3-post-card{display:grid!important;grid-template-columns:112px minmax(0,1fr)!important;align-items:stretch!important;min-height:112px}
body.search .a3-post-card .a3-card-thumb{width:112px!important;height:100%!important;min-height:112px;aspect-ratio:auto!important}
body.search .a3-post-card .a3-card-body{display:block!important;padding:12px 13px!important;min-width:0!important}
body.search .a3-post-card .a3-card-title,body.search .a3-post-card .a3-card-title a{display:block!important;visibility:visible!important;opacity:1!important;color:#111827!important}
body.search .a3-post-card .a3-card-title{margin:3px 0 6px!important;font-size:.98rem!important;line-height:1.5!important}
body.search .a3-post-card .a3-card-excerpt{display:-webkit-box!important;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden;margin-top:5px!important;font-size:.82rem!important}
}
@media (max-width:820px){.a3-site-header{position:relative!important;top:auto!important;backdrop-filter:none!important}.admin-bar .a3-site-header{top:auto!important}.a3-mobile-panel{top:0!important;padding-top:82px!important}.admin-bar .a3-mobile-panel{top:0!important;padding-top:128px!important}}
@media (min-width:1081px){body.home .a3-primary-nav a[href*="/choose-your-car/"]{background:linear-gradient(135deg,#ee2b1c,#ff6a3d)!important;color:#fff!important;box-shadow:0 8px 22px rgba(238,43,28,.24);padding-inline:14px!important}}
@media (max-width:1080px){
body.home .a3-site-header{margin-bottom:108px}
body.home .a3-primary-nav{display:block!important;position:absolute!important;top:68px;right:11px;left:11px;z-index:20;pointer-events:none}
body.home .a3-primary-nav>ul{display:block!important}
body.home .a3-primary-nav>ul>li{display:none!important}
body.home .a3-primary-nav>ul>li:has(>a[href*="/choose-your-car/"]){display:block!important;pointer-events:auto}
body.home .a3-primary-nav a[href*="/choose-your-car/"]{display:block!important;width:100%!important;padding:14px 16px!important;border-radius:16px!important;background:linear-gradient(135deg,#0f2742,#173f63 70%,#ee2b1c)!important;color:#fff!important;box-shadow:0 12px 30px rgba(15,39,66,.22);font-size:1.08rem!important;font-weight:900!important;text-align:center;white-space:normal!important}
body.home .a3-primary-nav a[href*="/choose-your-car/"]::before{content:"🚘 مركز سيارتك — ";color:#ffcf54}
body.home .a3-primary-nav a[href*="/choose-your-car/"]::after{content:"  • الأعطال والصيانة والزيوت وقطع الغيار";display:block;margin-top:3px;color:#d8e7f3;font-size:.76rem;font-weight:700}
}
@media (max-width:480px){body.home .a3-site-header{margin-bottom:112px}body.home .a3-primary-nav{top:64px;right:9px;left:9px}body.home .a3-primary-nav a[href*="/choose-your-car/"]{padding:13px 12px!important;font-size:1rem!important}.a3-entry-content table{font-size:.8rem!important}.a3-entry-content th,.a3-entry-content td{min-width:110px;padding:9px 10px!important}}
CSS;
        wp_register_style('a3tal-mobile-ux-patch', false, [], '3.1.0');
        wp_enqueue_style('a3tal-mobile-ux-patch');
        wp_add_inline_style('a3tal-mobile-ux-patch', $css);
    }

    public static function register_routes() {
        register_rest_route(self::NS, '/status', [
            'methods' => 'GET',
            'callback' => [__CLASS__, 'status'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/post/(?P<id>\\d+)', [
            'methods' => 'GET',
            'callback' => [__CLASS__, 'get_post'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/search-posts', [
            'methods' => 'GET',
            'callback' => [__CLASS__, 'search_posts'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/create-post', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'create_post'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/update-post', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'update_post'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/upload-image', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'upload_image'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/upload-image-data', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'upload_image_data'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/publish-bundle', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'publish_bundle'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/set-featured-image', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'set_featured_image'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/insert-images', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'insert_images'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/redirect', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'save_redirect'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/rollback-last', [
            'methods' => 'POST',
            'callback' => [__CLASS__, 'rollback_last'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);

        register_rest_route(self::NS, '/admin', [
            'methods' => ['GET', 'POST'],
            'callback' => [__CLASS__, 'admin_gateway'],
            'permission_callback' => [__CLASS__, 'authorize'],
        ]);
    }

    public static function authorize(WP_REST_Request $request) {
        $stored = (string) get_option(self::OPTION_KEY, '');
        if ($stored === '') {
            return new WP_Error('a3tal_no_key', 'A3tal Direct Bridge API key is not configured.', ['status' => 403]);
        }

        $provided = trim((string) $request->get_header('x-a3tal-key'));
        if ($provided === '') {
            $auth = trim((string) $request->get_header('authorization'));
            if (stripos($auth, 'Bearer ') === 0) {
                $provided = trim(substr($auth, 7));
            }
        }

        if ($provided === '' || !hash_equals($stored, $provided)) {
            return new WP_Error('a3tal_bad_key', 'Invalid API key.', ['status' => 403]);
        }

        return true;
    }

    public static function status() {
        return rest_ensure_response([
            'ok' => true,
            'plugin' => 'A3tal Direct Bridge',
            'version' => '3.1.0',
            'site' => home_url('/'),
            'time_gmt' => current_time('mysql', true),
            'routes' => [
                'GET /status',
                'GET /post/{id}',
                'GET /search-posts',
                'POST /create-post',
                'POST /update-post',
                'POST /upload-image',
                'POST /upload-image-data',
                'POST /publish-bundle',
                'POST /set-featured-image',
                'POST /insert-images',
                'POST /redirect',
                'POST /rollback-last',
                'GET|POST /admin?op=...',
            ],
            'admin_scope' => [
                'users_and_roles',
                'plugins_and_themes',
                'site_options_and_theme_mods',
                'taxonomies_and_menus',
                'comments_and_post_meta',
                'cache_rewrite_cron_and_updates',
                'wp_content_file_management',
            ],
            'server_root_access' => false,
        ]);
    }

    private static function yoast_meta_keys() {
        return [
            '_yoast_wpseo_focuskw',
            '_yoast_wpseo_title',
            '_yoast_wpseo_metadesc',
            '_yoast_wpseo_canonical',
            '_yoast_wpseo_opengraph-title',
            '_yoast_wpseo_opengraph-description',
            '_yoast_wpseo_twitter-title',
            '_yoast_wpseo_twitter-description',
        ];
    }

    private static function post_payload($post) {
        $meta = [];
        foreach (self::yoast_meta_keys() as $key) {
            $meta[$key] = get_post_meta($post->ID, $key, true);
        }

        return [
            'id' => $post->ID,
            'status' => $post->post_status,
            'type' => $post->post_type,
            'title' => get_the_title($post),
            'slug' => $post->post_name,
            'link' => get_permalink($post),
            'content' => $post->post_content,
            'excerpt' => $post->post_excerpt,
            'featured_media' => get_post_thumbnail_id($post->ID) ?: 0,
            'categories' => wp_get_post_categories($post->ID),
            'tags' => wp_get_post_tags($post->ID, ['fields' => 'ids']),
            'meta' => $meta,
            'modified_gmt' => get_post_modified_time('c', true, $post),
        ];
    }

    public static function get_post(WP_REST_Request $request) {
        $post = get_post((int) $request['id']);
        if (!$post) {
            return new WP_Error('a3tal_not_found', 'Post not found.', ['status' => 404]);
        }
        return rest_ensure_response(self::post_payload($post));
    }

    public static function search_posts(WP_REST_Request $request) {
        $search = sanitize_text_field((string) $request->get_param('search'));
        if ($search === '') {
            $search = sanitize_text_field((string) $request->get_param('s'));
        }

        $limit = max(1, min(100, (int) ($request->get_param('limit') ?: 20)));
        $status = sanitize_key((string) ($request->get_param('status') ?: 'any'));

        $q = new WP_Query([
            'post_type' => ['post', 'page'],
            'post_status' => $status === 'any' ? ['publish', 'draft', 'private', 'pending', 'future'] : [$status],
            's' => $search,
            'posts_per_page' => $limit,
            'orderby' => 'modified',
            'order' => 'DESC',
            'no_found_rows' => true,
        ]);

        $items = [];
        foreach ($q->posts as $post) {
            $items[] = [
                'id' => $post->ID,
                'title' => get_the_title($post),
                'status' => $post->post_status,
                'slug' => $post->post_name,
                'link' => get_permalink($post),
                'modified_gmt' => get_post_modified_time('c', true, $post),
            ];
        }

        return rest_ensure_response(['items' => $items, 'count' => count($items)]);
    }

    private static function normalize_terms($value) {
        if (!is_array($value)) {
            return [];
        }
        return array_values(array_filter(array_map('intval', $value)));
    }

    private static function save_backup($post_id) {
        $post = get_post($post_id);
        if (!$post) {
            return;
        }

        $backups = get_option(self::BACKUPS_KEY, []);
        if (!is_array($backups)) {
            $backups = [];
        }

        $backups[] = [
            'created_at' => time(),
            'post_id' => $post_id,
            'snapshot' => self::post_payload($post),
        ];

        if (count($backups) > 20) {
            $backups = array_slice($backups, -20);
        }
        update_option(self::BACKUPS_KEY, $backups, false);
    }

    private static function apply_meta($post_id, $meta) {
        if (!is_array($meta)) {
            return false;
        }

        $changed = false;
        foreach (self::yoast_meta_keys() as $key) {
            if (array_key_exists($key, $meta)) {
                update_post_meta($post_id, $key, sanitize_text_field((string) $meta[$key]));
                $changed = true;
            }
        }
        return $changed;
    }

    private static function refresh_seo_indexables($post_id, $meta_changed = false) {
        if (!$meta_changed) {
            return;
        }

        // Yoast builds its indexable presentation during post-save hooks. The
        // bridge writes SEO meta after the first wp_update_post(), so perform
        // one no-op post save after the meta write to make frontend metadata
        // immediately reflect the new values.
        if (defined('WPSEO_VERSION') || class_exists('WPSEO_Options')) {
            wp_update_post(['ID' => (int) $post_id]);
        }

        clean_post_cache((int) $post_id);
    }

    public static function create_post(WP_REST_Request $request) {
        $data = $request->get_json_params();
        $title = sanitize_text_field((string) ($data['title'] ?? ''));
        if ($title === '') {
            return new WP_Error('a3tal_title_required', 'title is required.', ['status' => 400]);
        }

        $postarr = [
            'post_type' => in_array(($data['type'] ?? 'post'), ['post', 'page'], true) ? $data['type'] : 'post',
            'post_title' => $title,
            'post_content' => wp_kses_post((string) ($data['content'] ?? '')),
            'post_excerpt' => wp_kses_post((string) ($data['excerpt'] ?? '')),
            'post_status' => in_array(($data['status'] ?? 'draft'), ['draft', 'publish', 'private', 'pending', 'future'], true) ? $data['status'] : 'draft',
        ];

        if (!empty($data['slug'])) {
            $postarr['post_name'] = sanitize_title($data['slug']);
        }

        $id = wp_insert_post($postarr, true);
        if (is_wp_error($id)) {
            return $id;
        }

        if (isset($data['categories'])) {
            wp_set_post_categories($id, self::normalize_terms($data['categories']), false);
        }
        if (isset($data['tags'])) {
            wp_set_post_tags($id, self::normalize_terms($data['tags']), false);
        }
        if (!empty($data['featured_media'])) {
            set_post_thumbnail($id, (int) $data['featured_media']);
        }
        $meta_changed = self::apply_meta($id, $data['meta'] ?? []);
        self::refresh_seo_indexables($id, $meta_changed);

        return new WP_REST_Response(self::post_payload(get_post($id)), 201);
    }

    public static function update_post(WP_REST_Request $request) {
        $data = $request->get_json_params();
        $id = (int) ($data['id'] ?? $data['post_id'] ?? 0);
        $post = get_post($id);

        if (!$post) {
            return new WP_Error('a3tal_not_found', 'Post not found.', ['status' => 404]);
        }

        self::save_backup($id);

        $update = ['ID' => $id];
        if (array_key_exists('title', $data)) {
            $update['post_title'] = sanitize_text_field((string) $data['title']);
        }
        if (array_key_exists('content', $data)) {
            $update['post_content'] = wp_kses_post((string) $data['content']);
        }
        if (array_key_exists('excerpt', $data)) {
            $update['post_excerpt'] = wp_kses_post((string) $data['excerpt']);
        }
        if (array_key_exists('slug', $data)) {
            $update['post_name'] = sanitize_title((string) $data['slug']);
        }
        if (array_key_exists('status', $data)) {
            $allowed = ['draft', 'publish', 'private', 'pending', 'future', 'trash'];
            $status = sanitize_key((string) $data['status']);
            if (!in_array($status, $allowed, true)) {
                return new WP_Error('a3tal_bad_status', 'Unsupported post status.', ['status' => 400]);
            }
            $update['post_status'] = $status;
        }

        $result = wp_update_post($update, true);
        if (is_wp_error($result)) {
            return $result;
        }

        if (isset($data['categories'])) {
            wp_set_post_categories($id, self::normalize_terms($data['categories']), false);
        }
        if (isset($data['tags'])) {
            wp_set_post_tags($id, self::normalize_terms($data['tags']), false);
        }
        if (array_key_exists('featured_media', $data)) {
            $media_id = (int) $data['featured_media'];
            $media_id ? set_post_thumbnail($id, $media_id) : delete_post_thumbnail($id);
        }
        $meta_changed = self::apply_meta($id, $data['meta'] ?? []);
        self::refresh_seo_indexables($id, $meta_changed);

        clean_post_cache($id);
        return rest_ensure_response(self::post_payload(get_post($id)));
    }


    private static function media_from_base64_payload($data, $post_id = 0) {
        if (!is_array($data)) {
            return new WP_Error('a3tal_image_payload_required', 'Image payload is required.', ['status' => 400]);
        }

        $raw = (string) ($data['image_base64'] ?? $data['base64'] ?? $data['data'] ?? '');
        if ($raw === '') {
            return new WP_Error('a3tal_image_data_required', 'image_base64 is required.', ['status' => 400]);
        }

        $declared_mime = '';
        if (preg_match('#^data:(image/[a-z0-9.+-]+);base64,(.+)$#is', $raw, $m)) {
            $declared_mime = strtolower(trim($m[1]));
            $raw = $m[2];
        }

        $raw = preg_replace('/\s+/', '', $raw);
        $bytes = base64_decode($raw, true);
        if ($bytes === false || $bytes === '') {
            return new WP_Error('a3tal_bad_image_base64', 'Invalid base64 image payload.', ['status' => 400]);
        }

        $max_bytes = 20 * 1024 * 1024;
        if (strlen($bytes) > $max_bytes) {
            return new WP_Error('a3tal_image_too_large', 'Decoded image exceeds the 20 MB bridge limit.', ['status' => 413]);
        }

        $info = @getimagesizefromstring($bytes);
        if (!$info || empty($info['mime'])) {
            return new WP_Error('a3tal_not_image', 'Decoded payload is not a valid image.', ['status' => 400]);
        }

        $mime = strtolower((string) $info['mime']);
        $allowed = [
            'image/jpeg' => 'jpg',
            'image/png'  => 'png',
            'image/webp' => 'webp',
            'image/gif'  => 'gif',
        ];
        if (!isset($allowed[$mime])) {
            return new WP_Error('a3tal_image_type_blocked', 'Only JPEG, PNG, WEBP and GIF images are allowed.', ['status' => 415]);
        }
        if ($declared_mime !== '' && $declared_mime !== $mime) {
            return new WP_Error('a3tal_image_mime_mismatch', 'Declared image MIME does not match decoded image.', ['status' => 400]);
        }

        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/media.php';
        require_once ABSPATH . 'wp-admin/includes/image.php';

        $base_name = sanitize_file_name((string) ($data['filename'] ?? ('a3tal-image.' . $allowed[$mime])));
        if ($base_name === '') {
            $base_name = 'a3tal-image.' . $allowed[$mime];
        }

        $tmp = wp_tempnam($base_name);
        if (!$tmp || file_put_contents($tmp, $bytes, LOCK_EX) === false) {
            if ($tmp) {
                @unlink($tmp);
            }
            return new WP_Error('a3tal_temp_write_failed', 'Could not create temporary image file.', ['status' => 500]);
        }

        $convert_webp = !array_key_exists('convert_webp', $data) || !empty($data['convert_webp']);
        $quality = max(45, min(95, (int) ($data['quality'] ?? 84)));
        $max_width = max(0, (int) ($data['max_width'] ?? 0));
        $max_height = max(0, (int) ($data['max_height'] ?? 0));

        $final_tmp = $tmp;
        $final_name = $base_name;
        $final_mime = $mime;

        if ($convert_webp || $max_width || $max_height) {
            $editor = wp_get_image_editor($tmp);
            if (!is_wp_error($editor)) {
                if ($max_width || $max_height) {
                    $size = $editor->get_size();
                    $target_w = $max_width ?: (int) ($size['width'] ?? 0);
                    $target_h = $max_height ?: (int) ($size['height'] ?? 0);
                    if ($target_w > 0 && $target_h > 0) {
                        $editor->resize($target_w, $target_h, false);
                    }
                }
                $editor->set_quality($quality);

                if ($convert_webp) {
                    $webp_tmp = wp_tempnam(pathinfo($base_name, PATHINFO_FILENAME) . '.webp');
                    $saved = $editor->save($webp_tmp, 'image/webp');
                    if (!is_wp_error($saved) && !empty($saved['path'])) {
                        $final_tmp = $saved['path'];
                        $final_name = sanitize_file_name(pathinfo($base_name, PATHINFO_FILENAME) . '.webp');
                        $final_mime = 'image/webp';
                        if ($final_tmp !== $tmp) {
                            @unlink($tmp);
                        }
                    }
                } elseif ($max_width || $max_height) {
                    $resized_tmp = wp_tempnam($base_name);
                    $saved = $editor->save($resized_tmp, $mime);
                    if (!is_wp_error($saved) && !empty($saved['path'])) {
                        $final_tmp = $saved['path'];
                        if ($final_tmp !== $tmp) {
                            @unlink($tmp);
                        }
                    }
                }
            }
        }

        $file = [
            'name' => $final_name,
            'tmp_name' => $final_tmp,
            'type' => $final_mime,
            'error' => 0,
            'size' => @filesize($final_tmp),
        ];

        $media_id = media_handle_sideload(
            $file,
            (int) $post_id,
            sanitize_text_field((string) ($data['title'] ?? ''))
        );

        if (is_wp_error($media_id)) {
            @unlink($final_tmp);
            return $media_id;
        }

        if (!empty($data['alt'])) {
            update_post_meta($media_id, '_wp_attachment_image_alt', sanitize_text_field((string) $data['alt']));
        }
        if (!empty($data['caption'])) {
            wp_update_post([
                'ID' => $media_id,
                'post_excerpt' => sanitize_text_field((string) $data['caption']),
            ]);
        }

        if (!empty($data['set_featured']) && $post_id) {
            set_post_thumbnail((int) $post_id, $media_id);
        }

        $src = wp_get_attachment_image_src($media_id, 'full');
        return [
            'media_id' => $media_id,
            'url' => $src ? $src[0] : wp_get_attachment_url($media_id),
            'width' => $src ? (int) $src[1] : null,
            'height' => $src ? (int) $src[2] : null,
            'mime' => get_post_mime_type($media_id),
            'filesize' => get_attached_file($media_id) && file_exists(get_attached_file($media_id)) ? filesize(get_attached_file($media_id)) : null,
            'featured_for_post' => (!empty($data['set_featured']) && $post_id) ? (int) $post_id : 0,
        ];
    }

    public static function upload_image_data(WP_REST_Request $request) {
        $data = $request->get_json_params();
        $post_id = (int) ($data['post_id'] ?? 0);

        if ($post_id && !get_post($post_id)) {
            return new WP_Error('a3tal_bad_post', 'post_id does not exist.', ['status' => 404]);
        }

        $result = self::media_from_base64_payload($data, $post_id);
        if (is_wp_error($result)) {
            return $result;
        }

        return new WP_REST_Response($result, 201);
    }

    private static function bundle_image_html($media, $alt = '', $caption = '') {
        $url = esc_url((string) ($media['url'] ?? ''));
        if ($url === '') {
            return '';
        }

        $html = '<figure class="wp-block-image size-full">';
        $html .= '<img src="' . $url . '" alt="' . esc_attr((string) $alt) . '" loading="lazy" decoding="async">';
        if ((string) $caption !== '') {
            $html .= '<figcaption>' . esc_html((string) $caption) . '</figcaption>';
        }
        $html .= '</figure>';
        return $html;
    }

    public static function publish_bundle(WP_REST_Request $request) {
        $data = $request->get_json_params();
        if (!is_array($data)) {
            return new WP_Error('a3tal_bundle_required', 'JSON bundle payload is required.', ['status' => 400]);
        }

        $post_data = $data['post'] ?? [];
        if (!is_array($post_data)) {
            return new WP_Error('a3tal_post_payload_required', 'post object is required.', ['status' => 400]);
        }

        $post_id = (int) ($post_data['id'] ?? $post_data['post_id'] ?? 0);
        $is_new = !$post_id;

        if ($is_new) {
            $title = sanitize_text_field((string) ($post_data['title'] ?? ''));
            if ($title === '') {
                return new WP_Error('a3tal_title_required', 'post.title is required.', ['status' => 400]);
            }

            $postarr = [
                'post_type' => in_array(($post_data['type'] ?? 'post'), ['post', 'page'], true) ? $post_data['type'] : 'post',
                'post_title' => $title,
                'post_content' => wp_kses_post((string) ($post_data['content'] ?? '')),
                'post_excerpt' => wp_kses_post((string) ($post_data['excerpt'] ?? '')),
                'post_status' => 'draft',
            ];
            if (!empty($post_data['slug'])) {
                $postarr['post_name'] = sanitize_title((string) $post_data['slug']);
            }

            $post_id = wp_insert_post($postarr, true);
            if (is_wp_error($post_id)) {
                return $post_id;
            }
        } else {
            $post = get_post($post_id);
            if (!$post) {
                return new WP_Error('a3tal_not_found', 'Target post not found.', ['status' => 404]);
            }
            self::save_backup($post_id);

            $update = ['ID' => $post_id, 'post_status' => 'draft'];
            if (array_key_exists('title', $post_data)) {
                $update['post_title'] = sanitize_text_field((string) $post_data['title']);
            }
            if (array_key_exists('content', $post_data)) {
                $update['post_content'] = wp_kses_post((string) $post_data['content']);
            }
            if (array_key_exists('excerpt', $post_data)) {
                $update['post_excerpt'] = wp_kses_post((string) $post_data['excerpt']);
            }
            if (array_key_exists('slug', $post_data)) {
                $update['post_name'] = sanitize_title((string) $post_data['slug']);
            }
            $updated = wp_update_post($update, true);
            if (is_wp_error($updated)) {
                return $updated;
            }
        }

        if (isset($post_data['categories'])) {
            wp_set_post_categories($post_id, self::normalize_terms($post_data['categories']), false);
        }
        if (isset($post_data['tags'])) {
            wp_set_post_tags($post_id, self::normalize_terms($post_data['tags']), false);
        }
        $meta_changed = self::apply_meta($post_id, $post_data['meta'] ?? []);

        $content = get_post_field('post_content', $post_id);
        $media_results = [];
        $media_items = $data['media'] ?? [];
        if (!is_array($media_items)) {
            $media_items = [];
        }

        foreach ($media_items as $index => $item) {
            if (!is_array($item)) {
                continue;
            }

            $item['post_id'] = $post_id;
            $media = self::media_from_base64_payload($item, $post_id);
            if (is_wp_error($media)) {
                wp_update_post(['ID' => $post_id, 'post_status' => 'draft']);
                return new WP_Error(
                    'a3tal_bundle_media_failed',
                    'Media item ' . ($index + 1) . ' failed: ' . $media->get_error_message(),
                    ['status' => 400, 'post_id' => $post_id]
                );
            }

            $key = sanitize_key((string) ($item['key'] ?? ('image_' . ($index + 1))));
            $media_results[$key] = $media;

            $role = sanitize_key((string) ($item['role'] ?? 'inline'));
            if ($role === 'featured' || !empty($item['set_featured'])) {
                set_post_thumbnail($post_id, (int) $media['media_id']);
            }

            if ($role !== 'featured') {
                $placeholder = (string) ($item['placeholder'] ?? ('{{a3tal_image:' . $key . '}}'));
                $html = self::bundle_image_html(
                    $media,
                    (string) ($item['alt'] ?? ''),
                    (string) ($item['caption'] ?? '')
                );

                if ($placeholder !== '' && strpos($content, $placeholder) !== false) {
                    $content = str_replace($placeholder, $html, $content);
                } elseif (!empty($item['append_if_missing'])) {
                    $content .= "\n" . $html;
                }
            }
        }

        $final_status = sanitize_key((string) ($post_data['status'] ?? ($data['status'] ?? 'publish')));
        if (!in_array($final_status, ['draft', 'publish', 'private', 'pending', 'future'], true)) {
            $final_status = 'publish';
        }

        $final = wp_update_post([
            'ID' => $post_id,
            'post_content' => wp_kses_post($content),
            'post_status' => $final_status,
        ], true);
        if (is_wp_error($final)) {
            return $final;
        }

        self::refresh_seo_indexables($post_id, $meta_changed);
        clean_post_cache($post_id);

        return rest_ensure_response([
            'ok' => true,
            'post' => self::post_payload(get_post($post_id)),
            'media' => $media_results,
        ]);
    }

    public static function upload_image(WP_REST_Request $request) {
        $data = $request->get_json_params();
        $url = esc_url_raw((string) ($data['image_url'] ?? $data['url'] ?? ''));
        if ($url === '') {
            return new WP_Error('a3tal_url_required', 'image_url is required.', ['status' => 400]);
        }

        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/media.php';
        require_once ABSPATH . 'wp-admin/includes/image.php';

        $post_id = (int) ($data['post_id'] ?? 0);
        $tmp = download_url($url, 60);
        if (is_wp_error($tmp)) {
            return $tmp;
        }

        $path = (string) parse_url($url, PHP_URL_PATH);
        $name = sanitize_file_name((string) ($data['filename'] ?? basename($path)));
        if ($name === '') {
            $name = 'a3tal-image.jpg';
        }

        $file = ['name' => $name, 'tmp_name' => $tmp];
        $media_id = media_handle_sideload($file, $post_id, sanitize_text_field((string) ($data['title'] ?? '')));
        if (is_wp_error($media_id)) {
            @unlink($tmp);
            return $media_id;
        }

        if (!empty($data['alt'])) {
            update_post_meta($media_id, '_wp_attachment_image_alt', sanitize_text_field((string) $data['alt']));
        }

        if (!empty($data['set_featured']) && $post_id) {
            set_post_thumbnail($post_id, $media_id);
        }

        $src = wp_get_attachment_image_src($media_id, 'full');
        return new WP_REST_Response([
            'media_id' => $media_id,
            'url' => $src ? $src[0] : wp_get_attachment_url($media_id),
            'width' => $src ? (int) $src[1] : null,
            'height' => $src ? (int) $src[2] : null,
            'featured_for_post' => (!empty($data['set_featured']) && $post_id) ? $post_id : 0,
        ], 201);
    }

    public static function set_featured_image(WP_REST_Request $request) {
        $data = $request->get_json_params();
        $post_id = (int) ($data['post_id'] ?? 0);
        $media_id = (int) ($data['media_id'] ?? 0);

        if (!get_post($post_id) || !wp_attachment_is_image($media_id)) {
            return new WP_Error('a3tal_bad_ids', 'Valid post_id and image media_id are required.', ['status' => 400]);
        }

        set_post_thumbnail($post_id, $media_id);
        return rest_ensure_response([
            'ok' => true,
            'post_id' => $post_id,
            'featured_media' => get_post_thumbnail_id($post_id),
        ]);
    }

    public static function insert_images(WP_REST_Request $request) {
        $data = $request->get_json_params();
        $post_id = (int) ($data['post_id'] ?? 0);
        $post = get_post($post_id);
        if (!$post) {
            return new WP_Error('a3tal_not_found', 'Post not found.', ['status' => 404]);
        }

        $images = $data['images'] ?? [];
        if (!is_array($images) || !$images) {
            return new WP_Error('a3tal_images_required', 'images array is required.', ['status' => 400]);
        }

        self::save_backup($post_id);
        $content = $post->post_content;

        foreach ($images as $image) {
            if (!is_array($image) || empty($image['url'])) {
                continue;
            }

            $url = esc_url((string) $image['url']);
            $alt = esc_attr((string) ($image['alt'] ?? ''));
            $caption = sanitize_text_field((string) ($image['caption'] ?? ''));
            $html = '<figure class="wp-block-image size-full"><img src="' . $url . '" alt="' . $alt . '" loading="lazy">';
            if ($caption !== '') {
                $html .= '<figcaption>' . esc_html($caption) . '</figcaption>';
            }
            $html .= '</figure>';

            $before = (string) ($image['before'] ?? '');
            $after = (string) ($image['after'] ?? '');

            if ($before !== '' && strpos($content, $before) !== false) {
                $content = str_replace($before, $html . $before, $content);
            } elseif ($after !== '' && strpos($content, $after) !== false) {
                $content = str_replace($after, $after . $html, $content);
            } else {
                $content .= $html;
            }
        }

        $result = wp_update_post(['ID' => $post_id, 'post_content' => $content], true);
        if (is_wp_error($result)) {
            return $result;
        }

        return rest_ensure_response(self::post_payload(get_post($post_id)));
    }

    public static function save_redirect(WP_REST_Request $request) {
        $data = $request->get_json_params();
        $source = '/' . ltrim((string) ($data['source_path'] ?? ''), '/');
        $source = trailingslashit(wp_parse_url(home_url($source), PHP_URL_PATH));
        $target = esc_url_raw((string) ($data['target_url'] ?? ''));
        $code = (int) ($data['status_code'] ?? 301);

        if ($source === '/' || $target === '' || !in_array($code, [301, 302, 307, 308], true)) {
            return new WP_Error('a3tal_bad_redirect', 'Valid source_path, target_url and redirect status are required.', ['status' => 400]);
        }

        $redirects = get_option(self::REDIRECTS_KEY, []);
        if (!is_array($redirects)) {
            $redirects = [];
        }
        $redirects[$source] = ['target' => $target, 'code' => $code];
        update_option(self::REDIRECTS_KEY, $redirects, false);

        return rest_ensure_response(['ok' => true, 'source_path' => $source, 'target_url' => $target, 'status_code' => $code]);
    }

    public static function maybe_redirect() {
        if (is_admin() || wp_doing_ajax() || (defined('REST_REQUEST') && REST_REQUEST)) {
            return;
        }

        $redirects = get_option(self::REDIRECTS_KEY, []);
        if (!is_array($redirects) || !$redirects) {
            return;
        }

        $path = wp_parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
        $path = trailingslashit('/' . ltrim((string) $path, '/'));

        if (isset($redirects[$path])) {
            $item = $redirects[$path];
            wp_safe_redirect($item['target'], (int) $item['code'], 'A3tal Direct Bridge');
            exit;
        }
    }

    public static function rollback_last(WP_REST_Request $request) {
        $data = $request->get_json_params();
        $requested_post_id = (int) ($data['post_id'] ?? 0);
        $backups = get_option(self::BACKUPS_KEY, []);

        if (!is_array($backups) || !$backups) {
            return new WP_Error('a3tal_no_backup', 'No rollback snapshot is available.', ['status' => 404]);
        }

        $index = null;
        for ($i = count($backups) - 1; $i >= 0; $i--) {
            if (!$requested_post_id || (int) $backups[$i]['post_id'] === $requested_post_id) {
                $index = $i;
                break;
            }
        }

        if ($index === null) {
            return new WP_Error('a3tal_no_backup', 'No rollback snapshot found for this post.', ['status' => 404]);
        }

        $entry = $backups[$index];
        $s = $entry['snapshot'];
        $id = (int) $entry['post_id'];

        $result = wp_update_post([
            'ID' => $id,
            'post_title' => $s['title'],
            'post_content' => $s['content'],
            'post_excerpt' => $s['excerpt'],
            'post_status' => $s['status'],
            'post_name' => $s['slug'],
        ], true);

        if (is_wp_error($result)) {
            return $result;
        }

        wp_set_post_categories($id, $s['categories'] ?? [], false);
        wp_set_post_tags($id, $s['tags'] ?? [], false);

        if (!empty($s['featured_media'])) {
            set_post_thumbnail($id, (int) $s['featured_media']);
        } else {
            delete_post_thumbnail($id);
        }

        $meta_changed = self::apply_meta($id, $s['meta'] ?? []);
        self::refresh_seo_indexables($id, $meta_changed);
        array_splice($backups, $index, 1);
        update_option(self::BACKUPS_KEY, $backups, false);

        return rest_ensure_response(['ok' => true, 'restored' => self::post_payload(get_post($id))]);
    }



    private static function admin_read_ops() {
        return [
            'site_info', 'plugins', 'themes', 'users', 'roles', 'options',
            'terms', 'menus', 'comments', 'updates', 'cron', 'file_read',
            'file_list', 'post_meta', 'audit_log', 'theme_mods'
        ];
    }

    private static function admin_is_read_op($op) {
        return in_array($op, self::admin_read_ops(), true);
    }

    private static function admin_confirm($data, $dangerous = false) {
        $ok = !empty($data['confirm']);
        if ($dangerous) {
            $ok = $ok && !empty($data['dangerous']);
        }
        if (!$ok) {
            return new WP_Error(
                'a3tal_confirmation_required',
                $dangerous ? 'confirm=true and dangerous=true are required for this operation.' : 'confirm=true is required for this operation.',
                ['status' => 400]
            );
        }
        return true;
    }

    private static function admin_audit($op, $ok, $note = '') {
        $key = 'a3tal_direct_bridge_admin_audit';
        $log = get_option($key, []);
        if (!is_array($log)) {
            $log = [];
        }

        $log[] = [
            'time_gmt' => current_time('mysql', true),
            'op' => sanitize_key((string) $op),
            'ok' => (bool) $ok,
            'note' => sanitize_text_field((string) $note),
            'ip_hash' => hash('sha256', (string) ($_SERVER['REMOTE_ADDR'] ?? '')),
        ];

        if (count($log) > 200) {
            $log = array_slice($log, -200);
        }
        update_option($key, $log, false);
    }

    private static function admin_result($op, $result) {
        return rest_ensure_response([
            'ok' => true,
            'op' => $op,
            'result' => $result,
        ]);
    }

    private static function admin_sensitive_option($key) {
        return (bool) preg_match(
            '/(?:pass(?:word)?|secret|token|salt|license|api[_-]?key|private[_-]?key|authorization|(?:^|[_-])auth(?:$|[_-]))/i',
            (string) $key
        );
    }

    private static function admin_redact_sensitive($value) {
        if (is_array($value)) {
            $out = [];
            foreach ($value as $key => $item) {
                if (is_string($key) && self::admin_sensitive_option($key)) {
                    $out[$key] = '[REDACTED]';
                } else {
                    $out[$key] = self::admin_redact_sensitive($item);
                }
            }
            return $out;
        }

        if (is_object($value)) {
            $copy = new stdClass();
            foreach (get_object_vars($value) as $key => $item) {
                if (self::admin_sensitive_option($key)) {
                    $copy->{$key} = '[REDACTED]';
                } else {
                    $copy->{$key} = self::admin_redact_sensitive($item);
                }
            }
            return $copy;
        }

        return $value;
    }

    private static function admin_protected_option($key) {
        return in_array((string) $key, [
            self::OPTION_KEY,
            'active_plugins',
            'template',
            'stylesheet',
        ], true);
    }

    private static function admin_content_path($relative, $must_exist = false) {
        $relative = str_replace('\\', '/', (string) $relative);
        $relative = ltrim($relative, '/');

        if ($relative === '' || strpos($relative, "\0") !== false || preg_match('#(^|/)\.\.(/|$)#', $relative)) {
            return new WP_Error('a3tal_bad_path', 'A safe path relative to wp-content is required.', ['status' => 400]);
        }

        $base = wp_normalize_path(WP_CONTENT_DIR);
        $candidate = wp_normalize_path($base . '/' . $relative);

        if (strpos($candidate . '/', trailingslashit($base)) !== 0) {
            return new WP_Error('a3tal_bad_path', 'Path must stay inside wp-content.', ['status' => 400]);
        }

        if ($must_exist) {
            $real = realpath($candidate);
            if ($real === false) {
                return new WP_Error('a3tal_file_missing', 'File or directory not found.', ['status' => 404]);
            }
            $real = wp_normalize_path($real);
            if (strpos($real . '/', trailingslashit($base)) !== 0) {
                return new WP_Error('a3tal_bad_path', 'Resolved path escapes wp-content.', ['status' => 400]);
            }
            return $real;
        }

        $parent = realpath(dirname($candidate));
        if ($parent === false) {
            return new WP_Error('a3tal_parent_missing', 'Parent directory does not exist.', ['status' => 400]);
        }
        $parent = wp_normalize_path($parent);
        if (strpos($parent . '/', trailingslashit($base)) !== 0) {
            return new WP_Error('a3tal_bad_path', 'Resolved parent escapes wp-content.', ['status' => 400]);
        }

        return $candidate;
    }

    private static function admin_text_extension_allowed($path) {
        $ext = strtolower((string) pathinfo($path, PATHINFO_EXTENSION));
        return in_array($ext, [
            'php', 'css', 'js', 'json', 'html', 'htm', 'txt', 'md',
            'xml', 'svg', 'yml', 'yaml', 'po', 'pot'
        ], true);
    }

    private static function admin_load_plugin_libs() {
        require_once ABSPATH . 'wp-admin/includes/plugin.php';
        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
        require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
    }

    private static function admin_load_theme_libs() {
        require_once ABSPATH . 'wp-admin/includes/theme.php';
        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
        require_once ABSPATH . 'wp-admin/includes/theme-install.php';
    }

    private static function admin_plugins() {
        self::admin_load_plugin_libs();
        $all = get_plugins();
        $items = [];
        foreach ($all as $file => $p) {
            $items[] = [
                'file' => $file,
                'name' => $p['Name'] ?? '',
                'version' => $p['Version'] ?? '',
                'author' => wp_strip_all_tags($p['Author'] ?? ''),
                'active' => is_plugin_active($file),
                'network_active' => is_multisite() ? is_plugin_active_for_network($file) : false,
            ];
        }
        return $items;
    }

    private static function admin_themes() {
        $active = get_stylesheet();
        $items = [];
        foreach (wp_get_themes() as $slug => $theme) {
            $items[] = [
                'stylesheet' => $slug,
                'name' => $theme->get('Name'),
                'version' => $theme->get('Version'),
                'author' => wp_strip_all_tags($theme->get('Author')),
                'active' => ($slug === $active),
                'parent' => $theme->parent() ? $theme->parent()->get_stylesheet() : null,
            ];
        }
        return $items;
    }

    private static function admin_users($data) {
        $limit = max(1, min(200, (int) ($data['limit'] ?? 100)));
        $users = get_users([
            'number' => $limit,
            'orderby' => 'ID',
            'order' => 'ASC',
        ]);
        $items = [];
        foreach ($users as $u) {
            $items[] = [
                'id' => $u->ID,
                'login' => $u->user_login,
                'display_name' => $u->display_name,
                'email' => $u->user_email,
                'roles' => array_values((array) $u->roles),
                'registered' => $u->user_registered,
            ];
        }
        return $items;
    }

    private static function admin_roles() {
        $roles = wp_roles();
        $out = [];
        foreach ($roles->roles as $slug => $role) {
            $caps = [];
            foreach ((array) ($role['capabilities'] ?? []) as $cap => $enabled) {
                if ($enabled) {
                    $caps[] = $cap;
                }
            }
            $out[$slug] = [
                'name' => $role['name'] ?? $slug,
                'capabilities' => $caps,
            ];
        }
        return $out;
    }

    private static function admin_options($data) {
        $keys = $data['keys'] ?? [];
        if (is_string($keys)) {
            $keys = array_filter(array_map('trim', explode(',', $keys)));
        }
        if (!is_array($keys) || !$keys) {
            return new WP_Error('a3tal_option_keys_required', 'keys array is required.', ['status' => 400]);
        }

        $out = [];
        foreach (array_slice($keys, 0, 100) as $key) {
            $key = sanitize_text_field((string) $key);
            if ($key === '' || $key === self::OPTION_KEY || self::admin_sensitive_option($key)) {
                $out[$key] = '[REDACTED]';
                continue;
            }
            $out[$key] = self::admin_redact_sensitive(get_option($key, null));
        }
        return $out;
    }

    private static function admin_terms($data) {
        $taxonomy = sanitize_key((string) ($data['taxonomy'] ?? 'category'));
        if (!taxonomy_exists($taxonomy)) {
            return new WP_Error('a3tal_bad_taxonomy', 'Taxonomy does not exist.', ['status' => 400]);
        }
        $terms = get_terms([
            'taxonomy' => $taxonomy,
            'hide_empty' => false,
            'number' => max(1, min(500, (int) ($data['limit'] ?? 200))),
        ]);
        if (is_wp_error($terms)) {
            return $terms;
        }
        return array_map(static function ($term) {
            return [
                'id' => $term->term_id,
                'name' => $term->name,
                'slug' => $term->slug,
                'parent' => $term->parent,
                'count' => $term->count,
                'description' => $term->description,
            ];
        }, $terms);
    }

    private static function admin_menus() {
        $menus = [];
        foreach (wp_get_nav_menus() as $menu) {
            $items = wp_get_nav_menu_items($menu->term_id);
            $menus[] = [
                'id' => $menu->term_id,
                'name' => $menu->name,
                'slug' => $menu->slug,
                'items' => array_map(static function ($item) {
                    return [
                        'id' => $item->ID,
                        'title' => $item->title,
                        'url' => $item->url,
                        'type' => $item->type,
                        'object' => $item->object,
                        'object_id' => (int) $item->object_id,
                        'parent' => (int) $item->menu_item_parent,
                        'order' => (int) $item->menu_order,
                    ];
                }, is_array($items) ? $items : []),
            ];
        }
        return [
            'locations' => get_nav_menu_locations(),
            'menus' => $menus,
        ];
    }

    private static function admin_comments($data) {
        $comments = get_comments([
            'number' => max(1, min(200, (int) ($data['limit'] ?? 50))),
            'status' => sanitize_key((string) ($data['status'] ?? 'all')),
            'post_id' => (int) ($data['post_id'] ?? 0),
            'orderby' => 'comment_ID',
            'order' => 'DESC',
        ]);
        return array_map(static function ($comment) {
            return [
                'id' => (int) $comment->comment_ID,
                'post_id' => (int) $comment->comment_post_ID,
                'author' => $comment->comment_author,
                'email' => $comment->comment_author_email,
                'content' => $comment->comment_content,
                'approved' => $comment->comment_approved,
                'date_gmt' => $comment->comment_date_gmt,
            ];
        }, $comments);
    }

    private static function admin_updates() {
        require_once ABSPATH . 'wp-admin/includes/update.php';
        wp_version_check();
        wp_update_plugins();
        wp_update_themes();

        $plugin_updates = get_site_transient('update_plugins');
        $theme_updates = get_site_transient('update_themes');
        $core_updates = get_core_updates(['dismissed' => false]);

        return [
            'core' => is_array($core_updates) ? array_map(static function ($u) {
                return [
                    'current' => $u->current ?? null,
                    'response' => $u->response ?? null,
                    'locale' => $u->locale ?? null,
                ];
            }, $core_updates) : [],
            'plugins' => isset($plugin_updates->response) ? array_keys((array) $plugin_updates->response) : [],
            'themes' => isset($theme_updates->response) ? array_keys((array) $theme_updates->response) : [],
        ];
    }

    private static function admin_cron($data) {
        $crons = _get_cron_array();
        $limit = max(1, min(500, (int) ($data['limit'] ?? 200)));
        $items = [];
        foreach ((array) $crons as $timestamp => $hooks) {
            foreach ((array) $hooks as $hook => $events) {
                foreach ((array) $events as $sig => $event) {
                    $items[] = [
                        'timestamp' => (int) $timestamp,
                        'hook' => $hook,
                        'schedule' => $event['schedule'] ?? false,
                        'interval' => $event['interval'] ?? null,
                    ];
                    if (count($items) >= $limit) {
                        break 3;
                    }
                }
            }
        }
        return $items;
    }

    private static function admin_file_read($data) {
        $path = self::admin_content_path($data['path'] ?? '', true);
        if (is_wp_error($path)) {
            return $path;
        }
        if (!is_file($path) || !self::admin_text_extension_allowed($path)) {
            return new WP_Error('a3tal_file_not_text', 'Only approved text/code files inside wp-content can be read.', ['status' => 400]);
        }
        $size = filesize($path);
        if ($size !== false && $size > 1048576) {
            return new WP_Error('a3tal_file_too_large', 'File exceeds 1 MB read limit.', ['status' => 413]);
        }
        $base = trailingslashit(wp_normalize_path(WP_CONTENT_DIR));
        return [
            'path' => ltrim(str_replace($base, '', wp_normalize_path($path)), '/'),
            'size' => $size,
            'sha256' => hash_file('sha256', $path),
            'content' => file_get_contents($path),
        ];
    }

    private static function admin_file_list($data) {
        $relative = trim((string) ($data['path'] ?? ''), '/');
        if ($relative === '') {
            $dir = wp_normalize_path(WP_CONTENT_DIR);
        } else {
            $dir = self::admin_content_path($relative, true);
            if (is_wp_error($dir)) {
                return $dir;
            }
        }
        if (!is_dir($dir)) {
            return new WP_Error('a3tal_not_directory', 'Path is not a directory.', ['status' => 400]);
        }
        $items = [];
        foreach (array_slice(scandir($dir) ?: [], 0, 500) as $name) {
            if ($name === '.' || $name === '..') {
                continue;
            }
            $full = wp_normalize_path($dir . '/' . $name);
            $items[] = [
                'name' => $name,
                'type' => is_dir($full) ? 'dir' : 'file',
                'size' => is_file($full) ? filesize($full) : null,
            ];
        }
        return $items;
    }

    private static function admin_post_meta($data) {
        $post_id = (int) ($data['post_id'] ?? 0);
        if (!$post_id || !get_post($post_id)) {
            return new WP_Error('a3tal_bad_post', 'Valid post_id is required.', ['status' => 400]);
        }
        $key = (string) ($data['key'] ?? '');
        if ($key !== '') {
            return [$key => get_post_meta($post_id, $key, true)];
        }
        return get_post_meta($post_id);
    }

    private static function admin_theme_mods() {
        return get_theme_mods();
    }

    private static function admin_site_info() {
        global $wp_version;
        return [
            'home' => home_url('/'),
            'site_url' => site_url('/'),
            'wordpress_version' => $wp_version,
            'php_version' => PHP_VERSION,
            'multisite' => is_multisite(),
            'active_theme' => get_stylesheet(),
            'parent_theme' => get_template(),
            'plugin_file' => plugin_basename(__FILE__),
            'wp_content_dir' => basename(WP_CONTENT_DIR),
            'permalink_structure' => get_option('permalink_structure'),
            'timezone_string' => get_option('timezone_string'),
            'debug' => defined('WP_DEBUG') && WP_DEBUG,
            'disable_file_edit' => defined('DISALLOW_FILE_EDIT') && DISALLOW_FILE_EDIT,
            'disable_file_mods' => defined('DISALLOW_FILE_MODS') && DISALLOW_FILE_MODS,
            'cron_disabled' => defined('DISABLE_WP_CRON') && DISABLE_WP_CRON,
        ];
    }

    private static function admin_write_option($data) {
        $options = $data['options'] ?? [];
        if (!is_array($options) || !$options) {
            return new WP_Error('a3tal_options_required', 'options object is required.', ['status' => 400]);
        }
        $changed = [];
        foreach ($options as $key => $value) {
            $key = sanitize_text_field((string) $key);
            if ($key === '' || $key === self::OPTION_KEY) {
                return new WP_Error('a3tal_protected_option', 'The bridge authentication option cannot be changed through the API.', ['status' => 403]);
            }
            if (self::admin_protected_option($key)) {
                $confirm = self::admin_confirm($data, true);
                if (is_wp_error($confirm)) {
                    return $confirm;
                }
            }
            update_option($key, $value);
            $changed[] = $key;
        }
        return ['updated' => $changed];
    }

    private static function admin_delete_option($data) {
        $keys = $data['keys'] ?? [];
        if (is_string($keys)) {
            $keys = array_filter(array_map('trim', explode(',', $keys)));
        }
        if (!is_array($keys) || !$keys) {
            return new WP_Error('a3tal_option_keys_required', 'keys array is required.', ['status' => 400]);
        }
        $deleted = [];
        foreach ($keys as $key) {
            $key = sanitize_text_field((string) $key);
            if ($key === '' || $key === self::OPTION_KEY || self::admin_protected_option($key)) {
                return new WP_Error('a3tal_protected_option', 'Protected options cannot be deleted through the API.', ['status' => 403]);
            }
            delete_option($key);
            $deleted[] = $key;
        }
        return ['deleted' => $deleted];
    }

    private static function admin_user_upsert($data) {
        require_once ABSPATH . 'wp-admin/includes/user.php';
        $id = (int) ($data['id'] ?? 0);
        $payload = [];

        if ($id) {
            $payload['ID'] = $id;
            if (!get_user_by('id', $id)) {
                return new WP_Error('a3tal_user_missing', 'User not found.', ['status' => 404]);
            }
        } else {
            $login = sanitize_user((string) ($data['login'] ?? ''), true);
            $email = sanitize_email((string) ($data['email'] ?? ''));
            if ($login === '' || $email === '') {
                return new WP_Error('a3tal_user_fields_required', 'login and email are required for a new user.', ['status' => 400]);
            }
            $payload['user_login'] = $login;
            $payload['user_email'] = $email;
            $payload['user_pass'] = wp_generate_password(32, true, true);
        }

        foreach (['email' => 'user_email', 'display_name' => 'display_name', 'first_name' => 'first_name', 'last_name' => 'last_name'] as $src => $dst) {
            if (array_key_exists($src, $data)) {
                $payload[$dst] = sanitize_text_field((string) $data[$src]);
            }
        }

        if (!empty($data['password'])) {
            $payload['user_pass'] = (string) $data['password'];
        }

        if (!empty($data['role'])) {
            $role = sanitize_key((string) $data['role']);
            if (!get_role($role)) {
                return new WP_Error('a3tal_bad_role', 'Role does not exist.', ['status' => 400]);
            }
            $payload['role'] = $role;
        }

        $user_id = wp_insert_user($payload);
        if (is_wp_error($user_id)) {
            return $user_id;
        }

        if (!$id && !empty($data['send_reset_link'])) {
            $user = get_user_by('id', $user_id);
            if ($user) {
                retrieve_password($user->user_login);
            }
        }

        $user = get_user_by('id', $user_id);
        return [
            'id' => $user_id,
            'login' => $user->user_login,
            'email' => $user->user_email,
            'roles' => array_values((array) $user->roles),
        ];
    }

    private static function admin_user_delete($data) {
        $confirm = self::admin_confirm($data, true);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        require_once ABSPATH . 'wp-admin/includes/user.php';
        $id = (int) ($data['id'] ?? 0);
        if (!$id || !get_user_by('id', $id)) {
            return new WP_Error('a3tal_user_missing', 'Valid user id is required.', ['status' => 404]);
        }
        $reassign = (int) ($data['reassign'] ?? 0);
        $ok = wp_delete_user($id, $reassign ?: null);
        return ['deleted' => (bool) $ok, 'id' => $id, 'reassigned_to' => $reassign ?: null];
    }

    private static function admin_role_upsert($data) {
        $slug = sanitize_key((string) ($data['role'] ?? ''));
        $name = sanitize_text_field((string) ($data['name'] ?? $slug));
        $caps = $data['capabilities'] ?? [];
        if ($slug === '' || !is_array($caps)) {
            return new WP_Error('a3tal_role_fields_required', 'role and capabilities are required.', ['status' => 400]);
        }

        $role = get_role($slug);
        if (!$role) {
            add_role($slug, $name, []);
            $role = get_role($slug);
        }
        if (!$role) {
            return new WP_Error('a3tal_role_failed', 'Could not create or load role.', ['status' => 500]);
        }

        foreach ($caps as $cap => $enabled) {
            $cap = sanitize_key((string) $cap);
            $enabled ? $role->add_cap($cap, true) : $role->remove_cap($cap);
        }
        return ['role' => $slug, 'updated' => true];
    }

    private static function admin_role_delete($data) {
        $confirm = self::admin_confirm($data, true);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        $slug = sanitize_key((string) ($data['role'] ?? ''));
        if ($slug === '' || in_array($slug, ['administrator', 'editor', 'author', 'contributor', 'subscriber'], true)) {
            return new WP_Error('a3tal_core_role_protected', 'Core roles cannot be removed through the bridge.', ['status' => 403]);
        }
        remove_role($slug);
        return ['role' => $slug, 'deleted' => true];
    }

    private static function admin_term_upsert($data) {
        $taxonomy = sanitize_key((string) ($data['taxonomy'] ?? 'category'));
        $id = (int) ($data['id'] ?? 0);
        if (!taxonomy_exists($taxonomy)) {
            return new WP_Error('a3tal_bad_taxonomy', 'Taxonomy does not exist.', ['status' => 400]);
        }
        $args = [];
        foreach (['slug', 'description'] as $field) {
            if (array_key_exists($field, $data)) {
                $args[$field] = sanitize_text_field((string) $data[$field]);
            }
        }
        if (array_key_exists('parent', $data)) {
            $args['parent'] = (int) $data['parent'];
        }

        if ($id) {
            $name = sanitize_text_field((string) ($data['name'] ?? ''));
            if ($name !== '') {
                $args['name'] = $name;
            }
            $result = wp_update_term($id, $taxonomy, $args);
        } else {
            $name = sanitize_text_field((string) ($data['name'] ?? ''));
            if ($name === '') {
                return new WP_Error('a3tal_term_name_required', 'name is required.', ['status' => 400]);
            }
            $result = wp_insert_term($name, $taxonomy, $args);
        }
        return $result;
    }

    private static function admin_term_delete($data) {
        $confirm = self::admin_confirm($data);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        $taxonomy = sanitize_key((string) ($data['taxonomy'] ?? 'category'));
        $id = (int) ($data['id'] ?? 0);
        return wp_delete_term($id, $taxonomy);
    }

    private static function admin_menu_create($data) {
        $name = sanitize_text_field((string) ($data['name'] ?? ''));
        if ($name === '') {
            return new WP_Error('a3tal_menu_name_required', 'name is required.', ['status' => 400]);
        }
        $id = wp_create_nav_menu($name);
        if (is_wp_error($id)) {
            return $id;
        }
        return ['menu_id' => $id, 'name' => $name];
    }

    private static function admin_menu_item_upsert($data) {
        $menu_id = (int) ($data['menu_id'] ?? 0);
        $item_id = (int) ($data['item_id'] ?? 0);
        if (!$menu_id) {
            return new WP_Error('a3tal_menu_id_required', 'menu_id is required.', ['status' => 400]);
        }

        $args = [
            'menu-item-status' => 'publish',
            'menu-item-title' => sanitize_text_field((string) ($data['title'] ?? '')),
            'menu-item-parent-id' => (int) ($data['parent_id'] ?? 0),
        ];

        if (!empty($data['url'])) {
            $args['menu-item-type'] = 'custom';
            $args['menu-item-url'] = esc_url_raw((string) $data['url']);
        } else {
            $args['menu-item-type'] = sanitize_key((string) ($data['type'] ?? 'post_type'));
            $args['menu-item-object'] = sanitize_key((string) ($data['object'] ?? 'page'));
            $args['menu-item-object-id'] = (int) ($data['object_id'] ?? 0);
        }

        $id = wp_update_nav_menu_item($menu_id, $item_id, $args);
        if (is_wp_error($id)) {
            return $id;
        }
        return ['menu_id' => $menu_id, 'item_id' => $id];
    }

    private static function admin_menu_assign($data) {
        $location = sanitize_key((string) ($data['location'] ?? ''));
        $menu_id = (int) ($data['menu_id'] ?? 0);
        $registered = get_registered_nav_menus();
        if ($location === '' || !array_key_exists($location, $registered)) {
            return new WP_Error('a3tal_bad_menu_location', 'Registered menu location is required.', ['status' => 400]);
        }
        $locations = get_nav_menu_locations();
        $locations[$location] = $menu_id;
        set_theme_mod('nav_menu_locations', $locations);
        return ['location' => $location, 'menu_id' => $menu_id];
    }

    private static function admin_menu_delete($data) {
        $confirm = self::admin_confirm($data);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        $menu_id = (int) ($data['menu_id'] ?? 0);
        $result = wp_delete_nav_menu($menu_id);
        return is_wp_error($result) ? $result : ['menu_id' => $menu_id, 'deleted' => true];
    }

    private static function admin_plugin_action($op, $data) {
        self::admin_load_plugin_libs();

        if ($op === 'plugin_install') {
            if (defined('DISALLOW_FILE_MODS') && DISALLOW_FILE_MODS) {
                return new WP_Error('a3tal_file_mods_disabled', 'WordPress file modifications are disabled.', ['status' => 403]);
            }
            $source = esc_url_raw((string) ($data['source_url'] ?? ''));
            if ($source === '') {
                $slug = sanitize_key((string) ($data['slug'] ?? ''));
                if ($slug === '') {
                    return new WP_Error('a3tal_plugin_slug_required', 'slug or source_url is required.', ['status' => 400]);
                }
                $api = plugins_api('plugin_information', ['slug' => $slug, 'fields' => ['sections' => false]]);
                if (is_wp_error($api)) {
                    return $api;
                }
                $source = $api->download_link;
            }

            $skin = new Automatic_Upgrader_Skin();
            $upgrader = new Plugin_Upgrader($skin);
            $result = $upgrader->install($source);
            if (is_wp_error($result)) {
                return $result;
            }
            if (!$result) {
                return new WP_Error('a3tal_plugin_install_failed', 'Plugin installation failed.', ['status' => 500]);
            }
            $plugin = $upgrader->plugin_info();
            if (!empty($data['activate']) && $plugin) {
                $activated = activate_plugin($plugin);
                if (is_wp_error($activated)) {
                    return $activated;
                }
            }
            return ['installed' => true, 'plugin' => $plugin, 'active' => $plugin ? is_plugin_active($plugin) : false];
        }

        $plugin = sanitize_text_field((string) ($data['plugin'] ?? ''));
        if ($plugin === '' || validate_file($plugin) !== 0) {
            return new WP_Error('a3tal_plugin_file_required', 'Valid plugin file is required.', ['status' => 400]);
        }

        if ($op === 'plugin_activate') {
            $result = activate_plugin($plugin);
            return is_wp_error($result) ? $result : ['plugin' => $plugin, 'active' => true];
        }
        if ($op === 'plugin_deactivate') {
            deactivate_plugins($plugin, false, is_multisite());
            return ['plugin' => $plugin, 'active' => is_plugin_active($plugin)];
        }
        if ($op === 'plugin_update') {
            $upgrader = new Plugin_Upgrader(new Automatic_Upgrader_Skin());
            $result = $upgrader->upgrade($plugin);
            return is_wp_error($result) ? $result : ['plugin' => $plugin, 'updated' => (bool) $result];
        }
        if ($op === 'plugin_delete') {
            $confirm = self::admin_confirm($data, true);
            if (is_wp_error($confirm)) {
                return $confirm;
            }
            if (is_plugin_active($plugin)) {
                deactivate_plugins($plugin, false, is_multisite());
            }
            $result = delete_plugins([$plugin]);
            return is_wp_error($result) ? $result : ['plugin' => $plugin, 'deleted' => (bool) $result];
        }

        return new WP_Error('a3tal_bad_plugin_action', 'Unsupported plugin operation.', ['status' => 400]);
    }

    private static function admin_theme_action($op, $data) {
        self::admin_load_theme_libs();

        if ($op === 'theme_install') {
            if (defined('DISALLOW_FILE_MODS') && DISALLOW_FILE_MODS) {
                return new WP_Error('a3tal_file_mods_disabled', 'WordPress file modifications are disabled.', ['status' => 403]);
            }
            $source = esc_url_raw((string) ($data['source_url'] ?? ''));
            if ($source === '') {
                $slug = sanitize_key((string) ($data['slug'] ?? ''));
                if ($slug === '') {
                    return new WP_Error('a3tal_theme_slug_required', 'slug or source_url is required.', ['status' => 400]);
                }
                $api = themes_api('theme_information', ['slug' => $slug, 'fields' => ['sections' => false]]);
                if (is_wp_error($api)) {
                    return $api;
                }
                $source = $api->download_link;
            }
            $upgrader = new Theme_Upgrader(new Automatic_Upgrader_Skin());
            $result = $upgrader->install($source);
            if (is_wp_error($result)) {
                return $result;
            }
            $theme_info = $upgrader->theme_info();
            $stylesheet = $theme_info ? $theme_info->get_stylesheet() : '';
            if (!empty($data['activate']) && $stylesheet) {
                switch_theme($stylesheet);
            }
            return ['installed' => (bool) $result, 'stylesheet' => $stylesheet, 'active' => ($stylesheet === get_stylesheet())];
        }

        $stylesheet = sanitize_text_field((string) ($data['stylesheet'] ?? ''));
        if ($stylesheet === '' || validate_file($stylesheet) !== 0 || !wp_get_theme($stylesheet)->exists()) {
            return new WP_Error('a3tal_theme_required', 'Valid installed theme stylesheet is required.', ['status' => 400]);
        }

        if ($op === 'theme_activate') {
            switch_theme($stylesheet);
            return ['stylesheet' => $stylesheet, 'active' => (get_stylesheet() === $stylesheet)];
        }
        if ($op === 'theme_update') {
            $upgrader = new Theme_Upgrader(new Automatic_Upgrader_Skin());
            $result = $upgrader->upgrade($stylesheet);
            return is_wp_error($result) ? $result : ['stylesheet' => $stylesheet, 'updated' => (bool) $result];
        }
        if ($op === 'theme_delete') {
            $confirm = self::admin_confirm($data, true);
            if (is_wp_error($confirm)) {
                return $confirm;
            }
            if ($stylesheet === get_stylesheet() || $stylesheet === get_template()) {
                return new WP_Error('a3tal_active_theme_protected', 'Active theme or active parent theme cannot be deleted.', ['status' => 403]);
            }
            $result = delete_theme($stylesheet);
            return is_wp_error($result) ? $result : ['stylesheet' => $stylesheet, 'deleted' => (bool) $result];
        }

        return new WP_Error('a3tal_bad_theme_action', 'Unsupported theme operation.', ['status' => 400]);
    }

    private static function admin_core_update($data) {
        $confirm = self::admin_confirm($data, true);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        if (defined('DISALLOW_FILE_MODS') && DISALLOW_FILE_MODS) {
            return new WP_Error('a3tal_file_mods_disabled', 'WordPress file modifications are disabled.', ['status' => 403]);
        }

        require_once ABSPATH . 'wp-admin/includes/update.php';
        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';

        wp_version_check();
        $updates = get_core_updates(['dismissed' => false]);
        if (!is_array($updates)) {
            return new WP_Error('a3tal_core_updates_unavailable', 'Could not read core updates.', ['status' => 500]);
        }

        $target = null;
        foreach ($updates as $update) {
            if (($update->response ?? '') === 'upgrade') {
                $target = $update;
                break;
            }
        }
        if (!$target) {
            return ['updated' => false, 'message' => 'WordPress core is already current.'];
        }

        $upgrader = new Core_Upgrader(new Automatic_Upgrader_Skin());
        $result = $upgrader->upgrade($target);
        return is_wp_error($result) ? $result : ['updated' => (bool) $result, 'target' => $target->current ?? null];
    }


    private static function admin_bridge_self_update($data) {
        $confirm = self::admin_confirm($data, true);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        if (defined('DISALLOW_FILE_MODS') && DISALLOW_FILE_MODS) {
            return new WP_Error('a3tal_file_mods_disabled', 'WordPress file modifications are disabled.', ['status' => 403]);
        }

        $url = 'https://raw.githubusercontent.com/marwanile1-cyber/a3tal/main/a3tal-direct-bridge.php';
        $response = wp_remote_get($url, [
            'timeout' => 30,
            'redirection' => 3,
            'headers' => ['Accept' => 'text/plain'],
        ]);
        if (is_wp_error($response)) {
            return $response;
        }

        $status = (int) wp_remote_retrieve_response_code($response);
        $code = (string) wp_remote_retrieve_body($response);
        if ($status !== 200 || strlen($code) < 1000) {
            return new WP_Error('a3tal_bridge_download_failed', 'Could not download a valid bridge file from GitHub.', ['status' => 502]);
        }
        if (strpos($code, 'Plugin Name: A3tal Direct Bridge') === false || strpos($code, 'final class A3tal_Direct_Bridge') === false) {
            return new WP_Error('a3tal_bridge_invalid_source', 'Downloaded source is not the A3tal Direct Bridge plugin.', ['status' => 400]);
        }

        $sha256 = hash('sha256', $code);
        $expected = strtolower(trim((string) ($data['expected_sha256'] ?? '')));
        if ($expected !== '' && !hash_equals($expected, $sha256)) {
            return new WP_Error('a3tal_bridge_checksum_mismatch', 'Downloaded bridge checksum does not match expected_sha256.', ['status' => 409]);
        }

        $backup = __FILE__ . '.bak-' . gmdate('Ymd-His');
        if (!copy(__FILE__, $backup)) {
            return new WP_Error('a3tal_bridge_backup_failed', 'Could not create a local backup of the current bridge.', ['status' => 500]);
        }

        $written = file_put_contents(__FILE__, $code, LOCK_EX);
        if ($written === false) {
            @copy($backup, __FILE__);
            return new WP_Error('a3tal_bridge_update_failed', 'Could not replace the bridge file.', ['status' => 500]);
        }

        preg_match('/\* Version:\s*([^\r\n]+)/', $code, $m);
        return [
            'updated' => true,
            'bytes' => $written,
            'sha256' => $sha256,
            'version' => isset($m[1]) ? trim($m[1]) : null,
            'backup' => basename($backup),
        ];
    }

    private static function admin_file_write($data) {
        $confirm = self::admin_confirm($data, true);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        if (defined('DISALLOW_FILE_MODS') && DISALLOW_FILE_MODS) {
            return new WP_Error('a3tal_file_mods_disabled', 'WordPress file modifications are disabled.', ['status' => 403]);
        }

        $path = self::admin_content_path($data['path'] ?? '', false);
        if (is_wp_error($path)) {
            return $path;
        }
        if (!self::admin_text_extension_allowed($path)) {
            return new WP_Error('a3tal_bad_file_extension', 'File extension is not approved for wp-content editing.', ['status' => 400]);
        }
        $content = (string) ($data['content'] ?? '');
        if (strlen($content) > 2097152) {
            return new WP_Error('a3tal_file_too_large', 'Write payload exceeds 2 MB.', ['status' => 413]);
        }

        $expected = (string) ($data['expected_sha256'] ?? '');
        if ($expected !== '' && file_exists($path)) {
            $actual = hash_file('sha256', $path);
            if (!hash_equals($expected, $actual)) {
                return new WP_Error('a3tal_file_conflict', 'File changed since it was read.', ['status' => 409]);
            }
        }

        $written = file_put_contents($path, $content, LOCK_EX);
        if ($written === false) {
            return new WP_Error('a3tal_file_write_failed', 'Could not write file.', ['status' => 500]);
        }
        return [
            'path' => ltrim(str_replace(trailingslashit(wp_normalize_path(WP_CONTENT_DIR)), '', wp_normalize_path($path)), '/'),
            'bytes' => $written,
            'sha256' => hash_file('sha256', $path),
        ];
    }

    private static function admin_file_delete($data) {
        $confirm = self::admin_confirm($data, true);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        $path = self::admin_content_path($data['path'] ?? '', true);
        if (is_wp_error($path)) {
            return $path;
        }
        if (!is_file($path)) {
            return new WP_Error('a3tal_not_file', 'Path is not a file.', ['status' => 400]);
        }
        if (wp_normalize_path($path) === wp_normalize_path(__FILE__)) {
            return new WP_Error('a3tal_bridge_self_delete_blocked', 'The active bridge cannot delete itself.', ['status' => 403]);
        }
        $ok = unlink($path);
        return ['deleted' => (bool) $ok];
    }

    private static function admin_cache_flush() {
        $done = ['object_cache' => wp_cache_flush()];

        if (function_exists('litespeed_purge_all')) {
            litespeed_purge_all();
            $done['litespeed'] = true;
        }
        if (has_action('litespeed_purge_all')) {
            do_action('litespeed_purge_all');
            $done['litespeed_action'] = true;
        }
        if (function_exists('rocket_clean_domain')) {
            rocket_clean_domain();
            $done['wp_rocket'] = true;
        }
        if (function_exists('w3tc_flush_all')) {
            w3tc_flush_all();
            $done['w3_total_cache'] = true;
        }
        if (function_exists('wp_cache_clear_cache')) {
            wp_cache_clear_cache();
            $done['wp_super_cache'] = true;
        }
        return $done;
    }

    private static function admin_transients_clear($data) {
        $confirm = self::admin_confirm($data);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        global $wpdb;
        $a = $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '\\_transient\\_%' OR option_name LIKE '\\_transient\\_timeout\\_%'");
        $b = 0;
        if (is_multisite()) {
            $b = $wpdb->query("DELETE FROM {$wpdb->sitemeta} WHERE meta_key LIKE '\\_site\\_transient\\_%' OR meta_key LIKE '\\_site\\_transient\\_timeout\\_%'");
        } else {
            $b = $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '\\_site\\_transient\\_%' OR option_name LIKE '\\_site\\_transient\\_timeout\\_%'");
        }
        wp_cache_flush();
        return ['deleted_rows' => (int) $a + (int) $b];
    }

    private static function admin_cron_run($data) {
        $hook = sanitize_key((string) ($data['hook'] ?? ''));
        if ($hook === '') {
            return new WP_Error('a3tal_hook_required', 'hook is required.', ['status' => 400]);
        }
        do_action_ref_array($hook, is_array($data['args'] ?? null) ? $data['args'] : []);
        return ['hook' => $hook, 'ran' => true];
    }

    private static function admin_cron_delete($data) {
        $confirm = self::admin_confirm($data);
        if (is_wp_error($confirm)) {
            return $confirm;
        }
        $hook = sanitize_key((string) ($data['hook'] ?? ''));
        if ($hook === '') {
            return new WP_Error('a3tal_hook_required', 'hook is required.', ['status' => 400]);
        }
        $args = is_array($data['args'] ?? null) ? $data['args'] : [];
        $timestamp = wp_next_scheduled($hook, $args);
        if (!$timestamp) {
            return ['hook' => $hook, 'unscheduled' => false];
        }
        $result = wp_unschedule_event($timestamp, $hook, $args);
        return is_wp_error($result) ? $result : ['hook' => $hook, 'unscheduled' => (bool) $result];
    }

    public static function admin_gateway(WP_REST_Request $request) {
        $data = strtoupper($request->get_method()) === 'GET' ? $request->get_params() : $request->get_json_params();
        if (!is_array($data)) {
            $data = [];
        }

        $op = sanitize_key((string) ($data['op'] ?? $request->get_param('op') ?? ''));
        if ($op === '') {
            return new WP_Error('a3tal_admin_op_required', 'op is required.', ['status' => 400]);
        }

        try {
            switch ($op) {
                case 'site_info':
                    $result = self::admin_site_info();
                    break;
                case 'plugins':
                    $result = self::admin_plugins();
                    break;
                case 'themes':
                    $result = self::admin_themes();
                    break;
                case 'users':
                    $result = self::admin_users($data);
                    break;
                case 'roles':
                    $result = self::admin_roles();
                    break;
                case 'options':
                    $result = self::admin_options($data);
                    break;
                case 'terms':
                    $result = self::admin_terms($data);
                    break;
                case 'menus':
                    $result = self::admin_menus();
                    break;
                case 'comments':
                    $result = self::admin_comments($data);
                    break;
                case 'updates':
                    $result = self::admin_updates();
                    break;
                case 'cron':
                    $result = self::admin_cron($data);
                    break;
                case 'file_read':
                    $result = self::admin_file_read($data);
                    break;
                case 'file_list':
                    $result = self::admin_file_list($data);
                    break;
                case 'post_meta':
                    $result = self::admin_post_meta($data);
                    break;
                case 'theme_mods':
                    $result = self::admin_theme_mods();
                    break;
                case 'audit_log':
                    $log = get_option('a3tal_direct_bridge_admin_audit', []);
                    $result = array_slice(is_array($log) ? $log : [], -max(1, min(200, (int) ($data['limit'] ?? 50))));
                    break;

                case 'option_set':
                    $result = self::admin_write_option($data);
                    break;
                case 'option_delete':
                    $result = self::admin_delete_option($data);
                    break;
                case 'post_meta_set':
                    $post_id = (int) ($data['post_id'] ?? 0);
                    $meta = $data['meta'] ?? [];
                    if (!$post_id || !get_post($post_id) || !is_array($meta)) {
                        $result = new WP_Error('a3tal_bad_post_meta', 'Valid post_id and meta object are required.', ['status' => 400]);
                        break;
                    }
                    foreach ($meta as $key => $value) {
                        update_post_meta($post_id, (string) $key, $value);
                    }
                    $result = ['post_id' => $post_id, 'updated_keys' => array_keys($meta)];
                    break;
                case 'post_meta_delete':
                    $post_id = (int) ($data['post_id'] ?? 0);
                    $keys = $data['keys'] ?? [];
                    if (is_string($keys)) {
                        $keys = array_filter(array_map('trim', explode(',', $keys)));
                    }
                    if (!$post_id || !get_post($post_id) || !is_array($keys)) {
                        $result = new WP_Error('a3tal_bad_post_meta', 'Valid post_id and keys are required.', ['status' => 400]);
                        break;
                    }
                    foreach ($keys as $key) {
                        delete_post_meta($post_id, (string) $key);
                    }
                    $result = ['post_id' => $post_id, 'deleted_keys' => array_values($keys)];
                    break;
                case 'term_upsert':
                    $result = self::admin_term_upsert($data);
                    break;
                case 'term_delete':
                    $result = self::admin_term_delete($data);
                    break;
                case 'menu_create':
                    $result = self::admin_menu_create($data);
                    break;
                case 'menu_item_upsert':
                    $result = self::admin_menu_item_upsert($data);
                    break;
                case 'menu_assign':
                    $result = self::admin_menu_assign($data);
                    break;
                case 'menu_delete':
                    $result = self::admin_menu_delete($data);
                    break;
                case 'user_upsert':
                    $result = self::admin_user_upsert($data);
                    break;
                case 'user_delete':
                    $result = self::admin_user_delete($data);
                    break;
                case 'role_upsert':
                    $result = self::admin_role_upsert($data);
                    break;
                case 'role_delete':
                    $result = self::admin_role_delete($data);
                    break;

                case 'plugin_install':
                case 'plugin_activate':
                case 'plugin_deactivate':
                case 'plugin_update':
                case 'plugin_delete':
                    $result = self::admin_plugin_action($op, $data);
                    break;

                case 'theme_install':
                case 'theme_activate':
                case 'theme_update':
                case 'theme_delete':
                    $result = self::admin_theme_action($op, $data);
                    break;

                case 'core_update':
                    $result = self::admin_core_update($data);
                    break;
                case 'bridge_self_update':
                    $result = self::admin_bridge_self_update($data);
                    break;
                case 'file_write':
                    $result = self::admin_file_write($data);
                    break;
                case 'file_delete':
                    $result = self::admin_file_delete($data);
                    break;
                case 'cache_flush':
                    $result = self::admin_cache_flush();
                    break;
                case 'rewrite_flush':
                    flush_rewrite_rules(false);
                    $result = ['flushed' => true];
                    break;
                case 'transients_clear':
                    $result = self::admin_transients_clear($data);
                    break;
                case 'cron_run':
                    $result = self::admin_cron_run($data);
                    break;
                case 'cron_delete':
                    $result = self::admin_cron_delete($data);
                    break;
                case 'theme_mod_set':
                    $name = sanitize_key((string) ($data['name'] ?? ''));
                    if ($name === '') {
                        $result = new WP_Error('a3tal_theme_mod_required', 'name is required.', ['status' => 400]);
                        break;
                    }
                    set_theme_mod($name, $data['value'] ?? null);
                    $result = ['name' => $name, 'updated' => true];
                    break;
                case 'theme_mod_delete':
                    $name = sanitize_key((string) ($data['name'] ?? ''));
                    if ($name === '') {
                        $result = new WP_Error('a3tal_theme_mod_required', 'name is required.', ['status' => 400]);
                        break;
                    }
                    remove_theme_mod($name);
                    $result = ['name' => $name, 'deleted' => true];
                    break;

                default:
                    return new WP_Error('a3tal_unknown_admin_op', 'Unsupported admin operation.', ['status' => 400]);
            }
        } catch (Throwable $e) {
            self::admin_audit($op, false, $e->getMessage());
            return new WP_Error('a3tal_admin_exception', $e->getMessage(), ['status' => 500]);
        }

        if (is_wp_error($result)) {
            self::admin_audit($op, false, $result->get_error_message());
            return $result;
        }

        if (!self::admin_is_read_op($op)) {
            self::admin_audit($op, true);
        }

        return self::admin_result($op, $result);
    }

    public static function admin_menu() {
        add_management_page(
            'A3tal Direct Bridge',
            'A3tal Direct Bridge',
            'manage_options',
            'a3tal-direct-bridge',
            [__CLASS__, 'settings_page']
        );
    }

    public static function register_settings() {
        register_setting('a3tal_direct_bridge', self::OPTION_KEY, [
            'type' => 'string',
            'sanitize_callback' => 'sanitize_text_field',
            'default' => '',
        ]);
    }

    public static function settings_page() {
        if (!current_user_can('manage_options')) {
            return;
        }

        if (isset($_POST['a3tal_generate_key']) && check_admin_referer('a3tal_generate_key_action')) {
            update_option(self::OPTION_KEY, wp_generate_password(48, false, false), false);
            echo '<div class="notice notice-success"><p>New API key generated.</p></div>';
        }

        $key = (string) get_option(self::OPTION_KEY, '');
        ?>
        <div class="wrap">
            <h1>A3tal Direct Bridge</h1>
            <p>Use this API key only in trusted clients. Never commit it to GitHub.</p>

            <form method="post" action="options.php">
                <?php settings_fields('a3tal_direct_bridge'); ?>
                <table class="form-table">
                    <tr>
                        <th scope="row"><label for="<?php echo esc_attr(self::OPTION_KEY); ?>">API Key</label></th>
                        <td>
                            <input type="password" id="<?php echo esc_attr(self::OPTION_KEY); ?>" name="<?php echo esc_attr(self::OPTION_KEY); ?>" value="<?php echo esc_attr($key); ?>" class="regular-text" autocomplete="off">
                            <p class="description">Header: <code>X-A3tal-Key: YOUR_KEY</code> or <code>Authorization: Bearer YOUR_KEY</code></p>
                        </td>
                    </tr>
                </table>
                <?php submit_button('Save API Key'); ?>
            </form>

            <hr>
            <form method="post">
                <?php wp_nonce_field('a3tal_generate_key_action'); ?>
                <input type="hidden" name="a3tal_generate_key" value="1">
                <?php submit_button('Generate New Random Key', 'secondary'); ?>
            </form>

            <p><strong>REST base:</strong> <code><?php echo esc_html(rest_url(self::NS . '/')); ?></code></p>
        </div>
        <?php
    }
}

A3tal_Direct_Bridge::init();

// Build package refresh: 3.1.0
