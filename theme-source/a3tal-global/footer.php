<footer class="g-footer">
  <div class="g-wrap">
    <div class="g-footer-grid">
      <div class="g-footer-brand">
        <a class="g-brand g-brand-footer" href="<?php echo esc_url(home_url('/')); ?>"><?php a3g_logo(); ?></a>
        <p>وجهتك العربية لكل ما يخص السيارات: أسعار، مراجعات، أعطال، صيانة ومراكز خدمة.</p>
        <div class="g-socials"><a href="#" aria-label="يوتيوب">▶</a><a href="#" aria-label="إنستجرام">◎</a><a href="#" aria-label="إكس">𝕏</a><a href="#" aria-label="فيسبوك">f</a></div>
      </div>
      <div><h3>روابط سريعة</h3><ul>
        <li><a href="<?php echo esc_url(a3g_cat_link(374)); ?>">أسعار السيارات</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(22)); ?>">المراجعات</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(21)); ?>">المقارنات</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(8)); ?>">أعطال وحلول</a></li>
      </ul></div>
      <div><h3>خدماتنا</h3><ul>
        <li><a href="<?php echo esc_url(a3g_cat_link(3)); ?>">الصيانة</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(33)); ?>">مراكز الخدمة</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(2)); ?>">أكواد الأعطال</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(85)); ?>">قطع الغيار</a></li>
      </ul></div>
      <div><h3>مساعدة</h3><ul>
        <li><a href="<?php echo esc_url(home_url('/about-us/')); ?>">من نحن</a></li>
        <li><a href="<?php echo esc_url(home_url('/contact/')); ?>">اتصل بنا</a></li>
        <li><a href="<?php echo esc_url(home_url('/privacy-policy/')); ?>">سياسة الخصوصية</a></li>
        <li><a href="<?php echo esc_url(home_url('/terms/')); ?>">شروط الاستخدام</a></li>
      </ul></div>
      <div class="g-newsletter"><h3>اشترك في نشرتنا البريدية</h3><p>كن أول من يعرف أهم أخبار السيارات والتحديثات الجديدة.</p><div class="g-newsletter-box"><input type="email" placeholder="بريدك الإلكتروني" aria-label="البريد الإلكتروني"><button type="button">اشتراك</button></div></div>
    </div>
    <div class="g-footer-bottom"><span>© <?php echo esc_html(date('Y')); ?> أعطال.كوم. جميع الحقوق محفوظة.</span><span>معلومات السيارات والأسعار تخضع للتحديث والمراجعة الدورية.</span></div>
  </div>
</footer>
<nav class="g-mobile-bottom" aria-label="اختصارات الجوال">
  <a href="<?php echo esc_url(home_url('/')); ?>"><span>⌂</span><b>الرئيسية</b></a>
  <a href="<?php echo esc_url(a3g_cat_link(374)); ?>"><span>🚘</span><b>الأسعار</b></a>
  <a class="is-main" href="<?php echo esc_url(a3g_cat_link(8)); ?>"><span>⚙</span><b>الأعطال</b></a>
  <a href="<?php echo esc_url(a3g_cat_link(3)); ?>"><span>🔧</span><b>الصيانة</b></a>
  <a href="<?php echo esc_url(a3g_cat_link(33)); ?>"><span>⌖</span><b>المراكز</b></a>
</nav>
<?php wp_footer(); ?>
</body>
</html>
