#!/usr/bin/env python3
"""Batch34 exact-slug publication preflight; read only."""
import json,urllib.parse,urllib.request
CODES=["P0355","P0482","P0744","U0201","U0213","U0429","C0034","C0047","B1448","B1449"]
for code in CODES:
 q=urllib.parse.urlencode({"slug":code.lower(),"per_page":3,"_fields":"id,slug,status,link"})
 u="https://a3tal.com/wp-json/wp/v2/a3tal-dtc?"+q
 with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"A3tal-DTC34-Preflight/20261026","Accept":"application/json"}),timeout=50) as f: rows=json.load(f)
 items=[x for x in rows if x.get("slug")==code.lower()]
 print("DTC34_PREFLIGHT",json.dumps({"code":code,"count":len(items),"rows":items}),flush=True)
 if len(items):raise RuntimeError("Existing live or draft record for "+code+"; choose new code")
print("DTC34_ALL_TEN_MISSING_SAFE_FOR_NEW_RELEASE")
