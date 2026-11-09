#!/usr/bin/env python3
"""Replace the disliked vector PSEO covers in batches 34 and 35 with actual
model-matched official Egyptian maker photography. Image-only change.

Never republish a record if it is not the expected published title and path.
Reapply original stored editorial content, protected metadata and canonical
without touching the article's wording, slug, source or hierarchy.
No synthetic car photographs, no made-up mechanical diagrams, no huge labels.
"""
import base64, io, json, os, re, time, traceback
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import requests

ROOT=Path(__file__).resolve().parents[1]
BASE="https://a3tal.com"
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("A3TAL_API_KEY is required")
H={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
S=requests.Session()
S.headers.update({"User-Agent":"A3tal-PSEO-OEM-Photo-Replacement/2026-11-09"})
UPLOAD=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
UPSERT=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
REPORT=ROOT/"reports/batch34-batch35-real-car-photo-replacements.json"
REPORT.parent.mkdir(parents=True,exist_ok=True)
RESULTS=[]
# Each link was observed in the corresponding Egyptian manufacturer's live model gallery.
PHOTO={
 34:[
 "https://www.chery-eg.com/media/ModelsBanner/model_page_banner_copy.jpg",
 "https://www.chery-eg.com/media/extDesignImages/550x300_1.jpg",
 "https://www.chery-eg.com/media/intDesignImages/Interior_main_banner_O1svYTX.jpg",
 "https://www.chery-eg.com/media/extDesignImages/550x300_2_7NwgM6u.jpg",
 "https://www.chery-eg.com/media/extDesignImages/550x300_3_iaSGPeO.jpg",
 ],
 35:[
 "https://cdngeely.cloudhosta.com/exterior_1_be2b7095fb.webp",
 "https://cdngeely.cloudhosta.com/exterior2_1_78a201c84b.webp",
 "https://cdngeely.cloudhosta.com/interior4_1_61631fe144.webp",
 "https://cdngeely.cloudhosta.com/exterior3_1_901226bb4c.webp",
 "https://cdngeely.cloudhosta.com/exterior4_1_4ef24753bc.webp",
 ]
}
INPUT={
 34:("data/car-reference/batch-34-chery-arrizo5-egypt.json","chery","arrizo5-15-dvvt-egypt"),
 35:("data/car-reference/batch-35-geely-emgrand-egypt.json","geely","emgrand-15d-6at-egypt"),
}
def get(url,**kw):
    last=None
    for n in range(4):
        try:
            r=S.get(url,timeout=65,**kw)
            r.raise_for_status()
            return r
        except Exception as e:
            last=e
            if n<3:time.sleep(2+n*2)
    raise RuntimeError("HTTP GET failed "+url+" "+repr(last))

def post(url,body):
    last=None
    for n in range(4):
        try:
            r=S.post(url,json=body,headers=H,timeout=180)
            if r.status_code>=500:raise requests.RequestException("server "+str(r.status_code))
            if not r.ok:raise RuntimeError("Bridge response "+str(r.status_code)+" "+r.text[:360])
            return r.json()
        except requests.RequestException as e:
            last=e
            if n<3:time.sleep(3+n*2)
    raise RuntimeError("Bridge upload timed out "+repr(last))

def page_url(brand,model,row):
    return BASE+"/car-reference/"+brand+"/"+model+"/"+("" if row["kind"]=="model" else row["slug"]+"/")

def current_record(slug,url,title):
    result=get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":30}).json()
    matches=[p for p in result if p.get("slug")==slug and p.get("status")=="publish"]
    if len(matches)!=1:raise RuntimeError("Expected unique published record "+slug+"; got "+str(len(matches)))
    p=matches[0]
    if p.get("link","").rstrip("/")!=url.rstrip("/"):
        raise RuntimeError("Wrong existing live URL, refusing update: "+str(p.get("link")))
    if p.get("title",{}).get("rendered","")!=title:
        raise RuntimeError("Existing live title changed, refusing update: "+str(p.get("title")))
    return p

def source_photo(url,brand):
    host=urlparse(url).hostname
    assert (brand=="chery" and host=="www.chery-eg.com") or (brand=="geely" and host=="cdngeely.cloudhosta.com"),"Not exact OEM gallery host"
    r=get(url)
    content=r.content
    if len(content)<12000:raise RuntimeError("Official photo tiny "+url+" "+str(len(content)))
    try:
        im=Image.open(io.BytesIO(content)).convert("RGB")
    except Exception as e:raise RuntimeError("Official photo invalid "+url) from e
    if im.width<500 or im.height<260:
        raise RuntimeError("Official photo below reasonable source resolution "+url+" "+str(im.size))
    print("OEM_PHOTO",url,"source_dimensions",im.size,flush=True)
    return im

def photograph_cover(im,brand):
    """Editorial photo-first 1600x900 WebP. No drawings, charts or headline text."""
    W,H=1600,900
    w,h=im.size
    if w/h>=1.5:
        c=ImageOps.fit(im,(W,H),method=Image.Resampling.LANCZOS,centering=(.5,.49))
    else:
        bg=ImageOps.fit(im,(W,H),method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(38))
        shade=Image.new("RGBA",(W,H),(7,20,35,65))
        bg=Image.alpha_composite(bg.convert("RGBA"),shade).convert("RGB")
        inset=ImageOps.contain(im,(W-120,H-80),method=Image.Resampling.LANCZOS)
        x=(W-inset.width)//2
        y=(H-inset.height)//2
        bg.paste(inset,(x,y))
        c=bg
    c=ImageEnhance.Contrast(c).enhance(1.035)
    c=ImageEnhance.Color(c).enhance(1.06)
    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    # Small unobtrusive site signature only; the photographic vehicle dominates.
    d.rounded_rectangle((1361,828,1560,875),radius=12,fill=(12,25,40,135))
    font=None
    for fp in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
               "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(fp).exists():font=ImageFont.truetype(fp,22);break
    if font:d.text((1387,836),"A3TAL.COM",font=font,fill=(245,250,255,245))
    c=Image.alpha_composite(c.convert("RGBA"),overlay).convert("RGB")
    out=io.BytesIO()
    c.save(out,"WEBP",quality=90,method=6)
    data=out.getvalue()
    if data[:4]!=b"RIFF" or data[8:12]!=b"WEBP" or len(data)<23000:
        raise RuntimeError("Replacement output not a sufficient photographic WebP")
    return data

def audit(url,title,filename):
    failure=None
    for i in range(9):
        try:
            page=get(url,params={"a3_replacement_photo_qa":str(time.time_ns())},
                     headers={"Cache-Control":"no-cache"}).text
            if title not in page:raise RuntimeError("title missing")
            if filename not in page:raise RuntimeError("new photo missing from page")
            m=re.search(r'<meta[^>]+property=["\\x27]og:image["\\x27][^>]*>',page,re.I)
            if not m or filename not in m.group(0):raise RuntimeError("OG image not yet updated")
            can=re.search(r'<link[^>]+rel=["\\x27]canonical["\\x27][^>]*>',page,re.I)
            if not can or url.rstrip("/") not in can.group(0):raise RuntimeError("canonical changed")
            if re.search(r'<meta[^>]+name=["\\x27]robots["\\x27][^>]*noindex',page[:22000],re.I):
                raise RuntimeError("indexability switched off")
            return True
        except Exception as e:
            failure=repr(e)
            if i<8:time.sleep(5)
    raise RuntimeError("Replacement failed public QA "+url+" "+str(failure))

def run():
    health=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    assert health.get("ok") and health.get("published",0)>=420 and health.get("drafts")==0,health
    for batch,(data_file,brand,model) in INPUT.items():
        data=json.loads((ROOT/data_file).read_text(encoding="utf8"))
        assert data["batch"]==batch and data["brand"]==brand and data["model_slug"]==model
        assert len(data["rows"])==5 and len(PHOTO[batch])==5
        for i,row in enumerate(data["rows"]):
            slug=row["slug"]
            url=page_url(brand,model,row)
            before=current_record(slug,url,row["title"])
            filename=f"a3tal-b{batch}-oem-photo-{slug}-rev2.webp"
            old_name=f"a3tal-pseo-b{batch}-"+("arrizo5" if batch==34 else "emgrand")+"-"+slug+".webp"
            page=get(url).text
            if filename in page:
                print("PHOTO_ALREADY_FIXED",url,flush=True)
                RESULTS.append({"url":url,"batch":batch,"status":"already_fixed","file":filename})
                continue
            if old_name not in page:
                raise RuntimeError("Expected old diagram not on page, refuse blind image overwrite: "+url)
            photo=source_photo(PHOTO[batch][i],brand)
            picture=photograph_cover(photo,brand)
            media=post(UPLOAD,{"filename":filename,
                               "image_base64":base64.b64encode(picture).decode("ascii"),
                               "convert_webp":False,
                               "title":row["title"]+" | صورة سيارة من المصدر الرسمي",
                               "alt":row["title"]+" - الصورة الأصلية من "+("شيري مصر" if batch==34 else "جيلي مصر")})
            image_id=int(media.get("media_id") or 0)
            if image_id<1 or not str(media.get("url","")).endswith(".webp"):
                raise RuntimeError("New official photo upload failed "+slug)
            data_payload={
              "kind":row["kind"],
              "market":"Egypt / Chery Arrizo 5 DVVT model" if batch==34 else "Egypt / Geely Emgrand 2026 OEM 6AT",
              "years":"المواصفات الرسمية المدققة 2026-11-09",
              "engine":"Chery Arrizo 5 1499cc DVVT / 5MT or CVT" if batch==34 else "Geely Emgrand 1.5D 1499cc 120HP 152Nm / 6AT",
              "category":row.get("category",""),
              "reviewed_at":"2026-11-09",
              "facts":[{"label":f[0],"value":f[1]} for f in row["facts"]],
              "sources":[{"title":("Chery Egypt Arrizo 5 Official" if batch==34 else "Geely Egypt Emgrand Official"),"url":u} for u in row["sources"]]
            }
            body={"kind":row["kind"],"slug":slug,"title":row["title"],
                  "parent_path":brand if row["kind"]=="model" else brand+"/"+model,
                  "featured_image_id":image_id,"status":"publish",
                  "allow_update_published":True,
                  "content":row["rich_html"],"excerpt":row["meta_description"],
                  "meta_title":row["title"]+" | أعطال.كوم",
                  "meta_description":row["meta_description"],"data":data_payload}
            op=post(UPSERT,{"items":[body]})
            results=op.get("results") or []
            if len(results)!=1 or not results[0].get("ok") or results[0].get("status")!="publish":
                raise RuntimeError("Published image swap rejected "+str(op)[:400])
            if results[0].get("url","").rstrip("/")!=url.rstrip("/"):
                raise RuntimeError("Live canonical changed during image-only correction "+url)
            audit(url,row["title"],filename)
            RESULTS.append({"batch":batch,"url":url,"status":"photo_replaced",
                            "source":PHOTO[batch][i],"new_og_filename":filename,
                            "media_id":image_id,"featured_image":media["url"],"verified":True})
            print("PHOTO_SWAP_AND_OG_VERIFIED",url,flush=True)
    after=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
    if after["published"]!=health["published"] or after["drafts"]!=0:
        raise RuntimeError("Photo-only repair changed published inventory "+str(after))
    print("ALL_TEN_OFFICIAL_REAL_CAR_PHOTOS_VERIFIED",len(RESULTS),after["published"],flush=True)

if __name__=="__main__":
    try:run()
    except Exception as e:
        RESULTS.append({"failed":repr(e),"traceback":traceback.format_exc()})
        raise
    finally:
        REPORT.write_text(json.dumps({"result":RESULTS},ensure_ascii=False,indent=2),encoding="utf8")
