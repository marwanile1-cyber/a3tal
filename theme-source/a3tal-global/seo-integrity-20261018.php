<?php
/**
 * A3tal SEO integrity patch, 2026-10-18.
 * Scope: align Yoast sitemap entries with existing robots policies, repair
 * verified article links, restore page heading hierarchy and add exact-model
 * navigation. Does not create content, change URLs, or remove WordPress posts.
 */
if (!defined('ABSPATH')) exit;

/** Yoast exclusion only for confirmed noindex or equivalent-canonical records. */
add_filter('wpseo_exclude_from_sitemap_by_post_ids', static function($excluded) {
    if (!is_array($excluded)) $excluded = [];
    $groups = [
        'page' => ['my-garage'],
        'a3_car' => [
            'suzuki-alto-2027-egypt', 'skoda-octavia-2027-egypt',
            'kia-k4-2027-egypt', 'hyundai-tucson-2027-egypt',
        ],
        'a3_motorcycle' => [
            'tvs-apache-rtr-160-4v-egypt', 'tvs-raider-125-egypt',
            'tvs-ntorq-125-re-egypt',
        ],
        'a3_parts_vendor' => ['ezz-elcv-tvs-authorized-distributor-egypt'],
        'a3_maintenance_plan' => [
            'pulsar-180-first-service', 'pulsar-180-second-service',
            'pulsar-180-third-service', 'pulsar-180-paid-periodic-service',
            'pulsar-180-engine-oil-first-service',
            'pulsar-180-engine-oil-periodic',
            'pulsar-180-oil-filter-periodic', 'pulsar-180-air-filter-periodic',
        ],
        'post' => [
            'radiator-internal-blockage-flow-temperature-test-2',
            'p0300-random-misfire',
            'مركز-خدمة-hyundai-egypt-ghabbour-auto',
        ],
    ];
    foreach ($groups as $type => $slugs) {
        $found = get_posts([
            'post_type' => $type,
            'post_status' => 'publish',
            'post_name__in' => $slugs,
            'posts_per_page' => count($slugs),
            'fields' => 'ids',
            'no_found_rows' => true,
            'suppress_filters' => true,
        ]);
        foreach ($found as $id) $excluded[] = (int) $id;
    }
    // Legacy Arabic privacy URL now resolves to the up-to-date unified policy.
    $legacy_policy = get_page_by_path('سياسة-الخصوصية', OBJECT, 'page');
    if ($legacy_policy instanceof WP_Post && $legacy_policy->post_status === 'publish') {
        $excluded[] = (int)$legacy_policy->ID;
    }
    return array_values(array_unique(array_map('absint', $excluded)));
}, 100);

/** Repair verified old links inside displayed article bodies without replacing stored copy. */
add_filter('the_content', static function($html) {
    if (!is_singular('post') || !in_the_loop() || !is_main_query()) return $html;
    $canonical = [
        'obd2-live-data-reading-guide' => 'live-data-obd2',
        'obd2-freeze-frame-data-guide' => 'freeze-frame-obd2',
    ];
    foreach ($canonical as $old => $new) {
        $html = str_replace(
            ['https://a3tal.com/'.$old.'/', 'http://a3tal.com/'.$old.'/'],
            home_url('/'.$new.'/'),
            $html
        );
    }
    // The following old URLs have no equivalent verified guide. Do NOT redirect
    // them to a vaguely related article or the homepage. Preserve anchor copy.
    $missing = [
        'electric-car-problems-egypt-guide',
        'engine-oil-change-cost-prices-egypt-2026',
        'toyota-cvt-fluid-fe-vs-tc',
    ];
    foreach ($missing as $slug) {
        $pattern = '~<a\b[^>]*href\s*=\s*(["\'])https?://(?:www\.)?a3tal\.com/'
                 . preg_quote($slug, '~') . '/?\1[^>]*>(.*?)</a>~isu';
        $html = preg_replace_callback($pattern, static function($match) {
            return '<span>'.$match[2].'</span>';
        }, $html);
    }
    return $html;
}, 45);

