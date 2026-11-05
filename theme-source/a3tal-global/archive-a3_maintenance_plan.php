<?php
// Load the reviewed lightweight assets only on this archive. Some hosts strip
// late template enqueues; print the audited, static file contents in head/footer
// so users actually receive the calculator after the data-driven HTML has loaded.
add_action('wp_head',static function(){
  $path=get_template_directory().'/maintenance-calculator-20261106.css';
  if(is_readable($path)){echo '<style id="a3ms-inline-style">';readfile($path);echo '</style>';}
},40);
add_action('wp_footer',static function(){
  $path=get_template_directory().'/assets/js/maintenance-calculator-20261106.js';
  if(is_readable($path)){echo '<script id="a3ms-inline-script">';readfile($path);echo '</script>';}
},40);
get_header();
$selected=absint(get_query_var('vehicle_entity'));
$plan_ids=get_posts([
  'post_type'=>'a3_maintenance_plan',
  'post_status'=>'publish',
  'numberposts'=>-1,
  'fields'=>'ids',
  'no_found_rows'=>true,
]);
$ready_vehicle_ids=[];
foreach($plan_ids as $plan_id){
  $entity_id=(int)get_post_meta($plan_id,'_a3_vehicle_entity_id',true);
  if($entity_id>0)$ready_vehicle_ids[$entity_id]=$entity_id;
}
$ready_vehicle_ids=array_values($ready_vehicle_ids);
$vehicles=$ready_vehicle_ids?get_posts([
  'post_type'=>['a3_car','a3_motorcycle'],
  'post_status'=>'publish',
  'numberposts'=>300,
  'post__in'=>$ready_vehicle_ids,
  'orderby'=>'title',
  'order'=>'ASC',
]):[];
$selected_post=($selected && in_array($selected,$ready_vehicle_ids,true)) ? get_post($selected) : null;
// Only a published vehicle with an actual maintenance record can be named here.
if($selected_post && !in_array(get_post_type($selected_post),['a3_car','a3_motorcycle'],true)) $selected_post=null;
?>
<section class="g-maintenance-hero"><div class="g-wrap g-maintenance-hero-grid">
  <div>
    <span>A3TAL MAINTENANCE</span>
    <h1>جدول صيانة يفهم عربيتك، مش جدول محفوظ</h1>
    <p>اختر مركبة لها بنود صيانة موثقة، وأدخل عدادك وتاريخ آخر خدمة لحساب الاستحقاق لكل بند. لن نعرض مواعيد افتراضية للموديلات بلا جدول معتمد.</p>
    <form method="get" class="g-maintenance-select">
      <label><small>اختر المركبة</small><select name="vehicle_entity" required><option value=""><?php echo $vehicles?'اختر السيارة أو الموتوسيكل':'لا توجد جداول مركبات منظمة بعد'; ?></option><?php foreach($vehicles as $v): ?><option value="<?php echo esc_attr($v->ID); ?>" <?php selected($selected,$v->ID); ?>><?php echo esc_html($v->post_title); ?></option><?php endforeach; ?></select></label>
      <button type="submit">عرض جدول الصيانة</button>
    </form>
  </div>
  <div class="g-maintenance-demo">
    <div class="a3ms-available-count" role="note"><strong><?php echo esc_html(number_format_i18n(count($vehicles))); ?> مركبة ببيانات منظمة</strong><span>المواعيد الحقيقية تظهر فقط بعد اختيار مركبة متاحة وإدخال بيانات العداد وسجل الخدمة. باقي مقالات الصيانة متاحة أسفل الصفحة.</span></div>
  </div>
</div></section>

<main class="g-wrap g-maintenance-main">
<?php if(!$selected): ?>
  <section class="g-maintenance-intro">
    <div><span>01</span><h2>اختر المركبة</h2><p>الموديل والمحرك هما الأساس، مش مجرد سنة الصنع.</p></div>
    <div><span>02</span><h2>أدخل العداد ونمط الاستخدام</h2><p>يُحسب كل بند من الفترة الخاصة بالمركبة، دون نقل أرقام موديل آخر.</p></div>
    <div><span>03</span><h2>حدّث سجل آخر صيانة</h2><p>تاريخ وعداد آخر خدمة لكل بند ضروريان لتأكيد المتأخر والمستحق.</p></div>
    <div><span>04</span><h2>تابع داخل «سيارتي»</h2><p>حفظ العداد وسجل الخدمة يتم داخل الجراج بعد تسجيل الدخول.</p></div>
  </section>
  <section class="g-maintenance-cta"><div><span>MY A3TAL GARAGE</span><h2>عايز الجدول يتحدث مع عداد عربيتك؟</h2><p>أضف مركبتك للجراج، وسجل الصيانة كل مرة بدل ما تحفظ المواعيد في دماغك، وهي أصلًا مش ناقصة.</p></div><a href="<?php echo esc_url(home_url('/my-garage/')); ?>">افتح سيارتي</a></section>
