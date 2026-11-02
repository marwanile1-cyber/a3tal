#!/usr/bin/env python3
"""Publish three original A3tal.com diagnosis guides: suspension, mechanics, electrics.
Uses the site's protected A3tal Direct Bridge through GitHub Actions only.
Safe deduplication, verified creative-commons photograph provenance and Yoast QA.
"""
import base64,io,json,os,re,urllib.request,urllib.parse,urllib.error
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance,ImageFilter,ImageDraw,ImageFont

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
POSTS=[
{
 "slug":"car-floating-wandering-highway-suspension-diagnosis",
 "file":"data/editorial/car-floating-wandering-highway-suspension-diagnosis-20261102.html",
 "title":"العربية بتعوم على السرعات؟ تشخيص المساعدين وجلب المقصات والدركسيون قبل التغيير",
 "excerpt":"العربية بتعوم على الطريق أو تحتاج تعديل الدركسيون باستمرار؟ تعرّف على الفرق بين ضعف المساعدين وتلف الجلب والبارات ومشاكل الكاوتش والزوايا.",
 "focus":"العربية بتعوم على السرعات",
 "category":"عفشة",
 "checks":["العربية بتعوم","جلب المقصات","الزوايا","{{a3tal_image:detail}}"],
 "dedup":["العربية بتعوم","car floating wandering highway"],
 "photo":[
   [("Front suspension .jpg","Sarbsinghdhammu","CC BY-SA 4.0"),("Front suspensions.jpg","Sarbsinghdhammu","CC BY-SA 4.0")],
   [("Front suspension of Toyota Land Cruiser J60.jpg","Pittigrilli","CC BY-SA 4.0"),("Live axle front suspension.jpg","Hustvedt","CC BY-SA 3.0")]
 ],
 "alt":[
  "لقطة حقيقية لمجموعة العفشة الأمامية بالسيارة تشمل المساعد والمقص، صورة توضيحية لتشخيص تعويم العربية",
  "تفاصيل مكونات التعليق والذراع والعجلة الأمامية من سيارة فعلية أثناء فحص أسباب عدم ثبات السيارة"
 ]
},
{
 "slug":"car-hesitates-cold-start-fine-when-warm",
 "file":"data/editorial/car-hesitates-cold-start-fine-when-warm-20261102.html",
 "title":"العربية بتنتش وهي باردة وتتظبط بعد التسخين؟ تشخيص حساس الحرارة والبوجيهات والهواء",
 "excerpt":"تقطيع العربية وهي باردة ثم انتظامها بعد التسخين: طريقة فحص حساس ECT وتسريب الهواء والكويل والبوجيه وبيانات OBD قبل تغيير القطع.",
 "focus":"العربية بتنتش وهي باردة",
 "category":"ميكانيكا",
 "checks":["العربية بتنتش","ECT","P0300","{{a3tal_image:detail}}"],
 "dedup":["بتنتش وهي باردة","hesitates cold start fine warm"],
 "photo":[
   [("Mechanic repairing car engine.jpg","Bembety","CC0"),("Car engine maintenance involves a mechanic inspecting and adjusting parts under the hood.jpg","Shixart1985","CC BY 2.0")],
   [("Car engine 01.jpg","Azorbli","CC BY-SA 4.0"),("Mechanic works on car engine performing routine maintenance and inspections on vehicle parts.jpg","Shixart1985","CC BY 2.0")]
 ],
 "alt":[
  "ميكانيكي يفحص محرك سيارة فعلية خلال تشخيص تقطيع المحرك عند التشغيل البارد",
  "فني يعمل داخل حوض محرك سيارة في ورشة صيانة لتوضيح فحص الإشعال والهواء والتغذية"
 ]
},
{
 "slug":"car-low-beam-headlights-not-working-high-beam-works",
 "file":"data/editorial/car-low-beam-not-working-high-beam-works-20261102.html",
 "title":"النور الواطي مش شغال والعالي شغال؟ أسباب الفيوز واللمبة والريلاي وطريقة الفحص",
 "excerpt":"العالي شغال والواطي فاصل في العربية؟ دليل تشخيص لمبة الواطي والفيوز والريلاي والمفتاح والضفيرة، مع الفرق بين الهالوجين وفوانيس LED.",
 "focus":"النور الواطي مش شغال والعالي شغال",
 "category":"كهربا",
 "checks":["النور الواطي","الريلاي","فيوز","{{a3tal_image:detail}}"],
 "dedup":["النور الواطي مش شغال","low beam headlight high beam works"],
 "photo":[
   [("Car headlamp.JPG","Prabhupuducherry","CC BY-SA 3.0"),("Headlight of a Soviet car.jpg","Dmitry Makeev","CC BY-SA 4.0")],
   [("045 Replacing car headlight bulb - HIR2 type 12V halogen lightbulb for Toyota Auris.jpg","Marek Ślusarczyk (Tupungato)","CC BY 3.0"),("Headlight of a Soviet car.jpg","Dmitry Makeev","CC BY-SA 4.0")]
 ],
 "alt":[
  "فانوس سيارة حقيقي يوضح موضع إضاءة النور الواطي والعالي أثناء فحص أعطال الكهرباء",
  "صورة حقيقية لقطعة لمبة هالوجين خاصة بفوانيس السيارات لتوضيح فحص الواطي دون خلطه بنظام LED"
 ]
}
]
CATEGORY_FALLBACK=3028

