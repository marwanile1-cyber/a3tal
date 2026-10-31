#!/usr/bin/env python3
"""Update existing BYD F3, Soueast S07 and BYD prices hub with dated, source-qualified market facts.
Never create replacement posts; protect editorial revisions and existing featured/OG images.
"""
import os, re, json, time, urllib.request, urllib.parse
SITE="https://a3tal.com"; BRIDGE=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
MARK="A3TAL-PRICE-OPPORTUNITIES-20261031"
PAGES=[
 {"id":82348,"slug":"byd-f3-price-egypt","date":"2026-10-02T00:54:43","cover":80220,"kind":"byd"},
 {"id":80530,"slug":"soueast-s07-price-specs-egypt-2026","date":"2026-10-02T00:57:09","cover":80532,"kind":"s07"},
 {"id":80219,"slug":"byd-prices-2026-misr","date":"2026-09-20T16:26:21","cover":80220,"kind":"hub"},
]
def request(url,payload=None,auth=False):
 headers={"Accept":"application/json","Cache-Control":"no-cache,no-store","User-Agent":"A3tal-Price-Accuracy-RevisionGuard/20261031"}
 if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
 data=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
 if data is not None:headers["Content-Type"]="application/json; charset=utf-8"
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers,data=data,method="POST" if data is not None else "GET"),timeout=120) as response:return json.load(response)
def wp(item):
 return request(SITE+"/wp-json/wp/v2/posts/"+str(item["id"])+"?"+urllib.parse.urlencode({
 "_fields":"id,title,slug,modified_gmt,status,featured_media,content,link,yoast_head_json,categories",
 "_price_audit":"20261031"}))
def place_before_first_heading(h,insert):
 pattern=r"(?=<h2(?:\s|>))"
 if len(re.findall(pattern,h,re.I))<3: raise RuntimeError("Missing expected existing headings")
 return re.sub(pattern,lambda m:insert+"\n",h,count=1,flags=re.I)
def s07(old):
 h=old
 original_prices={"1,390,000": "1,415,000","1,530,000":"1,555,000",
                  "1.39 مليون":"1.415 مليون","1.53 مليون":"1.555 مليون"}
 if h.count("1,390,000")<2 or h.count("1,530,000")<2:
  raise RuntimeError("S07 old prices not where expected")
 for a,b in original_prices.items():h=h.replace(a,b)
 # The 2026 model prices stay in their separate historical inventory paragraph.
 # Update only the dates associated with current 'last checked', not general past comparisons.
 h=h.replace("آخر مراجعة: 20 سبتمبر 2026","آخر مراجعة: 31 أكتوبر 2026")
 h=h.replace("وقت المراجعة في 20 سبتمبر 2026","في مراجعة 31 أكتوبر 2026")
 aside=(
 '<aside id="'+MARK+'-S07" dir="rtl" style="border-right:4px solid #0ea5e9;background:#f8fafc;'
 'padding:15px 18px;border-radius:10px;margin:22px 0">'
 '<h3>أسعار ساوإيست S07 موديل 2027 بعد زيادة أكتوبر</h3>'
 '<p><strong>تحديث 31 أكتوبر 2026:</strong> أظهرت قائمة MANEAST التي نشرتها مواقع سيارات متخصصة '
 'ارتفاعًا بمقدار <strong>25,000 جنيه</strong> لكل فئة يوم 19 أكتوبر. '
 'أصبح سعر Highline موديل 2027 <strong>1,415,000 جنيه</strong> بدل 1,390,000، '
 'وPremium <strong>1,555,000 جنيه</strong> بدل 1,530,000 جنيه. '
 'الفارق بين الفئتين <strong>140 ألف جنيه</strong>؛ وهو فرق يشمل اختلاف المحرك والتجهيزات.</p>'
 '<div class="g-table-wrap"><table><thead><tr><th>الفئة</th><th>قبل الزيادة</th><th>بعد الزيادة</th>'
 '</tr></thead><tbody><tr><td>Highline 2027</td><td>1,390,000 جنيه</td><td>1,415,000 جنيه</td>'
 '</tr><tr><td>Premium 2027</td><td>1,530,000 جنيه</td><td>1,555,000 جنيه</td></tr></tbody></table></div>'
 '<p>هذه أسعار منشورة نقلًا عن قائمة الوكيل، وليست عرض بيع ملزمًا من موزع بعينه. '
 'تأكد من سعر التسليم والفئة وسنة الموديل والضمان في فاتورة الحجز. '
 'لا تخلط بينها وبين عروض المخزون من موديل 2026.</p>'
 '<p><strong>المصادر:</strong> '
 '<a href="https://eg.hatla2ee.com/ar/new-car/soueast/S%2B07">سجل تغيرات الأسعار في هتلاقي</a>، '
 '<a href="https://www.contactcars.com/ar/new-cars/soueast-s_07">كونتكت كارز</a>، '
 '<a href="https://www.soueast-egypt.com/models/s07">المواصفات الرسمية من SOUEAST مصر</a>.</p>'
 '</aside>'
 )
 h=place_before_first_heading(h,aside)
 # Distinguish existing former reference 2026 vs 2027.
 assert h.count('id="'+MARK+'-S07"')==1
 if "1,415,000" not in h or "1,555,000" not in h:return None
 return {"html":h,"title":"سعر ساوايست S07 في مصر: فئات 2027 بعد زيادة أكتوبر",
         "meta":"سعر ساوايست S07 موديل 2027 في مصر بعد زيادة أكتوبر: Highline بـ1,415,000 جنيه وPremium بـ1,555,000 جنيه، مع فرق المحركات والمواصفات والعيوب.",
         "keyword":"سعر ساوايست S07 في مصر"}