<?php else:
  $items=[];
  if(have_posts()){
    while(have_posts()){the_post();
      $terms=get_the_terms(get_the_ID(),'a3_maintenance_kind');$kind=($terms&&!is_wp_error($terms))?$terms[0]->name:'صيانة';
      $items[]=[
        'id'=>get_the_ID(),'title'=>get_the_title(),'kind'=>$kind,
        'first_km'=>(int)get_post_meta(get_the_ID(),'_a3_first_due_km',true),
        'interval_km'=>(int)get_post_meta(get_the_ID(),'_a3_interval_km',true),
        'first_months'=>(int)get_post_meta(get_the_ID(),'_a3_first_due_months',true),
        'interval_months'=>(int)get_post_meta(get_the_ID(),'_a3_interval_months',true),
        'severe_km'=>(int)get_post_meta(get_the_ID(),'_a3_severe_interval_km',true),
        'severe_months'=>(int)get_post_meta(get_the_ID(),'_a3_severe_interval_months',true),
        'action'=>(string)get_post_meta(get_the_ID(),'_a3_service_action',true),
        'fluid'=>(string)get_post_meta(get_the_ID(),'_a3_fluid_spec',true),
        'qty'=>(string)get_post_meta(get_the_ID(),'_a3_fluid_quantity',true),
        'parts'=>(string)get_post_meta(get_the_ID(),'_a3_part_numbers',true),
        'minutes'=>(int)get_post_meta(get_the_ID(),'_a3_estimated_minutes',true),
        'checked'=>(string)get_post_meta(get_the_ID(),'_a3_source_checked_at',true),
        'source'=>(string)get_post_meta(get_the_ID(),'_a3_source_url',true),
      ];
    }
    usort($items,static fn($a,$b)=>($a['first_km']?:$a['interval_km'])<=>($b['first_km']?:$b['interval_km']));
  }