def request(path,protected=False,data=None,timeout=240):
    headers={"Accept":"application/json","User-Agent":"A3tal-3-Deep-Diagnostic-Guides/20261102","Cache-Control":"no-cache,no-store"}
    if protected:
        if not KEY:raise RuntimeError("Missing GitHub Actions A3TAL_API_KEY")
        headers["X-A3tal-Key"]=KEY
        headers["Authorization"]="Bearer "+KEY
    raw=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf-8")
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request((API if protected else SITE)+path,headers=headers,data=raw,method="POST" if raw is not None else "GET")
    with urllib.request.urlopen(req,timeout=timeout) as f:return json.load(f)

def check_existing(item):
    rows=request("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":item["slug"],"_fields":"id,slug,link,status,featured_media,content"}))
    if len(rows)>1:raise RuntimeError("Duplicate slug: "+item["slug"])
    if rows:
        p=rows[0]
        if p.get("status")=="publish" and p.get("featured_media") and "a3tal_image" not in (p.get("content") or {}).get("rendered",""):
            print("ALREADY_LIVE_VERIFIED",p["id"],p["link"],flush=True)
            return p
        raise RuntimeError("Existing incomplete or draft slug: stop rather than duplicate")
    for term in item["dedup"]:
        results=request("/search-posts?"+urllib.parse.urlencode({"search":term,"limit":100}),protected=True)
        for p in results.get("items",[]):
            title=p.get("title","").casefold()
            if item["category"]=="عفشة" and ("بتعوم" in title and "العربية" in title):
                raise RuntimeError("Existing suspension float intent found: "+str(p))
            if item["category"]=="ميكانيكا" and ("نتش" in title and ("بارد" in title or "تسخين" in title)):
                raise RuntimeError("Existing cold-start hesitation intent found: "+str(p))
            if item["category"]=="كهربا" and ("واطي" in title and "عالي" in title and "نور" in title):
                raise RuntimeError("Existing low beam intent found: "+str(p))
    return None

def load_commons_photo(choices):
    for filename,author,license in choices:
        name=urllib.parse.quote(filename,safe="")
        urls=[
          "https://commons.wikimedia.org/wiki/Special:Redirect/file/"+name+"?width=1920",
          "https://commons.wikimedia.org/wiki/Special:FilePath/"+name+"?width=1920",
          "https://commons.wikimedia.org/wiki/Special:Redirect/file/"+name
        ]
        for url in urls:
            try:
                headers={"User-Agent":"A3talEditorial/1.0 (https://a3tal.com; editorial photo reuse with credit)","Accept":"image/webp,image/jpeg,image/png,image/*"}
                with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=60) as f:
                    raw=f.read(20_000_000)
                if not 22_000<len(raw)<20_000_000:continue
                with Image.open(io.BytesIO(raw)) as original:
                    original.load()
                    if original.width<1000 or original.height<750:continue
                    image=ImageOps.exif_transpose(original).convert("RGB")
                    print("LICENSED_IMAGE",filename,image.size,author,license,flush=True)
                    return image,filename,author,license
            except Exception as ex:
                print("PHOTO_SOURCE_RETRY",filename,type(ex).__name__,flush=True)
    raise RuntimeError("No suitable licensed article-specific image found. Publication stopped.")

