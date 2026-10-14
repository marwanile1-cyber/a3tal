#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P2002","U0109","U0126","C0050","B0028"]
RECOVER_UPLOAD={}
INFO={"P2002":("DPF","amber"),"U0109":("PUMP-CAN","cyan"),"U0126":("STEER-CAN","cyan"),"C0050":("REAR-ABS","amber"),"B0028":("SIDE-SRS","amber")}
ALT={
"P2002":"صورة تقنية أصلية لفلتر جسيمات الديزل DPF وتدفق العادم في كود P2002",
"U0109":"رسم توضيحي حصري لوحدة التحكم في مضخة الوقود واتصالها عبر الشبكة في كود U0109",
"U0126":"صورة تشخيصية أصلية لحساس زاوية عجلة القيادة وإشارات شبكة المركبة عند U0126",
"C0050":"رسم فني لحساس ABS للعجلة الخلفية اليمنى ونظام سرعة العجلات في تطبيقات C0050",
"B0028":"تصميم حصري توضيحي للوسادة الهوائية الجانبية اليمنى في مقعد الراكب ونظام SRS"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    bright=(226,174,93) if tone=="amber" else (70,201,224)
    im=Image.new("RGB",(1200,800));d=ImageDraw.Draw(im)
    for y in range(800):
        r=y/800
        d.line((0,y,1200,y),fill=(int(10+9*r),int(19+13*r),int(31+17*r)),width=1)
    for x in range(18,1200,55):d.line((x,0,x,800),fill=(25,42,54),width=1)
    for y in range(21,800,55):d.line((0,y,1200,y),fill=(25,42,54),width=1)
    d.rounded_rectangle((33,37,1167,763),radius=25,outline=(95,114,125),width=2)
    d.ellipse((252,130,1034,700),outline=(40,62,77),width=3)
    if kind=="DPF":
        # Exhaust pipe and open ceramic honeycomb filtering core.
        d.rounded_rectangle((220,336,1028,545),radius=60,fill=(68,81,87),outline=(196,187,160),width=10)
        d.rounded_rectangle((373,312,829,576),radius=55,fill=(116,127,123),outline=(218,195,152),width=9)
        d.rounded_rectangle((413,344,799,546),radius=32,fill=(48,70,79),outline=(139,181,180),width=5)
        for k in range(9):
            for t in range(13):
                xx=435+t*28;yy=358+k*21
                d.ellipse((xx-8,yy-6,xx+8,yy+6),outline=(128,171,168),width=2)
        d.line([(278,438),(377,438)],fill=(218,147,82),width=14)
        d.line([(824,438),(952,438)],fill=(87,200,204),width=14)
        for xx in [455,701]:
            d.rounded_rectangle((xx-15,254,xx+30,348),radius=12,fill=(129,147,143),outline=(221,189,136),width=4)
            d.line([(xx+6,255),(xx+61,201),(xx+115,219)],fill=bright,width=6,joint="curve")
    elif kind=="PUMP-CAN":
        # Fuel tank pump and network control module as physically distinct items.
        d.rounded_rectangle((243,410,733,650),radius=65,fill=(59,86,95),outline=(189,197,180),width=8)
        d.rounded_rectangle((268,500,706,620),radius=36,fill=(31,105,119))
        d.rounded_rectangle((393,335,463,538),radius=16,fill=(127,136,134),outline=(220,198,164),width=6)
        d.rounded_rectangle((408,293,451,346),radius=8,fill=(45,62,72),outline=(170,189,195),width=3)
        d.ellipse((414,427,445,459),fill=bright)
        d.rounded_rectangle((813,298,1023,509),radius=27,fill=(44,61,75),outline=(167,198,201),width=7)
        d.rounded_rectangle((858,343,978,465),radius=17,fill=(78,114,124),outline=(119,185,192),width=4)
        for y in range(366,446,29):d.line((875,y,960,y),fill=(136,206,207),width=5)
        d.line([(447,293),(511,215),(818,215),(818,329)],fill=bright,width=6,joint="curve")
        d.line([(451,312),(565,257),(776,257),(829,365)],fill=(73,190,222),width=6,joint="curve")
    elif kind=="STEER-CAN":
        # Steering wheel angle pickup with outbound optical communication paths.
        d.ellipse((321,176,823,678),outline=(172,192,189),width=31)
        d.ellipse((364,219,781,635),outline=(64,102,118),width=8)
        d.polygon([(362,390),(786,390),(673,482),(475,482)],fill=(96,120,125))
        d.polygon([(555,451),(608,451),(651,619),(521,619)],fill=(96,120,125))
        d.ellipse((515,388,626,499),fill=(47,68,82),outline=(217,183,133),width=7)
        for a in [3.55,4.05,4.55,5.05,5.55]:
            x=572+int(194*math.cos(a));y=425+int(194*math.sin(a))
            d.line((572,425,x,y),fill=bright,width=3)
        d.rounded_rectangle((883,297,1048,453),radius=24,fill=(52,72,84),outline=(142,187,188),width=6)
        d.rounded_rectangle((919,340,1006,410),radius=8,fill=(103,132,135))
        for dy in [520,557]:
            d.line([(812,dy),(897,dy),(950,453)],fill=bright if dy==520 else (78,190,220),width=7,joint="curve")
    elif kind=="REAR-ABS":
        # Rear wheel rotor with magnet ring and an offset inductive pickup.
        d.ellipse((312,183,833,688),fill=(49,65,78),outline=(166,187,193),width=19)
        d.ellipse((370,238,778,635),outline=(90,134,151),width=16)
        d.ellipse((451,316,699,563),fill=(124,128,124),outline=(217,195,149),width=10)
        for k in range(16):
            a=2*math.pi*k/16
            x=575+int(103*math.cos(a));y=439+int(103*math.sin(a))
            d.ellipse((x-8,y-8,x+8,y+8),fill=(38,56,69),outline=(176,192,195),width=3)
        d.ellipse((536,400,616,480),fill=(37,54,64),outline=(225,195,139),width=6)
        d.rounded_rectangle((817,364,915,438),radius=14,fill=(144,149,143),outline=(226,199,151),width=6)
        d.line([(832,399),(757,410),(690,424)],fill=bright,width=10,joint="curve")
        d.rounded_rectangle((858,303,931,368),radius=9,fill=(37,59,69),outline=(150,193,207),width=4)
        d.line([(901,302),(978,256),(1096,278)],fill=(73,197,224),width=8,joint="curve")
    else:
        # Right-hand passenger seat with a separate side cushion illustration, not SRS wiring.
        d.rounded_rectangle((445,182,746,533),radius=92,fill=(87,105,115),outline=(192,203,198),width=11)
        d.rounded_rectangle((495,223,697,502),radius=66,fill=(48,68,81),outline=(138,161,172),width=7)
        d.rounded_rectangle((393,495,830,644),radius=44,fill=(84,102,114),outline=(203,201,182),width=9)
        d.polygon([(743,317),(875,346),(966,459),(881,561),(749,516)],fill=(174,186,187))
        d.arc((751,340,969,562),35,140,fill=(230,216,188),width=7)
        d.arc((792,295,1011,573),248,329,fill=bright,width=10)
        for a in [0,1,2]:
            yy=566+a*23
            d.line((486,yy,733,yy),fill=(53,68,79),width=5)
    d.text((73,716),"A3TAL.COM",font=font(20,True),fill=(220,186,126))
    d.line((74,750,257,750),fill=(165,133,81),width=3)
    bio=io.BytesIO()
    im.save(bio,format="WEBP",quality=87,method=5)
    return bio.getvalue()
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
    print("All batch 13 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
