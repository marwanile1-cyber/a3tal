<?php
/**
 * Plugin Name: A3tal Direct Bridge
 * Description: Secure REST bridge for managing A3tal.com posts, SEO fields, media and redirects from trusted AI clients.
 * Version: 2.1.0
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
            'version' => '2.1.0',
            'site' => home_url('/'),
            'time_gmt' => current_time('mysql', true),
            'routes' => [
                'GET /status',
                'GET /post/{id}',
                'GET /search-posts',
                'POST /create-post',
                'POST /update-post',
                'POST /upload-image',
                'POST /set-featured-image',
                'POST /insert-images',
                'POST /redirect',
                'POST /rollback-last',
            ],
        ]);
    }

    private static function yoast_meta_keys() {
        return [
            '_yoast_wpseo_focuskw',
            '_yoast_wpseo_title',
            '_yoast_wpseo_metadesc',
            '_yoast_wpseo_canonical',
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
            return;
        }
        foreach (self::yoast_meta_keys() as $key) {
            if (array_key_exists($key, $meta)) {
                update_post_meta($post_id, $key, sanitize_text_field((string) $meta[$key]));
            }
        }
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
        self::apply_meta($id, $data['meta'] ?? []);

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
        self::apply_meta($id, $data['meta'] ?? []);

        clean_post_cache($id);
        return rest_ensure_response(self::post_payload(get_post($id)));
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

        self::apply_meta($id, $s['meta'] ?? []);
        array_splice($backups, $index, 1);
        update_option(self::BACKUPS_KEY, $backups, false);

        return rest_ensure_response(['ok' => true, 'restored' => self::post_payload(get_post($id))]);
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
