#!/usr/bin/env python3
"""A3tal third 50-post editorial audit: source-backed Chery Arrizo 8 and Castrol EDGE prices.
No new URL, no automatic deletion or changed photos, update Chery's linked car price card
under A3tal Direct Bridge with meta preflight, preserve Yoast/index/OG identity.
Verified 2026-11-14 against Chery Egypt / Hatla2ee / Castrol Egypt / Egyptian sellers.
"""
import importlib.util,re,time,urllib.parse
m=importlib.util.spec_from_file_location("b","scripts/review-human-seo-geo-egypt-three-20261114.py")
b=importlib.util.module_from_spec(m);m.loader.exec_module(b)

DATA=[
{"id":82853,"slug":"chery-arrizo-8-egypt-review-price-specs","rev":"2026-10-01T22:33:07","cover":82871,
"title":"شيري أريزو 8 2026 في مصر: السعر الجديد والفئات والمواصفات",
"seo":"سعر شيري أريزو 8 2026 في مصر بعد الزيادة | أعطال",
"desc":"سعر شيري أريزو 8 2026 في مصر من 1,320,000 جنيه لفئة Luxury و1,400,000 جنيه لفئة Flagship بعد زيادة 22 أكتوبر، مع مواصفات المحرك 197 حصان وفتيس Wet DCT.",
"kw":"سعر شيري أريزو 8 2026",
"kind":"chery"},
{"id":80349,"slug":"saeer-zayt-kastrol-5w30-masr-2026","rev":"2026-09-20T16:27:59","cover":80351,
"title":"سعر زيت كاسترول EDGE 5W-30 في مصر: مقارنة عبوة 4 لتر",
"seo":"سعر زيت كاسترول EDGE 5W-30 مصر 2026 | أعطال",
"desc":"سعر Castrol EDGE 5W-30 A5/B5 عبوة 4 لتر في مصر بين عروض متاجر مختلفة؛ تحقق من SKU والمواصفة، وتعرّف على فرق أسعار سبتمبر ونوفمبر.",
"kw":"سعر زيت كاسترول EDGE 5W-30",
"kind":"castrol"}
]
MARK="a3tal-third50-pricing-20261114"

def getmeta(id,key):
   q=urllib.parse.urlencode({"op":"post_meta","post_id":id,"key":key})
   d=b.req("/admin?"+q)
   if not d.get("ok"):raise RuntimeError("Cannot read model meta before update")
   return str((d.get("result") or {}).get(key,"")).strip()

def guard(t,post,pub):
    if (int(post.get("id",0)),post.get("slug"),post.get("type"),post.get("status"),int(post.get("featured_media") or 0))!=(
       t["id"],t["slug"],"post","publish",t["cover"]):
       raise RuntimeError("Article or cover changed since human audit "+t["slug"])
    if not post["modified_gmt"].startswith(t["rev"]):raise RuntimeError("Price article edited concurrently")
    yo=pub.get("yoast_head_json") or {}
    if yo.get("canonical")!=b.SITE+"/"+t["slug"]+"/" or (yo.get("robots") or {}).get("index")=="noindex" or not yo.get("og_image"):
       raise RuntimeError("Yoast canonical/index/OG unexpected")
    return yo

def revised_chery(raw):
    if "1,300,000" not in raw or "1.3 مليون" not in raw:
       raise RuntimeError("Original Arrizo 8 prices differ")
    new=raw.replace("1,300,000","1,320,000").replace("1.3 مليون","1.32 مليون")
    if "آخر تحقق 1 أكتوبر 2026" in new:
       new=new.replace("آخر تحقق 1 أكتوبر 2026","آخر تحقق 14 نوفمبر 2026، والسعر ساري منذ 22 أكتوبر 2026",1)
    label='<section id="'+MARK+'-chery" dir="rtl"><p><strong>تحديث الأسعار 14 نوفمبر 2026:</strong> يبدأ السعر المنشور على <a href="https://www.chery-eg.com/ar/on-ground" rel="noopener noreferrer">موقع شيري مصر الرسمي</a> لشيري أريزو 8 من <strong>1,320,000 جنيه</strong> لفئة Luxury. وتسجل <a href="https://eg.hatla2ee.com/ar/new-car/chery/Arrizo-8" rel="noopener noreferrer">قائمة الفئات وتغييرات الأسعار المنشورة في 22 أكتوبر 2026</a> فئة Flagship عند <strong>1,400,000 جنيه</strong>، بعد زيادة 20 ألف جنيه على كل فئة من قائمة أبريل. هذه أسعار فئات الوكيل وليست أسعار معارض أو مستعمل.</p><div style="overflow-x:auto"><table><thead><tr><th>فئة شيري أريزو 8 موديل 2026</th><th>السعر بعد 22 أكتوبر</th></tr></thead><tbody><tr><td>Luxury</td><td>1,320,000 جنيه</td></tr><tr><td>Flagship</td><td>1,400,000 جنيه</td></tr></tbody></table></div><p>قبل الحجز تأكد من سنة الموديل والفئة والتوافر وعرض تسليم مؤرخ؛ وهذه الأسعار لا تعني ثبات السوق بعد تاريخ المراجعة. <a href="https://a3tal.com/cars/chery-arrizo-8-egypt/">ملف المواصفات المنظم للموديل</a> مرتبط بهذا المقال ويعرض سعر البداية بعد تحديثه.</p></section>\n'
    return label+new

