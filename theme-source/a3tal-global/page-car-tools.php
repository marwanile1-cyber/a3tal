<?php
/**
 * A3tal working utility page for fuel and workshop cost arithmetic.
 * This is an interactive calculator, not a price feed or mechanical diagnosis.
 * Does not collect, transmit or persist form values.
 */
defined('ABSPATH') || exit;
get_header();
?>
<main id="a3tal-real-tools" dir="rtl" class="a3rt">
  <div class="a3rt-wrap">
    <nav class="a3rt-crumb" aria-label="مسار التصفح"><a href="<?php echo esc_url(home_url('/')); ?>">الرئيسية</a><span aria-hidden="true"> / </span>أدوات مالك السيارة</nav>
    <header class="a3rt-hero">
      <span class="a3rt-kicker">A3TAL • أدوات حساب فعلية</span>
      <h1>حاسبة استهلاك البنزين وتكلفة صيانة السيارة</h1>
      <p>أدخل بياناتك بنفسك واحسب النتيجة فورًا. الحسابات تقديرية ولا تتطلب تسجيلًا ولا تُرسل بياناتك إلى الموقع.</p>
    </header>
    <nav class="a3rt-tabs" aria-label="الانتقال للأدوات"><a href="#fuel-use">حساب استهلاك الوقود</a><a href="#maintenance-cost">تقدير فاتورة الصيانة</a><a href="https://a3tal.com/car-tires-prices-egypt-2026/">فهم مقاسات الكاوتش</a></nav>
    <section class="a3rt-grid" aria-label="الحاسبات">
      <article id="fuel-use" class="a3rt-panel" aria-labelledby="fuel-title">
        <span class="a3rt-count">01 / استهلاك الوقود</span>
        <h2 id="fuel-title">العربية بتصرف كام لتر لكل 100 كم؟</h2>
        <p>املأ التانك أو قِس الوقود المستهلك والمسافة المقطوعة في الفترة نفسها. النتيجة تعتمد على أرقامك، مش استهلاك رسمي متخيَّل لموديل معين.</p>
        <form id="a3rt-fuel-form" class="a3rt-form">
          <label for="a3rt-litres">كم لتر بنزين استهلكت؟<input id="a3rt-litres" name="litres" required type="number" inputmode="decimal" min="0.01" step="any" placeholder="مثال: 25"></label>
          <label for="a3rt-distance">مشيت كام كيلومتر؟<input id="a3rt-distance" name="km" required type="number" inputmode="decimal" min="1" step="any" placeholder="مثال: 320"></label>
          <label for="a3rt-litre-price">سعر لتر البنزين الحالي (اختياري)<input id="a3rt-litre-price" name="price" type="number" inputmode="decimal" min="0" step="any" placeholder="اكتبه بنفسك"></label>
          <button type="submit">احسب الاستهلاك</button>
          <output id="a3rt-fuel-result" class="a3rt-output" role="status" aria-live="polite">النتيجة هتظهر هنا بعد الحساب.</output>
        </form>
        <p class="a3rt-note">معادلة الاستهلاك: (اللترات المستهلكة ÷ الكيلومترات) × 100. لو دخلت سعر اللتر، هنحسب تكلفة الكيلومتر أيضًا. لو فيه تسريب أو ريحة بنزين قوية، افحص السيارة بدل الاعتماد على الحساب.</p>
      </article>
      <article id="maintenance-cost" class="a3rt-panel" aria-labelledby="maintenance-title">
        <span class="a3rt-count">02 / فاتورة الورشة</span>
        <h2 id="maintenance-title">حاسبة تكلفة الصيانة</h2>
        <p>اكتب الأسعار اللي أكدتها الورشة في عرض السعر: الزيوت، القطع، المصنعية، الضريبة الفعلية وأي أعمال إضافية. مش بنفترض سعر صيانة أو ضريبة تلقائيًا.</p>
        <form id="a3rt-maint-form" class="a3rt-form">
          <label for="a3rt-fluids">زيوت وسوائل وفلاتر (جنيه)<input id="a3rt-fluids" name="fluids" type="number" min="0" step="any" inputmode="decimal" value="0"></label>
          <label for="a3rt-parts">قطع غيار أخرى (جنيه)<input id="a3rt-parts" name="parts" type="number" min="0" step="any" inputmode="decimal" value="0"></label>
          <label for="a3rt-labor">مصنعية (جنيه)<input id="a3rt-labor" name="labor" type="number" min="0" step="any" inputmode="decimal" value="0"></label>
          <label for="a3rt-vat">ضريبة مذكورة في عرض الورشة (جنيه)<input id="a3rt-vat" name="tax" type="number" min="0" step="any" inputmode="decimal" value="0"></label>
          <label for="a3rt-extra">أعمال إضافية معتمدة (جنيه)<input id="a3rt-extra" name="extra" type="number" min="0" step="any" inputmode="decimal" value="0"></label>
          <button type="submit">احسب إجمالي الفاتورة</button>
          <output id="a3rt-maint-result" class="a3rt-output" role="status" aria-live="polite">الإجمالي هيتحسب من البنود اللي تدخلها.</output>
        </form>
        <p class="a3rt-note">الحساب للمقارنة بين عروض الورش فقط، ولا يمثل سعرًا رسميًا من الوكيل. <a href="<?php echo esc_url(home_url('/maintenance-schedules/')); ?>">اعرف جدول الصيانة حسب موديلك</a> و<a href="<?php echo esc_url(home_url('/parts/')); ?>">راجع دليل قطع الغيار</a>.</p>
      </article>
    </section>
    <section class="a3rt-next" aria-labelledby="a3rt-next-title">
      <h2 id="a3rt-next-title">محتاج بيانات سيارتك قبل الحساب؟</h2>
      <p>افتح <a href="<?php echo esc_url(home_url('/cars/')); ?>">دليل أسعار وموديلات السيارات</a> أو <a href="<?php echo esc_url(home_url('/car-reference/')); ?>">المواصفات الفنية</a> أو <a href="<?php echo esc_url(home_url('/dtc/')); ?>">مكتبة أكواد الأعطال</a>. لا تنقل سعة زيت أو سعر صيانة من موديل مختلف.</p>
    </section>
  </div>
