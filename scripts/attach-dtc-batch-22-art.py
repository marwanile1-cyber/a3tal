#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P2563","U0107","C1241","C0237","B1421"]
RECOVER_UPLOAD={}
INFO={"P2563":("TURBO-SENSOR","amber"),"U0107":("THROTTLE-CAN","cyan"),"C1241":("ABS-POWER","amber"),"C0237":("REAR-WHEEL","cyan"),"B1421":("SOLAR-SENSOR","amber")}
ALT={
"P2563":"رسم فني حصري لحساس موضع مشغل التحكم في ضغط التيربو مع رمز P2563",
"U0107":"رسم توضيحي أصلي لوحدة بوابة الهواء الإلكترونية واتصال CAN للكود U0107",
"C1241":"تصميم تشخيصي أصلي لتغذية وحدة ABS وبطارية السيارة ونظام الثبات في تويوتا C1241",
"C0237":"صورة فنية أصلية لحساس سرعة العجلة الخلفية وبيانات الإشارة المتقطعة في بعض GM للكود C0237",
"B1421":"رسم حصري لحساس الشمس أعلى التابلوه ونظام التكييف الأوتوماتيك في تويوتا B1421"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    accent=(229,179,99) if tone=="amber" else (79,198,221)
    im=Image.new("RGB",(1200,800),(12,23,35));d=ImageDraw.Draw(im)
    for yy in range(800):
        t=yy/800;d.line((0,yy,1200,yy),fill=(int(11+10*t),int(21+12*t),int(36+13*t)))
    for x in range(24,1200,56):d.line((x,0,x,800),fill=(26,42,55))
    for y in range(24,800,56):d.line((0,y,1200,y),fill=(26,42,55))
    d.rounded_rectangle((36,37,1163,762),radius=27,outline=(94,112,125),width=3)
    d.ellipse((264,150,1038,713),outline=(46,68,83),width=3)
    if kind=="TURBO-SENSOR":
        # Compressor with radial turbine and independent servo / angle transducer.
        d.ellipse((272,243,765,677),fill=(60,85,99),outline=(208,195,170),width=11)
        d.ellipse((341,306,698,612),fill=(37,61,78),outline=(139,171,175),width=8)
        for k in range(9):
            a=2*math.pi*k/9
            points=[(519+int(r*math.cos(a+off)),460+int(r*math.sin(a+off))) for r,off in [(24,0),(154,.27),(87,.57)]]
            d.polygon(points,fill=(119,152,155),outline=(220,200,163))
        d.ellipse((485,426,553,494),fill=(206,178,119))
        d.rounded_rectangle((821,317,1029,504),radius=32,fill=(130,145,145),outline=(228,197,150),width=7)
        d.rounded_rectangle((861,347,988,469),radius=18,fill=(45,69,82),outline=accent,width=5)
        d.line([(823,411),(769,411),(711,452)],fill=(75,200,216),width=11,joint="curve")
        d.line([(921,318),(965,259),(1071,269)],fill=accent,width=8,joint="curve")
        d.arc((843,361,1004,459),30,150,fill=(89,181,194),width=6)
    elif kind=="THROTTLE-CAN":
        # Butterfly throttle in intake tube and separately monitored electronic actuator.
        d.rounded_rectangle((248,281,799,646),radius=110,fill=(98,116,121),outline=(207,190,161),width=12)
        d.ellipse((355,326,703,606),fill=(37,61,76),outline=(146,178,177),width=8)
        d.ellipse((436,383,626,546),fill=(124,145,150),outline=(216,190,155),width=5)
        d.line((531,343,531,574),fill=(226,188,134),width=13)
        d.polygon([(450,445),(615,475),(596,499),(445,466)],fill=(181,188,177))
        d.rounded_rectangle((832,313,1046,509),radius=33,fill=(46,71,87),outline=(151,189,199),width=8)
        for i,y in enumerate([354,391,428,465]):
            d.line((874,y,1010,y),fill=accent if i==2 else (93,160,181),width=7)
        d.line([(797,413),(830,413)],fill=(71,199,220),width=10)
        d.line([(944,315),(992,249),(1089,260)],fill=accent,width=7,joint="curve")
    elif kind=="ABS-POWER":
        # Battery + and - connection rails entering brake control module.
        d.rounded_rectangle((231,321,499,623),radius=33,fill=(84,113,124),outline=(197,199,170),width=11)
        d.rounded_rectangle((282,296,337,346),radius=9,fill=(171,182,173))
        d.rounded_rectangle((405,296,458,346),radius=9,fill=(171,182,173))
        d.line((304,378,304,434),fill=accent,width=13)
        d.line((278,407,333,407),fill=accent,width=13)
        d.line((409,408,463,408),fill=(79,195,208),width=13)
        d.rounded_rectangle((672,271,1027,636),radius=48,fill=(114,133,134),outline=(217,197,157),width=9)
        d.rounded_rectangle((712,316,987,596),radius=28,fill=(43,65,79),outline=(125,175,179),width=6)
        for y in [358,411,462,519,563]:d.line((756,y,945,y),fill=(92,149,166),width=7)
        d.line([(306,298),(306,217),(808,217),(808,272)],fill=accent,width=10,joint="curve")
        d.line([(432,630),(432,680),(848,680),(848,637)],fill=(86,205,220),width=9,joint="curve")
        d.ellipse((802,202,834,232),fill=(229,183,119))
    elif kind=="REAR-WHEEL":
        # Rear wheel tone ring and oscilloscope showing erratic pulses.
        d.ellipse((222,199,750,697),fill=(49,68,83),outline=(188,195,182),width=19)
        d.ellipse((272,246,699,650),outline=(100,142,154),width=13)
        d.ellipse((354,326,620,571),fill=(123,140,139),outline=(216,196,157),width=9)
        for k in range(17):
            a=2*math.pi*k/17
            xx=487+int(107*math.cos(a));yy=448+int(107*math.sin(a))
            d.ellipse((xx-9,yy-9,xx+9,yy+9),fill=(39,57,67),outline=(173,196,191),width=3)
        d.rounded_rectangle((669,294,790,385),radius=15,fill=(128,150,146),outline=(226,194,154),width=5)
        d.line([(672,330),(627,367)],fill=accent,width=10)
        d.rounded_rectangle((809,295,1083,563),radius=31,fill=(43,67,83),outline=(151,195,200),width=7)
        for yy in [350,409,468]:d.line((841,yy,1049,yy),fill=(63,99,111),width=2)
        d.line([(836,466),(859,466),(859,371),(890,371),(890,466),(918,466),(918,371),(952,371),(952,466),(969,466),(982,420),(1005,466),(1036,466)],fill=accent,width=7,joint="curve")
        d.line([(786,332),(809,332)],fill=(75,196,210),width=8)
    else:
        # Automotive climate sunload sensor on dashboard illuminated by sunlight.
        d.rounded_rectangle((218,443,974,638),radius=71,fill=(69,94,107),outline=(198,195,167),width=10)
        d.rounded_rectangle((269,467,929,604),radius=39,fill=(43,65,82),outline=(114,155,169),width=5)
        d.ellipse((504,374,680,542),fill=(112,133,139),outline=(222,194,155),width=10)
        d.ellipse((538,404,644,510),fill=(43,67,84),outline=accent,width=7)
        d.ellipse((570,434,614,480),fill=(94,185,196))
        d.ellipse((794,157,939,302),outline=(235,185,102),width=12)
        for k in range(9):
            a=2*math.pi*k/9
            xa=867+int(87*math.cos(a));ya=230+int(87*math.sin(a))
            xb=867+int(115*math.cos(a));yb=230+int(115*math.sin(a))
            d.line((xa,ya,xb,yb),fill=accent,width=7)
        for x in [832,872,911]:
            d.line([(x,323),(680,386)],fill=(232,165,91),width=6)
        d.rounded_rectangle((311,495,449,573),radius=17,fill=(76,122,139),outline=(132,180,185),width=5)
        for yy in [515,542]:d.line((343,yy,420,yy),fill=(145,198,201),width=5)
    d.text((75,715),"A3TAL.COM",font=font(20,True),fill=(226,187,123))
    d.line((76,746,267,746),fill=(159,130,85),width=3)
    raw=io.BytesIO();im.save(raw,format="WEBP",quality=88,method=5)
    return raw.getvalue()
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
    print("All batch 22 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
