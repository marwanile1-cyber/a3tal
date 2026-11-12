#!/usr/bin/env python3
import base64, hashlib, io, json, os, re, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont
BASE="https://a3tal.com"
API=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
ROWS=json.loads(Path("data/editorial/20261112-weak-categories/bundle.json").read_text("utf8"))["posts"]
EXPECTED=[17,6,2790,12,335,16,191,5,3,87]
NAMES=["lamps","filter","traffic","exhaust","battery","wiring","thermostat","atf","belt","training"]
LICENCES={"CC BY 2.0":"https://creativecommons.org/licenses/by/2.0/","CC BY 4.0":"https://creativecommons.org/licenses/by/4.0/","CC BY-SA 4.0":"https://creativecommons.org/licenses/by-sa/4.0/","CC BY-SA 3.0":"https://creativecommons.org/licenses/by-sa/3.0/","CC BY-SA 2.0":"https://creativecommons.org/licenses/by-sa/2.0/"}
REPORT=Path("reports/undercovered-ten-20261112-audit.json")
REPORT.parent.mkdir(exist_ok=True,parents=True)

def request(path,auth=False,data=None,timeout=350):
    headers={"User-Agent":"A3tal-CustomPhotoEditorial-20261112","Accept":"application/json","Cache-Control":"no-store"}
    if auth:
        if not KEY:raise RuntimeError("Direct Bridge secret missing")
        headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf8")
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    url=(API if auth else BASE)+path
    obj=urllib.request.Request(url,headers=headers,data=raw,method="POST" if raw is not None else "GET")
    try:
        with urllib.request.urlopen(obj,timeout=timeout) as f:return json.load(f)
    except urllib.error.HTTPError as e:
        raise RuntimeError(str(e.code)+" "+url+": "+e.read(500).decode("utf8","replace")) from e

def source_photo(p):
    name=p["photo"]["file"]
    if not name.lower().endswith((".jpg",".jpeg",".png")):raise RuntimeError("Invalid image name")
    name=name.replace(" ","_")
    url="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(name,safe="(),-._")
    q=urllib.request.Request(url,headers={"User-Agent":"A3talAutomotivePublisher/1.0 (https://a3tal.com)","Accept":"image/jpeg,image/*"})
    with urllib.request.urlopen(q,timeout=110) as f:raw=f.read(30_000_000)
    if len(raw)<50000:raise RuntimeError("No high quality photograph: "+url)
    with Image.open(io.BytesIO(raw)) as photo:
        photo.load()
        if photo.width<1550 or photo.height<1200:raise RuntimeError("Low-res photo "+name+" "+str(photo.size))
        # Make high-quality, consistent, independent editorial source canvas.
        im=ImageOps.fit(ImageOps.exif_transpose(photo).convert("RGB"),(2200,1400),method=Image.Resampling.LANCZOS)
    print("SOURCE_CC_PHOTO_APPROVED",p["slug"],len(raw),hashlib.sha256(raw).hexdigest()[:14],flush=True)
    return im

def webp(photo,index,role):
    W,H=(1600,900) if role=="featured" else (1360,860)
    crop=ImageOps.fit(photo,(W-26,H-26),method=Image.Resampling.LANCZOS,
      centering=(.48 if index%2==0 else .52,.49))
    crop=ImageEnhance.Contrast(crop).enhance(1.05)
    base=ImageOps.fit(photo,(W,H),method=Image.Resampling.LANCZOS)
    base=ImageEnhance.Brightness(base).enhance(.68)
    base.paste(crop,(13,13))
    draw=ImageDraw.Draw(base)
    draw.rectangle((13,13,21,H-13),fill=(188,31,53))
    draw.rectangle((13,H-21,W-13,H-13),fill=(17,34,57))
    try:ft=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",19)
    except OSError:ft=ImageFont.load_default()
    draw.rounded_rectangle((W-180,H-65,W-24,H-29),radius=9,fill=(15,32,49))
    draw.text((W-169,H-59),"A3TAL.COM",fill="white",font=ft)
    f=io.BytesIO();base.save(f,"WEBP",quality=89,method=6)
    raw=f.getvalue()
    if len(raw)<18000 or raw[:4]!=b"RIFF" or raw[8:12]!=b"WEBP":raise RuntimeError("Invalid photographic WebP")
    return raw

def filenames(i):
    stem="a3tal-20261112-"+NAMES[i]+"-original-photo-"
    return stem+"featured.webp",stem+"inline.webp"

def assets(p,i,photo):
    cover,inline=filenames(i)
    out=[]
    src="https://commons.wikimedia.org/wiki/File:"+urllib.parse.quote(p["photo"]["file"].replace(" ","_"),safe="(),-._")
    for role,name in [("featured",cover),("inline",inline)]:
        out.append({"key":role,"role":role,"filename":name,
         "image_base64":base64.b64encode(webp(photo,i,role)).decode("ascii"),
         "convert_webp":False,"alt":p["focus"]+"، صورة فوتوغرافية توضيحية عالية الجودة",
         "caption":"الصورة الأصلية: "+p["photo"]["author"]+"، "+p["photo"]["license"]+
                   "، تعديل وتصميم تحريري: أعطال.كوم؛ المصدر: "+src,
         "placeholder":"{{a3tal_image:inline}}"})
    return out