/** One semantic H1 per explicitly verified WordPress page; preserve the text. */
add_filter('the_content', static function($html) {
    if (!is_page() || !in_the_loop() || !is_main_query()) return $html;
    $slug = get_post_field('post_name', get_queried_object_id());
    $pages = [
        'cars-nissan-sunny', 'choose-your-car', 'اتصل-بنا',
        'editorial-team', 'opel-kingdom-desouk',
        'عن-الموقع', 'شروط-الاستخدام',
    ];
    $name = get_the_title(get_queried_object_id());
    if (!in_array($slug, $pages, true) && !in_array($name, ['اتصل بنا', 'عن الموقع', 'شروط الاستخدام'], true)) return $html;
    return preg_replace('~<h1(\s[^>]*)?>(.*?)</h1>~isu', '<h2$1>$2</h2>', $html, 1);
}, 48);

/** Missing Yoast descriptions for actual verified dealer/service entries. */
add_filter('wpseo_metadesc', static function($description) {
    if (trim((string)$description) !== '' || !is_singular(['a3_service_center','a3_showroom'])) return $description;
    $id = (int)get_queried_object_id();
    if (!$id) return $description;
    $post = get_post($id);
    if (!$post || $post->post_status !== 'publish') return $description;
    $body = trim(preg_replace('/\s+/u', ' ', wp_strip_all_tags((string)$post->post_content)));
    $intro = wp_trim_words($body, 27, '…');
    if (function_exists('mb_strlen') && mb_strlen($intro, 'UTF-8') >= 70) return $intro;
    $kind = $post->post_type === 'a3_showroom' ? 'المعرض' : 'مركز الخدمة';
    return get_the_title($id) . ' في دليل أعطال.كوم، مع بيانات ' . $kind
        . ' المتاحة وتفاصيل التواصل والموقع وكيفية التأكد من الخدمة قبل الزيارة.';
}, 160);

/** Exact car models only. Ambiguous comparison headlines receive no auto-link. */
add_filter('the_content', static function($html) {
    if (!is_singular('post') || !in_the_loop() || !is_main_query()) return $html;
    $id = (int)get_the_ID();
    $title = (string)get_the_title($id);
    $models = [
        ['~(?:كيا\s*K4|\bKia\s*K4\b)~iu', 'kia-k4-2027-egypt'],
        ['~(?:سكودا\s*أوكتافيا|\bSkoda\s*Octavia\b)~iu', 'skoda-octavia-2027-egypt'],
        ['~(?:سوزوكي\s*ألتو|\bSuzuki\s*Alto\b)~iu', 'suzuki-alto-2027-egypt'],
        ['~(?:هيونداي\s*توسان|\bHyundai\s*Tucson\b)~iu', 'hyundai-tucson-2027-egypt'],
        ['~(?:شيري\s*أريزو\s*5|\bChery\s*Arrizo\s*5\b)~iu', 'chery-arrizo-5-egypt'],
        ['~(?:شيري\s*تيجو\s*4\s*برو|\bTiggo\s*4\s*Pro\b)~iu', 'chery-tiggo-4-pro-egypt'],
        ['~(?:شيري\s*تيجو\s*7\s*برو\s*ماكس|\bTiggo\s*7\s*Pro\s*Max\b)~iu', 'chery-tiggo-7-pro-max-egypt'],
    ];
    $match = [];
    foreach ($models as [$pattern, $slug]) if (preg_match($pattern, $title)) $match[$slug] = true;
    if (count($match) !== 1) return $html;
    $slug = array_key_first($match);
    $vehicle = get_page_by_path($slug, OBJECT, 'a3_car');
    if (!$vehicle || $vehicle->post_status !== 'publish') return $html;
    $url = get_permalink($vehicle);
    if (!$url || strpos($html, $url) !== false) return $html;
    return $html . '<aside class="a3-seo-exact-model" aria-label="ملف السيارة المرتبط"'
        . ' style="margin:22px 0;padding:15px 18px;border:1px solid #dde5ee;border-radius:12px;background:#f6f9fc">'
        . '<strong>ملف السيارة في موسوعة أعطال</strong><p style="margin:5px 0 0">'
        . '<a href="'.esc_url($url).'">'.esc_html(get_the_title($vehicle)).': المواصفات والأسعار والأدلة المتاحة ←</a>'
        . '</p></aside>';
}, 60);


