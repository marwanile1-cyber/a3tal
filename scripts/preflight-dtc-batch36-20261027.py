#!/usr/bin/env python3
"""Never publish batch36 if any public slug is already present."""
import json,urllib.parse,urllib.request
CODES=["P0357","P0358","P0484","P0758","P0759","P0761","P0873","U0204","U0205","U0212"]
for code in CODES:
 q=urllib.parse.urlencode({"slug":code.lower(),"per_page":4,"_fields":"id,slug,status,link"})
 req=urllib.request.Request("https://a3tal.com/wp-json/wp/v2/a3tal-dtc?"+q,headers={"User-Agent":"A3tal-DTC36-Preflight/20261027","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=45) as f: rows=json.load(f)
 found=[x for x in rows if x.get("slug")==code.lower()]
 print("DTC36_PREFLIGHT",code,json.dumps(found),flush=True)
 if found:raise RuntimeError("Refuse duplicate: "+code)
print("DTC36_ALL_TEN_UNPUBLISHED")
