#!/usr/bin/env python3
"""Publish two distinct TVS motorcycle price articles through A3tal Direct Bridge only.
Original, article-specific branded WebP editorial treatments of official TVS product media.
Never use stock/generic other-model photos. No prices are presented as official MSRP.
"""
import base64, io, json, os, urllib.request, urllib.parse, urllib.error, re, time
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
CATEGORY=3028
TVS="https://www.tvsmotor.com/eg/-/media/Feature/IB/Webp-Images/"

ITEMS=[
{
 "slug":"tvs-hlx-150f-price-egypt-2026",
 "file":"data/editorial/tvs-hlx-150f-price-egypt-20261102.html",
 "title":"سعر موتوسيكل TVS HLX 150 F في مصر 2026.. 3 عروض للبيع والمواصفات والعيوب",
 "excerpt":"سعر TVS HLX 150 F موديل 2026 في مصر من 56,900 إلى 62,000 جنيه لدى معارض مختلفة، وليس سعر وكيل رسمي. المواصفات والفرامل والفرق عن HLX 150.",
 "meta":{
  "_yoast_wpseo_title":"سعر TVS HLX 150 F في مصر 2026 والمواصفات | أعطال.كوم",
  "_yoast_wpseo_metadesc":"سعر موتوسيكل TVS HLX 150 F في مصر 2026 بعروض 56,900 و58,000 و62,000 جنيه. المواصفات الرسمية، الفرامل الديسك والفرق عن HLX 150 قبل الشراء.",
  "_yoast_wpseo_focuskw":"سعر TVS HLX 150 F في مصر 2026"
 },
 "search":["HLX 150 F","HLX150F"],
 "fact":["56,900","58,000","62,000","147.49","12.3","{{a3tal_image:detail}}"],
 "model":"TVS HLX 150 F",
 "cover_sources":[
 TVS+"Non-Premium/HlX-150-F/Web/Colour/hlx-150-5-web-red.webp",
 TVS+"Non-Premium/HlX-150-F/Web/Banner/Banner.webp",
 TVS+"Non-Premium/HlX-150-F/Web/Features/hlx-150-f-brand--graphics.webp"
 ],
 "detail_sources":[
 TVS+"Non-Premium/HlX-150-F/Web/Features/hlx-150-F-web-carrier.webp",
 TVS+"Non-Premium/HlX-150-F/Web/Features/hlx-150-f-brand-New-Seat-Style.webp",
 TVS+"Non-Premium/HlX-150-F/Web/Overview/hlx-150-f-web-Mileage.webp"
 ],
 "cover_alt":"موتوسيكل TVS HLX 150 F الأحمر بمظهر جانبي، صورة المنتج الرسمية مع تصميم تحريري خاص بأعطال.كوم",
 "detail_alt":"تفاصيل موتوسيكل TVS HLX 150 F والحامل الخلفي للاستخدام العملي كما تظهر في المواد الرسمية"
},
{
 "slug":"tvs-ronin-nimbus-225-price-egypt-2026",
 "file":"data/editorial/tvs-ronin-nimbus-225-price-egypt-20261102.html",
 "title":"سعر TVS Ronin Nimbus 225 في مصر 2026.. 126 ألف جنيه وهل يستحق؟",
 "excerpt":"سعر TVS Ronin 225 المعروض بمصر 126 ألف جنيه لدى أحد البائعين، وليس سعرًا رسميًا للتوكيل. تعرف على مواصفات Nimbus 225 وABS والفتيس والعيوب.",
 "meta":{
  "_yoast_wpseo_title":"سعر TVS Ronin Nimbus 225 في مصر 2026 والمواصفات | أعطال.كوم",
  "_yoast_wpseo_metadesc":"سعر TVS Ronin 225 في مصر 2026 معروض بـ126 ألف جنيه لدى معرض، وليس سعرًا رسميًا. مواصفات Nimbus بمحرك 20.4 حصان وABS وأهم العيوب قبل الشراء.",
  "_yoast_wpseo_focuskw":"سعر TVS Ronin Nimbus 225 في مصر"
 },
 "search":["Ronin Nimbus","رونين 225","رونن 225"],
 "fact":["126,000","225.9","20.4","19.93","{{a3tal_image:detail}}"],
 "model":"TVS Ronin Nimbus 225",
 "cover_sources":[
 TVS+"Premium/Ronin-Nimbus/Web/color/nimbus-grey-new1.webp",
 TVS+"NewUI/Product/RONIN-NIMBUS/overview_image/04_overview_image.webp",
 TVS+"Premium/Ronin-Nimbus/Web/color/midnight-blue.webp"
 ],
 "detail_sources":[
 TVS+"Premium/Ronin-Nimbus/Web/feature/T-face-pilot-headlamp.webp",
 TVS+"Premium/Ronin-Nimbus/Web/feature/Assymetric-Speedometer.webp",
 TVS+"Premium/Ronin-Nimbus/Web/feature/Custom-Exhaust.webp"
 ],
 "cover_alt":"موتوسيكل TVS Ronin Nimbus 225 الرمادي بتصميم كلاسيكي عصري من صور TVS الرسمية داخل معالجة تحريرية حصرية",
 "detail_alt":"تفاصيل تصميم TVS Ronin Nimbus 225 وإضاءة LED والعناصر الفنية في صورة خاصة بالمقال"
}
]
def req(path,protected=False,payload=None,timeout=180):
 headers={"User-Agent":"A3tal-TVS-Editorial-20261102/1","Accept":"application/json","Cache-Control":"no-store"}
 if protected:
  if not KEY: raise RuntimeError("Missing protected Github Actions A3TAL_API_KEY")
  headers["X-A3tal-Key"]=KEY
  headers["Authorization"]="Bearer "+KEY
 raw=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf8")
 if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
 url=(API if protected else SITE)+path
 request=urllib.request.Request(url,headers=headers,data=raw,method="POST" if raw is not None else "GET")
 with urllib.request.urlopen(request,timeout=timeout) as f:return json.load(f)

