# A3tal AI Bridge

Custom WordPress REST bridge for **a3tal.com**.

## Why this exists

This plugin gives a trusted AI client a direct, controlled path to manage A3tal.com without depending on WPVibe/WPWriter limits.

It supports:

- Reading a post by ID
- Searching posts/pages
- Creating new posts
- Updating title/content/excerpt/status/slug/categories/tags
- Updating Yoast focus keyword, SEO title, meta description and canonical
- Uploading an image from a URL
- Setting/verifying featured images
- Inserting images into post content
- Creating 301/302/307/308 redirects
- Rolling back the latest post edit
- API-key authentication

## Installation

1. Download/clone this repository.
2. Place `a3tal-ai-bridge.php` inside a plugin folder named `a3tal-ai-bridge`.
3. Upload that folder to `wp-content/plugins/` or install it as a ZIP.
4. Activate **A3tal AI Bridge**.
5. In WordPress admin open **Tools → A3tal AI Bridge**.
6. Click **Generate New Random Key**.
7. Keep the key private. Do **not** commit it to GitHub.

## Authentication

Send either:

```
X-A3tal-Key: YOUR_SECRET_KEY
```

or:

```
Authorization: Bearer YOUR_SECRET_KEY
```

## REST base

```
https://a3tal.com/wp-json/a3tal-ai/v1/
```

## Main routes

- `GET /status`
- `GET /post/{id}`
- `GET /search-posts?search=...`
- `POST /create-post`
- `POST /update-post`
- `POST /upload-image`
- `POST /set-featured-image`
- `POST /insert-images`
- `POST /redirect`
- `POST /rollback-last`

## Example: update a post

```json
{
  "id": 80963,
  "title": "New title",
  "content": "<p>Updated article...</p>",
  "status": "publish",
  "meta": {
    "_yoast_wpseo_focuskw": "focus keyword",
    "_yoast_wpseo_title": "SEO title",
    "_yoast_wpseo_metadesc": "Meta description"
  }
}
```

## Example: create a 301 redirect

```json
{
  "source_path": "/red-vs-green-coolant-car/",
  "target_url": "https://a3tal.com/ultimate-radiator-coolant-guide-types-differences/",
  "status_code": 301
}
```

## Security

The repository must never contain the live API key. The secret stays inside WordPress options and is compared with `hash_equals()`.
