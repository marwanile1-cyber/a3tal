<?php
/**
 * Plugin Name: A3tal Contact
 * Description: Lightweight contact form and message inbox for A3tal.com.
 * Version: 1.0.0
 * Author: A3tal.com
 */
if (!defined('ABSPATH')) exit;

final class A3tal_Contact {
    const VERSION = '1.0.0';
    const ACTION = 'a3tal_contact_submit';

    public static function init() {
        add_action('init', [__CLASS__, 'register_message_type']);
        add_shortcode('a3tal_contact_form', [__CLASS__, 'shortcode']);
        add_action('admin_post_' . self::ACTION, [__CLASS__, 'handle']);
        add_action('admin_post_nopriv_' . self::ACTION, [__CLASS__, 'handle']);
        add_action('wp_enqueue_scripts', [__CLASS__, 'assets']);
        add_filter('manage_a3tal_message_posts_columns', [__CLASS__, 'columns']);
        add_action('manage_a3tal_message_posts_custom_column', [__CLASS__, 'column_content'], 10, 2);
    }

    public static function register_message_type() {
        register_post_type('a3tal_message', [
            'labels' => [
                'name' => 'رسائل التواصل',
                'singular_name' => 'رسالة',
                'menu_name' => 'رسائل التواصل',
                'all_items' => 'كل الرسائل',
                'view_item' => 'عرض الرسالة',
                'search_items' => 'بحث في الرسائل',
                'not_found' => 'لا توجد رسائل',
            ],
            'public' => false,
            'show_ui' => true,
            'show_in_menu' => true,
            'supports' => ['title', 'editor'],
            'menu_icon' => 'dashicons-email-alt',
            'capability_type' => 'post',
            'map_meta_cap' => true,
        ]);
    }

    public static function assets() {
        if (!is_singular()) return;
        global $post;
        if (!$post || strpos((string)$post->post_content, '[a3tal_contact_form') === false) return;
        wp_enqueue_style('a3tal-contact', plugin_dir_url(__FILE__) . 'assets/contact.css', [], self::VERSION);
    }

    private static function types() {
        return [
            'content' => 'تصحيح أو ملاحظة على المحتوى',
            'technical' => 'مشكلة فنية في الموقع',
            'business' => 'إعلان أو شراكة',
            'centers' => 'إضافة أو تحديث مركز خدمة',
            'other' => 'استفسار آخر',
        ];
    }

    public static function shortcode() {
        $status = isset($_GET['contact_status']) ? sanitize_key(wp_unslash($_GET['contact_status'])) : '';
        ob_start(); ?>
        <div class="a3-contact-wrap">
            <?php if ($status === 'sent'): ?>
                <div class="a3-contact-alert a3-contact-success" role="status">تم استلام رسالتك بنجاح. سيقوم فريق أعطال.كوم بمراجعتها.</div>
            <?php elseif ($status === 'error'): ?>
                <div class="a3-contact-alert a3-contact-error" role="alert">لم نتمكن من إرسال الرسالة. تأكد من البيانات وحاول مرة أخرى.</div>
            <?php elseif ($status === 'rate'): ?>
                <div class="a3-contact-alert a3-contact-error" role="alert">تم إرسال عدة رسائل خلال وقت قصير. حاول مرة أخرى لاحقًا.</div>
            <?php endif; ?>

            <form class="a3-contact-form" method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                <input type="hidden" name="action" value="<?php echo esc_attr(self::ACTION); ?>">
                <?php wp_nonce_field('a3tal_contact_form', 'a3tal_contact_nonce'); ?>
                <div class="a3-contact-hp" aria-hidden="true">
                    <label>اترك هذا الحقل فارغًا <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
                </div>
                <div class="a3-contact-grid">
                    <div class="a3-contact-field">
                        <label for="a3-name">الاسم <span>*</span></label>
                        <input id="a3-name" type="text" name="name" required maxlength="100" autocomplete="name">
                    </div>
                    <div class="a3-contact-field">
                        <label for="a3-email">البريد الإلكتروني <span>*</span></label>
                        <input id="a3-email" type="email" name="email" required maxlength="190" autocomplete="email" inputmode="email">
                    </div>
                </div>
                <div class="a3-contact-field">
                    <label for="a3-type">موضوع التواصل <span>*</span></label>
                    <select id="a3-type" name="type" required>
                        <?php foreach (self::types() as $key => $label): ?>
                            <option value="<?php echo esc_attr($key); ?>"><?php echo esc_html($label); ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="a3-contact-field">
                    <label for="a3-subject">عنوان الرسالة</label>
                    <input id="a3-subject" type="text" name="subject" maxlength="160">
                </div>
                <div class="a3-contact-field">
                    <label for="a3-message">التفاصيل <span>*</span></label>
                    <textarea id="a3-message" name="message" required minlength="10" maxlength="5000" rows="8" placeholder="اكتب التفاصيل بوضوح، وإذا كانت الملاحظة تخص مقالًا أضف رابط الصفحة."></textarea>
                </div>
                <label class="a3-contact-consent"><input type="checkbox" name="consent" value="1" required> أوافق على استخدام بياناتي للرد على هذه الرسالة وفق سياسة الخصوصية.</label>
                <button class="a3-contact-submit" type="submit">إرسال الرسالة</button>
                <p class="a3-contact-note">هذا النموذج للملاحظات والتواصل العام، وليس بديلًا عن الفحص الفني للسيارة أو خدمات الطوارئ.</p>
            </form>
        </div>
        <?php return ob_get_clean();
    }

