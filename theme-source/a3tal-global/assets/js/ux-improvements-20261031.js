(function () {
  'use strict';
  function track(name, details) {
    // Use the existing Analytics installation and its consent configuration.
    if (typeof window.gtag !== 'function') return;
    try { window.gtag('event', name, details); } catch (_) { /* Navigation stays independent of analytics. */ }
  }
  function area(element) {
    if (element.closest('.d-header,.g-header')) return 'header';
    if (element.closest('.d-toc')) return 'article_contents';
    if (element.closest('.si-results')) return 'search_results';
    if (element.closest('.g-directory-card')) return 'service_directory';
    if (element.closest('.g-home')) return 'homepage';
    return 'article';
  }
  function ready() {
    // The documented AdSense per-link control, applied before a navigation click.
    document.querySelectorAll('.g-header a,.d-header a,.d-breadcrumb a,.d-toc a,.si-results a,.g-service-brand-hubs a,.d-code-card>a').forEach(function (link) {
      link.setAttribute('data-google-vignette', 'false');
    });
    document.addEventListener('submit', function (event) {
      var form = event.target;
      if (!form || !form.matches('form[role="search"],.g-platform-filter')) return;
      var input = form.querySelector('[name="code"],[name="s"]');
      var value = input ? input.value.trim() : '';
      var kind = /^[PBCU][0-9][0-9A-F]{3}$/i.test(value) ? 'diagnostic_code' : (form.matches('.g-platform-filter') ? 'directory_filter' : 'site_search');
      // Do not send free text, phone numbers, vehicle details or personal data.
      track('a3tal_search', { search_type: kind, form_location: area(form) });
    }, true);
    document.addEventListener('click', function (event) {
      var link = event.target.closest ? event.target.closest('a[href]') : null;
      if (!link) return;
      var href = link.getAttribute('href') || '';
      var action = link.getAttribute('data-a3tal-action') || '';
      if (href.indexOf('tel:') === 0) action = 'call';
      if (action) track('a3tal_contact_click', { contact_type: action, link_location: area(link) });
      else if (link.closest('nav,.si-results')) track('a3tal_navigation', { link_location: area(link) });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready, { once: true });
  else ready();
}());
