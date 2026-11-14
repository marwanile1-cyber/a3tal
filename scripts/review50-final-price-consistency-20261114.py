#!/usr/bin/env python3
"""Fix A3tal Egypt November car prices at actual publicly served canonical URLs.
(1) Frontera article price table vs opening note
(2) Canonical Jetour T2 article instead of its redirected historical duplicate
(3) Opel Frontera a3_car model price card visible on the article.
Only GitHub and A3tal Direct Bridge with optimistic revision checks.
"""
import importlib.util
import re
import time
import urllib.parse

spec=importlib.util.spec_from_file_location("base","scripts/review-human-seo-geo-egypt-three-20261114.py")
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
MARK="a3tal-20261114-final-price-consistency"

CARS_ID=83196
T2_ID=81139
OPEL_ID=82603

def meta_val(pid,key):
    d=base.req("/admin?"+urllib.parse.urlencode({"op":"post_meta","post_id":pid,"key":key}))
    if not d.get("ok"):
        raise RuntimeError("Cannot read protected post meta "+key)
    return str(d.get("result",{}).get(key,"")).strip()

def ensure_post(row,pid,slug,cover,expected_date):
    if (row.get("id"),row.get("slug"),row.get("status"),row.get("type"),
        int(row.get("featured_media") or 0))!=(pid,slug,"publish","post",cover):
        raise RuntimeError("Wrong article identity or featured media: "+slug)
    if not row["modified_gmt"].startswith(expected_date):
        raise RuntimeError("Concurrent post revision: "+slug)
    pub=base.public_post(pid);seo=pub.get("yoast_head_json") or {}
    if (seo.get("robots") or {}).get("index")=="noindex" or not seo.get("og_image"):
        raise RuntimeError("SEO state changed; refuse update")
    return pub

def correct_frontera(body):
    if MARK+"-opel" in body:return None
    if "a3tal-human50-price-2-20261114-frontera" not in body:
        raise RuntimeError("First sourced price note not published")
    matches=0
    def rowreplace(m):
        nonlocal matches
        snippet=m.group(0)
        plain=re.sub(r"<[^>]+>"," ",snippet)
        if "السعر الرسمي الحالي" in plain and "1,230,000" in plain:
            matches+=1
            return snippet.replace("1,230,000","1,280,000")
        return snippet
    body=re.sub(r"<tr\b[^>]*>[\s\S]*?</tr>",rowreplace,body,flags=re.I)
    if matches!=1:raise RuntimeError("Expected one outdated current-price table row, got "+str(matches))
    body=body.replace("بيانات موديل فرونتيرا المرتبطة على أعطال</a> قد تتطلب تحديثًا منفصلًا إذا بقي السعر القديم معروضًا بها.",
                      "بيانات موديل فرونتيرا المرتبطة على أعطال</a> تُراجَع أيضًا لعرض سعر القائمة الجديدة.",1)
    # Keep September 1,230,000 occurrences explicitly identified as historical,
    # and keep the independent MG G50 Plus competitor price.
    body='<p id="'+MARK+'-opel"><strong>تاريخ المقارنة:</strong> أرقام سبتمبر مذكورة أدناه بوصفها أسعارًا سابقة؛ سعر فرونتيرا الرسمي المرجعي في 27 أكتوبر هو 1,280,000 جنيه.</p>\n'+body
    if "1,280,000" not in body:raise RuntimeError("Current price absent")
    return body

