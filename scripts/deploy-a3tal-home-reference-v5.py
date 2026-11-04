#!/usr/bin/env python3
"""Deploy exact-image A3tal homepage reference safely via GitHub + A3tal Direct Bridge.

Never overwrite articles, options, canonicals, or the car-reference engine.
Upload model-illustrative concept crops only as homepage art (not article media).
Update live theme with scoped, compare-and-swap PHP/CSS/JS patches and rollback.
"""
import base64
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types
import requests

BASE = "https://a3tal.com"
WP_MEDIA = BASE + "/wp-content/uploads/2026/11/"
THEME = Path("theme-source/a3tal-global")
IMAGES = THEME / "assets/img/reference-20261104"
REPORT = Path("reports/a3tal-home-reference-v5")
REPORT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("A3TAL_API_KEY", "")
if not KEY: raise SystemExit("Missing configured A3tal Direct Bridge API secret")
mod = types.ModuleType("a3tal_home_bridge")
SourceFileLoader(mod.__name__, "scripts/deploy-dtc-library.py").exec_module(mod)
Bridge = mod.Bridge

NEW = [
 "home-reference-20261104.css",
 "assets/js/home-reference-20261104.js",
 "home-reference-header-20261104.php",
 "home-reference-20261104.php",
]
EXISTING = ["functions.php", "header.php", "front-page.php"]
EXPECTED_ASSETS = 27
RELEASE = "A3TAL-HOME-REFERENCE-EXACT-20261104"
session = requests.Session()
session.headers.update({"User-Agent": "A3tal-Home-Reference-20261104/1.0"})

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def fetch_asset(url:str):
    try:
        r=session.get(url,timeout=50,headers={"Cache-Control":"no-cache"})
        if r.status_code==200 and r.content[:4]==b'RIFF' and r.content[8:12]==b'WEBP':
            return r.content
        if r.status_code in (404,410):return None
        raise RuntimeError(f"Unexpected image fetch HTTP {r.status_code}")
    except requests.RequestException as e:raise RuntimeError(f"Cannot preflight WordPress image URL: {type(e).__name__}") from None

def upload_images():
    files=sorted(IMAGES.glob("*.webp"))
    if len(files)!=EXPECTED_ASSETS:raise RuntimeError(f"Expected exactly 27 original design images; got {len(files)}")
    audit=[]
    for index,file in enumerate(files,1):
        body=file.read_bytes()
        if len(body)>80000 or body[:4]!=b'RIFF' or body[8:12]!=b'WEBP':
            raise RuntimeError("Missing/invalid image: "+file.name)
        fname="a3tal-ref-20261104-"+file.name
        url=WP_MEDIA+fname
        current=fetch_asset(url)
        if current is not None:
            if sha(current)!=sha(body):raise RuntimeError("Existing live media at expected URL differs: "+fname)
            status="existing-verified"
        else:
            payload={"filename":fname,"image_base64":base64.b64encode(body).decode("ascii"),
                     "convert_webp":False,
                     "title":"أعطال.كوم - عنصر تصميم واجهة موسوعة السيارات",
                     "alt":"عنصر توضيحي لتصميم موسوعة السيارات - أعطال.كوم"}
            response=session.post(BASE+"/wp-json/a3tal-direct/v1/upload-image-data",
                  headers={"X-A3tal-Key":KEY,"Content-Type":"application/json"},
                  json=payload,timeout=180)
            if response.status_code not in (200,201):
                # Never blindly resend an ambiguous WordPress media mutation.
                check=fetch_asset(url)
                if check is None or sha(check)!=sha(body):
                    raise RuntimeError(f"WordPress asset upload rejected HTTP {response.status_code}: {fname}")
            else:
                data=response.json()
                if str(data.get("url",""))!=url or not int(data.get("media_id") or 0):
                    raise RuntimeError("WordPress returned unexpected upload URL: "+fname)
            reread=fetch_asset(url)
            if reread is None or sha(reread)!=sha(body):
                raise RuntimeError("Uploaded image missing or byte changed: "+fname)
            status="uploaded"
        audit.append({"filename":fname,"url":url,"status":status,"sha256":sha(body)})
        print("IMAGE_VERIFIED",index,len(files),fname,status,flush=True)
        time.sleep(1.1)
    (REPORT/"images.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf8")
    return audit

