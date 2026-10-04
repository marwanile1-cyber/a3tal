<?php
if (!defined('ABSPATH')) exit;

final class A3CP_Admin {
    private const TYPES = [
        'a3_car' => ['label' => 'السيارات', 'icon' => '🚘'],
        'a3_motorcycle' => ['label' => 'الموتوسيكلات', 'icon' => '🏍️'],
        'a3_dtc' => ['label' => 'أكواد DTC', 'icon' => '⚙️'],
        'a3_service_center' => ['label' => 'مراكز الخدمة', 'icon' => '🔧'],
        'a3_showroom' => ['label' => 'معارض السيارات', 'icon' => '🏢'],
    ];

    public static function init(): void {
        add_action('admin_menu', [__CLASS__, 'menu'], 8);
        add_action('admin_enqueue_scripts', [__CLASS__, 'assets']);

        foreach (array_keys(self::TYPES) as $type) {
            add_filter("manage_{$type}_posts_columns", [__CLASS__, 'columns']);
            add_action("manage_{$type}_posts_custom_column", [__CLASS__, 'column_content'], 10, 2);
        }
    }

    public static function menu(): void {
        add_menu_page(
            'A3tal Platform',
            'A3tal Platform',
            'edit_posts',
            'a3tal-platform',
            [__CLASS__, 'dashboard'],
            'dashicons-car',
            24
        );

        add_submenu_page(
            'a3tal-platform',
            'لوحة المنصة',
            'نظرة عامة',
            'edit_posts',
            'a3tal-platform',
            [__CLASS__, 'dashboard']
        );
    }

    public static function dashboard(): void {
        if (!current_user_can('edit_posts')) return;

        echo '<div class="wrap a3cp-admin">';
        echo '<div class="a3cp-hero">';
        echo '<div><span>A3TAL CORE PLATFORM</span><h1>من المقالات إلى منصة مركبات مترابطة</h1><p>طبقة البيانات الأساسية للسيارات والموتوسيكلات وأكواد الأعطال ومراكز الخدمة ومعارض السيارات. لا تغيّر روابط المقالات الحالية.</p></div>';
        echo '<div class="a3cp-version">v' . esc_html(A3CP_VERSION) . '</div>';
        echo '</div>';

        echo '<div class="a3cp-grid">';
        foreach (self::TYPES as $type => $cfg) {
            $counts = wp_count_posts($type);
            $published = isset($counts->publish) ? (int) $counts->publish : 0;
            $draft = isset($counts->draft) ? (int) $counts->draft : 0;
            $add = admin_url('post-new.php?post_type=' . $type);
            $list = admin_url('edit.php?post_type=' . $type);

            echo '<section class="a3cp-card">';
            echo '<div class="a3cp-card-icon">' . esc_html($cfg['icon']) . '</div>';
            echo '<h2>' . esc_html($cfg['label']) . '</h2>';
            echo '<div class="a3cp-stats"><span><b>' . esc_html((string) $published) . '</b> منشور</span><span><b>' . esc_html((string) $draft) . '</b> مسودة</span></div>';
            echo '<div class="a3cp-actions"><a class="button button-primary" href="' . esc_url($add) . '">إضافة</a><a class="button" href="' . esc_url($list) . '">إدارة</a></div>';
            echo '</section>';
        }
        echo '</div>';

        echo '<div class="a3cp-rules">';
        echo '<h2>قواعد البيانات قبل النشر</h2>';
        echo '<ol>';
        echo '<li>لا تُنشر الأسعار أو المواصفات المؤكدة بدون مصدر موثوق وتاريخ مراجعة.</li>';
        echo '<li>«معتمد رسميًا» يحتاج إثباتًا رسميًا من الشركة أو الوكيل.</li>';
        echo '<li>«موثّق من أعطال» يعني التحقق من بيانات النشاط، وليس ضمان جودة الخدمة.</li>';
        echo '<li>المقالات الحالية تظل بروابطها الحالية، ويتم ربطها بالكيانات بدل نقلها.</li>';
        echo '</ol>';
        echo '</div>';
        echo '</div>';
    }

