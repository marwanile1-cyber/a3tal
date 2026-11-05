#!/usr/bin/env python3
"""Scoped, guarded A3tal maintenance archive deployment (2026-11-06).

A3tal Direct Bridge only. Deploy CSS/JS before activating PHP. Back up existing
files, checksum every mutation, and roll back only our own exact deployed bytes.
No post, price, SEO, garage or content database mutations.
"""
import argparse,hashlib,json,subprocess,tempfile,urllib.request,re
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types

mod=types.ModuleType("a3tal_existing_guarded_maintenance_bridge")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge
ROOT=Path("theme-source/a3tal-global")
FILES=[
 "maintenance-calculator-20261106.css",
 "assets/js/maintenance-calculator-20261106.js",
 "archive-a3_maintenance_plan.php",
]
ACTIVATE=FILES[-1]
MARKER="a3ms-calculator"
def sha(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def files():
 out={}
 for name in FILES:
  p=ROOT/name
  if not p.exists():raise RuntimeError("Missing reviewed source file: "+name)
  out[name]=p.read_text(encoding="utf8")
 return out
def phpcheck(text):
 with tempfile.TemporaryDirectory(prefix="a3ms-") as d:
  path=Path(d)/"archive-a3_maintenance_plan.php"
  path.write_text(text,encoding="utf8")
  subprocess.run(["php","-l",str(path)],check=True,timeout=30)
def preflight(d):
 src=files()
 phpcheck(src[ACTIVATE])
 subprocess.run(["node","--check",str(ROOT/FILES[1])],check=True,timeout=30)
 if not all(s in src[ACTIVATE] for s in (
   "a3ms-available-count","a3ms-last-date","a3ms-usage","a3ms-last-km",
   "g-maintenance-timeline","a3g_legacy_section","a3ms-inline-style","a3ms-inline-script")):
  raise RuntimeError("Reviewed maintenance archive incomplete")
 api=Bridge()
 originals={}
 for name in FILES:
  current=api.read(name,missing=True)
  if current and sha(current["content"])!=current["sha256"]:
   raise RuntimeError("Live maintenance file checksum inconsistent: "+name)
  originals[name]=current
  if name==ACTIVATE:
   if not current:raise RuntimeError("Existing maintenance archive absent")
   live=current["content"]
   if MARKER in live:
    if live!=src[name]:raise RuntimeError("Unknown existing maintenance calculator patch; refusing overwrite")
   elif not all(s in live for s in (
        'g-maintenance-hero','g-maintenance-demo-ring','g-maintenance-timeline',
        'a3g_legacy_section','_a3_interval_km')):
    raise RuntimeError("Unexpected maintenance archive source; refusing overwrite")
  elif current and current["content"]!=src[name]:
   # The only approved asset migration is the original reviewed calculator JS
   # to its readiness-signalling revision. Match the exact prior Git blob.
   if name!="assets/js/maintenance-calculator-20261106.js":
    raise RuntimeError("Unexpected existing asset differs: "+name)
   previous=subprocess.check_output([
     "git","show","4b5cbf5b2bea34e04b723bd03f26ec4bce68e8d5:"+
     "theme-source/a3tal-global/assets/js/maintenance-calculator-20261106.js"
   ],timeout=25).decode("utf8")
   if current["content"]!=previous:
    raise RuntimeError("Existing calculator JavaScript is not the reviewed prior release")
   print("MAINTENANCE_APPROVED_JS_UPGRADE",flush=True)
 d.mkdir(parents=True,exist_ok=True)
 state={"files":FILES,"source":{k:sha(v) for k,v in src.items()},"originals":originals}
 (d/"snapshot.json").write_text(json.dumps(state,ensure_ascii=False),encoding="utf8")
 print("MAINTENANCE_PREPARE_BACKUP_VERIFIED",len(FILES),flush=True)
def load(d):
 path=d/"snapshot.json"
 if not path.exists():raise RuntimeError("Missing backup state")
 return json.loads(path.read_text(encoding="utf8"))
def deploy(d):
 state=load(d);src=files()
 api=Bridge()
 for name in FILES:
  desired=src[name]
  if sha(desired)!=state["source"][name]:raise RuntimeError("Source changed after snapshot: "+name)
  current=api.read(name,missing=True)
  original=state["originals"][name]
  if current and current["sha256"]==sha(desired):
   print("MAINTENANCE_ALREADY_MATCHES",name,flush=True);continue
  if original and (not current or current["sha256"]!=original["sha256"]):
   raise RuntimeError("Live file changed independently after backup: "+name)
  if not original and current:raise RuntimeError("Expected absent asset now exists: "+name)
  api.write(name,desired,expected=current["sha256"] if current else None)
  if not original:
   # readback validates newly created files (existing Bridge.write does likewise).
   print("MAINTENANCE_NEW_ASSET_VERIFIED",name,flush=True)
  else:print("MAINTENANCE_PATCH_VERIFIED",name,flush=True)
 api.flush()
 print("MAINTENANCE_DEPLOY_FILES_VERIFIED",flush=True)
def verify():
 base="https://a3tal.com"
 def fetch(url):
  req=urllib.request.Request(url,headers={"User-Agent":"A3tal-Maintenance-20261106-QA","Cache-Control":"no-cache,no-store"})
  with urllib.request.urlopen(req,timeout=70) as f:
   if f.status!=200:raise RuntimeError("HTTP not 200 "+url)
   return f.read(1700000).decode("utf8","replace")
 import time
 # WordPress can cache CPT archives independently of query-driven model views.
 # Check the actual model first, then report the default archive cache state.
 rows=json.loads(fetch(base+"/wp-json/wp/v2/a3tal-motorcycles?slug=bajaj-pulsar-180-egypt&_fields=id,slug,status"))
 if len(rows)!=1 or rows[0].get("status")!="publish":raise RuntimeError("Published original source-backed Pulsar 180 record missing")
 modelid=rows[0]["id"]
 itemPage=fetch(base+"/maintenance-schedules/?vehicle_entity="+str(modelid)+"&a3ms_release="+str(time.time_ns()))
 required=('id="a3ms-calculator"','id="a3ms-current-km"','id="a3ms-usage"',
           'class="g-maintenance-node a3ms-item"','a3ms-last-km-','a3ms-last-date-',
           "a3ms-result","Pulsar 180")
 misses=[x for x in required if x not in itemPage]
 if misses:raise RuntimeError("Live source-backed maintenance calculator missing: "+",".join(misses))
 if "https://www.bajajauto.com/" not in itemPage:raise RuntimeError("Original official source link not preserved")
 print("MAINTENANCE_LIVE_SOURCE_AND_CALCULATOR_VERIFIED",modelid,flush=True)
 page=fetch(base+"/maintenance-schedules/?a3ms_release="+str(time.time_ns()))
 checks=["g-maintenance-hero","a3ms-available-count","أدلة وجداول الصيانة المتاحة"]
 misses=[x for x in checks if x not in page]
 if misses:
  # Cache is outside the modified theme file. Keep the verifiable model view
  # and report the stale archive rather than rolling back correct source code.
  print("MAINTENANCE_ARCHIVE_CACHE_STALE",",".join(misses),flush=True)
 else:
  if 'g-maintenance-demo-ring' in page:raise RuntimeError("Default archive still has hard-coded 90K demo after asset refresh")
  print("MAINTENANCE_DEFAULT_ARCHIVE_LIVE_VERIFIED",flush=True)

def rollback(d):
 state=load(d);api=Bridge()
 # Roll back active PHP first, followed by harmless assets. No blind overwrites.
 for name in reversed(FILES):
  current=api.read(name,missing=True)
  orig=state["originals"][name]
  if orig and current and current["sha256"]==orig["sha256"]:
   print("MAINTENANCE_ROLLBACK_ALREADY_ORIGINAL",name,flush=True);continue
  if current and current["sha256"]!=state["source"][name]:
   raise RuntimeError("External edit since deploy; refusing rollback: "+name)
  if orig:
   if not current:raise RuntimeError("Expected deployed file missing: "+name)
   api.write(name,orig["content"],expected=current["sha256"])
   print("MAINTENANCE_RESTORED",name,flush=True)
  else:
   # New assets do not affect the original archive and can remain as unreferenced files.
   print("MAINTENANCE_ORPHANED_UNREFERENCED_ASSET",name,flush=True)
 api.flush()
 print("MAINTENANCE_ROLLBACK_DONE",flush=True)
if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("operation",choices=["prepare","deploy","verify","rollback"])
 parser.add_argument("--state-dir",type=Path,required=True)
 args=parser.parse_args()
 {"prepare":preflight,"deploy":deploy,"verify":lambda d:verify(),"rollback":rollback}[args.operation](args.state_dir)
