#!/usr/bin/env python3
"""Publish four manually researched non-DTC features via the approved A3tal Direct Bridge."""
import os,json,base64,io,time,urllib.parse,urllib.request,urllib.error,html,re
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
DATA=Path("data/editorial-oct-15-2026.json")
CAT={"أسعار السيارات الجديدة":374,"مقارنات السيارات":21,"أعطال الفرامل والعفشة":10,"صيانة الموتوسيكلات":3028}
if not KEY:raise SystemExit("A3TAL_API_KEY secret unavailable")

def request(url,body=None,auth=True,retries=3):
    url=url if url.startswith("https://") else API+url
    headers={"User-Agent":"A3talEditorialBatch/2026-10-15","Accept":"application/json,text/html,image/*,*/*"}
    if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=None if body is None else json.dumps(body,ensure_ascii=False).encode("utf-8")
    if data is not None:headers["Content-Type"]="application/json"
    n=retries if data is None else 1
    for attempt in range(n):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=headers),timeout=140) as response:
                raw=response.read()
                return json.loads(raw) if auth else raw
        except Exception as ex:
            if attempt==n-1:raise
            print("READ_RETRY",url[:85],type(ex).__name__,str(ex)[:130],flush=True)
            time.sleep(4*(attempt+1))

def image_from_url(url,width=1600,height=900):
    raw=request(url,auth=False)
    im=Image.open(io.BytesIO(raw))
    im.load()
    if im.width<700 or im.height<450:
        raise RuntimeError("Not a real high resolution source photo: "+url+" "+str(im.size))
    if im.width/max(im.height,1)>3.5 or im.height/max(im.width,1)>2.8:
        raise RuntimeError("Inappropriate image aspect ratio: "+url)
    return ImageOps.fit(im.convert("RGB"),(width,height),method=Image.Resampling.LANCZOS,centering=(.50,.52))

def cover(entry):
    sources=entry["image_sources"]
    images=[image_from_url(u) for u in sources]
    if len(images)==2:
        # Distinct original 16:9 split editorial presentation, not reused from another page.
        dest=Image.new("RGB",(1600,900))
        for idx,img in enumerate(images):
            half=ImageOps.fit(img,(800,900),method=Image.Resampling.LANCZOS,centering=(.5,.5))
            dest.paste(half,(idx*800,0))
        images=[dest]
    if len(images)!=1:raise RuntimeError("Wrong number of photo sources")
    img=ImageEnhance.Contrast(images[0]).enhance(1.045)
    buf=io.BytesIO();img.save(buf,"WEBP",quality=85,method=6)
    raw=buf.getvalue()
    if not 25000<len(raw)<2400000:raise RuntimeError("Image output validation failed")
    name="a3tal-editorial-"+entry["slug"]+".webp"
    print("COVER_READY",name,len(raw),flush=True)
    return {"filename":name,"title":entry["image_alt"],"alt":entry["image_alt"],"role":"featured","convert_webp":False,"image_base64":base64.b64encode(raw).decode("ascii")}

def published_slug(slug):
    p=SITE+"/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":slug,"per_page":2,"_fields":"id,status,slug,link,featured_media,yoast_head_json"})
    rows=json.loads(request(p,auth=False))
    if len(rows)>1:raise RuntimeError("Duplicate slug: "+slug)
    return rows[0] if rows else None

def verify_link(link,slug,featured_id):
    for delay in (0,8,14,24):
        if delay:time.sleep(delay)
        try:
            public=request(link+"?a3tal_verify="+str(int(time.time())),auth=False,retries=1).decode("utf-8","replace")
            if not ("og:image" in public and "a3tal-editorial-"+slug in public and "noindex" not in public.lower()):
                raise RuntimeError("Missing intended cover og:image or page is noindexed")
            row=published_slug(slug)
            if not row or row.get("status")!="publish" or int(row.get("featured_media") or 0)!=int(featured_id):
                raise RuntimeError("WordPress public REST post status or cover mismatch")
            print("PUBLIC_VERIFIED",link,"featured",featured_id,flush=True)
            return
        except Exception as e:print("VERIFY_RETRY",link,str(e)[:180],flush=True)
    raise RuntimeError("Post live but public photo verification failed: "+link)

def main():
    batch=json.loads(DATA.read_text(encoding="utf-8"))
    st=request("/status")
    if not st.get("ok"):raise RuntimeError("Direct bridge is not responding")
    print("BRIDGE_VERSION",st.get("version"),flush=True)
    results=[]
    for index,item in enumerate(batch["items"],1):
        print("START_ARTICLE",index,item["title"],flush=True)
        category=CAT.get(item["section"])
        if not category:raise RuntimeError("No verified category assigned")
        old=published_slug(item["slug"])
        if old and old.get("status")=="publish" and old.get("featured_media"):
            verify_link(old["link"],item["slug"],old["featured_media"])
            results.append({"title":item["title"],"link":old["link"],"section":item["section"],"already":True})
            continue
        # Do not create topic if close-intent title is found already; use slug as strict idempotency.
        found=request("/search-posts?"+urllib.parse.urlencode({"search":item["focus"],"limit":60,"status":"any"})).get("items",[])
        for p in found:
            if p.get("slug")!=item["slug"] and (p.get("title","").strip()==item["title"].strip()):
                raise RuntimeError("Duplicate editorial title exists: "+p["title"])
        media=cover(item)
        post={"title":item["title"],"slug":item["slug"],"type":"post","status":"publish","excerpt":item["excerpt"],
          "content":item["html"],"categories":[category],
          "meta":{"_yoast_wpseo_title":item["title"],"_yoast_wpseo_metadesc":item["meta"],
                  "_yoast_wpseo_focuskw":item["focus"],"_yoast_wpseo_canonical":SITE+"/"+item["slug"]+"/",
                  "_yoast_wpseo_opengraph-title":item["title"],"_yoast_wpseo_opengraph-description":item["meta"]}}
        if old:post["id"]=old["id"]
        try:response=request("/publish-bundle",{"post":post,"media":[media]})
        except Exception as e:
            print("AMBIGUOUS_PUBLISH_DO_NOT_RETRY",item["slug"],str(e)[:240],flush=True)
            raise
        result=response.get("post") or {}
        pid=int(result.get("id") or 0)
        featured=int(result.get("featured_media") or 0)
        link=result.get("link") or SITE+"/"+item["slug"]+"/"
        if not response.get("ok") or not pid or not featured or result.get("status")!="publish":
            raise RuntimeError("Not published with featured photo: "+str(response)[:500])
        detail=request("/post/"+str(pid))
        if detail.get("status")!="publish" or int(detail.get("featured_media") or 0)!=featured:
            raise RuntimeError("Bridge readback mismatch: "+str(pid))
        # Featured image may be placed by the theme. Insert explicitly at article top if API only assigns thumbnail.
        verify_link(link,item["slug"],featured)
        results.append({"title":item["title"],"link":link,"section":item["section"],"already":False})
        print("ARTICLE_SUCCESS",json.dumps(results[-1],ensure_ascii=False),flush=True)
    print("A3TAL_EDITORIAL_RESULTS",json.dumps(results,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
