#!/usr/bin/env python3
"""Safety-gated, half-hourly GitHub Actions DTC *publication* queue.

Publish AT MOST one pre-authored, reviewed batch of TEN codes per scheduled run.
This tool does not generate content, invent definitions, or silently repeat
WordPress mutations. A missing/incomplete batch is a benign no-op.

Requires matching, reviewed files for batch NN:
 data/dtc-original-batch-NN.json (ready_for_auto_publish:true)
 scripts/publish-dtc-original-batch-NN.py
 scripts/render-dtc-batch-NN-art.py
 scripts/attach-dtc-batch-NN-photos.py
 plus NN registered in audit-dtc-og-images.py and repair-dtc-og-canary.py.

The matching publisher independently handles live code duplication checks.
If any post write becomes ambiguous, the publisher halts rather than replaying.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/"data"
SCRIPTS=ROOT/"scripts"
START_BATCH=25
SITE="https://a3tal.com"
CODE_RE=re.compile(r"^[PBCU][0-9][0-9A-F]{3}$")
DISTRIBUTION={"P":3,"U":3,"C":2,"B":2}


class TransientReadError(RuntimeError):
    """Temporary site or edge outage before any publication mutation."""



def print_state(*parts):
    print("AUTO_DTC_QUEUE", *parts, flush=True)


def run(*cmd):
    print_state("RUN", " ".join(str(arg) for arg in cmd))
    subprocess.run(list(map(str,cmd)),cwd=str(ROOT),check=True)


def fetch_published_code(code):
    url=SITE+"/wp-json/wp/v2/a3tal-dtc?"+urllib.parse.urlencode({
        "slug":code.lower(), "per_page":2, "_fields":"id,slug,status,featured_media,yoast_head_json"
    })
    req=urllib.request.Request(url,headers={
        "User-Agent":"A3tal-GitHub-Reviewed-Scheduler/1.0",
        "Accept":"application/json", "Cache-Control":"no-cache",
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=40) as stream:
                records=json.load(stream)
            if not isinstance(records,list):
                raise RuntimeError("Unexpected WordPress REST response")
            exact=[p for p in records if p.get("slug")==code.lower()]
            if len(exact)>1:
                raise RuntimeError("Duplicate WordPress page detected for "+code)
            return exact[0] if exact else None
        except urllib.error.HTTPError as exc:
            if attempt==2 or exc.code not in (408, 429, 500, 502, 503, 504, 520, 521, 522, 523, 524, 525, 526):
                if exc.code in (408, 429, 500, 502, 503, 504, 520, 521, 522, 523, 524, 525, 526):
                    raise TransientReadError("Temporary HTTP "+str(exc.code)+" reading "+code) from exc
                raise RuntimeError("Unexpected HTTP "+str(exc.code)+" reading "+code) from exc
            time.sleep(19*(attempt+1))
        except (urllib.error.URLError,TimeoutError) as exc:
            if attempt==2:
                raise TransientReadError("Temporary site connection failure reading "+code) from exc
            time.sleep(19*(attempt+1))


def check_batch(number,path):
    data=json.loads(path.read_text(encoding="utf-8"))
    if data.get("ready_for_auto_publish") is not True:
        return None,"awaiting explicit reviewed-ready flag"
    if number >= 28:
        qa=data.get("release_quality",{})
        required=(
            "photographic_covers_manually_reviewed",
            "article_specific_diagnostic_depth_reviewed",
            "source_and_oem_scope_verified",
            "relevant_video_embeds_checked_or_absence_explained",
            "originality_and_duplicate_intent_reviewed",
        )
        if not isinstance(qa,dict) or any(qa.get(k) is not True for k in required):
            return None,"batch28+ is blocked until photographic/editorial/video safety reviews are complete"
        for entry in data.get("items",[]):
            if not entry.get("video") and len(entry.get("no_video_reason","").strip())<40:
                return None,"video absent without specific source-research explanation: "+entry.get("code","unknown")
        renderer=SCRIPTS/f"render-dtc-batch-{number:02d}-art.py"
        if renderer.is_file():
            code=renderer.read_text(encoding="utf-8")
            if "ImageDraw" in code or "entirely drawn" in code.lower():
                return None,"Pillow-drawn featured images are forbidden for new DTC releases"
    items=data.get("items")
    if not isinstance(items,list) or len(items)!=10:
        raise RuntimeError(f"Batch {number} is not exactly 10 authored guides")
    codes=[item.get("code","") for item in items]
    registry_path=DATA/"dtc-eight-batch-editorial-plan-25-32.json"
    if not registry_path.is_file():
        raise RuntimeError("Approved eight-batch code registry is missing")
    registry=json.loads(registry_path.read_text(encoding="utf-8"))
    matches=[row for row in registry.get("batches",[]) if row.get("batch")==number]
    if len(matches)!=1 or [r["code"] for r in matches[0]["items"]]!=codes:
        raise RuntimeError("New published codes differ from the pre-reviewed eight-batch plan")
    for item,outlined in zip(items,matches[0]["items"]):
        intended=str(outlined.get("scope",""))
        if intended.startswith("oem:") and item.get("scope")!=intended:
            raise RuntimeError("OEM scope changed relative to approved editorial plan: "+item["code"])
    if len(set(codes))!=10 or any(not CODE_RE.fullmatch(c) for c in codes):
        raise RuntimeError(f"Batch {number} contains duplicate or invalid codes")
    if {p:sum(c.startswith(p) for c in codes) for p in DISTRIBUTION}!=DISTRIBUTION:
        raise RuntimeError(f"Batch {number} does not meet 3P/3U/2C/2B mix")
    if any(item.get("scope") is None for item in items):
        raise RuntimeError("A guide has no generic/OEM definition scope")
    required=[
      SCRIPTS/f"publish-dtc-original-batch-{number:02d}.py",
      SCRIPTS/f"render-dtc-batch-{number:02d}-art.py",
      SCRIPTS/f"attach-dtc-batch-{number:02d}-photos.py",
    ]
    absent=[str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    audits=(SCRIPTS/"audit-dtc-og-images.py").read_text()
    repair=(SCRIPTS/"repair-dtc-og-canary.py").read_text()
    key=f'"{number:02d}"'
    if key not in audits or key not in repair:
        absent.append("batch code not registered in both OG/audit scripts")
    if absent:
        return None,"awaiting required reviewed files: "+", ".join(absent)
    if any(len(item.get("steps",[]))!=5 or len(item.get("faqs",[]))!=3 for item in items):
        raise RuntimeError("Every scheduled guide must have five unique steps and 3 FAQs")
    if any(not item.get("source","").startswith("https://") for item in items):
        raise RuntimeError("Every scheduled code requires a citable technical reference")
    return (items,required),""


def unique_images(codes,number):
    folder=ROOT/f"assets/dtc-batch{number:02d}"
    manifest=folder/"manifest.json"
    if not manifest.is_file():
        raise RuntimeError("Missing unique WebP image manifest for batch "+str(number))
    data=json.loads(manifest.read_text(encoding="utf-8"))
    assets=data.get("files",[])
    if len(assets)!=10 or {entry["code"] for entry in assets}!=set(codes):
        raise RuntimeError("Original art manifest does not match the ten codes")
    if number>=28:
        qa=data.get("photographic_qa",{})
        entries=data.get("files",[])
        if qa.get("approved") is not True or qa.get("reviewer","").strip()=="" or \
           any(item.get("photorealism_approved") is not True or
               item.get("image_origin") not in ("original_photo","original_ai_photorealistic")
               for item in entries):
            raise RuntimeError("New DTC covers lack human-reviewed photographic provenance")
    digests=set()
    from PIL import Image
    for code in codes:
        path=folder/f"a3tal-dtc-{code.lower()}-exclusive.webp"
        raw=path.read_bytes()
        if not (25000<len(raw)<500000):
            raise RuntimeError("WebP cover size out of policy: "+code)
        with Image.open(path) as pic:
            if pic.format!="WEBP" or pic.size!=(1600,900):
                raise RuntimeError("Not the required original 1600x900 WebP: "+code)
            pic.verify()
        h=hashlib.sha256(raw).hexdigest()
        if h in digests:
            raise RuntimeError("Identical artwork repeated across codes")
        digests.add(h)
        entry=next(item for item in assets if item["code"]==code)
        if entry["sha256"]!=h or entry["bytes"]!=len(raw):
            raise RuntimeError("Image differs from editorial manifest: "+code)


def process_one(number,items,files,check_only):
    codes=[x["code"] for x in items]
    print_state("NEXT_REVIEWED_BATCH",number,",".join(codes))
    run(sys.executable,"-m","py_compile",*files)
    run(sys.executable,files[0],"--dry-run")
    if check_only:
        print_state("CHECK_ONLY_VALIDATED",number)
        return
    if not os.getenv("A3TAL_API_KEY"):
        raise RuntimeError("Publishing secret missing; never send an unauthenticated WordPress write")

    # Check all existing posts before any write. Only a contiguous published
    # prefix can be resumed. A hole indicates unexpected editorial changes.
    status=[]
    for code in codes:
        row=fetch_published_code(code)
        if row and row.get("status")!="publish":
            raise RuntimeError("Existing draft/private page requires editorial reconciliation: "+code)
        status.append(row)
        time.sleep(1.3)
    active=sum(row is not None for row in status)
    if status[:active] != [r for r in status if r is not None]:
        raise RuntimeError("Noncontiguous partial publication; stop to avoid duplicates")
    if any(r is not None for r in status[active:]):
        raise RuntimeError("Noncontiguous partial publication; stop for manual review")

    # Do not start a new publication wave while the previous ten-code
    # batch lacks publicly visible featured images or correct share art.
    if number==25:
        run(sys.executable,SCRIPTS/"audit-dtc-og-images.py","--batch","24")

    # Covers render locally and are verified BEFORE further WordPress posts.
    run(sys.executable,files[1])
    unique_images(codes,number)

    if active<10:
        print_state("PUBLISH_MISSING_ONLY",number,"start-index",active,"remaining",10-active)
        run(sys.executable,files[0],"--from-index",active)
    else:
        print_state("POSTS_ALREADY_LIVE",number,"resuming media/OG checks only")

    run(sys.executable,files[2])
    run(sys.executable,SCRIPTS/"repair-dtc-og-canary.py","--batch",f"{number:02d}")
    run(sys.executable,SCRIPTS/"audit-dtc-og-images.py","--batch",f"{number:02d}")
    print_state("BATCH_COMPLETED",number,"10 articles, 10 featured WebP, verified OpenGraph")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check-only",action="store_true")
    args=parser.parse_args()
    batch_files=[]
    for path in sorted(DATA.glob("dtc-original-batch-*.json")):
        m=re.fullmatch(r"dtc-original-batch-(\d{2}).json",path.name)
        if m and int(m.group(1))>=START_BATCH:
            batch_files.append((int(m.group(1)),path))
    if not batch_files:
        print_state("WAITING_FOR_PREWRITTEN_REVIEWED_BATCH", "No batch 25+ content found. No WordPress writes.")
        return
    for number,path in batch_files:
        ready,reason=check_batch(number,path)
        if ready is None:
            # Batch 28 was released separately under the owner's explicit
            # temporary-photo release. Its editorial auto-release flag must
            # remain false, but a fully published/OG-verified batch should not
            # permanently block future reviewed batches. This is READ-ONLY:
            # never bypass incomplete batch 28 or release batch 29.
            if number == 28:
                held_data = json.loads(path.read_text(encoding="utf-8"))
                historical_codes = "P0262 P0354 P0620 U0142 U0150 U0153 C0052 C0053 B2103 B2431".split()
                if [row.get("code") for row in held_data.get("items", [])] == historical_codes:
                    try:
                        existing = [fetch_published_code(code) for code in historical_codes]
                    except TransientReadError as exc:
                        print_state("PREFLIGHT_DEFERRED_NO_WRITES", str(exc))
                        return
                    complete = all(row is not None
                        and row.get("status") == "publish"
                        and row.get("featured_media")
                        and (row.get("yoast_head_json") or {}).get("og_image")
                        for row in existing)
                    if complete:
                        print_state("ALREADY_PUBLISHED_WITH_COVERS",number,
                            "Historical release verified; held flag preserved, no writes")
                        continue
            print_state("WAITING",number,reason,"No WordPress writes.")
            return
        items,files=ready
        try:
            existing=[fetch_published_code(i["code"]) for i in items]
        except TransientReadError as exc:
            # No writes have occurred in this scheduled run. Defer without
            # incorrectly classifying a Cloudflare 522 as a content failure.
            print_state("PREFLIGHT_DEFERRED_NO_WRITES",str(exc))
            return
        if all(p is not None and p.get("featured_media") and p.get("yoast_head_json",{}).get("og_image") for p in existing):
            print_state("ALREADY_PUBLISHED_WITH_COVERS",number)
            continue
        process_one(number,items,files,args.check_only)
        return
    print_state("ALL_REVIEWED_BATCHES_COMPLETE","Waiting for a new approved 10-code batch.")


if __name__=="__main__":
    main()
