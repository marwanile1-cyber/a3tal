#!/usr/bin/env python3
"""Guarded A3tal Direct Bridge deployment of Egypt homepage brands, prices and PSEO.

Scoped patches only. No posts, URLs, database records, or canonicals are mutated.
Creates rollback evidence and validates current live output before reporting success.
"""
from pathlib import Path
from importlib.machinery import SourceFileLoader
import hashlib, json, os, re, subprocess, tempfile, time, types
import requests

BASE="https://a3tal.com"
THEME=Path("theme-source/a3tal-global")
OUT=Path("reports/egypt-home-brands-prices-pseo-20261108")
OUT.mkdir(parents=True,exist_ok=True)
if not os.environ.get("A3TAL_API_KEY"):raise SystemExit("A3TAL_API_KEY is missing")
mod=types.ModuleType("A3talScopedBridge")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge
HOME="home-reference-20261104.php"
HOME_CSS="home-reference-20261104.css"
HEADER="home-reference-header-20261104.php"
PRICE="car-price-guide.php"
PRICE_CSS="car-price-guide.css"
PARTIAL="brand-collection-20261108.php"
FUNCTIONS="functions.php"
FILES=[PARTIAL,PRICE_CSS,PRICE,HOME_CSS,HOME,HEADER,FUNCTIONS]
BEGIN_HOME="<!-- A3TAL-EGYPT-BRANDS-20261108-BEGIN -->"
END_HOME="<!-- A3TAL-EGYPT-HOME-PSEO-20261108-END -->"
BEGIN_CSS="/* A3TAL EGYPT HOMEPAGE BRANDS PRICES PSEO - approved 2026-11-08 */"
END_CSS="/* END A3TAL EGYPT HOMEPAGE BRANDS PRICES PSEO 2026-11-08 */"
BEGIN_PRICE_CSS="/* A3TAL EGYPT BRAND COLLECTION 20261108:"
END_PRICE_CSS="/* END A3TAL EGYPT BRAND COLLECTION 20261108 */"
BEGIN_ALIAS="// Current Egypt-market brand aliases, for published-article title discovery."
END_ALIAS="$cg_brand_selected=$cg_brand_directory[$cg_brand_slug]??null;"
OLD_BRANDS='<section class="brands-bar">'
END_BRANDS='<div class="wrap"><section class="catalog">'
BENEFITS='    <section class="cg-benefits" aria-label="مميزات دليل السيارات">'
EXTRA='    <?php if($cg_brand_selected) require get_template_directory().\'/brand-collection-20261108.php\'; ?>'
CSS_VERSION="20261108.1"

def sha(s):return hashlib.sha256(s.encode("utf-8")).hexdigest()
def source(name):return (THEME/name).read_text("utf-8")
def one(s,marker):
    if s.count(marker)!=1:raise RuntimeError("Expected exactly one "+marker[:75])
    return s.index(marker)
def extract(s,start,end,tail_newline=False):
    i=one(s,start);j=one(s,end)+len(end)
    if j<i:raise RuntimeError("Markers out of order")
    if tail_newline and s[j:j+1]=="\n":j+=1
    return s[i:j]
def append_scoped(old,src,start,end):
    block=extract(src,start,end)
    if start in old or end in old:
        if old.count(block)!=1:raise RuntimeError("Conflicting partial scoped CSS")
        return old
    return old.rstrip()+"\n\n"+block+"\n"
def php_lint(s):
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"test.php"
        p.write_text(s,"utf-8")
        subprocess.run(["php","-l",str(p)],check=True,capture_output=True,timeout=25)

def patch_home(old):
    src=source(HOME)
    block=extract(src,BEGIN_HOME,END_HOME,True)
    if BEGIN_HOME in old or END_HOME in old:
        if old.count(block)!=1:raise RuntimeError("Home has a different 20261108 component; refusing overwrite")
        return old
    i=one(old,OLD_BRANDS);j=one(old,END_BRANDS)
    original=old[i:j]
    if original.count('class="brand"')!=8 or original.count("a3tal-ref-20261104-brand-")!=8:
        raise RuntimeError("Live brand logos no longer match audited Egyptian V5")
    updated=old[:i]+block+old[j:]
    php_lint(updated)
    if updated.count('class="a3egy-brand"')!=24:raise RuntimeError("24 links required")
    if updated.count('id="egypt-car-prices"')!=1 or updated.count('id="egypt-pseo"')!=1:
        raise RuntimeError("Home price and PSEO sections missing")
    return updated

