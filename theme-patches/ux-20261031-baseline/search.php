<?php
/**
 * Search journeys for the whole A3tal automotive ecosystem.
 * The standard WordPress search query and URLs are preserved.
 */
if (!defined('ABSPATH')) exit;
$si_query = trim((string)get_search_query(false));
$si_code = preg_match('/^[PBCU][0-9][0-9A-F]{3}$/iD', $si_query) ? strtoupper($si_query) : '';
$si_normalize = static function($value) {
    $text = wp_strip_all_tags((string)$value);
    $text = function_exists('mb_strtolower') ? mb_strtolower($text, 'UTF-8') : strtolower($text);
    $text = strtr($text, ['أ'=>'ا','إ'=>'ا','آ'=>'ا','ى'=>'ي','ة'=>'ه']);
    $text = preg_replace('/[\x{064B}-\x{065F}\x{0670}]/u','',$text);
    $text = preg_replace('/[^\p{L}\p{N}]+/u',' ',$text);
    return trim(preg_replace('/\s+/u',' ',$text));
};
$si_phrase = $si_normalize($si_query);
$si_tokens = array_values(array_filter(explode(' ', $si_phrase), static function($word){
    return (function_exists('mb_strlen') ? mb_strlen($word,'UTF-8') : strlen($word)) > 1;
}));
$si_intent = 'general';
if ($si_code) $si_intent = 'code';
elseif (preg_match('/(موتوسيكل|سكوتر|دراجه ناريه|motorcycle|scooter|bajaj|tvs)/iu',$si_query)) $si_intent='motorcycle';
elseif (preg_match('/(رعش|اهتزاز|عطل|اعطال|طقطق|صوت|تسريب|سخون|فرامل|دركسيون|فتيس|مشكله|مشاكل|موتور|حساس|لمبه|لمبة|ABS)/iu',$si_query)) $si_intent='diagnosis';
elseif (preg_match('/(قطع غيار|بطاريه|بطارية|فلتر زيت|فلتر هواء|بوجيه|تيل فرامل)/iu',$si_query)) $si_intent='parts';
elseif (preg_match('/(صيانه|صيانة|زيت|تغيير زيت|جدول صيانة|maintenance)/iu',$si_query)) $si_intent='maintenance';
elseif (preg_match('/(توكيل|مركز خدمه|مركز خدمة|معرض|وكيل|حجز صيانه)/iu',$si_query)) $si_intent='service';
elseif (preg_match('/(سعر|اسعار|أسعار|مواصفات|مراجعه|مراجعة|مقارن|اشتري|شراء|زيرو|فئات|تقسيط|price)/iu',$si_query)) $si_intent='purchase';

