<?php
if (!defined('ABSPATH')) exit;

final class A3CP_Ownership_Commerce {
    private const SCHEMA_VERSION = '0.2.0';

    private const TYPES = [
        'a3_part' => [
            'singular' => 'قطعة غيار',
            'plural' => 'قطع الغيار',
            'slug' => 'parts',
            'rest' => 'a3tal-parts',
        ],
        'a3_parts_vendor' => [
            'singular' => 'بائع قطع غيار',
            'plural' => 'أماكن بيع قطع الغيار',
            'slug' => 'parts-stores',
            'rest' => 'a3tal-parts-vendors',
        ],
        'a3_listing' => [
            'singular' => 'إعلان سيارة',
            'plural' => 'سيارات للبيع',
            'slug' => 'cars-for-sale',
            'rest' => 'a3tal-listings',
        ],
        'a3_maintenance_plan' => [
            'singular' => 'جدول صيانة',
            'plural' => 'جداول الصيانة',
            'slug' => 'maintenance-schedules',
            'rest' => 'a3tal-maintenance-plans',
        ],
    ];

    public static function init(): void {
        add_action('init', [__CLASS__, 'register_all'], 6);
        add_action('init', [__CLASS__, 'maybe_upgrade'], 30);
        add_action('rest_api_init', [__CLASS__, 'register_rest_routes']);
        add_action('a3cp_daily_reminders', [__CLASS__, 'process_due_reminders']);
        add_action('transition_post_status', [__CLASS__, 'protect_listing_publish'], 10, 3);
    }

    public static function register_all(): void {
        self::register_post_types();
        self::register_taxonomies();
        self::register_meta();
    }

    private static function labels(string $singular, string $plural): array {
        return [
            'name' => $plural,
            'singular_name' => $singular,
            'menu_name' => $plural,
            'add_new' => 'إضافة جديد',
            'add_new_item' => 'إضافة ' . $singular,
            'edit_item' => 'تعديل ' . $singular,
            'new_item' => $singular . ' جديد',
            'view_item' => 'عرض ' . $singular,
            'search_items' => 'بحث في ' . $plural,
            'not_found' => 'لا توجد نتائج',
            'not_found_in_trash' => 'لا توجد عناصر في سلة المهملات',
            'all_items' => 'الكل',
        ];
    }

    private static function register_post_types(): void {
        foreach (self::TYPES as $type => $cfg) {
            $supports = ['title', 'editor', 'excerpt', 'thumbnail', 'revisions'];
            if ($type === 'a3_listing') {
                $supports[] = 'author';
            }
            register_post_type($type, [
                'labels' => self::labels($cfg['singular'], $cfg['plural']),
                'public' => true,
                'publicly_queryable' => true,
                'show_ui' => true,
                'show_in_menu' => 'a3tal-platform',
                'show_in_rest' => true,
                'rest_base' => $cfg['rest'],
                'has_archive' => $cfg['slug'],
                'rewrite' => ['slug' => $cfg['slug'], 'with_front' => false, 'feeds' => false],
                'supports' => $supports,
                'exclude_from_search' => false,
                'hierarchical' => false,
                'query_var' => true,
                'can_export' => true,
                'delete_with_user' => false,
                'show_in_nav_menus' => true,
            ]);
        }
    }

    private static function tax_args(string $plural, string $singular, bool $hierarchical = false): array {
        return [
            'labels' => [
                'name' => $plural,
                'singular_name' => $singular,
                'menu_name' => $plural,
                'all_items' => 'الكل',
                'edit_item' => 'تعديل',
                'update_item' => 'تحديث',
                'add_new_item' => 'إضافة جديد',
            ],
            'public' => false,
            'publicly_queryable' => false,
            'show_ui' => true,
            'show_admin_column' => true,
            'show_in_rest' => true,
            'hierarchical' => $hierarchical,
            'rewrite' => false,
            'query_var' => false,
        ];
    }

