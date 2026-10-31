#!/usr/bin/env python3
"""Safely deploy a DTC related-code relevance improvement on existing live theme.
Bridge hash-matches the reviewed backup, PHP is linted and public P0420/P0171
recommendations are verified. No WordPress post, permalink or redirect is modified.
"""
import os, json, hashlib, re, subprocess, time, urllib.parse, urllib.request
from pathlib import Path
BASE="https://a3tal.com"
API=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
TARGET="themes/a3tal-global/dtc-library-single.php"
ORIGINAL=Path("theme-patches/backup-dtc-library-single-before-related-code-relevance-20261031.php")
SOURCE=Path("theme-source/a3tal-global/dtc-library-single.php")
MARKER="Relevance fix 2026-10-31"
def request(url,payload=None,auth=True):
    headers={"Accept":"application/json","User-Agent":"A3tal-Dtc-Related-Code-Guard/20261031",
             "Cache-Control":"no-cache,no-store"}
    if auth: headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,headers=headers,data=raw,method="POST" if raw is not None else "GET")
    with urllib.request.urlopen(req,timeout=100) as resp:return json.load(resp) if auth else resp.read().decode("utf8",errors="replace")
def live_read():
    url=API+"/admin?"+urllib.parse.urlencode({"op":"file_read","path":TARGET,"check":str(time.time_ns())})
    x=request(url)
    if x.get("ok") is not True or not isinstance(x.get("result"),dict):
        raise RuntimeError("Bridge rejected DTC template source read")
    return x["result"]
baseline=ORIGINAL.read_text("utf8")
modified=SOURCE.read_text("utf8")
assert baseline.count("$dtc_related_entries = array_slice($dtc_related_entries, 0, 3);")==1
assert MARKER not in baseline
assert modified.count(MARKER)==1 and "usort($dtc_related_candidates" in modified
assert "dtc_seen_related_urls" in modified and "P0420" in modified and "P0430" in modified
assert 2200<len(modified)-len(baseline)<4500
test=subprocess.run(["php","-l",str(SOURCE)],capture_output=True,text=True)
if test.returncode:raise RuntimeError("Invalid PHP: "+test.stderr[:450])
print("DTC_THEME_PHP_LINT_OK",flush=True)
before=live_read()
live_content=before.get("content","")
digest=hashlib.sha256(live_content.encode("utf8")).hexdigest()
if digest!=before.get("sha256"):raise RuntimeError("Bridge returned mismatched SHA")
if live_content==modified:
    print("DTC_RELATED_THEME_ALREADY_LIVE",flush=True)
else:
    if live_content!=baseline:raise RuntimeError("Live DTC template differs from reviewed baseline; no write")
    print("DTC_THEME_BACKUP_MATCHED_LIVE",digest[:15],flush=True)
    reply=request(API+"/admin",{"op":"file_write","path":TARGET,"content":modified,
                                  "expected_sha256":digest,"confirm":True,"dangerous":True})
    if not reply.get("ok"):raise RuntimeError("Bridge rejected guarded DTC theme write "+str(reply)[:180])
    after=live_read()
    if after.get("content")!=modified or after.get("sha256")!=hashlib.sha256(modified.encode("utf8")).hexdigest():
        raise RuntimeError("DTC live PHP content mismatch after guarded deployment")
    print("DTC_RELATED_THEME_HASH_VERIFIED",flush=True)
pages=[
  ("P0420",BASE+"/p0420-catalyst-efficiency-bank-1/",["P0430"]),
  ("P0171",BASE+"/p0171-system-too-lean-bank-1-diagnosis/",["P0172","P0174"]),
  ("P0300",BASE+"/p0300-random-misfire/",["P0301","P0302","P0303"]),
]
for code,url,expected in pages:
    matched=False
    results=[]
    for attempt in range(5):
        u=url+("?a3tal_related_qa=20261031-"+str(attempt))
        html=request(u,auth=False)
        match=re.search(r'aria-labelledby="dtc-related-title"[^>]*>(.*?)</section>',html,re.S)
        if not match:
            time.sleep(2);continue
        block=match.group(1)
        results=re.findall(r'<b class="d-code"[^>]*>\s*([PBCU][0-9A-F]{4})\s*</b>',block,re.I)
        if not results:results=re.findall(r'<b[^>]+class="d-code"[^>]*>\s*([PBCU][0-9A-F]{4})\s*</b>',block,re.I)
        if results and len(results)==len(set(results)) and "P0000" not in results and any(x in results for x in expected):
            matched=True;break
        time.sleep(2)
    if not matched:
        raise RuntimeError(f"DTC public related list not verified for {code}: {results}")
    print("DTC_RELATED_PUBLIC_VERIFIED",code,",".join(results),url,flush=True)
print("A3TAL_DTC_LIBRARY_RELEVANCE_DEPLOY_COMPLETE",flush=True)