def validate_originality(item):
 exact=req("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":item["slug"],"_fields":"id,slug,status,link,featured_media,content"}))
 if len(exact)>1:raise RuntimeError("Unexpected duplicate slug: "+item["slug"])
 if exact:
  q=exact[0]
  if q.get("status")=="publish" and q.get("featured_media") and q["slug"]==item["slug"] and "<table" in (q.get("content") or {}).get("rendered",""):
   print("ALREADY_PUBLISHED",q["id"],q["link"],flush=True)
   return q
  raise RuntimeError("Existing incomplete article at target slug. No overwrite.")
 for term in item["search"]:
  rows=req("/search-posts?"+urllib.parse.urlencode({"search":term,"limit":100}),protected=True)
  for row in rows.get("items",[]):
   name=(row.get("title","")+" "+row.get("slug","")).casefold()
   if item["slug"].replace("-price-egypt-2026","").replace("-225","") in name:
    raise RuntimeError("Intent collision identified: "+str(row))
   if item["model"].casefold() in name and ("سعر" in name or "price" in name):
    raise RuntimeError("Similar price page already exists: "+str(row))
 return None

def photo_from_official(sources):
 for url in sources:
  try:
   hdr={"User-Agent":"Mozilla/5.0 (compatible; A3talEditorial/2026; +https://a3tal.com/)","Accept":"image/webp,image/jpeg,image/png,image/*"}
   with urllib.request.urlopen(urllib.request.Request(url,headers=hdr),timeout=40) as f:raw=f.read(8_000_000)
   if not 16000<len(raw)<8_000_000:continue
   with Image.open(io.BytesIO(raw)) as im:
    im.load()
    if im.width<500 or im.height<260:continue
    im=ImageOps.exif_transpose(im).convert("RGBA")
    print("OFFICIAL_TVS_SOURCE",url,im.size,flush=True)
    return im,url
  except Exception as exc:
   print("PHOTO_SOURCE_UNAVAILABLE",url.rsplit("/",1)[-1],type(exc).__name__,flush=True)
 raise RuntimeError("No verified model-specific official TVS image available; stop publish")

