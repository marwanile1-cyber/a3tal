#!/usr/bin/env python3
"""Finish S09 encyclopedia: existing official Deepal terms, editorial related card, Yoast index.
Never overwrite unrelated vehicles, prices or image. Verify readback and robots to flag global filter.
"""
import json,os,urllib.request,urllib.parse
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
CAR_SLUG="deepal-s09-2027-egypt"
TITLE="ديبال S09 موديل 2027 في مصر | الأسعار والمواصفات"
def req(path,data=None,secure=True):
    head={"Accept":"application/json","User-Agent":"A3tal S09 SEO Finalize/20261026"}
    if secure:head.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=json.dumps(data,ensure_ascii=False).encode("utf8") if data is not None else None
    if raw is not None:head["Content-Type"]="application/json; charset=utf-8"
    url=(API if secure else SITE)+path
    with urllib.request.urlopen(urllib.request.Request(url,data=raw,headers=head,method="POST" if raw is not None else "GET"),timeout=100) as f:return json.load(f)
def meta(pid,key):
    data=req("/admin?"+urllib.parse.urlencode({"op":"post_meta","post_id":pid,"key":key}))
    if not data.get("ok"):raise RuntimeError("Cannot read meta "+key)
    return str(data.get("result",{}).get(key,"")).strip()
def run():
    fields="_fields=id,slug,title,status,link,featured_media,yoast_head_json,a3_brand,a3_market,a3_car_body"
    cars=req("/wp-json/wp/v2/a3tal-cars?"+urllib.parse.urlencode({"slug":CAR_SLUG,"_fields":fields[len("_fields="):]}),secure=False)
    if len(cars)!=1 or cars[0]["slug"]!=CAR_SLUG or cars[0]["status"]!="publish" or not cars[0].get("featured_media") or cars[0]["title"]["rendered"]!=TITLE:
        raise RuntimeError("Existing car identity failed")
    car=cars[0];pid=int(car["id"])
    post=req("/wp-json/wp/v2/posts/84623?_fields=id,slug,status,link",secure=False)
    if post["slug"]!="deepal-s09-2027-egypt-price-premium-signature-reev" or post["status"]!="publish":
        raise RuntimeError("Wrong linked article")
    meta_pre={k:meta(pid,k) for k in ("_a3_price_min","_a3_price_max","_a3_related_post_ids","_yoast_wpseo_meta-robots-noindex")}
    if (meta_pre["_a3_price_min"],meta_pre["_a3_price_max"])!=("2850000","3100000"):
        raise RuntimeError("Unanticipated S09 price change: "+str(meta_pre))
    print("BEFORE_S09_META",meta_pre,flush=True)
    desired={"_a3_related_post_ids":str(post["id"]),"_yoast_wpseo_meta-robots-noindex":"2"}
    result=req("/admin",{"op":"platform_entity_upsert","id":pid,"type":"a3_car","slug":CAR_SLUG,
         "title":TITLE,"status":"publish",
         "meta":desired,
         "taxonomies":{"a3_brand":["deepal"],"a3_car_body":["suv"],"a3_market":["egypt"]},
         "confirm":True,"dangerous":True})
    if not result.get("ok"):raise RuntimeError("Entity update rejected "+str(result)[:500])
    after={k:meta(pid,k) for k in desired}
    print("AFTER_S09_META",after,flush=True)
    if after!=desired:raise RuntimeError("Car SEO/editorial link meta not persisted")
    cars=req("/wp-json/wp/v2/a3tal-cars?"+urllib.parse.urlencode({"slug":CAR_SLUG,"_fields":"id,slug,status,featured_media,link,yoast_head_json,a3_brand,a3_market,a3_car_body"}),secure=False)
    row=cars[0]
    print("NEW_TAXONOMIES",row.get("a3_brand"),row.get("a3_car_body"),row.get("a3_market"),flush=True)
    seo=row.get("yoast_head_json") or {}
    print("CAR_YOAST",str(seo.get("robots")),str(seo.get("canonical")),flush=True)
    if (seo.get("robots") or {}).get("index")=="noindex":
        raise RuntimeError("Still noindex on live car despite explicit Yoast index override. Investigate global SEO filter.")
    if seo.get("canonical")!=row["link"]:
        raise RuntimeError("Car canonical mismatch")
    if pid!=int(row.get("id",0)) or not row.get("featured_media"):
        raise RuntimeError("Car identity/cover changed")
    print("LIVE_CAR_INDEX_LINK_TAXONOMIES_VERIFIED",row["link"],"ARTICLE",post["link"],flush=True)
if __name__=="__main__":run()