def revised_castrol(raw):
    if "2,500" not in raw or "سبتمبر 2026" not in raw:
       raise RuntimeError("Castrol original price/time differ")
    # Preserve dated old comparison as historical and add exact seller, pack, spec,
    # rather than rename nonidentical stock formulations 'official price'.
    lead='<section id="'+MARK+'-castrol" dir="rtl"><p><strong>تحديث أسعار 14 نوفمبر 2026:</strong> لا تعلن <a href="https://www.castrol.com/en_eg/egypt/home/products/our-brands/automotive/edge.html" rel="noopener noreferrer">Castrol Egypt</a> سعر تجزئة موحد لعبوة EDGE 5W-30 A5/B5. عند مراجعة العروض ظهرت عبوة <strong>4 لترات</strong> بسعر <strong>2,400 جنيه</strong> لدى <a href="https://zaytakonline.com/ar/products/zay-cast-edge-5w30-a5b5-4l" rel="noopener noreferrer">زيتك أونلاين</a>، بينما يسرد <a href="https://nacitaautocare.com/products/edge-5w-30-a5-b5-4l-advanced-full-synthetic-sp" rel="noopener noreferrer">NACITA Auto Care</a> منتجًا باسم EDGE 5W-30 A5/B5 4L بصيغة معلنة <strong>API SP</strong> بسعر <strong>2,875 جنيه</strong>. اختلاف المنتج أو الـSKU أو إصدار المواصفة قد يمنع المقارنة المباشرة، لذلك افحص بيانات العبوة قبل شراء الأرخص.</p><div style="overflow-x:auto"><table><thead><tr><th>المنتج والبائع وقت المراجعة</th><th>السعة</th><th>سعر العرض</th><th>تنبيه</th></tr></thead><tbody><tr><td>Castrol EDGE 5W-30 A5/B5 لدى زيتك أونلاين</td><td>4 لتر</td><td>2,400 جنيه</td><td>اعرض SKU/الصيغة عند الشراء</td></tr><tr><td>Castrol EDGE 5W-30 A5/B5 Advanced Full Synthetic-SP لدى NACITA</td><td>4 لتر</td><td>2,875 جنيه</td><td>تسمية API SP ظاهرة في عرض البائع؛ قارن بالصورة والملصق</td></tr></tbody></table></div><p>سعر 2,500 جنيه المذكور في مراجعة سبتمبر رقم تاريخي وليس السعر الرسمي الحالي. المواصفات الرسمية المنشورة لفئة 5W-30 A5/B5 تشمل <strong>API SN وACEA A5/B5 وSTJLR.03.5003</strong> بحسب صفحة Castrol Egypt؛ لا تعتبر مواصفات بائع مختلف موافقةً بديلة للمصنع. <a href="https://a3tal.com/engine-oil-viscosity-egypt-summer-5w30-vs-20w50/">اختيار اللزوجة الصحيحة</a> يبدأ من كتيب السيارة.</p></section>\n'
    text=raw.replace("أحدث سعر سوق منشور في مصر خلال سبتمبر 2026","سعر تقريبي قديم منشور في سبتمبر 2026").replace("الخلاصة – سبتمبر 2026","ملخص الأسعار التاريخية – سبتمبر 2026")
    return lead+text

