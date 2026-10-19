#!/usr/bin/env python3
"""Create ten distinct original diagnostic-process infographics and attach inline.
Art is an editorial decision-flow illustration, explicitly NOT an OEM wiring diagram.
Use A3tal Direct Bridge only. Existing hero, Yoast, taxonomy, slug and URL remain untouched.
"""
import os,io,re,json,time,base64,hashlib,urllib.request,urllib.parse,html
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display

BASE="https://a3tal.com"
API=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY")
if not KEY:raise RuntimeError("A3TAL_API_KEY missing")
ROSTER=[
 (80830,"hyundai-matrix-electrical-ac-interior-problems","تشخيص تكييف وكهرباء ماتريكس",["تمييز الهواء عن التبريد","فحص الضغط والمراوح","اختبار جهد وتوصيلات","تأكيد نتيجة التبريد"],"شحن الغاز ليس إصلاحًا للتسريب"),
 (80776,"chery-tiggo-8-pro-engine-gearbox-problems-acteco","تشخيص محرك و7DCT تيجو 8",["قراءة أكواد المحرك","اختبار الضغط والبوست","مقارنة TCM والحرارة","فحص ما بعد الإصلاح"],"لا تعمم ضعف السحب على التيربو"),
 (80764,"toyota-corolla-electrical-hybrid-screen-problems","تمييز كهرباء كورولا والهايبرد",["تحديد بنزين أم Hybrid","اختبار الشاشة و12V","فحص TPMS أو نظام الجر","تأكيد السبب بأداة مناسبة"],"لا تلمس دائرة الجهد العالي دون تأهيل"),
 (80681,"mg-5-suspension-steering-rack-problems","تشخيص طقطقة دركسيون MG5",["تحديد نوع الصوت","اختبار خلوص المفاصل","قياس جهد وأكواد EPS","إعادة فحص الزوايا"],"لا تغير Rack من الصوت وحده"),
 (80741,"hyundai-tucson-nx4-suspension-steering-problems","فحص دركسيون توسان NX4",["تمييز ميكانيكا عن EPS","فحص المفاصل والضغط","اختبار جهد ووحدة MDPS","تأكيد التوجيه والزوايا"],"لا تعمم عيب Coupling قديم على NX4"),
]
MARKERS={
 80830:"A3TAL-EDITORIAL-B7-MATRIX-AC-20261019",
 80776:"A3TAL-EDITORIAL-B7-TIGGO-ENGINE-20261019",
 80764:"A3TAL-EDITORIAL-B7-COROLLA-HYBRID-20261019",
 80681:"A3TAL-EDITORIAL-B7-MG5-SUSP-20261019",
 80741:"A3TAL-EDITORIAL-B7-TUCSON-SUSP-20261019",
}
FILENAME="a3tal-original-diagnostic-flow-b7-{id}-20261019.webp"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
HEADERS={"User-Agent":"A3tal-Editorial-Original-Diagrams/1.0","Accept":"application/json","Cache-Control":"no-store"}
last_bridge=0.0
def ar(s):return get_display(arabic_reshaper.reshape(s))
def font(n):return ImageFont.truetype(FONT,n)
def widths(text,f,d):return d.textbbox((0,0),ar(text),font=f)[2]
def centered(d,xy,t,f,fill):
    x,y=xy;z=ar(t);l=d.textbbox((0,0),z,font=f)[2]
    d.text((x-l/2,y),z,font=f,fill=fill)
def get(url,auth=False):
    h=dict(HEADERS)
    if auth:h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    req=urllib.request.Request(url,headers=h)
    with urllib.request.urlopen(req,timeout=75) as r:return json.load(r)
def write(endpoint,payload):
    global last_bridge
    time.sleep(max(0,13-(time.monotonic()-last_bridge)))
    last_bridge=time.monotonic()
    h=dict(HEADERS)
    h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    req=urllib.request.Request(API+endpoint,data=json.dumps(payload,ensure_ascii=False).encode(),headers=h)
    with urllib.request.urlopen(req,timeout=150) as r:return json.load(r)
