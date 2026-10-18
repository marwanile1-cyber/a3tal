<?php
/**
 * A3tal post-audit precision repairs.
 * Only proven dead internal targets are changed. Topic journeys require
 * published matching sources, not broad brand or price guessing.
 */
if (!defined('ABSPATH')) exit;

/* Validated HTTP 404 alternatives: old URL => equivalent published guide. */
function a3tal_repaired_internal_links(): array {
  return [
    'live-data-obd2-scanner-readings-guide' => 'live-data-obd2',
    'freeze-frame-obd2-diagnostic-data' => 'freeze-frame-obd2',
    'p0171-system-too-lean-bank1' => 'p0171-system-too-lean-bank-1-diagnosis',
    'geely-starray-maintenance-schedule' => 'geely-starray-2026-prices-maintenance-service-centers',
    'engine-oil-consumption-no-leak-causes' => 'engine-oil-loss-without-visible-leak',
  ];
}

/* 404 targets without a truly equivalent replacement are neutralized in-page.
   Their source articles remain intact; no misleading homepage redirects. */
add_filter('the_content', static function($html) {
  if (!is_singular('post') || !in_the_loop() || !is_main_query()) return $html;
  $dead = array_fill_keys([
    'كورس-كهرباء-السيارات-دليلك-للاحتراف-م',
    'أسباب-اهتزاز-السرعات-العا',
    'لمبات-أعطال-السيارات-ومعانيها-بالصور',
    'parasitic-battery-drain-test',
    'أعراض-تلف-افتيس-الأوتوماتيك',
    'toyota-corolla-maintenance-schedule-egypt',
    'electric-car-prices-egypt-2026',
    'cars-prices-egypt-2026-local-imported',
    'tire-rotation-service-cost-egypt-2026',
    'car-ac-hot-at-idle-cold-driving-causes',
    'أسعار-قطع-غيار-أوبل-انسجنيا-2025-دليلك-ال',
    'عالم-أكواد-أعطال-السيارات-dtc-موسوعة-شامل',
    'check-injection-renault-causes-solutions',
    'أعطال-طرمبة-البنزين',
  ],true);
  $replace=a3tal_repaired_internal_links();
  return preg_replace_callback('~<a\b[^>]*\bhref\s*=\s*(["\'])(https?://(?:www\.)?a3tal\.com/[^"\']*)\1[^>]*>(.*?)</a>~isu',
    static function($m) use ($replace,$dead) {
      $path=trim(rawurldecode((string)wp_parse_url(html_entity_decode($m[2],ENT_QUOTES,'UTF-8'),PHP_URL_PATH)),'/');
      if (isset($replace[$path])) {
        return str_replace($m[2],esc_url(home_url('/'.$replace[$path].'/')),$m[0]);
      }
      if (isset($dead[$path])) {
        return '<span class="a3tal-unavailable-destination">'.$m[3].'</span>';
      }
      return $m[0];
    },$html);
}, 47);

