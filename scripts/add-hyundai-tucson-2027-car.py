#!/usr/bin/env python3
"""One-time reviewed Tucson 2027 model hub via A3tal Direct Bridge.
Keeps indexed price news canonical; vehicle detail lives in the model encyclopedia.
"""
import json, os, time, urllib.parse, urllib.request, urllib.error

BASE="https://a3tal.com"
KEY=os.getenv("A3TAL_API_KEY","")
SLUG="hyundai-tucson-2027-egypt"
ARTICLE_ID=84008
IMAGE_ID=84009
RELATED="84008,80735,80738,80741,80752,80744,80749"
if not KEY:
    raise SystemExit("A3TAL_API_KEY secret not configured")

def request(url, payload=None, secure=False):
    headers={"User-Agent":"A3tal-Reviewed-Car-Editor/1.0",
             "Accept":"application/json","Cache-Control":"no-cache"}
    data=None
    if secure:
        headers["X-A3tal-Key"]=KEY
        headers["Authorization"]="Bearer "+KEY
    if payload is not None:
        data=json.dumps(payload,ensure_ascii=False).encode("utf-8")
        headers["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request(url,data=data,headers=headers)
    with urllib.request.urlopen(req,timeout=90) as response:
        return json.load(response)

def car_list(**params):
    params["per_page"]=40
    url=BASE+"/wp-json/wp/v2/a3tal-cars?"+urllib.parse.urlencode(params)
    result=request(url)
    if not isinstance(result,list):
        raise RuntimeError("Could not verify car index")
    return result

def main():
    post=request(BASE+f"/wp-json/wp/v2/posts/{ARTICLE_ID}?_fields=id,slug,status,link,featured_media,categories")
    if post.get("slug")!="hyundai-tucson-2027-prices-egypt" or post.get("status")!="publish":
        raise RuntimeError("Canonical published price article missing")
    if int(post.get("featured_media") or 0)!=IMAGE_ID or 374 not in post.get("categories",[]):
        raise RuntimeError("Article image or price category changed")
    image=request(BASE+f"/wp-json/wp/v2/media/{IMAGE_ID}?_fields=id,mime_type,source_url")
    if image.get("mime_type")!="image/webp":
        raise RuntimeError("Expected featured WebP media not verified")
    exact=car_list(slug=SLUG)
    english=car_list(search="tucson")
    arabic=car_list(search="توسان")
    possible={int(x["id"]):x for x in english+arabic}
    if len(exact)>1 or any(x.get("slug")!=SLUG for x in possible.values()):
        raise RuntimeError("Potential duplicate Tucson model in encyclopedia; refusing upsert")
    if len(exact)==1:
        car=exact[0]
        if car.get("status")!="publish" or int(car.get("featured_media") or 0)!=IMAGE_ID:
            raise RuntimeError("Existing model requires separate review")
        print("SUCCESS: Exact Tucson model already published",car["id"],car["link"],flush=True)
        return
    content="""<p>هيونداي توسان موديل 2027 في مصر سيارة SUV عائلية، وتتوفر بحسب قائمة الأسعار التي بدأ العمل بها في 15 أكتوبر 2026 في سبع فئات بأسعار تبدأ من 1,800,000 جنيه وتصل إلى 2,400,000 جنيه. هذه صفحة الموديل داخل موسوعة أعطال.كوم، ويظل مقال السعر المفصل هو مرجع المقارنة الأساسي لتجنب تكرار نية البحث.</p>
<h2>أسعار فئات هيونداي توسان 2027</h2>
<div style="overflow-x:auto"><table><thead><tr><th>الفئة</th><th>السعر المعلن</th></tr></thead><tbody>
<tr><td>Shadow</td><td>1,800,000 جنيه</td></tr>
<tr><td>Blaze</td><td>1,950,000 جنيه</td></tr>
<tr><td>Redline</td><td>2,050,000 جنيه</td></tr>
<tr><td>Redline N Pack</td><td>2,125,000 جنيه</td></tr>
<tr><td>Night</td><td>2,200,000 جنيه</td></tr>
<tr><td>Black Diamond</td><td>2,300,000 جنيه</td></tr>
<tr><td>N Line AWD</td><td>2,400,000 جنيه</td></tr>
</tbody></table></div>
<p><strong>التفاصيل الكاملة:</strong> <a href="https://a3tal.com/hyundai-tucson-2027-prices-egypt/">سعر هيونداي توسان 2027 والفروق بين الفئات ونصائح الشراء</a>. الأسعار قابلة للتغير لدى الوكيل؛ راجع السعر النهائي والتجهيزات كتابةً قبل الحجز.</p>
<h2>المحرك والفتيس والأعطال المرتبطة بتوسان</h2>
<p>توثق مواد توسان NX4 المصرية محرك Smartstream 1.6 Turbo GDI بقوة 180 حصانًا وعزم 265 نيوتن متر مع ناقل حركة 7DCT، مع اختلاف منظومة الجر حسب الفئة. يلزم مطابقة مواصفات سنة الموديل والفئة مع الوكيل قبل الشراء أو تطبيق توصية صيانة.</p>
<ul>
<li><a href="https://a3tal.com/hyundai-tucson-nx4-engine-problems-smartstream/">دليل محرك توسان NX4: التيربو والكربون وLSPI</a></li>
<li><a href="https://a3tal.com/hyundai-tucson-nx4-transmission-problems-dct/">دليل فتيس توسان DCT: النتشة والسخونة</a></li>
<li><a href="https://a3tal.com/hyundai-tucson-nx4-suspension-steering-problems/">العفشة والدركسيون وأسباب الطقطقة</a></li>
<li><a href="https://a3tal.com/hyundai-tucson-nx4-fault-codes-dtc-dictionary/">أكواد أعطال توسان NX4</a></li>
<li><a href="https://a3tal.com/hyundai-tucson-nx4-electrical-screen-battery-problems/">الكهرباء والشاشات والبطارية</a></li>
<li><a href="https://a3tal.com/used-hyundai-tucson-prices-egypt-2026/">دليل أسعار توسان المستعملة حسب الجيل</a></li>
</ul><p><small>مراجعة بيانات الأسعار: 16 أكتوبر 2026. مرجع الأسعار التفصيلي: <a href="https://eg.hatla2ee.com/ar/new-car/price-change/hyundai">سجل تغيرات أسعار هيونداي لدى هتلاقي</a>. الصورة البارزة تصميم بصري توضيحي حصري وليست صورة وثائقية لفئة محددة.</small></p>"""
    payload={
      "op":"platform_entity_upsert","type":"a3_car","slug":SLUG,
      "title":"هيونداي توسان 2027 في مصر","status":"publish",
      "content":content,
      "excerpt":"هيونداي توسان 2027 في مصر: سبع فئات من 1.8 إلى 2.4 مليون جنيه، مع المواصفات وروابط المحرك والفتيس والعفشة وأكواد الأعطال.",
      "featured_media":IMAGE_ID,
      "taxonomies":{"a3_brand":["hyundai"],"a3_market":["egypt"],"a3_car_body":["suv"]},
      "meta":{
        "_a3_year":"2027","_a3_price_min":"1800000","_a3_price_max":"2400000","_a3_currency":"EGP",
        "_a3_engine_cc":"1598","_a3_power_hp":"180","_a3_torque_nm":"265",
        "_a3_transmission":"7DCT","_a3_fuel":"بنزين","_a3_drivetrain":"أمامي أو AWD حسب الفئة",
        "_a3_seats":"5",
        "_a3_source_url":"https://a3tal.com/hyundai-tucson-2027-prices-egypt/",
        "_a3_source_checked_at":"2026-10-16",
        "_a3_related_post_ids":RELATED
      }
    }
    print("Preflight succeeded: no competing Tucson model record",flush=True)
    try:
        response=request(BASE+"/wp-json/a3tal-direct/v1/admin",payload,secure=True)
        if not response.get("ok"): raise RuntimeError("Bridge returned non-success")
        print("Bridge entity upsert returned:",response.get("result",{}).get("id"),flush=True)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as e:
        print("Write response interrupted; verifying exact-slug state without repeating write:",type(e).__name__,flush=True)
    time.sleep(20)
    items=car_list(slug=SLUG)
    if len(items)!=1 or items[0].get("status")!="publish":
        raise RuntimeError("No verified published model record after Bridge write")
    car=items[0]
    if int(car.get("featured_media") or 0)!=IMAGE_ID:
        raise RuntimeError("Car entity did not receive expected featured WebP")
    print("SUCCESS: Tucson 2027 encyclopedia entity",car["id"],car.get("link"),"related article",ARTICLE_ID,flush=True)

if __name__=="__main__":
    main()