    public static function columns(array $columns): array {
        $type = get_current_screen()?->post_type;

        if (in_array($type, ['a3_car', 'a3_motorcycle'], true)) {
            $columns['a3cp_year'] = 'السنة';
            $columns['a3cp_price'] = 'السعر';
            $columns['a3cp_checked'] = 'مراجعة المصدر';
        } elseif ($type === 'a3_dtc') {
            $columns['a3cp_code'] = 'الكود';
            $columns['a3cp_severity'] = 'الخطورة';
            $columns['a3cp_checked'] = 'مراجعة المصدر';
        } elseif (in_array($type, ['a3_service_center', 'a3_showroom'], true)) {
            $columns['a3cp_phone'] = 'الهاتف';
            $columns['a3cp_checked'] = 'آخر تحقق';
        }

        return $columns;
    }

    public static function column_content(string $column, int $post_id): void {
        switch ($column) {
            case 'a3cp_year':
                echo esc_html((string) get_post_meta($post_id, '_a3_year', true));
                break;
            case 'a3cp_price':
                $price = function_exists('a3cp_vehicle_price') ? a3cp_vehicle_price($post_id) : '';
                echo $price !== '' ? esc_html($price) : '—';
                break;
            case 'a3cp_checked':
                $date = (string) get_post_meta($post_id, '_a3_source_checked_at', true);
                echo $date !== '' ? esc_html($date) : '<span style="color:#b32d2e">غير محدد</span>';
                break;
            case 'a3cp_code':
                echo '<code>' . esc_html((string) get_post_meta($post_id, '_a3_dtc_code', true)) . '</code>';
                break;
            case 'a3cp_severity':
                $severity = (string) get_post_meta($post_id, '_a3_severity', true);
                $labels = ['low' => 'منخفضة', 'medium' => 'متوسطة', 'high' => 'مرتفعة', 'critical' => 'حرجة'];
                echo esc_html($labels[$severity] ?? '—');
                break;
            case 'a3cp_phone':
                echo esc_html((string) get_post_meta($post_id, '_a3_phone', true));
                break;
        }
    }

    public static function assets(string $hook): void {
        $screen = get_current_screen();
        if (!$screen) return;

        $is_platform = $screen->id === 'toplevel_page_a3tal-platform'
            || in_array((string) $screen->post_type, array_keys(self::TYPES), true);
        if (!$is_platform) return;

        $css = '
        .a3cp-admin{max-width:1180px}
        .a3cp-hero{margin:20px 0;display:flex;justify-content:space-between;gap:24px;align-items:center;padding:28px;border-radius:18px;background:linear-gradient(135deg,#081522,#12283c);color:#fff;box-shadow:0 16px 40px rgba(9,21,34,.12)}
        .a3cp-hero span{font-size:11px;color:#ff8d6b;font-weight:800;letter-spacing:.08em}
        .a3cp-hero h1{color:#fff;margin:6px 0 8px;font-size:28px}
        .a3cp-hero p{margin:0;color:#b7c4cf;max-width:760px}
        .a3cp-version{padding:9px 12px;border:1px solid rgba(255,255,255,.14);border-radius:999px;color:#fff;white-space:nowrap}
        .a3cp-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
        .a3cp-card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:18px;box-shadow:0 6px 22px rgba(15,23,42,.04)}
        .a3cp-card-icon{font-size:28px}.a3cp-card h2{margin:8px 0;font-size:17px}
        .a3cp-stats{display:flex;gap:10px;color:#64748b;font-size:11px}.a3cp-stats b{color:#0f172a}
        .a3cp-actions{display:flex;gap:7px;margin-top:16px}
        .a3cp-rules{margin-top:18px;background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:20px}
        .a3cp-rules h2{margin-top:0}.a3cp-rules li{margin:7px 0}
        .a3cp-fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 18px}
        .a3cp-field label{display:block;margin-bottom:5px}
        @media(max-width:1100px){.a3cp-grid{grid-template-columns:repeat(2,1fr)}}
        @media(max-width:700px){.a3cp-grid,.a3cp-fields{grid-template-columns:1fr}.a3cp-hero{align-items:flex-start;flex-direction:column}}
        ';
        wp_add_inline_style('wp-admin', $css);
    }
}