    private static function register_taxonomies(): void {
        register_taxonomy('a3_part_origin', ['a3_part'], self::tax_args('نوع / منشأ القطعة', 'نوع القطعة'));
        register_taxonomy('a3_part_category', ['a3_part'], self::tax_args('تصنيفات قطع الغيار', 'تصنيف القطعة', true));
        register_taxonomy('a3_vendor_status', ['a3_parts_vendor'], self::tax_args('حالة بائع قطع الغيار', 'حالة البائع'));
        register_taxonomy('a3_listing_condition', ['a3_listing'], self::tax_args('حالة السيارة', 'الحالة'));
        register_taxonomy('a3_maintenance_kind', ['a3_maintenance_plan'], self::tax_args('نوع بند الصيانة', 'نوع الصيانة'));

        foreach (['a3_part', 'a3_parts_vendor', 'a3_listing', 'a3_maintenance_plan'] as $type) {
            register_taxonomy_for_object_type('a3_market', $type);
        }
        foreach (['a3_part', 'a3_parts_vendor', 'a3_listing', 'a3_maintenance_plan'] as $type) {
            register_taxonomy_for_object_type('a3_brand', $type);
        }
    }

    private static function meta(string $type, string $key, string $data_type, callable $sanitize, bool $rest = true): void {
        register_post_meta($type, $key, [
            'type' => $data_type,
            'single' => true,
            'show_in_rest' => $rest,
            'sanitize_callback' => $sanitize,
            'auth_callback' => static fn() => current_user_can('edit_posts'),
        ]);
    }

    private static function register_meta(): void {
        foreach ([
            '_a3_part_number','_a3_oem_number','_a3_part_manufacturer','_a3_part_condition',
            '_a3_currency','_a3_source_checked_at','_a3_vehicle_entity_ids'
        ] as $key) {
            self::meta('a3_part', $key, 'string', 'sanitize_text_field');
        }
        self::meta('a3_part', '_a3_price_min', 'number', [__CLASS__, 'sanitize_number']);
        self::meta('a3_part', '_a3_price_max', 'number', [__CLASS__, 'sanitize_number']);
        self::meta('a3_part', '_a3_source_url', 'string', 'esc_url_raw');

        foreach (['_a3_phone','_a3_whatsapp','_a3_address','_a3_hours','_a3_source_checked_at'] as $key) {
            $sanitize = in_array($key, ['_a3_address','_a3_hours'], true) ? 'sanitize_textarea_field' : 'sanitize_text_field';
            self::meta('a3_parts_vendor', $key, 'string', $sanitize);
        }
        self::meta('a3_parts_vendor', '_a3_lat', 'number', [__CLASS__, 'sanitize_number']);
        self::meta('a3_parts_vendor', '_a3_lng', 'number', [__CLASS__, 'sanitize_number']);
        self::meta('a3_parts_vendor', '_a3_official_source_url', 'string', 'esc_url_raw');
        self::meta('a3_parts_vendor', '_a3_delivery_available', 'boolean', [__CLASS__, 'sanitize_bool']);

        foreach (['_a3_listing_currency','_a3_listing_location','_a3_listing_transmission','_a3_listing_fuel'] as $key) {
            self::meta('a3_listing', $key, 'string', 'sanitize_text_field');
        }
        self::meta('a3_listing', '_a3_vehicle_entity_id', 'integer', 'absint');
        self::meta('a3_listing', '_a3_listing_year', 'integer', 'absint');
        self::meta('a3_listing', '_a3_listing_mileage_km', 'integer', 'absint');
        self::meta('a3_listing', '_a3_listing_price', 'number', [__CLASS__, 'sanitize_number']);
        self::meta('a3_listing', '_a3_listing_owner_count', 'integer', 'absint');
        self::meta('a3_listing', '_a3_listing_featured', 'boolean', [__CLASS__, 'sanitize_bool']);
        self::meta('a3_listing', '_a3_listing_expires_at', 'string', 'sanitize_text_field');
        self::meta('a3_listing', '_a3_listing_contact_phone', 'string', 'sanitize_text_field', false);
        self::meta('a3_listing', '_a3_private_plate_hint', 'string', 'sanitize_text_field', false);
        self::meta('a3_listing', '_a3_private_vin_hint', 'string', 'sanitize_text_field', false);

        self::meta('a3_maintenance_plan', '_a3_vehicle_entity_id', 'integer', 'absint');
        self::meta('a3_maintenance_plan', '_a3_interval_km', 'integer', 'absint');
        self::meta('a3_maintenance_plan', '_a3_interval_months', 'integer', 'absint');
        self::meta('a3_maintenance_plan', '_a3_severe_interval_km', 'integer', 'absint');
        self::meta('a3_maintenance_plan', '_a3_severe_interval_months', 'integer', 'absint');
        self::meta('a3_maintenance_plan', '_a3_service_action', 'string', 'sanitize_text_field');
        self::meta('a3_maintenance_plan', '_a3_fluid_spec', 'string', 'sanitize_text_field');
        self::meta('a3_maintenance_plan', '_a3_fluid_quantity', 'string', 'sanitize_text_field');
        self::meta('a3_maintenance_plan', '_a3_part_numbers', 'string', 'sanitize_text_field');
        self::meta('a3_maintenance_plan', '_a3_estimated_minutes', 'integer', 'absint');
        self::meta('a3_maintenance_plan', '_a3_source_url', 'string', 'esc_url_raw');
        self::meta('a3_maintenance_plan', '_a3_source_checked_at', 'string', 'sanitize_text_field');
    }

