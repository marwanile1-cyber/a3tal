#!/usr/bin/env python3
"""Revision-safe refresh of three high-impression, low-CTR A3tal URLs.

Priorities are drawn from user's 2026-11-07 Search Console XLSX (last 3 months):
P0011 4052 impressions/7 clicks; P0342 3346/12; PCV 1790/13.
No new competing PSEO pages; no URL, category, image or canonical changes.
"""
import os, re, time, json, urllib.request, urllib.parse
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
STAMP="a3tal-gsc-opportunity-20261107"
CASES=[
 {"id":81111,"slug":"pcv-valve-failure-symptoms-oil-consumption","focus":"أعراض تلف بلف تبخير الزيت",
  "seo":"أعراض تلف بلف تبخير الزيت PCV: الفرق عن الشنابر والفحص الصحيح | أعطال.كوم",
  "meta":"أعراض تلف بلف تبخير الزيت PCV: صفير، سلانسية غير ثابتة ونقص الزيت. جدول يوضح الفرق عن الشنابر وتسريب الهواء، وفحوصات الورشة قبل تغيير البلف.",
  "marker":STAMP+"-pcv",
  "block":'''<section id="a3tal-gsc-opportunity-20261107-pcv" dir="rtl"><h2>أعراض تلف بلف تبخير الزيت: متى تتهم PCV ومتى تفحص الشنابر؟</h2><p><strong>ظهور الزيت في مدخل الهواء أو نقصه لا يثبت تلف PCV وحده.</strong> إذا كان البلف أو الخرطوم مسدودًا فقد يرتفع ضغط علبة المرافق وتظهر تهريبات زيت، بينما قد يؤدي خلل آخر إلى سحب هواء غير محسوب أو صفير أو اضطراب السلانسية حسب تصميم النظام. كما أن ارتفاع الغازات المتسربة من الاحتراق (Blow-by) بسبب تآكل المحرك قد يسبب أعراضًا قريبة؛ لذلك يجب التفريق بين السبب والنتيجة بالقياس.</p><div style="overflow-x:auto"><table><thead><tr><th>العَرَض</th><th>الاحتمال</th><th>الاختبار المطلوب</th></tr></thead><tbody><tr><td>صفير مع تغير السلانسية</td><td>تسريب في غشاء PCV أو خرطوم فاكيوم</td><td>فحص إحكام مسارات الهواء وقراءات Fuel Trim وفق المحرك</td></tr><tr><td>تهريب زيت من أكثر من جوان</td><td>ضغط علبة مرافق مرتفع، PCV مسدود أو Blow-by</td><td>قياس Crankcase Pressure وتقييم التهوية وحالة المحرك</td></tr><tr><td>دخان أزرق مستمر ونقص زيت واضح</td><td>مصدر دخول زيت للاحتراق، وليس PCV فقط</td><td>فحص التسريبات والتهوية وضغط السلندرات عند اللزوم</td></tr><tr><td>زيت خفيف في مجرى السحب</td><td>قد يكون أثرًا طبيعيًا محدودًا أو عطل تهوية</td><td>تقييم الكمية والأعراض وليس مشاهدة رواسب وحدها</td></tr></tbody></table></div><p>لا تضع يدك فوق فتحة الزيت لتجربة «قوة النفخ» مع موتور ساخن، ولا تفصل خراطيم فاكيوم بالمحرك أثناء الحركة. يراجع الفني مخطط المحرك، ووجود غشاء مدمج بالغطاء أو صمام منفصل، ويقيس الضغط وفق دليل الشركة. <a href="https://static.nhtsa.gov/odi/tsbs/2024/MC-11010490-0001.pdf" rel="nofollow">نشرة GM الفنية عن استهلاك الزيت</a> توصي بالتحقق من عدم وجود انسداد أو تلف في نظام تهوية علبة المرافق ضمن التشخيص، ولا تعتبر أي عرض منفرد دليلًا على PCV.</p></section>'''},
 {"id":80209,"slug":"dtc-p0342-chevrolet","focus":"P0342 شيفروليه",
  "seo":"كود P0342 شيفروليه ودايو: فحص إشارة حساس الكامة المنخفضة | أعطال.كوم",
  "meta":"كود P0342 شيفروليه ودايو يعني انخفاض إشارة دائرة حساس الكامة، وليس وجوب تغييره فورًا. شوف ترتيب فحص التغذية والأرضي والفيشة ومتى تحتاج أوسيلوسكوب.",
  "marker":STAMP+"-p0342",
  "block":'''<section id="a3tal-gsc-opportunity-20261107-p0342" dir="rtl"><h2>كود P0342 شيفروليه: إيه اللي تخلي الكهربائي يقيسه الأول؟</h2><p>لو ظهر P0342 على أفيو أو أوبترا أو دايو، فالكمبيوتر يسجل <strong>انخفاض إشارة دائرة حساس موضع الكامة</strong>، وليس «حساس الكامة بايظ» بشكل حاسم. لا تستخدم مكان فيشة أو عدد أسلاك أو Pinout من سيارة أخرى حتى لو نفس العلامة. اطلب من الفني تحديد كود المحرك والمخطط ومقارنة جهد التغذية والأرضي وشكل الإشارة بالبيانات الأصلية.</p><div style="overflow-x:auto"><table><thead><tr><th>ماذا وجد الفني؟</th><th>الخطوة التالية</th></tr></thead><tbody><tr><td>الإشارة منخفضة مع تغذية صحيحة</td><td>فحص قصر السلك للأرضي والحساس وموضعه باستخدام جهاز مناسب</td></tr><tr><td>التغذية أو الأرضي غير صحيحين</td><td>فحص الفيوزات والضفيرة والفيش قبل شراء حساس</td></tr><tr><td>العربية تتأخر في التشغيل مع P0335</td><td>مقارنة إشارات CKP/CMP وهبوط جهد البطارية أثناء التشغيل</td></tr><tr><td>P0016 مرافق بعد إصلاح كاتينة</td><td>التحقق من التوقيت الميكانيكي بعد إثبات سلامة الدائرة</td></tr></tbody></table></div><p>مسح الكود لا يصلح قفلة أو سلكًا مقطوعًا. لا تُجرّب توصيل 12 فولت مباشرة لطرف الإشارة دون مخطط، لأن ذلك قد يُتلف الكمبيوتر. إن كانت الأعراض عامة وليست تخص شيفروليه، ابدأ من <a href="https://a3tal.com/p0016-crankshaft-camshaft-correlation/">دليل P0016 عند اختلال العلاقة بين الكامة والكرنك</a> عندما يكون الكود مصاحبًا. المرجع الفني العام لتعريف Circuit Low: <a href="https://static.nhtsa.gov/odi/tsbs/2013/MC-10243913-9999.pdf" rel="nofollow">جدول تشخيص DTC الرسمي المنشور عبر NHTSA</a>، وليس مخطط أسلاك لأوبترا بعينها.</p></section>'''},
 {"id":114,"slug":"كود-p0011-سيارات-هيونداي","focus":"كود P0011 هيونداي",
  "seo":"كود P0011 هيونداي: فحص الزيت وبلف VVT قبل تغيير الكاتينة | أعطال.كوم",
  "meta":"معنى كود P0011 هيونداي وتأخر أو تقدم توقيت الكامة: اختبر مستوى الزيت وOCV وبيانات Target/Actual Cam Angle قبل تغيير حساس الكامة أو الكاتينة.",
  "marker":STAMP+"-p0011",
  "block":'''<section id="a3tal-gsc-opportunity-20261107-p0011" dir="rtl"><h2>P0011 هيونداي: هل العيب من بلف VVT ولا الكاتينة؟</h2><p><strong>P0011 كود أداء توقيت الكامة</strong>، لذلك لا يثبت تلف حساس الكامة أو بلف VVT منفردًا. إذا كان مستوى الزيت أو مواصفته غير صحيحين، أو ضغطه غير كافٍ، يمكن أن تتأثر حركة Cam Phaser. كذلك قد تكون مشكلة OCV أو فلتره أو الأسلاك أو التوقيت الميكانيكي. تختلف أجزاء المحرك التي تحمل الاسم نفسه بين أكسنت وإلنترا وتوسان والمحركات المختلفة.</p><div style="overflow-x:auto"><table><thead><tr><th>الملاحظة</th><th>بماذا يبدأ الفني؟</th></tr></thead><tbody><tr><td>تغيير الزيت متأخر أو المستوى غير مناسب</td><td>تأكيد الزيت الموصى به والمستوى وحالة ضغط الزيت</td></tr><tr><td>زاوية الكامة Actual لا تتبع Target</td><td>اختبار OCV ودائرة التحكم ومسار الزيت وCam Phaser</td></tr><tr><td>P0011 مع P0016 أو صوت من التوقيت</td><td>فحص الترابط CKP/CMP والتوقيت الميكانيكي وفق دليل المحرك</td></tr><tr><td>لمبة ضغط الزيت أو خبط واضح بالمحرك</td><td>إيقاف التشغيل والتحقق من ضغط الزيت لدى فني قبل إعادة التشغيل</td></tr></tbody></table></div><p>قيمة مقاومة بلف VVT أو زاوية الكامة المقبولة ليست رقمًا واحدًا لكل هيونداي. اطلب تقرير الأكواد وFreeze Frame وقراءات Live Data قبل دفع ثمن حساس أو كاتينة. للمقارنة مع المعنى القياسي راجع <a href="https://a3tal.com/p0011-camshaft-timing-over-advanced/">دليل P0011 العام وتقدم توقيت الكامة</a>. وللدائرة الكهربائية المختلفة تمامًا راجع <a href="https://a3tal.com/dtc-p0342-chevrolet/">P0342 وانخفاض إشارة حساس الكامة</a>. لا تنقل إجراءات تغيير الأجزاء من محرك آخر.</p></section>'''}
]
def call(path,payload=None,protected=True):
 h={"User-Agent":"A3tal-GSC-TopImpression-ConservativeRefresh/20261107","Accept":"application/json","Cache-Control":"no-store"}
 if protected:
  if not KEY:raise RuntimeError("Missing A3TAL_API_KEY")
  h["X-A3tal-Key"]=KEY;h["Authorization"]="Bearer "+KEY
 body=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf-8")
 if body is not None:h["Content-Type"]="application/json; charset=utf-8"
 u=(API if protected else SITE)+path
 with urllib.request.urlopen(urllib.request.Request(u,data=body,headers=h,method="POST" if body is not None else "GET"),timeout=150) as res:return json.load(res)
