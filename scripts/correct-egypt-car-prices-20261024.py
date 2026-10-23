#!/usr/bin/env python3
"""October 24 2026: guarded live price corrections. GitHub Actions -> A3tal Direct Bridge only."""
import json,os,re
from urllib.request import Request,urlopen
from urllib.parse import urlencode

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ["A3TAL_API_KEY"]
HEAD={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Accept":"application/json","User-Agent":"A3tal-Oct24-Price-Repair/1.0"}
MARK="تحديث الأسعار المنشورة في 22 أكتوبر 2026"
SOURCES={
"hyundai-tucson-2027-egypt":"https://www.masrawy.com/autos/autos_news/details/2026/10/22/3066784/",
"chery-tiggo-7-pro-max-egypt":"https://www.masrawy.com/autos/autos_news/details/2026/10/22/3066843/",
"deepal-s07-2026-egypt":"https://www.masrawy.com/autos/autos_news/details/2026/10/22/3066800"}
CARS=[
("hyundai-tucson-2027-egypt",1800000,2400000,1850000,2450000,{"1,800,000":"1,850,000","1,950,000":"2,000,000","2,050,000":"2,100,000","2,125,000":"2,175,000","2,200,000":"2,240,000","2,300,000":"2,350,000","2,400,000":"2,450,000"}),
("chery-tiggo-7-pro-max-egypt",1320000,1420000,1340000,1440000,{"1,320,000":"1,340,000","1,420,000":"1,440,000"}),
("deepal-s07-2026-egypt",1925000,2015000,1975000,2065000,{"1,925,000":"1,975,000","2,015,000":"2,065,000"})]
def req(url,body=None,secure=True):
    h=HEAD if secure else {"Accept":"application/json","User-Agent":"A3tal-Price-Correction-Read/1.0","Cache-Control":"no-cache"}
    data=json.dumps(body,ensure_ascii=False).encode("utf8") if body is not None else None
    with urlopen(Request(url,headers=h,data=data,method="POST" if data is not None else "GET"),timeout=100) as f:return json.load(f)
def api(path,body=None):return req(API+path,body)
def model(slug):
    rows=req(SITE+"/wp-json/wp/v2/a3tal-cars?"+urlencode({"slug":slug,"_fields":"id,slug,status,featured_media,link"}),secure=False)
    if len(rows)!=1 or rows[0]["slug"]!=slug or rows[0]["status"]!="publish" or not rows[0].get("featured_media"):
        raise RuntimeError("Car identity, count or image failed: "+slug)
    return rows[0]
def post(pid):return api("/post/"+str(pid))
def meta(pid,key):
    r=api("/admin?"+urlencode({"op":"post_meta","post_id":pid,"key":key}))
    if not r.get("ok"):raise RuntimeError("Meta read failed")
    return str(r["result"].get(key,"")).strip()
def swap(s,prices):
    regex=re.compile("|".join(map(re.escape,sorted(prices,key=len,reverse=True))))
    return regex.sub(lambda m:prices[m.group()],s)
def note(slug):
    if slug.startswith("hyundai"):
        desc="هيونداي توسان 2027: من 1,850,000 إلى 2,450,000 جنيه. هناك اختلاف في المصادر حول فئة Blaze: مصراوي وShift يذكران 2,000,000 جنيه، بينما يعرض هتلاقي 2,200,000 جنيه؛ يرجى مراجعة القائمة المباشرة للوكيل قبل الحجز."
    elif slug.startswith("chery"):
        desc="شيري تيجو 7 برو ماكس 2027: الفئة الأولى 1,340,000 جنيه، والفئة الأعلى 1,440,000 جنيه."
    else:
        desc="ديبال S07 موديل 2026: REEV بسعر 1,975,000 جنيه، وBEV بسعر 2,065,000 جنيه."
    return '<p><strong>'+MARK+':</strong> '+desc+' <a href="'+SOURCES[slug]+'">مصدر أسعار 22 أكتوبر</a>. تاريخ مراجعة المصدر: 24 أكتوبر 2026. الأسعار لا تشمل الرسوم أو أي تغيير لاحق عند التسليم.</p>\n'
def revise_text(slug,content,excerpt,prices,article=False):
    if MARK in content:return content,excerpt
    content=note(slug)+swap(content,prices)
    excerpt=swap(excerpt or "",prices)
    if slug.startswith("hyundai"):
        for old,new in [("1.8 إلى 2.4 مليون","1.85 إلى 2.45 مليون"),("1.8 مليون","1.85 مليون"),("2.4 مليون","2.45 مليون"),
            ("2.05 مليون","2.10 مليون"),("2.125 مليون","2.175 مليون"),("2.2 مليون","2.24 مليون"),("2.3 مليون","2.35 مليون")]:
            content=content.replace(old,new)
            excerpt=excerpt.replace(old,new)
        content=content.replace("قائمة الأسعار السارية من 15 أكتوبر 2026","قائمة الأسعار المنشورة في 22 أكتوبر 2026")
        content=content.replace("قائمة الأسعار التي بدأ العمل بها في 15 أكتوبر 2026","قائمة الأسعار المنشورة في 22 أكتوبر 2026")
        content=content.replace("مراجعة بيانات الأسعار: 16 أكتوبر 2026","مراجعة بيانات الأسعار: 24 أكتوبر 2026")
        content=content.replace("آخر مراجعة للأسعار: <strong>16 أكتوبر 2026</strong>","آخر مراجعة للأسعار: <strong>24 أكتوبر 2026</strong>")
        content=content.replace("25 ألف جنيه لكل فئة","50 ألف جنيه لمعظم الفئات و40 ألف جنيه لفئة Night")
        content=content.replace("وفق سجل التغييرات المؤرخ 15 أكتوبر 2026","وفق تحركات الأسعار المنشورة في 22 أكتوبر 2026")
        content=content.replace("<td>Night</td><td>2,240,000 جنيه</td><td>400,000 جنيه</td>","<td>Night</td><td>2,240,000 جنيه</td><td>390,000 جنيه</td>")
    return content,excerpt
def tidy_text(slug,content,excerpt,article=False):
    if slug.startswith("chery"):
        changes=[
            ("1.32 مليون","1.34 مليون"),
            ("وفق قائمة شيري الرسمية أثناء مراجعة 9 أكتوبر 2026","وفق الأسعار المنشورة يوم 22 أكتوبر 2026"),
            ("1,340,000 جنيه عند مراجعة 9 أكتوبر 2026","1,340,000 جنيه وفق قائمة 22 أكتوبر 2026"),
            ("يعرض موقع شيري مصر سعرًا ابتدائيًا بقيمة","بحسب قائمة الأسعار المنشورة في 22 أكتوبر 2026، يبلغ السعر الابتدائي"),
            ("**تاريخ مراجعة البيانات:** 9 أكتوبر 2026","**تاريخ مراجعة المواصفات:** 9 أكتوبر 2026، والأسعار: 24 أكتوبر 2026"),
            ("<strong>تاريخ مراجعة البيانات:</strong> 9 أكتوبر 2026","<strong>تاريخ مراجعة المواصفات:</strong> 9 أكتوبر 2026، والأسعار: 24 أكتوبر 2026")
        ]
    elif article:
        changes=[
            ("حسب القائمة السارية من 15 أكتوبر 2026","حسب القائمة المنشورة في 22 أكتوبر 2026"),
            ("آخر مراجعة تحريرية: 16 أكتوبر 2026","آخر مراجعة تحريرية: 24 أكتوبر 2026"),
            ("سجل تغييرات أسعار هيونداي في هتلاقي بتاريخ 15 أكتوبر 2026","سجل تغييرات أسعار هيونداي في هتلاقي بتاريخ 22 أكتوبر 2026"),
            ("تغطية قائمة جي بي أوتو اعتبارًا من 15 أكتوبر 2026","تغطية قائمة 15 أكتوبر السابقة وقائمة 22 أكتوبر الأحدث"),
            ("نعم، أظهر تحديث 15 أكتوبر زيادة قدرها 25,000 جنيه في سعر كل فئة مقارنة بالقائمة السابقة.","نعم، أظهر تحديث 15 أكتوبر زيادة قدرها 25,000 جنيه لكل فئة، ثم جاءت قائمة 22 أكتوبر بزيادة جديدة بلغت 50,000 جنيه لمعظم الفئات و40,000 جنيه لفئة Night بحسب المصادر المنشورة.")
        ]
    else:changes=[]
    for old,new in changes:
        content=content.replace(old,new)
        excerpt=excerpt.replace(old,new)
    return content,excerpt
def updated_seo_meta(old):
    desc=(old.get("meta") or {}).get("_yoast_wpseo_metadesc","")
    if not desc:return {}
    new=desc.replace("1.32 مليون","1.34 مليون").replace("1.8 مليون","1.85 مليون").replace("2.4 مليون","2.45 مليون")
    new=new.replace("1,320,000","1,340,000").replace("1,800,000","1,850,000").replace("2,400,000","2,450,000")
    return {"_yoast_wpseo_metadesc":new} if new!=desc else {}
def save_content(old,content,excerpt):
    seo=updated_seo_meta(old)
    if old["content"]==content and old["excerpt"]==excerpt and not seo:return
    body={"id":old["id"],"expected_modified_gmt":old["modified_gmt"],"content":content,"excerpt":excerpt}
    if seo:body["meta"]=seo
    # Do not retry an ambiguous write; verify afterward.
    api("/update-post",body)
    after=post(old["id"])
    if (after["slug"],after["status"],after["featured_media"]) != (old["slug"],old["status"],old["featured_media"]):
        raise RuntimeError("Post identity/media changed after update: "+old["slug"])
    if MARK not in after["content"]:raise RuntimeError("Price annotation not saved: "+old["slug"])
def correct_car(c):
    slug,old_min,old_max,new_min,new_max,prices=c
    row=model(slug);pid=row["id"];item=post(pid)
    if item["slug"]!=slug or item["type"]!="a3_car" or item["featured_media"]!=row["featured_media"]:raise RuntimeError("Unexpected car record: "+slug)
    current_min=meta(pid,"_a3_price_min");current_max=meta(pid,"_a3_price_max")
    oldmax={str(old_max),str(new_max),"0",""} if old_max is not None else {"0","",str(new_max),str(new_min)}
    if current_min not in {str(old_min),str(new_min)} or current_max not in oldmax:
        raise RuntimeError("Price drift: "+slug+" min="+current_min+" max="+current_max)
    content,excerpt=revise_text(slug,item["content"],item["excerpt"],prices)
    content,excerpt=tidy_text(slug,content,excerpt)
    save_content(item,content,excerpt)
    desired={"_a3_price_min":str(new_min),"_a3_price_max":str(new_max),"_a3_source_checked_at":"2026-10-24"}
    before={k:meta(pid,k) for k in desired}
    print("PRICE_META_BEFORE",slug,repr(before),flush=True)
    if any(before[k]!=v for k,v in desired.items()):
        ans=api("/admin",{"op":"post_meta_set","post_id":pid,"meta":desired,"confirm":True,"dangerous":True})
        print("PRICE_META_WRITE_RESPONSE",str(ans)[:500],flush=True)
    after={k:meta(pid,k) for k in desired}
    print("PRICE_META_AFTER",slug,repr(after),flush=True)
    if any(after[k]!=v for k,v in desired.items()):
        # Upsert uses the core-platform metadata writer; never alter content or media.
        result=api("/admin",{"op":"platform_entity_upsert","id":pid,"type":"a3_car",
                    "slug":slug,"title":item["title"],"status":"publish","meta":desired,
                    "confirm":True,"dangerous":True})
        print("CORE_ENTITY_META_WRITE_RESPONSE",str(result)[:450],flush=True)
        after={k:meta(pid,k) for k in desired}
        print("CORE_ENTITY_META_AFTER",slug,repr(after),flush=True)
    for k,v in desired.items():
        if after[k]!=v:raise RuntimeError("Meta verification failed "+slug+" "+k+" actual="+repr(after[k])+" expected="+repr(v))
    print("LIVE_CORRECTED_CAR",slug,row["link"],flush=True)
def correct_article():
    item=post(84008)
    if item["slug"]!="hyundai-tucson-2027-prices-egypt" or item["type"]!="post" or item["status"]!="publish" or not item["featured_media"]:
        raise RuntimeError("Tucson article mismatch")
    slug="hyundai-tucson-2027-egypt"
    content,excerpt=revise_text(slug,item["content"],item["excerpt"],CARS[0][-1],True)
    content,excerpt=tidy_text(slug,content,excerpt,article=True)
    save_content(item,content,excerpt)
    result=post(84008)
    if not all(v in result["content"] for v in (MARK,"1,850,000","2,450,000")):raise RuntimeError("Tucson article verification failed")
    print("LIVE_CORRECTED_ARTICLE",result["link"],flush=True)
def main():
    st=api("/status")
    if not st.get("ok"):raise RuntimeError("Bridge unavailable")
    for c in CARS:
        model(c[0])
    print("PREFLIGHT_VERIFIED three existing price records",flush=True)
    for c in CARS:correct_car(c)
    correct_article()
    print("A3TAL_OCTOBER_PRICES_CORRECTION_VERIFIED",flush=True)
if __name__=="__main__":main()
