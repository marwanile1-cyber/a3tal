#!/usr/bin/env python3
"""Revision-guarded live repair of homepage automotive feed.

Always keep a3_car (structured vehicle records) distinct from editorial posts.
New price/review articles in WordPress categories 374,22,21 appear in a separate
labelled feed without fabricating new vehicle records or changing any old URLs.
"""
import importlib.util
import hashlib
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("theme-source/a3tal-global")
BRIDGE_SOURCE = Path("scripts/deploy-dtc-library.py")
MODULE_MARKER = "A3TAL-HOME-RECENT-VEHICLES-AND-ARTICLES-20261022"
CSS_MARKER = "/* A3TAL-HOME-CAR-EDITORIAL-FEED-20261022 */"
OLD_SECTION_BEGIN = "<?php if($cars->have_posts()): ?>\n<section class=\"g-section g-home-cars-section\">"
NEW_SECTION_BEGIN = "<?php if($cars->have_posts() || $car_editorials->have_posts()): ?>"
NEXT_SECTION = '<section class="g-section g-section-soft g-home-dtc-zone">'
MOTO_QUERY = "$moto_articles=new WP_Query(["

spec = importlib.util.spec_from_file_location("a3tal_bridge_runtime", BRIDGE_SOURCE)
# Importlib spec_file_from_location may not recognize a ".py" path whose filename
# includes hyphens on older interpreters, so load directly with SourceFileLoader.
from importlib.machinery import SourceFileLoader
loader = SourceFileLoader("a3tal_bridge_runtime", str(BRIDGE_SOURCE))
import types
module = types.ModuleType("a3tal_bridge_runtime")
loader.exec_module(module)
Bridge = module.Bridge


def one_span(raw, start, end, label):
    a = raw.find(start)
    if a < 0 or raw.find(start, a + 1) != -1:
        raise RuntimeError(f"Expected exactly one start anchor in {label}")
    b = raw.find(end, a)
    if b < 0 or raw.find(end, b + 1) != -1:
        raise RuntimeError(f"Expected exactly one end anchor after {label}")
    return raw[a:b]


def lint_php(src):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"front-page.php"
        path.write_text(src,encoding="utf-8")
        subprocess.run(["php","-l",str(path)],check=True,timeout=20)


def patched_front(live, intended):
    source_query = one_span(intended,
        "/* "+MODULE_MARKER, MOTO_QUERY, "approved source query")
    source_section = one_span(intended, NEW_SECTION_BEGIN, NEXT_SECTION,
                              "approved editorial and vehicle feed")
    if live.count(MODULE_MARKER) > 1:
        raise RuntimeError("Multiple homepage feed markers found")
    if MODULE_MARKER in live:
        # Idempotence: already applied. Never silently reconcile unexpected drift.
        if source_section not in live or source_query not in live:
            raise RuntimeError("Existing marker but different live feed; manual review required")
        return live, False

    old_query = one_span(live, "$cars=new WP_Query([", MOTO_QUERY,
                         "original vehicles query")
    if (old_query.count("'post_type'=>'a3_car'") != 1
        or "'orderby'=>'date'" not in old_query
        or "'posts_per_page'=>6" not in old_query
        or "car_editorials" in old_query):
        raise RuntimeError("Unexpected cars query, refusing sitewide overwrite")
    old_section = one_span(live, OLD_SECTION_BEGIN, NEXT_SECTION,
                           "original recently added cars section")
    if (old_section.count('سيارات مضافة حديثًا') != 1
        or old_section.count("a3g_platform_card()") != 1
        or "car_editorials" in old_section):
        raise RuntimeError("Unexpected homepage markup, refusing unsafe replacement")

    result=live.replace(old_query,source_query,1).replace(old_section,source_section,1)
    if result.count(MODULE_MARKER)!=1 or result.count("g-home-car-editorial-grid")!=1:
        raise RuntimeError("Feed replacement markers not unique")
    lint_php(result)
    return result, True


def patched_css(live, intended):
    if intended.count(CSS_MARKER)!=1:
        raise RuntimeError("No unique approved CSS marker")
    block=intended[intended.index(CSS_MARKER):]
    if not block.endswith("\n"):
        block+="\n"
    if CSS_MARKER in live:
        if block.strip() not in live:
            raise RuntimeError("Live stylesheet contains different feed CSS, refuse clobber")
        return live,False
    return live.rstrip()+"\n\n"+block, True


def main():
    front_source=(ROOT/"front-page.php").read_text("utf-8")
    css_source=(ROOT/"style.css").read_text("utf-8")
    lint_php(front_source)
    if MODULE_MARKER not in front_source or CSS_MARKER not in css_source:
        raise RuntimeError("Source files are missing approved patch markers")

    client=Bridge()
    old_front=client.read("front-page.php")
    new_front,changed=patched_front(old_front["content"],front_source)
    if changed:
        client.write("front-page.php",new_front,old_front["sha256"])
        print("HOMEPAGE_DYNAMIC_CAR_FEED_DEPLOYED_VEHICLES_DISTINCT_FROM_ARTICLES",flush=True)
    else:print("HOMEPAGE_FEED_ALREADY_CORRECT",flush=True)

    old_css=client.read("style.css")
    new_css,changed_css=patched_css(old_css["content"],css_source)
    if changed_css:
        client.write("style.css",new_css,old_css["sha256"])
        print("HOMEPAGE_CAR_FEED_RESPONSIVE_CSS_DEPLOYED",flush=True)
    else:print("HOMEPAGE_FEED_CSS_ALREADY_CORRECT",flush=True)

    client.flush()
    print("HOMEPAGE_CAR_SECTION_CACHE_FLUSH_COMPLETE",flush=True)


if __name__=="__main__":
    main()
