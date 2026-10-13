#!/usr/bin/env python3
"""Repair Yoast OG/Twitter image for confirmed original DTC post, using existing Direct Bridge.
Idempotent for matching media, only writes to whitelisted DTC batch slugs, no content changes.
"""
import os,json,time,urllib.request,urllib.error,urllib.parse,html,argparse
ROOT="https://a3tal.com"
KEY=os.environ["A3TAL_API_KEY"]
BATCHES={
  "07-08":["P0138","P0192","P0193","P0449","P0105","P0140","P0190","P0205","P0481"],
  "09":["P0012","P0206","P0452","P0506","P0706"],
  "10":["P0017","P0116","P0139","P0234","P0453"]
}
STAMP=0
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"A3tal-DTC-OG-Repair/1.0","Accept":"application/json","Cache-Control":"no-cache"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req,timeout=40) as res:return json.load(res)
        except urllib.error.HTTPError as err:
            if err.code not in (429,500,502,503,504,520,522,524) or attempt==3:
                raise RuntimeError("Read-only OG preflight HTTP "+str(err.code)) from None
            print("Transient origin read",err.code,"attempt",attempt+1,flush=True)
        except (urllib.error.URLError,TimeoutError):
            if attempt==3:
                raise RuntimeError("Read-only OG preflight transport error") from None
        time.sleep(35*(attempt+1))
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
    previous=[x.get("url","") for x in post.get("yoast_head_json",{}).get("og_image",[])]
    if url in previous:
        print("Already correct; preserving",code,id,flush=True)
    else:
        print("Repairing Yoast OG/Twitter for",code,id,"featured",media,flush=True)
        meta={"_yoast_wpseo_opengraph-image":url,"_yoast_wpseo_opengraph-image-id":str(media),
              "_yoast_wpseo_twitter-image":url,"_yoast_wpseo_twitter-image-id":str(media)}
        bridge({"op":"post_meta_set","post_id":id,"meta":meta})
        # Refresh indexable using standard post-save hook, keeping the existing content.
        title=html.unescape(str(post.get("title",{}).get("rendered","")))
        if not title:raise RuntimeError("Original post title absent: "+code)
        try:
            bridge({"op":"platform_entity_upsert","type":"a3_dtc","id":id,"title":title,"status":"publish"})
        except (urllib.error.HTTPError,TimeoutError,urllib.error.URLError) as err:
            # A lost HTTP response may follow a successful save. Verify live OG,
            # never blindly send another WordPress post-save mutation.
            print("Ambiguous WordPress post-save:",code,type(err).__name__,"checking public OG",flush=True)
            current=get(ROOT+"/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,yoast_head_json")
            actual=[x.get("url","") for x in current[0].get("yoast_head_json",{}).get("og_image",[])] if current else []
            if url not in actual:
                raise RuntimeError("Post-save unconfirmed for "+code+"; safe to re-evaluate next run") from None
            print("Recovered Yoast update after lost HTTP response:",code,flush=True)
    after=get(ROOT+"/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,featured_media,yoast_head_json")
    og=[x.get("url","") for x in after[0].get("yoast_head_json",{}).get("og_image",[])]
    print("VERIFIED_OG_STATE",code,"featured",media,"og_images",og,flush=True)
    if url not in og:raise RuntimeError("Yoast OG did not reflect featured art after cache refresh: "+code)
    print("SUCCESS",code,url,flush=True)
if __name__=="__main__":
  parser=argparse.ArgumentParser()
  parser.add_argument("--batch",choices=sorted(BATCHES),default="07-08")
  args=parser.parse_args()
  for c in BATCHES[args.batch]:one(c)
