<?php
if (!defined('ABSPATH')) exit;

final class A3CP_Content_Types {
    private const TYPES = [
        'a3_car' => [
            'singular' => 'سيارة',
            'plural' => 'السيارات',
            'menu' => 'السيارات',
            'slug' => 'cars',
            'rest' => 'a3tal-cars',
        ],
        'a3_motorcycle' => [
            'singular' => 'موتوسيكل',
            'plural' => 'الموتوسيكلات',
            'menu' => 'الموتوسيكلات',
            'slug' => 'motorcycles',
            'rest' => 'a3tal-motorcycles',
        ],
        'a3_dtc' => [
            'singular' => 'كود عطل',
            'plural' => 'أكواد الأعطال DTC',
            'menu' => 'أكواد DTC',
            'slug' => 'dtc',
            'rest' => 'a3tal-dtc',
        ],
        'a3_service_center' => [
            'singular' => 'مركز خدمة',
            'plural' => 'مراكز الخدمة',
            'menu' => 'مراكز الخدمة',
            'slug' => 'service-centers',
            'rest' => 'a3tal-service-centers',
        ],
        'a3_showroom' => [
            'singular' => 'معرض سيارات',
            'plural' => 'معارض السيارات',
            'menu' => 'معارض السيارات',
            'slug' => 'car-showrooms',
            'rest' => 'a3tal-showrooms',
        ],
    ];

    public static function init(): void {
        add_action('init', [__CLASS__, 'register_all'], 5);
        add_filter('query_vars', [__CLASS__, 'query_vars']);
        add_action('pre_get_posts', [__CLASS__, 'filter_entity_archives']);
        add_filter('wp_robots', [__CLASS__, 'robots']);
        add_action('init', [__CLASS__, 'seed_reference_entities'], 40);
        add_action('init', [__CLASS__, 'seed_motorcycle_entities'], 41);
        add_action('a3cp_seed_motorcycles', [__CLASS__, 'seed_motorcycle_entities']);
        add_action('init', [__CLASS__, 'seed_showroom_batch_v1'], 43);
        add_action('a3cp_seed_showrooms_v1', [__CLASS__, 'seed_showroom_batch_v1']);
        add_action('init', [__CLASS__, 'seed_showroom_guides_v1'], 44);
        add_action('a3cp_seed_showroom_guides_v1', [__CLASS__, 'seed_showroom_guides_v1']);
        add_action('init', [__CLASS__, 'seed_showroom_featured_v1'], 45);
        add_action('a3cp_seed_showroom_featured_v1', [__CLASS__, 'seed_showroom_featured_v1']);
        add_action('init', [__CLASS__, 'enrich_showroom_directory_v2'], 46);
        add_action('a3cp_enrich_showrooms_v2', [__CLASS__, 'enrich_showroom_directory_v2']);
        add_action('init', [__CLASS__, 'seed_showroom_custom_media_v2'], 47);
        add_action('a3cp_seed_showroom_custom_media_v2', [__CLASS__, 'seed_showroom_custom_media_v2']);
        add_action('init', [__CLASS__, 'seed_motorcycle_expansion_v2'], 48);
        add_action('a3cp_seed_motorcycle_expansion_v2', [__CLASS__, 'seed_motorcycle_expansion_v2']);
        add_action('init', [__CLASS__, 'seed_motorcycle_guides_v1'], 49);
        add_action('a3cp_seed_motorcycle_guides_v1', [__CLASS__, 'seed_motorcycle_guides_v1']);
    }

    public static function register_all(): void {
        self::register_post_types();
        self::register_taxonomies();
        self::register_meta();
    }

    private static function labels(string $singular, string $plural, string $menu): array {
        return [
            'name' => $plural,
            'singular_name' => $singular,
            'menu_name' => $menu,
            'add_new' => 'إضافة جديد',
            'add_new_item' => 'إضافة ' . $singular,
            'edit_item' => 'تعديل ' . $singular,
            'new_item' => $singular . ' جديد',
            'view_item' => 'عرض ' . $singular,
            'view_items' => 'عرض ' . $plural,
            'search_items' => 'بحث في ' . $plural,
            'not_found' => 'لا توجد نتائج',
            'not_found_in_trash' => 'لا توجد عناصر في سلة المهملات',
            'all_items' => 'كل ' . $plural,
            'archives' => 'أرشيف ' . $plural,
            'attributes' => 'خصائص ' . $singular,
            'featured_image' => 'الصورة الرئيسية',
            'set_featured_image' => 'تعيين الصورة الرئيسية',
            'remove_featured_image' => 'إزالة الصورة الرئيسية',
        ];
    }

    private static function register_post_types(): void {
        foreach (self::TYPES as $type => $cfg) {
            register_post_type($type, [
                'labels' => self::labels($cfg['singular'], $cfg['plural'], $cfg['menu']),
                'public' => true,
                'publicly_queryable' => true,
                'show_ui' => true,
                'show_in_menu' => 'a3tal-platform',
                'show_in_rest' => true,
                'rest_base' => $cfg['rest'],
                'has_archive' => $cfg['slug'],
                'rewrite' => [
                    'slug' => $cfg['slug'],
                    'with_front' => false,
                    'feeds' => false,
                ],
                'supports' => ['title', 'editor', 'excerpt', 'thumbnail', 'revisions'],
                'exclude_from_search' => false,
                'hierarchical' => false,
                'query_var' => true,
                'can_export' => true,
                'delete_with_user' => false,
                'show_in_nav_menus' => true,
                'menu_position' => 25,
            ]);
        }
    }

