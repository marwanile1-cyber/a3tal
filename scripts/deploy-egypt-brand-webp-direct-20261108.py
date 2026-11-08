#!/usr/bin/env python3
"""Publish direct WebP car-brand marks to WordPress, then update only Egypt homepage brand cards.

The emblems derive from the repository's existing pinned, user-facing automobile logo
dataset. No external logos, generated marks, new article URLs, or content edits.
"""
import os, re, json, time, hashlib, base64, io, types
from pathlib import Path
from importlib.machinery import SourceFileLoader
import requests
from PIL import Image

BASE="https://a3tal.com"
MEDIA=BASE+"/wp-content/uploads/2026/11/"
ROOT=Path("theme-source/a3tal-global")
REPORT=Path("reports/egypt-brand-real-webp-20261108")
REPORT.mkdir(parents=True,exist_ok=True)
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise SystemExit("A3tal Bridge key unavailable")
m=types.ModuleType("a3tal_media_bridge")
SourceFileLoader(m.__name__,"scripts/deploy-dtc-library.py").exec_module(m)
Bridge=m.Bridge
NAME="home-reference-20261104.php"
BEGIN="<!-- A3TAL-EGYPT-BRANDS-20261108-BEGIN -->"
END="<!-- A3TAL-EGYPT-HOME-PRICES-20261108-BEGIN -->"
BRANDS={
"toyota":"Toyota","hyundai":"Hyundai","chevrolet":"Chevrolet","kia":"Kia",
"nissan":"Nissan","mg":"MG","chery":"Chery","geely":"Geely",
"jetour":"Jetour","jaecoo":"Jaecoo","byd":"BYD","renault":"Renault",
"opel":"Opel","suzuki":"Suzuki","skoda":"Skoda","changan":"Changan",
"haval":"Haval","gac":"GAC","deepal":"Changan Deepal",
"dongfeng":"Dongfeng","baic":"BAIC","kgm":"KGM","ford":"Ford"
}
def sha(s):return hashlib.sha256(s.encode("utf-8")).hexdigest()
def source_data():
    data=(ROOT/"assets/js/dtc-brand-logos.generated.js").read_text("utf-8")
    needle="Object.freeze("
    if data.count(needle)!=1:raise RuntimeError("Pinned logo library changed unexpectedly")
    blob=data[data.index(needle)+len(needle):data.rfind(")")]
    logos=json.loads(blob)
    if not all(logos.get(k,"").startswith("data:image/webp;base64,") for k in BRANDS.values()):
        raise RuntimeError("Missing one of the 23 audited logos")
    return logos
def webp_thumbnail(raw):
    im=Image.open(io.BytesIO(raw))
    im.seek(0);im=im.convert("RGBA");im.thumbnail((200,88),Image.Resampling.LANCZOS)
    out=io.BytesIO();im.save(out,format="WEBP",quality=86,method=6)
    result=out.getvalue()
    if result[:4]!=b"RIFF" or result[8:12]!=b"WEBP" or len(result)>30000:
        raise RuntimeError("Logo optimization produced invalid WebP")
    return result
session=requests.Session()
session.headers.update({"User-Agent":"Mozilla/5.0 (A3tal Brand Logos/1.0)"})
def get_image(url):
    r=session.get(url,timeout=35,headers={"Cache-Control":"no-cache"})
    if r.status_code==200:
        if r.content[:4]!=b"RIFF" or r.content[8:12]!=b"WEBP":
            raise RuntimeError("Existing media has wrong content type: "+url)
        return r.content
    if r.status_code in (404,410):return None
    raise RuntimeError("Media public read HTTP "+str(r.status_code))
