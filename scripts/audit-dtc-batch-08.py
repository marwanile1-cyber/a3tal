#!/usr/bin/env python3
"""Read-only check of published DTC canonicals after ambiguous Cloudflare write responses."""
import json,time,urllib.request,urllib.error,urllib.parse
BASE="https://a3tal.com"
CODES=["P0105","P0140","P0190","P0205","P0481"]
def check(code):
  uri=BASE+"/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,status,link"
  heads={"User-Agent":"Mozilla/5.0 (compatible; A3talIntegrityAudit/1.0)","Accept":"application/json","Cache-Control":"no-cache"}
  for attempt in range(3):
    try:
      req=urllib.request.Request(uri,headers=heads)
      with urllib.request.urlopen(req,timeout=35) as result:
        obj=json.load(result)
        if not isinstance(obj,list):raise RuntimeError("Unexpected REST shape")
        matches=[x for x in obj if x.get("slug")==code.lower() and x.get("status")=="publish"]
        if len(matches)>1:raise RuntimeError("Duplicate canonical slug: "+code)
        return {"code":code,"state":"PUBLISHED" if matches else "NOT_IN_PUBLIC_REST","id":matches[0]["id"] if matches else None,"url":matches[0]["link"] if matches else None}
    except urllib.error.HTTPError as err:
      if err.code not in (429,502,503,504,520,522,524):
        return {"code":code,"state":"UNCONFIRMED_HTTP_"+str(err.code)}
      print("TRANSIENT",code,err.code,"safe retry",attempt+1,flush=True)
    except (TimeoutError,urllib.error.URLError,json.JSONDecodeError):
      print("TRANSIENT",code,"read timeout/transport",attempt+1,flush=True)
    time.sleep(25*(attempt+1))
  return {"code":code,"state":"UNCONFIRMED_HOST_UNREACHABLE"}
def main():
  for code in CODES:
    item=check(code)
    print("DTC_AUDIT",json.dumps(item,ensure_ascii=False),flush=True)
    # Do not change live content. No false no-availability conclusion after outage.
    time.sleep(3)
if __name__=="__main__":main()
