#!/usr/bin/env python3
"""Replace reviewed batch27 illustrated covers, without touching post slugs/content.
Requires assets/dtc-batch27-photographic/ files already committed.
"""
import base64, hashlib, io, json, os, time, urllib.request
from pathlib import Path
from PIL import Image

SITE="https://a3tal.com"
ROOT=Path(__file__).resolve().parent.parent
FOLDER=ROOT/"assets/dtc-batch27-photographic"
CODES="P0261 P0327 P0571 U0125 U0132 U0141 C0044 C0046 B1213 B1232".split()
KEY=os.getenv("A3TAL_API_KEY","")
last_call=0

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"A3tal-Photo-Quality/1.0","Cache-Control":"no-cache"}),timeout=50) as r:
        return json.load(r)

def bridge(endpoint,payload):
    global last_call
    if not KEY:raise RuntimeError("No A3TAL_API_KEY")
    time.sleep(max(0,22-(time.monotonic()-last_call)))
    last_call=time.monotonic()
    data=json.dumps(payload,ensure_ascii=False).encode()
    req=urllib.request.Request(SITE+"/wp-json/a3tal-direct/v1"+endpoint,data=data,headers={
        "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,
        "Content-Type":"application/json","Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=90) as response:
        return json.load(response)

def valid_assets():
    manifest=json.loads((FOLDER/"manifest.json").read_text(encoding="utf-8"))
    entries=manifest["files"]
    if len(entries)!=10 or {e["code"] for e in entries}!=set(CODES):
        raise RuntimeError("Exactly ten original code-specific covers are required")
    seen=set();images={}
    for e in entries:
        code=e["code"];filename="a3tal-dtc-"+code.lower()+"-photographic.webp"
        if e["filename"]!=filename or e.get("image_origin")!="original_ai_photorealistic":
            raise RuntimeError("Unreviewed image metadata: "+code)
        raw=(FOLDER/filename).read_bytes()
        h=hashlib.sha256(raw).hexdigest()
        if h in seen or h!=e["sha256"] or len(raw)!=e["bytes"] or not 30000<=len(raw)<500000:
            raise RuntimeError("Image checksum/size/duplication failure: "+code)
        with Image.open(io.BytesIO(raw)) as im:
            if im.format!="WEBP" or im.size!=(1600,900):raise RuntimeError("Wrong image format: "+code)
            im.verify()
        seen.add(h);images[code]=raw
    return images

def wp_post(code):
    url=SITE+"/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,status,featured_media,link,yoast_head_json"
    rows=get(url)
    found=[r for r in rows if r["slug"]==code.lower() and r["status"]=="publish"]
    if len(found)!=1:raise RuntimeError("Published identity could not be verified for "+code)
    return found[0]

def media_url(media_id):
    if not media_id:return ""
    return get(SITE+"/wp-json/wp/v2/media/"+str(media_id)+"?_fields=source_url")["source_url"]

def main():
    images=valid_assets()
    if not KEY:raise RuntimeError("Bridge credentials missing")
    for code in CODES:
        post=wp_post(code)
        post_id=int(post["id"]);media_id=int(post.get("featured_media") or 0)
        src=media_url(media_id)
        prefix="a3tal-dtc-"+code.lower()
        if prefix+"-photographic" in src:
            print("ALREADY_CORRECTED",code,flush=True)
            continue
        if prefix+"-exclusive" not in src:
            raise RuntimeError("Unexpected featured media for "+code+"; avoid overwriting editorial edits")
        image_id=int(bridge("/upload-image-data",{
            "post_id":post_id,"filename":prefix+"-photographic.webp",
            "title":"أعطال.كوم | "+code+" | صورة تشخيصية واقعية حصرية",
            "alt":"مشهد تشخيصي واقعي من تصميم أعطال.كوم لكود "+code,
            "image_base64":base64.b64encode(images[code]).decode("ascii"),"convert_webp":False
        })["media_id"])
        if image_id<=0:raise RuntimeError("No uploaded ID for "+code)
        print("UPLOADED",code,image_id,flush=True)
        result=bridge("/set-featured-image",{"post_id":post_id,"media_id":image_id})
        if int(result.get("featured_media") or 0)!=image_id:
            raise RuntimeError("Featured write unverified; do not reupload: "+code)
        updated=wp_post(code)
        if int(updated["id"])!=post_id or updated["slug"]!=code.lower():
            raise RuntimeError("Post identity changed: "+code)
        if int(updated.get("featured_media") or 0)!=image_id:
            raise RuntimeError("New featured media not persistent: "+code)
        og=updated.get("yoast_head_json",{}).get("og_image",[])
        if not any(prefix+"-photographic" in i.get("url","") for i in og if isinstance(i,dict)):
            raise RuntimeError("Check pending stale OG/cache for "+code+" before proceeding")
        print("PHOTO_OG_CONFIRMED",code,updated.get("link"),flush=True)
    print("BATCH27_PHOTOGRAPHY_VERIFIED",flush=True)

if __name__=="__main__":main()
