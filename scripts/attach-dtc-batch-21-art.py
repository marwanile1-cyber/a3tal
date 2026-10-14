#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0523","U0106","U0159","C0236","B0094"]
RECOVER_UPLOAD={}
INFO={"P0523":("OIL-SENSOR","amber"),"U0106":("GLOW-COMM","cyan"),"U0159":("PARK-ASSIST","cyan"),"C0236":("ABS-COMPARISON","amber"),"B0094":("CENTER-IMPACT","amber")}
ALT={
"P0523":"رسم أصلي لحساس ضغط زيت المحرك وقراءة إشارة الضغط الكهربائية المرتفعة للكود P0523",
"U0106":"تصميم فني حصري لوحدة شمعات تسخين محرك الديزل واتصالها بالشبكة للكود U0106",
"U0159":"صورة توضيحية أصلية لوحدة التحكم في حساسات الركن وشبكة الاتصال للكود U0159",
"C0236":"رسم تشخيصي حصري لنظام ABS يوضح اختلاف معنى C0236 بين GM وToyota دون مخطط كهربائي خاص",
"B0094":"تصميم أصلي توضيحي لحساس الاصطدام الأمامي المركزي ونظام حماية الركاب SRS للكود B0094"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    accent=(230,178,100) if tone=="amber" else (81,202,219)
    im=Image.new("RGB",(1200,800),(13,23,37));d=ImageDraw.Draw(im)
    for yy in range(800):
        mix=yy/800
        d.line((0,yy,1200,yy),fill=(int(11+9*mix),int(24+12*mix),int(36+15*mix)))
    for xx in range(26,1200,55):d.line((xx,0,xx,800),fill=(27,44,58))
    for yy in range(25,800,55):d.line((0,yy,1200,yy),fill=(27,44,58))
    d.rounded_rectangle((39,39,1161,763),radius=28,outline=(92,114,126),width=3)
    d.ellipse((250,145,1042,705),outline=(45,68,86),width=3)
    if kind=="OIL-SENSOR":
        # Sensor body inserted in a metal oil gallery with a non-OEM voltage waveform.
        d.rounded_rectangle((210,467,996,635),radius=69,fill=(66,86,97),outline=(197,194,166),width=10)
        d.rounded_rectangle((247,503,959,598),radius=42,fill=(34,92,112),outline=(92,163,168),width=4)
        for xx in [300,420,540,660,780,900]:
            d.arc((xx,515,xx+80,588),15,165,fill=(85,169,188),width=5)
        d.rounded_rectangle((492,299,647,490),radius=22,fill=(130,145,141),outline=(230,201,150),width=7)
        for yy in range(348,477,25):d.line((492,yy,646,yy),fill=(83,103,110),width=5)
        d.rounded_rectangle((526,231,613,309),radius=10,fill=(43,66,80),outline=(157,192,200),width=5)
        d.line([(570,231),(646,179),(733,192)],fill=accent,width=8,joint="curve")
        d.rounded_rectangle((792,252,1015,434),radius=27,fill=(41,65,80),outline=(146,179,183),width=7)
        d.line([(816,363),(848,344),(881,351),(916,281),(951,340),(985,289)],fill=accent,width=9,joint="curve")
    elif kind=="GLOW-COMM":
        # Diesel preheat electronics, three insulated plugs and two-wire communication motif.
        d.rounded_rectangle((260,250,551,511),radius=38,fill=(58,85,98),outline=(183,194,186),width=9)
        d.rounded_rectangle((298,285,510,472),radius=23,fill=(34,59,76),outline=(106,153,170),width=5)
        for y in range(324,454,32):d.line((329,y,480,y),fill=(91,187,204),width=7)
        for idx,cx in enumerate([642,803,965]):
            d.rounded_rectangle((cx-32,337,cx+32,587),radius=13,fill=(131,144,141),outline=(226,196,145),width=6)
            for y in range(370,490,18):d.line((cx-29,y,cx+29,y),fill=(73,92,99),width=4)
            d.rounded_rectangle((cx-15,580,cx+15,655),radius=6,fill=(198,161,104),outline=(228,211,176),width=3)
            d.rounded_rectangle((cx-22,276,cx+22,344),radius=8,fill=(41,61,76),outline=(159,191,198),width=4)
            d.line([(cx,276),(cx,212),(570,212),(550,298)],fill=accent if idx==1 else (84,166,185),width=5,joint="curve")
        d.line([(551,373),(583,373),(583,455),(620,455)],fill=(72,198,214),width=7,joint="curve")
    elif kind=="PARK-ASSIST":
        # Rear bumper with four ultrasonic transducers and separate communication module.
        d.rounded_rectangle((186,367,959,620),radius=105,fill=(81,106,114),outline=(218,201,168),width=11)
        d.rounded_rectangle((209,420,935,572),radius=75,fill=(42,68,84),outline=(147,170,174),width=5)
        for cx in [300,478,665,839]:
            d.ellipse((cx-38,446,cx+38,522),fill=(61,103,120),outline=(162,209,202),width=7)
            d.ellipse((cx-15,469,cx+15,499),fill=(34,65,81),outline=accent,width=4)
        d.rounded_rectangle((742,207,1045,334),radius=26,fill=(40,62,78),outline=(133,179,197),width=7)
        for x in [796,861,926,987]:d.ellipse((x-11,256,x+11,278),fill=accent)
        d.line([(793,336),(726,392),(665,445)],fill=(79,194,215),width=7,joint="curve")
        for cx in [300,478,665]:
            d.arc((cx-72,334,cx+72,447),200,340,fill=(73,190,207),width=5)
    elif kind=="ABS-COMPARISON":
        # Left: wheel-speed pickup. Right: hydraulic solenoid. Two different OEM meanings.
        d.ellipse((199,248,629,673),fill=(45,64,79),outline=(172,192,195),width=17)
        d.ellipse((249,299,580,624),outline=(107,151,161),width=13)
        d.ellipse((315,367,512,554),fill=(112,131,129),outline=(223,190,142),width=9)
        for k in range(11):
            a=2*math.pi*k/11;x=413+int(76*math.cos(a));y=464+int(76*math.sin(a))
            d.ellipse((x-7,y-7,x+7,y+7),fill=(43,59,70),outline=(173,185,177),width=2)
        d.rounded_rectangle((565,332,651,402),radius=14,fill=(146,160,154),outline=(227,192,142),width=6)
        d.line([(568,368),(525,392)],fill=accent,width=9)
        d.rounded_rectangle((764,289,1036,599),radius=39,fill=(96,116,119),outline=(205,194,162),width=9)
        d.rounded_rectangle((806,336,991,548),radius=20,fill=(41,64,81),outline=(135,175,185),width=6)
        for yy in [368,427,485]:d.rounded_rectangle((833,yy,971,yy+33),radius=12,fill=(118,143,146))
        for xx in [830,958]:
            d.line([(xx,595),(xx,666)],fill=(79,181,200),width=9)
        d.line([(703,240),(703,674)],fill=(83,105,117),width=4)
    else:
        # Front-center impact sensor as an isolated component, no deployment firing circuit.
        d.polygon([(202,562),(310,324),(896,324),(1050,562),(940,635),(308,635)],fill=(61,85,97),outline=(164,180,180))
        d.line([(304,325),(901,325)],fill=(218,193,156),width=12)
        d.rounded_rectangle((487,380,716,558),radius=30,fill=(129,145,144),outline=(222,198,160),width=8)
        d.rounded_rectangle((527,415,677,524),radius=19,fill=(44,67,82),outline=accent,width=7)
        d.ellipse((578,434,629,488),fill=(104,143,154))
        d.rounded_rectangle((792,378,986,502),radius=26,fill=(40,67,83),outline=(151,189,199),width=6)
        for cx in [833,883,932]:d.ellipse((cx-10,423,cx+10,443),fill=(84,201,216))
        d.line([(714,468),(789,441)],fill=accent,width=8,joint="curve")
        d.arc((401,297,746,632),210,290,fill=(232,179,99),width=10)
    d.text((70,713),"A3TAL.COM",font=font(20,True),fill=(231,187,126))
    d.line((72,745,270,745),fill=(166,133,89),width=3)
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
    print("All batch 21 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