def lint_php(content,name):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/Path(name).name
        p.write_text(content,encoding="utf8")
        subprocess.run(["php","-l",str(p)],check=True,capture_output=True,timeout=30)

def source(name):return (THEME/name).read_text("utf8")
def modify_front(live):
    """Guardedly replace the duplicated V5 homepage with its single reviewed template.

    This touches only front-page.php; posts, CPT archives, permalinks,
    options and canonical configuration remain unchanged. The previous
    live file is captured for a compare-and-swap rollback.
    """
    reviewed=source("front-page.php")
    if live==reviewed:
        return live
    anchor="<?php get_template_part('home-reference-20261104'); ?>"
    existing=[
        '<main class="g-home g-home-platform a3r-production-home">',
        '<section class="a3r-home-directory"',
        'class="g-section g-home-cars-section"',
        'class="g-v3-mobile-dock"',
        '<?php get_footer(); ?>'
    ]
    if live.count(anchor)!=1 or any(live.count(value)!=1 for value in existing):
        raise RuntimeError("Live homepage no longer matches the reviewed duplicated V5 layout; refusing unsafe replacement")
    if live.count("</main>")!=1 or live.count("get_header();")!=1:
        raise RuntimeError("Unexpected live PHP wrapper; not removing homepage content")
    if reviewed.count(anchor)!=1 or "a3r-home-directory" in reviewed:
        raise RuntimeError("Reviewed homepage still contains duplicate navigation")
    lint_php(reviewed,"front-page.php")
    return reviewed

def modify_header(live):
    if 'home-reference-header-20261104' in live:return live
    marker='<header class="g-header">'
    if live.count(marker)!=1 or live.rstrip().count("</header>")!=1:
        raise RuntimeError("Live global header unexpectedly changed")
    out=live.replace(marker,
         "<?php if(is_front_page()): ?>\n<?php get_template_part('home-reference-header-20261104'); ?>\n<?php else: ?>\n"+marker,1)
    out=out.rstrip()+"\n<?php endif; ?>\n"
    lint_php(out,"header.php")
    return out

def modify_functions(live):
    marker="function a3g_reference_v5_home_assets()"
    if marker not in live:
        action="add_action('wp_enqueue_scripts','a3g_assets');"
        if live.count(action)!=1:raise RuntimeError("Theme enqueue insertion point changed")
        addition="""
function a3g_reference_v5_home_assets(){
 if(!is_front_page())return;
 $base=get_template_directory_uri();
 wp_enqueue_style('a3g-reference-v5',$base.'/home-reference-20261104.css',['a3g-style'],'20261104.5');
 wp_enqueue_script('a3g-reference-v5',$base.'/assets/js/home-reference-20261104.js',[],'20261104.5',true);
}
add_action('wp_enqueue_scripts','a3g_reference_v5_home_assets',25);
"""
        live=live.replace(action,action+"\n"+addition,1)
    start="function a3g_preload_home_hero_image() {"
    end="add_action('wp_head', 'a3g_preload_home_hero_image', 2);"
    if live.count(start)!=1 or live.count(end)!=1:raise RuntimeError("Homepage LCP preload anchor changed")
    i=live.index(start);j=live.index(end)
    new="""function a3g_preload_home_hero_image() {
 if(!is_front_page())return;
 $base=content_url('/uploads/2026/11/');
 echo '<link rel="preload" as="image" media="(min-width: 701px)" href="'.esc_url($base.'a3tal-ref-20261104-hero-desktop.webp').'" fetchpriority="high">'.PHP_EOL;
 echo '<link rel="preload" as="image" media="(max-width: 700px)" href="'.esc_url($base.'a3tal-ref-20261104-hero-desktop.webp').'" fetchpriority="high">'.PHP_EOL;
}
"""
    out=live[:i]+new+live[j:]
    # Fresh URL versions are required after the CSS isolation and JS fixes;
    # never rely on stale edge/browser caches of the original V5 assets.
    if "'20261104.5'" in out:
        if out.count("'20261104.5'") != 2:
            raise RuntimeError("Unexpected V5 asset version anchors in live functions.php")
        out=out.replace("'20261104.5'","'20261104.6'")
    if "a3g_encyclopedia_home_assets" in out and "'20261104-v5'" in out:
        out=out.replace("'20261104-v5'","'20261104-v5b'")
    if "'20261104.6'" in out:
        if out.count("'20261104.6'") != 2:
            raise RuntimeError("Unexpected V5 cached asset versions")
        out=out.replace("'20261104.6'","'20261104.7'")
    if "a3g_encyclopedia_home_assets" in out and "'20261104-v5b'" in out:
        out=out.replace("'20261104-v5b'","'20261104-v5c'")
    if "'20261104.7'" in out:
        if out.count("'20261104.7'") != 2:
            raise RuntimeError("Unexpected V5 cache version 7 anchors")
        out=out.replace("'20261104.7'","'20261104.8'")
    if "a3g_encyclopedia_home_assets" in out and "'20261104-v5c'" in out:
        out=out.replace("'20261104-v5c'","'20261104-v5d'")
    lint_php(out,"functions.php")
    return out

