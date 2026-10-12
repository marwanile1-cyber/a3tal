#!/usr/bin/env python3
"""Repair Mazda 3 2027 placement in all three homepage feeds via A3tal Direct Bridge."""
import os,json,time,hashlib,re,subprocess,tempfile
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

BASE="https://a3tal.com/wp-json/a3tal-direct/v1"
SECRET=os.environ.get("A3TAL_API_KEY","")
if not SECRET: raise RuntimeError("Missing GitHub A3TAL_API_KEY secret")

def call(path,data=None,retries=4):
    url=BASE+path
    headers={"X-A3tal-Key":SECRET,"Authorization":"Bearer "+SECRET,"User-Agent":"A3tal editorial home-feed repair/1.0"}
    body=json.dumps(data,ensure_ascii=False).encode("utf-8") if data is not None else None
    if body: headers["Content-Type"]="application/json"
    for n in range(retries):
        try:
            req=Request(url,data=body,headers=headers,method="POST" if body else "GET")
            with urlopen(req,timeout=150) as r: return json.load(r)
        except Exception as e:
            print("Bridge request failed",path.split("?")[0],n+1,str(e)[:230],flush=True)
            if n==retries-1: raise
            time.sleep(5*(n+1))

def public(url,attempts=4):
    for n in range(attempts):
        try:
            req=Request(url,headers={"User-Agent":"Mozilla/5.0 A3tal homepage QA","Cache-Control":"no-cache"})
            with urlopen(req,timeout=90) as r: return r.read().decode("utf-8","replace")
        except Exception as e:
            print("Public fetch retry",str(e)[:160],flush=True)
            if n==attempts-1: raise
            time.sleep(5*(n+1))

def admin_get(op,**kwargs):
    d={"op":op};d.update(kwargs)
    r=call("/admin?"+urlencode(d))
    if not r.get("ok"): raise RuntimeError("admin "+op+" failed: "+str(r)[:500])
    return r["result"]

def admin_post(op,**kwargs):
    d={"op":op};d.update(kwargs)
    r=call("/admin",d)
    if not r.get("ok"):raise RuntimeError("admin "+op+" failed: "+str(r)[:500])
    return r["result"]

def term_id(taxonomy,slug,create_name=None):
    terms=admin_get("terms",taxonomy=taxonomy,limit=500)
    matches=[x for x in terms if x.get("slug")==slug]
    if matches:return int(matches[0]["id"])
    if create_name:
        print("Creating missing term",taxonomy,slug,flush=True)
        response=admin_post("term_upsert",taxonomy=taxonomy,slug=slug,name=create_name)
        return int(response["term_id"])
    return None

def patch_home(live):
    content=live["content"]
    original=content
    carquery=re.compile(r"\$home_car_slugs\s*=\s*\[.*?\];\s*\$home_car_ids\s*=\s*\[\];.*?\$cars\s*=\s*new WP_Query\(\[.*?\]\);",re.S)
    recent_car="""$cars=new WP_Query([
  'post_type'=>'a3_car',
  'post_status'=>'publish',
  'posts_per_page'=>6,
  'orderby'=>'date',
  'order'=>'DESC',
  'ignore_sticky_posts'=>true,
  'no_found_rows'=>true,
]);"""
    if "$home_car_slugs=" in content:
        content,num=carquery.subn(recent_car,content)
        if num!=1:raise RuntimeError("Cannot safely locate unique hard-coded 6-car block")
    if "'posts_per_page'=>6" not in content or "'post_type'=>'a3_car'" not in content:
        raise RuntimeError("Car query is missing or unexpectedly different")
    price_old="$prices=a3g_query(['cat'=>374,'posts_per_page'=>4,'post__not_in'=>$hero_id?[$hero_id]:[]]);"
    price_new="$prices=a3g_query(['cat'=>374,'posts_per_page'=>4]);"
    news_old="$news=a3g_query(['posts_per_page'=>4,'post__not_in'=>$hero_id?[$hero_id]:[]]);"
    news_new="$news=a3g_query(['posts_per_page'=>4]);"
    for old,new,label in [(price_old,price_new,"price"),(news_old,news_new,"news")]:
        if old in content:
            content=content.replace(old,new,1)
            print("Patched",label,"newest entry exclusion",flush=True)
        elif new not in content:
            raise RuntimeError("Cannot safely locate "+label+" query; aborting")
    if content==original:
        print("Frontpage PHP already repaired; no file mutation required",flush=True)
        return content
    with tempfile.NamedTemporaryFile(suffix=".php",mode="w",encoding="utf-8") as tmp:
        tmp.write(content);tmp.flush()
        cp=subprocess.run(["php","-l",tmp.name],capture_output=True,text=True,check=True)
        print("PHP validation:",cp.stdout.strip(),flush=True)
    saved=admin_post("file_write",path="themes/a3tal-global/front-page.php",content=content,
        expected_sha256=live["sha256"],confirm=True,dangerous=True)
    expected=hashlib.sha256(content.encode("utf-8")).hexdigest()
    if saved.get("sha256")!=expected:raise RuntimeError("Live theme SHA mismatch")
    print("Live homepage theme patched:",saved["sha256"],flush=True)
    return content

