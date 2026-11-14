#!/usr/bin/env python3
"""BMW DTC corrected code meanings and time-limited BYD DM-i promotion refresh.
Second human50 editorial review. Revisions protected and publish only through Direct Bridge.
"""
import importlib.util,re,time
spec=importlib.util.spec_from_file_location("base","scripts/review-human-seo-geo-egypt-three-20261114.py")
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
BMW={"id":80920,"slug":"bmw-fault-codes-dtc-full-list-2026","mod":"2026-10-01T23:23:21","cover":80921,"title":"أكواد أعطال BMW ورسائل iDrive 2026: كيف تقرأ DTC وتشخّص العطل؟","seo":"أكواد أعطال BMW 2026 ورسائل iDrive: التشخيص | أعطال","desc":"دليل قراءة أكواد BMW وiDrive موديل 2026: الفرق بين OBD وBMW ISTA وأكواد Misfire وUnderboost وتحذيرات الجهد العالي، دون تغيير قطع بناءً على كود وحده.","kw":"أكواد أعطال BMW 2026","html":"<p><strong>أكواد أعطال BMW ورسائل iDrive في موديلات 2026</strong> لا تعني أن كل رسالة تقابل قطعة واحدة يجب تغييرها. رسالة <strong>Drivetrain</strong> أو <strong>Chassis Stabilization</strong> تصف نطاق المشكلة، بينما القراءة التشخيصية لوحدة التحكم وتسجيل ظروف ظهور العطل هي بداية تحديد السبب. يختلف تفسير كود BMW الداخلي باختلاف الطراز والمحرك ووحدة التحكم وإصدار السوفتوير، ولذلك لا يوجد «جدول عالمي مضمون» يترجم كل رمز في كل BMW.</p>\n<p>تؤكد <a href=\"https://bmwtechinfo.bmwgroup.com/tisUI/assets/site_information.pdf\" rel=\"noopener noreferrer\">BMW Technical Information System</a> أن أدوات <strong>ISTA</strong> تقدم فحص أكواد الأعطال وخطط الاختبار وتوثيق إجراءات الإصلاح ومخططات الكهرباء وP-Code Lookup. هذا أوثق من نسب رقم خاص بكنترول إلى تلف تيربو أو حساس دون وصفه المعتمد للسيارة.</p>\n<h2>الفرق بين كود OBD2 ورسالة BMW في iDrive</h2>\n<div style=\"overflow-x:auto\"><table><thead><tr><th>المصدر</th><th>ما يقدمه؟</th><th>الحدود</th></tr></thead><tbody>\n<tr><td>رسالة iDrive/Check Control</td><td>تنبيه السائق إلى خلل ونصيحة فورية</td><td>ليست تقريرًا كاملًا عن السبب</td></tr>\n<tr><td>OBD2 Generic</td><td>أكواد انبعاثات ومحرك قياسية وأحيانًا Freeze Frame</td><td>قد لا يرى وحدات DSC أو التكييف أو الجهد العالي</td></tr>\n<tr><td>BMW ISTA أو أداة قادرة على الوحدات</td><td>DTC، بيانات حية، اختبارات موجهة ووصف خاص بـECU</td><td>تحتاج معرفة كود المحرك وVIN وإجراء الفحص الصحيح</td></tr>\n</tbody></table></div>\n<h2>أكواد وأعراض شائعة: ما الاختبار المناسب؟</h2>\n<div style=\"overflow-x:auto\"><table><thead><tr><th>الكود أو الرسالة</th><th>المعنى العام</th><th>خطوة تشخيصية</th></tr></thead><tbody>\n<tr><td>P0300–P0306</td><td>اختلال احتراق عام أو حسب الأسطوانة إذا كان المحرك يدعمها</td><td>Misfire counters، الإشعال، الوقود، تسريب هواء أو ضغط الأسطوانات</td></tr>\n<tr><td>P0299</td><td>ضغط شحن أقل من المتوقع لدى المحركات التيربو التي تسجله</td><td>Boost requested/actual، تسريب الخراطيم والإنتركولر والتحكم في التيربو</td></tr>\n<tr><td>P0171</td><td>خليط فقير في Bank 1 عند المحركات المعنية</td><td>Fuel Trim، تسريب فاكيوم، MAF/ضغط وقود وقياس فعلي</td></tr>\n<tr><td>P0562</td><td>جهد نظام منخفض في وحدة تسجل هذا الكود</td><td>بطارية 12V وهبوط جهد الأرضي والشحن تحت الحمل</td></tr>\n<tr><td>Drivetrain Malfunction</td><td>مجموعة دفع أو تحكم أو تخفيض قوة</td><td>اقرأ وحدات المحرك والفتيس والتحكم الهجين بحسب السيارة</td></tr>\n<tr><td>Chassis Stabilization</td><td>تنبيه متعلق بأنظمة الثبات/الشاسيه</td><td>DSC وWheel Speed وSteering Angle والجهد والتوصيلات</td></tr>\n</tbody></table></div>\n<p>هذه أمثلة على طرق التشخيص، وليست قائمة نهائية لكل أكواد BMW الداخلية. أرقام BMW المصنعة مثل 120308 أو 101F01 تحتاج <strong>وصف الوحدة المحدد في ISTA</strong> وسياق سجل الأعطال، ولا يُشترى لها Actuator أو Wastegate من الاسم المتداول وحده.</p>\n<h2>هل كل كود Underboost يعني تغيير التيربو؟</h2>\n<p>لا. قد يكون التسريب في مسار الشحن أو حساس ضغط أو مشكلة تحكم أو عادم أو عدم توافق بيانات التشغيل. ابدأ بقراءة Boost المطلوب والفعلي وفحص الخراطيم والوصلات والتحكم تحت الحمل الآمن. لو توجد حرارة مفرطة أو دخان كثيف أو أصوات طحن، تجنب القيادة حتى الفحص المتخصص. راجع <a href=\"https://a3tal.com/bmw-m3-m4-2026-performance-specs-faults/\">محرك BMW S58 وأنظمة الدفع في M3 وM4</a> لفهم اختلاف النسخ.</p>\n<h2>BMW Neue Klasse: هل توجد رموز أعطال واحدة لكل i3 وiX3؟</h2>\n<p>لا يوجد دليل عام موثوق يثبت أن أي رمز محدد من الإنترنت يمثل عطل تبريد بطارية أو وحدة شحن في جميع سيارات Neue Klasse. أعلنت <a href=\"https://www.bmwgroup.com/en/news/general/2026/series-production-of-the-bmw-i3.html\" rel=\"noopener noreferrer\">BMW بدء إنتاج i3 الكهربائية الجديدة في أغسطس 2026</a>، لكن توصيف أكواد الجهد العالي يتطلب نظام التشخيص وتفاصيل السيارة. لا تلمس كابلات HV البرتقالية أو موصلات البطارية، ولا تكرر محاولات تشغيل وشحن عند تحذير عزل كهربائي؛ اطلب فنيًا مؤهلًا.</p>\n<h2>هل تحديث OTA يحل 70% من أعطال BMW؟</h2>\n<p><strong>لا توجد نسبة 70% موثقة</strong> من BMW يمكن تطبيقها على كل الموديلات والرسائل. قد تحل حملة برمجية مشكلة محددة إذا نصت عليها نشرة خدمة رسمية، لكن ضعف جهد أو تسريب شحن أو خلل حساس أو دائرة كهرباء لن يتحول تلقائيًا إلى عطل «كاذب». لا تحدّث البرمجة كبديل عن قراءة الأكواد وحفظ Freeze Frame.</p>\n<h2>الطريقة السليمة لتشخيص BMW دون تبديل قطع عشوائي</h2>\n<ol><li>سجّل VIN وسنة التصنيع والمحرك ووحدات التحكم والتجهيزات.</li><li>صور رسالة iDrive وأوقات ظهورها، وحالة البطارية والطقس والسرعة.</li><li>اقرأ جميع وحدات السيارة بالأداة المناسبة واحفظ الأكواد وFreeze Frame قبل المسح.</li><li>افحص جهد 12V والأرضي والفيوزات إن كانت هناك رسائل كثيرة متزامنة.</li><li>استخدم اختبارًا موجهًا من ISTA والقياسات المناسبة لعزل السبب عن العرض.</li><li>بعد الإصلاح، اختبر السيارة في ظروف آمنة وتحقق من عودة الأكواد.</li></ol>\n<p>لقراءة الأعطال الهجينة ومخاطر الجهد العالي دون تعميم على كل فئات BMW، افتح <a href=\"https://a3tal.com/bmw-x7-xm-2026-specs-luxury-faults/\">دليل X7 وXM والفرق بين أنظمة الدفع</a> أو <a href=\"https://a3tal.com/bmw-x5-2026-hybrid-specs-problems-maintenance/\">دليل BMW X5 xDrive50e</a>.</p>\n<h2>الأسئلة الشائعة عن أكواد BMW</h2>\n<h3>هل أقدر أحدد العطل من رقم 120308 وحده؟</h3><p>لا، يجب قراءة وصف DTC من وحدة التحكم على نظام تشخيص مناسب مع VIN وبيانات التشغيل، ثم اختبار النظام المعني.</p>\n<h3>هل جهاز OBD2 الرخيص يشوف كل أعطال BMW؟</h3><p>غالبًا لا؛ قد يقرأ أكواد انبعاثات عامة بينما تحتاج وحدات DSC والفتيس والتكييف والجهد العالي أداة تدعمها.</p>\n<h3>هل رسالة Drivetrain تمنعني من القيادة؟</h3><p>اتبع نص الرسالة في دليل سيارتك. عند ضعف شديد أو تحذير أحمر أو سخونة أو صوت غير طبيعي توقف في مكان آمن واطلب المساعدة.</p>"}
MARK="a3tal-second50-nov14-bmw-dtc-byd"
DMI={"id":81877,"slug":"byd-dmi-free-maintenance-egypt","cover":81879,"modified":"2026-09-16T17:18:26"}
def validate(row,t,typ):
    if (int(row.get("id",0)),row.get("slug"),row.get("type"),row.get("status"),int(row.get("featured_media") or 0))!=(t["id"],t["slug"],"post","publish",t["cover"]):
        raise RuntimeError("Article ID, slug or OG cover changed: "+typ)
    if not row["modified_gmt"].startswith(t.get("mod",t.get("modified",""))):raise RuntimeError("Article modified, stop")
    pub=base.public_post(t["id"]);yoast=pub.get("yoast_head_json") or {}
    if yoast.get("canonical")!=base.SITE+"/"+t["slug"]+"/" or not yoast.get("og_image") or (
        yoast.get("robots") or {}).get("index")=="noindex":raise RuntimeError("SEO canonical/OG/robots blocked")
    return pub

