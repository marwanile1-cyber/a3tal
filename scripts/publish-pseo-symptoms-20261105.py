#!/usr/bin/env python3
"""Publish 3 distinct A3tal diagnostic articles scoped to model + symptom.
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
    "slug": "nissan-sunny-n17-ac-weak-at-idle",
    "file": "data/editorial/pseo-20261105/nissan-sunny-n17-ac-weak-at-idle.html",
    "title": "تكييف نيسان صني N17 ضعيف وهي واقفة ويتحسن مع المشي؟ خطوات التشخيص",
    "excerpt": "ضعف تكييف صني N17 في الزحمة مقارنة بالسير: ازاي تفرق بين فلتر التكييف والمروحة والمكثف والفريون وتتأكد من السبب قبل تغيير الكمبروسر.",
    "focus": "تكييف نيسان صني ضعيف وهي واقفة",
    "category": "تكييف",
    "checks": [
      "المكثف",
      "نيسان صني N17",
      "{{a3tal_image:detail}}"
    ],
    "dedup": [
      "تكييف صني N17",
      "صني N17 تكييف الوقوف"
    ],
    "match": [
      "صني",
      "تكييف",
      "الوقوف"
    ],
    "photo": [
      [
        [
          "Nissan Sylphy B17 engine room.jpg",
          "TTTNIS",
          "Public domain"
        ],
        [
          "Car engine 01.jpg",
          "Azorbli",
          "CC BY-SA 4.0"
        ]
      ],
      [
        [
          "Car engine maintenance involves a mechanic inspecting and adjusting parts under the hood.jpg",
          "Shixart1985",
          "CC BY 2.0"
        ],
        [
          "Mechanic repairing car engine.jpg",
          "Bembety",
          "CC0"
        ]
      ]
    ],
    "alt": [
      "صورة حقيقية لمقصورة محرك من عائلة نيسان B17 لتوضيح فحص تبريد مكثف التكييف في الوقوف",
      "صورة توضيحية لفني يفحص محرك سيارة ومسار تبريد التكييف وليست توثيقًا لعطل سيارة بعينها"
    ]
  },
  {
    "slug": "opel-astra-j-battery-drains-overnight-diagnosis",
    "file": "data/editorial/pseo-20261105/opel-astra-j-battery-drains-overnight-diagnosis.html",
    "title": "بطارية أوبل أسترا J بتفضى بعد الركنة؟ فحص السحب الكهربائي قبل تغيير البطارية",
    "excerpt": "بطارية أوبل أسترا J تفضى بعد الركنة؟ خطوات قياس السحب بعد نوم وحدات السيارة وفحص الدينامو والإضافات قبل شراء بطارية جديدة.",
    "focus": "أوبل أسترا J البطارية بتفضى",
    "category": "كهربا",
    "checks": [
      "أسترا J",
      "السحب",
      "{{a3tal_image:detail}}"
    ],
    "dedup": [
      "أسترا J بطارية",
      "سحب كهرباء أسترا"
    ],
    "match": [
      "أسترا",
      "بطارية",
      "ركنة"
    ],
    "photo": [
      [
        [
          "Car battery.jpg",
          "Azorbli",
          "CC BY-SA 4.0"
        ],
        [
          "Auto mechanic checking old car battery voltage.jpg",
          "Shixart1985",
          "CC BY 2.0"
        ]
      ],
      [
        [
          "Mechanic working on a car battery.jpg",
          "Kwamitsey",
          "CC BY 4.0"
        ],
        [
          "Car battery.jpg",
          "Azorbli",
          "CC BY-SA 4.0"
        ]
      ]
    ],
    "alt": [
      "صورة توضيحية حقيقية لفحص بطارية سيارة قبل قياس استهلاك الكهرباء في أوبل أسترا J",
      "فني يفحص بطارية سيارة أثناء اختبار السحب الكهربائي بعد الركنة"
    ]
  },
  {
    "slug": "hyundai-accent-rb-battery-light-when-ac-on",
    "file": "data/editorial/pseo-20261105/hyundai-accent-rb-battery-light-when-ac-on.html",
    "title": "لمبة البطارية بتنور في هيونداي أكسنت RB مع تشغيل التكييف؟ تشخيص الشحن والسير والأرضي",
    "excerpt": "أسباب ظهور لمبة الشحن في أكسنت RB مع التكييف وكيف يفحص الفني الدينامو والسير والتوصيلات والبطارية تحت الحمل قبل تغيير القطع.",
    "focus": "لمبة البطارية أكسنت RB مع التكييف",
    "category": "كهربا",
    "checks": [
      "أكسنت RB",
      "الدينامو",
      "{{a3tal_image:detail}}"
    ],
    "dedup": [
      "أكسنت RB لمبة بطارية",
      "لمبة شحن أكسنت تكييف"
    ],
    "match": [
      "أكسنت",
      "لمبة",
      "بطارية"
    ],
    "photo": [
      [
        [
          "Mechanic repairing car engine.jpg",
          "Bembety",
          "CC0"
        ],
        [
          "Car engine 01.jpg",
          "Azorbli",
          "CC BY-SA 4.0"
        ]
      ],
      [
        [
          "Alternator.jpg",
          "Angelsharum",
          "CC BY-SA 3.0"
        ],
        [
          "Mechanic works on car engine performing routine maintenance and inspections on vehicle parts.jpg",
          "Shixart1985",
          "CC BY 2.0"
        ]
      ]
    ],
    "alt": [
      "صورة توضيحية لفني يفحص حوض محرك سيارة أثناء تشخيص عطل الشحن في هيونداي أكسنت RB",
      "صورة توضيحية لمولد شحن سيارة لفهم أجزاء منظومة الدينامو ولا تمثل قطعة مطابقة بالضرورة لأكسنت RB"
    ]
  }
]
CATEGORY_FALLBACK=3028

def request(path,protected=False,data=None,timeout=240):
    headers={"Accept":"application/json","User-Agent":"A3tal-PSEO-UniqueSymptoms/20261105","Cache-Control":"no-cache,no-store"}
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
            title=(p.get("title") or "").casefold()
            if all(word.casefold() in title for word in item["match"]):
                raise RuntimeError("Competing topic detected, needs editorial merge "+str(p)[:220])
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
    source=source.replace("<h2>أسئلة شائعة</h2>","<div class=\"a3tal-inline-photo\">{{a3tal_image:detail}}</div><h2>أسئلة شائعة</h2>",1)
    if len(source)<4200 or source.count("<h2>")<5 or source.count("<h3>")<3 or source.count("<table")<1:
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
    # Confirmed live A3tal WordPress IDs: 11 Suspension, 9 Engine problems, 13 Electrical.
    category_map={"عفشة":(11,"نظام التعليق"),"ميكانيكا":(9,"مشاكل المحرك"),"كهربا":(13,"أعطال كهربائية")}
    if item["category"]=="تكييف":
        cats=request("/wp-json/wp/v2/categories?"+urllib.parse.urlencode({"search":"تكييف","per_page":50}))
        matches=[cat for cat in cats if "تكييف" in cat.get("name","")]
        if len(matches)!=1:raise RuntimeError("Cannot uniquely resolve live AC category")
        cat_id,expected_name=int(matches[0]["id"]),"تكييف"
    else:
        cat_id,expected_name=category_map[item["category"]]
    cat=request("/wp-json/wp/v2/categories/"+str(cat_id))
    if expected_name not in cat.get("name",""):
        raise RuntimeError("Live automotive category mismatch; refusing taxonomy changes")
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
    print("PSEO_SYMPTOMS_NOV05_COMPLETE",flush=True)
if __name__=="__main__":main()
