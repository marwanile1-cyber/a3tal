#!/usr/bin/env python3
"""Manual SEO/GEO article review 2: motorcycle choice and valve failure diagnostics.
Updates two existing A3tal Egypt posts through A3tal Direct Bridge only.
"""
import html
import importlib.util
import re
import time

spec=importlib.util.spec_from_file_location("a3tal_human_base","scripts/review-human-seo-geo-egypt-three-20261114.py")
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
MARK="a3tal-human-review-20261114-next"
ROWS=[
 {"id":83148,"slug":"scooter-vs-motorcycle-egypt","cover":83338,
  "expected_date":"2026-10-08T15:09:56","kind":"scooter","anchor":"الاختلاف في وضعية القيادة والتشغيل",
  "title":"سكوتر أم موتوسيكل في مصر؟ الفرق في الاستخدام والصيانة والتكلفة",
  "seo":"سكوتر أم موتوسيكل؟ مقارنة الاستخدام والصيانة | أعطال",
  "description":"سكوتر أم موتوسيكل في مصر؟ قارن الزحام والدليفري واستهلاك البنزين وناقل CVT والسلسلة والتكلفة، وحدد الأنسب لك قبل الشراء.",
  "keyword":"سكوتر أم موتوسيكل"},
 {"id":80955,"slug":"engine-valves-function-problems-guide","cover":80956,
  "expected_date":"2026-10-01T23:23:18","kind":"valves",
  "title":"أعطال صبابات الموتور: الأعراض وفحص الكبس والتوقيت قبل الإصلاح",
  "seo":"أعطال صبابات الموتور: الأعراض وطرق الفحص | أعطال",
  "description":"تعرف على وظيفة صبابات السحب والعادم، وعلامات تلف كاوتش الصباب واعوجاج الصمامات، وكيف يميز الفني بينها وبين الشنابر وأعطال الكاتينة.",
  "keyword":"أعطال صبابات الموتور"},
]