    private static function redirect($status) {
        $ref = wp_get_referer();
        if (!$ref) $ref = home_url('/اتصل-بنا/');
        $ref = remove_query_arg('contact_status', $ref);
        wp_safe_redirect(add_query_arg('contact_status', $status, $ref));
        exit;
    }

    public static function handle() {
        if (!isset($_POST['a3tal_contact_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['a3tal_contact_nonce'])), 'a3tal_contact_form')) {
            self::redirect('error');
        }

        if (!empty($_POST['website'])) {
            self::redirect('sent');
        }

        $ip = isset($_SERVER['REMOTE_ADDR']) ? (string) $_SERVER['REMOTE_ADDR'] : '';
        $ip_hash = hash_hmac('sha256', $ip, wp_salt('auth'));
        $rate_key = 'a3tal_contact_' . substr($ip_hash, 0, 24);
        $count = (int) get_transient($rate_key);
        if ($count >= 4) self::redirect('rate');
        set_transient($rate_key, $count + 1, 15 * MINUTE_IN_SECONDS);

        $name = sanitize_text_field(wp_unslash($_POST['name'] ?? ''));
        $email = sanitize_email(wp_unslash($_POST['email'] ?? ''));
        $type = sanitize_key(wp_unslash($_POST['type'] ?? 'other'));
        $subject = sanitize_text_field(wp_unslash($_POST['subject'] ?? ''));
        $message = sanitize_textarea_field(wp_unslash($_POST['message'] ?? ''));
        $consent = !empty($_POST['consent']);

        $types = self::types();
        if (!isset($types[$type])) $type = 'other';

        if ($name === '' || !is_email($email) || mb_strlen($message) < 10 || !$consent) {
            self::redirect('error');
        }

        $post_title = sprintf('%s — %s — %s', $types[$type], $name, current_time('Y-m-d H:i'));
        $post_id = wp_insert_post([
            'post_type' => 'a3tal_message',
            'post_status' => 'private',
            'post_title' => wp_strip_all_tags($post_title),
            'post_content' => $message,
        ], true);

        if (is_wp_error($post_id)) self::redirect('error');

        update_post_meta($post_id, '_a3tal_contact_name', $name);
        update_post_meta($post_id, '_a3tal_contact_email', $email);
        update_post_meta($post_id, '_a3tal_contact_type', $type);
        update_post_meta($post_id, '_a3tal_contact_subject', $subject);
        update_post_meta($post_id, '_a3tal_contact_ip_hash', $ip_hash);
        update_post_meta($post_id, '_a3tal_contact_source', esc_url_raw(wp_get_referer()));

        $admin_email = sanitize_email((string) get_option('admin_email'));
        if (is_email($admin_email)) {
            $mail_subject = '[A3tal] ' . $types[$type] . ($subject ? ' — ' . $subject : '');
            $body = "الاسم: {$name}\nالبريد: {$email}\nالنوع: {$types[$type]}\n";
            if ($subject) $body .= "العنوان: {$subject}\n";
            $body .= "\nالرسالة:\n{$message}\n\nرقم الرسالة: {$post_id}\n";
            $headers = ['Reply-To: ' . $name . ' <' . $email . '>'];
            wp_mail($admin_email, $mail_subject, $body, $headers);
        }

        self::redirect('sent');
    }

    public static function columns($columns) {
        return [
            'cb' => $columns['cb'] ?? '<input type="checkbox" />',
            'title' => 'الرسالة',
            'a3tal_type' => 'النوع',
            'a3tal_sender' => 'المرسل',
            'date' => 'التاريخ',
        ];
    }

    public static function column_content($column, $post_id) {
        if ($column === 'a3tal_type') {
            $type = (string) get_post_meta($post_id, '_a3tal_contact_type', true);
            $types = self::types();
            echo esc_html($types[$type] ?? $type);
        }
        if ($column === 'a3tal_sender') {
            $name = (string) get_post_meta($post_id, '_a3tal_contact_name', true);
            $email = (string) get_post_meta($post_id, '_a3tal_contact_email', true);
            echo esc_html($name);
            if ($email) echo '<br><a href="mailto:' . esc_attr($email) . '">' . esc_html($email) . '</a>';
        }
    }
}
A3tal_Contact::init();
