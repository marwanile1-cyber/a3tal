# A3TAL CODE LAB | Arabic OBD-II library expansion

## Product position
An original Arabic diagnosis reference for motorists in Egypt and the Arab region, inspired by the usability of OBD code reference directories, without translating or replicating another site's articles or artwork.

## Published before this program
As checked 2026-10-12: 44 code entries in /dtc/. Existing codes are owned by their original indexed URLs; do not duplicate/repost them. The initial checked inventory included P0000, P0010, P0011, P0013, P0014, P0016, P0087, P0101, P0110, P0114, P0115, P0128, P0135, P0171, P0172, P0226, P0299, P0300–P0304, P0335, P0340, P0342, P03A3, P0420, P0430, P0442, P0455, P0507, P0562, P0597, P0700, P0741, P1083, P1115, P1299, P1632, P2288, C1010, U0100. Verify live state before later publishing.

## Batch 01 | original full guides, started 2026-10-12
P0102, P0113, P0122, P0133, P0401, P0441, P0456, P0500, U0121.
Files: data/dtc-original-batch-01.json and scripts/publish-dtc-original-batch.py.

## Batch 02 | ten reviewed original pages
P0103, P0106, P0107, P0108, P0117, P0118, P0121, P0123, P0130, P0174.
Files: data/dtc-original-batch-02.json and scripts/publish-dtc-original-batch-02.py.
P0112 was deliberately omitted: the existing indexed multi-code article already covers P0110 through P0115, so adding a separate P0112 page would risk competing with that guide.
Status: automated live publishing initiated on 2026-10-12; individual URLs must be verified after GitHub Actions finishes.

## Batch 03 | confirmed published
P0200, P0201, P0325, P0336, P0351, P0606, P0715, P0720, P0730, P0750.
Files: data/dtc-original-batch-03.json and scripts/publish-dtc-original-batch-03.py.
Published live 2026-10-12 and independently verified all 10 URLs with index/follow. GitHub run: https://github.com/marwanile1-cyber/a3tal/actions/runs/38249377691.
Catalog after batch: 72 accessible code explanations. Search for P0200 and P0750 returned one result apiece.
Host failure note: initial write of P0200 returned HTTP 522, but live WP article existed; never blindly repeat an ambiguous mutation. Production content identity verified through authenticated WP REST and checked public routes.

## Batch 04 | publication triggered 2026-10-12
P0202, P0203, P0341, P0352, P0365, P0705, P0716, P0722, P0740, P0755.
Files: data/dtc-original-batch-04.json and scripts/publish-dtc-original-batch-04.py.
Primary definitions checked against the Delaware DMV DTC technical code list. These guides cover injectors, camshaft position, ignition and safe automatic transmission diagnosis. Existing pages and prior indexed tutorials are preserved.
GitHub workflow: https://github.com/marwanile1-cyber/a3tal/actions/runs/38253042671.
Status: complete. GitHub Actions succeeded with 10 new published WordPress posts (IDs 83507–83516), and all ten public detail URLs were verified index/follow. The catalog displayed 82 available code explanations after this batch. Exact lookup for P0755 returned one result. Completed 2026-10-12.

## Batch 05 | 10 original Arabic guides
P0204, P0305, P0353, P0403, P0443, P0480, P0756, P0760, U0101, P0521.
Files: data/dtc-original-batch-05.json and scripts/publish-dtc-original-batch-05.py.
Live preflight identified existing P0741 guide at /p0741-torque-converter-clutch-diagnosis/; this code was deliberately excluded to avoid SEO cannibalization, with P0760 selected instead.
Explanations are written originally in Arabic, with symptoms, electrical/mechanical distinction, five diagnostic steps, repair decision, safety and FAQs. P0521 includes a high-priority engine oil pressure stop warning.
Launch: https://github.com/marwanile1-cyber/a3tal/actions/runs/38273911204
Status: completed successfully. GitHub Actions published ten new live entries (WordPress post IDs 83517–83526); all ten public details verified as index/follow. The catalog now displays 92 available explanations. Search for P0521 and U0101 returned exactly one result each, while the original P0741 guide remained indexed and searchable. Completed 2026-10-12.

