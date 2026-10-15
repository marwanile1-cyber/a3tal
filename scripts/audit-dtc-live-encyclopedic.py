#!/usr/bin/env python3
"""Read-only live QA: article, OpenGraph, actual iframe embed, and image origin.
Fail closed: a workflow exit=0 is not approval of photographic realism.
"""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parent.parent
BASE="https://a3tal.com"

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta={}
        self.images=[]
        self.iframes=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="meta":
            self.meta.setdefault(a.get("property") or a.get("name"),[]).append(a.get("content",""))
        if tag=="img": self.images.append(a.get("src",""))
        if tag=="iframe": self.iframes.append(a.get("src",""))

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"A3tal-ReadOnly-Live-Editorial-QA/1.0","Accept":"text/html","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=45) as r:
        if r.status!=200: raise RuntimeError("HTTP "+str(r.status))
        return r.read().decode("utf-8","replace")

def audit(batch):
    path=ROOT/"data"/f"dtc-original-batch-{batch:02d}.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    rows=[]
    for article in data["items"]:
        code=article["code"]
        url=f"{BASE}/dtc/{code.lower()}/"
        row={"code":code,"url":url,"pass":False,"errors":[]}
        try:
            html=fetch(url)
            tags=Tags();tags.feed(html)
            row["og_image"]=tags.meta.get("og:image",[])
            row["html_iframes"]=tags.iframes
            row["has_cover"]=any(f"a3tal-dtc-{code.lower()}-exclusive" in s for s in tags.images)
            row["has_matching_og"]=any(f"a3tal-dtc-{code.lower()}-exclusive" in s for s in row["og_image"])
            row["wordcount_rough"]=len(re.findall(r"\S+",re.sub(r"<[^>]+>"," ",re.sub(r"<(script|style)[^>]*>.*?</\\1>"," ",html,flags=re.I|re.S))))
            if not row["has_cover"]:row["errors"].append("Featured image not confirmed in rendered HTML")
            if not row["has_matching_og"]:row["errors"].append("OpenGraph image does not match DTC cover")
            if row["wordcount_rough"]<780:row["errors"].append("Rendered page text below minimum")
            video=article.get("video")
            if video:
                vid=video["id"]
                row["expected_video_id"]=vid
                row["has_actual_embed"]=any(vid in src and ("youtube.com/embed/" in src or "youtube-nocookie.com/embed/" in src) for src in tags.iframes)
                if not row["has_actual_embed"]:
                    row["errors"].append("Expected YouTube iframe not present in raw rendered HTML")
            else:
                row["video_status"]="no video selected: relevance & embeddability review needed"
            row["pass"]=not row["errors"]
        except (urllib.error.URLError,TimeoutError,OSError,ValueError) as exc:
            row["errors"].append("Live read unavailable: "+str(exc)[:160])
        print("QA",code,"PASS" if row["pass"] else "FAIL",", ".join(row["errors"]),flush=True)
        rows.append(row)
    renderer=ROOT/"scripts"/f"render-dtc-batch-{batch:02d}-art.py"
    illustration_generator=renderer.exists() and bool(re.search(r"\bImageDraw\b|drawn with Pillow|entirely drawn",renderer.read_text(encoding="utf-8"),re.I))
    report={"batch":batch,"pages_pass":sum(x["pass"] for x in rows),"pages_total":len(rows),"art_generator_draws_illustrations":illustration_generator,
      "photography_approval":"REJECT: known script-drawn imagery" if illustration_generator else "UNVERIFIED: requires visual review of actual cover assets",
      "results":rows}
    out=ROOT/"dtc-live-qa-result.json";out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("RESULT",json.dumps({k:v for k,v in report.items() if k!="results"},ensure_ascii=False),flush=True)
    return 1 if (report["pages_pass"]!=len(rows) or illustration_generator) else 0

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--batch",type=int,default=27);a=p.parse_args()
    sys.exit(audit(a.batch))