    public static function sanitize_number($value): float {
        return is_numeric($value) ? (float) $value : 0.0;
    }

    public static function sanitize_bool($value): bool {
        return filter_var($value, FILTER_VALIDATE_BOOLEAN);
    }

    public static function maybe_upgrade(): void {
        if ((string) get_option('a3cp_ownership_schema_version') === self::SCHEMA_VERSION) return;
        self::register_all();
        self::create_tables();
        self::seed_terms();
        self::schedule_cron();
        update_option('a3cp_ownership_schema_version', self::SCHEMA_VERSION, false);
        flush_rewrite_rules(false);
    }

    private static function create_tables(): void {
        global $wpdb;
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';

        $charset = $wpdb->get_charset_collate();
        $garage = $wpdb->prefix . 'a3tal_garage';
        $events = $wpdb->prefix . 'a3tal_service_events';
        $reminders = $wpdb->prefix . 'a3tal_reminders';

        dbDelta("CREATE TABLE {$garage} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            user_id bigint(20) unsigned NOT NULL,
            vehicle_type varchar(20) NOT NULL DEFAULT 'car',
            entity_id bigint(20) unsigned NOT NULL DEFAULT 0,
            nickname varchar(120) NOT NULL DEFAULT '',
            year smallint(5) unsigned NOT NULL DEFAULT 0,
            odometer_km int(10) unsigned NOT NULL DEFAULT 0,
            usage_profile varchar(30) NOT NULL DEFAULT 'normal',
            plate_hint varchar(24) NOT NULL DEFAULT '',
            vin_hint varchar(24) NOT NULL DEFAULT '',
            ownership_started date NULL,
            created_at datetime NOT NULL,
            updated_at datetime NOT NULL,
            PRIMARY KEY  (id),
            KEY user_id (user_id),
            KEY entity_id (entity_id)
        ) {$charset};");

        dbDelta("CREATE TABLE {$events} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            user_id bigint(20) unsigned NOT NULL,
            garage_id bigint(20) unsigned NOT NULL,
            event_type varchar(60) NOT NULL DEFAULT 'service',
            event_date date NOT NULL,
            odometer_km int(10) unsigned NOT NULL DEFAULT 0,
            title varchar(190) NOT NULL DEFAULT '',
            details text NULL,
            cost decimal(14,2) NOT NULL DEFAULT 0,
            currency varchar(12) NOT NULL DEFAULT '',
            next_due_km int(10) unsigned NOT NULL DEFAULT 0,
            next_due_date date NULL,
            created_at datetime NOT NULL,
            PRIMARY KEY  (id),
            KEY user_id (user_id),
            KEY garage_id (garage_id),
            KEY event_date (event_date)
        ) {$charset};");

        dbDelta("CREATE TABLE {$reminders} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            user_id bigint(20) unsigned NOT NULL,
            garage_id bigint(20) unsigned NOT NULL,
            reminder_key varchar(120) NOT NULL,
            title varchar(190) NOT NULL,
            due_km int(10) unsigned NOT NULL DEFAULT 0,
            due_date date NULL,
            status varchar(20) NOT NULL DEFAULT 'active',
            email_opt_in tinyint(1) NOT NULL DEFAULT 0,
            last_notified_at datetime NULL,
            created_at datetime NOT NULL,
            updated_at datetime NOT NULL,
            PRIMARY KEY  (id),
            KEY user_id (user_id),
            KEY garage_id (garage_id),
            KEY due_date (due_date),
            KEY status (status)
        ) {$charset};");
    }

