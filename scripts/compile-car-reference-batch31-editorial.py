#!/usr/bin/env python3
"""Compile manually researched, non-overlapping Arabic automotive guides from editorial seeds.
This is a publishing input compiler, not a mass article spinner: each page requires
three separately authored model-specific explanatory sections and verified facts.
"""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/car-reference/batch31-editorial-seeds"
DEST=ROOT/"data/car-reference/batch-31-eight-real-models-composed.json"
def paragraph(t):return "<p>"+t+"</p>"
def heading(t):return "<h2>"+t+"</h2>"
def heading3(t):return "<h3>"+t+"</h3>"
def table(rows):
    return '<div class="a3tal-responsive-table" style="overflow-x:auto"><table><tbody>'+''.join("<tr><th scope='row'>"+html.escape(str(k))+"</th><td>"+html.escape(str(v))+"</td></tr>" for k,v in rows)+"</tbody></table></div>"
def related(cl,slug):
    hub="https://a3tal.com/car-reference/"+cl["brand"]+"/"+cl["model"]["slug"]+"/"
    anchors=["<a href='"+hub+"'>الدليل الشامل للموديل</a>"]
    anchors.extend("<a href='"+hub+x["slug"]+"/'>"+html.escape(x["short"])+"</a>" for x in cl["specs"] if x["slug"]!=slug)
    anchors+=["<a href='https://a3tal.com/car-reference/"+cl["brand"]+"/'>دليل العلامة</a>"]
    return heading("مواصفات فنية أخرى لنفس الموديل")+paragraph(" · ".join(anchors))
def sources(cl):
    return paragraph("المراجع الرسمية: "+" · ".join("<a rel='nofollow noopener' href='"+u+"'>"+html.escape(cl["brand_title"])+" - المواصفات الأصلية</a>" for u in cl["brand_sources"])+". جرى التركيز على النسخة المصرية المحددة، ولا تنطبق البيانات بالضرورة على أجيال أو أسواق أخرى.")
