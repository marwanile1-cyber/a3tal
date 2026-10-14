#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0421","U0415","C0110","C0161","B0051"]
RECOVER_UPLOAD={}
INFO={"P0421":("CATALYST","amber"),"U0415":("ABS-DATA","cyan"),"C0110":("ABS-PUMP","amber"),"C0161":("BRAKE-SWITCH","cyan"),"B0051":("SRS-STATUS","amber")}
ALT={
"P0421":"رسم حصري للمحول الحفاز وحساسات الأكسجين أثناء تسخين المحرك P0421",
"U0415":"صورة تقنية حصرية لتبادل بيانات ABS عبر شبكة السيارة والكود U0415",
"C0110":"تصميم تشخيصي توضيحي لموتور مضخة ABS ووحدة تعديل ضغط الفرامل للكود C0110",
"C0161":"رسم أصلي لمفتاح دواسة الفرامل وإشارة BCM إلى وحدة ABS في تطبيقات C0161",
"B0051":"رسم حصري لوحدة SRS وحالة الوسائد والأحزمة، مع تأكيد اختلاف تعريف B0051 حسب الشركة"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    accent=(226,177,110) if tone=="amber" else (83,206,224)
    im=Image.new("RGB",(1200,800),(14,25,37)); d=ImageDraw.Draw(im)
    for y in range(800):
        t=y/800
        d.line((0,y,1200,y),fill=(int(12+t*10),int(22+t*12),int(34+t*14)))
    for x in range(30,1200,57):d.line((x,0,x,800),fill=(26,43,57))
    for y in range(20,800,57):d.line((0,y,1200,y),fill=(26,43,57))
    d.rounded_rectangle((38,40,1161,761),radius=29,outline=(91,118,125),width=3)
    d.ellipse((285,150,965,710),outline=(48,69,85),width=3)
    if kind=="CATALYST":
        # Two exhaust pipe sections, central ceramic monolith and upstream/downstream probes.
        d.rounded_rectangle((205,341,1020,544),radius=63,fill=(86,100,103),outline=(207,199,171),width=10)
        d.rounded_rectangle((398,304,785,574),radius=55,fill=(129,132,124),outline=(215,199,153),width=10)
        d.rounded_rectangle((444,343,751,531),radius=27,fill=(53,73,79),outline=(107,155,165),width=4)
        for y in range(359,515,22):
            for x in range(458,735,25):
                d.ellipse((x-7,y-7,x+7,y+7),outline=(168,186,175),width=2)
        for x in [333,848]:
            d.rounded_rectangle((x-18,239,x+26,351),radius=11,fill=(153,159,150),outline=(223,194,145),width=5)
            d.rounded_rectangle((x-10,197,x+18,249),radius=6,fill=(46,62,72),outline=(160,187,197),width=3)
            d.line([(x+5,194),(x+66,155),(x+122,175)],fill=accent,width=7,joint="curve")
        for xx in (263,316,371):d.line((xx,433,xx+36,433),fill=(224,151,98),width=8)
        for xx in (829,895,961):d.line((xx,433,xx+32,433),fill=(74,200,205),width=8)
    elif kind=="ABS-DATA":
        # Four wheel sources feeding ABS controller; a single invalid signal is marked distinctly.
        d.rounded_rectangle((452,301,758,546),radius=35,fill=(54,78,89),outline=(171,197,191),width=8)
        d.rounded_rectangle((485,332,722,513),radius=17,fill=(37,55,69),outline=(97,159,171),width=5)
        for y in [363,402,441,480]:d.line((516,y,698,y),fill=(107,187,199),width=8)
        for px,py in [(326,242),(878,242),(326,634),(878,634)]:
            d.ellipse((px-58,py-58,px+58,py+58),fill=(38,57,70),outline=(158,174,176),width=9)
            d.ellipse((px-27,py-27,px+27,py+27),outline=accent,width=6)
            d.line([(px+(45 if px<600 else -45),py),(446 if px<600 else 762,390 if py<400 else 468)],fill=(82,199,215) if py<400 else (218,170,95),width=6,joint="curve")
        d.polygon([(849,565),(899,487),(949,565)],fill=(219,156,82),outline=(245,212,161))
        d.line((900,517,900,541),fill=(41,57,67),width=7)
    elif kind=="ABS-PUMP":
        # Hydraulic block with independent cylindrical pump motor and safe schematic conduits.
        d.rounded_rectangle((384,292,796,570),radius=32,fill=(126,137,134),outline=(219,200,157),width=9)
        for y in [335,394,453,512]:
            for x in [446,565,683]:
                d.ellipse((x-26,y-21,x+26,y+21),fill=(59,83,93),outline=(170,183,184),width=4)
        d.rounded_rectangle((784,352,1001,522),radius=65,fill=(65,83,95),outline=(197,200,184),width=9)
        d.ellipse((851,392,963,480),fill=(35,55,70),outline=accent,width=8)
        for y in [314,374,434,494]:
            d.line([(387,y+6),(333,y+6),(333,220 if y<420 else 659),(259,220 if y<420 else 659)],fill=(90,177,188),width=8,joint="curve")
        d.rounded_rectangle((827,273,951,349),radius=12,fill=(38,57,70),outline=(153,192,194),width=5)
        d.line([(900,274),(998,240),(1103,255)],fill=accent,width=7,joint="curve")
    elif kind=="BRAKE-SWITCH":
        # Foot pedal geometry with spring switch and distinct stop-lamp signal.
        d.line([(495,196),(495,506),(676,609)],fill=(162,178,178),width=26,joint="curve")
        d.rounded_rectangle((585,548,782,655),radius=24,fill=(69,91,98),outline=(205,188,152),width=10)
        for x in range(618,760,28):d.line((x,568,x,634),fill=(109,137,143),width=5)
        d.rounded_rectangle((543,269,679,348),radius=18,fill=(143,151,144),outline=(227,200,150),width=7)
        d.line([(574,345),(584,408)],fill=accent,width=13)
        d.rounded_rectangle((758,265,988,467),radius=25,fill=(43,65,80),outline=(130,174,187),width=7)
        for y in (302,349,396):d.line((798,y,942,y),fill=(102,188,196),width=8)
        d.line([(677,303),(731,252),(876,252)],fill=accent,width=8,joint="curve")
        d.ellipse((796,508,858,570),outline=(227,162,92),width=10)
        d.line((828,508,828,477),fill=(227,162,92),width=6)
    else:
        # SDM crash status & seat-belt module icons, conceptual not a firing circuit.
        d.rounded_rectangle((416,275,801,540),radius=43,fill=(66,86,95),outline=(205,199,172),width=10)
        d.rounded_rectangle((451,311,769,503),radius=29,fill=(34,56,70),outline=(123,160,169),width=6)
        for y in [344,393,442]:d.line((479,y,742,y),fill=(103,141,157),width=7)
        d.ellipse((518,356,599,437),outline=accent,width=8)
        d.rounded_rectangle((862,317,1013,487),radius=35,fill=(115,129,136),outline=(216,204,166),width=8)
        d.polygon([(902,357),(950,355),(982,421),(942,458),(904,426)],fill=(192,201,188))
        d.line((903,408,976,408),fill=(81,103,117),width=7)
        d.arc((275,318,432,502),100,270,fill=(225,165,102),width=10)
        d.line([(420,417),(370,455),(310,480)],fill=accent,width=9,joint="curve")
        d.line([(799,405),(862,405)],fill=(83,194,211),width=8)
    d.text((72,711),"A3TAL.COM",font=font(21,True),fill=(225,192,138))
    d.line((74,745,263,745),fill=(162,132,85),width=3)
    stream=io.BytesIO()
    im.save(stream,format="WEBP",quality=87,method=5)
    return stream.getvalue()
last=0.0
def api(endpoint,payload=None):
    global last
    if not KEY:raise RuntimeError("Missing A3TAL direct bridge secret")
    time.sleep(max(0,22-(time.monotonic()-last)));last=time.monotonic()
    data=json.dumps(payload,ensure_ascii=False).encode("utf-8") if payload is not None else None
    headers={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,
             "Accept":"application/json","User-Agent":"A3tal-Original-Art/1.0",
             "Cache-Control":"no-store"}
    if payload is not None:headers["Content-Type"]="application/json"
    req=urllib.request.Request(ROOT+endpoint,data=data,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=75) as response:
            return json.load(response)
    except urllib.error.HTTPError as err:
        raise RuntimeError("Bridge "+endpoint+" returned HTTP "+str(err.code)) from None
def resolve_posts():
    # Read-only public WordPress lookup, no guessing IDs and no uploading to unpublished pages.
    resolved={}
    for code in CODES:
        path="https://a3tal.com/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,status,link"
        req=urllib.request.Request(path,headers={"User-Agent":"A3tal-Art-Preflight/1.0","Accept":"application/json","Cache-Control":"no-cache"})
        try:
            with urllib.request.urlopen(req,timeout=35) as stream:
                entries=json.load(stream)
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as err:
            raise RuntimeError("Cannot verify published record safely for "+code+": "+type(err).__name__) from None
        matching=[x for x in entries if x.get("slug")==code.lower() and x.get("status")=="publish"]
        if len(matching)!=1:raise RuntimeError("Code not exactly once published: "+code)
        resolved[code]=int(matching[0]["id"])
        print("VERIFIED POST",code,resolved[code],flush=True)
    return resolved
def main():
    posts=resolve_posts()
    for code,post_id in posts.items():
        post=api("/post/"+str(post_id))
        if post["status"]!="publish" or post["slug"]!=code.lower():
            raise RuntimeError("Wrong published DTC page for "+code)
        if post.get("featured_media"):
            print("Already has featured media, preserving:",code,post["featured_media"],flush=True)
            continue
        print("Published post preflight",code,"featured=",post.get("featured_media"),flush=True)
        img=image_for(code)
        if not (10_000<len(img)<450_000):raise RuntimeError("Unexpected illustration size for "+code)
        payload={"post_id":post_id,"filename":"a3tal-dtc-"+code.lower()+"-exclusive.webp",
                 "title":"A3tal "+code+" diagnostic artwork","alt":ALT[code],
                 "image_base64":base64.b64encode(img).decode("ascii"),"convert_webp":False}
        # If an image upload has an uncertain response, never blindly repeat the mutation.
        if code in RECOVER_UPLOAD:
            media_id=RECOVER_UPLOAD[code]
            print("Reusing previously uploaded art",code,media_id,flush=True)
        else:
            media=api("/upload-image-data",payload)
            media_id=int(media["media_id"])
            print("Art uploaded",code,"media",media_id,flush=True)
        confirm=api("/set-featured-image",{"post_id":post_id,"media_id":media_id})
        print("Set-featured server result",code,confirm.get("featured_media"),flush=True)
        if int(confirm.get("featured_media") or 0)!=media_id:
            raise RuntimeError("WordPress refused featured image for "+code)
        # Host cache layers can serve an older post response after a successful mutation.
        checked=None
        for check in range(3):
            checked=api("/post/"+str(post_id)+"?a3tal_media_verify="+str(int(time.time())))
            got=int(checked.get("featured_media") or 0)
            print("Readback",code,"attempt",check+1,"featured",got,flush=True)
            if got==media_id:break
            time.sleep(25)
        if int(checked.get("featured_media") or 0)!=media_id:
            raise RuntimeError("Featured image persisted in mutation response but post endpoint not consistent for "+code)
        print("VERIFIED COVER",code,checked["link"],"image",media_id,"bytes",len(img),flush=True)
    print("All batch 15 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
