#!/usr/bin/env python3
"""Evidence-backed, revision-locked November 2026 price corrections of three existing Egypt posts.
Sources checked on 2026-11-14: Hyundai/GB price list reported by Al-Mal/Ahram,
Nissan November list corroborated by Masrawy/Youm7/Hatla2ee,
and MG Motors Egypt's own buying guide.
No new posts/URLs/categories/media, no speculative prices; preserve OG and inline images.
"""
import re,time,importlib.util

spec=importlib.util.spec_from_file_location("a3human","scripts/review-human-seo-geo-egypt-three-20261114.py")
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

MARK="a3tal-price-reviewed-20261114"
T=[
{"id":81359,"slug":"hyundai-elantra-ad-2027-price-egypt","cover":81360,"modified":"2026-10-02T00:24:02","kind":"elantra",
 "title":"سعر هيونداي إلنترا AD 2027 في مصر بعد زيادة نوفمبر: الفئات الأربع",
 "seo":"سعر هيونداي إلنترا AD 2027 بعد زيادة نوفمبر | أعطال",
 "desc":"أسعار هيونداي إلنترا AD 2027 في مصر بعد قائمة 5 نوفمبر: 1.06 و1.16 و1.175 و1.275 مليون جنيه للفئات الأربع، مع الفروق والمواصفات.",
 "kw":"سعر هيونداي إلنترا AD 2027",
 "replacements":[("1,020,000","1,060,000"),("1,120,000","1,160,000"),("1,135,000","1,175,000"),("1,235,000","1,275,000"),("1.020","1.060"),("1.120","1.160"),("1.135","1.175"),("1.235","1.275")],
 "intro":'<section id="a3tal-price-reviewed-20261114-elantra" dir="rtl"><p><strong>تحديث أسعار 14 نوفمبر 2026:</strong> وفق قائمة غبور المعلنة والسارية من 5 نوفمبر، تبدأ إلنترا AD موديل 2027 بفئة Baseline من <strong>1,060,000 جنيه</strong>، ثم Modern بسعر <strong>1,160,000 جنيه</strong>، وModern Sunroof بسعر <strong>1,175,000 جنيه</strong>، وأعلى فئة Topline بسعر <strong>1,275,000 جنيه</strong>. هذه أسعار الفئات الرسمية المنقولة عن قائمة الوكيل، وليست متوسط أسعار معارض أو أسعار سيارات مستعملة.</p><p><strong>المصدر والتاريخ:</strong> <a href="https://auto.ahram.org.eg/News/134204.aspx" rel="noopener noreferrer">الأهرام أوتو، قائمة غبور بتاريخ 5 نوفمبر 2026</a>، و<a href="https://almalnews.com/2146599/" rel="noopener noreferrer">المال، 11 نوفمبر 2026</a>. الأسعار قابلة للتغيير لدى الوكيل؛ اطلب عرضًا مكتوبًا بتاريخ الشراء.</p></section>'},
{"id":81836,"slug":"nissan-magnite-price-egypt","cover":81838,"modified":"2026-10-10T19:09:04","kind":"magnite",
 "title":"سعر نيسان ماجنايت 2027 في مصر بعد زيادة نوفمبر: أسعار الفئات",
 "seo":"سعر نيسان ماجنايت 2027 في مصر نوفمبر | أعطال",
 "desc":"أسعار نيسان ماجنايت 2027 في مصر بعد زيادة 4 نوفمبر: Visia بـ860 ألف وAcenta بـ910 آلاف وTekna بـ940 ألف وTekna+ بـ960 ألف جنيه.",
 "kw":"سعر نيسان ماجنايت 2027",
 "replacements":[("819,999","860,000"),("859,999","910,000"),("879,999","940,000"),("899,999","960,000")],
 "intro":'<section id="a3tal-price-reviewed-20261114-magnite" dir="rtl"><p><strong>تحديث سعر نيسان ماجنايت 2027 بتاريخ 14 نوفمبر:</strong> قائمة نيسان مصر الصادرة في <strong>4 نوفمبر 2026</strong> تضع الفئات الأربع عند <strong>860,000 جنيه Visia</strong>، و<strong>910,000 جنيه Acenta</strong>، و<strong>940,000 جنيه Tekna</strong>، و<strong>960,000 جنيه Tekna+</strong>. الأسعار التالية تعكس قائمة نوفمبر، أما أرقام أكتوبر في تقارير سابقة فهي تاريخية وليست سعر الحجز الحالي.</p><p>المصدر: <a href="https://www.masrawy.com/autos/autos_news/details/2026/11/4/3073449" rel="noopener noreferrer">مصراوي، إعلان قائمة نوفمبر</a>، ومراجعة <a href="https://eg.hatla2ee.com/ar/new-car/nissan/Magnite" rel="noopener noreferrer">أسعار الفئات وتاريخ سريانها في هتلاقي</a>. يؤكد السعر الفعلي مع الموزع عند التعاقد.</p></section>'},
{"id":81498,"slug":"mg-zs-price-egypt","cover":81499,"modified":"2026-09-12T11:14:16","kind":"mg",
 "title":"سعر MG ZS وNew MG ZS في مصر: مقارنة الجيلين والأسعار",
 "seo":"سعر MG ZS وNew ZS في مصر بعد تحديث نوفمبر | أعطال",
 "desc":"سعر New MG ZS في مصر يبدأ من 1,165,000 جنيه حسب MG Motors الرسمي. مقارنة مع ZS الجيل السابق والسعر المرجعي وتجهيزات كل نسخة.",
 "kw":"سعر MG ZS في مصر",
 "replacements":[("1,150,000","1,165,000"),("1.150","1.165"),("75 ألف","90 ألف"),("75,000","90,000")],
 "intro":'<section id="a3tal-price-reviewed-20261114-mg" dir="rtl"><p><strong>تحديث 14 نوفمبر 2026:</strong> يؤكد <a href="https://www.mgmotor.com.eg/buying-guide/?lang=ar" rel="noopener noreferrer">موقع MG Motors مصر الرسمي</a> أن <strong>New MG ZS</strong> تبدأ حاليًا من <strong>1,165,000 جنيه</strong>؛ وهو رقم مختلف عن 1,150,000 جنيه في قائمة سابقة. انتبه إلى أن <strong>MG ZS الجيل السابق</strong> ليست نفس New ZS، وأن سعر 1,075,000 جنيه المتداول للجيل السابق يُذكر هنا <strong>كمرجع لقوائم سابقة</strong> ولا يثبت توافر سيارة جديدة من هذا الجيل عند الوكيل اليوم. افحص سنة الموديل والفئة والتوافر وسعر التسليم كتابةً.</p><p>يوضح الوكيل أن السعر النهائي قد يتغير حتى وقت التسليم؛ لذلك تبقى الفروق السعرية داخل المقارنة حسابًا مرجعيًا لا عرض بيع ملزمًا.</p></section>'},
]

