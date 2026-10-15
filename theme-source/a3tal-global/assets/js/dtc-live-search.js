/* Progressive DTC search: the normal archive form remains fully functional without JS. */
(function () {
  'use strict';
  var form = document.querySelector('[data-dtc-search]');
  if (!form || !window.a3talDtcLookup || !window.fetch) return;
  var input = form.querySelector('input[name="code"]');
  if (!input) return;
  var family = form.querySelector('input[name="family"]');
  var panel = document.createElement('div');
  panel.id = 'a3tal-dtc-suggestions';
  panel.className = 'd-search-suggestions';
  panel.hidden = true;
  panel.setAttribute('aria-live', 'polite');
  form.insertAdjacentElement('afterend', panel);
  input.setAttribute('aria-controls', panel.id);
  input.setAttribute('aria-expanded', 'false');
  var timer = null, controller = null, sequence = 0;
  function hide() {
    panel.hidden = true;
    input.setAttribute('aria-expanded', 'false');
  }
  function show() {
    panel.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  }
  function element(tag, className, value) {
    var el = document.createElement(tag);
    if (className) el.className = className;
    if (value != null) el.textContent = value;
    return el;
  }
  function render(data) {
    panel.replaceChildren();
    var results = Array.isArray(data.results) ? data.results.slice(0, 8) : [];
    panel.appendChild(element('p', 'd-suggest-heading', data.total + ' نتيجة مطابقة في المكتبة'));
    results.forEach(function (item) {
      if (!item || !/^https?:\/\//i.test(item.url || '')) return;
      var link = element('a', 'd-suggest-item');
      link.href = item.url;
      link.appendChild(element('b', 'd-suggest-code', item.code));
      link.appendChild(element('span', 'd-suggest-title', item.title));
      link.appendChild(element('small', 'd-suggest-system', item.system));
      panel.appendChild(link);
    });
    if (!results.length) panel.appendChild(element('p', 'd-suggest-none', 'لا يوجد كود مطابق. جرّب اسم الحساس أو رقمًا آخر.'));
    show();
  }
  input.addEventListener('input', function () {
    var query = input.value.trim();
    sequence += 1;
    var current = sequence;
    window.clearTimeout(timer);
    if (controller) controller.abort();
    if (query.length < 2) { hide(); return; }
    timer = window.setTimeout(function () {
      controller = new AbortController();
      var params = new URLSearchParams({action:'a3g_dtc_lookup',q:query,family:family ? family.value : ''});
      fetch(window.a3talDtcLookup.endpoint + '?' + params.toString(), {
        credentials: 'same-origin', signal: controller.signal,
        headers: {'Accept':'application/json'}
      }).then(function (response) {
        if (!response.ok) throw new Error('search unavailable');
        return response.json();
      }).then(function (json) {
        if (current === sequence && json && json.success && json.data) render(json.data);
      }).catch(function (error) {
        if (error.name !== 'AbortError') hide();
      });
    }, 220);
  });
  input.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') hide();
  });
  document.addEventListener('click', function (event) {
    if (!form.contains(event.target) && !panel.contains(event.target)) hide();
  });
})();
