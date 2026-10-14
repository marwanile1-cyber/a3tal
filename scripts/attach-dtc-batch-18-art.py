#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P2101","U0128","U0184","C0561","B0070"]
RECOVER_UPLOAD={}
INFO={"P2101":("THROTTLE","amber"),"U0128":("EPB-CAN","cyan"),"U0184":("RADIO-CAN","cyan"),"C0561":("ESC-DISABLED","amber"),"B0070":("PRETENSIONER","amber")}
ALT={
"P2101":"رسم فني حصري لموتور بوابة الهواء الإلكترونية وحساس موضع الخانق P2101",
"U0128":"تصميم تشخيصي أصلي لوحدة فرامل اليد الإلكترونية EPB وشبكة الاتصال U0128",
"U0184":"رسم حصري لشاشة الراديو ووحدة الترفيه وتبادل رسائل CAN للكود U0184",
"C0561":"رسم معلوماتي أصلي لوحدة الثبات ESC والتحكم في الجر وحالة التعطيل للكود C0561",
"B0070":"رسم توضيحي أصلي لحزام الأمان وآلية الشداد الكهربائي دون عرض دوائر التفجير للكود B0070"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tonality=INFO[code]
    accent=(225,170,102) if tonality=="amber" else (82,196,220)
    im=Image.new("RGB",(1200,800),(11,23,36));d=ImageDraw.Draw(im)
    for y in range(800):
        t=y/800;d.line((0,y,1200,y),fill=(int(12+10*t),int(23+10*t),int(34+16*t)))
    for x in range(25,1200,58):d.line((x,0,x,800),fill=(28,45,59))
    for y in range(23,800,58):d.line((0,y,1200,y),fill=(28,45,59))
    d.rounded_rectangle((36,39,1164,766),radius=30,outline=(94,114,129),width=3)
    d.ellipse((257,154,1031,704),outline=(45,70,85),width=3)
    if kind=="THROTTLE":
        # Electronically-actuated throttle body with central butterfly plate.
        d.ellipse((329,219,843,696),fill=(80,103,113),outline=(213,194,165),width=12)
        d.ellipse((388,274,778,628),fill=(35,60,73),outline=(147,171,174),width=8)
        d.ellipse((459,333,701,562),fill=(105,130,138),outline=(216,194,158),width=8)
        d.line((578,316,578,583),fill=(233,196,132),width=16)
        d.polygon([(466,405),(697,450),(687,492),(471,454)],fill=(150,160,158),outline=(211,198,168))
        d.rounded_rectangle((852,317,1047,515),radius=33,fill=(53,77,91),outline=(171,195,192),width=7)
        for y in (353,391,430,471):d.line((895,y,1002,y),fill=(105,175,189),width=8)
        d.line([(831,414),(854,414)],fill=accent,width=10)
        d.line([(913,318),(944,258),(1056,248)],fill=(80,203,222),width=9,joint="curve")
    elif kind=="EPB-CAN":
        # Rear rotor and controlled electric parking-brake caliper with standalone controller.
        d.ellipse((271,204,763,696),fill=(50,74,89),outline=(185,196,188),width=16)
        d.ellipse((331,259,703,631),outline=(94,136,148),width=11)
        d.ellipse((404,331,625,552),fill=(119,136,136),outline=(214,192,156),width=8)
        for k in range(12):
            a=2*math.pi*k/12;x=514+int(83*math.cos(a));y=441+int(83*math.sin(a))
            d.ellipse((x-8,y-8,x+8,y+8),fill=(38,58,73),outline=(175,191,197))
        d.rounded_rectangle((638,326,826,518),radius=27,fill=(129,149,148),outline=(230,199,156),width=8)
        d.rounded_rectangle((738,341,845,442),radius=19,fill=(52,77,90),outline=accent,width=6)
        d.rounded_rectangle((897,290,1052,467),radius=22,fill=(44,70,86),outline=(159,190,195),width=7)
        for y in (325,365,405):d.line((925,y,1020,y),fill=(130,196,201),width=6)
        d.line([(829,416),(861,463),(898,463)],fill=accent,width=8,joint="curve")
        d.line([(862,363),(894,338)],fill=(85,198,213),width=7)
    elif kind=="RADIO-CAN":
        # Head unit with display, twin knobs and a separate network module.
        d.rounded_rectangle((254,238,932,631),radius=49,fill=(76,96,107),outline=(202,202,177),width=10)
        d.rounded_rectangle((297,272,892,532),radius=25,fill=(35,61,79),outline=(99,153,169),width=5)
        for x in [337,459,581,703,825]:
            d.line((x,345,x+69,315),fill=(69,144,174),width=7)
            d.line((x,389,x+58,389),fill=(91,181,199),width=7)
            d.line((x,431,x+48,460),fill=accent,width=6)
        for cx in [371,802]:
            d.ellipse((cx-40,552,cx+40,625),fill=(44,69,83),outline=(206,195,172),width=7)
            d.ellipse((cx-13,575,cx+13,601),fill=(133,170,171))
        d.rounded_rectangle((949,279,1083,440),radius=23,fill=(44,69,83),outline=(161,191,197),width=6)
        for x in [974,1014,1053]:d.ellipse((x-6,337,x+6,349),fill=accent)
        d.line([(931,338),(948,338)],fill=(83,198,224),width=7)
    elif kind=="ESC-DISABLED":
        # Vehicle bird-eye outline plus stability wheel vectors and controller.
        d.rounded_rectangle((410,242,778,618),radius=118,fill=(49,75,92),outline=(203,196,169),width=10)
        d.rounded_rectangle((464,292,725,573),radius=77,fill=(95,120,131),outline=(147,174,176),width=5)
        for cx in (410,778):
            for cy in (323,535):
                d.rounded_rectangle((cx-45,cy-69,cx+45,cy+69),radius=27,fill=(33,50,64),outline=(140,155,161),width=6)
        d.rounded_rectangle((868,300,1031,493),radius=30,fill=(40,62,78),outline=(162,186,196),width=7)
        for i,y in enumerate((340,387,434)):
            d.line((900,y,996,y),fill=accent if i==1 else (75,185,208),width=8)
        d.arc((320,214,533,405),90,245,fill=(234,171,92),width=9)
        d.arc((673,435,891,636),260,82,fill=(80,198,211),width=9)
        d.line([(774,423),(856,382)],fill=accent,width=9,joint="curve")
    else:
        # Seatbelt shoulder ribbon, buckle and pretensioner silhouette; no firing circuit.
        d.line([(432,235),(701,511)],fill=(161,180,184),width=44)
        d.line([(432,235),(701,511)],fill=(218,197,154),width=20)
        d.rounded_rectangle((396,191,482,284),radius=18,fill=(117,139,143),outline=(222,195,151),width=7)
        d.ellipse((416,212,464,260),fill=(39,61,76),outline=(190,199,193),width=4)
        d.rounded_rectangle((644,484,801,634),radius=27,fill=(109,135,137),outline=(218,196,159),width=8)
        d.rounded_rectangle((692,517,758,611),radius=14,fill=(44,66,80),outline=(221,196,161),width=5)
        d.rounded_rectangle((848,325,1038,509),radius=34,fill=(48,68,84),outline=(159,189,188),width=6)
        d.ellipse((898,366,988,449),outline=accent,width=8)
        d.line([(794,558),(855,469)],fill=accent,width=8,joint="curve")
        d.line([(416,249),(354,313),(327,387)],fill=(76,190,217),width=7,joint="curve")
    d.text((75,710),"A3TAL.COM",font=font(20,True),fill=(233,189,125))
    d.line((76,744,269,744),fill=(162,128,85),width=3)
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
    print("All batch 18 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
