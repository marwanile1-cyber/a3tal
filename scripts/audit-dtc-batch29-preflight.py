#!/usr/bin/env python3
"""Read-only availability and featured-asset audit for the next DTC batch.
No WordPress writes, no secrets, no guessing that an HTTP error means unpublished.
"""
import json,urllib.request,urllib.parse
CODES="P0316 P0496 P0733 U0154 U0163 U0170 C0061 C0062 B1411 B1412".split()
BASE="https://a3tal.com"
def get(url):
    req=urllib.request.Request(url,headers={"Accept":"application/json","Cache-Control":"no-cache","User-Agent":"A3tal-Batch29-Preflight/1.0"})
    with urllib.request.urlopen(req,timeout=50) as resp:return json.load(resp)
def main():
    report=[]
    for code in CODES:
        query=urllib.parse.urlencode({"slug":code.lower(),"_fields":"id,slug,status,link,featured_media,yoast_head_json,title"})
        try:
            found=get(BASE+"/wp-json/wp/v2/a3tal-dtc?"+query)
            exact=[x for x in found if x.get("slug")==code.lower()]
            if len(exact)>1:raise RuntimeError("DUPLICATE WordPress DTC slug")
            if not exact:
                result={"code":code,"state":"missing"}
            else:
                p=exact[0];result={"code":code,"state":p.get("status","unknown"),"id":p.get("id"),"url":p.get("link"),"featured":p.get("featured_media"),"og_image":bool(p.get("yoast_head_json",{}).get("og_image"))}
        except Exception as e:result={"code":code,"state":"unknown_ERROR","error":str(e)}
        report.append(result)
        print("BATCH29_PREFLIGHT",json.dumps(result,ensure_ascii=False),flush=True)
    if any(row["state"]=="unknown_ERROR" for row in report):
        raise RuntimeError("Cannot safely infer missing posts with WordPress response errors")
    if any(row["state"] not in ("missing","publish") for row in report):
        raise RuntimeError("A non-public DTC already owns a planned slug; stop to protect drafts")
    print("BATCH29_READ_ONLY_DONE",json.dumps({"existing":sum(x["state"]=="publish" for x in report),"missing":sum(x["state"]=="missing" for x in report)},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
