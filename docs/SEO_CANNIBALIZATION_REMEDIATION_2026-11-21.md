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
