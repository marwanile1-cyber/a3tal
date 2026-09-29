<?php
/**
 * Plugin Name: A3tal Editorial Trust
 * Description: Editorial roles, public author profiles, reviewer attribution and trust metadata for A3tal.com.
 * Version: 1.1.0
 * Author: A3tal.com
 */
if (!defined('ABSPATH')) exit;

final class A3tal_Editorial_Trust {
    const VERSION = '1.1.0';
    const META_REVIEWER = '_a3tal_reviewed_by';

    public static function init() {
        add_action('init', [__CLASS__, 'register_roles']);
        add_action('show_user_profile', [__CLASS__, 'profile_fields']);
        add_action('edit_user_profile', [__CLASS__, 'profile_fields']);
        add_action('personal_options_update', [__CLASS__, 'save_profile_fields']);
        add_action('edit_user_profile_update', [__CLASS__, 'save_profile_fields']);
        add_action('add_meta_boxes', [__CLASS__, 'add_review_box']);
        add_action('save_post_post', [__CLASS__, 'save_review_box']);
        add_filter('the_content', [__CLASS__, 'append_trust_box'], 30);
        add_shortcode('a3tal_team', [__CLASS__, 'team_shortcode']);
    }

    public static function register_roles() {
        if (!get_role('a3tal_writer')) {
            add_role('a3tal_writer', 'كاتب أعطال', [
                'read' => true,
                'edit_posts' => true,
                'delete_posts' => true,
                'upload_files' => true,
            ]);
        }
        if (!get_role('a3tal_reviewer')) {
            add_role('a3tal_reviewer', 'مراجع محتوى أعطال', [
                'read' => true,
                'edit_posts' => true,
                'edit_others_posts' => true,
                'edit_published_posts' => true,
                'upload_files' => true,
            ]);
        }
    }

    private static function meta_fields() {
        return [
            'a3tal_role_title' => 'المسمى التحريري',
            'a3tal_specialty' => 'التخصص',
            'a3tal_experience' => 'الخبرة العملية أو التحريرية',
            'a3tal_credentials' => 'المؤهلات أو الاعتمادات',
            'a3tal_profile_url' => 'رابط مهني موثوق',
        ];
    }

    public static function profile_fields($user) {
        if (!current_user_can('edit_user', $user->ID)) return;
        ?>
        <h2>ملف أعطال.كوم التحريري</h2>
        <table class="form-table" role="presentation">
            <?php foreach (self::meta_fields() as $key => $label): ?>
                <tr>
                    <th><label for="<?php echo esc_attr($key); ?>"><?php echo esc_html($label); ?></label></th>
                    <td><input type="text" class="regular-text" id="<?php echo esc_attr($key); ?>" name="<?php echo esc_attr($key); ?>" value="<?php echo esc_attr(get_user_meta($user->ID, $key, true)); ?>"></td>
                </tr>
            <?php endforeach; ?>
            <tr>
                <th>إظهار الملف للعامة</th>
                <td><label><input type="checkbox" name="a3tal_public_profile" value="1" <?php checked((bool)get_user_meta($user->ID, 'a3tal_public_profile', true)); ?>> أعرض هذا الكاتب/المراجع في الموقع بعد اكتمال اسمه وسيرته</label></td>
            </tr>
        </table>
        <?php
    }

    public static function save_profile_fields($user_id) {
        if (!current_user_can('edit_user', $user_id)) return;
        foreach (self::meta_fields() as $key => $label) {
            if (isset($_POST[$key])) update_user_meta($user_id, $key, sanitize_text_field(wp_unslash($_POST[$key])));
        }
        update_user_meta($user_id, 'a3tal_public_profile', !empty($_POST['a3tal_public_profile']) ? 1 : 0);
    }

    private static function is_public_profile($user_id) {
        $u = get_userdata($user_id);
        if (!$u) return false;
        if (!get_user_meta($user_id, 'a3tal_public_profile', true)) return false;
        if (strpos((string)$u->display_name, '@') !== false) return false;
        $bio = trim((string)get_the_author_meta('description', $user_id));
        $role = trim((string)get_user_meta($user_id, 'a3tal_role_title', true));
        return $u->display_name !== '' && ($bio !== '' || $role !== '');
    }

