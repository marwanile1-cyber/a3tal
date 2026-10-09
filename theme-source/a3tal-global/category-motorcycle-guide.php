<?php
/**
 * Motorcycle guide archive: dedicated editorial hub for A3tal.
 */
if (!defined('ABSPATH')) exit;
add_filter('wpseo_title', static function($title) {
  return is_category('motorcycle-guide')
    ? 'دليل الموتوسيكلات والسكوتر في مصر | الأعطال والصيانة والشراء - أعطال.كوم'
    : $title;
}, 99);
add_filter('wpseo_metadesc', static function($description) {
  return is_category('motorcycle-guide')
    ? 'دليل موتوسيكلات مصر: تشخيص المارش والبطارية وسخونة المحرك وسير السكوتر CVT، الصيانة وقطع الغيار وفحص المستعمل ومراجعات الموديلات.'
    : $description;
}, 99);
add_filter('wpseo_opengraph_image', static function($image) {
  return is_category('motorcycle-guide')
    ? 'https://a3tal.com/wp-content/uploads/2026/10/a3tal-motorcycle-category-workshop-cover.webp'
    : $image;
}, 99);
add_filter('wpseo_twitter_image', static function($image) {
  return is_category('motorcycle-guide')
    ? 'https://a3tal.com/wp-content/uploads/2026/10/a3tal-motorcycle-category-workshop-cover.webp'
    : $image;
}, 99);
get_header();
$mg_category = get_queried_object();
$mg_total = ($mg_category instanceof WP_Term) ? (int)$mg_category->count : 0;
$mg_blocks = [
  [
    'id' => 'motorcycle-diagnostics',
    'label' => 'تشخيص الأعطال',
    'title' => 'اعرف سبب العطل قبل تغيير أي قطعة',
    'copy' => 'المارش لا يعمل، المحرك يسخن، البطارية تفرغ، أو السكوتر يهتز عند الانطلاق. ابدأ من الأعراض وخطوات الفحص.',
    'items' => [
      'motorcycle-wont-start-diagnosis-egypt',
      'motorcycle-overheating-causes-diagnosis',
      'motorcycle-battery-charging-problems',
      'scooter-cvt-belt-variator-problems',
      'fuel-injection-vs-carburetor-motorcycle',
      'abs-cbs-disc-drum-motorcycle-brakes',
    ],
  ],
  [
    'id' => 'motorcycle-care',
    'label' => 'الصيانة وقطع الغيار',
    'title' => 'صيانة مناسبة للموديل وطريقة استخدامك',
    'copy' => 'الزيت والإطارات والفرامل والمكونات الاستهلاكية؛ جداول وأولويات فحص من غير تعميم أرقام على كل موتوسيكل.',
    'items' => [
      'motorcycle-maintenance-schedule-guide',
      'motorcycle-oil-guide',
      'motorcycle-tyres-guide-egypt',
      'motorcycle-genuine-vs-aftermarket-parts',
    ],
  ],
  [
    'id' => 'motorcycle-buying',
    'label' => 'الشراء والمقارنات',
    'title' => 'اختار الموتوسيكل المناسب من غير تخمين',
    'copy' => 'اختيار السعة، وفحص المستعمل، والفرق بين السكوتر والموتوسيكل، وتكلفة التشغيل في مصر.',
    'items' => [
      'used-motorcycle-buying-checklist-egypt',
      'scooter-vs-motorcycle-egypt',
      'delivery-motorcycle-buying-guide',
      'motorcycle-engine-sizes-125-150-160-200-250',
      'new-motorcycle-delivery-checklist',
    ],
  ],
  [
    'id' => 'motorcycle-reviews',
    'label' => 'مراجعات الموديلات',
    'title' => 'مراجعات عملية لموديلات موجودة في مصر',
    'copy' => 'المواصفات الموثقة ونقاط فحص المستعمل وتوفر الصيانة والقطع بدل الادعاء بتجارب قيادة لم تحدث.',
    'items' => [
      'dayun-4a-150-egypt-review',
      'hogen-3-150-egypt-review',
      'halawa-express-150-egypt-review',
      'haoji-ka150-egypt-review',
    ],
  ],
];
?>
<style>
.mg-hero{background:linear-gradient(100deg,rgba(9,24,36,.97),rgba(11,33,49,.88) 52%,rgba(11,33,49,.55)),url('https://a3tal.com/wp-content/uploads/2026/10/a3tal-motorcycle-category-workshop-cover.webp') center/cover;color:#fff;padding:54px 0 48px}
.mg-hero .g-wrap{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(230px,.7fr);align-items:center;gap:35px}
.mg-kicker{color:#b8d2dd;font-size:13px;font-weight:800;letter-spacing:1px}
.mg-hero h1{font-size:clamp(30px,4vw,52px);line-height:1.3;margin:8px 0 15px;color:#fff}
.mg-hero p{font-size:17px;color:#deebee;max-width:750px;margin:0 0 20px}
.mg-actions,.mg-jumps{display:flex;gap:10px;flex-wrap:wrap}
.mg-actions a{display:inline-block;padding:11px 18px;background:#fff;color:#132b38;border-radius:10px;font-weight:800}
.mg-actions a+ a{background:transparent;border:1px solid #92b8c6;color:#fff}
.mg-stat{border:1px solid #6b9aaa;border-radius:18px;padding:24px;background:rgba(255,255,255,.06);text-align:center}
.mg-stat strong{display:block;font-size:46px;color:#fff;line-height:1.2}
.mg-stat small{font-size:15px;color:#c0d9df}
.mg-nav{background:#fff;border-bottom:1px solid #e6ebef;padding:16px 0}
.mg-jumps a{font-size:14px;font-weight:800;border:1px solid #dbe5e9;border-radius:9px;padding:9px 15px;color:#1b4353}
.mg-main{padding-top:30px;padding-bottom:75px}
.mg-section{margin:0 0 45px;scroll-margin-top:95px}
.mg-section-head{display:flex;gap:24px;align-items:end;justify-content:space-between;margin-bottom:19px}
.mg-section-head>div{max-width:770px}
.mg-section-head small{font-weight:850;color:#2a7380}
.mg-section-head h2{font-size:clamp(21px,3vw,30px);line-height:1.45;color:#132c3b;margin:2px 0 5px}
.mg-section-head p{color:#576b77;margin:0}
.mg-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.mg-card{background:#fff;border:1px solid #e3e9ed;border-radius:16px;overflow:hidden;box-shadow:0 8px 26px rgba(12,32,48,.055)}
.mg-card-media{display:block;aspect-ratio:16/9;background:#173344;overflow:hidden}
.mg-card-media img{width:100%;height:100%;object-fit:cover}
.mg-card-body{padding:17px}
.mg-card-body h3{font-size:17px;line-height:1.55;margin:0 0 8px;color:#132a3a}
.mg-card-body h3 a:hover,.mg-read:hover{color:#16718a}
.mg-card-body p{color:#5d6975;font-size:14px;margin:0 0 12px;line-height:1.75}
.mg-read{font-size:13px;color:#126484;font-weight:850}
.mg-shelf{padding:27px 0 0;border-top:1px solid #dce5ea}
.mg-shelf .mg-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.mg-meta{font-size:12px;color:#71818b;margin-bottom:5px}
.mg-empty{background:#fff;padding:30px;border-radius:15px}
.mg-pagination{margin:30px 0;display:flex;justify-content:center}
.mg-pagination .nav-links{display:flex;gap:8px;flex-wrap:wrap}
.mg-pagination .page-numbers{padding:7px 13px;background:#fff;border:1px solid #dbe3e7;border-radius:7px}
.mg-pagination .current{background:#163f51;color:#fff}
.mg-foot{margin:36px 0 0;border-radius:15px;background:#132b39;color:#fff;padding:25px}
.mg-foot h2{margin:0 0 5px;color:#fff;font-size:23px}
.mg-foot p{margin:0 0 13px;color:#d0e0e5}
.mg-foot a{display:inline-block;background:#fff;color:#123242;border-radius:8px;padding:9px 15px;font-weight:800}
@media(max-width:900px){.mg-grid,.mg-shelf .mg-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:620px){.mg-hero{padding:34px 0}.mg-hero .g-wrap{grid-template-columns:1fr;gap:15px}.mg-stat{padding:14px}.mg-stat strong{font-size:30px}.mg-grid,.mg-shelf .mg-grid{grid-template-columns:1fr}.mg-section-head{display:block}.mg-nav{padding:12px 0}.mg-jumps a{padding:7px 11px}.mg-main{padding-top:25px}}
</style>
<section class="mg-hero">
  <div class="g-wrap">
    <div>
      <span class="mg-kicker">A3TAL MOTORCYCLE GUIDE</span>
      <h1>دليل الموتوسيكلات والسكوتر في مصر</h1>
      <p>من اختيار موديل مناسب إلى تشخيص الأعطال والصيانة، مقالات عملية مرتبطة بقاعدة مواصفات الموتوسيكلات. لكل عرض أسباب محتملة وفحوص مناسبة، من غير تغيير قطع بالتخمين.</p>
      <div class="mg-actions">
        <a href="<?php echo esc_url(home_url('/motorcycles/')); ?>">استعرض موديلات الموتوسيكلات</a>
        <a href="#motorcycle-diagnostics">ابدأ بتشخيص العطل</a>
      </div>
      <small style="display:block;margin-top:12px;font-size:11px;color:#d4e1e5">صورة خلفية القسم: <a href="https://commons.wikimedia.org/wiki/File:Motorcycle_Repair.jpg" rel="noopener noreferrer" target="_blank" style="color:inherit;text-decoration:underline">Johnnybam / Wikimedia Commons</a>، رخصة <a href="https://creativecommons.org/licenses/by-sa/4.0/" rel="noopener noreferrer" target="_blank" style="color:inherit;text-decoration:underline">CC BY-SA 4.0</a>، معالجة تحريرية بالقص والتحجيم والصورة المعدّلة بنفس الرخصة.</small>
    </div>
    <div class="mg-stat"><strong><?php echo esc_html(number_format_i18n($mg_total)); ?></strong><small>دليلًا ومراجعة في هذا القسم</small></div>
  </div>
</section>
<nav class="mg-nav" aria-label="أقسام دليل الموتوسيكلات">
  <div class="g-wrap mg-jumps">
    <?php foreach($mg_blocks as $block): ?>
    <a href="#<?php echo esc_attr($block['id']); ?>"><?php echo esc_html($block['label']); ?></a>
    <?php endforeach; ?>
    <a href="#motorcycle-all">كل المقالات</a>
  </div>
</nav>
<main class="g-wrap mg-main">
  <?php foreach($mg_blocks as $block): ?>
  <section class="mg-section" id="<?php echo esc_attr($block['id']); ?>">
    <header class="mg-section-head"><div>
      <small><?php echo esc_html($block['label']); ?></small>
      <h2><?php echo esc_html($block['title']); ?></h2>
      <p><?php echo esc_html($block['copy']); ?></p>
    </div></header>
    <div class="mg-grid">
    <?php foreach($block['items'] as $slug):
      $moto_post = get_page_by_path($slug,OBJECT,'post');
      if(!$moto_post || $moto_post->post_status!=='publish') continue;
      $moto_id = (int)$moto_post->ID;
      $moto_image = get_the_post_thumbnail_url($moto_id,'large');
    ?>
      <article class="mg-card">
        <a class="mg-card-media" href="<?php echo esc_url(get_permalink($moto_id)); ?>" aria-label="<?php echo esc_attr(get_the_title($moto_id)); ?>">
          <?php if($moto_image): ?><img src="<?php echo esc_url($moto_image); ?>" loading="lazy" decoding="async" alt="<?php echo esc_attr(get_post_meta(get_post_thumbnail_id($moto_id),'_wp_attachment_image_alt',true) ?: get_the_title($moto_id)); ?>"><?php endif; ?>
        </a>
        <div class="mg-card-body">
          <h3><a href="<?php echo esc_url(get_permalink($moto_id)); ?>"><?php echo esc_html(get_the_title($moto_id)); ?></a></h3>
          <p><?php echo esc_html(wp_trim_words(wp_strip_all_tags($moto_post->post_excerpt ?: $moto_post->post_content),21,'…')); ?></p>
          <a class="mg-read" href="<?php echo esc_url(get_permalink($moto_id)); ?>">قراءة الدليل ←</a>
        </div>
      </article>
    <?php endforeach; ?>
    </div>
  </section>
  <?php endforeach; ?>
  <section class="mg-section mg-shelf" id="motorcycle-all">
    <div class="mg-section-head"><div><small>أحدث المنشورات</small><h2>جميع أدلة ومراجعات الموتوسيكلات</h2>
      <p>الأحدث أولًا؛ انتقل للصفحة التالية لمشاهدة بقية المقالات دون ضياع الموضوعات القديمة.</p></div></div>
    <?php if(have_posts()): ?><div class="mg-grid">
    <?php while(have_posts()):the_post(); $mg_id=get_the_ID(); ?>
      <article class="mg-card">
        <a class="mg-card-media" href="<?php the_permalink(); ?>" aria-label="<?php echo esc_attr(get_the_title()); ?>">
          <?php if(has_post_thumbnail()): ?><?php the_post_thumbnail('large',['loading'=>'lazy','decoding'=>'async']); ?><?php endif; ?>
        </a>
        <div class="mg-card-body">
          <div class="mg-meta">آخر تحديث <?php echo esc_html(get_the_modified_date('j F Y')); ?></div>
          <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
          <p><?php echo esc_html(wp_trim_words(wp_strip_all_tags(get_the_excerpt()),19,'…')); ?></p>
          <a class="mg-read" href="<?php the_permalink(); ?>">افتح المقال ←</a>
        </div>
      </article>
    <?php endwhile; ?></div>
    <div class="mg-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
    <?php else: ?><div class="mg-empty">لا توجد مقالات متاحة الآن.</div><?php endif; ?>
  </section>
  <section class="mg-foot">
    <h2>تدور على موديل بعينه؟</h2>
    <p>قاعدة الموتوسيكلات تحتوي ملفات المواصفات المتاحة فعليًا، والمقالات هنا تكمل قرار الشراء والفحص والصيانة.</p>
    <a href="<?php echo esc_url(home_url('/motorcycles/')); ?>">افتح قاعدة الموتوسيكلات ←</a>
  </section>
</main>
<?php get_footer(); ?>
