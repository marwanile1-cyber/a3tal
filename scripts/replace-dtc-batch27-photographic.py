#!/usr/bin/env python3
"""Guarded, source-pinned batch27 photo-only replacement via A3tal Direct Bridge.

Phases: validate -> prepare -> apply. Production writes run only after an
encrypted backup artifact exists. No post content, slug, permalink or canonical
edits, no publication of extra codes, and no replay of ambiguous writes.
"""
import argparse,base64,hashlib,io,json,os,re,time,urllib.error,urllib.parse,urllib.request,zipfile
from pathlib import Path
from PIL import Image

SITE="https://a3tal.com"
ROOT=Path(__file__).resolve().parent.parent
ZIP=ROOT/"assets/dtc-batch27-photographic.zip"
EXPECTED_ZIP_SHA="17fed09e399164dae0293fe8f035aa5d76e2b56aae6517114479328ecbeeea73"
CODES="P0261 P0327 P0571 U0125 U0132 U0141 C0044 C0046 B1213 B1232".split()
KEY=os.getenv("A3TAL_API_KEY","")
last_call=0
TRANSIENT=(408,429,500,502,503,504,520,521,522,523,524,525,526)

def checksum(b):return hashlib.sha256(b).hexdigest()
def validate_package():
    if not ZIP.is_file() or checksum(ZIP.read_bytes())!=EXPECTED_ZIP_SHA:
        raise RuntimeError("Approved photorealistic image ZIP not in GitHub or checksum differs; stop without site changes")
    with zipfile.ZipFile(ZIP) as z:
        if len(z.namelist())!=11 or len(set(z.namelist()))!=11:raise RuntimeError("ZIP must hold exactly ten WebPs and manifest")
        m=json.loads(z.read("manifest.json"))
        if m["batch"]!=27 or len(m["files"])!=10 or {r["code"] for r in m["files"]}!=set(CODES):
            raise RuntimeError("Unexpected code roster in manifest")
        seen=set();images={}
        for r in m["files"]:
            code=r["code"];name=f"a3tal-dtc-{code.lower()}-photographic.webp"
            if r["filename"]!=name or r.get("image_origin")!="original_ai_photorealistic":
                raise RuntimeError("Wrong photographic origin or name for "+code)
            raw=z.read(name)
            if len(raw)!=r["bytes"] or checksum(raw)!=r["sha256"] or not 25000<len(raw)<500000:
                raise RuntimeError("Corrupt or unexpected photo for "+code)
            with Image.open(io.BytesIO(raw)) as im:
                if im.format!="WEBP" or im.size!=(1600,900):raise RuntimeError("Invalid 1600x900 WebP "+code)
                im.verify()
            if r["sha256"] in seen:raise RuntimeError("Duplicated photo content")
            seen.add(r["sha256"]);images[code]=raw
        return images

def read(url):
    for n in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"A3tal-Reviewed-Photo-Restore/1.0","Accept":"application/json","Cache-Control":"no-cache"})
            with urllib.request.urlopen(req,timeout=45) as res:return json.load(res)
        except urllib.error.HTTPError as e:
            if n==2 or e.code not in TRANSIENT:raise
        except (TimeoutError,urllib.error.URLError):
            if n==2:raise
        time.sleep(22*(n+1))

def post(code):
    args=urllib.parse.urlencode({"slug":code.lower(),"_fields":"id,slug,status,title,featured_media,yoast_head_json,link"})
    rows=read(SITE+"/wp-json/wp/v2/a3tal-dtc?"+args)
    found=[r for r in rows if r.get("slug")==code.lower() and r.get("status")=="publish"]
    if len(found)!=1:raise RuntimeError("Published code not unique: "+code)
    return found[0]

def medium(mid):
    return read(SITE+"/wp-json/wp/v2/media/"+str(mid)+"?_fields=id,source_url,mime_type")
def og(post):
    return [r.get("url","") for r in post.get("yoast_head_json",{}).get("og_image",[]) if isinstance(r,dict)]
def candidates(code):
    name="a3tal-dtc-"+code.lower()+"-photographic"
    args=urllib.parse.urlencode({"search":name,"per_page":30,"_fields":"id,source_url,mime_type"})
    result=read(SITE+"/wp-json/wp/v2/media?"+args)
    return [r for r in result if r.get("mime_type")=="image/webp"
            and re.search(r"/"+re.escape(name)+r"(?:-\d+)?\.webp$",r.get("source_url",""))]

def bridge(endpoint,payload):
    global last_call
    if not KEY:raise RuntimeError("Bridge secret missing; no website writes")
    time.sleep(max(0,23-(time.monotonic()-last_call)));last_call=time.monotonic()
    body=json.dumps(payload,ensure_ascii=False).encode()
    req=urllib.request.Request(SITE+"/wp-json/a3tal-direct/v1"+endpoint,data=body,headers={
        "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,
        "Content-Type":"application/json","Accept":"application/json","Cache-Control":"no-store",
        "User-Agent":"A3tal-Reviewed-Photo-Restore/1.0"})
    # One shot. On missing HTTP response, abort; the next run resolves
    # already-uploaded media by exact filename instead of repeating upload.
    with urllib.request.urlopen(req,timeout=90) as res:return json.load(res)