    public static function add_review_box() {
        add_meta_box('a3tal-reviewer', 'المراجعة التحريرية', [__CLASS__, 'review_box'], 'post', 'side', 'high');
    }

    public static function review_box($post) {
        wp_nonce_field('a3tal_reviewer_save', 'a3tal_reviewer_nonce');
        $current = (int)get_post_meta($post->ID, self::META_REVIEWER, true);
        $users = get_users(['role__in' => ['a3tal_reviewer', 'editor', 'administrator'], 'orderby' => 'display_name']);
        echo '<p><label for="a3tal-reviewed-by">تمت المراجعة بواسطة</label></p>';
        echo '<select id="a3tal-reviewed-by" name="a3tal_reviewed_by" style="width:100%">';
        echo '<option value="0">لم يحدد مراجع</option>';
        foreach ($users as $u) {
            if (strpos((string)$u->display_name, '@') !== false && !self::is_public_profile($u->ID)) continue;
            echo '<option value="' . esc_attr($u->ID) . '" ' . selected($current, $u->ID, false) . '>' . esc_html($u->display_name) . '</option>';
        }
        echo '</select>';
        echo '<p style="font-size:11px;color:#646970">لن يظهر اسم المراجع للعامة إلا إذا كان ملفه العام مكتملًا.</p>';
    }

