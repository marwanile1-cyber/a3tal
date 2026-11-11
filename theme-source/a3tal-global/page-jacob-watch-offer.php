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
$hero  = esc_url((string) ($gallery['hero'] ?? ''));
$videos = [
  'steel' => 'https://raw.githubusercontent.com/marwanile1-cyber/a3tal/main/assets/watch-offer/watch-steel-real-video.mp4',
  'gold' => 'https://raw.githubusercontent.com/marwanile1-cyber/a3tal/main/assets/watch-offer/watch-rose-gold-real-video.mp4',
  'box' => 'https://raw.githubusercontent.com/marwanile1-cyber/a3tal/main/assets/watch-offer/watch-box-real-video.mp4',
];
$product_schema = [
  '@context' => 'https://schema.org',
  '@graph' => [
    [
      '@type' => 'Product',
      '@id' => get_permalink() . '#watch-offer',
      'name' => 'ساعة جاكوب اند كو هاي كوبي في مصر - تصميم مستوحى من Oil Pump وOpera Godfather',
      'description' => 'عرض ساعة هاي كوبي مستوحاة من تصميمات Jacob & Co، وليست ساعة أصلية من العلامة. تصميمان فضي وذهبي وردي، بسعر 24000 جنيه للقطعة، مع ست قطع فقط متاحة من المجموعة عند نشر العرض.',
      'url' => get_permalink(),
      'image' => array_values(array_filter([$hero, $steel, $gold, $box])),
      'category' => 'Wristwatch inspired-design replica',
      'offers' => [
        '@type' => 'Offer',
        'url' => get_permalink(),
        'priceCurrency' => 'EGP',
        'price' => '24000',
        'availability' => 'https://schema.org/LimitedAvailability',
        'inventoryLevel' => ['@type' => 'QuantitativeValue', 'value' => 6],
      ],
    ],
    [
      '@type' => 'VideoObject',
      'name' => 'معاينة فعلية للساعة الفضية بتصميم Oil Pump',
      'description' => 'فيديو حقيقي للقطعة الفضية المعروضة وليس فيديو للساعة الأصلية.',
      'thumbnailUrl' => [$steel],
      'uploadDate' => '2026-11-11T21:00:00+02:00',
      'duration' => 'PT19S',
      'contentUrl' => $videos['steel'],
      'embedUrl' => get_permalink() . '#watch-videos',
    ],
    [
      '@type' => 'VideoObject',
      'name' => 'معاينة فعلية للساعة الذهبية بتصميم Opera Godfather',
      'description' => 'فيديو حقيقي للتصميم الذهبي المعروض وليس للساعة الأصلية.',
      'thumbnailUrl' => [$gold],
      'uploadDate' => '2026-11-11T21:00:00+02:00',
      'duration' => 'PT14S',
      'contentUrl' => $videos['gold'],
      'embedUrl' => get_permalink() . '#watch-videos',
    ],
    [
      '@type' => 'VideoObject',
      'name' => 'صندوق عرض الساعة الخشبي - فيديو حقيقي',
      'description' => 'معاينة علبة الساعة الفعلية.',
      'thumbnailUrl' => [$box],
      'uploadDate' => '2026-11-11T22:00:00+02:00',
      'duration' => 'PT10S',
      'contentUrl' => $videos['box'],
      'embedUrl' => get_permalink() . '#watch-videos',
    ],
  ],
];
$whatsapp = 'https://wa.me/201025036151?text=' . rawurlencode('مرحبًا، أرغب في حجز الساعة الفضية من عرض 24,000 جنيه، وأريد تأكيد التوفر والتفاصيل.');
?>
<!doctype html>
<html <?php language_attributes(); ?> dir="rtl">
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0e0e0f">
<?php wp_head(); ?>
<script type="application/ld+json"><?php echo wp_json_encode($product_schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES); ?></script>
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