def admin(op,**fields):
    obj=bridge("/admin",{"op":op,**fields})
    if not isinstance(obj,dict) or obj.get("ok") is not True:
        raise RuntimeError("Bridge operation rejected: "+op)
    return obj["result"]

def prepare(snapshot):
    validate_package()
    rows=[]
    for code in CODES:
        p=post(code);mid=int(p.get("featured_media") or 0)
        if not mid:raise RuntimeError("Cannot preserve original image: "+code)
        md=medium(mid)
        src=md.get("source_url","")
        if not any(k in src for k in (f"a3tal-dtc-{code.lower()}-exclusive",f"a3tal-dtc-{code.lower()}-photographic")):
            raise RuntimeError("Unexpected editor-supplied cover; never overwrite "+code)
        rows.append({"code":code,"post_id":int(p["id"]),"slug":p["slug"],"title":p["title"]["rendered"],
                     "featured_media":mid,"source_url":src,"og_image":og(p)})
        print("SNAPSHOT",code,mid,flush=True)
    snapshot.parent.mkdir(parents=True,exist_ok=True)
    snapshot.write_text(json.dumps({"zip_sha256":EXPECTED_ZIP_SHA,"posts":rows},ensure_ascii=False,indent=2))
    print("PREPARED_SAFE_ROLLBACK",len(rows),flush=True)

def apply(snapshot):
    photos=validate_package()
    if not KEY:raise RuntimeError("Bridge secret missing")
    state=json.loads(snapshot.read_text())
    if state.get("zip_sha256")!=EXPECTED_ZIP_SHA or [r["code"] for r in state.get("posts",[])]!=CODES:
        raise RuntimeError("Encrypted backup preflight/state not matched")
    for row in state["posts"]:
        code=row["code"];p=post(code);post_id=int(p["id"])
        if post_id!=row["post_id"] or p["slug"]!=row["slug"]:
            raise RuntimeError("Page changed identity: "+code)
        current=int(p.get("featured_media") or 0)
        md=medium(current)
        target=f"a3tal-dtc-{code.lower()}-photographic"
        if target in md.get("source_url",""):
            selected=current
            print("PHOTO_ALREADY_ASSIGNED",code,flush=True)
        else:
            if current!=row["featured_media"]:
                raise RuntimeError("Someone edited featured media since preflight: "+code)
            matches=candidates(code)
            if len(matches)>1:raise RuntimeError("Multiple previously uploaded candidates: "+code)
            if matches:
                selected=int(matches[0]["id"])
                print("RESUME_EXISTING_UPLOAD",code,selected,flush=True)
            else:
                upl=bridge("/upload-image-data",{"post_id":post_id,"filename":target+".webp",
                    "title":"أعطال.كوم | "+code+" | مشهد تشخيص فوتوغرافي",
                    "alt":"مشهد فوتوغرافي مولّد للذكاء الاصطناعي لتشخيص كود "+code,
                    "image_base64":base64.b64encode(photos[code]).decode(),"convert_webp":False})
                selected=int(upl["media_id"])
                if not selected:raise RuntimeError("Upload ID missing: "+code)
                print("UPLOADED",code,selected,flush=True)
            updated=bridge("/set-featured-image",{"post_id":post_id,"media_id":selected})
            if int(updated.get("featured_media") or 0)!=selected:
                raise RuntimeError("Cannot verify new featured image: "+code)
            print("FEATURED_REPLACED",code,current,selected,flush=True)
        newurl=medium(selected).get("source_url","")
        if target not in newurl:raise RuntimeError("Media origin mismatch: "+code)
        if newurl not in og(p):
            admin("post_meta_set",post_id=post_id,meta={
                "_yoast_wpseo_opengraph-image":newurl,"_yoast_wpseo_opengraph-image-id":str(selected),
                "_yoast_wpseo_twitter-image":newurl,"_yoast_wpseo_twitter-image-id":str(selected)})
            # Prompt WordPress/Yoast to rebuild the indexable without altering content or slug.
            admin("platform_entity_upsert",type="a3_dtc",id=post_id,title=row["title"],status="publish")
        for attempt in range(4):
            updated=post(code)
            if int(updated.get("featured_media") or 0)==selected and newurl in og(updated):
                print("LIVE_VERIFIED_FEATURED_AND_OG",code,updated["link"],flush=True)
                break
            if attempt==3:raise RuntimeError("Featured/OG has not converged: "+code)
            time.sleep(30)
    print("ALL_10_PHOTOS_AND_OG_VERIFIED",flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("phase",choices=["validate","prepare","apply"])
    parser.add_argument("--state",type=Path,default=Path(".dtc-photo-rollback.json"))
    x=parser.parse_args()
    if x.phase=="validate":validate_package();print("CHECKSUMS_AND_IMAGES_VALIDATED")
    elif x.phase=="prepare":prepare(x.state)
    else:apply(x.state)
