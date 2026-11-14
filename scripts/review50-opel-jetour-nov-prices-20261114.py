#!/usr/bin/env python3
"""Update dated Opel Frontera and Jetour T2 price articles in A3tal Egypt.
Two independent manufacturer/agency price facts were checked 14 Nov 2026.
Preserve URL, existing historical price context, OG image and original media.
"""
import re,time,importlib.util

s=importlib.util.spec_from_file_location("base","scripts/review-human-seo-geo-egypt-three-20261114.py")
base=importlib.util.module_from_spec(s);s.loader.exec_module(base)

MARK="a3tal-human50-price-2-20261114"
ROWS=[
{"id":82603,"slug":"opel-frontera-price-specs-egypt","cover":82604,
 "mod":"2026-09-29T12:35:27","kind":"frontera",
 "title":"سعر أوبل فرونتيرا 2027 في مصر بعد زيادة أكتوبر: 1.28 مليون جنيه",
 "seo":"سعر أوبل فرونتيرا 2027 بعد زيادة أكتوبر | أعطال",
 "desc":"سعر أوبل فرونتيرا 2027 في مصر ارتفع إلى 1,280,000 جنيه من 27 أكتوبر، وفق قائمة المنصور. المواصفات والـ7 مقاعد والفروق قبل الشراء.",
 "kw":"سعر أوبل فرونتيرا 2027",
 "links":["https://a3tal.com/cars/opel-frontera-egypt/"],
 "note":'<section id="a3tal-human50-price-2-20261114-frontera" dir="rtl"><p><strong>آخر تحديث للسعر: 14 نوفمبر 2026.</strong> السعر الرسمي الأحدث لفئة <strong>أوبل فرونتيرا 2027 GS / Luxury</strong> ذات السبعة مقاعد هو <strong>1,280,000 جنيه مصري</strong> وفق قائمة <strong>المنصور للسيارات</strong> التي بدأ تطبيقها <strong>27 أكتوبر 2026</strong>، بعد زيادة 50 ألف جنيه على سعر سبتمبر البالغ 1,230,000 جنيه. هذا سعر رسمي للفئة، لا يشمل بالضرورة مصروفات الترخيص والتأمين.</p><p>مصادر التحديث: <a href="https://almalnews.com/2143667/" rel="noopener noreferrer">جريدة المال، 27 أكتوبر، نقلًا عن المنصور</a>، وصفحة <a href="https://eltawkeel.com/ar/car-info/84/opel/2027/frontera-2027" rel="noopener noreferrer">الحجز والمواصفات في منصة التوكيل</a>. يجب تأكيد سعر التسليم المكتوب لدى الوكيل قبل الحجز. <a href="https://a3tal.com/cars/opel-frontera-egypt/">بيانات موديل فرونتيرا المرتبطة على أعطال</a> قد تتطلب تحديثًا منفصلًا إذا بقي السعر القديم معروضًا بها.</p></section>'},
{"id":80325,"slug":"jetour-t2-2026-price-egypt-review","cover":80326,
 "mod":"2026-10-01T01:52:48","kind":"jetour",
 "title":"جيتور T2 2027 في مصر: أسعار الفئات البنزين وi-DM و4x4",
 "seo":"جيتور T2 2027: الأسعار والفئات وi-DM 4x4 | أعطال",
 "desc":"أسعار جيتور T2 2027 تبدأ من 1.9 مليون جنيه، وi-DM العادية 2.15 مليون، ونسخة i-DM 4x4 الجديدة 2.3 مليون جنيه وفق طرح نوفمبر.",
 "kw":"سعر جيتور T2 2027 في مصر",
 "links":["https://a3tal.com/jetour-t2-idm-4x4-2027-egypt-price-specs/"],
 "note":'<section id="a3tal-human50-price-2-20261114-jetour" dir="rtl"><p><strong>تحديث أسعار جيتور T2 موديل 2027 بتاريخ 14 نوفمبر 2026:</strong> فئة T2 Luxury البنزين من <strong>1,900,000 جنيه</strong>، وMatt Colour من <strong>1,930,000 جنيه</strong>، وفئة <strong>T2 i-DM العادية</strong> الهجينة القابلة للشحن بسعر <strong>2,150,000 جنيه</strong>، بينما أطلقت قصراوي نسخة <strong>T2 i-DM 4x4</strong> ذات الدفع الرباعي بسعر رسمي <strong>2,300,000 جنيه</strong> يوم 1 نوفمبر. اختلاف الـ150 ألف جنيه بين نسختي i-DM لا يعني ارتفاع سعر الفئة القديمة تلقائيًا، فالـ4x4 طراز مستقل من عائلة T2.</p><div style="overflow-x:auto"><table><thead><tr><th scope="col">فئة جيتور T2</th><th scope="col">السعر المرجعي الرسمي</th></tr></thead><tbody><tr><td>Luxury بنزين</td><td>1,900,000 جنيه</td></tr><tr><td>Matt Colour بنزين</td><td>1,930,000 جنيه</td></tr><tr><td>i-DM هجين 2WD</td><td>2,150,000 جنيه</td></tr><tr><td>i-DM 4x4 هجين ودفع رباعي</td><td>2,300,000 جنيه</td></tr></tbody></table></div><p>للمواصفات والفرق بين المنظومتين، اقرأ <a href="https://a3tal.com/jetour-t2-idm-4x4-2027-egypt-price-specs/">دليل جيتور T2 i-DM 4x4 المنشور بالفعل</a>. المصادر: <a href="https://almalnews.com/2144714/" rel="noopener noreferrer">إعلان قصراوي عن نسخة 4x4 في جريدة المال، 1 نوفمبر</a>، وصفحة <a href="https://www.contactcars.com/ar/new-cars/jetour-t2/63912fd6c896" rel="noopener noreferrer">فئات T2 الأربع على كونتكت كارز</a>. الأسعار قد تختلف يوم الحجز والتسليم؛ اطلب عرضًا مؤرخًا للفئة نفسها.</p></section>'}
]

