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
  $slug=(string)get_post_field('post_name',get_the_ID());
  $all=a3tal_editorial_approved_journeys();
  if (!isset($all[$slug])) return $html;
  $links=[];
  foreach ($all[$slug] as $target_slug) {
    if ($target_slug===$slug) continue;
    $post=get_page_by_path($target_slug,OBJECT,'post');
    if (!($post instanceof WP_Post) || $post->post_status!=='publish' || $post->ID===get_the_ID()) continue;
    $url=get_permalink($post);
    if (!$url || strpos($html,$url)!==false) continue;
    $links[]='<li><a href="'.esc_url($url).'">'.esc_html(get_the_title($post)).'</a></li>';
    if (count($links)>=2) break;
  }
  if (!$links) return $html;
  return $html.'<aside class="a3tal-topical-journey" aria-label="أدلة متعلقة بنفس الموضوع"'
    .' style="margin:20px 0;padding:14px 18px;border:1px solid #d9e3ed;border-radius:12px">'
    .'<h2 style="font-size:1.15em;margin:0 0 8px">أدلة مكملة لنفس السيارة أو العطل</h2>'
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