def patch_price(old):
    src=source(PRICE)
    patch=extract(src,BEGIN_ALIAS,END_ALIAS,False)
    if BEGIN_ALIAS not in old:
        a=one(old,END_ALIAS)
        old=old[:a]+patch.replace(END_ALIAS,"")+old[a:]
    elif old.count(patch)!=1:raise RuntimeError("Brand directory has conflicting changes")
    old_begin='<?php elseif($cg_brand_selected && $cg_related_guides): ?>'
    new_begin='<?php elseif($cg_brand_selected): ?>'
    end='<?php else: ?><p class="cg-empty">مفيش موديلات مطابقة للفلاتر دي حاليًا.'
    if old_begin in old:
        i=one(old,old_begin);j=one(old,end)
        new_fragment=extract(src,new_begin,end).split(end,1)[0]
        old=old[:i]+new_fragment+old[j:]
    elif new_begin not in old:raise RuntimeError("Archive empty-brand presentation changed")
    subs=[
      ('<?php if ($cg_brands): ?>','<?php if ($cg_brand_directory): ?>'),
      ('<?php foreach(array_slice($cg_brands,0,18) as $term): ?>','<?php foreach($cg_brand_directory as $brand_slug=>$brand_info): ?>'),
      ("<?php echo esc_attr($term->name); ?>","<?php echo esc_attr($brand_info['name']); ?>"),
      ("<?php echo esc_url(add_query_arg('brand',$term->slug,$cg_url)); ?>","<?php echo esc_url(add_query_arg('brand',$brand_slug,$cg_url)); ?>"),
      ("<?php echo esc_html(function_exists('mb_substr') ? mb_substr($term->name,0,2) : substr($term->name,0,2)); ?>","<?php echo esc_html(strtoupper($brand_slug)); ?>"),
      ("<?php echo esc_html($term->name); ?>","<?php echo esc_html($brand_info['name']); ?>"),
      ("""<?php foreach($cg_brands as $t): ?><option value="<?php echo esc_attr($t->slug); ?>" <?php selected($cg_brand,$t->slug); ?>><?php echo esc_html($t->name); ?></option><?php endforeach; ?>""",
       """<?php foreach($cg_brand_directory as $slug=>$brand): ?><option value="<?php echo esc_attr($slug); ?>" <?php selected($cg_brand_slug,$slug); ?>><?php echo esc_html($brand['name']); ?></option><?php endforeach; ?>""")
    ]
    for a,b in subs:
        if a in old:
            if old.count(a)!=1:raise RuntimeError("Ambiguous brand listing selector")
            old=old.replace(a,b,1)
        elif b not in old:raise RuntimeError("Archive brand listing unexpected: "+a[:70])
    if EXTRA not in old:
        i=one(old,BENEFITS)
        old=old[:i]+EXTRA+"\n\n"+old[i:]
    if "get_template_directory_uri().'/car-price-guide.css',[], '1.1.0'" in old:
        old=old.replace("get_template_directory_uri().'/car-price-guide.css',[], '1.1.0'",
                        "get_template_directory_uri().'/car-price-guide.css',[], '1.1.1'",1)
    if "get_template_directory_uri().'/car-price-guide.css',[], '1.1.1'" not in old:
        raise RuntimeError("Archive CSS version missing")
    php_lint(old)
    return old

def patch_header(old):
    current=old
    replacements=[
        ('<a href="https://a3tal.com/?s=سعر">الأسعار</a>',
         '<a href="https://a3tal.com/cars/">أسعار السيارات</a>'),
        ('<a href="https://a3tal.com/car-reference/">دليل السيارات</a>',
         '<a href="https://a3tal.com/#egypt-car-brands">الماركات</a><a href="https://a3tal.com/car-reference/">دليل السيارات</a>')
    ]
    for a,b in replacements:
        if a in current:
            if current.count(a)!=1:raise RuntimeError("Header target duplicated")
            current=current.replace(a,b,1)
        elif b not in current:raise RuntimeError("Header navigation no longer matches")
    php_lint(current)
    return current

def patch_functions(old):
    # Do not overwrite any unrelated production PHP; only refresh home style version.
    if CSS_VERSION in old:return old
    patterns=[
      r"(wp_enqueue_style\('a3g-reference-v5'[^;\n]*?,['\"])20261104\.\d+(['\"]\);)",
      r"(wp_enqueue_style\('a3g-encyclopedia-home'[^;\n]*?,['\"])20261104-v5[a-z]?(['\"]\);)"
    ]
    for pattern in patterns:
        result,count=re.subn(pattern,lambda m:m.group(1)+CSS_VERSION+m.group(2),old,count=1)
        if count==1:
            php_lint(result)
            return result
    raise RuntimeError("Production homepage CSS registration not recognized; avoid stale render")