def verify(p,i,id,featured):
    data=request("/wp-json/wp/v2/posts/"+str(id)+"?"+urllib.parse.urlencode(
     {"_fields":"id,slug,status,link,featured_media,categories,content,yoast_head_json"}))
    url=BASE+"/"+p["slug"]+"/"
    seo=data.get("yoast_head_json") or {}
    body=(data.get("content") or {}).get("rendered","")
    og=(seo.get("og_image") or [{}])[0].get("url","")
    a,b=filenames(i)
    checks={"url":data.get("link")==url,"status":data.get("status")=="publish",
    "category":p["category"] in data.get("categories",[]),
    "featured":int(data.get("featured_media") or 0)==int(featured) and int(featured)>0,
    "og":a in og,"canonical":seo.get("canonical")==url,
    "index":(seo.get("robots") or {}).get("index")!="noindex",
    "inline":b in body,"sections":body.count("<h2")>=6,
    "source":"commons.wikimedia.org" in body,"placeholder":"{{a3tal_image:" not in body}
    if not all(checks.values()):raise RuntimeError("LIVE_QA_FAILED "+str(checks)+" "+url)
    print("GAP_POST_PUBLIC_SEO_PHOTO_VERIFIED",url,flush=True)
    return {"url":url,"category":p["category"],"id":id,"featured":featured,"og":og,"checks":checks}

def main():
    if not KEY:raise RuntimeError("Missing A3TAL_API_KEY")
    if len(ROWS)!=10 or [p["category"] for p in ROWS]!=EXPECTED:raise RuntimeError("Category audit mismatch")
    if len({p["slug"] for p in ROWS})!=10 or len({p["photo"]["file"] for p in ROWS})!=10:raise RuntimeError("Duplicate article or image")
    # Resolve every image and category before publishing any new content.
    photos=[]
    for p in ROWS:
        if p["photo"]["license"] not in LICENCES:raise RuntimeError("Wrong image license")
        info=request("/wp-json/wp/v2/categories/"+str(p["category"])+"?_fields=id,name")
        if info.get("id")!=p["category"]:raise RuntimeError("Wrong category")
        if len(p["html"])<2700 or p["html"].count("<h2>")<6:raise RuntimeError("Thin content")
        photos.append(source_photo(p))
    print("ALL_TEN_AUTHENTIC_LICENSED_PHOTOS_PREFLIGHT_PASSED",flush=True)
    done=[]
    for i,p in enumerate(ROWS):
        url=BASE+"/"+p["slug"]+"/"
        search=request("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":p["slug"],"per_page":5,
          "_fields":"id,status,slug,link,featured_media,categories"}))
        if len(search)>1:raise RuntimeError("Duplicate existing slug")
        if search:
            old=search[0]
            if old["status"]!="publish" or not old.get("featured_media"):raise RuntimeError("Existing invalid post")
            row=verify(p,i,old["id"],old["featured_media"])
        else:
            src="https://commons.wikimedia.org/wiki/File:"+urllib.parse.quote(p["photo"]["file"].replace(" ","_"),safe="(),-._")
            license_url=LICENCES[p["photo"]["license"]]
            attribution='<p><small>صورة فوتوغرافية مرخصة: <a href="'+src+'" rel="nofollow noopener noreferrer">'+p["photo"]["author"]+'</a>، <a href="'+license_url+'" rel="nofollow noopener noreferrer">'+p["photo"]["license"]+'</a>، تعديل وتكوين تحريري بواسطة أعطال.كوم.</small></p>'
            body=p["html"].replace("<h2>","<figure>{{a3tal_image:inline}}</figure><h2>",1)+attribution
            meta={"_yoast_wpseo_title":p["title"]+" | أعطال.كوم",
             "_yoast_wpseo_metadesc":p["meta"],"_yoast_wpseo_focuskw":p["focus"],
             "_yoast_wpseo_canonical":url,"_yoast_wpseo_opengraph-title":p["title"],
             "_yoast_wpseo_opengraph-description":p["meta"]}
            post={"type":"post","status":"publish","slug":p["slug"],"title":p["title"],
                 "content":body,"categories":[p["category"]],"excerpt":p["meta"],"meta":meta}
            result=request("/publish-bundle",auth=True,data={"post":post,"media":assets(p,i,photos[i])},timeout=420)
            published=result.get("post") or {}
            if not published.get("id") or not published.get("featured_media") or published.get("status")!="publish":
                raise RuntimeError("Incomplete publish response "+p["slug"]+" "+str(published)[:350])
            row=verify(p,i,published["id"],published["featured_media"])
        done.append(row)
        REPORT.write_text(json.dumps({"completed":len(done),"posts":done},ensure_ascii=False,indent=2),"utf8")
    print("ALL_TEN_WEAK_CATEGORY_POSTS_PUBLISHED",len(done),flush=True)

if __name__=="__main__":main()
