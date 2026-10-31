#!/usr/bin/env python3
"""Fix Jetour HTML table validity and mobile scrolling using existing theme .g-table-wrap CSS."""
import os,json,urllib.request,urllib.parse,time
SITE="https://a3tal.com";API=SITE+"/wp-json/a3tal-direct/v1";KEY=os.environ["A3TAL_API_KEY"]
ID=80401;SLUG="%d9%85%d8%b1%d8%a7%d9%83%d8%b2-%d8%ae%d8%af%d9%85%d8%a9-%d8%ac%d9%8a%d8%aa%d9%88%d8%b1-%d8%a7%d9%84%d9%85%d8%b9%d8%aa%d9%85%d8%af%d8%a9-%d9%81%d9%8a-%d9%85%d8%b5%d8%b1"
EXPECTED_DATE="2026-10-31T12:41:07";COVER=82886
MARKER="A3TAL-JETOUR-AHMED-MAREY-SERVICE-20261031-V1"
def request(url,body=None,auth=False):
    headers={"Accept":"application/json","User-Agent":"A3tal-Jetour-Table-HTML-Fix/20261031","Cache-Control":"no-cache,no-store"}
    if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    raw=json.dumps(body,ensure_ascii=False).encode("utf8") if body is not None else None
    if raw is not None:headers["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers,data=raw,method="POST" if raw is not None else "GET"),timeout=120) as response:return json.load(response)
def wp():
    return request(SITE+"/wp-json/wp/v2/posts/"+str(ID)+"?"+urllib.parse.urlencode({
        "_fields":"id,slug,modified_gmt,status,link,featured_media,content,yoast_head_json",
        "jetour_fix":"oct31"}))
old=wp()
if (old["id"],old["slug"],old["status"],old["featured_media"])!=(ID,SLUG,"publish",COVER):
    raise RuntimeError("Post identity, status or image mismatch")
h=old["content"]["rendered"]
if 'class="g-table-wrap"' in h and '<tr class="'+MARKER+'"' in h:
    print("JETOUR_MOBILE_TABLE_FIX_ALREADY_APPLIED",old["link"],flush=True);raise SystemExit(0)
if old["modified_gmt"]!=EXPECTED_DATE:raise RuntimeError("Concurrent article edit; refuse overwrite")
before=old.get("yoast_head_json") or {}
bad="<p><!-- "+MARKER+" --></p>\n<tr style=\"background: #f7f9fb\">\n<td style=\"padding: 12px;border: 1px solid #d8dee4\"><strong>الإسكندرية – أحمد مرعي</strong></td>"
new="<tr class=\""+MARKER+"\" style=\"background: #f7f9fb\">\n<td style=\"padding: 12px;border: 1px solid #d8dee4\"><strong>الإسكندرية – أحمد مرعي</strong></td>"
if h.count(bad)!=1:raise RuntimeError("Jetour stray paragraph and row expected exactly once")
h=h.replace(bad,new,1)
old_location='<div style="margin: 18px 0;max-width:100%">'
old_other='<div style="margin: 18px 0">'
if h.count(old_location)!=2 or h.count(old_other)!=2:raise RuntimeError("Jetour existing table wrappers unexpected")
h=h.replace(old_location,'<div class="g-table-wrap" style="margin: 18px 0;max-width:100%">',2)
h=h.replace(old_other,'<div class="g-table-wrap" style="margin: 18px 0">',2)
if h.count('class="g-table-wrap"')!=4 or h.count(MARKER)!=1:raise RuntimeError("Jetour table scroll or marker count invalid")
if wp()["modified_gmt"]!=old["modified_gmt"]:raise RuntimeError("Concurrent edit during preflight")
print("JETOUR_MOBILE_FIX_PREFLIGHT_OK",len(h),flush=True)
r=request(API+"/update-post",{"id":ID,"slug":SLUG,"content":h},True)
if r.get("ok") is False or r.get("error"):raise RuntimeError("Bridge update failed "+str(r)[:250])
live=None
for i in range(5):
    x=wp()
    if x["content"]["rendered"].count('class="g-table-wrap"')==4:live=x;break
    time.sleep(3)
if live is None:raise RuntimeError("Mobile wrapper classes missing on production")
body=live["content"]["rendered"]
assert ('<tr class="'+MARKER+'"') in body and "<p><!-- "+MARKER not in body
assert body.count("01273337055")==2 and "12 مركزًا" in body and body.count("class=\"g-table-wrap\"")==4
seo=live.get("yoast_head_json") or {}
assert (live["slug"],live["status"],live["featured_media"])==(SLUG,"publish",COVER)
assert seo.get("canonical")==before.get("canonical") and seo.get("og_image") and seo.get("robots",{}).get("index")!="noindex"
print("JETOUR_MOBILE_FIX_LIVE_VERIFIED",live["link"],"4_scroll_wrappers",flush=True)
