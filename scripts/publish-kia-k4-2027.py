#!/usr/bin/env python3
"""Publish Kia K4 2027 Egypt with 3 automotive press photographs through the approved bridge."""
import os, io, json, time, re, base64, urllib.request, urllib.parse, urllib.error
from PIL import Image, ImageOps, ImageEnhance

BASE="https://a3tal.com"
API=BASE+"/wp-json/a3tal-direct/v1"
SECRET=os.getenv("A3TAL_API_KEY","")
SLUG="kia-k4-2027-egypt-prices-engines"
if not SECRET:raise SystemExit("A3TAL_API_KEY secret is missing")
TITLE="كيا K4 موديل 2027 تبدأ من 1.52 مليون جنيه.. هل يستحق محرك 190 حصانًا فرق 200 ألف؟"
SHORT="كيا K4 موديل 2027 في مصر تبدأ من 1,519,900 جنيه، وتصل إلى 1,859,900 جنيه. الأسعار والفئات والمحركان 123 و190 حصانًا والفروق قبل الحجز."
SEO_TITLE="سعر كيا K4 2027 في مصر: الفئات والمحرك 190 حصانًا"
SEO_DESC="أسعار كيا K4 موديل 2027 في مصر: Highline بسعر 1,519,900 جنيه، GT-line بسعر 1,719,900، وBlack Edition بسعر 1,859,900. الفرق الحقيقي بين الفئات والمحركين."
CONTENT=r"""
<p>أعلنت كيا مصر قائمة أسعار <strong>كيا K4 موديل 2027</strong>، لتبدأ السيدان الكورية من <strong>1,519,900 جنيه</strong> وتصل إلى <strong>1,859,900 جنيه</strong>. في وقت يبحث فيه مشترو السيارات الجديدة عن قيمة ما يدفعونه، تطرح K4 سؤالًا مختلفًا عن مجرد سعر الشراء: هل يكفي محرك الفئة الأولى بقوة 123 حصانًا، أم تستحق النسخة التيربو ذات 190 حصانًا دفع 200 ألف جنيه إضافية؟</p>
<p>الفرق بين أول وآخر فئة يصل إلى 340 ألف جنيه، لكن القصة لا تتعلق بالمظهر فقط. فالسيارة تتغير فيها مجموعة الحركة ونوع التعليق الخلفي وبعض التجهيزات. هنا نعرض قائمة الأسعار المنشورة في <strong>13 أكتوبر 2026</strong>، ونقارن الفئات وفق المواصفات المنشورة على موقع وكيل كيا المصري، مع توضيح الأشياء التي ينبغي التأكد منها قبل الحجز.</p>

<h2>أسعار كيا K4 موديل 2027 في مصر بعد التعديل</h2>
<div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table><thead><tr><th>الفئة</th><th>السعر الرسمي المعلن</th><th>الزيادة عن القائمة السابقة</th></tr></thead><tbody><tr><td>Highline</td><td><strong>1,519,900 جنيه</strong></td><td>20,000 جنيه</td></tr><tr><td>GT-line</td><td><strong>1,719,900 جنيه</strong></td><td>20,000 جنيه</td></tr><tr><td>GT-line Black Edition</td><td><strong>1,859,900 جنيه</strong></td><td>10,000 جنيه</td></tr></tbody></table></div>
<p>تطابق هذه الأسعار تغطية مصراوي في 13 أكتوبر، كما تُظهر حركة الأسعار المنشورة على هتلاقي الزيادات الثلاث من قوائم K4 السابقة. <a href="https://www.masrawy.com/autos/autos_news/details/2026/10/13/3062279/" target="_blank" rel="nofollow noopener">مصدر إعلان الأسعار: مصراوي</a>، مع <a href="https://eg.hatla2ee.com/ar/new-car/price-change" target="_blank" rel="nofollow noopener">سجل التغيرات في هتلاقي</a>.</p>
<p>أسعار الموقع الرسمي للوكيل قد تُعرض أحيانًا بقائمة قديمة قبل تحديثها، لذلك يعتمد هذا الخبر على السعر المنشور للقائمة الجديدة بتاريخها المحدد. يجب الحصول من الموزع على عرض سعر مكتوب، يتضمن موعد التسليم وسياسة الحجز، بدل الاعتماد على سعر قد يتغير من يوم لآخر.</p>

<h2>محرك 123 حصانًا أم 190 حصانًا؟ الفرق الحقيقي بين فئات K4</h2>
<p>تتوفر كيا K4 بمحركين مختلفين في مصر وفق <a href="https://kia.com.eg/ar/models/specifications/The_K4" target="_blank" rel="nofollow noopener">المواصفات المنشورة على موقع كيا مصر</a>. تستخدم فئة Highline محرك بنزين 1.6 لتر بدون تيربو يولد <strong>123 حصانًا</strong> وعزم <strong>151 نيوتن متر</strong> مع فتيس أوتوماتيك 6 سرعات. أما GT-line وBlack Edition فتستخدمان محرك 1.6 لتر تيربو بقوة <strong>190 حصانًا</strong> وعزم <strong>264 نيوتن متر</strong> مع أوتوماتيك 8 سرعات.</p>
<div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table><thead><tr><th>المواصفة</th><th>Highline</th><th>GT-line / Black</th></tr></thead><tbody><tr><td>المحرك</td><td>1.6 Gamma</td><td>1.6 T-GDI</td></tr><tr><td>القوة</td><td>123 حصانًا</td><td>190 حصانًا</td></tr><tr><td>العزم</td><td>151 نيوتن متر</td><td>264 نيوتن متر</td></tr><tr><td>الفتيس</td><td>6 سرعات أوتوماتيك</td><td>8 سرعات أوتوماتيك</td></tr><tr><td>التعليق الخلفي</td><td>Torsion Beam</td><td>Multi-Link</td></tr><tr><td>الجر</td><td>أمامي</td><td>أمامي</td></tr></tbody></table></div>
<p>الفارق البالغ <strong>67 حصانًا</strong> و113 نيوتن متر في العزم ليس تفصيلًا تسويقيًا، لكنه لا يخبر وحده عن جودة التجربة في الزحام أو استهلاك البنزين على الطرق المصرية. وحدها تجربة قيادة مناسبة توضح استجابة الفتيس وراحة التعليق، خصوصًا مع اختلاف التعليق الخلفي بين الفئات.</p>
{{a3tal_image:interior}}

<h2>هل تستحق GT-line زيادة 200 ألف جنيه على Highline؟</h2>
<p>هذه الزيادة لا تشتري جنوطًا أكبر فقط؛ فبحسب كيا مصر تنتقل السيارة إلى مجموعة حركة تيربو أقوى وناقل 8 سرعات وتعليق خلفي متعدد الوصلات، مع تجهيزات مثل عدادات رقمية 12.3 بوصة وتكييف أوتوماتيكي ثنائي المناطق ومبدلات سرعات خلف عجلة القيادة. لذلك فإن المقارنة هنا بين تجربتي قيادة وتجهيز مختلفتين، لا بين فئتين لديهما المحرك نفسه.</p>
<p>إذا كان الاستخدام الأساسي داخل المدينة وبمعدل كيلومترات محدود، فقد تكون Highline الاختيار الأكثر اتزانًا عندما تكفي قوتها للمالك. أما من يقود كثيرًا على الطرق السريعة ويهتم بالتسارع والمرونة أثناء التجاوز، فقد يجد النسخة التيربو أكثر ملاءمة بشرط حساب تكاليف الصيانة والتأمين والبنزين أولًا.</p>

<h2>ما الذي تضيفه Black Edition مقابل 140 ألف جنيه؟</h2>
<p>تستخدم الفئة الأعلى المحرك التيربو نفسه بقوة 190 حصانًا، لذلك لا تدفع 140 ألف جنيه لتحصل على قوة أكبر من GT-line. الفارق يتجه إلى المظهر وتجهيزات الراحة؛ إذ تُظهر قائمة كيا مصر تجهيزات مثل <strong>فتحة سقف واسعة، وشاحن هاتف لاسلكي، ومقعد سائق كهربائي، وجنوط سوداء 18 بوصة، ومصابيح أمامية متطورة</strong>. القاعدة البسيطة: اخترها إذا كانت هذه التجهيزات مهمة فعلًا في استخدامك اليومي، لا لأن اسمها أعلى فئة.</p>
<p>ويجب التأكد من القائمة الخاصة بالسيارة المتاحة في معرضك؛ فقد يختلف وصف الفئة بين تحديثات الموقع وكتيبات الوكيل وبعض المنشورات الإخبارية، كما أن تجهيزات السوق الأمريكية لا تُثبت تلقائيًا توافرها في مصر.</p>
{{a3tal_image:rear}}

<h2>الأبعاد والأمان والضمان في كيا K4</h2>
<p>طول السيارة <strong>4710 مم</strong> وعرضها 1850 مم وقاعدة عجلاتها 2720 مم بحسب مواصفات الوكيل، مع خزان بنزين 47 لترًا. وفي الأمان، تُظهر قائمة المواصفات أن أنظمة ABS والثبات الإلكتروني ESP ومراقبة ضغط الإطارات ومساعد صعود المرتفعات والوسائد الهوائية الأمامية والجانبية والستائرية أساسية في الفئات المذكورة. وتضيف الفئة الأعلى بعض وظائف تجنب الاصطدام المرتبطة بالنقطة العمياء وفق الجدول.</p>
<p>يعلن موقع الوكيل المصري ضمانًا لمدة <strong>5 سنوات أو 100 ألف كيلومتر</strong> وفق الشروط المعتمدة. هذه مواصفات منشورة لا تعني أن جميع تجهيزات مساعدة القيادة المذكورة في تقارير دولية موجودة في كل سيارة مصرية. افحص ورقة التجهيزات ورقم الفئة قبل التوقيع.</p>

<h2>كيا K4 أم سكودا أوكتافيا 2027: أيهما أقرب لاحتياجاتك؟</h2>
<p>تبدأ K4 من نحو 1.52 مليون جنيه، بينما تبدأ <a href="https://a3tal.com/skoda-octavia-2027-egypt-prices-trims/">سكودا أوكتافيا 2027 من 1.825 مليون جنيه</a> وفق القائمتين المنشورتين في أكتوبر. الفارق الأولي بين سعرَي البداية حوالي <strong>305 آلاف جنيه</strong>، لكنه ليس مقارنة فئة بفئة؛ فالمحركات وأنظمة التعليق والتجهيزات مختلفة، وقد يقترب سعر K4 التيربو من أوكتافيا الأساسية.</p>
<p>الأفضل تحديد ميزانية الشراء والتأمين والصيانة أولًا، ثم اختبار السيارة بمرافقة ركاب بالغين في المقاعد الخلفية وفحص مساحة الشنطة والرؤية عند الركن. للمقارنة مع الخيارات الاقتصادية أو الأعلى سعرًا يمكن الرجوع أيضًا إلى <a href="https://a3tal.com/اسعار-السيارات-الجديدة-في-مصر-2026/">دليل أسعار السيارات الجديدة في مصر</a> الذي يُحدّث دوريًا.</p>

<h2>قبل حجز كيا K4 الجديدة</h2>
<ol><li>اطلب عرضًا مكتوبًا بالسعر النهائي وموعد التسليم والتجهيزات ورقم الفئة.</li><li>جرّب فئتي المحرك إن أمكن، لأن فرق 200 ألف جنيه يشمل اختلافًا ميكانيكيًا مؤثرًا.</li><li>تأكد من كتالوج الصيانة ومواعيد الخدمة وأي شروط خاصة بالمحرك التيربو والضمان.</li><li>افحص وسائل الأمان الموجودة على السيارة المعروضة فعلًا بدل نقل قائمة سيارة أجنبية.</li><li>قارن قيمة التجهيزات الإضافية بالفارق المالي الحقيقي في عقد الشراء.</li></ol>

<h2>أسئلة شائعة عن كيا K4 2027</h2>
<h3>ما سعر كيا K4 موديل 2027 في مصر؟</h3><p>تبدأ Highline من 1,519,900 جنيه، وGT-line من 1,719,900 جنيه، وBlack Edition من 1,859,900 جنيه في قائمة 13 أكتوبر 2026. السعر الفعلي عند التسليم يحتاج تأكيدًا من الموزع.</p>
<h3>هل كل فئات كيا K4 فيها تيربو؟</h3><p>لا. فئة Highline تستخدم محرك 1.6 لتر بقوة 123 حصانًا وناقل 6 سرعات، بينما فئتا GT-line وBlack Edition تستخدمان 1.6 تيربو بقوة 190 حصانًا مع ناقل 8 سرعات.</p>
<h3>ما الفرق بين GT-line وBlack Edition؟</h3><p>القوة وناقل الحركة متشابهان وفق الوكيل. الفارق الأساسي في تجهيزات مثل فتحة السقف والشاحن اللاسلكي والمقعد الكهربائي والتفاصيل الخارجية، مقابل زيادة 140 ألف جنيه.</p>
<h3>هل كيا K4 تناسب الأسرة؟</h3><p>أبعادها وقاعدة عجلاتها تجعلها مرشحة للاستخدام العائلي، لكن الحكم النهائي يحتاج تجربة المقاعد الخلفية ومساحة الشنطة وراحة الركوب عمليًا. لا يُستنتج الاتساع من الأرقام وحدها.</p>

<p><small>آخر مراجعة: 14 أكتوبر 2026. الأسعار من قائمة 13 أكتوبر، والمواصفات من الوكيل المصري. الصور الصحفية من كيا مصر وكيا العالمية، وقد تختلف تجهيزات السيارة الظاهرة عن الفئة المتاحة في السوق المحلية.</small></p>
""".strip()

