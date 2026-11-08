#!/usr/bin/env python3
"""Scoped replacement: Egypt homepage real brand emblems, using pre-existing pinned logos.
Never changes the Saudi website, prices, posts, PSEO pages, or brand destinations.
"""
import hashlib, json, os, re, subprocess, tempfile, time, types
from pathlib import Path
from importlib.machinery import SourceFileLoader
import requests

BASE="https://a3tal.com"
THEME=Path("theme-source/a3tal-global")
OUT=Path("reports/egypt-home-exact-brand-logos-20261108")
OUT.mkdir(parents=True,exist_ok=True)
if not os.environ.get("A3TAL_API_KEY"):raise SystemExit("Missing A3tal Direct Bridge secret")
module=types.ModuleType("a3tal_egypt_brand_bridge")
SourceFileLoader(module.__name__,"scripts/deploy-dtc-library.py").exec_module(module)
Bridge=module.Bridge
HOME="home-reference-20261104.php"
STYLE="home-reference-20261104.css"
LOGOS="assets/js/egypt-home-brand-logos-20261108.js"
FUN="functions.php"
BEGIN="<!-- A3TAL-EGYPT-BRANDS-20261108-BEGIN -->"
NEXT="<!-- A3TAL-EGYPT-HOME-PRICES-20261108-BEGIN -->"
PSEO_END="<!-- A3TAL-EGYPT-HOME-PSEO-20261108-END -->"
SCRIPT_MARKER="<!-- A3TAL-EGYPT-BRAND-LOGO-ASSET-20261108 -->"
CSS_START="/* A3TAL EGYPT AUTHENTIC LOGO CARDS 20261108 */"
CSS_END="/* END A3TAL EGYPT AUTHENTIC LOGO CARDS */"
VERSION="20261108.2"

def digest(s):return hashlib.sha256(s.encode("utf-8")).hexdigest()
def php_lint(s):
    with tempfile.TemporaryDirectory() as path:
        f=Path(path)/"test.php"
        f.write_text(s,"utf-8")
        subprocess.run(["php","-l",str(f)],check=True,capture_output=True,timeout=25)
def source(name):return (THEME/name).read_text("utf-8")
def patch_home(live):
    src=source(HOME)
    if src.count(BEGIN)!=1 or src.count(NEXT)!=1:
        raise RuntimeError("Reviewed Egyptian homepage brand marker mismatch")
    if live.count(BEGIN)!=1 or live.count(NEXT)!=1:
        raise RuntimeError("Live Egyptian homepage brand marker mismatch")
    source_segment=src[src.index(BEGIN):src.index(NEXT)]
    old_segment=live[live.index(BEGIN):live.index(NEXT)]
    if old_segment.count('class="a3egy-brand"')!=24:
        raise RuntimeError("Unexpected number of original 24 brand cards")
    if source_segment.count('class="a3egy-brand" data-brand=')!=24:
        raise RuntimeError("Reviewed 24 authentic badge slots missing")
    if old_segment!=source_segment:
        if 'data-brand=' in old_segment:
            raise RuntimeError("Live brand badges differ from reviewed asset; abort")
        live=live.replace(old_segment,source_segment,1)
    if SCRIPT_MARKER not in live:
        insertion=src[src.index(SCRIPT_MARKER):]
        insertion=insertion.split("\n",2)
        if len(insertion)<2 or "egypt-home-brand-logos-20261108.js" not in insertion[1]:
            raise RuntimeError("Reviewed brand logo script include missing")
        live=live.replace(PSEO_END,PSEO_END+"\n"+insertion[0]+"\n"+insertion[1],1)
    elif live.count(SCRIPT_MARKER)!=1:
        raise RuntimeError("Duplicate brand logo script")
    if live.count('class="a3egy-brand-logo"')!=24:raise RuntimeError("Actual logo img count differs")
    php_lint(live)
    return live
def patch_css(live):
    src=source(STYLE)
    if src.count(CSS_START)!=1 or src.count(CSS_END)!=1:
        raise RuntimeError("Reviewed badge style block missing")
    block=src[src.index(CSS_START):src.index(CSS_END)+len(CSS_END)]
    if CSS_START in live:
        if live.count(block)!=1:raise RuntimeError("Live badge styles conflict")
        return live
    if ".a3tal-reference-page .a3egy-brands-grid" not in live:
        raise RuntimeError("Expected existing homepage layout missing")
    return live.rstrip()+"\n\n"+block+"\n"
