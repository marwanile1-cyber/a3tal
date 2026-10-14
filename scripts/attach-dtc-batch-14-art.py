#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0243","U0102","U0129","C0045","B0081"]
RECOVER_UPLOAD={}
INFO={"P0243":("TURBO-CONTROL","amber"),"U0102":("TRANSFER-CAN","cyan"),"U0129":("BRAKE-CAN","cyan"),"C0045":("ABS-LEFT","amber"),"B0081":("PRESENCE","amber")}
ALT={
"P0243":"صورة تقنية توضيحية حصرية لصمام التحكم في بوابة التيربو Wastegate للكود P0243",
"U0102":"رسم تشخيصي أصلي لوحدة التحكم في الدفع الرباعي Transfer Case واتصال الشبكة U0102",
"U0129":"تصميم توضيحي فني لوحدة التحكم الإلكترونية في الفرامل واتصالات CAN في U0129",
"C0045":"صورة تشخيصية أصلية لحساس سرعة العجلة الخلفية اليسرى في تطبيقات كود ABS C0045",
"B0081":"رسم تقني حصري لنظام استشعار وجود الراكب الأمامي Passenger Presence للكود B0081"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,group=INFO[code]
    accent=(233,174,98) if group=="amber" else (83,199,215)
    im=Image.new("RGB",(1200,800),(12,21,32));d=ImageDraw.Draw(im)
    for y in range(800):
        t=y/800;d.line((0,y,1200,y),fill=(int(11+9*t),int(21+12*t),int(31+17*t)))
    for x in range(24,1200,55):d.line((x,0,x,800),fill=(27,43,52))
    for y in range(25,800,55):d.line((0,y,1200,y),fill=(27,43,52))
    d.rounded_rectangle((39,39,1161,762),radius=28,outline=(96,113,120),width=3)
    d.ellipse((255,143,1050,710),outline=(42,65,81),width=3)
    if kind=="TURBO-CONTROL":
        d.ellipse((295,205,757,668),fill=(74,87,98),outline=(215,195,157),width=10)
        d.ellipse((349,262,703,614),fill=(37,56,73),outline=(145,172,175),width=7)
        for k in range(9):
            a=2*math.pi*k/9;cx=526;cy=437
            pts=[(cx+int(rad*math.cos(a+off)),cy+int(rad*math.sin(a+off))) for rad,off in [(35,0),(165,.23),(97,.54)]]
            d.polygon(pts,fill=(116,142,149),outline=(210,200,176))
        d.ellipse((492,405,558,471),fill=(219,179,115))
        d.rounded_rectangle((858,305,1026,475),radius=25,fill=(121,137,134),outline=(226,194,143),width=6)
        d.rounded_rectangle((903,261,981,314),radius=9,fill=(38,59,71),outline=(153,191,202),width=4)
        d.line([(936,262),(1011,224),(1095,244)],fill=accent,width=7,joint="curve")
        d.line([(856,397),(792,397),(762,470)],fill=(77,200,216),width=9,joint="curve")
        for x in (889,930,972):d.ellipse((x-8,378,x+8,394),fill=(57,79,88))
    elif kind=="TRANSFER-CAN":
        # Axles, wheels and centered transfer case with an ECU network connection.
        d.rounded_rectangle((441,287,784,570),radius=50,fill=(83,106,109),outline=(210,196,167),width=8)
        d.ellipse((498,348,722,517),fill=(41,65,76),outline=(154,182,187),width=6)
        d.rounded_rectangle((554,367,669,488),radius=22,fill=(127,139,135),outline=(219,188,136),width=5)
        for cy in [260,624]:
            d.line((596,cy,596,365 if cy<400 else 492),fill=(148,173,183),width=18)
            d.line((290,cy,913,cy),fill=(164,182,180),width=16)
            for cx in [278,932]:
                d.ellipse((cx-55,cy-57,cx+55,cy+57),fill=(38,57,69),outline=(192,188,161),width=13)
        d.rounded_rectangle((893,324,1044,470),radius=23,fill=(44,69,80),outline=(135,185,194),width=6)
        for y in (360,389,418):d.line((921,y,1017,y),fill=(92,184,199),width=5)
        d.line([(722,407),(850,348),(896,348)],fill=accent,width=8,joint="curve")
    elif kind=="BRAKE-CAN":
        # ABS control unit with four fluid outlets and twin CAN signal paths.
        d.rounded_rectangle((340,275,816,575),radius=42,fill=(94,111,117),outline=(202,196,173),width=10)
        d.rounded_rectangle((389,320,765,528),radius=27,fill=(40,62,78),outline=(143,180,186),width=6)
        for y in range(345,513,27):d.line((420,y,725,y),fill=(86,126,143),width=6)
        for idx,x in enumerate((399,512,629,745)):
            d.ellipse((x-28,555,x+28,610),fill=(140,156,153),outline=(215,195,155),width=5)
            d.line([(x,609),(x,656),(x+60,692)],fill=(73,164,190),width=7,joint="curve")
        d.rounded_rectangle((872,330,1030,495),radius=26,fill=(45,64,79),outline=(167,192,191),width=6)
        for px in [909,950,992]:d.ellipse((px-12,390,px+12,414),fill=(104,193,198))
        d.line([(814,364),(851,305),(1014,284)],fill=accent,width=7,joint="curve")
        d.line([(814,411),(855,368),(1064,355)],fill=(76,193,222),width=6,joint="curve")
    elif kind=="ABS-LEFT":
        d.ellipse((357,177,855,688),fill=(41,61,75),outline=(184,197,197),width=16)
        d.ellipse((400,223,812,647),outline=(98,130,146),width=17)
        d.ellipse((471,301,751,579),fill=(112,124,125),outline=(212,193,154),width=9)
        for k in range(14):
            a=2*math.pi*k/14;x=613+int(113*math.cos(a));y=440+int(113*math.sin(a))
            d.ellipse((x-10,y-10,x+10,y+10),fill=(30,48,58),outline=(181,198,194),width=3)
        d.ellipse((571,397,656,484),fill=(40,58,73),outline=(231,207,156),width=6)
        d.rounded_rectangle((231,323,346,413),radius=15,fill=(124,141,141),outline=(214,191,149),width=6)
        d.line([(342,369),(406,389),(473,421)],fill=accent,width=11,joint="curve")
        d.rounded_rectangle((247,272,331,326),radius=9,fill=(37,58,70),outline=(143,185,200),width=4)
        d.line([(273,275),(205,232),(113,248)],fill=(65,191,217),width=7,joint="curve")
    else:
        # Occupant presence mat in passenger cushion and seat, no explosive equipment depicted.
        d.rounded_rectangle((441,150,742,523),radius=87,fill=(89,108,116),outline=(201,197,174),width=10)
        d.rounded_rectangle((470,189,714,484),radius=58,fill=(47,73,86),outline=(147,180,179),width=6)
        d.rounded_rectangle((353,481,851,654),radius=51,fill=(76,101,112),outline=(193,200,185),width=10)
        d.rounded_rectangle((395,520,809,613),radius=31,fill=(45,73,86),outline=(119,161,166),width=5)
        for x in range(437,790,45):
            for y in (545,575):
                d.ellipse((x-8,y-8,x+8,y+8),fill=(82,182,191))
        d.rounded_rectangle((871,333,1024,487),radius=22,fill=(39,64,77),outline=(162,193,195),width=6)
        for xx in (913,952,987):d.ellipse((xx-10,386,xx+10,406),fill=accent)
        d.line([(806,568),(863,521),(939,487)],fill=accent,width=8,joint="curve")
    d.text((72,714),"A3TAL.COM",font=font(21,True),fill=(231,185,118))
    d.line((73,750,272,750),fill=(157,127,78),width=3)
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
    print("All batch 14 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