H={"X-A3tal-Key":SECRET,"Authorization":"Bearer "+SECRET,"User-Agent":"A3talKiaK4Publisher/1.0","Accept":"application/json"}
def get(url,data=None,secure=True,retries=3):
    link=url if url.startswith("https://") else API+url
    h=H.copy() if secure else {"User-Agent":"Mozilla/5.0 A3tal Editorial","Accept":"image/*,*/*"}
    body=json.dumps(data,ensure_ascii=False).encode("utf-8") if data is not None else None
    if body is not None:h["Content-Type"]="application/json"
    for i in range(retries if body is None else 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(link,headers=h,data=body),timeout=145) as r:
                out=r.read()
                return json.loads(out) if secure else out
        except Exception as ex:
            if i+1>=(retries if body is None else 1):raise
            print("GET retry",i+1,type(ex).__name__,str(ex)[:130],flush=True);time.sleep((i+1)*8)

def photo(url):
    raw=get(url,secure=False)
    img=Image.open(io.BytesIO(raw)).convert("RGB")
    if img.width<700 or img.height<450:raise RuntimeError("Source image too small: "+str(img.size))
    img=ImageOps.fit(img,(1600,900),method=Image.Resampling.LANCZOS,centering=(.5,.52))
    return ImageEnhance.Contrast(img).enhance(1.045)

