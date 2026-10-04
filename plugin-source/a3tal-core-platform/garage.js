(() => {
  'use strict';

  const root = document.getElementById('a3tal-garage-app');
  if (!root || !window.A3talGarage || !A3talGarage.isLoggedIn) return;

  const state = {
    garage: [],
    selected: null,
    catalogs: { car: [], motorcycle: [] },
    maintenance: new Map()
  };

  const $ = (s, ctx=document) => ctx.querySelector(s);
  const $$ = (s, ctx=document) => Array.from(ctx.querySelectorAll(s));

  async function api(path, options={}) {
    const config = {
      credentials: 'same-origin',
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'X-WP-Nonce': A3talGarage.nonce,
        ...(options.headers || {})
      }
    };
    const res = await fetch(A3talGarage.rest + path.replace(/^\//,''), config);
    let data = {};
    try { data = await res.json(); } catch(e) {}
    if (!res.ok) {
      throw new Error(data?.message || 'حدث خطأ أثناء الاتصال بأعطال.');
    }
    return data;
  }

  async function loadCatalogs() {
    const read = async url => {
      const res = await fetch(url, {credentials:'same-origin'});
      if (!res.ok) return [];
      const rows = await res.json();
      return rows.map(row => ({
        id: Number(row.id),
        title: row?.title?.rendered ? decodeEntities(row.title.rendered) : ('#'+row.id),
        year: row?.meta?._a3_year || ''
      }));
    };
    const [cars, motorcycles] = await Promise.all([
      read(A3talGarage.carsUrl),
      read(A3talGarage.motorcyclesUrl)
    ]);
    state.catalogs.car = cars;
    state.catalogs.motorcycle = motorcycles;
  }

  function decodeEntities(text) {
    const area = document.createElement('textarea');
    area.innerHTML = text || '';
    return area.value;
  }

  async function loadGarage() {
    const data = await api('garage');
    state.garage = Array.isArray(data.items) ? data.items : [];
    renderVehicles();
    if (state.garage.length) {
      const keep = state.selected && state.garage.find(v => Number(v.id) === Number(state.selected.id));
      await selectVehicle(keep ? keep.id : state.garage[0].id);
    } else {
      state.selected = null;
      $('#a3garage-empty').hidden = false;
      $('#a3garage-detail').hidden = true;
    }
    await refreshStats();
  }

  function vehicleTitle(v) {
    const type = v.vehicle_type === 'motorcycle' ? 'motorcycle' : 'car';
    const entity = state.catalogs[type].find(x => Number(x.id) === Number(v.entity_id));
    return entity?.title || v.nickname || (type === 'car' ? 'سيارة' : 'موتوسيكل');
  }

  function renderVehicles() {
    const box = $('#a3garage-vehicles');
    box.innerHTML = '';
    if (!state.garage.length) {
      box.innerHTML = '<div class="a3garage-side-empty">لسه مفيش مركبات في الجراج.</div>';
      return;
    }
    state.garage.forEach(v => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'a3garage-vehicle-card' + (state.selected && Number(state.selected.id) === Number(v.id) ? ' is-active' : '');
      btn.dataset.id = v.id;
      btn.innerHTML = `
        <span class="a3garage-vehicle-icon">${v.vehicle_type === 'motorcycle' ? '🏍️' : '🚘'}</span>
        <span class="a3garage-vehicle-copy">
          <b>${escapeHtml(vehicleTitle(v))}</b>
          <small>${v.year ? escapeHtml(v.year) + ' • ' : ''}${formatNumber(v.odometer_km)} كم</small>
        </span>
      `;
      btn.addEventListener('click', () => selectVehicle(v.id));
      box.appendChild(btn);
    });
  }

  async function selectVehicle(id) {
    const found = state.garage.find(v => Number(v.id) === Number(id));
    if (!found) return;
    state.selected = found;
    renderVehicles();

    $('#a3garage-empty').hidden = true;
    $('#a3garage-detail').hidden = false;
    $('#a3garage-selected-type').textContent = found.vehicle_type === 'motorcycle' ? 'موتوسيكل' : 'سيارة';
    $('#a3garage-selected-title').textContent = vehicleTitle(found);
    $('#a3garage-selected-year').textContent = found.year ? 'موديل ' + found.year : 'السنة غير محددة';
    $('#a3garage-selected-km').textContent = formatNumber(found.odometer_km) + ' كم';
    $('#a3garage-selected-usage').textContent = usageLabel(found.usage_profile);

    const sell = $('[data-garage-action="sell"]');
    if (sell) sell.hidden = found.vehicle_type !== 'car';

    await loadMaintenance(found.id);
  }

  async function loadMaintenance(id) {
    const box = $('#a3garage-maintenance');
    box.innerHTML = '<div class="a3garage-loading">جاري بناء جدول الصيانة حسب مركبتك...</div>';
    try {
      const data = await api(`garage/${id}/maintenance`);
      state.maintenance.set(Number(id), data);
      renderMaintenance(data);
      updateNext(data);
    } catch (err) {
      box.innerHTML = '<div class="a3garage-maintenance-empty">' + escapeHtml(err.message) + '</div>';
    }
  }

  function renderMaintenance(data) {
    const box = $('#a3garage-maintenance');
    const items = Array.isArray(data.items) ? data.items : [];
    if (!items.length) {
      box.innerHTML = `
        <div class="a3garage-maintenance-empty">
          <span>🗓️</span>
          <h4>جدول الصيانة للموديل ده لسه بيتبني</h4>
          <p>هنعرض هنا الزيت والفلاتر والسوائل والفرامل والبوجيهات وباقي البنود بعد مراجعة المصدر الرسمي.</p>
        </div>`;
      return;
    }

    box.innerHTML = '';
    items.forEach(item => {
      const status = item.status || 'upcoming';
      const label = status === 'due' ? 'مستحقة الآن' : status === 'soon' ? 'قريبًا' : 'لاحقًا';
      const remaining = item.remaining_km === null
        ? ''
        : item.remaining_km <= 0
          ? `متأخرة ${formatNumber(Math.abs(item.remaining_km))} كم`
          : `باقي ${formatNumber(item.remaining_km)} كم`;
      const date = item.next_due_date ? new Date(item.next_due_date+'T00:00:00').toLocaleDateString('ar-EG',{year:'numeric',month:'short',day:'numeric'}) : '';
      const card = document.createElement('article');
      card.className = 'a3garage-maint-card is-' + status;
      card.innerHTML = `
        <div class="a3garage-maint-top">
          <span class="a3garage-maint-status">${label}</span>
          <span class="a3garage-maint-kind">${escapeHtml(item.action || item.kind || 'صيانة')}</span>
        </div>
        <h4>${escapeHtml(item.title || 'بند صيانة')}</h4>
        <div class="a3garage-progress"><i style="width:${Math.max(0,Math.min(100,Number(item.progress || 0)))}%"></i></div>
        <div class="a3garage-maint-facts">
          ${remaining ? '<span><small>المسافة</small><b>'+escapeHtml(remaining)+'</b></span>' : ''}
          ${date ? '<span><small>التاريخ</small><b>'+escapeHtml(date)+'</b></span>' : ''}
          ${item.fluid_spec ? '<span><small>المواصفة</small><b>'+escapeHtml(item.fluid_spec)+'</b></span>' : ''}
          ${item.part_numbers ? '<span><small>أرقام القطع</small><b>'+escapeHtml(item.part_numbers)+'</b></span>' : ''}
        </div>
      `;
      box.appendChild(card);
    });
  }

  function updateNext(data) {
    const items = Array.isArray(data.items) ? data.items : [];
    const first = items[0];
    if (!first) {
      $('#a3garage-next-title').textContent = 'لا يوجد جدول منشور للمركبة حتى الآن';
      $('#a3garage-next-copy').textContent = 'سيظهر تلقائيًا بعد إضافة جدول موثق للموديل.';
      $('#a3garage-next-percent').textContent = '—';
      $('#a3garage-next-ring').style.setProperty('--a3-progress','0deg');
      return;
    }
    const pct = Math.max(0, Math.min(100, Number(first.progress || 0)));
    $('#a3garage-next-title').textContent = first.title || 'الصيانة القادمة';
    const bits = [];
    if (first.remaining_km !== null) {
      bits.push(first.remaining_km <= 0 ? 'مستحقة الآن' : 'باقي ' + formatNumber(first.remaining_km) + ' كم');
    }
    if (first.next_due_date) bits.push('حتى ' + new Date(first.next_due_date+'T00:00:00').toLocaleDateString('ar-EG'));
    $('#a3garage-next-copy').textContent = bits.join(' • ') || 'راجع تفاصيل البند أدناه.';
    $('#a3garage-next-percent').textContent = pct + '%';
    $('#a3garage-next-ring').style.setProperty('--a3-progress',(pct*3.6)+'deg');
  }

  async function refreshStats() {
    $('#a3garage-stat-vehicles').textContent = state.garage.length;
    $('#a3garage-stat-km').textContent = formatNumber(state.garage.reduce((sum,v)=>sum+Number(v.odometer_km||0),0));

    let due = 0, soon = 0;
    const results = await Promise.all(state.garage.map(async v => {
      if (state.maintenance.has(Number(v.id))) return state.maintenance.get(Number(v.id));
      try {
        const data = await api(`garage/${v.id}/maintenance`);
        state.maintenance.set(Number(v.id), data);
        return data;
      } catch(e) { return {items:[]}; }
    }));
    results.forEach(data => (data.items || []).forEach(item => {
      if (item.status === 'due') due++;
      if (item.status === 'soon') soon++;
    }));
    $('#a3garage-stat-due').textContent = due;
    $('#a3garage-stat-soon').textContent = soon;
  }

  function usageLabel(v) {
    return ({
      normal:'استخدام عادي',
      'city-heavy':'مدينة وزحام كثيف',
      highway:'طرق مفتوحة / سفر',
      severe:'استخدام شاق'
    })[v] || 'استخدام عادي';
  }

  function formatNumber(v) {
    return new Intl.NumberFormat('ar-EG').format(Number(v || 0));
  }

  function escapeHtml(str) {
    return String(str ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  }

  function showDialog(id) {
    const d = document.getElementById(id);
    if (d && typeof d.showModal === 'function') d.showModal();
  }
  function closeDialog(el) {
    const d = el.closest('dialog');
    if (d) d.close();
  }
  $$('[data-dialog-close]').forEach(btn => btn.addEventListener('click',()=>closeDialog(btn)));

  function fillVehicleOptions(type) {
    const select = $('#a3garage-add-form select[name="entity_id"]');
    select.innerHTML = '<option value="">اختر الموديل</option>';
    (state.catalogs[type] || []).forEach(v => {
      const o = document.createElement('option');
      o.value = v.id;
      o.textContent = v.title + (v.year ? ' — ' + v.year : '');
      select.appendChild(o);
    });
  }

  $$('[data-garage-action="add"]').forEach(btn => btn.addEventListener('click',()=>{
    fillVehicleOptions($('#a3garage-add-form select[name="vehicle_type"]').value);
    showDialog('a3garage-add-dialog');
  }));
  $('#a3garage-add-form select[name="vehicle_type"]')?.addEventListener('change',e=>fillVehicleOptions(e.target.value));

  $('[data-garage-action="odometer"]')?.addEventListener('click',()=>{
    if (!state.selected) return;
    $('#a3garage-odo-form input[name="odometer_km"]').value = state.selected.odometer_km || 0;
    showDialog('a3garage-odo-dialog');
  });

  $('[data-garage-action="service"]')?.addEventListener('click',()=>{
    if (!state.selected) return;
    const form=$('#a3garage-service-form');
    form.querySelector('[name="event_date"]').value = new Date().toISOString().slice(0,10);
    form.querySelector('[name="odometer_km"]').value = state.selected.odometer_km || 0;
    showDialog('a3garage-service-dialog');
  });

  $('[data-garage-action="sell"]')?.addEventListener('click',()=>{
    if (!state.selected || state.selected.vehicle_type !== 'car') return;
    showDialog('a3garage-sell-dialog');
  });

  function formData(form) {
    return Object.fromEntries(new FormData(form).entries());
  }
  function message(form, text, bad=false) {
    const box = $('[data-form-message]', form);
    if (!box) return;
    box.textContent = text || '';
    box.classList.toggle('is-error', !!bad);
  }

  $('#a3garage-add-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    const form=e.currentTarget;
    message(form,'جاري الإضافة...');
    try {
      await api('garage',{method:'POST',body:JSON.stringify(formData(form))});
      form.closest('dialog').close();
      form.reset();
      await loadGarage();
    } catch(err) { message(form,err.message,true); }
  });

  $('#a3garage-odo-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    if(!state.selected) return;
    const form=e.currentTarget;
    try {
      await api('garage/'+state.selected.id,{method:'PATCH',body:JSON.stringify(formData(form))});
      form.closest('dialog').close();
      state.maintenance.delete(Number(state.selected.id));
      await loadGarage();
    } catch(err) { message(form,err.message,true); }
  });

  $('#a3garage-service-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    if(!state.selected) return;
    const form=e.currentTarget;
    try {
      await api('garage/'+state.selected.id+'/maintenance',{method:'POST',body:JSON.stringify(formData(form))});
      form.closest('dialog').close();
      state.maintenance.delete(Number(state.selected.id));
      await loadMaintenance(state.selected.id);
      await refreshStats();
    } catch(err) { message(form,err.message,true); }
  });

  $('#a3garage-sell-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    if(!state.selected) return;
    const form=e.currentTarget;
    try {
      const data=await api('garage/'+state.selected.id+'/sell',{method:'POST',body:JSON.stringify(formData(form))});
      message(form,data.message || 'تم إرسال الإعلان للمراجعة.');
      setTimeout(()=>form.closest('dialog').close(),1200);
    } catch(err) { message(form,err.message,true); }
  });

  Promise.all([loadCatalogs()]).then(loadGarage).catch(err => {
    const box=$('#a3garage-vehicles');
    if(box) box.innerHTML='<div class="a3garage-side-empty">'+escapeHtml(err.message)+'</div>';
  });
})();