?>
  <section class="g-maintenance-selected">
    <div><?php if($selected_post&&has_post_thumbnail($selected)): echo get_the_post_thumbnail($selected,'medium_large'); else: ?><span class="g-fallback">A3TAL</span><?php endif; ?></div>
    <div><span>جدول الصيانة الموثق</span><h2><?php echo esc_html($selected_post?$selected_post->post_title:'المركبة'); ?></h2><p>الفترات أدناه للموديل المختار فقط. الحساب استرشادي؛ تاريخ آخر صيانة لكل بند يحدد ما إذا كانت الخدمة قد نُفذت بالفعل.</p></div>
    <a href="<?php echo esc_url(home_url('/my-garage/')); ?>">أضفها إلى سيارتي</a>
  </section>

  <?php if($items): ?>
  <section class="a3ms-card" aria-labelledby="a3ms-title">
    <h2 id="a3ms-title">احسب الصيانة القادمة من عدادك</h2>
    <p>اكتب قراءة العداد الحالية، ثم آخر مرة نفذت كل بند أدناه إن كنت تعرفها. البنود التي لا نعرف تاريخ تنفيذها ستظهر «تحتاج مراجعة السجل»، بدل حساب موعد مؤكد من التخمين.</p>
    <form id="a3ms-calculator">
      <div class="a3ms-fields">
        <label for="a3ms-current-km">عداد المركبة الحالي (كم)<input id="a3ms-current-km" type="number" min="0" max="3000000" step="1" inputmode="numeric" placeholder="مثال: 57000" required></label>
        <label for="a3ms-usage">طبيعة الاستخدام<select id="a3ms-usage"><option value="normal">عادي</option><option value="severe">شاق (عندما يذكر المصدر فترة خاصة)</option></select></label>
        <label for="a3ms-delivery-date">تاريخ بداية الاستخدام (اختياري)<input id="a3ms-delivery-date" type="date" max="<?php echo esc_attr(wp_date('Y-m-d')); ?>"></label>
      </div>
      <button id="a3ms-calc-button" type="submit">احسب الاستحقاقات</button>
      <p class="a3ms-note">تاريخ بداية الاستخدام يُستخدم للخدمة الأولى فقط عند توافر فترة بالشهور. وللصيانة المتكررة يُفضّل إدخال تاريخ آخر تنفيذ للبند نفسه. لا تُخزن هذه المدخلات على الخادم.</p>
      <div class="a3ms-alert" id="a3ms-notice" role="status" aria-live="polite">بعد الحساب تظهر نتائج مستقلة لكل بند، من بيانات الشركة المنشورة فقط.</div>
      <div id="a3ms-summary" aria-live="polite" hidden></div>
    </form>
    <p>لتقدير فاتورة القطع والمصنعية باستخدام أسعار الورشة الفعلية: <a href="<?php echo esc_url(home_url('/car-tools/#maintenance-cost')); ?>">افتح حاسبة تكلفة الصيانة</a>. ولحفظ العداد وسجل الإصلاحات: <a href="<?php echo esc_url(home_url('/my-garage/')); ?>">افتح «سيارتي»</a>.</p>
  </section>
  <section class="g-maintenance-timeline">
    <div class="g-maintenance-rail"></div>
    <?php foreach($items as $index=>$it): $km=$it['first_km']?:$it['interval_km']; ?>
      <article class="g-maintenance-node a3ms-item" data-verified="<?php echo esc_attr(($it['source'] && $it['checked']) ? '1' : '0'); ?>" data-first-km="<?php echo esc_attr($it['first_km']); ?>" data-interval-km="<?php echo esc_attr($it['interval_km']); ?>" data-first-months="<?php echo esc_attr($it['first_months']); ?>" data-interval-months="<?php echo esc_attr($it['interval_months']); ?>" data-severe-km="<?php echo esc_attr($it['severe_km']); ?>" data-severe-months="<?php echo esc_attr($it['severe_months']); ?>">
        <div class="g-maintenance-node-point"><b><?php echo $km?esc_html(number_format_i18n($km/1000,0).'K'):'⏱'; ?></b></div>
        <div class="g-maintenance-node-card">
          <div class="g-maintenance-node-top"><span><?php echo esc_html($it['kind']); ?></span><?php if($it['action']): ?><b><?php echo esc_html($it['action']); ?></b><?php endif; ?></div>
          <h3><?php echo esc_html($it['title']); ?></h3>
          <div class="g-maintenance-node-facts">
            <?php if($it['interval_km']): ?><span><small>كل</small><b><?php echo esc_html(number_format_i18n($it['interval_km']).' كم'); ?></b></span><?php endif; ?>
            <?php if($it['interval_months']): ?><span><small>أو كل</small><b><?php echo esc_html($it['interval_months'].' شهر'); ?></b></span><?php endif; ?>
            <?php if($it['severe_km']): ?><span class="is-severe"><small>استخدام شاق</small><b><?php echo esc_html(number_format_i18n($it['severe_km']).' كم'); ?></b></span><?php endif; ?>
            <?php if($it['minutes']): ?><span><small>وقت تقريبي</small><b><?php echo esc_html($it['minutes'].' دقيقة'); ?></b></span><?php endif; ?>
          </div>
          <?php if($it['fluid']||$it['qty']||$it['parts']): ?><div class="g-maintenance-tech"><?php if($it['fluid']): ?><span><small>المواصفة</small><?php echo esc_html($it['fluid']); ?></span><?php endif; ?><?php if($it['qty']): ?><span><small>الكمية</small><?php echo esc_html($it['qty']); ?></span><?php endif; ?><?php if($it['parts']): ?><span><small>أرقام القطع</small><?php echo esc_html($it['parts']); ?></span><?php endif; ?></div><?php endif; ?>
          <div class="a3ms-history">
            <label for="a3ms-last-km-<?php echo esc_attr($it['id']); ?>">آخر تنفيذ لهذا البند عند عداد (كم) <input class="a3ms-last-km" id="a3ms-last-km-<?php echo esc_attr($it['id']); ?>" type="number" min="0" max="3000000" step="1" inputmode="numeric" placeholder="اختياري"></label>
            <label for="a3ms-last-date-<?php echo esc_attr($it['id']); ?>">تاريخ آخر تنفيذ لهذا البند <input class="a3ms-last-date" id="a3ms-last-date-<?php echo esc_attr($it['id']); ?>" type="date" max="<?php echo esc_attr(wp_date('Y-m-d')); ?>"></label>
          </div>
          <span class="a3ms-status">بانتظار حساب</span><div class="a3ms-result" role="status" aria-live="polite">أدخل العداد واضغط زر الحساب أعلى القائمة.</div>
          <?php if($it['source']||$it['checked']): ?><footer><?php if($it['checked']): ?><span>مراجعة: <?php echo esc_html($it['checked']); ?></span><?php endif; ?><?php if($it['source']): ?><a href="<?php echo esc_url($it['source']); ?>" target="_blank" rel="nofollow noopener">المصدر</a><?php endif; ?></footer><?php endif; ?>
        </div>
      </article>
    <?php endforeach; ?>
  </section>
  <?php else: ?><div class="g-platform-empty"><?php echo a3g_icon('calendar'); ?><h2>لا يوجد جدول موثّق لهذه المركبة حاليًا</h2><p>الموديل غير جاهز للحساب الآلي. استعرض المقالات المتاحة أسفل الصفحة، ولا تستخدم أرقام موديل مختلف.</p><a href="<?php echo esc_url(a3g_cat_link(86)); ?>">أدلة الصيانة المنشورة</a></div><?php endif; ?>
<?php endif; ?>

<?php a3g_legacy_section(
  [86],
  'أدلة وجداول الصيانة المتاحة',
  'مقالات وجداول صيانة منشورة تساعدك في الزيت والفلاتر والسوائل وفترات الفحص، مع الرجوع إلى دليل المالك للموديل عند تحديد المواعيد الدقيقة.',
  16,
  [],
  86
); ?>
</main>
<?php get_footer(); ?>