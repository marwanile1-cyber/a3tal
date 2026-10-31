#!/usr/bin/env python3
"""Improve existing Egypt service centers guide with verified GB Auto and Mansour hubs."""
import os,json,time,urllib.request,urllib.parse
SITE="https://a3tal.com";API=SITE+"/wp-json/a3tal-direct/v1";KEY=os.environ["A3TAL_API_KEY"]
ID=79924
SLUG="%d9%85%d8%b1%d8%a7%d9%83%d8%b2-%d8%ae%d8%af%d9%85%d8%a9-%d8%a7%d9%84%d8%b3%d9%8a%d8%a7%d8%b1%d8%a7%d8%aa-%d9%81%d9%8a-%d9%85%d8%b5%d8%b1-%d8%af%d9%84%d9%8a%d9%84%d9%83-%d8%a7%d9%84%d8%a3%d9%83%d8%a8"
MODIFIED="2026-09-06T13:00:28";FEATURED=79926;MARK="A3TAL-CENTER-HUB-UPDATED-20261031"
def request(url,body=None,auth=False):
    headers={"Accept":"application/json","User-Agent":"A3tal-Service-Center-Guide-Update/20261031","Cache-Control":"no-cache,no-store"}
    if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=json.dumps(body,ensure_ascii=False).encode("utf8") if body is not None else None
    if data is not None:headers["Content-Type"]="application/json; charset=utf-8"
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers,data=data,method="POST" if data is not None else "GET"),timeout=120) as response:return json.load(response)
def wp():
    return request(SITE+"/wp-json/wp/v2/posts/"+str(ID)+"?"+urllib.parse.urlencode({
        "_fields":"id,slug,status,modified_gmt,link,featured_media,content,yoast_head_json", "service_hub_check":"20261031"}))
old=wp()
if (old["id"],old["slug"],old["status"],old["featured_media"])!=(ID,SLUG,"publish",FEATURED):
    raise RuntimeError("Existing guide identity/cover mismatch")
h=old["content"]["rendered"]
if MARK in h:
    print("SERVICE_CENTER_HUB_ALREADY_UPDATED",old["link"]);raise SystemExit(0)
if old["modified_gmt"]!=MODIFIED:raise RuntimeError("Guide modified since original audit")
if len(h)<13000 or h.count("<h2>")<15:raise RuntimeError("Unexpected guide content")
seo=old.get("yoast_head_json") or {}
if not seo.get("og_image") or seo.get("robots",{}).get("index")=="noindex":raise RuntimeError("SEO preflight failed")
start="<h2>دليل مراكز صيانة السيارات حسب العلامة</h2>"
assert h.count(start)==1
# Add two existing, verified hub pages rather than creating duplicate posts.
tbody="<tbody>\n<tr>\n<td style=\"border: 1px solid #ddd; padding: 10px;\"><strong>هيونداي</strong>"
assert h.count(tbody)==1
row=(
 '<tbody>\n<tr class="'+MARK+'"><td style="border: 1px solid #ddd; padding: 10px;"><strong>غبور أوتو</strong></td>'
 '<td style="border: 1px solid #ddd; padding: 10px;"><a href="https://a3tal.com/ghabbour-auto-maintenance-booking-numbers-branches/">أرقام غبور وحجز الصيانة حسب الماركة</a></td>'
 '<td style="border: 1px solid #ddd; padding: 10px;">مراجعة الأرقام الرسمية 31 أكتوبر 2026</td></tr>\n'
 '<tr><td style="border: 1px solid #ddd; padding: 10px;"><strong>منصور للسيارات</strong></td>'
 '<td style="border: 1px solid #ddd; padding: 10px;"><a href="https://a3tal.com/الدليل-الشامل-أرقام-مراكز-خدمة-المنصو/">الخط الساخن لمجموعة منصور ومراكز العلامات</a></td>'
 '<td style="border: 1px solid #ddd; padding: 10px;">مراجعة الأرقام والتصنيفات 31 أكتوبر 2026</td></tr>\n'
 '<tr>\n<td style="border: 1px solid #ddd; padding: 10px;"><strong>هيونداي</strong>'
)
h=h.replace(tbody,row,1)
oldjet='<td style="border: 1px solid #ddd; padding: 10px;">محدث سبتمبر 2026</td>'
assert h.count(oldjet)==1
h=h.replace(oldjet,'<td style="border: 1px solid #ddd; padding: 10px;">مراجعة 31 أكتوبر 2026: 12 مركز ما بعد بيع</td>',1)
olddate="<strong>آخر مراجعة: سبتمبر 2026.</strong>"
assert h.count(olddate)==1
h=h.replace(olddate,
  "<strong>مراجعة روابط غبور ومنصور وجيتور: 31 أكتوبر 2026.</strong> بقية العلامات تُراجع حسب تحديث صفحاتها المنفصلة.",1)
# Use the current theme's existing horizontal-scroll class, not disallowed inline overflow style.
head="<h2>دليل مراكز صيانة السيارات حسب العلامة</h2>\n<table"
assert h.count(head)==1
h=h.replace(head,'<h2>دليل مراكز صيانة السيارات حسب العلامة</h2>\n<div class="g-table-wrap">\n<table',1)
endtable="</tbody>\n</table>"
assert h.count(endtable)>=1
# Only wrap the first brand-index table.
pos=h.index("</tbody>\n</table>",h.index(start))
h=h[:pos]+h[pos:].replace("</tbody>\n</table>","</tbody>\n</table>\n</div>",1)
if h.count(MARK)!=1 or 'class="g-table-wrap"' not in h or len(h)<len(old["content"]["rendered"]):
    raise RuntimeError("Guide patch failed checks")
if wp()["modified_gmt"]!=old["modified_gmt"]:raise RuntimeError("Concurrent guide modification")
print("CENTER_HUB_PREFLIGHT_OK",ID,len(h),flush=True)
reply=request(API+"/update-post",{
  "id":ID,"slug":SLUG,
  "title":"مراكز خدمة السيارات في مصر: دليل التوكيلات والصيانة المعتمدة",
  "content":h,
  "meta":{
    "_yoast_wpseo_title":"مراكز خدمة السيارات في مصر | التوكيلات والحجز والفروع | أعطال",
    "_yoast_wpseo_metadesc":"دليل مراكز خدمة السيارات في مصر حسب الماركة: غبور ومنصور وجيتور وكيا وهيونداي وسكودا وغيرها، مع روابط الأرقام والفروع والحجز الموثقة."
  }
},True)
if reply.get("ok") is False or reply.get("error"):raise RuntimeError("Bridge write rejected "+str(reply)[:250])
live=None
for _ in range(5):
    p=wp()
    if MARK in p["content"]["rendered"]:live=p;break
    time.sleep(3)
if live is None:raise RuntimeError("Center guide patch not live")
if (live["id"],live["slug"],live["status"],live["featured_media"])!=(ID,SLUG,"publish",FEATURED):
    raise RuntimeError("Guide identity or media changed")
newseo=live.get("yoast_head_json") or {}
if newseo.get("canonical")!=seo.get("canonical") or not newseo.get("og_image") or newseo.get("robots",{}).get("index")=="noindex":
    raise RuntimeError("Guide canonical, image, index integrity failed")
if "مراجعة 31 أكتوبر 2026: 12 مركز" not in live["content"]["rendered"] or 'class="g-table-wrap"' not in live["content"]["rendered"]:
    raise RuntimeError("Guide updates incomplete")
print("CENTER_HUB_LIVE_VERIFIED",live["link"],"image",live["featured_media"],flush=True)
