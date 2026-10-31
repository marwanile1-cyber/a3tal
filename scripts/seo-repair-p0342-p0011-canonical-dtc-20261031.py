#!/usr/bin/env python3
"""Improve two canonical a3tal.com DTC articles while leaving legacy redirects untouched.
Conservative Bridge-guarded update with full post revision token checks and live SEO verification.
"""
import os,json,time,urllib.request,urllib.parse,re
SITE="https://a3tal.com"; BRIDGE=SITE+"/wp-json/a3tal-direct/v1"; KEY=os.environ["A3TAL_API_KEY"]
STAMP="A3TAL-DTC-BRAND-GENERIC-INTENT-20261031"
TARGETS=[
 {"id":80209,"code":"P0342","type":"cmp","modified":"2026-10-08T00:08:46","slug":"dtc-p0342-chevrolet",
  "cover":80210,"canonical":SITE+"/dtc-p0342-chevrolet/",
  "description":"كود P0342 حساس الكامة Circuit Low في شيفروليه ودايو: اختبر سلك الإشارة والتغذية والأرضي ونوع الحساس قبل تغييره، مع الفرق عن P0340 وP0016."},
 {"id":114,"code":"P0011","type":"vvt","modified":"2026-10-08T00:08:46","slug":"كود-p0011-سيارات-هيونداي",
  "cover":115,"canonical":SITE+"/كود-p0011-سيارات-هيونداي/",
  "description":"كود P0011 هيونداي وتوقيت الكامة المتقدم: ابدأ بالزيت وضغطه، ثم OCV وCam Phaser والكاتينة وLive Data قبل تغيير حساس الكامة أو البلف."}
]
P0342=(
'<section id="'+STAMP+'-P0342" dir="rtl" class="a3tal-diagnostic-safety">'
'<h2>هل P0342 خاص بشيفروليه ودايو فقط؟</h2>'
'<p><strong>لا.</strong> P0342 وصف قياسي لكود انخفاض إشارة دائرة حساس الكامة A، وقد يظهر في علامات ومحركات مختلفة. هذا الدليل يعرض حالة شيفروليه ودايو، لكنه لا يعني أن مواقع الحساس وأرقام أطرافه وتغذيته واحدة في كل الموديلات. في بعض التطبيقات يكون الحساس Hall بثلاثة أسلاك، وفي تطبيقات أخرى تختلف التقنية والجهود. اعتمد على مخطط السيارة ورقم المحرك قبل القياس.</p>'
'<div class="g-table-wrap"><table><thead><tr><th>النتيجة عند الفحص</th><th>الاختبار الصحيح قبل شراء الحساس</th></tr></thead><tbody>'
'<tr><td>خط الإشارة منخفض باستمرار</td><td>تحقق من قصر إلى الأرضي ومن حالة الفيشة والضفيرة، ثم راقب إشارة CMP أثناء دوران المحرك</td></tr>'
'<tr><td>التغذية أو الأرضي غير طبيعي</td><td>قارن القراءات بمخطط المصنع؛ قيمة التغذية ليست واحدة لكل السيارات</td></tr>'
'<tr><td>التغذية سليمة لكن الإشارة لا تتبدل</td><td>افحص الحساس والجزء الذي يقرأه وموضعه وفق دليل الخدمة، باستخدام الأوسيلوسكوب عند الحاجة</td></tr>'
'<tr><td>ظهر P0016 بجانب P0342</td><td>بعد سلامة الدائرة، تحقق من العلاقة بين إشارات الكامة والكرنك والتوقيت الميكانيكي</td></tr>'
'</tbody></table></div>'
'<p><strong>لا تختصر أطراف الفيشة أو توصل جهدًا خارجيًا</strong> دون اتباع مخطط المصنع؛ الاختبار الخاطئ قد يتلف وحدة التحكم. للمقارنة اقرأ <a href="https://a3tal.com/p0340-camshaft-sensor-circuit-diagnosis/">الفرق مع كود P0340</a> و<a href="https://a3tal.com/p0016-crankshaft-camshaft-correlation/">تشخيص P0016 عند اختلاف توقيت الكرنك والكامة</a>.</p>'
'<p><strong>مرجع فني:</strong> <a href="https://charm.li/Chevrolet/1999/Camaro%20V8-5.7L%20VIN%20G/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/P%20Code%20Charts/P0342/" rel="noopener noreferrer">مثال من تعليمات تشخيص شيفروليه P0342</a> لتأكيد ترتيب اختبار التغذية والأرضي والإشارة؛ المثال ليس مواصفات لجميع سيارات شيفروليه أو دايو.</p>'
'</section>')
P0011=(
'<section id="'+STAMP+'-P0011" dir="rtl" class="a3tal-diagnostic-safety">'
'<h2>هل P0011 معناه تغيير بلف VVT أم حساس الكامة؟</h2>'
'<p><strong>ليس بالضرورة.</strong> P0011 يعني أن زاوية كامة A في Bank 1 متقدمة أكثر من أمر الكمبيوتر أو أن التحكم في التوقيت لم يتبع الهدف المطلوب. هو كود أداء منظومة التوقيت وليس تشخيصًا مباشرًا لتلف حساس الكامة أو الـOCV. يظهر الكود في موديلات غير هيونداي أيضًا، بينما خطوات الفحص النهائية تعتمد على المحرك وسنة التصنيع ونظام CVVT.</p>'
'<div class="g-table-wrap"><table><thead><tr><th>ما الذي ظهر؟</th><th>ما الذي تفحصه أولًا؟</th></tr></thead><tbody>'
'<tr><td>P0011 وحده ومستوى الزيت منخفض أو مواصفته غير صحيحة</td><td>صحح المستوى والمواصفة وفق دليل المالك وافحص حالة الزيت قبل اتهام الكاتينة</td></tr>'
'<tr><td>Actual Cam Angle لا يتبع Target</td><td>اختبر أمر التحكم للـOCV وممر الزيت وCam Phaser وفق تعليمات المحرك</td></tr>'
'<tr><td>P0011 مع P0016</td><td>راجع ترابط إشارات الكرنك والكامة وتوقيت الكاتينة والشداد بعد الفحص الأولي</td></tr>'
'<tr><td>لمبة ضغط الزيت أو صوت خبط ميكانيكي</td><td>توقف بأمان وافحص ضغط الزيت ميكانيكيًا لدى مختص قبل تشغيل المحرك مجددًا</td></tr>'
'</tbody></table></div>'
'<p>لا تستخدم قيم زاوية Cam أو مقاومة بلف VVT من موديل آخر؛ حدود التشخيص تختلف بين المحركات. اقرأ <a href="https://a3tal.com/live-data-obd2/">كيفية مقارنة بيانات Live Data</a> و<a href="https://a3tal.com/p0016-crankshaft-camshaft-correlation/">متى يشير P0016 إلى خلل في التزامن</a>. وللتشخيص الكهربائي المختلف عن هذا الكود راجع <a href="https://a3tal.com/dtc-p0342-chevrolet/">P0342 وانخفاض إشارة حساس الكامة</a>.</p>'
'<p><strong>مرجع فني:</strong> <a href="https://charm.li/Toyota/2005/RAV4%204WD%20L4-2.4L%20%282AZ-FE%29/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/P%20Code%20Charts/P0011/" rel="noopener noreferrer">تسلسل فحص P0011 في دليل خدمة تويوتا</a> يوضح أهمية Freeze Frame وتوقيت الكامة ومنظومة VVT. هذا مثال تشخيصي للمقارنة، وليس مواصفة فحص هيونداي.</p>'
'</section>')
BLOCKS={"cmp":P0342,"vvt":P0011}
def request(url,payload=None):
 headers={"Accept":"application/json","Cache-Control":"no-cache,no-store","X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"User-Agent":"A3tal-DTC-SEO-Intent-Guard/20261031"}
 raw=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
 if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers,data=raw,method="POST" if raw is not None else "GET"),timeout=120) as resp:return json.load(resp)