SCOOTER_INTRO="""
<section id="a3tal-human-review-20261114-next-scooter" dir="rtl">
<p><strong>سكوتر أم موتوسيكل؟</strong> لو مشاويرك أغلبها داخل المدينة وبتقف وتتحرك كتير، السكوتر الأوتوماتيك ممكن يريحك من التعامل المستمر مع الدبرياج والغيارات. أما لو متعود على النقلات وبتدور على مواصفات تعليق أو حمولة أو نوع استخدام محدد، فالموتوسيكل اليدوي يستحق المقارنة. مفيش اختيار يكسب لكل الناس.</p>
<p>قبل السعر، قارن <strong>وزن الدراجة وارتفاع المقعد وتوافر قطع الغيار</strong> وسهولة الصيانة في منطقتك. السكوتر غالبًا فيه سير وبكرات CVT تحتاج متابعة، بينما موتوسيكلات كثيرة تعمل بسلسلة وتروس وقابض. ما تفترضش إن كل سكوتر بنفس الناقل أو إن كل موتوسيكل مناسب للسفر.</p>
<h2>اختار حسب طبيعة مشوارك</h2>
<div style="overflow-x:auto"><table>
<thead><tr><th scope="col">الاستخدام</th><th scope="col">ابدأ بمقارنة</th><th scope="col">ما الذي تحسمه بالتجربة؟</th></tr></thead>
<tbody>
<tr><td>زحام ومشاوير قصيرة</td><td>سكوتر مناسب الحجم أو موتوسيكل خفيف</td><td>سهولة الوقوف والتحكم والفرملة</td></tr>
<tr><td>دليفري يومي</td><td>الحمولة الفعلية والتكلفة الدورية وتوافر القطع</td><td>التوازن مع الصندوق والمسافات المتكررة</td></tr>
<tr><td>طرق أطول</td><td>ثبات الطراز وحماية الهواء والراحة والفرامل</td><td>المقعد والأداء عند سرعة قانونية مناسبة</td></tr>
<tr><td>مبتدئ</td><td>الوزن وسهولة المناورة والدعم الفني والتدريب</td><td>إمكان وضع القدمين على الأرض بثبات</td></tr>
</tbody></table></div>
</section>
"""
SCOOTER_MORE="""
<section id="a3tal-human-review-20261114-next-scooter-more" dir="rtl">
<h2>أسئلة مختصرة قبل شراء سكوتر أو موتوسيكل</h2>
<h3>هل كل سكوتر أوفر في البنزين؟</h3>
<p>لأ. الاستهلاك يتغير حسب المحرك والوزن والسرعة وطريقة القيادة والحالة الفنية؛ قارن أرقام الطرازين وتكلفة الصيانة بدل الحكم من شكل الدراجة.</p>
<h3>هل السكوتر يصلح للدليفري؟</h3>
<p>قد يكون عمليًا، لكن راجع أقصى حمولة مسموحة وثبات صندوق التوصيل ومساحة التخزين والتبريد وحالة الطريق قبل اختيار موديل بعينه.</p>
<p>لو لسه بتختار سعة الموتور، راجع <a href="https://a3tal.com/motorcycle-engine-sizes-125-150-160-200-250/">الفرق بين 125 و150 و200 و250 سي سي</a>. ولو هتشتري مستعملًا، استخدم <a href="https://a3tal.com/used-motorcycle-buying-checklist-egypt/">قائمة فحص الموتوسيكل المستعمل</a>، أما لو جديدًا فراجع <a href="https://a3tal.com/new-motorcycle-delivery-checklist/">قائمة الاستلام من المعرض</a>.</p>
<p><strong>للسلامة قبل كل مشوار:</strong> اعتمد فحص الإطارات والفرامل والإضاءة والسوائل والتوجيه كما تشرح <a href="https://msf-usa.org/documents/library/t-clocs-pre-ride-inspection-checklist/" rel="noopener noreferrer">مؤسسة Motorcycle Safety Foundation في قائمة T-CLOCS</a>، مع الرجوع لدليل المالك لكل طراز.</p>
</section>
"""
VALVES_HTML="""
<section id="a3tal-human-review-20261114-next-valves" dir="rtl">
<p><strong>أعطال صبابات الموتور</strong> ممكن تظهر في صورة ضعف كبس، تقطيع بالمحرك، استهلاك زيت أو دخان من العادم. لكن العرض وحده ما يثبتش إن الصباب نفسه تالف. المهم تفرق بين تسريب الضغط من الصباب، وتلف كاوتش الصباب، ومشكلة توقيت الكاتينة، وتآكل الشنابر؛ لأن كل حالة لها فحص وإصلاح مختلف.</p>
<p>الصبابات جزء من رأس المحرك (وش السلندر). صباب السحب ينظم مرور الهواء إلى الأسطوانة، وصباب العادم يسمح بخروج غازات الاحتراق. عمود الكامات يحدد توقيت فتحها وإغلاقها حسب تصميم الموتور، عبر آلية تشغيل قد تختلف من محرك لآخر، ولا يشترط وجود روكر أرم بنفس الشكل في كل السيارات.</p>
<h2>إيه وظيفة صبابات السحب والعادم؟</h2>
<p>في محرك البنزين رباعي الأشواط، يبدأ شوط السحب بفتح صمام السحب وهبوط البستم، ثم تُغلق الصمامات أثناء الضغط، ثم يُنتج الاحتراق قوة الدفع، وأخيرًا يفتح صمام العادم لطرد الغازات. بعض المحركات تضيف الوقود مباشرة داخل الأسطوانة وليس مع الهواء قبل الصباب؛ لذلك وصف الصباب بأنه «يدخل البنزين» مش دقيق في كل الأنظمة.</p>
<p>لفهم العلاقة بين البستم والكامات والكرنك، راجع <a href="https://a3tal.com/engine-operation-cycles-parts-guide/">شرح الأشواط الأربعة وأجزاء موتور السيارة</a>. ده موضوع تعليمي مختلف عن تشخيص تلف الصبابات في المقال الحالي.</p>
<h2>أشهر أعراض تلف الصبابات وكيف تفرق بينها</h2>
<div style="overflow-x:auto"><table>
<thead><tr><th scope="col">العرض</th><th scope="col">احتمالات يجب استبعادها</th><th scope="col">الفحص المناسب</th></tr></thead>
<tbody>
<tr><td>تقطيع وضعف سحب مع انخفاض الكبس</td><td>صباب لا يغلق بإحكام، شنابر أو جوان أو خلل توقيت</td><td>Compression ثم Leak-down وتحديد موضع تسرب الهواء</td></tr>
<tr><td>دخان أزرق أو نقص زيت</td><td>جلود صبابات، شنابر، PCV أو تيربو حسب المحرك</td><td>متابعة استهلاك الزيت وفحص التسريب والضغط وأسباب الدخان</td></tr>
<tr><td>صوت تكتكة من أعلى الموتور</td><td>خلوص صبابات، تاكيهات، تزييت أو عناصر أخرى</td><td>تحديد مصدر الصوت وضغط الزيت ومواصفات الخلوص</td></tr>
<tr><td>المارش بيلف والمحرك مش بيشتغل بعد عطل توقيت</td><td>سير/جنزير كاتينة أو توقيت غير مضبوط مع احتمال تلف ميكانيكي</td><td>فحص توافق التوقيت والكبس حسب دليل الصيانة</td></tr>
</tbody></table></div>
<p>لو في دخان أزرق بعد تشغيل بارد أو بعد التهدئة الطويلة فقد يكون كاوتش الصباب احتمالًا، لكنه مش تشخيصًا نهائيًا. كذلك انخفاض الكبس في سلندر لا يعني تلقائيًا تغيير طقم الصبابات قبل تحديد مكان فقد الضغط.</p>
<h2>هل انقطاع سير الكاتينة يعوج الصبابات دائمًا؟</h2>
<p><strong>لا.</strong> هناك محركات من نوع Interference Engine قد يصطدم فيها البستم بالصباب عند فقد التوقيت، ومحركات أخرى من نوع Free-running تكون فيها المسافة كافية لتقليل خطر التصادم. النتيجة مرتبطة بتصميم المحرك وسرعته ولحظة العطل، مش قاعدة واحدة لكل السيارات. لا تحاول تشغيل المحرك مرارًا بعد الاشتباه بانقطاع السير؛ الأفضل نقله للفحص.</p>
<p>تنبه شركة <a href="https://cms.gates.com/~/media/Files/Gates/Automotive/Catalogs/Automotive/TimingBeltReplacementGuide.pdf" rel="noopener noreferrer">Gates في دليل تغيير سير التوقيت</a> إلى الفرق بين النوعين وإمكانية تلف الصبابات والمكابس في محركات التداخل. أرقام تغيير السير أو الجنزير تختلف من موديل لآخر؛ المرجع النهائي هو كتالوج السيارة ورقم المحرك.</p>
<h2>كاوتش الصباب أم الشنابر: إزاي الفني يحدد السبب؟</h2>
<p>كاوتش الصباب يمنع مرور زيت زائد عبر ساق الصمام إلى مجرى السحب أو العادم، بينما الشنابر تساعد على إحكام الضغط والتحكم في الزيت على جدار الأسطوانة. الفني ينظر إلى ظروف ظهور الدخان واستهلاك الزيت وتهوية الكارتيرة، ثم يستخدم اختبارات مناسبة. اختبار الكبس وحده مش كافي دائمًا لتحديد سبب استهلاك الزيت، وقراءة أكواد كمبيوتر الأعطال لا تحل محل القياس الميكانيكي.</p>
<h2>خطوات الفحص قبل فك وش السلندر</h2>
<ol>
<li>سجّل العرض الفعلي: تقطيع بارد، ضعف عزم، دخان أو نقص زيت، وحدد متى يظهر.</li>
<li>افحص مستوى الزيت ونوعه وحالة التبريد، وأي تسريب خارجي أو عطل إشعال أو وقود يمكن أن يشبه الأعراض.</li>
<li>استخدم قراءة الأكواد والبيانات الحية إن وجدت، ثم قِس ضغط الأسطوانات بالأسلوب الموصى به للمحرك.</li>
<li>عند انخفاض الكبس، نفّذ Leak-down بواسطة فني مؤهل وحدد هل التسرب عبر السحب أو العادم أو الكارتيرة أو منظومة التبريد.</li>
<li>راجع توقيت الكاتينة والفحص البصري عند الحاجة، ولا تُقرّر تغيير الصبابات أو فك الوش إلا بعد دليل فني كافٍ.</li>
</ol>
<p>إذا ظهر صوت خبط قوي أو تحذير زيت مع فقد كبير للقوة، أوقف المحرك بشكل آمن. لا تُدخل أدوات في منظومة الكاتينة أثناء دوران المحرك ولا تتعامل مع فكها كتجربة منزلية.</p>
<h2>هل تغيير كاوتش الصباب معناه عمرة موتور؟</h2>
<p>مش بالضرورة. أحيانًا يكون الإصلاح محدودًا بجلود الصبابات إذا أثبت التشخيص سلامة باقي الأجزاء، لكن صبابًا محروقًا أو معوجًا قد يحتاج أعمالًا في رأس المحرك. وتآكل الشنابر أو جدار الأسطوانة حالة أخرى. اقرأ <a href="https://a3tal.com/full-engine-overhaul-vs-half-rebuild-guide/">الفرق بين العمرة الكاملة ونصف العمرة</a> لفهم القرار، ولا توافق على مقايسة كبيرة من وصف للدخان فقط.</p>
<h2>أسئلة شائعة عن أعطال الصبابات</h2>
<h3>هل ضعف السحب معناه الصبابات بايظة؟</h3>
<p>لا. ممكن يكون من البوجيهات أو الوقود أو حساسات أو ضغط شحن التيربو، حسب السيارة. الأعراض تحدد مسار الفحص فقط.</p>
<h3>هل كود Misfire يثبت اعوجاج صباب؟</h3>
<p>لا. كود الميسفاير يعني أن الكمبيوتر رصد خللًا بالاحتراق في سلندر أو أكثر. اختبار الضغط والتسرب يفيد في تمييز السبب الميكانيكي عن الإشعال والوقود.</p>
<h3>هل لازم أعرف سعر إصلاح الصبابات قبل الكشف؟</h3>
<p>السعر يتوقف على المحرك وحجم العمل وقطع الغيار وفك الوش ونوع التشغيل. اطلب قياسات واضحة ومقايسة بنود بعد التشخيص، بدل سعر ثابت غير موثوق.</p>
</section>
"""