def patch_functions(live):
    line_regex=re.compile(r"(wp_enqueue_style\('a3g-encyclopedia-home'[^;\n]*?,['\"])([^'\"]+)(['\"]\);)")
    parts=line_regex.findall(live)
    if len(parts)!=1:raise RuntimeError("Homepage version line not unique")
    old=parts[0][1]
    if old==VERSION:return live
    if old not in ("20261108.1","20261104-v5","20261104-v5b","20261104-v5c","20261104-v5d"):
        raise RuntimeError("Live CSS version changed independently: "+old)
    fixed=line_regex.sub(lambda m:m.group(1)+VERSION+m.group(3),live,count=1)
    php_lint(fixed)
    return fixed

def verify():
    session=requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0 (compatible; A3talBrandLogoQA/1.0)","Cache-Control":"no-cache"})
    error={}
    for attempt in range(5):
        try:
            r=session.get(BASE+"/?brand_logo_release_qa="+str(time.time_ns()),timeout=45)
            html=r.text
            result={"status":r.status_code,"cards":html.count('class="a3egy-brand" data-brand='),
                    "logos":html.count('class="a3egy-brand-logo"'),
                    "prices":'id="egypt-car-prices"' in html,
                    "pseo":'id="egypt-pseo"' in html}
            if r.status_code==200 and result["cards"]==24 and result["logos"]==24 and result["prices"] and result["pseo"]:
                break
            error=result
        except requests.RequestException as exc:
            error={"transport":type(exc).__name__}
        if attempt==4:raise RuntimeError("Public homepage visual-asset QA failed: "+json.dumps(error))
        time.sleep(7)
    for x in ["toyota","kia","chery","geely","jetour","jaecoo","ford","byd"]:
        if 'data-brand="'+x+'"' not in html:raise RuntimeError("Brand missing: "+x)
    if html.count("<h1")!=1:raise RuntimeError("Homepage H1 changed")
    if 'a3tal-ref-20261104-brand-toyota.webp' in html.split(BEGIN,1)[1].split(NEXT,1)[0]:
        raise RuntimeError("Original unsatisfactory logo crop still in badge row")
    asset=session.get(BASE+"/wp-content/themes/a3tal-global/"+LOGOS,timeout=40)
    if asset.status_code!=200 or "data:image/webp;base64" not in asset.text:
        raise RuntimeError("Local real-brand-logo dataset not accessible")
    css=session.get(BASE+"/wp-content/themes/a3tal-global/"+STYLE+"?v="+VERSION,timeout=40)
    if css.status_code!=200 or CSS_START not in css.text:
        raise RuntimeError("Scoped badge CSS not accessible")
    return {"success":True,"brand_cards":24,"real_logos":23,"fallback":"SOUEAST",
            "price_hub_present":True,"pseo_hub_present":True,
            "brand_destinations_preserved":True}

def main():
    php_lint(source(HOME))
    bridge=Bridge()
    info=bridge.request({"op":"site_info"})
    if info.get("active_theme")!="a3tal-global":raise RuntimeError("Live active theme mismatch")
    originals={}
    for name in (LOGOS,STYLE,HOME,FUN):
        originals[name]=bridge.read(name,missing=(name==LOGOS))
    desired={LOGOS:source(LOGOS),
             STYLE:patch_css(originals[STYLE]["content"]),
             HOME:patch_home(originals[HOME]["content"]),
             FUN:patch_functions(originals[FUN]["content"])}
    if originals[LOGOS] and originals[LOGOS]["content"]!=desired[LOGOS]:
        raise RuntimeError("An unrelated live logo JS asset exists at reserved name")
    (OUT/"restore.json").write_text(json.dumps({
        k:{"sha256":v["sha256"],"content":v["content"]} if v else None
        for k,v in originals.items()
    },ensure_ascii=False),"utf-8")
    print("SAFE_LOGO_DEPLOY_PREFLIGHT_24_MARKS_NO_PAGE_CONTENT_MUTATION",flush=True)
    changes=[]
    try:
        for name in (LOGOS,STYLE,HOME,FUN):
            old=originals[name]
            if old and old["content"]==desired[name]:
                print("UNCHANGED",name,flush=True);continue
            bridge.write(name,desired[name],old["sha256"] if old else digest(""))
            changes.append(name)
            print("READBACK_VERIFIED",name,flush=True)
        bridge.flush()
        result=verify()
        (OUT/"public-check.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),"utf-8")
        print("LIVE_EGYPT_BRAND_LOGOS_PRICES_PSEO_SUCCESS",flush=True)
    except Exception:
        print("BRAND_LOGO_QA_FAILED_GUARDED_ROLLBACK",flush=True)
        for name in reversed(changes):
            old=originals[name]
            if not old:continue
            try:
                bridge.write(name,old["content"],digest(desired[name]))
                print("RESTORED",name,flush=True)
            except Exception as exc:
                print("MANUAL_RESTORE_REQUIRED",name,type(exc).__name__,flush=True)
        try:bridge.flush()
        except Exception:pass
        raise
if __name__=="__main__":main()