def upload_all():
    pool=source_data()
    summary=[]
    for i,(slug,key) in enumerate(BRANDS.items(),1):
        raw=base64.b64decode(pool[key].split(",",1)[1])
        body=webp_thumbnail(raw)
        filename="a3tal-egypt-brand-emblem-20261108-"+slug+".webp"
        url=MEDIA+filename
        current=get_image(url)
        if current is not None:
            if hashlib.sha256(current).digest()!=hashlib.sha256(body).digest():
                raise RuntimeError("Existing logo filename differs; no overwrite: "+slug)
            state="already_verified"
        else:
            payload={"filename":filename,"image_base64":base64.b64encode(body).decode(),
                "convert_webp":False,"title":"شعار سيارات "+key+" - أعطال مصر",
                "alt":"شعار سيارات "+key}
            r=session.post(BASE+"/wp-json/a3tal-direct/v1/upload-image-data",
                headers={"X-A3tal-Key":KEY,"Content-Type":"application/json"},
                json=payload,timeout=75)
            if r.status_code not in (200,201):
                check=get_image(url)
                if check is None or hashlib.sha256(check).digest()!=hashlib.sha256(body).digest():
                    raise RuntimeError("Media upload failed HTTP "+str(r.status_code)+": "+slug)
            else:
                result=r.json()
                if str(result.get("url",""))!=url:
                    raise RuntimeError("Unexpected WordPress uploaded media URL: "+slug)
            state="uploaded"
        check=get_image(url)
        if check is None or hashlib.sha256(check).digest()!=hashlib.sha256(body).digest():
            raise RuntimeError("Published logo mismatch: "+slug)
        summary.append({"slug":slug,"media":url,"bytes":len(body),"state":state})
        print("LIVE_REAL_BRAND_WEBP",i,len(BRANDS),slug,state,flush=True)
        time.sleep(0.75)
    (REPORT/"images.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),"utf-8")
    return summary
def patch_template(old):
    src=(ROOT/NAME).read_text("utf-8")
    for text in (old,src):
        if text.count(BEGIN)!=1 or text.count(END)!=1:
            raise RuntimeError("Egypt homepage audited brand markers missing or duplicated")
    desired=src[src.index(BEGIN):src.index(END)]
    before=old[old.index(BEGIN):old.index(END)]
    if desired.count('class="a3egy-brand has-brand-logo"')!=23:
        raise RuntimeError("Source must embed exactly 23 direct WebP badges")
    if before==desired:return old
    if before.count('class="a3egy-brand"')!=24:
        raise RuntimeError("Current live homepage brand layout changed independently")
    result=old.replace(before,desired,1)
    if "a3tal-egypt-brand-emblem-20261108-toyota.webp" not in result:
        raise RuntimeError("Branded model links missing")
    return result
def verify_public():
    for retry in range(5):
        try:
            r=session.get(BASE+"/?a3tal_real_webp_logo_verify="+str(time.time_ns()),timeout=55)
            html=r.text
            summary={"http":r.status_code,
                     "images":html.count("a3tal-egypt-brand-emblem-20261108-"),
                     "priced":'id="egypt-car-prices"' in html,
                     "pseo":'id="egypt-pseo"' in html}
            if r.status_code==200 and summary["images"]>=23 and summary["priced"] and summary["pseo"]:
                (REPORT/"public-qa.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),"utf-8")
                print("LIVE_EGYPT_BRAND_IMAGES_PRICES_PSEO_VERIFIED",json.dumps(summary),flush=True)
                return
        except requests.RequestException as exc:
            summary={"error":type(exc).__name__}
        print("PUBLIC_MEDIA_QA_RETRY",retry+1,summary,flush=True)
        time.sleep(6)
    raise RuntimeError("Real WebP brand badges not visible in public HTML")
def main():
    logos=upload_all()
    bridge=Bridge()
    before=bridge.read(NAME)
    revised=patch_template(before["content"])
    (REPORT/"homepage-before.txt").write_text(before["content"],"utf-8")
    if revised==before["content"]:print("DIRECT_LOGOS_ALREADY_LIVE",flush=True)
    else:
        try:
            bridge.write(NAME,revised,before["sha256"])
            bridge.flush()
            verify_public()
        except Exception:
            print("DIRECT_LOGO_QA_FAILED_SCOPED_ROLLBACK",flush=True)
            try:
                bridge.write(NAME,before["content"],sha(revised))
                bridge.flush()
                print("ROLLED_BACK_HOMEPAGE_ONLY",flush=True)
            except Exception as exc:
                print("MANUAL_REVIEW_REQUIRED",type(exc).__name__,flush=True)
            raise
    if revised==before["content"]:verify_public()
    print("SUCCESS_23_BRAND_IMAGES_DIRECT_WEBP_EGYPT",flush=True)
if __name__=="__main__":main()
