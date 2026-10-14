#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P06DD","U0103","U0164","C0265","B0090"]
RECOVER_UPLOAD={}
INFO={"P06DD":("OIL-CONTROL","amber"),"U0103":("GEAR-CAN","cyan"),"U0164":("HVAC-CAN","cyan"),"C0265":("EBCM-RELAY","amber"),"B0090":("CRASH-SENSOR","amber")}
ALT={
"P06DD":"رسم تشخيصي حصري لدائرة التحكم في ضغط زيت المحرك وطلمبة الزيت للكود P06DD",
"U0103":"صورة أصلية لوحدة اختيار غيارات ناقل الحركة الإلكتروني وشبكة CAN المرتبطة بالكود U0103",
"U0164":"تصميم فني حصري لوحدة التكييف HVAC واتصالها بشبكة السيارة للكود U0164",
"C0265":"رسم حصري لدائرة ريلاي موتور ABS داخل وحدة التحكم في الفرامل EBCM للكود C0265",
"B0090":"تصميم تشخيصي أصلي لحساس الاصطدام الأمامي الأيسر المرتبط بنظام SRS والكود B0090"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    accent=(233,184,112) if tone=="amber" else (78,200,219)
    im=Image.new("RGB",(1200,800),(12,22,36));d=ImageDraw.Draw(im)
    for y in range(800):
        t=y/800
        d.line((0,y,1200,y),fill=(int(11+10*t),int(22+12*t),int(36+14*t)))
    for x in range(28,1200,58):d.line((x,0,x,800),fill=(26,43,55))
    for y in range(24,800,58):d.line((0,y,1200,y),fill=(26,43,55))
    d.rounded_rectangle((38,36,1160,767),radius=27,outline=(98,112,128),width=3)
    d.ellipse((263,135,1042,707),outline=(48,73,91),width=3)
    if kind=="OIL-CONTROL":
        # Variable oil pump cross section with control solenoid, illustrative rather than OEM schematic.
        d.ellipse((349,269,796,663),fill=(78,98,108),outline=(214,192,151),width=12)
        d.ellipse((404,320,737,606),fill=(30,52,66),outline=(127,160,169),width=9)
        for k in range(7):
            ang=2*math.pi*k/7
            pts=[(568+int(r*math.cos(ang+off)),461+int(r*math.sin(ang+off))) for r,off in [(34,0),(143,.3),(85,.65)]]
            d.polygon(pts,fill=(126,154,158),outline=(211,198,168))
        d.ellipse((533,424,605,495),fill=(214,181,124),outline=(224,208,177),width=5)
        d.rounded_rectangle((844,306,1008,449),radius=26,fill=(114,129,129),outline=(232,192,147),width=7)
        d.rounded_rectangle((883,265,972,317),radius=11,fill=(40,61,74),outline=(160,192,205),width=4)
        d.line([(926,267),(1015,219),(1097,233)],fill=accent,width=8,joint="curve")
        d.line([(837,393),(774,393),(755,439)],fill=(78,201,215),width=10,joint="curve")
        d.line([(428,568),(315,568),(267,525)],fill=(75,176,202),width=9,joint="curve")
        d.line([(328,624),(445,624)],fill=accent,width=8)
    elif kind=="GEAR-CAN":
        # Gear selector P-R-N-D module and network transmitter, not a transmission gear teardown.
        d.rounded_rectangle((335,294,743,667),radius=54,fill=(71,91,108),outline=(204,192,165),width=11)
        d.rounded_rectangle((401,339,680,613),radius=28,fill=(30,53,70),outline=(104,152,165),width=6)
        d.rounded_rectangle((508,196,572,485),radius=25,fill=(138,149,151),outline=(227,194,146),width=7)
        d.ellipse((474,166,607,280),fill=(61,80,95),outline=(197,213,212),width=9)
        for idx in range(4):
            y=356+idx*59
            d.rounded_rectangle((611,y,657,y+43),radius=8,fill=(98,153,160) if idx==2 else (53,78,94))
            d.line((438,y+22,480,y+22),fill=accent,width=5)
        d.rounded_rectangle((819,319,1033,512),radius=26,fill=(46,67,82),outline=(142,187,198),width=6)
        d.rounded_rectangle((871,364,982,469),radius=12,fill=(74,121,138))
        for y in (386,415,444):d.line((899,y,953,y),fill=(145,204,205),width=5)
        d.line([(744,399),(784,359),(820,359)],fill=(80,200,221),width=9,joint="curve")
        d.line([(745,438),(788,463),(820,463)],fill=accent,width=8,joint="curve")
    elif kind=="HVAC-CAN":
        # Automatic climate control unit with two fan vents and independent bus controller.
        d.rounded_rectangle((247,295,965,592),radius=48,fill=(61,84,96),outline=(190,201,193),width=10)
        d.rounded_rectangle((290,330,927,557),radius=33,fill=(28,49,64),outline=(98,149,163),width=5)
        for cx in (413,791):
            d.ellipse((cx-92,359,cx+92,544),outline=(78,173,195),width=10)
            for k in range(8):
                a=2*math.pi*k/8
                pts=[(cx+int(r*math.cos(a+off)),453+int(r*math.sin(a+off))) for r,off in [(23,0),(79,.2),(53,.53)]]
                d.polygon(pts,fill=(111,155,168),outline=(213,199,174))
            d.ellipse((cx-18,435,cx+18,471),fill=accent)
        d.rounded_rectangle((549,369,672,514),radius=19,fill=(41,83,101),outline=(92,187,201),width=5)
        for y in [391,431,469]:d.line((567,y,654,y),fill=(138,204,215),width=6)
        d.rounded_rectangle((853,190,1032,302),radius=23,fill=(45,67,79),outline=(146,195,200),width=6)
        d.line([(935,301),(935,329),(902,329)],fill=accent,width=7,joint="curve")
        d.line([(934,190),(997,143),(1098,154)],fill=(74,201,225),width=7,joint="curve")
    elif kind=="EBCM-RELAY":
        # EBCM module and inset relay with output to pump cylinder.
        d.rounded_rectangle((294,269,784,639),radius=48,fill=(104,124,126),outline=(217,195,159),width=9)
        d.rounded_rectangle((338,313,737,589),radius=29,fill=(34,60,75),outline=(114,155,166),width=6)
        for y in [357,409,462,513]:
            d.line((383,y,689,y),fill=(100,143,158),width=8)
        d.rounded_rectangle((484,351,620,495),radius=20,fill=(76,103,113),outline=accent,width=7)
        d.ellipse((522,383,583,444),outline=(207,198,165),width=7)
        for x in (516,583):d.line((x,496,x,548),fill=(211,164,102),width=9)
        d.rounded_rectangle((854,335,1043,536),radius=63,fill=(69,89,101),outline=(190,193,181),width=10)
        d.ellipse((904,397,1003,475),fill=(36,55,70),outline=(212,187,146),width=6)
        d.line([(779,428),(842,428)],fill=accent,width=12)
        d.line([(399,639),(399,686),(293,686)],fill=(82,193,214),width=8,joint="curve")
    else:
        # Sensor housing mounted near vehicle's left frontal structure, not a deployment circuit.
        d.polygon([(226,517),(350,275),(780,275),(992,517),(891,583),(341,583)],fill=(65,84,101),outline=(143,166,177))
        d.line([(350,275),(780,275)],fill=(197,194,166),width=12)
        d.rounded_rectangle((403,343,591,505),radius=27,fill=(112,129,128),outline=(225,202,158),width=8)
        d.ellipse((442,377,548,473),fill=(40,61,75),outline=accent,width=7)
        d.ellipse((481,419,517,455),fill=(202,174,118))
        d.line([(590,416),(729,416),(780,362)],fill=(86,204,225),width=9,joint="curve")
        d.rounded_rectangle((745,304,891,406),radius=18,fill=(42,67,82),outline=(158,197,202),width=6)
        for x in (781,826,866):d.ellipse((x-8,346,x+8,361),fill=(142,190,197))
        d.arc((304,311,661,652),200,290,fill=accent,width=11)
    d.text((74,715),"A3TAL.COM",font=font(20,True),fill=(230,189,132))
    d.line((74,749,263,749),fill=(165,130,85),width=3)
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
    print("All batch 17 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
