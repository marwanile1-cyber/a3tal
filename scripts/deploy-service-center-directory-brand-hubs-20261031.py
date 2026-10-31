#!/usr/bin/env python3
"""Guarded deployment for service-center brand hubs, exact live backup and PHP lint."""
from pathlib import Path
import os, json, hashlib, tempfile, subprocess, time, urllib.request, urllib.parse
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
TARGET="themes/a3tal-global/platform-archive-directory.php"
SOURCE=Path("theme-source/a3tal-global/platform-archive-directory.php")
BACKUP=Path("theme-patches/backup-platform-archive-directory-before-brand-hubs-20261031.php")
MARKER="g-service-brand-hubs"
def request(url,payload=None):
    headers={
      "X-A3tal-Key":KEY,
      "Authorization":"Bearer "+KEY,
      "Accept":"application/json",
      "Cache-Control":"no-cache,no-store",
      "User-Agent":"A3tal-Guarded-Service-Directory-Hubs/20261031"
    }
    raw=json.dumps(payload,ensure_ascii=False).encode("utf-8") if payload is not None else None
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,headers=headers,data=raw,method="POST" if raw is not None else "GET")
    with urllib.request.urlopen(req,timeout=110) as response:return json.load(response)
def read_live():
    qs=urllib.parse.urlencode({"op":"file_read","path":TARGET,"nonce":str(time.time_ns())})
    response=request(API+"/admin?"+qs)
    if not response.get("ok") or not isinstance(response.get("result"),dict):
        raise RuntimeError("Authenticated live file read failed")
    return response["result"]
source=SOURCE.read_text("utf8")
backup=BACKUP.read_text("utf8")
if MARKER not in source or MARKER in backup:
    raise RuntimeError("Source/backup markers incorrect")
if source.count("$quick_hubs=")!=1 or source.count("<?php if(!$is_showroom): ?>")!=1:
    raise RuntimeError("Unreviewed repeated brand shortcuts")
if len(source)-len(backup)<1000:
    raise RuntimeError("Unexpected source diff extent")
with tempfile.NamedTemporaryFile("w",suffix=".php",encoding="utf8",delete=False) as temp:
    temp.write(source)
    temp_name=temp.name
try:
    subprocess.run(["php","-l",temp_name],check=True,capture_output=True,text=True)
finally:
    os.unlink(temp_name)
print("SERVICE_DIRECTORY_PHP_LINT_OK",flush=True)
before=read_live()
livecode=before.get("content","")
oldhash=hashlib.sha256(livecode.encode("utf8")).hexdigest()
if oldhash!=before.get("sha256"):
    raise RuntimeError("Bridge returned inconsistent current live SHA")
if source==livecode:
    print("SERVICE_DIRECTORY_HUBS_ALREADY_LIVE",flush=True)
    raise SystemExit(0)
if livecode!=backup:
    raise RuntimeError("Actual live directory PHP diverged from reviewed repository backup; no write allowed")
print("SERVICE_DIRECTORY_LIVE_SOURCE_MATCHES_BACKUP",oldhash[:15],flush=True)
r=request(API+"/admin",{
    "op":"file_write",
    "path":TARGET,
    "content":source,
    "expected_sha256":before["sha256"],
    "confirm":True,
    "dangerous":True
})
if not r.get("ok"):
    raise RuntimeError("Bridge did not confirm guarded template write")
after=read_live()
if after.get("content")!=source:
    raise RuntimeError("Live directory PHP content mismatch after deployment")
if after.get("sha256")!=hashlib.sha256(source.encode("utf8")).hexdigest():
    raise RuntimeError("Live directory PHP hash differs from reviewed source")
# Check public HTML without requiring a WordPress login. Cache may need refreshing,
# but the direct PHP file proof above is authoritative for the template deployment.
pageurl=SITE+"/service-centers/?a3tal_hubs_qa=20261031"
verified=False
for i in range(4):
    public=urllib.request.Request(pageurl,headers={"User-Agent":"A3tal-Service-Directory-QA/20261031","Cache-Control":"no-cache"})
    with urllib.request.urlopen(public,timeout=100) as response:
        html=response.read().decode("utf8",errors="replace")
    if MARKER in html and "جيتور: المراكز المعتمدة" in html:
        verified=True
        break
    time.sleep(3)
if not verified:
    # A source-hash-confirmed deployment is still true even if the HTML has a stale
    # page cache. Do not return false success for cache-invisible UX.
    raise RuntimeError("Source deployed and verified, but public archive HTML lacks new links; inspect cache")
print("SERVICE_DIRECTORY_LIVE_VERIFIED",SITE+"/service-centers/","hub_links",html.count('class="g-service-brand-hubs"'),flush=True)