def update_body(t,raw):
    new=raw
    stats={}
    for old,value in t["replacements"]:
        # Whole number and whole lakh-notation replacements, never substring of an SKU.
        pat=r"(?<![\d])"+re.escape(old)+r"(?![\d])"
        new,n=re.subn(pat,lambda m:value,new)
        stats[old]=n
    if any(stats[x]==0 for x in (
        ["1,020,000","1,120,000","1,135,000","1,235,000"] if t["kind"]=="elantra" else
        ["819,999","859,999","879,999","899,999"] if t["kind"]=="magnite" else
        ["1,150,000","75 ألف"])):
        raise RuntimeError("Expected dated prices were not all present "+str(stats))
    if t["kind"]=="elantra":
        if "2 أكتوبر 2026" not in new:
            raise RuntimeError("Expected historical Hyundai date changed")
        new=new.replace("آخر تحديث للأسعار: 2 أكتوبر 2026","آخر تحديث للأسعار: 5 نوفمبر 2026، وتم التحقق يوم 14 نوفمبر",1)
    if t["kind"]=="magnite":
        old_phrase="آخر مراجعة للأسعار: 10 أكتوبر 2026"
        if old_phrase not in new:raise RuntimeError("Nissan review date missing")
        new=new.replace(old_phrase,"آخر مراجعة للأسعار: 14 نوفمبر 2026",1)
        new=new.replace("سعر نيسان ماجنايت في مصر بعد زيادة أكتوبر","سعر نيسان ماجنايت في مصر بعد زيادة نوفمبر")
        new=new.replace("بحسب قائمة نيسان الجديدة المعلنة خلال أكتوبر","بحسب قائمة نيسان الجديدة المعلنة خلال نوفمبر")
        new=new.replace("الفارق بين أول وآخر فئة يبلغ 80 ألف جنيه","الفارق بين أول وآخر فئة يبلغ 100 ألف جنيه")
        # Old October source may remain as historic, but not as the source of November table.
        new=new.replace("ويستند الجدول التالي إلى","وكان جدول أكتوبر السابق يستند إلى",1)
        new=new.replace("أعلنت نيسان مصر انتهاء عروض أسعار الإطلاق في 6 أكتوبر وبدء تطبيق القائمة الجديدة بزيادات من 12 إلى 32 ألف جنيه حسب الفئة.",
                        "أعلنت نيسان في 4 نوفمبر زيادة أسعار ماجنايت من 40 إلى 60 ألف جنيه على الفئات، بعد تغييرات سابقة خلال أكتوبر.",1)
    if t["kind"]=="mg":
        # Clarify what is available officially: legacy ZS pricing is not today's
        # published New ZS listing on MG's current Egyptian catalogue.
        new=new.replace("سعر MG ZS في مصر</strong> رسميًا من",
                        "سعر MG ZS الجيل السابق</strong> في قوائم السوق القديمة من",1)
        new=new.replace("بحسب قائمة الأسعار الحالية المنشورة من الوكيل، يبدأ سعر MG ZS من",
                        "بحسب قوائم السوق المرجعية للجيل السابق، كان سعر MG ZS يبدأ من",1)
        new=new.replace("حاليًا يبلغ حوالي <strong>90 ألف جنيه فقط</strong>",
                        "كمقارنة حسابية بين سعر سابق للجيل القديم وسعر New ZS الحالي، يبلغ <strong>90 ألف جنيه</strong>",1)
        new=new.replace("سعر الجيل السابق","سعر الجيل السابق",1)
    if t["intro"].count('id="'+MARK+"-"+t["kind"]+'"')!=1:
        raise RuntimeError("Invalid source-qualified price note")
    new=t["intro"]+"\n"+new
    if len(new)<len(raw) or len(new)-len(raw)>4500:
        raise RuntimeError("Unexpected price update size")
    if len(re.findall(r"<img\b",new,re.I))!=len(re.findall(r"<img\b",raw,re.I)):
        raise RuntimeError("Original inline photos changed")
    if MARK not in new or any(n<0 for n in stats.values()):
        raise RuntimeError("Update marker missing")
    return new,stats