    private static function seed_terms(): void {
        self::seed('a3_part_origin', [
            'genuine-oem' => 'أصلي Genuine / OEM',
            'oes' => 'OES مورد أصلي',
            'aftermarket' => 'Aftermarket معروف',
            'economy-china' => 'بديل اقتصادي / صيني',
            'imported-used' => 'استيراد خارج / مستعمل أصلي',
            'remanufactured' => 'مجدّد / Remanufactured',
            'used-local' => 'مستعمل محلي',
        ]);
        self::seed('a3_vendor_status', [
            'official-distributor' => 'موزع / بائع رسمي',
            'verified' => 'موثّق من أعطال',
            'independent' => 'بائع مستقل',
        ]);
        self::seed('a3_listing_condition', [
            'excellent' => 'ممتازة',
            'very-good' => 'جيدة جدًا',
            'good' => 'جيدة',
            'needs-work' => 'تحتاج مصروف',
        ]);
        self::seed('a3_maintenance_kind', [
            'engine-oil' => 'زيت المحرك',
            'oil-filter' => 'فلتر الزيت',
            'air-filter' => 'فلتر الهواء',
            'cabin-filter' => 'فلتر التكييف',
            'fuel-filter' => 'فلتر الوقود',
            'spark-plugs' => 'البوجيهات',
            'transmission-fluid' => 'زيت ناقل الحركة',
            'coolant' => 'سائل التبريد',
            'brake-fluid' => 'زيت الفرامل',
            'brake-pads' => 'تيل الفرامل',
            'timing-system' => 'سير / جنزير التوقيت',
            'battery' => 'البطارية',
            'tires' => 'الإطارات',
            'inspection' => 'فحص دوري',
        ]);

        self::seed('a3_part_category', [
            'engine' => 'المحرك',
            'ignition' => 'الإشعال',
            'fuel-system' => 'نظام الوقود',
            'cooling' => 'التبريد',
            'transmission' => 'ناقل الحركة',
            'suspension' => 'العفشة والتعليق',
            'steering' => 'التوجيه',
            'brakes' => 'الفرامل',
            'electrical' => 'الكهرباء والحساسات',
            'air-conditioning' => 'التكييف',
            'filters' => 'الفلاتر',
            'body' => 'الهيكل والسمكرة',
            'lighting' => 'الإضاءة',
            'tires-wheels' => 'الإطارات والجنوط',
            'motorcycle-parts' => 'قطع غيار الموتوسيكلات',
        ]);
    }

    private static function seed(string $taxonomy, array $terms): void {
        foreach ($terms as $slug => $name) {
            if (!term_exists($slug, $taxonomy)) {
                wp_insert_term($name, $taxonomy, ['slug' => $slug]);
            }
        }
    }

    private static function schedule_cron(): void {
        if (!wp_next_scheduled('a3cp_daily_reminders')) {
            wp_schedule_event(time() + HOUR_IN_SECONDS, 'daily', 'a3cp_daily_reminders');
        }
    }