def correct_canonical_t2(body):
    if MARK+"-jetour" in body:return None
    if body.count("2,150,000")<1 or len(body)<3500:
        raise RuntimeError("Canonically published T2 article unexpected")
    latest='<section id="'+MARK+'-jetour" dir="rtl"><p><strong>تحديث 14 نوفمبر 2026 لأسعار جيتور T2 في مصر:</strong> تتوافر T2 Luxury البنزين من 1,900,000 جنيه، وMatt Colour من 1,930,000 جنيه، ونسخة <strong>T2 i-DM الهجينة العادية 2WD</strong> من 2,150,000 جنيه. وأطلق الوكيل قصراوي يوم <strong>1 نوفمبر 2026</strong> فئة منفصلة جديدة اسمها <strong>T2 i-DM 4x4</strong> بسعر رسمي <strong>2,300,000 جنيه</strong>. لا تخلط الـ4x4 مع i-DM الدفع الأمامي الموجودة في الجدول الأقدم أدناه؛ الفارق 150 ألف جنيه مقابل تجهيزات دفع وبطارية مختلفة.</p><div style="overflow-x:auto"><table><thead><tr><th>الفئة</th><th>السعر الرسمي بالجنيه</th></tr></thead><tbody><tr><td>Luxury بنزين</td><td>1,900,000</td></tr><tr><td>Matt Colour بنزين</td><td>1,930,000</td></tr><tr><td>i-DM 2WD</td><td>2,150,000</td></tr><tr><td>i-DM 4x4</td><td>2,300,000</td></tr></tbody></table></div><p>راجع <a href="https://a3tal.com/jetour-t2-idm-4x4-2027-egypt-price-specs/">مواصفات ومقارنة فئة جيتور T2 i-DM 4x4 المفصلة</a> بدل تكرار مقال مستقل عنها في هذه الصفحة. المصدر: <a href="https://almalnews.com/2144714/" rel="noopener noreferrer">جريدة المال عن إعلان قصراوي في 1 نوفمبر 2026</a>، و<a href="https://www.contactcars.com/ar/new-cars/jetour-t2/63912fd6c896" rel="noopener noreferrer">أسعار فئات T2 الأربع لدى كونتكت كارز</a>. الأسعار تخص الفئات المذكورة وتخضع لتأكيد سعر التسليم لدى الوكيل.</p></section>'
    body=body.replace("آخر مراجعة للأسعار والمواصفات: 5 سبتمبر 2026","المراجعة الأصلية للمواصفات: 5 سبتمبر 2026، وتحديث الفئات: 14 نوفمبر 2026",1)
    return latest+"\n"+body

