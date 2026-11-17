#!/usr/bin/env python3
"""One-time authenticated A3tal Direct Bridge image upload for ten existing posts.

Input: GitHub-tracked Base64 ZIP, originally exported from ChatGPT image generation.
No fake photo claims, no new articles, no slug/canonical/category/SEO title changes.
All image bytes, post IDs, original images and link targets are checked before writes.
Idempotent across partial successes: completed featured+inline uploads are skipped.
"""
import base64
import hashlib
import html
import io
import json
import os
import re
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/"data/seo10-webp-upload-20261117.json").read_text(encoding="utf-8"))
B64=ROOT/CFG["zip_b64_path"]
HOST="https://a3tal.com"
API=HOST+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise SystemExit("Missing required Direct Bridge secret")
MARK="a3tal-seo10-exclusive-webp-20261117"
if len(CFG["items"])!=10 or len({i["id"] for i in CFG["items"]})!=10:
    raise SystemExit("Ten distinct article IDs are required")

def request(url,body=None,auth=True):
    headers={"Accept":"application/json","User-Agent":"curl/8.5.0","Cache-Control":"no-cache"}
    if auth:
        headers["X-A3tal-Key"]=KEY
        headers["Authorization"]="Bearer "+KEY
    raw=None if body is None else json.dumps(body,ensure_ascii=False).encode("utf-8")
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,data=raw,headers=headers,method="POST" if raw else "GET")
    with urllib.request.urlopen(req,timeout=175) as response:
        return json.load(response)

def bridge(pid):return request(API+"/post/"+str(pid))
def public_post(pid):
    return request(HOST+"/wp-json/wp/v2/posts/"+str(pid)+
                   "?_fields=id,status,slug,link,featured_media,yoast_head_json&cb=a3tal-image-"+str(time.time_ns()),auth=False)
def media(mid):
    return request(HOST+"/wp-json/wp/v2/media/"+str(mid)+
                   "?_fields=id,source_url,alt_text,media_details",auth=False)
def url_norm(u):
    p=urllib.parse.urlsplit(str(u))
    return p.scheme+"://"+p.netloc+urllib.parse.unquote(p.path).rstrip("/")
def og(seo):
    ims=seo.get("og_image") or []
    return (ims[0].get("url") if isinstance(ims,list) and ims else "") or ""
def check_original(item,source,wp):
    if int(source.get("id") or 0)!=item["id"] or int(wp.get("id") or 0)!=item["id"]:
        raise RuntimeError("Post ID mismatch "+str(item["id"]))
    if str(source.get("status"))!="publish" or wp.get("status")!="publish":
        raise RuntimeError("Post is not published: "+str(item["id"]))
    if urllib.parse.unquote(source.get("slug",""))!=item["slug"] or urllib.parse.unquote(wp.get("slug",""))!=item["slug"]:
        raise RuntimeError("Unexpected slug "+str(item["id"]))
    if int(source.get("featured_media") or 0)<1:
        raise RuntimeError("No existing featured image for post "+str(item["id"]))
    seo=wp.get("yoast_head_json") or {}
    if url_norm(seo.get("canonical",""))!=url_norm(wp.get("link","")):
        raise RuntimeError("Canonical mismatch "+str(item["id"]))
    if not og(seo) or (seo.get("robots") or {}).get("index")=="noindex":
        raise RuntimeError("Unhealthy indexability metadata "+str(item["id"]))
    if "a3tal-seo10-answer-first" not in source.get("content",""):
        raise RuntimeError("Expected recently revised answer-first content missing "+str(item["id"]))
    return seo

def extract_bundle():
    txt=B64.read_text(encoding="utf-8").strip()
    if len(txt)<1000000:
        raise RuntimeError("Missing or truncated Base64 image archive")
    binary=base64.b64decode(txt,validate=True)
    digest=hashlib.sha256(binary).hexdigest()
    if digest!=CFG["zip_sha256"]:
        raise RuntimeError("Transfer ZIP SHA256 mismatch; refusing image uploads")
    z=zipfile.ZipFile(io.BytesIO(binary))
    expected={i["file"] for i in CFG["items"]}
    if set(z.namelist())!=expected:
        raise RuntimeError("ZIP contains missing, extra or unexpected files")
    checked={}
    try:
        from PIL import Image
    except ImportError as e:
        raise RuntimeError("Pillow missing, refusing unvalidated image uploads") from e
    for item in CFG["items"]:
        name=item["file"]
        b=z.read(name)
        if not b.startswith(b"RIFF") or b[8:12]!=b"WEBP":
            raise RuntimeError("Invalid WebP "+name)
        with Image.open(io.BytesIO(b)) as im:
            if im.format!="WEBP" or im.size!=(1600,900):
                raise RuntimeError("Unexpected image dimensions "+name)
            im.verify()
        checked[name]=b
        print("MEDIA_FILE_QA_PASS",name,len(b),flush=True)
    return checked

def new_media_filename(item):
    return "a3tal-exclusive-20261117-"+item["file"]

def expected_media_url(existing_url,item):
    # WordPress can suffix a duplicate filename (-1.webp).
    stem=new_media_filename(item).removesuffix(".webp")
    return stem in urllib.parse.unquote(existing_url or "")

def inline_figure(item,url):
    alt=html.escape(item["alt"],quote=True)
    image_url=html.escape(url,quote=True)
    return ("\n<figure id='"+MARK+"-"+str(item["id"])+"' class='wp-block-image a3tal-exclusive-article-image' "
            "style='max-width:100%;margin:18px auto 24px;text-align:center'>"
            "<img src='"+image_url+"' width='1600' height='900' alt='"+alt+"' "
            "decoding='async' loading='eager' style='display:block;width:100%;max-width:1600px;height:auto;border-radius:9px' />"
            "<figcaption>صورة فوتوغرافية توضيحية لموضوع الفحص؛ لا توثق حالة إصلاح بعينها.</figcaption>"
            "</figure>\n")

