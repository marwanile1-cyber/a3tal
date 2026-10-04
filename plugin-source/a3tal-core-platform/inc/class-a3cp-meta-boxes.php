<?php
if (!defined('ABSPATH')) exit;

final class A3CP_Meta_Boxes {
    private const VEHICLE_FIELDS = [
        '_a3_year' => ['label' => 'سنة الموديل', 'type' => 'number'],
        '_a3_price_min' => ['label' => 'أقل سعر', 'type' => 'number', 'step' => '0.01'],
        '_a3_price_max' => ['label' => 'أعلى سعر', 'type' => 'number', 'step' => '0.01'],
        '_a3_currency' => ['label' => 'العملة', 'type' => 'text', 'placeholder' => 'EGP / SAR / AED'],
        '_a3_engine_cc' => ['label' => 'سعة المحرك CC', 'type' => 'number'],
        '_a3_power_hp' => ['label' => 'القوة HP', 'type' => 'number'],
        '_a3_torque_nm' => ['label' => 'العزم Nm', 'type' => 'number'],
        '_a3_transmission' => ['label' => 'ناقل الحركة', 'type' => 'text'],
        '_a3_fuel' => ['label' => 'الوقود / نظام الدفع', 'type' => 'text'],
        '_a3_drivetrain' => ['label' => 'نظام الجر', 'type' => 'text', 'placeholder' => 'FWD / RWD / AWD / 4WD'],
        '_a3_source_url' => ['label' => 'المصدر الرسمي', 'type' => 'url'],
        '_a3_source_checked_at' => ['label' => 'تاريخ مراجعة المصدر', 'type' => 'date'],
        '_a3_related_post_ids' => ['label' => 'معرّفات المقالات المرتبطة', 'type' => 'text', 'placeholder' => 'مثال: 123,456,789'],
    ];

    private const DIRECTORY_FIELDS = [
        '_a3_phone' => ['label' => 'الهاتف', 'type' => 'text'],
        '_a3_whatsapp' => ['label' => 'واتساب', 'type' => 'text'],
        '_a3_address' => ['label' => 'العنوان', 'type' => 'textarea'],
        '_a3_lat' => ['label' => 'Latitude', 'type' => 'number', 'step' => '0.000001'],
        '_a3_lng' => ['label' => 'Longitude', 'type' => 'number', 'step' => '0.000001'],
        '_a3_hours' => ['label' => 'ساعات العمل', 'type' => 'textarea'],
        '_a3_official_source_url' => ['label' => 'مصدر التحقق الرسمي', 'type' => 'url'],
        '_a3_source_checked_at' => ['label' => 'تاريخ التحقق', 'type' => 'date'],
    ];

    private const DTC_FIELDS = [
        '_a3_dtc_code' => ['label' => 'الكود', 'type' => 'text', 'placeholder' => 'P0420'],
        '_a3_dtc_system' => ['label' => 'النظام', 'type' => 'text', 'placeholder' => 'المحرك / الانبعاثات / الشبكات'],
        '_a3_severity' => [
            'label' => 'درجة الخطورة',
            'type' => 'select',
            'options' => ['low' => 'منخفضة', 'medium' => 'متوسطة', 'high' => 'مرتفعة', 'critical' => 'حرجة'],
        ],
        '_a3_code_scope' => [
            'label' => 'نطاق الكود',
            'type' => 'select',
            'options' => ['generic' => 'عام OBD-II', 'manufacturer' => 'خاص بالشركة المصنعة'],
        ],
        '_a3_manufacturer' => ['label' => 'الشركة المصنعة عند الحاجة', 'type' => 'text'],
        '_a3_drive_advice' => ['label' => 'نصيحة القيادة', 'type' => 'textarea'],
        '_a3_source_url' => ['label' => 'المصدر الفني / الرسمي', 'type' => 'url'],
        '_a3_source_checked_at' => ['label' => 'تاريخ مراجعة المصدر', 'type' => 'date'],
        '_a3_related_post_ids' => ['label' => 'معرّفات المقالات المرتبطة', 'type' => 'text', 'placeholder' => 'مثال: 123,456'],
    ];

    public static function init(): void {
        add_action('add_meta_boxes', [__CLASS__, 'add_boxes']);
        add_action('save_post', [__CLASS__, 'save'], 10, 2);
    }

    public static function add_boxes(): void {
        foreach (['a3_car', 'a3_motorcycle'] as $type) {
            add_meta_box(
                'a3cp_vehicle_data',
                'بيانات المركبة — A3tal Platform',
                [__CLASS__, 'render_vehicle'],
                $type,
                'normal',
                'high'
            );
        }

        add_meta_box(
            'a3cp_car_extra',
            'بيانات إضافية للسيارة',
            [__CLASS__, 'render_car_extra'],
            'a3_car',
            'side',
            'default'
        );

        foreach (['a3_service_center', 'a3_showroom'] as $type) {
            add_meta_box(
                'a3cp_directory_data',
                'بيانات المكان والتحقق — A3tal Platform',
                [__CLASS__, 'render_directory'],
                $type,
                'normal',
                'high'
            );
        }

        add_meta_box(
            'a3cp_dtc_data',
            'بيانات كود العطل — A3tal Platform',
            [__CLASS__, 'render_dtc'],
            'a3_dtc',
            'normal',
            'high'
        );
    }