def bridge(id):return request(BRIDGE+"/post/"+str(id))
def wp(id):
 return request(SITE+"/wp-json/wp/v2/posts/"+str(id)+"?"+urllib.parse.urlencode({"_fields":"id,slug,title,modified_gmt,status,link,featured_media,yoast_head_json,content","_audit":"intent31"}))
def insert(h,addition):
 tags=list(re.finditer(r"<h2(?:\s[^>]*)?>",h,re.I))
 if len(tags)<5:raise RuntimeError("Unexpected DTC article heading count; manual review needed")
 i=tags[0].start()
 return h[:i]+addition+"\n"+h[i:]
allrows=[]
for t in TARGETS:
 p=bridge(t["id"]); w=wp(t["id"])
 if p["id"]!=t["id"] or p["status"]!="publish" or urllib.parse.unquote(p["slug"])!=t["slug"] or p["featured_media"]!=t["cover"]:
  raise RuntimeError("Original identity / cover changed for "+str(t["id"]))
 if w["modified_gmt"]!=t["modified"]:raise RuntimeError("Concurrent original edit detected "+str(t["id"]))
 if w["yoast_head_json"].get("canonical")!=t["canonical"] or not w["yoast_head_json"].get("og_image") or w["yoast_head_json"].get("robots",{}).get("index")=="noindex":
  raise RuntimeError("DTC canonical, image or index preflight mismatch "+str(t["id"]))
 orig=p["content"]
 if STAMP in orig:
  print("DTC_ALREADY_UPDATED",t["id"],p["link"],flush=True);continue
 if len(orig)<5000 or t["code"] not in orig:raise RuntimeError("Original post missing technical content")
 new=insert(orig,BLOCKS[t["type"]])
 if new.count('id="'+STAMP+'-'+t["code"]+'"')!=1 or len(new)-len(orig)<1000:raise RuntimeError("New DTC section safety check failed")
 allrows.append((t,p,w,new))
 print("DTC_PREFLIGHT_OK",t["id"],len(orig),len(new),flush=True)
