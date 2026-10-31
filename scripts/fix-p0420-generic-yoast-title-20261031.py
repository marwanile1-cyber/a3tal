#!/usr/bin/env python3
"""Replace misleading generic P0420 Yoast headline with descriptive search title."""
import json,os,time,urllib.request,urllib.parse
SITE="https://a3tal.com";API=SITE+"/wp-json/a3tal-direct/v1";KEY=os.environ["A3TAL_API_KEY"]
PID=81336;SLUG="p0420-catalyst-efficiency-bank-1";FEATURED=81337
OLD="كود P0420 | أعطال.كوم | التفاصيل والخدمات"
NEW="كود P0420: هل علبة البيئة تالفة؟ الأسباب والفحص | أعطال"
LAST="2026-10-31T14:11:16"
def request(url,payload=None):
 headers={"Accept":"application/json","Cache-Control":"no-cache,no-store",
          "User-Agent":"A3tal-DTC-P0420-CTR-Guard/20261031",
          "X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY}
 raw=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
 if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
 with urllib.request.urlopen(urllib.request.Request(url,data=raw,method="POST" if raw is not None else "GET",headers=headers),timeout=120) as res:return json.load(res)
def pub():
 return request(SITE+"/wp-json/wp/v2/posts/"+str(PID)+"?"+urllib.parse.urlencode({"_fields":"id,status,slug,modified_gmt,featured_media,link,title,yoast_head_json","_q":"t31"}))
p=pub();s=p.get("yoast_head_json") or {}
if (p["id"],p["status"],p["slug"],p["featured_media"])!=(PID,"publish",SLUG,FEATURED):
 raise RuntimeError("Original P0420 identity drift")
if s.get("title")==NEW and s.get("og_title")==NEW:
 print("P0420_SEO_ALREADY_FIXED",p["link"],flush=True)
 raise SystemExit(0)
if p["modified_gmt"]!=LAST or s.get("title")!=OLD:raise RuntimeError("Concurrent editorial change to P0420; abort")
if s.get("robots",{}).get("index")=="noindex" or not s.get("og_image"):raise RuntimeError("Original SEO integrity bad")
seo_before={"canonical":s["canonical"],"og_image":s["og_image"][0]["url"],
            "description":s.get("description"),"og_description":s.get("og_description")}
bridge_before=request(API+"/post/"+str(PID))
if (bridge_before["id"],bridge_before["slug"],bridge_before["status"],bridge_before["featured_media"])!=(PID,SLUG,"publish",FEATURED):
 raise RuntimeError("Bridge post identity changed since public audit")
bridge_token=bridge_before.get("modified_gmt","")
if not bridge_token.startswith(LAST):
 raise RuntimeError("Bridge revision differs from audited WP version; refusing update")
r=request(API+"/update-post",{"id":PID,"slug":SLUG,"expected_modified_gmt":bridge_token,
 "meta":{"_yoast_wpseo_title":NEW,"_yoast_wpseo_opengraph-title":NEW,
         "_yoast_wpseo_twitter-title":NEW}})
if r.get("ok") is False or r.get("error"):raise RuntimeError("Bridge title update refused "+str(r)[:200])
for tries in range(5):
 a=pub();y=a.get("yoast_head_json") or {}
 if y.get("title")==NEW and y.get("og_title")==NEW:break
 time.sleep(3)
else:raise RuntimeError("Updated P0420 Yoast title not visible")
if a["slug"]!=SLUG or a["status"]!="publish" or a["featured_media"]!=FEATURED or y.get("canonical")!=seo_before["canonical"] or y.get("og_image",[{}])[0].get("url")!=seo_before["og_image"] or y.get("description")!=seo_before["description"] or y.get("og_description")!=seo_before["og_description"] or y.get("robots",{}).get("index")=="noindex":
 raise RuntimeError("P0420 title fix regressed source metadata")
print("P0420_DESCRIPTIVE_YOAST_LIVE_VERIFIED",NEW,a["link"],flush=True)
