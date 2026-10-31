#!/usr/bin/env python3
"""Guarded production fix: DTC batch39 featured illustrations must appear in article body.
Full unchanged backup, PHP lint, atomic SHA-enforced A3tal Direct Bridge deployment.
"""
from pathlib import Path
import os,hashlib,json,subprocess,urllib.request,urllib.parse,time
ROOT=Path(__file__).resolve().parents[1]
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
TARGET="themes/a3tal-global/dtc-library-single.php"
SRC=ROOT/"theme-source/a3tal-global/dtc-library-single.php"
BAK=ROOT/"theme-patches/backup-dtc-library-single-before-filename-cover-guard-20261031.php"
MARK="A3TAL-DTC39-FEATURED-VISIBLE-20261031"
def call(url,payload=None,auth=True):
  headers={"User-Agent":"A3tal-DTC-39-Feature-Visibility-20261031","Accept":"application/json","Cache-Control":"no-cache,no-store"}
  if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
  raw=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
  if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
  with urllib.request.urlopen(urllib.request.Request(url,headers=headers,data=raw,method="POST" if raw is not None else "GET"),timeout=110) as r:
    b=r.read()
  return json.loads(b.decode("utf8")) if auth else b.decode("utf8",errors="replace")
def read_live():
  q=urllib.parse.urlencode({"op":"file_read","path":TARGET,"qa":str(time.time_ns())})
  r=call(API+"/admin?"+q)
  if not r.get("ok") or not isinstance(r.get("result"),dict):raise RuntimeError("Cannot audit current live theme file")
  return r["result"]
old=BAK.read_text("utf8");new=SRC.read_text("utf8")
if old.count(MARK)!=1 or new.count(MARK)!=1:raise RuntimeError("Unexpected original/new image patch marker")
if old.count("(?:5|10|39)")!=1 or new.count("$dtc_is_code_specific_art")<2:raise RuntimeError("Filename based cover guard missing")
if "get_the_post_thumbnail($dtc_id, 'full'" not in new:raise RuntimeError("Full-resolution featured art missing")
if not (100<len(new)-len(old)<800):raise RuntimeError("Unreviewed template changes")
subprocess.run(["php","-l",str(SRC)],check=True)
print("BATCH39_FEATURED_PHP_LINT_OK",flush=True)
before=read_live()
pre=before["content"]
if hashlib.sha256(pre.encode("utf8")).hexdigest()!=before["sha256"]:raise RuntimeError("Bridge live file digest invalid")
if pre==new:print("BATCH39_FEATURED_TEMPLATE_ALREADY_DEPLOYED",flush=True)
else:
  if pre!=old:raise RuntimeError("Live theme differs from preserved exact backup; no write")
  print("BATCH39_FEATURED_LIVE_MATCHES_REVIEWED_BACKUP",before["sha256"][:15],flush=True)
  result=call(API+"/admin",{"op":"file_write","path":TARGET,"content":new,
          "expected_sha256":before["sha256"],"confirm":True,"dangerous":True})
  if not result.get("ok"):raise RuntimeError("Bridge denied guarded theme write "+str(result)[:260])
after=read_live()
if after.get("content")!=new or after.get("sha256")!=hashlib.sha256(new.encode("utf8")).hexdigest():
  raise RuntimeError("Live theme file differs from reviewed update")
print("BATCH39_FEATURED_THEME_HASH_VERIFIED",flush=True)
for code in ["p0136","p0400","p0455","p0101","p0016"]:
  good=False
  for attempt in range(6):
    url=SITE+"/dtc/"+code+"/?a3tal_featured_qa="+str(time.time_ns())
    html=call(url,auth=False)
    # Presence of original visual inside figure, not only Yoast head or site logo.
    figure=html.find('class="d-dtc-featured"')
    if figure>=0:
      snippet=html[figure:figure+2200]
      if "wp-post-image" in snippet and "a3tal-dtc-"+code+"-exclusive-ar" in snippet and "<figcaption" in snippet:
        good=True;break
    time.sleep(3)
  if not good:raise RuntimeError("Live inline featured art not seen for "+code)
  print("BATCH39_ART_VISIBLE_IN_ARTICLE",code,url.split("?")[0],flush=True)
print("BATCH39_ORIGINAL_COVERS_NOW_VISIBLE_AND_RESPONSIVE",flush=True)
