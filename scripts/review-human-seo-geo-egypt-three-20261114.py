#!/usr/bin/env python3
"""Human-reviewed A3tal Egypt editorial corrections for three existing posts.
Only GitHub + A3tal Direct Bridge; no new URLs, no category/media edits.
2026-11-14: remove redundant intros, repair four-stroke explanation,
add short fact-first answers, attributable primary sources and verified links.
"""
import html
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

SITE = "https://a3tal.com"
BRIDGE = SITE + "/wp-json/a3tal-direct/v1"
KEY = os.environ.get("A3TAL_API_KEY", "")
MARK = "a3tal-human-review-20261114"
TARGETS = [
    {
        "id": 80948, "slug": "engine-operation-cycles-parts-guide",
        "expected_date": "2026-10-01T23:23:19", "cover": 80949,
        "kind": "engine", "anchor": "البستم (Piston)",
        "title": "كيف يعمل موتور السيارة؟ شرح الأشواط الأربعة وأجزاء المحرك",
        "seo": "كيف يعمل موتور السيارة؟ الأشواط الأربعة وأجزاء المحرك | أعطال",
        "description": "كيف يعمل موتور السيارة؟ شرح مبسط للأشواط الأربعة ووظيفة البستم والكرنك والصبابات والكامات والبوجيه، والفرق بين العطل والعرض قبل الإصلاح.",
        "keyword": "كيف يعمل موتور السيارة"
    },
    {
        "id": 83156, "slug": "new-motorcycle-delivery-checklist",
        "expected_date": "2026-10-08T15:07:31", "cover": 83340,
        "kind": "new", "anchor": "جدول استلام موتوسيكل زيرو قبل التوقيع",
        "title": "استلام موتوسيكل زيرو: قائمة الفحص قبل التوقيع والخروج من المعرض",
        "seo": "استلام موتوسيكل زيرو: قائمة فحص قبل التوقيع | أعطال",
        "description": "قبل استلام موتوسيكل زيرو، راجع أرقام الشاسيه والمحرك والمستندات والفرامل والإطارات والعداد والضمان. قائمة فحص واضحة ومتى ترفض الاستلام.",
        "keyword": "استلام موتوسيكل زيرو"
    },
    {
        "id": 83150, "slug": "used-motorcycle-buying-checklist-egypt",
        "expected_date": "2026-10-08T15:07:34", "cover": 83342,
        "kind": "used", "anchor": "ابدأ بالأوراق والهوية قبل التشغيل",
        "title": "شراء موتوسيكل مستعمل في مصر: فحص الشاسيه والموتور والأوراق",
        "seo": "شراء موتوسيكل مستعمل في مصر: فحص قبل الشراء | أعطال",
        "description": "قبل شراء موتوسيكل مستعمل في مصر، افحص الأوراق وأرقام الشاسيه والمحرك والتسريب والفرامل والإطارات. تعرف على علامات رفض الصفقة وتكلفة الإصلاحات.",
        "keyword": "شراء موتوسيكل مستعمل"
    },
]

def req(path, data=None, secure=True):
    headers = {"Accept": "application/json", "Cache-Control": "no-store",
               "User-Agent": "A3tal-Human-Editorial-20261114/1.0"}
    if secure:
        if not KEY:
            raise RuntimeError("A3tal Bridge secret missing")
        headers.update({"X-A3tal-Key": KEY, "Authorization": "Bearer " + KEY})
    body = None if data is None else json.dumps(data, ensure_ascii=False).encode("utf-8")
    if body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
    url = (BRIDGE if secure else SITE) + path
    attempts = 1 if body is not None else 5
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    url, headers=headers, data=body,
                    method="POST" if body is not None else "GET"
            ), timeout=90) as response:
                return json.load(response)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as ex:
            if body is not None or attempt == attempts - 1:
                raise
            if isinstance(ex, urllib.error.HTTPError) and ex.code not in (
                429, 500, 502, 503, 504, 520, 522, 524, 525
            ):
                raise
            time.sleep(3 * (attempt + 1))
    raise RuntimeError("Unreachable retry")

def bridge_post(pid):
    return req("/post/" + str(pid))

def public_post(pid):
    return req("/wp-json/wp/v2/posts/" + str(pid) +
               "?_fields=id,slug,status,modified_gmt,link,featured_media,title,yoast_head_json",
               secure=False)

