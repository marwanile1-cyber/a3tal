#!/usr/bin/env python3
"""Publish Octavia 2027 Egypt editorial and attach it to the car directory using A3tal Direct Bridge."""
import os, json, re, base64, io, time, urllib.request, urllib.parse, urllib.error
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

BASE = "https://a3tal.com"
API = BASE + "/wp-json/a3tal-direct/v1"
KEY = os.environ.get("A3TAL_API_KEY", "")
SLUG = "skoda-octavia-2027-egypt-prices-trims"
if not KEY: raise SystemExit("Missing A3TAL_API_KEY")
TITLE = "سكودا أوكتافيا 2027 تبدأ من 1.825 مليون جنيه في مصر.. هل تستحق فرق 425 ألف بين الفئات؟"
YOAST_TITLE = "سعر سكودا أوكتافيا 2027 في مصر.. 3 فئات حتى 2.25 مليون"
DESC = "أسعار سكودا أوكتافيا 2027 في مصر تبدأ من 1,825,000 جنيه. قارن Loft وLounge وSuite، ومواصفات محرك 1.4 TSI وفرق 425 ألف جنيه قبل الشراء."
EXCERPT = "سكودا أوكتافيا 2027 في مصر: الفئة Loft بسعر 1.825 مليون، Lounge بسعر 2.05 مليون، Suite بسعر 2.25 مليون. الأسعار ومواصفات 1.4 TSI وكيف تختار الفئة الأنسب."
CONTENT = r"""
<p><strong>سكودا أوكتافيا موديل 2027</strong> وصلت إلى قائمة الأسعار الجديدة في مصر بثلاث فئات تبدأ من <strong>1,825,000 جنيه</strong> وتصل إلى <strong>2,250,000 جنيه</strong>. وأعلنت كيان إيجيبت، وكيل سكودا المحلي، الأسعار التي نشرتها الصحافة المتخصصة يوم 13 أكتوبر 2026، لتعيد السيارة سؤالًا مهمًا إلى سوق السيدان: هل تكفي الفئة Loft، أم تستحق Lounge وSuite دفع مئات الآلاف الإضافية؟</p>
<p>الفارق بين أول فئة وآخر فئة يبلغ <strong>425 ألف جنيه</strong>، وهو مبلغ لا يُحسم بمظهر الجنوط والشاشة وحدهما. في هذا التقرير من أعطال.كوم نراجع الأسعار الرسمية، وما هو معروف عن المحرك وناقل الحركة، وكيف يتحقق المشتري من اختلاف تجهيزات كل فئة قبل دفع الحجز، دون خلط مواصفات النسخ الأوروبية بالمواصفات المصرية.</p>

<h2>أسعار سكودا أوكتافيا 2027 الرسمية في مصر</h2>
<div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table><thead><tr><th scope="col">فئة سكودا أوكتافيا 2027</th><th scope="col">السعر الجديد</th><th scope="col">الزيادة الأخيرة المسجلة</th></tr></thead><tbody><tr><td>Selection Loft</td><td><strong>1,825,000 جنيه</strong></td><td>25,000 جنيه</td></tr><tr><td>Selection Lounge</td><td><strong>2,050,000 جنيه</strong></td><td>50,000 جنيه</td></tr><tr><td>Selection Suite</td><td><strong>2,250,000 جنيه</strong></td><td>100,000 جنيه</td></tr></tbody></table></div>
<p>الأسعار الثلاثة تطابق القائمة المنشورة عن كيان إيجيبت بتاريخ 13 أكتوبر 2026، بينما أورد موقع «هتلاقي» زيادات 25 و50 و100 ألف جنيه مقارنة بالقيم التي كانت مسجلة مباشرة قبل تحديث الأسعار. قد تختلف قيمة الزيادة عند المقارنة بقائمة أقدم خاصة بموديل 2026، لذلك لا يصح اعتبار كل رقم منشور للزيادة المقارنةَ نفسها.</p>
<p>المصدران: <a href="https://almalnews.com/2140872/" target="_blank" rel="nofollow noopener">جريدة المال: قائمة الوكيل</a> و<a href="https://eg.hatla2ee.com/ar/new-car/price-change/skoda" target="_blank" rel="nofollow noopener">هتلاقي: سجل تغيّر الأسعار</a>. هذه أسعار معلنة وليست تأكيدًا بتوفر كل لون وفئة لدى كل معرض، كما أن مصروفات الترخيص والتأمين لا تُعد مشمولة تلقائيًا.</p>

<h2>425 ألف جنيه بين أول وآخر فئة.. أين يذهب فرق السعر؟</h2>
<p>الانتقال من Loft إلى Lounge يحتاج <strong>225 ألف جنيه</strong> إضافية، ثم تحتاج Suite إلى <strong>200 ألف جنيه</strong> أخرى. لا تعني هذه الفروق زيادة أداء المحرك بالضرورة؛ الفكرة الأساسية في مستويات التجهيز والراحة. لهذا لا يكفي اتخاذ قرار الشراء بناءً على سعر الفئة الأعلى أو شكلها في الصور.</p>
<p>نشرة تجهيزات أوكتافيا المنشورة على موقع سكودا مصر للنسخة الأقدم MY2025 تذكر فروقًا في مقاسات الجنوط وبعض وظائف الإضاءة وتجهيزات صندوق الأمتعة بين Loft وLounge وSuite. لكنها <strong>ليست بديلًا عن ورقة مواصفات موديل 2027 المصري</strong>. قبل الحجز، اطلب من الوكيل جدول فئتك المكتوب وحدد التجهيزات المهمة شخصيًا: عدد الوسائد الهوائية، نوع المصابيح، كاميرات الركن، فتح الشنطة، المقعد الكهربائي، والتجهيزات التي تدفع مقابلها.</p>
{{a3tal_image:cockpit}}

<h3>متى تكون Loft الاختيار الأذكى؟</h3>
<p>إذا كان المطلوب سيارة عائلية بالمحرك وناقل الحركة الأساسيين نفسهما، ولا تحتاج تجهيزات الرفاهية الأعلى، فقد تكون Loft الأكثر اتزانًا من ناحية الميزانية. الأهم أن تراجع قائمة الأمان الفعلية وتجرّب المقعد والشاشة والركن قبل الاكتفاء بوصف «الفئة الأولى».</p>
<h3>ومتى تستحق Lounge أو Suite الزيادة؟</h3>
<p>عندما تكون تجهيزات إضافية محددة ضمن أولويات الاستخدام اليومي، لا مجرد رغبة في امتلاك أعلى فئة. قارن قيمة كل تجهيز تحتاجه بالفارق الكامل، وفكر أيضًا في تكلفة التأمين والإطارات والصيانة المرتبطة بالفئة التي تختارها.</p>

<h2>محرك سكودا أوكتافيا A8 موديل 2027 وناقل الحركة</h2>
<p>تعتمد أوكتافيا المصرية بمحرك <strong>1.4 لتر TSI تيربو</strong> بقوة <strong>150 حصانًا</strong> وعزم <strong>250 نيوتن متر</strong> متصل بناقل <strong>أوتوماتيكي 8 سرعات</strong> مع جر أمامي، وفق البيانات المنشورة للسوق المصري وصفحة سكودا الإقليمية للمحرك. وهي نقطة تستحق التدقيق لأن البعض يخلط بين فتيس أوكتافيا A8 المصرية وناقل DSG الموجود في نسخ وأجيال أخرى.</p>
<div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table><thead><tr><th>البند</th><th>المواصفة المرجعية</th></tr></thead><tbody><tr><td>المحرك</td><td>1.4 TSI بنزين تيربو</td></tr><tr><td>القوة</td><td>150 حصانًا</td></tr><tr><td>العزم</td><td>250 نيوتن متر</td></tr><tr><td>ناقل الحركة</td><td>أوتوماتيكي 8 سرعات</td></tr><tr><td>نظام الدفع</td><td>أمامي</td></tr></tbody></table></div>
<p>وتنشر سكودا الشرق الأوسط هذه المواصفات للمحرك ذاته. أما أرقام التسارع والاستهلاك فهي أرقام اختبارية تختلف ظروفها عن ازدحام القاهرة وطبيعة القيادة الفعلية، فلا ينبغي تحويلها إلى وعد بمعدل استهلاك ثابت. راجع <a href="https://www.skoda-me.com/models/octavia/selection" target="_blank" rel="nofollow noopener">مواصفات المحرك على موقع سكودا الإقليمي</a>، واقرأ أيضًا دليل أعطال.كوم حول <a href="https://a3tal.com/skoda-octavia-dsg-transmission-problems/">الفرق بين فتيس أوكتافيا A7 وA8</a>.</p>

<h2>هل أوكتافيا 2027 سيارة جديدة بالكامل؟</h2>
<p>رقم سنة الموديل لا يعني وحده ظهور جيل جديد أو محرك مختلف. أوكتافيا الحالية تنتمي إلى الجيل الرابع الذي حصل على تحديثات تصميمية وتقنية، ومن أبرز سماته واجهة أمامية ومصابيح بتصميم مختلف عن النسخ السابقة. لكن المعروض في مصر قد يختلف تفصيليًا عن سيارات التصوير الأوروبية في تجهيزات المقصورة وأنظمة المساعدة.</p>
<p>من يهمه الاختيار بين موديل 2026 و2027 عليه مقارنة رقم الشاسيه وسنة الصنع وقائمة التجهيزات وتاريخ الضمان، ثم تقدير فرق السعر الحقيقي في عرض البيع. لا يكفي أن يقول البائع «الشكل الجديد» دون تحديد ما تغير بالفعل.</p>
{{a3tal_image:seats}}

<h2>هل تستحق سكودا أوكتافيا 2027 السعر بعد الزيادات؟</h2>
<p>أهم نقاط قوة أوكتافيا على الورق هي التركيز على الاستخدام العائلي، والمحرك التيربو المناسب للطرق السريعة، وناقل الحركة ذي الثماني سرعات، مع تدرج واضح في الفئات. في المقابل، بلوغ أعلى فئة 2.25 مليون جنيه يفرض مقارنتها بسيارات أخرى في الفئة السعرية نفسها وبعروض الوكلاء الفعلية، وليس الاكتفاء بالمواصفات المكتوبة.</p>
<p>قبل قرار الشراء، من الأفضل تجربة ثلاثة أمور: مساحة المقعد الخلفي والشنطة مع احتياجات الأسرة، وثبات السيارة وراحتها على نوع الطرق المستخدمة يوميًا، وتكلفة الضمان والصيانة والإطارات. دليل <a href="https://a3tal.com/skoda-octavia-maintenance-prices-guide-2026/">صيانة سكودا أوكتافيا A8</a> على أعطال.كوم يساعد في فهم أهمية مواصفات الزيت ومواعيد الخدمة. ولمن يفكر في سوق المستعمل بدلًا من دفع سعر الزيرو، تتوفر <a href="https://a3tal.com/used-skoda-prices-egypt-2026/">مقارنة أسعار سكودا المستعملة</a>.</p>

<h2>5 أمور تحقق منها قبل حجز أوكتافيا 2027</h2>
<ol><li>اطلب قائمة تجهيزات مكتوبة للفئة ورقم الموديل، ولا تعتمد على صور نسخة خارج مصر.</li><li>تأكد من سعر التسليم النهائي وموعده وسياسة رد مبلغ الحجز.</li><li>راجع تاريخ بدء الضمان ومواعيد الصيانة وقيمة الزيارة الدورية وفق الكتالوج المعتمد.</li><li>جرّب السيارة على طريق مشابه لاستخدامك اليومي، وخصوصًا الراحة والعزل والرؤية.</li><li>قارن قيمة الانتقال بين Loft وLounge وSuite بالتجهيزات التي ستستخدمها فعليًا.</li></ol>
<p>يمكن الرجوع كذلك إلى <a href="https://a3tal.com/skoda-new-car-prices-egypt-2026/">دليل أسعار سيارات سكودا 2026</a> للمقارنة التاريخية، مع الانتباه إلى أن الأسعار القديمة ليست بالضرورة أسعار البيع المتاحة الآن.</p>

<h2>أسئلة شائعة عن سكودا أوكتافيا 2027</h2>
<h3>كم سعر سكودا أوكتافيا 2027 في مصر؟</h3><p>تبدأ فئة Loft من 1,825,000 جنيه، وسعر Lounge هو 2,050,000 جنيه، وتصل Suite إلى 2,250,000 جنيه وفق القائمة المنشورة في 13 أكتوبر 2026. تأكد من سعر التسليم والتوفر لدى الوكيل.</p>
<h3>ما الفرق السعري بين Loft وSuite؟</h3><p>425 ألف جنيه. الفرق إلى Lounge وحدها 225 ألف جنيه، ثم 200 ألف جنيه إضافية إلى Suite. تحديد الفئة الأفضل يعتمد على تجهيزاتها المصرية الموثقة واحتياجات المشتري.</p>
<h3>هل فتيس أوكتافيا A8 المصرية DSG؟</h3><p>النسخة المصرية بمحرك 1.4 TSI تستخدم ناقل حركة أوتوماتيكي من 8 سرعات، ولا ينبغي خلطها ببعض نسخ وأجيال أوكتافيا الأخرى المزودة بناقل DSG.</p>
<h3>هل موديل 2027 مختلف جذريًا عن 2026؟</h3><p>لا يكفي تغيير سنة الموديل لإثبات وجود جيل مختلف. المرجع هو قائمة المواصفات المحلية ورقم السيارة الفعلي. قبل الشراء، اطلب مقارنة مكتوبة بين الفئتين وسنتَي الموديل.</p>

<p><small>آخر مراجعة للأسعار: 14 أكتوبر 2026. مصادر الصور: Škoda Auto / Škoda Storyboard، صور صحفية للجيل الرابع المُحدّث بهدف التوضيح، وقد تختلف تفاصيل السوق المصري والفئات. الأسعار قابلة للتغيير.</small></p>
"""
HEADERS = {"X-A3tal-Key":KEY, "Authorization":"Bearer "+KEY, "User-Agent":"A3talOctaviaPublisher/1.0", "Accept":"application/json"}