def live_public():
    # A successful bridge write is not proof that public visitors see it.
    # Retry transient origin disconnects instead of failing on the first socket reset.
    last_error=None
    for attempt in range(4):
        try:
            url=BASE+"/?a3tal_reference_v5="+str(time.time_ns())
            r=session.get(url,timeout=60,headers={"Cache-Control":"no-cache"})
            r.raise_for_status()
            return r.text
        except requests.RequestException as exc:
            last_error=exc
            print("PUBLIC_HOMEPAGE_READ_RETRY",attempt+1,type(exc).__name__,flush=True)
            if attempt<3:time.sleep(3+attempt*2)
    raise RuntimeError("Public homepage verification unavailable after 4 attempts: "+type(last_error).__name__) from last_error

def verify_live():
    for i in range(9):
        s=live_public()
        if "a3tal-reference-page" in s and "دليلك الشامل للسيارات في مصر" in s:
            break
        time.sleep(5)
    else:raise RuntimeError("User-facing homepage did not switch to exact reference after cache flush")
    if len(re.findall(r'<h1\b',s,re.I))!=1:raise RuntimeError("Homepage must retain exactly one H1")
    for required in ["brand-toyota.webp","carcard","أحدث موديلات السيارات",
                     "مواصفات السيارات","مكتبة الأعطال","الموتوسيكلات",
                     "قطع الغيار","جداول الصيانة","مراكز الخدمة"]:
        if required not in s:
            if required.endswith(".webp") and "a3tal-ref-20261104-"+required in s:
                continue
            raise RuntimeError("Missing source homepage or PSEO navigation: "+required)
    for path in ["/car-reference/","/dtc/","/motorcycles/","/parts/",
                 "/maintenance-schedules/","/service-centers/"]:
        if 'href="'+BASE+path+'"' not in s:
            raise RuntimeError("Missing public navigation destination: "+path)
    for brand in ["geely","toyota","kia","hyundai","nissan","mg","chevrolet","byd"]:
        href='href="'+BASE+'/cars/?brand='+brand+'"'
        if href not in s:
            raise RuntimeError("Wrong homepage car-brand logo destination: "+brand)
    if 'class="allbrands" href="'+BASE+'/cars/"' not in s:
        raise RuntimeError("All brands must lead to the cars archive")
    for image in ["a3tal-ref-20261104-service-specs.webp","a3tal-ref-20261104-service-dtc.webp",
                  "tvs-raider-125-egypt.webp","a3tal-egypt-parts-market-20261026-hero-original-20261025-1024x576.webp",
                  "a3tal-ref-20261104-service-maintenance.webp",
                  "a3tal-authorized_hero-real-photograph-20261022-1024x576.webp"]:
        if image not in s: raise RuntimeError("Missing PSEO card artwork: "+image)
    if s.count('class="hub-visual"')!=6:
        raise RuntimeError("Expected six visual homepage PSEO cards")
    if s.count('class="hub-card hub-card-visual"')!=6:
        raise RuntimeError("Expected six compact homepage navigation cards")
    for forbidden in ["استكشف باقي موسوعة أعطال","g-home-dtc-zone",
         "g-home-cars-section","g-home-os-section","g-home-moto-section",
         "g-v3-mobile-dock"]:
        if forbidden in s:
            raise RuntimeError("Duplicate legacy homepage section survived production deployment: "+forbidden)
    if s.count('<nav class="dock"')!=1:
        raise RuntimeError("Expected one V5 mobile dock, no duplicate navigation")
    canon=re.search(r'<link\b[^>]*\brel=["\x27]canonical["\x27][^>]*\bhref=["\x27]([^"\x27]+)',s,re.I)
    if not canon or canon.group(1).rstrip("/")!=BASE:raise RuntimeError("Homepage canonical unexpectedly changed")
    css=session.get(BASE+"/wp-content/themes/a3tal-global/home-reference-20261104.css",timeout=45).text
    if "a3tal-ref-20261104-hero-desktop.webp" not in css:raise RuntimeError("Final reference stylesheet not accessible")
    js=session.get(BASE+"/wp-content/themes/a3tal-global/assets/js/home-reference-20261104.js",timeout=45).text
    if "searchForm" not in js:raise RuntimeError("External search-mode logic absent")
    if 'id="menuToggle"' not in s or "a3tal-v5-home-interactions" not in s:
        raise RuntimeError("Inline mobile navigation interaction absent")
    (REPORT/"homepage-preview-check.json").write_text(json.dumps({"ok":True,"canonical":canon.group(1),
      "h1_count":1,"exact_reference_images":EXPECTED_ASSETS,"old_sections":False},ensure_ascii=False,indent=2),encoding="utf8")
    print("LIVE_HOMEPAGE_REFERENCE_AND_SEO_VERIFIED",flush=True)

