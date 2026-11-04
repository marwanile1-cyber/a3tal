# A3tal homepage V4 encyclopedia preview

Status: **draft branch only; no live deployment**.

## Goal
Promote the existing verified /car-reference/ section on the homepage and in the header navigation, keeping the current car-price/editorial, DTC, ownership, motorcycle and services sections alive.

## New modules
- Editorial hero with intent-aware search tabs: vehicle /, verified reference /car-reference/, DTC /dtc/, price search /.
- Four high-priority entry cards.
- Six paths to existing sections.
- Technical-reference panel with live post-count via WordPress.
- Three existing, published model records, resolved by get_page_by_path with actual featured photos.
- Five existing published brand pages, omitted automatically if not present.
- Mobile dock: reference replaces Services shortcut, while services remains in menu and other sections.
- Desktop nav: direct technical reference entry instead of Compare; comparisons remain in Cars dropdown and homepage.

## Non-goals
- No new technical PSEO posts, fabricated specs or unverified prices.
- No changes to individual post SEO, meta, canonicals, or gallery images.
- No autoplay video, maps, or hero slider.

## Checks before production
1. Review the visual prototype in desktop and mobile.
2. Pass PHP lint, JS syntax, and SEO-preservation CI.
3. Test browser widths 390, 768, 1024, 1440 with actual WordPress output.
4. Confirm three reference models and five brand pages resolve to published posts.
5. Confirm a single H1, correct canonical/Yoast, valid imagery and LCP/CLS.
6. Preserve backups and deploy using the authorized GitHub -> A3tal Direct Bridge process only.

Mockup drawings are schematic; WordPress candidate uses currently owned featured photographs.