CATEGORY_ADDENDUM={
"engine-specs":("التأكد من المجموعة الميكانيكية قبل قطع الغيار","اسم المحرك وفتيس السيارة لا يكفيان لطلب زيت أو كمية سوائل أو كود قطعة. يجب مطابقة رقم الشاسيه ورمز المحرك وسنة الإنتاج ونوع الناقل ثم استخدام كتالوج الخدمة المناسب. ولو ظهرت رعشة أو ضعف عزم أو تأخير نقلات فالمواصفة ليست تشخيصًا؛ العطل يحتاج فحصًا وقراءة بيانات فعلية قبل استبدال أي جزء."),
"dimensions":("ماذا تعني المقاسات على أرض الواقع؟","قياسات الصانع مهمة لمقارنة السيارات والتخطيط للجراج، لكنها ليست جميع الأبعاد اللازمة للمناورة. فتح المرايا والأبواب، ومنحدر المدخل، وبروزات الصدام والحمولة يمكن أن تؤثر في دخول السيارة. لذلك ينبغي قياس الجراج على الطبيعة، وعدم اعتبار خلوص الأرض رقمًا يضمن المرور فوق أي مطب أو رامب دون احتكاك."),
"luggage-volume":("من الحجم المعلن إلى الاستخدام الحقيقي","السعة باللتر تعبر عن حجم حيز الأمتعة في وضع مقاعد معين، وليست وزن البضاعة الذي تستطيع السيارة حمله. ربما تكفي سعة كبيرة لحقائب مرنة لكنها لا تستوعب قطعة صلبة بسبب شكل فتحة التحميل أو بروزات الرفارف. عند نقل أمتعة أو السفر بعائلة، تبقى أحزمة التثبيت ومراجعة الحمولة المسموحة أهم من الرقم التسويقي وحده."),
"tire-specs":("قبل اختيار كاوتش أو جنط جديد","قطر الجنط بالبوصة جزء واحد من مقاس الإطار؛ يلزم كذلك عرض الإطار وارتفاع جانبه ومؤشرا الحمولة والسرعة، إضافةً إلى ضغط النفخ الصحيح من ملصق السيارة. الانتقال إلى جنط فئة أخرى ليس قرارًا شكليًا فحسب؛ قد يؤثر في الراحة والخلوص مع الفرامل والحساسات. لا يُستبدل المقاس الأصلي دون تحقق فني من التوافق."),
"chassis-specs":("كيف تُراجع العفشة بعيدًا عن التخمين؟","نوع نظام التعليق يساعد على تحديد القطع لكنه لا يعطي حكمًا قاطعًا على راحة الركوب أو سبب الخبط. ينبغي البدء بفحص الكاوتش والضغط وانتظام التآكل وزوايا العجل، ثم الجلب والمساعدين والوصلات. تعديل السوست أو ارتفاع السيارة ليس وسيلة تسمح بتجاوز الحمولة الأصلية أو إلغاء متطلبات الثبات والهندسة المعتمدة."),
"safety-specs":("ما حدود أنظمة الأمان؟","تعمل ABS وESC والحساسات والوسائد وغيرها ضمن شروط تشغيل محددة ولا تمنع كل حادث. وجود تجهيز في قائمة فئة أعلى لا يعني توفره في الفئة الأساسية؛ والاختصارات المتشابهة قد تشير لوظائف مختلفة. بعد حادث أو إصلاح الصدام والزجاج قد تحتاج الحساسات أو الكاميرات إلى فحص ومعايرة، ولا يصح اختبار التدخل الآلي بتعريض أحد للخطر."),
"adas-specs":("مساعدة السائق ليست قيادة ذاتية","أنظمة الرصد والكاميرات والتحذير تتأثر بسرعة السيارة والطقس ووضوح خطوط الطريق وحالة الحساسات، وقد تتوقف أو تقل كفاءتها حين تتسخ العدسات. يجب أن يظل السائق متحكمًا في المقود والفرامل والمسافة الآمنة. تحقق من الفئة وتجهيزاتها الأصلية ولا تفترض أن أي رمز على شاشة العدادات يثبت وجود جميع المساعدات المتقدمة."),
"infotainment":("التأكد من التجهيز قبل الاستبدال","قد تختلف مقاسات الشاشة والبلوتوث وميزات ربط الهاتف والأوامر الصوتية بحسب الفئة وتاريخ تصنيعها. توقف الشاشة أو الكاميرا لا يعني تلف الوحدة مباشرة؛ يلزم فحص التغذية والتوصيلات والتحديثات المناسبة. لا تستخدم توصيلات تعديل عشوائية أو تفترض أن شاشة موديل آخر ستعمل لمجرد تشابه المقاس الخارجي."),
"trim-features":("كيف تثبت أن التجهيز أصلي للفئة؟","عند المقارنة بين الفئات ينبغي طلب قائمة تجهيز رسمية مطابقة لسنة الإنتاج ورقم الشاسيه، لأن الصور الترويجية قد تعرض فئة أعلى أو أسواقًا أخرى. تختلط في سوق المستعمل أحيانًا إضافات الوكيل أو المالك مع تجهيز المصنع، ولذلك يفيد اختبار الوظائف على السيارة الفعلية وعدم دفع فارق سعر مقابل خاصية لم تُراجع أصالتها وحالتها."),
"fuel-specs":("لا تجعل سعة الخزان رقم استهلاك","سعة خزان الوقود ليست كمية البنزين التي تدخل دائمًا عند التفويل؛ فهناك وقود متبقٍ عند ظهور التحذير كما يتغير الاستهلاك مع الزحام والسرعة والتكييف. لا يمكن استخراج مدى قيادة مضمون من السعة وحدها دون معدل استهلاك موثق وظروف قياس متطابقة. ولا يجوز تقديم أرقام اختيار زيت أو سوائل خدمة من جدول التسويق."),
"charging":("قوة الشاحن ليست معدل شحن مضمون","قدرة المحطة المكتوبة على الجهاز تمثل حدًا اسميًا بينما القدرة التي تقبلها السيارة تتغير بحسب حرارة البطارية ونسبة الشحن وتوفر الكهرباء. لذلك لا تعني محطة أسرع بالضرورة شحن السيارة في نصف الوقت، كما أن الزمن المنشور لا يجوز نسبته من صفر إلى مئة دون تحديد نافذة الاختبار. فحص شاحن منزلي أو تركيبه يحتاج كهربائيًا مؤهلًا."),
"battery-specs":("سلامة البطارية أهم من التخمين","سعة البطارية بالكيلووات ساعة لا تعني القدرة اللحظية للموتور بالكيلووات ولا تعطي وحدها مدى مضمونًا. كما لا يجوز استنتاج صحة البطارية من رقم المدى الذي يتغير على الشاشة بتغير الاستهلاك. لا تُفتح علبة الجهد العالي ولا تُفك توصيلاتها دون إجراءات عزل وفني مؤهل؛ ويتم تقييم حالتها بأدوات صيانة مناسبة."),
"electric-range":("المدى المعياري ليس ضمان رحلة","أرقام WLTP أو NEDC مرتبطة باختبار محدد؛ لا تقارن بين معيارين مختلفين، ولا تجعل نقطة وصول الرحلة عند صفر شحن بناءً على رقم الكتالوج. ترفع السرعة والرياح والحرارة والحمولة واستخدام التكييف الاستهلاك في ظروف كثيرة. تأكد من توفر محطة شحن بديلة وخطط لهامش طاقة مناسب قبل السفر."),
}
def render_spec(cl,sp):
    assert len(sp["facts"])>=10 and len(sp["sections"])==3
    assert all(len(t.split())>=48 for title,t in sp["sections"]),(cl["key"],sp["slug"])
    addon=CATEGORY_ADDENDUM.get(sp["category"],CATEGORY_ADDENDUM["trim-features"])
    lead=sp["lead"]
    assert len(lead.split())>=42,(cl["key"],sp["slug"],"lead words",len(lead.split()))
    htmlbody=paragraph(lead)+heading("جدول المواصفات الخاصة بهذا الموضوع")+table(sp["facts"])
    for t,body in sp["sections"]:
        htmlbody+=heading(t)+paragraph(body)
    htmlbody+=heading(addon[0])+paragraph(addon[1])
    htmlbody+=heading("أسئلة شائعة")+heading3(sp["qa"][0][0])+paragraph(sp["qa"][0][1])+heading3(sp["qa"][1][0])+paragraph(sp["qa"][1][1])
    htmlbody+=related(cl,sp["slug"])+sources(cl)
    return htmlbody
