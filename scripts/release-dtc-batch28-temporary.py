#!/usr/bin/env python3
"""One batch28-only production release: user-authorized temporary photo-based covers.
No other batch flag changed. Never replay an ambiguous WordPress write.
"""
import importlib.util,json,os,subprocess,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
CODES="P0262 P0354 P0620 U0142 U0150 U0153 C0052 C0053 B2103 B2431".split()
def execute(*args):
    print("BATCH28_RELEASE_STEP"," ".join(map(str,args)),flush=True)
    subprocess.run(list(map(str,args)),cwd=str(ROOT),check=True)
def main():
    if os.getenv("A3TAL_BATCH28_TEMP_RELEASE")!="1":raise RuntimeError("Explicit temporary release not authorized")
    if not os.getenv("A3TAL_API_KEY"):raise RuntimeError("Missing protected A3tal Bridge key")
    data=json.loads((ROOT/"data/dtc-original-batch-28.json").read_text(encoding="utf-8"))
    if [x.get("code") for x in data.get("items",[])]!=CODES:raise RuntimeError("Unexpected code roster")
    if data.get("ready_for_auto_publish") is not False:raise RuntimeError("Automatic release gate must remain closed for temporary images")
    execute(sys.executable,"scripts/validate-dtc-batch28.py")
    execute(sys.executable,"scripts/publish-dtc-original-batch-28.py","--dry-run")
    execute(sys.executable,"scripts/render-dtc-batch-28-art.py")
    # Validate every temporary image BEFORE any WordPress post or attachment write.
    manifest=json.loads((ROOT/"assets/dtc-batch28/manifest.json").read_text(encoding="utf-8"))
    import hashlib
    if manifest.get("release_class")!="TEMPORARY_ART_EXPLICITLY_AUTHORIZED_BY_OWNER":
        raise RuntimeError("Unexpected photo release class")
    entries=manifest.get("files",[])
    if [r.get("code") for r in entries]!=CODES:raise RuntimeError("Missing or reordered temporary images")
    for entry in entries:
        p=ROOT/"assets/dtc-batch28"/entry["filename"]
        raw=p.read_bytes()
        with Image.open(p) as im:
            if im.format!="WEBP" or im.size!=(1600,900):raise RuntimeError("Bad temporary image "+entry["code"])
            im.verify()
        if hashlib.sha256(raw).hexdigest()!=entry["sha256"] or len(raw)!=entry["bytes"]:
            raise RuntimeError("Image manifest mismatch "+entry["code"])
    print("BATCH28_ALL_TEN_TEMP_IMAGES_VERIFIED_BEFORE_PUBLISH",flush=True)
    # Import only read-only existing-code routine: any duplicate or hole halts this run.
    spec=importlib.util.spec_from_file_location("dtc_queue_read", ROOT/"scripts/scheduled-dtc-reviewed-queue.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    rows=[mod.fetch_published_code(code) for code in CODES]
    count=sum(x is not None for x in rows)
    if any(x is None for x in rows[:count]) or any(x is not None for x in rows[count:]):
        raise RuntimeError("Noncontiguous partial batch28 detected; no WordPress mutations")
    if any(x is not None and x.get("status")!="publish" for x in rows):
        raise RuntimeError("Existing unpublished article detected")
    print("BATCH28_EXISTING_PUBLIC_POSTS",count,"TO_CREATE",10-count,flush=True)
    if count<10:
        execute(sys.executable,"scripts/publish-dtc-original-batch-28.py","--from-index",count)
    # Recheck after all writes, and never attach artwork to missing/duplicate posts.
    after=[mod.fetch_published_code(code) for code in CODES]
    if any(x is None or x.get("status")!="publish" for x in after):
        raise RuntimeError("Not all 10 codes published; halt before media writes")
    print("BATCH28_TEN_ARTICLES_PUBLISHED",flush=True)
    execute(sys.executable,"scripts/attach-dtc-batch-28-photos.py")
    execute(sys.executable,"scripts/repair-dtc-og-canary.py","--batch","28")
    execute(sys.executable,"scripts/audit-dtc-og-images.py","--batch","28")
    for code in CODES:print("BATCH28_FINAL_VERIFIED_URL",f"https://a3tal.com/dtc/{code.lower()}/",flush=True)
    print("BATCH28_TEMPORARY_RELEASE_COMPLETE_IMAGES_AND_OG_CHECKED",flush=True)
if __name__=="__main__":main()