def transform(row,old):
    if MARK+"-"+row["kind"] in old:return None
    if len(old)<1400 or not old.count("<h2"):
        raise RuntimeError("Original price article unexpectedly truncated")
    if row["kind"]=="frontera":
        if old.count("1,230,000")<3 or "40 ألف" not in old:
            raise RuntimeError("Expected historic Opel price context missing")
        # Apply new official price to contexts explicitly referring to Frontera
        # while preserving competitor MG G50's independent 1.23m value.
        def fixrow(m):
            snippet=m.group()
            if "أوبل فرونتيرا" in re.sub("<[^>]+>"," ",snippet) and "1,230,000" in snippet:
                return snippet.replace("1,230,000","1,280,000")
            return snippet
        temp,n=re.subn(r"<tr\b[^>]*>[\s\S]*?</tr>",fixrow,old,flags=re.I)
        old=temp
        old=old.replace("السعر الرسمي الحالي","السعر الرسمي الحالي حسب قائمة 27 أكتوبر",1)
        # Historical lines remain historical, rather than silently rewired.
        old=old.replace("ارتفع السعر الرسمي من 1,190,000 إلى <strong>1,230,000 جنيه</strong>، أي زيادة قدرها 40 ألف جنيه.",
                        "ارتفع السعر أولًا من 1,190,000 إلى 1,230,000 جنيه خلال سبتمبر (+40 ألف)، ثم زاد إلى <strong>1,280,000 جنيه</strong> في 27 أكتوبر (+50 ألف).",1)
        # Target current-only prose, not older source quotations.
        old=old.replace("السعر الرسمي المعلن بعد زيادة 27 سبتمبر هو 1,230,000 جنيه للفئة المتاحة",
                        "السعر الرسمي الأحدث في 27 أكتوبر هو 1,280,000 جنيه، بعدما كان 1,230,000 جنيه في سبتمبر للفئة المتاحة",1)
        old=old.replace("أحدث زيادة معلنة رفعت السعر الرسمي إلى 1.23 مليون جنيه",
                        "زيادة سبتمبر رفعت السعر إلى 1.23 مليون، ثم رفعته قائمة 27 أكتوبر إلى 1.28 مليون جنيه",1)
        old=old.replace("سعر رسمي جديد 1.23 مليون جنيه",
                        "سعر رسمي جديد 1.28 مليون جنيه",1)
        old=old.replace("الزيادة رفعت سعر فرونتيرا بنسبة تقارب 3.4% فقط",
                        "كانت زيادة سبتمبر نحو 3.4%، وتبعتها زيادة 50 ألف جنيه في أكتوبر",1)
        old=old.replace("ماذا تحصل مقابل 1.23 مليون جنيه؟","ماذا تحصل مقابل 1.28 مليون جنيه؟",1)
        # Do not replace old MG G50 value.
        extra=old.count("1,280,000")
        if extra<2:raise RuntimeError("Expected current Opel table updated in source")
    else:
        if old.count("2,150,000")<2 or "5 سبتمبر 2026" not in old:
            raise RuntimeError("Expected verified T2 original prices/date differ")
        old=old.replace("آخر مراجعة للأسعار والمواصفات: 5 سبتمبر 2026",
                        "المراجعة الأصلية للمواصفات: 5 سبتمبر 2026، وتحديث الفئات والأسعار: 14 نوفمبر 2026",1)
    new=row["note"]+"\n"+old
    if len(re.findall("<img\\b",new,re.I))!=len(re.findall("<img\\b",row.get("old_original",old),re.I)):
        raise RuntimeError("Inline images changed unexpectedly")
    if new.count('id="'+MARK+"-"+row["kind"]+'"')!=1:
        raise RuntimeError("Missing unique revision marker")
    return new

