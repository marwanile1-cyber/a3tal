/* A3tal maintenance calculator v1. Verified per-model source data only.
 * Nothing is stored, sent or inferred from unrelated models.
 */
(function(){
  'use strict';
  const root=document.getElementById('a3ms-calculator');
  if(!root) return;
  const kmInput=root.querySelector('#a3ms-current-km');
  const firstDate=root.querySelector('#a3ms-delivery-date');
  const usage=root.querySelector('#a3ms-usage');
  const action=root.querySelector('#a3ms-calc-button');
  const notice=root.querySelector('#a3ms-notice');
  const summary=root.querySelector('#a3ms-summary');
  const rows=Array.from(document.querySelectorAll('.a3ms-item'));
  const nf=new Intl.NumberFormat('ar-EG',{maximumFractionDigits:0});
  const str=(v)=>String(v==null?'':v).trim();
  const intValue=(v)=>{const text=str(v);if(!/^\d+$/.test(text))return null;const n=Number(text);return Number.isSafeInteger(n)&&n>=0&&n<=3000000?n:null;};
  const isoDate=(value)=>{
    if(!/^\d{4}-\d{2}-\d{2}$/.test(str(value)))return null;
    const d=new Date(value+'T12:00:00Z');
    return !Number.isNaN(d.getTime())&&d.toISOString().slice(0,10)===value?d:null;
  };
  const addMonths=(date,months)=>{
    const d=new Date(date.getTime());
    const day=d.getUTCDate();
    d.setUTCDate(1);d.setUTCMonth(d.getUTCMonth()+months);
    const lastDay=new Date(Date.UTC(d.getUTCFullYear(),d.getUTCMonth()+1,0)).getUTCDate();
    d.setUTCDate(Math.min(day,lastDay));
    return d;
  };
  const formatDate=(d)=>new Intl.DateTimeFormat('ar-EG',{day:'numeric',month:'short',year:'numeric',timeZone:'UTC'}).format(d);
  const dateToday=()=>{const now=new Date();return new Date(Date.UTC(now.getFullYear(),now.getMonth(),now.getDate(),12));};
  const dayDiff=(a,b)=>Math.ceil((a.getTime()-b.getTime())/86400000);
  function clearRow(node,message){
    node.classList.remove('a3ms-due','a3ms-soon','a3ms-review','a3ms-later');
    const label=node.querySelector('.a3ms-status'),result=node.querySelector('.a3ms-result');
    label.textContent='بانتظار حساب';result.textContent=message;
  }
  function calculate(){
    const current=intValue(kmInput.value);
    if(current===null){
      notice.textContent='أدخل قراءة العداد الحالية بالكيلومتر من 0 إلى 3,000,000.';
      summary.hidden=true;
      rows.forEach(n=>clearRow(n,'أدخل قراءة العداد ثم اضغط احسب الاستحقاقات.'));
      return;
    }
    const today=dateToday(),delivered=str(firstDate.value)?isoDate(firstDate.value):null;
    if(str(firstDate.value) && (!delivered||delivered>today)){
      notice.textContent='تاريخ بداية الاستخدام لازم يكون تاريخًا صحيحًا وليس في المستقبل.';
      summary.hidden=true;return;
    }
    let due=0,soon=0,review=0,later=0;
    rows.forEach((node)=>{
      const status=node.querySelector('.a3ms-status');
      const result=node.querySelector('.a3ms-result');
      node.classList.remove('a3ms-due','a3ms-soon','a3ms-review','a3ms-later');
      if(node.dataset.verified!=='1'){
        status.textContent='بيانات غير مكتملة';result.textContent='الجدول غير موثق بمصدر وتاريخ مراجعة، لذلك لم نحسب موعدًا آليًا.';review++;node.classList.add('a3ms-review');return;
      }
      const firstKm=Number(node.dataset.firstKm)||0;
      const firstMonths=Number(node.dataset.firstMonths)||0;
      const regularKm=Number(node.dataset.intervalKm)||0;
      const severeKm=Number(node.dataset.severeKm)||0;
      const regularMonths=Number(node.dataset.intervalMonths)||0;
      const severeMonths=Number(node.dataset.severeMonths)||0;
      const kmInterval=usage.value==='severe'&&severeKm>0?severeKm:regularKm;
      const monthInterval=usage.value==='severe'&&severeMonths>0?severeMonths:regularMonths;
      const lastKmField=node.querySelector('.a3ms-last-km');
      const lastDateField=node.querySelector('.a3ms-last-date');
      const lastKm=str(lastKmField.value)?intValue(lastKmField.value):null;
      const lastDate=str(lastDateField.value)?isoDate(lastDateField.value):null;
      if((str(lastKmField.value)&&lastKm===null)||(lastKm!==null&&lastKm>current)
        ||(str(lastDateField.value)&&(!lastDate||lastDate>today))){
        status.textContent='راجع الإدخال';result.textContent='عداد آخر صيانة يجب ألا يتجاوز العداد الحالي، والتاريخ لا يجوز أن يكون في المستقبل.';review++;node.classList.add('a3ms-review');return;
      }
      let nextKm=null,explicitKm=false,needsRecord=false,nextDate=null,explicitDate=false;
      if(lastKm!==null){
        if(kmInterval>0){nextKm=lastKm+kmInterval;explicitKm=true;}
      }else if(firstKm>0){
        if(current<firstKm){nextKm=firstKm;}
        else if(kmInterval>0){
          const cycles=Math.floor((current-firstKm)/kmInterval)+1;
          nextKm=firstKm+cycles*kmInterval;
          needsRecord=true;
        }else{needsRecord=true;}
      }
      if(lastDate){
        if(monthInterval>0){nextDate=addMonths(lastDate,monthInterval);explicitDate=true;}
      }else if(delivered&&firstMonths>0){
        nextDate=addMonths(delivered,firstMonths);
        if(nextDate<today)needsRecord=true;
      }else if(monthInterval>0 || firstMonths>0){
        needsRecord=true;
      }
      if(lastKm!==null&&kmInterval<=0&&monthInterval<=0){
        status.textContent='خدمة سابقة مسجلة';result.textContent='خدمة أولى أو غير متكررة؛ راجع تعليمات الشركة ولا تعيدها افتراضيًا.';later++;node.classList.add('a3ms-later');return;
      }
      const kmRemaining=nextKm===null?null:nextKm-current;
      const daysRemaining=nextDate?dayDiff(nextDate,today):null;
      const notes=[];
      if(nextKm!==null)notes.push('الموعد المحسوب: '+nf.format(nextKm)+' كم'+(kmRemaining>0?'، باقي '+nf.format(kmRemaining)+' كم':kmRemaining===0?'، عند العداد الحالي':'، متجاوز بـ'+nf.format(-kmRemaining)+' كم'));
      if(nextDate)notes.push('موعد الزمن: '+formatDate(nextDate)+(daysRemaining>0?'، باقي '+daysRemaining+' يومًا':''));
      else if(firstMonths>0||monthInterval>0)notes.push('لم يُحسب موعد الشهور: أدخل تاريخ الاستلام أو آخر صيانة للبند.');
      if(usage.value==='severe'&&severeKm<=0&&severeMonths<=0)notes.push('لا توجد فترة استخدام شاق موثقة لهذا البند؛ عُرضت الفترة العادية.');
      if(!notes.length)notes.push('الفترة المسجلة لا تكفي لحساب الموعد، راجع جدول الشركة.');
      const isDue=(explicitKm&&kmRemaining!==null&&kmRemaining<=0)
        ||(explicitDate&&daysRemaining!==null&&daysRemaining<=0)
        ||(nextKm!==null&&lastKm===null&&current===firstKm&&firstKm>0)
        ||(nextDate!==null&&delivered&&firstMonths>0&&daysRemaining!==null&&daysRemaining<=0&&lastDate===null);
      const isSoon=(kmRemaining!==null&&kmRemaining>=0&&kmRemaining<=1000)
        ||(daysRemaining!==null&&daysRemaining>=0&&daysRemaining<=30);
      if(needsRecord&&(!lastKm&&!lastDate)&&(current>=firstKm||nextDate)){
        status.textContent='تحتاج مراجعة السجل';
        notes.push('بدون تاريخ الصيانة السابقة لا يمكن التأكد إذا كانت نُفذت بالفعل.');
        node.classList.add('a3ms-review');review++;
      }else if(isDue){
        status.textContent='راجع استحقاق الخدمة الآن';node.classList.add('a3ms-due');due++;
      }else if(isSoon){
        status.textContent='صيانة قريبة';node.classList.add('a3ms-soon');soon++;
      }else{
        status.textContent='استحقاق قادم';node.classList.add('a3ms-later');later++;
      }
      result.textContent=notes.join(' • ');
    });
    summary.hidden=false;
    summary.textContent='نتائج الحساب: '+due+' بند مستحق للتحقق، '+soon+' قريب، '+review+' يحتاج مراجعة السجل، '+later+' لاحقًا.';
    notice.textContent='الحساب استرشادي من الفترات الموثقة للمركبة المختارة. مواعيد الشهور والكيلومترات تُراجع معًا وأيهما أسبق عند توافر بيانات آخر صيانة لكل بند. لم تُحفظ أي بيانات.';
  }
  action.addEventListener('click',calculate);
  root.addEventListener('submit',event=>{event.preventDefault();calculate();});
  root.querySelectorAll('input,select').forEach(el=>el.addEventListener('change',()=>{
    if(!summary.hidden)calculate();
  }));
  rows.forEach(n=>n.querySelectorAll('input').forEach(el=>el.addEventListener('change',()=>{
    if(!summary.hidden)calculate();
  })));
})();