def update_article(t,old,pub,new):
    fresh=b.bridge_post(t["id"])
    if fresh["modified_gmt"]!=old["modified_gmt"] or fresh["content"]!=old["content"]:
        raise RuntimeError("Concurrent article edit")
    meta={"_yoast_wpseo_title":t["seo"],"_yoast_wpseo_metadesc":t["desc"],"_yoast_wpseo_focuskw":t["kw"],
          "_yoast_wpseo_opengraph-title":t["seo"],"_yoast_wpseo_opengraph-description":t["desc"],
          "_yoast_wpseo_twitter-title":t["seo"],"_yoast_wpseo_twitter-description":t["desc"]}
    try:
        b.req("/update-post",{"id":t["id"],"expected_modified_gmt":fresh["modified_gmt"],"title":t["title"],"content":new,"meta":meta})
    except Exception as ex:
        if MARK+"-"+t["kind"] not in b.bridge_post(t["id"])["content"]:
            raise RuntimeError("Price update unconfirmed; do not retry") from ex
    after=b.bridge_post(t["id"]);seo=b.public_post(t["id"])["yoast_head_json"]
    if (after["slug"],after["status"],after["title"],int(after.get("featured_media") or 0))!=(
       t["slug"],"publish",t["title"],t["cover"]):
       raise RuntimeError("Price update article identity/cover drift")
    if after["content"].count('id="'+MARK+"-"+t["kind"]+'"')!=1:
       raise RuntimeError("Price note not saved")
    if seo["canonical"]!=pub["yoast_head_json"]["canonical"] or (
       seo.get("robots") or {}).get("index")=="noindex" or seo.get("description")!=t["desc"]:
       raise RuntimeError("Canonical/meta SEO failed")
    if seo.get("og_image", [{}])[0].get("url")!=pub["yoast_head_json"].get("og_image",[{}])[0].get("url"):
       raise RuntimeError("Original featured OG image changed")
    print("THIRD50_PRICE_LIVE_VERIFIED",t["id"],after["link"],flush=True)

def main():
    plan=[]
    for t in DATA:
      old=b.bridge_post(t["id"]);pub=b.public_post(t["id"])
      if MARK+"-"+t["kind"] in old.get("content",""):
         print("THIRD50_ALREADY",t["slug"],flush=True);continue
      guard(t,old,pub)
      body=revised_chery(old["content"]) if t["kind"]=="chery" else revised_castrol(old["content"])
      if (len(re.findall(r"<img\b",body,re.I))!=len(re.findall(r"<img\b",old["content"],re.I)) or
         body.count('id="'+MARK+"-"+t["kind"]+'"')!=1):
         raise RuntimeError("Media/unique update protection failed")
      plan.append((t,old,pub,body))
      print("THIRD50_PRICE_PREFLIGHT",t["id"],len(old["content"]),len(body),flush=True)
    car=b.bridge_post(83191)
    if (int(car.get("id",0)),car.get("slug"),car.get("type"),car.get("status"),int(car.get("featured_media") or 0))!=(
        83191,"chery-arrizo-8-egypt","a3_car","publish",82871):
        raise RuntimeError("Linked Chery model identity changed")
    pmin=getmeta(83191,"_a3_price_min")
    pmax=getmeta(83191,"_a3_price_max")
    print("ARRIZO8_MODEL_PRICE_BEFORE",pmin,pmax,flush=True)
    if pmin not in ("1300000","1320000") or pmax not in ("","1300000","1380000","1400000"):
       raise RuntimeError("Unexpected linked car model pricing")
    print("THIRD50_ALL_PRICE_PREFLIGHTS_PASSED",len(plan),flush=True)
    for t,old,pub,new in plan:
       update_article(t,old,pub,new)
       time.sleep(1)
    # Only update the existing a3_car price record, never overwrite its
    # unrelated technical spec meta, featured image, taxonomy or slug.
    if pmin!="1320000" or pmax!="1400000":
       current=b.bridge_post(83191)
       if current["modified_gmt"]!=car["modified_gmt"] or getmeta(83191,"_a3_price_min")!=pmin or getmeta(83191,"_a3_price_max")!=pmax:
          raise RuntimeError("Chery model edited concurrently; stop")
       d=b.req("/admin",{"op":"platform_entity_upsert","type":"a3_car","id":83191,"slug":"chery-arrizo-8-egypt",
            "title":current["title"],"status":"publish",
            "meta":{"_a3_price_min":"1320000","_a3_price_max":"1400000"},"confirm":True,"dangerous":True})
       if not d.get("ok"):raise RuntimeError("Bridge rejected model price update")
       after=b.bridge_post(83191)
       if (after.get("slug"),after.get("type"),after.get("featured_media"))!=(
          "chery-arrizo-8-egypt","a3_car",82871):
          raise RuntimeError("Chery car ID/media changed")
       if getmeta(83191,"_a3_price_min")!="1320000" or getmeta(83191,"_a3_price_max")!="1400000":
          raise RuntimeError("Chery car prices did not persist")
       print("THIRD50_CHERY_CAR_CARD_VERIFIED",83191,"1320000","1400000",flush=True)
    print("A3TAL_THIRD50_PRICE_UPDATES_COMPLETE",flush=True)

if __name__=="__main__":main()