def main():
    opel=base.bridge_post(OPEL_ID);opub=ensure_post(opel,OPEL_ID,"opel-frontera-price-specs-egypt",82604,"2026-11-14T16:13:43")
    t2=base.bridge_post(T2_ID);tpub=ensure_post(t2,T2_ID,"jetour-t2-egypt-review-specs-price",81140,"2026-10-02T00:54:45")
    vehicle=base.bridge_post(CARS_ID)
    if (vehicle.get("id"),vehicle.get("type"),vehicle.get("slug"),vehicle.get("status"),int(vehicle.get("featured_media") or 0))!=(
         CARS_ID,"a3_car","opel-frontera-egypt","publish",82604):
         raise RuntimeError("Opel linked model record changed unexpectedly")
    price=meta_val(CARS_ID,"_a3_price_min")
    price_max=meta_val(CARS_ID,"_a3_price_max")
    print("MODEL_PRICE_PREFLIGHT",price,price_max,flush=True)
    if price not in ("1230000","1280000"):
        raise RuntimeError("Unexpected original Opel model reference price: "+price)
    if price_max and price_max not in ("1230000","1280000"):
        raise RuntimeError("Unexpected Opel max-price state: "+price_max)
    opel_updated=correct_frontera(opel["content"])
    t2_updated=correct_canonical_t2(t2["content"])
    for before,after in ((opel["content"],opel_updated),(t2["content"],t2_updated)):
        if after is not None and len(re.findall(r"<img\b",before,re.I))!=len(re.findall(r"<img\b",after,re.I)):
            raise RuntimeError("Original inline image count changed")
    print("ACTUAL_CANONICAL_PRICE_PRECHECKS_PASSED",int(opel_updated is not None),int(t2_updated is not None),flush=True)
    for t,old,pub,body,seo_title,desc in [
      (OPEL_ID,opel,opub,opel_updated,
       "سعر أوبل فرونتيرا 2027 بعد زيادة أكتوبر | أعطال",
       "سعر أوبل فرونتيرا 2027 في مصر ارتفع إلى 1,280,000 جنيه من 27 أكتوبر، وفق قائمة المنصور. المواصفات والـ7 مقاعد والفروق قبل الشراء."),
      (T2_ID,t2,tpub,t2_updated,
       "جيتور T2 2027: الفئات والأسعار ونسخة i-DM 4x4 | أعطال",
       "جيتور T2 2027 من 1.9 مليون، وi-DM من 2.15 مليون، وi-DM 4x4 الجديدة من 2.3 مليون جنيه وفق طرح قصراوي نوفمبر 2026.")
    ]:
        if body is None:
            print("ALREADY_VERIFIED",old.get("link"),flush=True);continue
        now=base.bridge_post(t)
        if now["modified_gmt"]!=old["modified_gmt"] or now["content"]!=old["content"]:
            raise RuntimeError("Concurrent post revision, abort")
        meta={"_yoast_wpseo_title":seo_title,"_yoast_wpseo_metadesc":desc,
              "_yoast_wpseo_opengraph-title":seo_title,
              "_yoast_wpseo_opengraph-description":desc,
              "_yoast_wpseo_twitter-title":seo_title,
              "_yoast_wpseo_twitter-description":desc}
        try:
            base.req("/update-post",{"id":t,"expected_modified_gmt":now["modified_gmt"],"content":body,"meta":meta})
        except Exception as e:
            confirm=base.bridge_post(t)
            if MARK not in confirm.get("content",""):
                raise RuntimeError("No write confirmation; stop") from e
        after=base.bridge_post(t);p=base.public_post(t);seo=p.get("yoast_head_json") or {}
        if after.get("slug")!=old["slug"] or after.get("status")!="publish" or after.get("featured_media")!=old.get("featured_media"):
            raise RuntimeError("Identity/media unexpectedly modified")
        if seo.get("canonical")!=pub["yoast_head_json"].get("canonical") or (
           seo.get("robots") or {}).get("index")=="noindex":
            raise RuntimeError("SEO canonical or robots changed")
        if (seo.get("og_image") or [{}])[0].get("url")!=(
            pub["yoast_head_json"].get("og_image") or [{}])[0].get("url"):
            raise RuntimeError("OG feature image changed")
        if MARK not in after["content"]:raise RuntimeError("Correction marker not published")
        print("ACTUAL_CANONICAL_ARTICLE_VERIFIED",t,after["link"],flush=True)
        time.sleep(1)
    # Update the model price source, not just the article. Use API pre-read
    # and preservation of title, slug, featured image, and post type.
    if price=="1230000" or (price_max=="1230000"):
        nowcar=base.bridge_post(CARS_ID)
        if nowcar.get("modified_gmt")!=vehicle.get("modified_gmt") or (
          meta_val(CARS_ID,"_a3_price_min")!=price or
          meta_val(CARS_ID,"_a3_price_max")!=price_max):
          raise RuntimeError("Model price or body edited concurrently, stop")
        result=base.req("/admin",{"op":"platform_entity_upsert","id":CARS_ID,
          "type":"a3_car","slug":"opel-frontera-egypt","title":nowcar["title"],
          "status":"publish","meta":{"_a3_price_min":"1280000","_a3_price_max":"1280000"},
          "confirm":True,"dangerous":True})
        if result.get("ok") is False:raise RuntimeError("Bridge refused model price upsert")
        aftercar=base.bridge_post(CARS_ID)
        if (aftercar.get("id"),aftercar.get("slug"),aftercar.get("type"),aftercar.get("featured_media"))!=(
          CARS_ID,"opel-frontera-egypt","a3_car",82604):
          raise RuntimeError("Model identity/featured image changed")
        if meta_val(CARS_ID,"_a3_price_min")!="1280000" or meta_val(CARS_ID,"_a3_price_max")!="1280000":
          raise RuntimeError("Opel model price didn't persist")
        print("OPEL_FRONTERA_MODEL_CARD_PRICE_VERIFIED",CARS_ID,"1280000",flush=True)
    print("A3TAL_CANONICAL_PRICE_CONSISTENCY_FINISHED",flush=True)

if __name__=="__main__":main()