## Batch 06 | 10 original diagnostics, 2026-10-13
P0131, P0132, P0134, P0141, P0191, P0306, P0402, P0446, P0731, U0140.
Files: data/dtc-original-batch-06.json and scripts/publish-dtc-original-batch-06.py.
Each entry has an original Arabic meaning, system explanation, symptoms, causes, five code-specific diagnostic steps, related code distinctions, repair criteria, safety warning, and three FAQs. Source definitions cross-checked against generic DTC dictionaries and manufacturer service data. All ten live catalog exact lookups returned 0 before publication, avoiding competing legacy URLs.
Run: https://github.com/marwanile1-cyber/a3tal/actions/runs/38416199560.
Status: complete. GitHub Actions run succeeded; all ten detail URLs independently opened and verified as index/follow (four retried successfully after transient host 522/timeouts). The public archive displayed 102 available code explanations on 2026-10-13. U0140 exact-code search returned one result. New WordPress post IDs start at 83539 and include 83548. Older code guides preserved.

## Proposed editorial queue (check the live catalog before each batch)

### Air measurement and fuel
P0103, P0106, P0107, P0108, P0112, P0117, P0118, P0121, P0123, P0130, P0131, P0132, P0134, P0137, P0138, P0141, P0174, P0191, P0192, P0193.

### Ignition, misfire, timing and injectors
P0200, P0201, P0202, P0203, P0204, P0305, P0306, P0315, P0325, P0336, P0341, P0351, P0352, P0365.

### EVAP, emissions and cooling
P0402, P0403, P0404, P0410, P0421, P0431, P0440, P0443, P0446, P0449, P0451, P0452, P0457, P0480, P0496, P0520, P0521, P0597 (existing; do not republish), P0125.

### Gearbox and electrical control
P0560, P0601, P0603, P0606, P0705, P0715, P0716, P0720, P0722, P0730, P0731, P0740, P0750, P0755, P0760, P0868.

### Network / communication
U0001, U0073, U0101, U0109, U0115, U0126, U0140, U0146, U0155, U0401.
Focus on communication checks: power and ground, wiring topology and affected modules, not premature ECU replacement.

### ABS, airbags and body
Specific B/C codes must be checked against make/year and manufacturer service data before claiming a universal definition. Prefer verified generic codes and manufacturer-specific sections. Never present maker-specific codes as universal.

## Mandatory editorial acceptance gates
1. Correct manufacturer-independent DTC definition verified against independent technical sources. Flag manufacturer-specific definitions and variant types.
2. Own Arabic explanation, not translated copyrighted prose. Explain exactly what the ECM/TCM/ABS sees, not merely a named part.
3. Unique symptoms, ranked *possible* causes (never invented statistical probabilities), five code-specific diagnostic checkpoints, interpretation, repair decisions, safety and FAQs.
4. Do not state that the code alone confirms a failed component; do not invent fixed electrical pinouts, voltages, prices or repair costs for all vehicles.
5. One canonical indexable URL per code; existing original indexed guides remain live. Code search and page variants are noindex and canonicalized to the main page.
6. Guest discussion to WordPress moderation; optional verified external YouTube URL only.
7. Publish in reviewed batches, with dry-run and exact slug checks and stop on API/host errors; verify public pages before announcing completion.


## Batch 07 | five reviewed guides with exclusive featured artwork, 2026-10-13
P0137, P0138, P0192, P0193, P0449.
Original text: data/dtc-original-batch-07.json; publisher: scripts/publish-dtc-original-batch-07.py.
Live article IDs: 83549–83553, canonical slugs /dtc/p0137/, /dtc/p0138/, /dtc/p0192/, /dtc/p0193/, /dtc/p0449/.
Run https://github.com/marwanile1-cyber/a3tal/actions/runs/38429319437 completed successfully with five new posts, no duplicates.
Each guide contains code-specific symptoms, realistic differential diagnosis, five diagnostic checkpoints, safety and three short FAQs. Sources are attribution for technical meanings, not copied prose.
Five individually generated original technical illustrations uploaded as attachments 83554–83558 and confirmed as featured media through A3tal Direct Bridge. Image run: https://github.com/marwanile1-cyber/a3tal/actions/runs/38430947788.
The global garage relationship feature provides code links from actual live vehicle records and a generic OBD-II reference hub from brand/model selections. "_a3_verified_dtc_codes" must be paired with an HTTPS "_a3_verified_dtc_source" on a vehicle record to assert a verified specific car/code relationship; otherwise never label general DTCs as known common failures of that model. The matching back-link only appears when verified. Do not add duplicate indexable model-code pages or unsupported year/engine compatibility.


