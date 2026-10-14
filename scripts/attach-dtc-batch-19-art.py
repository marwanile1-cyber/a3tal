#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0544","U0104","U0111","C0299","B0095"]
RECOVER_UPLOAD={}
INFO={"P0544":("EXHAUST-EGT","amber"),"U0104":("CRUISE-CAN","cyan"),"U0111":("HYBRID-BECM","cyan"),"C0299":("BRAKE-BOOSTER","amber"),"B0095":("CRASH-RIGHT","amber")}
ALT={
"P0544":"رسم حصري لحساس حرارة غازات العادم EGT وموضع قراءة Bank 1 Sensor 1 للكود P0544",
"U0104":"رسم توضيحي أصلي لاتصال وحدة مثبت السرعة بالشبكة ورسائل التحكم للكود U0104",
"U0111":"صورة فنية أصلية لوحدة إدارة بطارية الهايبرد والكهرباء وشبكة CAN للكود U0111",
"C0299":"رسم تقني لمساعد الفرامل ومقياس فاكيوم Brake Booster في تطبيقات C0299",
"B0095":"تصميم تشخيصي أصلي لحساس الاصطدام الأمامي الأيمن ونظام SRS للكود B0095"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    accent=(231,180,104) if tone=="amber" else (72,201,227)
    image=Image.new("RGB",(1200,800),(11,23,36))
    d=ImageDraw.Draw(image)
    for y in range(800):
        p=y/800
        d.line((0,y,1200,y),fill=(int(11+12*p),int(22+13*p),int(36+14*p)),width=1)
    for x in range(24,1200,56):d.line((x,0,x,800),fill=(26,44,55))
    for y in range(24,800,56):d.line((0,y,1200,y),fill=(26,44,55))
    d.rounded_rectangle((37,39,1163,763),radius=28,outline=(93,119,126),width=3)
    d.ellipse((244,136,1050,703),outline=(42,66,81),width=3)
    if kind=="EXHAUST-EGT":
        # Exhaust bend, EGT sensor housing and heat flow, not an OEM wiring guide.
        d.line([(248,557),(410,558),(486,440),(696,440),(770,301),(943,303)],fill=(110,126,131),width=86,joint="curve")
        d.line([(248,557),(410,558),(486,440),(696,440),(770,301),(943,303)],fill=(34,58,73),width=61,joint="curve")
        for x,y in [(399,557),(506,440),(602,440),(799,301)]:
            d.ellipse((x-16,y-15,x+16,y+15),fill=(226,157,91))
        d.rounded_rectangle((597,249,670,440),radius=15,fill=(149,153,141),outline=(222,205,166),width=6)
        d.rounded_rectangle((614,189,651,263),radius=11,fill=(47,66,78),outline=(169,196,196),width=5)
        d.line([(634,189),(740,156),(867,184)],fill=accent,width=8,joint="curve")
        for y in (312,341,371):d.line((606,y,660,y),fill=(72,92,97),width=5)
        d.arc((486,244,765,527),200,310,fill=(237,150,80),width=12)
    elif kind=="CRUISE-CAN":
        # Cruise module data shared with speed and braking sensors.
        d.ellipse((282,200,783,700),outline=(178,188,181),width=29)
        d.ellipse((350,268,717,632),outline=(77,126,147),width=8)
        for k in range(9):
            a=2*math.pi*k/9
            x=534+int(153*math.cos(a));y=450+int(153*math.sin(a))
            d.line((535,450,x,y),fill=(84,134,149),width=5)
        d.ellipse((478,398,592,511),fill=(47,68,83),outline=(224,197,162),width=7)
        d.rounded_rectangle((868,293,1053,513),radius=27,fill=(47,72,88),outline=(146,181,196),width=7)
        for x in (911,959,1008):
            d.ellipse((x-15,350,x+15,380),fill=accent)
            d.line((x,407,x,478),fill=(76,161,186),width=5)
        d.line([(761,419),(811,365),(867,365)],fill=accent,width=8,joint="curve")
        d.line([(760,473),(811,449),(864,449)],fill=(68,197,228),width=7,joint="curve")
    elif kind=="HYBRID-BECM":
        # Enclosed battery pack underbody cells, isolated BECM box and orange HV warning trace.
        d.rounded_rectangle((272,296,788,610),radius=45,fill=(72,91,105),outline=(190,202,187),width=10)
        d.rounded_rectangle((308,334,754,574),radius=25,fill=(35,58,72),outline=(97,149,162),width=5)
        for y in (359,432,505):
            for x in (339,434,529,624):
                d.rounded_rectangle((x,y,x+77,y+46),radius=10,fill=(96,140,150),outline=(155,188,192),width=3)
                d.line((x+13,y+24,x+62,y+24),fill=(42,81,93),width=5)
        d.rounded_rectangle((865,307,1047,522),radius=31,fill=(44,71,87),outline=(150,192,197),width=7)
        d.rounded_rectangle((904,347,1007,480),radius=17,fill=(88,139,151),outline=(165,201,199),width=4)
        d.line([(791,407),(854,407)],fill=accent,width=8)
        d.line([(788,460),(849,460)],fill=(228,156,92),width=9)
        d.polygon([(889,574),(935,499),(981,574)],fill=(230,162,84),outline=(237,195,123))
        d.line((935,530,935,549),fill=(42,63,76),width=7)
        d.ellipse((930,553,942,565),fill=(42,63,76))
    elif kind=="BRAKE-BOOSTER":
        # Vacuum canister, master cylinder and gauge without unsafe disassembly instructions.
        d.ellipse((320,234,784,699),fill=(56,79,92),outline=(204,194,168),width=13)
        d.ellipse((363,276,741,653),outline=(113,154,159),width=13)
        d.ellipse((436,346,667,577),fill=(98,120,124),outline=(218,194,147),width=9)
        d.ellipse((508,422,595,509),fill=(43,66,80),outline=accent,width=8)
        d.rounded_rectangle((760,361,1031,492),radius=22,fill=(133,144,137),outline=(224,196,145),width=7)
        d.rounded_rectangle((948,309,1006,365),radius=11,fill=(44,69,79),outline=(171,193,198),width=5)
        d.line([(983,312),(1052,261),(1096,271)],fill=(77,192,216),width=8,joint="curve")
        d.ellipse((311,163,486,332),fill=(36,63,79),outline=(190,199,193),width=8)
        d.arc((349,201,447,305),175,359,fill=accent,width=8)
        d.line((400,244,443,216),fill=(228,157,84),width=7)
        d.line([(446,305),(511,346)],fill=(90,188,208),width=8)
    else:
        # Right-front satellite crash sensor on front crossmember, not an initiator circuit.
        d.polygon([(227,513),(371,293),(826,293),(1002,521),(891,592),(343,592)],fill=(61,83,96),outline=(155,175,176))
        d.line((368,296,825,296),fill=(201,195,169),width=12)
        d.rounded_rectangle((615,356,805,525),radius=27,fill=(124,141,142),outline=(227,201,161),width=8)
        d.ellipse((653,392,768,496),fill=(36,60,76),outline=accent,width=8)
        d.ellipse((697,428,732,463),fill=(203,181,139))
        d.line([(617,438),(504,438),(471,370)],fill=(72,200,223),width=8,joint="curve")
        d.rounded_rectangle((389,326,514,422),radius=18,fill=(41,67,80),outline=(149,193,198),width=5)
        for x in (421,450,481):d.ellipse((x-7,364,x+7,380),fill=(142,194,198))
        d.arc((544,269,877,622),45,139,fill=accent,width=12)
    d.text((75,717),"A3TAL.COM",font=font(20,True),fill=(233,194,137))
    d.line((75,747,272,747),fill=(161,128,85),width=3)
    f=io.BytesIO();image.save(f,format="WEBP",quality=88,method=5)
    return f.getvalue()
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
    print("All batch 19 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
