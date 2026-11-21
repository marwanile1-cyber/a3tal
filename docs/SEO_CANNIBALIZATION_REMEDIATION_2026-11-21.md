# A3tal Egypt — Cannibalization remediation record (2026-11-21)

## Production scope
- Root WordPress: https://a3tal.com/ (Egypt).
- Separate /ksa/ installation **not modified**.
- All changes through GitHub Actions and A3tal Direct Bridge; no WPWriter.
- No posts deleted; originals retained as published, noindexed 301 sources. Redirects point to anchored sections in the retained model hub.
- Core update traffic recovery is **not** yet proven by current-period GSC.

## Confirmed fixes
- 3 Ghabbour/Mansour consolidation redirects: https://github.com/marwanile1-cyber/a3tal/actions/runs/44904773843
- 7 old malformed URL 404 fixes: https://github.com/marwanile1-cyber/a3tal/actions/runs/44906946821
- 3 redirected dealer pages removed from post XML sitemap, reducing 640 to 637: https://github.com/marwanile1-cyber/a3tal/actions/runs/44907583513
- 11 internal link URLs replaced in nine published articles: https://github.com/marwanile1-cyber/a3tal/actions/runs/44907812169
- 16 model fact records consolidated into 3 hubs: https://github.com/marwanile1-cyber/a3tal/actions/runs/44908933064
- 26 Kia Sportage NQ5 records consolidated into one retained hub: https://github.com/marwanile1-cyber/a3tal/actions/runs/44909168278
- 85 Kia and Hyundai fact records consolidated into four hubs: https://github.com/marwanile1-cyber/a3tal/actions/runs/44909326151
- Total: **127 subordinate fact records consolidated into 8 authoritative hubs**, with original content backed up as GitHub Actions artifacts (90 days) and 301 instructions stored in A3tal Direct Bridge.
- Duplicate generic advisory paragraph blocks removed from merged copies: 57 in first four hubs (https://github.com/marwanile1-cyber/a3tal/actions/runs/44909615137), 145 in four further hubs (https://github.com/marwanile1-cyber/a3tal/actions/runs/44909671398); **202 repeated paragraphs** removed without altering the underlying technical source sections.
- Live site sitemap verification: car-reference URLs **456 -> 329**; post-sitemap **637**: https://github.com/marwanile1-cyber/a3tal/actions/runs/44909679705

## Model hub IDs
| Existing hub | Parent post ID | Sources redirected |
| --- | ---: | ---: |
| /car-reference/nissan/sunny-n17-egypt/ | 85086 | 6 |
| /car-reference/chevrolet/optra-2026-egypt/ | 85128 | 6 |
| /car-reference/jetour/t1-15t-7dct-egypt-2026/ | 86164 | 4 |
| /car-reference/kia/sportage-nq5-2023/ | 84890 | 26 |
| /car-reference/kia/seltos-sp2-2023/ | 84888 | 25 |
| /car-reference/kia/cerato-bd-2023/ | 84886 | 24 |
| /car-reference/hyundai/elantra-cn7-2025/ | 85047 | 20 |
| /car-reference/hyundai/tucson-nx4e-2025/ | 85063 | 16 |

## Outstanding work
- Verify all 127 live raw HTTP status codes and targets independently (run: https://github.com/marwanile1-cyber/a3tal/actions/runs/44909771908).
- Audit the remaining car-reference clusters individually; many subpages target different engine/market/fuel variants. Do **not** blanket-redirect based on URL similarities without moving accurate technical detail and checking indexability.
- Audit remaining article-vs-article query cannibalization with **page+query** GSC extracts when first-party access is available. The 92-day bulk report alone does not establish lost query ownership.
- Check the site when Google November 2026 Core Update is complete and wait at least 7 days to compare a stable period to comparable pre-November 10 days.
- Keep technical data engine-/transmission-/market-specific; avoid combining different fluid specifications into a single unsafe figure.
- **Do not rerun one-shot migration workflows** after successful deployment. Each requires exact parent/child counts and source-content migration guards. Any new change needs a fresh audited batch.

## Additional verified production batch (continuation on 2026-11-21)
- Four MG/Geely/Chery hubs: **37** additional consolidated source URLs, with full content migration + saved 301 instructions: https://github.com/marwanile1-cyber/a3tal/actions/runs/44910379524
- Copy cleanup for these hubs: **27** exact repeated generic advisory paragraphs removed: https://github.com/marwanile1-cyber/a3tal/actions/runs/44910545387
- Four Captiva/Magnite/Patrol/MG GT hubs: **27** more source URLs consolidated, with backup + saved 301 instructions: https://github.com/marwanile1-cyber/a3tal/actions/runs/44910678907
- Copy cleanup for this batch: **20** exact repeated generic advisory paragraphs removed: https://github.com/marwanile1-cyber/a3tal/actions/runs/44910819308
- Independent complete verification: **191/191** raw live HTTP 301 responses with correct targets; **16/16** hubs return content, index/follow and self-canonical; **0** redirected old sources in the XML sitemap; car-reference sitemap **456 -> 265**: https://github.com/marwanile1-cyber/a3tal/actions/runs/44910835942
- Consolidated total now **191** old model-reference URLs into **16** existing hubs; **249** exact repeated generic paragraphs removed in total (202 earlier + 27 + 20), without deleting sections of technical facts.
- GSC new date-by-page-by-query breakdown still unavailable; no traffic recovery claim.

### Additional model hubs
| Canonical model hub | Parent post ID | Child sources with 301 |
| --- | ---: | ---: |
| /car-reference/mg/new-zs-cvt-egypt/ | 85464 | 10 |
| /car-reference/geely/starray-15t-7dct-egypt/ | 85466 | 10 |
| /car-reference/chery/tiggo9-phev-2026-egypt/ | 85535 | 10 |
| /car-reference/mg/new-hs-15t-luxury-hybrid-egypt/ | 85851 | 7 |
| /car-reference/chevrolet/captiva-2026-egypt/ | 85149 | 7 |
| /car-reference/nissan/magnite-2026-egypt/ | 85094 | 7 |
| /car-reference/nissan/patrol-y63-egypt/ | 85654 | 7 |
| /car-reference/mg/mg-gt-15t-egypt/ | 85148 | 6 |

## FINAL VERIFIED RESULT — 2026-11-21

These are the latest verified counts. Supersede earlier intermediate counts in this file.

- 393 / 393 legacy car-reference fact URLs: live HTTP 301, correct target and anchor.
- 52 / 52 model hubs: index/follow, self canonical, accessible.
- Car-reference XML sitemap reduced from 456 to 63; all 393 old URLs absent, all 52 hubs present.
- Full QA: https://github.com/marwanile1-cyber/a3tal/actions/runs/44912432183
- 304 exactly repeated generic advisory paragraphs removed across consolidated hubs; all technical sections retained.
- All original children and model hub contents saved in GitHub Actions artifacts, no mass deletion.

### Extra batches now complete
- Jetour T2 i-DM, Opel Frontera, Renault Boreal: 29 redirected sources, 3 hubs, https://github.com/marwanile1-cyber/a3tal/actions/runs/44911351892
- Kia and MG 10 hubs: 62 sources, https://github.com/marwanile1-cyber/a3tal/actions/runs/44911480279
- Nissan and Renault 10 hubs: 59 sources, https://github.com/marwanile1-cyber/a3tal/actions/runs/44911771853
- Remaining 13 model hubs: 52 sources, https://github.com/marwanile1-cyber/a3tal/actions/runs/44912070039
- Last exact boilerplate dedupe: 55 paragraphs, https://github.com/marwanile1-cyber/a3tal/actions/runs/44912299530

### Internal linking and plugin template fix
- The first read-only post+reference scan found 997 outdated links in 32 indexable model guides (source content), https://github.com/marwanile1-cyber/a3tal/actions/runs/44912690489
- All 997 href attributes updated to link directly to the correct canonical model section, in 32 guides, full original HTML backups preserved, https://github.com/marwanile1-cyber/a3tal/actions/runs/44913356949
- A later read-only scan confirmed 0 links to any of the 393 redirected fact cards across 635 sitemap-listed regular posts and 62 reference archive/model records, https://github.com/marwanile1-cyber/a3tal/actions/runs/44913486278
- Live single and archive templates of the car-reference plugin were surgically patched via GitHub + A3tal Direct Bridge with expected SHA validation and PHP lint. They now omit children marked with _yoast_wpseo_meta-robots-noindex=1 in linked cards/search output. Backups retained, https://github.com/marwanile1-cyber/a3tal/actions/runs/44913163162
- CRITICAL DEPLOYMENT NOTE: Production plugin code had pre-existing drift from plugin-source/a3tal-car-reference in GitHub: the live main plugin PHP contains extra Yoast OG image handlers, and live single.php had an older facts-table guard. The work above preserved production differences and patched only two live templates. DO NOT redeploy the old plugin-source ZIP or rerun deploy-a3tal-car-reference.yml until its source is reconciled with current live plugin content; otherwise it may reverse these fixes or erase existing OG behavior. Read-only SHA/diff check: https://github.com/marwanile1-cyber/a3tal/actions/runs/44913066898

### Ordinary articles
- Compared 636 of 637 sitemap-listed published article bodies and titles; 8 broad title-similarity pairs surfaced, most are distinct models, marques or new/used search intent. No mass redirects based on title similarity. https://github.com/marwanile1-cyber/a3tal/actions/runs/44912349884
- Two brake-fluid DOT 3/4/5.1 guides had matching intent; the short duplicate was noindexed and permanently redirected to the comprehensive version, with a unique safety clarification moved and the original preserved: https://github.com/marwanile1-cyber/a3tal/actions/runs/44912578853

### Still needed for measurable organic-search recovery
- Fresh first-party GSC export with date + query + page to measure query loss and identify genuinely competing articles. The 92-day aggregate export cannot establish this.
- Evaluate a stable period at least one week after Google officially completes the November 2026 Core Update. Do not attribute traffic recovery to these changes without measured data.
- Review the current on-site plugin-source drift before any future car-reference plugin deployment.


## POST-393 FOLLOW-UP QA — 21 November 2026 (Egypt only)

Read-only public verification completed in two additional workflows; this section supersedes preliminary concerns about legacy broken URLs and DTC robots mismatch:

1. [Residual DTC and redirects](https://github.com/marwanile1-cyber/a3tal/actions/runs/44914635806): 14/14 specifically listed legacy 301 sources return the intended direct permanent targets. The live post XML sitemap contains 636 entries, DTC XML contains 235 URLs (234 individual code pages plus its archive), car-reference XML contains 63 URLs. The tested DTC noindex samples P0342, P0420, and P0335 are *not* in the XML sitemap. No sitemap-listed individual DTC code page was found noindexed, noncanonical, or non-200 by the audit.
2. [Fourteen-source internal-link and XML audit](https://github.com/marwanile1-cyber/a3tal/actions/runs/44915633700): none of the 14 redirected legacy sources is present in any of the eight checked Egypt sitemaps (posts, pages, DTC, car-reference, service centers, showrooms, cars, categories). Scanned REST records: 650 posts, 13 pages, and 455 car-reference records. Only **two stale href attributes** were detected, each **inside another already 301-redirected former Mansour post**, IDs 81108 and 79906; they are not active links from the retained indexable destination pages. Source pages are archived as 301 redirects, so these two stored-content references do not warrant an extra redirect or rewriting live canonical content.
3. [Previously verified 393 model-spec redirects and 52 hubs](https://github.com/marwanile1-cyber/a3tal/actions/runs/44912432183) and [post-rewrite link rescan](https://github.com/marwanile1-cyber/a3tal/actions/runs/44913486278) remain successful. The 997 href changes targeted only the old 393 fact-card children, distinct from the 14 legacy redirects checked above.
4. Ordinary article similarity audit found 8 title-based pairs among 636/637 then-current sitemap-listed articles. The one true DOT3/DOT4/DOT5.1 duplication was merged and redirected. The other highlighted pairs compare different models or explicitly distinct purchase states, **not proven same-query competition**. Avoid new 301 based on titles alone.

**Decision on this tested scope:** zero additional 301 rules or changes to retained Egypt model hubs are justified by this audit. This is **not** a claim of universal no-cannibalization: a settled-date GSC query+page export is still required to prove or disprove competing live article URLs for the same queries. The account's GSC Wizard read access currently returns `payment_required`, and the available 92-day aggregate workbook does not map each query to every landing page. Do not turn this limitation into speculative bulk redirects.

**Coverage note:** custom service-center and showroom REST routes under guessed `/wp/v2/a3_service_center` and `/wp/v2/a3_showroom` returned 404 (unsupported REST endpoints), so their content hrefs were not inspected; their public sitemaps were inspected and were clean of the 14 legacy source URLs. This gap cannot be described as full internal-link completeness for those custom types.

**Revisit only on new evidence:** (i) one exact query returning multiple indexable Egypt pages with conflicting intent or (ii) newly discovered 301 failure or live internal links from canonical indexable pages to retired URLs. No page deletion or redirect expansion is authorized by the present evidence.


## EXACT-INTENT POST REMEDIATION — 21 November 2026 (follow-up)

Confirmed sitewide active-post semantic review and targeted fixes **within Egypt only**.

- [Read-only audit before changes](https://github.com/marwanile1-cyber/a3tal/actions/runs/44916869504): 635 active REST article records matched to then-live 636 `post-sitemap.xml` entries. 62 *automatically similar title/heading/body pairs*, **not** 62 proven keyword cannibalizations. No exact normalized focus-title duplicates.
- Manual review of active public content found **four same-intent duplicate article pairs**. All four old pages were archived as Yoast `noindex` with canonical to the chosen primary and persistent direct **HTTP 301** redirects through A3tal Direct Bridge; each primary returns 200. Existing bodies are not deleted; original source+target post contents are stored as GitHub Actions artifacts for rollback. Primary bodies were not automatically overwritten with concatenated text.
- Three pairs and their exact live 301 verification: [GitHub run 44917091817](https://github.com/marwanile1-cyber/a3tal/actions/runs/44917091817). Details:
  1. `/humming-noise-increases-with-speed-wheel-bearing-tires-gearbox/` -> `/wheel-bearing-humming-noise-diagnosis/` (old post 82596 -> retained 81463; historical aggregate GSC 8 clicks vs 31 for retained).
  2. `/car-overheats-in-traffic-cools-when-driving-fan-thermostat-diagnosis/` -> `/car-overheats-in-traffic-cools-while-driving/` (old 84754 -> retained 82480; retained had three historical clicks while source not in top-1000 export).
  3. `/car-battery-parasitic-draw-diagnosis/` -> `/car-battery-drains-overnight-while-parked-parasitic-draw-diagnosis/` (old 81395 -> retained 84487; retained had three clicks in historical top-1000 export; newer canonical also covers battery/alternator and safe parasitic-draw diagnosis).
- Fourth pair: `/opel-insignia-spare-parts-prices-guide-egypt-2026/` (post 80144, historic 12 clicks) -> `/أسعار-قطع-غيار-أوبل-انسيجنيا-2025-دليلك-ال/` (post 79933, historic 80 clicks). [Verified 301 run 44917312486](https://github.com/marwanile1-cyber/a3tal/actions/runs/44917312486). Both source and destination original content backed up.
- [Link cleanup after the first 3 redirects](https://github.com/marwanile1-cyber/a3tal/actions/runs/44917205181): **10 old href attributes in 10 indexable posts replaced directly with final 200 URL**; revisions preconditioned, backup JSON stored, all edits verified.
- [Link cleanup after the 4th redirect](https://github.com/marwanile1-cyber/a3tal/actions/runs/44917368258): **two more old href attributes in two indexable articles corrected**. Total new-round internal href repairs: **12 in 12 posts**; zero advanced-HTML skips.
- [Re-run of live semantic audit after the four merges](https://github.com/marwanile1-cyber/a3tal/actions/runs/44917395086): 632 entries in `post-sitemap.xml`; 631 of those are active WordPress articles. Remaining **58 high-level similarity candidates**, none auto-proven to share the same search intent just by a similarity score. Strongest apparent matches compare different car variants (XPENG G7 vs P7+), new vs used Skoda, Jetour X70 vs X90, different manufacturers for DTC P0171, or parent vs child (e.g. general transmission faults vs valve-body specific). These should **not** be mass-redirected absent actual query-page overlap evidence.
- [One unmatched sitemap URL inspected directly](https://github.com/marwanile1-cyber/a3tal/actions/runs/44917484594): the one non-REST-entry in `post-sitemap.xml` is the **homepage** `https://a3tal.com/`, HTTP 200, self canonical, index/follow. It is not a hidden competing article. All four newly retired URLs are **absent** from this 632-entry sitemap.
- The standalone GSC worksheets from 15 November 2026 show aggregate keywords and URLs separately, not query-page-date rows. Historical 92-day clicks listed above guide which primary to retain but **do not prove recent impressions or diagnose Google's November update**. The connected Semrush `resource_organic` report returned `API UNITS BALANCE IS ZERO` on this audit; GSC Wizard returned `payment_required` earlier. No claim of complete live Google query cannibalization is possible without a suitable query/page/date export.

**Current confirmed totals:** 393 original model facts redirect correctly to 52 retained hubs, plus the previously verified 14 legacy redirects, plus 4 additional *new* same-intent article redirects in this follow-up. These are different groups; do not label all of them as part of the `393`. 12 internal hrefs to the four newest retired URLs were repaired. Four original source articles are archived/redirected, not destroyed, and their prechange snapshots are in the respective Actions artifacts. Only further precise evidence should justify additional 301 rules.


## SECOND-PASS LIVE INTERNAL HREF AUDIT — 21 November 2026

A subsequent targeted audit expanded beyond the prior 393 and the later 18 legacy rules. The [read-only all-active-article internal-href report](https://github.com/marwanile1-cyber/a3tal/actions/runs/44918025205) inspected 631 sitemap-listed WordPress posts, 10 pages, and 62 sitemap-listed car-reference records (post-sitemap 632 includes the homepage); unknown links from other custom types remain outside its scope.

**Before latest repairs** 46 distinct internally linked paths were absent from the eight enumerated sitemaps. Live network checks returned: 16 direct HTTP 200 paths, **12 redirecting paths with 60 total stale internal hrefs**, and **18 HTTP 404 paths referenced 25 times**. Direct 200 URLs absent from a sitemap are not automatically broken; redirect and missing status are concrete.

**Nine safe redirect-source families corrected:** [successful live A3tal Direct Bridge run 44918185898](https://github.com/marwanile1-cyber/a3tal/actions/runs/44918185898): 9 historical 301 source paths with semantically appropriate current targets and verified live HTTP 301→200, self canonicals and indexability. A total of **37 old hrefs were replaced in 28 active Egypt posts**, all 28 posts verified after the write and originals backed up. Main source clusters:
- `/obd2-freeze-frame-data-guide/` (11 hrefs) and `/freeze-frame-obd2-diagnostic-data/` (1) → `/freeze-frame-obd2/`.
- `/obd2-live-data-reading-guide/` (11) and `/live-data-obd2-scanner-readings-guide/` (1) → `/live-data-obd2/`.
- `/engine-overheating-causes-solutions/` (9) → the canonical indexed generic car-engine overheating guide `/ما-هي-الأسباب-الشائعة-لسخونة-محرك-السي/`.
- Another 4 one-href equivalent links were fixed: oil consumption without visible leak, Geely Starray maintenance, Opel P03A3 to canonical code, and P0171 to its canonical diagnostic guide.

**Three NOT SAFE for blind target link rewrite:** 23 remaining old hrefs across `/p0300-random-misfire/` (17), `/p0011-camshaft-timing-over-advanced/` (3) and `/p0342-camshaft-position-sensor-circuit-low/` (3). These three redirects resolve to Chevrolet, Hyundai and Chevrolet articles respectively, although the source anchors can refer to generic P0300/P0011/P0342 OBD-II codes and even from other manufacturers' posts. Redirects technically return a success status but manufacturer-specific targeting is not proven appropriate for all linking contexts; do not rewrite generic anchors to the brand-specific destinations en masse. Preserve existing rules until code-specific global page intent and GSC query/page evidence are verified; potential brand/general intent split is a distinct SEO priority.

**Broken-link inventory** (from the same read-only run): 18 distinct 404 paths linked 25 times. A [separate read-only contextual anchor + destination QA run](https://github.com/marwanile1-cyber/a3tal/actions/runs/44918320054) inspected exact in-article anchor text and independently validated live 200, self-canonical, indexable and in-sitemap destinations for 11 mapping candidates. These are **verified candidates, not applied repairs**:
1. `/engine-oil-change-cost-prices-egypt-2026/` (3 anchors, all specifically describing oil selection/change) → `/engine-oil-change-guide-egypt-2025/`.
2. `/toyota-cvt-fluid-fe-vs-tc/` (2) → `/toyota-cvt-fluid-price-egypt-fe-vs-tc/`.
3. `/cars-prices-egypt-2026-local-imported/` (1; anchor actually mentions *economical* new cars) → the more precise `/new-economical-car-prices-egypt-2026-encyclopedia/`, not the broader car-prices hub.
4. `/check-injection-renault-causes-solutions/` (1) → `/renault-fault-codes-check-injection-solution/` (must preserve the explicit Check Injection anchor; destination contains that section).
5. `/parasitic-battery-drain-test/` (1) → `/car-battery-drains-overnight-while-parked-parasitic-draw-diagnosis/`.
6. `/toyota-corolla-maintenance-schedule-egypt/` (1) → `/toyota-corolla-maintenance-prices-guide-2026/`.
7. `/أسباب-اهتزاز-السرعات-العا/` (1) → `/رجة-في-السيارة-على-سرعة-80-أو-100-أو-120/`.
8. `/أسعار-قطع-غيار-أوبل-انسجنيا-2025-دليلك-ال/` (1, spelling variant) → `/أسعار-قطع-غيار-أوبل-انسيجنيا-2025-دليلك-ال/`.
9. `/أعراض-تلف-افتيس-الأوتوماتيك/` (1, typo) → `/الدليل-الشامل-أعراض-تلف-الفتيس-الأوتو/`.
10. `/عالم-أكواد-أعطال-السيارات-dtc-موسوعة-شامل/` (1) → `/dtc/` indexable code archive.
11. `/أعطال-طرمبة-البنزين/` (1; broad fuel pump title) → `/fuel-pump-low-pressure-how-to-test-before-replacement/` covers pressure diagnosis but is narrower. **Hold pending manual contextual adjustment** rather than pretending both have identical breadth.

**Unmatched broken intent paths:** `/electric-car-problems-egypt-guide/` (3), `/كورس-كهرباء-السيارات-دليلك-للاحتراف-م/` (3), `/hyundai-tucson-engine-gearbox-repair-costs/` (1), `/hyundai-tucson-2026-2027-used-price-buying-guide-egypt/` (1), `/car-ac-hot-at-idle-cold-driving-causes/` (1), `/tire-rotation-service-cost-egypt-2026/` (1), `/لمبات-أعطال-السيارات-ومعانيها-بالصور/` (1). Leave these untreated until a real matching page exists, a justified 301 is verified, or the original article anchor can be safely rewritten without dead links.

**Original content retention review:** [successful read-only comparison](https://github.com/marwanile1-cyber/a3tal/actions/runs/44917972463) examined the four recent redirected post pairs and archived heading/section-level differences in Actions artifacts. Source bodies remain available in backups; heading disparities are only a cue for editorial migration, not proof that unique content was irretrievably lost. In particular verify P0480/P0483/P0117 troubleshooting in the traffic-overheating retained article and multimeter/Sleep Mode/Voltage Drop precautions in the parked-battery retained article before claiming the four merges are editorially complete.

**This session's confirmed new modifications:** only the nine-family internal-href repair (37 hrefs in 28 active posts) was successfully persisted and verified. The 404 source-to-destination options were **read-only checked and recorded, NOT applied**; a subsequent attempted write workflow was blocked by tool safety checks, so no 404 edit should be claimed. The earlier four article 301s and 12 href repairs remain as previously documented. Do not broaden 301 rules merely to hide broken article links.


## DTC INDEXABILITY VERIFICATION FOR THE 23 RESIDUAL HREFS

[Successful live read-only check](https://github.com/marwanile1-cyber/a3tal/actions/runs/44918526333) confirmed that the 23 active internal hrefs pointing to three generic old URLs should **not** be blindly rewritten to guessed `/dtc/{code}/` pages:
- `/dtc/p0300/`: HTTP **404**, not in code sitemap, after the generic slug `/p0300-random-misfire/` returns 301 to a Chevrolet-specific guide. 17 old hrefs remain pending contextual editorial repair.
- `/dtc/p0011/`: HTTP **404**, not in code sitemap, after generic `/p0011-camshaft-timing-over-advanced/` returns 301 to a Hyundai-titled guide. 3 old hrefs remain pending.
- `/dtc/p0342/`: HTTP **200 but `noindex,follow`**, self canonical, absent from XML. Generic old `/p0342-camshaft-position-sensor-circuit-low/` goes by 301 to indexable Chevrolet article. 3 old hrefs remain pending.

**Decision:** Protect the site's existing indexing strategy. Do not insert links to a 404 or noindex generic DTC entry and do not automatically direct arbitrary car manufacturers' links to a Chevrolet/Hyundai-titled page. A deliberate generic-vs-brand code landing strategy (including title/content, indexability, GSC intent and links) is the next prerequisite before changing these redirects. No production 301 or DTC sitemap entry was changed by this check.


## FINAL LINK-STATUS RECHECK AFTER 25 DEAD-HREF REPAIRS

Follow-up execution completed via GitHub + A3tal Direct Bridge in Egypt only. **This section supersedes the earlier pending-404 inventory**, without changing the separate generic DTC redirects.

- [First 404 cleanup run](https://github.com/marwanile1-cyber/a3tal/actions/runs/44918741753) succeeded: **13 stale hrefs fixed across 13 retained indexable posts** using exact live HTTP 404 source and HTTP 200 selfcanonical/indexable target guards. Original article bodies and affected IDs backed up in the corresponding Actions artifact. Matched intents included CVT Toyota FE/TC, Corolla service schedule, Renault Check Injection, engine oil change, the parked battery parasitic draw test, vibration-at-speed, an Opel Insignia URL typo, general transmission faults and the DTC index.
- [Second 404 cleanup run](https://github.com/marwanile1-cyber/a3tal/actions/runs/44918965142) succeeded: **10 hrefs fixed across 8 indexable posts**. Search of all 631 indexable WordPress post titles located exact same-intent matches that had been missed by the original candidate mapping: published EV troubleshooting guide, car-electrics learning roadmap, A/C weak at idle, tire rotation schedule/technique, dashboard warning lights, and fuel-pump symptoms vs filter. These are **href rewrites only**, no invented new 301s.
- [Tucson contextual anchor fix](https://github.com/marwanile1-cyber/a3tal/actions/runs/44919092066) succeeded: last **2 dead hrefs inside post 80567** updated after replacing misleading anchor labels with target-accurate text: used Tucson buying/prices link and Hyundai Tucson NX4 DCT diagnosis link. Original Tucson body backed up.
- [Independent second-pass internal URL crawler after all fixes](https://github.com/marwanile1-cyber/a3tal/actions/runs/44919146560) succeeded, checked **631 sitemap-listed WordPress posts, 10 sitemap-listed pages, and 62 sitemap-listed car-reference records** against eight Egyptian sitemaps. Found **zero HTTP 404/410 linked internal paths and zero broken href occurrences** in that scanned scope. Previously: 18 unique dead source paths / 25 dead href occurrences. After repair: 19 unlisted internal paths remain, of which 16 are HTTP 200 and three are HTTP 301. Exact outstanding **23 redirected hrefs**, split by P0300 17, P0011 3, P0342 3.
- [Read-only anchor-by-anchor audit of those 23 links](https://github.com/marwanile1-cyber/a3tal/actions/runs/44919222563) confirmed that the anchor text is about the **generic fault code**, e.g. generic P0300 from a Kia Cerato article, generic P0011 from Toyota Corolla, and P0342 from broad camshaft sensor articles. Do not rewrite all of them to brand-specific Chevrolet or Hyundai landing pages. The existing 301 rules do resolve successfully but the generic-vs-brand search intent mismatch remains **unresolved**. The generic `/dtc/p0300/` and `/dtc/p0011/` are 404, and `/dtc/p0342/` is 200/noindex, so do not insert those as replacements either.

**Summary as of this verification:** this post-393 work verified 4 article-duplicate 301s and repaired **74 total internal hrefs**: 12 stale hrefs following the four new duplicate redirects + 37 previously redirecting but semantically matched hrefs + 25 dead hrefs. No 404 remains in the scanned live/root post/page/reference content. The 393 historical fact-card internal href repairs (997) are an independent earlier campaign, not included in the new 74 count.

**Caveats:** This crawl does not cover every template-driven/navigation link or custom service-center/showroom post content whose REST endpoints are unavailable. Also the 23 generic-code-to-brand redirects are **not** a clean SEO resolution and need deliberate landing-page intent planning, ideally with query/page/date Search Console export. No unverified SEO traffic gains are claimed.


## LATEST EGYPT CLOSEOUT — 23 GENERIC DTC HREFS AND 3 CANONICAL CONTENT GAPS

Date: 21 November 2026. Scope strictly the Egyptian root `a3tal.com` project, not the separate `/ksa/` installation.

### Decision: preserve existing successful P0300/P0011/P0342 canonical URLs

The [three-code public content comparison](https://github.com/marwanile1-cyber/a3tal/actions/runs/44919778405) showed that their brand-titled current canonical landing pages contain **general cross-make diagnostic information**, while the old generic articles are substantially overlapping archives with 301 redirects:

- Former `/p0300-random-misfire/` (post 81329, ~1,756 words, off sitemap) and retained `/فك-لغز-كود-العطل-p0300-في-شيفروليه-دليل-التش/` (post 79856, ~1,784 words) share the same major general-code headings. The retained page is indexable, HTTP 200, self-canonical. Its brand-specific title can be editorially evaluated separately, but should not be changed solely from this link crawl.
- Former `/p0011-camshaft-timing-over-advanced/` (post 82275, ~1,356 words, off sitemap) points to retained `/كود-p0011-سيارات-هيونداي/` (post 114, ~2,936 words), whose published headings explicitly discuss generic meaning and examples for Hyundai, Nissan, Toyota and VAG. No justification to revive a near-identical generic competing page.
- Former `/p0342-camshaft-position-sensor-circuit-low/` (post 82276, ~2,067 words, off sitemap) points to retained `/dtc-p0342-chevrolet/` (post 80209, ~2,732 words). The canonical has general sensor circuit / Bank / diagnosis details plus Chevrolet examples; is indexable, selfcanonical and HTTP 200. Generic `/dtc/p0342/` remains noindexed. Do not create a duplicate without query-by-page evidence.

The available historical 92-day Google Search Console export showed *retained canonical clicks* of **30 P0300**, **58 P0011**, **90 P0342**; these numbers are **not** recent recovery claims. Thus avoid modifying their successful 301 source rules or page-title targeting without newer query-page evidence.

### 23 direct internal href corrections verified

[Successful workflow run 44919957228](https://github.com/marwanile1-cyber/a3tal/actions/runs/44919957228): all **23 direct internal href references** to the three old, already redirecting generic-code source paths were updated in **22 published articles**. Only the `href` attribute changed: links now point directly to the **same destination that the prior 301 already reached**; no shift of landing-page intent was introduced by this change. Guarded preflight confirmed that the existing 200 destination pages are sitemap-listed, selfcanonical and indexable, and contain generic diagnostic sections before editing. Original 22 article bodies are stored in the workflow artifact; all 22 edits reread and verified through A3tal Direct Bridge. Current legacy 301 rules, SEO title, canonical and original archived content left unchanged. Residual opportunity: the destinations' visible brand-titled H1/SEO titles may not match some generic-code anchor expectations, but cannot be resolved by creating immediate duplicate pages.

[Independent final root internal URL status crawl 44920060803](https://github.com/marwanile1-cyber/a3tal/actions/runs/44920060803): **ZERO internal redirect hrefs** and **ZERO internal HTTP 404/410 hrefs** among the scanned live public article/page/reference bodies. Detailed inventory: 631 active WordPress posts, 10 sitemap-listed pages, 62 sitemap-listed car-reference records; eight sitemaps. There were 16 internally linked paths not found in those eight XML inventories, **all 16 HTTP 200** (31 href occurrences total). Not a claim for sitewide template assets/custom service-center bodies which were outside REST coverage.

Updated post-393 href repair subtotal: **97** = 12 after four article-duplicate 301s + 37 earlier semantically matched legacy-301 hrefs + 25 repaired dead hrefs + 23 three-generic-code 301 hrefs. The earlier **997** car-model child redirect internal hrefs are a separate campaign; don't mix counts.

### Unique archived technical detail preserved without reopening competing pages

[Read-only safety detail comparison 44920122379](https://github.com/marwanile1-cyber/a3tal/actions/runs/44920122379) found several precise diagnostic details absent from retained guide text: workshop-safe 12/6 wheel-play tests and caliper heating vs bearing, fan-control/ECT codes P0480/P0483/P0117, and battery Sleep Mode / fuse Voltage Drop / multimeter caution. Older Opel Insignia source contained a cabin-air-filter price range that was **not** migrated because it is stale/unverified and the primary article already covers main parts-buying intents.

[Successful source-preserving edits 44920270892](https://github.com/marwanile1-cyber/a3tal/actions/runs/44920270892): inserted **one concise missing safety/diagnosis section** into each of three existing, retained Egypt posts while keeping original article HTML, metadata and primary URL:
1. Wheel hub noise article `/wheel-bearing-humming-noise-diagnosis/` (post 81463): safe lifting/12-and-6 check limitations, ball-joint differentiation and brake-caliper heat.
2. Traffic-overheating canonical `/car-overheats-in-traffic-cools-while-driving/` (post 82480): P0480/P0483/P0117 distinction, electrical tests, cooling-system refill/bleed and hot-pressure-cap warning.
3. Parked-battery-drain canonical `/car-battery-drains-overnight-while-parked-parasitic-draw-diagnosis/` (post 84487): Sleep Mode, fuse Voltage Drop, module wake-up and multimeter ammeter-current safety.
All three pre-change live full post bodies were backed up with WordPress modification timestamps and edits verified after saving, no speculative external price figures. Supporting specialist references inspected: Fluke parasitic drain guide `https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-find-parasitic-battery-drain-with-a-multimeter`; HELLA cooling system diagnostics `https://www.hella.com/techworld/uk/technical/car-cooling-system/cooling-system-check/`; MOOG wheel/suspension checks `https://www.moogparts.com/technical/bulletins/tech-tips/How-to-Isolate-Suspension-Noises.html`.

[Independent live HTTP/content verification 44920348693](https://github.com/marwanile1-cyber/a3tal/actions/runs/44920348693): each of the three former source URLs **remains HTTP 301 to the intended primary**; all three retained pages **HTTP 200, selfcanonical, indexable and in the post XML sitemap**; and the new technical details were verified in publicly rendered HTML. 3/3 pass.

### What is *not* proved

The remediation does not establish an increase in Google organic clicks or that the full site is free of all semantic cannibalization. The prior 58 article similarity candidate pairs remain largely model-distinct; live query-to-page-to-date GSC export is still needed before wider 301 reorganization. No new redirects were invented in this closeout and no `/ksa/` installation was touched.


## NON-POST SITEMAP CRAWL AND SERVICE-CENTER DIRECTORY 301 CARD FIX — 2026-11-21

The 97 individual WordPress internal href changes and three retained-guide safety restorations were followed by an independent review of the public **non-post XML-listed material** to catch template-generated links invisible to `/wp-json/wp/v2/posts`.

- [Read-only custom-content audit](https://github.com/marwanile1-cyber/a3tal/actions/runs/44920480171): **375 public URLs**, all HTTP 200 when fetched: 235 DTC, 63 car-reference, 14 service-center, 11 showroom, 8 car, 33 category and 11 WordPress page URLs. The `post-sitemap.xml` remained separately covered by the earlier 631-post article scan. Inspected `main`/article link markup excluding nav/header/footer and compared with eight known sitemap sets. Of 83 non-sitemap internal paths, the first request saw 78 direct 200, three existing 301 sources with **six total href occurrences** on the service-center archive, one Cloudflare email-protection path `/cdn-cgi/l/email-protection/` reported 404 at non-JS HTTP level and one `/cars-for-sale/` initially reported HTTP 500. Neither of the latter two is evidence for a new 301 rule.
- [Read-only live template SHA/market recheck](https://github.com/marwanile1-cyber/a3tal/actions/runs/44920775728) verified that live source `themes/a3tal-global/ux-improvements-20261031.php` **exactly equaled** the repository source at SHA256 `937cfc04de75e74ac1a0bcd44cf7787be1a85bcd6303d9f85ce3d6f29d16db0b`, as did the archive directory and market templates. `/cars-for-sale/` was directly probed **three more times** under cache-busting parameters: **3/3 HTTP 200**, correct marketplace title, not a reproducible 500. Thus no redirect or speculative PHP fix was applied for the apparent transient error.
- The remaining real template-generated issue was isolated to `a3g_ux_directory_guides()` in `ux-improvements-20261031.php`: it used a query for *published* category-33 posts and did not exclude the three previously retired Ghabbour/Mansour guides nor Yoast-noindexed article records. This let `/service-centers/` display two card links each to `/mansour-chevrolet-maintenance-booking-numbers-branches/`, `/مركز-خدمة-منصور-شيفروليه-الرئيسي-في-ال/`, and `/دليلك-الشامل-أفضل-مراكز-خدمة-غبور-أوتو/`; all three sources correctly 301 to their retained destinations. The primary archive's manually curated shortcut links already pointed to retained pages.
- [Successful guarded live theme repair run](https://github.com/marwanile1-cyber/a3tal/actions/runs/44920960019): patched *only* `theme-source/a3tal-global/ux-improvements-20261031.php` and deployed exactly that theme file through GitHub + A3tal Direct Bridge. Within the archive guide filter, skip records with Yoast noindex meta and three specified retired dealer slugs. Pre-deployment compared full live file SHA to exact known source and PHP-linted the new source; archived the entire previous live file; Bridge `file_write` used `expected_sha256` and reread the resulting file. Cache flushed. Live independent archive request returned **HTTP 200**, **48 current card anchor elements** with **zero hrefs** to the three retired sources, verified with a cache-busting request.
- Cloudflare `/cdn-cgi/l/email-protection/` is a platform-managed obfuscated-email link that plain HTTP scanning can report as 404 even though browser JS may resolve it. Do not bulk-replace this as an ordinary missing content article or create a 301. Actual user-browser click behavior requires a separate browser-level audit if the mail links are business-critical.

**Cumulative editorial/link update accounting:** four earlier newly verified same-intent article 301 rules, 97 rewritten direct internal article hrefs from the last follow-ups (the 997 older model fact-card hrefs are a distinct campaign), three retained guides with restored unique diagnostic warnings, and the just-deployed archive-level template filter eliminating six visible old redirect card links. Do not add the six template links to the 97 stored post-body hrefs (they are different sources of markup). This work is not proof of Search Console ranking recovery; it specifically improves internal crawl efficiency and indexing clarity.