def prepare(item,role,sources,size,filename,alt):
 original,source=photo_from_official(sources)
 w,h=size
 # Branded original editorial composition. Keep all motorcycle geometry. A slightly
 # defocused, desaturated version of the official scene fills the letterbox.
 base=ImageOps.fit(original.convert("RGB"),(w,h),method=Image.Resampling.LANCZOS,centering=(.5,.5))
 base=base.filter(ImageFilter.GaussianBlur(max(10,w//82)))
 base=ImageEnhance.Color(base).enhance(.55)
 base=ImageEnhance.Brightness(base).enhance(.77)
 # Foreground is contained, never stretched or artificially redrawn.
 foreground=ImageOps.contain(original,(int(w*.92),int(h*.90)),method=Image.Resampling.LANCZOS)
 x=(w-foreground.width)//2;y=(h-foreground.height)//2
 if foreground.mode=="RGBA":base.paste(foreground,(x,y),foreground)
 else:base.paste(foreground,(x,y))
 # Subtle brand, no large headline or unreadable advertising blocks
 draw=ImageDraw.Draw(base)
 draw.rounded_rectangle((w-208,h-56,w-24,h-18),radius=9,fill=(15,28,40,155))
 try:
  font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",18)
 except OSError:font=ImageFont.load_default()
 draw.text((w-189,h-47),"A3tal.com",fill="#ffffff",font=font)
 out=io.BytesIO();base.save(out,"WEBP",quality=87,method=6)
 raw=out.getvalue()
 if not 23000<len(raw)<2500000:raise RuntimeError("Unexpected edited image size "+str(len(raw)))
 return {"key":role,"role":"featured" if role=="cover" else "inline",
         "filename":filename,"image_base64":base64.b64encode(raw).decode("ascii"),
         "convert_webp":False,"alt":alt,
         "caption":"صورة للموديل من المواد الرسمية لشركة TVS، معالجة وتكوين تحريري خاص بأعطال.كوم. مصدر صورة المنتج: "+source,
         "placeholder":"{{a3tal_image:detail}}"}

def publish(item):
 source=Path(item["file"]).read_text(encoding="utf-8")
 if len(source)<9000 or source.count("<h2>")<8 or source.count("<table")<2 or source.count("<h3>")<4:
  raise RuntimeError("Content structure/depth failed "+item["slug"])
 if not all(s in source for s in item["fact"]):
  raise RuntimeError("Important facts not reviewed "+item["slug"])
 existing=validate_originality(item)
 if existing:return existing["link"]
 slug=item["slug"];url=SITE+"/"+slug+"/"
 photos=[
  prepare(item,"cover",item["cover_sources"],(1600,900),"a3tal-"+slug+"-exclusive-cover.webp",item["cover_alt"]),
  prepare(item,"detail",item["detail_sources"],(1400,840),"a3tal-"+slug+"-exclusive-detail.webp",item["detail_alt"])
 ]
 post={"type":"post","title":item["title"],"slug":slug,"status":"publish",
       "content":source,"excerpt":item["excerpt"],"categories":[CATEGORY],
       "meta":dict(item["meta"],**{
         "_yoast_wpseo_canonical":url,
         "_yoast_wpseo_opengraph-title":item["title"],
         "_yoast_wpseo_opengraph-description":item["excerpt"],
         "_yoast_wpseo_twitter-title":item["title"],
         "_yoast_wpseo_twitter-description":item["excerpt"]
       })}
 try:
  result=req("/publish-bundle",protected=True,payload={"post":post,"media":photos},timeout=300)
 except (TimeoutError,urllib.error.URLError):
  print("WRITE_TIMED_OUT_VERIFY_ONLY",slug,flush=True)
  hits=req("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":slug,"_fields":"id,slug,status,featured_media,link"}))
  if len(hits)!=1 or hits[0]["status"]!="publish" or not hits[0].get("featured_media"):raise
  result={"post":hits[0]}
 info=result.get("post") or {}
 if info.get("status")!="publish" or info.get("slug")!=slug or not info.get("featured_media"):
  raise RuntimeError("Bridge did not confirm published cover "+slug)
 verify=req("/wp-json/wp/v2/posts/"+str(info["id"])+"?"+urllib.parse.urlencode({"_fields":"id,slug,status,link,featured_media,categories,content,yoast_head_json"}))
 body=verify.get("content",{}).get("rendered","")
 yoast=verify.get("yoast_head_json") or {}
 og=(yoast.get("og_image") or [{}])[0].get("url","")
 if (verify.get("link")!=url or verify.get("status")!="publish"
     or CATEGORY not in verify.get("categories",[])
     or not verify.get("featured_media") or "{{a3tal_image" in body
     or "exclusive-detail" not in body or "exclusive-cover" not in og
     or yoast.get("canonical")!=url or (yoast.get("robots") or {}).get("index")=="noindex"):
  raise RuntimeError("Live site publication/SEO/media failed QA "+slug)
 print("PUBLISHED_VERIFIED",info["id"],url,"COVER_ID",verify["featured_media"],"OG_IMAGE",og,flush=True)
 return url

def main():
 if not KEY:raise RuntimeError("No protected bridge credential")
 # One batch, separate canonical URLs; idempotent and guarded against duplicate posts.
 for item in ITEMS:publish(item)
 print("TWO_TVS_MOTORCYCLE_ARTICLES_COMPLETED",flush=True)
if __name__=="__main__":main()
