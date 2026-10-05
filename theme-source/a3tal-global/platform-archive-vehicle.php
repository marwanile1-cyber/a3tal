<?php
if (!defined('ABSPATH')) exit;
$type=$a3g_vehicle_type??get_query_var('post_type');
$is_moto=$type==='a3_motorcycle';
$title=$is_moto?'الموتوسيكلات والسكوتر':'السيارات';
$subtitle=$is_moto?'أسعار ومواصفات ومراجعات وصيانة الموتوسيكلات والسكوتر في مكان واحد.':'اكتشف السيارات حسب الماركة والسوق والسنة ونوع الهيكل، مع الأسعار والمواصفات والمحتوى المرتبط.';
$type_tax=$is_moto?'a3_motorcycle_type':'a3_car_body';
$vehicle_ids=get_posts([
  'post_type'=>$type,
  'post_status'=>'publish',
  'posts_per_page'=>-1,
  'fields'=>'ids',
  'no_found_rows'=>true,
]);
$brands=$vehicle_ids?get_terms(['taxonomy'=>'a3_brand','hide_empty'=>true,'object_ids'=>$vehicle_ids]):[];
$markets=$vehicle_ids?get_terms(['taxonomy'=>'a3_market','hide_empty'=>true,'object_ids'=>$vehicle_ids]):[];
$types=$vehicle_ids?get_terms(['taxonomy'=>$type_tax,'hide_empty'=>true,'object_ids'=>$vehicle_ids]):[];
$year_raw=absint(get_query_var('year'));
$year_value=($year_raw>=1950&&$year_raw<=2100)?(string)$year_raw:'';
?>
<?php get_header(); ?>
<section class="g-platform-archive-hero">
  <div class="g-wrap">
    <span><?php echo $is_moto?'A3TAL MOTORCYCLES':'A3TAL CARS'; ?></span>
    <h1><?php echo esc_html($title); ?></h1>
    <p><?php echo esc_html($subtitle); ?></p>
    <form class="g-platform-filter" method="get">
      <label><small>الماركة</small><select name="brand"><option value="">كل الماركات</option><?php foreach($brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('brand'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small>السوق</small><select name="market"><option value="">كل الأسواق</option><?php foreach($markets as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('market'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small><?php echo $is_moto?'النوع':'نوع الهيكل'; ?></small><select name="vehicle_type"><option value="">كل الأنواع</option><?php foreach($types as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected(get_query_var('vehicle_type'),$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?></select></label>
      <label><small>سنة الموديل</small><input type="number" min="1950" max="2100" name="year" value="<?php echo esc_attr($year_value); ?>" placeholder="مثال: 2026"></label>
      <button type="submit"><?php echo a3g_icon('search'); ?><span>فلترة</span></button>
    </form>
  </div>
</section>

<main class="g-wrap g-platform-archive">
  <div class="g-platform-archive-head">
    <div><span>قاعدة بيانات أعطال</span><h2><?php echo $is_moto?'اختر الموتوسيكل المناسب':'اختر السيارة المناسبة'; ?></h2></div>
    <b><?php global $wp_query; $a3g_vehicle_count=(int)$wp_query->found_posts; echo esc_html((!$is_moto && $a3g_vehicle_count===0)?'أسعار ومراجعات متاحة':number_format_i18n($a3g_vehicle_count).' نتيجة'); ?></b>
  </div>

  <?php if(have_posts()): ?>
    <div class="g-platform-grid">
      <?php while(have_posts()):the_post();a3g_platform_card();endwhile; ?>
    </div>
    <div class="g-platform-pagination"><?php the_posts_pagination(['mid_size'=>2,'prev_text'=>'السابق','next_text'=>'التالي']); ?></div>
  <?php elseif($is_moto): ?>
    <div class="g-platform-empty">
      <?php echo a3g_icon('motorcycle'); ?>
      <h2>لا توجد نتائج منشورة بهذه الفلاتر حاليًا</h2>
      <p>غيّر الفلاتر أو ارجع للقائمة الكاملة للموتوسيكلات المنشورة.</p>
      <a href="<?php echo esc_url(get_post_type_archive_link($type)); ?>">مسح الفلاتر</a>
    </div>
  <?php else: ?>
    <div class="g-platform-bridge-note">
      <?php echo a3g_icon('car'); ?>
      <div><h2>ابدأ من الأسعار والمراجعات المتاحة الآن</h2><p>تصفح أحدث أسعار السيارات والمراجعات والمقارنات المنشورة على أعطال، ثم استخدم ملفات الموديلات المنظمة فور إضافتها إلى قاعدة السيارات.</p><div class="g-platform-bridge-actions"><a href="<?php echo esc_url(a3g_cat_link(374)); ?>">أسعار السيارات</a><a href="<?php echo esc_url(a3g_cat_link(22)); ?>">مراجعات السيارات</a></div></div>
    </div>
  <?php endif; ?>

  <?php if($is_moto): ?>
    <?php
      $brand_guide=get_page_by_path('motorcycle-brands-egypt-complete-guide',OBJECT,'post');
      $brand_guide_url=$brand_guide?get_permalink($brand_guide):get_post_type_archive_link('a3_motorcycle');
      $moto_groups=[
        'ياباني'=>[
          ['Honda','honda'],['Yamaha','yamaha'],['Suzuki','suzuki'],['Kawasaki','kawasaki']
        ],
        'هندي'=>[
          ['TVS','tvs'],['Bajaj','bajaj'],['Hero','hero'],['Royal Enfield','royal-enfield']
        ],
        'صيني حديث'=>[
          ['CFMOTO','cfmoto'],['QJMotor','qjmotor'],['Zontes','zontes'],['Voge','voge']
        ],
        'صيني اقتصادي وصناعي'=>[
          ['Lifan','lifan'],['Loncin','loncin'],['Haojue','haojue'],['Dayun','dayun']
        ],
        'تايواني وسكوتر'=>[
          ['SYM','sym'],['Kymco','kymco']
        ],
        'أوروبي وأمريكي'=>[
          ['BMW Motorrad','bmw-motorrad'],['Ducati','ducati'],['Triumph','triumph'],['KTM','ktm'],
          ['Aprilia','aprilia'],['Piaggio','piaggio'],['Vespa','vespa'],['Peugeot Motocycles','peugeot-motocycles'],['Harley-Davidson','harley-davidson']
        ],
        'علامات متعددة المنشأ'=>[
          ['Benelli','benelli'],['Keeway','keeway']
        ],
      ];
      $live_brand_slugs=[];
      $live_ids=get_posts(['post_type'=>'a3_motorcycle','post_status'=>'publish','posts_per_page'=>-1,'fields'=>'ids']);
      foreach($live_ids as $mid){
        $terms=get_the_terms($mid,'a3_brand');
        if($terms&&!is_wp_error($terms)) foreach($terms as $term)$live_brand_slugs[$term->slug]=true;
      }
    ?>
    <section class="g-moto-brand-universe">
      <div class="g-section-head">
        <div>
          <span>MOTORCYCLE BRANDS</span>
          <h2>الماركات اللي هنغطيها في أعطال</h2>
          <p>من الياباني والهندي لحد الصيني الحديث والاقتصادي. الموديلات المنشورة فعليًا تفتح فلتر الماركة، والباقي داخل دليل الماركات لحد ما بيانات الموديلات المصرية تتوثق.</p>
        </div>
        <a href="<?php echo esc_url($brand_guide_url); ?>">دليل الماركات الكامل</a>
      </div>
      <div class="g-moto-origin-groups">
        <?php foreach($moto_groups as $origin=>$items): ?>
          <div class="g-moto-origin-group">
            <h3><?php echo esc_html($origin); ?></h3>
            <div class="g-moto-brand-chips">
              <?php foreach($items as [$name,$slug]):
                $url=!empty($live_brand_slugs[$slug])
                  ? add_query_arg('brand',$slug,get_post_type_archive_link('a3_motorcycle'))
                  : $brand_guide_url;
              ?>
                <a class="<?php echo !empty($live_brand_slugs[$slug])?'is-live':''; ?>" href="<?php echo esc_url($url); ?>">
                  <b><?php echo esc_html($name); ?></b>
                  <small><?php echo !empty($live_brand_slugs[$slug])?'موديلات منشورة':'ضمن الدليل'; ?></small>
                </a>
              <?php endforeach; ?>
            </div>
          </div>
        <?php endforeach; ?>
      </div>
    </section>

    <?php
      $moto_cat=get_category_by_slug('motorcycle-guide');
      if($moto_cat):
        $moto_guides=a3g_query(['cat'=>(int)$moto_cat->term_id,'posts_per_page'=>12]);
        if($moto_guides->have_posts()):
    ?>
      <section class="g-moto-guide-zone">
        <div class="g-section-head">
          <div>
            <span>A3TAL MOTO GUIDE</span>
            <h2>شراء وصيانة وقطع غيار وأعطال الموتوسيكلات</h2>
            <p>المحتوى هنا مبني على قرار المستخدم الحقيقي: يشتري إيه، يراجع إيه، يصين إزاي، ويعرف الفرق بين التقنية والمواصفات بدل كلام القهاوي المقدس.</p>
          </div>
          <a href="<?php echo esc_url(get_category_link($moto_cat)); ?>">كل دليل الموتوسيكلات</a>
        </div>
        <div class="g-showroom-guide-grid g-moto-guide-grid">
          <?php while($moto_guides->have_posts()):$moto_guides->the_post();a3g_card(get_the_ID(),'g-showroom-guide-card g-moto-guide-card');endwhile;wp_reset_postdata(); ?>
        </div>
      </section>
    <?php endif;endif; ?>

  <?php else: ?>
    <?php a3g_legacy_section([374],'أسعار السيارات الجديدة','أحدث أسعار السيارات المنشورة على أعطال، مرتبة للوصول السريع إلى السعر والمواصفات والتفاصيل.',8,[],374); ?>
    <?php a3g_legacy_section([22],'مراجعات السيارات','مراجعات وتجارب الشراء الموجودة بالفعل، من غير إنشاء نسخ جديدة لنفس النية.',6,[],22); ?>
    <?php a3g_legacy_section([21],'مقارنات بين السيارات','مقارنات عملية تساعدك على مراجعة الفروق في المواصفات والتجهيزات قبل الشراء.',6,[],21); ?>
  <?php endif; ?>
</main>
<?php get_footer(); ?>
