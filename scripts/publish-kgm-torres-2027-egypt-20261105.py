#!/usr/bin/env python3
"""Publish verified 2027 KGM Torres Egypt launch article via A3tal Direct Bridge.
- Exact Egyptian pricing and engine validation
- Strict same-intent duplicate guard
- Official KGM New Torres photography, page-specific edited WebP with attribution
- Live featured media, inline image, canonical, robots and OG verification
"""
import base64,io,json,os,re,urllib.parse,urllib.request,urllib.error
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance,ImageDraw,ImageFont

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
SLUG="kgm-torres-2027-egypt-price-trims-8speed"
URL=SITE+"/"+SLUG+"/"
TITLE="سعر KGM توريس 2027 في مصر: 5 فئات وفتيس AISIN الجديد.. أي فئة تستحق؟"
FILE=Path("data/editorial/kgm-torres-2027-egypt-facelift-prices-20261105.html")
CATEGORY=374
SOURCE="https://allways.kg-mobility.com/kgm-%EB%89%B4-%ED%86%A0%EB%A0%88%EC%8A%A4-%EC%B6%9C%EC%8B%9C-%ED%8C%8C%EC%9B%8C%ED%8A%B8%EB%A0%88%EC%9D%B8-%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C-%EC%A0%95%ED%86%B5-suv-%EA%B0%90%EC%84%B1/"
BASE="https://allways.kg-mobility.com/wp-content/uploads/2026/05/"
COVER=[BASE+"0_batch.jpg",BASE+"1-1_batch.jpg",BASE+"1-3_batch.jpg"]
DETAIL=[BASE+"2-1_batch.jpg",BASE+"2-2_batch.jpg",BASE+"2-4_batch.jpg"]

def jreq(path,protected=False,data=None):
 head={"Accept":"application/json","User-Agent":"A3tal-KGM-Torres-2027-Original-Editorial/20261105","Cache-Control":"no-store"}
 if protected:
  if not KEY:raise RuntimeError("Missing A3TAL_API_KEY GitHub secret")
  head.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
 raw=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf-8")
 if raw is not None:head["Content-Type"]="application/json; charset=utf-8"
 req=urllib.request.Request((API if protected else SITE)+path,data=raw,headers=head,method="POST" if raw is not None else "GET")
 with urllib.request.urlopen(req,timeout=300) as f:return json.load(f)

def dedup():
 exact=jreq("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":SLUG,"_fields":"id,slug,status,link,featured_media,content"}))
 if len(exact)>1:raise RuntimeError("Multiple posts of the same slug")
 if exact:
  p=exact[0];html=(p.get("content") or {}).get("rendered","")
  if p.get("status")=="publish" and p.get("featured_media") and "1,650,000" in html and "AISIN" in html and "a3tal_image" not in html:
   print("ALREADY_PUBLISHED_VERIFIED",p["id"],p["link"],flush=True)
   return p
  raise RuntimeError("Existing incomplete or draft slug: manual reconciliation required")
 for term in ("توريس 2027","Torres 2027","kgm-torres-2027"):
  matches=jreq("/search-posts?"+urllib.parse.urlencode({"search":term,"limit":100}),protected=True)
  for p in matches.get("items",[]):
   title=str(p.get("title",""))+" "+str(p.get("slug",""))
   if ("2027" in title and ("توريس" in title or "Torres" in title or "torres" in title.lower())):
    raise RuntimeError("Existing identical 2027 Egypt launch intent; do not duplicate: "+str(p)[:300])
 return None

def load_official_photo(urls):
 for url in urls:
  try:
   head={"User-Agent":"Mozilla/5.0 (compatible; A3talEditorial/20261105; +https://a3tal.com)","Accept":"image/jpeg,image/webp,image/png,image/*"}
   with urllib.request.urlopen(urllib.request.Request(url,headers=head),timeout=55) as f:raw=f.read(12_000_000)
   if not 35000<len(raw)<12_000_000:continue
   with Image.open(io.BytesIO(raw)) as im:
    im.load()
    if im.width<1100 or im.height<640:continue
    print("OFFICIAL_MANUFACTURER_IMAGE",url,im.size,flush=True)
    return ImageOps.exif_transpose(im).convert("RGB"),url
  except Exception as e:print("IMAGE_CANDIDATE_FAILED",url.rsplit("/",1)[-1],type(e).__name__,flush=True)
 raise RuntimeError("Could not fetch an authentic KGM New Torres official image; publication safely stopped.")

def make_media(role,photo,src,size,alt):
 w,h=size;out=ImageOps.fit(photo,size,method=Image.Resampling.LANCZOS,centering=(.50,.51))
 out=ImageEnhance.Contrast(out).enhance(1.065)
 out=ImageEnhance.Color(out).enhance(1.05)
 out=ImageEnhance.Sharpness(out).enhance(1.06)
 overlay=Image.new("RGBA",size,(0,0,0,0));d=ImageDraw.Draw(overlay)
 d.rounded_rectangle((w-183,h-56,w-19,h-17),radius=11,fill=(10,22,36,138))
 try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",17)
 except OSError:font=ImageFont.load_default()
 d.text((w-163,h-46),"A3tal.com",font=font,fill=(255,255,255,240))
 out=Image.alpha_composite(out.convert("RGBA"),overlay).convert("RGB")
 b=io.BytesIO();out.save(b,"WEBP",quality=87,method=6)
 raw=b.getvalue()
 if not 45000<len(raw)<2400000:raise RuntimeError("WebP size outside accepted range")
 fn="a3tal-kgm-torres-2027-egypt-"+role+"-editorial.webp"
 return {"key":role,"role":"featured" if role=="cover" else "inline",
         "filename":fn,"image_base64":base64.b64encode(raw).decode("ascii"),
         "convert_webp":False,"alt":alt,
         "caption":"صورة للطراز KGM New Torres من مدونة الشركة المصنعة الرسمية، معالجة وتكوين مخصصان لأعطال.كوم. المصدر: "+src+"؛ تختلف بعض تفاصيل التجهيز حسب السوق.",
         "placeholder":"{{a3tal_image:detail}}"}