def byd(old):
 h=old
 aside=(
 '<aside id="'+MARK+'-BYD" dir="rtl" style="border-right:4px solid #0ea5e9;'
 'background:#f8fafc;padding:15px 18px;border-radius:10px;margin:20px 0">'
 '<h3>سعر BYD F3 خلال أكتوبر: لماذا تختلف سنة الموديل بين المصادر؟</h3>'
 '<p><strong>آخر تحقق 31 أكتوبر 2026:</strong> تعرض صفحة <a href="https://bydegypt.com/byd-f3/">'
 'BYD Egypt الرسمية</a> السيارة ضمن <strong>موديل 2025</strong>. في المقابل، '
 '<a href="https://ellithy.com/new-vehicles/284">صفحة الليثي للسيارات</a> '
 'تعلن BYD F3 بوصفها <strong>موديل 2026</strong> (آخر تحديث مدون لديها 1 سبتمبر). '
 'إذن لا يصح القول إن موديل 2026 غير موجود قطعًا، ولا الجزم بأن كل المعروض موديل 2026. '
 'سنة الموديل الحقيقية تُحسم من فاتورة السيارة والمستندات ورقم الشاسيه، ومطابقتها مع جهة البيع.</p>'
 '<div class="g-table-wrap"><table><thead><tr><th>الفئة</th><th>سعر مكتوب بوصفه رسميًا على موقع الموزع</th><th>سعر البيع الظاهر لديه</th>'
 '</tr></thead><tbody><tr><td>1.5 M/T</td><td>650,000 جنيه</td><td>660,000 جنيه</td></tr>'
 '<tr><td>1.5 A/T</td><td>730,000 جنيه</td><td>740,000 جنيه</td></tr></tbody></table></div>'
 '<p>هذه بيانات إعلان تجاري لموزع، ولا تمثل إثباتًا بأن BYD Egypt أعلنت سعرًا رسميًا جديدًا '
 'لموديل 2026 على موقعها. بعض مواقع السوق تعرض قوائم 2025 بأسعار مختلفة. '
 'اطلب عرض سعر مكتوب يوضح سنة الموديل والفئة ومصاريف التسليم قبل دفع مقدم.</p>'
 '</aside>')
 h=place_before_first_heading(h,aside)
 # Preserve all original editorial opinion and specifications, but don't leave an outdated "latest" date unqualified.
 h=h.replace("الخلاصة – تحديث 20 سبتمبر 2026","الخلاصة في مراجعة 20 سبتمبر 2026 (راجع تصحيح أكتوبر بالأعلى)")
 # Replace falsely unqualified direct answer statements in the FAQ only if the exact text is still unchanged.
 a="إذا كنت تقصد السعر خلال عام 2026، فأحدث القوائم في سبتمبر تضع المانيوال قرب 650 ألف جنيه والأوتوماتيك قرب 730 ألف جنيه. أما صفحة BYD Egypt نفسها فما زالت تعرض السيارة كموديل سنة 2025."
 b="في مراجعة 31 أكتوبر 2026، يعرض الليثي للسيارات مانيوال بسعر 660 ألف جنيه وأوتوماتيك 740 ألفًا، مع ذكر 650 و730 ألفًا كسعرين رسميين في صفحته. يعرض الموزع موديل 2026 بينما موقع BYD Egypt يذكر موديل 2025؛ لذلك يجب تأكيد سنة الموديل والسعر المكتوب قبل الشراء."
 if h.count(a)==1:h=h.replace(a,b,1)
 if h.count('id="'+MARK+'-BYD"')!=1:raise RuntimeError("BYD update duplicated")
 return {"html":h,"title":"سعر BYD F3 2026 في مصر: المانيوال والأوتوماتيك وحقيقة الموديل",
         "meta":"سعر BYD F3 2026 في مصر: المانيوال والأوتوماتيك عند الموزعين، والفرق بين عرض موديل 2026 وبيانات BYD Egypt لموديل 2025، قبل الشراء.",
         "keyword":"سعر BYD F3 2026 في مصر"}
