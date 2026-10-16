<?php
/**
 * Price-by-trim display for existing A3tal car slugs.
 * Future records may use _a3_trim_prices_v1 JSON, but NO row is displayed
 * without a dated, URL-backed source and a numeric EGP price.
 * Legacy single /cars/{slug}/ URLs and source editorial articles are preserved.
 */
if (!defined('ABSPATH')) exit;

function a3tal_car_trim_rows($post_id) {
    $post_id = absint($post_id);
    if ($post_id < 1 || get_post_type($post_id) !== 'a3_car') return [];
    $source_url = trim((string)get_post_meta($post_id,'_a3_source_url',true));
    $checked = trim((string)get_post_meta($post_id,'_a3_source_checked_at',true));
    // Evidence must exist on the model record, not assumed from a price range.
    if (!preg_match('~^https?://~i',$source_url) || !preg_match('/^20\d\d-[01]\d-[0-3]\d$/',$checked)) return [];
    $min = (float)get_post_meta($post_id,'_a3_price_min',true);
    $max = (float)get_post_meta($post_id,'_a3_price_max',true);
    if ($min < 1) return [];
    // Only model records with a verified exact trim-price breakdown are seeded.
    // Values below mirror published A3tal car articles reviewed in October 2026.
    $reviewed = [
        83648 => ['slug'=>'skoda-octavia-2027-egypt','rows'=>[
            ['name'=>'Loft','price'=>1825000],
            ['name'=>'Lounge','price'=>2050000],
            ['name'=>'Suite','price'=>2250000],
        ]],
        83532 => ['slug'=>'mazda-3-2027-egypt','rows'=>[
            ['name'=>'Highline سيدان','price'=>1609000],
            ['name'=>'Highline هاتشباك','price'=>1619000],
        ]],
        83538 => ['slug'=>'suzuki-alto-2027-egypt','rows'=>[
            ['name'=>'مانيوال','price'=>535000],
        ]],
        83425 => ['slug'=>'jac-js2-2027-egypt','rows'=>[
            ['name'=>'Smart','price'=>775000],
        ]],
    ];
    $raw = get_post_meta($post_id,'_a3_trim_prices_v1',true);
    $rows = [];
    if (is_string($raw) && $raw !== '') {
        $data = json_decode($raw,true);
        if (json_last_error() === JSON_ERROR_NONE && is_array($data)) $rows = $data;
    } elseif (isset($reviewed[$post_id]) && get_post_field('post_name',$post_id) === $reviewed[$post_id]['slug']) {
        $rows = $reviewed[$post_id]['rows'];
    }
    if (!$rows || count($rows)>24) return [];
    $clean = [];
    foreach ($rows as $row) {
        if (!is_array($row)) return [];
        $name = sanitize_text_field($row['name'] ?? '');
        $price = $row['price'] ?? null;
        if ($name === '' || strlen($name)>140 || !is_numeric($price)) return [];
        $price = (float)$price;
        if ($price < 1000 || $price > 100000000 || ($max > 0 && $price > $max) || $price < $min) return [];
        $clean[] = ['name'=>$name,'price'=>$price,
            'detail'=>isset($row['detail']) ? sanitize_text_field($row['detail']) : ''];
    }
    return $clean;
}

function a3tal_car_render_trims($post_id) {
    $rows = a3tal_car_trim_rows($post_id);
    if (!$rows) return;
    $source = esc_url(get_post_meta($post_id,'_a3_source_url',true));
    $checked = esc_html(get_post_meta($post_id,'_a3_source_checked_at',true));
    $currency = strtoupper(trim((string)get_post_meta($post_id,'_a3_currency',true)));
    if ($currency !== 'EGP') return;
    ?>
    <section id="trims" class="g-vehicle-panel cg-trim-panel" aria-labelledby="cg-trim-heading">
        <div class="g-section-head">
            <div><span>VERIFIED MODEL PRICES</span><h2 id="cg-trim-heading">أسعار فئات <?php echo esc_html(get_the_title($post_id)); ?></h2></div>
        </div>
        <p class="cg-trim-lead">أسعار الفئات المعلنة في السوق المصري كما وردت في البيانات المنشورة، وليست عروض أسعار ملزمة. تحقق من الوكيل يوم الحجز.</p>
        <div class="cg-trim-scroller" role="region" aria-label="جدول أسعار فئات السيارة" tabindex="0">
            <table class="cg-trim-table">
                <thead><tr><th scope="col">الفئة</th><th scope="col">السعر المعلن</th><th scope="col">معلومات إضافية</th></tr></thead>
                <tbody>
                <?php foreach($rows as $row): ?>
                <tr><th scope="row"><?php echo esc_html($row['name']); ?></th>
                    <td class="cg-trim-price" dir="auto"><?php echo esc_html(number_format_i18n($row['price'],0)); ?> جنيه</td>
                    <td><?php echo esc_html($row['detail'] ?: 'راجع تجهيزات الفئة مع الوكيل'); ?></td>
                </tr>
                <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <p class="cg-trim-proof">آخر مراجعة مسجلة: <time datetime="<?php echo esc_attr($checked); ?>"><?php echo $checked; ?></time>
            <?php if($source): ?> · <a href="<?php echo $source; ?>" rel="nofollow noopener noreferrer" target="_blank">مصدر بيانات السيارة <span class="screen-reader-text">(يفتح نافذة جديدة)</span></a><?php endif; ?>
        </p>
    </section>
    <?php
}