</main>
<style>
.a3rt{background:#f3f7fc;color:#142f49;padding:28px 0 65px;font-family:"IBM Plex Sans Arabic",Tahoma,sans-serif}
.a3rt *{box-sizing:border-box}.a3rt-wrap{width:min(1180px,calc(100% - 32px));margin:auto}
.a3rt a{color:#11639b}.a3rt-crumb{font-size:14px;margin-bottom:18px}.a3rt-crumb a{text-decoration:none}
.a3rt-hero{background:linear-gradient(135deg,#0c2944,#16456d);color:#fff;padding:33px 36px;border-radius:20px}
.a3rt-kicker,.a3rt-count{font-size:12px;font-weight:750;letter-spacing:.04em;color:#3e9dd8}
.a3rt-hero .a3rt-kicker{color:#92d8fb}
.a3rt-hero h1{font-size:clamp(25px,3vw,38px);margin:8px 0 10px;line-height:1.45;color:#fff}
.a3rt-hero p{margin:0;line-height:1.9;color:#e4eff8}
.a3rt-tabs{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}
.a3rt-tabs a{display:inline-flex;align-items:center;background:#fff;border:1px solid #dae5ef;padding:10px 15px;border-radius:11px;text-decoration:none;font-size:14px;font-weight:700}
.a3rt-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;align-items:start}
.a3rt-panel{background:#fff;padding:26px;border-radius:18px;border:1px solid #dae5ef;box-shadow:0 8px 26px #1131540c;scroll-margin-top:90px}
.a3rt-panel h2{font-size:23px;margin:10px 0;color:#122c48;line-height:1.5}.a3rt-panel p{line-height:1.85}
.a3rt-form{display:grid;gap:13px;margin-top:18px}
.a3rt-form label{display:grid;gap:7px;font-weight:650;font-size:14px}
.a3rt-form input{display:block;width:100%;border:1px solid #b7cbe0;border-radius:10px;background:#fff;padding:12px 13px;color:#152d43;font:inherit;font-size:16px}
.a3rt-form button{cursor:pointer;background:#125f98;color:#fff;border:0;border-radius:10px;padding:13px 18px;font:inherit;font-weight:800;font-size:15px}
.a3rt-form button:hover{background:#0c476f}
.a3rt-form input:focus-visible,.a3rt a:focus-visible,.a3rt button:focus-visible{outline:3px solid #6abbea;outline-offset:3px}
.a3rt-output{display:block;min-height:60px;background:#eff7fd;border:1px solid #cce1f1;border-radius:11px;padding:14px 16px;font-weight:750;line-height:1.8;color:#114269}
.a3rt-note{font-size:13px;color:#536c81;background:#f7fafc;border-radius:10px;padding:10px 12px}
.a3rt-next{margin-top:22px;background:#fff;border:1px solid #dae5ef;border-radius:16px;padding:20px}
.a3rt-next h2{font-size:20px;margin:0 0 6px}.a3rt-next p{line-height:1.8;margin:0}
@media(max-width:780px){.a3rt-grid{grid-template-columns:minmax(0,1fr)}.a3rt-hero{padding:24px 20px}.a3rt-panel{padding:20px}.a3rt-panel h2{font-size:21px}.a3rt-tabs a{flex:1;justify-content:center;min-width:130px}}
</style>
<script>
(function(){
'use strict';
var nf=new Intl.NumberFormat('ar-EG',{maximumFractionDigits:2});
function val(id,optional){
 var el=document.getElementById(id),raw=el.value.trim();
 if(optional&&raw==='')return 0;
 var n=Number(raw);return Number.isFinite(n)&&n>=0?n:NaN;
}
function render(out,message){out.textContent=message;}
var fuel=document.getElementById('a3rt-fuel-form');
fuel.addEventListener('submit',function(event){
 event.preventDefault();
 var litres=val('a3rt-litres',false),distance=val('a3rt-distance',false),price=val('a3rt-litre-price',true);
 var out=document.getElementById('a3rt-fuel-result');
 if(!(litres>0&&distance>0)||!Number.isFinite(price)){render(out,'من فضلك أدخل كمية وقود ومسافة صحيحتين، وسعرًا غير سالب إذا حددته.');return;}
 var per100=litres/distance*100,perlitre=distance/litres;
 var message='استهلاكك الفعلي: '+nf.format(per100)+' لتر/100 كم؛ و'+nf.format(perlitre)+' كم لكل لتر.';
 if(price>0)message+=' التكلفة المحسوبة: '+nf.format(litres*price/distance)+' جنيه/كم.';
 render(out,message);
});
var maint=document.getElementById('a3rt-maint-form');
maint.addEventListener('submit',function(event){
 event.preventDefault();
 var ids=['a3rt-fluids','a3rt-parts','a3rt-labor','a3rt-vat','a3rt-extra'];
 var items=ids.map(id=>val(id,true)),out=document.getElementById('a3rt-maint-result');
 if(items.some(x=>!Number.isFinite(x))){render(out,'راجع البنود: كل مبلغ لازم يكون رقمًا صفرًا أو أكبر.');return;}
 var total=items.reduce((a,b)=>a+b,0);
 render(out,'إجمالي البنود المُدخلة: '+nf.format(total)+' جنيه مصري. هذا تقدير من أرقامك، مش عرض سعر ملزم.');
});
})();
</script>
<?php get_footer(); ?>
