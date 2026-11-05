#!/usr/bin/env python3
"""Stage 1 fix: replace misleading home search links with working utility forms,
and make newly linked car records open their real canonical price articles.

A3tal Direct Bridge only. Never overwrite unexpected live theme changes.
Only three reviewed theme files + one utility WordPress page are in scope.
"""
import hashlib,json,os,re,time,urllib.parse,urllib.request,urllib.error
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types

module=types.ModuleType("a3tal_scoped_stage1_bridge")
SourceFileLoader(module.__name__,"scripts/deploy-dtc-library.py").exec_module(module)
Bridge=module.Bridge
ROOT=Path("theme-source/a3tal-global")
BASE="https://a3tal.com"
PAGE_SLUG="car-tools"
PAGE_PATH="/car-tools/"
HOMEPATH="home-reference-20261104.php"
CARPATH="car-price-guide.php"
TOOLS="page-car-tools.php"
STEPS=[]
def sha(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def public_text(path):
 req=urllib.request.Request(BASE+path,headers={"Cache-Control":"no-cache,no-store","User-Agent":"A3tal-Stage1-Live-QA/20261105"})
 with urllib.request.urlopen(req,timeout=85) as r:
  if r.status!=200:raise RuntimeError("Live HTTP not 200: "+path)
  return r.read(2000000).decode("utf8","replace")
def public_json(path):
 return json.loads(public_text(path))
def page():
 arr=public_json("/wp-json/wp/v2/pages?"+urllib.parse.urlencode({"slug":PAGE_SLUG,"_fields":"id,slug,status,title,link","per_page":10}))
 if len(arr)>1:raise RuntimeError("Multiple pages with car-tools slug")
 return arr[0] if arr else None
def ensure_tools_template(api):
 src=(ROOT/TOOLS).read_text("utf8")
 assert "a3rt-fuel-form" in src and "a3rt-maint-form" in src and "get_footer();" in src
 live=api.read(TOOLS,missing=True)
 if live:
  if live["sha256"]!=sha(src):raise RuntimeError("Existing car-tools template differs: refusing overwrite")
  print("WORKING_TOOLS_TEMPLATE_ALREADY_DEPLOYED",flush=True);return
 api.write(TOOLS,src)
 print("WORKING_TOOLS_TEMPLATE_LIVE_VERIFIED",flush=True)
def ensure_page(api):
 existing=page()
 if existing:
  if existing.get("status")!="publish" or existing.get("link")!=BASE+PAGE_PATH:
   raise RuntimeError("Existing car-tools page in unexpected state")
  print("WORKING_TOOLS_PAGE_ALREADY_PUBLISHED",existing["id"],flush=True);return
 data={"type":"page","status":"publish","slug":PAGE_SLUG,"title":"حاسبة استهلاك البنزين وتكلفة صيانة السيارة",
       "content":"<p>أدوات حساب بدون تخزين بيانات. استخدم الحاسبتين التفاعليتين لقياس استهلاك الوقود وتقدير فاتورة الورشة.</p>",
       "excerpt":"احسب استهلاك البنزين من كمية الوقود والمسافة وتكلفة الصيانة من البنود المدخلة، بدون أرقام أسعار مفترضة.",
       "meta":{
        "_yoast_wpseo_title":"حاسبة استهلاك البنزين وتكلفة صيانة السيارة | أعطال.كوم",
        "_yoast_wpseo_metadesc":"حاسبة فعلية لاستهلاك السيارة باللتر لكل 100 كم وتقدير تكلفة الصيانة من قطع وزيوت ومصنعية وضريبة مدخلة يدويًا.",
        "_yoast_wpseo_meta-robots-noindex":"1"
       }}
 raw=json.dumps(data,ensure_ascii=False).encode("utf8")
 headers={"Accept":"application/json","Cache-Control":"no-store","User-Agent":"A3tal-Stage1-20261105","X-A3tal-Key":api.key,"Authorization":"Bearer "+api.key,"Content-Type":"application/json"}
 request=urllib.request.Request(BASE+"/wp-json/a3tal-direct/v1/create-post",data=raw,headers=headers,method="POST")
 try:
  with urllib.request.urlopen(request,timeout=90) as resp:result=json.load(resp)
 except (TimeoutError,urllib.error.URLError):
  result={}
 published=page()
 if not published or published.get("status")!="publish" or published.get("link")!=BASE+PAGE_PATH:
  raise RuntimeError("Cannot confirm a published car-tools page after write")
 print("WORKING_TOOLS_PAGE_PUBLISHED_VERIFIED",published["id"],flush=True)
def homepage_patch(live):
 pairs=[
  ("if(!$home_car_img)$home_car_img=content_url('/uploads/2026/11/a3tal-ref-20261104-service-specs.webp');",
   "if(!$home_car_img)$home_car_img=content_url('/uploads/2026/11/a3tal-ref-20261104-service-specs.webp');\n$home_main_post_id=(int)get_post_meta(get_the_ID(),'_a3_primary_price_post_id',true);\n$home_main_post_url=($home_main_post_id && get_post_type($home_main_post_id)==='post' && get_post_status($home_main_post_id)==='publish') ? get_permalink($home_main_post_id) : get_permalink();"),
  ('<a class="carcard" href="<?php the_permalink(); ?>">','<a class="carcard" href="<?php echo esc_url($home_main_post_url); ?>">'),
  ('<a href="https://a3tal.com/?s=صيانة"><span>▦</span>معلومات تكلفة الصيانة</a>','<a href="https://a3tal.com/car-tools/#maintenance-cost"><span>▦</span>احسب تكلفة الصيانة</a>'),
  ('<a href="https://a3tal.com/?s=استهلاك+الوقود"><span>⛽</span>معلومات استهلاك الوقود</a>','<a href="https://a3tal.com/car-tools/#fuel-use"><span>⛽</span>احسب استهلاك البنزين</a>'),
  ('<a href="https://a3tal.com/?s=مقاسات+الإطارات"><span>◉</span>مقاسات الإطارات</a>','<a href="https://a3tal.com/car-tires-prices-egypt-2026/"><span>◉</span>دليل مقاسات الكاوتش</a>')
 ]
 for old,new in pairs:
  if new in live:continue
  if live.count(old)!=1:raise RuntimeError("Unexpected homepage patch anchor: "+old[:70])
  live=live.replace(old,new,1)
 if live.count("a3tal-reference-page")<1 or "home_main_post_url" not in live:
  raise RuntimeError("Homepage exact-reference or car anchor missing")
 return live
def cars_patch(live):
 old="  $href = get_permalink($id);"
 new="  // Fresh catalogue records can safely point at their one verified, indexable price article.\n  // Leave established car records' current permalink and SEO policy unchanged.\n  $primary_price_post=(int)get_post_meta($id,'_a3_primary_price_post_id',true);\n  $href=($primary_price_post && get_post_type($primary_price_post)==='post'\n    && get_post_status($primary_price_post)==='publish') ? get_permalink($primary_price_post) : get_permalink($id);"
 if new in live:return live
 if live.count(old)!=1:raise RuntimeError("Unexpected car price guide card anchor; no overwrite")
 return live.replace(old,new,1)
def patch_one(api,name,patch):
 current=api.read(name)
 if not current:raise RuntimeError("Live theme file missing: "+name)
 desired=patch(current["content"])
 if desired==current["content"]:
  print("ALREADY_PATCHED",name,flush=True);return
 # The reviewed repository source and live target must contain the same unique patch.
 local=(ROOT/name).read_text("utf8")
 if not all(word in local for word in (("home_main_post_url","car-tools/#fuel-use") if name==HOMEPATH else ("_a3_primary_price_post_id","get_permalink($primary_price_post)"))):
  raise RuntimeError("Repository source lacks approved patch for "+name)
 api.write(name,desired,current["sha256"])
 print("SCOPED_THEME_PATCH_DEPLOYED",name,flush=True)
def verify():
 html=public_text("/?a3tal_stage1_qa="+str(int(time.time())))
 checks=["a3tal-reference-page","car-tools/#maintenance-cost","car-tools/#fuel-use","car-tires-prices-egypt-2026/"]
 for key in checks:
  if key not in html:raise RuntimeError("Live homepage missing functional tool: "+key)
 for old in ["?s=استهلاك+الوقود","?s=مقاسات+الإطارات"]:
  if old in html:raise RuntimeError("Old placeholder search tool still exposed "+old)
 tool=public_text("/car-tools/?a3tal_stage1_qa="+str(int(time.time())))
 for key in ['id="a3rt-fuel-form"','id="a3rt-maint-form"','id="fuel-use"','id="maintenance-cost"','litres/distance*100']:
  if key not in tool:raise RuntimeError("Missing working calculator source: "+key)
 cars=public_text("/cars/?a3tal_stage1_qa="+str(int(time.time())))
 for slug in ["kgm-torres-2027-egypt-price-trims-8speed/","renault-boreal-2027-egypt-price-trims/","jetour-t2-idm-4x4-2027-egypt-price-specs/"]:
  if slug not in cars:raise RuntimeError("Cars archive missing canonical article link: "+slug)
 print("LIVE_STAGE1_HOME_CALCULATORS_CAR_PRICE_LINKS_VERIFIED",flush=True)
def main():
 if not os.getenv("A3TAL_API_KEY"):raise RuntimeError("Missing Direct Bridge secret")
 api=Bridge()
 ensure_tools_template(api)
 ensure_page(api)
 patch_one(api,CARPATH,cars_patch)
 patch_one(api,HOMEPATH,homepage_patch)
 api.flush()
 verify()
 print("STAGE_ONE_HOME_TOOLS_AND_MODEL_LINKS_COMPLETE",flush=True)
if __name__=="__main__":main()
