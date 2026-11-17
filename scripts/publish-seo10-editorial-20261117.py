#!/usr/bin/env python3
"""Ten guarded existing-post editorial improvements for A3tal Egypt.
Read latest Bridge source before writing. Keep slug, status, categories,
featured image, og:image and Yoast canonical stable. Never claim expert
review actually occurred unless external approval is recorded.
"""
import json, os, re, html, time, urllib.request, urllib.parse
from pathlib import Path

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
if not KEY:raise RuntimeError("Missing A3TAL_API_KEY secret")
data=json.loads((Path(__file__).resolve().parents[1]/"data/a3tal-seo10-editorial-20261117.json").read_text(encoding="utf-8"))
cases=data["cases"]
if len(cases)!=10 or len(set(c["id"] for c in cases))!=10:raise RuntimeError("Expected 10 unique targets")
MARK="a3tal-seo10-diagnostic-20261117"
def request(url,body=None,auth=True):
 headers={"User-Agent":"curl/8.5.0","Accept":"application/json","Cache-Control":"no-cache"}
 if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
 raw=None if body is None else json.dumps(body,ensure_ascii=False).encode("utf-8")
 if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
 req=urllib.request.Request(url,data=raw,headers=headers,method="POST" if raw else "GET")
 with urllib.request.urlopen(req,timeout=175) as rsp:return json.load(rsp)
def bridge(pid):return request(API+"/post/"+str(pid))
def public(pid):return request(SITE+"/wp-json/wp/v2/posts/"+str(pid)+"?_fields=id,slug,status,link,featured_media,yoast_head_json",auth=False)
def norm(s):return urllib.parse.unquote(s).rstrip("/").lower()
def seo_ok(before,wp,c):
 if not wp or wp.get("id")!=c["id"]:raise RuntimeError("Incorrect public post ID")
 if norm(before.get("slug",""))!=norm(c["slug"]) or norm(wp.get("slug",""))!=norm(c["slug"]):
  raise RuntimeError("Slug mismatch "+str(c["id"]))
 if before.get("status")!="publish" or wp.get("status")!="publish":raise RuntimeError("Target is not published")
 if not before.get("featured_media") or before.get("featured_media")!=wp.get("featured_media"):
  raise RuntimeError("No confirmed original featured image "+str(c["id"]))
 seo=wp.get("yoast_head_json") or {}
 if seo.get("canonical") and norm(seo["canonical"])!=norm(wp["link"]):raise RuntimeError("Canonical mismatch")
 if not seo.get("og_image"):raise RuntimeError("OG image absent")
 if (seo.get("robots") or {}).get("index")=="noindex":raise RuntimeError("Unexpected noindex")
 if len(before.get("content") or "")<6500:raise RuntimeError("Unexpected short original")
 return seo
def esc(s):return html.escape(str(s),quote=True)
def table_rows(rows):
 return "".join("<tr style='background:"+("#ffffff" if i%2==0 else "#eef5f9")+"'>"
                "<th scope='row' style='padding:12px;text-align:right;color:#123950;border:1px solid #d1dce2;min-width:145px'>"+esc(r[0])+"</th>"
                "<td style='padding:12px;border:1px solid #d1dce2;min-width:160px'>"+esc(r[1])+"</td>"
                "<td style='padding:12px;border:1px solid #d1dce2;min-width:170px'>"+esc(r[2])+"</td></tr>"
                for i,r in enumerate(rows))
def top(c):
 return "\n<section id='"+MARK+"-"+str(c["id"])+"' dir='rtl' class='a3tal-seo10-answer-first' style='border-right:5px solid #006784;border-radius:9px;background:#f5fafc;padding:18px 20px;margin:0 0 22px;color:#153345;line-height:1.85'>"+\
 "<h2 style='margin:0 0 10px;font-size:1.22em;color:#063a58'>"+esc(c["headline"])+"</h2>"+\
 "<p style='margin:0'><strong>الإجابة المباشرة:</strong> "+esc(c["answer"])+"</p></section>\n"
