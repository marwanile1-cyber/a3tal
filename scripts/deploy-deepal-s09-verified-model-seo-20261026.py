#!/usr/bin/env python3
"""Scoped source-backed S09 model page SEO rollout with live theme-file backup/rollback.
Only modifies vehicle #84627 and appends a gated filter to existing live functions.php.
Leaves all other car robots, sitemap policies, article URLs and theme design untouched.
"""
import argparse,hashlib,json,os,subprocess,tempfile,types,urllib.request,urllib.parse
from pathlib import Path
from importlib.machinery import SourceFileLoader
mod=types.ModuleType("a3tal_existing_guarded_bridge")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge
REPO_FN=Path("theme-source/a3tal-global/functions.php")
CAR_BODY=Path("data/editorial/deepal-s09-2027-encyclopedia-vehicle-20261026.html")
START="/* A3TAL-DEEPAL-S09-VERIFIED-CAR-INDEX-20261026:START */"
END="/* A3TAL-DEEPAL-S09-VERIFIED-CAR-INDEX-20261026:END */"
API="https://a3tal.com"
def sha(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def patch_block():
    source=REPO_FN.read_text("utf8")
    if source.count(START)!=1 or source.count(END)!=1:raise RuntimeError("Approved S09-only SEO patch not unique")
    content=source[source.index(START):source.index(END)+len(END)]
    if "84627" not in content or "84623" not in content or "6500" not in content:
        raise RuntimeError("Approved noindex exception is not safely gated")
    return content
def phpcheck(text):
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"functions.php";p.write_text(text,"utf8")
        subprocess.run(["php","-l",str(p)],check=True,timeout=25)
def load_state(d):return json.loads((Path(d)/"s09-live-theme-backup.json").read_text("utf8"))
def prepare(d):
    p=Path(d);p.mkdir(parents=True,exist_ok=True)
    current=Bridge().read("functions.php")
    content=current["content"]
    if not all(x in content for x in ("a3g_structured_car_robots","a3g_verified_chery_indexable_request","add_filter('wpseo_robots'")):
        raise RuntimeError("Unexpected live SEO layer: refuse mutation")
    if START in content or END in content:
        if content.count(START)==1 and patch_block() in content:
            print("S09_INDEX_PATCH_ALREADY_PRESENT",flush=True)
        else:raise RuntimeError("Unknown partial S09 live patch, not touching it")
    phpcheck(content)
    state={"content":content,"sha256":sha(content),"preexisting_patch":START in content}
    (p/"s09-live-theme-backup.json").write_text(json.dumps(state,ensure_ascii=False),"utf8")
    print("LIVE_THEME_BACKED_UP",state["sha256"],"chars",len(content),flush=True)
def req(path,body=None):
    h={"Accept":"application/json","User-Agent":"A3tal-S09-CarIndex-QA/20261026","Cache-Control":"no-cache,no-store"}
    raw=json.dumps(body,ensure_ascii=False).encode("utf8") if body else None
    if raw:h["Content-Type"]="application/json"
    with urllib.request.urlopen(urllib.request.Request(API+path,data=raw,headers=h,method="POST" if raw else "GET"),timeout=75) as r:
        return json.load(r)
def update_car():
    prior=req("/wp-json/wp/v2/a3tal-cars/84627?_fields=id,slug,status,title,featured_media,content")
    if prior.get("slug")!="deepal-s09-2027-egypt" or prior.get("status")!="publish" or not prior.get("featured_media"):
        raise RuntimeError("Car identity/media drift")
    content=CAR_BODY.read_text("utf8")
    if len(content)<9500 or content.count("<h2>")<9 or content.count("<table")<1:
        raise RuntimeError("Substantive model page content below index exception gate")
    data={"op":"platform_entity_upsert","id":84627,"type":"a3_car",
          "title":"ديبال S09 موديل 2027 في مصر | الأسعار والمواصفات",
          "slug":"deepal-s09-2027-egypt","status":"publish",
          "content":content,"taxonomies":{"a3_brand":["deepal"],"a3_car_body":["suv"],"a3_market":["egypt"]},
          "meta":{"_a3_related_post_ids":"84623","_a3_source_checked_at":"2026-10-26",
                  "_yoast_wpseo_meta-robots-noindex":"2"},
          "confirm":True,"dangerous":True}
    b=Bridge()
    result=b.request(data,write=True)
    if not result.get("id") or int(result["id"])!=84627:raise RuntimeError("Car update was not acknowledged")
    latest=req("/wp-json/wp/v2/a3tal-cars/84627?_fields=id,slug,status,featured_media,content")
    rendered=(latest.get("content") or {}).get("rendered","")
    if len(rendered)<9500 or latest.get("featured_media")!=prior["featured_media"]:
        raise RuntimeError("Published car content/cover readback failure")
    print("SOURCE_BACKED_ENRICHED_CAR_VERIFIED",84627,"HTML_CHARS",len(rendered),flush=True)
def deploy(d):
    state=load_state(d)
    live=Bridge().read("functions.php")
    original=live["content"]
    approved=patch_block()
    if START in original:
        if original.count(START)==1 and approved in original:
            print("LIVE_S09_THEME_PATCH_ALREADY_MATCHES",flush=True)
            return
        raise RuntimeError("Existing live theme patch is not the approved one")
    if sha(original)!=state["sha256"]:
        raise RuntimeError("Live functions.php changed after snapshot; abort without overwrite")
    if original.count("a3g_structured_car_robots")!=2:
        raise RuntimeError("Unexpected existing car robots filter structure")
    patched=original.rstrip()+"\n\n"+approved+"\n"
    phpcheck(patched)
    Bridge().write("functions.php",patched,expected=state["sha256"])
    (Path(d)/"s09-deployed-theme-sha.txt").write_text(sha(patched),"utf8")
    print("LIVE_S09_FILTER_SCOPED_DEPLOYED",sha(patched),flush=True)
def verify():
    url="/cars/deepal-s09-2027-egypt/"
    # Public source needs both index directive and canonical, unlike Yoast REST-only checks.
    # Add harmless fresh query to bypass stale URL HTML caches.
    request=urllib.request.Request(API+url+"?a3tal_s09_seo_check=20261026",
        headers={"User-Agent":"Mozilla/5.0 A3tal-SEO-Audit/2026-10-26","Cache-Control":"no-cache"})
    with urllib.request.urlopen(request,timeout=75) as response:
        html=response.read(1_800_000).decode("utf8","replace")
    low=html.lower()
    if 'name="robots" content="noindex' in low or "noindex, follow" in low:
        raise RuntimeError("Public car page STILL noindex after theme patch")
    if "index, follow" not in low or "deepal-s09-2027-egypt/" not in low:
        raise RuntimeError("Public index/canonical proof missing")
    if "s09-official-exterior" not in low or "deepal-s09-2027-egypt-price-premium-signature-reev" not in low:
        raise RuntimeError("S09 model photo/editorial link missing")
    print("PUBLIC_S09_CAR_INDEX_FOLLOW_CANONICAL_VERIFIED",API+url,flush=True)
def rollback(d):
    state=load_state(d)
    deployed=Path(d)/"s09-deployed-theme-sha.txt"
    if not deployed.exists():
        print("NO_THEME_MUTATION_TO_REVERT",flush=True);return
    b=Bridge()
    live=b.read("functions.php")
    if sha(live["content"])==state["sha256"]:
        print("THEME_ALREADY_ORIGINAL",flush=True);return
    if sha(live["content"])!=deployed.read_text("utf8").strip():
        raise RuntimeError("Current live theme changed externally; refuse blind rollback")
    b.write("functions.php",state["content"],expected=sha(live["content"]))
    print("S09_THEME_ROLLED_BACK_TO_EXACT_PREDEPLOY_BACKUP",flush=True)
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("operation",choices=["prepare","update-car","deploy","verify","rollback"])
    ap.add_argument("--state-dir",default=os.environ.get("RUNNER_TEMP","/tmp"))
    a=ap.parse_args()
    {"prepare":prepare,"update-car":lambda d:update_car(),
     "deploy":deploy,"verify":lambda d:verify(),"rollback":rollback}[a.operation](a.state_dir)
