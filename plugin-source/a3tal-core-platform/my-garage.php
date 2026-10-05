<?php
if (!defined('ABSPATH')) exit;
get_header();
?>
<section class="a3garage-hero">
  <div class="g-wrap a3garage-hero-inner">
    <div>
      <span>MY A3TAL GARAGE</span>
      <h1>جراجك الرقمي على أعطال.كوم</h1>
      <p>أضف سيارتك أو موتوسيكلك مرة واحدة، وتابع العداد والصيانة القادمة وسجل الخدمات وقطع الغيار المناسبة، واعرض سيارتك للبيع من نفس المكان.</p>
    </div>
    <div class="a3garage-hero-badge">
      <b>خصوصية أولًا</b>
      <small>لا نعرض رقم اللوحة أو VIN للعامة.</small>
    </div>
  </div>
</section>

<main class="g-wrap a3garage-shell" id="a3tal-garage-app">
<?php if (!is_user_logged_in()): ?>
  <section class="a3garage-login">
    <div class="a3garage-login-icon">A3</div>
    <h2>سجّل الدخول لفتح جراجك</h2>
    <p>الجراج مرتبط بحسابك حتى يظل سجل المركبة والعداد والصيانة محفوظًا معك.</p>
    <div class="a3garage-onboarding">
      <span><b>1</b> سجّل الدخول أو أنشئ حسابًا.</span>
      <span><b>2</b> اختر موديلك وأدخل العداد الحالي.</span>
      <span><b>3</b> سجّل الصيانة وتابع الاستحقاقات من نفس الصفحة.</span>
    </div>
    <div class="a3garage-login-actions">
      <a href="<?php echo esc_url(wp_login_url(home_url('/my-garage/'))); ?>">تسجيل الدخول</a>
      <?php if(get_option('users_can_register')): ?><a class="is-secondary" href="<?php echo esc_url(wp_registration_url()); ?>">إنشاء حساب</a><?php endif; ?>
    </div>
  </section>
