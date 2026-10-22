#!/usr/bin/env python3
"""Guarded premium UX rollout to the existing A3tal theme.

Only:
- hero + homepage section launcher (same canonical destinations)
- mobile quick nav inside the homepage
- additive responsive styles for homepage, car models, DTC, article readability

No post/permalink/canonical/robots/content modification.
Compare existing live source and refuse unexpected theme drift.
"""
from pathlib import Path
from importlib.machinery import SourceFileLoader
import hashlib
import json
import os
import subprocess
import tempfile
import types

mod=types.ModuleType("a3tal_deploy_bridge_runtime")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge

ROOT=Path("theme-source/a3tal-global")
HERO_MARKER="A3TAL-EXPERIENCE-V3-20261022"
CSS_START="/* A3TAL-PREMIUM-UX-V3-20261022:START */"
CSS_END="/* A3TAL-PREMIUM-UX-V3-20261022:END */"
HERO_BEG='<section class="g-hero-section g-platform-home-hero'
NEXT_CARS='<?php if($cars->have_posts() || $car_editorials->have_posts()): ?>'
DOCK_BEG='<nav class="g-v3-mobile-dock"'
MAIN_END='</main>'

def digest(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def php_lint(s):
    with tempfile.TemporaryDirectory() as td:
        name=Path(td)/"front-page.php"
        name.write_text(s,encoding="utf-8")
        subprocess.run(["php","-l",str(name)],check=True,timeout=30)

def span_once(s,begin,end):
    i=s.find(begin)
    if i<0 or s.find(begin,i+len(begin))>=0:
        raise RuntimeError("Expected one begin anchor: "+begin)
    j=s.find(end,i+len(begin))
    if j<0 or s.find(end,j+len(end))>=0:
        raise RuntimeError("Expected one end anchor: "+end)
    return s[i:j]

def patch_front(original,approved):
    new_hero=span_once(approved,HERO_BEG,NEXT_CARS)
    dock=span_once(approved,DOCK_BEG,MAIN_END)
    if approved.count(HERO_MARKER)!=1 or approved.count(DOCK_BEG)!=1:
        raise RuntimeError("Approved hero/dock must be unique")
    if original.count(HERO_MARKER)==1 and original.count(DOCK_BEG)==1:
        if new_hero in original and dock in original:
            return original,False
        raise RuntimeError("An unrecognized v3 installation exists; refuse overwrite")
    if HERO_MARKER in original or DOCK_BEG in original:
        raise RuntimeError("Partial premium UX state; resolve before writing")

    old_hero=span_once(original,HERO_BEG,NEXT_CARS)
    checks=['g-hero-content','g-platform-launcher','g-universal-search',
            "a3g_platform_link('a3_dtc'","a3g_platform_link('a3_car'"]
    if any(v not in old_hero for v in checks) or old_hero.count('g-launch-icon')<8:
        raise RuntimeError("Live homepage hero is not the expected legacy template")
    if original.count(MAIN_END)!=1:
        raise RuntimeError("Homepage has unexpected main structure")
    if original.count(NEXT_CARS)!=1:
        raise RuntimeError("Homepage vehicle feed was changed by another deploy")
    if 'g-home-car-editorial-grid' not in original:
        raise RuntimeError("Latest article feed missing: do not regress past repairs")

    updated=original.replace(old_hero,new_hero,1).replace(MAIN_END,dock+MAIN_END,1)
    required=['g-v3-hero-inner','g-v3-mobile-dock','g-home-cars-section',
              'g-home-dtc-zone','g-home-os-section','g-review-grid','g-news-grid']
    if any(r not in updated for r in required):
        raise RuntimeError("Homepage module lost after surgical hero change")
    if updated.count('<main')!=1 or updated.count('</main>')!=1:
        raise RuntimeError("Homepage main tag count changed")
    php_lint(updated)
    return updated,True

def patch_style(original,approved):
    if approved.count(CSS_START)!=1 or approved.count(CSS_END)!=1:
        raise RuntimeError("Reviewed CSS markers must each be unique")
    block=approved[approved.index(CSS_START):approved.index(CSS_END)+len(CSS_END)]
    if CSS_START in original or CSS_END in original:
        if original.count(CSS_START)==1 and block in original:
            return original,False
        raise RuntimeError("Live CSS has conflicting design patch")
    if '.g-hero-section' not in original or '.g-entry' not in original:
        raise RuntimeError("Live theme style no longer matches shared a3tal-global")
    return original.rstrip()+"\n\n"+block+"\n",True

def main():
    if not os.environ.get("A3TAL_API_KEY"):
        raise RuntimeError("Production bridge secret absent")
    approved_front=(ROOT/"front-page.php").read_text("utf-8")
    approved_style=(ROOT/"style.css").read_text("utf-8")
    php_lint(approved_front)
    bridge=Bridge()
    evidence=Path("v3-qa-backup")
    evidence.mkdir(exist_ok=True)

    live_front=bridge.read("front-page.php")
    new_front,do_front=patch_front(live_front["content"],approved_front)
    (evidence/"live-front-before.php").write_text(live_front["content"],encoding="utf-8")
    print("BASELINE_FRONT_SHA",live_front["sha256"],"approved_patch_needed",do_front,flush=True)

    live_style=bridge.read("style.css")
    new_style,do_css=patch_style(live_style["content"],approved_style)
    (evidence/"live-style-before.css").write_text(live_style["content"],encoding="utf-8")
    print("BASELINE_STYLE_SHA",live_style["sha256"],"approved_patch_needed",do_css,flush=True)

    # Prepare and lint both before making the first live mutation.
    php_lint(new_front)
    if new_front.count(HERO_MARKER)!=1 or new_style.count(CSS_START)!=1:
        raise RuntimeError("Staging integrity failed")

    # First stage CSS ensures the new markup can never ship without its styles
    # unless the authenticated write itself fails and leaves the old homepage.
    if do_css:
        bridge.write("style.css",new_style,live_style["sha256"])
        print("V3_DESIGN_STYLES_LIVE_VERIFIED",digest(new_style),flush=True)
    if do_front:
        bridge.write("front-page.php",new_front,live_front["sha256"])
        print("V3_PREMIUM_HOMEPAGE_LIVE_VERIFIED",digest(new_front),flush=True)

    bridge.flush()
    print("V3_CACHE_FLUSHED",flush=True)

if __name__=="__main__":
    main()
