#!/usr/bin/env python3
"""Attach published Suzuki Alto 2027 price news to the live A3TAL car database.

Ensures a single a3_car entity with verified October 2026 Egyptian price,
safely linking the existing indexable price article as the canonical guide.
The global theme already noindexes vehicle entity pages by default.
"""
import json, os, time, urllib.parse, urllib.request, urllib.error

BASE="https://a3tal.com"
KEY=os.getenv("A3TAL_API_KEY","")
SLUG="suzuki-alto-2027-egypt"
ARTICLE_ID=83533
IMAGE_ID=83535
if not KEY:
    raise SystemExit("A3TAL_API_KEY secret unavailable")

def send(url,payload=None,secured=False):
    headers={"User-Agent":"A3TAL-Live-Entity-Installer/1.0","Accept":"application/json","Cache-Control":"no-cache"}
    if secured:
        headers["X-A3tal-Key"]=KEY
        headers["Authorization"]="Bearer "+KEY
    body=None
    if payload is not None:
        body=json.dumps(payload,ensure_ascii=False).encode("utf-8")
        headers["Content-Type"]="application/json"
    request=urllib.request.Request(url,data=body,headers=headers)
    with urllib.request.urlopen(request,timeout=65) as response:
        return json.load(response)

def read_entity():
    # Unauthenticated REST read is sufficient for published car entries.
    url=BASE+"/wp-json/wp/v2/a3tal-cars?"+urllib.parse.urlencode({"slug":SLUG,"per_page":2})
    return send(url)

def main():
    story=send(BASE+"/wp-json/wp/v2/posts/"+str(ARTICLE_ID))
    if story.get("status")!="publish" or story.get("slug")!="suzuki-alto-2027-price-egypt-535000":
        raise RuntimeError("Expected published news article missing; refuse car insert")
    if int(story.get("featured_media") or 0)!=IMAGE_ID:
        raise RuntimeError("Story's real featured Suzuki photo unexpectedly changed")
    image=send(BASE+"/wp-json/wp/v2/media/"+str(IMAGE_ID))
    if image.get("mime_type")!="image/webp":
        raise RuntimeError("Expected WebP media is missing")
    before=read_entity()
    if len(before)>1:
        raise RuntimeError("Conflicting car entries already exist")
    content="""<p>سوزوكي ألتو موديل 2027 في مصر، سيارة هاتشباك صغيرة من خمس أبواب، معروضة رسميًا بسعر 535,000 جنيه لفئة مانيوال واحدة بحسب المعلومات المراجعة في أكتوبر 2026. مناسبة في المقام الأول للتنقل اليومي داخل المدينة، بينما ينبغي تجربة المساحة الخلفية وأداء المحرك تحت الحمل قبل قرار الشراء.</p>
<h2>سعر ومواصفات سوزوكي ألتو 2027</h2>
<ul>
<li>السعر الرسمي المعلن: <strong>535 ألف جنيه مصري</strong> قبل تكاليف الترخيص والتأمين.</li>
<li>محرك بنزين 998 سي سي، ثلاث أسطوانات، بقوة معلنة 67 حصانًا وعزم 89 نيوتن متر.</li>
<li>ناقل حركة مانيوال خمس سرعات، ودفع أمامي.</li>
<li>هيكل هاتشباك بخمس أبواب ومقاعد لخمسة أشخاص، مع مساحة محدودة للشنطة.</li>
<li>تجهيزات الأمان المعلنة تشمل ست وسائد هوائية وABS ونظام ثبات ESP؛ راجع تجهيزات الفئة المصرية عند التسليم.</li>
</ul>
<h2>الخبر الكامل وسعر الوكيل والمقارنات</h2>
<p>للتفاصيل والمميزات والعيوب والمقارنة مع نيسان صني وبروتون ساجا، اقرأ <a href="https://a3tal.com/suzuki-alto-2027-price-egypt-535000/">سعر سوزوكي ألتو 2027 في مصر: المواصفات وهل تستحق الشراء؟</a>. يظل المقال الإخباري هو المصدر الأساسي المفهرس لهذا الموضوع، بينما ملف السيارة هنا جزء من قاعدة موديلات أعطال.كوم للتصفح والفلترة.</p>
<p><small>مراجعة البيانات: 13 أكتوبر 2026. السعر الرسمي قد يتغير، ويُرجع إلى الوكيل عند الشراء. الصورة لسيارة ألتو K10 من عائلة التصميم، بعدسة Vis M، <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>، وقد تختلف تفاصيل فئة السوق المصري.</small></p>"""
    payload={
        "op":"platform_entity_upsert",
        "type":"a3_car",
        "slug":SLUG,
        "title":"سوزوكي ألتو 2027 في مصر",
        "status":"publish",
        "content":content,
        "excerpt":"سوزوكي ألتو 2027 في مصر: السعر الرسمي 535 ألف جنيه لفئة مانيوال، محرك 998 سي سي بقوة 67 حصانًا و6 وسائد هوائية، مع رابط لمقارنة الأسعار.",
        "featured_media":IMAGE_ID,
        "taxonomies":{"a3_brand":["suzuki"],"a3_market":["egypt"],"a3_car_body":["hatchback"]},
        "meta":{
            "_a3_year":"2027",
            "_a3_price_min":"535000",
            "_a3_price_max":"535000",
            "_a3_currency":"EGP",
            "_a3_engine_cc":"998",
            "_a3_power_hp":"67",
            "_a3_torque_nm":"89",
            "_a3_transmission":"مانيوال 5 سرعات",
            "_a3_fuel":"بنزين",
            "_a3_drivetrain":"أمامي",
            "_a3_seats":"5",
            "_a3_source_url":"https://a3tal.com/suzuki-alto-2027-price-egypt-535000/",
            "_a3_source_checked_at":"2026-10-13",
            "_a3_related_post_ids":str(ARTICLE_ID)
        }
    }
    print("Preflight passed. Existing matching car records:",len(before),flush=True)
    # If a job is rerun, updating this one exact slug is intentional.
    try:
        response=send(BASE+"/wp-json/a3tal-direct/v1/admin",payload,secured=True)
        if not response.get("ok"):
            raise RuntimeError("Bridge rejected record")
        result=response.get("result",{})
        print("Bridge upsert returned car", result.get("id"), result.get("link"),flush=True)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as err:
        # Lost write acknowledgement is ambiguous: don't repeat the write.
        print("Write acknowledgement interrupted, verifying one canonical entity", type(err).__name__,flush=True)
    time.sleep(25)
    after=read_entity()
    if len(after)!=1 or after[0].get("slug")!=SLUG or after[0].get("status")!="publish":
        raise RuntimeError("Car entity not confirmed live after write. Inspect before retry.")
    if int(after[0].get("featured_media") or 0)!=IMAGE_ID:
        raise RuntimeError("Car entity has no verified WebP featured photo")
    cid=after[0]["id"]
    print("SUCCESS: Published Suzuki Alto car entity",cid,after[0]["link"],"linked to news",ARTICLE_ID,flush=True)

if __name__=="__main__":
    main()