    public static function register_rest_routes(): void {
        register_rest_route('a3tal-platform/v1', '/garage', [
            [
                'methods' => WP_REST_Server::READABLE,
                'callback' => [__CLASS__, 'rest_garage_list'],
                'permission_callback' => [__CLASS__, 'rest_logged_in'],
            ],
            [
                'methods' => WP_REST_Server::CREATABLE,
                'callback' => [__CLASS__, 'rest_garage_create'],
                'permission_callback' => [__CLASS__, 'rest_logged_in'],
            ],
        ]);

        register_rest_route('a3tal-platform/v1', '/garage/(?P<id>\d+)', [
            [
                'methods' => WP_REST_Server::EDITABLE,
                'callback' => [__CLASS__, 'rest_garage_update'],
                'permission_callback' => [__CLASS__, 'rest_logged_in'],
            ],
            [
                'methods' => WP_REST_Server::DELETABLE,
                'callback' => [__CLASS__, 'rest_garage_delete'],
                'permission_callback' => [__CLASS__, 'rest_logged_in'],
            ],
        ]);

        register_rest_route('a3tal-platform/v1', '/garage/(?P<id>\d+)/maintenance', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [__CLASS__, 'rest_add_service_event'],
            'permission_callback' => [__CLASS__, 'rest_logged_in'],
        ]);