def patch_byd(old):
    if MARK+"-byd" in old:return None
    if len(old)<5000 or "11 إلى 17 سبتمبر 2026" not in old or "17 سبتمبر" not in old:
        raise RuntimeError("Original September promo article unexpected")
    # Keep original September history, but put the separate current November offer first.
    notice='<section id="'+MARK+'-byd" dir="rtl"><p><strong>تحديث 14 نوفمبر 2026:</strong> عرض صيانة BYD الذي ورد في المقال الأصلي كان صالحًا للحجز خلال <strong>11–17 سبتمبر 2026</strong> وانتهى. لكن حساب <a href="https://oa.linkedin.com/company/egyptbyd" rel="noopener noreferrer">BYD Egypt – ManDream الرسمي على LinkedIn</a> أعلن في نوفمبر <strong>عرض حجز جديدًا</strong> يتضمن صيانة مجانية لمدة <strong>3 سنوات أو حتى 45,000 كم</strong>، وآخر يوم معلن للحجز هو <strong>15 نوفمبر 2026</strong>. لا نفترض أن شروط العرض الجديد أو الموديلات المشمولة مطابقة تلقائيًا لعرض DM-i القديم. للحصول على تأكيد مكتوب للفئة والمصاريف والبنود المستثناة، تواصل مع الوكيل على <strong>17669</strong>، وهو الرقم المنشور في إعلان الشركة.</p><p>الأرقام التالية عن برنامج سبتمبر معلومات أرشيفية ما لم تؤكد ManDream كتابيًا أنها جزء من عرض نوفمبر. وبعد يوم 15 نوفمبر لا تعتبر الصيانة المجانية متاحة دون إعلان تمديد جديد.</p></section>\n'
    updated=notice+old
    old_sentence="العرض بدأ 11 سبتمبر ويستمر حتى 17 سبتمبر 2026 وفق الشروط والأحكام المعلنة."
    if old_sentence in updated:
        updated=updated.replace(old_sentence,"عرض سبتمبر الأصلي كان من 11 إلى 17 سبتمبر 2026 وانتهى. هناك عرض حجز منفصل معلن في نوفمبر حتى 15 نوفمبر وفق إشعار الشركة وشروطه.",1)
    updated=updated.replace("الفترة المعلنة للعرض من 11 إلى 17 سبتمبر 2026.",
      "عرض سبتمبر الأصلي كان من 11 إلى 17 سبتمبر 2026 وانتهى، وهناك عرض منفصل معلن في نوفمبر للحجز حتى 15 نوفمبر 2026.",1)
    updated=updated.replace("وبما أن العرض المعلن ينتهي في 17 سبتمبر،",
      "وبما أن عرض سبتمبر الأصلي انتهى وعرض نوفمبر له موعد معلن مختلف،",1)
    if "15 نوفمبر" not in updated or updated.count('id="'+MARK+'-byd"')!=1:raise RuntimeError("BYD update missing current cutoff")
    return updated

