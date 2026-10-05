<footer class="g-footer">
  <div class="g-wrap">
    <div class="g-footer-grid">
      <div class="g-footer-brand">
        <a class="g-brand g-brand-footer" href="<?php echo esc_url(home_url('/')); ?>"><?php a3g_logo(); ?></a>
        <p>وجهتك العربية لكل ما يخص السيارات: أسعار، مراجعات، أعطال، صيانة ومراكز خدمة.</p>
        
      </div>
      <div><h3>روابط سريعة</h3><ul>
        <li><a href="<?php echo esc_url(a3g_cat_link(374)); ?>">أسعار السيارات</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(22)); ?>">المراجعات</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(21)); ?>">المقارنات</a></li>
        <li><a href="<?php echo esc_url(a3g_cat_link(8)); ?>">أعطال وحلول</a></li>
      </ul></div>
      <div><h3>خدماتنا</h3><ul>
        <li><a href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>">الصيانة</a></li>
        <li><a href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>">مراكز الخدمة</a></li>
        <li><a href="<?php echo esc_url(a3g_platform_link('a3_dtc','/dtc/')); ?>">أكواد الأعطال</a></li>
        <li><a href="<?php echo esc_url(a3g_platform_link('a3_part','/parts/')); ?>">قطع الغيار</a></li>
      </ul></div>
      <div><h3>مساعدة</h3><ul>
        <li><a href="<?php echo esc_url(get_permalink(43)); ?>">من نحن</a></li>
        <li><a href="<?php echo esc_url(get_permalink(41)); ?>">اتصل بنا</a></li>
        <li><a href="<?php echo esc_url(get_permalink(3)); ?>">سياسة الخصوصية</a></li>
        <li><a href="<?php echo esc_url(get_permalink(48)); ?>">شروط الاستخدام</a></li>
      </ul></div>
      <div class="g-newsletter"><h3>اشترك في نشرتنا البريدية</h3><p>كن أول من يعرف أهم أخبار السيارات والتحديثات الجديدة.</p><div class="g-newsletter-box"><input type="email" placeholder="بريدك الإلكتروني" aria-label="البريد الإلكتروني"><button type="button">اشتراك</button></div></div>
    </div>
    <div class="g-footer-bottom"><span>© <?php echo esc_html(date('Y')); ?> أعطال.كوم. جميع الحقوق محفوظة.</span><span>معلومات السيارات والأسعار تخضع للتحديث والمراجعة الدورية.</span></div>
  </div>
</footer>
<nav class="g-mobile-bottom" aria-label="اختصارات الجوال">
  <a href="<?php echo esc_url(home_url('/')); ?>"><span>⌂</span><b>الرئيسية</b></a>
  <a href="<?php echo esc_url(a3g_platform_link('a3_car','/cars/')); ?>"><span><?php echo a3g_icon('car'); ?></span><b>السيارات</b></a>
  <a class="is-main" href="<?php echo esc_url(a3g_cat_link(8)); ?>"><span><?php echo a3g_icon('warning'); ?></span><b>الأعطال</b></a>
  <a href="<?php echo esc_url(a3g_platform_link('a3_maintenance_plan','/maintenance-schedules/')); ?>"><span><?php echo a3g_icon('calendar'); ?></span><b>الصيانة</b></a>
  <a href="<?php echo esc_url(a3g_platform_link('a3_service_center','/service-centers/')); ?>"><span><?php echo a3g_icon('pin'); ?></span><b>المراكز</b></a>
</nav>
<?php wp_footer(); ?>
</body>
</html>
