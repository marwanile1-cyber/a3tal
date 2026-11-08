#!/usr/bin/env python3
"""Safely link EV5/EV6/EV9 into Kia's live brand hub; keep old media and canonicals."""
import json,os,re,time
from html import escape
from pathlib import Path
import requests
BASE="https://a3tal.com"; REST=BASE+"/wp-json/wp/v2/car-reference-records"; API=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
S=requests.Session();S.headers["User-Agent"]="A3tal-Kia-Electric-Model-Hub-Linker/1.0"
KEY=os.environ["A3TAL_API_KEY"]
REPORT=Path(__file__).resolve().parents[1]/"data/car-reference/kia-electric-ev5-ev6-ev9-hub-audit.json"
models=[
 ("ev5-longrange-egypt","كيا EV5 الكهربائية في مصر","بطارية LFP سعتها88.1kWh، الفروق بين FWD ‏229 حصان وGT-Line AWD ‏325 حصان والمدى والشحن"),
 ("ev6-longrange-egypt","كيا EV6 الكهربائية في مصر","بطارية84kWh وموتور225 حصان ودفع خلفي RWD مع المدى والشحن وفرق Earth وGT-Line"),
 ("ev9-gtline-egypt","كيا EV9 الكهربائية في مصر","بطارية99.8kWh ودفع AWD ‏380 حصان ونسخ ستة أو سبعة مقاعد مع شرح تضارب المدى الرسمي"),
]
r=S.get(REST,params={"slug":"kia","per_page":2},timeout=60);r.raise_for_status()
rows=[x for x in r.json() if x.get("slug")=="kia" and x.get("status")=="publish"]
assert len(rows)==1,"Kia brand must exist"
old=rows[0]
assert old["id"]==84884 and old["featured_media"]==84955 and old["link"].rstrip("/")==BASE+"/car-reference/kia"
html=old["content"]["rendered"]
assert "دليل كيا" in html and html.count("</tbody>")==1 and "/ev3-air-earth-gtline-egypt/" in html, "Unexpected hub content; refuse destructive update"
new_links=[]
for slug,title,summary in models:
    u=BASE+"/car-reference/kia/"+slug+"/"
    test=S.get(u,timeout=60);test.raise_for_status()
    assert test.url.split("?")[0].rstrip("/")==u.rstrip("/")
    assert "canonical" in test.text.lower() and "og:image" in test.text.lower()
    if "/"+slug+"/" not in html:
        row="<tr><th scope='row'><a href='"+escape(u,quote=True)+"'>"+escape(title)+"</a></th><td>"+escape(summary)+"</td></tr>"
        html=html.replace("</tbody>",row+"</tbody>",1)
        new_links.append(u)
if not new_links:
    print("KIA_HUB_ALL_3_ELECTRIC_MODELS_ALREADY_LINKED")
else:
    html+="<p>الموديلات الكهربائية EV3 وEV5 وEV6 وEV9 تختلف في البطارية والدفع ومدى الاختبار وتجهيزات الأمان. عند البحث عن مواصفة فنية افتح صفحة الموديل والفئة أولًا، ولا تستخدم نوع زيت أو رقم مدى أو زمن شحن موديل آخر.</p>"
    payload={"kind":"brand","slug":"kia","title":old["title"]["rendered"],"status":"publish","parent_path":"","featured_image_id":84955,"allow_update_published":True,
      "content":html,"excerpt":"دليل سيارات كيا في مصر: موديلات البنزين والهجين والكهرباء EV3 وEV5 وEV6 وEV9، مع المواصفات الفنية بحسب الفئة.",
      "meta_title":"مواصفات سيارات كيا في مصر: بنزين وهايبرد وكهرباء | أعطال.كوم",
      "meta_description":"دليل مواصفات سيارات كيا في مصر: سيراتو وسيلتوس وسبورتاج وسورينتو وكرنفال وEV3 وEV5 وEV6 وEV9. اختر الموديل لتعرف البطارية والمحرك والصيانة.",
      "data":{"kind":"brand","market":"مصر","years":"حسب الموديل","engine":"محركات بنزين وهجينة وكهربائية","reviewed_at":"2026-11-08","sources":[{"title":"كيا مصر EV5","url":"https://www.kia.com.eg/kia-ev5-specifications"},{"title":"كيا مصر EV6","url":"https://www.kia.com.eg/kia-ev6-specifications"},{"title":"كيا مصر EV9","url":"https://www.kia.com.eg/kia-ev9-specifications"}]}}
    response=S.post(API,headers={"X-A3tal-Key":KEY},json={"items":[payload],"allow_update_published":True},timeout=180)
    response.raise_for_status()
    result=response.json();assert result.get("ok") and result.get("results",[{}])[0].get("ok"),result
    assert result["results"][0]["url"].rstrip("/")==old["link"].rstrip("/")
validated=False
for attempt in range(9):
    actual=S.get(old["link"],params={"electric_kia_link_qa":str(time.time_ns())},headers={"Cache-Control":"no-cache"},timeout=65).text
    if all("/car-reference/kia/"+slug+"/" in actual for slug,_,_ in models) and "canonical" in actual.lower() and "og:image" in actual.lower():
        validated=True;break
    time.sleep(3)
assert validated,"Kia hub missing one or more new electric model links or SEO media"
after=S.get(REST,params={"slug":"kia","per_page":2},timeout=50).json()
assert len(after)==1 and after[0]["id"]==84884 and after[0]["featured_media"]==84955
assert after[0]["content"]["rendered"].count("/ev9-gtline-egypt/")==1
REPORT.write_text(json.dumps({"ok":True,"url":old["link"],"brand_post_id":84884,"media_preserved":84955,"added":new_links,"models":[s for s,_,_ in models]},ensure_ascii=False,indent=2),encoding="utf8")
print("KIA_EV5_EV6_EV9_BRAND_HUB_LINKS_AND_ORIGINAL_MEDIA_VERIFIED",len(new_links),flush=True)