/** Exact subject journeys after manual review, avoiding cross-brand link farms. */
function a3tal_editorial_approved_journeys(): array {
  return [
    'stft-ltft-fuel-trim-diagnosis' => ['p0171-system-too-lean-bank-1-diagnosis'],
    '6-speed-automatic-transmission-cars-dexron-vi-oil' => ['automatic-transmission-fluid-change-guide-risks'],
    'automatic-transmission-fluid-change-guide-risks' => ['6-speed-automatic-transmission-cars-dexron-vi-oil'],
    'geely-starray-2026-review-specs-faults' => ['geely-starray-2026-prices-maintenance-service-centers'],
    'geely-starray-2026-prices-maintenance-service-centers' => ['geely-starray-2026-review-specs-faults'],
    'toyota-corolla-2026-price-egypt-specs-guide' => ['toyota-corolla-electrical-ac-problems','toyota-corolla-suspension-steering-problems'],
    'toyota-corolla-electrical-ac-problems' => ['toyota-corolla-electrical-hybrid-screen-problems','toyota-corolla-2026-price-egypt-specs-guide'],
    'toyota-corolla-electrical-hybrid-screen-problems' => ['toyota-corolla-electrical-ac-problems'],
    'toyota-corolla-suspension-steering-problems' => ['toyota-corolla-2026-price-egypt-specs-guide'],
    'toyota-dtc-fault-codes-list' => ['toyota-corolla-fault-codes-dtc-dictionary'],
    'toyota-corolla-fault-codes-dtc-dictionary' => ['toyota-dtc-fault-codes-list'],
    'skoda-octavia-a7-a8-engine-problems' => ['skoda-octavia-dsg-transmission-problems','skoda-octavia-suspension-steering-guide'],
    'skoda-octavia-dsg-transmission-problems' => ['skoda-octavia-a7-a8-engine-problems','skoda-octavia-suspension-steering-guide'],
    'skoda-octavia-suspension-steering-guide' => ['skoda-octavia-a7-a8-engine-problems','skoda-octavia-dsg-transmission-problems'],
    'skoda-octavia-electrical-ac-problems' => ['skoda-octavia-a7-a8-engine-problems'],
    'hyundai-elantra-electrical-sensor-problems' => ['hyundai-elantra-suspension-maintenance-guide'],
    'hyundai-elantra-suspension-maintenance-guide' => ['hyundai-elantra-electrical-sensor-problems'],
    'hyundai-tucson-nx4-transmission-problems-dct' => ['hyundai-tucson-nx4-suspension-steering-problems','hyundai-tucson-nx4-fault-codes-dtc-dictionary'],
    'hyundai-tucson-nx4-suspension-steering-problems' => ['hyundai-tucson-nx4-transmission-problems-dct'],
    'hyundai-tucson-nx4-fault-codes-dtc-dictionary' => ['hyundai-tucson-nx4-transmission-problems-dct'],
    'renault-megane-electrical-rlink2-problems' => ['renault-megane-suspension-steering-problems'],
    'renault-megane-suspension-steering-problems' => ['renault-megane-electrical-rlink2-problems'],
    'mg-5-electrical-screen-tpms-problems' => ['mg-5-suspension-steering-rack-problems'],
    'mg-5-suspension-steering-rack-problems' => ['mg-5-electrical-screen-tpms-problems'],
    'mg-6-electrical-screen-battery-problems' => ['mg-6-engine-turbo-problems-lspi-oil'],
    'mg-6-engine-turbo-problems-lspi-oil' => ['mg-6-electrical-screen-battery-problems'],
    'kia-sportage-dct-gearbox-overheating-problems' => ['kia-sportage-fault-codes-dtc-full-list-guide'],
    'kia-sportage-fault-codes-dtc-full-list-guide' => ['kia-sportage-dct-gearbox-overheating-problems'],
    'nissan-sunny-engine-common-faults' => ['nissan-sunny-prices-service-centers-2026'],
    'mitsubishi-xpander-fault-codes-dtc-guide' => ['mitsubishi-xpander-engine-performance-fuel-pump-faults', 'mitsubishi-xpander-electrical-ac-problems-smart-key'],
    'mitsubishi-xpander-electrical-ac-problems-smart-key' => ['mitsubishi-xpander-fault-codes-dtc-guide', 'mitsubishi-xpander-engine-performance-fuel-pump-faults'],
    'modern-car-safety-systems-encyclopedia' => ['ما-هو-نظام-abs', 'cruise-control-system-types-faults-encyclopedia'],
    'cruise-control-system-types-faults-encyclopedia' => ['modern-car-safety-systems-encyclopedia', 'ما-هو-نظام-abs'],
    'car-license-renewal-costs-3-years-guide' => ['traffic-fines-prices-radars-egypt-2026'],
    'traffic-fines-prices-radars-egypt-2026' => ['car-license-renewal-costs-3-years-guide'],
    'thinkdiag-2-في-مصر-المواصفات،-تكويد-الحساسات،-ا' => ['live-data-obd2', 'freeze-frame-obd2'],
    'live-data-obd2' => ['freeze-frame-obd2', 'thinkdiag-2-في-مصر-المواصفات،-تكويد-الحساسات،-ا'],
    'freeze-frame-obd2' => ['thinkdiag-2-في-مصر-المواصفات،-تكويد-الحساسات،-ا', 'live-data-obd2'],
    'أعطال-التكييف-في-السيارات' => ['car-ac-complete-maintenance-guide', 'car-ac-compressor-types-and-maintenance'],
    'fiat-tipo-maintenance-schedule-prices-egypt' => ['common-car-maintenance-mistakes-shorten-life'],
    'common-car-maintenance-mistakes-shorten-life' => ['fiat-tipo-maintenance-schedule-prices-egypt'],
    'bmw-maintenance-costs-warranty-egypt-2026' => ['bmw-x5-2026-hybrid-specs-problems-maintenance', 'bmw-2026-neue-klasse-i3-specs-problems'],
    'bmw-x5-2026-hybrid-specs-problems-maintenance' => ['bmw-2026-neue-klasse-i3-specs-problems', 'bmw-maintenance-costs-warranty-egypt-2026'],
    'bmw-2026-neue-klasse-i3-specs-problems' => ['bmw-maintenance-costs-warranty-egypt-2026', 'bmw-x5-2026-hybrid-specs-problems-maintenance'],
    'تقرير-شامل-byd-seagull-في-مصر-المواصفات،-السع' => ['مراجعة-byd-seal-هل-قتلت-قاتلة-تسلا-هيمنة-مودي', 'geely-geometry-c-vs-byd-atto-3-comparison'],
    'مراجعة-byd-seal-هل-قتلت-قاتلة-تسلا-هيمنة-مودي' => ['geely-geometry-c-vs-byd-atto-3-comparison', 'vw-id4-crozz-2026-price-egypt'],
    'geely-geometry-c-vs-byd-atto-3-comparison' => ['vw-id4-crozz-2026-price-egypt', 'changan-benni-estar-price-egypt'],
    'vw-id4-crozz-2026-price-egypt' => ['changan-benni-estar-price-egypt', 'mg-cyberster-electric-sports-car-review'],
    'changan-benni-estar-price-egypt' => ['mg-cyberster-electric-sports-car-review', 'تقرير-شامل-byd-seagull-في-مصر-المواصفات،-السع'],
    'mg-cyberster-electric-sports-car-review' => ['تقرير-شامل-byd-seagull-في-مصر-المواصفات،-السع', 'مراجعة-byd-seal-هل-قتلت-قاتلة-تسلا-هيمنة-مودي'],
    'motorcycle-maintenance-schedule-guide' => ['motorcycle-chain-slack-tightening-maintenance-guide', 'motorcycle-tyres-guide-egypt'],
    'motorcycle-chain-slack-tightening-maintenance-guide' => ['motorcycle-tyres-guide-egypt', 'motorcycle-genuine-vs-aftermarket-parts'],
    'motorcycle-tyres-guide-egypt' => ['motorcycle-genuine-vs-aftermarket-parts', 'motorcycle-maintenance-schedule-guide'],
    'motorcycle-genuine-vs-aftermarket-parts' => ['motorcycle-maintenance-schedule-guide', 'motorcycle-chain-slack-tightening-maintenance-guide'],
    'motorcycle-brands-egypt-complete-guide' => ['chinese-motorcycles-egypt-guide', 'japanese-vs-indian-vs-chinese-motorcycle'],
    'chinese-motorcycles-egypt-guide' => ['japanese-vs-indian-vs-chinese-motorcycle', 'motorcycle-brands-egypt-complete-guide'],
    'japanese-vs-indian-vs-chinese-motorcycle' => ['motorcycle-brands-egypt-complete-guide', 'chinese-motorcycles-egypt-guide'],
    'used-motorcycle-buying-checklist-egypt' => ['delivery-motorcycle-buying-guide', 'new-motorcycle-delivery-checklist'],
    'delivery-motorcycle-buying-guide' => ['new-motorcycle-delivery-checklist', 'scooter-vs-motorcycle-egypt'],
    'new-motorcycle-delivery-checklist' => ['scooter-vs-motorcycle-egypt', 'motorcycle-engine-sizes-125-150-160-200-250'],
    'scooter-vs-motorcycle-egypt' => ['motorcycle-engine-sizes-125-150-160-200-250', 'used-motorcycle-buying-checklist-egypt'],
    'motorcycle-engine-sizes-125-150-160-200-250' => ['used-motorcycle-buying-checklist-egypt', 'delivery-motorcycle-buying-guide'],
    'عيوب-نيسان-صني-n17' => ['جدول-صيانة-نيسان-صني-2026', 'nissan-sunny-engine-common-faults'],
    'جدول-صيانة-نيسان-صني-2026' => ['nissan-sunny-engine-common-faults', 'nissan-sunny-brakes-suspension-guide'],
    'rear-main-seal-leak-symptoms-cost' => ['engine-oil-loss-without-visible-leak'],
    'engine-oil-loss-without-visible-leak' => ['rear-main-seal-leak-symptoms-cost'],
    'نتشة-الفتيس-تيجو-7' => ['automatic-transmission-fluid-change-guide-risks'],
    'chery-tiggo-8-pro-maintenance-prices-guide-2026' => ['chery-tiggo-8-pro-engine-gearbox-problems-acteco'],
    'fuel-injection-vs-carburetor-motorcycle' => ['motorcycle-maintenance-schedule-guide'],
    'steering-wheel-vibrates-when-braking-diagnosis' => ['sinking-brake-pedal-master-cylinder-abs-diagnosis'],
    'hyundai-elantra-engine-problems-guide' => ['hyundai-elantra-transmission-problems-guide', 'hyundai-elantra-electrical-sensor-problems'],
    'hyundai-elantra-transmission-problems-guide' => ['hyundai-elantra-electrical-sensor-problems', 'hyundai-elantra-suspension-maintenance-guide'],
    'nissan-sunny-brakes-suspension-guide' => ['nissan-sunny-transmission-fluid-matic-s-price-specs', 'nissan-sunny-prices-service-centers-2026'],
    'nissan-sunny-transmission-fluid-matic-s-price-specs' => ['nissan-sunny-prices-service-centers-2026', 'nissan-sunny-engine-common-faults'],
    'nissan-sunny-prices-service-centers-2026' => ['nissan-sunny-engine-common-faults', 'nissan-sunny-brakes-suspension-guide'],
    'toyota-corolla-suspension-brakes-guide' => ['toyota-corolla-electrical-ac-problems', 'toyota-corolla-electrical-hybrid-screen-problems'],
    'hyundai-tucson-nx4-engine-problems-smartstream' => ['hyundai-tucson-nx4-electrical-screen-battery-problems', 'hyundai-tucson-nx4-transmission-problems-dct'],
    'hyundai-tucson-nx4-electrical-screen-battery-problems' => ['hyundai-tucson-nx4-transmission-problems-dct', 'hyundai-tucson-nx4-suspension-steering-problems'],
    'chery-tiggo-8-pro-suspension-comfort-nvh' => ['chery-tiggo-8-pro-electrical-battery-tailgate-problems', 'chery-tiggo-8-pro-fault-codes-dtc-dictionary'],
    'chery-tiggo-8-pro-electrical-battery-tailgate-problems' => ['chery-tiggo-8-pro-fault-codes-dtc-dictionary', 'chery-tiggo-8-pro-screens-technology-problems'],
    'chery-tiggo-8-pro-fault-codes-dtc-dictionary' => ['chery-tiggo-8-pro-screens-technology-problems', 'chery-tiggo-8-pro-engine-gearbox-problems-acteco'],
    'chery-tiggo-8-pro-screens-technology-problems' => ['chery-tiggo-8-pro-engine-gearbox-problems-acteco', 'chery-tiggo-8-pro-suspension-comfort-nvh'],
    'chery-tiggo-8-pro-engine-gearbox-problems-acteco' => ['chery-tiggo-8-pro-suspension-comfort-nvh', 'chery-tiggo-8-pro-electrical-battery-tailgate-problems'],
    'jetour-suspension-steering-stability-problems' => ['jetour-fault-codes-dtc-dictionary', 'jetour-engine-problems-1-5t-vs-1-6t'],
    'jetour-fault-codes-dtc-dictionary' => ['jetour-engine-problems-1-5t-vs-1-6t', 'jetour-suspension-steering-stability-problems'],
    'jetour-engine-problems-1-5t-vs-1-6t' => ['jetour-suspension-steering-stability-problems', 'jetour-fault-codes-dtc-dictionary'],
    'opel-insignia-grand-sport-engine-lspi-problems' => ['opel-insignia-suspension-steering-ground-clearance', 'opel-insignia-electrical-intellilux-screen-problems'],
    'opel-insignia-suspension-steering-ground-clearance' => ['opel-insignia-electrical-intellilux-screen-problems', 'opel-insignia-fault-codes-dtc-dictionary'],
    'opel-insignia-electrical-intellilux-screen-problems' => ['opel-insignia-fault-codes-dtc-dictionary', 'opel-insignia-grand-sport-engine-lspi-problems'],
    'opel-insignia-fault-codes-dtc-dictionary' => ['opel-insignia-grand-sport-engine-lspi-problems', 'opel-insignia-suspension-steering-ground-clearance'],
    'hyundai-matrix-engine-gearbox-fuel-consumption' => ['hyundai-matrix-suspension-stability-shocks', 'hyundai-matrix-electrical-ac-interior-problems'],
    'hyundai-matrix-suspension-stability-shocks' => ['hyundai-matrix-electrical-ac-interior-problems', 'hyundai-matrix-fault-codes-dtc-dictionary'],
    'hyundai-matrix-electrical-ac-interior-problems' => ['hyundai-matrix-fault-codes-dtc-dictionary', 'hyundai-matrix-engine-gearbox-fuel-consumption'],
    'hyundai-matrix-fault-codes-dtc-dictionary' => ['hyundai-matrix-engine-gearbox-fuel-consumption', 'hyundai-matrix-suspension-stability-shocks'],
    'opel-astra-j-14-turbo-engine-piston-failure-lspi' => ['opel-astra-j-cooling-system-leaks-thermostat', 'opel-astra-j-transmission-electrical-stabilitrak-problems'],
    'opel-astra-j-cooling-system-leaks-thermostat' => ['opel-astra-j-transmission-electrical-stabilitrak-problems', 'opel-astra-j-fault-codes-dtc-dictionary'],
    'opel-astra-j-transmission-electrical-stabilitrak-problems' => ['opel-astra-j-fault-codes-dtc-dictionary', 'opel-astra-j-14-turbo-engine-piston-failure-lspi'],
    'opel-astra-j-fault-codes-dtc-dictionary' => ['opel-astra-j-14-turbo-engine-piston-failure-lspi', 'opel-astra-j-cooling-system-leaks-thermostat'],
    'mg-6-suspension-stability-tires-guide' => ['mg-6-gearbox-dct-problems-maintenance', 'mg-6-engine-turbo-problems-lspi-oil'],
    'mg-6-gearbox-dct-problems-maintenance' => ['mg-6-engine-turbo-problems-lspi-oil', 'mg-6-electrical-screen-battery-problems'],
    'kia-sportage-tgdi-engine-turbo-carbon-buildup' => ['kia-sportage-suspension-brakes-wheels-problems', 'kia-sportage-electrical-screens-adas-problems'],
    'kia-sportage-suspension-brakes-wheels-problems' => ['kia-sportage-electrical-screens-adas-problems', 'kia-sportage-dct-gearbox-overheating-problems'],
    'kia-sportage-electrical-screens-adas-problems' => ['kia-sportage-dct-gearbox-overheating-problems', 'kia-sportage-fault-codes-dtc-full-list-guide'],
    'dealer-vs-authorized-distributor-vs-private-showroom-egypt' => ['how-to-verify-car-showroom-authorized-egypt', 'new-car-delivery-checklist-egypt'],
    'how-to-verify-car-showroom-authorized-egypt' => ['new-car-delivery-checklist-egypt', 'questions-before-booking-new-car-egypt'],
    'new-car-delivery-checklist-egypt' => ['questions-before-booking-new-car-egypt', 'test-drive-before-buying-car-egypt'],
    'questions-before-booking-new-car-egypt' => ['test-drive-before-buying-car-egypt', 'dealer-vs-authorized-distributor-vs-private-showroom-egypt'],
    'test-drive-before-buying-car-egypt' => ['dealer-vs-authorized-distributor-vs-private-showroom-egypt', 'how-to-verify-car-showroom-authorized-egypt'],
    'car-showroom-finance-hidden-costs-egypt' => ['compare-car-showroom-offers-egypt', 'car-overprice-egypt-dealership-guide'],
    'compare-car-showroom-offers-egypt' => ['car-overprice-egypt-dealership-guide', 'overprice-2024-loss-december-2025'],
    'car-overprice-egypt-dealership-guide' => ['overprice-2024-loss-december-2025', 'car-showroom-finance-hidden-costs-egypt'],
    'overprice-2024-loss-december-2025' => ['car-showroom-finance-hidden-costs-egypt', 'compare-car-showroom-offers-egypt'],
    'car-ac-complete-maintenance-guide' => ['car-ac-compressor-types-and-maintenance'],
    'car-ac-compressor-types-and-maintenance' => ['car-ac-complete-maintenance-guide'],
    'exhaust-system-car-encyclopedia' => ['car-exhaust-smoke-colors-causes', 'egr-valve-failure-symptoms-guide'],
    'car-exhaust-smoke-colors-causes' => ['egr-valve-failure-symptoms-guide', 'exhaust-system-car-encyclopedia'],
    'egr-valve-failure-symptoms-guide' => ['exhaust-system-car-encyclopedia', 'car-exhaust-smoke-colors-causes'],
    'engine-valves-function-problems-guide' => ['engine-operation-cycles-parts-guide', 'full-engine-overhaul-vs-half-rebuild-guide'],
    'engine-operation-cycles-parts-guide' => ['full-engine-overhaul-vs-half-rebuild-guide', 'engine-valves-function-problems-guide'],
    'رعشة-العربية-على-السلانسيه' => ['رعشة-في-الموتور-وهو-واقف', 'p0507-high-idle-rpm-diagnosis'],
    'رعشة-في-الموتور-وهو-واقف' => ['p0507-high-idle-rpm-diagnosis', 'rpm-بيعلى-ويوطي'],
    'p0507-high-idle-rpm-diagnosis' => ['rpm-بيعلى-ويوطي', 'مكان-حساس-الايدل-وتنظيفه'],
    'liqui-moly-engine-oils' => ['saeer-zayt-kastrol-5w30-masr-2026', 'shell-helix-ultra-10000-price-specs-egypt'],
    'saeer-zayt-kastrol-5w30-masr-2026' => ['shell-helix-ultra-10000-price-specs-egypt', 'motul-8100-xcess-gen2-5w40-price-egypt'],
    'shell-helix-ultra-10000-price-specs-egypt' => ['motul-8100-xcess-gen2-5w40-price-egypt', 'liqui-moly-engine-oils'],
    'motul-8100-xcess-gen2-5w40-price-egypt' => ['liqui-moly-engine-oils', 'saeer-zayt-kastrol-5w30-masr-2026'],
    'sinking-brake-pedal-master-cylinder-abs-diagnosis' => ['ما-هو-نظام-abs', 'دليلك-الشامل-لصيانة-نظام-abs-ومعالجة-أشه'],
    'used-cars-market-egypt-2026' => ['test-drive-before-buying-car-egypt', 'dealer-vs-authorized-distributor-vs-private-showroom-egypt'],
    'spark-plug-wet-with-fuel-diagnosis' => ['الفرق-بين-البوجيهات-العادية-والليزر', 'البوجيهات-إزاي-تعرف-إنها-بايظة؟-وأم'],
    'الفرق-بين-البوجيهات-العادية-والليزر' => ['البوجيهات-إزاي-تعرف-إنها-بايظة؟-وأم', 'spark-plug-wet-with-fuel-diagnosis'],
    'البوجيهات-إزاي-تعرف-إنها-بايظة؟-وأم' => ['spark-plug-wet-with-fuel-diagnosis', 'الفرق-بين-البوجيهات-العادية-والليزر'],
    'mitsubishi-xpander-engine-performance-fuel-pump-faults' => ['fuel-pump-low-pressure-how-to-test-before-replacement','mitsubishi-xpander-electrical-ac-problems-smart-key'],
    'renault-kadjar-high-pressure-fuel-pump-problems' => ['fuel-pump-low-pressure-how-to-test-before-replacement'],
    'hyundai-elantra-ad-maintenance-schedule-prices-2026' => ['hyundai-elantra-electrical-sensor-problems','hyundai-elantra-suspension-maintenance-guide'],
    'chevrolet-optra-transmission-fluid-price-egypt' => ['automatic-transmission-fluid-change-guide-risks'],
    'rpm-بيعلى-ويوطي' => ['مكان-حساس-الايدل-وتنظيفه','stft-ltft-fuel-trim-diagnosis'],
    'مكان-حساس-الايدل-وتنظيفه' => ['rpm-بيعلى-ويوطي'],
    'mobil-dot4-brake-fluid-price-egypt' => ['brake-fluid-change-moisture-test-dot4'],
    'car-water-pump-symptoms-prices-egypt-2026' => ['صيانة-دورة-التبريد-السيارة'],
    'full-engine-overhaul-vs-half-rebuild-guide' => ['engine-oil-loss-without-visible-leak'],
    'ما-هو-نظام-abs' => ['دليلك-الشامل-لصيانة-نظام-abs-ومعالجة-أشه'],
    'دليلك-الشامل-لصيانة-نظام-abs-ومعالجة-أشه' => ['ما-هو-نظام-abs'],
    'car-stalls-wont-restart-diagnosis' => ['live-data-obd2'],
    'car-stalls-while-driving-causes-diagnosis' => ['car-stalls-wont-restart-diagnosis'],
    'renault-sandero-common-fault-codes' => ['live-data-obd2','freeze-frame-obd2'],
    'intake-manifold-gasket-symptoms-leak' => ['stft-ltft-fuel-trim-diagnosis','p0171-system-too-lean-bank-1-diagnosis'],
    'tps-sensor-symptoms-testing-guide' => ['live-data-obd2'],
    'automatic-car-poor-acceleration-causes' => ['automatic-transmission-fluid-change-guide-risks'],
    'صيانة-دورة-التبريد-السيارة' => ['car-water-pump-symptoms-prices-egypt-2026'],
  ];
}

