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
