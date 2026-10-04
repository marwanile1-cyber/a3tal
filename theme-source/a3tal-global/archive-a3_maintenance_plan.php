<?php
get_header();
$selected=absint(get_query_var('vehicle_entity'));
$vehicles=get_posts([
  'post_type'=>['a3_car','a3_motorcycle'],
  'post_status'=>'publish',
  'numberposts'=>300,
  'orderby'=>'title',
  'order'=>'ASC',
]);
$selected_post=$selected?get_post($selected):null;
?>
<section class="g-maintenance-hero"><div class="g-wrap g-maintenance-hero-grid">
  <div>
    <span>A3TAL MAINTENANCE</span>
    <h1>جدول صيانة يفهم عربيتك، مش جدول محفوظ</h1>
    <p>اختر المركبة وشوف الصيانة بالكيلومتر والزمن، مع وضع خاص للاستخدام الشاق ومواصفات السوائل وأرقام القطع.</p>
    <form method="get" class="g-maintenance-select">
      <label><small>اختر المركبة</small><select name="vehicle_entity" required><option value="">اختر السيارة أو الموتوسيكل</option><?php foreach($vehicles as $v): ?><option value="<?php echo esc_attr($v->ID); ?>" <?php selected($selected,$v->ID); ?>><?php echo esc_html($v->post_title); ?></option><?php endforeach; ?></select></label>
      <button type="submit">عرض جدول الصيانة</button>
    </form>
  </div>
  <div class="g-maintenance-demo">
    <div class="g-maintenance-demo-ring"><span>90K</span><small>الصيانة القادمة</small></div>
    <div class="g-maintenance-demo-list"><span class="is-due"><b>زيت المحرك</b><small>مستحق الآن</small></span><span class="is-soon"><b>فلتر الهواء</b><small>باقي 1,500 كم</small></span><span class="is-ok"><b>سائل الفرامل</b><small>باقي 5 أشهر</small></span></div>
  </div>
</div></section>

<main class="g-wrap g-maintenance-main">
<?php if(!$selected): ?>
  <section class="g-maintenance-intro">
    <div><span>01</span><h2>اختر المركبة</h2><p>الموديل والمحرك هما الأساس، مش مجرد سنة الصنع.</p></div>
    <div><span>02</span><h2>حدد استخدامك</h2><p>عادي، مدينة وزحام، سفر، أو استخدام شاق.</p></div>
    <div><span>03</span><h2>تابع الاستحقاقات</h2><p>كيلومترات وشهور وقطع وسوائل في Timeline واحدة.</p></div>
    <div><span>04</span><h2>احفظها في سيارتي</h2><p>أعطال يحسب المتبقي تلقائيًا من عدادك الحقيقي.</p></div>
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
    <div><span>جدول الصيانة</span><h2><?php echo esc_html($selected_post?$selected_post->post_title:'المركبة'); ?></h2><p>الفترات أدناه هي البيانات المنشورة للموديل. الاستخدام الشاق قد يقلل بعض الفترات.</p></div>
    <a href="<?php echo esc_url(home_url('/my-garage/')); ?>">أضفها إلى سيارتي</a>
  </section>

  <?php if($items): ?>
  <section class="g-maintenance-timeline">
    <div class="g-maintenance-rail"></div>
    <?php foreach($items as $index=>$it): $km=$it['first_km']?:$it['interval_km']; ?>
      <article class="g-maintenance-node">
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
          <?php if($it['source']||$it['checked']): ?><footer><?php if($it['checked']): ?><span>مراجعة: <?php echo esc_html($it['checked']); ?></span><?php endif; ?><?php if($it['source']): ?><a href="<?php echo esc_url($it['source']); ?>" target="_blank" rel="nofollow noopener">المصدر</a><?php endif; ?></footer><?php endif; ?>
        </div>
      </article>
    <?php endforeach; ?>
  </section>
  <?php else: ?><div class="g-platform-empty"><span>🗓️</span><h2>لسه مفيش جدول موثّق للموديل ده</h2><p>مش هنخترع فترات صيانة. هنضيفها بعد مراجعة دليل المالك أو مصدر الشركة.</p></div><?php endif; ?>
<?php endif; ?>
</main>
<?php get_footer(); ?>