/** Complete only genuinely missing descriptions; never overwrite editorial Yoast copy. */
add_filter('wpseo_metadesc', static function($description) {
    if (trim((string)$description) !== '') return $description;
    if (is_post_type_archive('a3_service_center')) {
        return 'دليل مراكز صيانة السيارات في مصر على أعطال.كوم، مع بيانات المراكز المنشورة ووسائل التواصل والمواقع والتحقق من الجهة قبل الحجز.';
    }
    if (is_post_type_archive('a3_parts_vendor')) {
        return 'دليل أماكن بيع قطع غيار السيارات والجهات المدرجة على أعطال.كوم، مع المعلومات المتاحة عن التوافق والشراء وطرق التحقق من البائع.';
    }
    if (is_post_type_archive('a3_maintenance_plan')) {
        return 'جداول صيانة المركبات حسب الموديل والمسافة والوقت في أعطال.كوم، مع أدلة تغيير الزيوت والفلاتر ومراجعة تعليمات المصنع.';
    }
    if (!is_singular(['post','a3_motorcycle'])) return $description;
    $post = get_post((int)get_queried_object_id());
    if (!$post || $post->post_status !== 'publish') return $description;
    $body = trim(preg_replace('/\s+/u', ' ', wp_strip_all_tags((string)$post->post_content)));
    if (function_exists('mb_strlen') && mb_strlen($body,'UTF-8') < 95) return $description;
    return wp_trim_words($body, 25, '…');
}, 180);

/**
 * Link a car model to published, verified service centers of the same brand.
 * Never assume any center services this exact trim without confirmation.
 */
add_filter('the_content', static function($html) {
    if (!is_singular('a3_car') || !in_the_loop() || !is_main_query()) return $html;
    $car_id=(int)get_the_ID();
    $brand=strtolower(trim((string)a3g_first_term($car_id,'a3_brand')));
    $title=(string)get_the_title($car_id);
    $groups=[];
    if ($brand==='chery' || strpos($title,'شيري')!==false) {
        $groups=['chery-gb-abu-rawash-service-center','chery-gb-amriya-alexandria-service-center'];
    } elseif ($brand==='skoda' || strpos($title,'سكودا')!==false) {
        $groups=['skoda-kayan-new-cairo-service-center','skoda-express-sheikh-zayed-service-center'];
    }
    if (!$groups) return $html;
    $links=[];
    foreach($groups as $slug) {
        $center=get_page_by_path($slug,OBJECT,'a3_service_center');
        if (!$center || $center->post_status!=='publish') continue;
        $url=get_permalink($center);
        if ($url) $links[]='<li><a href="'.esc_url($url).'">'.esc_html(get_the_title($center)).'</a></li>';
    }
    if (!$links) return $html;
    return $html.'<aside class="a3-seo-brand-centers" aria-label="دليل مراكز الخدمة"'
      .' style="margin:20px 0;padding:15px 18px;border:1px solid #dde5ee;border-radius:12px;background:#f6f9fc">'
      .'<h2 style="font-size:1.2em;margin:0 0 8px">مراكز خدمة العلامة المتاحة في دليل أعطال</h2>'
      .'<ul style="margin:0 0 8px">'.implode('',$links).'</ul>'
      .'<p style="margin:0">تأكد من الخدمات المتاحة لموديلك وسنة الصنع قبل الحجز.</p></aside>';
}, 62);