    public static function save_review_box($post_id) {
        if (!isset($_POST['a3tal_reviewer_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['a3tal_reviewer_nonce'])), 'a3tal_reviewer_save')) return;
        if (!current_user_can('edit_post', $post_id)) return;
        $uid = isset($_POST['a3tal_reviewed_by']) ? absint($_POST['a3tal_reviewed_by']) : 0;
        if ($uid && get_userdata($uid)) update_post_meta($post_id, self::META_REVIEWER, $uid);
        else delete_post_meta($post_id, self::META_REVIEWER);
    }

    private static function person_card($user_id, $label) {
        if (!self::is_public_profile($user_id)) return '';
        $u = get_userdata($user_id);
        $role = trim((string)get_user_meta($user_id, 'a3tal_role_title', true));
        $spec = trim((string)get_user_meta($user_id, 'a3tal_specialty', true));
        $bio = trim((string)get_the_author_meta('description', $user_id));
        $url = trim((string)get_user_meta($user_id, 'a3tal_profile_url', true));
        $avatar = get_avatar($user_id, 64, '', $u->display_name, ['class' => 'a3tal-trust-avatar']);
        $name = esc_html($u->display_name);
        if ($url) $name = '<a href="' . esc_url($url) . '" rel="author noopener">' . $name . '</a>';
        return '<div class="a3tal-trust-person">' . $avatar . '<div><small>' . esc_html($label) . '</small><strong>' . $name . '</strong>' .
            ($role ? '<span>' . esc_html($role) . '</span>' : '') .
            ($spec ? '<em>' . esc_html($spec) . '</em>' : '') .
            ($bio ? '<p>' . esc_html(wp_trim_words($bio, 24)) . '</p>' : '') .
            '</div></div>';
    }

    public static function append_trust_box($content) {
        if (!is_singular('post') || !in_the_loop() || !is_main_query()) return $content;
        $author_id = (int)get_post_field('post_author', get_the_ID());
        $reviewer_id = (int)get_post_meta(get_the_ID(), self::META_REVIEWER, true);
        $author = self::person_card($author_id, 'كتابة');
        $reviewer = $reviewer_id ? self::person_card($reviewer_id, 'مراجعة') : '';
        if ($author === '' && $reviewer === '') return $content;
        $box = '<section class="a3tal-editorial-trust" aria-label="فريق إعداد المحتوى"><h2>فريق إعداد ومراجعة المحتوى</h2><div class="a3tal-trust-grid">' . $author . $reviewer . '</div></section>';
        return $content . $box;
    }

    private static function core_team() {
        return [
            [
                'name' => 'م/ محمد',
                'role' => 'مهندس تشخيص أعطال وتكييف سيارات',
                'experience' => 'خبرة نحو 15 عامًا',
                'center' => 'مركز أوبل كينج دوم',
                'bio' => 'متخصص في تشخيص أعطال السيارات وأنظمة التكييف، ويشارك في المراجعة الفنية للمحتوى المرتبط بالأعراض، خطوات الفحص، وأعطال التكييف.'
            ],
            [
                'name' => 'م/ أحمد',
                'role' => 'مهندس استقبال وفحص شامل للسيارات',
                'experience' => 'خبرة نحو 10 سنوات',
                'center' => 'مركز أوبل كينج دوم',
                'bio' => 'متخصص في الكشف على حالة السيارة بالكامل وتشخيص مشكلات الميكانيكا والعفشة، ويشارك في مراجعة المحتوى المرتبط بالفحص والتشخيص العام.'
            ],
            [
                'name' => 'م/ محمود',
                'role' => 'متخصص كهرباء سيارات',
                'experience' => 'خبرة نحو 5 سنوات',
                'center' => 'مركز أوبل كينج دوم',
                'bio' => 'متخصص في أعطال كهرباء السيارات، ويشارك في مراجعة المحتوى المرتبط بالدوائر الكهربائية، الشحن، البطارية، والحساسات.'
            ],
        ];
    }

    private static function core_team_card($person) {
        return '<article class="a3tal-trust-person a3tal-core-team-person"><div class="a3tal-team-initial">' . esc_html(mb_substr(str_replace('م/ ', '', $person['name']), 0, 1)) . '</div><div><small>فريق المراجعة الفنية</small><strong>' . esc_html($person['name']) . '</strong><span>' . esc_html($person['role']) . '</span><em>' . esc_html($person['experience']) . ' • ' . esc_html($person['center']) . '</em><p>' . esc_html($person['bio']) . '</p></div></article>';
    }

    public static function team_shortcode() {
        $cards = '';
        foreach (self::core_team() as $person) {
            $cards .= self::core_team_card($person);
        }

        $users = get_users(['meta_key' => 'a3tal_public_profile', 'meta_value' => '1', 'orderby' => 'display_name']);
        foreach ($users as $u) {
            if (!self::is_public_profile($u->ID)) continue;
            $cards .= self::person_card($u->ID, 'فريق أعطال.كوم');
        }

        return '<div class="a3tal-team-intro"><p>يعتمد أعطال.كوم على مراجعة فنية عملية للمحتوى المتخصص في الأعطال والصيانة، مع الاستفادة من خبرات فريق يعمل في مركز أوبل كينج دوم.</p></div><div class="a3tal-team-grid">' . $cards . '</div>';
    }
}
A3tal_Editorial_Trust::init();

add_action('wp_enqueue_scripts', function() {
    if (!is_singular() && !is_page()) return;
    wp_register_style('a3tal-editorial-trust-inline', false, [], A3tal_Editorial_Trust::VERSION);
    wp_enqueue_style('a3tal-editorial-trust-inline');
    wp_add_inline_style('a3tal-editorial-trust-inline', '.a3tal-editorial-trust{margin:34px 0;padding:20px;border:1px solid #e2e8f0;border-radius:18px;background:#f8fafc}.a3tal-editorial-trust h2{margin-top:0}.a3tal-trust-grid,.a3tal-team-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}.a3tal-trust-person{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:14px}.a3tal-trust-avatar{border-radius:50%}.a3tal-trust-person small,.a3tal-trust-person span,.a3tal-trust-person em{display:block}.a3tal-trust-person small{color:#64748b;font-size:11px}.a3tal-trust-person strong{display:block;font-size:15px;margin:2px 0}.a3tal-trust-person span{font-size:12px;color:#334155}.a3tal-trust-person em{font-size:11px;color:#64748b;font-style:normal}.a3tal-trust-person p{font-size:12px;color:#475569;margin:8px 0 0}');
});