def main():
    plans=[]
    for t in ROWS:
        old=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
        if MARK+"-"+t["kind"] in old.get("content",""):
            print("ALREADY_UPDATED",old["link"]);continue
        if (old.get("id"),old.get("slug"),old.get("status"),old.get("type"),int(old.get("featured_media") or 0))!=(t["id"],t["slug"],"publish","post",t["cover"]):
            raise RuntimeError("Post identity or media changed")
        if not old["modified_gmt"].startswith(t["mod"]):
            raise RuntimeError("Post changed since audited, stop")
        seo=pub.get("yoast_head_json") or {}
        if (seo.get("robots") or {}).get("index")=="noindex" or not seo.get("og_image"):
            raise RuntimeError("SEO before mutation not indexable")
        t["old_original"]=old["content"]
        revised=transform(t,old["content"])
        for u in t["links"]:
            if u not in revised:raise RuntimeError("Link not in sourced revision")
        plans.append((t,old,pub,revised))
        print("NOV_PRICES_EXTRA_PREFLIGHT",t["id"],"original",len(old["content"]),"updated",len(revised),flush=True)
    print("NOV_EXTRA_PRICE_PREFLIGHTS_DONE",len(plans),flush=True)
    for t,old,pub0,body in plans:
        now=base.bridge_post(t["id"])
        if now["modified_gmt"]!=old["modified_gmt"] or now["content"]!=old["content"]:
            raise RuntimeError("Concurrent revision detected")
        meta={"_yoast_wpseo_title":t["seo"],"_yoast_wpseo_metadesc":t["desc"],"_yoast_wpseo_focuskw":t["kw"],
              "_yoast_wpseo_opengraph-title":t["seo"],"_yoast_wpseo_opengraph-description":t["desc"],
              "_yoast_wpseo_twitter-title":t["seo"],"_yoast_wpseo_twitter-description":t["desc"]}
        try:
            base.req("/update-post",{"id":t["id"],"expected_modified_gmt":now["modified_gmt"],
                                     "content":body,"title":t["title"],"meta":meta})
        except Exception as ex:
            chk=base.bridge_post(t["id"])
            if MARK+"-"+t["kind"] not in chk.get("content",""):
                raise RuntimeError("Update unconfirmed, do not retry") from ex
        after=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
        seo=pub.get("yoast_head_json") or {}
        if (after["slug"],after["status"],int(after.get("featured_media") or 0))!=(t["slug"],"publish",t["cover"]):
            raise RuntimeError("Post slug/status/featured changed")
        if after["content"].count('id="'+MARK+"-"+t["kind"]+'"')!=1:
            raise RuntimeError("Sourced price note missing")
        if seo.get("canonical")!=pub0["yoast_head_json"].get("canonical") or (
            seo.get("robots") or {}).get("index")=="noindex" or seo.get("description")!=t["desc"]:
            raise RuntimeError("Yoast SEO changed unintentionally")
        if (seo.get("og_image") or [{}])[0].get("url")!=(
            pub0["yoast_head_json"].get("og_image") or [{}])[0].get("url"):
            raise RuntimeError("Original OG image changed")
        print("EXTRA_NOV_PRICE_LIVE_VERIFIED",t["id"],after["link"],flush=True)
        time.sleep(2)
    print("A3TAL_HUMAN50_NOV_PRICE_EXTRA_TWO_DONE",flush=True)
if __name__=="__main__":main()
