#!/usr/bin/env python3
"""Link three verified new diagnostics from existing relevant hubs, without rewriting older articles."""
import os,json,urllib.request
SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY","")
LINKS=[
 (80892,"kia-sportage-electrical-screens-adas-problems",85256,
 "kia-sportage-nq5-reverse-camera-black-screen",
 '<p><strong>لأعطال الرجوع للخلف:</strong> لو شاشة سبورتاج NQ5 لا تعرض صورة الكاميرا عند اختيار R، راجع <a href="https://a3tal.com/kia-sportage-nq5-reverse-camera-black-screen/">دليل تشخيص كاميرا الرجوع السوداء والفيش وإشارة R</a> قبل تغيير الكاميرا.</p>'),
 (82230,"hyundai-elantra-hd-price-egypt",85260,
 "hyundai-elantra-hd-abs-light-after-wheel-bearing",
 '<p><strong>فحص قبل شراء إلنترا HD مستعملة:</strong> راقب لمبات الفرامل ونظام ABS، وراجع <a href="https://a3tal.com/hyundai-elantra-hd-abs-light-after-wheel-bearing/">خطوات فحص لمبة ABS بعد تغيير رمان بلي العجل</a> إذا ظهرت بعد الصيانة.</p>'),
 (84572,"suspension-knock-after-replacing-shock-absorbers-diagnosis",85264,
 "brake-clunk-first-stop-after-reversing-diagnosis",
 '<p><strong>لو الصوت يظهر عند الفرملة لا فوق المطبات:</strong> اقرأ <a href="https://a3tal.com/brake-clunk-first-stop-after-reversing-diagnosis/">تشخيص صوت الطقة عند أول فرملة بعد تغيير اتجاه السير</a> للتفرقة بين التيل والكاليبر وجلب المقص.</p>')
]
def call(path,payload=None):
 if not KEY:raise RuntimeError("Missing Direct Bridge secret")
 headers={"User-Agent":"A3tal-Context-Links-20261105","Accept":"application/json","Cache-Control":"no-store","X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY}
 data=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf8")
 if data is not None:headers["Content-Type"]="application/json; charset=utf-8"
 request=urllib.request.Request(API+path,headers=headers,method="POST" if data is not None else "GET",data=data)
 with urllib.request.urlopen(request,timeout=160) as response:return json.load(response)
def main():
 for old_id,old_slug,new_id,new_slug,note in LINKS:
  new=call("/post/"+str(new_id))
  new_url=SITE+"/"+new_slug+"/"
  if new.get("status")!="publish" or new.get("slug")!=new_slug or new.get("link")!=new_url or not new.get("featured_media"):
   raise RuntimeError("New diagnostic not fully published: "+new_slug)
  current=call("/post/"+str(old_id))
  if current.get("status")!="publish" or current.get("slug")!=old_slug or current.get("link")!=SITE+"/"+old_slug+"/":
   raise RuntimeError("Parent post mismatched: "+old_slug)
  existing=current.get("content")
  if not isinstance(existing,str) or len(existing)<1800:raise RuntimeError("Unexpected existing parent HTML: "+old_slug)
  if new_url in existing:
   print("CONTEXT_LINK_ALREADY_EXISTS",old_slug,new_slug,flush=True)
   continue
  updated=existing.rstrip()+"\n"+note
  result=call("/update-post",{"id":old_id,"content":updated,"expected_modified_gmt":current["modified_gmt"]})
  if result.get("id")!=old_id or result.get("slug")!=old_slug or new_url not in result.get("content",""):
   raise RuntimeError("Direct Bridge update verification failed: "+old_slug)
  if result.get("featured_media")!=current.get("featured_media"):
   raise RuntimeError("Existing featured image unexpectedly changed: "+old_slug)
  print("CONTEXT_LINK_VERIFIED",SITE+"/"+old_slug+"/",new_url,flush=True)
 print("A3TAL_THREE_CONTEXT_LINKS_COMPLETE",flush=True)
if __name__=="__main__":main()