## Batch 08 | publication verified (2026-10-13)
Published after read-only recovery from Cloudflare 522:
- P0105: https://a3tal.com/dtc/p0105/ (83559)
- P0140: https://a3tal.com/dtc/p0140/ (83560)
- P0190: https://a3tal.com/dtc/p0190/ (83561)
- P0205: https://a3tal.com/dtc/p0205/ (83562)
- P0481: https://a3tal.com/dtc/p0481/ (83563)
Publisher successful recovery run https://github.com/marwanile1-cyber/a3tal/actions/runs/38436725158. The status of the five featured artworks must only be marked complete after confirmed upload + post readback + OG image inspection. Image workflow source: scripts/attach-dtc-batch-08-art.py.

## Batch 09 | five drafted, held until Batch 08 image success
P0012 (VVT timing over-retarded), P0206 (injector 6 electrical), P0452 (FTP sensor low), P0506 (idle below target), P0706 (transmission range performance).
Article sources: data/dtc-original-batch-09.json; script: scripts/publish-dtc-original-batch-09.py. Images: scripts/attach-dtc-batch-09-art.py. Dedicated prepublish validation success: https://github.com/marwanile1-cyber/a3tal/actions/runs/38437391269.
Publishing chain gated by success: batch 08 artwork => batch 09 original articles => batch 09 artwork.
Do not call any pending/failed workflow a successful production deployment. Do not associate generic DTCs to specific model-years without an independently verified manufacturer diagnostic reference.


