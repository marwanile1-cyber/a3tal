#!/usr/bin/env python3
"""Repair Yoast OG/Twitter image for confirmed original DTC post, using existing Direct Bridge.
Idempotent for matching media, only writes to whitelisted DTC batch slugs, no content changes.
"""
import os,json,time,urllib.request,urllib.error,urllib.parse,html
ROOT="https://a3tal.com"
KEY=os.environ["A3TAL_API_KEY"]
CODES=["P0137"]
STAMP=0
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"A3tal-DTC-OG-Repair/1.0","Accept":"application/json","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=35) as res:return json.load(res)
def bridge(payload):
    global STAMP
    time.sleep(max(0,23-(time.monotonic()-STAMP)));STAMP=time.monotonic()
    body=json.dumps(payload,ensure_ascii=False).encode("utf-8")
    req=urllib.request.Request(ROOT+"/wp-json/a3tal-direct/v1/admin",data=body,headers={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Accept":"application/json","Cache-Control":"no-cache","User-Agent":"A3tal-DTC-OG-Repair/1.0"})
    with urllib.request.urlopen(req,timeout=80) as res:
        obj=json.load(res)
    if not obj.get("ok"):raise RuntimeError("Bridge returned failed operation")
    return obj["result"]
def one(code):
    found=get(ROOT+"/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,status,title,featured_media,yoast_head_json")
    matches=[x for x in found if x.get("slug")==code.lower() and x.get("status")=="publish"]
    if len(matches)!=1:raise RuntimeError("No unique published DTC page: "+code)
    post=matches[0];id=int(post["id"]);media=int(post.get("featured_media") or 0)
    if not media:raise RuntimeError("Missing featured art: "+code)
    art=get(ROOT+"/wp-json/wp/v2/media/"+str(media)+"?_fields=id,source_url,mime_type")
    url=art.get("source_url","")
    if not url.startswith(ROOT+"/wp-content/uploads/") or art.get("mime_type")!="image/webp":
        raise RuntimeError("Invalid featured media URL/mime: "+code)
    current=bridge({"op":"post_meta","post_id":id,"key":"_yoast_wpseo_opengraph-image"})
    if isinstance(current,dict) and current.get("_yoast_wpseo_opengraph-image")==url:
        print("Already synchronized",code,id,url,flush=True)
    else:
        print("Setting verified Yoast image",code,id,media,flush=True)
        meta={"_yoast_wpseo_opengraph-image":url,"_yoast_wpseo_opengraph-image-id":str(media),
              "_yoast_wpseo_twitter-image":url,"_yoast_wpseo_twitter-image-id":str(media)}
        bridge({"op":"post_meta_set","post_id":id,"meta":meta})
        check=bridge({"op":"post_meta","post_id":id,"key":"_yoast_wpseo_opengraph-image"})
        if not isinstance(check,dict) or check.get("_yoast_wpseo_opengraph-image")!=url:
            raise RuntimeError("Meta write could not be verified: "+code)
    # Force Yoast indexable refresh through the normal WordPress post-save hook.
    title=html.unescape(str(post.get("title",{}).get("rendered","")).replace("&amp;","&"))
    if not title:raise RuntimeError("Missing original post title")
    bridge({"op":"platform_entity_upsert","type":"a3_dtc","id":id,"title":title,"status":"publish"})
    after=get(ROOT+"/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,featured_media,yoast_head_json")
    og=[x.get("url","") for x in after[0].get("yoast_head_json",{}).get("og_image",[])]
    print("VERIFIED_OG_STATE",code,"featured",media,"og_images",og,flush=True)
    if url not in og:raise RuntimeError("Yoast OG did not reflect featured art after cache refresh: "+code)
    print("SUCCESS",code,url,flush=True)
if __name__=="__main__":
  for c in CODES:one(c)