def pack(img,filename,alt,role,placeholder=None):
    o=io.BytesIO();img.save(o,"WEBP",quality=84,method=6)
    p={"filename":filename,"title":alt,"alt":alt,"role":role,"convert_webp":False,"image_base64":base64.b64encode(o.getvalue()).decode("ascii")}
    if placeholder:p["placeholder"]=placeholder
    print("WEBP ready",filename,len(o.getvalue()),flush=True)
    return p

def main():
    st=get("/status");print("BRIDGE",st.get("version"),st.get("ok"),flush=True)
    if not st.get("ok"):raise RuntimeError("Bridge unavailable")
    items=get("/search-posts?"+urllib.parse.urlencode({"search":"كيا K4","limit":100,"status":"any"})).get("items",[])
    items2=get("/search-posts?"+urllib.parse.urlencode({"search":"كيا كي 4","limit":100,"status":"any"})).get("items",[])
    combined={x["id"]:x for x in items+items2}.values()
    same=[x for x in combined if x.get("slug")==SLUG]
    dup=[x for x in combined if x.get("slug")!=SLUG and ("2027" in x.get("title","")) and ("k4" in x.get("title","").lower() or "كي 4" in x.get("title",""))]
    print("Kia K4 existing",json.dumps(list(combined),ensure_ascii=False)[:2000],flush=True)
    if dup:raise RuntimeError("Potential K4 2027 duplicate, stop to review")
    chosen=[374]
    try:
        terms=get("/admin?op=terms&taxonomy=category&limit=500").get("result",[])
        for name in ["اسعار السيارات الجديدة","أسعار السيارات الجديدة","أسعار السيارات","أخبار السيارات"]:
            match=next((t for t in terms if t.get("name","").strip()==name),None)
            if match:chosen=[int(match["id"])];break
    except Exception as ex:print("Using established category 374",str(ex)[:100],flush=True)
    p={"title":TITLE,"slug":SLUG,"type":"post","status":"publish","excerpt":SHORT,"content":CONTENT,"categories":chosen,
       "meta":{"_yoast_wpseo_title":SEO_TITLE,"_yoast_wpseo_metadesc":SEO_DESC,"_yoast_wpseo_focuskw":"سعر كيا K4 2027 في مصر","_yoast_wpseo_canonical":BASE+"/"+SLUG+"/","_yoast_wpseo_opengraph-title":TITLE,"_yoast_wpseo_opengraph-description":SEO_DESC}}
    if same:p["id"]=same[0]["id"]
    images=[
      pack(photo("https://kia.com.eg/uploads/sliders/68ac0f925d3ed1756106642.jpg"),"kia-k4-2027-egypt-exterior-featured-a3tal.webp","كيا K4 السيدان بتصميمها الحديث على الطريق في صورة صحفية من كيا مصر","featured"),
      pack(photo("https://press.kia.com/content/dam/kiapress/SK/Pressreleases/2024/kia-k-4-2025/kia-k4-int-2-digital-1920x1080.jpg"),"kia-k4-2027-egypt-interior-a3tal.webp","مقصورة كيا K4 الرقمية وعجلة القيادة وشاشات العدادات - صورة صحفية من كيا","inline","{{a3tal_image:interior}}"),
      pack(photo("https://kia.com.eg/uploads/models/68908f7f293f91754304383.jpg"),"kia-k4-2027-egypt-rear-a3tal.webp","كيا K4 السيدان من الخلف على طريق مفتوح في صورة من كيا مصر","inline","{{a3tal_image:rear}}")
    ]
    print("Sending guarded publish bundle...",flush=True)
    try:result=get("/publish-bundle",{"post":p,"media":images})
    except Exception as ex:print("WRITE AMBIGUOUS. Do NOT blindly repeat.",str(ex)[:180],flush=True);raise
    pub=result.get("post",{}); pid=pub.get("id")
    print("WRITE_RESULT",json.dumps({"ok":result.get("ok"),"id":pid,"status":pub.get("status"),"link":pub.get("link"),"featured":pub.get("featured_media"),"media":{k:v.get("url") for k,v in result.get("media",{}).items()}},ensure_ascii=False),flush=True)
    if not result.get("ok") or not pid or pub.get("status")!="publish" or not pub.get("featured_media"):raise RuntimeError("Post wasn't published with featured")
    chk=get("/post/"+str(pid));content=chk.get("content","")
    if chk.get("status")!="publish" or chk.get("featured_media")!=pub.get("featured_media") or "{{a3tal_image:" in content or len(re.findall(r"<img\b",content))<2:raise RuntimeError("Image/post readback failed")
    link=chk.get("link") or pub.get("link")
    print("ARTICLE_CONFIRMED",link,"ID",pid,"FEATURED",pub.get("featured_media"),flush=True)
    ent={"op":"platform_entity_upsert","type":"a3_car","slug":"kia-k4-2027-egypt","title":"كيا K4 موديل 2027 في مصر","status":"publish",
         "content":'<p>كيا K4 موديل 2027 السيدان في مصر من 1,519,900 حتى 1,859,900 جنيه. محرك 1.6 لتر بقوة 123 حصانًا في Highline، ومحرك 1.6 تيربو 190 حصانًا في فئتي GT-line وBlack Edition. <a href="'+link+'">عرض الأسعار والفئات والمقارنة الكاملة</a>.</p>',
         "excerpt":SHORT,"featured_media":pub.get("featured_media"),"taxonomies":{"a3_brand":["kia"],"a3_market":["egypt"],"a3_car_body":["sedan"]},
         "meta":{"_a3_year":"2027","_a3_price_min":"1519900","_a3_price_max":"1859900","_a3_currency":"EGP","_a3_engine_cc":"1591","_a3_power_hp":"123","_a3_torque_nm":"151","_a3_transmission":"أوتوماتيك 6 سرعات / 8 سرعات تيربو","_a3_fuel":"بنزين","_a3_drivetrain":"أمامي","_a3_seats":"5","_a3_source_url":link,"_a3_source_checked_at":"2026-10-14","_a3_related_post_ids":str(pid)}}
    try:
        cars=json.loads(get(BASE+"/wp-json/wp/v2/a3tal-cars?"+urllib.parse.urlencode({"slug":"kia-k4-2027-egypt","per_page":2}),secure=False))
        if len(cars)>1:raise RuntimeError("Duplicate car entities")
        er=get("/admin",ent)
        if not er.get("ok"):raise RuntimeError("Entity update not acknowledged")
        print("CAR_ENTITY_CONFIRMED",json.dumps({"id":er.get("result",{}).get("id"),"link":er.get("result",{}).get("link")},ensure_ascii=False),flush=True)
    except Exception as ex:print("CAR_ENTITY_NEEDS_RECHECK",str(ex)[:150],flush=True)
    for wait in (0,12,20,34):
        if wait:time.sleep(wait)
        try:
            html=get(link+"?a3tal_verify="+str(int(time.time())),secure=False,retries=1).decode("utf-8","replace")
            if "كيا K4" not in html or "og:image" not in html or "kia-k4-2027-egypt-exterior-featured-a3tal" not in html:
                raise RuntimeError("Title/og:image missing in public HTML")
            print("PUBLIC_HTML_VERIFIED",link,"og:image correct",flush=True);return
        except Exception as ex:print("PUBLIC_RETRY",str(ex)[:160],flush=True)
    raise RuntimeError("Article is published but CDN og:image not yet verified: "+link)
if __name__=="__main__":main()