def section_contains(html, heading,needle):
    # Each target is in its own HTML <section>; use the next closing </section> boundary.
    pos=html.find(heading)
    if pos<0: return False,"Heading not found"
    tail=html[pos:]
    end=tail.find("</section>")
    if end<0: return False,"Section closing tag missing"
    block=tail[:end]
    return needle in block,block[:750].replace("\n"," ")

def main():
    article=call("/post/83527")
    assert article["status"]=="publish" and 374 in article["categories"]
    assert article.get("featured_media")==83528
    print("Original article verified:",article["link"],flush=True)
    brand_id=term_id("a3_brand","mazda","Mazda")
    market_id=term_id("a3_market","egypt")
    sedan_id=term_id("a3_car_body","sedan")
    hatch_id=term_id("a3_car_body","hatchback")
    print("Taxonomy IDs",{"mazda":brand_id,"egypt":market_id,"sedan":sedan_id,"hatchback":hatch_id},flush=True)
    taxonomy={"a3_brand":[brand_id]}
    if market_id:taxonomy["a3_market"]=[market_id]
    bodies=[x for x in (sedan_id,hatch_id) if x]
    if bodies:taxonomy["a3_car_body"]=bodies
    source_link=article["link"]
    entity_html=(
      "<p>ملف مازدا 3 موديل 2027 في قاعدة السيارات بأعطال.كوم، ويجمع بين نسختي Highline سيدان وهاتشباك بأسعار"
      " 1,609,000 و1,619,000 جنيه على الترتيب وفق قائمة 12 أكتوبر 2026.</p>"
      '<p><strong>التفاصيل والمقارنة والفروق بين الفئتين:</strong> <a href="'+source_link+'">سعر مازدا 3 موديل 2027 في مصر والمواصفات وهل تستحق الشراء؟</a>.</p>'
      "<p>الأسعار مرجعية وقابلة للتغيير. راجع الوكيل قبل الحجز، ولا تعتمد على أي تجهيز غير مثبت في القائمة المحلية.</p>"
    )
    entity={
      "type":"a3_car","slug":"mazda-3-2027-egypt","title":"مازدا 3 موديل 2027 في مصر",
      "status":"publish","featured_media":83528,
      "excerpt":"مازدا 3 موديل 2027 في مصر: سيدان Highline بسعر 1,609,000 جنيه وهاتشباك Highline بسعر 1,619,000 جنيه بعد زيادة 20 ألف جنيه.",
      "content":entity_html,"taxonomies":taxonomy,
      "meta":{
        "_a3_year":2027,"_a3_price_min":1609000,"_a3_price_max":1619000,
        "_a3_currency":"EGP","_a3_engine_cc":1500,
        "_a3_transmission":"أوتوماتيك SKYACTIV","_a3_fuel":"بنزين",
        "_a3_source_url":"https://almalnews.com/2140654/",
        "_a3_source_checked_at":"2026-10-12",
        "_a3_related_post_ids":"83527",
        "_yoast_wpseo_meta-robots-noindex":"1"
      }
    }
    saved=admin_post("platform_entity_upsert",**entity)
    eid=int(saved["id"])
    print("VEHICLE ENTITY:",json.dumps(saved,ensure_ascii=False),flush=True)
    assert saved.get("featured_media")==83528 and saved.get("slug")=="mazda-3-2027-egypt"
    admin_post("post_meta_set",post_id=83527,meta={"_a3_vehicle_entity_id":eid})
    print("Article linked to structured vehicle",eid,flush=True)

    live=admin_get("file_read",path="themes/a3tal-global/front-page.php")
    print("Live frontpage SHA before:",live["sha256"],"size",live["size"],flush=True)
    patch_home(live)
    clean=admin_post("cache_flush")
    print("Cleared caches:",json.dumps(clean,ensure_ascii=False),flush=True)

    # Verify all three target blocks independently on the public homepage.
    targets=[
      ("سيارات مضافة حديثًا","mazda-3-2027-egypt"),
      ("أحدث أسعار السيارات","mazda-3-2027-egypt-price-specs"),
      ("آخر الأخبار والترند","mazda-3-2027-egypt-price-specs")
    ]
    for n in range(5):
        h=public("https://a3tal.com/?mazda_home_verify="+str(int(time.time()))+"-"+str(n))
        results={title:section_contains(h,title,marker)[0] for title,marker in targets}
        print("HOME QA",n+1,json.dumps(results,ensure_ascii=False),flush=True)
        if all(results.values()):break
        time.sleep(8)
    else:
        for title,marker in targets:
            good,snip=section_contains(h,title,marker)
            print("MISS",title,snip[:700],flush=True)
        raise RuntimeError("At least one of three homepage sections did not show Mazda after cache flush")
    # Extra: plain homepage response. CDNs may serve stale unbusted HTML.
    try:
        plain=public("https://a3tal.com/")
        print("PLAIN HOMEPAGE",json.dumps({title:section_contains(plain,title,marker)[0] for title,marker in targets},ensure_ascii=False),flush=True)
    except Exception as e:
        print("Plain homepage request warning:",str(e)[:250],flush=True)
    car_url=saved.get("link")
    if not car_url:car_url="https://a3tal.com/cars/mazda-3-2027-egypt/"
    print("SUCCESS: Article:",source_link,"Vehicle:",car_url,"and 3/3 homepage blocks confirmed.",flush=True)
if __name__=="__main__":main()
