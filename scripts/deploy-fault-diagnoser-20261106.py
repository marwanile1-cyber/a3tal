#!/usr/bin/env python3
"""Deploy a safe, original A3tal fault triage page and related static assets via Direct Bridge.
Preserve current home template. Do not link into navigation until independent browser QA passes.
"""
import hashlib,json,os,urllib.request,urllib.parse,urllib.error,sys
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types
m=types.ModuleType("a3tal_guarded_bridge")
SourceFileLoader(m.__name__,"scripts/deploy-dtc-library.py").exec_module(m)
Bridge=m.Bridge
SITE="https://a3tal.com"
SLUG="fault-diagnosis"
FILES=[
 "fault-diagnoser-20261106.css",
 "assets/js/fault-diagnoser-20261106.js",
 "page-fault-diagnosis.php",
]
ROOT=Path("theme-source/a3tal-global")
def sha(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def public(url):
 req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"A3tal-Interactive-Fault-20261106","Cache-Control":"no-cache,no-store"})
 with urllib.request.urlopen(req,timeout=80) as f:return json.load(f)
def existing():
 rows=public(SITE+"/wp-json/wp/v2/pages?"+urllib.parse.urlencode({"slug":SLUG,"per_page":10,"_fields":"id,slug,status,link,title,template"}))
 if len(rows)>1:raise RuntimeError("Ambiguous page slug")
 return rows[0] if rows else None
def source_check():
 texts={name:(ROOT/name).read_text(encoding="utf8") for name in FILES}
 if texts[FILES[1]].count("item(\"")<18:raise RuntimeError("Too few audited symptom scenarios")
 needed=["a3fd-app","a3fd-inline-script","a3fd-inline-style","get_header();","get_footer();"]
 if any(x not in texts[FILES[2]] for x in needed):raise RuntimeError("Template incomplete")
 if not all(x in texts[FILES[1]] for x in ("stopReason","emergency","fault","root.dataset.ready")):
  # No network AI inference; all safety checks remain deterministic.
  if not all(x in texts[FILES[1]] for x in ("stopReason","emergency","root.dataset.ready","cases=[")):
   raise RuntimeError("The deterministic safety rule engine is incomplete")
 return texts
def main():
 if not os.environ.get("A3TAL_API_KEY"):raise RuntimeError("Missing Direct Bridge secret")
 data=source_check()
 api=Bridge()
 # Upfront name and hash compatibility checks protect all other live theme files.
 for name in FILES:
  old=api.read(name,missing=True)
  if old and old.get("sha256")!=sha(data[name]):
   raise RuntimeError("Unknown existing fault-diagnosis file: "+name)
  print("FAULT_SOURCE_PREFLIGHT",name,"new" if not old else "verified",flush=True)
 page=existing()
 if page and (page.get("status")!="publish" or page.get("link")!=SITE+"/"+SLUG+"/"):
  raise RuntimeError("Existing fault-diagnosis WordPress page in unexpected state")
 # Write low-risk assets before template.
 for name in FILES:
  old=api.read(name,missing=True)
  if not old:
   api.write(name,data[name])
   print("FAULT_THEME_FILE_PUBLISHED",name,flush=True)
  else:
   print("FAULT_THEME_FILE_ALREADY_VERIFIED",name,flush=True)
 api.flush()
 if not page:
  post={
   "type":"page","status":"publish","slug":SLUG,
   "title":"مشخّص الأعطال الذكي للسيارات والموتوسيكلات",
   "excerpt":"اختر نوع المركبة والعَرَض، وجاوب على أسئلة بسيطة لمعرفة مستوى الخطورة وترتيب فحوصات الأعطال والروابط الفنية، دون تخمين الأسعار.",
   "content":"<p>اختَر العَرَض واحصل على خطوات فرز وفحص استرشادية بمصادر ومراجع. لا يحل محل فحص فني أو تصريح بالقيادة.</p>",
   "meta":{
    "_yoast_wpseo_title":"مشخّص الأعطال الذكي للسيارات والموتوسيكلات | أعطال.كوم",
    "_yoast_wpseo_metadesc":"مشخّص تفاعلي لأعطال السيارات والموتوسيكلات: لمبات وأصوات وروائح وتسريب واهتزازات. أسئلة متابعة وتحذيرات سلامة وروابط تشخيص، بدون تخمين أسعار.",
    "_yoast_wpseo_focuskw":"مشخّص أعطال السيارات",
    "_yoast_wpseo_canonical":SITE+"/"+SLUG+"/"
   }
  }
  raw=json.dumps(post,ensure_ascii=False).encode("utf8")
  headers={"Accept":"application/json","Content-Type":"application/json; charset=utf-8","User-Agent":"A3tal-Guarded-Fault-20261106","X-A3tal-Key":api.key,"Authorization":"Bearer "+api.key}
  req=urllib.request.Request(SITE+"/wp-json/a3tal-direct/v1/create-post",headers=headers,data=raw,method="POST")
  try:
   with urllib.request.urlopen(req,timeout=150) as f:
    result=json.load(f)
   print("FAULT_PAGE_BRIDGE_RESULT",str(result)[:300],flush=True)
  except (TimeoutError,urllib.error.URLError) as error:
   print("FAULT_PAGE_AMBIGUOUS_WRITE_READBACK_ONLY",type(error).__name__,flush=True)
 page=existing()
 if not page or page.get("status")!="publish" or page.get("link")!=SITE+"/"+SLUG+"/":
  raise RuntimeError("New page not verified through public WordPress API")
 print("FAULT_PAGE_WORDPRESS_PUBLISHED",page["id"],page["link"],flush=True)
 url=SITE+"/"+SLUG+"/?fd_qa=20261106"
 req=urllib.request.Request(url,headers={"User-Agent":"A3tal-Fault-Readback-20261106","Cache-Control":"no-store"})
 with urllib.request.urlopen(req,timeout=80) as f:
  html=f.read(2_000_000).decode("utf8","replace")
 for key in ("id=\"a3fd-app\"","id=\"a3fd-inline-script\"","id=\"a3fd-inline-style\"","مشخّص الأعطال الذكي"):
  if key not in html:raise RuntimeError("Published page missing functional body or media: "+key)
 print("FAULT_PAGE_HTML_AND_ASSETS_VERIFIED",len(html),flush=True)
if __name__=="__main__":main()
