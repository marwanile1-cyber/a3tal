#!/usr/bin/env python3
"""Check the site's actual internal-link targets, including redirects and 404s."""
import json,collections,concurrent.futures,requests
from urllib.parse import urlsplit
report=json.load(open('old-audit/seo-audit-report.json'))
items=report.get('non_sitemap_link_destinations',[])[:80]
def check(p):
  u=p['url'];source_count=p['source_count']
  try:
    r=requests.get(u,headers={'User-Agent':'Mozilla/5.0 (compatible; A3talSEO/1.0)'},timeout=28,allow_redirects=True)
    hops=[{"status":x.status_code,"url":x.url,"location":x.headers.get('location','')} for x in r.history]
    return {"url":u,"sources":source_count,"status":r.status_code,"final":r.url,"redirect_count":len(hops),"hops":hops,"content_type":r.headers.get("content-type","")}
  except Exception as e:return {"url":u,"sources":source_count,"error":str(e)[:180]}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  res=list(pool.map(check,items))
bad=[p for p in res if p.get('status') not in (200,301,302) and not "/cdn-cgi/" in p['url']]
hops=[p for p in res if p.get('redirect_count',0)>0]
print('LINK_TARGET_AUDIT',json.dumps({'count':len(res),'broken_count':len(bad),'redirected_count':len(hops),'broken':bad,'redirected':hops[:40]},ensure_ascii=False),flush=True)
open('link-target-diagnostics.json','w').write(json.dumps(res,ensure_ascii=False,indent=2))
