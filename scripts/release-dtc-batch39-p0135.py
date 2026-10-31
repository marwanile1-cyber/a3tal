#!/usr/bin/env python3
"""Owner-authorized one-time A3tal batch39 release. No duplicate pages, no blind write retries.
The source images are explicitly TEMPORARY: never describe them as newly exclusive.
"""
import base64,hashlib,html,io,json,os,time,urllib.parse,urllib.request,urllib.error,zipfile
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance
ROOT=Path(__file__).resolve().parents[1]
SITE="https://a3tal.com"
BRIDGE=SITE+"/wp-json/a3tal-direct/v1"
FILE=ROOT/"data/dtc-batch39-p0135-20261031.json"
ZIP=ROOT/"assets/dtc-batch27-photographic.zip"
CODES="P0135".split()
SOURCE="P0135".split()
KEY=os.getenv("A3TAL_API_KEY","")
LAST=0.0
def log(*a): print("BATCH39",*a,flush=True)
def pause():
 global LAST
 time.sleep(max(0,12-(time.monotonic()-LAST)))
 LAST=time.monotonic()
def read(url):
 req=urllib.request.Request(url,headers={"User-Agent":"A3tal-OwnerBatch39/1.0","Accept":"application/json","Cache-Control":"no-store"})
 for attempt in range(3):
  try:
   with urllib.request.urlopen(req,timeout=55) as r:return json.load(r)
  except urllib.error.HTTPError as e:
   if attempt==2 or e.code not in (408,429,500,502,503,504,520,522,524): raise
  except (TimeoutError,urllib.error.URLError):
   if attempt==2:raise
  time.sleep(22*(attempt+1))
def post(code):
 q=urllib.parse.urlencode({"slug":code.lower(),"per_page":2,"_fields":"id,slug,status,featured_media,yoast_head_json,link,title"})
 rows=read(SITE+"/wp-json/wp/v2/a3tal-dtc?"+q)
 if not isinstance(rows,list):raise RuntimeError("Bad public REST listing "+code)
 found=[x for x in rows if x.get("slug")==code.lower()]
 if len(found)>1:raise RuntimeError("Duplicate DTC code: "+code)
 return found[0] if found else None
def media(mid):
 return read(SITE+"/wp-json/wp/v2/media/"+str(mid)+"?_fields=id,source_url,mime_type")
def matches(code):
 name="a3tal-dtc-"+code.lower()+"-batch39-original-ar"
 q=urllib.parse.urlencode({"search":name,"per_page":30,"_fields":"id,source_url,mime_type"})
 return [x for x in read(SITE+"/wp-json/wp/v2/media?"+q) if name in x.get("source_url","") and x.get("mime_type")=="image/webp"]
def request(endpoint,data):
 if not KEY:raise RuntimeError("A3TAL_API_KEY unavailable")
 pause()
 req=urllib.request.Request(BRIDGE+endpoint,data=json.dumps(data,ensure_ascii=False).encode("utf8"),
  headers={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json",
           "Accept":"application/json","User-Agent":"A3tal-OwnerBatch39/1.0","Cache-Control":"no-store"},method="POST")
 with urllib.request.urlopen(req,timeout=110) as r:return json.load(r)
def admin(**data):
 r=request("/admin",data)
 if r.get("ok") is not True or "result" not in r:raise RuntimeError("Bridge admin rejected")
 return r["result"]
def photos():
 import subprocess,sys
 subprocess.run([sys.executable,str(ROOT/"scripts/render-dtc-batch39-p0135-infographic.py")],cwd=ROOT,check=True)
 path=ROOT/"assets/dtc-batch39/a3tal-dtc-p0135-original-ar.webp"
 raw=path.read_bytes()
 from PIL import Image
 with Image.open(path) as image:
  if image.format!="WEBP" or image.size!=(1600,900):raise RuntimeError("Image invalid")
 if not (25000<len(raw)<950000):raise RuntimeError("Unexpected image size")
 log("ORIGINAL_CUSTOM_IMAGE_STAGED","P0135",len(raw))
 return {"P0135":raw}
