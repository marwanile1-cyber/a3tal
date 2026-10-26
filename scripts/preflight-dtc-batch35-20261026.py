#!/usr/bin/env python3
"""Read-only production slug preflight before DTC batch35 authoring."""
import json,urllib.parse,urllib.request
CODES=["P0356","P0483","P0751","P0872","U0202","U0214","U0430","P0753","P0754","P0761","P0763","P0770","P0780","P0880","U0203","U0220","C0051","C0063","C0070"]
for code in CODES:
 q=urllib.parse.urlencode({"slug":code.lower(),"per_page":3,"_fields":"id,slug,status,link"})
 req=urllib.request.Request("https://a3tal.com/wp-json/wp/v2/a3tal-dtc?"+q,headers={"User-Agent":"A3tal-DTC35-Preflight/20261026","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=45) as f: data=json.load(f)
 found=[x for x in data if x.get("slug")==code.lower()]
 print("DTC35_PREFLIGHT",code,json.dumps(found),flush=True)
 if found:print("DTC35_DUPLICATE",code,flush=True)
print("DTC35_COMPLETE_CHECK_REVIEW_DUPLICATES_BEFORE_RELEASE")