def main():
 if not KEY:raise RuntimeError("No protected bridge credential")
 html=FILE.read_text("utf-8").strip()
 if len(html)<12500 or html.count("<h2>")<9 or html.count("<h3>")<7 or html.count("<table")<3:raise RuntimeError("Article structure validation failed")
 for fact in ("1,650,000","1,790,000","1,925,000","2,075,000","300 نيوتن","163 حصان","AISIN","2026","2027","{{a3tal_image:detail}}"):
  if fact not in html:raise RuntimeError("Verified price, model or media required: "+fact)
 if dedup():return
 cat=jreq("/wp-json/wp/v2/categories/"+str(CATEGORY))
 if "أسعار السيارات" not in cat.get("name","") and "اسعار السيارات" not in cat.get("name",""):raise RuntimeError("Unexpected category 374")
 cover,coverurl=load_official_photo(COVER)
 detail,detailurl=load_official_photo(DETAIL)
 if coverurl==detailurl:raise RuntimeError("Cover and detail photo must differ")
 media=[
  make_media("cover",cover,coverurl,(1600,900),"صورة حقيقية لكيا جي إم توريس KGM Torres 2027 فيس ليفت، الواجهة الجديدة، تفاصيل الشبكة والمصابيح"),
  make_media("detail",detail,detailurl,(1400,840),"مقصورة KGM توريس المحدثة 2027 والكونسول الجديد ومحدد الفتيس والشاشات")
 ]
 post={
  "type":"post","status":"publish","slug":SLUG,"title":TITLE,"content":html,
  "categories":[CATEGORY],
  "excerpt":"أسعار KGM توريس 2027 في مصر من 1.65 إلى 2.075 مليون جنيه. تفاصيل 5 فئات والمحرك 163 حصان وفتيس AISIN 8 سرعات والفروق عن موديل 2026.",
  "meta":{
   "_yoast_wpseo_title":"سعر KGM توريس 2027 في مصر والفئات والفتيس الجديد | أعطال.كوم",
   "_yoast_wpseo_metadesc":"أسعار KGM توريس 2027 في مصر تبدأ من 1.65 مليون جنيه. مقارنة الفئات الخمس، موتور 163 حصان، فتيس AISIN 8 سرعات والفروق عن 2026.",
   "_yoast_wpseo_focuskw":"سعر KGM توريس 2027 في مصر",
   "_yoast_wpseo_canonical":URL,
   "_yoast_wpseo_opengraph-title":TITLE,
   "_yoast_wpseo_opengraph-description":"توريس 2027 في مصر من 1.65 مليون: مقارنة الفئات الخمس ومواصفات الفتيس الياباني الجديد وأفضل فئة حسب الاستخدام.",
   "_yoast_wpseo_twitter-title":TITLE,
   "_yoast_wpseo_twitter-description":"KGM توريس 2027: الأسعار الرسمية وتجهيزات Comfort وAdvanced وPremium وLuxury وBlack Edition."
  }
 }
 try:result=jreq("/publish-bundle",protected=True,data={"post":post,"media":media})
 except (TimeoutError,urllib.error.URLError):
  print("AMBIGUOUS_WRITE_VERIFY_ONLY",flush=True)
  rows=jreq("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":SLUG,"_fields":"id,slug,status,link,featured_media"}))
  if len(rows)!=1 or rows[0].get("status")!="publish" or not rows[0].get("featured_media"):raise
  result={"post":rows[0]}
 p=result.get("post") or {}
 if p.get("status")!="publish" or p.get("slug")!=SLUG or not p.get("featured_media"):raise RuntimeError("Bridge did not confirm publication with featured media")
 live=jreq("/wp-json/wp/v2/posts/"+str(p["id"])+"?"+urllib.parse.urlencode({"_fields":"id,slug,status,link,featured_media,categories,content,yoast_head_json"}))
 seo=live.get("yoast_head_json") or {}
 body=(live.get("content") or {}).get("rendered","")
 og=(seo.get("og_image") or [{}])[0].get("url","")
 if (live.get("status")!="publish" or live.get("link")!=URL or live.get("featured_media")!=p.get("featured_media")
  or CATEGORY not in live.get("categories",[]) or "{{a3tal_image" in body
  or "torres-2027-egypt-detail-editorial.webp" not in body or "torres-2027-egypt-cover-editorial.webp" not in og
  or seo.get("canonical")!=URL or (seo.get("robots") or {}).get("index")=="noindex"):
  raise RuntimeError("Live URL, image, indexability or canonical QA failed for "+URL)
 print("PUBLISHED_VERIFIED",p["id"],URL,"CATEGORY",CATEGORY,"FEATURED",p["featured_media"],"OG_IMAGE",og,flush=True)

if __name__=="__main__":main()