add_filter('the_content', static function($html) {
  if (!is_singular('post') || !in_the_loop() || !is_main_query()) return $html;
  $slug=trim(rawurldecode((string)wp_parse_url(get_permalink(get_the_ID()),PHP_URL_PATH)),'/');
  $all=a3tal_editorial_approved_journeys();
  if (!isset($all[$slug])) return $html;
  $links=[];
  foreach ($all[$slug] as $target_slug) {
    if ($target_slug===$slug) continue;
    $post=get_page_by_path($target_slug,OBJECT,'post');
    if (!($post instanceof WP_Post)) {
      $target_id=url_to_postid(home_url('/'.$target_slug.'/'));
      if ($target_id && get_post_type($target_id)==='post') $post=get_post($target_id);
    }
    if (!($post instanceof WP_Post) || $post->post_status!=='publish' || $post->ID===get_the_ID()) continue;
    $url=get_permalink($post);
    if (!$url || strpos($html,$url)!==false) continue;
    $links[]='<li><a href="'.esc_url($url).'">'.esc_html(get_the_title($post)).'</a></li>';
    if (count($links)>=2) break;
  }
  if (!$links) return $html;
  return $html.'<aside class="a3tal-topical-journey" aria-label="أدلة متعلقة بنفس الموضوع"'
    .' style="margin:20px 0;padding:14px 18px;border:1px solid #d9e3ed;border-radius:12px">'
    .'<h2 style="font-size:1.15em;margin:0 0 8px">أدلة ومقارنات مرتبطة بموضوعك</h2>'
    .'<ul style="margin:0">'.implode('',$links).'</ul></aside>';
}, 66);

