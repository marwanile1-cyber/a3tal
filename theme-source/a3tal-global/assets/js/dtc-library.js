/* DTC discussions: native WordPress storage, no account or email required. */
(function () {
  'use strict';
  function normalizeCode(value) {
    return value.replace(/[٠-٩۰-۹]/g, function (digit) {
      var point = digit.charCodeAt(0);
      return String(point >= 1776 ? point - 1776 : point - 1632);
    }).replace(/\s+/g, '').toUpperCase();
  }
  document.querySelectorAll('form[data-dtc-search]').forEach(function (searchForm) {
    searchForm.addEventListener('submit', function () {
      var code = searchForm.querySelector('[name="code"]');
      if (code) code.value = normalizeCode(code.value);
    });
  });
  var section = document.getElementById('dtc-discussion');
  var config = window.a3Dtc || {};
  if (!section || !config.ajaxUrl) return;
  var form = section.querySelector('.d-comment-form');
  if (!form) return;
  var submit = form.querySelector('[type="submit"]');
  var status = form.querySelector('.d-form-status');
  var parent = form.querySelector('[name="comment_parent"]');
  var replyBox = form.querySelector('.d-reply-context');
  var replyName = form.querySelector('.d-reply-name');
  var postId = section.getAttribute('data-post-id');
  var token = null;
  var tokenLoading = null;
  var busy = false;

  function makeVisitor() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') return window.crypto.randomUUID();
    if (window.crypto && window.crypto.getRandomValues) {
      var bytes = new Uint8Array(24);
      window.crypto.getRandomValues(bytes);
      return Array.from(bytes, function (b) { return b.toString(16).padStart(2, '0'); }).join('');
    }
    return 'dtc-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2);
  }
  var visitor = '';
  try {
    visitor = window.localStorage.getItem('a3g_dtc_visitor_v1') || '';
    if (!/^[a-zA-Z0-9_-]{16,96}$/.test(visitor)) {
      visitor = makeVisitor();
      window.localStorage.setItem('a3g_dtc_visitor_v1', visitor);
    }
  } catch (e) { visitor = makeVisitor(); }

  function message(text, kind) {
    status.textContent = text;
    status.setAttribute('data-state', kind || 'info');
  }

  function request(action, fields, protectedRequest) {
    var body = new URLSearchParams();
    body.set('action', action);
    body.set('post_id', postId);
    body.set('visitor', visitor);
    if (protectedRequest && token) {
      body.set('_ajax_nonce', token.nonce);
      body.set('challenge', token.challenge);
    }
    Object.keys(fields || {}).forEach(function (key) { body.set(key, fields[key]); });
    return fetch(config.ajaxUrl, {
      method: 'POST', credentials: 'same-origin', cache: 'no-store',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': 'application/json' },
      body: body.toString()
    }).then(function (response) {
      return response.json().then(function (result) {
        if (!result || result.success !== true) {
          var error = new Error(result && result.data && result.data.message || 'تعذر الاتصال. حاول مرة أخرى.');
          error.code = result && result.data && result.data.code || 'network';
          throw error;
        }
        return result.data;
      });
    }).catch(function (error) {
      if (error.code) throw error;
      var networkError = new Error('تعذر الاتصال بالخادم. مشاركتك ما زالت موجودة، ويمكنك المحاولة مجددًا.');
      networkError.code = 'network';
      throw networkError;
    });
  }

  function refreshToken() {
    if (tokenLoading) return tokenLoading;
    tokenLoading = request('a3g_dtc_token', {}, false).then(function (data) {
      if (!data.nonce || !data.challenge) throw new Error('تعذر تجهيز النموذج. أعد المحاولة.');
      token = { nonce: data.nonce, challenge: data.challenge, issuedAt: Date.now(), expiresAt: Date.now() + data.expiresIn * 1000 };
      // The signed challenge enforces a short, invisible minimum fill time.
      return new Promise(function (resolve) { window.setTimeout(resolve, 2200); });
    }).finally(function () { tokenLoading = null; });
    return tokenLoading;
  }

  function ensureToken() {
    if (tokenLoading) return tokenLoading;
    if (!token || Date.now() > token.expiresAt - 10000) return refreshToken();
    return Promise.resolve();
  }

  function protectedRequest(action, fields) {
    return ensureToken().then(function () { return request(action, fields, true); }).catch(function (error) {
      if (error.code !== 'token_expired') throw error;
      return refreshToken().then(function () { return request(action, fields, true); });
    });
  }

  function resetReply() {
    parent.value = '0';
    replyBox.hidden = true;
    replyName.textContent = '';
  }

  section.addEventListener('click', function (event) {
    var reply = event.target.closest('.d-comment-reply');
    if (reply && section.contains(reply)) {
      parent.value = reply.getAttribute('data-comment-id');
      replyName.textContent = reply.getAttribute('data-author') || 'المشاركة';
      replyBox.hidden = false;
      form.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
      form.querySelector('[name="comment"]').focus({ preventScroll: true });
      return;
    }
    if (event.target.closest('.d-reply-cancel')) { resetReply(); return; }
    var report = event.target.closest('.d-comment-report');
    if (!report || !section.contains(report) || report.disabled) return;
    report.disabled = true;
    var reportStatus = report.parentElement.querySelector('.d-report-status');
    reportStatus.textContent = 'جارٍ إرسال البلاغ…';
    protectedRequest('a3g_dtc_report', { comment_id: report.getAttribute('data-comment-id') }).then(function (data) {
      reportStatus.textContent = data.message;
      report.textContent = 'تم الإبلاغ';
    }).catch(function (error) {
      reportStatus.textContent = error.message || 'تعذر الإبلاغ الآن. حاول مجددًا.';
      report.disabled = false;
    });
  });

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (busy || !form.reportValidity()) return;
    busy = true;
    submit.disabled = true;
    form.setAttribute('aria-busy', 'true');
    message('جارٍ إرسال مشاركتك…');
    var fields = {};
    new FormData(form).forEach(function (value, key) { fields[key] = value; });
    protectedRequest('a3g_dtc_comment', fields).then(function (data) {
      form.querySelector('[name="comment"]').value = '';
      form.querySelector('[name="tried"]').value = '';
      resetReply();
      message(data.message, 'success');
    }).catch(function (error) {
      message(error.message || 'تعذر الإرسال. مشاركتك ما زالت موجودة، ويمكنك المحاولة مجددًا.', 'error');
    }).finally(function () {
      busy = false;
      submit.disabled = false;
      form.removeAttribute('aria-busy');
    });
  });

  refreshToken().then(function () {
    submit.disabled = false;
    message('مشاركتك ستظهر بعد المراجعة.');
  }).catch(function (error) {
    // Submission retries token setup; keep the form usable after transient errors.
    submit.disabled = false;
    message(error.message || 'تعذر تجهيز النموذج الآن. يمكنك إعادة المحاولة عند الإرسال.', 'error');
  });
})();