def make_photo(item,role,choices,target,alt):
    im,filename,author,license=load_commons_photo(choices)
    width,height=target
    # Model-created editorial 16:9 / 5:3 composition from photo with cautious sharpening,
    # cinematic color grading, and a subtle attribution-compatible site mark. No fake mechanical fault.
    out=ImageOps.fit(im,target,method=Image.Resampling.LANCZOS,centering=(0.5,0.48))
    out=ImageEnhance.Contrast(out).enhance(1.055)
    out=ImageEnhance.Color(out).enhance(.98)
    out=ImageEnhance.Sharpness(out).enhance(1.08)
    canvas=out.convert("RGBA")
    overlay=Image.new("RGBA",target,(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    d.rounded_rectangle((width-178,height-56,width-21,height-17),radius=9,fill=(8,19,34,139))
    try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",17)
    except OSError:font=ImageFont.load_default()
    d.text((width-162,height-47),"A3tal.com",fill=(255,255,255,242),font=font)
    final=Image.alpha_composite(canvas,overlay).convert("RGB")
    binary=io.BytesIO()
    final.save(binary,"WEBP",quality=85,method=6)
    raw=binary.getvalue()
    if not 30_000<len(raw)<2_500_000:raise RuntimeError("Generated WebP size invalid")
    source="https://commons.wikimedia.org/wiki/File:"+urllib.parse.quote(filename.replace(" ","_"),safe="_().")
    caption=("صورة توضيحية حقيقية لمكونات السيارات وليست تصويرًا لسيارة القارئ أو تشخيصًا مؤكدًا. "
             "المصور: "+author+"؛ الرخصة: "+license+"؛ قص وتعديل لوني مخصص لأعطال.كوم. المصدر: "+source)
    return {"key":role,"role":"featured" if role=="cover" else "inline",
            "filename":"a3tal-"+item["slug"]+"-"+role+"-exclusive.webp",
            "image_base64":base64.b64encode(raw).decode("ascii"),"convert_webp":False,
            "alt":alt,"caption":caption,"placeholder":"{{a3tal_image:detail}}"}

def publish(item):
    source=Path(item["file"]).read_text("utf-8").strip()
    if len(source)<7300 or source.count("<h2>")<8 or source.count("<h3>")<5 or source.count("<table")<1:
        raise RuntimeError("Editorial quality guard failed for "+item["slug"])
    for term in item["checks"]:
        if term not in source:raise RuntimeError("Fact/intent guard failed "+term)
    existing=check_existing(item)
    if existing:return
    cover=make_photo(item,"cover",item["photo"][0],(1600,900),item["alt"][0])
    detail=make_photo(item,"detail",item["photo"][1],(1400,840),item["alt"][1])
    slug=item["slug"];canonical=SITE+"/"+slug+"/"
    # Existing automotive diagnostics belong in the WordPress posts system.
    # Category 3028 is motorcycles, so DO NOT assign it to car posts.
    # Select the site's actual automotive repair/suspension/mechanics/electrical taxonomy from live REST.
    cats=request("/wp-json/wp/v2/categories?per_page=100&search="+urllib.parse.quote(item["category"]))
    matches=[c for c in cats if c.get("name","").find(item["category"])>=0 and c.get("count",0)>0]
    # Prefer exact diagnostic category, not broad or incidental product pages.
    cat_id=int(matches[0]["id"]) if matches else 0
    if not cat_id:raise RuntimeError("Could not confirm relevant automotive category for "+item["category"])
    payload={
      "title":item["title"],"slug":slug,"type":"post","status":"publish",
      "content":source,"excerpt":item["excerpt"],"categories":[cat_id],
      "meta":{
        "_yoast_wpseo_title":item["title"]+" | أعطال.كوم",
        "_yoast_wpseo_metadesc":item["excerpt"],
        "_yoast_wpseo_focuskw":item["focus"],
        "_yoast_wpseo_canonical":canonical,
        "_yoast_wpseo_opengraph-title":item["title"],
        "_yoast_wpseo_opengraph-description":item["excerpt"],
        "_yoast_wpseo_twitter-title":item["title"],
        "_yoast_wpseo_twitter-description":item["excerpt"]
      }
    }
    try:
        result=request("/publish-bundle",protected=True,data={"post":payload,"media":[cover,detail]},timeout=300)
    except (TimeoutError,urllib.error.URLError) as ex:
        print("AMBIGUOUS_WRITE_VERIFY_ONLY",slug,type(ex).__name__,flush=True)
        rows=request("/wp-json/wp/v2/posts?"+urllib.parse.urlencode({"slug":slug,"_fields":"id,slug,status,featured_media,link"}))
        if len(rows)!=1 or rows[0].get("status")!="publish" or not rows[0].get("featured_media"):raise
        result={"post":rows[0]}
    p=result.get("post") or {}
    if p.get("slug")!=slug or p.get("status")!="publish" or not p.get("featured_media"):
        raise RuntimeError("Bridge did not confirm published post and featured image")
    verification=request("/wp-json/wp/v2/posts/"+str(p["id"])+"?"+urllib.parse.urlencode({"_fields":"id,slug,status,link,featured_media,content,categories,yoast_head_json"}))
    seo=verification.get("yoast_head_json") or {}
    og=(seo.get("og_image") or [{}])[0].get("url","")
    content=(verification.get("content") or {}).get("rendered","")
    if (verification.get("link")!=canonical or verification.get("status")!="publish"
        or cat_id not in verification.get("categories",[]) or not verification.get("featured_media")
        or "{{a3tal_image" in content or "-detail-exclusive" not in content
        or "-cover-exclusive" not in og or seo.get("canonical")!=canonical
        or (seo.get("robots") or {}).get("index")=="noindex"):
        raise RuntimeError("Failed live article media or SEO checks "+slug)
    print("PUBLISHED_VERIFIED",p["id"],canonical,"CATEGORY",cat_id,
          "FEATURED",verification["featured_media"],"OG_IMAGE",og,flush=True)

def main():
    if not KEY:raise RuntimeError("Missing scoped A3tal Direct Bridge credential")
    for item in POSTS:publish(item)
    print("THREE_CAR_REPAIR_GUIDES_COMPLETE",flush=True)
if __name__=="__main__":main()