def section(c):
 return "\n<section dir='rtl' class='a3tal-seo10-expert-decision' style='margin:22px 0;line-height:1.9;color:#202e35'>"+\
 "<h2 style='color:#0e4965;font-size:1.3em;margin:20px 0 10px'>مصفوفة التشخيص: العلامة وأول فحص قبل تغيير القطع</h2>"+\
 "<div style='width:100%;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch'><table style='border-collapse:collapse;min-width:560px;width:100%;font-size:0.94em'><thead><tr style='background:#123d57;color:#fff'><th scope='col' style='padding:12px;text-align:right'>العلامة</th><th scope='col' style='padding:12px;text-align:right'>الاحتمال الأقرب للفحص</th><th scope='col' style='padding:12px;text-align:right'>الخطوة الصحيحة</th></tr></thead><tbody>"+table_rows(c["table"])+"</tbody></table></div>"+\
 "<h2 style='color:#0e4965;font-size:1.3em;margin:23px 0 12px'>ملاحظات فنية تفرق في قرار الإصلاح</h2>"+c["section"]+\
 "<p style='background:#fff6ea;border:1px solid #e9c28f;border-radius:7px;padding:12px 14px'><strong>تنبيه أمان:</strong> "+esc(c["warning"])+"</p>"+\
 "<p style='font-size:.94em'><strong>مصدر فني للتحقق:</strong> <a href='"+esc(c["source"])+"' target='_blank' rel='noopener noreferrer'>"+esc(c["sourceName"])+"</a>. ويمكن متابعة الموضوع المرتبط في <a href='"+esc(c["internal"])+"'>دليل أعطال.كوم المتخصص</a>.</p></section>\n"
def bio(c):
 return "\n<section dir='rtl' class='a3tal-seo10-author' style='border:1px solid #d4dfe6;border-radius:9px;padding:17px 19px;margin:25px 0;background:#fff;color:#1e3542'><h2 style='font-size:1.12em;margin:0 0 9px'>معلومات إعداد المقال والفريق الفني</h2><p style='margin:0 0 8px'><strong>المحتوى:</strong> فريق تحرير أعطال.كوم. تم تحرير هذا التحديث بناءً على المراجع الفنية المعلنة داخل المقال.</p><p style='margin:0'><strong>الخبير المتخصص ضمن فريق الموقع:</strong> المهندس "+esc(c["expert"])+"، "+esc(c["role"])+"، بخبرة "+esc(c["years"])+".</p></section>\n"
def clean_legacy(pid,old):
 s=old
 if pid==79952:
  start=s.find("<!-- Google News Article Schema -->")
  target=s.find('<div style="background:#eef6ff')
  if not (start==0 and 800<target<4700 and 'body { font-family' in s[:target] and 'tr:nth-child(even)' in s[:target]):raise RuntimeError("Unsafe ABS legacy CSS removal")
  s=s[target:]
 if pid==80153:
  start=s.find("body { font-family: 'Segoe UI'")
  target=s.find('<nav aria-label="breadcrumb">',start)
  if not (0<start<2100 and 1100<target-start<4000 and '.speakable-summary' in s[start:target]):
   raise RuntimeError("Unsafe auto transmission visible CSS removal")
  s=s[:start]+s[target:]
 if pid==79890:
  start=s.find('<h2 style="color: red">تجربتنا في "أعطال.كوم" مع صوت خبط المحرك</h2>')
  end=s.find('<h3 style="color: blue">توصيات الخبراء الذهبية:</h3>',start)
  if not (start>0 and 200<end-start<2200):raise RuntimeError("Invented experience case structure changed; stop")
  repl=("<h2 style='color:#0e4965'>مثال توضيحي: لماذا إخفاء لمبة الزيت ليس إصلاحًا؟</h2>"
        "<p>لو لمبة ضغط الزيت بتومض عند الوقوف وظهر صوت خبط، فالخطوة الصحيحة إيقاف التشغيل وفحص الضغط الحقيقي ومسار التزييت. استخدام زيت أعلى لزوجة أو إضافة من غير تشخيص قد يغيّر ظهور العرض، لكنه لا يثبت معالجة الطرمبة أو الخلوصات أو انسداد المسار. تحديد سبب انخفاض الضغط يتطلب قياسات ورشة، ثم مقايسة مرتبطة بنتيجة الفحص.</p>")
  s=s[:start]+repl+s[end:].replace("توصيات الخبراء الذهبية:","نصائح للحفاظ على التزييت:",1)
 if pid==80521:
  s=s.replace('تصل لـ 200,000 لفة في الدقيقة','قد تصل سرعته إلى قيم مرتفعة تختلف حسب تصميم المحرك والتيربو')
  s=s.replace('هواء أكثر + بنزين أكثر = انفجار أقوى وعزم دوران (Torque) مضاعف.','ضغط هواء أكبر يسمح للمحرك بإنتاج قدرة وعزم أعلى عند توافر الوقود والتحكم المناسبين، من غير نسبة زيادة ثابتة لكل محرك.')
 if pid in (81039,80508,80611):
  s=s.replace("آخر مراجعة:  20 سبتمبر 2026.","تاريخ مراجعة النسخة الأصلية: 20 سبتمبر 2026. تحديث تحريري ومرجعي: 17 نوفمبر 2026.")
  s=s.replace("آخر مراجعة: 20 سبتمبر 2026.","تاريخ مراجعة النسخة الأصلية: 20 سبتمبر 2026. تحديث تحريري ومرجعي: 17 نوفمبر 2026.")
 if pid==81009:
  s=s.replace("آخر مراجعة فنية: 19 سبتمبر 2026.","تاريخ المراجعة الأصلية: 19 سبتمبر 2026. تحديث تحريري وإضافة مصادر فنية: 17 نوفمبر 2026.")
 if pid==80992:
  s=s.replace("حماية محرك سيارتك من الانصهار والتلف التام","حماية المحرك من السخونة والأضرار الميكانيكية")
 return s
