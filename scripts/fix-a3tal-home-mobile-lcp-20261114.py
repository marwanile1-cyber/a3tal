#!/usr/bin/env python3
"""Deploy narrowly scoped responsive LCP fix to A3tal via GitHub + Direct Bridge.
Checks local reviewed patch against EXACT pre-fix live PHP/CSS, verifies public
HTML and responsive CSS, and can restore originals via checksum CAS.
No article, post status, SEO URL, category, option, or data changes.
"""
import hashlib,json,os,re,subprocess,sys,time
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types,requests
ROOT=Path("theme-source/a3tal-global")
BASE="https://a3tal.com"
REPORT=Path("reports/a3tal-20261114-mobile-performance-fix.json")
REPORT.parent.mkdir(parents=True,exist_ok=True)
mod=types.ModuleType("safe_a3tal_direct_bridge")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge
OLD_HERO='<div class="hero-mobile-scene" role="img" aria-label="صورة تصميمية لسيارة حمراء في المدينة"></div>'
NEW_HERO='<img class="hero-mobile-scene" src="<?php echo esc_url(content_url(\'/uploads/2026/11/a3tal-ref-20261104-hero-mobile.webp\')); ?>" width="1200" height="440" loading="eager" fetchpriority="high" decoding="async" alt="سيارة حمراء في مدينة، الصورة الرئيسية لأعطال.كوم">'
OLD_PRICE='<?php if($price_article_image): ?><img loading="lazy" decoding="async" src="<?php echo esc_url($price_article_image); ?>" alt="<?php echo esc_attr(get_the_title($price_article_id)); ?>"><?php else: ?>'
NEW_PRICE='<?php if($price_article_image): ?><?php echo get_the_post_thumbnail($price_article_id, \'medium_large\', [\'loading\'=>\'lazy\',\'decoding\'=>\'async\',\'sizes\'=>\'(max-width:720px) 48vw, (max-width:1200px) 32vw, 380px\',\'alt\'=>get_the_title($price_article_id)]); ?><?php else: ?>'
REFERENCE_QUERY="""// Reuse existing, already stable homepage car query; avoid extra home data scans.
$home_new_reference = post_type_exists('a3_car_ref') ? get_posts([
 'post_type'=>'a3_car_ref','post_status'=>'publish','numberposts'=>6,
 'orderby'=>'modified','order'=>'DESC'
]) : [];
"""
PATCH_CSS='''
/* A3TAL-CORE-WEB-VITALS-MOBILE-HERO-20261114:START
   Real DOM image makes the mobile hero eligible for native preload/fetchpriority.
   Keep the exact reviewed 125px crop and original CSS layout. */
.a3tal-reference-page img.hero-mobile-scene{display:none}
@media(max-width:720px){
 .a3tal-reference-page img.hero-mobile-scene{
  display:block;width:100%;height:125px;max-width:100%;object-fit:cover;object-position:center 51%;
  background:none;border-radius:0;flex-shrink:0;
 }
}
/* A3TAL-CORE-WEB-VITALS-MOBILE-HERO-20261114:END */
'''
FILES=["home-reference-20261104.php","home-reference-20261104.css"]
def sha(value):
    return hashlib.sha256(value.encode("utf8")).hexdigest()
def reverse(name,reviewed):
    if name.endswith(".css"):
        if not reviewed.endswith(PATCH_CSS):raise RuntimeError("CSS source patch not exact")
        return reviewed[:-len(PATCH_CSS)]
    if reviewed.count(NEW_HERO)!=1 or reviewed.count(NEW_PRICE)!=1:raise RuntimeError("Homepage source did not match reviewed patch")
    before=reviewed.replace(NEW_HERO,OLD_HERO).replace(NEW_PRICE,OLD_PRICE)
    # Six below-hero graphical nav tiles were changed from eager to lazy.
    assert before.count('class="hub-visual" loading="lazy"')==6
    return before.replace('class="hub-visual" loading="lazy"','class="hub-visual" loading="eager"')
def only_blank_line_drift(a,b):
    import difflib
    changes=[item for item in difflib.ndiff(a.splitlines(),b.splitlines()) if item[:2] in ("+ ","- ")]
    return 0<len(changes)<=3 and all(not item[2:].strip() for item in changes)
