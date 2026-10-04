<?php
/**
 * Plugin Name: A3tal Core Platform
 * Plugin URI: https://a3tal.com/
 * Description: Core data layer for A3tal.com cars, motorcycles, DTC codes, service centers and car showrooms.
 * Version: 0.2.3
 * Author: A3tal.com
 * Requires at least: 6.4
 * Requires PHP: 8.0
 * Text Domain: a3tal-core-platform
 */

if (!defined('ABSPATH')) exit;

define('A3CP_VERSION', '0.2.3');
define('A3CP_FILE', __FILE__);
define('A3CP_DIR', plugin_dir_path(__FILE__));
define('A3CP_URL', plugin_dir_url(__FILE__));

require_once A3CP_DIR . 'inc/class-a3cp-content-types.php';
require_once A3CP_DIR . 'inc/class-a3cp-meta-boxes.php';
require_once A3CP_DIR . 'inc/class-a3cp-admin.php';
require_once A3CP_DIR . 'inc/class-a3cp-ownership-commerce.php';
require_once A3CP_DIR . 'inc/class-a3cp-showroom-editorial.php';

function a3cp_boot(): void {
    A3CP_Content_Types::init();
    A3CP_Meta_Boxes::init();
    A3CP_Admin::init();
    A3CP_Ownership_Commerce::init();
    A3CP_Showroom_Editorial::init();
}
add_action('plugins_loaded', 'a3cp_boot');

function a3cp_activate(): void {
    A3CP_Content_Types::register_all();
    A3CP_Content_Types::seed_core_terms();
    A3CP_Ownership_Commerce::register_all();
    flush_rewrite_rules(false);
}
register_activation_hook(__FILE__, 'a3cp_activate');

function a3cp_deactivate(): void {
    flush_rewrite_rules(false);
}
register_deactivation_hook(__FILE__, 'a3cp_deactivate');

/**
 * Public helper: returns a formatted price range for a vehicle entity.
 */
function a3cp_vehicle_price(int $post_id = 0): string {
    $post_id = $post_id ?: get_the_ID();
    $min = (float) get_post_meta($post_id, '_a3_price_min', true);
    $max = (float) get_post_meta($post_id, '_a3_price_max', true);
    $currency = trim((string) get_post_meta($post_id, '_a3_currency', true));

    if ($min <= 0 && $max <= 0) return '';
    $suffix = $currency !== '' ? ' ' . $currency : '';
    if ($min > 0 && $max > 0 && $min !== $max) {
        return number_format_i18n($min, 0) . ' – ' . number_format_i18n($max, 0) . $suffix;
    }
    $value = $min > 0 ? $min : $max;
    return number_format_i18n($value, 0) . $suffix;
}

/**
 * Public helper: fetch a scalar platform field without exposing storage details.
 */
function a3cp_field(string $key, int $post_id = 0): string {
    $post_id = $post_id ?: get_the_ID();
    return trim((string) get_post_meta($post_id, $key, true));
}
