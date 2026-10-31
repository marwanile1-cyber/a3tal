#!/usr/bin/env python3
"""Refresh OG/Twitter descriptions of three already reviewed price pages; do not alter body."""
import os,json,time,urllib.request,urllib.parse
SITE="https://a3tal.com";BASE=SITE+"/wp-json/a3tal-direct/v1";KEY=os.environ["A3TAL_API_KEY"]
ROWS=[
 (82348,"byd-f3-price-egypt",80220,"2026-10-31T12:57:35","سعر BYD F3 2026 في مصر: المانيوال والأوتوماتيك عند الموزعين، والفرق بين عرض موديل 2026 وبيانات BYD Egypt لموديل 2025، قبل الشراء."),
 (80530,"soueast-s07-price-specs-egypt-2026",80532,"2026-10-31T12:57:38","سعر ساوايست S07 موديل 2027 في مصر بعد زيادة أكتوبر: Highline بـ1,415,000 جنيه وPremium بـ1,555,000 جنيه، مع فرق المحركات والمواصفات والعيوب."),
 (80219,"byd-prices-2026-misr",80220,"2026-10-31T12:55:25","أسعار سيارات BYD في مصر حسب الموديل والفئة، مع تنبيه اختلاف سنة موديل F3 بين موقع BYD Egypt وعروض الموزعين، وروابط التحقق قبل الشراء.")
]
def req(url,payload=None,auth=False):
 headers={"Accept":"application/json","Cache-Control":"no-cache,no-store","User-Agent":"A3tal-OG-Price-Social-Meta/20261031"}
 if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
 raw=json.dumps(payload,ensure_ascii=False).encode("utf8") if payload is not None else None
 if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
 with urllib.request.urlopen(urllib.request.Request(url,data=raw,headers=headers,method="POST" if raw is not None else "GET"),timeout=120) as r:return json.load(r)
def wp(id):
 return req(SITE+"/wp-json/wp/v2/posts/"+str(id)+"?"+urllib.parse.urlencode({
  "_fields":"id,slug,status,modified_gmt,featured_media,link,yoast_head_json", "_ogcheck":"20261031"}))
for id,slug,cover,expected,desc in ROWS:
 post=wp(id)
 assert (post["id"],post["slug"],post["status"],post["featured_media"])==(id,slug,"publish",cover),"Post identity changed"
 if post["modified_gmt"]!=expected:raise RuntimeError("Concurrent modification: "+str(id))
 old=post["yoast_head_json"]
 if old.get("description")!=desc:raise RuntimeError("Yoast standard description diverged "+str(id))
 existing_og=old.get("og_description")
 if existing_og==desc and old.get("twitter_misc",{})==desc:print("SOCIAL_META_ALREADY_DONE",id,flush=True);continue
 before_img=old.get("og_image",[{}])[0].get("url");before_can=old.get("canonical")
 ret=req(BASE+"/update-post",{"id":id,"slug":slug,"meta":{
  "_yoast_wpseo_opengraph-description":desc,
  "_yoast_wpseo_twitter-description":desc}},True)
 if ret.get("error") or ret.get("ok") is False:raise RuntimeError("Bridge failure "+str(id))
 done=None
 for _ in range(5):
  now=wp(id);meta=now.get("yoast_head_json") or {}
  if meta.get("og_description")==desc and meta.get("description")==desc:done=now;break
  time.sleep(3)
 if not done:raise RuntimeError("Live Yoast OG description did not refresh "+str(id))
 y=done["yoast_head_json"]
 if y.get("canonical")!=before_can or y.get("og_image",[{}])[0].get("url")!=before_img or y.get("robots",{}).get("index")=="noindex":
  raise RuntimeError("OG or index integrity regression "+str(id))
 print("PRICE_OG_LIVE_VERIFIED",id,done["link"],flush=True)
print("PRICE_SOCIAL_DESCRIPTIONS_COMPLETE",flush=True)