def readable_markup(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def split_original_at_anchor(body, target):
    headers = list(re.finditer(r"<h2\b[^>]*>[\s\S]*?</h2>", body, re.I))
    if len(headers) < 7:
        raise RuntimeError("Original article headings changed: " + target["slug"])
    positions = [m for m in headers if target["anchor"] in readable_markup(m.group())]
    if len(positions) != 1:
        raise RuntimeError("Expected unique detailed-section anchor not found: " + target["slug"])
    anchor = positions[0]
    intro, tail = body[:anchor.start()], body[anchor.start():]
    if "<img" in intro.lower() or "<figure" in intro.lower():
        raise RuntimeError("Original inline illustration in intro; protect it: " + target["slug"])
    if len(intro) < 150 or len(tail) < 1200:
        raise RuntimeError("Unexpected source article layout: " + target["slug"])
    return intro, tail

ENGINE_INTRO = """
<section id="a3tal-human-review-20261114-engine" dir="rtl">
<p><strong>كيف يعمل موتور السيارة؟</strong> في أغلب محركات البنزين رباعية الأشواط، يدخل الهواء إلى الأسطوانة، ثم يُضغط، ثم يشتعل الوقود لتتحول طاقة الاحتراق إلى حركة، وأخيرًا تخرج غازات العادم. البستم يتحرك لأعلى ولأسفل، وذراع التوصيل ينقل القوة إلى عمود الكرنك الذي يدور ليصل العزم عبر منظومة نقل الحركة إلى العجلات. هذه هي الفكرة الأساسية من غير تشبيهات مبالغ فيها.</p>
<p>الخطوات التالية تشرح محرك البنزين رباعي الأشواط، وهو الأكثر شيوعًا في سيارات الركوب، وليست وصفًا حرفيًا لمحرك ديزل أو ثنائي الأشواط أو نظام كهربائي.</p>
<h2>الأشواط الأربعة للمحرك بالترتيب</h2>
<div style="overflow-x:auto"><table>
<thead><tr><th scope="col">الشوط</th><th scope="col">حركة البستم</th><th scope="col">ما يحدث داخله؟</th></tr></thead>
<tbody>
<tr><td>السحب</td><td>لأسفل</td><td>يدخل الهواء عبر صمام السحب؛ ويتحدد توقيت إضافة الوقود حسب نظام الحقن.</td></tr>
<tr><td>الضغط</td><td>لأعلى</td><td>تُغلق الصمامات ويُضغط الهواء أو خليط الوقود والهواء داخل الأسطوانة.</td></tr>
<tr><td>القدرة</td><td>لأسفل</td><td>تشعل البوجيهات الخليط في محرك البنزين؛ ضغط الغازات يدفع البستم لأسفل.</td></tr>
<tr><td>العادم</td><td>لأعلى</td><td>يفتح صمام العادم فتخرج غازات الاحتراق.</td></tr>
</tbody></table></div>
<p><strong>سؤال سريع:</strong> هل يحدث شوط قدرة في كل لفة كرنك؟ لا، في المحرك رباعي الأشواط تحتاج الأسطوانة دورتين كاملتين للكرنك حتى تُكمل الأشواط الأربعة. ويختلف ترتيب اشتعال الأسطوانات في المحرك متعدد الأسطوانات.</p>
<p>للمرجع الفني، راجع <a href="https://www.briggsandstratton.com/en-gb/support/videos/how-4-cycle-engines-work" rel="noopener noreferrer">شرح الأشواط الأربعة لدى Briggs &amp; Stratton</a>. يوضح المصدر المبدأ الميكانيكي لمحرك بنزين صغير، بينما تتغير أنظمة الحقن والإدارة بين محركات السيارات.</p>
</section>
"""

ENGINE_EXTRA = """
<section dir="rtl" id="a3tal-human-review-20261114-engine-details">
<h2>متى يشير العرض إلى جزء داخل الموتور؟</h2>
<p>استهلاك الزيت المصحوب بدخان أزرق قد يكون مرتبطًا بالشنابر أو جلود الصبابات أو منظومة التهوية أو التيربو إذا كان موجودًا؛ لا تحدد القطعة من لون الدخان وحده. ضعف السحب قد ينتج أيضًا عن إشعال أو وقود أو حساسات، وليس بالضرورة عن عمرة موتور. افصل بين الوصف الذي يلاحظه السائق والقياس الذي يؤكد السبب.</p>
<p>إذا استمر صوت خبط معدني قوي أو ظهر تحذير ضغط الزيت، أوقف المحرك في مكان آمن بدل استكمال القيادة. الفني المؤهل يبدأ بفحص الزيت والضغط والأكواد والضغط داخل الأسطوانات حسب الأعراض، ثم يقرر مدى الحاجة إلى فك أجزاء.</p>
<p>للتفاصيل المرتبطة فعلًا بالموضوع راجع <a href="https://a3tal.com/engine-valves-function-problems-guide/">وظيفة صبابات الموتور وأعطالها</a>، ثم <a href="https://a3tal.com/full-engine-overhaul-vs-half-rebuild-guide/">الفرق بين عمرة الموتور الكاملة والنصف عمرة</a> إذا وصل التشخيص إلى تآكل ميكانيكي مثبت.</p>
</section>
"""

NEW_INTRO = """
<section id="a3tal-human-review-20261114-new" dir="rtl">
<p><strong>قبل استلام موتوسيكل زيرو من المعرض</strong>، افحصه وهو واقف وبارد إن أمكن، وطابق رقم الشاسيه ورقم المحرك والموديل مع الفاتورة والأوراق الرسمية. جرّب الفرامل والأنوار والعداد والمارش والمفاتيح، ودوّن أي خدش أو لمبة تحذير قبل التوقيع. توقيع الاستلام مش بديل عن المعاينة.</p>
<p>لو وجدت اختلافًا في أرقام الهوية، أو تسريبًا واضحًا، أو مشكلة في الفرامل والتوجيه، لا تعتبرها «حاجة بسيطة هتتظبط بعدين». اطلب توضيحًا مكتوبًا ومعالجة الخلل قبل الاستلام، أو اختر وحدة أخرى حسب اتفاق البيع.</p>
</section>
"""

NEW_EXTRA = """
<section dir="rtl" id="a3tal-human-review-20261114-new-details">
<h2>أسئلة مهمة قبل التوقيع على الاستلام</h2>
<h3>هل أمشي بالموتوسيكل وفيه لمبة تحذير شغالة؟</h3>
<p>لا تعتبر لمبة الزيت أو الحرارة أو عطل الفرامل أمرًا طبيعيًا من غير الرجوع لدليل المالك. بعض لمبات الاختبار تنطفئ بعد بدء التشغيل حسب الموديل؛ استمرار تحذير غير مفسر يستلزم فحصًا قبل التحرك.</p>
<h3>هل ضغط الكاوتش يكون زي أي موتوسيكل من نفس السعة؟</h3>
<p>لا. اضبط الضغط والإطارات باردة حسب ملصق الموتوسيكل أو كتيب الطراز وحمولته، مش على رقم عام لركوبتين مختلفتين.</p>
<h3>أحتفظ بإيه لو لقيت عيب يوم الاستلام؟</h3>
<p>احتفظ بالفاتورة ومحضر أو نموذج التسليم وصور رقم الشاسيه والعداد والعيب، واطلب توثيق ملاحظتك وتاريخ الإجراء التالي من المعرض.</p>
<p><strong>مرجع سلامة:</strong> <a href="https://msf-usa.org/documents/library/t-clocs-pre-ride-inspection-checklist/" rel="noopener noreferrer">قائمة فحص الدراجة T-CLOCS من Motorcycle Safety Foundation</a>. ولمن لم يحسم اختيار السعة، اقرأ <a href="https://a3tal.com/motorcycle-engine-sizes-125-150-160-200-250/">دليل اختيار سعة 125 إلى 250 سي سي</a>. ولو بتقارن بالشراء المستعمل، فراجع <a href="https://a3tal.com/used-motorcycle-buying-checklist-egypt/">فحص الموتوسيكل المستعمل قبل الدفع</a>.</p>
</section>
"""

USED_INTRO = """
<section id="a3tal-human-review-20261114-used" dir="rtl">
<p><strong>قبل شراء موتوسيكل مستعمل في مصر</strong>، افصل بين 3 أسئلة: هل الأوراق سليمة وصاحب البيع له حق التصرف؟ هل الشاسيه والمحرك والفرامل آمنون؟ وكم ستدفع بعد الشراء لتغيير الإطارات أو السلسلة أو السوائل؟ الموتوسيكل اللامع مش بالضرورة صفقة نظيفة.</p>
<p>اطلب تشوف الموتور باردًا، وافحص الأرقام والمستندات في ضوء النهار قبل التجربة. أي رقم مطموس أو اختلاف غير مفسر أو أثر حادث مؤثر على الشاسيه سبب كافٍ لوقف الصفقة لحد التحقق، حتى لو السعر مغرٍ. الفحص ده مش بديل عن مراجعة الأوراق في الجهة المختصة أو كشف فني متخصّص.</p>
</section>
"""

USED_EXTRA = """
<section dir="rtl" id="a3tal-human-review-20261114-used-details">
<h2>أسئلة سريعة عند شراء موتوسيكل مستعمل</h2>
<h3>هل العداد القليل دليل إن الموتوسيكل سليم؟</h3>
<p>لأ. راجع حالة المقابض والدواسات والسلسلة والإطارات وسجل الصيانة ومطابقة الأرقام، ولا تعتبر قراءة العداد وحدها إثباتًا للكيلومترات الحقيقية.</p>
<h3>هل ينفع أدفع عربون قبل ما أشوف الأوراق؟</h3>
<p>الأفضل ما تدفعش قبل مطابقة بيانات البائع والشاسيه. أي عربون لازم يكون بإيصال واضح يحدد الدراجة والمبلغ والشروط وطريقة الاسترداد؛ وراجع الإجراءات القانونية السارية في مصر.</p>
<h3>أعمل إيه لو ظهرت رعشة أو سحب ناحية واحدة؟</h3>
<p>أوقف تجربة القيادة لو ظهر خلل يؤثر على السيطرة أو الفرامل. فحص استقامة الشوكة والشاسيه والعجل لا يُحسم بتجربة قصيرة؛ اعرض الدراجة على فني مختص قبل اتخاذ قرار الشراء.</p>
<p><strong>مرجع فحص مستقل:</strong> <a href="https://mic.org/downloads/MIC_Buying-Selling_Used_Motorcycle_Guide%28Mobile%29.pdf" rel="noopener noreferrer">دليل Motorcycle Industry Council لفحص الموتوسيكل المستعمل</a>. للمقارنة بين أنواع الاستخدام اقرأ <a href="https://a3tal.com/scooter-vs-motorcycle-egypt/">سكوتر أم موتوسيكل؟</a>، ولمعرفة اختلاف إجراءات المعاينة اقرأ <a href="https://a3tal.com/new-motorcycle-delivery-checklist/">قائمة استلام موتوسيكل زيرو</a>.</p>
</section>
"""

def build(target, original):
    mark = MARK + "-" + target["kind"]
    if mark in original:
        return None
    intro, tail = split_original_at_anchor(original, target)
    if "<h2" not in intro.lower():
        raise RuntimeError("Expected redundant intro headings before detailed article")
    if target["kind"] == "engine":
        if "تحويل الحركة المستقيمة" not in tail:
            raise RuntimeError("Engine factual correction target missing")
        # Correct the crankshaft/connecting-rod role, without changing other sections.
        tail, replacements = re.subn(
            r"وظيفته هي تحويل الحركة المستقيمة \(فوق وتحت\) للبستم إلى حركة دورانية تدير العجلات في النهاية\.",
            "وظيفته نقل القوة بين البستم وعمود الكرنك؛ وتحوّل الآلية المكوّنة منهما معًا حركة البستم الترددية إلى دوران عند عمود الكرنك.",
            tail, count=1)
        if replacements != 1:
            raise RuntimeError("Unable to correct exact crankshaft claim safely")
        new = ENGINE_INTRO + tail + ENGINE_EXTRA
    elif target["kind"] == "new":
        new = NEW_INTRO + tail + NEW_EXTRA
    else:
        new = USED_INTRO + tail + USED_EXTRA
    if new.count('id="' + mark + '"') != 1:
        raise RuntimeError("Missing unique editorial revision marker")
    if len(new) < 3200 or len(new) > 24000:
        raise RuntimeError("Unexpected length after human revision")
    if len(re.findall(r"<h2\b", new, re.I)) < 5:
        raise RuntimeError("Substantive H2 headings disappeared")
    if len(re.findall(r'<img\b',new,re.I)) != len(re.findall(r'<img\b',original,re.I)):
        raise RuntimeError("Original inline media changed")
    return new

def ensure_identity(target, live, public):
    if (int(live.get("id",0)),live.get("slug"),live.get("status"),live.get("type"),
        int(live.get("featured_media") or 0)) != (
        target["id"],target["slug"],"publish","post",target["cover"]):
        raise RuntimeError("Post identity, featured image, slug or status changed: "+target["slug"])
    if public.get("slug") != target["slug"] or public.get("status") != "publish":
        raise RuntimeError("Public WordPress post identity mismatch: "+target["slug"])
    if live["modified_gmt"][:19] != target["expected_date"][:19]:
        raise RuntimeError("Original article changed since human review: "+target["slug"])
    seo=public.get("yoast_head_json") or {}
    if seo.get("canonical") != SITE + "/" + target["slug"] + "/":
        raise RuntimeError("Original canonical not as expected: "+target["slug"])
    if (seo.get("robots") or {}).get("index")=="noindex" or not seo.get("og_image"):
        raise RuntimeError("Original index/OG integrity failed: "+target["slug"])

def main():
    planned=[]
    for target in TARGETS:
        live=bridge_post(target["id"])
        public=public_post(target["id"])
        if MARK+"-"+target["kind"] in live.get("content",""):
            print("HUMAN_ALREADY_REVIEWED",live.get("link"),flush=True)
            continue
        ensure_identity(target,live,public)
        updated=build(target,live["content"])
        old_headers=[readable_markup(h) for h in re.findall(
            r"<h2\b[^>]*>[\s\S]*?</h2>",live["content"],re.I)]
        print("HUMAN_PREFLIGHT",target["slug"],"old_chars",len(live["content"]),
              "new_chars",len(updated),"old_H2",len(old_headers),flush=True)
        planned.append((target,live,public,updated))
    print("ALL_HUMAN_PREFLIGHTS_PASSED",len(planned),flush=True)
    for target,before,before_public,updated in planned:
        now=bridge_post(target["id"])
        if now["modified_gmt"]!=before["modified_gmt"] or now["content"]!=before["content"]:
            raise RuntimeError("Concurrent article edit; stop: "+target["slug"])
        meta={
            "_yoast_wpseo_title":target["seo"],
            "_yoast_wpseo_metadesc":target["description"],
            "_yoast_wpseo_focuskw":target["keyword"],
            "_yoast_wpseo_opengraph-title":target["seo"],
            "_yoast_wpseo_opengraph-description":target["description"],
            "_yoast_wpseo_twitter-title":target["seo"],
            "_yoast_wpseo_twitter-description":target["description"],
        }
        payload={
            "id":target["id"],"expected_modified_gmt":now["modified_gmt"],
            "slug":target["slug"],"title":target["title"],
            "content":updated,"meta":meta
        }
        try:
            response=req("/update-post",payload)
            if response.get("error") or response.get("ok") is False:
                raise RuntimeError("Bridge rejected update: "+str(response)[:220])
        except Exception as ex:
            check=bridge_post(target["id"])
            if MARK+"-"+target["kind"] not in check.get("content",""):
                raise RuntimeError("Write unconfirmed, will not retry: "+target["slug"]) from ex
            print("HUMAN_RECOVERED_TIMEOUT",target["slug"],flush=True)
        final=bridge_post(target["id"])
        pub=public_post(target["id"])
        seo=pub.get("yoast_head_json") or {}
        if (final.get("slug"),final.get("status"),int(final.get("featured_media") or 0))!=(
            target["slug"],"publish",target["cover"]):
            raise RuntimeError("Slug/status/featured media changed after publishing")
        if final.get("content","").count('id="' + MARK+"-"+target["kind"] + '"')!=1:
            raise RuntimeError("Revision marker not visible in stored content")
        if final.get("title")!=target["title"] or seo.get("description")!=target["description"]:
            raise RuntimeError("SEO or displayed title not saved")
        if seo.get("canonical")!=before_public["yoast_head_json"]["canonical"]:
            raise RuntimeError("Canonical changed after update")
        if (seo.get("robots") or {}).get("index")=="noindex":
            raise RuntimeError("Page changed to noindex")
        before_img=(before_public["yoast_head_json"].get("og_image") or [{}])[0].get("url")
        after_img=(seo.get("og_image") or [{}])[0].get("url")
        if before_img!=after_img:
            raise RuntimeError("Featured og:image changed unexpectedly")
        for required_url in (
            ["https://a3tal.com/engine-valves-function-problems-guide/","https://a3tal.com/full-engine-overhaul-vs-half-rebuild-guide/"]
            if target["kind"]=="engine" else
            ["https://a3tal.com/used-motorcycle-buying-checklist-egypt/","https://a3tal.com/motorcycle-engine-sizes-125-150-160-200-250/"]
            if target["kind"]=="new" else
            ["https://a3tal.com/scooter-vs-motorcycle-egypt/","https://a3tal.com/new-motorcycle-delivery-checklist/"]
        ):
            if required_url not in final.get("content",""):
                raise RuntimeError("Missing verified contextual internal link: "+required_url)
        print("HUMAN_EDITORIAL_LIVE_VERIFIED",target["id"],final["link"],
              "canonical",seo.get("canonical"),"cover",final.get("featured_media"),
              "og",after_img,flush=True)
        time.sleep(2)
    print("A3TAL_THREE_HUMAN_SEO_GEO_REVISIONS_DONE",flush=True)

if __name__=="__main__":
    main()
