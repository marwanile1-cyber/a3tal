#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P0691","U023A","C0051","C0800","B1325"]
RECOVER_UPLOAD={}
INFO={"P0691":("COOLING-FAN","amber"),"U023A":("ADAS-CAMERA","cyan"),"C0051":("STEER-ANGLE","amber"),"C0800":("EPS-VOLTAGE","cyan"),"B1325":("BODY-POWER","amber")}
ALT={
"P0691":"صورة فنية أصلية لمروحة تبريد الردياتير وريلاي التحكم والكود P0691",
"U023A":"رسم تشخيصي حصري لكاميرا القيادة المساعدة ADAS ووحدة معالجة الصور والكود U023A",
"C0051":"صورة أصلية لحساس زاوية عجلة القيادة وقراءات Steering Angle للكود C0051",
"C0800":"رسم فني أصلي لتغذية وحدة الباور الكهربائي PSCM وتوصيل الأرضي والكود C0800",
"B1325":"تصميم تشخيصي حصري لتغذية وحدات المقصورة والشحن Device Power 1 للكود B1325"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    accent=(232,179,96) if tone=="amber" else (82,194,225)
    im=Image.new("RGB",(1200,800),(12,23,37));d=ImageDraw.Draw(im)
    for y in range(800):
        r=y/800
        d.line((0,y,1200,y),fill=(int(12+11*r),int(22+13*r),int(36+14*r)))
    for x in range(24,1200,55):d.line((x,0,x,800),fill=(29,46,60))
    for y in range(24,800,55):d.line((0,y,1200,y),fill=(29,46,60))
    d.rounded_rectangle((39,39,1161,761),radius=26,outline=(96,118,128),width=3)
    d.ellipse((265,142,1031,693),outline=(44,73,92),width=3)
    if kind=="COOLING-FAN":
        d.ellipse((284,173,829,716),fill=(49,73,85),outline=(197,197,172),width=19)
        d.ellipse((327,216,787,674),outline=(103,142,151),width=7)
        for k in range(8):
            a=2*math.pi*k/8
            pts=[(558+int(rad*math.cos(a+off)),445+int(rad*math.sin(a+off))) for rad,off in [(42,0),(209,.24),(141,.67)]]
            d.polygon(pts,fill=(112,150,160),outline=(202,198,172))
        d.ellipse((506,395,611,495),fill=(39,67,82),outline=accent,width=7)
        d.rounded_rectangle((844,330,1042,499),radius=29,fill=(58,81,91),outline=(201,192,157),width=7)
        d.rounded_rectangle((887,369,1007,465),radius=18,fill=(100,124,127))
        for x in (911,951,988):d.ellipse((x-10,408,x+10,430),fill=accent)
        d.line([(822,410),(851,410)],fill=(82,199,218),width=9)
        d.line([(950,327),(1017,274),(1102,291)],fill=accent,width=8,joint="curve")
    elif kind=="ADAS-CAMERA":
        d.rounded_rectangle((244,284,846,601),radius=45,fill=(72,97,109),outline=(203,202,180),width=11)
        d.rounded_rectangle((281,321,810,559),radius=29,fill=(37,57,70),outline=(114,154,166),width=6)
        d.ellipse((399,337,666,562),fill=(84,123,138),outline=(201,192,158),width=9)
        d.ellipse((441,370,620,528),fill=(33,60,78),outline=(123,201,216),width=6)
        d.ellipse((487,407,572,492),fill=(25,42,59),outline=accent,width=7)
        d.ellipse((522,438,543,457),fill=(128,193,212))
        d.rounded_rectangle((879,318,1068,506),radius=27,fill=(46,73,88),outline=(162,193,194),width=6)
        for y in [357,403,447]:d.line((909,y,1038,y),fill=(103,184,200),width=8)
        d.line([(840,387),(878,387)],fill=accent,width=9)
        d.line([(838,451),(878,451)],fill=(89,192,219),width=9)
    elif kind=="STEER-ANGLE":
        d.ellipse((293,177,815,705),outline=(197,201,187),width=34)
        d.ellipse((339,224,765,653),outline=(68,127,144),width=9)
        d.polygon([(338,386),(780,389),(643,505),(467,505)],fill=(117,138,145))
        d.polygon([(531,473),(609,473),(660,658),(485,658)],fill=(102,125,136))
        d.ellipse((509,382,618,491),fill=(42,71,86),outline=accent,width=9)
        for deg in range(210,334,22):
            ang=math.radians(deg)
            x=562+int(220*math.cos(ang));y=440+int(220*math.sin(ang))
            d.line((562,440,x,y),fill=(61,147,179),width=3)
        d.rounded_rectangle((874,339,1060,492),radius=30,fill=(47,72,90),outline=(171,195,193),width=7)
        d.arc((905,358,1031,464),190,346,fill=accent,width=9)
        d.line([(778,423),(855,399),(879,399)],fill=accent,width=7,joint="curve")
    elif kind=="EPS-VOLTAGE":
        d.rounded_rectangle((332,251,831,627),radius=46,fill=(95,113,124),outline=(208,201,174),width=10)
        d.rounded_rectangle((376,292,788,570),radius=30,fill=(35,63,80),outline=(121,168,177),width=6)
        for y in [331,383,435,488,542]:d.line((416,y,745,y),fill=(94,155,174),width=7)
        for x in [451,512,573,634,695]:
            d.ellipse((x-12,310,x+12,333),fill=(191,201,176))
        d.rounded_rectangle((882,296,1046,475),radius=27,fill=(50,75,90),outline=(167,189,197),width=7)
        d.line((914,342,1013,342),fill=(229,176,102),width=9)
        d.line((914,389,1013,389),fill=(89,199,218),width=9)
        d.line((968,296,968,256),fill=accent,width=9)
        d.line([(829,391),(874,391)],fill=(74,198,227),width=10)
        d.line([(583,626),(583,680),(446,680)],fill=(230,182,106),width=9,joint="curve")
        for k in [426,445,465]:d.line((k,680,446,709),fill=accent,width=5)
    else:
        # Vehicle body electronics controller + separate battery positive supply and ground.
        d.rounded_rectangle((324,281,790,620),radius=43,fill=(82,103,114),outline=(212,196,162),width=10)
        d.rounded_rectangle((371,320,741,573),radius=27,fill=(41,64,78),outline=(127,165,179),width=6)
        for y in [356,405,454,503]:d.line((413,y,703,y),fill=(99,155,172),width=7)
        d.ellipse((478,375,570,467),fill=(38,62,77),outline=accent,width=8)
        d.rounded_rectangle((869,326,1047,492),radius=22,fill=(54,79,92),outline=(172,190,185),width=7)
        d.rounded_rectangle((893,349,1019,469),radius=16,fill=(87,126,141))
        d.line((936,378,980,378),fill=(232,182,106),width=8)
        d.line((958,357,958,402),fill=(232,182,106),width=8)
        d.line((942,431,985,431),fill=(51,83,96),width=9)
        d.line([(789,406),(865,406)],fill=(76,193,217),width=9)
        d.line([(556,619),(556,685),(432,685)],fill=accent,width=9,joint="curve")
    d.text((75,714),"A3TAL.COM",font=font(20,True),fill=(229,188,129))
    d.line((75,747,267,747),fill=(165,134,85),width=3)
    bio=io.BytesIO();im.save(bio,format="WEBP",quality=88,method=5)
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
    print("All batch 20 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
