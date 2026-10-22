#!/usr/bin/env python3
"""Read-only private WordPress state recovery check for batch 30."""
import os,json,html,re,urllib.request
from html.parser import HTMLParser
from pathlib import Path
BASE="https://a3tal.com/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
IDS={"U0180":84060,"U0181":84061,"U0182":84062,"C0063":84063,"C0064":84064,"B1413":84065,"B1423":84066}
class Txt(HTMLParser):
 def __init__(self):super().__init__();self.items=[]
 def handle_data(self,t):self.items.append(t)
def count(s):
 p=Txt();p.feed(s);return len(re.findall(r"\S+",html.unescape(" ".join(p.items))))
for code,id in IDS.items():
 url=BASE+"/post/"+str(id)
 with urllib.request.urlopen(urllib.request.Request(url,headers={"X-A3tal-Key":KEY,"User-Agent":"A3tal-Read-Only-Check"}),timeout=50) as r:
  x=json.load(r)
 content=x.get("content","")
 addition=json.load(open("data/dtc-batch30-enrichment-"+code.lower()+"-20261022.json",encoding="utf8"))["html"]
 print("CHECK",json.dumps({"code":code,"id":x.get("id"),"slug":x.get("slug"),
 "status":x.get("status"),"modified_gmt":x.get("modified_gmt"),"words":count(content),
 "marker":('data-a3tal-batch30="'+code+'"') in content,"exact_suffix":content.endswith(addition),
 "html_suffix_match":addition in content,"need_addendum":addition not in content},ensure_ascii=False),flush=True)
