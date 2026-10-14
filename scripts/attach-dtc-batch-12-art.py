#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0380","P0530","U0073","C0040","B0010"]
RECOVER_UPLOAD={}
INFO={"P0380":("GLOW","amber"),"P0530":("AC","cyan"),"U0073":("BUS","cyan"),"C0040":("ABS-R","amber"),"B0010":("PASSENGER-SRS","amber")}
ALT={
"P0380":"رسم فني أصلي لشمعات تسخين الديزل ووحدة التحكم الكهربائية المرتبطة بالكود P0380",
"P0530":"صورة تشخيصية أصلية لحساس ضغط الفريون وكمبروسر تكييف السيارة الخاص بالكود P0530",
"U0073":"تصميم حصري لشبكة CAN وخطوط الاتصال بين وحدات السيارة المرتبطة بالكود U0073",
"C0040":"رسم تقني لحساس سرعة العجلة الأمامية اليمنى وحلقة ABS للكود C0040 وفق تطبيقات محددة",
"B0010":"صورة حصرية توضيحية للوسادة الهوائية الأمامية للراكب داخل التابلوه والكود B0010"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    accent=(238,181,105) if tone=="amber" else (76,205,219)
    W,H=1200,800
    im=Image.new("RGB",(W,H),(12,22,35))
    d=ImageDraw.Draw(im)
    for yy in range(H):
        ratio=yy/H
        d.line((0,yy,W,yy),fill=(int(11+15*ratio),int(20+12*ratio),int(31+15*ratio)))
    for xx in range(20,W,55):d.line((xx,0,xx,H),fill=(26,43,55),width=1)
    for yy in range(20,H,55):d.line((0,yy,W,yy),fill=(26,43,55),width=1)
    d.rounded_rectangle((35,35,1165,765),radius=24,outline=(90,112,124),width=3)
    d.ellipse((265,139,1025,714),outline=(44,68,83),width=3)
    if kind=="GLOW":
        # Three independent metallic glow plugs with insulated threaded housings.
        for idx,cx in enumerate([423,607,790]):
            d.rounded_rectangle((cx-28,262,cx+28,546),radius=15,fill=(123,135,139),outline=(221,209,179),width=5)
            for yy in range(305,415,15):d.line((cx-27,yy,cx+27,yy),fill=(72,82,89),width=4)
            d.rounded_rectangle((cx-15,532,cx+15,641),radius=7,fill=(226,164,90) if idx==1 else (163,175,173),outline=(230,203,155),width=3)
            d.rounded_rectangle((cx-19,221,cx+19,277),radius=7,fill=(45,63,75),outline=(149,174,183),width=3)
        d.rounded_rectangle((907,338,1030,505),radius=24,fill=(44,66,79),outline=(190,196,182),width=6)
        for cx in [423,607,790]:
            d.line([(cx,225),(cx,174),(970,174),(970,336)],fill=accent,width=5,joint="curve")
        for x in (940,970,1000):
            d.ellipse((x-5,390,x+5,400),fill=(82,190,212))
    elif kind=="AC":
        # Compressor cutaway with high-side line and pressure transducer.
        d.ellipse((333,294,710,669),fill=(77,94,104),outline=(211,202,178),width=10)
        d.ellipse((384,344,660,620),fill=(33,51,64),outline=(120,155,162),width=8)
        for t in range(7):
            a=2*math.pi*t/7
            d.line((522,483,522+int(118*math.cos(a)),483+int(118*math.sin(a))),fill=(129,169,179),width=13)
        d.ellipse((487,447,557,520),fill=(209,177,122),outline=(242,213,166),width=5)
        d.line([(702,448),(801,447),(801,300),(1063,300)],fill=(145,174,181),width=22,joint="curve")
        d.rounded_rectangle((850,236,932,333),radius=13,fill=(150,157,149),outline=(222,191,143),width=5)
        d.rounded_rectangle((869,190,912,248),radius=8,fill=(36,51,61),outline=(169,192,201),width=4)
        d.line([(891,190),(980,154),(1081,167)],fill=accent,width=8,joint="curve")
        d.ellipse((868,284,905,321),fill=accent)
    elif kind=="BUS":
        # Four ECU nodes sharing a two-wire network with gateway, no OEM pinout.
        d.line([(252,374),(949,374)],fill=(75,202,217),width=11)
        d.line([(252,416),(949,416)],fill=(229,168,94),width=11)
        for idx,(cx,cy) in enumerate([(279,245),(589,249),(914,256),(589,559)]):
            d.rounded_rectangle((cx-93,cy-50,cx+93,cy+67),radius=20,fill=(39,59,72),outline=(159,187,189),width=5)
            for t in range(4):
                xx=cx-62+t*39
                d.line((xx,cy-50,xx,cy-80),fill=(150,174,182),width=5)
            d.rounded_rectangle((cx-55,cy-16,cx+55,cy+30),radius=9,fill=(85,116,128))
            if idx==3:
                d.line([(cx,cy-50),(cx,416)],fill=accent,width=6)
            else:
                d.line((cx,cy+67,cx,374),fill=accent,width=6)
            for px in [cx-22,cx,cx+22]:d.ellipse((px-5,cy-4,px+5,cy+6),fill=(209,210,189))
        for xx in [420,747]:d.ellipse((xx-14,362,xx+14,390),fill=(216,172,101))
    elif kind=="ABS-R":
        # Disc, wheel speed pickup at top right; illustrative right front channel.
        d.ellipse((359,178,817,675),fill=(43,57,69),outline=(171,188,193),width=18)
        d.ellipse((393,214,785,641),outline=(104,131,147),width=13)
        d.ellipse((473,300,712,548),fill=(112,123,126),outline=(218,196,157),width=9)
        for t in range(14):
            a=2*math.pi*t/14
            x=592+int(102*math.cos(a));y=424+int(102*math.sin(a))
            d.ellipse((x-10,y-10,x+10,y+10),fill=(30,42,55),outline=(185,195,197),width=3)
        d.ellipse((558,388,628,462),fill=(38,61,75),outline=(228,208,175),width=5)
        d.rounded_rectangle((804,277,909,362),radius=15,fill=(133,145,144),outline=(217,192,147),width=6)
        d.line([(836,326),(779,365),(726,396)],fill=accent,width=12,joint="curve")
        d.rounded_rectangle((849,220,916,281),radius=11,fill=(37,58,71),outline=(149,173,187),width=4)
        d.line([(895,221),(979,183),(1100,210)],fill=(72,186,215),width=8,joint="curve")
    elif kind=="PASSENGER-SRS":
        # Passenger dashboard and enclosed airbag silhouette; no squib wiring diagram.
        d.rounded_rectangle((180,248,1060,636),radius=65,fill=(48,65,78),outline=(175,190,189),width=9)
        d.rounded_rectangle((233,279,1011,605),radius=52,fill=(30,45,61),outline=(104,132,145),width=5)
        d.rounded_rectangle((536,313,959,438),radius=24,fill=(70,92,105),outline=(185,183,160),width=6)
        d.rounded_rectangle((553,326,937,426),radius=17,fill=(93,110,117))
        d.ellipse((613,344,882,577),fill=(166,177,177),outline=(234,226,199),width=8)
        d.arc((644,362,856,552),30,150,fill=(94,121,133),width=8)
        d.arc((653,365,844,550),210,310,fill=(94,121,133),width=7)
        d.polygon([(412,507),(575,493),(590,573),(399,575)],fill=(53,75,88))
        d.arc((922,244,1075,418),70,205,fill=accent,width=10)
    d.text((70,714),"A3TAL.COM",font=font(19,True),fill=(235,192,122))
    d.line((71,745,246,745),fill=(145,124,88),width=3)
    bio=io.BytesIO();im.save(bio,format="WEBP",quality=87,method=5)
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
    print("All batch 12 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