def pub(pid):
 return call("/wp-json/wp/v2/posts/"+str(pid)+"?_fields=id,slug,status,link,featured_media,yoast_head_json,modified_gmt",protected=False)
def main():
 if not KEY:raise RuntimeError("Missing key")
 for row in CASES:
  original=call("/post/"+str(row["id"]))
  public=pub(row["id"])
  if (original.get("id")!=row["id"] or original.get("status")!="publish" or
      urllib.parse.unquote(original.get("slug","")).strip("/")!=row["slug"] or
      not original.get("featured_media") or
      original.get("featured_media")!=public.get("featured_media")):
   raise RuntimeError("Live identity or image mismatch: "+row["slug"])
  oldseo=public.get("yoast_head_json") or {}
  if not oldseo.get("canonical") or not oldseo.get("og_image") or (oldseo.get("robots") or {}).get("index")=="noindex":
   raise RuntimeError("Canonical/index/image already broken: "+row["slug"])
  old=original.get("content","")
  if row["marker"] in old:
   print("GSC_UPDATE_ALREADY_APPLIED",original["link"],flush=True);continue
  if len(old)<2500 or old.lower().count("<h2")<3:
   raise RuntimeError("Unexpected original HTML: "+row["slug"])
  m=re.search(r"<h2(?:\s[^>]*)?>",old,re.I)
  if not m:raise RuntimeError("Missing first H2")
  new=old[:m.start()]+row["block"]+"\n"+old[m.start():]
  if new.count('id="'+row["marker"]+'"')!=1 or len(new)<len(old)+1050:
   raise RuntimeError("Wrong patch insertion")
  latest=call("/post/"+str(row["id"]))
  if latest.get("modified_gmt")!=original.get("modified_gmt"):
   raise RuntimeError("Concurrent editorial change: "+row["slug"])
  payload={"id":row["id"],"expected_modified_gmt":latest["modified_gmt"],"content":new,"meta":{
   "_yoast_wpseo_title":row["seo"],"_yoast_wpseo_metadesc":row["meta"],
   "_yoast_wpseo_focuskw":row["focus"],"_yoast_wpseo_opengraph-title":row["seo"],
   "_yoast_wpseo_opengraph-description":row["meta"],
   "_yoast_wpseo_twitter-title":row["seo"],"_yoast_wpseo_twitter-description":row["meta"]}}
  result=call("/update-post",payload)
  if result.get("error") or result.get("ok") is False:raise RuntimeError("Bridge declined patch "+row["slug"])
  verified=False
  for i in range(6):
   after=call("/post/"+str(row["id"])); live=pub(row["id"]); seo=live.get("yoast_head_json") or {}
   if row["marker"] in after.get("content","") and (seo.get("description") or "")==row["meta"]:
    if (after.get("featured_media")!=original.get("featured_media") or
        urllib.parse.unquote(after.get("slug","")).strip("/")!=row["slug"] or
        after.get("status")!="publish" or seo.get("canonical")!=oldseo.get("canonical") or
        (seo.get("og_image") or [{}])[0].get("url")!=(oldseo.get("og_image") or [{}])[0].get("url") or
        (seo.get("robots") or {}).get("index")=="noindex"):
      raise RuntimeError("WordPress post image/canonical/index changed unexpectedly")
    verified=True;print("GSC_TOP_QUERY_UPDATE_VERIFIED",row["id"],after["link"],flush=True);break
   time.sleep(3)
  if not verified:raise RuntimeError("Patch did not verify: "+row["slug"])
 print("A3TAL_GSC_THREE_EXISTING_PAGES_COMPLETE",flush=True)
if __name__=="__main__":main()