def render_model(cl):
    m=cl["model"]
    assert len(m["intro"].split())>=65
    b=paragraph(m["intro"])+heading("ملخص بيانات السيارة لدى الوكيل")+table(m["facts"])
    for label,body in m["sections"]:
        b+=heading(label)+paragraph(body)
    b+=heading("روابط الصفحات الفنية المتخصصة")
    b+=paragraph(" · ".join("<a href='https://a3tal.com/car-reference/"+cl["brand"]+"/"+m["slug"]+"/"+v["slug"]+"/'>"+html.escape(v["short"])+"</a>" for v in cl["specs"]))
    b+=heading("أسئلة شائعة")
    for q,a in m["qa"]:b+=heading3(q)+paragraph(a)
    b+=related(cl,"")+sources(cl)
    return b
def main():
    names=["mg-new-hs","mg-one","mg-rx5plus","renault-duster-new","renault-kardian","renault-taliant","renault-megane","renault-austral"]
    clusters=[]
    for name in names:
        fn=SOURCE/(name+".json")
        seed=json.loads(fn.read_text(encoding="utf8"))
        assert seed["key"]==name
        assert len(seed["specs"])==(7 if name=="mg-new-hs" else 6)
        assert seed["brand"] in ("mg","renault")
        assert len(seed["photos"])>=2
        seed["model"]["rich_html"]=render_model(seed)
        seed["model"]["sources"]=seed["brand_sources"]
        for row in seed["specs"]:
            row["rich_html"]=render_spec(seed,row)
            row["engine"]=seed["model"]["engine"]
            row["sources"]=seed["brand_sources"]
            row["intro"]=row["lead"]
            row["detail"]=row["sections"][0][1]
            row["warning"]="التحقق من الفئة وسنة الإنتاج ورقم الشاسيه قبل شراء الأجزاء أو إجراء الصيانة."
            if not row.get("metric"):row["metric"]=row["facts"][0][1]
            row["meta_description"]=(row["title"]+"، مقارنة فنية من المصدر الرسمي المصري مع جدول وإرشادات الفحص والشراء.")[:153]
        m=seed["model"]
        m["meta_description"]=(m["title"]+"، دليل مواصفات فني محلي وروابط منفصلة للمحرك والمقاسات والأمان والفئات.")[:153]
        assert len({x["slug"] for x in [m]+seed["specs"]})==len(seed["specs"])+1
        for page in [m]+seed["specs"]:
            w=len(re.sub("<[^>]+>"," ",page["rich_html"]).split())
            assert w>=290,(name,page["slug"],w)
            assert page["rich_html"].count("<h2>")>=4
            assert page["rich_html"].count("<table>")==1
            assert "a3tal.com/car-reference/" in page["rich_html"]
            assert len(page["meta_description"])<=155
        clusters.append(seed)
        print("EDITORIAL_SEED_PASS",name,"unique_pages",len(seed["specs"])+1,"word_counts",[len(re.sub("<[^>]+>"," ",p["rich_html"]).split()) for p in [m]+seed["specs"]],flush=True)
    assert sum(1+len(c["specs"]) for c in clusters)==57
    DEST.write_text(json.dumps({"batch":31,"date":"2026-11-08","note":"8 independently researched official Egyptian car model clusters, 57 new factual PSEO articles, no fabricated technical service capacities.","clusters":clusters},ensure_ascii=False,indent=2),encoding="utf8")
    print("FIFTY_SEVEN_EDITORIALLY_WRITTEN_UNIQUE_EGYPT_PSEO_PAGES_READY",flush=True)
if __name__=="__main__":main()