/* Reciprocal links from code-specific editorial posts to uniquely indexable DTC pages.
   Excluded/canonicalized codes never get competing article-to-stub links. */
add_filter('the_content', static function($html) {
  if (!is_singular('post') || !in_the_loop() || !is_main_query() || !function_exists('a3g_dtc_indexable_codes')) return $html;
  $title=(string)get_the_title();
  preg_match_all('/(?<![A-Z0-9])([PBCU][0-9][0-9A-F]{3})(?![A-Z0-9])/i',$title,$m);
  if (!$m || empty($m[1])) return $html;
  $approved=a3g_dtc_indexable_codes();
  $items=[];
  foreach (array_unique(array_map('strtoupper',$m[1])) as $code) {
    if (!isset($approved[$code])) continue;
    $record=get_page_by_path(strtolower($code),OBJECT,'a3_dtc');
    if (!($record instanceof WP_Post) || $record->post_status!=='publish') continue;
    $url=get_permalink($record);
    if (!$url || strpos($html,$url)!==false) continue;
    $items[]='<a href="'.esc_url($url).'">الشرح الفني لكود '.esc_html($code).' في المكتبة</a>';
    if (count($items)>=2) break;
  }
  if (!$items) return $html;
  return $html.'<p class="a3tal-code-journey" style="margin:16px 0"><strong>من موسوعة أكواد الأعطال:</strong> '.implode('، ',$items).'.</p>';
}, 68);


