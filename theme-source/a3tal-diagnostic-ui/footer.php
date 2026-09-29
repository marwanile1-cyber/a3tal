<footer class="a3-site-footer">
  <div class="a3-container">
    <div class="a3-footer-grid">
      <div>
        <a class="a3-brand" href="<?php echo esc_url(home_url('/')); ?>">
          <span class="a3-brand-mark">أ</span>
          <span class="a3-brand-copy"><strong style="color:#fff">أعطال.كوم</strong><small>تشخيص وصيانة السيارات</small></span>
        </a>
        <p>محتوى يساعدك على فهم العرض، معرفة الاختبارات المنطقية، وتقليل تغيير القطع بالتخمين.</p>
      </div>
      <div><h3>التشخيص</h3><ul><li><a href="<?php echo esc_url(a3du_search_url('أعطال السيارات')); ?>">أعطال السيارات</a></li><li><a href="<?php echo esc_url(a3du_search_url('P0420')); ?>">أكواد DTC</a></li><li><a href="<?php echo esc_url(a3du_search_url('حساس')); ?>">الحساسات</a></li></ul></div>
      <div><h3>السيارة</h3><ul><li><a href="<?php echo esc_url(a3du_search_url('صيانة')); ?>">الصيانة</a></li><li><a href="<?php echo esc_url(a3du_search_url('دليل السيارات')); ?>">دليل السيارات</a></li><li><a href="<?php echo esc_url(a3du_search_url('مركز خدمة')); ?>">مراكز الخدمة</a></li></ul></div>
      <div><h3>الموقع</h3><ul><li><a href="<?php echo esc_url(home_url('/عن-الموقع/')); ?>">عن الموقع</a></li><li><a href="<?php echo esc_url(home_url('/contact/')); ?>">اتصل بنا</a></li><li><a href="<?php echo esc_url(home_url('/privacy-policy/')); ?>">الخصوصية</a></li></ul></div>
    </div>
    <div class="a3-footer-bottom">© <?php echo esc_html(date('Y')); ?> أعطال.كوم</div>
  </div>
</footer>
<nav class="a3-bottom-nav" aria-label="تنقل سريع">
  <a href="<?php echo esc_url(home_url('/')); ?>"><span class="a3-bottom-icon">⌂</span><span>الرئيسية</span></a>
  <a class="is-primary" href="<?php echo esc_url(a3du_search_url('عطل')); ?>"><span class="a3-bottom-icon">⌕</span><span>شخّص</span></a>
  <a href="<?php echo esc_url(a3du_search_url('P0420')); ?>"><span class="a3-bottom-icon">#</span><span>DTC</span></a>
  <a href="#" class="a3-open-car"><span class="a3-bottom-icon">▣</span><span>عربيتي</span></a>
  <a href="<?php echo esc_url(a3du_search_url('')); ?>"><span class="a3-bottom-icon">≡</span><span>المزيد</span></a>
</nav>
<div class="a3-modal" id="a3-car-modal" aria-hidden="true">
  <div class="a3-modal-card">
    <h2>أضف عربيتك</h2>
    <p style="color:#64748B">احفظ بيانات السيارة على هذا الجهاز لتخصيص تجربة التصفح. النسخة التجريبية تحفظ الاختيار محليًا فقط.</p>
    <div class="a3-field-grid">
      <div class="a3-field"><label for="a3-car-make">الماركة</label><input id="a3-car-make" placeholder="مثال: Hyundai"></div>
      <div class="a3-field"><label for="a3-car-model">الموديل</label><input id="a3-car-model" placeholder="مثال: Elantra AD"></div>
      <div class="a3-field"><label for="a3-car-year">السنة</label><input id="a3-car-year" inputmode="numeric" placeholder="2019"></div>
      <div class="a3-field"><label for="a3-car-engine">المحرك</label><input id="a3-car-engine" placeholder="1.6 MPI"></div>
    </div>
    <div class="a3-modal-actions">
      <button class="a3-btn a3-btn-primary" id="a3-save-car" type="button">حفظ السيارة</button>
      <button class="a3-btn" id="a3-close-car" type="button">إلغاء</button>
    </div>
  </div>
</div>
<?php wp_footer(); ?>
</body></html>