def build(t,original):
    marker=MARK+"-"+t["kind"]
    if marker in original:
        return None
    if t["kind"]=="scooter":
        intro,tail=base.split_original_at_anchor(original,t)
        if len(re.findall(r"<h2\b",intro,re.I))<4:
            raise RuntimeError("Short duplicated original intro changed")
        new=SCOOTER_INTRO+tail+SCOOTER_MORE
    else:
        if len(original)<1500 or len(original)>17000:
            raise RuntimeError("Unexpected valves original content size")
        # Preserve the original in-body educational image verbatim. It is distinct
        # from the WP featured image and must not disappear during the rewrite.
        imgs=re.findall(r'<img\b[^>]*>',original,re.I)
        image_paras=re.findall(r'<p\b[^>]*>\s*<img\b[^>]*>\s*</p>',original,re.I|re.S)
        if len(imgs)!=1 or len(image_paras)!=1:
            raise RuntimeError("Unreviewed article media layout; stop to protect inline images")
        if "انقطاع سير الكاتينة" not in base.readable_markup(original) or "كاوتش الصباب" not in base.readable_markup(original):
            raise RuntimeError("Original valve themes differ; do not overwrite")
        anchor='<h2>إيه وظيفة صبابات السحب والعادم؟</h2>'
        if VALVES_HTML.count(anchor)!=1:
            raise RuntimeError("Editorial rewrite image slot changed")
        new=VALVES_HTML.replace(anchor,image_paras[0]+'\n'+anchor,1)
        if len(re.findall(r'<img\b',new,re.I))!=len(imgs):
            raise RuntimeError("Original inline image not preserved")
    if new.count('id="'+marker+'"')!=1 or len(new)<3000 or new.count("<h2")<5:
        raise RuntimeError("Unsafe revised markup")
    return new