def validate():
 data=json.loads(FILE.read_text(encoding="utf8"))
 rows=data.get("items",[])
 if data.get("batch")!=39 or [r.get("code") for r in rows]!=CODES:
  raise RuntimeError("Batch37 roster/sequence differs from reviewed plan")
 if any(r.get("slug")!=r["code"].lower() or r.get("word_count",0)<1500 or
        not r.get("content","").startswith("<p>") or
        not r.get("source","").startswith("https://") or
        r.get("media_status")!="awaiting_exclusive_infographic" for r in rows):
  raise RuntimeError("Incomplete editorial content or unsupported status")
 for r in rows:
  actual=len(__import__("re").sub(r"<[^>]+>"," ",r["content"]).split())
  if actual<1500 or actual!=int(r["word_count"]):raise RuntimeError("Original article under 1500 or count inconsistent: "+r["code"])
  if r.get("qa",{}).get("ready_for_publication") is not True:raise RuntimeError("Manuscript review pending: "+r["code"])
  if len(r.get("content",""))<8000:raise RuntimeError("Suspiciously short body: "+r["code"])
  log("EDITORIAL_VALID",r["code"],actual,"words")
 return rows
def ensure_images(images):
 # Only attach interim images to the posts created or confirmed as this exact batch.
 for code in CODES:
  row=post(code)
  if not row or row.get("status")!="publish":raise RuntimeError("Post not live for image "+code)
  mid=int(row.get("featured_media") or 0)
  target="a3tal-dtc-"+code.lower()+"-batch39-original-ar"
  if mid:
   current=media(mid);url=current.get("source_url","")
   if target not in url:
    # An editor may have already supplied a BETTER final photo; do not overwrite it.
    log("EDITOR_FEATURED_PRESERVED",code,mid,url)
    continue
  else:
   candidates=matches(code)
   if len(candidates)>1:raise RuntimeError("Ambiguous prior image upload "+code)
   if candidates:
    mid=int(candidates[0]["id"]);log("RECOVER_MEDIA",code,mid)
   else:
    log("UPLOADING_INTERIM",code)
    uploaded=request("/upload-image-data",{"post_id":int(row["id"]),"filename":target+".webp",
      "title":"أعطال.كوم | "+code+" | شكل حساس الأكسجين وأعراض العطل","alt":"كود P0135 خلل دائرة سخان حساس الأكسجين الأمامي B1S1 مع رسم توضيحي لشكل الحساس",
      "image_base64":base64.b64encode(images[code]).decode(),"convert_webp":False})
    mid=int(uploaded.get("media_id") or 0)
    if not mid:raise RuntimeError("Upload response missing media id "+code)
   changed=request("/set-featured-image",{"post_id":int(row["id"]),"media_id":mid})
   if int(changed.get("featured_media") or 0)!=mid:raise RuntimeError("Featured image write mismatch "+code)
  source=media(mid).get("source_url","")
  if not source.endswith(".webp"):raise RuntimeError("Featured image not WebP "+code)
  observed=[x.get("url") for x in (post(code).get("yoast_head_json") or {}).get("og_image",[]) if isinstance(x,dict)]
  if source not in observed:
   admin(op="post_meta_set",post_id=int(row["id"]),meta={
    "_yoast_wpseo_opengraph-image":source,"_yoast_wpseo_opengraph-image-id":str(mid),
    "_yoast_wpseo_twitter-image":source,"_yoast_wpseo_twitter-image-id":str(mid)})
   admin(op="platform_entity_upsert",type="a3_dtc",id=int(row["id"]),
         title=html.unescape(row["title"]["rendered"]),status="publish")
  if source not in [x.get("url") for x in (post(code).get("yoast_head_json") or {}).get("og_image",[]) if isinstance(x,dict)]:
   raise RuntimeError("Open Graph image not verified for "+code)
  log("LIVE_FEATURED_AND_OG_VERIFIED",code,source)
