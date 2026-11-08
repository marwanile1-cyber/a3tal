#!/usr/bin/env python3
"""Deploy ONLY the bilingual Egyptian homepage brand cards via A3tal Direct Bridge.

Preserves every other live homepage and theme line. Uses checked existing live
SHA-256 for writes and retains rollback copies in the GitHub Action artifact.
"""
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import types
from pathlib import Path
from importlib.machinery import SourceFileLoader
import requests

BASE="https://a3tal.com"
THEME=Path("theme-source/a3tal-global")
OUT=Path("reports/a3tal-home-brand-cards-20261108")
OUT.mkdir(parents=True,exist_ok=True)
if not os.environ.get("A3TAL_API_KEY"):
    raise SystemExit("Missing A3tal Direct Bridge key")
mod=types.ModuleType("brand_cards_bridge")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge
PHP="home-reference-20261104.php"
CSS="home-reference-20261104.css"
FUN="functions.php"
BEGIN="<!-- A3TAL-HOME-BRAND-TEXT-CARDS-20261108:BEGIN -->"
END="<!-- A3TAL-HOME-BRAND-TEXT-CARDS-20261108:END -->"
STYLE_BEGIN="/* A3TAL BRAND-NAME CARDS 20261108:"
STYLE_END="/* END A3TAL BRAND-NAME CARDS 20261108 */"
OLD_START='<section class="brands-bar">'
OLD_END='<div class="wrap"><section class="catalog">'
NEW_VERSION="20261108.1"

