#!/usr/bin/env python3
"""Link existing Chery model records to actual published editorial articles.
Only fills empty related-post-IDs metadata; no posts created, slugs modified,
prices changed, or uncertain years assigned.
"""
import importlib.util
import json
import urllib.request
import urllib.parse

spec=importlib.util.spec_from_file_location("bridge","scripts/deploy-dtc-library.py")
bridge=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)
BASE="https://a3tal.com"
# Article 80189 (prices by budget) discusses both Tiggo 7 Pro models.
# Article 80234 is a dedicated Tiggo 4 Pro review and price guide.
PATCHES=[
    {"car_id":83387,"slug":"chery-tiggo-7-pro-max-egypt","posts":[80189]},
    {"car_id":83386,"slug":"chery-tiggo-7-pro-egypt","posts":[80189]},
    {"car_id":83385,"slug":"chery-tiggo-4-pro-egypt","posts":[80234,80189]},
]

def read_public(endpoint):
    url=BASE+endpoint
    req=urllib.request.Request(url,headers={"User-Agent":"A3tal-Editorial-Link-Repair/1.0","Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=40) as r:return json.load(r)

def normalize(data,key):
    x=data.get(key,[])
    if isinstance(x,list):x=x[0] if x else ""
    return str(x if x is not None else "").strip()

def main():
    client=bridge.Bridge()
    state=client.request({"op":"site_info"})
    if state.get("active_theme")!="a3tal-global":raise RuntimeError("Unexpected theme: abort")
    posts={}
    for n in sorted({p for patch in PATCHES for p in patch["posts"]}):
        page=read_public(f"/wp-json/wp/v2/posts/{n}?_fields=id,slug,title,status")
        if int(page.get("id",0))!=n or page.get("status")!="publish":
            raise RuntimeError("Related article not public: "+str(n))
        posts[n]=page.get("title",{}).get("rendered","")
    if "تيجو 4 برو" not in posts[80234] or "أسعار السيارات" not in posts[80189]:
        raise RuntimeError("Published article identifiers no longer match expected subjects")
    for item in PATCHES:
        car=read_public(f"/wp-json/wp/v2/a3tal-cars/{item['car_id']}?_fields=id,slug,status")
        if car.get("slug")!=item["slug"] or int(car.get("id",0))!=item["car_id"] or car.get("status")!="publish":
            raise RuntimeError("Car record changed identity: "+item["slug"])
        existing=client.request({"op":"post_meta","post_id":item["car_id"],"key":"_a3_related_post_ids"})
        before=normalize(existing,"_a3_related_post_ids")
        target=",".join(str(p) for p in item["posts"])
        if before==target:
            print("CHERY_RELATED_ALREADY_LINKED",item["slug"],target,flush=True)
            continue
        if before:
            print("CHERY_RELATED_SKIP_NONEMPTY",item["slug"],before,flush=True)
            continue
        try:
            client.request({"op":"post_meta_set","post_id":item["car_id"],"meta":{"_a3_related_post_ids":target},"confirm":True,"dangerous":True},write=True)
        except RuntimeError as e:
            # Never blindly repeat a mutation on an HTTP 522: validate readback.
            print("CHERY_RELATED_WRITE_RECHECK",item["slug"],str(e),flush=True)
        after=client.request({"op":"post_meta","post_id":item["car_id"],"key":"_a3_related_post_ids"})
        if normalize(after,"_a3_related_post_ids")!=target:
            raise RuntimeError("Related metadata did not match after update: "+item["slug"])
        print("CHERY_RELATED_LINK_CONFIRMED",item["slug"],target,flush=True)
    print("CHERY_RELATED_LINK_BATCH_COMPLETE",len(PATCHES),flush=True)

if __name__=="__main__":
    main()