// Rank just the current page of the existing WordPress query.
// Never change canonical URLs, WordPress relevance matching, or indexed articles.
$si_rows=[];
$si_position=0;
while (have_posts()) {
    the_post();
    $id=(int)get_the_ID();
    $title=$si_normalize(get_the_title($id));
    $type=get_post_type($id);
    $score=0;
    if ($si_phrase !== '' && $title === $si_phrase) $score+=500;
    elseif ($si_phrase !== '' && strpos($title,$si_phrase)!==false) $score+=210;
    $hits=0;
    foreach ($si_tokens as $word) {
        if (strpos($title,$word)!==false) { $score+=36; $hits++; }
    }
    if ($si_tokens && $hits===count($si_tokens)) $score+=90;
    if ($si_code && $type==='a3_dtc') {
        $dtc_meta=strtoupper((string)get_post_meta($id,'_a3_dtc_code',true));
        if ($dtc_meta===$si_code || preg_match('/\b'.preg_quote($si_code,'/').'\b/i',get_the_title($id))) $score+=750;
    }
    if ($si_intent==='motorcycle' && $type==='a3_motorcycle') $score+=40;
    if ($si_intent==='purchase' && $type==='a3_car') $score+=30;
    if ($si_intent==='maintenance' && $type==='a3_maintenance_plan') $score+=45;
    if ($si_intent==='service' && in_array($type,['a3_service_center','a3_showroom'],true)) $score+=45;
    if ($si_intent==='parts' && in_array($type,['a3_part','a3_parts_vendor'],true)) $score+=45;
    if ($si_intent==='diagnosis' && $type==='a3_dtc') $score+=15;
    // Very weak matches stay available under More results, never presented as an exact answer.
    $si_rows[]=['id'=>$id,'score'=>$score,'order'=>$si_position++];
}
wp_reset_postdata();
if ($si_intent==='general') {
    foreach ($si_rows as $row) {
        if (get_post_type($row['id'])==='a3_car') { $si_intent='purchase'; break; }
    }
}
usort($si_rows,static function($a,$b){return ($b['score']<=>$a['score']) ?: ($a['order']<=>$b['order']);});
$si_primary=array_slice($si_rows,0,3);
$si_more=array_slice($si_rows,3);
$si_title = [
  'code'=>'ابدأ بالكود المطابق',
  'diagnosis'=>'ابدأ بتشخيص المشكلة',
  'purchase'=>'ابدأ بالموديل أو دليل الشراء',
  'maintenance'=>'ابدأ بخطوات الصيانة',
  'parts'=>'ابدأ بفحص القطعة أو دليلها',
  'service'=>'ابدأ بمركز الخدمة أو الوكيل',
  'motorcycle'=>'ابدأ بدليل الموتوسيكل المناسب',
  'general'=>'النتائج الأقرب لبحثك',
][$si_intent];
$si_next = [
  'code'=>[
    ['title'=>'ابحث داخل مكتبة أكواد DTC','desc'=>'شروح وفحوصات أكواد P وB وC وU','url'=>get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/')],
    ['title'=>'تشخيص العطل من الأعراض','desc'=>'لو معندكش جهاز فحص','url'=>a3g_cat_link(8)],
  ],
  'diagnosis'=>[
    ['title'=>'دليل الأعطال والتشخيص','desc'=>'الفحص من العَرَض قبل تغيير القطع','url'=>a3g_cat_link(8)],
    ['title'=>'مكتبة أكواد الأعطال','desc'=>'لو جهاز الكشف طلع كود','url'=>get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/')],
  ],
  'purchase'=>[
    ['title'=>'دليل موديلات السيارات','desc'=>'أسعار وفئات ومواصفات منظمة','url'=>get_post_type_archive_link('a3_car') ?: home_url('/cars/')],
    ['title'=>'مقارنات السيارات','desc'=>'احسم قرار الشراء بالمقارنة','url'=>a3g_cat_link(21)],
  ],
  'maintenance'=>[
    ['title'=>'جداول الصيانة','desc'=>'المواعيد والمتطلبات حسب البيانات المنشورة','url'=>get_post_type_archive_link('a3_maintenance_plan') ?: home_url('/maintenance-schedules/')],
    ['title'=>'الزيوت والصيانة','desc'=>'شروحات عملية قبل إجراء الصيانة','url'=>a3g_cat_link(3)],
  ],
  'parts'=>[
    ['title'=>'دليل قطع الغيار','desc'=>'افهم وظيفة القطعة وتوافقها','url'=>get_post_type_archive_link('a3_part') ?: home_url('/parts/')],
    ['title'=>'أعراض الأعطال','desc'=>'تأكد من المشكلة قبل شراء القطعة','url'=>a3g_cat_link(8)],
  ],
  'service'=>[
    ['title'=>'مراكز الخدمة','desc'=>'استكشف المراكز المنشورة والبيانات المتاحة','url'=>get_post_type_archive_link('a3_service_center') ?: home_url('/service-centers/')],
    ['title'=>'المعارض والوكلاء','desc'=>'بيانات الفروع والتواصل المنشورة','url'=>get_post_type_archive_link('a3_showroom') ?: home_url('/car-showrooms/')],
  ],
  'motorcycle'=>[
    ['title'=>'دليل الموتوسيكلات','desc'=>'الموديلات والمواصفات والأسعار','url'=>get_post_type_archive_link('a3_motorcycle') ?: home_url('/motorcycles/')],
    ['title'=>'دليل أعطال الموتوسيكل','desc'=>'الصيانة والأعطال الخاصة بالدراجات','url'=>home_url('/category/motorcycle-guide/')],
  ],
  'general'=>[
    ['title'=>'السيارات وأسعارها','desc'=>'تصفح الموديلات والبيانات','url'=>get_post_type_archive_link('a3_car') ?: home_url('/cars/')],
    ['title'=>'مكتبة الأكواد','desc'=>'تشخيص من الكود أو العَرَض','url'=>get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/')],
  ],
][$si_intent];
$si_css=get_template_directory().'/search-intent.css';
if(is_file($si_css)) wp_enqueue_style('a3tal-search-intent',get_template_directory_uri().'/search-intent.css',['a3g-style'],(string)filemtime($si_css));
get_header(); ?>
<header class="si-hero">
  <div class="g-wrap">
    <span class="si-eyebrow">A3TAL · SMART DISCOVERY</span>
    <h1>نتائج البحث عن: <?php echo esc_html($si_query); ?></h1>
    <p>النتائج الأقرب أولًا، وبعدها المسار المناسب للبحث في الأسعار أو الأعطال أو الصيانة. لا نعتبر مجرد تشابه الكلمات دليلًا على توافق قطعة أو عطل مع موديل.</p>
    <form class="si-search-form" role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
      <label for="si-phrase">عدّل بحثك</label>
      <input id="si-phrase" type="search" name="s" value="<?php echo esc_attr($si_query); ?>" placeholder="موديل، كود P0139، عَرَض عطل، قطعة غيار" required>
      <button type="submit">بحث</button>
    </form>
  </div>
</header>
<main class="g-wrap si-layout" id="si-results">
  <?php if ($si_primary): ?>
    <section class="si-results" aria-labelledby="si-primary-title">
      <div class="si-heading"><span>أول خطوة</span><h2 id="si-primary-title"><?php echo esc_html($si_title); ?></h2><p>الترتيب حسب مدى تطابق العنوان ونوع المعلومة مع بحثك، وليس حسب عدد المشاهدات.</p></div>
      <div class="g-archive-grid si-primary-grid">
        <?php foreach($si_primary as $entry) a3g_card($entry['id']); ?>
      </div>
    </section>
  <?php else: ?>
    <section class="si-empty"><h2>مفيش نتيجة مباشرة للبحث ده</h2><p>جرّب اسم الموديل من غير سنة أو اكتب كود العطل كما ظهر في جهاز الفحص. وتقدر تبدأ من الأقسام التالية.</p></section>
  <?php endif; ?>
  <section class="si-next" aria-labelledby="si-next-title">
    <div class="si-heading"><span>استكمل بحثك</span><h2 id="si-next-title">المسار التالي المناسب</h2><p>دي أبواب مرتبطة بنوع بحثك، مش ادعاء إن المقالات أو الأكواد تخص موديلًا معينًا.</p></div>
    <div class="si-next-grid">
      <?php foreach($si_next as $route): ?>
        <a class="si-next-link" href="<?php echo esc_url($route['url']); ?>"><strong><?php echo esc_html($route['title']); ?></strong><small><?php echo esc_html($route['desc']); ?></small><span aria-hidden="true">←</span></a>
      <?php endforeach; ?>
    </div>
  </section>
  <?php if ($si_more): ?>
    <section class="si-results si-other" aria-labelledby="si-other-title">
      <div class="si-heading"><span>قراءات إضافية</span><h2 id="si-other-title">نتائج أخرى قد تساعدك</h2><p>العناوين دي أقل تطابقًا مع بحثك، فراجع موضوع المقال قبل فتحه.</p></div>
      <div class="g-archive-grid si-secondary-grid">
        <?php foreach($si_more as $entry) a3g_card($entry['id']); ?>
      </div>
    </section>
  <?php endif; ?>
  <?php if ($GLOBALS['wp_query']->max_num_pages > 1): ?>
    <nav class="si-pagination" aria-label="صفحات نتائج البحث"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'النتائج السابقة','next_text'=>'النتائج التالية']); ?></nav>
  <?php endif; ?>
</main>
<?php get_footer(); ?>