def main():
    plans=[]
    for t in ROWS:
        live=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
        if MARK+"-"+t["kind"] in live.get("content",""):
            print("ALREADY_UPDATED",live.get("link"),flush=True)
            continue
        base.ensure_identity(t,live,pub)
        new=build(t,live["content"])
        plans.append((t,live,pub,new))
        print("NEXT_HUMAN_PREFLIGHT",t["slug"],len(live["content"]),len(new),flush=True)
    print("NEXT_TWO_PREFLIGHTS_COMPLETE",len(plans),flush=True)
    for t,before,before_public,new in plans:
        reread=base.bridge_post(t["id"])
        if reread["modified_gmt"]!=before["modified_gmt"] or reread["content"]!=before["content"]:
            raise RuntimeError("Concurrent revision; abort "+t["slug"])
        meta={"_yoast_wpseo_title":t["seo"],"_yoast_wpseo_metadesc":t["description"],
              "_yoast_wpseo_focuskw":t["keyword"],
              "_yoast_wpseo_opengraph-title":t["seo"],
              "_yoast_wpseo_opengraph-description":t["description"],
              "_yoast_wpseo_twitter-title":t["seo"],
              "_yoast_wpseo_twitter-description":t["description"]}
        payload={"id":t["id"],"expected_modified_gmt":reread["modified_gmt"],
                 "slug":t["slug"],"title":t["title"],"content":new,"meta":meta}
        try:
            base.req("/update-post",payload)
        except Exception as ex:
            check=base.bridge_post(t["id"])
            if MARK+"-"+t["kind"] not in check.get("content",""):
                raise RuntimeError("Write not confirmed; no retry "+t["slug"]) from ex
        final=base.bridge_post(t["id"]);pub=base.public_post(t["id"])
        seo=pub.get("yoast_head_json") or {}
        if (final.get("slug"),final.get("status"),int(final.get("featured_media") or 0))!=(
                t["slug"],"publish",t["cover"]):
            raise RuntimeError("Link/cover/status changed")
        if final.get("title")!=t["title"] or seo.get("description")!=t["description"]:
            raise RuntimeError("New title/metadata not saved")
        if final.get("content","").count('id="'+MARK+"-"+t["kind"]+'"')!=1:
            raise RuntimeError("New content marker missing")
        if seo.get("canonical")!=before_public["yoast_head_json"]["canonical"]:
            raise RuntimeError("Canonical changed")
        if (seo.get("robots") or {}).get("index")=="noindex":
            raise RuntimeError("Unexpected noindex")
        if (seo.get("og_image") or [{}])[0].get("url")!=(
                before_public["yoast_head_json"].get("og_image") or [{}])[0].get("url"):
            raise RuntimeError("og:image changed")
        must=(["https://a3tal.com/motorcycle-engine-sizes-125-150-160-200-250/",
               "https://a3tal.com/new-motorcycle-delivery-checklist/"]
              if t["kind"]=="scooter" else
              ["https://a3tal.com/engine-operation-cycles-parts-guide/",
               "https://a3tal.com/full-engine-overhaul-vs-half-rebuild-guide/"])
        if any(u not in final["content"] for u in must):
            raise RuntimeError("Contextual links not saved")
        print("NEXT_HUMAN_LIVE_VERIFIED",final["link"],"cover",t["cover"],"canonical",seo["canonical"],flush=True)
        time.sleep(2)
    print("A3TAL_NEXT_TWO_HUMAN_ARTICLES_DONE",flush=True)

if __name__=="__main__":
    main()
