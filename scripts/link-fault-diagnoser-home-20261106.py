#!/usr/bin/env python3
"""Expose an independently browser-tested diagnostic tool on the exact existing A3tal homepage.
Only replace an existing one-slot tool link and add a submenu entry; preserve layout.
"""
import hashlib,os,urllib.request,urllib.parse,json
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types
m=types.ModuleType("a3tal_nav_bridge")
SourceFileLoader(m.__name__,"scripts/deploy-dtc-library.py").exec_module(m)
Bridge=m.Bridge
BASE="https://a3tal.com"
ROOT=Path("theme-source/a3tal-global")
HOME="home-reference-20261104.php"
HEADER="header.php"
ORIG_HOME='<a href="https://a3tal.com/dtc/"><span>⚙</span>معرفة كود العطل</a>'
NEW_HOME='<a href="https://a3tal.com/fault-diagnosis/"><span>⚙</span>مشخّص الأعطال الذكي</a>'
ORIG_HEADER='<a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(8)); ?>">أعطال وحلول</a><a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link(\'a3_dtc\',\'/dtc/\')); ?>">أكواد DTC</a>'
NEW_HEADER='<a data-google-vignette="false" href="<?php echo esc_url(a3g_cat_link(8)); ?>">أعطال وحلول</a><a data-google-vignette="false" href="<?php echo esc_url(home_url(\'/fault-diagnosis/\')); ?>">مشخّص الأعطال الذكي</a><a data-google-vignette="false" href="<?php echo esc_url(a3g_platform_link(\'a3_dtc\',\'/dtc/\')); ?>">أكواد DTC</a>'
def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"A3tal-Fault-Nav-QA","Cache-Control":"no-cache,no-store"})
 with urllib.request.urlopen(req,timeout=85) as f:return f.read(2000000).decode("utf8","replace")
def verified():
 source=fetch(BASE+"/fault-diagnosis/?fault_nav_source_check=1")
 if "id=\"a3fd-app\"" not in source or "id=\"a3fd-inline-script\"" not in source:
  raise RuntimeError("Unverified fault tool; navigation will not be changed")
 if "fault-diagnoser-20261106.js" not in source and "root.dataset.ready" not in source:
  raise RuntimeError("No installed deterministic engine")
def one(api,path,before,after):
 local=(ROOT/path).read_text("utf8")
 if local.count(after)!=1:raise RuntimeError("Reviewed source missing exact new navigation label "+path)
 orig=api.read(path)
 current=orig["content"]
 if current.count(after)==1 and current.count(before)==0:
  print("FAULT_NAV_ALREADY_LIVE",path,flush=True);return
 if current.count(before)!=1 or current.count(after)!=0:
  raise RuntimeError("Unexpected live navigation source; refusing blanket overwrite: "+path)
 target=current.replace(before,after,1)
 api.write(path,target,orig["sha256"])
 print("FAULT_NAV_PATCH_VERIFIED",path,flush=True)
def main():
 if not os.getenv("A3TAL_API_KEY"):raise RuntimeError("No bridge access")
 verified()
 api=Bridge()
 one(api,HOME,ORIG_HOME,NEW_HOME)
 one(api,HEADER,ORIG_HEADER,NEW_HEADER)
 api.flush()
 html=fetch(BASE+"/?fault_nav_qa=20261106")
 if "fault-diagnosis/" not in html or "مشخّص الأعطال الذكي" not in html:
  raise RuntimeError("Live homepage not linked to verified fault triage")
 print("FAULT_DIAGNOSER_LINKED_FROM_LIVE_HOMEPAGE_AND_HEADER",flush=True)
if __name__=="__main__":main()
