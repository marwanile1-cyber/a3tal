#!/usr/bin/env python3
"""Publish only unique Yoast meta descriptions for existing DTC batch34 posts.

Revision-guarded in-place update-post through A3tal Direct Bridge. Never
creates posts, changes media/content/slug, or retries an uncertain write.
"""
import json,os,time,urllib.parse,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SITE="https://a3tal.com"
BRIDGE=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
IDS={"P0355":None,"P0482":None,"P0744":None,"U0201":None,"U0213":None,"U0429":None,"C0034":None,"C0047":None,"B1448":None,"B1449":None}
H={"User-Agent":"A3tal-DTC34-SEO-20261026","Accept":"application/json","Cache-Control":"no-cache"}
def req(method,url,body=None,private=False):
    headers=dict(H)
    if private:
        if not KEY: raise RuntimeError("Missing dedicated GitHub bridge secret")
        headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=json.dumps(body,ensure_ascii=False).encode("utf8") if body is not None else None
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,method=method,data=raw,headers=headers),timeout=90) as response:
        return json.load(response)
def priv(id):
    return req("GET",BRIDGE+"/post/"+str(id)+"?nonce="+str(time.time_ns()),private=True)
def pub(code):
    q=urllib.parse.urlencode({"slug":code.lower(),"per_page":2,"_fields":"id,slug,status,featured_media,yoast_head_json,link","nonce":str(time.time_ns())})
    rows=req("GET",SITE+"/wp-json/wp/v2/a3tal-dtc?"+q)
    if not isinstance(rows,list) or len(rows)!=1:return None
    return rows[0]
def main():
    global IDS
    resolved={}
    for code in IDS:
        row=pub(code)
        if row is None or row.get("status")!="publish" or int(row.get("id") or 0)<=0:
            raise RuntimeError("Expected live batch34 post missing, stop all writes: "+code)
        resolved[code]=int(row["id"])
    if len(set(resolved.values()))!=10:raise RuntimeError("Duplicate ids detected")
    IDS=resolved
    data=json.loads((ROOT/"data/dtc-batch34-yoast-metadesc-20261026.json").read_text(encoding="utf8"))
    desc=data["descriptions"]
    if data.get("batch")!=34 or set(desc)!=set(IDS):raise RuntimeError("Mismatched roster or metadata")
    staged={}
    for code,id in IDS.items():
        description=desc[code]
        if not 105<=len(description)<=160 or code not in description:
            raise RuntimeError("Non-specific or invalid description "+code)
        a=pub(code);p=priv(id)
        if not a or a.get("id")!=id or a.get("status")!="publish" or int(a.get("featured_media") or 0)<1:
            raise RuntimeError("Published DTC record or original cover changed: "+code)
        if p.get("id")!=id or p.get("slug")!=code.lower() or p.get("type")!="a3_dtc" or p.get("status")!="publish":
            raise RuntimeError("Private identity mismatch "+code)
        if not (a.get("yoast_head_json") or {}).get("og_image"):
            raise RuntimeError("OpenGraph photo missing before meta patch "+code)
        existing=(p.get("meta") or {}).get("_yoast_wpseo_metadesc") or ""
        if existing and existing!=description:
            raise RuntimeError("Existing nonmatching hand-authored description; refuse overwriting "+code)
        staged[code]=(p,a,description,not existing)
        print("META_PREFLIGHT",code,"exists",bool(existing),"canonical",(a.get("yoast_head_json") or {}).get("canonical"),flush=True)
    for code,(p,a,description,write) in staged.items():
        id=IDS[code]
        if not write:
            print("META_ALREADY_SAVED",code,flush=True)
        else:
            latest=priv(id)
            if latest.get("modified_gmt")!=p.get("modified_gmt"):
                raise RuntimeError("Revision changed since preflight "+code)
            print("META_ONLY_WRITE_STARTED",code,flush=True)
            try:
                result=req("POST",BRIDGE+"/update-post",{
                  "id":id,"expected_modified_gmt":latest["modified_gmt"],
                  "meta":{"_yoast_wpseo_metadesc":description}
                },private=True)
            except Exception as exc:
                recovered=priv(id)
                if (recovered.get("meta") or {}).get("_yoast_wpseo_metadesc")==description:
                    print("META_WRITE_RECOVERED_BY_READBACK",code,flush=True)
                else:raise RuntimeError("Uncertain Yoast meta write; stop at "+code) from exc
            else:
                if int(result.get("id") or 0)!=id:raise RuntimeError("Unexpected post id after SEO edit "+code)
        latest=priv(id)
        if latest.get("slug")!=code.lower() or latest.get("status")!="publish" or (latest.get("meta") or {}).get("_yoast_wpseo_metadesc")!=description:
            raise RuntimeError("Saved Yoast description mismatch "+code)
        now=pub(code)
        if not now or now.get("id")!=id or now.get("status")!="publish" or now.get("featured_media")!=a.get("featured_media"):
            raise RuntimeError("Live status or cover changed for "+code)
        seo=now.get("yoast_head_json") or {}
        if (seo.get("canonical") or "").rstrip("/")!=SITE+"/dtc/"+code.lower():
            raise RuntimeError("Canonical unexpectedly changed "+code)
        if not (seo.get("og_image") or []):raise RuntimeError("OpenGraph media changed "+code)
        # No assertion that Yoast has rebuilt its REST indexable synchronously.
        reflected=(seo.get("description") or "").strip()
        print("SEO_META_SAVED",code,"WP_ID",id,"yoast_rest_reflected",reflected==description,"description_length",len(description),flush=True)
        time.sleep(1)
    print("BATCH34_TEN_PRIVATE_YOAST_META_DESCRIPTIONS_SAVED_NO_SLUG_OR_MEDIA_CHANGE",flush=True)
if __name__=="__main__":main()