    private static function tax_args(string $plural, string $singular, bool $hierarchical = false): array {
        return [
            'labels' => [
                'name' => $plural,
                'singular_name' => $singular,
                'search_items' => 'بحث',
                'all_items' => 'الكل',
                'edit_item' => 'تعديل',
                'update_item' => 'تحديث',
                'add_new_item' => 'إضافة جديد',
                'new_item_name' => 'اسم جديد',
                'menu_name' => $plural,
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
        register_taxonomy(
            'a3_brand',
            ['a3_car', 'a3_motorcycle', 'a3_service_center', 'a3_showroom'],
            self::tax_args('الماركات', 'الماركة')
        );

        register_taxonomy(
            'a3_market',
            ['a3_car', 'a3_motorcycle', 'a3_dtc', 'a3_service_center', 'a3_showroom'],
            self::tax_args('الأسواق', 'السوق', true)
        );

        register_taxonomy(
            'a3_car_body',
            ['a3_car'],
            self::tax_args('نوع هيكل السيارة', 'نوع الهيكل')
        );

        register_taxonomy(
            'a3_motorcycle_type',
            ['a3_motorcycle'],
            self::tax_args('نوع الموتوسيكل', 'النوع')
        );

        register_taxonomy(
            'a3_directory_status',
            ['a3_service_center', 'a3_showroom'],
            self::tax_args('حالة الاعتماد', 'حالة الاعتماد')
        );

        register_taxonomy(
            'a3_service_type',
            ['a3_service_center'],
            self::tax_args('أنواع الخدمة', 'الخدمة')
        );

        register_taxonomy(
            'a3_dtc_family',
            ['a3_dtc'],
            self::tax_args('عائلة كود العطل', 'عائلة الكود')
        );
    }

    private static function meta(string $type, string $key, string $data_type, callable $sanitize): void {
        register_post_meta($type, $key, [
            'type' => $data_type,
            'single' => true,
            'show_in_rest' => true,
            'sanitize_callback' => $sanitize,
            'auth_callback' => static fn() => current_user_can('edit_posts'),
        ]);
    }

    private static function register_meta(): void {
        foreach (['a3_car', 'a3_motorcycle'] as $type) {
            self::meta($type, '_a3_year', 'integer', 'absint');
            self::meta($type, '_a3_price_min', 'number', [__CLASS__, 'sanitize_number']);
            self::meta($type, '_a3_price_max', 'number', [__CLASS__, 'sanitize_number']);
            self::meta($type, '_a3_currency', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_engine_cc', 'number', [__CLASS__, 'sanitize_number']);
            self::meta($type, '_a3_power_hp', 'number', [__CLASS__, 'sanitize_number']);
            self::meta($type, '_a3_torque_nm', 'number', [__CLASS__, 'sanitize_number']);
            self::meta($type, '_a3_transmission', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_fuel', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_drivetrain', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_source_url', 'string', 'esc_url_raw');
            self::meta($type, '_a3_source_checked_at', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_related_post_ids', 'string', [__CLASS__, 'sanitize_id_list']);
        }
        self::meta('a3_car', '_a3_seats', 'integer', 'absint');

        self::meta('a3_motorcycle', '_a3_cooling', 'string', 'sanitize_text_field');
        self::meta('a3_motorcycle', '_a3_front_brake', 'string', 'sanitize_text_field');
        self::meta('a3_motorcycle', '_a3_rear_brake', 'string', 'sanitize_text_field');
        self::meta('a3_motorcycle', '_a3_tyre_type', 'string', 'sanitize_text_field');
        self::meta('a3_motorcycle', '_a3_tank_l', 'number', [__CLASS__, 'sanitize_number']);
        self::meta('a3_motorcycle', '_a3_weight_kg', 'number', [__CLASS__, 'sanitize_number']);
        self::meta('a3_motorcycle', '_a3_warranty', 'string', 'sanitize_text_field');
        self::meta('a3_motorcycle', '_a3_use_case', 'string', 'sanitize_text_field');
        self::meta('a3_motorcycle', '_a3_origin_country', 'string', 'sanitize_text_field');

        foreach (['a3_service_center', 'a3_showroom'] as $type) {
            self::meta($type, '_a3_phone', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_whatsapp', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_address', 'string', 'sanitize_textarea_field');
            self::meta($type, '_a3_lat', 'number', [__CLASS__, 'sanitize_number']);
            self::meta($type, '_a3_lng', 'number', [__CLASS__, 'sanitize_number']);
            self::meta($type, '_a3_hours', 'string', 'sanitize_textarea_field');
            self::meta($type, '_a3_official_source_url', 'string', 'esc_url_raw');
            self::meta($type, '_a3_source_checked_at', 'string', 'sanitize_text_field');
        }

        self::meta('a3_showroom', '_a3_email', 'string', 'sanitize_email');
        self::meta('a3_showroom', '_a3_booking_url', 'string', 'esc_url_raw');
        self::meta('a3_showroom', '_a3_maps_query', 'string', 'sanitize_text_field');
        self::meta('a3_showroom', '_a3_services', 'string', 'sanitize_textarea_field');
        self::meta('a3_showroom', '_a3_staff_public', 'string', 'sanitize_textarea_field');
        self::meta('a3_showroom', '_a3_staff_source_url', 'string', 'esc_url_raw');
        self::meta('a3_showroom', '_a3_data_note', 'string', 'sanitize_textarea_field');

        self::meta('a3_dtc', '_a3_dtc_code', 'string', [__CLASS__, 'sanitize_dtc_code']);
        self::meta('a3_dtc', '_a3_dtc_system', 'string', 'sanitize_text_field');
        self::meta('a3_dtc', '_a3_severity', 'string', 'sanitize_key');
        self::meta('a3_dtc', '_a3_drive_advice', 'string', 'sanitize_textarea_field');
        self::meta('a3_dtc', '_a3_code_scope', 'string', 'sanitize_key');
        self::meta('a3_dtc', '_a3_manufacturer', 'string', 'sanitize_text_field');
        self::meta('a3_dtc', '_a3_source_url', 'string', 'esc_url_raw');
        self::meta('a3_dtc', '_a3_source_checked_at', 'string', 'sanitize_text_field');
        self::meta('a3_dtc', '_a3_related_post_ids', 'string', [__CLASS__, 'sanitize_id_list']);
    }

    public static function sanitize_number($value): float {
        return is_numeric($value) ? (float) $value : 0.0;
    }

    public static function sanitize_id_list($value): string {
        $parts = preg_split('/[^0-9]+/', (string) $value);
        $ids = array_values(array_unique(array_filter(array_map('absint', (array) $parts))));
        return implode(',', $ids);
    }

    public static function sanitize_dtc_code($value): string {
        $value = strtoupper(preg_replace('/[^A-Z0-9]/i', '', (string) $value));
        return substr($value, 0, 8);
    }

    public static function seed_core_terms(): void {
        self::seed('a3_directory_status', [
            'official' => 'معتمد رسميًا',
            'verified' => 'موثّق من أعطال',
            'independent' => 'مستقل',
        ]);
        self::seed('a3_dtc_family', [
            'p-powertrain' => 'P — المحرك وناقل الحركة',
            'b-body' => 'B — أنظمة الهيكل والمقصورة',
            'c-chassis' => 'C — الشاسيه والتعليق والفرامل',
            'u-network' => 'U — الشبكات والاتصالات',
        ]);
        self::seed('a3_car_body', [
            'sedan' => 'سيدان',
            'suv' => 'SUV',
            'crossover' => 'كروس أوفر',
            'hatchback' => 'هاتشباك',
            'coupe' => 'كوبيه',
            'pickup' => 'بيك أب',
            'mpv' => 'MPV',
            'van' => 'فان',
        ]);
        self::seed('a3_motorcycle_type', [
            'scooter' => 'سكوتر',
            'commuter' => 'اقتصادي / تنقل يومي',
            'sport' => 'رياضي',
            'naked' => 'Naked',
            'cruiser' => 'Cruiser',
            'adventure' => 'Adventure',
            'touring' => 'Touring',
            'off-road' => 'Off-road',
            'electric' => 'كهربائي',
        ]);
        self::seed('a3_market', [
            'egypt' => 'مصر',
            'saudi-arabia' => 'السعودية',
            'uae' => 'الإمارات',
            'kuwait' => 'الكويت',
            'bahrain' => 'البحرين',
        ]);
    }

    private static function seed(string $taxonomy, array $terms): void {
        foreach ($terms as $slug => $name) {
            if (!term_exists($slug, $taxonomy)) {
                wp_insert_term($name, $taxonomy, ['slug' => $slug]);
            }
        }
    }

    public static function query_vars(array $vars): array {
        $vars[] = 'brand';
        $vars[] = 'market';
        $vars[] = 'year';
        $vars[] = 'vehicle_type';
        $vars[] = 'code';
        $vars[] = 'directory_status';
        return $vars;
    }

    public static function filter_entity_archives(WP_Query $query): void {
        if (is_admin() || !$query->is_main_query()) return;

        $type = $query->get('post_type');
        if (is_array($type)) {
            $type = reset($type);
        }
        $type = (string) $type;

        if (in_array($type, ['a3_car', 'a3_motorcycle'], true)) {
            $query->set('posts_per_page', 24);
            $query->set('orderby', ['modified' => 'DESC', 'title' => 'ASC']);

            $tax_query = [];
            $brand = sanitize_title((string) get_query_var('brand'));
            $market = sanitize_title((string) get_query_var('market'));
            if ($brand !== '') {
                $tax_query[] = ['taxonomy' => 'a3_brand', 'field' => 'slug', 'terms' => $brand];
            }
            if ($market !== '') {
                $tax_query[] = ['taxonomy' => 'a3_market', 'field' => 'slug', 'terms' => $market];
            }

            $vehicle_type = sanitize_title((string) get_query_var('vehicle_type'));
            if ($vehicle_type !== '') {
                $taxonomy = $type === 'a3_car' ? 'a3_car_body' : 'a3_motorcycle_type';
                $tax_query[] = ['taxonomy' => $taxonomy, 'field' => 'slug', 'terms' => $vehicle_type];
            }

            if ($tax_query) {
                $query->set('tax_query', count($tax_query) > 1 ? array_merge(['relation' => 'AND'], $tax_query) : $tax_query);
            }

            $year = absint(get_query_var('year'));
            if ($year >= 1950 && $year <= 2100) {
                $query->set('meta_query', [[
                    'key' => '_a3_year',
                    'value' => $year,
                    'compare' => '=',
                    'type' => 'NUMERIC',
                ]]);
            }
            return;
        }

        if ($type === 'a3_dtc') {
            $query->set('posts_per_page', 40);
            $query->set('orderby', 'title');
            $query->set('order', 'ASC');

            $code = self::sanitize_dtc_code((string) get_query_var('code'));
            if ($code !== '') {
                $query->set('meta_query', [[
                    'key' => '_a3_dtc_code',
                    'value' => $code,
                    'compare' => '=',
                ]]);
            }
            return;
        }

        if (in_array($type, ['a3_service_center', 'a3_showroom'], true)) {
            $query->set('posts_per_page', 24);
            $query->set('orderby', ['modified' => 'DESC', 'title' => 'ASC']);

            $tax_query = [];
            $brand = sanitize_title((string) get_query_var('brand'));
            $market = sanitize_title((string) get_query_var('market'));
            $status = sanitize_title((string) get_query_var('directory_status'));

            if ($brand !== '') {
                $tax_query[] = ['taxonomy' => 'a3_brand', 'field' => 'slug', 'terms' => $brand];
            }
            if ($market !== '') {
                $tax_query[] = ['taxonomy' => 'a3_market', 'field' => 'slug', 'terms' => $market];
            }
            if ($status !== '') {
                $tax_query[] = ['taxonomy' => 'a3_directory_status', 'field' => 'slug', 'terms' => $status];
            }
            if ($tax_query) {
                $query->set('tax_query', count($tax_query) > 1 ? array_merge(['relation' => 'AND'], $tax_query) : $tax_query);
            }
        }
    }

    public static function seed_reference_entities(): void {
        if ((string) get_option('a3cp_dtc_reference_seed_v1') === 'done') return;

        $items = [
            [
                'code' => 'P0420',
                'slug' => 'p0420-catalyst-efficiency-bank-1',
                'title' => 'P0420 — كفاءة المحول الحفاز أقل من الحد Bank 1',
                'system' => 'المحرك / الانبعاثات',
                'severity' => 'medium',
                'drive' => 'يمكن أن تستمر السيارة في العمل، لكن تجاهل السبب لفترة طويلة قد يخفي مشكلة احتراق أو عادم أعمق. شخّص السبب قبل استبدال المحول الحفاز.',
            ],
            [
                'code' => 'P0430',
                'slug' => 'p0430-catalyst-efficiency-bank-2',
                'title' => 'P0430 — كفاءة المحول الحفاز أقل من الحد Bank 2',
                'system' => 'المحرك / الانبعاثات',
                'severity' => 'medium',
                'drive' => 'لا يعني الكود وحده أن المحول الحفاز تالف. افحص أسباب الاحتراق وحساسات الأكسجين وتسريب العادم قبل قرار الاستبدال.',
            ],
            [
                'code' => 'P0335',
                'slug' => 'p0335-crankshaft-position-sensor',
                'title' => 'P0335 — عطل دائرة حساس موضع عمود الكرنك CKP',
                'system' => 'المحرك / إدارة الإشعال والحقن',
                'severity' => 'high',
                'drive' => 'قد يسبب الكود تقطيعًا أو توقف المحرك أو عدم إعادة التشغيل. إذا ظهرت أعراض توقف مفاجئ فالأولوية للتشخيص بدل مواصلة القيادة.',
            ],
            [
                'code' => 'P0342',
                'slug' => 'dtc-p0342-chevrolet',
                'title' => 'P0342 — إشارة منخفضة في دائرة حساس الكامة A',
                'system' => 'المحرك / حساس موضع عمود الكامة',
                'severity' => 'medium',
                'drive' => 'ابدأ بفحص التغذية والأرضي والأسلاك والإشارة. الكود لا يثبت وحده أن حساس الكامة نفسه تالف.',
            ],
        ];

        $all_ready = true;

        foreach ($items as $item) {
            $existing = get_posts([
                'post_type' => 'a3_dtc',
                'post_status' => 'any',
                'posts_per_page' => 1,
                'fields' => 'ids',
                'meta_key' => '_a3_dtc_code',
                'meta_value' => $item['code'],
            ]);
            if ($existing) continue;

            $source = get_page_by_path($item['slug'], OBJECT, 'post');
            if (!$source instanceof WP_Post || $source->post_status !== 'publish') {
                $all_ready = false;
                continue;
            }

            $excerpt = get_the_excerpt($source);
            if (!$excerpt) {
                $excerpt = wp_trim_words(wp_strip_all_tags((string) $source->post_content), 34);
            }

            $content = '<p>هذه صفحة مرجعية سريعة للكود <strong>' . esc_html($item['code']) . '</strong> داخل قاعدة أكواد أعطال.كوم. تم ربطها بالشرح الفني المنشور بالفعل حتى لا نكرر نفس نية البحث في صفحتين.</p>';
            $content .= '<p><a href="' . esc_url(get_permalink($source)) . '">اقرأ الشرح الكامل للكود وخطوات التشخيص ←</a></p>';

            $id = wp_insert_post([
                'post_type' => 'a3_dtc',
                'post_status' => 'publish',
                'post_title' => $item['title'],
                'post_name' => strtolower($item['code']),
                'post_excerpt' => wp_strip_all_tags($excerpt),
                'post_content' => $content,
            ], true);

            if (is_wp_error($id)) {
                $all_ready = false;
                continue;
            }

            update_post_meta($id, '_a3_dtc_code', $item['code']);
            update_post_meta($id, '_a3_dtc_system', $item['system']);
            update_post_meta($id, '_a3_severity', $item['severity']);
            update_post_meta($id, '_a3_drive_advice', $item['drive']);
            update_post_meta($id, '_a3_code_scope', 'generic');
            update_post_meta($id, '_a3_related_post_ids', (string) $source->ID);
            update_post_meta($id, '_a3_entity_stub', '1');
            wp_set_object_terms($id, 'p-powertrain', 'a3_dtc_family', false);
        }

        if ($all_ready) {
            update_option('a3cp_dtc_reference_seed_v1', 'done', false);
        }
    }

    public static function seed_motorcycle_entities(): void {
        if ((string) get_option('a3cp_motorcycle_seed_v1') === 'done') return;

        if (!term_exists('tvs', 'a3_brand')) {
            wp_insert_term('TVS', 'a3_brand', ['slug' => 'tvs']);
        }

        $items = [
            [
                'slug' => 'tvs-apache-rtr-160-4v-egypt',
                'title' => 'TVS Apache RTR 160 4V',
                'type' => 'sport',
                'engine' => 160,
                'transmission' => 'يدوي 5 سرعات',
                'fuel' => 'بنزين',
                'source' => 'https://www.tvsmotor.com/ar/eg/our-products/tvs-apache-rtr-160-4v',
                'excerpt' => 'دراجة رياضية بمحرك 4 صمامات مبرد بالزيت، وسعة فعلية 159.7 سم³، وناقل حركة من 5 سرعات بحسب TVS مصر.',
                'content' => '<h2>بيانات سريعة</h2><ul><li>السعة الفعلية: 159.7 سم³.</li><li>محرك 4 أشواط مبرد بالزيت.</li><li>ناقل حركة 5 سرعات.</li><li>خزان وقود 12 لتر.</li></ul><p>هذه صفحة بيانات أولية مرتبطة بالمصدر الرسمي لـTVS مصر، وسيتم توسيعها بالمراجعة والصيانة والأعطال وقطع الغيار قبل فتحها للفهرسة.</p>',
            ],
            [
                'slug' => 'tvs-raider-125-egypt',
                'title' => 'TVS Raider 125',
                'type' => 'commuter',
                'engine' => 125,
                'transmission' => 'يدوي 5 سرعات',
                'fuel' => 'بنزين',
                'source' => 'https://www.tvsmotor.com/ar/eg/our-products/tvs-raider',
                'excerpt' => 'موتوسيكل تنقل يومي بمحرك سعة فعلية 124.76 سم³، وقدرة معلنة 12.9 حصان وناقل 5 سرعات بحسب TVS مصر.',
                'content' => '<h2>بيانات سريعة</h2><ul><li>السعة الفعلية: 124.76 سم³.</li><li>القدرة المعلنة: 12.9 حصان عند 8000 دورة/دقيقة.</li><li>ناقل حركة 5 سرعات.</li><li>خزان وقود 10 لترات.</li></ul><p>هذه صفحة بيانات أولية من المصدر الرسمي لـTVS مصر، وسيتم استكمالها بالمراجعة والصيانة والأعطال وقطع الغيار.</p>',
            ],
            [
                'slug' => 'tvs-ntorq-125-re-egypt',
                'title' => 'TVS Ntorq 125 RE',
                'type' => 'scooter',
                'engine' => 125,
                'transmission' => 'أوتوماتيك',
                'fuel' => 'بنزين',
                'source' => 'https://www.tvsmotor.com/ar/eg/our-products/tvs-ntorq-125-re',
                'excerpt' => 'سكوتر بمحرك 124.79 سم³ ثلاثي الصمامات، بقدرة 6.9 كيلوواط وعزم 10.5 نيوتن متر بحسب TVS مصر.',
                'content' => '<h2>بيانات سريعة</h2><ul><li>السعة الفعلية: 124.79 سم³.</li><li>القدرة المعلنة: 6.9 كيلوواط عند 7500 دورة/دقيقة.</li><li>العزم المعلن: 10.5 نيوتن متر عند 5500 دورة/دقيقة.</li><li>خزان الوقود 5 لترات.</li></ul><p>هذه صفحة بيانات أولية من المصدر الرسمي لـTVS مصر، وسيتم استكمالها بالمراجعة والصيانة والأعطال وقطع الغيار.</p>',
            ],
        ];

        $all_ready = true;

        foreach ($items as $item) {
            $existing = get_page_by_path($item['slug'], OBJECT, 'a3_motorcycle');
            if ($existing instanceof WP_Post) continue;

            $id = wp_insert_post([
                'post_type' => 'a3_motorcycle',
                'post_status' => 'publish',
                'post_title' => $item['title'],
                'post_name' => $item['slug'],
                'post_excerpt' => $item['excerpt'],
                'post_content' => $item['content'],
            ], true);

            if (is_wp_error($id)) {
                $all_ready = false;
                continue;
            }

            update_post_meta($id, '_a3_engine_cc', $item['engine']);
            update_post_meta($id, '_a3_transmission', $item['transmission']);
            update_post_meta($id, '_a3_fuel', $item['fuel']);
            update_post_meta($id, '_a3_source_url', $item['source']);
            update_post_meta($id, '_a3_source_checked_at', '2026-10-04');
            update_post_meta($id, '_a3_entity_stub', '1');

            wp_set_object_terms($id, 'tvs', 'a3_brand', false);
            wp_set_object_terms($id, 'egypt', 'a3_market', false);
            wp_set_object_terms($id, $item['type'], 'a3_motorcycle_type', false);
        }

        if ($all_ready) {
            update_option('a3cp_motorcycle_seed_v1', 'done', false);
        }
    }

    public static function seed_showroom_batch_v1(): void {
        if ((string) get_option('a3cp_showroom_seed_v1') === 'done') return;

        foreach ([
            'toyota' => 'Toyota',
            'mg' => 'MG',
            'chery' => 'Chery',
        ] as $slug => $name) {
            if (!term_exists($slug, 'a3_brand')) {
                wp_insert_term($name, 'a3_brand', ['slug' => $slug]);
            }
        }

        $items = [
            [
                'slug' => 'toyota-egypt-cairo-festival-city-showroom',
                'title' => 'معرض تويوتا كايرو فيستيفال سيتي',
                'brand' => 'toyota',
                'address' => 'كايرو فيستيفال سيتي، الطريق الدائري، القاهرة، مصر',
                'phone' => '16550',
                'hours' => 'تحقق من مواعيد العمل الحالية عبر تويوتا مصر قبل الزيارة.',
                'source' => 'https://toyota.com.eg/ar/locations',
                'intro' => 'يظهر موقع تويوتا كايرو فيستيفال سيتي ضمن شبكة تويوتا مصر الرسمية. وجوده داخل Cairo Festival City يجعله من نقاط البيع المهمة في شرق القاهرة للراغبين في معاينة سيارات تويوتا الجديدة والاستفسار عن الحجز والتسليم والتمويل.',
                'visit' => 'إذا كان هدفك تجربة قيادة أو مشاهدة فئة بعينها، تواصل مسبقًا للتأكد من توافر الموديل واللون والفئة داخل صالة العرض في يوم الزيارة. وجود السيارة على الموقع الرسمي لا يعني أن كل التجهيزات متاحة للعرض في نفس اللحظة.',
            ],
            [
                'slug' => 'toyota-egypt-sheikh-zayed-showroom',
                'title' => 'معرض تويوتا الشيخ زايد',
                'brand' => 'toyota',
                'address' => 'محور 26 يوليو، الشيخ زايد، داخل محطة Chillout، الجيزة',
                'phone' => '16550',
                'hours' => 'تحقق من مواعيد العمل الحالية عبر تويوتا مصر قبل الزيارة.',
                'source' => 'https://toyota.com.eg/ar/locations',
                'intro' => 'فرع تويوتا الشيخ زايد مدرج ضمن مواقع Toyota Egypt الرسمية ويخدم الشيخ زايد و6 أكتوبر وغرب القاهرة. يمكن استخدامه للاستفسار عن السيارات المتاحة والعروض والحجز، مع ضرورة تأكيد التوافر قبل التحرك.',
                'visit' => 'اطلب عرض سعر مكتوب يوضح الفئة وسنة الموديل وموعد التسليم وأي تكاليف إضافية مرتبطة بالترخيص أو التأمين أو الإضافات الاختيارية. المقارنة بين السعر النقدي والتمويل يجب أن تكون على أساس التكلفة الإجمالية لا القسط الشهري فقط.',
            ],
            [
                'slug' => 'toyota-egypt-madinaty-showroom',
                'title' => 'معرض تويوتا مدينتي',
                'brand' => 'toyota',
                'address' => 'بنزينة وطنية، أمام بوابة مدينتي 1، القاهرة',
                'phone' => '16550',
                'hours' => 'تحقق من مواعيد العمل الحالية عبر تويوتا مصر قبل الزيارة.',
                'source' => 'https://toyota.com.eg/ar/locations',
                'intro' => 'تدرج تويوتا مصر موقع مدينتي ضمن شبكتها الرسمية. الموقع مناسب لسكان مدينتي والشروق والقاهرة الجديدة عند البحث عن سيارة تويوتا جديدة أو الاستفسار عن الحجز والتوافر.',
                'visit' => 'إذا كنت تريد Test Drive، احجز الموعد مسبقًا وحدد الموديل المطلوب. اسأل أيضًا عن مدة التسليم المكتوبة وسياسة استرداد الحجز إذا تغير السعر أو تأخر التسليم.',
            ],
            [
                'slug' => 'toyota-egypt-abbassia-showroom',
                'title' => 'معرض تويوتا العباسية',
                'brand' => 'toyota',
                'address' => '10 شارع المستشفى اليوناني، السرايات، الوايلي، القاهرة',
                'phone' => '16550',
                'hours' => 'تحقق من مواعيد العمل الحالية عبر تويوتا مصر قبل الزيارة.',
                'source' => 'https://toyota.com.eg/ar/locations',
                'intro' => 'فرع تويوتا العباسية من المواقع الرسمية التي تذكرها Toyota Egypt في القاهرة. العنوان الرسمي المتاح هو 10 شارع المستشفى اليوناني بمنطقة السرايات في الوايلي.',
                'visit' => 'جهز قائمة قصيرة بالموديلات والفئات التي تقارن بينها واسأل عن فرق التجهيزات الفعلي وليس اسم الفئة فقط. عند الحجز احتفظ بنسخة من إيصال الدفع وشروط التسليم وأي ملحقات متفق عليها.',
            ],
            [
                'slug' => 'mg-mansour-new-cairo-showroom',
                'title' => 'معرض MG منصور القاهرة الجديدة',
                'brand' => 'mg',
                'address' => 'Chillout – Triumph، الطريق الدائري، القطامية، القاهرة',
                'phone' => '16424',
                'hours' => 'السبت 10:00 ص–10:00 م، الأحد إلى الخميس 9:00 ص–10:00 م، الجمعة 2:00 م–10:00 م.',
                'source' => 'https://www.mgmotor.com.eg/locations-showrooms/',
                'intro' => 'تدرج MG Motor Egypt فرع منصور القاهرة الجديدة كمعرض رسمي ضمن شبكة منصور MG. الصفحة الرسمية تنشر العنوان ورقم الاتصال ومواعيد العمل، لذلك تظهر حالة الفرع هنا كمعتمد رسميًا.',
                'visit' => 'قبل دفع الحجز اطلب عرض سعر واضح يذكر اسم الفئة وسنة الموديل واللون وموعد التسليم وأي مصاريف إدارية. وإذا كنت تريد تجربة قيادة فاطلب تأكيد الموديل المتاح للتجربة والموعد قبل الزيارة.',
            ],
            [
                'slug' => 'mg-mansour-madinaty-showroom',
                'title' => 'معرض MG منصور مدينتي',
                'brand' => 'mg',
                'address' => 'Chillout، مدينتي، طريق القاهرة السويس عند بوابات التحصيل',
                'phone' => '16424',
                'hours' => 'السبت 10:00 ص–10:00 م، الأحد إلى الخميس 9:00 ص–10:00 م، الجمعة 2:00 م–10:00 م.',
                'source' => 'https://www.mgmotor.com.eg/locations-showrooms/',
                'intro' => 'معرض منصور MG مدينتي مدرج رسميًا ضمن شبكة MG Motor Egypt. موقعه على طريق القاهرة السويس يخدم مدينتي والشروق وشرق القاهرة ويتيح الاستفسار عن موديلات MG والحجز والعروض.',
                'visit' => 'قارن بين الفئات على أساس التجهيزات المهمة لك فعلًا مثل أنظمة الأمان والمحرك والضمان، وليس على فرق السعر وحده. اسأل عن السعر النهائي وقت التسليم لأن الشركة نفسها توضح أن السعر النهائي يتحدد عند التسليم.',
            ],
            [
                'slug' => 'mg-mansour-smouha-showroom',
                'title' => 'معرض MG منصور سموحة',
                'brand' => 'mg',
                'address' => '90 شارع فوزي معاذ، سموحة، الإسكندرية',
                'phone' => '16424',
                'hours' => 'السبت 11:00 ص–10:00 م، الأحد إلى الخميس 9:00 ص–10:00 م، الجمعة 2:00 م–10:00 م.',
                'source' => 'https://www.mgmotor.com.eg/locations-showrooms/',
                'intro' => 'فرع منصور MG سموحة هو معرض MG الرسمي المدرج في الإسكندرية على موقع MG Motor Egypt، وعنوانه 90 شارع فوزي معاذ في سموحة.',
                'visit' => 'اسأل قبل الزيارة عن السيارة المعروضة فعليًا واللون والفئة، ثم دوّن السعر النقدي وسعر التمويل والدفعة المقدمة والتأمين والمصاريف الإدارية كل بند منفصل حتى تكون المقارنة عادلة.',
            ],
            [
                'slug' => 'mg-mansour-mansoura-showroom',
                'title' => 'معرض MG منصور المنصورة',
                'brand' => 'mg',
                'address' => '44 شارع عبد السلام عارف، طريق المجزر، بجوار سيراميكا كليوباترا، المنصورة',
                'phone' => '16424',
                'hours' => 'السبت 11:00 ص–10:00 م، الأحد إلى الخميس 9:00 ص–10:00 م، الجمعة 2:00 م–10:00 م.',
                'source' => 'https://www.mgmotor.com.eg/locations-showrooms/',
                'intro' => 'تدرج MG Motor Egypt معرض منصور المنصورة ضمن شبكة معارضها الرسمية في الدقهلية، مع نشر العنوان ورقم التواصل ومواعيد العمل.',
                'visit' => 'إذا كانت السيارة غير موجودة للمعاينة، لا تعتمد على صور الكتالوج وحدها. اطلب موعد وصول سيارة عرض أو تجربة قيادة، وتأكد من مواصفات الفئة المصرية لأن التجهيزات قد تختلف بين الأسواق.',
            ],
            [
                'slug' => 'chery-gb-abbas-el-akkad-showroom',
                'title' => 'معرض شيري GB عباس العقاد',
                'brand' => 'chery',
                'address' => '51 شارع عباس العقاد، مدينة نصر، القاهرة',
                'phone' => '16661',
                'hours' => 'السبت إلى الأربعاء 9:00 ص–10:00 م، الخميس 9:00 ص–11:00 م، الجمعة 2:00 م–11:00 م.',
                'source' => 'https://chery-eg.com/en/find_us',
                'intro' => 'يعرض موقع Chery Egypt الرسمي فرع GB عباس العقاد ضمن شبكة شيري في مصر، مع العنوان ورقم التواصل ومواعيد العمل المنشورة.',
                'visit' => 'قبل الحجز اسأل عن الفئة وسنة الموديل والضمان وموعد التسليم المكتوب. ولأن شيري تطرح أكثر من SUV وسيدان، المقارنة داخل نفس العلامة مهمة قبل الانتقال مباشرة إلى قرار الشراء.',
            ],
            [
                'slug' => 'chery-kernel-fifth-settlement-showroom',
                'title' => 'معرض شيري Kernel التجمع الخامس',
                'brand' => 'chery',
                'address' => '59 الحي الأول، مركز مدينة القاهرة الجديدة، مجمع البنوك، القاهرة',
                'phone' => '15050',
                'hours' => 'السبت إلى الأربعاء 9:00 ص–10:00 م، الخميس 9:00 ص–11:00 م، الجمعة 2:00 م–11:00 م.',
                'source' => 'https://chery-eg.com/en/find_us',
                'intro' => 'يظهر Chery Kernel 5th Settlement في دليل Chery Egypt الرسمي بالقاهرة الجديدة، مع عنوانه داخل مجمع البنوك ورقم الاتصال ومواعيد العمل.',
                'visit' => 'أكد مسبقًا الموديل المتاح للعرض أو تجربة القيادة، واسأل عن السعر النهائي والضمان ومصاريف التسجيل وأي عروض تمويل. وجود عرض تسويقي لا يعني بالضرورة أنه الأنسب بعد حساب التكلفة الإجمالية.',
            ],
        ];

        $all_ready = true;

        foreach ($items as $item) {
            $existing = get_page_by_path($item['slug'], OBJECT, 'a3_showroom');
            if ($existing instanceof WP_Post) continue;

            $content = '<h2>عن ' . esc_html($item['title']) . '</h2>';
            $content .= '<p>' . esc_html($item['intro']) . '</p>';
            $content .= '<h2>ماذا تفعل قبل زيارة المعرض؟</h2>';
            $content .= '<p>' . esc_html($item['visit']) . '</p>';
            $content .= '<ul><li>اتصل أولًا لتأكيد الموديل والفئة واللون المتاحين للمعاينة.</li><li>اطلب السعر النقدي والتكلفة الإجمالية للتمويل كلٌ على حدة.</li><li>ثبّت موعد التسليم وشروط الحجز والاسترداد كتابةً.</li><li>عند تجربة القيادة ركّز على الرؤية والراحة والفرامل والعزل وسهولة الركن، وليس التسارع فقط.</li></ul>';
            $content .= '<h2>كيف نتحقق من حالة المعرض؟</h2>';
            $content .= '<p>حالة «معتمد رسميًا» في أعطال.كوم تعني أن المعرض ظاهر في دليل العلامة الرسمي وقت آخر مراجعة. لا تعني الحالة ضمان السعر أو المخزون أو تجربة العميل، لأن هذه التفاصيل تتغير ويجب تأكيدها مباشرة قبل الشراء.</p>';
            $content .= '<h2>قبل دفع الحجز</h2>';
            $content .= '<p>راجع اسم الشركة في إيصال الحجز، رقم الشاسيه عند تخصيص السيارة، سنة الموديل، الفئة، اللون، قيمة الدفعة، موعد التسليم، وسياسة رد المبلغ. لا تعتمد على وعد شفهي إذا كان البند مؤثرًا في قرار الشراء.</p>';

            $id = wp_insert_post([
                'post_type' => 'a3_showroom',
                'post_status' => 'publish',
                'post_title' => $item['title'],
                'post_name' => $item['slug'],
                'post_excerpt' => wp_trim_words(wp_strip_all_tags($item['intro'] . ' ' . $item['visit']), 34),
                'post_content' => $content,
            ], true);

            if (is_wp_error($id)) {
                $all_ready = false;
                continue;
            }

            update_post_meta($id, '_a3_phone', $item['phone']);
            update_post_meta($id, '_a3_address', $item['address']);
            update_post_meta($id, '_a3_hours', $item['hours']);
            update_post_meta($id, '_a3_official_source_url', $item['source']);
            update_post_meta($id, '_a3_source_checked_at', '2026-10-04');

            wp_set_object_terms($id, $item['brand'], 'a3_brand', false);
            wp_set_object_terms($id, 'egypt', 'a3_market', false);
            wp_set_object_terms($id, 'official', 'a3_directory_status', false);
        }

        if ($all_ready) {
            update_option('a3cp_showroom_seed_v1', 'done', false);
        }
    }

    public static function seed_showroom_guides_v1(): void {
        if ((string) get_option('a3cp_showroom_guides_seed_v1') === 'done') return;

        $term = term_exists('car-showrooms-guide', 'category');
        if (!$term) {
            $term = wp_insert_term('دليل معارض السيارات', 'category', [
                'slug' => 'car-showrooms-guide',
                'description' => 'أدلة الشراء من معارض السيارات والحجز والاستلام وتجربة القيادة والتمويل.',
            ]);
        }
        if (is_wp_error($term)) return;
        $cat_id = is_array($term) ? (int) $term['term_id'] : (int) $term;

        $guides = [
            [
                'slug' => 'dealer-vs-authorized-distributor-vs-private-showroom-egypt',
                'title' => 'الفرق بين الوكيل والموزع المعتمد والمعرض الخاص في مصر',
                'excerpt' => 'افهم الفرق بين الوكيل والموزع المعتمد والمعرض الخاص قبل شراء سيارة جديدة، ومتى تكون صفة الاعتماد مهمة فعلًا.',
                'content' => '<h2>ليه لازم تعرف أنت بتشتري من مين؟</h2><p>اسم المعرض وحده لا يكفي لتحديد علاقته بالعلامة. قد تشتري من الوكيل أو من موزع معتمد ظاهر في شبكة العلامة أو من معرض مستقل يبيع سيارات من أكثر من مصدر. الفارق لا يعني تلقائيًا أن خيارًا أفضل دائمًا، لكنه يغيّر طريقة التحقق من السعر والتجهيز والضمان وموعد التسليم.</p><h2>الوكيل أو الشركة الرسمية</h2><p>هو الكيان الذي يمثل العلامة في السوق المحلي أو يدير التوزيع الرسمي لها. أفضل طريقة للتحقق هي البدء من موقع العلامة نفسه وليس إعلان المعرض. تويوتا مصر وMG Motor Egypt وشيري مصر تنشر أدلة مواقع وفروع يمكن استخدامها كمرجع مباشر.</p><h2>الموزع المعتمد</h2><p>الموزع المعتمد جهة يذكرها الوكيل أو العلامة ضمن شبكة البيع. عند ظهور اسم المعرض في الدليل الرسمي يمكنك اعتبار حالة الاعتماد مثبتة وقت المراجعة، لكن السعر والمخزون والعروض تحتاج تأكيدًا منفصلًا لأنها متغيرة.</p><h2>المعرض الخاص أو المستقل</h2><p>قد يملك سيارات جاهزة للتسليم أو عروضًا مختلفة، لكنه ليس بالضرورة جزءًا من شبكة العلامة. قبل الحجز اسأل عن مصدر السيارة والفاتورة والضمان وسنة الموديل وتاريخ الإنتاج، ولا تخلط بين عبارة «متخصص في العلامة» و«موزع معتمد».</p><h2>إيه اللي تقارنه قبل القرار؟</h2><ul><li>السعر النهائي وليس الرقم المعلن فقط.</li><li>الفئة وسنة الموديل واللون ورقم الشاسيه عند التخصيص.</li><li>موعد التسليم المكتوب وسياسة الحجز.</li><li>الضمان ومكان تنفيذ الصيانة.</li><li>التأمين والترخيص والإضافات الاختيارية.</li></ul><h2>الخلاصة</h2><p>ابدأ من دليل العلامة الرسمي لتعرف حالة الجهة، ثم قارن العرض نفسه. الاعتماد يثبت العلاقة بالشبكة الرسمية لكنه لا يغني عن قراءة عرض السعر والعقد ومراجعة السيارة عند الاستلام.</p><p><strong>مصادر تحقق مفيدة:</strong> دليل مواقع Toyota Egypt، ودليل معارض MG Motor Egypt، ودليل Chery Egypt.</p>',
            ],
            [
                'slug' => 'how-to-verify-car-showroom-authorized-egypt',
                'title' => 'كيف تتأكد أن معرض السيارات معتمد رسميًا؟',
                'excerpt' => 'خطوات عملية للتحقق من اعتماد معرض السيارات قبل دفع الحجز، من المصدر الرسمي للعلامة حتى بيانات الفاتورة.',
                'content' => '<h2>ما تعتمدش على كلمة «معتمد» في الإعلان</h2><p>أسهل خطوة للتحقق هي البحث عن اسم المعرض أو الفرع داخل موقع العلامة الرسمي. وجود شعار كبير على الواجهة أو صفحة فيسبوك لا يثبت وحده أن المكان جزء من شبكة البيع الحالية.</p><h2>1. افتح Dealer Locator الرسمي</h2><p>ابحث في صفحة الفروع أو Find Us التابعة للعلامة. إذا وجدت اسم الجهة والعنوان ورقم الهاتف متطابقين، عندها يكون عندك مرجع مباشر يمكن الرجوع إليه. أعطال.كوم يستخدم نفس المبدأ عند منح حالة «معتمد رسميًا» داخل دليل المعارض.</p><h2>2. طابق البيانات مش الاسم فقط</h2><p>بعض الأسماء التجارية تتكرر أو يكون لها أكثر من فرع. طابق المدينة والعنوان ورقم الهاتف، خصوصًا قبل تحويل مبلغ حجز.</p><h2>3. اطلب عرض سعر مكتوب</h2><p>العرض الجيد يحدد الموديل والفئة وسنة السيارة والسعر وطريقة الدفع ومدة صلاحية العرض. إذا كان بند مهم في القرار غير مكتوب، اسأل عنه قبل الدفع وليس بعده.</p><h2>4. اسأل عن الجهة التي ستصدر الفاتورة</h2><p>اعرف اسم الشركة التي سيصدر منها إيصال الحجز أو الفاتورة وتأكد أنه نفس الطرف الذي تتعامل معه. لا ترسل أموالًا إلى حساب شخصي لمجرد أن المحادثة تحمل لوجو معروف.</p><h2>5. تحقق مرة ثانية قبل الاستلام</h2><p>الاعتماد لا يمنع الأخطاء في الفئة أو اللون أو التجهيز. عند تخصيص السيارة طابق البيانات المكتوبة مع السيارة نفسها ورقم الشاسيه والمستندات.</p><h2>إشارة حمراء مهمة</h2><p>إذا رفض المعرض توضيح صفته أو مصدر السيارة أو الجهة التي ستصدر الفاتورة، فدي علامة كافية إنك ما تستعجلش. القرار الجيد يحب الورق الواضح، مش الحكايات الحلوة.</p>',
            ],
            [
                'slug' => 'new-car-delivery-checklist-egypt',
                'title' => 'Checklist استلام سيارة زيرو من المعرض',
                'excerpt' => 'قائمة عملية لاستلام سيارة جديدة من المعرض: الهيكل، الإطارات، العدادات، التجهيزات، المستندات ورقم الشاسيه.',
                'content' => '<h2>لا تستلم السيارة على عجل</h2><p>يوم الاستلام بيكون مليان حماس وتصوير ومفاتيح لامعة، وده تحديدًا الوقت اللي ممكن تعدّي فيه تفصيلة تزعلك بعدين. خصص وقتًا هادئًا للفحص قبل مغادرة المعرض.</p><h2>فحص الهيكل الخارجي</h2><ul><li>لف حول السيارة في إضاءة جيدة وابحث عن خدوش أو اختلاف واضح في لون الدهان.</li><li>راجع الزجاج والفوانيس والمرايات والحساسات.</li><li>افتح الأبواب والشنطة والكبوت وتأكد من انتظام الفتح والغلق.</li><li>راجع الجنوط والإطارات وتاريخها وحالتها الظاهرة.</li></ul><h2>داخل المقصورة</h2><ul><li>جرب التكييف والشاشة والكاميرا والحساسات والنوافذ والمرايات.</li><li>راجع حالة الفرش والتابلوه والسقف.</li><li>تأكد من وجود المفتاح الاحتياطي والكتيبات والملحقات المتفق عليها.</li></ul><h2>العداد والتنبيهات</h2><p>لاحظ قراءة العداد عند الاستلام وشغّل السيارة وتأكد أن لمبات التحذير الطبيعية تنطفئ بعد التشغيل وفق نظام السيارة. إذا ظهر تحذير مستمر اسأل عنه قبل التحرك.</p><h2>المستندات والأرقام</h2><p>طابق رقم الشاسيه في السيارة مع المستندات، وراجع اسم الموديل والفئة وسنة الصنع واللون. احتفظ بإيصال الحجز والفاتورة وأي ورقة ضمان أو صيانة تُسلّم لك.</p><h2>التجهيزات المتفق عليها</h2><p>إذا شمل الاتفاق دواسات أو حماية دهان أو كاميرا أو ترخيص أو تأمين أو أي إضافة، راجعها بندًا بندًا. جملة «هنبعتهالك بعدين» لازم تكون مكتوبة لو البند مدفوع ضمن الصفقة.</p><h2>قبل مغادرة المعرض</h2><p>التقط صورة للعداد ورقم الشاسيه وحالة السيارة وقت الاستلام. إذا لاحظت ملاحظة، سجّلها مع مسؤول التسليم قبل المغادرة بدل ما تبدأ رحلة إثبات طويلة لاحقًا.</p>',
            ],
            [
                'slug' => 'test-drive-before-buying-car-egypt',
                'title' => 'تجربة القيادة قبل الشراء: 15 حاجة تختبرها في العربية',
                'excerpt' => 'دليل Test Drive عملي: وضعية القيادة، الرؤية، العزل، الفرامل، التكييف، الركن، استجابة الفتيس والمطبات.',
                'content' => '<h2>اختبار القيادة مش لفة سريعة حوالين المعرض</h2><p>التجربة المفيدة هدفها تعرف هل العربية مناسبة ليومك أنت، مش هل العربية سريعة. قبل الوصول اطلب حجز Test Drive للموديل والفئة الأقرب لما ستشتريه.</p><h2>قبل التحرك</h2><ul><li>اضبط المقعد والدركسيون وشوف هل توصل للدواسات براحة.</li><li>اختبر الرؤية للأمام والجوانب والخلف.</li><li>شغّل التكييف والشاشة ووصل هاتفك لو النظام يسمح.</li><li>اجلس في المقعد الخلفي بنفسك لو الأسرة ستستخدم السيارة.</li></ul><h2>أثناء القيادة</h2><ul><li>استجابة الدواسة من السكون.</li><li>سلاسة الفتيس في الزحام.</li><li>قوة الفرامل وسهولة التحكم فيها.</li><li>وزن الدركسيون في السرعات البطيئة.</li><li>الرؤية عند الدوران وتغيير الحارة.</li><li>العزل من صوت المحرك والإطارات والهواء.</li><li>تصرف التعليق على المطبات والطرق المكسرة.</li><li>سهولة الركن واستخدام الكاميرا والحساسات.</li></ul><h2>اختبر سيناريو استخدامك</h2><p>إذا كان استخدامك الأساسي داخل المدينة، اهتم بالرؤية والتكييف والركن أكثر من رقم التسارع. إذا كنت تسافر كثيرًا، اختبر ثبات المقعد والعزل واستجابة التجاوز. وإذا كان معك أطفال، جرّب الدخول للمقاعد الخلفية وحجم الشنطة عمليًا.</p><h2>بعد التجربة</h2><p>اكتب ثلاث نقاط أعجبتك وثلاث نقاط ضايقتك قبل ما تدخل في كلام السعر. اعمل نفس القائمة لكل سيارة تقارن بينها. دوّن ملاحظاتك بعد كل تجربة قيادة حتى لا تختلط عليك تفاصيل السيارات عند المقارنة.</p>',
            ],
            [
                'slug' => 'car-showroom-finance-hidden-costs-egypt',
                'title' => 'التقسيط من معرض السيارات: احسب التكلفة الحقيقية قبل ما تبص للقسط',
                'excerpt' => 'طريقة مقارنة عروض تقسيط السيارات من المعارض بالدفعة والمصاريف والتأمين وإجمالي المدفوع بدل التركيز على القسط فقط.',
                'content' => '<h2>القسط الصغير مش معناه عرض أرخص</h2><p>مقارنة عروض التمويل بالقسط الشهري فقط من أسرع الطرق لاتخاذ قرار غلط. المدة الأطول قد تخفّض القسط لكنها تغيّر إجمالي ما ستدفعه، وقد توجد مصاريف مرتبطة بالتمويل أو التأمين تختلف بين عرض وآخر.</p><h2>اكتب الأرقام كلها في سطر واحد</h2><ul><li>سعر السيارة النقدي.</li><li>الدفعة المقدمة.</li><li>عدد الأقساط وقيمة كل قسط.</li><li>أي مصاريف إدارية معلنة.</li><li>تكلفة التأمين إذا كانت جزءًا من العرض.</li><li>أي دفعة أخيرة أو Balloon Payment إن وجدت.</li></ul><h2>احسب إجمالي المدفوع</h2><p>ابدأ من الدفعة المقدمة ثم أضف مجموع الأقساط وكل الرسوم المرتبطة بالصفقة. الرقم الناتج هو اللي تقارنه بعرض آخر، وليس القسط المكتوب بخط كبير على الإعلان.</p><h2>اسأل عن ثبات السعر وموعد التسليم</h2><p>إذا كانت السيارة ستُسلّم لاحقًا، اعرف بوضوح متى يُثبت السعر النهائي وكيف يتعامل العرض مع أي تغيير قبل التسليم. اطلب الإجابة في المستندات وليس في محادثة شفوية.</p><h2>ما الذي يجعل المقارنة عادلة؟</h2><p>قارن نفس الفئة ونفس مدة التمويل ونفس الدفعة المقدمة قدر الإمكان. لو تغير متغيرين أو ثلاثة معًا، العرض الأرخص ظاهريًا ممكن يكون أغلى عند جمع كل شيء.</p><h2>قبل التوقيع</h2><p>اقرأ جدول السداد كاملًا وشروط السداد المبكر أو التأخير وأي تأمين مرتبط بالعقد. إذا كان بند مالي مش مفهوم، خده مكتوب وافهمه قبل التوقيع. المعادلة بسيطة: الغموض بعد التوقيع أغلى من سؤال محرج قبل التوقيع.</p>',
            ],
            [
                'slug' => 'car-overprice-egypt-dealership-guide',
                'title' => 'الأوفر برايس عند شراء سيارة جديدة: إمتى تمشي من الصفقة؟',
                'excerpt' => 'كيف تتعامل مع فرق السعر عن السعر الرسمي، وتقارن قيمة التسليم الفوري بعرض بديل بدون قرار متسرع.',
                'content' => '<h2>إيه هو الفرق اللي لازم تسأل عنه؟</h2><p>في بعض أوقات نقص المعروض قد تجد سيارة متاحة للتسليم بسعر أعلى من السعر المعلن لدى الوكيل أو العلامة. المهم هنا ألا تتعامل مع الفرق كرقم معزول؛ لازم تعرف ماذا تحصل مقابله وهل السعر النهائي مكتوب بوضوح.</p><h2>ابدأ بالسعر الرسمي الحالي</h2><p>راجع موقع العلامة أو تواصل مع الشبكة الرسمية لمعرفة السعر المتاح وقت المقارنة. لا تعتمد على Screenshot قديم لأن الأسعار والعروض قد تتغير.</p><h2>اسأل عن سبب فرق السعر</h2><p>هل الفرق مقابل تسليم فوري؟ هل يتضمن إضافات أو تأمينًا أو ترخيصًا؟ هل السيارة نفس الفئة وسنة الموديل؟ افصل قيمة السيارة عن أي خدمة إضافية حتى تعرف أنت بتدفع مقابل إيه.</p><h2>احسب تكلفة الانتظار</h2><p>التسليم الفوري له قيمة عند بعض المشترين، لكن لازم تحط لها سقفًا. قارن فرق السعر مع بدائل السوق ووقت الانتظار الفعلي لدى جهات أخرى، ولا تجعل استعجالك يحدد السعر وحده.</p><h2>إمتى توقف التفاوض وتمشي؟</h2><ul><li>لو السعر النهائي غير واضح أو يتغير أثناء إنهاء الصفقة.</li><li>لو لا يمكنك تحديد مصدر الزيادة أو الخدمات المضافة.</li><li>إذا كانت الفئة أو سنة الموديل مختلفة عن المعروض في المقارنة.</li><li>لو الحجز يحتاج دفعًا بدون شروط استرداد واضحة.</li></ul><h2>المهم في النهاية</h2><p>مش كل فرق سعر معناه صفقة سيئة، ومش كل تسليم فوري يستاهل أي رقم. قارن السعر النهائي والوقت والضمان والتجهيزات، وحدد مسبقًا أقصى فرق تقبل دفعه بدل ما القرار يتاخد في لحظة حماس.</p>',
            ],
            [
                'slug' => 'questions-before-booking-new-car-egypt',
                'title' => '20 سؤال تسألهم قبل ما تدفع حجز عربية جديدة',
                'excerpt' => 'أسئلة الحجز المهمة عن السعر والفئة والتسليم والضمان والتمويل والاسترداد قبل دفع أي مبلغ للمعرض.',
                'content' => '<h2>أسئلة عن السيارة نفسها</h2><ol><li>دي أنهي فئة بالضبط؟</li><li>سنة الموديل كام؟</li><li>إيه التجهيزات اللي تختلف عن الفئة الأقل والأعلى؟</li><li>اللون اللي عايزه متاح؟</li><li>هل فيه عربية Display أو Test Drive لنفس الفئة؟</li></ol><h2>أسئلة عن السعر</h2><ol start="6"><li>السعر النقدي النهائي كام؟</li><li>هل في مصاريف إضافية غير السعر؟</li><li>العرض ساري لحد إمتى؟</li><li>السعر بيتثبت وقت الحجز ولا وقت التسليم؟</li><li>الإضافات الاختيارية إجبارية ولا لأ؟</li></ol><h2>أسئلة عن التسليم</h2><ol start="11"><li>موعد التسليم المتوقع مكتوب فين؟</li><li>إيه اللي يحصل لو التسليم اتأخر؟</li><li>إمتى يتم تخصيص رقم الشاسيه؟</li><li>هل السيارة مخزنة محليًا ولا لسه في الطريق؟</li><li>إيه الأوراق اللي هستلمها مع العربية؟</li></ol><h2>أسئلة عن الحجز والتمويل</h2><ol start="16"><li>قيمة الحجز كام؟</li><li>إيه شروط استرداد الحجز؟</li><li>إذا كان الشراء بالتقسيط، إجمالي المدفوع كام؟</li><li>التأمين داخل العرض ولا منفصل؟</li><li>مين الجهة اللي هتصدر إيصال الحجز والفاتورة؟</li></ol><h2>ليه الأسئلة دي مهمة؟</h2><p>لأن معظم الخلافات تبدأ من بند كل طرف كان فاهمه بطريقة مختلفة. اطلب توضيح كل بند مهم قبل الدفع واحتفظ بما تم الاتفاق عليه كتابةً.</p>',
            ],
            [
                'slug' => 'compare-car-showroom-offers-egypt',
                'title' => 'كيف تقارن عرضين من معرضين دون أن يضللك القسط الشهري؟',
                'excerpt' => 'نموذج بسيط لمقارنة عرضين لشراء نفس السيارة: السعر النهائي، التمويل، التسليم، الضمان، الإضافات والتأمين.',
                'content' => '<h2>قارن نفس الحاجة بنفس الحاجة</h2><p>قبل ما تقول إن عرض A أرخص من B، اتأكد إن الاتنين لنفس الفئة ونفس سنة الموديل ونفس طريقة الدفع. اختلاف الفئة أو مدة التمويل كفاية يخلي المقارنة مضللة.</p><h2>اعمل جدول من ست خانات</h2><p>اكتب أمام كل معرض: السعر النقدي، الدفعة المقدمة، إجمالي الأقساط، الرسوم الإضافية، موعد التسليم، والإضافات أو الخدمات المشمولة. بهذه الطريقة الأرقام الصغيرة المبعثرة تتحول إلى صفقة يمكن مقارنتها.</p><h2>ادّي للتسليم وزن لكن مش شيك على بياض</h2><p>لو معرض هيسلم فورًا وآخر بعد فترة، التسليم الأسرع له قيمة. لكن ضع رقمًا منطقيًا لهذه القيمة بدل ما تدفع أي فرق بسبب جملة «العربية آخر واحدة».</p><h2>التأمين والترخيص والإضافات</h2><p>عرض يشمل خدمات إضافية قد يكون أغلى ظاهريًا وأفضل في الإجمالي، أو العكس إذا كانت الإضافات مسعرة أعلى من السوق. افصل كل بند قبل الحكم.</p><h2>خانة مهمة: وضوح الاتفاق</h2><p>العرض الذي يوضح شروط الحجز والتسليم والسعر كتابةً أكثر أمانًا في اتخاذ القرار من عرض أرخص لكنه مليان عبارات مفتوحة. السعر مش البند الوحيد اللي له تكلفة.</p><h2>قرار الشراء</h2><p>بعد توحيد البيانات، ستعرف هل الفرق الحقيقي 5 آلاف ولا 50 ألف، وهل سببه السيارة أم التمويل أم خدمة إضافية. وساعتها القسط الشهري عندها يصبح رقمًا ضمن الصفقة الكاملة، وليس المعيار الوحيد للحكم على العرض.</p>',
            ],
        ];

        $ok = true;
        foreach ($guides as $guide) {
            $existing = get_page_by_path($guide['slug'], OBJECT, 'post');
            if ($existing instanceof WP_Post) continue;

            $id = wp_insert_post([
                'post_type' => 'post',
                'post_status' => 'publish',
                'post_title' => $guide['title'],
                'post_name' => $guide['slug'],
                'post_excerpt' => $guide['excerpt'],
                'post_content' => $guide['content'],
                'post_category' => [$cat_id],
            ], true);

            if (is_wp_error($id)) {
                $ok = false;
                continue;
            }

            update_post_meta($id, '_yoast_wpseo_title', $guide['title'] . ' | أعطال.كوم');
            update_post_meta($id, '_yoast_wpseo_metadesc', $guide['excerpt']);
            update_post_meta($id, '_a3_showroom_guide', '1');
        }

        if ($ok) {
            update_option('a3cp_showroom_guides_seed_v1', 'done', false);
        }
    }

    public static function seed_showroom_featured_v1(): void {
        if ((string) get_option('a3cp_showroom_featured_seed_v1') === 'done') return;

        $showroom_media = [
            'toyota-egypt-cairo-festival-city-showroom' => 81116,
            'toyota-egypt-sheikh-zayed-showroom' => 80768,
            'toyota-egypt-madinaty-showroom' => 80771,
            'toyota-egypt-abbassia-showroom' => 80762,
            'mg-mansour-new-cairo-showroom' => 81499,
            'mg-mansour-madinaty-showroom' => 80881,
            'mg-mansour-smouha-showroom' => 80691,
            'mg-mansour-mansoura-showroom' => 80198,
            'chery-gb-abbas-el-akkad-showroom' => 83039,
            'chery-kernel-fifth-settlement-showroom' => 82871,
        ];

        $guide_media = [
            'dealer-vs-authorized-distributor-vs-private-showroom-egypt' => 81116,
            'how-to-verify-car-showroom-authorized-egypt' => 83039,
            'new-car-delivery-checklist-egypt' => 81499,
            'test-drive-before-buying-car-egypt' => 82871,
            'car-showroom-finance-hidden-costs-egypt' => 80198,
            'car-overprice-egypt-dealership-guide' => 80691,
            'questions-before-booking-new-car-egypt' => 80768,
            'compare-car-showroom-offers-egypt' => 80881,
        ];

        $ok = true;
        foreach ($showroom_media as $slug => $media_id) {
            $post = get_page_by_path($slug, OBJECT, 'a3_showroom');
            if (!$post instanceof WP_Post || !wp_attachment_is_image($media_id)) {
                $ok = false;
                continue;
            }
            set_post_thumbnail($post->ID, $media_id);
        }

        foreach ($guide_media as $slug => $media_id) {
            $post = get_page_by_path($slug, OBJECT, 'post');
            if (!$post instanceof WP_Post || !wp_attachment_is_image($media_id)) {
                $ok = false;
                continue;
            }
            set_post_thumbnail($post->ID, $media_id);
        }

        if ($ok) {
            update_option('a3cp_showroom_featured_seed_v1', 'done', false);
        }
    }

    public static function enrich_showroom_directory_v2(): void {
        if ((string) get_option('a3cp_showroom_enrich_v2') === 'done') return;

        $brand_defaults = [
            'toyota' => [
                'email' => 'Customer.Care@toyotaegypt.com.eg',
                'booking' => 'https://toyota.com.eg/en/test-drive',
                'services' => "بيع سيارات جديدة\nحجز تجربة قيادة عبر Toyota Egypt\nاستفسارات الحجز والتسليم\nعروض وتمويل حسب المتاح",
                'note' => 'تويوتا مصر تنشر شبكة الفروع رسميًا وتوفر حجز تجربة قيادة إلكترونيًا. الرقم 16550 هو خط خدمة العملاء الرسمي.',
            ],
            'mg' => [
                'email' => '',
                'booking' => 'https://www.mgmotor.com.eg/contact-us/',
                'services' => "بيع سيارات MG الجديدة\nطلب تجربة قيادة\nطلب عرض سعر\nاستفسارات التمويل والحجز والتسليم",
                'note' => 'MG Motor Egypt تنشر عنوان الفرع ورقم الاتصال وساعات العمل، وتوفر طلب Test Drive أو عرض سعر عبر موقعها الرسمي.',
            ],
            'chery' => [
                'email' => '',
                'booking' => 'https://chery-eg.com/en/test_drive',
                'services' => "بيع سيارات شيري الجديدة\nحجز تجربة قيادة\nتسجيل اهتمام بالموديل\nاستفسارات العروض والتقسيط",
                'note' => 'Chery Egypt تنشر الفروع وأرقام الاتصال وساعات العمل وتوفر نموذج Test Drive رسمي واختيار المعرض داخل الطلب.',
            ],
        ];

        $items = [
            'toyota-egypt-cairo-festival-city-showroom' => ['brand'=>'toyota'],
            'toyota-egypt-sheikh-zayed-showroom' => ['brand'=>'toyota'],
            'toyota-egypt-madinaty-showroom' => ['brand'=>'toyota'],
            'toyota-egypt-abbassia-showroom' => ['brand'=>'toyota'],
            'mg-mansour-new-cairo-showroom' => ['brand'=>'mg'],
            'mg-mansour-madinaty-showroom' => ['brand'=>'mg'],
            'mg-mansour-smouha-showroom' => ['brand'=>'mg'],
            'mg-mansour-mansoura-showroom' => ['brand'=>'mg'],
            'chery-gb-abbas-el-akkad-showroom' => ['brand'=>'chery'],
            'chery-kernel-fifth-settlement-showroom' => ['brand'=>'chery'],
        ];

        $ok = true;
        foreach ($items as $slug => $cfg) {
            $post = get_page_by_path($slug, OBJECT, 'a3_showroom');
            if (!$post instanceof WP_Post) {
                $ok = false;
                continue;
            }

            $brand = $cfg['brand'];
            $defaults = $brand_defaults[$brand];
            $address = (string) get_post_meta($post->ID, '_a3_address', true);

            update_post_meta($post->ID, '_a3_email', $defaults['email']);
            update_post_meta($post->ID, '_a3_booking_url', $defaults['booking']);
            update_post_meta($post->ID, '_a3_maps_query', $address);
            update_post_meta($post->ID, '_a3_services', $defaults['services']);
            update_post_meta($post->ID, '_a3_data_note', $defaults['note']);

            // Names are intentionally added only when a public professional source
            // clearly ties the person to this exact branch. Never infer or guess staff.
            if (!get_post_meta($post->ID, '_a3_staff_public', true)) {
                update_post_meta($post->ID, '_a3_staff_public', '');
            }
        }

        if ($ok) update_option('a3cp_showroom_enrich_v2', 'done', false);
    }

    private static function showroom_asset(string $key, string $url, string $filename, string $alt): int {
        $existing = get_posts([
            'post_type' => 'attachment',
            'post_status' => 'inherit',
            'posts_per_page' => 1,
            'fields' => 'ids',
            'meta_key' => '_a3_asset_key',
            'meta_value' => $key,
        ]);
        if ($existing) return (int) $existing[0];

        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/media.php';
        require_once ABSPATH . 'wp-admin/includes/image.php';

        $tmp = download_url($url, 45);
        if (is_wp_error($tmp)) return 0;

        $file = ['name' => $filename, 'tmp_name' => $tmp];
        $id = media_handle_sideload($file, 0, $alt);

        if (is_wp_error($id)) {
            @unlink($tmp);
            return 0;
        }

        update_post_meta($id, '_wp_attachment_image_alt', $alt);
        update_post_meta($id, '_a3_asset_key', $key);
        return (int) $id;
    }

    public static function seed_showroom_custom_media_v2(): void {
        if ((string) get_option('a3cp_showroom_custom_media_v2') === 'done') return;

        $base = 'https://raw.githubusercontent.com/marwanile1-cyber/a3tal/main/assets/showrooms/';
        $exterior = self::showroom_asset(
            'showroom-official-exterior-v2',
            $base . 'showroom-official-exterior.webp',
            'a3tal-showroom-official-exterior.webp',
            'معرض سيارات حديث بتصميم احترافي من أعطال.كوم'
        );
        $interior = self::showroom_asset(
            'showroom-premium-interior-v2',
            $base . 'showroom-premium-interior.webp',
            'a3tal-showroom-premium-interior.webp',
            'صالة عرض سيارات حديثة بتصميم احترافي من أعطال.كوم'
        );

        if (!$exterior || !$interior) return;

        $showroom_map = [
            'toyota-egypt-cairo-festival-city-showroom' => $exterior,
            'toyota-egypt-sheikh-zayed-showroom' => $interior,
            'toyota-egypt-madinaty-showroom' => $exterior,
            'toyota-egypt-abbassia-showroom' => $interior,
            'mg-mansour-new-cairo-showroom' => $exterior,
            'mg-mansour-madinaty-showroom' => $interior,
            'mg-mansour-smouha-showroom' => $exterior,
            'mg-mansour-mansoura-showroom' => $interior,
            'chery-gb-abbas-el-akkad-showroom' => $exterior,
            'chery-kernel-fifth-settlement-showroom' => $interior,
        ];

        $guide_map = [
            'dealer-vs-authorized-distributor-vs-private-showroom-egypt' => $interior,
            'how-to-verify-car-showroom-authorized-egypt' => $exterior,
            'new-car-delivery-checklist-egypt' => $interior,
            'test-drive-before-buying-car-egypt' => $exterior,
            'car-showroom-finance-hidden-costs-egypt' => $interior,
            'car-overprice-egypt-dealership-guide' => $exterior,
            'questions-before-booking-new-car-egypt' => $interior,
            'compare-car-showroom-offers-egypt' => $exterior,
        ];

        $ok = true;
        foreach ($showroom_map as $slug => $media_id) {
            $post = get_page_by_path($slug, OBJECT, 'a3_showroom');
            if (!$post instanceof WP_Post) { $ok = false; continue; }
            set_post_thumbnail($post->ID, $media_id);
        }
        foreach ($guide_map as $slug => $media_id) {
            $post = get_page_by_path($slug, OBJECT, 'post');
            if (!$post instanceof WP_Post) { $ok = false; continue; }
            set_post_thumbnail($post->ID, $media_id);
        }

        if ($ok) update_option('a3cp_showroom_custom_media_v2', 'done', false);
    }

    private static function motorcycle_asset(string $key, string $url, string $filename, string $alt): int {
        $existing = get_posts([
            'post_type' => 'attachment',
            'post_status' => 'inherit',
            'posts_per_page' => 1,
            'fields' => 'ids',
            'meta_key' => '_a3_asset_key',
            'meta_value' => $key,
        ]);
        if ($existing) return (int) $existing[0];

        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/media.php';
        require_once ABSPATH . 'wp-admin/includes/image.php';

        $tmp = download_url($url, 45);
        if (is_wp_error($tmp)) return 0;

        $file = ['name' => $filename, 'tmp_name' => $tmp];
        $id = media_handle_sideload($file, 0, $alt);
        if (is_wp_error($id)) {
            @unlink($tmp);
            return 0;
        }

        update_post_meta($id, '_wp_attachment_image_alt', $alt);
        update_post_meta($id, '_a3_asset_key', $key);
        return (int) $id;
    }

    public static function seed_motorcycle_expansion_v2(): void {
        if ((string) get_option('a3cp_motorcycle_expansion_v2') === 'done') return;

        $brands = [
            'tvs'=>'TVS','bajaj'=>'Bajaj','honda'=>'Honda','yamaha'=>'Yamaha','suzuki'=>'Suzuki',
            'kawasaki'=>'Kawasaki','ktm'=>'KTM','bmw-motorrad'=>'BMW Motorrad','ducati'=>'Ducati',
            'triumph'=>'Triumph','harley-davidson'=>'Harley-Davidson','royal-enfield'=>'Royal Enfield',
            'hero'=>'Hero','benelli'=>'Benelli','keeway'=>'Keeway','cfmoto'=>'CFMOTO','qjmotor'=>'QJMotor',
            'zontes'=>'Zontes','voge'=>'Voge','lifan'=>'Lifan','loncin'=>'Loncin','haojue'=>'Haojue',
            'dayun'=>'Dayun','sym'=>'SYM','kymco'=>'Kymco','piaggio'=>'Piaggio','vespa'=>'Vespa',
            'aprilia'=>'Aprilia','peugeot-motocycles'=>'Peugeot Motocycles'
        ];
        foreach($brands as $slug=>$name){
            if(!term_exists($slug,'a3_brand')) wp_insert_term($name,'a3_brand',['slug'=>$slug]);
        }

        $types = [
            'commuter'=>'استخدام يومي',
            'sport'=>'رياضي',
            'scooter'=>'سكوتر',
            'adventure'=>'Adventure',
            'touring'=>'Touring',
            'cruiser'=>'Cruiser',
            'off-road'=>'Off-road',
            'electric'=>'كهربائي',
            'cub'=>'Cub / Underbone',
        ];
        foreach($types as $slug=>$name){
            if(!term_exists($slug,'a3_motorcycle_type')) wp_insert_term($name,'a3_motorcycle_type',['slug'=>$slug]);
        }

        $items = [
            [
                'slug'=>'bajaj-pulsar-180-egypt',
                'title'=>'Bajaj Pulsar 180 في مصر',
                'brand'=>'bajaj','type'=>'sport','origin'=>'الهند',
                'engine'=>178.06,'power'=>17.02,'torque'=>14.22,'trans'=>'يدوي 5 سرعات','fuel'=>'بنزين',
                'cooling'=>'تبريد هواء','front'=>'قرص 260 مم','rear'=>'قرص 230 مم','tyres'=>'Tubeless',
                'tank'=>15,'weight'=>147,'warranty'=>'راجع الوكيل أو الموزع وقت الشراء','use'=>'تنقل يومي بطابع رياضي',
                'source'=>'https://www.bajajauto.com/ar-eg/bikes/pulsar-180',
                'image'=>'https://cdn.bajajauto.com/ar-eg/-/media/globalbajajauto/common-media/product-detail-page-banners/latam/pulsar-180.webp',
                'excerpt'=>'Bajaj Pulsar 180 بمحرك 178.06 سم³ وقوة 17.02 PS وعزم 14.22 نيوتن متر مع ناقل 5 سرعات وفرامل قرصية أمامية وخلفية.',
                'content'=>'<h2>نظرة عامة على Bajaj Pulsar 180</h2><p>Pulsar 180 من الموديلات التي تعرضها Bajaj رسميًا للسوق المصري. تركيبتها تميل للاستخدام اليومي مع شكل رياضي، وتعتمد على محرك DTS-i أحادي الأسطوانة رباعي الأشواط ومبرد بالهواء.</p><h2>المحرك والأداء</h2><p>السعة الرسمية 178.06 سم³، والقوة القصوى 17.02 PS عند 8500 دورة/دقيقة، والعزم 14.22 نيوتن متر عند 6500 دورة/دقيقة. ناقل الحركة من 5 سرعات.</p><h2>الفرامل والإطارات</h2><p>الفرامل الأمامية قرص 260 مم والخلفية قرص 230 مم، والإطاران بدون أنبوب داخلي. وهو تجهيز يمنحها مستوى أعلى من بعض الدراجات الاقتصادية التي تعتمد على الطنابير في الأمام والخلف.</p><h2>الأبعاد والاستخدام</h2><p>الوزن الفارغ المعلن 147 كجم، والخلوص الأرضي 150 مم، وسعة خزان الوقود 15 لتر. قبل الشراء جرّب وضعية القيادة والوزن أثناء المناورة البطيئة، خصوصًا إذا كانت هذه أول دراجة لك.</p><h2>قبل الشراء في مصر</h2><ul><li>تأكد من سنة الموديل والفئة الفعلية.</li><li>اسأل عن الضمان وشبكة الصيانة وقطع الاستهلاك.</li><li>راجع توافر تيل الفرامل والسلسلة والتروس والفلاتر قبل الحجز.</li><li>لا تعتمد على سعر قديم أو إعلان غير مؤرخ؛ السعر والتوافر يتغيران.</li></ul><p><small>المصدر المرجعي: Bajaj Auto Egypt. آخر مراجعة للبيانات: 4 أكتوبر 2026.</small></p>'
            ],
            [
                'slug'=>'bajaj-boxer-150-hd-egypt',
                'title'=>'Bajaj Boxer 150 HD في مصر',
                'brand'=>'bajaj','type'=>'commuter','origin'=>'الهند',
                'engine'=>144.8,'power'=>12,'torque'=>12.55,'trans'=>'يدوي 5 سرعات','fuel'=>'بنزين',
                'cooling'=>'تبريد هواء','front'=>'طنبورة 130 مم','rear'=>'طنبورة 130 مم','tyres'=>'Tube type',
                'tank'=>11,'weight'=>125,'warranty'=>'12 شهرًا أو 30,000 كم وفق صفحة Bajaj Egypt','use'=>'استخدام يومي ومسافات وتشغيل عملي',
                'source'=>'https://www.bajajauto.com/ar-eg/bikes/boxer-150hd',
                'image'=>'https://cdn.bajajauto.com/ar-eg/-/media/globalbajajauto/common-media/360/latam/boxer-150-hd/red/00.webp',
                'excerpt'=>'Bajaj Boxer 150 HD بمحرك 144.8 سم³ وقدرة 12 PS وناقل 5 سرعات وخزان 11 لتر، موجه للاستخدام العملي اليومي.',
                'content'=>'<h2>نظرة عامة على Bajaj Boxer 150 HD</h2><p>Boxer 150 HD واحدة من الدراجات التي تعرضها Bajaj رسميًا في مصر، وموقعها الطبيعي هو الاستخدام العملي اليومي والطرق التي تحتاج بساطة واعتمادية أكثر من التجهيزات الرياضية.</p><h2>المحرك وناقل الحركة</h2><p>المحرك 144.8 سم³، أحادي الأسطوانة رباعي الأشواط ومبرد بالهواء، بقوة 12 PS عند 7500 دورة/دقيقة وعزم 12.55 نيوتن متر عند 5000 دورة/دقيقة، مع ناقل من 5 سرعات.</p><h2>التعليق والراحة</h2><p>تعليق أمامي تلسكوبي وتعليق خلفي SNS، ومقعد طويل وواسع نسبيًا. الخلوص والأبعاد يجعلونها أقرب لفلسفة التشغيل العملي من الموتوسيكل الرياضي.</p><h2>الفرامل والإطارات</h2><p>الفرامل الأمامية والخلفية طنابير ميكانيكية 130 مم، والإطارات من النوع الأنبوبي. لو استخدامك سريع أو على طرق مفتوحة، ضع في الاعتبار أن تجهيز الفرامل يختلف عن دراجات بقرص أمامي أو ABS.</p><h2>التجهيزات والضمان</h2><p>صفحة Bajaj Egypt تذكر منفذ USB ومؤشر تروس، كما تذكر ضمان 12 شهرًا لمسافة 30,000 كم. راجع شروط الضمان المكتوبة وقت الشراء لأن الشروط الفعلية قد ترتبط بسياسة الوكيل والصيانة الدورية.</p><p><small>المصدر المرجعي: Bajaj Auto Egypt. آخر مراجعة للبيانات: 4 أكتوبر 2026.</small></p>'
            ],
        ];

        $ok=true;
        foreach($items as $item){
            $post=get_page_by_path($item['slug'],OBJECT,'a3_motorcycle');
            if(!$post instanceof WP_Post){
                $id=wp_insert_post([
                    'post_type'=>'a3_motorcycle','post_status'=>'publish','post_title'=>$item['title'],
                    'post_name'=>$item['slug'],'post_excerpt'=>$item['excerpt'],'post_content'=>$item['content']
                ],true);
                if(is_wp_error($id)){ $ok=false; continue; }
                $post=get_post($id);
            }
            $id=(int)$post->ID;
            update_post_meta($id,'_a3_engine_cc',$item['engine']);
            update_post_meta($id,'_a3_power_hp',$item['power']);
            update_post_meta($id,'_a3_torque_nm',$item['torque']);
            update_post_meta($id,'_a3_transmission',$item['trans']);
            update_post_meta($id,'_a3_fuel',$item['fuel']);
            update_post_meta($id,'_a3_cooling',$item['cooling']);
            update_post_meta($id,'_a3_front_brake',$item['front']);
            update_post_meta($id,'_a3_rear_brake',$item['rear']);
            update_post_meta($id,'_a3_tyre_type',$item['tyres']);
            update_post_meta($id,'_a3_tank_l',$item['tank']);
            update_post_meta($id,'_a3_weight_kg',$item['weight']);
            update_post_meta($id,'_a3_warranty',$item['warranty']);
            update_post_meta($id,'_a3_use_case',$item['use']);
            update_post_meta($id,'_a3_origin_country',$item['origin']);
            update_post_meta($id,'_a3_source_url',$item['source']);
            update_post_meta($id,'_a3_source_checked_at','2026-10-04');
            wp_set_object_terms($id,$item['brand'],'a3_brand',false);
            wp_set_object_terms($id,'egypt','a3_market',false);
            wp_set_object_terms($id,$item['type'],'a3_motorcycle_type',false);

            if(!has_post_thumbnail($id)){
                $media=self::motorcycle_asset('moto-'.$item['slug'],$item['image'],$item['slug'].'.webp',$item['title']);
                if($media) set_post_thumbnail($id,$media);
            }
        }

        // Enrich the existing TVS entities with richer structured motorcycle fields.
        $tvs=[
            'tvs-apache-rtr-160-4v-egypt'=>['origin'=>'الهند','cooling'=>'تبريد بالزيت','tank'=>12,'use'=>'رياضي يومي'],
            'tvs-raider-125-egypt'=>['origin'=>'الهند','cooling'=>'تبريد هواء','tank'=>10,'use'=>'تنقل يومي'],
            'tvs-ntorq-125-re-egypt'=>['origin'=>'الهند','cooling'=>'تبريد هواء','tank'=>5,'front'=>'قرص 220 مم مع SBT','use'=>'سكوتر للمدينة'],
        ];
        foreach($tvs as $slug=>$meta){
            $post=get_page_by_path($slug,OBJECT,'a3_motorcycle');
            if(!$post instanceof WP_Post) continue;
            update_post_meta($post->ID,'_a3_origin_country',$meta['origin']);
            update_post_meta($post->ID,'_a3_cooling',$meta['cooling']);
            update_post_meta($post->ID,'_a3_tank_l',$meta['tank']);
            update_post_meta($post->ID,'_a3_use_case',$meta['use']);
            if(!empty($meta['front'])) update_post_meta($post->ID,'_a3_front_brake',$meta['front']);
        }

        if($ok) update_option('a3cp_motorcycle_expansion_v2','done',false);
    }

    public static function seed_motorcycle_guides_v1(): void {
        if ((string) get_option('a3cp_motorcycle_guides_v1') === 'done') return;

        $term=term_exists('motorcycle-guide','category');
        if(!$term){
            $term=wp_insert_term('دليل الموتوسيكلات','category',[
                'slug'=>'motorcycle-guide',
                'description'=>'دليل شراء وصيانة ومقارنة الموتوسيكلات والسكوتر وقطع الغيار في مصر.'
            ]);
        }
        if(is_wp_error($term)) return;
        $cat_id=is_array($term)?(int)$term['term_id']:(int)$term;

        $guides=[
            [
                'slug'=>'motorcycle-brands-egypt-complete-guide',
                'title'=>'دليل ماركات الموتوسيكلات في مصر: الياباني والهندي والصيني والأوروبي',
                'excerpt'=>'مرجع شامل لماركات الموتوسيكلات والسكوتر من Honda وYamaha وSuzuki وTVS وBajaj إلى CFMOTO وQJMotor وZontes وLifan وLoncin وغيرها.',
                'content'=>'<h2>خريطة ماركات الموتوسيكلات</h2><p>سوق الموتوسيكلات لا يتوقف عند الياباني. فيه مدارس مختلفة: الياباني المعروف بالاعتمادية وانتشار الخبرة، الهندي الذي يركز غالبًا على التشغيل اليومي والقيمة، التايواني القوي في السكوتر، الأوروبي الذي يغطي الأداء والـTouring والـPremium، والصيني الذي أصبح فيه فرق ضخم بين مصنع يصنع دراجات اقتصادية بسيطة وعلامة تنافس في فئات متوسطة وكبيرة.</p><h2>الماركات اليابانية</h2><p><strong>Honda، Yamaha، Suzuki، Kawasaki</strong> هي الأسماء اليابانية الأساسية. قبل شراء أي موديل في مصر لا يكفي اسم العلامة؛ الأهم هو توافر الموديل نفسه وقطع صيانته ومصدره المحلي.</p><h2>الماركات الهندية</h2><p><strong>TVS، Bajaj، Hero، Royal Enfield</strong>. Bajaj تعرض رسميًا في مصر Pulsar 180 وBoxer 150 HD، وTVS لديها حضور رسمي بمنتجات مثل Apache RTR 160 4V وRaider 125 وNtorq 125 RE. الهندي مهم جدًا لمن يبحث عن تشغيل يومي وقطع استهلاك وتكلفة ملكية معقولة.</p><h2>الماركات التايوانية</h2><p><strong>SYM وKymco</strong> من أشهر الأسماء في عالم السكوتر. عند المقارنة ركّز على توفر السيور والرولات وقطع الـCVT والبلاستيك والفرامل، لأن السكوتر له نمط صيانة مختلف عن الموتوسيكل اليدوي.</p><h2>الماركات الأوروبية والأمريكية</h2><p><strong>BMW Motorrad، Ducati، Triumph، KTM، Aprilia، Piaggio، Vespa، Peugeot Motocycles، Harley-Davidson</strong>. هنا تكلفة الصيانة والقطع والتخصص الفني تصبح جزءًا من قرار الشراء، خصوصًا مع المحركات الأكبر والإلكترونيات وأنظمة التعليق والفرامل المتقدمة.</p><h2>الماركات الصينية الحديثة</h2><p><strong>CFMOTO، QJMotor، Zontes، Voge</strong> تمثل الجيل الصيني الأحدث الذي يركز على التصميم والتقنيات والفئات المتوسطة والكبيرة. CFMOTO تعرض عالميًا عائلات SR وNK وMT وCL، وQJMotor تملك تشكيلة واسعة من الرياضي والـNaked والـTouring.</p><h2>الماركات الصينية الاقتصادية</h2><p><strong>Lifan، Loncin، Haojue، Dayun</strong> وأسماء صينية أخرى تظهر بدرجات مختلفة حسب المستورد والسوق. Lifan مثلًا شركة صينية كبيرة لديها Street وCruiser وScooter وOff-road وE-bike، وLoncin لها تاريخ صناعي ومحركات ومنتجات مرتبطة بالسوق المصري. هنا لا تشتري على اسم البلد فقط: اسأل عن كود المحرك، مصدر القطع، الوكيل الفعلي، وتوافر قطع الكهرباء والفتيس والبلاستيك.</p><h2>Benelli وKeeway</h2><p>العلامتان لهما هوية تسويقية مختلفة، لكنهما اليوم ضمن منظومة صناعية مرتبطة بمجموعة Qianjiang الصينية. لذلك الحكم عليهما بكلمة «إيطالي» أو «صيني» فقط يضيّع الصورة. المهم الموديل والمصنع والمنصة والمحرك وخدمة ما بعد البيع.</p><h2>كيف تستخدم هذا الدليل؟</h2><ul><li>اختار السعة ونوع الاستخدام أولًا.</li><li>بعدها الماركة والموديل.</li><li>راجع توفر قطع الاستهلاك قبل الشراء.</li><li>اسأل عن مركز خدمة يفهم نفس المحرك أو المنصة.</li><li>لا تعتمد على سمعة بلد المنشأ وحدها.</li></ul><p>أعطال.كوم سيعامل كل موديل ككيان مستقل: مواصفات، أعطال، صيانة، قطع غيار ومصادر، بدل أحكام عامة من نوع الياباني لا يعطل والصيني كله واحد، لأن التقييم الدقيق يجب أن يعتمد على بيانات الموديل نفسه وخدمة ما بعد البيع، لا على أحكام عامة عن بلد المنشأ.</p>'
            ],
            [
                'slug'=>'chinese-motorcycles-egypt-guide',
                'title'=>'الموتوسيكلات الصيني في مصر: من CFMOTO وQJMotor لحد Lifan وLoncin',
                'excerpt'=>'دليل عملي لفهم فروق الموتوسيكلات الصينية الحديثة والاقتصادية، وأهم ما يجب فحصه قبل الشراء وقطع الغيار والصيانة.',
                'content'=>'<h2>الموتوسيكلات الصينية ليست فئة واحدة</h2><p>من الأخطاء الشائعة التعامل مع كلمة «صيني» وكأن جميع المصانع تقدم المستوى نفسه، بينما الواقع يضم شركات عالمية كبيرة ودراجات اقتصادية بسيطة تحت أسماء متعددة. في الصين شركات ضخمة لها R&D ومنتجات عالمية وفئات كبيرة، وفي نفس الوقت توجد دراجات اقتصادية بسيطة تُباع تحت أسماء تجارية مختلفة حسب المستورد.</p><h2>CFMOTO</h2><p>من أبرز العلامات الصينية الحديثة، ولديها عائلات SR الرياضية وNK الـNaked وMT الـAdventure وCL الكلاسيكية. الشركة نفسها تعرض منتجات من 125 سم³ وحتى فئات أكبر بكثير.</p><h2>QJMotor</h2><p>علامة تابعة لصانع كبير بدأ نشاطه منذ الثمانينيات، وله حضور عالمي واسع. مهم عند الشراء معرفة اسم الموديل العالمي وكود المحرك لأن الأسماء التجارية قد تختلف بين الأسواق.</p><h2>Zontes وVoge</h2><p>علامتان تستهدفان غالبًا شريحة أعلى من الصيني الاقتصادي التقليدي، مع اهتمام أكبر بالتجهيزات والإلكترونيات والمحركات المتوسطة. قرار الشراء هنا يجب أن يربط المواصفات بخدمة ما بعد البيع والقطع المحلية.</p><h2>Lifan وLoncin</h2><p>Lifan لديها خطوط Street وCruiser وScooter وOff-road وE-bike، بينما Loncin شركة صناعية كبيرة في المحركات والدراجات ولها تاريخ تعاون وتصنيع مرتبط بمصر. عند شراء موديل اقتصادي يحمل منصة أو محركًا من هذه المدارس، كود المحرك أهم من شكل الملصق على التانك.</p><h2>Haojue وDayun</h2><p>أسماء صينية معروفة في الدراجات العملية والـCommuter والسكوتر حسب السوق. لا تفترض توفر كل موديل عالميًا في مصر؛ وجود العلامة شيء وتوفر الموديل والدعم المحلي شيء آخر.</p><h2>قبل شراء موتوسيكل صيني</h2><ul><li>صور رقم الشاسيه وكود المحرك.</li><li>اسأل عن تيل الفرامل والسلسلة والتروس والبوجيه والفلاتر.</li><li>اعرف هل الكهرباء والـECU والحساسات لها بدائل أم لا.</li><li>تحقق من وكيل أو مستورد حالي وليس اسمًا قديمًا على إعلان.</li><li>راجع سوق المستعمل لأن سهولة إعادة البيع جزء من تكلفة الملكية.</li></ul><h2>متى يكون الصيني منطقيًا؟</h2><p>عندما يعطيك تجهيزًا أو سعة أو سعرًا مناسبًا وتكون القطع والخدمة متاحة للموديل نفسه. ومتى يكون صفقة سيئة؟ عندما تشتري مواصفات على الورق ولا تستطيع العثور على قطعة استهلاك بعد أول عطل بسيط.</p>'
            ],
            [
                'slug'=>'japanese-vs-indian-vs-chinese-motorcycle',
                'title'=>'ياباني أم هندي أم صيني؟ اختر الموتوسيكل وفق الاستخدام لا بلد المنشأ',
                'excerpt'=>'مقارنة عملية بين مدارس الموتوسيكلات اليابانية والهندية والصينية من حيث الاستخدام والصيانة والقطع وإعادة البيع.',
                'content'=>'<h2>بلد المنشأ وحده ليس مواصفة</h2><p>بلد المنشأ تعطيك خلفية عن الصناعة، لكنها لا تقول لك وحدها إن موديلًا معينًا مناسب لك. قد تجد دراجة صينية حديثة بتجهيزات قوية، أو دراجة هندية عملية، أو دراجة يابانية مستعملة بحالة سيئة تجعل تكلفة امتلاكها أعلى من البدائل.</p><h2>الياباني</h2><p>يمتاز غالبًا بتاريخ طويل في المحركات والشاسيه وانتشار خبرة الصيانة، لكن السعر وقطع بعض الموديلات المستوردة قد يكونان مرتفعين.</p><h2>الهندي</h2><p>TVS وBajaj وHero وRoyal Enfield مدارس مختلفة، لكن السوق الهندي بطبيعته دفع الشركات للاهتمام بالاستخدام اليومي والتحمل وكفاءة التشغيل.</p><h2>الصيني</h2><p>الفارق بين CFMOTO أو QJMotor وبين دراجة اقتصادية مجهولة المصدر كبير جدًا. افصل بين الشركة والموديل والمستورد، ولا تشتري على جملة «كله صيني» أو «الصيني بقى زي الياباني» لأن قرار الشراء يجب أن يعتمد على الموديل والخدمة والقطع، وليس على تعميمات غير دقيقة.</p><h2>المقارنة الصح</h2><p>قارن قطع الغيار، مركز الخدمة، الفرامل، الإطارات، وزن الدراجة، استهلاكك اليومي، إعادة البيع، وسجل الموديل نفسه. النتيجة أحيانًا تكون ياباني، وأحيانًا هندي، وأحيانًا صيني محترم.</p>'
            ],
            [
                'slug'=>'scooter-vs-motorcycle-egypt',
                'title'=>'سكوتر أم موتوسيكل؟ الفرق في الاستخدام والصيانة والتكلفة',
                'excerpt'=>'مقارنة بين السكوتر والموتوسيكل اليدوي في المدينة والدليفري والمسافات والصيانة والـCVT والراحة.',
                'content'=>'<h2>السكوتر ليس مجرد موتوسيكل من دون ناقل يدوي</h2><p>السكوتر له تصميم واستخدام وصيانة مختلفة، خصوصًا مع ناقل CVT والسيور والرولات ومساحات التخزين ووضعية الجلوس.</p><h2>السكوتر للمدينة</h2><p>مريح في الزحام، سهل في التوقف والتحرك، وغالبًا عملي في التخزين. لكنه يحتاج اهتمامًا بصيانة الـCVT والسيور والرولات وعدم تجاهل صوت النقل.</p><h2>الموتوسيكل اليدوي</h2><p>يعطيك تحكمًا مباشرًا في الغيارات ويناسب طيفًا واسعًا من السعات والاستخدامات، من الـCommuter وحتى Adventure وSport.</p><h2>الدليفري</h2><p>الاختيار يعتمد على الحمولة والمسافات وسهولة الصيانة واستهلاك الإطارات والفرامل، مش على شكل الدراجة وحده.</p><h2>قبل القرار</h2><p>جرّب وضعية الجلوس، سهولة المناورة، مساحة التخزين، تكلفة القطع الدورية، وخبرة الورش المتاحة للموديل.</p>'
            ],
            [
                'slug'=>'motorcycle-engine-sizes-125-150-160-200-250',
                'title'=>'125 أم 150 أم 160 أم 200 أم 250 سي سي؟ افهم السعة قبل الشراء',
                'excerpt'=>'شرح عملي لفروق سعات الموتوسيكلات الشائعة وتأثيرها على الاستخدام والوزن والحرارة والسرعات والصيانة.',
                'content'=>'<h2>السعة ليست مقياسًا للجودة</h2><p>السعة الأكبر لا تعني أن الدراجة أحسن لكل شخص. محرك 125 أو 150 قد يكون أنسب للزحام والتشغيل اليومي، بينما 200 أو 250 يديك مرونة أكبر خارج المدينة لكنه قد يأتي بوزن وتكلفة أعلى.</p><h2>125–150 سي سي</h2><p>فئة عملية للمدينة والتنقل اليومي، وتنتشر فيها دراجات وسكوترات كثيرة. ركّز على العزم عند السرعات المنخفضة وتوفر القطع أكثر من رقم القوة وحده.</p><h2>160–180 سي سي</h2><p>منطقة وسط تجمع الاستخدام اليومي مع أداء أعلى نسبيًا، مثل TVS Apache RTR 160 4V وBajaj Pulsar 180.</p><h2>200–250 سي سي</h2><p>قد تناسب الطرق المفتوحة والمسافات أكثر حسب التصميم، لكن معها يزيد تأثير جودة الفرامل والإطارات والتبريد وخبرة الصيانة.</p><h2>اختار على وزنك وطريقك</h2><p>راكب خفيف داخل المدينة احتياجه مختلف عن شخص يسافر بطريق سريع أو يحمل راكبًا ثانيًا يوميًا. السعة جزء من المعادلة، مش المعادلة كلها.</p>'
            ],
            [
                'slug'=>'used-motorcycle-buying-checklist-egypt',
                'title'=>'شراء موتوسيكل مستعمل: Checklist قبل ما تدفع جنيه',
                'excerpt'=>'قائمة فحص للموتوسيكل المستعمل تشمل الشاسيه والمحرك والدخان والتبريد والكهرباء والفرامل والإطارات والسلسلة والأوراق.',
                'content'=>'<h2>ابدأ بالأوراق والهوية</h2><p>طابق رقم الشاسيه والمحرك مع المستندات قبل ما تدخل في قصة صوت الموتور. أي اختلاف هنا أهم من لمعان الخزان.</p><h2>افحص التشغيل بارد</h2><p>اطلب تشغيل الدراجة وهي باردة إن أمكن. لاحظ سهولة التشغيل والدخان والأصوات غير الطبيعية وثبات السلانسية بعد التسخين.</p><h2>السلسلة والتروس</h2><p>افحص الشد والتآكل والأسنان. مجموعة مهملة تعطيك فكرة عن نمط صيانة المالك حتى قبل فتح المحرك.</p><h2>الفرامل والإطارات</h2><p>راجع سمك التيل أو حالة الطنابير، حالة الأقراص، تشققات الإطارات وتاريخها، وأي تسريب من المساعدين.</p><h2>الكهرباء</h2><p>جرب الأنوار والإشارات والمارش والعداد والشحن، وافحص أي توصيلات عشوائية أو أسلاك مقطوعة ومجمعة.</p><h2>تجربة القيادة</h2><p>اسمع الفتيس، جرّب الفرامل، راقب استقامة الدركسيون، ولاحظ إذا كانت الدراجة تسحب ناحية معينة. لو مش فاهم في الموديل اعرضه على فني يعرف هذا الموديل قبل الشراء، لأن تكلفة الفحص أقل من إصلاح عطل مخفي بعد إتمام الصفقة.</p>'
            ],
            [
                'slug'=>'motorcycle-maintenance-schedule-guide',
                'title'=>'جدول صيانة الموتوسيكل: ما البنود التي تحتاج مراجعة دورية؟',
                'excerpt'=>'مرجع عملي لتنظيم زيت المحرك والسلسلة والفرامل والإطارات والفلاتر والبوجيه والبطارية والتبريد بدون افتراض أرقام موحدة لكل موديل.',
                'content'=>'<h2>لا يوجد جدول صيانة واحد يصلح لكل الموتوسيكلات</h2><p>الفترات الدقيقة لازم تأتي من دليل المالك للموديل. لكن فيه مجموعات بنود لازم تتكرر في أي خطة صيانة منظمة.</p><h2>زيت المحرك</h2><p>استخدم اللزوجة والمواصفة التي يحددها المصنع وراقب المستوى والتسريب. لا تنقل فترة تغيير من موديل لموديل لأن سعة الزيت وطبيعة المحرك والاستخدام تختلف.</p><h2>السلسلة والتروس</h2><p>تنظيف وتشحيم وضبط الشد وفحص التآكل بشكل دوري، خصوصًا مع المطر والتراب والاستخدام اليومي.</p><h2>الفرامل</h2><p>راجع التيل أو الأحذية، سائل الفرامل في الأنظمة الهيدروليكية، حالة الخراطيم والأقراص.</p><h2>الإطارات</h2><p>ضغط صحيح وحالة نقشة وتشققات وعمر الإطار. الإطار الرديء أو المتقادم قد يحد من أداء نظام الفرامل مهما كانت مواصفاته جيدة.</p><h2>التبريد والفلتر والبوجيه</h2><p>حسب نوع المحرك: تبريد هواء أو زيت أو سائل. راجع الفلاتر والبوجيه وسائل التبريد حسب دليل الموديل.</p><h2>البطارية والشحن</h2><p>ضعف المارش أو الإضاءة قد يكون بطارية أو شحنًا أو توصيلات، فلا تبدأ بشراء بطارية كل مرة.</p>'
            ],
            [
                'slug'=>'motorcycle-genuine-vs-aftermarket-parts',
                'title'=>'قطع غيار الموتوسيكل: أصلي ولا Aftermarket ولا تجاري؟',
                'excerpt'=>'كيف تفرّق بين OEM وAftermarket والبدائل التجارية، ومتى تكون القطعة الأصلية مهمة ومتى ينفع البديل المحترم.',
                'content'=>'<h2>ليس كل بديل سيئًا، كما أن وجود شعار على العبوة لا يكفي لضمان جودة القطعة</h2><p>OEM تعني قطعة بمواصفة الصانع، بينما Aftermarket قد يكون من شركة ممتازة أو اقتصادية. المشكلة الحقيقية في القطعة مجهولة المصدر أو غير المطابقة.</p><h2>قطع ما ينفعش تستهين بها</h2><p>الفرامل والإطارات وأجزاء التوجيه وبعض مكونات المحرك والكهرباء الحساسة تستحق مصدرًا معروفًا ومواصفة واضحة.</p><h2>رقم القطعة أهم من شكلها</h2><p>في موديلات كثيرة القطعة تشبه أخرى لكن المقاس أو الفيشة أو المعايرة مختلفة. استخدم Part Number أو كود واضح للموديل وسنة الصنع.</p><h2>في المحركات الصينية</h2><p>بعض المحركات الصينية تشترك في عائلات وأكواد، وده قد يسهل البدائل، لكن ما ينفعش تفترض التوافق لأن الموتور شكله واحد. كود المحرك والمقاسات هما الفيصل.</p>'
            ],
            [
                'slug'=>'delivery-motorcycle-buying-guide',
                'title'=>'اختيار موتوسيكل للدليفري: احسب التشغيل قبل سعر الشراء',
                'excerpt'=>'دليل اختيار موتوسيكل أو سكوتر للدليفري بناءً على استهلاك القطع والراحة والتحميل والتوقف المتكرر والصيانة.',
                'content'=>'<h2>استخدامات التوصيل من أنماط التشغيل القاسية</h2><p>عدد ساعات التشغيل والتوقف والانطلاق والحمولة يخلي المعيار مختلف عن شخص يركب 20 كم في اليوم.</p><h2>ركز على قطع الاستهلاك</h2><p>تيل الفرامل، الإطارات، السلسلة والتروس، القابض أو الـCVT، الزيت والفلاتر. سعر شراء أقل مع قطع نادرة ممكن يقلب أغلى اختيار بعد شهور.</p><h2>وضعية القيادة</h2><p>جرب المقعد والدركسيون ومساحة القدمين وحمل الصندوق. ألم الظهر واليد بعد خمس ساعات مش بند مكتوب في الكتالوج لكنه حقيقي جدًا.</p><h2>السعة</h2><p>السعة الصغيرة قد تكون منطقية داخل المدينة، لكن الحمولة والطريق والسرعات المطلوبة قد تحتاج عزمًا أكبر. اختار سيناريو عملك لا رأي صاحبك.</p>'
            ],
            [
                'slug'=>'fuel-injection-vs-carburetor-motorcycle',
                'title'=>'حقن إلكتروني ولا كربراتير في الموتوسيكل؟',
                'excerpt'=>'الفرق بين EFI والكربراتير في التشغيل والصيانة والحساسات واستهلاك الوقود وسهولة الإصلاح.',
                'content'=>'<h2>الكربراتير أبسط ميكانيكيًا</h2><p>يعتمد على دوائر وقود ميكانيكية وضبط، ويمكن لفنيين كثيرين التعامل معه. لكنه يتأثر بالضبط والاتساخ والارتفاع والحرارة أكثر.</p><h2>EFI أدق في التحكم</h2><p>الحقن الإلكتروني يستخدم حساسات وECU للتحكم في الوقود، وغالبًا يعطي تشغيلًا أكثر ثباتًا وانبعاثات وتحكمًا أفضل، لكنه يضيف مضخة وحساسات ووحدة تحكم يجب تشخيصها بدل التخمين.</p><h2>كيف تختار؟</h2><p>الموديل وتنفيذ النظام وخدمة ما بعد البيع أهم من اسم التقنية. EFI سيئ الصيانة لا يتحول فجأة إلى سحر، وكربراتير مضبوط ممكن يخدم سنين.</p>'
            ],
            [
                'slug'=>'abs-cbs-disc-drum-motorcycle-brakes',
                'title'=>'ABS وCBS وديسك وطنبورة: افهم فرامل الموتوسيكل قبل الشراء',
                'excerpt'=>'شرح مبسط لأنظمة فرامل الموتوسيكلات والسكوتر والفرق بين ABS وCBS والقرص والطنبورة وما الذي تبحث عنه في المواصفات.',
                'content'=>'<h2>القرص والطنبورة نوع فرامل، ABS وCBS أنظمة مساعدة</h2><p>الديسك أو القرص يختلف عن الطنبورة في التصميم والتبريد والاستجابة، بينما ABS يمنع قفل العجلة في ظروف معينة، وCBS يوزع جزءًا من قوة الفرملة بين العجلتين في أنظمة معينة.</p><h2>ABS</h2><p>ميزة أمان مهمة خصوصًا على الأسطح الزلقة والفرملة القوية، لكن وجوده لا يعوض إطارًا سيئًا أو مسافة أمان معدومة.</p><h2>CBS</h2><p>شائع في بعض السكوترات والدراجات الصغيرة ويساعد على توزيع الفرملة، لكنه ليس نفس وظيفة ABS.</p><h2>الطنبورة</h2><p>أبسط وأقل تكلفة في تطبيقات كثيرة، لكنها مختلفة في تبديد الحرارة والإحساس مقارنة بالقرص.</p><h2>قبل الشراء</h2><p>اعرف بالضبط تجهيز الفئة التي ستشتريها، لأن نفس الموديل قد يختلف بين سوق وآخر أو بين فئة وأخرى.</p>'
            ],
            [
                'slug'=>'new-motorcycle-delivery-checklist',
                'title'=>'Checklist استلام موتوسيكل زيرو من المعرض',
                'excerpt'=>'قائمة استلام موتوسيكل جديد: الشاسيه، المحرك، العدادات، الفرامل، الإطارات، السوائل، المفاتيح والمستندات.',
                'content'=>'<h2>طابق الأرقام أولًا</h2><p>رقم الشاسيه ورقم المحرك والموديل واللون وسنة الصنع يجب أن تتطابق مع المستندات.</p><h2>افحص قبل التشغيل</h2><p>راجع الدهان والبلاستيك والمرايات والجنوط والإطارات وأي خدوش نقل أو تخزين.</p><h2>شغل كل شيء</h2><p>المارش والأنوار والإشارات والعداد والكلاكس والـABS أو لمبات التحذير إن وجدت.</p><h2>الفرامل والسوائل</h2><p>تأكد من مستوى السوائل الظاهر وعدم وجود تسريب، وجرب ضغط الفرامل قبل التحرك.</p><h2>المفاتيح والكتيبات</h2><p>استلم المفتاح الاحتياطي ودليل المالك وكتيب الضمان وأي عدة أو ملحقات تأتي مع الموديل.</p><h2>قبل ما تمشي</h2><p>صوّر العداد وحالة الدراجة وأرقامها، واسأل عن أول صيانة وشروط الضمان كتابةً.</p>'
            ],
            [
                'slug'=>'motorcycle-tyres-guide-egypt',
                'title'=>'إطارات الموتوسيكل: المقاس والضغط والعمر أهم من الاسم على الجنب',
                'excerpt'=>'دليل لفهم مقاسات إطارات الموتوسيكل والـTubeless والأنبوبي والضغط والتشققات وتاريخ التصنيع.',
                'content'=>'<h2>المقاس جزء من تصميم الدراجة</h2><p>لا تغير عرض أو ارتفاع الإطار عشوائيًا لمجرد شكل أعرض. المقاس يؤثر على المناورة والارتفاع وقراءة السرعة والخلوص.</p><h2>Tubeless ولا Tube</h2><p>كل نظام له جنط وتصميم مناسب. لا تفترض إمكانية التحويل من غير مراجعة فنية صحيحة.</p><h2>الضغط</h2><p>اتبع ضغط المصنع حسب الحمولة. الضغط القليل أو الزائد يغير التماسك والتآكل والحرارة.</p><h2>العمر والحالة</h2><p>راجع التشققات والتصلب والتآكل غير المنتظم وتاريخ التصنيع. النقشة وحدها لا تقول إن الإطار حالته ممتازة.</p>'
            ],
            [
                'slug'=>'motorcycle-oil-guide',
                'title'=>'زيت الموتوسيكل: اللزوجة وJASO أهم من حكاية الزيت التقيل والخفيف',
                'excerpt'=>'كيف تختار زيت الموتوسيكل من دليل المالك وتفهم اللزوجة وJASO والقابض المبلل ومواعيد الفحص.',
                'content'=>'<h2>ابدأ من دليل المالك</h2><p>اللزوجة والمواصفة وسعة الزيت تختلف بين المحركات، لذلك لا توجد لزوجة أو فترة تغيير واحدة تصلح لكل الموتوسيكلات.</p><h2>JASO والقابض</h2><p>كثير من الموتوسيكلات اليدوية تستخدم زيتًا مشتركًا للمحرك والفتيس مع كلتش مبلل، وهنا مواصفة الزيت مهمة حتى لا تؤثر الإضافات على القابض.</p><h2>راقب المستوى</h2><p>نقص الزيت أخطر من اختيار ماركة أقل شهرة. افحص بالطريقة التي يحددها المصنع وعلى سطح مستوٍ.</p><h2>الاستخدام القاسي</h2><p>الحرارة والزحام والتشغيل الطويل قد تجعل ظروفك مختلفة عن الاستخدام المثالي. اتبع جدول المصنع وحدود الاستخدام الشاق إن كانت مذكورة بدل اختراع فترة تغيير من عندنا.</p>'
            ],
        ];

        $ok=true;
        foreach($guides as $guide){
            $existing=get_page_by_path($guide['slug'],OBJECT,'post');
            if($existing instanceof WP_Post) continue;
            $id=wp_insert_post([
                'post_type'=>'post','post_status'=>'publish','post_title'=>$guide['title'],
                'post_name'=>$guide['slug'],'post_excerpt'=>$guide['excerpt'],
                'post_content'=>$guide['content'],'post_category'=>[$cat_id]
            ],true);
            if(is_wp_error($id)){ $ok=false; continue; }
            update_post_meta($id,'_yoast_wpseo_title',$guide['title'].' | أعطال.كوم');
            update_post_meta($id,'_yoast_wpseo_metadesc',$guide['excerpt']);
            update_post_meta($id,'_a3_motorcycle_guide','1');
        }

        // Reuse genuine motorcycle entity imagery for guide cards until each guide receives bespoke art.
        $thumbs=get_posts([
            'post_type'=>'a3_motorcycle','post_status'=>'publish','posts_per_page'=>8,
            'fields'=>'ids','meta_query'=>[['key'=>'_thumbnail_id','compare'=>'EXISTS']]
        ]);
        if($thumbs){
            $posts=get_posts(['post_type'=>'post','post_status'=>'publish','posts_per_page'=>30,'category'=>$cat_id]);
            $i=0;
            foreach($posts as $post){
                if(!has_post_thumbnail($post->ID)){
                    $src_id=$thumbs[$i % count($thumbs)];
                    $media=(int)get_post_thumbnail_id($src_id);
                    if($media) set_post_thumbnail($post->ID,$media);
                    $i++;
                }
            }
        }

        if($ok) update_option('a3cp_motorcycle_guides_v1','done',false);
    }

    public static function robots(array $robots): array {
        if (is_singular(['a3_dtc','a3_motorcycle','a3_car']) && get_post_meta(get_queried_object_id(), '_a3_entity_stub', true)) {
            $robots['noindex'] = true;
            unset($robots['index']);
        }
        if (is_post_type_archive(array_keys(self::TYPES))) {
            global $wp_query;
            if ($wp_query instanceof WP_Query && (int) $wp_query->found_posts === 0) {
                $robots['noindex'] = true;
                unset($robots['index']);
            }
        }
        return $robots;
    }
}
