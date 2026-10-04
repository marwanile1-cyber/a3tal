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
            self::meta($type, '_a3_engine_cc', 'integer', 'absint');
            self::meta($type, '_a3_power_hp', 'integer', 'absint');
            self::meta($type, '_a3_torque_nm', 'integer', 'absint');
            self::meta($type, '_a3_transmission', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_fuel', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_drivetrain', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_source_url', 'string', 'esc_url_raw');
            self::meta($type, '_a3_source_checked_at', 'string', 'sanitize_text_field');
            self::meta($type, '_a3_related_post_ids', 'string', [__CLASS__, 'sanitize_id_list']);
        }
        self::meta('a3_car', '_a3_seats', 'integer', 'absint');

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
                'visit' => 'لو تريد Test Drive، احجز الموعد مسبقًا وحدد الموديل المطلوب. اسأل أيضًا عن مدة التسليم المكتوبة وسياسة استرداد الحجز إذا تغير السعر أو تأخر التسليم.',
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
                'visit' => 'لو السيارة غير موجودة للمعاينة، لا تعتمد على صور الكتالوج وحدها. اطلب موعد وصول سيارة عرض أو تجربة قيادة، وتأكد من مواصفات الفئة المصرية لأن التجهيزات قد تختلف بين الأسواق.',
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
                'content' => '<h2>ما تعتمدش على كلمة «معتمد» في الإعلان</h2><p>أسهل خطوة للتحقق هي البحث عن اسم المعرض أو الفرع داخل موقع العلامة الرسمي. وجود شعار كبير على الواجهة أو صفحة فيسبوك لا يثبت وحده أن المكان جزء من شبكة البيع الحالية.</p><h2>1. افتح Dealer Locator الرسمي</h2><p>ابحث في صفحة الفروع أو Find Us التابعة للعلامة. إذا وجدت اسم الجهة والعنوان ورقم الهاتف متطابقين، عندها يكون عندك مرجع مباشر يمكن الرجوع إليه. أعطال.كوم يستخدم نفس المبدأ عند منح حالة «معتمد رسميًا» داخل دليل المعارض.</p><h2>2. طابق البيانات مش الاسم فقط</h2><p>بعض الأسماء التجارية تتكرر أو يكون لها أكثر من فرع. طابق المدينة والعنوان ورقم الهاتف، خصوصًا قبل تحويل مبلغ حجز.</p><h2>3. اطلب عرض سعر مكتوب</h2><p>العرض الجيد يحدد الموديل والفئة وسنة السيارة والسعر وطريقة الدفع ومدة صلاحية العرض. لو بند مهم في القرار غير مكتوب، اسأل عنه قبل الدفع وليس بعده.</p><h2>4. اسأل عن الجهة التي ستصدر الفاتورة</h2><p>اعرف اسم الشركة التي سيصدر منها إيصال الحجز أو الفاتورة وتأكد أنه نفس الطرف الذي تتعامل معه. لا ترسل أموالًا إلى حساب شخصي لمجرد أن المحادثة تحمل لوجو معروف.</p><h2>5. تحقق مرة ثانية قبل الاستلام</h2><p>الاعتماد لا يمنع الأخطاء في الفئة أو اللون أو التجهيز. عند تخصيص السيارة طابق البيانات المكتوبة مع السيارة نفسها ورقم الشاسيه والمستندات.</p><h2>إشارة حمراء مهمة</h2><p>إذا رفض المعرض توضيح صفته أو مصدر السيارة أو الجهة التي ستصدر الفاتورة، فدي علامة كافية إنك ما تستعجلش. القرار الجيد يحب الورق الواضح، مش الحكايات الحلوة.</p>',
            ],
            [
                'slug' => 'new-car-delivery-checklist-egypt',
                'title' => 'Checklist استلام سيارة زيرو من المعرض',
                'excerpt' => 'قائمة عملية لاستلام سيارة جديدة من المعرض: الهيكل، الإطارات، العدادات، التجهيزات، المستندات ورقم الشاسيه.',
                'content' => '<h2>ما تستلمش العربية على عجل</h2><p>يوم الاستلام بيكون مليان حماس وتصوير ومفاتيح لامعة، وده تحديدًا الوقت اللي ممكن تعدّي فيه تفصيلة تزعلك بعدين. خصص وقتًا هادئًا للفحص قبل مغادرة المعرض.</p><h2>فحص الهيكل الخارجي</h2><ul><li>لف حول السيارة في إضاءة جيدة وابحث عن خدوش أو اختلاف واضح في لون الدهان.</li><li>راجع الزجاج والفوانيس والمرايات والحساسات.</li><li>افتح الأبواب والشنطة والكبوت وتأكد من انتظام الفتح والغلق.</li><li>راجع الجنوط والإطارات وتاريخها وحالتها الظاهرة.</li></ul><h2>داخل المقصورة</h2><ul><li>جرب التكييف والشاشة والكاميرا والحساسات والنوافذ والمرايات.</li><li>راجع حالة الفرش والتابلوه والسقف.</li><li>تأكد من وجود المفتاح الاحتياطي والكتيبات والملحقات المتفق عليها.</li></ul><h2>العداد والتنبيهات</h2><p>لاحظ قراءة العداد عند الاستلام وشغّل السيارة وتأكد أن لمبات التحذير الطبيعية تنطفئ بعد التشغيل وفق نظام السيارة. لو في تحذير مستمر اسأل عنه قبل التحرك.</p><h2>المستندات والأرقام</h2><p>طابق رقم الشاسيه في السيارة مع المستندات، وراجع اسم الموديل والفئة وسنة الصنع واللون. احتفظ بإيصال الحجز والفاتورة وأي ورقة ضمان أو صيانة تُسلّم لك.</p><h2>التجهيزات المتفق عليها</h2><p>لو الاتفاق شمل دواسات أو حماية دهان أو كاميرا أو ترخيص أو تأمين أو أي إضافة، راجعها بندًا بندًا. جملة «هنبعتهالك بعدين» لازم تكون مكتوبة لو البند مدفوع ضمن الصفقة.</p><h2>قبل مغادرة المعرض</h2><p>خد صورة للعداد ورقم الشاسيه وحالة السيارة وقت الاستلام. لو لاحظت ملاحظة، سجّلها مع مسؤول التسليم قبل المغادرة بدل ما تبدأ رحلة إثبات طويلة لاحقًا.</p>',
            ],
            [
                'slug' => 'test-drive-before-buying-car-egypt',
                'title' => 'تجربة القيادة قبل الشراء: 15 حاجة تختبرها في العربية',
                'excerpt' => 'دليل Test Drive عملي: وضعية القيادة، الرؤية، العزل، الفرامل، التكييف، الركن، استجابة الفتيس والمطبات.',
                'content' => '<h2>اختبار القيادة مش لفة سريعة حوالين المعرض</h2><p>التجربة المفيدة هدفها تعرف هل العربية مناسبة ليومك أنت، مش هل العربية سريعة. قبل الوصول اطلب حجز Test Drive للموديل والفئة الأقرب لما ستشتريه.</p><h2>قبل التحرك</h2><ul><li>اضبط المقعد والدركسيون وشوف هل توصل للدواسات براحة.</li><li>اختبر الرؤية للأمام والجوانب والخلف.</li><li>شغّل التكييف والشاشة ووصل هاتفك لو النظام يسمح.</li><li>اجلس في المقعد الخلفي بنفسك لو الأسرة ستستخدم السيارة.</li></ul><h2>أثناء القيادة</h2><ul><li>استجابة الدواسة من السكون.</li><li>سلاسة الفتيس في الزحام.</li><li>قوة الفرامل وسهولة التحكم فيها.</li><li>وزن الدركسيون في السرعات البطيئة.</li><li>الرؤية عند الدوران وتغيير الحارة.</li><li>العزل من صوت المحرك والإطارات والهواء.</li><li>تصرف التعليق على المطبات والطرق المكسرة.</li><li>سهولة الركن واستخدام الكاميرا والحساسات.</li></ul><h2>اختبر سيناريو استخدامك</h2><p>لو استخدامك الأساسي مدينة، اهتم بالرؤية والتكييف والركن أكثر من رقم التسارع. لو تسافر كثيرًا، اختبر ثبات المقعد والعزل واستجابة التجاوز. ولو معك أطفال، جرّب الدخول للمقاعد الخلفية وحجم الشنطة عمليًا.</p><h2>بعد التجربة</h2><p>اكتب ثلاث نقاط أعجبتك وثلاث نقاط ضايقتك قبل ما تدخل في كلام السعر. اعمل نفس القائمة لكل سيارة تقارن بينها. الذاكرة بعد زيارة معرضين تبدأ تتصرف كأن كل العربيات كانت نفس اللون ونفس الكرسي.</p>',
            ],
            [
                'slug' => 'car-showroom-finance-hidden-costs-egypt',
                'title' => 'التقسيط من معرض السيارات: احسب التكلفة الحقيقية قبل ما تبص للقسط',
                'excerpt' => 'طريقة مقارنة عروض تقسيط السيارات من المعارض بالدفعة والمصاريف والتأمين وإجمالي المدفوع بدل التركيز على القسط فقط.',
                'content' => '<h2>القسط الصغير مش معناه عرض أرخص</h2><p>مقارنة عروض التمويل بالقسط الشهري فقط من أسرع الطرق لاتخاذ قرار غلط. المدة الأطول قد تخفّض القسط لكنها تغيّر إجمالي ما ستدفعه، وقد توجد مصاريف مرتبطة بالتمويل أو التأمين تختلف بين عرض وآخر.</p><h2>اكتب الأرقام كلها في سطر واحد</h2><ul><li>سعر السيارة النقدي.</li><li>الدفعة المقدمة.</li><li>عدد الأقساط وقيمة كل قسط.</li><li>أي مصاريف إدارية معلنة.</li><li>تكلفة التأمين إذا كانت جزءًا من العرض.</li><li>أي دفعة أخيرة أو Balloon Payment إن وجدت.</li></ul><h2>احسب إجمالي المدفوع</h2><p>ابدأ من الدفعة المقدمة ثم أضف مجموع الأقساط وكل الرسوم المرتبطة بالصفقة. الرقم الناتج هو اللي تقارنه بعرض آخر، وليس القسط المكتوب بخط كبير على الإعلان.</p><h2>اسأل عن ثبات السعر وموعد التسليم</h2><p>لو السيارة ستُسلّم لاحقًا، اعرف بوضوح متى يُثبت السعر النهائي وكيف يتعامل العرض مع أي تغيير قبل التسليم. اطلب الإجابة في المستندات وليس في محادثة شفوية.</p><h2>ما الذي يجعل المقارنة عادلة؟</h2><p>قارن نفس الفئة ونفس مدة التمويل ونفس الدفعة المقدمة قدر الإمكان. لو تغير متغيرين أو ثلاثة معًا، العرض الأرخص ظاهريًا ممكن يكون أغلى عند جمع كل شيء.</p><h2>قبل التوقيع</h2><p>اقرأ جدول السداد كاملًا وشروط السداد المبكر أو التأخير وأي تأمين مرتبط بالعقد. لو بند مالي مش مفهوم، خده مكتوب وافهمه قبل التوقيع. المعادلة بسيطة: الغموض بعد التوقيع أغلى من سؤال محرج قبل التوقيع.</p>',
            ],
            [
                'slug' => 'car-overprice-egypt-dealership-guide',
                'title' => 'الأوفر برايس عند شراء سيارة جديدة: إمتى تمشي من الصفقة؟',
                'excerpt' => 'كيف تتعامل مع فرق السعر عن السعر الرسمي، وتقارن قيمة التسليم الفوري بعرض بديل بدون قرار متسرع.',
                'content' => '<h2>إيه هو الفرق اللي لازم تسأل عنه؟</h2><p>في بعض أوقات نقص المعروض قد تجد سيارة متاحة للتسليم بسعر أعلى من السعر المعلن لدى الوكيل أو العلامة. المهم هنا ألا تتعامل مع الفرق كرقم معزول؛ لازم تعرف ماذا تحصل مقابله وهل السعر النهائي مكتوب بوضوح.</p><h2>ابدأ بالسعر الرسمي الحالي</h2><p>راجع موقع العلامة أو تواصل مع الشبكة الرسمية لمعرفة السعر المتاح وقت المقارنة. لا تعتمد على Screenshot قديم لأن الأسعار والعروض قد تتغير.</p><h2>اسأل عن سبب فرق السعر</h2><p>هل الفرق مقابل تسليم فوري؟ هل يتضمن إضافات أو تأمينًا أو ترخيصًا؟ هل السيارة نفس الفئة وسنة الموديل؟ افصل قيمة السيارة عن أي خدمة إضافية حتى تعرف أنت بتدفع مقابل إيه.</p><h2>احسب تكلفة الانتظار</h2><p>التسليم الفوري له قيمة عند بعض المشترين، لكن لازم تحط لها سقفًا. قارن فرق السعر مع بدائل السوق ووقت الانتظار الفعلي لدى جهات أخرى، ولا تجعل استعجالك يحدد السعر وحده.</p><h2>إمتى توقف التفاوض وتمشي؟</h2><ul><li>لو السعر النهائي غير واضح أو يتغير أثناء إنهاء الصفقة.</li><li>لو لا يمكنك تحديد مصدر الزيادة أو الخدمات المضافة.</li><li>لو الفئة أو سنة الموديل مختلفة عن المعروض في المقارنة.</li><li>لو الحجز يحتاج دفعًا بدون شروط استرداد واضحة.</li></ul><h2>المهم في النهاية</h2><p>مش كل فرق سعر معناه صفقة سيئة، ومش كل تسليم فوري يستاهل أي رقم. قارن السعر النهائي والوقت والضمان والتجهيزات، وحدد مسبقًا أقصى فرق تقبل دفعه بدل ما القرار يتاخد في لحظة حماس.</p>',
            ],
            [
                'slug' => 'questions-before-booking-new-car-egypt',
                'title' => '20 سؤال تسألهم قبل ما تدفع حجز عربية جديدة',
                'excerpt' => 'أسئلة الحجز المهمة عن السعر والفئة والتسليم والضمان والتمويل والاسترداد قبل دفع أي مبلغ للمعرض.',
                'content' => '<h2>أسئلة عن السيارة نفسها</h2><ol><li>دي أنهي فئة بالضبط؟</li><li>سنة الموديل كام؟</li><li>إيه التجهيزات اللي تختلف عن الفئة الأقل والأعلى؟</li><li>اللون اللي عايزه متاح؟</li><li>هل فيه عربية Display أو Test Drive لنفس الفئة؟</li></ol><h2>أسئلة عن السعر</h2><ol start="6"><li>السعر النقدي النهائي كام؟</li><li>هل في مصاريف إضافية غير السعر؟</li><li>العرض ساري لحد إمتى؟</li><li>السعر بيتثبت وقت الحجز ولا وقت التسليم؟</li><li>الإضافات الاختيارية إجبارية ولا لأ؟</li></ol><h2>أسئلة عن التسليم</h2><ol start="11"><li>موعد التسليم المتوقع مكتوب فين؟</li><li>إيه اللي يحصل لو التسليم اتأخر؟</li><li>إمتى يتم تخصيص رقم الشاسيه؟</li><li>هل السيارة مخزنة محليًا ولا لسه في الطريق؟</li><li>إيه الأوراق اللي هستلمها مع العربية؟</li></ol><h2>أسئلة عن الحجز والتمويل</h2><ol start="16"><li>قيمة الحجز كام؟</li><li>إيه شروط استرداد الحجز؟</li><li>لو بالتقسيط، إجمالي المدفوع كام؟</li><li>التأمين داخل العرض ولا منفصل؟</li><li>مين الجهة اللي هتصدر إيصال الحجز والفاتورة؟</li></ol><h2>ليه الأسئلة دي مهمة؟</h2><p>لأن معظم الخلافات تبدأ من بند كل طرف كان فاهمه بطريقة مختلفة. خليك مزعج خمس دقائق قبل الدفع بدل ما تقضي أسبوعين تشرح إن البائع قالك كلام مختلف.</p>',
            ],
            [
                'slug' => 'compare-car-showroom-offers-egypt',
                'title' => 'إزاي تقارن عرضين من معرضين من غير ما القسط يضحك عليك؟',
                'excerpt' => 'نموذج بسيط لمقارنة عرضين لشراء نفس السيارة: السعر النهائي، التمويل، التسليم، الضمان، الإضافات والتأمين.',
                'content' => '<h2>قارن نفس الحاجة بنفس الحاجة</h2><p>قبل ما تقول إن عرض A أرخص من B، اتأكد إن الاتنين لنفس الفئة ونفس سنة الموديل ونفس طريقة الدفع. اختلاف الفئة أو مدة التمويل كفاية يخلي المقارنة مضللة.</p><h2>اعمل جدول من ست خانات</h2><p>اكتب أمام كل معرض: السعر النقدي، الدفعة المقدمة، إجمالي الأقساط، الرسوم الإضافية، موعد التسليم، والإضافات أو الخدمات المشمولة. بهذه الطريقة الأرقام الصغيرة المبعثرة تتحول إلى صفقة يمكن مقارنتها.</p><h2>ادّي للتسليم وزن لكن مش شيك على بياض</h2><p>لو معرض هيسلم فورًا وآخر بعد فترة، التسليم الأسرع له قيمة. لكن ضع رقمًا منطقيًا لهذه القيمة بدل ما تدفع أي فرق بسبب جملة «العربية آخر واحدة».</p><h2>التأمين والترخيص والإضافات</h2><p>عرض يشمل خدمات إضافية قد يكون أغلى ظاهريًا وأفضل في الإجمالي، أو العكس إذا كانت الإضافات مسعرة أعلى من السوق. افصل كل بند قبل الحكم.</p><h2>خانة مهمة: وضوح الاتفاق</h2><p>العرض الذي يوضح شروط الحجز والتسليم والسعر كتابةً أكثر أمانًا في اتخاذ القرار من عرض أرخص لكنه مليان عبارات مفتوحة. السعر مش البند الوحيد اللي له تكلفة.</p><h2>قرار الشراء</h2><p>بعد توحيد البيانات، ستعرف هل الفرق الحقيقي 5 آلاف ولا 50 ألف، وهل سببه السيارة أم التمويل أم خدمة إضافية. وساعتها القسط الشهري يرجع لمكانه الطبيعي: رقم ضمن الصفقة، مش ساحر بيخبي باقي الحساب.</p>',
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
