#!/usr/bin/env python3
"""Hotfix only the A3tal Egypt published brand-directory partial (safe native WP search)."""
import hashlib, json, os, sys, time, requests, types
from importlib.machinery import SourceFileLoader
from pathlib import Path
if not os.environ.get("A3TAL_API_KEY"):raise SystemExit("A3TAL_API_KEY missing")
m=types.ModuleType("a3tal_hotfix_bridge")
SourceFileLoader(m.__name__,"scripts/deploy-dtc-library.py").exec_module(m)
api=m.Bridge()
p="brand-collection-20261108.php"
new=Path("theme-source/a3tal-global")/p
content=new.read_text("utf-8")
assert "a3tal_brand_title_filter" not in content and "search_columns" in content
old=api.read(p)
if not old:raise RuntimeError("Brand partial is not installed; do not create unreviewed file")
if old["content"]!=content:
    if "A3tal Egypt car-brand overview" not in old["content"] or "a3tal_brand_title_filter" not in old["content"]:
        raise RuntimeError("Live brand partial differs from the reviewed earlier version")
    api.write(p,content,old["sha256"])
    print("BRAND_QUERY_HOTFIX_READBACK_VERIFIED",flush=True)
else:print("SAFE_BRAND_QUERY_ALREADY_LIVE",flush=True)
api.flush()
s=requests.Session()
s.headers["User-Agent"]="Mozilla/5.0"
for attempt in range(4):
    try:
        r=s.get("https://a3tal.com/cars/?brand=geely&safe_brand_query="+str(time.time_ns()),timeout=50)
        if r.status_code==200 and "دليل جيلي في أعطال.كوم" in r.text and 'id="all-brand-content"' in r.text:
            print("GEELY_BRAND_PUBLIC_200_VERIFIED",len(r.text),flush=True)
            break
        print("GEELY_CHECK_RETRY",r.status_code,flush=True)
    except requests.RequestException as e:
        print("GEELY_TRANSIENT",type(e).__name__,flush=True)
    if attempt==3:raise RuntimeError("Geely brand public check is still failing")
    time.sleep(8)
