#!/usr/bin/env python3
"""Idempotently publish a researched K4-vs-Octavia comparison via the approved bridge.
Only append the published comparison to precisely verified existing car records.
Do not overwrite article URLs, prices, images or unrelated relationship IDs.
"""
import base64
import io
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
DATA=Path("data/comparisons/k4-vs-octavia-2027-egypt.json")
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY: raise SystemExit("Missing A3TAL_API_KEY GitHub secret")

def http(url, data=None, auth=True, retries=3):
    url=url if url.startswith("https://") else API+url
    headers={"User-Agent":"A3talVerifiedComparison/1.0","Accept":"application/json,image/webp,text/html,*/*","Cache-Control":"no-cache"}
    if auth: headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    payload=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf-8")
    if payload is not None: headers["Content-Type"]="application/json"
    attempts=1 if payload is not None else retries
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=payload, headers=headers),timeout=150) as response:
                result=response.read()
            return json.loads(result) if auth else result
        except Exception as exc:
            if attempt+1>=attempts:raise
            print("READ_ONLY_RETRY",attempt+1,type(exc).__name__,str(exc)[:150],flush=True)
            time.sleep(8*(attempt+1))

def remote_post(slug):
    endpoint=SITE+"/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":slug,"per_page":3,"_fields":"id,slug,status,link,featured_media"})
    rows=json.loads(http(endpoint,auth=False))
    if len(rows)>1: raise RuntimeError("Duplicate article slug: "+slug)
    return rows[0] if rows else None

def make_feature(sources,slug):
    photos=[]
    for url in sources:
        img=Image.open(io.BytesIO(http(url,auth=False)))
        img.load()
        if img.width<1100 or img.height<600:raise RuntimeError("Source photo is too small for editorial cover: "+url)
        photos.append(ImageOps.fit(img.convert("RGB"),(800,900),method=Image.Resampling.LANCZOS,centering=(.52,.48)))
    if len(photos)!=2:raise RuntimeError("Expected exactly two verified car photos")
    canvas=Image.new("RGB",(1600,900))
    for i,photo in enumerate(photos):canvas.paste(photo,(800*i,0))
    # Editorial split without overlaid text or misleading compositing.
    ImageDraw.Draw(canvas).rectangle((796,0,804,900),fill=(228,230,232))
    canvas=ImageEnhance.Contrast(canvas).enhance(1.04)
    output=io.BytesIO()
    canvas.save(output,format="WEBP",quality=85,method=6)
    photo=output.getvalue()
    if not 40000<len(photo)<2400000: raise RuntimeError("WebP featured image failed size validation")
    filename="a3tal-k4-vs-octavia-2027-official-photos.webp"
    print("FEATURED_WEBP_READY",len(photo),flush=True)
    return {"filename":filename,
            "title":"مقارنة كيا K4 وسكودا أوكتافيا في مصر بصورتين فوتوغرافيتين",
            "alt":"كيا K4 السيدان وسكودا أوكتافيا المحدثة، مقارنة فوتوغرافية بين السيارتين",
            "role":"featured","convert_webp":False,
            "image_base64":base64.b64encode(photo).decode("ascii")}

def bridge_client():
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location("a3tal_direct_bridge","scripts/deploy-dtc-library.py")
    module=module_from_spec(spec);spec.loader.exec_module(module)
    return module.Bridge()

def car_record(slug):
    url=SITE+"/wp-json/wp/v2/a3tal-cars?"+urllib.parse.urlencode({"slug":slug,"per_page":3,"_fields":"id,slug,status,title"})
    cars=json.loads(http(url,auth=False))
    if len(cars)!=1 or cars[0].get("status")!="publish" or cars[0].get("slug")!=slug:
        raise RuntimeError("Expected unique published car record: "+slug)
    return int(cars[0]["id"])

def read_related(client,id_):
    result=client.request({"op":"post_meta","post_id":id_,"key":"_a3_related_post_ids"})
    val=result.get("_a3_related_post_ids","")
    if isinstance(val,list):val=val[0] if val else ""
    return str(val or "").strip()

def link_both_cars(article_id,car_slugs):
    client=bridge_client()
    for slug in car_slugs:
        vid=car_record(slug)
        current=read_related(client,vid)
        existing=[int(x) for x in re.findall(r"\d+",current)]
        # The post may already be curated for 1-3 models. Never remove those links.
        if article_id in existing:
            print("CAR_LINK_ALREADY_PRESENT",slug,flush=True)
            continue
        target=",".join(map(str,[*existing,article_id]))
        if current and not re.fullmatch(r"[\d,\s;|]+",current):
            raise RuntimeError("Unrecognized existing manual car relationships, skip mutation: "+slug)
        try:
            client.request({"op":"post_meta_set","post_id":vid,
                            "meta":{"_a3_related_post_ids":target},
                            "confirm":True,"dangerous":True},write=True)
        except RuntimeError as exc:
            print("CAR_LINK_WRITE_RESPONSE_UNCERTAIN_RECHECK",slug,str(exc)[:130],flush=True)
        actual=read_related(client,vid)
        if [int(x) for x in re.findall(r"\d+",actual)]!=[*existing,article_id]:
            raise RuntimeError("Related car IDs did not read back correctly: "+slug)
        print("CAR_COMPARISON_LINK_VERIFIED",slug,"article",article_id,flush=True)

