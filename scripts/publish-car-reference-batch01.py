#!/usr/bin/env python3
"""Publish only manually curated Kia service specifications through A3tal Direct Bridge.
No invented specs. No overwrite of existing published records. Idempotent URL checks.
"""
import os, io, json, time, base64, hashlib
from pathlib import Path
from urllib.parse import quote
import requests
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/car-reference/batch-01-kia-verified-2026-11-02.json"
BASE="https://a3tal.com"
KEY=os.environ["A3TAL_API_KEY"].strip()
SESSION=requests.Session()
SESSION.headers.update({"User-Agent":"A3tal-Car-Reference-Publisher/1.0"})
API=BASE+"/wp-json/a3tal-car-reference/v1/upsert"
MEDIA=BASE+"/wp-json/a3tal-direct/v1/upload-image-data"
HEADERS={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
OUT=ROOT/"car-reference-batch01-results.json"
RESULTS=[]
def safe_get(url):
    try:
        r=SESSION.get(url,timeout=35,headers={"Cache-Control":"no-cache"})
        return r if r.status_code==200 else None
    except requests.RequestException:
        return None

def already_live(path):
    r=safe_get(BASE+"/car-reference/"+path.strip("/")+"/")
    return bool(r is not None and "a3cr-article" in r.text)

def req(url,obj):
    for attempt in range(4):
        try:
            r=SESSION.post(url,headers=HEADERS,json=obj,timeout=120)
            payload=r.json()
            if r.status_code>=500:
                raise RuntimeError("HTTP "+str(r.status_code))
            if r.status_code>=400:
                raise RuntimeError("HTTP "+str(r.status_code)+" "+str(payload.get("message") or payload.get("code"))[:200])
            return payload
        except (requests.RequestException,ValueError,RuntimeError) as exc:
            if attempt==3: raise RuntimeError(f"POST failed: {str(exc)[:220]}")
            time.sleep(3*(attempt+1))

def font(size,bold=False):
    paths=(["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    return ImageFont.truetype(paths[0],size)

def artwork(label,sub,hero,key,kind):
    """Original per-record automotive technical illustration. Never a borrowed product image."""
    im=Image.new("RGB",(1200,675))
    d=ImageDraw.Draw(im)
    h=int(hashlib.sha256(key.encode()).hexdigest()[:8],16)
    palette=[(34,146,204),(28,174,143),(224,120,70),(141,125,232),(82,175,210)]
    accent=palette[h%len(palette)]
    for y in range(675):
        c=(max(4,10+y//65),max(13,26+y//40),max(27,44+y//28))
        d.line((0,y,1200,y),fill=c)
    for i in range(15):
        x=80+i*76
        d.line((x,60,x,650),fill=(21,43,64),width=1)
    for i in range(8):
        y=90+i*76
        d.line((35,y,1160,y),fill=(21,43,64),width=1)
    d.rounded_rectangle((50,45,1150,630),radius=35,outline=(54,93,118),width=3)
    d.rectangle((50,45,62,630),fill=accent)
    # Stylised original car / engine-component diagram, deliberately illustrative.
    d.rounded_rectangle((650,245,1065,522),radius=36,outline=(102,141,157),width=5)
    d.rounded_rectangle((690,285,1025,470),radius=24,outline=accent,width=7)
    for j in range(4):
        x=720+j*75
        d.rounded_rectangle((x,320,x+42,404),radius=10,outline=(187,210,217),width=5)
    for j in range(7):
        d.line((697+j*50,266,719+j*50,247),fill=accent,width=4)
    d.ellipse((795,485,907,589),outline=accent,width=10)
    d.ellipse((824,514,877,561),outline=(200,222,224),width=4)
    d.text((100,94),"A3TAL   /   CAR REFERENCE",font=font(22,True),fill=(203,224,231))
    d.text((100,158),label[:32],font=font(42,True),fill=(249,251,252))
    d.text((100,218),sub[:40],font=font(28),fill=(159,193,208))
    d.rounded_rectangle((100,335,615,470),radius=24,fill=(18,53,74),outline=accent,width=2)
    d.text((126,364),hero[:20],font=font(55,True),fill=(245,248,249))
    d.text((100,549),kind.upper()+"  /  OWNER MANUAL VERIFIED",font=font(19,True),fill=(183,203,214))
    out=io.BytesIO()
    im.save(out,format="WEBP",quality=86,method=5)
    return out.getvalue()

def create_image(path,title,subtitle,primary,kind):
    raw=artwork(title,subtitle,primary,path,kind)
    payload={"image_base64":base64.b64encode(raw).decode("ascii"),
       "filename":"a3tal-reference-"+path.replace("/","-")+".webp",
       "title":title,"alt":"رسم فني حصري لدليل مواصفات "+title,
       "convert_webp":False}
    reply=req(MEDIA,payload)
    image_id=int(reply.get("media_id",0))
    if not image_id: raise RuntimeError("Image upload did not return media_id for "+path)
    return image_id,reply.get("url","")

def html_content(record,model=None):
    kind=record["kind"]
    if kind=="brand":
        return ("<p>يجمع دليل كيا على أعطال.كوم بيانات الصيانة الفنية القابلة للتحقق من أدلة المالك الرسمية، مع فصل كل جيل ومحرك وناقل حركة عن غيره. "
         "الهدف معرفة السعات والمواصفات قبل شراء الزيت أو بدء الصيانة، وليس استبدال كتالوج السيارة.</p>"
         "<h2>طريقة استخدام الدليل</h2><p>اختر الموديل ورمز الجيل أولًا، ثم اختر محرك السيارة ونوع ناقل الحركة. "
         "تحتوي الصفحات الفرعية على قيم موثقة مرتبطة بسنة إصدار محددة للدليل وعلى رابط المصدر الأصلي.</p>"
         "<h2>اختلاف الأسواق</h2><p>تذكر بعض أدلة كيا لزوجة مختلفة لمصر والشرق الأوسط عن الأسواق الأخرى. "
         "لذلك لا يجوز تعميم توصية دولة على سيارة أخرى بدون مطابقة كود المحرك وسنة الصنع.</p>")
    if kind=="model":
        return ("<p>هذه صفحة تجميع للمواصفات الفنية الخاصة بـ"+record["title"]+"، اعتمادًا على دليل المالك الرسمي لسنة 2023. "
          "الاختلاف بين الفئات والمحركات قد يغير كمية زيت المحرك، ونوع زيت ناقل الحركة، وسعة التبريد حتى داخل الجيل نفسه.</p>"
          "<h2>اختيار النسخة الصحيحة</h2><p>"+model["safety"]+
          " يتم عرض الملفات الفرعية حسب نوع المحرك أو الفتيس حتى لا تتحول المقارنة إلى جدول واحد مضلل.</p>"
          "<h2>قبل تغيير السوائل</h2><p>راجع ملصق السيارة، ورمز المحرك، ودليل المالك المرفق مع السيارة. "
          "وجود وصف «مصر والشرق الأوسط» في بعض الصفحات يخص المواصفة الواردة صراحة في دليل كيا، وليس ضمان توافر كل نسخة محرك في السوق المحلي.</p>")
    cat=record["category"]
    intro={
    "engine-oil":"توضح هذه البطاقة سعة الزيت الواردة في دليل المالك عند التفريغ وإعادة التعبئة، مع تمييز درجة اللزوجة عن مستوى الجودة. لا تعتمد على اسم السيارة وحده لأن سعات المحركات تختلف.",
    "transmission-oil":"تخص الأرقام نوع ناقل الحركة المذكور في البطاقة، ولا يجوز استخدام سائل فتيس أوتوماتيك تقليدي في ناقل DCT أو IVT لمجرد تقارب السعات.",
    "coolant":"سعة دورة التبريد المذكورة هي سعة النظام في دليل المالك وليست بالضرورة كمية السائل التي ستخرج أثناء التفريغ الجزئي. لا تفتح الغطاء والمحرك ساخن.",
    "fuel":"تخص السعة خزان الوقود المحدد في دليل المالك. مقدار التعبئة الفعلي يتأثر بالكمية المتبقية في الخزان وبموعد فصل مسدس محطة الوقود."
    }[cat]
    facts=record["facts"]
    details="؛ ".join(x[0]+" "+x[1] for x in facts)
    return ("<p>هذه المعلومات خاصة بـ"+model["name"]+"، مع "+record["engine"]+"، كما يرد في نسخة دليل المالك لسنة 2023. "+intro+"</p>"
      "<h2>البيانات المعتمدة ومجال استخدامها</h2><p>"+details+
      ". هذه القيم مطابقة لصف نوع المحرك/ناقل الحركة المشار إليه ولا تعني أن جميع فئات السيارة لها نفس المواصفات.</p>"
      "<h2>كيف تتأكد قبل الصيانة؟</h2><p>طابق كود المحرك على السيارة ونوع الفتيس وسنة الطراز مع بيانات الدليل، ثم تحقق من تصنيف السائل واللزوجة إن وجدا. "
      "السعة الإجمالية لا تساوي دائمًا كمية التعبئة في تغيير جزئي. استخدم إجراءات القياس أو الملء المذكورة في دليل المالك، وارجع للمركز المختص عند اختلاف التجهيزات.</p>"
      "<h2>ملاحظة عن السوق المصري</h2><p>عندما يذكر الدليل مصر والشرق الأوسط بالاسم تُعرض المواصفة المخصصة لهما. "
      "أما المحركات أو نواقل الحركة غير المطروحة محليًا، فالبيانات مرجع تقني للنسخة المحددة فقط ولا تُنسب تلقائيًا لكل سيارة مصرية.</p>")

def publish(record,model,kind,path):
    if already_live(path):
        print("SKIP existing published",path,flush=True)
        RESULTS.append({"path":path,"status":"already-published"})
        return
    facts=record.get("facts",[])
    primary=(facts[0][1] if facts else ("2023" if kind=="model" else "KIA"))
    sub=(record.get("engine") or ("OWNER'S MANUAL" if kind=="brand" else model["family"]))
    img_id,img_url=create_image(path,("KIA 2023 "+ (model["family"].upper() if model else "REFERENCE")),sub,primary,kind)
    data={"market":"دليل كيا العالمي؛ مواصفات مصر والشرق الأوسط حيث وردت","years":"2023" if kind!="brand" else "عدة إصدارات","engine":record.get("engine",""),
      "category":record.get("category",""),"reviewed_at":"2026-11-02",
      "facts":[{"label":a,"value":b} for a,b in facts],
      "sources":[{"title":("دليل المالك الرسمي لكيا "+model["family"]+" 2023" if model else "الموقع الرسمي لدليل مالك كيا"),"url":model["ref"] if model else "https://ownersmanual.kia.com/"}]}
    entry={"title":record["title"],"slug":record["slug"],"kind":kind,"parent_path":record.get("parent_path",""),
       "status":"publish","featured_image_id":img_id,"data":data,"content":html_content(record,model),
       "excerpt":"مواصفات فنية موثقة من دليل مالك كيا؛ اختر المحرك والناقل الصحيحين قبل الصيانة.",
       "meta_title":record["title"]+" | دليل أعطال.كوم",
       "meta_description":"تفاصيل "+record["title"]+" بالمواصفات الرسمية، مع السعة والمصدر الأصلي وتحذيرات مطابقة كود المحرك والسوق."}
    response=req(API,{"items":[entry]})
    values=response.get("results") or []
    if not values or not values[0].get("ok"):
        raise RuntimeError("upsert rejected "+path+": "+str(values)[:250])
    live_url=values[0]["url"]
    checks=None
    for i in range(3):
        checks=safe_get(live_url)
        if checks is not None:break
        time.sleep(3)
    if checks is None or record["title"] not in checks.text:
        raise RuntimeError("Live verification failed: "+live_url)
    if "og:image" not in checks.text.lower():
        print("WARN missing og:image in "+live_url,flush=True)
    if "noindex" in checks.text[:12000].lower():
        print("WARN inspect noindex in "+live_url,flush=True)
    print("PUBLISHED",live_url,"image",img_id,flush=True)
    RESULTS.append({"path":path,"url":live_url,"status":"published","image":img_url})

def main():
    spec=json.loads(DATA.read_text(encoding="utf-8"))
    print("Preflight: 30 curated records / verified manufacturer references",flush=True)
    all_models={m["slug"]:m for m in spec["models"]}
    assert len(spec["specs"])+len(all_models)+1==30
    work=[]
    brand={**spec["brand"],"kind":"brand","parent_path":""}
    work.append((brand,None,"brand",brand["slug"]))
    for m in spec["models"]:
        rec={"title":m["name"],"slug":m["slug"],"kind":"model","parent_path":"kia",
           "facts":[["سنة نسخة دليل المالك","2023"],["الجيل"," ".join(m["slug"].split("-")[:-1])]]}
        work.append((rec,m,"model","kia/"+m["slug"]))
    for s in spec["specs"]:
        m=all_models[s["model"]]
        rec={**s,"kind":"spec","parent_path":"kia/"+m["slug"]}
        work.append((rec,m,"spec","kia/"+m["slug"]+"/"+s["slug"]))
    assert len({p for _,_,_,p in work})==30
    limit=max(1,min(30,int(os.environ.get("A3CR_LIMIT","30"))))
    work=work[:limit]
    print("Deployment limit:",limit,flush=True)
    try:
        for rec,model,kind,path in work:
            publish(rec,model,kind,path)
    finally:
        OUT.write_text(json.dumps({"results":RESULTS},ensure_ascii=False,indent=2),encoding="utf-8")
        print("Report saved:",OUT.name,"count",len(RESULTS),flush=True)

if __name__=="__main__":main()