def guard(t,row,pub):
    if (int(row.get("id",0)),row.get("slug"),row.get("status"),row.get("type"),
        int(row.get("featured_media") or 0))!=(t["id"],t["slug"],"publish","post",t["cover"]):
        raise RuntimeError("Post identity drift "+t["slug"])
    if not row["modified_gmt"].startswith(t["modified"]):
        raise RuntimeError("Post modified since public review "+t["slug"])
    if pub.get("slug")!=t["slug"] or pub.get("status")!="publish":
        raise RuntimeError("WP REST post drift")
    y=pub.get("yoast_head_json") or {}
    if y.get("canonical")!=base.SITE+"/"+t["slug"]+"/" or not y.get("og_image") or (
        y.get("robots") or {}).get("index")=="noindex":
        raise RuntimeError("Pre-update Yoast mismatch")
    if len(row.get("content",""))<4000:
        raise RuntimeError("Original body incomplete")

def main():
    plans=[]
    for t in T:
        row=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
        if MARK+"-"+t["kind"] in row.get("content",""):
            print("PRICE_ALREADY_UPDATED",row["link"],flush=True);continue
        guard(t,row,pub)
        body,stats=update_body(t,row["content"])
        plans.append((t,row,pub,body))
        print("PRICE_PREFLIGHT",t["slug"],"replacements",stats,"original",len(row["content"]),"new",len(body),flush=True)
    print("ALL_THREE_PRICE_PREFLIGHTS_PASSED",len(plans),flush=True)
    for t,old,pub0,body in plans:
        now=base.bridge_post(t["id"])
        if now.get("modified_gmt")!=old.get("modified_gmt") or now.get("content")!=old.get("content"):
            raise RuntimeError("Concurrent post changes; abort")
        meta={"_yoast_wpseo_title":t["seo"],"_yoast_wpseo_metadesc":t["desc"],
              "_yoast_wpseo_focuskw":t["kw"],
              "_yoast_wpseo_opengraph-title":t["seo"],
              "_yoast_wpseo_opengraph-description":t["desc"],
              "_yoast_wpseo_twitter-title":t["seo"],
              "_yoast_wpseo_twitter-description":t["desc"]}
        try:
            res=base.req("/update-post",{
                "id":t["id"],"expected_modified_gmt":now["modified_gmt"],
                "title":t["title"],"content":body,"meta":meta
            })
            if res.get("error") or res.get("ok") is False:
                raise RuntimeError("Bridge rejected update")
        except Exception as ex:
            recovered=base.bridge_post(t["id"])
            if MARK+"-"+t["kind"] not in recovered.get("content",""):
                raise RuntimeError("Write not confirmed; no automatic retry") from ex
        after=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
        seo=pub.get("yoast_head_json") or {}
        if (after.get("slug"),after.get("status"),after.get("title"),
            int(after.get("featured_media") or 0))!=(
            t["slug"],"publish",t["title"],t["cover"]):
            raise RuntimeError("Post identity/cover/title changed")
        if after["content"].count('id="'+MARK+"-"+t["kind"]+'"')!=1:
            raise RuntimeError("Date/source note not saved")
        if seo.get("description")!=t["desc"] or seo.get("canonical")!=pub0["yoast_head_json"]["canonical"]:
            raise RuntimeError("SEO title/meta/canonical failed")
        if (seo.get("robots") or {}).get("index")=="noindex":
            raise RuntimeError("Unexpected noindex")
        if (seo.get("og_image") or [{}])[0].get("url")!=(
            pub0["yoast_head_json"].get("og_image") or [{}])[0].get("url"):
            raise RuntimeError("OG image changed")
        print("EVIDENCE_BACKED_PRICE_LIVE_VERIFIED",t["id"],after["link"],"cover",after["featured_media"],flush=True)
        time.sleep(2)
    print("A3TAL_PRICE_TRIO_NOVEMBER_2026_COMPLETED",flush=True)
if __name__=="__main__":main()
