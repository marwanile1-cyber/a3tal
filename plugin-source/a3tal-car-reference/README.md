# A3tal Car Reference Engine

WordPress custom post type "دليل المواصفات الفنية" with nested URLs:
- /car-reference/ (archive)
- /car-reference/hyundai/ (brand)
- /car-reference/hyundai/elantra-md/ (model)
- /car-reference/hyundai/elantra-md/engine-oil/ (spec)

No invented automotive data are shipped. Archive is noindex until sourced records exist. Old WordPress content, /cars/, /dtc/, the theme and the car garage remain unchanged.

Health: GET /wp-json/a3tal-car-reference/v1/health
Import: POST /wp-json/a3tal-car-reference/v1/upsert, X-A3tal-Key is the existing full admin bridge key. Import batch 1-25 records. Publish requires original editorial content, attached featured image, HTTPS source and at least 2 spec facts. Changes to published records require allow_update_published=true.

Initial release adds an empty but functional section and REST importer, not bulk-generated pages.