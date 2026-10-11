<?php
/** Anonymous, moderated discussions scoped to published DTC guides. */
if (!defined('ABSPATH')) exit;

add_action('init', function() {
    if (post_type_exists('a3_dtc')) add_post_type_support('a3_dtc', 'comments');
}, 99);

function a3g_dtc_discussion_assets() {
    if (!function_exists('a3g_dtc_is_library') || !a3g_dtc_is_library()) return;
    wp_enqueue_script('a3g-dtc-library', get_template_directory_uri().'/assets/js/dtc-library.js', [], '1.0.0', true);
    wp_localize_script('a3g-dtc-library', 'a3Dtc', ['ajaxUrl' => admin_url('admin-ajax.php')]);
}
add_action('wp_enqueue_scripts', 'a3g_dtc_discussion_assets', 20);

function a3g_dtc_discussion_target($post_id) {
    if (!function_exists('a3g_dtc_is_comment_target') || !a3g_dtc_is_comment_target($post_id)) return false;
    $post = get_post($post_id);
    return $post && $post->post_status === 'publish' && $post->post_password === '';
}

function a3g_dtc_origin($url) {
    $parts = wp_parse_url($url);
    if (!is_array($parts) || empty($parts['host']) || empty($parts['scheme'])) return '';
    $scheme = strtolower($parts['scheme']);
    if (!in_array($scheme, ['http', 'https'], true)) return '';
    $port = isset($parts['port']) ? (int)$parts['port'] : ($scheme === 'https' ? 443 : 80);
    return $scheme.'://'.strtolower($parts['host']).':'.$port;
}

