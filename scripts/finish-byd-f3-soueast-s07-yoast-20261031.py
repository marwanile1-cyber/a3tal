#!/usr/bin/env python3
"""Finish Yoast on two existing October price refreshes; no body rewrite or media updates."""
import os,json,time,urllib.request,urllib.parse
KEY=os.environ["A3TAL_API_KEY"];SITE="https://a3tal.com";BASE=SITE+"/wp-json/a3tal-direct/v1"
ROWS=[
 {"id":82348,"slug":"byd-f3-price-egypt","cover":80220,"modified":"2026-10-31T12:55:23",
  "title":"سعر BYD F3 2026 في مصر: المانيوال والأوتوماتيك وحقيقة الموديل",
  "meta":"سعر BYD F3 2026 في مصر: المانيوال والأوتوماتيك عند الموزعين، والفرق بين عرض موديل 2026 وبيانات BYD Egypt لموديل 2025، قبل الشراء."},
 {"id":80530,"slug":"soueast-s07-price-specs-egypt-2026","cover":80532,"modified":"2026-10-31T12:55:24",
  "title":"سعر ساوايست S07 في مصر: فئات 2027 بعد زيادة أكتوبر",
  "meta":"سعر ساوايست S07 موديل 2027 في مصر بعد زيادة أكتوبر: Highline بـ1,415,000 جنيه وPremium بـ1,555,000 جنيه، مع فرق المحركات والمواصفات والعيوب."}
]
def fetch(url,data=None,auth=False):
 headers={"Accept":"application/json","User-Agent":"A3tal-Price-Yoast-Final-20261031","Cache-Control":"no-cache,no-store"}
 if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
 raw=json.dumps(data,ensure_ascii=False).encode("utf8") if data is not None else None
 if raw is not None: headers["Content-Type"]="application/json; charset=utf-8"
 with urllib.request.urlopen(urllib.request.Request(url,data=raw,headers=headers,method="POST" if raw is not None else "GET"),timeout=120) as resp: return json.load(resp)
def wp(d):
 return fetch(SITE+"/wp-json/wp/v2/posts/"+str(d["id"])+"?"+urllib.parse.urlencode({"_fields":"id,title,slug,status,modified_gmt,featured_media,content,yoast_head_json,link","_q":"20261031"}))
for d in ROWS:
 p=wp(d)
 if (p["id"],p["slug"],p["status"],p["featured_media"],p["title"]["rendered"])!=(
 d["id"],d["slug"],"publish",d["cover"],d["title"]):raise RuntimeError("Existing post state drift "+str(d["id"]))
 if p["modified_gmt"]!=d["modified"]:raise RuntimeError("Concurrent update detected "+str(d["id"]))
 seo=p["yoast_head_json"]
 if not seo.get("og_image") or seo.get("robots",{}).get("index")=="noindex":raise RuntimeError("Unexpected original Yoast state")
 if seo.get("title")==d["title"] and seo.get("description")==d["meta"]:
  print("YOAST_ALREADY_CORRECT",d["id"],flush=True);continue
 previmage=seo.get("og_image")[0].get("url")
 prevcanonical=seo.get("canonical")
 r=fetch(BASE+"/update-post",{"id":d["id"],"slug":d["slug"],
     "meta":{"_yoast_wpseo_title":d["title"],
             "_yoast_wpseo_metadesc":d["meta"],
             "_yoast_wpseo_opengraph-title":d["title"]}},True)
 if r.get("error") or r.get("ok") is False:raise RuntimeError("Yoast bridge update refused "+str(r)[:220])
 live=None
 for i in range(5):
  q=wp(d)
  y=q.get("yoast_head_json") or {}
  if y.get("title")==d["title"] and y.get("description")==d["meta"]:
   live=q;break
  time.sleep(3)
 if live is None:raise RuntimeError("Yoast title or description did not refresh "+str(d["id"]))
 y=live["yoast_head_json"]
 if (live["slug"],live["status"],live["featured_media"])!=(d["slug"],"publish",d["cover"]) or y.get("canonical")!=prevcanonical or y.get("og_image",[{}])[0].get("url")!=previmage or y.get("robots",{}).get("index")=="noindex":
  raise RuntimeError("Yoast image canonical title or status integrity failed "+str(d["id"]))
 print("YOAST_LIVE_VERIFIED",d["id"],y["title"],live["link"],flush=True)
print("A3TAL_PRICE_YOAST_COMPLETE",flush=True)