<?php else: ?>
  <div class="a3garage-toolbar">
    <div>
      <span>لوحة المركبات</span>
      <h2>سياراتي وموتوسيكلاتي</h2>
    </div>
    <button type="button" class="a3garage-primary" data-garage-action="add">+ إضافة مركبة</button>
  </div>

  <div class="a3garage-stats">
    <div><small>المركبات</small><strong id="a3garage-stat-vehicles">0</strong></div>
    <div><small>صيانة مستحقة</small><strong id="a3garage-stat-due">0</strong></div>
    <div><small>قريبة الاستحقاق</small><strong id="a3garage-stat-soon">0</strong></div>
    <div><small>إجمالي الكيلومترات</small><strong id="a3garage-stat-km">0</strong></div>
  </div>

  <div class="a3garage-layout">
    <aside class="a3garage-sidebar">
      <div class="a3garage-side-head"><strong>مركباتي</strong><button type="button" data-garage-action="add">+</button></div>
      <div id="a3garage-vehicles" class="a3garage-vehicles">
        <div class="a3garage-skeleton"></div>
        <div class="a3garage-skeleton"></div>
      </div>
    </aside>

    <section class="a3garage-main">
      <div id="a3garage-empty" class="a3garage-empty">
        <span>🚗</span>
        <h2>أضف أول مركبة</h2>
        <p>بعد الإضافة، أعطال هيبدأ يرتب لك جدول الصيانة حسب الموديل والعداد وطبيعة الاستخدام.</p>
        <button type="button" class="a3garage-primary" data-garage-action="add">إضافة مركبة</button>
      </div>

      <div id="a3garage-detail" hidden>
        <div class="a3garage-vehicle-hero">
          <div>
            <span id="a3garage-selected-type">سيارة</span>
            <h2 id="a3garage-selected-title">—</h2>
            <div class="a3garage-vehicle-meta">
              <span id="a3garage-selected-year">—</span>
              <span id="a3garage-selected-km">—</span>
              <span id="a3garage-selected-usage">—</span>
            </div>
          </div>
          <div class="a3garage-vehicle-actions">
            <button type="button" data-garage-action="odometer">تحديث العداد</button>
            <button type="button" data-garage-action="service">سجل صيانة</button>
            <button type="button" class="a3garage-sell" data-garage-action="sell">عرض للبيع</button>
          </div>
        </div>

        <section class="a3garage-next">
          <div class="a3garage-next-ring" id="a3garage-next-ring"><span id="a3garage-next-percent">0%</span></div>
          <div>
            <span>الصيانة الأقرب</span>
            <h3 id="a3garage-next-title">جاري حساب جدول الصيانة...</h3>
            <p id="a3garage-next-copy">بناءً على العداد وطبيعة الاستخدام.</p>
          </div>
        </section>

        <div class="a3garage-section-head">
          <div><span>MAINTENANCE TIMELINE</span><h3>حالة الصيانة الآن</h3></div>
          <div class="a3garage-legend"><i class="is-due"></i> مستحقة <i class="is-soon"></i> قريبًا <i class="is-ok"></i> لاحقًا</div>
        </div>
        <div id="a3garage-maintenance" class="a3garage-maintenance"></div>

        <section class="a3garage-quick-grid">
          <a href="<?php echo esc_url(get_post_type_archive_link('a3_part') ?: home_url('/parts/')); ?>"><span>⚙️</span><b>قطع مناسبة لمركبتك</b><small>OEM وAftermarket والبدائل</small></a>
          <a href="<?php echo esc_url(get_post_type_archive_link('a3_parts_vendor') ?: home_url('/parts-stores/')); ?>"><span>🧰</span><b>أماكن بيع القطع</b><small>رسمي، موثّق ومستقل</small></a>
          <a href="<?php echo esc_url(get_post_type_archive_link('a3_service_center') ?: home_url('/service-centers/')); ?>"><span>🔧</span><b>مراكز الخدمة</b><small>حسب الماركة والسوق</small></a>
          <a href="<?php echo esc_url(get_post_type_archive_link('a3_dtc') ?: home_url('/dtc/')); ?>"><span>⚠️</span><b>أكواد الأعطال</b><small>ابحث عن كود DTC</small></a>
        </section>
      </div>
    </section>
  </div>

  <dialog class="a3garage-dialog" id="a3garage-add-dialog">
    <form method="dialog" class="a3garage-dialog-card" id="a3garage-add-form">
      <div class="a3garage-dialog-head"><div><span>إضافة مركبة</span><h3>عرّف أعطال على مركبتك</h3></div><button value="cancel" type="button" data-dialog-close>×</button></div>
      <div class="a3garage-form-grid">
        <label><span>النوع</span><select name="vehicle_type"><option value="car">سيارة</option><option value="motorcycle">موتوسيكل</option></select></label>
        <label><span>الموديل</span><select name="entity_id" required><option value="">اختر الموديل</option></select></label>
        <label><span>اسم مختصر</span><input name="nickname" placeholder="مثال: عربيتي اليومية"></label>
        <label><span>سنة الموديل</span><input name="year" type="number" min="1950" max="2100"></label>
        <label><span>عداد الكيلومترات</span><input name="odometer_km" type="number" min="0" required></label>
        <label><span>طبيعة الاستخدام</span><select name="usage_profile"><option value="normal">عادي</option><option value="city-heavy">مدينة وزحام كثيف</option><option value="highway">سفر / طرق مفتوحة</option><option value="severe">استخدام شاق</option></select></label>
        <label><span>آخر جزء من رقم اللوحة <small>اختياري</small></span><input name="plate_hint" maxlength="12"></label>
        <label><span>آخر 6 من VIN <small>اختياري</small></span><input name="vin_hint" maxlength="6"></label>
        <label><span>بداية الملكية</span><input name="ownership_started" type="date"></label>
      </div>
      <div class="a3garage-dialog-actions"><button value="cancel" type="button" data-dialog-close>إلغاء</button><button type="submit" class="a3garage-primary">إضافة للجراج</button></div>
      <div class="a3garage-form-message" data-form-message></div>
    </form>
  </dialog>

  <dialog class="a3garage-dialog" id="a3garage-odo-dialog">
    <form method="dialog" class="a3garage-dialog-card" id="a3garage-odo-form">
      <div class="a3garage-dialog-head"><div><span>تحديث العداد</span><h3>كم وصلت المركبة الآن؟</h3></div><button type="button" data-dialog-close>×</button></div>
      <label class="a3garage-wide-label"><span>عداد الكيلومترات الحالي</span><input name="odometer_km" type="number" min="0" required></label>
      <div class="a3garage-dialog-actions"><button type="button" data-dialog-close>إلغاء</button><button type="submit" class="a3garage-primary">تحديث</button></div>
      <div class="a3garage-form-message" data-form-message></div>
    </form>
  </dialog>

  <dialog class="a3garage-dialog" id="a3garage-service-dialog">
    <form method="dialog" class="a3garage-dialog-card" id="a3garage-service-form">
      <div class="a3garage-dialog-head"><div><span>سجل الصيانة</span><h3>أضف عملية صيانة للسجل</h3></div><button type="button" data-dialog-close>×</button></div>
      <div class="a3garage-form-grid">
        <label><span>نوع الصيانة</span><select name="event_type"><option value="engine-oil">زيت المحرك</option><option value="oil-filter">فلتر الزيت</option><option value="air-filter">فلتر الهواء</option><option value="cabin-filter">فلتر التكييف</option><option value="brake-pads">تيل الفرامل</option><option value="transmission-fluid">زيت الفتيس</option><option value="coolant">سائل التبريد</option><option value="inspection">فحص دوري</option><option value="service">صيانة أخرى</option></select></label>
        <label><span>التاريخ</span><input name="event_date" type="date" required></label>
        <label><span>العداد وقت الصيانة</span><input name="odometer_km" type="number" min="0" required></label>
        <label><span>العنوان</span><input name="title" placeholder="مثال: تغيير زيت وفلتر"></label>
        <label><span>التكلفة</span><input name="cost" type="number" min="0" step="0.01"></label>
        <label><span>العملة</span><input name="currency" value="EGP"></label>
        <label><span>الاستحقاق القادم بالكيلومتر</span><input name="next_due_km" type="number" min="0"></label>
        <label><span>الاستحقاق القادم بالتاريخ</span><input name="next_due_date" type="date"></label>
        <label class="a3garage-span-2"><span>ملاحظات</span><textarea name="details" rows="3"></textarea></label>
      </div>
      <div class="a3garage-dialog-actions"><button type="button" data-dialog-close>إلغاء</button><button type="submit" class="a3garage-primary">حفظ الصيانة</button></div>
      <div class="a3garage-form-message" data-form-message></div>
    </form>
  </dialog>

  <dialog class="a3garage-dialog" id="a3garage-sell-dialog">
    <form method="dialog" class="a3garage-dialog-card" id="a3garage-sell-form">
      <div class="a3garage-dialog-head"><div><span>A3TAL MARKET</span><h3>اعرض سيارتك للبيع</h3></div><button type="button" data-dialog-close>×</button></div>
      <div class="a3garage-form-grid">
        <label><span>السعر المطلوب</span><input name="price" type="number" min="1" required></label>
        <label><span>العملة</span><input name="currency" value="EGP"></label>
        <label><span>الموقع</span><input name="location" placeholder="المحافظة / المدينة"></label>
        <label><span>هاتف التواصل</span><input name="phone" inputmode="tel"></label>
        <label class="a3garage-span-2"><span>وصف مختصر</span><textarea name="description" rows="4" placeholder="الحالة، الصيانة، الملاحظات المهمة..."></textarea></label>
      </div>
      <div class="a3garage-safety-note">رقم اللوحة وVIN لا يظهران في الإعلان. الإعلان يدخل للمراجعة قبل النشر.</div>
      <div class="a3garage-dialog-actions"><button type="button" data-dialog-close>إلغاء</button><button type="submit" class="a3garage-primary">إرسال الإعلان للمراجعة</button></div>
      <div class="a3garage-form-message" data-form-message></div>
    </form>
  </dialog>
<?php endif; ?>
</main>
<?php get_footer(); ?>