def main():
    for path in NEW:
        if not (THEME/path).is_file():raise RuntimeError("Missing reviewed source: "+path)
        if path.endswith(".php"):lint_php(source(path),path)
    images=upload_images()
    bridge=Bridge()
    live={}
    prepared={}
    for name in NEW+EXISTING:
        data=bridge.read(name,missing=name in NEW)
        live[name]=data
        if name in NEW:
            if data and data["content"]!=source(name):
                # Permit only the known, reviewed previous live revisions.
                # Other production edits must stop the deployment, not be overwritten.
                previous={"home-reference-20261104.css":("1ea34bd36d55deceb4c911b2145556d111eb4da3","a958e8225d83138a2c22d818d51747a27a3c1c1c","34d4174bc999f468e8f39f018c2ddb616f2ebdb5"),
                          "home-reference-20261104.php":("c302a40d27311cdd210e38a859360b8606ad8dfa","daf4ac29b66669086c72564f512df0b241d93131","d6c3ee1216a0d7e05db51e28d349f8497aa27c01"),
                          "assets/js/home-reference-20261104.js":"27e9cc0848332616ca1e0b1f6287f2884cb49b57"}
                raw=data["content"].encode("utf8")
                git_blob=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()
                if git_blob not in (previous.get(name) if isinstance(previous.get(name),tuple) else (previous.get(name),)):
                    raise RuntimeError("Live "+name+" differs from audited pre-fix release; refusing overwrite")
                print("AUDITED_REFERENCE_UPGRADE",name,flush=True)
            prepared[name]=source(name)
        elif name=="front-page.php":prepared[name]=modify_front(data["content"])
        elif name=="header.php":prepared[name]=modify_header(data["content"])
        elif name=="functions.php":prepared[name]=modify_functions(data["content"])
        if name in EXISTING:
            (REPORT/(name+".before.txt")).write_text(data["content"],encoding="utf8")
    print("LIVE_THEME_PREFLIGHT_SHA_VALIDATED",flush=True)
    changed=[]
    try:
        for name in NEW+EXISTING:
            wanted=prepared[name]
            old=live[name]
            if old and old["content"]==wanted:
                print("SKIPPED_ALREADY_DEPLOYED",name,flush=True);continue
            expected=old["sha256"] if old else sha(b"")
            bridge.write(name,wanted,expected)
            changed.append(name)
            print("DEPLOYED_VERIFIED",name,flush=True)
        bridge.flush()
        verify_live()
    except Exception:
        print("DEPLOYMENT_CHECK_FAILED_STARTING_GUARDED_ROLLBACK",flush=True)
        for name in reversed(changed):
            old=live[name]
            if old is None:continue  # dormant new file is harmless when original header/home restored
            try:
                bridge.write(name,old["content"],sha(prepared[name].encode("utf8")))
                print("ROLLBACK_VERIFIED",name,flush=True)
            except Exception as e:
                print("ROLLBACK_REQUIRES_MANUAL_REVIEW",name,type(e).__name__,flush=True)
        try:bridge.flush()
        except Exception:pass
        raise
    print("SUCCESS_EXACT_27_REFERENCE_ASSETS_AND_HOMEPAGE_DEPLOYED",len(images),flush=True)

if __name__=="__main__":main()
