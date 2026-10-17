#!/usr/bin/env python3
"""One-time guarded release of exactly four missing batch29 articles.

Six confirmed live batch29 pages are never updated, duplicated, or re-published.
Creates temporary clearly-labelled cover images before any WordPress mutation.
No unsafe replay after ambiguous Bridge write.
"""
import base64,hashlib,html,importlib.util,io,json,os,time,urllib.parse,urllib.request,urllib.error,zipfile
from pathlib import Path
from PIL import Image,ImageEnhance,ImageOps
ROOT=Path(__file__).resolve().parent.parent
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
FILE=ROOT/"data/dtc-batch29-completion-4.json"
MISSING="U0154 U0170 C0061 C0062".split()
LIVE="P0316 P0496 P0733 U0163 B1411 B1412".split()
SOURCE={"U0154":"U0141","U0170":"U0125","C0061":"C0044","C0062":"C0046"}
SOURCES_ZIP=ROOT/"assets/dtc-batch27-photographic.zip"
DELAY=23
last=0.0
def paced():
    global last
    time.sleep(max(0,DELAY-(time.monotonic()-last)))
    last=time.monotonic()
def public(code):
    q=urllib.parse.urlencode({"slug":code.lower(),"_fields":"id,slug,status,link,featured_media,yoast_head_json,title"})
    req=urllib.request.Request(SITE+"/wp-json/wp/v2/a3tal-dtc?"+q,headers={"User-Agent":"A3tal-Batch29-SafeRelease/1.0","Accept":"application/json","Cache-Control":"no-cache"})
    for i in range(4):
        try:
            with urllib.request.urlopen(req,timeout=45) as r:d=json.load(r)
            matches=[x for x in d if x.get("slug")==code.lower()]
            if len(matches)>1:raise RuntimeError("Duplicate code "+code)
            return matches[0] if matches else None
        except urllib.error.HTTPError as e:
            if i==3 or e.code not in (408,429,500,502,503,504,520,522,524):raise
        except (TimeoutError,urllib.error.URLError):
            if i==3:raise
        time.sleep(18*(i+1))
def api(endpoint,obj):
    if not KEY:raise RuntimeError("A3tal Bridge key not configured")
    paced()
    payload=json.dumps(obj,ensure_ascii=False).encode()
    req=urllib.request.Request(API+endpoint,data=payload,headers={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,
      "Content-Type":"application/json","Accept":"application/json","Cache-Control":"no-store","User-Agent":"A3tal-Batch29-SafeRelease/1.0"})
    with urllib.request.urlopen(req,timeout=90) as r:return json.load(r)
def adm(**payload):
    result=api("/admin",payload)
    if result.get("ok") is not True or "result" not in result:raise RuntimeError("Bridge admin response invalid")
    return result["result"]
def covers():
    if not SOURCES_ZIP.is_file():raise RuntimeError("Approved photographic source ZIP missing")
    out={}
    with zipfile.ZipFile(SOURCES_ZIP) as z:
        for i,code in enumerate(MISSING):
            raw=z.read("a3tal-dtc-"+SOURCE[code].lower()+"-photographic.webp")
            with Image.open(io.BytesIO(raw)) as original:
                pic=ImageOps.fit(original.convert("RGB"),(1600,900),method=Image.Resampling.LANCZOS)
            pic=ImageEnhance.Color(pic).enhance(0.93+i*.027)
            pic=ImageEnhance.Contrast(pic).enhance(0.98+i*.019)
            buffer=io.BytesIO();pic.save(buffer,format="WEBP",quality=84,method=6)
            out[code]=buffer.getvalue()
            if not (25000<len(out[code])<500000):raise RuntimeError("Temporary cover size out of range "+code)
            print("BATCH29_PREPARED_TEMP_PHOTO",code,len(out[code]),flush=True)
    return out
