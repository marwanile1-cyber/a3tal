# Image replacement drop zone

Place the reviewed binary file `a3tal-kia-image-replacements.zip` in this directory. The workflow `.github/workflows/replace-kia-featured-images.yml` starts on this ZIP's push and uses A3tal Direct Bridge to replace the 5 existing featured images, verifying actual HTML and og:image on each live page. Do not commit arbitrary files or credentials. The uploaded ZIP should contain exactly five WebP images as provided in the project package.
