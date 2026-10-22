#!/usr/bin/env python3
"""Safely enrich the remaining seven already-published batch31 DTC pages (never create posts).

Read-before-write + revision-guarded Bridge update-post + readback.
No title/slug/status/image modification; never retry an ambiguous write.
"""
import html,json,os,re,time,urllib.parse,urllib.request,urllib.error
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE="https://a3tal.com"
BRIDGE=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
CODE_ID={"U0183":84093,"U0185":84094,"U0190":84095,"C006A":84096,"C0069":84097,"B1441":84098,"B1442":84099}
HEADERS={"User-Agent":"A3tal-DTC31-Editorial-20261022","Accept":"application/json","Cache-Control":"no-cache"}

class HTMLText(HTMLParser):
    def __init__(self):super().__init__();self.buff=[];self.depth=0
    def handle_starttag(self,tag,attrs):
        if tag in ("script","style"):self.depth+=1
    def handle_endtag(self,tag):
        if tag in ("script","style"):self.depth=max(0,self.depth-1)
    def handle_data(self,s):
        if not self.depth:self.buff.append(s)

def words(body):
    p=HTMLText();p.feed(body)
    return len(re.findall(r"\S+",html.unescape(" ".join(p.buff))))

def api(method,url,payload=None,private=False):
    headers=dict(HEADERS)
    if private:
        if not KEY:raise RuntimeError("A3TAL_API_KEY missing")
        headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,headers=headers,method=method,data=raw)
    with urllib.request.urlopen(req,timeout=90) as resp:return json.load(resp)

def private_post(pid):
    return api("GET",BRIDGE+"/post/"+str(pid)+"?nonce="+str(time.time_ns()),private=True)

def public_post(code):
    params=urllib.parse.urlencode({"slug":code.lower(),"per_page":2,
        "_fields":"id,slug,status,featured_media,yoast_head_json"})
    records=api("GET",BASE+"/wp-json/wp/v2/a3tal-dtc?"+params+"&nonce="+str(time.time_ns()))
    if not isinstance(records,list) or len(records)!=1:raise RuntimeError(code+" missing or duplicate public post")
    return records[0]

def main():
    if not KEY:raise RuntimeError("No Bridge key")
    additions={}
    for code in CODE_ID:
        f=ROOT/"data"/("dtc-batch31-enrichment-"+code.lower()+"-20261022.json")
        d=json.loads(f.read_text(encoding="utf8"))
        if d.get("batch")!=31 or d.get("code")!=code:raise RuntimeError("Invalid manuscript "+code)
        extra=d["html"]
        if f'data-a3tal-batch31="{code}"' not in extra or words(extra)<800:
            raise RuntimeError("Thin or invalid addendum "+code)
        additions[code]=extra
    # All identities, present images and revisions validated before any write.
    pre={}
    for code,pid in CODE_ID.items():
        pub=public_post(code)
        row=private_post(pid)
        if pub.get("id")!=pid or pub.get("status")!="publish" or int(pub.get("featured_media") or 0)<1:
            raise RuntimeError("Public post/image mismatch "+code)
        if row.get("id")!=pid or row.get("slug")!=code.lower() or row.get("type")!="a3_dtc" or row.get("status")!="publish":
            raise RuntimeError("Private post identity mismatch "+code)
        before=row.get("content","")
        if len(before)<2500:raise RuntimeError("Existing article unexpectedly short "+code)
        marker=f'data-a3tal-batch31="{code}"'
        if marker in before:
            print("ALREADY_ENRICHED",code,"words",words(before),flush=True)
            if words(before)<1500:raise RuntimeError("Enriched article still below target "+code)
            pre[code]=None
            continue
        candidate=before+"\n"+additions[code]
        count=words(candidate)
        if count<1500:raise RuntimeError(f"{code}: would be only {count} words; no mutation")
        pre[code]=(row,candidate)
        print("READY_EXISTING_POST",code,pid,"before",words(before),"after",count,"image",pub["featured_media"],flush=True)
    for code,payload in pre.items():
        if payload is None:continue
        row,new_body=payload
        print("GUARDED_CONTENT_UPDATE_STARTED",code,flush=True)
        try:
            result=api("POST",BRIDGE+"/update-post",{
                "id":row["id"],
                "expected_modified_gmt":row["modified_gmt"],
                "content":new_body},private=True)
        except Exception as exc:
            latest=private_post(row["id"])
            if latest.get("content")==new_body:
                print("RECOVERED_AFTER_AMBIGUOUS_UPDATE",code,flush=True)
                continue
            raise RuntimeError("Stopped after uncertain write to "+code) from exc
        if int(result.get("id") or 0)!=row["id"]:
            raise RuntimeError("Bridge updated unexpected record for "+code)
        confirmed=private_post(row["id"])
        actual=confirmed.get("content","")
        marker=f'data-a3tal-batch31="{code}"'
        if confirmed.get("status")!="publish" or confirmed.get("slug")!=code.lower() or marker not in actual:
            raise RuntimeError("WordPress readback lost status, identity, or diagnostic addendum for "+code)
        if words(actual)<1500:
            raise RuntimeError("Post under 1500 words after write "+code)
        if actual!=new_body:
            print("WORDPRESS_NORMALIZED_EDITORIAL_HTML",code,"verified_words",words(actual),flush=True)
        pub=public_post(code)
        if pub.get("id")!=row["id"] or pub.get("status")!="publish" or int(pub.get("featured_media") or 0)<1:
            raise RuntimeError("Published slug/status/cover changed "+code)
        print("UPDATED_AND_VERIFIED",code,BASE+"/dtc/"+code.lower()+"/","words",words(confirmed["content"]),flush=True)
        time.sleep(3)
    print("DTC31_FINAL7_EDITORIAL_VERIFIED_1500_PLUS_EXISTING_URLS_UNCHANGED",flush=True)

if __name__=="__main__":main()
