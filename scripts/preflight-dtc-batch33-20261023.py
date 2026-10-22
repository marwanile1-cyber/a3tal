#!/usr/bin/env python3
"""DTC batch33 strictly read-only duplicate-preflight. Never mutate WordPress."""
import urllib.request, urllib.parse, json
CODES=["P0346","P0743","P0871","U0195","U0200","U0428","C0031","C003A","B1445","B1447"]
BASE="https://a3tal.com/wp-json/wp/v2/a3tal-dtc"
result=[]
for code in CODES:
    q=urllib.parse.urlencode({"slug":code.lower(),"per_page":3,"_fields":"id,slug,status,link,title,featured_media"})
    req=urllib.request.Request(BASE+"?"+q,headers={"Accept":"application/json","User-Agent":"A3tal-DTC33-DuplicatePreflight/20261023"})
    with urllib.request.urlopen(req,timeout=50) as response: rows=json.load(response)
    rows=[x for x in rows if x.get("slug")==code.lower()]
    result.append({"code":code,"count":len(rows),"posts":[{"id":v.get("id"),"status":v.get("status"),"link":v.get("link")} for v in rows]})
    print("DTC33_PREFLIGHT",json.dumps(result[-1]),flush=True)
print("DTC33_PREFLIGHT_SUMMARY",json.dumps({"found":sum(x["count"] for x in result),"missing":sum(x["count"]==0 for x in result),"all":result}),flush=True)
if any(x["count"]>1 for x in result):raise RuntimeError("Duplicate slugs already present; stop")
