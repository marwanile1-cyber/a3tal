#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0105","P0140","P0190","P0205","P0481"]
# The first upload succeeded before a stale/ambiguous post detail read; reuse it.
RECOVER_UPLOAD={}
INFO={
"P0105":("MAP / BARO PRESSURE SENSOR","CIRCUIT CORRELATION","MAP","pulse"),
"P0140":("REAR OXYGEN SENSOR / BANK 1 SENSOR 2","NO ACTIVITY","O2","low"),
"P0190":("FUEL RAIL PRESSURE SENSOR A","CIRCUIT MALFUNCTION","FUEL","high"),
"P0205":("FUEL INJECTOR / CYLINDER 5","DRIVER CIRCUIT","INJECTOR","pulse"),
"P0481":("RADIATOR FAN / CONTROL 2","CONTROL CIRCUIT","FAN","high")
}
ALT={
"P0105":"تصميم أصلي توضيحي لحساس ضغط السحب MAP ومسار الهواء وإشارة غير متسقة للكود P0105",
"P0140":"صورة تشخيصية توضيحية لحساس أكسجين خلفي وإشارة لا تتغير لكود P0140",
"P0190":"تصميم فني لمسطرة الوقود وحساس ضغط Fuel Rail Pressure الخاص بالكود P0190",
"P0205":"رسم أصلي لدائرة رشاش الأسطوانة الخامسة وخطوط التحكم في P0205",
"P0481":"صورة تقنية توضيحية لدائرة ريلاي ومروحة تبريد المحرك الثانية للكود P0481"
}

FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    label,status,kind,mode=INFO[code]
    warm=(247,176,81) if mode=="high" else (72,216,230)
    bg=Image.new("RGB",(1200,800))
    d=ImageDraw.Draw(bg)
    for y in range(800):
        r=int(9+12*y/800);g=int(18+13*y/800);b=int(29+16*y/800)
        d.line([(0,y),(1200,y)],fill=(r,g,b))
    for x in range(20,1200,50):d.line([(x,0),(x,800)],fill=(25,40,51),width=1)
    for y in range(10,800,50):d.line([(0,y),(1200,y)],fill=(25,40,51),width=1)
    d.rounded_rectangle((28,28,1172,772),radius=24,outline=(91,108,121),width=2)
    d.rounded_rectangle((47,52,446,744),radius=21,fill=(16,30,45),outline=(63,88,100),width=2)
    d.text((73,90),"A3TAL  /  GLOBAL GARAGE",font=font(20,True),fill=(221,183,116))
    d.line((73,133,416,133),fill=(94,107,116),width=2)
    d.text((68,211),code,font=font(100,True),fill=(249,241,222))
    d.text((76,343),status,font=font(21,True),fill=warm)
    label_terms=label.split("  /  ")
    for k,t in enumerate(label_terms):d.text((75,392+36*k),t,font=font(15,True),fill=(170,191,209))
    d.rounded_rectangle((72,586,419,660),radius=12,fill=(28,45,58),outline=(79,110,120))
    d.text((94,601),"OBD-II  /  DIAGNOSTIC",font=font(18,True),fill=(229,232,234))
    d.text((95,631),"ILLUSTRATIVE • NOT CAR-SPECIFIC",font=font(11),fill=(164,185,200))
    d.text((73,705),"A3TAL.COM",font=font(16,True),fill=(227,187,113))
    d.rounded_rectangle((478,75,1126,254),radius=17,fill=(12,30,44),outline=(63,109,125),width=2)
    d.text((503,93),"LIVE SIGNAL  /  ILLUSTRATIVE",font=font(17,True),fill=(166,191,202))
    for gx in range(502,1110,47):d.line((gx,130,gx,236),fill=(32,59,72))
    for gy in [140,172,205,235]:d.line((501,gy,1108,gy),fill=(32,59,72))
    graph=[]
    for n in range(0,581,4):
        x=514+n
        if mode=="low":y=213+3*math.sin(n*.06)+1*math.cos(n*.016)
        elif mode=="high":y=157+15*math.sin(n*.042)+5*math.sin(n*.11)
        else:y=154 if (int(n/70)%2) else 212
        graph.append((x,int(y)))
    d.line(graph,fill=warm,width=5,joint="curve")
    # The hardware is symbolic, not a claimed diagram for any specific vehicle.
    if kind=="O2":
        d.rounded_rectangle((554,415,810,610),radius=42,fill=(69,81,89),outline=(172,179,181),width=5)
        d.rounded_rectangle((570,445,795,576),radius=29,fill=(95,102,105))
        for x in range(584,785,15):d.line((x,451,x+14,575),fill=(147,132,105),width=3)
        d.rounded_rectangle((789,470,1090,570),radius=38,fill=(60,72,78),outline=(158,165,166),width=7)
        d.line((810,518,1090,518),fill=(231,148,81),width=11)
        d.rounded_rectangle((952,378,1013,501),radius=15,fill=(160,160,155),outline=(231,205,150),width=4)
        d.rounded_rectangle((966,343,1001,390),radius=5,fill=(49,63,73),outline=(171,191,205),width=3)
        d.line([(986,343),(1031,325),(1067,330),(1099,303)],fill=(72,184,206),width=7,joint="curve")
        d.line((977,477,977,504),fill=warm,width=9)
        d.text((820,635),"CATALYST → REAR SENSOR",font=font(17,True),fill=(198,212,220))
    elif kind=="FUEL":
        d.rounded_rectangle((540,452,1078,526),radius=24,fill=(104,113,122),outline=(200,198,185),width=5)
        d.line((557,478,1064,478),fill=(195,199,200),width=5)
        for x in [618,745,879,1006]:
            d.rounded_rectangle((x-18,525,x+20,636),radius=8,fill=(58,67,76),outline=(153,169,173),width=4)
            d.rounded_rectangle((x-9,620,x+12,669),radius=5,fill=(92,146,162),outline=(105,183,210),width=3)
        d.rounded_rectangle((845,363,911,452),radius=16,fill=(147,153,150),outline=(218,199,156),width=5)
        d.rounded_rectangle((855,330,899,373),radius=6,fill=(40,53,67),outline=(167,183,195),width=4)
        d.line([(878,329),(935,307),(1020,312),(1083,281)],fill=(73,197,212),width=7,joint="curve")
        d.ellipse((865,397,893,424),fill=warm)
        d.text((790,695),"PRESSURE SIGNAL / RAIL",font=font(17,True),fill=(195,215,229))
    elif kind=="MAP":
        # Metallic throttle/intake casting with a pressure sensor and a marked electrical trace.
        d.rounded_rectangle((565,474,1092,612),radius=57,fill=(80,91,96),outline=(197,198,183),width=7)
        d.rounded_rectangle((591,506,1066,581),radius=32,fill=(40,53,64),outline=(115,139,148),width=3)
        for x in range(620,1010,48):d.line((x,517,x,567),fill=(61,104,120),width=2)
        d.rounded_rectangle((799,359,912,475),radius=18,fill=(135,147,146),outline=(231,200,147),width=5)
        d.rounded_rectangle((824,320,887,365),radius=7,fill=(32,46,57),outline=(170,201,211),width=3)
        d.line([(853,326),(935,313),(1042,340),(1086,320)],fill=warm,width=7,joint="curve")
        d.ellipse((844,427,873,457),fill=warm)
        d.text((728,683),"MANIFOLD AIR PRESSURE / MAP",font=font(17,True),fill=(207,217,223))
    elif kind=="INJECTOR":
        # Fuel rail with five discrete injection branches highlighting cylinder 5.
        d.rounded_rectangle((530,433,1090,502),radius=24,fill=(125,136,143),outline=(232,211,171),width=6)
        d.line((550,468,1074,468),fill=(208,217,218),width=5)
        for k,x in enumerate([581,690,801,912,1020]):
            d.rounded_rectangle((x-15,501,x+20,629),radius=9,fill=(61,78,89),outline=(152,170,178),width=4)
            d.rounded_rectangle((x-13,605,x+18,648),radius=5,fill=warm if k==4 else (61,122,148),outline=(176,191,198),width=3)
            d.line([(x,490),(x,438)],fill=(120,183,201) if k==4 else (81,104,113),width=6)
            d.text((x-5,655),str(k+1),font=font(14,True),fill=(237,192,121) if k==4 else (142,168,178))
        d.line([(1031,437),(1054,381),(1090,381)],fill=warm,width=7,joint="curve")
        d.text((706,697),"CYLINDER 5  /  INJECTOR CONTROL",font=font(16,True),fill=(197,213,224))
    elif kind=="FAN":
        # Radial fan + controller; no manufacturer-specific relay pin positions.
        d.ellipse((579,384,864,672),fill=(31,44,54),outline=(155,185,190),width=9)
        d.ellipse((607,409,839,646),outline=(71,109,126),width=4)
        for k in range(7):
            angle=2*math.pi*k/7
            pts=[]
            for delta,radius in [(0,42),(.18,115),(.48,118),(.65,64)]:
                a=angle+delta
                pts.append((722+int(radius*math.cos(a)),526+int(radius*math.sin(a))))
            d.polygon(pts,fill=(92,113,129),outline=(163,175,184))
        d.ellipse((681,486,765,569),fill=(148,153,150),outline=(238,199,129),width=5)
        d.rounded_rectangle((920,446,1064,565),radius=17,fill=(43,60,71),outline=(167,190,194),width=5)
        d.text((947,485),"CTRL",font=font(21,True),fill=warm)
        d.line([(866,526),(921,526)],fill=warm,width=8)
        d.line([(988,445),(988,396),(1089,379)],fill=(72,191,206),width=6,joint="curve")
        d.text((800,698),"FAN SPEED CONTROL 2",font=font(18,True),fill=(207,218,230))
    else:
        d.rounded_rectangle((541,430,754,640),radius=24,fill=(36,51,60),outline=(154,170,170),width=6)
        d.rounded_rectangle((559,451,735,616),radius=13,fill=(62,66,65),outline=(116,130,130),width=3)
        random.seed(449)
        for _ in range(90):
            x=random.randint(565,732);y=random.randint(459,605)
            d.ellipse((x,y,x+7,y+7),fill=(87,98,89))
        d.line([(753,514),(814,514),(814,470),(868,470)],fill=(76,170,198),width=14,joint="curve")
        d.rounded_rectangle((871,422,955,519),radius=15,fill=(133,141,139),outline=(209,213,198),width=5)
        d.rounded_rectangle((892,393,937,434),radius=7,fill=(45,57,69),outline=(168,182,190),width=4)
        d.line([(916,393),(973,371),(1046,374),(1080,347)],fill=(76,196,213),width=7,joint="curve")
        d.line([(954,479),(1028,479),(1083,527)],fill=(64,145,175),width=11,joint="curve")
        d.text((827,653),"VENT VALVE / EVAP",font=font(18,True),fill=(201,214,222))
    bio=io.BytesIO();bg.save(bio,format="WEBP",quality=83,method=5)
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
    print("All batch 08 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