def main():
    selected=[]
    for t,kind in ((BMW,"bmw"),(DMI,"byd")):
        old=base.bridge_post(t["id"]);pub=validate(old,t,kind)
        if MARK+"-"+kind in old.get("content",""):
            print("SECOND50_ALREADY",kind,flush=True);continue
        if kind=="bmw":
            if re.search(r"<img\b",old.get("content",""),re.I):raise RuntimeError("Original BMW inline media would be lost")
            body='<section id="'+MARK+'-bmw" dir="rtl">'+t["html"]+'</section>'
        else:body=patch_byd(old["content"])
        if len(body)<2500 or (kind=="bmw" and body.count("<h2>")<6):
            raise RuntimeError("New editorial body too short")
        if len(re.findall(r"<img\b",body,re.I))!=len(re.findall(r"<img\b",old["content"],re.I)):
            raise RuntimeError("Inline image preservation check failed")
        selected.append((t,kind,old,pub,body))
        print("SECOND50_NEW_PREFLIGHT",kind,t["id"],len(old["content"]),len(body),flush=True)
    print("SECOND50_NEW_ALL_PREFLIGHTS_PASSED",len(selected),flush=True)
    for t,kind,old,previous,body in selected:
        now=base.bridge_post(t["id"])
        if now["modified_gmt"]!=old["modified_gmt"] or now["content"]!=old["content"]:
            raise RuntimeError("Concurrent edits stop all")
        payload={"id":t["id"],"expected_modified_gmt":old["modified_gmt"],"content":body}
        if kind=="bmw":
            payload["title"]=t["title"]
            payload["meta"]={"_yoast_wpseo_title":t["seo"],"_yoast_wpseo_metadesc":t["desc"],
                "_yoast_wpseo_focuskw":t["kw"],
                "_yoast_wpseo_opengraph-title":t["seo"],"_yoast_wpseo_opengraph-description":t["desc"],
                "_yoast_wpseo_twitter-title":t["seo"],"_yoast_wpseo_twitter-description":t["desc"]}
        try:base.req("/update-post",payload)
        except Exception as err:
            if MARK+"-"+kind not in base.bridge_post(t["id"]).get("content",""):
                raise RuntimeError("Unconfirmed write - no retry") from err
        after=base.bridge_post(t["id"]);pub=base.public_post(t["id"]);seo=pub.get("yoast_head_json") or {}
        if (after["slug"],after["status"],int(after.get("featured_media") or 0))!=(t["slug"],"publish",t["cover"]):
            raise RuntimeError("Slug, status or featured image drift")
        if after["content"].count('id="'+MARK+"-"+kind+'"')!=1:
            raise RuntimeError("Revision note not present")
        if seo.get("canonical")!=previous["yoast_head_json"]["canonical"] or (
          seo.get("robots") or {}).get("index")=="noindex" or (
          seo.get("og_image") or [{}])[0].get("url")!=(
          previous["yoast_head_json"].get("og_image") or [{}])[0].get("url"):
          raise RuntimeError("SEO image/index/canonical changed")
        if kind=="bmw" and seo.get("description")!=t["desc"]:
            raise RuntimeError("BMW Yoast meta not saved")
        print("SECOND50_BMW_BYD_LIVE_VERIFIED",kind,t["id"],after["link"],flush=True)
        time.sleep(1)
    print("SECOND50_BMW_DTC_BYD_REFRESH_DONE",flush=True)
if __name__=="__main__":main()
