#!/usr/bin/env python3
"""Exclude only the existing above-the-fold A3tal home mobile hero from
LiteSpeed lazy loading. Preserves six PSEO cards and all current price cards.
Read/compare the complete live PHP file before making a one-attribute change.
Uses Direct Bridge checksum CAS, public verification, safe conditional rollback.
"""
import hashlib,json,re,os,time,subprocess,tempfile,types
from pathlib import Path
from importlib.machinery import SourceFileLoader
import requests
SOURCE=Path("theme-source/a3tal-global/home-reference-20261104.php")
REPORT=Path("reports/a3tal-20261114-litespeed-lcp-exclude.json")
REPORT.parent.mkdir(exist_ok=True,parents=True)
BASE="https://a3tal.com"
NAME="home-reference-20261104.php"
OLD='width="1200" height="440" loading="eager" fetchpriority="high" decoding="async" alt="سيارة حمراء'
NEW='width="1200" height="440" loading="eager" data-no-lazy="1" fetchpriority="high" decoding="async" alt="سيارة حمراء'
mod=types.ModuleType("a3tal_litespeed_lcp_bridge")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge
def html_check():
    r=requests.get(BASE+"/",params={"hero_no_lazy_20261114":str(time.time_ns())},
       headers={"Cache-Control":"no-cache, no-store","User-Agent":"Mozilla/5.0"},timeout=45)
    if r.status_code!=200:raise RuntimeError("Homepage HTTP "+str(r.status_code))
    s=r.text
    # The DOM image must escape LiteSpeed rewrite, unlike previous lazy-loaded audit.
    match=re.search(r'<img[^>]*class=["\\\'][^"\\\']*hero-mobile-scene[^>]*>',s,re.I)
    if not match:raise RuntimeError("Hero IMG missing from public HTML")
    hero=match.group(0)
    m=re.search(r'<div class="a3egy-reference-grid">(.*?)</div>',s,re.S)
    result={"h1_one":len(re.findall("<h1",s,re.I))==1,
     "pseo_cards":m.group(1).count("a3egy-reference-card") if m else 0,
     "prices":'class="a3egy-price-grid"' in s,
     "hero_no_lazy":'data-no-lazy="1"' in hero,
     "hero_not_litespeed_lazy":'data-lazyloaded=' not in hero and 'data-src=' not in hero,
     "hero_fetch_high":'fetchpriority="high"' in hero,
     "hero_loading_eager":'loading="eager"' in hero}
    if not all([result["h1_one"],result["pseo_cards"]>=5,result["prices"],result["hero_no_lazy"],result["hero_not_litespeed_lazy"],result["hero_fetch_high"],result["hero_loading_eager"]]):
        raise RuntimeError("Homepage LiteSpeed DOM verification failed "+repr(result))
    return result
def main():
    if not os.environ.get("A3TAL_API_KEY"):raise RuntimeError("Missing A3tal Direct Bridge key")
    expected=SOURCE.read_text("utf8")
    if expected.count(NEW)!=1 or expected.count(OLD)!=0:raise RuntimeError("Local reviewed source not uniquely patched")
    before=expected.replace(NEW,OLD)
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/NAME
        path.write_text(expected,"utf8")
        test=subprocess.run(["php","-l",str(path)],capture_output=True,text=True,timeout=40)
        if test.returncode:raise RuntimeError("PHP lint failed "+test.stdout+test.stderr)
    bridge=Bridge()
    live=bridge.read(NAME)
    if live["content"]==expected:
        print("ALREADY_EXCLUDED_LITESPEED_LCP_LIVE",flush=True)
    elif live["content"]!=before:
        raise RuntimeError("Source drift detected; leave production unchanged "+hashlib.sha256(live["content"].encode()).hexdigest()[:12])
    else:
        bridge.write(NAME,expected,expected=live["sha256"])
        print("SINGLE_HERO_NO_LAZY_ATTRIBUTE_DEPLOYED",flush=True)
    if live["content"]!=expected:bridge.flush()
    proof=None
    for attempt in range(6):
        try:
            proof=html_check()
            break
        except Exception as err:
            if attempt==5:
                # Only undo if we changed the source and it still matches our exact write.
                if live["content"]!=expected:
                    current=bridge.read(NAME)
                    if current["content"]==expected:
                        bridge.write(NAME,before,expected=current["sha256"])
                        bridge.flush()
                        print("ROLLBACK_SOURCE_SAFELY_RESTORED_AFTER_IMAGE_VERIFY_FAILURE",flush=True)
                raise
            time.sleep(7)
    REPORT.write_text(json.dumps({"success":True,"url":BASE+"/","fix":"LiteSpeed exact hero data-no-lazy attribute","checks":proof},ensure_ascii=False,indent=2),"utf8")
    print("LITESPEED_HERO_NO_LAZY_AND_PSEO_6_CARDS_VERIFIED",proof,flush=True)
if __name__=="__main__":main()
