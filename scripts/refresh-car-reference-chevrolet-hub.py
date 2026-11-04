#!/usr/bin/env python3
"""Update existing Chevrolet brand reference page to link Optra and Captiva.
Never change its permalink, published post ID, or featured media.
"""
import json,os,re,time
from pathlib import Path
import requests

SITE="https://a3tal.com"
S=requests.Session()
KEY=os.environ["A3TAL_API_KEY"]
BRAND=SITE+"/car-reference/chevrolet/"
OPTRA=SITE+"/car-reference/chevrolet/optra-2026-egypt/"
CAPTIVA=SITE+"/car-reference/chevrolet/captiva-2026-egypt/"
OUT=Path("car-reference-chevrolet-hub-update-proof.json")
BODY="""<p>يجمع دليل المواصفات الفنية لشيفروليه في أعطال.كوم بيانات السيارات من كتالوجات شيفروليه مصر الرسمية، مع الفصل بين الموديلات والأجيال. يضم أوبترا الجديدة 2026 وكابتيفا 2026، وتختلف السيارتان في المحرك ومساحات الركوب ومقاس الإطارات وتجهيزات الأمان.</p>
<h2>اختر موديل شيفروليه المطلوب</h2>
<p><a href="https://a3tal.com/car-reference/chevrolet/optra-2026-egypt/">دليل مواصفات أوبترا الجديدة 2026</a> يعرض محرك 1485 سم³ وناقل CVT وسعة الوقود والشنطة ووسائل الأمان لفئتي LS وLT. و<a href="https://a3tal.com/car-reference/chevrolet/captiva-2026-egypt/">دليل مواصفات كابتيفا 2026</a> يغطي محرك 1450 سم³ تيربو وناقل CVT ومقاس إطارات 215/55 R18، والفرق بين النسخ ذات 5 أو 7 مقاعد وتجهيزات الفرامل والوسائد.</p>
<h2>اختلافات الجيل والسوق عند شراء القطع</h2>
<p>أوبترا الجديدة ليست أوبترا القديمة، وكابتيفا 2026 ليست كابتيفا EV الكهربائية. لا تُنقل مواصفات أي موديل للآخر أو تُحدد كمية زيت الفتيس من اسم CVT وحده؛ يجب مطابقة رقم الشاسيه وكتيب السيارة والفئة والتجهيزات.</p>
<h2>ملاحظة مهمة بشأن سعة تانك كابتيفا</h2>
<p>تعرض نسختا الكتالوج الإنجليزي والعربي لشيفروليه كابتيفا قيمتين مختلفتين لسعة خزان الوقود، ولذلك لم نعتبر الرقم محسومًا. يحتاج المالك إلى التأكد من دليل سيارته أو الوكيل. ونحتفظ بمقالات الأسعار والمراجعة والأعطال في صفحاتها المستقلة حتى لا تتكرر نية البحث.</p>"""

def get(url,**kwargs):
    error=None
    for attempt in range(5):
        try:
            r=S.get(url,timeout=55,**kwargs)
            if r.status_code in (408,429,500,502,503,504,520,521,522,523,524):
                raise requests.RequestException("Transient HTTP "+str(r.status_code))
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            error=e
            if attempt<4:time.sleep((attempt+1)*4)
    raise RuntimeError("GET retry exhaustion "+url+" "+str(error))

def existing():
    r=get(SITE+"/wp-json/wp/v2/car-reference-records",params={"slug":"chevrolet","per_page":20})
    a=[x for x in r.json() if x.get("slug")=="chevrolet" and x.get("status")=="publish"]
    if len(a)!=1 or a[0]["link"].rstrip("/")!=BRAND.rstrip("/"):
        raise RuntimeError("Chevrolet brand page missing or slug collision")
    return a[0]

def main():
    old=existing()
    media=int(old.get("featured_media") or 0)
    if not media:raise RuntimeError("Existing Chevy featured image missing")
    for p in (OPTRA,CAPTIVA):
        if not get(p).ok:raise RuntimeError("Child page unavailable "+p)
    payload={
      "title":"دليل المواصفات الفنية لسيارات شيفروليه في مصر",
      "slug":"chevrolet","kind":"brand","parent_path":"",
      "status":"publish","allow_update_published":True,
      "featured_image_id":media,
      "content":BODY,
      "excerpt":"مواصفات شيفروليه أوبترا الجديدة وكابتيفا 2026 في مصر من كتالوجات الوكيل الرسمية.",
      "data":{"kind":"brand","market":"كتالوجات شيفروليه مصر 2026",
        "years":"2026","engine":"","category":"",
        "reviewed_at":"2026-11-04","facts":[],
        "sources":[
          {"title":"كتالوج شيفروليه أوبترا 2026","url":"https://www.chevroletarabia.com/content/dam/chevrolet/middle-east/egypt/english/index/cars/2026-optra/the-all-new-optra-2026-brochure.pdf"},
          {"title":"كتالوج كابتيفا 2026","url":"https://www.chevroletarabia.com/content/dam/chevrolet/middle-east/egypt/english/index/cars/2026-captiva/Captiva-brochure-2026.pdf"}]},
      "meta_title":"دليل مواصفات شيفروليه مصر: أوبترا وكابتيفا 2026 | أعطال.كوم",
      "meta_description":"مواصفات شيفروليه أوبترا وكابتيفا 2026 في مصر: المحركات والفتيس والكاوتش والأبعاد والوسائد من كتالوجات الشركة الرسمية."
    }
    r=S.post(SITE+"/wp-json/a3tal-car-reference/v1/upsert",
      json={"items":[payload]},headers={"X-A3tal-Key":os.environ["A3TAL_API_KEY"],"Content-Type":"application/json"},
      timeout=165)
    r.raise_for_status()
    result=r.json()
    values=result.get("results") or []
    if len(values)!=1 or not values[0].get("ok") or values[0].get("status")!="publish":
        raise RuntimeError("Hub upsert failed "+repr(result)[:500])
    for k in range(8):
        try:
            h=get(BRAND,params={"chevrolet_hub_qa":str(time.time_ns())},headers={"Cache-Control":"no-cache"}).text
            if "optra-2026-egypt" not in h or "captiva-2026-egypt" not in h:raise RuntimeError("linked child missing")
            if "noindex" in h[:15000].lower():raise RuntimeError("noindex")
            canon=re.findall(r'<link\b[^>]*rel=["\x27]canonical["\x27][^>]*>',h,re.I)
            if not canon or BRAND.rstrip("/") not in canon[0]:raise RuntimeError("bad canonical")
            if not re.search(r'<meta[^>]*property=["\x27]og:image["\x27]',h,re.I):raise RuntimeError("missing og:image")
            break
        except Exception:
            if k==7:raise
            time.sleep(4)
    now=existing()
    if int(now["id"])!=int(old["id"]) or int(now["featured_media"])!=media:
        raise RuntimeError("Brand image or post ID unexpectedly changed")
    report={"url":BRAND,"id":old["id"],"media_id":media,"linked":[OPTRA,CAPTIVA],
        "same_post_and_image":True,"verified":True}
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
    print("CHEVROLET HUB VERIFIED",json.dumps(report,ensure_ascii=False),flush=True)

if __name__=="__main__":main()