def ensure_inline(item,url):
    pid=item["id"]
    live=bridge(pid)
    original=live.get("content","")
    if MARK+"-"+str(pid) in original:
        if url not in original:
            raise RuntimeError("Marker exists but image URL changed: "+str(pid))
        print("IMAGE_INLINE_ALREADY_PRESENT",pid,flush=True)
        return
    marker=re.search(r'<section\b[^>]*class=["\'][^"\']*a3tal-seo10-answer-first[^"\']*["\'][^>]*>[\s\S]{10,2700}?</section>',original,re.I)
    if not marker:
        raise RuntimeError("No exact original answer-first section for inline insertion "+str(pid))
    changed=original[:marker.end()]+inline_figure(item,url)+original[marker.end():]
    if changed.count("<img")!=original.count("<img")+1:
        raise RuntimeError("Unexpected image-count change")
    oldlinks=re.findall(r'<a\b[^>]*href=["\']([^"\']+)',original,re.I)
    newlinks=re.findall(r'<a\b[^>]*href=["\']([^"\']+)',changed,re.I)
    if oldlinks!=newlinks:
        raise RuntimeError("Original editorial links changed")
    res=request(API+"/update-post",{"id":pid,"expected_modified_gmt":live["modified_gmt"],"content":changed})
    if res.get("error") or res.get("ok") is False:
        raise RuntimeError("Bridge rejected inline addition "+str(pid))
    again=bridge(pid)
    if MARK+"-"+str(pid) not in again.get("content","") or url not in again.get("content",""):
        raise RuntimeError("New image failed inline verification "+str(pid))
    print("IMAGE_INLINE_PUBLISHED",pid,flush=True)

def update_one(item,img_bytes,baseline):
    pid=item["id"]
    target_name=new_media_filename(item)
    wp=public_post(pid)
    seo_before=check_original(item,baseline,wp)
    old_featured=int(wp["featured_media"])
    prev_og=og(seo_before)
    media_id=None
    if expected_media_url(prev_og,item):
        media_id=old_featured
        existing=media(media_id)
        image_url=existing["source_url"]
        print("IMAGE_ALREADY_FEATURED",pid,media_id,flush=True)
    else:
        payload={
            "post_id":pid,
            "filename":target_name,
            "title":"أعطال.كوم | "+item["file"].removesuffix(".webp").replace("-"," "),
            "alt":item["alt"],
            "convert_webp":False,
            "image_base64":base64.b64encode(img_bytes).decode("ascii")
        }
        uploaded=request(API+"/upload-image-data",payload)
        media_id=int(uploaded.get("media_id") or 0)
        image_url=uploaded.get("url") or ""
        if media_id<1 or not image_url:
            raise RuntimeError("Bridge did not return usable uploaded image "+str(pid))
        md=media(media_id)
        if not expected_media_url(md.get("source_url",""),item):
            raise RuntimeError("Uploaded media source name unexpected "+str(pid))
        if md.get("alt_text","")!=item["alt"]:
            raise RuntimeError("Uploaded media ALT differs "+str(pid))
        dimensions=md.get("media_details") or {}
        if dimensions.get("width",0)<1200 or dimensions.get("height",0)<630:
            raise RuntimeError("Uploaded image resolution too small "+str(pid))
        print("IMAGE_MEDIA_UPLOADED",pid,media_id,image_url,flush=True)
        changed=request(API+"/set-featured-image",{"post_id":pid,"media_id":media_id})
        if int(changed.get("featured_media") or 0)!=media_id:
            raise RuntimeError("Featured image did not change "+str(pid))
        print("IMAGE_FEATURED_ASSIGNED",pid,media_id,flush=True)
    ensure_inline(item,image_url)
    for retry in range(6):
        after=public_post(pid)
        seo_after=after.get("yoast_head_json") or {}
        new_og=og(seo_after)
        if int(after.get("featured_media") or 0)==media_id and expected_media_url(new_og,item):
            if url_norm(seo_after.get("canonical",""))!=url_norm(seo_before.get("canonical","")):
                raise RuntimeError("Canonical changed after image upload")
            if (seo_after.get("robots") or {}).get("index")=="noindex":
                raise RuntimeError("Noindex introduced after image upload")
            if after.get("link")!=wp.get("link"):
                raise RuntimeError("Permalink changed after image upload")
            return print("IMAGE_LIVE_VERIFIED",pid,media_id,new_og,flush=True)
        time.sleep(3)
    raise RuntimeError("Featured media or OG image failed public verification "+str(pid))

def main():
    binary_files=extract_bundle()
    preflight=[]
    for item in CFG["items"]:
        original=bridge(item["id"])
        wp=public_post(item["id"])
        check_original(item,original,wp)
        preflight.append((item,original))
        print("POST_PREFLIGHT_OK",item["id"],wp["link"],flush=True)
    print("ALL_IMAGE_AND_POST_PREFLIGHTS_PASSED",len(preflight),flush=True)
    for item,orig in preflight:
        # Reconfirm no concurrent changes to the original article before mutation.
        now=bridge(item["id"])
        if now.get("modified_gmt")!=orig.get("modified_gmt") or now.get("content")!=orig.get("content"):
            raise RuntimeError("Concurrent article update; stop before touching "+str(item["id"]))
        update_one(item,binary_files[item["file"]],orig)
    print("ALL_TEN_IMAGES_UPLOADED_ASSIGNED_AND_VERIFIED",flush=True)

if __name__=="__main__":
    main()
