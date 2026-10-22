#!/usr/bin/env python3
"""Safely restore user-approved original H1 and paragraph in the deployed V3 hero.

Limited to the two exact text nodes and one responsive CSS override.
All other homepage markup, vehicle feed, search form, URLs and SEO are preserved.
The bridge uses per-file SHA256 compare-and-swap, with predeploy backups.
"""
import hashlib
import os
import subprocess
import tempfile
import types
from importlib.machinery import SourceFileLoader
from pathlib import Path

mod=types.ModuleType("a3tal_hero_bridge")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge

ROOT=Path("theme-source/a3tal-global")
HERO_MARKER="A3TAL-EXPERIENCE-V3-20261022"
CSS_BEG="/* A3TAL-HERO-RESTORE-ORIGINAL-COPY-20261022:START */"
CSS_END="/* A3TAL-HERO-RESTORE-ORIGINAL-COPY-20261022:END */"
OLD_TITLE='<h1 id="g-v3-main-title">كل ما تحتاجه عن <span>سيارتك، في مكان واحد.</span></h1>'
NEW_TITLE='<h1 id="g-v3-main-title">موسوعة أعطال السيارات وأكواد التشخيص والأسعار ومراكز الصيانة</h1>'
OLD_DESC='<p class="g-v3-hero-lead">شخّص أعطال السيارات، افهم الأكواد، قارن الأسعار والمراجعات، ووصل لمراكز الخدمة وقطع الغيار. معلومات مترابطة بدل البحث من أول وجديد.</p>'
NEW_DESC='<p class="g-v3-hero-lead">اكتشف كل ما تحتاج معرفته عن سيارتك في مكان واحد. تعرّف على أعطال السيارات وأسبابها وطرق إصلاحها، وافهم أكواد الأعطال OBD-II، واستكشف أسعار السيارات ومواصفاتها ومقارناتها، مع دليل مراكز الصيانة والخدمة لمساعدتك على التشخيص الصحيح واتخاذ القرار بثقة.</p>'

def lint_php(code):
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/"front-page.php"
        p.write_text(code,encoding="utf-8")
        subprocess.run(["php","-l",str(p)],check=True,timeout=20)

def validate_markup(code):
    if code.count(HERO_MARKER)!=1 or code.count("g-v3-hero-inner")<1:
        raise RuntimeError("Unexpected live hero baseline. Refusing to rewrite.")
    if code.count('id="g-v3-main-title"')!=1 or code.count('class="g-v3-hero-lead"')!=1:
        raise RuntimeError("Hero title/description selectors are not unique")
    if code.count("g-home-car-editorial-grid")<1 or code.count("g-v3-mobile-dock")<1:
        raise RuntimeError("Existing site navigation and car feed missing")
    lint_php(code)

def patch_html(live, approved):
    validate_markup(approved)
    if live.count(HERO_MARKER)!=1:
        raise RuntimeError("V3 hero is no longer the current theme")
    if NEW_TITLE in live and NEW_DESC in live:
        validate_markup(live)
        return live,False
    if live.count(OLD_TITLE)!=1 or live.count(OLD_DESC)!=1:
        raise RuntimeError("Live hero copy differs from expected baseline")
    update=live.replace(OLD_TITLE,NEW_TITLE,1).replace(OLD_DESC,NEW_DESC,1)
    validate_markup(update)
    if approved.count(NEW_TITLE)!=1 or approved.count(NEW_DESC)!=1:
        raise RuntimeError("Approved GitHub hero copy is different")
    return update,True

def css_override(approved):
    if approved.count(CSS_BEG)!=1 or approved.count(CSS_END)!=1:
        raise RuntimeError("Approved CSS override marker missing")
    beg=approved.index(CSS_BEG)
    end=approved.index(CSS_END)+len(CSS_END)
    return approved[beg:end]

def patch_style(live,approved):
    block=css_override(approved)
    if CSS_BEG in live:
        if live.count(CSS_BEG)!=1 or block not in live:
            raise RuntimeError("Unexpected current CSS override")
        return live,False
    if "A3TAL-PREMIUM-UX-V3-20261022:END" not in live:
        raise RuntimeError("Deployed premium UX stylesheet missing")
    return live.rstrip()+"\n\n"+block+"\n",True

def main():
    if not os.environ.get("A3TAL_API_KEY"):
        raise RuntimeError("Missing configured A3TAL bridge secret")
    approved_html=(ROOT/"front-page.php").read_text("utf-8")
    approved_css=(ROOT/"style.css").read_text("utf-8")
    validate_markup(approved_html)
    bridge=Bridge()
    backup=Path("hero-restore-predeploy-backup")
    backup.mkdir(exist_ok=True)

    live_html=bridge.read("front-page.php")
    live_style=bridge.read("style.css")
    (backup/"front-page.php").write_text(live_html["content"],encoding="utf-8")
    (backup/"style.css").write_text(live_style["content"],encoding="utf-8")
    new_html,changed_html=patch_html(live_html["content"],approved_html)
    new_style,changed_css=patch_style(live_style["content"],approved_css)
    if changed_css:
        bridge.write("style.css",new_style,live_style["sha256"])
        print("HERO_ORIGINAL_COPY_CSS_VERIFIED",flush=True)
    if changed_html:
        bridge.write("front-page.php",new_html,live_html["sha256"])
        print("HERO_ORIGINAL_H1_AND_DESCRIPTION_VERIFIED",flush=True)
    bridge.flush()
    print("HERO_COPY_RESTORED_AND_CACHE_FLUSHED",flush=True)

if __name__=="__main__":
    main()