def request(url, payload=None, secure=True, tries=3):
    address = url if url.startswith("https://") else API+url
    h = dict(HEADERS if secure else {"User-Agent":"A3tal.com automotive editorial","Accept":"*/*"})
    data = None
    if payload is not None:
        h["Content-Type"]="application/json"
        data=json.dumps(payload,ensure_ascii=False).encode("utf-8")
    for i in range(tries if payload is None else 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(address,data=data,headers=h),timeout=150) as resp:
                raw=resp.read()
                return json.loads(raw) if secure else raw
        except (urllib.error.URLError, TimeoutError) as ex:
            if payload is not None or i==tries-1: raise
            print("Read retry", i+1, type(ex).__name__, str(ex)[:100], flush=True)
            time.sleep(10*(i+1))

def photo(url, size=(1600,900)):
    raw=request(url,secure=False)
    im=Image.open(io.BytesIO(raw)).convert("RGB")
    if min(im.size)<700: raise RuntimeError("Poor-quality source image")
    im=ImageOps.fit(im,size,method=Image.Resampling.LANCZOS,centering=(0.5,0.48))
    im=ImageEnhance.Contrast(im).enhance(1.045)
    im=ImageEnhance.Color(im).enhance(1.045)
    return im

def media(im, filename, alt, role, placeholder=None):
    out=io.BytesIO(); im.save(out,"WEBP",quality=86,method=6)
    print("Prepared",filename,len(out.getvalue()),im.size,flush=True)
    p={"filename":filename,"title":alt,"alt":alt,"role":role,"convert_webp":False,"image_base64":base64.b64encode(out.getvalue()).decode("ascii")}
    if placeholder: p["placeholder"]=placeholder
    return p

