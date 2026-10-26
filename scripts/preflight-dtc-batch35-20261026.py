#!/usr/bin/env python3
"""Read-only production slug preflight before DTC batch35 authoring."""
import json,urllib.parse,urllib.request
CODES=["P0356","P0483","P0750","P0751","P0872","U0202","U0214","U0430","C0037","C0039"]
for code in CODES:
 q=urllib.parse.urlencode({"slug":code.lower(),"per_page":3,"_fields":"id,slug,status,link"})
 req=urllib.request.Request("https://a3tal.com/wp-json/wp/v2/a3tal-dtc?"+q,headers={"User-Agent":"A3tal-DTC35-Preflight/20261026","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=45) as f: data=json.load(f)
 found=[x for x in data if x.get("slug")==code.lower()]
 print("DTC35_PREFLIGHT",code,json.dumps(found),flush=True)
 if found:raise RuntimeError("Code is already published or visible; refuse duplicate "+code)
print("DTC35_TEN_UNSEEN_CODES_CONFIRMED")