def pub_verify():
    agent={"User-Agent":"Mozilla/5.0 (A3talLive-LCP-Fix-QA)","Cache-Control":"no-cache, no-store"}
    url=BASE+"/?a3tal_lcp_fix=20261114_"+str(time.time_ns())
    q=requests.get(url,timeout=45,headers=agent)
    if q.status_code!=200:raise RuntimeError("Homepage HTTP "+str(q.status_code))
    h=q.text
    checks={
        "one_h1":len(re.findall(r"<h1\\b",h,re.I))==1,
        "canonical":'<link rel="canonical" href="https://a3tal.com/"' in h or re.search(r'<link[^>]+rel=["\\\']canonical["\\\'][^>]+https://a3tal.com/',h,re.I) is not None,
        "hero_img":'class="hero-mobile-scene"' in h and 'fetchpriority="high"' in h,
        "no_legacy_hero_div":OLD_HERO not in h,
        "real_prices":'id="egypt-car-prices"' in h and 'class="a3egy-price-grid"' in h,
        "pseo":'id="egypt-pseo"' in h,
        "six_recovered_pseo_cards":bool(re.search(r'<div class="a3egy-reference-grid">(.*?)</div>',h,re.S) and re.search(r'<div class="a3egy-reference-grid">(.*?)</div>',h,re.S).group(1).count("a3egy-reference-card")>=5),
        "responsive_price_sizes":'sizes="(max-width:720px) 48vw' in h or "sizes=" in h[h.find("a3egy-price-grid"):h.find("a3egy-market-quick")],
    }
    if not all(checks.values()):raise RuntimeError("Homepage DOM QA failed "+repr(checks))
    css=requests.get(BASE+"/wp-content/themes/a3tal-global/home-reference-20261104.css?fix="+str(time.time_ns()),headers=agent,timeout=45)
    if css.status_code!=200 or "A3TAL-CORE-WEB-VITALS-MOBILE-HERO-20261114:END" not in css.text:
        raise RuntimeError("Responsive CSS marker not visible publicly")
    return checks
def main():
    if not os.environ.get("A3TAL_API_KEY"):raise RuntimeError("Bridge key not configured")
    reviewed={n:(ROOT/n).read_text("utf8") for n in FILES}
    before={n:reverse(n,reviewed[n]) for n in FILES}
    # Static tests: preserve full content except reviewed replacements.
    for n in FILES:
        if not reviewed[n] or len(reviewed[n])<20000:raise RuntimeError("Unexpected partial reviewed theme file "+n)
    with __import__('tempfile').TemporaryDirectory() as td:
        php=Path(td)/"home.php"
        php.write_text(reviewed[FILES[0]],"utf8")
        lint=subprocess.run(["php","-l",str(php)],capture_output=True,text=True,timeout=40)
        if lint.returncode:raise RuntimeError("PHP syntax broken "+lint.stdout+lint.stderr)
    br=Bridge()
    live={n:br.read(n) for n in FILES}
    prepared={n:reviewed[n] for n in FILES}
    for n in FILES:
        if live[n]["content"]==reviewed[n]:
            print("ALREADY_DEPLOYED",n,flush=True)
        elif n.endswith(".php") and live[n]["content"]==before[n].replace(REFERENCE_QUERY,""):
            print("CONFIRMED_LIVE_REGRESSION_MISSING_PSEO_POST_QUERY__RESTORE_IN_TARGET",n,flush=True)
        elif n.endswith(".css") and only_blank_line_drift(before[n], live[n]["content"]):
            print("EXACT_CSS_ONLY_BLANK_LINE_DRIFT_PRESERVED",n,flush=True)
            prepared[n]=live[n]["content"]+PATCH_CSS
        elif live[n]["content"]!=before[n]:
            import difflib
            print("LIVE_THEME_DRIFT_DIAGNOSTIC",n,"live_chars",len(live[n]["content"]),"expected_chars",len(before[n]),flush=True)
            diffs=list(difflib.unified_diff(before[n].splitlines(),live[n]["content"].splitlines(),n=2))
            print("LIVE_THEME_DRIFT_PREVIEW", "\\n".join(z[:260] for z in diffs[:55]),flush=True)
            raise RuntimeError("LIVE_SOURCE_DRIFT_STOPPED_WITHOUT_WRITE "+n+" live="+sha(live[n]["content"])[:16]+" expected="+sha(before[n])[:16])
        else:
            print("SOURCE_PREPATCH_EXACT_CONFIRMED",n,flush=True)
    changed=[]
    try:
        for n in FILES:
            if live[n]["content"]==reviewed[n]:continue
            br.write(n,prepared[n],expected=live[n]["sha256"])
            changed.append(n)
            print("PRECISE_THEME_FILE_DEPLOYED",n,flush=True)
        br.flush()
        proof=None
        for i in range(5):
            try:
                proof=pub_verify()
                break
            except Exception:
                if i==4:raise
                time.sleep(8)
        data={"success":True,"changed":changed,"files":{n:sha(prepared[n]) for n in FILES},
              "checks":proof,"scope":"LCP-only native DOM IMG, price responsive thumbnails, six nav tiles lazy"}
        REPORT.write_text(json.dumps(data,indent=2,ensure_ascii=False),"utf8")
        print("HOMEPAGE_MOBILE_LCP_DOM_CSS_RESPONSIVE_PRICE_PHOTOS_LIVE_VERIFIED",flush=True)
    except Exception:
        if changed:
            print("VERIFY_FAILED_RESTORING_ORIGINALS_WITH_CAS",changed,flush=True)
            for n in reversed(changed):
                try:
                    current=br.read(n)
                    if current["content"]==prepared[n]:
                        br.write(n,live[n]["content"],expected=current["sha256"])
                        print("ROLLBACK_SUCCEEDED",n,flush=True)
                except Exception as e:print("ROLLBACK_REQUIRES_MANUAL_REVIEW",n,str(e),flush=True)
            br.flush()
        raise
if __name__=="__main__":main()