def hub(old):
 h=old
 insert=(
 '<aside id="'+MARK+'-HUB" dir="rtl" style="border-right:4px solid #0ea5e9;'
 'background:#f8fafc;padding:14px 17px;margin:20px 0;border-radius:10px">'
 '<h3>تحديث BYD F3 في مصر: السعر وسنة الموديل</h3>'
 '<p>مراجعة 31 أكتوبر 2026: يدرج <a href="https://bydegypt.com/byd-f3/">موقع BYD Egypt</a> '
 'موديل F3 تحت سنة 2025، بينما يقدم <a href="https://ellithy.com/new-vehicles/284">'
 'الليثي</a> السيارة بوصفها موديل 2026، بأسعار عرض 660 ألف جنيه للمانيوال '
 'و740 ألفًا للأوتوماتيك (ويذكر سعرين مرجعيين 650 و730 ألفًا). '
 'لا يمكن الجزم بسنة موديل أي سيارة معروضة دون مستنداتها. '
 'راجع <a href="https://a3tal.com/byd-f3-price-egypt/">تفاصيل سعر BYD F3 والفئات والتحقق من سنة الموديل</a>.</p>'
 '</aside>')
 h=place_before_first_heading(h,insert)
 # Keep old historical market list, but correct claim that these are 2026 October live all-model prices.
 h=h.replace("أحدث الأسعار المتداولة في السوق خلال سبتمبر 2026","أسعار مرجعية منشورة خلال سبتمبر 2026")
 h=h.replace("أسعار سيارات BYD الحالية في مصر","أسعار BYD المرجعية حسب آخر مراجعة لكل موديل")
 if h.count('id="'+MARK+'-HUB"')!=1:raise RuntimeError("BYD hub update duplicated")
 return {"html":h,"title":None,
         "meta":"أسعار سيارات BYD في مصر حسب الموديل والفئة، مع تنبيه اختلاف سنة موديل F3 بين موقع BYD Egypt وعروض الموزعين، وروابط التحقق قبل الشراء.",
         "keyword":"أسعار سيارات BYD في مصر"}
fn={"byd":byd,"s07":s07,"hub":hub}
preflight=[]
for item in PAGES:
 post=wp(item)
 if (post["id"],post["slug"],post["status"],post["featured_media"])!=(item["id"],item["slug"],"publish",item["cover"]):
  raise RuntimeError("Post identity, featured media, status mismatch: "+str(item["id"]))
 original=post.get("content",{}).get("rendered","")
 if ('id="'+MARK+"-"+item["kind"].upper()+'"') in original:
  print("ALREADY_UPDATED",item["id"],post["link"],flush=True)
  continue
 if post["modified_gmt"]!=item["date"]:
  raise RuntimeError("Concurrent or prior edit, refusing: "+str(item["id"])+" "+post["modified_gmt"])
 if len(original)<2500 or original.count("<h2")<4:
  raise RuntimeError("Unexpected live original HTML content for "+str(item["id"]))
 seo=post.get("yoast_head_json") or {}
 if not seo.get("og_image") or seo.get("robots",{}).get("index")=="noindex":
  raise RuntimeError("Image or index regression in original "+str(item["id"]))
 revision=fn[item["kind"]](original)
 if not revision or len(revision["html"])<len(original) or revision["html"].count("<h2")!=original.count("<h2"):
  raise RuntimeError("Content guard failed "+str(item["id"]))
 preflight.append((item,post,revision))
 print("PREFLIGHT_OK",item["id"],len(original),len(revision["html"]),flush=True)

for item,post,revision in preflight:
 pid=item["id"]
 livebefore=wp(item)
 if livebefore["modified_gmt"]!=post["modified_gmt"]:raise RuntimeError("Edit conflict before write "+str(pid))
 payload={"id":pid,"slug":item["slug"],"content":revision["html"],
          "meta":{"_yoast_wpseo_metadesc":revision["meta"],"_yoast_wpseo_focuskw":revision["keyword"]}}
 if revision["title"]:payload["title"]=revision["title"]
 response=request(BRIDGE+"/update-post",payload,True)
 if response.get("ok") is False or response.get("error"):
  raise RuntimeError("WordPress update failed "+str(pid)+" "+str(response)[:200])
 confirmed=None
 for tries in range(5):
  got=wp(item)
  content=got["content"]["rendered"]
  if 'id="'+MARK+"-"+item["kind"].upper()+'"' in content: confirmed=got;break
  time.sleep(3)
 if not confirmed:raise RuntimeError("Post update not visible "+str(pid))
 afterseo=confirmed.get("yoast_head_json") or {}
 if (confirmed["id"],confirmed["slug"],confirmed["status"],confirmed["featured_media"])!=(pid,item["slug"],"publish",item["cover"]):
  raise RuntimeError("Post ID/url/cover invalid after write "+str(pid))
 if afterseo.get("canonical")!=(post.get("yoast_head_json") or {}).get("canonical") or not afterseo.get("og_image") or afterseo.get("robots",{}).get("index")=="noindex":
  raise RuntimeError("SEO metadata after update incorrect "+str(pid))
 print("LIVE_VERIFIED",pid,confirmed["link"],"image",confirmed["featured_media"],"modified",confirmed["modified_gmt"],flush=True)
print("A3TAL_OCTOBER_PRICE_PAGE_UPDATES_DONE",flush=True)