def digest(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def lint_php(s):
    with tempfile.TemporaryDirectory() as root:
        f=Path(root)/"template.php"
        f.write_text(s,encoding="utf-8")
        subprocess.run(["php","-l",str(f)],check=True,timeout=25,capture_output=True)

def source_slice(s,start,end,after=False):
    if s.count(start)!=1 or s.count(end)!=1:
        raise RuntimeError("Expected exactly one audited source marker pair")
    i=s.index(start); j=s.index(end,i)+len(end)
    if after and j<len(s) and s[j]=="\n":j+=1
    return s[i:j]

def patch_php(current,source):
    new_block=source_slice(source,BEGIN,END,True)
    if BEGIN in current or END in current:
        if current.count(new_block)==1:return current
        raise RuntimeError("Live homepage already has different brand-name cards; preserve it")
    if current.count(OLD_START)!=1 or current.count(OLD_END)!=1:
        raise RuntimeError("Original live brand bar shape no longer matches reviewed template")
    i=current.index(OLD_START);j=current.index(OLD_END,i)
    old=current[i:j]
    if old.count('class="brand"')!=8 or old.count("a3tal-ref-20261104-brand-")!=8:
        raise RuntimeError("Unexpected existing Egyptian brand row; unsafe to replace")
    merged=current[:i]+new_block+current[j:]
    lint_php(merged)
    if merged.count('class="a3r-brand-name-card"')!=12:
        raise RuntimeError("Must have exactly 12 brand links")
    return merged

def patch_css(current,source):
    new_block=source_slice(source,STYLE_BEGIN,STYLE_END)
    if STYLE_BEGIN in current or STYLE_END in current:
        if current.count(new_block)==1:return current
        raise RuntimeError("Live stylesheet already has a nonmatching brand-card patch")
    if ".a3tal-reference-page .brands-grid" not in current:
        raise RuntimeError("Original stylesheet layout changed")
    return current.rstrip()+"\n\n"+new_block+"\n"

def patch_functions(current):
    if "'"+NEW_VERSION+"'" in current and "wp_enqueue_style('a3g-reference-v5'" in current:
        return current
    old=re.compile(r"(wp_enqueue_style\('a3g-reference-v5',[^;\n]*,')20261104\.\d+('\);)")
    new,n=old.subn(lambda m:m.group(1)+NEW_VERSION+m.group(2),current)
    if n!=1:raise RuntimeError("Cannot safely cache-bust original V5 stylesheet")
    lint_php(new)
    return new

def public_verify():
    s=requests.Session()
    s.headers.update({"User-Agent":"Mozilla/5.0 (compatible; A3talBrandCardsQA/1.0)","Cache-Control":"no-cache"})
    for attempt in range(4):
        try:
            html=s.get(BASE+"/?brand_name_cards_qa="+str(time.time_ns()),timeout=45).text
            if html.count('class="a3r-brand-name-card"')==12 and BEGIN in html:
                break
        except requests.RequestException:
            pass
        if attempt==3:raise RuntimeError("Public homepage has not exposed new brand cards")
        time.sleep(5)
    else:raise RuntimeError("Public homepage brand verification failed")
    for must in ['lang="en">TOYOTA</strong>','lang="en">FORD</strong>',
                 'lang="en">CHEVROLET</strong>','lang="en">KIA</strong>',
                 'lang="en">HYUNDAI</strong>','تصفح كل الماركات',
                 'href="https://a3tal.com/?s=%D9%81%D9%88%D8%B1%D8%AF"']:
        if must not in html:raise RuntimeError("Missing a specific new brand/card/link: "+must)
    if len(re.findall(r"<h1\b",html,re.I))!=1:
        raise RuntimeError("Homepage H1 count changed")
    brand=html.split(BEGIN,1)[1].split(END,1)[0]
    if "a3tal-ref-20261104-brand-" in brand or "<img" in brand:
        raise RuntimeError("Old brand logo images still embedded in new brand section")
    style=s.get(BASE+"/wp-content/themes/a3tal-global/home-reference-20261104.css?ver="+NEW_VERSION,timeout=45).text
    if STYLE_BEGIN not in style or STYLE_END not in style:
        raise RuntimeError("Live brand-card stylesheet not public")
    return {"verified":True,"cards":12,"ford_has_real_content":True,"h1":1,"css_version":NEW_VERSION}

def main():
    source_php=(THEME/PHP).read_text("utf-8")
    source_css=(THEME/CSS).read_text("utf-8")
    assert source_php.count(BEGIN)==1 and source_php.count(END)==1
    assert source_css.count(STYLE_BEGIN)==1 and source_css.count(STYLE_END)==1
    lint_php(source_php)
    bridge=Bridge()
    originals={}
    for name in (PHP,CSS,FUN):
        originals[name]=bridge.read(name)
    desired={
        CSS:patch_css(originals[CSS]["content"],source_css),
        PHP:patch_php(originals[PHP]["content"],source_php),
        FUN:patch_functions(originals[FUN]["content"])
    }
    (OUT/"predeployment-backups.json").write_text(json.dumps({
        k:{"sha256":v["sha256"],"content":v["content"]} for k,v in originals.items()
    },ensure_ascii=False),encoding="utf-8")
    print("SAFE_BRAND_PATCH_PREFLIGHT_PASS",flush=True)
    changed=[]
    try:
        for name in (CSS,PHP,FUN):
            if desired[name]==originals[name]["content"]:
                print("ALREADY_MATCHES",name,flush=True)
                continue
            bridge.write(name,desired[name],originals[name]["sha256"])
            changed.append(name)
            print("BRAND_SECTION_FILE_VERIFIED",name,flush=True)
        bridge.flush()
        result=public_verify()
        (OUT/"public-live-qa.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    except Exception:
        print("QA_OR_DEPLOY_FAILED_GUARDED_ROLLBACK",flush=True)
        for name in reversed(changed):
            try:
                bridge.write(name,originals[name]["content"],digest(desired[name]))
                print("ROLLED_BACK",name,flush=True)
            except Exception as e:
                print("MANUAL_ROLLBACK_NEEDED",name,type(e).__name__,flush=True)
        try:bridge.flush()
        except Exception:pass
        raise
    print("SUCCESS_LIVE_12_EGYPTIAN_BRAND_TEXT_CARDS",flush=True)

if __name__=="__main__":
    main()
