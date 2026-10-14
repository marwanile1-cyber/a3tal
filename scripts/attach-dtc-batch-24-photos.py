#!/usr/bin/env python3
"""Attach five original code-specific illustrated WebP covers to matching published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0237","P0451","P0765","U0122","U0401","U0167","C0037","C0041","B1318","B0092"]
RECOVER_UPLOAD={}
ALT={
 "P0237":"صورة فنية حصرية لحساس ضغط شحن التيربو P0237 ودائرة الهواء",
 "P0451":"تصميم أصلي لخزان الوقود ومستشعر ضغط أبخرة البنزين EVAP P0451",
 "P0765":"تصميم تفصيلي أصلي لجسم بلف الفتيس وسولينويد النقل D كود P0765",
 "U0122":"تصميم حصري لوحدة VDC للثبات الإلكتروني وعجلات السيارة U0122",
 "U0401":"تصميم أصلي لوحدة ECM وبيانات الشبكة غير الصالحة U0401",
 "U0167":"رسم فني حصري لمفتاح الإيموبلايزر ووحدة مانع تشغيل المحرك U0167",
 "C0037":"تصميم فني حصري لحساس سرعة عجلة ABS الخلفية اليسرى C0037",
 "C0041":"تصميم توضيحي حصري لحساس سرعة عجلة ABS الأمامية اليمنى C0041",
 "B1318":"تصميم أصلي لجهد بطارية السيارة ووحدة توزيع الكهرباء في تطبيقات فورد B1318",
 "B0092":"تصميم فني أصلي لمقعد الراكب ونظام استشعار وجوده PPS في تطبيقات GM B0092"
}
PHOTO_ROOT=Path("assets/dtc-batch24")
def image_for(code):
    path=PHOTO_ROOT/("a3tal-dtc-"+code.lower()+"-exclusive.webp")
    if not path.is_file():
        raise RuntimeError("Missing reviewed original photographic cover: "+str(path))
    raw=path.read_bytes()
    if not 25_000<len(raw)<500_000:
        raise RuntimeError("Invalid illustration byte size for "+code)
    with Image.open(io.BytesIO(raw)) as photo:
        if photo.format!="WEBP" or photo.width<1600 or photo.height<900:
            raise RuntimeError("Cover must be original high-resolution 1600x900 WebP: "+code)
        photo.verify()
    return raw
last=0.0
def api(endpoint,payload=None):
    global last
    if not KEY:raise RuntimeError("Missing A3TAL direct bridge secret")
    time.sleep(max(0,22-(time.monotonic()-last)));last=time.monotonic()
    data=json.dumps(payload,ensure_ascii=False).encode("utf-8") if payload is not None else None
    headers={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,
             "Accept":"application/json","User-Agent":"A3tal-Original-Art/1.0",
             "Cache-Control":"no-store"}
    if payload is not None:headers["Content-Type"]="application/json"
    req=urllib.request.Request(ROOT+endpoint,data=data,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=75) as response:
            return json.load(response)
    except urllib.error.HTTPError as err:
        raise RuntimeError("Bridge "+endpoint+" returned HTTP "+str(err.code)) from None
def resolve_posts():
    # Read-only public WordPress lookup, no guessing IDs and no uploading to unpublished pages.
    resolved={}
    for code in CODES:
        path="https://a3tal.com/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,status,link"
        req=urllib.request.Request(path,headers={"User-Agent":"A3tal-Art-Preflight/1.0","Accept":"application/json","Cache-Control":"no-cache"})
        try:
            with urllib.request.urlopen(req,timeout=35) as stream:
                entries=json.load(stream)
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as err:
            raise RuntimeError("Cannot verify published record safely for "+code+": "+type(err).__name__) from None
        matching=[x for x in entries if x.get("slug")==code.lower() and x.get("status")=="publish"]
        if len(matching)!=1:raise RuntimeError("Code not exactly once published: "+code)
        resolved[code]=int(matching[0]["id"])
        print("VERIFIED POST",code,resolved[code],flush=True)
    return resolved
def main():
    posts=resolve_posts()
    for code,post_id in posts.items():
        post=api("/post/"+str(post_id))
        if post["status"]!="publish" or post["slug"]!=code.lower():
            raise RuntimeError("Wrong published DTC page for "+code)
        if post.get("featured_media"):
            print("Already has featured media, preserving:",code,post["featured_media"],flush=True)
            continue
        print("Published post preflight",code,"featured=",post.get("featured_media"),flush=True)
        img=image_for(code)
        if not (10_000<len(img)<450_000):raise RuntimeError("Unexpected original illustration size for "+code)
        payload={"post_id":post_id,"filename":"a3tal-dtc-"+code.lower()+"-exclusive.webp",
                 "title":"A3tal "+code+" original diagnostic visual","alt":ALT[code],
                 "image_base64":base64.b64encode(img).decode("ascii"),"convert_webp":False}
        # If an image upload has an uncertain response, never blindly repeat the mutation.
        if code in RECOVER_UPLOAD:
            media_id=RECOVER_UPLOAD[code]
            print("Reusing previously uploaded art",code,media_id,flush=True)
        else:
            media=api("/upload-image-data",payload)
            media_id=int(media["media_id"])
            print("Art uploaded",code,"media",media_id,flush=True)
        confirm=api("/set-featured-image",{"post_id":post_id,"media_id":media_id})
        print("Set-featured server result",code,confirm.get("featured_media"),flush=True)
        if int(confirm.get("featured_media") or 0)!=media_id:
            raise RuntimeError("WordPress refused featured image for "+code)
        # Host cache layers can serve an older post response after a successful mutation.
        checked=None
        for check in range(3):
            checked=api("/post/"+str(post_id)+"?a3tal_media_verify="+str(int(time.time())))
            got=int(checked.get("featured_media") or 0)
            print("Readback",code,"attempt",check+1,"featured",got,flush=True)
            if got==media_id:break
            time.sleep(25)
        if int(checked.get("featured_media") or 0)!=media_id:
            raise RuntimeError("Featured image persisted in mutation response but post endpoint not consistent for "+code)
        print("VERIFIED COVER",code,checked["link"],"image",media_id,"bytes",len(img),flush=True)
    print("All batch 24 original diagnostic illustrations processed safely",flush=True)
if __name__=="__main__":main()