## Production update 2026-10-13, after publication of batch 09
- Batch 07: P0137 P0138 P0192 P0193 P0449, five published, original WebP attached, og:image matches individual featured image (verified via GitHub action #38439638921).
- Batch 08: P0105 P0140 P0190 P0205 P0481, five published with original art and matched og:image (action #38439638921).
- Batch 09: P0012 P0206 P0452 P0506 P0706, five original posts published successfully (action #38440241260, post IDs 83578..83582).
- Batch 09 original art was uploaded, assigned and validated on the post metadata, and Yoast OG verified; the first media pipeline failed only at HTML image display because the live custom template previously limited image display to batch07/08. Theme change to accept all reviewed five-guide batches committed; deployment in progress. On successful scoped theme deployment a safe idempotent batch09 media/OG/display verification workflow retries and must pass before batch10.
- Batch 10 correctly gap-audited against FIXED_EXISTING, replacing the originally considered P0011 P0335 P0340 P0507 P0562 because these were already published. New five: P0017 P0116 P0139 P0234 P0453. Original text in data/dtc-original-batch-10.json. Review + image generation validation passed in action #38442331688. Publish will only follow full success of batch09 artwork+OG HTML audit; all five new codes still subject to live catalog duplicate preflight.
- No manufacturer/year/engine-specific fault associations to be invented from generic OBD explanations; those require references for each link.


## Permanent family diversity policy | 14 October 2026
Do not publish only P-prefix codes. Every five-guide editorial batch must include genuine original content in all four systems when a verified, useful gap exists:
- P: powertrain (engine / transmission).
- U: network, loss of communication, gateways (read originating module, current/historical state).
- C: chassis, ABS/ESP/steering/suspension (OEM code definition and suffix must be confirmed; no presumed make compatibility).
- B: body/interior/airbags/SRS (OEM full suffix matters; do not give DIY probing or disabling advice for pyrotechnic equipment).

Preferred batch mix: 2P + 1U + 1C + 1B; sometimes rotate to 1P + 2U + 1C + 1B. Every new post must pass existing-catalog intent check, include five meaningful checks, source caveat and a unique locally created featured 1200x800 WebP. Featured image must appear in article and match Yoast og:image. A page only gets vehicle-model links when the actual OEM reference confirms applicability to that generation/engine; generic codes are useful references, not automatically "common faults" of each vehicle.

Batch 11 (mixed) published October 14: P0217 / P0463 / U0155 / C0035 / B0001, original posts 83613 through 83617, run https://github.com/marwanile1-cyber/a3tal/actions/runs/38551648148. Featured illustrations run separately and must be verified before declaring fully finished. A3tal archive and model guide filters were updated to read all PBCU letters rather than only powertrain.


## Mixed-family batch 12 | 2026-10-14
Source articles data/dtc-original-batch-12.json; publisher scripts/publish-dtc-original-batch-12.py; unique original art scripts/attach-dtc-batch-12-art.py; release workflows publish-original-dtc-batch-12.yml and publish-dtc-original-batch-12-art.yml.
Balance 2 P + 1 U + 1 C + 1 B:
- P0380: diesel glow plug pre-heater circuit A, never confuse with petrol spark plugs.
- P0530: automotive A/C refrigerant pressure sensor circuit, never infer missing refrigerant or vent pressurised refrigerant.
- U0073: Bus A off and network integrity, do not automatically replace PCM.
- C0040: right-front wheel speed sensor only where OEM ABS reference agrees (not universal); retain suffix, module and VIN caveat. GM/NHTSA technical bulletin is the grounding reference.
- B0010: passenger front Stage 1 airbag SRS, require subcode and OEM verification; absolutely no DIY probing of pyrotechnic initiators.

Published only after live duplicate preflight and full previous-batch image/OG audit. Artwork must be 1200x800 exclusive WebP, set as featured, visible within body and confirmed via Yoast og:image before calling completed. The next batch should rotate to 1P+2U+1C+1B when valuable documented U-code gaps exist, instead of blindly producing another 2P batch.


## Mixed-families batch 13, 2026-10-14
- Published all 5 new codes: P2002 / U0109 / U0126 / C0050 / B0028.
- Original editorial: data/dtc-original-batch-13.json, assembled from independently authored verified drafts data/dtc-batch13-*.json.
- Publisher completed with five created and no duplicates: https://github.com/marwanile1-cyber/a3tal/actions/runs/38558331375
- Exclusive 1200x800 WebP pictures for each, plus Yoast image synchronization and body display audit: https://github.com/marwanile1-cyber/a3tal/actions/runs/38558607486. Do not mark artwork fully complete until run success.
- OEM-specific caveat C0050 right-rear wheel ABS only in applications such as GM with code suffix. B0028 is right side airbag deployment circuit in supported OEM systems, and absolutely no consumer squib/airbag probing instructions.

## Mixed-families batch 14, staged only
- Planned codes P0243 / U0102 / U0129 / C0045 / B0081, preserving 1P+2U+1C+1B.
- Original drafts in data/dtc-batch14-*.json assembled in data/dtc-original-batch-14.json; guarded publisher scripts/publish-dtc-original-batch-14.py; five new original technical illustrations scripts/attach-dtc-batch-14-art.py.
- Five article and five WebP QA workflow successful: https://github.com/marwanile1-cyber/a3tal/actions/runs/38559521771.
- Publishing is gated to successful completion of batch13 artwork and a fresh direct public audit of all five images and Yoast share cards. Never claim batch14 live before publishing log confirms actual post IDs and new slugs.
- B0081 passenger presence system definitions/suffix vary by OEM; use linked GM service bulletin and VIN-specific wording. Do not allow incorrect OEM assumptions to become model-specific links.


## Verified follow-up 14 October 2026
- Batch13 article publication: SUCCESS run 38558331375, post IDs 83649-83653, five created zero duplicates.
- Batch13 1200x800 individually original WebP attachment, post readback, Yoast og:image and rendered image audits: SUCCESS run 38558607486, media IDs 83654-83658.
- Batch14 original 1P 2U 1C 1B: P0243 / U0102 / U0129 / C0045 / B0081. Five original articles staged in data/dtc-original-batch-14.json, five distinct original drawings staged and independently passed run 38559521771.
- Batch14 publishing automatically triggered after successful batch13 art with fresh public audit. Run 38559901880; do not label as published until real success with five new canonical slugs.
- Batch14 art workflow automatically follows successful publication; always require full media/post verification and social OG matching.


## Continuous mixed DTC expansion | batch15 + batch16 | 2026-10-14
Batch 14 completed including post and image/social OG QA: https://github.com/marwanile1-cyber/a3tal/actions/runs/38560193164
Batch15 published five new unique posts (P0421 U0415 C0110 C0161 B0051) with ids 83685-83689, zero repeats: https://github.com/marwanile1-cyber/a3tal/actions/runs/38566562368
Batch15 covers/WebP/Yoast OG are handled separately: https://github.com/marwanile1-cyber/a3tal/actions/runs/38566852717; mark complete only after final all-five HTML/OG audit.
Batch15 safety: C0110 brake pump and C0161 brake switch are qualified by GM manufacturer application. B0051 is especially sensitive: GM DTC service manuals document Deployment Commanded while other diagnostic catalogs may label a center-front-row seatbelt sensor; never publish as a universally identical part, recommend SRS specialist and follow OEM post-collision procedures; do not teach squib probing or crash-data bypass.
Batch16 authored original 1P+2U+1C+1B: P2459 (DPF regeneration frequency), U0131 (EPS module communication), U0151 (restraints module communication), C0550 (brake ECU performance on supported GM systems), B0020 (left-side airbag deployment circuit on supported systems). Five distinct original WebP 1200x800 images and five articles validated: https://github.com/marwanile1-cyber/a3tal/actions/runs/38568262034.
Automatic gate: only after full successful batch15 artwork/OG verified publish batch16; only after successful batch16 post publication attach its five original WebP images, sync Yoast OG and verify visible images. Scripts workflows in repo, do not promise live status until GitHub and public audit confirm.


## DTC original balanced batches 17 and 18 | 2026-10-14
- **Batch16 complete:** five published P2459 U0131 U0151 C0550 B0020, all five 1200x800 WebP covers verified in body, featured images, and social OG. https://github.com/marwanile1-cyber/a3tal/actions/runs/38568826871
- **Batch17 published** five original missing codes (P06DD U0103 U0164 C0265 B0090), five created and no existing duplicate: https://github.com/marwanile1-cyber/a3tal/actions/runs/38571133497. Five unique original images with illustration source scripts/attach-dtc-batch-17-art.py; art workflow https://github.com/marwanile1-cyber/a3tal/actions/runs/38571464828. Only declare media complete on successful public image and OpenGraph audit.
- Batch17 editorial special concerns: P06DD oil pressure control requires stopping with actual low oil-pressure warning; C0265 GM EBCM relay is OEM-specific, not all vehicles; B0090 left frontal impact sensor may have differing subfaults and is always restricted SRS service. No how-to bypass.
- **Batch18 prepared** five original P2101 U0128 U0184 C0561 B0070 guides at data/dtc-original-batch-18.json, five exclusive 1200x800 WebP at scripts/attach-dtc-batch-18-art.py. QA success: https://github.com/marwanile1-cyber/a3tal/actions/runs/38572559038.
- Batch18 publication workflow .github/workflows/publish-original-dtc-batch-18.yml automatically runs only after successful batch17 art and an independently fresh five-post HTML+OG audit; media workflow only after successful batch18 publication. Do not count batch18 as live until it reports five newly created canonical slugs and art QA success.
- IMPORTANT: C0561 has manufacturer-dependent meanings; detailed article explicitly limits System Disabled Information Stored interpretation to relevant GM EBCM setups and calls for full OEM suffix. B0070 references a pyrotechnic belt pretensioner: no live electrical circuit testing advice.
- **Longer-term:** build truly useful vehicle-specific owner pages from validated OEM/year/engine evidence and cite it. Do not hallucinate that a generic code is a frequent fault of any model just because that model can use OBD. Add verified model links only where source evidence exists.
