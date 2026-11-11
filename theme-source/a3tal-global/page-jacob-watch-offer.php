<?php
/**
 * Template Name: Luxury Watch Offer
 * Template Post Type: page
 * A3tal isolated luxury watch landing page - November 2026
 */
defined('ABSPATH') || exit;
$gallery = get_post_meta(get_the_ID(), '_a3tal_watch_gallery', true);
$gallery = is_array($gallery) ? $gallery : [];
$steel = esc_url((string) ($gallery['steel'] ?? ''));
$gold  = esc_url((string) ($gallery['gold'] ?? ''));
$box   = esc_url((string) ($gallery['box'] ?? ''));
$whatsapp = 'https://wa.me/201025036151?text=' . rawurlencode('مرحبًا، أرغب في حجز الساعة الفضية من عرض 24,000 جنيه، وأريد تأكيد التوفر والتفاصيل.');
?>
<!doctype html>
<html <?php language_attributes(); ?> dir="rtl">
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0e0e0f">
<?php wp_head(); ?>
<style id="jw-luxury-page">
:root{--jw-bg:#080909;--jw-surface:#121314;--jw-stroke:rgba(223,187,108,.28);--jw-gold:#deb66b;--jw-gold-light:#ffe0a0;--jw-text:#f5f1e7;--jw-muted:#c9c1b3}
html{scroll-behavior:smooth}
body{margin:0!important;background:var(--jw-bg)!important;color:var(--jw-text)!important;font-family:Tahoma,Arial,sans-serif!important;overflow-x:hidden}
body.admin-bar .jw-nav{top:32px}
.jw *, .jw *:before,.jw *:after{box-sizing:border-box}
.jw{direction:rtl;background:#090a0a;color:#f6f1e9;line-height:1.7;overflow:hidden;min-height:100vh;isolation:isolate}
.jw a{text-decoration:none}
.jw button,.jw a{touch-action:manipulation}
.jw button:focus-visible,.jw a:focus-visible{outline:3px solid #fff2c5;outline-offset:4px}
.jw-shell{width:min(1200px,calc(100% - 44px));margin:auto}
.jw-nav{height:80px;display:flex;align-items:center;gap:30px;justify-content:space-between;border-bottom:1px solid var(--jw-stroke);position:relative;z-index:20;background:#0c0c0d}
.jw-wordmark{display:flex;align-items:center;gap:12px;color:#f8ddb0;font-size:19px;font-family:Georgia,'Times New Roman',serif;font-weight:700;letter-spacing:1.1px;white-space:nowrap}
.jw-mark{border:1px solid #bb8c40;border-radius:50%;width:38px;height:38px;display:grid;place-items:center;color:#f7dca5;font-size:23px;font-family:Georgia,serif}
.jw-menu{display:flex;align-items:center;gap:26px;font-size:13px}
.jw-menu a{color:#dfd5c5;font-weight:600}
.jw-menu a:hover{color:var(--jw-gold-light)}
.jw-nav-cta{border:1px solid var(--jw-stroke);color:#f2d7a4;padding:10px 18px;border-radius:5px;font-size:13px;font-weight:bold}
.jw-eyebrow{color:#e0bc78;letter-spacing:2px;font-size:12px;font-weight:bold;display:block;margin-bottom:14px}
.jw-hero{background:radial-gradient(circle at 73% 16%,rgba(136,89,31,.18),transparent 38%),radial-gradient(circle at 12% 55%,rgba(157,116,48,.11),transparent 35%),#090a0b;border-bottom:1px solid #302717}
.jw-hero-grid{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:46px;min-height:640px;padding:54px 0 65px}
.jw h1,.jw h2,.jw h3,.jw p{margin-top:0}
.jw h1{font-family:Georgia,Tahoma,serif;color:#ffe0a0;font-size:clamp(36px,4vw,62px);line-height:1.28;margin-bottom:20px;letter-spacing:-1px}
.jw h1 span{display:block;font-family:Tahoma,Arial,sans-serif;color:#eee7dc;font-size:clamp(20px,2.1vw,28px);font-weight:400;margin-top:10px}
.jw-lead{font-size:17px;line-height:1.95;color:#cbbfae;max-width:560px}
.jw-sale{display:flex;align-items:center;gap:20px;flex-wrap:wrap;margin:26px 0 16px}
.jw-price{font-size:clamp(38px,4.1vw,60px);line-height:1.1;font-weight:900;color:#ffe0a0;font-family:Tahoma,Arial,sans-serif;white-space:nowrap}
.jw-price small{font-size:18px;color:#e0c89a;font-weight:400}
.jw-promo{display:inline-flex;align-items:center;gap:8px;color:#0b0b0c;background:linear-gradient(125deg,#f8dfa5,#c69b4e);border-radius:24px;padding:7px 14px;font-size:13px;font-weight:bold}
.jw-stock{border:1px solid #7c493f;color:#ffc8ae;background:linear-gradient(100deg,#3b1712,#1a1010);padding:11px 16px;border-radius:9px;display:inline-flex;align-items:center;gap:10px;font-weight:800;margin:4px 0 18px}
.jw-stock:before{content:"";width:8px;height:8px;background:#ef6d5b;border-radius:50%;box-shadow:0 0 0 5px #eb6b5726}
.jw-variants{display:flex;flex-wrap:wrap;gap:10px;margin:7px 0 22px}
.jw-variant{background:#161616;border:1px solid #4d4233;color:#e1d9c7;border-radius:10px;padding:12px 18px;cursor:pointer;font:700 14px Tahoma,Arial;transition:.2s}
.jw-variant[aria-pressed="true"]{border-color:#e5bd74;background:#302413;color:#ffe6b0;box-shadow:0 0 0 1px #d6ab5e inset}
.jw-buttons{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0 22px}
.jw-btn{display:inline-flex;align-items:center;justify-content:center;text-align:center;gap:8px;min-height:53px;padding:12px 23px;border-radius:9px;font-size:16px;font-weight:900;transition:transform .2s,filter .2s}
.jw-btn:hover{transform:translateY(-2px);filter:brightness(1.09)}
.jw-btn-primary{background:linear-gradient(115deg,#f8df9f,#b88637);color:#12100b!important;box-shadow:0 12px 32px #a47b2726}
.jw-btn-outline{border:1px solid #b89458;color:#f4d7a1!important;background:#13100c}
.jw-underbtn{color:#bfb7aa;font-size:12px;line-height:1.8;max-width:490px}
.jw-visual{position:relative;min-width:0}
.jw-main-image{position:relative;aspect-ratio:1/1;overflow:hidden;display:grid;place-items:center;border-radius:22px;background:radial-gradient(circle at 50% 40%,#403322 0%,#191612 45%,#070707 90%);border:1px solid #77603a;box-shadow:0 38px 95px #000a,0 0 0 11px #15120e}
.jw-main-image:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,#edc88318,transparent 40%,#0005);z-index:1;pointer-events:none}
.jw-main-image img{width:100%;height:100%;object-fit:cover;display:block;filter:contrast(1.08) saturate(1.07);transition:opacity .15s,transform .3s}
.jw-main-image img:hover{transform:scale(1.035)}
.jw-image-label{position:absolute;z-index:2;bottom:17px;right:18px;background:#0b0b0bd9;color:#ffe1aa;padding:7px 12px;border:1px solid #ab8544;border-radius:30px;font-size:12px}
.jw-mini-pics{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:24px}
.jw-mini-pics button{appearance:none;border:1px solid #55452c;border-radius:12px;padding:0;overflow:hidden;background:#181716;cursor:pointer;aspect-ratio:1;position:relative}
.jw-mini-pics button:focus,.jw-mini-pics button:hover{border-color:#ebc786}
.jw-mini-pics img{width:100%;height:100%;object-fit:cover;display:block}
.jw-mini-pics span{position:absolute;bottom:0;right:0;left:0;background:#0009;color:white;font-size:11px;text-align:center}
.jw-reassure{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-bottom:1px solid #282521;background:#101010}
.jw-reassure div{padding:23px 10px;text-align:center;border-left:1px solid #393025;font-size:13px;color:#e4dac8}
.jw-reassure div:last-child{border-left:0}
.jw-reassure strong{display:block;color:#f5d493;font-size:15px;margin-bottom:3px}
.jw-section{padding:76px 0}
.jw-heading{text-align:center;margin-bottom:35px}
.jw-heading .jw-eyebrow{margin-bottom:8px}
.jw h2{font-family:Georgia,Tahoma,serif;color:#f3d08c;font-size:clamp(27px,3vw,39px);line-height:1.4}
.jw-heading p{color:#c3b9a8;font-size:15px}
.jw-features{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.jw-feature{border:1px solid #4b3a25;background:linear-gradient(160deg,#1b1b19,#101010);border-radius:14px;padding:28px 22px;min-height:180px}
.jw-feature-num{color:#b98f4a;font-family:Georgia,serif;font-size:26px;display:block;margin-bottom:14px}
.jw-feature h3{color:#f4d59e;font-size:18px;margin-bottom:9px}
.jw-feature p{color:#bdb7ab;font-size:13px;line-height:1.9;margin:0}
.jw-gallery{background:radial-gradient(circle at 12% 15%,#3c291655,transparent 32%),#0f1010;border-block:1px solid #3b2c1d}
.jw-gallery-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.jw-gallery-card{overflow:hidden;border:1px solid #463b29;border-radius:13px;background:#171717}
.jw-gallery-card img{aspect-ratio:1;object-fit:cover;width:100%;display:block}
.jw-gallery-card .jw-caption{padding:15px 18px;color:#ead29e;font-weight:700;font-size:14px}
.jw-detail-layout{display:grid;grid-template-columns:1.05fr .95fr;gap:50px;align-items:center}
.jw-detail-layout img{width:100%;border-radius:18px;border:1px solid #544028}
.jw-specs{width:100%;border-collapse:collapse;font-size:14px}
.jw-specs th,.jw-specs td{padding:17px 13px;border-bottom:1px solid #3c3326;vertical-align:top}
.jw-specs th{color:#e8bf78;width:36%;font-weight:700;text-align:right}
.jw-specs td{color:#d3c9b8}
.jw-detail-footnote{font-size:12px;color:#a7a096;line-height:1.9;margin-top:18px}
.jw-scarcity{background:linear-gradient(130deg,#17100b,#281909,#100d0c);border-block:1px solid #735b2f;text-align:center;padding:48px 20px}
.jw-scarcity h2{font-size:clamp(27px,3.4vw,46px);margin-bottom:4px}
.jw-qty{font-size:clamp(34px,5vw,66px);color:#ffe4ac;font-weight:900}
.jw-scarcity p{color:#c9b8a0;margin:0 0 26px}
.jw-faq-grid{max-width:850px;margin:auto}
.jw details{background:#141514;border:1px solid #393122;border-radius:11px;margin-bottom:11px;padding:3px 20px}
.jw summary{cursor:pointer;padding:18px 0;font-weight:700;color:#f0dec0;font-size:15px}
.jw details p{color:#bdb6ab;font-size:14px;padding-bottom:15px;margin:0}
.jw-bottom{padding:72px 0 94px;text-align:center;background:radial-gradient(circle at 50% 0%,#4b361b55,transparent 58%),#0c0d0d}
.jw-bottom .jw-price{margin:14px 0}
.jw-bottom p{color:#cbc4b7}
.jw-bottom .jw-buttons{justify-content:center}
.jw-disclaimer{font-size:12px;color:#a79b85;border-top:1px solid #28231a;padding-top:24px;margin-top:32px;max-width:800px;margin-inline:auto}
.jw-bottom-footer{border-top:1px solid #2b261e;padding:24px 0 85px;display:flex;justify-content:space-between;gap:15px;font-size:12px;color:#a89d8c}
.jw-bottom-footer a{color:#bba47a}
.jw-sticky{display:none}
@media(max-width:980px){.jw-hero-grid{gap:28px;min-height:auto}.jw-features{grid-template-columns:repeat(2,1fr)}.jw h1{font-size:40px}.jw-detail-layout{gap:30px}}
@media(max-width:720px){
body.admin-bar .jw-nav{top:46px}.jw-shell{width:min(100% - 28px,560px)}.jw-nav{height:64px}.jw-wordmark{font-size:15px}.jw-mark{width:33px;height:33px;font-size:19px}.jw-menu{display:none}.jw-nav-cta{font-size:12px;padding:9px 12px}
.jw-hero-grid{grid-template-columns:1fr;padding:35px 0 45px;gap:33px}.jw-hero-copy{order:2}.jw-visual{order:1;max-width:550px;width:100%;margin:auto}.jw h1{font-size:34px;margin-bottom:13px}.jw h1 span{font-size:21px}.jw-lead{font-size:14px}
.jw-main-image{box-shadow:0 20px 40px #0008,0 0 0 4px #15110d;border-radius:16px}.jw-mini-pics{margin-top:13px;gap:8px}
.jw-sale{gap:10px}.jw-price{font-size:40px}.jw-btn{width:100%;font-size:15px}.jw-stock{font-size:13px}
.jw-reassure{grid-template-columns:1fr 1fr}.jw-reassure div{border-bottom:1px solid #342b20}.jw-reassure div:last-child{grid-column:span 2}
.jw-section{padding:54px 0}.jw-features{gap:10px}.jw-feature{min-height:146px;padding:18px 14px}.jw-feature h3{font-size:15px}.jw-feature p{font-size:12px}.jw-feature-num{font-size:22px;margin-bottom:7px}
.jw-gallery-grid{grid-template-columns:1fr 1fr;gap:10px}.jw-gallery-card .jw-caption{font-size:12px;padding:10px 12px}.jw-gallery-card:last-child{grid-column:span 2;max-width:340px;margin:auto;width:100%}
.jw-detail-layout{grid-template-columns:1fr;gap:27px}.jw-detail-layout img{max-width:480px;margin:auto}
.jw-specs th,.jw-specs td{padding:13px 8px;font-size:12px}.jw-bottom-footer{display:block;text-align:center;padding-bottom:105px}
.jw-bottom{padding:55px 0 35px}.jw-sticky{position:fixed;display:flex;align-items:center;justify-content:space-between;gap:11px;bottom:0;left:0;right:0;padding:10px 14px max(10px,env(safe-area-inset-bottom));z-index:999999;background:#0b0b0bef;border-top:1px solid #be9754;backdrop-filter:blur(14px);box-shadow:0 -8px 35px #0009}.jw-sticky .jw-btn{width:auto;min-height:43px;padding:7px 14px;font-size:13px}.jw-sticky .jw-sticky-price{font-size:20px;color:#fce0a6;font-weight:900;white-space:nowrap}.jw-sticky .jw-sticky-price small{font-size:10px;display:block;color:#d7c7ab;font-weight:400}
}
@media(prefers-reduced-motion:reduce){.jw *, .jw *:before,.jw *:after{scroll-behavior:auto!important;transition:none!important}}
</style>
</head>
<body <?php body_class('a3tal-watch-landing'); ?>>
<?php if (function_exists('wp_body_open')) wp_body_open(); ?>
<div class="jw" id="top">
<header class="jw-nav jw-shell" aria-label="القائمة الرئيسية للعرض">
  <a class="jw-wordmark" href="#top"><span class="jw-mark">W</span><span>WATCH COLLECTION</span></a>
  <nav class="jw-menu" aria-label="روابط الصفحة"><a href="#collection">المجموعة</a><a href="#details">المواصفات</a><a href="#questions">الأسئلة</a><a href="#reserve">الحجز</a></nav>
  <a class="jw-nav-cta" href="#reserve">احجز ساعتك</a>
</header>
<main>
<section class="jw-hero" aria-labelledby="watch-title">
<div class="jw-shell jw-hero-grid">
  <div class="jw-hero-copy">
    <span class="jw-eyebrow">PRIVATE COLLECTION / LIMITED OFFER</span>
    <h1 id="watch-title">ساعة تخطف الأنظار <span>تصميم مستوحى من Jacob &amp; Co</span></h1>
    <p class="jw-lead">تفاصيل لافتة من أول نظرة، واجهة بتصميم مكشوف، وحزام أسود أنيق. اختار اللمسة الفضية أو الذهبية الوردية، واستلمها مع علبة العرض الخشبية الفاخرة الظاهرة بالصور.</p>
    <div class="jw-sale"><span class="jw-price">24,000 <small>جنيه مصري</small></span><span class="jw-promo">عرض سعر خاص</span></div>
    <div class="jw-stock">المتاح من المجموعة بالكامل: 6 قطع فقط</div>
    <p style="font-size:13px;color:#d7c9b4;margin-bottom:8px">اختار التصميم المفضل:</p>
    <div class="jw-variants" role="group" aria-label="اختيار شكل الساعة">
      <button class="jw-variant" type="button" data-watch-variant="steel" aria-pressed="true">الفضي الأسود</button>
      <button class="jw-variant" type="button" data-watch-variant="gold" aria-pressed="false">الذهبي الوردي</button>
    </div>
    <div class="jw-buttons">
      <a class="jw-btn jw-btn-primary" data-watch-whatsapp href="<?php echo esc_url($whatsapp); ?>" target="_blank" rel="noopener noreferrer">احجز ساعتك الآن</a>
      <a class="jw-btn jw-btn-outline" href="tel:+201025036151" dir="ltr">01025036151</a>
    </div>
    <p class="jw-underbtn">الحجز والاستفسارات عبر واتساب أو الاتصال المباشر. يجرى تأكيد اللون والتوفر عند التواصل.</p>
  </div>
  <div class="jw-visual">
    <div class="jw-main-image">
      <?php if ($steel) : ?><img id="jw-current-watch" src="<?php echo $steel; ?>" alt="الساعة الفضية الفعلية من تصوير المنتج" width="760" height="760" fetchpriority="high"><?php endif; ?>
      <span class="jw-image-label" id="jw-current-label">التصميم الفضي</span>
    </div>
    <div class="jw-mini-pics">
      <button type="button" data-watch-variant="steel" aria-label="اعرض الساعة الفضية"><img src="<?php echo $steel; ?>" alt="لقطة حقيقية للساعة الفضية" width="400" height="400"></button>
      <button type="button" data-watch-variant="gold" aria-label="اعرض الساعة الذهبية"><img src="<?php echo $gold; ?>" alt="لقطة حقيقية للساعة الذهبية الوردية" width="400" height="400"></button>
      <button type="button" id="jw-show-box" aria-label="اعرض صورة علبة الساعة"><img src="<?php echo $box; ?>" alt="علبة العرض الخشبية مع الساعة" width="400" height="400"></button>
    </div>
  </div>
</div>
</section>
<div class="jw-reassure"><div><strong>صورة المنتج الفعلي</strong> من اللقطات المقدمة للساعة</div><div><strong>علبة عرض خشبية</strong> تصميم أنيق للتقديم والحفظ</div><div><strong>حجز مباشر</strong> واتساب واتصال على نفس الرقم</div></div>
<section class="jw-section" id="why">
 <div class="jw-shell">
  <div class="jw-heading"><span class="jw-eyebrow">THE DETAILS MATTER</span><h2>ليه الساعة دي مختلفة؟</h2><p>التفاصيل الصغيرة هي اللي بتعمل الانطباع الكبير.</p></div>
  <div class="jw-features">
   <article class="jw-feature"><span class="jw-feature-num">01</span><h3>واجهة استثنائية</h3><p>تكوين بصري مكشوف بتفاصيل دقيقة تلفت النظر من كل زاوية.</p></article>
   <article class="jw-feature"><span class="jw-feature-num">02</span><h3>اختيارين مميزين</h3><p>شكل فضي وأسود أو تشطيب ذهبي وردي بحسب ذوقك.</p></article>
   <article class="jw-feature"><span class="jw-feature-num">03</span><h3>سوار أسود كلاسيكي</h3><p>نقشة جلدية أنيقة تكمل الإطلالة من غير مبالغة.</p></article>
   <article class="jw-feature"><span class="jw-feature-num">04</span><h3>بوكس فاخر</h3><p>علبة طويلة بتشطيب خشبي ولوحة معدنية ظاهرة في صور المنتج.</p></article>
  </div>
 </div>
</section>
<section class="jw-section jw-gallery" id="collection">
 <div class="jw-shell">
  <div class="jw-heading"><span class="jw-eyebrow">REAL PRODUCT GALLERY</span><h2>المجموعة على الطبيعة</h2><p>صور مقتطفة من الفيديوهات الفعلية وصورة العلبة المرفقة.</p></div>
  <div class="jw-gallery-grid">
   <figure class="jw-gallery-card"><img src="<?php echo $steel; ?>" loading="lazy" decoding="async" alt="تصميم الساعة الفضية من الفيديو" width="760" height="760"><figcaption class="jw-caption">تصميم فضي بتفاصيل سوداء وذهبية</figcaption></figure>
   <figure class="jw-gallery-card"><img src="<?php echo $gold; ?>" loading="lazy" decoding="async" alt="تصميم الساعة الذهبية الوردية من الفيديو" width="760" height="760"><figcaption class="jw-caption">تصميم ذهبي وردي وسوار أسود</figcaption></figure>
   <figure class="jw-gallery-card"><img src="<?php echo $box; ?>" loading="lazy" decoding="async" alt="صورة البوكس الخشبي الفعلي" width="760" height="760"><figcaption class="jw-caption">علبة العرض الخشبية</figcaption></figure>
  </div>
 </div>
</section>
<section class="jw-section" id="details">
 <div class="jw-shell jw-detail-layout">
  <div><span class="jw-eyebrow">PRODUCT DETAILS</span><h2>تفاصيل العرض</h2>
   <table class="jw-specs"><tbody>
    <tr><th scope="row">النوع</th><td>ساعة هاي كوبي بتصميم مستوحى من ساعات Jacob &amp; Co</td></tr>
    <tr><th scope="row">الألوان الظاهرة</th><td>فضي وأسود، أو ذهبي وردي وأسود</td></tr>
    <tr><th scope="row">واجهة الساعة</th><td>تصميم زخرفي مكشوف مع تفاصيل متعددة</td></tr>
    <tr><th scope="row">السوار</th><td>أسود بتصميم جلدي ونقشة كلاسيكية</td></tr>
    <tr><th scope="row">العلبة</th><td>بوكس عرض خشبي داكن بلوحة معدنية</td></tr>
    <tr><th scope="row">السعر</th><td>24,000 جنيه مصري للقطعة</td></tr>
    <tr><th scope="row">المخزون المتاح</th><td>6 قطع إجمالًا وقت نشر العرض</td></tr>
   </tbody></table>
   <p class="jw-detail-footnote">الصور توضح الشكل الخارجي للقطعة المعروضة. نوع الحركة وخصائص مقاومة الماء والضمان لا تُعد مؤكدة قبل الاستفسار عن تفاصيل النسخة المتوفرة.</p>
  </div>
  <div><img src="<?php echo $box; ?>" alt="صندوق الساعة الخشبي المصور مع المنتج" loading="lazy" decoding="async" width="760" height="760"></div>
 </div>
</section>
<section class="jw-scarcity" id="reserve"><div class="jw-shell">
 <span class="jw-eyebrow">LIMITED STOCK</span><h2>العدد المتاح محدود فعلًا</h2><div class="jw-qty">6 قطع فقط</div><p>السعر الخاص 24,000 جنيه. تأكد من توافر التصميم المفضل وقت الحجز.</p>
 <div class="jw-buttons" style="justify-content:center"><a data-watch-whatsapp class="jw-btn jw-btn-primary" href="<?php echo esc_url($whatsapp); ?>" target="_blank" rel="noopener noreferrer">احجز عبر واتساب</a><a class="jw-btn jw-btn-outline" href="tel:+201025036151" dir="ltr">01025036151</a></div>
</div></section>
<section class="jw-section" id="questions"><div class="jw-shell">
 <div class="jw-heading"><h2>الأسئلة اللي تهمك قبل الحجز</h2></div>
 <div class="jw-faq-grid">
  <details><summary>هل الساعة أصلية من Jacob &amp; Co؟</summary><p>لا. المعروض نسخة هاي كوبي بتصميم مستوحى من ساعات Jacob &amp; Co، وليست منتجًا أصليًا أو معتمدًا من الشركة.</p></details>
  <details><summary>هل متاح الفضي والذهبي؟</summary><p>الصور المعروضة توضح التصميمين. تأكيد توافر كل لون يتم عبر واتساب أو الهاتف قبل الحجز.</p></details>
  <details><summary>هل البوكس ضمن العرض؟</summary><p>الصورة المعروضة لعلبة التقديم الخشبية التي تم إرسالها مع صور المنتج. يرجى تأكيد محتويات القطعة المحجوزة وقت التواصل.</p></details>
  <details><summary>إزاي أحجز الساعة؟</summary><p>اضغط على زر واتساب وسيتم تجهيز رسالة بالتفاصيل واللون المختار، أو اتصل على 01025036151.</p></details>
 </div>
</div></section>
<section class="jw-bottom"><div class="jw-shell">
 <span class="jw-eyebrow">YOUR NEXT STATEMENT PIECE</span><h2>اختار التصميم اللي يشبهك</h2><div class="jw-price">24,000 <small>جنيه مصري</small></div>
 <p>سعر خاص، والعدد المتاح من المجموعة بالكامل 6 قطع فقط.</p>
 <div class="jw-buttons"><a data-watch-whatsapp class="jw-btn jw-btn-primary" href="<?php echo esc_url($whatsapp); ?>" target="_blank" rel="noopener noreferrer">احجز دلوقتي عبر واتساب</a><a class="jw-btn jw-btn-outline" href="tel:+201025036151">اتصل للاستفسار</a></div>
 <p class="jw-disclaimer">هذه صفحة عرض لنسخ ساعات هاي كوبي مستوحاة من تصاميم Jacob &amp; Co، وليست تابعة للعلامة التجارية أو موزعًا رسميًا لها. يتم تأكيد المواصفات النهائية والضمان والشحن عند الحجز.</p>
</div></section>
</main>
<footer class="jw-bottom-footer jw-shell"><span>عرض ساعات مستقل عبر أعطال.كوم</span><a href="https://a3tal.com/">العودة إلى أعطال.كوم</a></footer>
<div class="jw-sticky"><span class="jw-sticky-price">24,000 ج.م<small>6 قطع متاحة إجمالًا</small></span><a data-watch-whatsapp class="jw-btn jw-btn-primary" href="<?php echo esc_url($whatsapp); ?>" target="_blank" rel="noopener noreferrer">احجز واتساب</a></div>
</div>
<script id="jw-actions">
(function(){
'use strict';
var images={steel:<?php echo wp_json_encode($steel); ?>,gold:<?php echo wp_json_encode($gold); ?>,box:<?php echo wp_json_encode($box); ?>};
var img=document.getElementById('jw-current-watch'),label=document.getElementById('jw-current-label'),choice='steel';
function waLink(name){return 'https://wa.me/201025036151?text='+encodeURIComponent('مرحبًا، أريد حجز ساعة '+(name==='gold'?'التصميم الذهبي الوردي':'التصميم الفضي')+' بسعر 24,000 جنيه من العرض محدود الكمية، برجاء تأكيد التوفر والتفاصيل.');}
function select(name){if(!images[name]||!img)return;if(name==='steel'||name==='gold')choice=name;img.src=images[name];img.alt=name==='box'?'صورة علبة الساعة الخشبية':('صورة المنتج الفعلي، التصميم '+(name==='gold'?'الذهبي الوردي':'الفضي'));label.textContent=name==='box'?'علبة الساعة':(name==='gold'?'التصميم الذهبي الوردي':'التصميم الفضي');document.querySelectorAll('[data-watch-variant]').forEach(function(b){if(b.classList.contains('jw-variant'))b.setAttribute('aria-pressed',String(b.dataset.watchVariant===choice));});document.querySelectorAll('[data-watch-whatsapp]').forEach(function(a){a.href=waLink(choice);});}
document.querySelectorAll('[data-watch-variant]').forEach(function(b){b.addEventListener('click',function(){select(b.dataset.watchVariant);});});
var bx=document.getElementById('jw-show-box');if(bx)bx.addEventListener('click',function(){select('box');});select('steel');
})();
</script>
<?php wp_footer(); ?>
</body></html>