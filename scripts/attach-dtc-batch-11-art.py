#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0217","P0463","U0155","C0035","B0001"]
RECOVER_UPLOAD={}
INFO={"P0217":("COOL","amber"),"P0463":("FUEL","cyan"),"U0155":("CLUSTER","cyan"),"C0035":("ABS","amber"),"B0001":("SRS","amber")}
ALT={
"P0217":"صورة حصرية توضيحية لرادياتير ومحرك ساخن ونظام التبريد المرتبط بالكود P0217",
"P0463":"صورة حصرية تقنية لخزان الوقود وعوامة البنزين وقراءة مستوى الوقود للكود P0463",
"U0155":"صورة أصلية للوحة عدادات رقمية وشبكة اتصالات السيارة المرتبطة بكود U0155",
"C0035":"صورة حصرية لحساس سرعة العجلة ونظام ABS مع توضيح موقع الحساس في تطبيقات C0035",
"B0001":"صورة توضيحية للوسادة الهوائية الأمامية داخل عجلة القيادة ونظام SRS للكود B0001"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    """Render original non-OEM illustrative hardware artwork, no promotional text."""
    kind,tone=INFO[code]
    accent=(236,173,91) if tone=="amber" else (87,203,225)
    W,H=1200,800
    im=Image.new("RGB",(W,H),(13,23,35))
    d=ImageDraw.Draw(im)
    for y in range(H):
        v=y/float(H)
        d.line((0,y,W,y),fill=(int(9+13*v),int(20+13*v),int(34+14*v)))
    for x in range(0,W,60):
        d.line((x,0,x,H),fill=(26,40,54),width=1)
    for y in range(0,H,60):
        d.line((0,y,W,y),fill=(26,40,54),width=1)
    d.rounded_rectangle((36,38,1164,760),radius=28,outline=(103,120,127),width=3)
    d.ellipse((300,165,955,738),outline=(49,73,87),width=3)
    d.ellipse((366,221,889,677),outline=(53,90,107),width=3)
    if kind=="COOL":
        # Radiator with coolant flow, hose and heat source.
        d.rounded_rectangle((385,224,815,620),radius=30,fill=(58,78,88),outline=(192,196,186),width=8)
        d.rounded_rectangle((415,253,786,589),radius=18,fill=(31,48,59),outline=(130,168,180),width=4)
        for x in range(441,784,20):
            d.line((x,263,x,578),fill=(80,145,159),width=6)
        for y in range(273,580,45):
            d.line((428,y,774,y),fill=(117,159,166),width=4)
        d.rounded_rectangle((810,305,1027,382),radius=35,fill=(86,112,121),outline=(213,199,169),width=5)
        d.line([(819,344),(885,344),(925,320),(1019,320)],fill=(196,130,90),width=12,joint="curve")
        d.ellipse((540,348,654,462),outline=accent,width=12)
        for k in range(6):
            a=math.pi*k/3
            x=596+int(44*math.cos(a));y=405+int(44*math.sin(a))
            d.ellipse((x-12,y-12,x+12,y+12),fill=accent)
        for dx in (0,100,200):
            px=480+dx
            d.arc((px,100,px+100,220),190,330,fill=(237,135,86),width=9)
    elif kind=="FUEL":
        # Tank with liquid, hinged sender arm and float.
        d.rounded_rectangle((285,296,946,617),radius=74,fill=(65,83,86),outline=(193,203,190),width=9)
        d.rounded_rectangle((314,430,916,583),radius=42,fill=(31,103,116),outline=(76,160,181),width=2)
        for y in range(465,574,38):
            d.arc((335,y,898,y+50),5,170,fill=(74,171,188),width=3)
        d.ellipse((741,392,793,446),fill=(202,161,104),outline=(236,217,180),width=5)
        d.line((765,420,581,490),fill=(232,183,111),width=12)
        d.rounded_rectangle((545,466,612,506),radius=13,fill=accent,outline=(235,232,215),width=4)
        d.rounded_rectangle((734,247,820,318),radius=17,fill=(105,123,128),outline=(205,192,163),width=5)
        d.line([(776,246),(816,209),(946,200)],fill=(85,190,205),width=8,joint="curve")
        d.ellipse((743,283,787,326),fill=(78,104,111),outline=accent,width=5)
    elif kind=="CLUSTER":
        # Instrument panel / cluster with two needle gauges, digital center and network lines.
        d.rounded_rectangle((254,270,968,632),radius=61,fill=(48,67,81),outline=(184,195,192),width=10)
        d.rounded_rectangle((284,299,939,599),radius=43,fill=(19,32,43),outline=(98,140,155),width=5)
        for cx in (442,789):
            d.ellipse((cx-116,340,cx+116,572),outline=(76,155,176),width=10)
            for k in range(11):
                angle=math.pi*.95+math.pi*1.1*k/10
                x1=cx+int(91*math.cos(angle));y1=456+int(91*math.sin(angle))
                x2=cx+int(109*math.cos(angle));y2=456+int(109*math.sin(angle))
                d.line((x1,y1,x2,y2),fill=(181,205,207),width=4)
            d.line((cx,456,cx+int(82*math.cos(.85 if cx<600 else 2.6)),456-int(82*math.sin(.85 if cx<600 else 2.6))),fill=accent,width=10)
            d.ellipse((cx-16,440,cx+16,472),fill=(179,194,194))
        d.rounded_rectangle((560,386,670,519),radius=12,fill=(27,58,68),outline=(91,181,199),width=5)
        for y in range(408,510,29):d.line((580,y,649,y),fill=(99,202,213),width=5)
        for xx in [363,504,690,839]:
            d.line([(xx,631),(xx,688),(xx+50,704)],fill=(70,185,215),width=6,joint="curve")
    elif kind=="ABS":
        # Wheel hub, rotor and non-contact speed-sensor silhouette.
        d.ellipse((384,175,829,653),fill=(45,57,70),outline=(177,190,190),width=15)
        d.ellipse((414,207,798,622),outline=(103,131,147),width=18)
        d.ellipse((476,274,734,550),fill=(95,109,115),outline=(223,193,142),width=9)
        for k in range(12):
            a=2*math.pi*k/12
            x=605+int(101*math.cos(a));y=412+int(101*math.sin(a))
            d.ellipse((x-12,y-12,x+12,y+12),fill=(32,42,51),outline=(189,198,194),width=3)
        d.ellipse((560,369,649,455),fill=(47,61,73),outline=(212,215,205),width=7)
        d.rounded_rectangle((787,304,890,383),radius=18,fill=(132,142,140),outline=(215,185,138),width=6)
        d.line([(831,338),(767,371),(727,392)],fill=accent,width=10,joint="curve")
        d.rounded_rectangle((848,261,925,305),radius=9,fill=(45,62,72),outline=(132,178,190),width=4)
        d.line([(892,264),(973,226),(1092,242)],fill=(70,184,208),width=8,joint="curve")
    elif kind=="SRS":
        # Conceptual steering wheel and folded-airbag cushion; no explosive wiring diagrams.
        d.ellipse((345,197,886,674),outline=(170,177,179),width=44)
        d.ellipse((385,232,848,637),outline=(44,62,78),width=13)
        d.polygon([(370,389),(838,382),(726,460),(493,462)],fill=(93,108,115))
        d.polygon([(580,439),(652,438),(690,632),(547,630)],fill=(96,112,121))
        d.rounded_rectangle((490,337,735,527),radius=56,fill=(46,65,78),outline=(208,178,134),width=8)
        d.rounded_rectangle((533,374,698,485),radius=45,fill=(153,161,156),outline=(231,224,206),width=5)
        for x in range(562,685,26):d.arc((x,391,x+28,460),0,180,fill=(108,121,126),width=3)
        d.arc((705,275,1020,535),225,320,fill=accent,width=9)
        d.arc((706,263,1028,548),228,309,fill=(87,191,211),width=4)
    # Small brand credit only; no giant words over the image.
    d.text((67,710),"A3TAL.COM",fill=(228,189,126),font=font(20,True))
    d.line((65,749,232,749),fill=(163,136,92),width=3)
    bio=io.BytesIO()
    im.save(bio,format="WEBP",quality=88,method=5)
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
    print("All batch 11 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