def build(c,original):
 pid=c["id"]
 if MARK+"-"+str(pid) in original:return None
 cleaned=clean_legacy(pid,original)
 if len(cleaned)<len(original)-3100:raise RuntimeError("Too much original text removed")
 content=top(c)+cleaned
 block=section(c)+bio(c)
 end=content.lower().rfind("</article>")
 if end>=0:content=content[:end]+block+content[end:]
 else:content=content+block
 if content.count('id="'+MARK)==0 and content.count("id='"+MARK)!=1:raise RuntimeError("Answer block missing")
 if content.count("a3tal-seo10-author")!=1 or content.count("a3tal-seo10-expert-decision")!=1:raise RuntimeError("Sections malformed")
 if content.count("<img")!=original.count("<img"):raise RuntimeError("Inline media count changed")
 oldlinks=re.findall(r'href="([^"]+)"',original,re.I)
 newlinks=re.findall(r'href="([^"]+)"',content,re.I)
 if any(u not in newlinks for u in oldlinks):raise RuntimeError("Original hyperlink disappeared")
 if len(content)<len(original)+1200:raise RuntimeError("Editor additions unexpectedly small")
 return content
def verify_same_before_after(before,after,seo_before,wp_after):
 for attr in ("id","slug","status","featured_media","title","type","categories","tags"):
  if attr in before and before.get(attr)!=after.get(attr):raise RuntimeError("Original identity changed "+attr)
 if wp_after["featured_media"]!=before["featured_media"]:raise RuntimeError("Public cover changed")
 seo_after=wp_after.get("yoast_head_json") or {}
 if seo_after.get("canonical")!=seo_before.get("canonical"):raise RuntimeError("Canonical changed")
 old_og=(seo_before.get("og_image") or [{}])[0].get("url")
 new_og=(seo_after.get("og_image") or [{}])[0].get("url")
 if old_og!=new_og:raise RuntimeError("OG image changed")
 if (seo_after.get("robots") or {}).get("index")=="noindex":raise RuntimeError("Unexpected noindex")
def main():
 plans=[]
 for c in cases:
  before=bridge(c["id"]);wp=public(c["id"])
  seo=seo_ok(before,wp,c)
  changed=build(c,before["content"])
  if changed is None:
   print("ALREADY_PROCESSED",c["id"],wp["link"],flush=True)
   continue
  plans.append((c,before,seo,changed))
  print("SEO10_PREFLIGHT_OK",c["id"],len(before["content"]),len(changed),flush=True)
 print("SEO10_PREFLIGHTS_COMPLETE",len(plans),flush=True)
 for c,before,seo,content in plans:
  pid=c["id"];recent=bridge(pid)
  if recent["modified_gmt"]!=before["modified_gmt"] or recent["content"]!=before["content"]:
   raise RuntimeError("Concurrent WordPress revision. No overwrite: "+str(pid))
  payload={"id":pid,"expected_modified_gmt":before["modified_gmt"],"content":content,"meta":{"_yoast_wpseo_metadesc":c["meta"]}}
  result=request(API+"/update-post",payload)
  if result.get("error") or result.get("ok") is False:raise RuntimeError("Bridge declined "+str(pid))
  after=bridge(pid);wp_after=public(pid)
  verify_same_before_after(before,after,seo,wp_after)
  if MARK+"-"+str(pid) not in after.get("content",""):raise RuntimeError("Live content missing marker "+str(pid))
  if (wp_after.get("yoast_head_json") or {}).get("description")!=c["meta"]:
   raise RuntimeError("Meta description not persisted "+str(pid))
  print("SEO10_POST_PUBLISHED_VERIFIED",pid,wp_after["link"],flush=True)
 print("SEO10_ALL_UPDATES_COMPLETED",len(plans),flush=True)
if __name__=="__main__":main()
