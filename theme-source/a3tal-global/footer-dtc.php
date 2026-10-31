<?php if (!defined('ABSPATH')) exit; ?>
<footer class="d-footer">
  <div class="d-wrap d-footer-row">
    <div><a class="d-footer-brand" data-google-vignette="false" href="<?php echo esc_url(home_url('/')); ?>">أعطال.كوم</a><p>الكود بداية التشخيص. الفحص يحدد السبب.</p></div>
    <nav aria-label="روابط مساعدة">
      <a href="<?php echo esc_url(home_url('/')); ?>">أعطال.كوم</a>
      <?php foreach ([43 => 'عن أعطال', 41 => 'اتصل بنا', 3 => 'الخصوصية'] as $dtc_page_id => $dtc_label): if (get_post_status($dtc_page_id) !== 'publish') continue; ?>
        <a href="<?php echo esc_url(get_permalink($dtc_page_id)); ?>"><?php echo esc_html($dtc_label); ?></a>
      <?php endforeach; ?>
    </nav>
    <small>© <?php echo esc_html(wp_date('Y')); ?> أعطال.كوم</small>
  </div>
</footer>
<?php wp_footer(); ?>
</body>
</html>