    public static function render_vehicle(WP_Post $post): void {
        self::nonce();
        echo '<div class="a3cp-fields">';
        self::render_fields($post, self::VEHICLE_FIELDS);
        echo '</div>';
        echo '<p><strong>مهم:</strong> لا تنشر سعرًا أو مواصفة باعتبارها مؤكدة قبل إضافة المصدر وتاريخ المراجعة.</p>';
    }

    public static function render_car_extra(WP_Post $post): void {
        self::nonce();
        self::field($post, '_a3_seats', ['label' => 'عدد المقاعد', 'type' => 'number']);
    }

    public static function render_directory(WP_Post $post): void {
        self::nonce();
        echo '<div class="a3cp-fields">';
        self::render_fields($post, self::DIRECTORY_FIELDS);
        echo '</div>';
        echo '<p><strong>حالة الاعتماد:</strong> اخترها من صندوق «حالة الاعتماد». استخدم «معتمد رسميًا» فقط عند وجود إثبات رسمي، و«موثّق من أعطال» بعد التحقق الفعلي من البيانات.</p>';
    }

    public static function render_dtc(WP_Post $post): void {
        self::nonce();
        echo '<div class="a3cp-fields">';
        self::render_fields($post, self::DTC_FIELDS);
        echo '</div>';
        echo '<p>عنوان الصفحة يكتب للقارئ، بينما حقل «الكود» يحتفظ بالقيمة القياسية مثل P0420.</p>';
    }

    private static function nonce(): void {
        wp_nonce_field('a3cp_save_entity', 'a3cp_entity_nonce');
    }

    private static function render_fields(WP_Post $post, array $fields): void {
        foreach ($fields as $key => $cfg) {
            self::field($post, $key, $cfg);
        }
    }

    private static function field(WP_Post $post, string $key, array $cfg): void {
        $value = get_post_meta($post->ID, $key, true);
        $label = esc_html($cfg['label'] ?? $key);
        $type = $cfg['type'] ?? 'text';
        $placeholder = esc_attr($cfg['placeholder'] ?? '');

        echo '<p class="a3cp-field">';
        echo '<label for="' . esc_attr($key) . '"><strong>' . $label . '</strong></label>';

        if ($type === 'textarea') {
            echo '<textarea class="widefat" rows="3" id="' . esc_attr($key) . '" name="' . esc_attr($key) . '" placeholder="' . $placeholder . '">' . esc_textarea((string) $value) . '</textarea>';
        } elseif ($type === 'select') {
            echo '<select class="widefat" id="' . esc_attr($key) . '" name="' . esc_attr($key) . '">';
            echo '<option value="">— اختر —</option>';
            foreach (($cfg['options'] ?? []) as $option_value => $option_label) {
                echo '<option value="' . esc_attr($option_value) . '" ' . selected((string) $value, (string) $option_value, false) . '>' . esc_html($option_label) . '</option>';
            }
            echo '</select>';
        } else {
            $step = isset($cfg['step']) ? ' step="' . esc_attr($cfg['step']) . '"' : '';
            echo '<input class="widefat" type="' . esc_attr($type) . '" id="' . esc_attr($key) . '" name="' . esc_attr($key) . '" value="' . esc_attr((string) $value) . '" placeholder="' . $placeholder . '"' . $step . '>';
        }

        echo '</p>';
    }

    public static function save(int $post_id, WP_Post $post): void {
        if (!isset($_POST['a3cp_entity_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['a3cp_entity_nonce'])), 'a3cp_save_entity')) return;
        if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;
        if (wp_is_post_revision($post_id)) return;
        if (!current_user_can('edit_post', $post_id)) return;

        $fields = [];
        if (in_array($post->post_type, ['a3_car', 'a3_motorcycle'], true)) {
            $fields = self::VEHICLE_FIELDS;
            if ($post->post_type === 'a3_car') {
                $fields['_a3_seats'] = ['type' => 'number'];
            }
        } elseif (in_array($post->post_type, ['a3_service_center', 'a3_showroom'], true)) {
            $fields = self::DIRECTORY_FIELDS;
        } elseif ($post->post_type === 'a3_dtc') {
            $fields = self::DTC_FIELDS;
        } else {
            return;
        }

        foreach ($fields as $key => $cfg) {
            if (!array_key_exists($key, $_POST)) continue;
            $raw = wp_unslash($_POST[$key]);
            $value = self::sanitize($key, $raw, $cfg['type'] ?? 'text');

            if ($value === '' || $value === null) {
                delete_post_meta($post_id, $key);
            } else {
                update_post_meta($post_id, $key, $value);
            }
        }
    }

    private static function sanitize(string $key, $value, string $type) {
        if (in_array($key, ['_a3_source_url', '_a3_official_source_url'], true)) {
            return esc_url_raw((string) $value);
        }
        if ($key === '_a3_related_post_ids') {
            return A3CP_Content_Types::sanitize_id_list($value);
        }
        if ($key === '_a3_dtc_code') {
            return A3CP_Content_Types::sanitize_dtc_code($value);
        }
        if (in_array($key, ['_a3_severity', '_a3_code_scope'], true)) {
            return sanitize_key((string) $value);
        }
        if ($type === 'number') {
            return A3CP_Content_Types::sanitize_number($value);
        }
        if ($type === 'textarea') {
            return sanitize_textarea_field((string) $value);
        }
        return sanitize_text_field((string) $value);
    }
}