def draw_diagram(pid,title,labels,warning):
    w,h=1600,900
    palette=[("#0a2234","#38c8c7"),("#17344a","#e0b66e"),("#112a43","#82b7ef"),
             ("#18394b","#83c9ba"),("#183047","#e7bd7a")]
    base_color,accent=palette[pid%len(palette)]
    im=Image.new("RGB",(w,h),base_color)
    d=ImageDraw.Draw(im)
    # Professional, original editorial vector diagram: avoid any simulated OEM schematics.
    for y in range(h):
        a=y/h
        col=(int(13+14*a),int(39+13*a),int(55+15*a))
        d.line((0,y,w,y),fill=col)
    for k in range(1,16):d.line((k*100,0,k*100,h),fill="#264558",width=1)
    for k in range(1,9):d.line((0,k*100,w,k*100),fill="#264558",width=1)
    d.rounded_rectangle((82,80,1518,220),radius=28,fill="#203f52",outline="#426b78",width=3)
    title_f=font(49)
    while widths(title,title_f,d)>1300 and title_f.size>35:title_f=font(title_f.size-2)
    centered(d,(800,111),title,title_f,"#eff8fa")
    centered(d,(800,240),"رسم توضيحي لمسار التشخيص خطوة بخطوة",font(27),"#b0d2dc")
    xs=[1290,910,530,150];cw=300
    for i,label in enumerate(labels):
        x=xs[i];y=337
        d.rounded_rectangle((x-8,y+10,x+cw+8,663),radius=29,fill="#102838")
        d.rounded_rectangle((x,y,x+cw,649),radius=25,fill="#25495a",outline=accent,width=5)
        d.rounded_rectangle((x+95,y+32,x+205,y+90),radius=22,fill=accent)
        d.text((x+130,y+41),f"{i+1:02d}",font=font(31),fill="#0d2837")
        # two-line Arabic text that fits card
        if len(label)>24:
            words=label.split();line1=" ".join(words[:(len(words)+1)//2]);line2=" ".join(words[(len(words)+1)//2:])
            ls=[line1,line2]
        else:ls=[label]
        fy=y+145
        for ln in ls:
            f=font(28)
            while widths(ln,f,d)>cw-38 and f.size>22:f=font(f.size-1)
            centered(d,(x+cw/2,fy),ln,f,"#ffffff");fy+=49
        if i<3:
            ax=x-40;ay=497
            d.line((ax+26,ay,ax-40,ay),fill=accent,width=8)
            d.polygon([(ax-43,ay),(ax-15,ay-16),(ax-15,ay+16)],fill=accent)
    d.rounded_rectangle((120,729,1480,808),radius=22,fill="#254556",outline="#457387",width=2)
    fw=font(27)
    while widths(warning,fw,d)>1270 and fw.size>20:fw=font(fw.size-1)
    centered(d,(800,748),warning,fw,"#f3e9d9")
    centered(d,(800,837),"أعطال.كوم | توضيح تعليمي لا يمثل مخطط توصيل أو إجراء خدمة معتمد",font(20),"#b1cbd2")
    o=io.BytesIO();im.save(o,"WEBP",quality=86,method=6)
    raw=o.getvalue()
    if not 20_000<len(raw)<450_000:raise RuntimeError("Unreasonable original WebP "+str((pid,len(raw))))
    return raw
def read_post(pid):
    p=get(API+"/post/"+str(pid),auth=True)
    if p.get("id")!=pid or p.get("status")!="publish" or p.get("type")!="post":
        raise RuntimeError("Unexpected post identity "+str(pid))
    return p
def media_name(pid):return FILENAME.format(id=pid)
def find_media(pid):
    stem=media_name(pid).rsplit(".",1)[0]
    q=urllib.parse.urlencode({"search":stem,"per_page":20,"_fields":"id,source_url,mime_type"})
    a=get(BASE+"/wp-json/wp/v2/media?"+q)
    matches=[v for v in a if stem in v.get("source_url","") and v.get("mime_type")=="image/webp"]
    if len(matches)>1:raise RuntimeError("Ambiguous media candidates "+stem)
    return matches[0] if matches else None
def verify_public(slug,filename):
    q="?visual_qa=20261019"+str(int(time.time()))
    with urllib.request.urlopen(urllib.request.Request(BASE+"/"+slug+"/"+q,headers={"User-Agent":"Mozilla/5.0","Cache-Control":"no-cache"}),timeout=70) as r:s=r.read().decode("utf-8","replace")
    if filename not in s or "<figure" not in s:raise RuntimeError("Missing rendered inline image "+slug)
    if "og:image" not in s:raise RuntimeError("Featured OG changed "+slug)
def main():
    preflight=[]
    for pid,slug,title,labels,warning in ROSTER:
        p=read_post(pid)
        if p.get("slug")!=slug or not p.get("featured_media"):raise RuntimeError("Wrong slug or missing hero "+slug)
        if MARKERS[pid] not in p.get("content",""):raise RuntimeError("Editorial article not ready "+slug)
        if not p.get("modified_gmt"):raise RuntimeError("Missing modified timestamp "+slug)
        preflight.append((pid,slug,title,labels,warning,p))
    print("BATCH07_ORIGINAL_IMAGE_PREFLIGHT_PASS",len(preflight),flush=True)
    for pid,slug,title,labels,warning,p in preflight:
        filename=media_name(pid)
        if filename in p.get("content",""):
            verify_public(slug,filename);print("IMAGE_ALREADY_INLINE",slug,flush=True);continue
        media=find_media(pid)
        if not media:
            raw=draw_diagram(pid,title,labels,warning)
            payload={"post_id":pid,"filename":filename,"title":"مسار تشخيص توضيحي أصلي: "+title,
              "alt":"تصميم توضيحي حصري عن "+title+" يوضح خطوات الفحص، وليس رسمًا فنيًا معتمدًا من الشركة",
              "convert_webp":False,"image_base64":base64.b64encode(raw).decode()}
            try:img=write("/upload-image-data",payload)
            except Exception as e:
                media=find_media(pid)
                if not media:raise RuntimeError("Upload uncertain; refuse blind reupload "+slug) from e
            else:media={"id":int(img["media_id"])}
        mid=int(media["id"])
        med=get(BASE+"/wp-json/wp/v2/media/"+str(mid)+"?_fields=id,mime_type,source_url")
        src=med.get("source_url","")
        if filename not in src or med.get("mime_type")!="image/webp":raise RuntimeError("Wrong uploaded media "+slug)
        fig='<figure class="a3tal-inline-diagnostic-original" style="margin:24px 0"><img src="'+html.escape(src,quote=True)+'" alt="'+html.escape("مخطط تشخيص أصلي توضيحي: "+title,quote=True)+'" loading="lazy" width="1600" height="900" decoding="async" style="width:100%;height:auto;border-radius:12px"><figcaption style="font-size:.875rem;color:#586a76">رسم توضيحي أصلي لمسار الفحص؛ لا يمثل مخطط المصنع أو توصيلات السيارة الفعلية.</figcaption></figure>'
        fresh=read_post(pid)
        if fresh.get("content")!=p.get("content") or fresh.get("modified_gmt")!=p.get("modified_gmt"):raise RuntimeError("Concurrent update before image "+slug)
        content=fresh["content"];ix=content.find("<!-- "+MARKERS[pid]+" -->")
        if ix<0:raise RuntimeError("Missing marker before patch "+slug)
        insertion=content.find("</p>",ix)
        if insertion<0:raise RuntimeError("No body paragraph after marker "+slug)
        insertion+=len("</p>")
        content=content[:insertion]+"\n"+fig+"\n"+content[insertion:]
        try:write("/update-post",{"id":pid,"content":content,"expected_modified_gmt":fresh["modified_gmt"]})
        except Exception as err:
            if filename not in read_post(pid).get("content",""):
                raise RuntimeError("Update uncertain, cannot retry "+slug) from err
        done=read_post(pid)
        if filename not in done.get("content","") or int(done.get("featured_media") or 0)!=int(p.get("featured_media") or 0):
            raise RuntimeError("Image not attached or featured unexpectedly altered "+slug)
        verify_public(slug,filename)
        print("ORIGINAL_INLINE_IMAGE_VERIFIED",BASE+"/"+slug+"/","image_id",mid,flush=True)
        time.sleep(3)
    print("EGYPT_BATCH07_FIVE_ORIGINAL_DIAGRAMS_VERIFIED",flush=True)
if __name__=="__main__":main()
