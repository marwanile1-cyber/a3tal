#!/usr/bin/env python3
"""Idempotent existing Jetour service centers correction with revision and SEO integrity guards."""
import os,json,re,time,urllib.parse,urllib.request
SITE="https://a3tal.com"
BASE=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
ID=80401
SLUG="%d9%85%d8%b1%d8%a7%d9%83%d8%b2-%d8%ae%d8%af%d9%85%d8%a9-%d8%ac%d9%8a%d8%aa%d9%88%d8%b1-%d8%a7%d9%84%d9%85%d8%b9%d8%aa%d9%85%d8%af%d8%a9-%d9%81%d9%8a-%d9%85%d8%b5%d8%b1"
EXPECTED="2026-10-20T17:16:10"
COVER=82886
MARKER="A3TAL-JETOUR-AHMED-MAREY-SERVICE-20261031-V1"
def req(url,body=None,auth=False):
    headers={"Accept":"application/json","User-Agent":"A3tal-Jetour-Service-SEO-Verified/20261031","Cache-Control":"no-cache,no-store"}
    if auth: headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=json.dumps(body,ensure_ascii=False).encode("utf8") if body is not None else None
    if data is not None:headers["Content-Type"]="application/json; charset=utf-8"
    request=urllib.request.Request(url,headers=headers,data=data,method="POST" if data is not None else "GET")
    with urllib.request.urlopen(request,timeout=120) as resp: return json.load(resp)
def wp():
    return req(SITE+"/wp-json/wp/v2/posts/"+str(ID)+"?"+urllib.parse.urlencode({
      "_fields":"id,slug,status,modified_gmt,link,featured_media,content,categories,yoast_head_json",
      "a3tal_audit":"20261031"}))
p=wp()
if (p["id"],p["slug"],p["status"],p["featured_media"])!=(ID,SLUG,"publish",COVER):raise RuntimeError("JETOUR identity/featured mismatch")
h=p["content"]["rendered"]
if MARKER in h:
    print("JETOUR_ALREADY_UPDATED",p["link"],flush=True);raise SystemExit(0)
if p["modified_gmt"]!=EXPECTED:raise RuntimeError("JETOUR concurrent change detected; no overwrite")
if len(h)<13000 or h.count("<h2>")<9 or "جيتور" not in h:raise RuntimeError("JETOUR unexpected original HTML structure")
priorseo=p.get("yoast_head_json") or {}
if not priorseo.get("og_image") or priorseo.get("robots",{}).get("index")=="noindex":raise RuntimeError("JETOUR current SEO integrity invalid")
# The latest official Jetour aftersales location filter includes Ahmed Marey, Alexandria.
# Place it after the current Alexandria Alex ECC row in the governorates table.
anchor='<td style="padding: 12px;border: 1px solid #d8dee4"><strong>الإسماعيلية – سلطان أوتوموتيف</strong></td>'
assert h.count(anchor)==1,"JETOUR expected Ismailia row exactly once"
additional='''<!-- A3TAL-JETOUR-AHMED-MAREY-SERVICE-20261031-V1 -->
<tr style="background: #f7f9fb">
<td style="padding: 12px;border: 1px solid #d8dee4"><strong>الإسكندرية – أحمد مرعي</strong></td>
<td style="padding: 12px;border: 1px solid #d8dee4">بشاير الخير 3، منطقة الاستثمار، الإسكندرية</td>
<td style="padding: 12px;border: 1px solid #d8dee4">السبت–الخميس: 9 ص–5 م</td>
<td style="padding: 12px;border: 1px solid #d8dee4"><a href="tel:01273337055">01273337055</a></td>
</tr>
<tr>
'''
before="<tr>\n"+anchor
assert h.count(before)==1,"JETOUR governorates insertion point has changed"
h=h.replace(before,additional+anchor,1)
olddate="آخر مراجعة للأرقام والعناوين: 5 سبتمبر 2026"
assert h.count(olddate)==1,"JETOUR dated field changed unexpectedly"
h=h.replace(olddate,"آخر مراجعة للأرقام والعناوين: 31 أكتوبر 2026",1)
oldcount="تضم القائمة الحالية 11 مركزًا"
assert h.count(oldcount)==1,"JETOUR count phrase changed unexpectedly"
h=h.replace(oldcount,"تضم القائمة الحالية 12 مركزًا",1)
# Existing wide tables should scroll within their containers, not overflow the phone viewport.
oldwrap='<div style="margin: 18px 0">\n<table style="width: 100%;border-collapse: collapse;min-width: 9'
assert h.count(oldwrap)==2,"JETOUR expected exactly two wide location tables"
h=h.replace(oldwrap,'<div style="margin: 18px 0;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch">\n<table style="width: 100%;border-collapse: collapse;min-width: 9',2)
ref="https://jetouregypt.com/shopping-tools/our-locations/"
assert h.count(ref)>=1,"JETOUR official source missing"
# Add explicit useful navigation from the page to other verified workshop references.
needle="<h2>كيف تحجز صيانة جيتور خطوة بخطوة؟</h2>"
assert h.count(needle)==1,"JETOUR booking heading unavailable"
linknote=('<p>في الإسكندرية، يظهر <strong>مركز أحمد مرعي</strong> ضمن قسم <strong>Aftersales</strong> '
'على <a href="'+ref+'" rel="noopener noreferrer">موقع جيتور الرسمي</a>، بخلاف صالات المبيعات فقط. '
'يمكن أيضًا تصفح <a href="https://a3tal.com/service-centers/">دليل مراكز الخدمة في أعطال</a> '
'للاطلاع على مراكز علامات أخرى؛ وهو ليس بديلًا عن تأكيد اعتماد مركز جيتور من الوكيل.</p>\n')
h=h.replace(needle,linknote+needle,1)
if h.count(MARKER)!=1 or len(h)<14000:raise RuntimeError("JETOUR final HTML validation failed")
if wp()["modified_gmt"]!=p["modified_gmt"]:raise RuntimeError("JETOUR concurrent edit before write")
print("JETOUR_PREFLIGHT_OK",ID,len(h),flush=True)
reply=req(BASE+"/update-post",{"id":ID,"slug":SLUG,"content":h,
 "meta":{"_yoast_wpseo_metadesc":
 "توكيل جيتور مصر: الخط الساخن 16263 ومراكز صيانة القصراوي المعتمدة في القاهرة والجيزة والإسكندرية والمحافظات، مع الأرقام والعناوين ومواعيد الحجز."}},True)
if reply.get("error") or reply.get("ok") is False:raise RuntimeError("JETOUR bridge write rejected "+str(reply)[:220])
live=None
for _ in range(5):
    q=wp()
    if MARKER in q["content"]["rendered"]:live=q;break
    time.sleep(3)
if live is None:raise RuntimeError("JETOUR live published HTML not updated")
if (live["id"],live["slug"],live["status"],live["featured_media"])!=(ID,SLUG,"publish",COVER):
    raise RuntimeError("JETOUR post identity or media changed")
now=live.get("yoast_head_json") or {}
if now.get("canonical")!=priorseo.get("canonical") or not now.get("og_image") or now.get("robots",{}).get("index")=="noindex":
    raise RuntimeError("JETOUR SEO canonical, index or image regressed")
for check in ["01273337055","12 مركزًا","31 أكتوبر 2026","overflow-x:auto"]:
    if check not in live["content"]["rendered"]:raise RuntimeError("JETOUR missing "+check)
print("JETOUR_LIVE_VERIFIED",live["link"],"IMG",live["featured_media"],"CANONICAL",now.get("canonical"),flush=True)
