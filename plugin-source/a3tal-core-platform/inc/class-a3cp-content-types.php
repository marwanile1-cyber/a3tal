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
