# A3tal mandatory car-reference image gate

Status: **MANDATORY** for every new PSEO batch on both A3tal Egypt and Saudi properties.

The user explicitly prioritized this on 2026-11-09 after rejecting schematic/placeholder images in batches 34/35.

## Non-negotiable rules

1. Every featured image **must visually depict the exact real car model and generation** named by the article, sourced from an identifiable manufacturer's or licensed official dealer's corresponding model gallery. Do not substitute a different model or trim/generation or invent a vehicle's design.
2. Use original real car photography as the dominant visual; no line art, generic technical illustrations, synthetic silhouette, fake engine/gearbox diagrams, fake AI-generated cars, generic stock photos, clip-art, noisy marketing banners, giant labels, or text blocks. Crop/correct a real manufacturer photo into a tasteful editorial cover. Small A3TAL.COM branding is optional.
3. Separate real photos for distinct pages. Gallery shots may include a model-specific exterior, cabin or vehicle detail relevant to an article; do not pretend the photo documents a part or feature it does not actually show.
4. Verify the official model gallery and individual photo URLs are valid and dimensions meet minimum quality; enforce exact trusted source host(s). Reject small thumbnails and unrelated photos. Prefer landscape images and frame the full recognizably correct vehicle; do not crop off its identity to make a decorative card.
5. Make true WebP at 1600x900 or the explicit article brief's dimensions, with responsive WordPress thumbnails. Upload via A3tal Direct Bridge. Avoid external hotlinks in the final published featured image.
6. Set the actual WordPress featured image. Post-publish verify publicly the page's full-size og:image URL, the visible `<img>`, 1600x900 output image metadata, HTTP 200, canonical, indexability and direct link; include this in a QA report.
7. Safeguard existing published records: verify exact slug/path/title, never override unrelated pages; retain the original content, sources, metadata and permalink when replacing only an image.
8. **Fail closed** if real model-matched photos are not verified. Do not silently fall back to vector art, old broken pictures, default WP thumbnails, generic icons or unrelated dealer pictures.
9. Check both desktop/mobile presentation at appropriate viewport before calling a batch visually complete where browser validation is available.
10. No batch is complete merely because GitHub Actions were committed or triggered; verify all target public pages and their image/og tags.

User-facing images in ChatGPT found by image search are not proof of what has been uploaded to WordPress. Only verified site URLs prove replacement.