function a3g_dtc_request_is_same_origin() {
    $origin = isset($_SERVER['HTTP_ORIGIN']) && is_string($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
    if ($origin === '') $origin = isset($_SERVER['HTTP_REFERER']) && is_string($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : '';
    $actual = a3g_dtc_origin($origin);
    return $actual !== '' && $actual === a3g_dtc_origin(home_url('/'));
}

function a3g_dtc_field($name) {
    return isset($_POST[$name]) && is_string($_POST[$name]) ? trim(wp_unslash($_POST[$name])) : '';
}

function a3g_dtc_digits($value) {
    return strtr($value, ['٠'=>'0','١'=>'1','٢'=>'2','٣'=>'3','٤'=>'4','٥'=>'5','٦'=>'6','٧'=>'7','٨'=>'8','٩'=>'9','۰'=>'0','۱'=>'1','۲'=>'2','۳'=>'3','۴'=>'4','۵'=>'5','۶'=>'6','۷'=>'7','۸'=>'8','۹'=>'9']);
}

function a3g_dtc_text_length($value) {
    return function_exists('mb_strlen') ? mb_strlen($value, 'UTF-8') : preg_match_all('/./us', $value);
}

function a3g_dtc_visitor() {
    $value = a3g_dtc_field('visitor');
    return preg_match('/\A[a-zA-Z0-9_-]{16,96}\z/D', $value) ? $value : '';
}

function a3g_dtc_fingerprint($value) {
    return substr(hash_hmac('sha256', $value, wp_salt('nonce')), 0, 40);
}

function a3g_dtc_request_ip() {
    // Do not trust client-supplied X-Forwarded-For / CDN headers for rate limits.
    $value = isset($_SERVER['REMOTE_ADDR']) && is_string($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
    return filter_var($value, FILTER_VALIDATE_IP) ? $value : 'unknown';
}

function a3g_dtc_challenge($post_id, $visitor) {
    $payload = time().'.'.wp_generate_password(24, false, false);
    return $payload.'.'.hash_hmac('sha256', $post_id.'|'.$visitor.'|'.$payload, wp_salt('nonce'));
}

function a3g_dtc_challenge_valid($challenge, $post_id, $visitor) {
    if (!preg_match('/\A([0-9]{10})\.([a-zA-Z0-9]{24})\.([a-f0-9]{64})\z/D', $challenge, $parts)) return false;
    $age = time() - (int)$parts[1];
    $expected = hash_hmac('sha256', $post_id.'|'.$visitor.'|'.$parts[1].'.'.$parts[2], wp_salt('nonce'));
    return $age >= 2 && $age <= 30 * MINUTE_IN_SECONDS && hash_equals($expected, $parts[3]);
}

function a3g_dtc_json_error($code, $message, $status = 400) {
    nocache_headers();
    wp_send_json_error(['code' => $code, 'message' => $message], $status);
}

function a3g_dtc_ajax_context($needs_token = true) {
    if (!a3g_dtc_request_is_same_origin()) a3g_dtc_json_error('origin', 'افتح صفحة الكود على أعطال ثم حاول مرة أخرى.', 403);
    $post_id_raw = a3g_dtc_field('post_id');
    $post_id = ctype_digit($post_id_raw) ? (int)$post_id_raw : 0;
    if (!$post_id || !a3g_dtc_discussion_target($post_id)) a3g_dtc_json_error('target', 'هذه المناقشة غير متاحة.', 404);
    $visitor = a3g_dtc_visitor();
    if (!$visitor) a3g_dtc_json_error('visitor', 'تعذر تجهيز المشاركة. حدّث الصفحة وحاول مرة أخرى.');
    if (a3g_dtc_field('website') !== '') a3g_dtc_json_error('validation', 'تعذر إرسال المشاركة.');
    if ($needs_token) {
        if (!wp_verify_nonce(a3g_dtc_field('_ajax_nonce'), 'a3g_dtc_discuss_'.$post_id)) a3g_dtc_json_error('token_expired', 'انتهت صلاحية النموذج. سنجهّزه مجددًا، ثم يمكنك الإرسال.', 403);
        if (!a3g_dtc_challenge_valid(a3g_dtc_field('challenge'), $post_id, $visitor)) a3g_dtc_json_error('token_expired', 'انتظر لحظات ثم حاول إرسال مشاركتك مرة أخرى.', 403);
    }
    return ['post_id' => $post_id, 'visitor' => $visitor, 'ip' => a3g_dtc_request_ip()];
}

function a3g_dtc_ajax_token() {
    $context = a3g_dtc_ajax_context(false);
    nocache_headers();
    wp_send_json_success([
        'nonce' => wp_create_nonce('a3g_dtc_discuss_'.$context['post_id']),
        'challenge' => a3g_dtc_challenge($context['post_id'], $context['visitor']),
        'expiresIn' => 30 * MINUTE_IN_SECONDS,
    ]);
}
add_action('wp_ajax_a3g_dtc_token', 'a3g_dtc_ajax_token');
add_action('wp_ajax_nopriv_a3g_dtc_token', 'a3g_dtc_ajax_token');

function a3g_dtc_rate_limit($context, $mode) {
    $visitor_key = 'a3g_dtc_'.$mode.'_v_'.a3g_dtc_fingerprint($context['visitor']);
    $ip_key = 'a3g_dtc_'.$mode.'_ip_'.a3g_dtc_fingerprint($context['ip']);
    $now = time();
    $visitor = get_transient($visitor_key);
    $ip = get_transient($ip_key);
    if (!is_array($visitor) || $now - (int)$visitor['start'] >= HOUR_IN_SECONDS) $visitor = ['start' => $now, 'last' => 0, 'count' => 0];
    if (!is_array($ip) || $now - (int)$ip['start'] >= HOUR_IN_SECONDS) $ip = ['start' => $now, 'count' => 0];
    // Allows an ordinary reply conversation while bounding automated submissions.
    if ($now - (int)$visitor['last'] < 8 || (int)$visitor['count'] >= 20 || (int)$ip['count'] >= 80) {
        a3g_dtc_json_error('rate_limit', 'أرسلت مشاركات متتابعة بسرعة. انتظر قليلًا ثم حاول مرة أخرى.', 429);
    }
    $visitor['last'] = $now;
    $visitor['count']++;
    $ip['count']++;
    set_transient($visitor_key, $visitor, HOUR_IN_SECONDS);
    set_transient($ip_key, $ip, HOUR_IN_SECONDS);
}

function a3g_dtc_force_pending($approved, $data) {
    // Respect anti-spam decisions and errors; otherwise require manual approval.
    if (is_wp_error($approved) || in_array($approved, ['spam', 'trash'], true)) return $approved;
    return 0;
}

function a3g_dtc_ajax_comment() {
    $context = a3g_dtc_ajax_context();
    $post_id = $context['post_id'];
    $alias = sanitize_text_field(a3g_dtc_field('alias'));
    $body = sanitize_textarea_field(a3g_dtc_field('comment'));
    $car = sanitize_text_field(a3g_dtc_field('car'));
    $year = a3g_dtc_digits(a3g_dtc_field('year'));
    $codes = strtoupper(sanitize_text_field(a3g_dtc_digits(a3g_dtc_field('codes'))));
    $tried = sanitize_textarea_field(a3g_dtc_field('tried'));
    if (!is_user_logged_in() && ($alias === '' || a3g_dtc_text_length($alias) > 60)) a3g_dtc_json_error('alias', 'اكتب اسمًا ظاهرًا لا يتجاوز 60 حرفًا.');
    if (a3g_dtc_text_length($body) < 5 || a3g_dtc_text_length($body) > 5000) a3g_dtc_json_error('comment', 'اكتب مشاركتك بين 5 و5000 حرف.');
    if (a3g_dtc_text_length($car) > 120 || a3g_dtc_text_length($codes) > 120 || a3g_dtc_text_length($tried) > 1500) a3g_dtc_json_error('details', 'اختصر معلومات السيارة والأكواد وما جُرّب، ثم أعد الإرسال.');
    if ($year !== '' && (!preg_match('/\A[0-9]{4}\z/D', $year) || (int)$year < 1950 || (int)$year > (int)wp_date('Y') + 2)) a3g_dtc_json_error('year', 'اكتب سنة موديل صحيحة من أربعة أرقام.');
    $parent_raw = a3g_dtc_field('comment_parent');
    if ($parent_raw !== '' && !ctype_digit($parent_raw)) a3g_dtc_json_error('parent', 'تعذر تحديد التعليق الذي ترد عليه.');
    $parent_id = (int)$parent_raw;
    if ($parent_id) {
        $parent = get_comment($parent_id);
        if (!$parent || (int)$parent->comment_post_ID !== $post_id || (string)$parent->comment_approved !== '1' || !in_array($parent->comment_type, ['', 'comment'], true)) a3g_dtc_json_error('parent', 'يمكن الرد على المشاركات المنشورة في هذه الصفحة فقط.');
    }
    a3g_dtc_rate_limit($context, 'submit');
    // Scoped filters only while this validated custom request is processed.
    // Ordinary WordPress comment endpoints/settings remain unchanged.
    $open = function($value, $id) use ($post_id) { return (int)$id === $post_id ? true : $value; };
    $disabled = function() { return 0; };
    $pending = function($approved, $data) use ($post_id) {
        return (int)($data['comment_post_ID'] ?? 0) === $post_id ? a3g_dtc_force_pending($approved, $data) : $approved;
    };
    $silent = function($notify, $comment_id) use ($post_id) {
        $item = get_comment($comment_id);
        return $item && (int)$item->comment_post_ID === $post_id ? false : $notify;
    };
    add_filter('comments_open', $open, PHP_INT_MAX, 2);
    add_filter('pre_option_require_name_email', $disabled, PHP_INT_MAX);
    add_filter('pre_option_comment_registration', $disabled, PHP_INT_MAX);
    add_filter('pre_comment_approved', $pending, PHP_INT_MAX, 2);
    add_filter('notify_moderator', $silent, PHP_INT_MAX, 2);
    add_filter('notify_post_author', $silent, PHP_INT_MAX, 2);
    try {
        $comment = wp_handle_comment_submission([
            'comment_post_ID' => $post_id,
            'author' => $alias,
            'email' => '',
            'url' => '',
            'comment' => $body,
            'comment_parent' => $parent_id,
        ]);
    } finally {
        remove_filter('comments_open', $open, PHP_INT_MAX);
        remove_filter('pre_option_require_name_email', $disabled, PHP_INT_MAX);
        remove_filter('pre_option_comment_registration', $disabled, PHP_INT_MAX);
        remove_filter('pre_comment_approved', $pending, PHP_INT_MAX);
        remove_filter('notify_moderator', $silent, PHP_INT_MAX);
        remove_filter('notify_post_author', $silent, PHP_INT_MAX);
    }
    if (is_wp_error($comment)) {
        $code = $comment->get_error_code();
        $message = 'تعذر حفظ المشاركة الآن. حاول مرة أخرى بعد قليل.';
        if ($code === 'comment_duplicate') $message = 'هذه المشاركة أُرسلت بالفعل. ستظهر بعد مراجعتها.';
        elseif ($code === 'comment_flood') $message = 'انتظر قليلًا قبل إرسال مشاركة جديدة.';
        a3g_dtc_json_error($code, $message, in_array($code, ['comment_duplicate','comment_flood'], true) ? 429 : 400);
    }
    add_comment_meta($comment->comment_ID, '_a3g_dtc_discussion', 1, true);
    foreach (['car'=>$car, 'year'=>$year, 'codes'=>$codes, 'tried'=>$tried] as $key=>$value) {
        if ($value !== '') add_comment_meta($comment->comment_ID, '_a3g_dtc_'.$key, $value, true);
    }
    if ((string)$comment->comment_approved === '1') wp_set_comment_status($comment->comment_ID, 'hold');
    nocache_headers();
    wp_send_json_success(['message' => 'تم استلام مشاركتك. ستظهر بعد مراجعة فريق أعطال. احتفظ برابط الصفحة للعودة ومتابعة الردود.']);
}
add_action('wp_ajax_a3g_dtc_comment', 'a3g_dtc_ajax_comment');
add_action('wp_ajax_nopriv_a3g_dtc_comment', 'a3g_dtc_ajax_comment');

function a3g_dtc_ajax_report() {
    $context = a3g_dtc_ajax_context();
    $id_raw = a3g_dtc_field('comment_id');
    $comment_id = ctype_digit($id_raw) ? (int)$id_raw : 0;
    $comment = get_comment($comment_id);
    if (!$comment || (int)$comment->comment_post_ID !== $context['post_id'] || (string)$comment->comment_approved !== '1' || !in_array($comment->comment_type, ['', 'comment'], true)) a3g_dtc_json_error('target', 'يمكن الإبلاغ عن المشاركات المنشورة في هذه الصفحة فقط.', 404);
    $key = '_a3g_dtc_report_'.a3g_dtc_fingerprint($context['ip'].'|'.$context['visitor']);
    if (!get_comment_meta($comment_id, $key, true)) {
        a3g_dtc_rate_limit($context, 'report');
        if (add_comment_meta($comment_id, $key, current_time('mysql'), true)) {
            $count = (int)get_comment_meta($comment_id, '_a3g_dtc_report_count', true);
            update_comment_meta($comment_id, '_a3g_dtc_report_count', $count + 1);
            update_comment_meta($comment_id, '_a3g_dtc_reported_at', current_time('mysql'));
        }
    }
    nocache_headers();
    wp_send_json_success(['message' => 'وصل البلاغ إلى فريق أعطال للمراجعة.']);
}
add_action('wp_ajax_a3g_dtc_report', 'a3g_dtc_ajax_report');
add_action('wp_ajax_nopriv_a3g_dtc_report', 'a3g_dtc_ajax_report');

// No new email/subscription flow, including when moderators later approve it.
function a3g_dtc_comment_mail($notify, $comment_id) {
    return get_comment_meta($comment_id, '_a3g_dtc_discussion', true) ? false : $notify;
}
add_filter('notify_moderator', 'a3g_dtc_comment_mail', 20, 2);
add_filter('notify_post_author', 'a3g_dtc_comment_mail', 20, 2);

function a3g_dtc_comment_depth($comment) {
    $depth = 0;
    $parent_id = (int)$comment->comment_parent;
    while ($parent_id && $depth < 3) {
        $parent = get_comment($parent_id);
        if (!$parent || (int)$parent->comment_post_ID !== (int)$comment->comment_post_ID || (string)$parent->comment_approved !== '1') break;
        $depth++;
        $parent_id = (int)$parent->comment_parent;
    }
    return $depth;
}

/** Match the public discussion's stable date/ID order and 30-item pages. */
function a3g_dtc_comment_url($comment) {
    global $wpdb;
    $comment = get_comment($comment);
    if (!$comment || !a3g_dtc_discussion_target((int)$comment->comment_post_ID)) return home_url('/dtc/');
    $url = get_permalink((int)$comment->comment_post_ID);
    if ((string)$comment->comment_approved !== '1') return $url.'#dtc-discussion';
    $position = (int)$wpdb->get_var($wpdb->prepare(
        "SELECT COUNT(*) FROM {$wpdb->comments} WHERE comment_post_ID=%d AND comment_approved='1' AND comment_type IN ('','comment') AND (comment_date_gmt < %s OR (comment_date_gmt = %s AND comment_ID <= %d))",
        (int)$comment->comment_post_ID, $comment->comment_date_gmt, $comment->comment_date_gmt, (int)$comment->comment_ID
    ));
    $page = max(1, (int)ceil($position / 30));
    if ($page > 1) $url = add_query_arg('dcpage', $page, $url);
    return $url.'#dtc-comment-'.(int)$comment->comment_ID;
}

function a3g_dtc_render_discussion($post_id) {
    $post_id = (int)$post_id;
    if (!a3g_dtc_discussion_target($post_id)) return;
    $page_raw = isset($_GET['dcpage']) && is_scalar($_GET['dcpage']) ? (string)$_GET['dcpage'] : '1';
    $page = ctype_digit($page_raw) ? max(1, (int)$page_raw) : 1;
    $total = (int)get_comments(['post_id'=>$post_id, 'status'=>'approve', 'type'=>'comment', 'count'=>true]);
    $pages = max(1, (int)ceil($total / 30));
    $page = min($page, $pages);
    $comments = get_comments(['post_id'=>$post_id, 'status'=>'approve', 'type'=>'comment', 'number'=>30, 'offset'=>($page-1)*30, 'orderby'=>['comment_date_gmt'=>'ASC', 'comment_ID'=>'ASC'], 'order'=>'ASC']);
    $user = wp_get_current_user();
    ?>
    <section id="dtc-discussion" class="d-discussion d-panel" aria-labelledby="dtc-discussion-title" data-post-id="<?php echo esc_attr($post_id); ?>">
      <header class="d-section-heading">
        <div><span class="d-kicker">تجارب الناس</span><h2 id="dtc-discussion-title" class="d-section-title">اسأل وشارك تجربتك</h2></div>
        <span class="d-discussion-count"><?php echo esc_html(number_format_i18n($total)); ?> مشاركة</span>
      </header>
      <p class="d-discussion-intro">شارك سؤالك أو نتيجة الفحص باسم ظاهر. لا تحتاج إلى حساب. تُراجع المشاركات قبل ظهورها، وتجارب الزوار تخص سياراتهم وظروفها.</p>
      <?php if ($comments): ?>
      <div class="d-discussion-list">
      <?php foreach ($comments as $comment):
          $name = wp_strip_all_tags((string)$comment->comment_author);
          if ($name === '') $name = 'زائر أعطال';
          $letter = function_exists('mb_substr') ? mb_substr($name, 0, 1, 'UTF-8') : preg_replace('/^(.).*$/us', '$1', $name);
          $car = (string)get_comment_meta($comment->comment_ID, '_a3g_dtc_car', true);
          $year = (string)get_comment_meta($comment->comment_ID, '_a3g_dtc_year', true);
          $codes = (string)get_comment_meta($comment->comment_ID, '_a3g_dtc_codes', true);
          $tried = (string)get_comment_meta($comment->comment_ID, '_a3g_dtc_tried', true);
          $parent = $comment->comment_parent ? get_comment($comment->comment_parent) : null;
          if ($parent && ((int)$parent->comment_post_ID !== $post_id || (string)$parent->comment_approved !== '1')) $parent = null;
      ?>
        <article id="dtc-comment-<?php echo esc_attr($comment->comment_ID); ?>" class="d-comment" style="--depth:<?php echo esc_attr(a3g_dtc_comment_depth($comment)); ?>">
          <header class="d-comment-head"><span class="d-avatar" aria-hidden="true"><?php echo esc_html($letter); ?></span><div>
            <strong class="d-comment-name"><?php echo esc_html($name); ?></strong>
            <?php if ((int)$comment->user_id > 0 && user_can((int)$comment->user_id, 'moderate_comments')): ?><span class="d-staff-badge">فريق أعطال</span><?php endif; ?>
            <time class="d-comment-date" datetime="<?php echo esc_attr(get_comment_date('c', $comment)); ?>"><?php echo esc_html(get_comment_date('j F Y', $comment)); ?></time>
          </div></header>
          <?php if ($car !== '' || $year !== ''): ?><p class="d-comment-car"><?php echo esc_html(implode(' · ', array_filter([$car, $year], function($value) { return $value !== ''; }))); ?></p><?php endif; ?>
          <?php if ($parent): ?><p class="d-comment-parent">ردًا على <?php echo esc_html(wp_strip_all_tags($parent->comment_author)); ?></p><?php endif; ?>
          <div class="d-comment-body"><?php echo nl2br(esc_html(wp_strip_all_tags($comment->comment_content))); ?></div>
          <?php if ($codes !== ''): ?><p class="d-comment-car">أكواد أخرى: <bdi><?php echo esc_html($codes); ?></bdi></p><?php endif; ?>
          <?php if ($tried !== ''): ?><div class="d-comment-tried"><strong>ما جُرّب:</strong> <?php echo nl2br(esc_html($tried)); ?></div><?php endif; ?>
          <div class="d-comment-actions"><button type="button" class="d-comment-reply" data-comment-id="<?php echo esc_attr($comment->comment_ID); ?>" data-author="<?php echo esc_attr($name); ?>">رد على المشاركة</button><button type="button" class="d-comment-report" data-comment-id="<?php echo esc_attr($comment->comment_ID); ?>">إبلاغ</button><span class="d-report-status" role="status" aria-live="polite"></span></div>
        </article>
      <?php endforeach; ?>
      </div>
      <?php if ($pages > 1): ?><nav class="d-discussion-pagination" aria-label="صفحات المناقشة">
        <?php if ($page > 1): ?><a href="<?php echo esc_url(add_query_arg('dcpage', $page-1).'#dtc-discussion'); ?>">المشاركات السابقة</a><?php endif; ?>
        <span><?php echo esc_html(number_format_i18n($page).' / '.number_format_i18n($pages)); ?></span>
        <?php if ($page < $pages): ?><a href="<?php echo esc_url(add_query_arg('dcpage', $page+1).'#dtc-discussion'); ?>">المشاركات التالية</a><?php endif; ?>
      </nav><?php endif; ?>
      <?php else: ?><div class="d-empty"><strong>ابدأ أول نقاش عن هذا الكود</strong><p>احكِ الأعراض وما جُرّب في سيارتك. التفاصيل تساعد الآخرين على فهم سؤالك.</p></div><?php endif; ?>
      <form id="d-comment-form" class="d-comment-form" method="post" data-post-id="<?php echo esc_attr($post_id); ?>" aria-describedby="dtc-form-note">
        <h3>اكتب مشاركتك</h3>
        <p id="dtc-form-note" class="d-form-note">الاسم والمشاركة مطلوبان. معلومات السيارة اختيارية. تجنب نشر رقم الهاتف أو بياناتك الخاصة.</p>
        <div class="d-reply-context" hidden>ردًا على <strong class="d-reply-name"></strong><button type="button" class="d-reply-cancel">إلغاء الرد</button></div>
        <input type="hidden" name="comment_parent" value="0">
        <div class="d-field"><label for="dtc-alias">الاسم الظاهر <span aria-hidden="true">*</span></label><input id="dtc-alias" name="alias" type="text" maxlength="60" autocomplete="nickname" required value="<?php echo esc_attr($user->exists() ? ($user->display_name ?: $user->user_login) : ''); ?>"<?php echo $user->exists() ? ' readonly' : ''; ?> placeholder="اسمك أو اسم مستعار"></div>
        <div class="d-field"><label for="dtc-comment">سؤالك أو تجربتك <span aria-hidden="true">*</span></label><textarea id="dtc-comment" name="comment" rows="5" minlength="5" maxlength="5000" required placeholder="متى ظهر الكود؟ وما الأعراض التي لاحظتها؟"></textarea></div>
        <details class="d-form-extra"><summary>أضف معلومات السيارة — اختياري</summary><div class="d-form-row">
          <div class="d-field"><label for="dtc-car">الماركة والموديل</label><input id="dtc-car" name="car" type="text" maxlength="120" placeholder="مثل: تويوتا كورولا"></div>
          <div class="d-field"><label for="dtc-year">سنة الموديل</label><input id="dtc-year" name="year" type="text" inputmode="numeric" maxlength="4" pattern="[0-9٠-٩۰-۹]{4}" placeholder="مثل: 2018"></div>
          <div class="d-field"><label for="dtc-codes">أكواد أخرى ظهرت</label><input id="dtc-codes" name="codes" type="text" maxlength="120" dir="ltr" placeholder="P0300, P0171"></div>
          <div class="d-field"><label for="dtc-tried">ما جُرّب بالفعل</label><textarea id="dtc-tried" name="tried" rows="2" maxlength="1500" placeholder="الفحوصات أو الإصلاحات التي أُجريت"></textarea></div>
        </div></details>
        <div class="d-honeypot" aria-hidden="true" hidden><label for="dtc-website">اترك هذا الحقل فارغًا</label><input id="dtc-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="d-form-footer"><button type="submit" class="d-button d-submit-comment" disabled>إرسال للمراجعة</button><small>مشاركة بدون تسجيل دخول</small></div>
        <p class="d-form-status" role="status" aria-live="polite">جارٍ تجهيز النموذج…</p>
        <noscript><p>فعّل JavaScript لاستخدام نموذج المشاركة دون حساب.</p></noscript>
      </form>
    </section>
    <?php
}

function a3g_dtc_admin_comment_columns($columns) {
    $columns['a3g_dtc_discussion'] = 'مناقشات الأكواد';
    return $columns;
}
add_filter('manage_edit-comments_columns', 'a3g_dtc_admin_comment_columns');

function a3g_dtc_admin_comment_column($column, $comment_id) {
    if ($column !== 'a3g_dtc_discussion') return;
    if (get_comment_meta($comment_id, '_a3g_dtc_discussion', true)) echo '<span>مشاركة المكتبة</span><br>';
    $count = (int)get_comment_meta($comment_id, '_a3g_dtc_report_count', true);
    if ($count) echo '<strong style="color:#b32d2e">'.esc_html(number_format_i18n($count)).' بلاغ</strong><br><a href="'.esc_url(get_edit_comment_link($comment_id)).'">مراجعة المشاركة</a>';
}
add_action('manage_comments_custom_column', 'a3g_dtc_admin_comment_column', 10, 2);

function a3g_dtc_admin_comment_box($comment) {
    if (!current_user_can('edit_comment', $comment->comment_ID)) return;
    $labels = ['car'=>'السيارة', 'year'=>'السنة', 'codes'=>'الأكواد المصاحبة', 'tried'=>'ما جُرّب', 'report_count'=>'عدد البلاغات', 'reported_at'=>'آخر بلاغ'];
    foreach ($labels as $key=>$label) {
        $value = (string)get_comment_meta($comment->comment_ID, '_a3g_dtc_'.$key, true);
        if ($value !== '') echo '<p><strong>'.esc_html($label).':</strong> '.nl2br(esc_html($value)).'</p>';
    }
    echo '<p>البلاغات طلب للمراجعة فقط ولا تُخفي المشاركة تلقائيًا. استخدم أدوات WordPress المعتادة للقبول أو الرفض.</p>';
}
add_action('add_meta_boxes_comment', function($comment) {
    if (get_comment_meta($comment->comment_ID, '_a3g_dtc_discussion', true) || get_comment_meta($comment->comment_ID, '_a3g_dtc_report_count', true)) {
        add_meta_box('a3g-dtc-discussion', 'بيانات مناقشة دليل أعطال', 'a3g_dtc_admin_comment_box', 'comment', 'normal');
    }
});
