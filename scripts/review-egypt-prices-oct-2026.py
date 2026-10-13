#!/usr/bin/env python3
"""A3tal.com October 2026 Egyptian price-list audit and cautious editorial refresh.
The only write channel is A3tal Direct Bridge via GitHub Actions. No WPWriter.
Official EIT Kia price-list supplied 13 Oct 2026; Skoda price-change source
https://eg.hatla2ee.com/ar/new-car/price-change .
Avoid changing article slugs, media, Yoast or prices for model years not verified.
"""
import os, sys, json, time, re
from urllib.request import Request, urlopen
from urllib.parse import urlencode

BASE="https://a3tal.com"
BRIDGE=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
APPLY=os.getenv("PRICE_APPLY","0")=="1"
if not KEY: raise SystemExit("A3TAL_API_KEY not configured")
HEADERS={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Accept":"application/json","User-Agent":"A3tal-Egypt-Price-Audit/2026-10-14"}

POSTS={
 "seltos":83428,
 "electric":80371,
 "new_cars":80189,
 "skoda":80666,
 "sportage":81438,
 "ev3":81223,
 "pv5":82270,
}
MARK="A3TAL-PRICE-REVIEW-2026-10-13"
KIA_K4={"Highline":1519900,"GT-Line":1719900,"GT-Line Black Edition":1859900}
KIA_SELTOS={"EX":1369900,"Highline Turbo":1524900,"Topline Turbo":1674900}
KIA_SPORTAGE={"LX":1824900,"EX":1924900,"Highline":2074900,"Premium":2299900,"GT-Line":2399900}

def get(url, protected=True):
    h=HEADERS if protected else {"Accept":"application/json","User-Agent":"A3tal-Price-Audit/1.0"}
    req=Request(url,headers=h)
    for n in range(3):
        try:
            with urlopen(req,timeout=80) as f: return json.load(f)
        except Exception as e:
            if n==2: raise
            print("READ RETRY",type(e).__name__,str(e)[:100],flush=True)
            time.sleep(5*(n+1))

def post(path, data):
    # Exactly one attempt: never replay a timed-out write without confirming state.
    req=Request(BRIDGE+path,data=json.dumps(data,ensure_ascii=False).encode(),headers=HEADERS,method="POST")
    with urlopen(req,timeout=120) as f: return json.load(f)

def find_heading(body, phrase):
    pattern=r"(<h[23][^>]*>\s*[^<]*"+re.escape(phrase)+r"[^<]*</h[23]>)"
    m=re.search(pattern,body,re.I)
    return m

def update_editorial(postid, old, new, label):
    if new==old:
        print("UNCHANGED",label,flush=True);return
    if not APPLY:
        print("DRY RUN",label,"chars",len(old),"->",len(new),flush=True);return
    current=get(BRIDGE+"/post/"+str(postid))
    if current["content"]!=old: raise RuntimeError("Conflict: article changed since preflight: "+label)
    result=post("/update-post",{"id":postid,"content":new})
    if result["id"]!=postid:
        raise RuntimeError("Edit acknowledgment missing: "+label)
    verified=get(BRIDGE+"/post/"+str(postid))
    # WordPress applies wp_kses_post and can strip inline style attributes.
    # Check distinctive saved facts rather than demanding byte-identical HTML.
    checks={
        "seltos":["13 أكتوبر 2026","قائمة EIT"],
        "electric":["كيا EV9 2025","3,750,000","كيا EV6 2026"],
        "new_cars":["كيا K4 2027","1,859,900","1,674,900"],
        "skoda":["أوكتافيا 2027","2,625,000","3,150,000"]
    }
    if (verified["slug"]!=current["slug"] or verified["featured_media"]!=current["featured_media"]
       or verified["status"]!=current["status"] or
       not all(token in verified["content"] for token in checks[label])):
        raise RuntimeError("Post data verification failed for "+label)
    print("UPDATED VERIFIED",label,verified["link"],flush=True)

def seltos_refresh(c):
    body=c["content"]
    if MARK+"-SELTOS" in body:return body
    pattern=r"(آخر مراجعة للأسعار والمواصفات:\s*)10 أكتوبر 2026"
    replacement=(r"\g<1>13 أكتوبر 2026"
       " <!-- "+MARK+"-SELTOS -->"
       " (قائمة EIT السارية من 13 أكتوبر 2026 لموديل 2027؛ جميع أسعار الفئات الثلاث مطابقة للجدول أدناه)")
    result,count=re.subn(pattern,replacement,body,count=1)
    if count!=1: raise RuntimeError("Seltos existing review date differs, manual inspection required")
    return result

def electric_refresh(c):
    body=c["content"]
    if MARK+"-ELECTRIC" in body:return body
    target=find_heading(body,"سيارات ديبال الكهربائية")
    if not target: raise RuntimeError("Electric guide heading not found, unsafe to insert")
    add=(
    "<!-- "+MARK+"-ELECTRIC -->\n"
    "<h3>أسعار كيا EV5 وEV6 وEV9 وPV5 في أكتوبر 2026</h3>"
    "<p>بحسب قائمة EIT المؤرخة 13 أكتوبر 2026، الأسعار التالية للنسخ المصرية المحددة. "
    "ظهرت فئة GT بسعر 3 ملايين جنيه ضمن EV6. لا تُخلط سنة الموديل بين الطرازات.</p>"
    '<div style="overflow-x:auto"><table><thead><tr><th>السيارة والسنة</th><th>الفئة</th><th>السعر بالجنيه</th></tr></thead><tbody>'
    '<tr><td>كيا EV5 2026</td><td>Air / Earth / GT-Line</td><td>2,050,000 / 2,300,000 / 2,550,000</td></tr>'
    '<tr><td>كيا EV6 2026</td><td>Earth / GT-Line / GT</td><td>2,300,000 / 2,550,000 / 3,000,000</td></tr>'
    '<tr><td>كيا EV9 2025</td><td>7 مقاعد / 6 Swiveling / 6 Relaxing</td><td>3,700,000 / 3,750,000 / 3,800,000</td></tr>'
    '<tr><td>كيا PV5 2026</td><td>Elite</td><td>2,500,000</td></tr>'
    '</tbody></table></div>'
    '<p><small>تاريخ التحقق: 13 أكتوبر 2026، أسعار وكيل وليست عروض تسليم أو سعر سوق مستعمل. '
    'المصدر: قائمة أسعار Kia Egypt / EIT المحدثة بتاريخ 13 أكتوبر 2026.</small></p>\n'
    )
    return body[:target.start()]+add+body[target.start():]

def cars_refresh(c):
    body=c["content"]
    if MARK+"-GENERAL" in body:return body
    target=find_heading(body,"أسعار سيارات 2027 من 1.5 إلى 2.5 مليون")
    if not target: raise RuntimeError("New-car guide target section not found")
    snippet=(
       "\n<!-- "+MARK+"-GENERAL -->\n"
       "<h3>أحدث أسعار كيا K4 وسيلتوس وسبورتاج 2027</h3>"
       "<p>توضح قائمة وكيل كيا EIT السارية من 13 أكتوبر 2026 ارتفاع K4 بمقدار 10 إلى 20 ألف جنيه "
       "وسيلتوس بمقدار 20 إلى 50 ألف جنيه حسب الفئة مقارنة بالقائمة السابقة، مع استقرار أسعار سبورتاج 2027.</p>"
       '<div style="overflow-x:auto"><table><thead><tr><th>الموديل</th><th>أقل سعر رسمي</th><th>أعلى سعر رسمي</th></tr></thead><tbody>'
       '<tr><td>كيا K4 2027</td><td>1,519,900 جنيه</td><td>1,859,900 جنيه</td></tr>'
       '<tr><td>كيا سيلتوس 2027</td><td>1,369,900 جنيه</td><td>1,674,900 جنيه</td></tr>'
       '<tr><td>كيا سبورتاج 2027</td><td>1,824,900 جنيه</td><td>2,399,900 جنيه</td></tr>'
       '</tbody></table></div>'
       '<p>اقرأ <a href="https://a3tal.com/kia-seltos-price-specs-egypt-buying-guide/">تفاصيل فئات سيلتوس</a> '
       'و<a href="https://a3tal.com/kia-sportage-2027-price-egypt/">مقارنة فئات سبورتاج 2027</a>. '
       '<small>مصدر الأسعار: قائمة Kia Egypt / EIT الرسمية المؤرخة 13 أكتوبر 2026؛ '
       'التأمين والترخيص ورسوم التسليم غير مشمولة ما لم يذكر الوكيل خلاف ذلك.</small></p>\n'
    )
    return body[:target.end()]+snippet+body[target.end():]

def skoda_refresh(c):
    body=c["content"]
    if MARK+"-SKODA" in body:return body
    m=re.search(r"<h2\\b[^>]*>",body,re.I)
    if not m: raise RuntimeError("Skoda article has no h2")
    insert=(
      "\n<!-- "+MARK+"-SKODA -->\n"
      '<h2>تحديث أسعار سكودا 2027 في مصر بتاريخ 13 أكتوبر 2026</h2>'
      '<p>صدرت قائمة أسعار موديلات سكودا 2027 في مصر خلال أكتوبر 2026. '
      'أسعار سنة الموديل 2027 أدناه منفصلة عن جدول موديل 2026 الموجود في الدليل.</p>'
      '<div style="overflow-x:auto"><table><thead><tr><th>الطراز 2027</th><th>الفئة</th><th>السعر الرسمي بالجنيه</th></tr></thead><tbody>'
      '<tr><td>سكودا أوكتافيا A8</td><td>Loft</td><td>1,825,000</td></tr>'
      '<tr><td>سكودا أوكتافيا A8</td><td>Lounge</td><td>2,050,000</td></tr>'
      '<tr><td>سكودا أوكتافيا A8</td><td>Suite</td><td>2,250,000</td></tr>'
      '<tr><td>سكودا كودياك</td><td>Loft</td><td>2,625,000</td></tr>'
      '<tr><td>سكودا كودياك</td><td>Suite</td><td>3,000,000</td></tr>'
      '<tr><td>سكودا كودياك</td><td>Sportline</td><td>3,150,000</td></tr>'
      '</tbody></table></div>'
      '<p>وفق سجل تحركات السوق المؤرخ 13 أكتوبر، بلغت زيادات أوكتافيا 25 إلى 100 ألف جنيه '
      'بحسب الفئة مقارنة بالقائمة السابقة لموديل 2027، وزادت كودياك بمقدار 25 إلى 50 ألف جنيه. '
      'جدول موديل 2026 الأصلي في أسفل الصفحة لا يُستخدم باعتباره سعرًا لموديل 2027.</p>'
      '<p><small>المراجع: '
      '<a href="https://eg.hatla2ee.com/ar/new-car/price-change/skoda">هتلاقي: حركة أسعار سكودا</a>، '
      '<a href="https://www.shift-eg.com/news/local-news/details/27055/">تقرير الوكيل عن سكودا أوكتافيا 2027</a>. '
      'آخر مراجعة للأسعار: 13 أكتوبر 2026.</small></p>\n'
    )
    return body[:m.start()]+insert+body[m.start():]

def main():
    health=get(BRIDGE+"/status")
    print("BRIDGE",health.get("ok"),health.get("version"),"APPLY",APPLY,flush=True)
    records=get(BASE+"/wp-json/wp/v2/a3tal-cars?per_page=100&_fields=id,slug,title,link",protected=False)
    kia=[{"id":r["id"],"name":r["title"]["rendered"],"slug":r["slug"]} for r in records if "kia" in r["title"]["rendered"].lower() or "كيا" in r["title"]["rendered"]]
    print("CAR_ENTITIES",len(records),"KIA",json.dumps(kia,ensure_ascii=False),flush=True)
    if len(records)<10: raise RuntimeError("Car database unexpectedly sparse")
    seltos_car=next((x for x in kia if x["slug"]=="kia-seltos-egypt-2026"),None)
    if not seltos_car: raise RuntimeError("Expected Seltos car entity missing; do not create duplicate")
    if seltos_car["id"]!=83434: raise RuntimeError("Unexpected Seltos car id")
    oldyear=get(BRIDGE+"/admin?"+urlencode({"op":"post_meta","post_id":83434,"key":"_a3_year"}))
    print("SELTOS_META_YEAR",oldyear.get("result"),flush=True)
    entries={k:get(BRIDGE+"/post/"+str(v)) for k,v in POSTS.items()}
    for k,c in entries.items():
        print("POST",k,c["id"],c["slug"],"chars",len(c["content"]),"featured",c["featured_media"],
              "contains2027","2027" in c["content"],flush=True)
    for k,price in (("seltos",1369900),("sportage",1824900),("ev3",1400000),("pv5",2500000)):
        token=format(price,",")
        if token not in entries[k]["content"]:raise RuntimeError("Known verified current "+k+" price missing: "+token)
    changes=[
      ("seltos",seltos_refresh),
      ("electric",electric_refresh),
      ("new_cars",cars_refresh),
      ("skoda",skoda_refresh),
    ]
    planned=[(k,entries[k]["content"],f(entries[k])) for k,f in changes]
    print("PLANNED",[(k,a!=b,len(b)-len(a)) for k,a,b in planned],flush=True)
    if not APPLY:
        print("AUDIT COMPLETE, NO WRITES. To apply, set PRICE_APPLY=1 in workflow.",flush=True)
        return
    # Update standalone Seltos entity in-place. Preserve slug, image, taxonomy, source URL and links.
    if oldyear.get("result",{}).get("_a3_year") not in ("2026","2027"):
        raise RuntimeError("Unexpected Seltos year metadata; refuse site write")
    for label,old,new in planned:
        update_editorial(POSTS[label],old,new,label)
        time.sleep(4)
    if oldyear.get("result",{}).get("_a3_year")=="2026" or "2026" in seltos_car["name"]:
        live_car=get(BRIDGE+"/post/83434")
        if live_car["slug"]!="kia-seltos-egypt-2026" or live_car["featured_media"]!=83433:
            raise RuntimeError("Unexpected Seltos original slug/photo: do not modify")
        if "10 أكتوبر 2026" not in live_car["content"]:
            raise RuntimeError("Unexpected Seltos content date; check manually")
        fixed_content=live_car["content"].replace(
            "وفق موقع كيا الرسمي بتاريخ 10 أكتوبر 2026",
            "وفق قائمة أسعار EIT السارية من 13 أكتوبر 2026 لموديل 2027"
        )
        if fixed_content==live_car["content"]:
            raise RuntimeError("Old Seltos attribution not found; avoid stale source")
        payload={
          "op":"platform_entity_upsert","type":"a3_car","id":83434,
          "title":"Kia Seltos 2027","status":"publish","content":fixed_content,
          "excerpt":"كيا سيلتوس موديل 2027 في مصر: EX بسعر 1,369,900 جنيه، Highline Turbo بسعر 1,524,900 جنيه، Topline Turbo بسعر 1,674,900 جنيه وفق قائمة 13 أكتوبر 2026.",
          "meta":{"_a3_year":"2027","_a3_source_checked_at":"2026-10-13"}
        }
        response=post("/admin",payload)
        if not response.get("ok") or response.get("result",{}).get("id")!=83434:
            raise RuntimeError("Seltos car bridge confirmation missing")
        fresh=get(BASE+"/wp-json/wp/v2/a3tal-cars?slug=kia-seltos-egypt-2026&_fields=id,slug,title,link",protected=False)
        year=get(BRIDGE+"/admin?"+urlencode({"op":"post_meta","post_id":83434,"key":"_a3_year"}))
        updated_car=get(BRIDGE+"/post/83434")
        if (len(fresh)!=1 or fresh[0]["title"]["rendered"]!="Kia Seltos 2027"
           or year.get("result",{}).get("_a3_year")!="2027"
           or "EIT السارية من 13 أكتوبر 2026" not in updated_car["content"]
           or updated_car["slug"]!=live_car["slug"]
           or updated_car["featured_media"]!=live_car["featured_media"]):
            raise RuntimeError("Seltos public year/title verification failed")
        print("CAR VERIFIED 2027",fresh[0]["link"],flush=True)
    print("SUCCESS: October Kia prices and targeted Skoda 2027 note synchronized; original URLs preserved.",flush=True)

if __name__=="__main__":
    main()