/** Unique metadata for individually indexable DTC records only. */
add_filter('wpseo_metadesc', static function($current) {
  if (trim((string)$current)!=='' || !is_singular('a3_dtc') || !function_exists('a3g_dtc_indexable_codes')) return $current;
  $id=(int)get_queried_object_id();
  if (!$id || get_post_status($id)!=='publish') return $current;
  $code=function_exists('a3g_dtc_current_code')?a3g_dtc_current_code($id):'';
  $approved=a3g_dtc_indexable_codes();
  if (!$code || !isset($approved[$code])) return $current;
  $intro=trim((string)get_post_field('post_excerpt',$id));
  if ($intro==='') $intro=(string)get_post_field('post_content',$id);
  $intro=trim((string)preg_replace('/\s+/u',' ',wp_strip_all_tags(strip_shortcodes($intro))));
  if ($intro==='') return $current;
  $text=(function_exists('mb_substr')?mb_substr($intro,0,153,'UTF-8'):wp_html_excerpt($intro,153,''));
  $last=trim($text);
  if ($last==='' || (function_exists('mb_strlen') && mb_strlen($last,'UTF-8')<65)) return $current;
  return $last . ($last===$intro?'':'…');
}, 200);


/** Vetted DTC cluster neighbors: relationships by diagnostic subsystem, not P/B/C/U first letter. */
add_filter('the_content', static function($html) {
  if (!is_singular('a3_dtc') || !in_the_loop() || !is_main_query() ||
      !function_exists('a3g_dtc_current_code') || !function_exists('a3g_dtc_indexable_codes')) return $html;
  $id=(int)get_queried_object_id();
  $code=a3g_dtc_current_code($id);
  $approved=a3g_dtc_indexable_codes();
  if (!isset($approved[$code])) return $html;
  $groups=[
    ['P0116','P0117','P0118','P0119'],
    ['P0121','P0122','P0123'],
    ['P0130','P0131','P0132','P0133','P0134'],
    ['P0137','P0138','P0139','P0140','P0141'],
    ['P0190','P0191','P0192','P0193'],
    ['P0200','P0201','P0202','P0203','P0204','P0205','P0206'],
    ['P0305','P0306','P0316'],
    ['P0325','P0327','P0328'],
    ['P0336','P0341','P0345','P0365','P0369'],
    ['P0351','P0352','P0353','P0354'],
    ['P0401','P0402','P0403'],
    ['P0441','P0443','P0446','P0456'],
    ['P0451','P0452','P0453'],
    ['P0505','P0506'],
    ['P0705','P0706'],
    ['P0715','P0716'],
    ['P0720','P0722'],
    ['P0730','P0731','P0732','P0733'],
    ['U0101','U0102','U0103','U0104'],
    ['U0121','U0122','U0123'],
    ['C0035','C0040','C0045','C0050'],
    ['B0001','B0010','B0020'],
  ];
  $near=[];
  foreach ($groups as $group) {
    if (in_array($code,$group,true)) {
      $near=$group; break;
    }
  }
  if (!$near) return $html;
  $links=[];
  foreach ($near as $peer) {
    if ($peer===$code || !isset($approved[$peer])) continue;
    $post=get_page_by_path(strtolower($peer),OBJECT,'a3_dtc');
    if (!($post instanceof WP_Post) || $post->post_status!=='publish') continue;
    $url=get_permalink($post);
    if (!$url || strpos($html,$url)!==false) continue;
    $links[]='<li><a href="'.esc_url($url).'">كود '.esc_html($peer).': '.esc_html(get_the_title($post)).'</a></li>';
    if (count($links)>=3) break;
  }
  if (!$links) return $html;
  return $html.'<aside class="a3tal-dtc-system-journey" aria-label="أكواد مرتبطة بنفس النظام"'
     .' style="margin:20px 0;padding:15px 18px;border:1px solid #dae3ec;border-radius:12px">'
     .'<h2 style="font-size:1.12em;margin:0 0 9px">أكواد مرتبطة بنفس نظام التشخيص</h2>'
     .'<p>قد تظهر أكواد مشابهة عند فحص نفس الدائرة. معنى كل كود وطريقة اختباره مختلفان.</p>'
     .'<ul>'.implode('',$links).'</ul></aside>';
}, 75);
