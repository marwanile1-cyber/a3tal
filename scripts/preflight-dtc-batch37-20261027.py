#!/usr/bin/env python3
"""Stop production before duplicate slugs are created in batch37."""
import json,urllib.parse,urllib.request
CODES=["P0359","P0360","P0485","P0762","P0763","P0874","U0206","U0207","U0215","U0216"]
for code in CODES:
    q=urllib.parse.urlencode({"slug":code.lower(),"per_page":4,"_fields":"id,slug,status,link"})
    req=urllib.request.Request("https://a3tal.com/wp-json/wp/v2/a3tal-dtc?"+q,headers={"User-Agent":"A3tal-Preflight-37/20261027","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=40) as f:rows=json.load(f)
    found=[r for r in rows if r.get("slug")==code.lower()]
    print("BATCH37_CHECK",code,json.dumps(found),flush=True)
    if found:raise RuntimeError("Previously published code "+code)
print("BATCH37_NO_DUPLICATES")