.jw-art-banner{background:#070707;padding:30px 0 26px;border-bottom:1px solid #352617}
.jw-art-banner img{width:100%;height:auto;max-height:620px;object-fit:cover;border:1px solid #66502d;border-radius:16px;display:block}
.jw-art-banner p{text-align:center;color:#aaa093;font-size:12px;margin:10px 0 0}
.jw-videos{background:#0d0e0e;border-top:1px solid #40301d;border-bottom:1px solid #40301d}
.jw-video-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.jw-video-card{background:#1a1917;border:1px solid #564026;border-radius:16px;overflow:hidden}
.jw-video-card video{display:block;width:100%;aspect-ratio:9/13;object-fit:contain;background:#000;max-height:470px}
.jw-video-card>div{padding:17px 17px 14px}
.jw-video-card h3{font-size:17px;color:#f0d49b;margin:0 0 7px}
.jw-video-card p{font-size:13px;color:#b8ad9e;margin:0}
.jw-video-note{text-align:center;color:#cbbca3;font-size:12px;margin-top:25px}
.jw-editorial{border-top:1px solid #342a19;background:linear-gradient(#121211,#0b0b0b)}
.jw-article-body{max-width:970px;margin:auto;color:#e0d9cd;font-size:15px;line-height:2.12}
.jw-article-body p{margin:0 0 20px}
.jw-article-body h2{font-size:clamp(23px,2.6vw,31px);margin:39px 0 16px;line-height:1.5}
.jw-article-body h3{color:#ebd09a;font-size:19px;margin:28px 0 12px}
.jw-article-body strong{color:#f6d99c}
.jw-article-body a{color:#f6d99c;text-decoration:underline;text-underline-offset:4px}
.jw-table-scroller{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}
.jw-compare{width:100%;border-collapse:collapse;min-width:590px;font-size:14px;line-height:1.7}
.jw-compare th,.jw-compare td{border:1px solid #4c3b24;padding:12px 14px;text-align:right}
.jw-compare thead th{background:#372915;color:#fce5b1}
.jw-compare tbody th{color:#e5c98e;background:#1c1915}
.jw-compare tbody td{background:#151514}
.jw-source-note{margin-top:28px!important;border-right:3px solid #ac8748;padding:14px 17px;background:#191711;color:#c9c0b2;font-size:12px}
@media(max-width:720px){.jw-video-grid{grid-template-columns:1fr;gap:15px;max-width:430px;margin:auto}.jw-video-card video{max-height:480px}.jw-article-body{font-size:14px;line-height:2}.jw-art-banner img{border-radius:11px}.jw-editorial .jw-heading h2{font-size:25px}}

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
    <h1 id="watch-title">ساعة جاكوب اند كو هاي كوبي في مصر <span>تصميمات مستوحاة من Oil Pump وOpera Godfather</span></h1>
    <p class="jw-lead">اكتشف ساعة هاي كوبي بتصميم هيكلي لافت مستوحى من أشهر إبداعات Jacob &amp; Co. اختار التصميم الفضي أو الذهبي الوردي، وشاهد فيديوهات المنتج الحقيقي والبوكس قبل الحجز. سعر العرض 24,000 جنيه، والكمية المتاحة 6 قطع فقط.</p>
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
      <?php if ($steel) : ?><img id="jw-current-watch" class="skip-lazy no-lazy" loading="eager" decoding="async" data-no-lazy="1" data-skip-lazy="true" src="<?php echo $steel; ?>" alt="صورة دعائية توضيحية عالية الجودة لساعة باللون الفضي مستوحاة من Oil Pump" width="760" height="760" fetchpriority="high"><?php endif; ?>
      <span class="jw-image-label" id="jw-current-label">صورة عرض فنية: التصميم الفضي</span>
    </div>
    <div class="jw-mini-pics">
      <button type="button" data-watch-variant="steel" aria-label="اعرض الساعة الفضية"><img src="<?php echo $steel; ?>" alt="تصوير دعائي توضيحي للنسخة الفضية" width="400" height="400"></button>
      <button type="button" data-watch-variant="gold" aria-label="اعرض الساعة الذهبية"><img src="<?php echo $gold; ?>" alt="تصوير دعائي توضيحي للنسخة الذهبية الوردية" width="400" height="400"></button>
      <button type="button" id="jw-show-box" aria-label="اعرض صورة علبة الساعة"><img src="<?php echo $box; ?>" alt="علبة العرض الخشبية مع الساعة" width="400" height="400"></button>
    </div>
  </div>
</div>
</section>
<div class="jw-reassure"><div><strong>صور ستوديو احترافية</strong> للتصميم مع تمييزها عن المنتج الفعلي</div><div><strong>3 فيديوهات حقيقية</strong> للساعة الفضية والذهبية والبوكس</div><div><strong>حجز مباشر</strong> عبر واتساب أو الاتصال</div></div>
<?php if ($hero) : ?>
<section class="jw-art-banner" aria-label="صورة عرض احترافية للتصميمين">
 <div class="jw-shell"><img src="<?php echo $hero; ?>" width="1536" height="1024" loading="lazy" decoding="async" alt="صورة دعائية فنية عالية الجودة تعرض تصميمي الساعة الفضي والذهبي مع صندوق عرض خشبي">
 <p>تصوير دعائي فني توضيحي للتصميمات. لمعاينة شكل القطع الحقيقية شاهد الفيديوهات الأصلية في القسم التالي.</p></div>
</section>
<?php endif; ?>
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
  <div class="jw-heading"><span class="jw-eyebrow">LUXURY WATCH GALLERY</span><h2>صور عالية الجودة للتصميمين</h2><p>صور ستوديو فنية لتوضيح الشكل العام؛ الفيديوهات التالية تصور القطع الحقيقية.</p></div>
  <div class="jw-gallery-grid">
   <figure class="jw-gallery-card"><img src="<?php echo $steel; ?>" loading="lazy" decoding="async" alt="تصميم الساعة الفضية من الفيديو" width="760" height="760"><figcaption class="jw-caption">التصميم الفضي: صورة عرض فنية توضيحية</figcaption></figure>
   <figure class="jw-gallery-card"><img src="<?php echo $gold; ?>" loading="lazy" decoding="async" alt="تصميم الساعة الذهبية الوردية من الفيديو" width="760" height="760"><figcaption class="jw-caption">الذهبي الوردي: صورة عرض فنية توضيحية</figcaption></figure>
   <figure class="jw-gallery-card"><img src="<?php echo $box; ?>" loading="lazy" decoding="async" alt="صورة البوكس الخشبي الفعلي" width="760" height="760"><figcaption class="jw-caption">علبة العرض الخشبية</figcaption></figure>
  </div>
 </div>
</section>
<section class="jw-section jw-videos" id="watch-videos" aria-labelledby="watch-videos-title">
<div class="jw-shell">
 <div class="jw-heading"><span class="jw-eyebrow">WATCH THE REAL PRODUCT</span><h2 id="watch-videos-title">شاهد الساعة الحقيقية بالفيديو</h2><p>هذه الفيديوهات الثلاثة من القطع المرسلة بالفعل، عكس صور الاستوديو التوضيحية بالأعلى.</p></div>
 <div class="jw-video-grid">
  <article class="jw-video-card"><video controls playsinline preload="metadata" poster="<?php echo $steel; ?>" aria-label="فيديو الساعة الفضية الحقيقية"><source src="<?php echo esc_url($videos['steel']); ?>" type="video/mp4">متصفحك لا يدعم عرض الفيديو.</video><div><h3>الساعة الفضية</h3><p>معاينة الواجهة والسوار والتشطيب من التصوير الأصلي للقطعة.</p></div></article>
  <article class="jw-video-card"><video controls playsinline preload="metadata" poster="<?php echo $gold; ?>" aria-label="فيديو الساعة الذهبية الوردية الحقيقية"><source src="<?php echo esc_url($videos['gold']); ?>" type="video/mp4">متصفحك لا يدعم عرض الفيديو.</video><div><h3>الساعة الذهبية الوردية</h3><p>شاهد التفاصيل والشكل على الطبيعة قبل اختيار اللون.</p></div></article>
  <article class="jw-video-card"><video controls playsinline preload="metadata" poster="<?php echo $box; ?>" aria-label="فيديو العلبة الخشبية الحقيقية"><source src="<?php echo esc_url($videos['box']); ?>" type="video/mp4">متصفحك لا يدعم عرض الفيديو.</video><div><h3>العلبة الخشبية</h3><p>فيديو من البوكس الذي تم تقديمه مع الساعة لعرض اللون والتشطيب الداخلي.</p></div></article>
 </div>
 <p class="jw-video-note">الصور الدعائية مخصصة لعرض فكرة التصميم، أما هذه المقاطع فهي المرجع المرئي للمنتج الفعلي. تأكد من مواصفات النسخة المتوفرة عند الحجز.</p>
</div>
</section>
<section class="jw-section" id="details">
 <div class="jw-shell jw-detail-layout">
  <div><span class="jw-eyebrow">PRODUCT DETAILS</span><h2>مواصفات ساعة جاكوب اند كو هاي كوبي المعروضة</h2>
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
<section class="jw-section jw-editorial" id="watch-guide">
<div class="jw-shell">
  <div class="jw-heading"><span class="jw-eyebrow">BUYING GUIDE • EGYPT</span><h2>ساعة جاكوب اند كو هاي كوبي في مصر: دليل التصميم والسعر قبل الحجز</h2><p>معلومات واضحة تساعد على فهم التصميمين المعروضين واختيار المناسب.</p></div>
  <div class="jw-article-body">
   <p>عند البحث عن <strong>ساعة جاكوب اند كو هاي كوبي في مصر</strong> تظهر صور عديدة لساعات مختلفة جدًا رغم تشابه الأسماء المستخدمة في المتاجر. بعض الساعات لها واجهات مزدحمة بالتفاصيل الصناعية، وأخرى تتميز بأشكال أسطوانية وتروس ظاهرة. لذلك من المهم ألّا يعتمد الاختيار على اسم العلامة وحده، بل على شكل القطعة المصورة فعلًا وحجمها الظاهري وطريقة الحجز ومحتويات العلبة. تعرض هذه الصفحة تصميمين مستوحَيين من إبداعات Jacob &amp; Co، أحدهما فضي والآخر ذهبي وردي، بسعر موحد يبلغ 24,000 جنيه مصري للقطعة، مع ست قطع إجمالًا في المخزون وقت الإعلان عن العرض.</p>
   <p>الساعة المعروضة هنا <strong>نسخة هاي كوبي وليست ساعة أصلية من Jacob &amp; Co</strong>، وبالتالي لا يصح نقل مواصفات الحركة السويسرية أو قيمة الأحجار أو مواد التصنيع من موقع الشركة الأصلية إليها. الصور الدعائية تمنح تصورًا جماليًا واضحًا، بينما الفيديوهات المرفقة أعلى الصفحة هي وسيلة المعاينة الفعلية المتاحة للتصميمين والبوكس.</p>
   <h3>لماذا يلفت هذا النوع من الساعات الأنظار؟</h3>
   <p>السبب الرئيسي هو أسلوب التصميم الذي يجعل الواجهة جزءًا من شخصية الساعة. بدل المينا التقليدية البسيطة، تظهر أجزاء وأشكال متعددة تشبه التروس والمؤشرات والأنابيب أو الأسطوانات الصغيرة. هذا التباين بين الخلفية الداكنة والعناصر المعدنية يمنح الساعة حضورًا قويًا، خاصة مع البدلة أو الملابس الرسمية الداكنة. والاختيار النهائي هنا يعتمد على درجة اللمعان التي يفضلها المشتري: الفضي أكثر هدوءًا من حيث الإطار، والذهبي الوردي أكثر دفئًا ووضوحًا.</p>
   <h2>التصميم الفضي المستوحى من Jacob &amp; Co Oil Pump</h2>
   <p>يتميز شكل <strong>Oil Pump</strong> بطابعه الصناعي المستوحى من معدات استخراج النفط. يظهر في تصميم الساعة الفضي المرسل ذراع معدني بارز باللون الذهبي، وعناصر دائرية صغيرة وتفاصيل حمراء فوق واجهة داكنة. يتفاعل لون الهيكل الفضي مع تلك الأجزاء، ولذلك يبدو المظهر متوازنًا رغم كثرة التفاصيل. هذا التصميم مناسب لمن يحب الساعات الفنية التي تُرى تفاصيلها بوضوح من مسافة قريبة، وفي الوقت نفسه يريد هيكلًا خارجيًا بلون محايد.</p>
   <p>في الإصدارات الأصلية لدى Jacob &amp; Co توجد حركات وتقنيات معقدة مرتبطة بهذه الفكرة، لكن <strong>وجود الشكل نفسه في نسخة هاي كوبي لا يثبت وجود توربيون فعلي أو آلية مضخة متحركة</strong>. التأكد من الحركة ونوع الماكينة يكون من خلال فحص النسخة المعروضة أو الاستفسار المباشر عن مواصفاتها، وليس عبر نقل قائمة مواصفات الساعة الأصلية.</p>
   <h2>التصميم الذهبي الوردي المستوحى من Opera Godfather</h2>
   <p>التصميم الآخر يتميز بهيكل ذهبي وردي وحزام أسود وواجهة داكنة بتفاصيل لامعة، مع عناصر دائرية وأسطوانية مستوحاة من أسلوب ساعات <strong>Opera Godfather</strong>. اللون الذهبي الوردي أكثر بروزًا في الإضاءة، ولهذا يتجه إليه عادة من يريد ساعة تبدو قطعة إكسسوار أساسية لا مجرد أداة لمعرفة الوقت. ويمكن مشاهدة هيكلها الجانبي وطبيعة السوار بوضوح في الفيديو المخصص لها.</p>
   <p>تشتهر بعض الساعات الأصلية من مجموعة Opera Godfather بخصائص موسيقية وآليات فائقة التعقيد؛ لكن هذه الخصائص لا تُنسب إلى الساعة المعروضة هنا، لأن التشابه هو في <strong>الطابع الشكلي للتصميم</strong> فقط. ومن الأفضل عند السؤال عن الساعة تحديد «التصميم الذهبي الوردي» لتسهيل تأكيد القطعة المقصودة وتوافرها.</p>
   <h2>الفرق بين الساعة الفضية والذهبية الوردية</h2>
   <div class="jw-table-scroller"><table class="jw-compare"><thead><tr><th>وجه المقارنة</th><th>الفضية</th><th>الذهبية الوردية</th></tr></thead><tbody>
    <tr><th>فكرة التصميم</th><td>أجزاء صناعية مستوحاة من Oil Pump</td><td>تفاصيل زخرفية وأسطوانية مستوحاة من Opera Godfather</td></tr>
    <tr><th>لون الهيكل الظاهر</th><td>فضي مع عناصر ذهبية</td><td>ذهبي وردي</td></tr>
    <tr><th>لون السوار</th><td>أسود بنقشة جلدية</td><td>أسود بنقشة جلدية</td></tr>
    <tr><th>الانطباع العام</th><td>ميكانيكي جريء مع لون خارجي هادئ</td><td>مظهر فاخر أكثر دفئًا ولمعانًا</td></tr>
    <tr><th>سعر العرض للقطعة</th><td>24,000 جنيه</td><td>24,000 جنيه</td></tr>
   </tbody></table></div>
   <h2>مواصفات نسخة هاي كوبي: ما الذي نعرفه فعلًا؟</h2>
   <p>هناك فرق بين المواصفات الظاهرة في التصوير والمواصفات الفنية التي تحتاج تأكيدًا من البائع. اللون العام للهيكل والواجهة السوداء وشكل السوار وتفاصيل البوكس يمكن ملاحظتها في الملفات المرفقة. أما نوع الحركة، وبلد تصنيع الماكينة، وقطر الهيكل الدقيق، ونوع الزجاج، ومقاومة الماء، ومدة الضمان، فلا يمكن إثباتها من الصور وحدها. لهذا لا تعرض هذه الصفحة أرقامًا تقنية منقولة من الموديلات الأصلية على أنها تخص النسخ المعروضة.</p>
   <h3>الواجهة الهيكلية والتشطيب الخارجي</h3>
   <p>أكثر ما يميز هذه الساعات هو توزيع العناصر على المينا بصورة غير تقليدية. في الشكل الفضي تبرز الأجزاء الذهبية والحمراء مقابل الخلفية الداكنة، بينما يعتمد الشكل الذهبي الوردي على حضور اللون المعدني حول الواجهة. عند معاينة الفيديو، يُفضل ملاحظة وضوح المؤشرات، وحواف الهيكل، والانعكاسات فوق الزجاج، وكيف يبدو التصميم عند تحريك الساعة أمام الإضاءة.</p>
   <h3>السوار الأسود والراحة على المعصم</h3>
   <p>تظهر النسختان بسوار أسود ذي نقشة جلدية. الملمس الحقيقي والمادة المستخدمة ودرجة المرونة لا يمكن حسمها من الفيديو وحده، ولذلك يُستحسن تأكيدها أثناء التواصل. ويمكن أيضًا السؤال عن طول السوار ومدى ملاءمته لمحيط المعصم، خصوصًا أن هذا النوع من التصاميم يبدو أكبر بصريًا من الساعات الكلاسيكية البسيطة.</p>
   <h3>بوكس الساعة الخشبي</h3>
   <p>العلبة الظاهرة في الصور والفيديو طويلة وداكنة اللون، بتصميم يشبه الخشب ولوحة معدنية في الغطاء، ومن الداخل بطانة سوداء لحفظ الساعة وعرضها. وجود بوكس أنيق يزيد جاذبية الساعة كهدية. ومع ذلك، ينبغي تأكيد محتويات طلب الشراء عند الحجز، بما في ذلك نوع التغليف وأي أوراق أو ملحقات تأتي مع القطعة المتوفرة.</p>
   <h2>سعر ساعة جاكوب اند كو هاي كوبي في مصر: 24,000 جنيه</h2>
   <p><strong>سعر العرض الحالي هو 24,000 جنيه مصري للساعة الواحدة</strong> سواء وقع الاختيار على الشكل الفضي أو الذهبي الوردي، حسب التوفر الفعلي. ويشمل الإعلان أن المخزون الإجمالي المتاح ست قطع عند طرح العرض. لا توجد في هذه الصفحة مقارنة موثقة تكفي للجزم بأن السعر هو الأقل في السوق المصري، كما لم يُعتمد سعر أصلي سابق لحساب نسبة خصم محددة. عند مقارنة عروض متاجر الساعات، ينبغي مقارنة نفس جودة النسخة ومحتويات البوكس والضمان وسياسة الاستبدال، لا رقم السعر وحده.</p>
   <h2>كيف تستخدم الصور والفيديوهات قبل شراء الساعة؟</h2>
   <p>ابدأ بصور الاستوديو لفهم الستايل العام الذي تختاره، ثم ارجع إلى <a href="#watch-videos">الفيديوهات الحقيقية للمنتج</a> وشاهد الواجهة والسوار من أكثر من زاوية. لا تعتبر أي تفصيل غير موجود في تصوير المنتج الحقيقي ميزة مضمونة في القطعة. إذا كان يهمك عنصر محدد، مثل حركة جزء داخل المينا أو نوع القفل أو سمك الساعة، اطلب تأكيده صراحة عند الحجز. هذه الطريقة أهم من الاعتماد على صور جذابة فقط، لأنها تقلل الفارق بين التوقعات والقطعة التي سيتم تسليمها.</p>
   <h2>هل تصلح هذه الساعة كهدية؟</h2>
   <p>قد تكون مناسبة كهدية لمحبي الساعات ذات الشكل الجريء والتصميمات غير التقليدية، وبخاصة من يفضلون الإكسسوارات اللافتة. النسخة الفضية تميل إلى مظهر محايد نسبيًا، والذهبية الوردية تمنح حضورًا أكثر وضوحًا. البوكس المصور يزيد جاذبية العرض، لكن محتوياته النهائية يتم تأكيدها قبل الحجز. ولمن يفضل ساعة بسيطة وخفيفة جدًا، قد يكون هذا النوع ذو التفاصيل الكثيرة أقل ملاءمة من الساعة التقليدية.</p>
   <h2>نصائح للعناية بالساعة بعد الاستلام</h2>
   <p>لتقليل ظهور آثار الاستخدام، امسح الساعة بقطعة قماش ناعمة وجافة بعد الارتداء، واحتفظ بها داخل علبتها عند عدم الاستخدام. تجنب المواد الكيميائية والمنظفات القوية والاحتكاك بالأجسام الصلبة. لا تتعامل مع الساعة باعتبارها مقاومة للماء حتى يتم تأكيد تصنيفها فعليًا، ولا تضغط على أي جزء زخرفي أو تحاول تحريكه بالقوة. وإذا ظهرت مشكلة في الضبط أو الحركة، تواصل مع البائع لمعرفة الإجراء المناسب بدل فتح الغطاء بنفسك.</p>
   <h2>طريقة حجز ساعة جاكوب اند كو هاي كوبي</h2>
   <p>اختر التصميم الفضي أو الذهبي الوردي من أعلى الصفحة، ثم اضغط على زر <a href="#reserve">احجز ساعتك الآن</a> لفتح واتساب برسالة جاهزة تتضمن التصميم وسعر العرض. ويمكن الاتصال مباشرة على <a href="tel:+201025036151" dir="ltr">01025036151</a> للاستفسار عن المواصفات الدقيقة والكمية الباقية وطريقة التسليم وأي تكاليف إضافية. عدد الست قطع يشير إلى المخزون المعلن وقت نشر العرض، ولا يُعد رقمًا لحظيًا يتناقص تلقائيًا بعد كل طلب.</p>
   <p class="jw-source-note">للاطلاع على فكرة التصميم الأصلي فقط، يمكن مراجعة <a href="https://jacobandco.com/news/jacob-co-oil-pump-timepiece-modernized-masterpiece-for-a-new-era" target="_blank" rel="noopener noreferrer">وصف Oil Pump لدى الشركة المصنّعة</a> و<a href="https://jacobandco.com/timepieces/opera-godfather/rose-gold-diamond-barrels" target="_blank" rel="noopener noreferrer">مجموعة Opera Godfather الأصلية</a>. المواصفات المذكورة هناك تخص الساعات الأصلية، ولا تثبت مواصفات نسخ الهاي كوبي المعروضة للبيع هنا.</p>
  </div>
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
<script id="jw-actions" type="text/javascript" class="litespeed-no-defer" data-no-defer="1" data-no-optimize="1" data-cfasync="false">
(function(){
'use strict';
var images={steel:<?php echo wp_json_encode($steel); ?>,gold:<?php echo wp_json_encode($gold); ?>,box:<?php echo wp_json_encode($box); ?>};
var img=document.getElementById('jw-current-watch'),label=document.getElementById('jw-current-label'),choice='steel';
function waLink(name){return 'https://wa.me/201025036151?text='+encodeURIComponent('مرحبًا، أريد حجز ساعة '+(name==='gold'?'التصميم الذهبي الوردي':'التصميم الفضي')+' بسعر 24,000 جنيه من العرض محدود الكمية، برجاء تأكيد التوفر والتفاصيل.');}
function select(name){if(!images[name]||!img)return;if(name==='steel'||name==='gold')choice=name;img.src=images[name];img.alt=name==='box'?'صورة علبة الساعة الخشبية الفعلية':('صورة ستوديو فنية توضيحية، التصميم '+(name==='gold'?'الذهبي الوردي':'الفضي'));['data-src','data-lazy-src','data-original','data-lazy-original'].forEach(function(attr){if(img.hasAttribute(attr))img.setAttribute(attr,images[name]);});label.textContent=name==='box'?'صورة العلبة الفعلية':(name==='gold'?'صورة عرض فنية: الذهبي الوردي':'صورة عرض فنية: الفضي');document.querySelectorAll('[data-watch-variant]').forEach(function(b){if(b.classList.contains('jw-variant'))b.setAttribute('aria-pressed',String(b.dataset.watchVariant===choice));});document.querySelectorAll('[data-watch-whatsapp]').forEach(function(a){a.href=waLink(choice);});}
document.querySelectorAll('[data-watch-variant]').forEach(function(b){b.addEventListener('click',function(){select(b.dataset.watchVariant);});});
var bx=document.getElementById('jw-show-box');if(bx)bx.addEventListener('click',function(){select('box');});select('steel');
})();
</script>
<?php wp_footer(); ?>
</body></html>