for t,p,w,new in allrows:
 latest=bridge(t["id"])
 if latest["modified_gmt"]!=p["modified_gmt"]:raise RuntimeError("Concurrent edit after preflight "+str(t["id"]))
 payload={"id":t["id"],"expected_modified_gmt":latest["modified_gmt"],
  "content":new,"meta":{"_yoast_wpseo_metadesc":t["description"],"_yoast_wpseo_opengraph-description":t["description"],"_yoast_wpseo_twitter-description":t["description"]}}
 result=request(BRIDGE+"/update-post",payload)
 if result.get("error") or result.get("ok") is False:raise RuntimeError("Bridge update failed "+str(t["id"])+str(result)[:150])
 done=None
 for k in range(6):
  a=bridge(t["id"]);b=wp(t["id"])
  seo=b.get("yoast_head_json",{})
  if STAMP in a["content"] and seo.get("description")==t["description"] and seo.get("og_description")==t["description"]:
   done=(a,b);break
  time.sleep(3)
 if not done:raise RuntimeError("Live DTC patch or Yoast descriptions did not appear "+str(t["id"]))
 a,b=done
 if urllib.parse.unquote(a["slug"])!=t["slug"] or a["status"]!="publish" or a["featured_media"]!=t["cover"] or b["yoast_head_json"].get("canonical")!=t["canonical"] or not b["yoast_head_json"].get("og_image") or b["yoast_head_json"].get("robots",{}).get("index")=="noindex":
  raise RuntimeError("DTC post / SEO identity changed after publish "+str(t["id"]))
 print("DTC_LIVE_VERIFIED",t["id"],a["link"],"featured",a["featured_media"],flush=True)
print("P0011_P0342_CANONICAL_ARTICLES_COMPLETE",flush=True)
