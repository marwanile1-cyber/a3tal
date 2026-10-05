# A3tal Direct Bridge 3.0

Administrator-grade WordPress REST bridge for **a3tal.com**.

## Live architecture

- WordPress plugin: `a3tal-direct-bridge.php`
- REST namespace: `/wp-json/a3tal-direct/v1`
- GitHub workflow: `.github/workflows/a3tal-bridge.yml`
- Authentication: repository secret `A3TAL_API_KEY` sent in request headers
- The API key must never be committed to the repository or placed in a URL.

## Existing content operations

- Read/search posts and pages
- Create/update posts and pages
- Yoast title, focus keyword, meta description and canonical
- Upload images, set featured images and insert images in content
- Redirects
- Per-post rollback snapshots

## Administrator gateway

Use `GET|POST /admin` with an `op` parameter.

Read operations include:

- `site_info`
- `plugins`
- `themes`
- `users`
- `roles`
- `options`
- `terms`
- `menus`
- `comments`
- `updates`
- `cron`
- `file_read`
- `file_list`
- `post_meta`
- `theme_mods`
- `audit_log`

Write operations include:

- Site option set/delete
- Arbitrary post meta set/delete
- Taxonomy term create/update/delete
- Navigation menu create/update/assign/delete
- User create/update/delete
- Role create/update/delete
- Plugin install/activate/deactivate/update/delete
- Theme install/activate/update/delete
- WordPress core update
- Theme mod set/delete
- Cache and rewrite flushing
- Transient cleanup
- Cron execution/unscheduling
- Text/code file management inside `wp-content`
- `bridge_self_update` for future bridge releases

Destructive or code-writing operations require explicit `confirm=true`; the highest-risk operations also require `dangerous=true`.

## Boundary

Bridge 3.0 is designed to provide WordPress Administrator-level control. It intentionally does **not** provide operating-system root access, arbitrary shell execution, access to `wp-config.php`, or unrestricted filesystem access outside `wp-content`.

## Audit and safety

- Admin mutations are logged inside WordPress in a rolling bridge audit log.
- The bridge authentication option cannot be changed through the API.
- File paths are normalized and restricted to `wp-content`.
- File writes support `expected_sha256` conflict checking.
- GitHub Actions suppresses `/admin` response bodies by default so sensitive values are not written to public logs.
- A backup branch was created before the 3.0 upgrade: `backup/bridge-2.1.1-2026-09-28`.
- A PHP lint workflow checks bridge syntax on every bridge-file push.

## Current deployment note

Updating this repository does not update the currently installed WordPress plugin automatically. The live site was verified on 2026-09-28 and reported Bridge **2.1.0**. Version 3.0 must therefore be installed on the site once. After 3.0 is live, the `bridge_self_update` operation can update the bridge from this repository for future releases.


## Editorial image policy

All article and featured images must follow [A3tal Editorial Image Policy](A3TAL-IMAGE-POLICY.md). The default is photorealistic, scene-based automotive imagery. Vector, icon-based, infographic-style or generic rendered images are rejected unless a technical diagram is explicitly required by the content.