def categories():
    try:
        r=request("/admin?op=terms&taxonomy=category&limit=500")
        terms=r.get("result",[])
        for key in ("أسعار السيارات الجديدة","اسعار السيارات الجديدة","أسعار السيارات","أخبار السيارات"):
            x=next((x for x in terms if x.get("name","").strip()==key),None)
            if x: return [int(x["id"])]
    except Exception as e: print("Category lookup fallback:",str(e)[:150],flush=True)
    return [374]

def main():
    status=request("/status"); print("BRIDGE STATUS:",status.get("version"),status.get("ok"),flush=True)
    if not status.get("ok"): raise RuntimeError("Bridge is unavailable")
    qs=urllib.parse.urlencode({"search":"أوكتافيا 2027","limit":100,"status":"any"})
    hits=request("/search-posts?"+qs).get("items",[])
    same=[p for p in hits if p.get("slug")==SLUG]
    competing=[p for p in hits if p.get("slug")!=SLUG and "2027" in p.get("title","") and ("أوكتافيا" in p.get("title","") or "octavia" in p.get("title","").lower())]
    print("Existing Octavia candidates:",json.dumps(hits,ensure_ascii=False)[:2400],flush=True)
    if competing: raise RuntimeError("Potential duplicate 2027 Octavia article: "+str(competing[:4]))
    post={"title":TITLE,"slug":SLUG,"type":"post","status":"publish","excerpt":EXCERPT,"content":CONTENT,"categories":categories(),"meta":{
        "_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc":DESC,
        "_yoast_wpseo_focuskw":"سعر سكودا أوكتافيا 2027 في مصر",
        "_yoast_wpseo_canonical":BASE+"/"+SLUG+"/",
        "_yoast_wpseo_opengraph-title":TITLE,
        "_yoast_wpseo_opengraph-description":DESC
    }}
    if same:
        post["id"]=same[0]["id"]
        print("Updating canonical existing post",post["id"],flush=True)
    hero=photo("https://cdn.skoda-storyboard.com/2024/02/OCT_FL_004a_low-copy_437ebc70-1440x810.jpg")
    cockpit=photo("https://cdn.skoda-storyboard.com/2024/02/OCT_FL_044_low_407b6fbc-1440x1080.jpg")
    seats=photo("https://cdn.skoda-storyboard.com/2024/02/OCT_FL_097_low_ba269fc2-1440x1080.jpg")
    pictures=[
        media(hero,"skoda-octavia-2027-egypt-prices-a3tal-hero.webp","سكودا أوكتافيا A8 فيس ليفت من الأمام - أسعار مصر موديل 2027","featured"),
        media(cockpit,"skoda-octavia-2027-egypt-cockpit-a3tal.webp","المقصورة الأمامية لسكودا أوكتافيا A8 المُحدثة - صورة من سكودا","inline","{{a3tal_image:cockpit}}"),
        media(seats,"skoda-octavia-2027-egypt-rear-seats-a3tal.webp","مقاعد سكودا أوكتافيا الخلفية - صورة تصميمية رسمية","inline","{{a3tal_image:seats}}")
    ]
    print("PUBLISH BUNDLE: sending article + 3 WEBP photos...",flush=True)
    try:
        res=request("/publish-bundle",{"post":post,"media":pictures})
    except Exception as e:
        print("WRITE UNCONFIRMED. Do not blindly retry: ",str(e)[:240],flush=True);raise
    p=res.get("post",{}); pid=p.get("id")
    print("BRIDGE RESULT",json.dumps({"ok":res.get("ok"),"post":p,"media":{k:{"media_id":v.get("media_id"),"url":v.get("url"),"mime":v.get("mime")} for k,v in res.get("media",{}).items()}},ensure_ascii=False)[:3500],flush=True)
    if not res.get("ok") or not pid or p.get("status")!="publish" or not p.get("featured_media"): raise RuntimeError("Not fully published")
    checked=request("/post/"+str(pid)); content=checked.get("content","")
    if checked.get("status")!="publish" or checked.get("featured_media")!=p.get("featured_media") or "{{a3tal_image:" in content or len(re.findall(r"<img\b",content))<2:
        raise RuntimeError("POST READBACK failed: images not set in published article")
    url=checked.get("link") or p.get("link")
    print("PUBLISHED_CONFIRMED",url,"POST_ID",pid,"FEATURED_MEDIA",p["featured_media"],"INLINE_IMAGES",len(re.findall(r"<img\b",content)),flush=True)
    # Associate the news with the car catalog to fill the recent-cars module.
    entity={
      "op":"platform_entity_upsert","type":"a3_car","slug":"skoda-octavia-2027-egypt",
      "title":"سكودا أوكتافيا 2027 في مصر","status":"publish",
      "content":'<p>سكودا أوكتافيا A8 موديل 2027 في مصر بثلاث فئات: Loft بسعر 1,825,000 جنيه، Lounge بسعر 2,050,000 جنيه، وSuite بسعر 2,250,000 جنيه. محرك 1.4 TSI بقوة 150 حصانًا، وعزم 250 نيوتن متر، وناقل أوتوماتيكي 8 سرعات.</p><p>اقرأ <a href="'+url+'">الأسعار والفروق بين الفئات والمواصفات وما يجب مراجعته قبل الشراء</a> في دليل أعطال.كوم.</p>',
      "excerpt":EXCERPT,"featured_media":p["featured_media"],
      "taxonomies":{"a3_brand":["skoda"],"a3_market":["egypt"],"a3_car_body":["sedan"]},
      "meta":{
        "_a3_year":"2027","_a3_price_min":"1825000","_a3_price_max":"2250000","_a3_currency":"EGP",
        "_a3_engine_cc":"1395","_a3_power_hp":"150","_a3_torque_nm":"250","_a3_transmission":"أوتوماتيك 8 سرعات",
        "_a3_fuel":"بنزين","_a3_drivetrain":"أمامي","_a3_seats":"5",
        "_a3_source_url":url,"_a3_source_checked_at":"2026-10-14","_a3_related_post_ids":str(pid)
      }
    }
    try:
        existing=json.loads(request(BASE+"/wp-json/wp/v2/a3tal-cars?"+urllib.parse.urlencode({"slug":"skoda-octavia-2027-egypt","per_page":2}),secure=False))
        if len(existing)>1: raise RuntimeError("Duplicate Octavia 2027 cars found")
        er=request("/admin",entity)
        if not er.get("ok"): raise RuntimeError("Car platform bridge upsert returned not ok")
        print("CAR_ENTITY_PUBLISHED:",json.dumps({"id":er.get("result",{}).get("id"),"link":er.get("result",{}).get("link")},ensure_ascii=False),flush=True)
    except Exception as e:
        print("CAR_ENTITY_WARNING: Article is already published; car-card update requires checking.",type(e).__name__,str(e)[:220],flush=True)
    # Cache/CDN verification; distinct from direct bridge state.
    for pause in [0,12,24,40]:
        if pause:time.sleep(pause)
        try:
            html=request(url+"?a3tal_check="+str(int(time.time())),secure=False,tries=2).decode("utf-8","replace")
            if "سكودا أوكتافيا" not in html:raise RuntimeError("title not visible yet")
            if "og:image" not in html:raise RuntimeError("og:image is missing")
            if not re.search("skoda-octavia-2027-egypt-prices-a3tal-hero",html,re.I):raise RuntimeError("hero/OG image URL missing")
            print("PUBLIC_HTML_VERIFIED:",url,"og:image, article headline and featured image present",flush=True)
            return
        except Exception as e:print("PUBLIC_VERIFY_RETRY:",str(e)[:220],flush=True)
    raise RuntimeError("Published in bridge but public CDN og:image needs recheck: "+url)

if __name__=="__main__": main()