def main():
    data=json.loads(DATA.read_text(encoding="utf-8"))
    slug=data["slug"]
    if data["category_id"]!=21 or len(data["html"])<11000:
        raise RuntimeError("Comparison content is incomplete or lacks category")
    if data["html"].count("<h2>")<7 or data["html"].count("<table>")<3:
        raise RuntimeError("Editorial depth/decision tables missing")
    if data["html"].count("https://a3tal.com/cars/")<2:
        raise RuntimeError("Model journey links are incomplete")
    old=remote_post(slug)
    if old and old.get("status")=="publish":
        if not old.get("featured_media"):raise RuntimeError("Existing slug is published without featured image; manual review needed")
        id_=int(old["id"])
        print("ARTICLE_ALREADY_LIVE",old["link"],id_,flush=True)
    elif old:
        raise RuntimeError("Existing comparison slug has an unpublished draft; do not clobber editorial work")
    else:
        status=http("/status")
        if not status.get("ok"):raise RuntimeError("Direct Bridge unavailable")
        matches=http("/search-posts?"+urllib.parse.urlencode({"search":"كيا K4 سكودا أوكتافيا","status":"any","limit":100})).get("items",[])
        for item in matches:
            if item.get("slug")==slug:continue
            name=str(item.get("title","")).casefold()
            if ("k4" in name and ("octavia" in name or "أوكتافيا" in name)):
                raise RuntimeError("Possible same-intent comparison already exists: "+str(item.get("id")))
        post={"title":data["title"],"slug":slug,"type":"post","status":"publish",
              "excerpt":data["excerpt"],"content":data["html"],"categories":[data["category_id"]],
              "meta":{"_yoast_wpseo_title":data["seo_title"],"_yoast_wpseo_metadesc":data["meta"],
                      "_yoast_wpseo_focuskw":data["focus"],"_yoast_wpseo_canonical":SITE+"/"+slug+"/",
                      "_yoast_wpseo_opengraph-title":data["title"],
                      "_yoast_wpseo_opengraph-description":data["meta"]}}
        cover=make_feature(data["source_photos"],slug)
        print("SENDING_ONE_IDEMPOTENT_PUBLISH_BUNDLE",slug,flush=True)
        try:
            result=http("/publish-bundle",{"post":post,"media":[cover]})
        except Exception as exc:
            print("AMBIGUOUS_PUBLISH_NO_AUTOMATIC_REPLAY",str(exc)[:170],flush=True)
            raise
        published=result.get("post") or {}
        id_=int(published.get("id") or 0)
        if not result.get("ok") or not id_ or published.get("status")!="publish" or not published.get("featured_media"):
            raise RuntimeError("Bundle did not return a published article with featured WebP")
        print("ARTICLE_PUBLISHED",published.get("link"),id_,published.get("featured_media"),flush=True)
    # Publishing and relationship updates are separately confirmed. Never assume a crosslink happened.
    confirmed=remote_post(slug)
    if not confirmed or confirmed["status"]!="publish" or int(confirmed.get("id") or 0)!=id_:
        raise RuntimeError("Published post could not be confirmed in public REST")
    link=confirmed["link"]
    assert int(confirmed.get("featured_media") or 0)>0
    for pause in (0,10,20,35):
        if pause:time.sleep(pause)
        try:
            page=http(link+"?a3tal_release_check="+str(int(time.time())),auth=False,retries=1).decode("utf-8","replace")
            for marker in ["كيا K4","أوكتافيا","skoda-octavia-2027-egypt","kia-k4-2027-egypt","a3tal-k4-vs-octavia-2027-official-photos","og:image"]:
                if marker not in page: raise RuntimeError("Missing expected public HTML marker: "+marker)
            if "noindex" in page.lower(): raise RuntimeError("New comparison unexpectedly noindexed")
            print("COMPARISON_PUBLIC_HTML_VERIFIED",link,flush=True)
            break
        except Exception as exc:
            if pause==35:raise
            print("COMPARISON_PUBLIC_RECHECK",str(exc)[:140],flush=True)
    link_both_cars(id_,data["car_slugs"])
    print("COMPARISON_WITH_MODEL_LINKS_COMPLETE",link,flush=True)

if __name__=="__main__":
    main()
