#!/usr/bin/env python3
"""Gated 2027 G318 car indexing without changing global thin vehicle policy.
Checks source, safeguards live theme snapshot and restores on failed public QA.
"""
import os,json,hashlib,types,subprocess,tempfile,argparse,urllib.request
from pathlib import Path
from importlib.machinery import SourceFileLoader
mod=types.ModuleType("a3tal_reuse_reviewed_bridge")
SourceFileLoader(mod.__name__,"scripts/deploy-dtc-library.py").exec_module(mod)
Bridge=mod.Bridge
SRC=Path("theme-source/a3tal-global/functions.php")
START="/* A3TAL-DEEPAL-G318-VERIFIED-CAR-INDEX-20261027:START */"
END="/* A3TAL-DEEPAL-G318-VERIFIED-CAR-INDEX-20261027:END */"
def digest(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def approved():
    src=SRC.read_text("utf8")
    if src.count(START)!=1 or src.count(END)!=1:raise RuntimeError("Unreviewed or duplicate G318 SEO exception")
    part=src[src.index(START):src.index(END)+len(END)]
    for mark in ["84672","84660,84664,84668","deepal-g318-2027-egypt","8000","2026-10-27"]:
        if mark not in part:raise RuntimeError("Missing scoped G318 index guard "+mark)
    return part
def lint(s):
    with tempfile.TemporaryDirectory() as td:
        f=Path(td)/"functions.php";f.write_text(s,"utf8")
        subprocess.run(["php","-l",str(f)],check=True,timeout=30)
def statefile(root):return Path(root)/"g318-original-theme.json"
def prepare(root):
    Path(root).mkdir(parents=True,exist_ok=True)
    v=Bridge().read("functions.php")
    original=v["content"]
    if "a3g_structured_car_robots" not in original or "A3TAL-DEEPAL-S09-VERIFIED-CAR-INDEX-20261026:END" not in original:
        raise RuntimeError("Global car SEO or prior S09 source drift. Refuse to modify theme")
    if START in original and approved() not in original:raise RuntimeError("Unknown G318 patch already present")
    lint(original)
    statefile(root).write_text(json.dumps({"content":original,"sha":digest(original)},ensure_ascii=False),"utf8")
    print("EXACT_LIVE_THEME_BACKED_UP",len(original),digest(original),flush=True)
def deploy(root):
    data=json.loads(statefile(root).read_text("utf8"))
    live=Bridge().read("functions.php")
    source=live["content"]
    if START in source:
        if approved() in source:print("ALREADY_CORRECT_G318_INDEX_PATCH",flush=True);return
        raise RuntimeError("Conflicting index override found")
    if digest(source)!=data["sha"]:raise RuntimeError("Theme modified since backup, cannot overwrite")
    new=source.rstrip()+"\n\n"+approved()+"\n"
    lint(new)
    Bridge().write("functions.php",new,expected=data["sha"])
    (Path(root)/"g318-new-theme-sha").write_text(digest(new),"utf8")
    print("SCOPED_G318_ONLY_INDEX_PATCH_DEPLOYED",digest(new),flush=True)
def verify(root):
    url="https://a3tal.com/cars/deepal-g318-2027-egypt/?g318_public_qa=20261027"
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (A3tal-G318-Live-QA)","Cache-Control":"no-cache"}),timeout=85) as r:
        html=r.read(1700000).decode("utf8","replace")
    low=html.lower()
    if "noindex, follow" in low or 'name="robots" content="noindex' in low:
        raise RuntimeError("Public G318 model still noindex")
    for marker in ["index, follow","deepal-g318-2027-egypt/","deepal-g318-vs-s09-egypt-2027-comparison",
                   "deepal-g318-2027-egypt-full-review-prices-ownership","deepal-egypt-official-service-centers",
                   "a3tal-g318-review-exterior","2,135,000","2,285,000"]:
        if marker not in html:raise RuntimeError("Public G318 page missing "+marker)
    print("G318_INDEX_FOLLOW_SOURCE_CAR_AND_THREE_JOURNEYS_PUBLIC_VERIFIED",url,flush=True)
def rollback(root):
    data=json.loads(statefile(root).read_text("utf8"))
    marker=Path(root)/"g318-new-theme-sha"
    if not marker.exists():
        print("NO_LIVE_THEME_CHANGE_TO_ROLLBACK",flush=True);return
    b=Bridge()
    live=b.read("functions.php")
    if digest(live["content"])==data["sha"]:print("THEME_ALREADY_SNAPSHOT",flush=True);return
    if digest(live["content"])!=marker.read_text("utf8"):
        raise RuntimeError("External theme edit since G318 deployment, refuse unsafe rollback")
    b.write("functions.php",data["content"],expected=digest(live["content"]))
    print("G318_THEME_RESTORED_VERIFIED",flush=True)
if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("op",choices=["prepare","deploy","verify","rollback"])
    a.add_argument("--state-dir",default=os.environ.get("RUNNER_TEMP","/tmp"))
    x=a.parse_args()
    globals()[x.op](x.state_dir)