        register_rest_route('a3tal-platform/v1', '/garage/(?P<id>\d+)/sell', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [__CLASS__, 'rest_create_listing'],
            'permission_callback' => [__CLASS__, 'rest_logged_in'],
        ]);
    }

    public static function rest_logged_in(): bool {
        return is_user_logged_in();
    }

    private static function owned_garage_row(int $id, int $user_id): ?object {
        global $wpdb;
        $table = $wpdb->prefix . 'a3tal_garage';
        $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d AND user_id=%d", $id, $user_id));
        return $row ?: null;
    }

    public static function rest_garage_list(WP_REST_Request $request) {
        global $wpdb;
        $user_id = get_current_user_id();
        $table = $wpdb->prefix . 'a3tal_garage';
        $rows = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$table} WHERE user_id=%d ORDER BY updated_at DESC", $user_id), ARRAY_A);
        return rest_ensure_response(['items' => $rows ?: []]);
    }

    public static function rest_garage_create(WP_REST_Request $request) {
        global $wpdb;
        $user_id = get_current_user_id();
        $data = self::garage_payload($request);
        if (is_wp_error($data)) return $data;

        $now = current_time('mysql');
        $data['user_id'] = $user_id;
        $data['created_at'] = $now;
        $data['updated_at'] = $now;

        $table = $wpdb->prefix . 'a3tal_garage';
        $ok = $wpdb->insert($table, $data);
        if (!$ok) return new WP_Error('a3cp_garage_create_failed', 'تعذر إضافة المركبة إلى الجراج.', ['status' => 500]);

        return rest_ensure_response(['id' => (int) $wpdb->insert_id, 'created' => true]);
    }

    public static function rest_garage_update(WP_REST_Request $request) {
        global $wpdb;
        $user_id = get_current_user_id();
        $id = absint($request['id']);
        if (!self::owned_garage_row($id, $user_id)) {
            return new WP_Error('a3cp_garage_not_found', 'المركبة غير موجودة.', ['status' => 404]);
        }

        $data = self::garage_payload($request, true);
        if (is_wp_error($data)) return $data;
        $data['updated_at'] = current_time('mysql');

        $table = $wpdb->prefix . 'a3tal_garage';
        $wpdb->update($table, $data, ['id' => $id, 'user_id' => $user_id]);
        return rest_ensure_response(['id' => $id, 'updated' => true]);
    }

    public static function rest_garage_delete(WP_REST_Request $request) {
        global $wpdb;
        $user_id = get_current_user_id();
        $id = absint($request['id']);
        if (!self::owned_garage_row($id, $user_id)) {
            return new WP_Error('a3cp_garage_not_found', 'المركبة غير موجودة.', ['status' => 404]);
        }

        $wpdb->delete($wpdb->prefix . 'a3tal_reminders', ['garage_id' => $id, 'user_id' => $user_id]);
        $wpdb->delete($wpdb->prefix . 'a3tal_service_events', ['garage_id' => $id, 'user_id' => $user_id]);
        $wpdb->delete($wpdb->prefix . 'a3tal_garage', ['id' => $id, 'user_id' => $user_id]);
        return rest_ensure_response(['deleted' => true]);
    }

    private static function garage_payload(WP_REST_Request $request, bool $partial = false) {
        $raw = $request->get_json_params();
        if (!is_array($raw)) $raw = [];

        $fields = [];
        if (!$partial || array_key_exists('vehicle_type', $raw)) {
            $vehicle_type = sanitize_key((string) ($raw['vehicle_type'] ?? 'car'));
            if (!in_array($vehicle_type, ['car', 'motorcycle'], true)) $vehicle_type = 'car';
            $fields['vehicle_type'] = $vehicle_type;
        }
        if (!$partial || array_key_exists('entity_id', $raw)) $fields['entity_id'] = absint($raw['entity_id'] ?? 0);
        if (!$partial || array_key_exists('nickname', $raw)) $fields['nickname'] = sanitize_text_field((string) ($raw['nickname'] ?? ''));
        if (!$partial || array_key_exists('year', $raw)) $fields['year'] = absint($raw['year'] ?? 0);
        if (!$partial || array_key_exists('odometer_km', $raw)) $fields['odometer_km'] = absint($raw['odometer_km'] ?? 0);
        if (!$partial || array_key_exists('usage_profile', $raw)) {
            $usage = sanitize_key((string) ($raw['usage_profile'] ?? 'normal'));
            $fields['usage_profile'] = in_array($usage, ['normal','severe','city-heavy','highway'], true) ? $usage : 'normal';
        }

        // Privacy by design: only short masked hints, never full plate/VIN in this table.
        if (!$partial || array_key_exists('plate_hint', $raw)) {
            $hint = preg_replace('/[^\p{L}\p{N}]/u', '', (string) ($raw['plate_hint'] ?? ''));
            $fields['plate_hint'] = mb_substr($hint, -6);
        }
        if (!$partial || array_key_exists('vin_hint', $raw)) {
            $hint = strtoupper(preg_replace('/[^A-Z0-9]/i', '', (string) ($raw['vin_hint'] ?? '')));
            $fields['vin_hint'] = substr($hint, -6);
        }
        if (!$partial || array_key_exists('ownership_started', $raw)) {
            $date = sanitize_text_field((string) ($raw['ownership_started'] ?? ''));
            $fields['ownership_started'] = preg_match('/^\d{4}-\d{2}-\d{2}$/', $date) ? $date : null;
        }

        return $fields;
    }

    public static function rest_add_service_event(WP_REST_Request $request) {
        global $wpdb;
        $user_id = get_current_user_id();
        $garage_id = absint($request['id']);
        if (!self::owned_garage_row($garage_id, $user_id)) {
            return new WP_Error('a3cp_garage_not_found', 'المركبة غير موجودة.', ['status' => 404]);
        }

        $raw = $request->get_json_params();
        if (!is_array($raw)) $raw = [];
        $event_date = sanitize_text_field((string) ($raw['event_date'] ?? current_time('Y-m-d')));
        if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $event_date)) {
            return new WP_Error('a3cp_bad_event_date', 'تاريخ الصيانة غير صالح.', ['status' => 400]);
        }

        $table = $wpdb->prefix . 'a3tal_service_events';
        $ok = $wpdb->insert($table, [
            'user_id' => $user_id,
            'garage_id' => $garage_id,
            'event_type' => sanitize_key((string) ($raw['event_type'] ?? 'service')),
            'event_date' => $event_date,
            'odometer_km' => absint($raw['odometer_km'] ?? 0),
            'title' => sanitize_text_field((string) ($raw['title'] ?? 'صيانة')),
            'details' => sanitize_textarea_field((string) ($raw['details'] ?? '')),
            'cost' => self::sanitize_number($raw['cost'] ?? 0),
            'currency' => sanitize_text_field((string) ($raw['currency'] ?? '')),
            'next_due_km' => absint($raw['next_due_km'] ?? 0),
            'next_due_date' => self::sanitize_date($raw['next_due_date'] ?? null),
            'created_at' => current_time('mysql'),
        ]);
        if (!$ok) return new WP_Error('a3cp_service_event_failed', 'تعذر حفظ سجل الصيانة.', ['status' => 500]);

        return rest_ensure_response(['id' => (int) $wpdb->insert_id, 'created' => true]);
    }

    public static function rest_create_listing(WP_REST_Request $request) {
        $user_id = get_current_user_id();
        $garage_id = absint($request['id']);
        $garage = self::owned_garage_row($garage_id, $user_id);
        if (!$garage || $garage->vehicle_type !== 'car') {
            return new WP_Error('a3cp_garage_car_required', 'يجب اختيار سيارة مملوكة من جراجك.', ['status' => 400]);
        }

        $raw = $request->get_json_params();
        if (!is_array($raw)) $raw = [];
        $price = self::sanitize_number($raw['price'] ?? 0);
        if ($price <= 0) {
            return new WP_Error('a3cp_listing_price_required', 'أدخل سعرًا صالحًا للإعلان.', ['status' => 400]);
        }

        $entity_title = $garage->entity_id ? get_the_title((int) $garage->entity_id) : '';
        $title = $entity_title !== '' ? $entity_title : ($garage->nickname ?: 'سيارة للبيع');
        if ($garage->year) $title .= ' ' . (int) $garage->year;

        $post_id = wp_insert_post([
            'post_type' => 'a3_listing',
            'post_status' => 'pending',
            'post_author' => $user_id,
            'post_title' => sanitize_text_field($title),
            'post_content' => wp_kses_post((string) ($raw['description'] ?? '')),
            'post_excerpt' => sanitize_textarea_field((string) ($raw['summary'] ?? '')),
        ], true);
        if (is_wp_error($post_id)) return $post_id;

        update_post_meta($post_id, '_a3_vehicle_entity_id', (int) $garage->entity_id);
        update_post_meta($post_id, '_a3_listing_year', (int) $garage->year);
        update_post_meta($post_id, '_a3_listing_mileage_km', (int) $garage->odometer_km);
        update_post_meta($post_id, '_a3_listing_price', $price);
        update_post_meta($post_id, '_a3_listing_currency', sanitize_text_field((string) ($raw['currency'] ?? 'EGP')));
        update_post_meta($post_id, '_a3_listing_location', sanitize_text_field((string) ($raw['location'] ?? '')));
        update_post_meta($post_id, '_a3_listing_contact_phone', sanitize_text_field((string) ($raw['phone'] ?? '')));
        update_post_meta($post_id, '_a3_private_plate_hint', (string) $garage->plate_hint);
        update_post_meta($post_id, '_a3_private_vin_hint', (string) $garage->vin_hint);
        update_post_meta($post_id, '_a3_listing_expires_at', gmdate('Y-m-d', time() + 45 * DAY_IN_SECONDS));

        return rest_ensure_response([
            'id' => (int) $post_id,
            'status' => 'pending',
            'message' => 'تم إرسال الإعلان للمراجعة قبل النشر.',
        ]);
    }

    private static function sanitize_date($value): ?string {
        $value = sanitize_text_field((string) $value);
        return preg_match('/^\d{4}-\d{2}-\d{2}$/', $value) ? $value : null;
    }

    public static function protect_listing_publish(string $new_status, string $old_status, WP_Post $post): void {
        if ($post->post_type !== 'a3_listing' || $new_status !== 'publish' || $old_status === 'publish') return;
        if (!current_user_can('edit_others_posts')) return;
        if (!get_post_meta($post->ID, '_a3_listing_expires_at', true)) {
            update_post_meta($post->ID, '_a3_listing_expires_at', gmdate('Y-m-d', time() + 45 * DAY_IN_SECONDS));
        }
    }

    public static function process_due_reminders(): void {
        global $wpdb;
        $table = $wpdb->prefix . 'a3tal_reminders';
        $today = current_time('Y-m-d');
        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE status='active' AND email_opt_in=1 AND due_date IS NOT NULL AND due_date<=%s AND (last_notified_at IS NULL OR last_notified_at<DATE_SUB(NOW(), INTERVAL 7 DAY)) LIMIT 100",
            $today
        ));

        foreach ($rows ?: [] as $row) {
            $user = get_userdata((int) $row->user_id);
            if (!$user || !is_email($user->user_email)) continue;
            wp_mail(
                $user->user_email,
                'تذكير صيانة من أعطال.كوم',
                'موعد قريب: ' . wp_strip_all_tags((string) $row->title)
            );
            $wpdb->update($table, ['last_notified_at' => current_time('mysql')], ['id' => (int) $row->id]);
        }
    }
}