def verify_site():
    session=requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0 (A3tal QA; Linux)","Cache-Control":"no-cache"})
    last={}
    for n in range(5):
        try:
            response=session.get(BASE+"/?a3tal_brand_review="+str(time.time_ns()),timeout=45)
            html=response.text
            last={"status":response.status_code,"brands":html.count('class="a3egy-brand"'),
                  "prices":'id="egypt-car-prices"' in html,"pseo":'id="egypt-pseo"' in html}
            if response.status_code==200 and last["brands"]==24 and last["prices"] and last["pseo"]:break
        except requests.RequestException as e:last={"exception":type(e).__name__}
        if n==4:raise RuntimeError("Homepage public QA: "+json.dumps(last))
        time.sleep(8)
    if len(re.findall(r"<h1\b",html,re.I))!=1:raise RuntimeError("Wrong H1 count")
    for s in ["?brand=geely","?brand=chery","?brand=jetour","?brand=jaecoo",
              "?brand=byd","?brand=chevrolet","?brand=ford"]:
        if s not in html:raise RuntimeError("Missing brand link "+s)
    if "أحدث موديلات السيارات" not in html:raise RuntimeError("Existing homepage modules lost")
    for slug in ("geely","ford","chery"):
        response=session.get(BASE+"/cars/?brand="+slug+"&qa="+str(time.time_ns()),timeout=50)
        text=response.text
        if response.status_code!=200 or 'id="all-brand-content"' not in text:
            raise RuntimeError("Missing public brand archive: "+slug+" HTTP "+str(response.status_code))
        if "cg-brand-editorial-list" not in text and "cg-empty" not in text:
            raise RuntimeError("No published editorial/empty state for "+slug)
    css=session.get(BASE+"/wp-content/themes/a3tal-global/home-reference-20261104.css?ver="+CSS_VERSION,timeout=40).text
    if BEGIN_CSS not in css:raise RuntimeError("New homepage stylesheet missing")
    return {"ok":True,"home":last,"brand_pages":["geely","ford","chery"],
            "canonical_home":"https://a3tal.com/","no_published_posts_modified":True}

def main():
    for p in (HOME,HEADER,PRICE,PARTIAL):
        php_lint(source(p))
    bridge=Bridge()
    info=bridge.request({"op":"site_info"})
    if info.get("active_theme")!="a3tal-global":raise RuntimeError("Wrong live theme")
    originals={}
    for name in FILES:
        originals[name]=bridge.read(name,missing=(name==PARTIAL))
    desired={}
    desired[PARTIAL]=source(PARTIAL)
    if originals[PARTIAL] and originals[PARTIAL]["content"]!=desired[PARTIAL]:
        raise RuntimeError("Existing live brand partial differs; no overwrite")
    desired[PRICE_CSS]=append_scoped(originals[PRICE_CSS]["content"],source(PRICE_CSS),BEGIN_PRICE_CSS,END_PRICE_CSS)
    desired[PRICE]=patch_price(originals[PRICE]["content"])
    desired[HOME_CSS]=append_scoped(originals[HOME_CSS]["content"],source(HOME_CSS),BEGIN_CSS,END_CSS)
    desired[HOME]=patch_home(originals[HOME]["content"])
    desired[HEADER]=patch_header(originals[HEADER]["content"])
    desired[FUNCTIONS]=patch_functions(originals[FUNCTIONS]["content"])
    (OUT/"rollback.json").write_text(json.dumps({
       k:{"content":v["content"],"sha256":v["sha256"]} if v else None
       for k,v in originals.items()},ensure_ascii=False),encoding="utf-8")
    print("PREFLIGHT_CHECKED_24_BRANDS_REAL_PRICES_PSEO_AND_COLLECTION",flush=True)
    changed=[]
    try:
        for name in FILES:
            before=originals[name]
            if before and before["content"]==desired[name]:
                print("ALREADY_MATCHES",name,flush=True);continue
            bridge.write(name,desired[name],before["sha256"] if before else sha(""))
            changed.append(name)
            print("WRITTEN_AND_CHECKSUM_VERIFIED",name,flush=True)
        bridge.flush()
        report=verify_site()
        (OUT/"public-qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),"utf-8")
        print("SUCCESS_LIVE_EGYPT_PRICES_PSEO_BRANDS_24",flush=True)
    except Exception:
        print("DEPLOYMENT_ERROR_ATTEMPTING_GUARDED_ROLLBACK",flush=True)
        for name in reversed(changed):
            before=originals[name]
            # Existing files are restored by CAS. New partial remains unreachable after rollback.
            if before is None:continue
            try:
                bridge.write(name,before["content"],sha(desired[name]))
                print("RESTORED",name,flush=True)
            except Exception as e:
                print("ROLLBACK_MANUAL_REVIEW_NEEDED",name,str(e),flush=True)
        try:bridge.flush()
        except Exception:pass
        raise

if __name__=="__main__":main()