def main():
    payload=json.loads(FILE.read_text(encoding="utf-8"))
    rows=payload["items"]
    if [x.get("code") for x in rows]!=MISSING or payload.get("existing_production_codes")!=LIVE:
        raise RuntimeError("Unexpected or modified 29 roster")
    for r in rows:
        if len(r.get("steps",[]))!=5 or len(r.get("deep_dive",[]))!=4 or len(r.get("decision",[]))!=3 or len(r.get("faqs",[]))!=3:raise RuntimeError("Thin guide "+r["code"])
        if len(r.get("intro","").split())<35 or len(r.get("how","").split())<35:raise RuntimeError("Thin intro "+r["code"])
    photos=covers()
    spec=importlib.util.spec_from_file_location("dtc28pub",ROOT/"scripts/publish-dtc-original-batch-28.py")
    lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)
    before={c:public(c) for c in LIVE+MISSING}
    for c in LIVE:
        if not before[c] or before[c].get("status")!="publish":
            raise RuntimeError("Expected six already live batch29 guides: "+c)
    for c in MISSING:
        if before[c] and before[c].get("status")!="publish":
            raise RuntimeError("Existing draft must be reconciled: "+c)
    if not KEY:raise RuntimeError("No Bridge key, no publishing")
    info=adm(op="site_info")
    if info.get("active_theme")!="a3tal-global":raise RuntimeError("Unexpected active theme")
    for r in rows:
        code=r["code"]
        prior=public(code)
        if prior:
            print("BATCH29_ALREADY_LIVE_PRESERVE",code,prior["id"],flush=True)
            continue
        row={**r,"name":r["title"],"summary":r["intro"],"related_codes":r["related"],"video":None}
        body=lib.render(row)
        body+='\n<p><strong>مصدر التحقق الفني:</strong> <a href="'+html.escape(r["source"])+'" target="_blank" rel="noopener noreferrer">الدليل المرجعي للكود</a>. تختلف الإجراءات الدقيقة حسب رقم الهيكل ومواصفات وحدة التحكم.</p>'
        body+='\n<p><em>الصورة المستخدمة مؤقتًا صورة تشخيص عامة مشتقة من أرشيف صور الموقع، وليست تصويرًا خاصًا لقطعة هذا الكود. سيتم استبدالها بصورة مستقلة.</em></p>'
        entity={"op":"platform_entity_upsert","type":"a3_dtc","slug":code.lower(),
          "title":"كود "+code+": "+r["title"]+" | دليل التشخيص والأسباب",
          "status":"publish","excerpt":r["intro"][:245],"content":body,
          "meta":{"_a3_dtc_code":code,"_a3_dtc_system":r["system"],
            "_a3_code_scope":r["scope"],"_a3_drive_advice":r["safety"],
            "_a3_source_url":r["source"],"_a3_source_checked_at":"2026-10-17",
            "_a3_dtc_batch":"A3TAL-DTC-2026-10-17-29-COMPLETE-MISSING-4"}}
        print("BATCH29_PUBLISHING",code,flush=True)
        try:result=adm(**entity)
        except Exception as e:
            print("BATCH29_WRITE_UNCONFIRMED",code,type(e).__name__,flush=True)
            check=public(code)
            if check and check.get("status")=="publish":
                print("BATCH29_RECOVERED_POST",code,check.get("id"),flush=True)
                continue
            raise RuntimeError("Stop after unknown write for "+code) from e
        if result.get("slug")!=code.lower() or int(result.get("id") or 0)<=0:
            raise RuntimeError("Unexpected DTC post identity "+code)
        print("BATCH29_PUBLISHED",code,result.get("id"),result.get("link"),flush=True)
    complete={c:public(c) for c in LIVE+MISSING}
    if any(not complete[c] or complete[c].get("status")!="publish" for c in LIVE+MISSING):
        raise RuntimeError("Not all 10 batch29 guides published; don't touch featured images")
    print("BATCH29_TEN_CONTENT_POSTS_CONFIRMED",flush=True)
    for code in MISSING:
        item=public(code)
        mid=int(item.get("featured_media") or 0)
        if mid:
            print("BATCH29_EXISTING_FEATURED_PRESERVED",code,mid,flush=True)
            continue
        filename="a3tal-dtc-"+code.lower()+"-temporary-photographic.webp"
        upl=api("/upload-image-data",{"post_id":int(item["id"]),"filename":filename,
          "title":"أعطال.كوم "+code+" صورة تشخيص عامة مؤقتة",
          "alt":"صورة ورشة فوتوغرافية توضيحية مؤقتة لكود "+code+" وليست شكل المستشعر الدقيق",
          "image_base64":base64.b64encode(photos[code]).decode(),"convert_webp":False})
        media=int(upl.get("media_id") or 0)
        if media<=0:raise RuntimeError("Media upload failed for "+code)
        changed=api("/set-featured-image",{"post_id":int(item["id"]),"media_id":media})
        if int(changed.get("featured_media") or 0)!=media:raise RuntimeError("Cannot set cover "+code)
        print("BATCH29_FEATURED_IMAGE_SET",code,media,flush=True)
    for code in MISSING:
        post=public(code)
        mid=int(post.get("featured_media") or 0)
        if not mid:raise RuntimeError("Featured image missing "+code)
        url=SITE+"/wp-json/wp/v2/media/"+str(mid)+"?_fields=id,source_url,mime_type"
        req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"A3tal-Batch29-MediaVerify/1.0","Cache-Control":"no-cache"})
        with urllib.request.urlopen(req,timeout=40) as resp:art=json.load(resp)
        source=art.get("source_url","")
        if not source or art.get("mime_type")!="image/webp":raise RuntimeError("Invalid featured image "+code)
        existing=[x.get("url","") for x in post.get("yoast_head_json",{}).get("og_image",[]) if isinstance(x,dict)]
        if source not in existing:
            adm(op="post_meta_set",post_id=int(post["id"]),meta={
               "_yoast_wpseo_opengraph-image":source,"_yoast_wpseo_opengraph-image-id":str(mid),
               "_yoast_wpseo_twitter-image":source,"_yoast_wpseo_twitter-image-id":str(mid)})
            # standard post-save to refresh Yoast indexable without changing content
            adm(op="platform_entity_upsert",type="a3_dtc",id=int(post["id"]),title=html.unescape(post["title"]["rendered"]),status="publish")
        refreshed=public(code)
        if source not in [x.get("url") for x in refreshed.get("yoast_head_json",{}).get("og_image",[]) if isinstance(x,dict)]:
            raise RuntimeError("Yoast OG unverified for "+code)
        print("BATCH29_FEATURED_OG_VERIFIED",code,source,flush=True)
    print("BATCH29_COMPLETE_10_LIVE_ALL_4_NEW_FEATURED_AND_OG_VERIFIED",flush=True)
if __name__=="__main__":main()