def verify_previous_release():
 previous="P0361 P0362 P0363 P0486 P0487 P0488 P0764 P0766 P0767 P0768".split()
 for code in previous:
  row=post(code)
  if not row or row.get("status")!="publish":
   raise RuntimeError("Previous batch37 article missing: "+code)
  mid=int(row.get("featured_media") or 0)
  if not mid:
   raise RuntimeError("Previous batch37 image absent: "+code)
  src=media(mid).get("source_url","")
  images=[x.get("url","") for x in (row.get("yoast_head_json") or {}).get("og_image",[]) if isinstance(x,dict)]
  if not src or src not in images:
   raise RuntimeError("Previous batch37 og:image mismatch: "+code)
 log("PREVIOUS_BATCH36_ALL_TEN_FEATURED_OG_CONFIRMED")

def main():
 if os.getenv("A3TAL_BATCH39_RELEASE")!="1":raise RuntimeError("Batch37 explicit manual release flag missing")
 if not KEY:raise RuntimeError("Bridge secret missing")
 rows=validate()
 verify_previous_release()
 images=photos()
 prior=[post(c) for c in CODES]
 if any(p and p.get("status")!="publish" for p in prior):raise RuntimeError("Existing nonpublic article; stop")
 count=sum(p is not None for p in prior)
 if any(p is None for p in prior[:count]) or any(p is not None for p in prior[count:]):
  raise RuntimeError("Noncontiguous live batch - human review needed")
 info=admin(op="site_info")
 if info.get("active_theme")!="a3tal-global":raise RuntimeError("Unexpected theme; no writes")
 for row in rows[count:]:
  code=row["code"]
  # Recheck immediately before each mutation. A lost write must NEVER be retried blindly.
  current=post(code)
  if current:raise RuntimeError("Preexisting page appeared during publication: "+code)
  content=row["content"]+"\n<p><em>الصورة البارزة تصميم أصلي توضيحي لشكل حساس الأكسجين، والكود لا يثبت أن الحساس نفسه تالف.</em></p>"
  entity={"op":"platform_entity_upsert","type":"a3_dtc","slug":code.lower(),"title":row["title"],
   "status":"publish","excerpt":row["excerpt"],"content":content,
   "meta":{"_a3_dtc_code":code,"_a3_dtc_system":row["system"],
           "_a3_code_scope":row["scope"],"_a3_source_url":row["source"],
           "_a3_source_checked_at":"2026-10-31",
           "_a3_dtc_batch":"A3TAL-DTC-2026-10-31-39"}}
  log("PUBLISH_ATTEMPT",code)
  try:res=admin(**entity)
  except Exception as exc:
   check=post(code)
   if check and check.get("status")=="publish":
    log("RECOVERED_AFTER_AMBIGUOUS_WRITE",code,check["id"])
    continue
   raise RuntimeError("Unconfirmed write: stop rather than retry "+code) from exc
  if res.get("slug")!=code.lower() or int(res.get("id") or 0)<=0:
   raise RuntimeError("Unexpected result identity "+code)
  log("POST_WRITTEN",code,res.get("link"),res["id"])
 verified=[post(code) for code in CODES]
 if any(not x or x.get("status")!="publish" for x in verified):
  raise RuntimeError("Missing live posts; stop before images")
 log("P0135_ARTICLE_LIVE")
 ensure_images(images)
 for code in CODES:
  p=post(code)
  if not p or p.get("status")!="publish" or not int(p.get("featured_media") or 0) or not (p.get("yoast_head_json") or {}).get("og_image"):
   raise RuntimeError("Final publication not verified for "+code)
  log("FINAL_URL","https://a3tal.com/dtc/"+code.lower()+"/")
 log("BATCH39_P0135_PUBLISHED_WITH_ORIGINAL_INFOGRAPHIC_AND_OG")
if __name__=="__main__":main()
