#!/usr/bin/env python3
"""Create five distinct original diagnostic cutaway illustrations and attach them to published DTC records.
No borrowed photography, no invented vehicle-specific wiring diagrams, no third-party image CDN.
No unsafe write retries. This job is idempotent if the post already has a featured image.
"""
import base64, io, json, math, os, random, time, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KEY=os.environ.get("A3TAL_API_KEY","")
ROOT="https://a3tal.com/wp-json/a3tal-direct/v1"
CODES=["P2459","U0131","U0151","C0550","B0020"]
RECOVER_UPLOAD={}
INFO={"P2459":("REGEN","amber"),"U0131":("EPS-CAN","cyan"),"U0151":("SRS-CAN","cyan"),"C0550":("BRAKE-ECU","amber"),"B0020":("SIDE-AIRBAG","amber")}
ALT={
"P2459":"تصميم حصري لفلتر جسيمات الديزل DPF وعمليات تجديد السخام للكود P2459",
"U0131":"رسم فني لوحدة مساعدة التوجيه الكهربائي EPS وشبكة الاتصال عند فقد الرسائل U0131",
"U0151":"تصميم تشخيصي أصلي لوحدة نظام SRS واتصالها بالشبكة عند الكود U0151",
"C0550":"رسم توضيحي لوحدة التحكم الإلكترونية ABS وتغذية الجهاز والأرضي للكود C0550",
"B0020":"صورة أصلية لموضع الوسادة الهوائية الجانبية اليسرى ونظام حماية الركاب B0020"
}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,bold=False):
    name=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(name,size)
def line(draw,points,fill,width=3):
    draw.line(points,fill=fill,width=width,joint="curve")
def image_for(code):
    kind,tone=INFO[code]
    accent=(229,176,97) if tone=="amber" else (75,198,218)
    im=Image.new("RGB",(1200,800),(11,21,32));d=ImageDraw.Draw(im)
    for y in range(800):
        ratio=y/800
        d.line((0,y,1200,y),fill=(int(10+13*ratio),int(22+10*ratio),int(35+15*ratio)))
    for x in range(24,1200,55):d.line((x,0,x,800),fill=(25,42,54))
    for y in range(25,800,55):d.line((0,y,1200,y),fill=(25,42,54))
    d.rounded_rectangle((36,37,1164,766),radius=27,outline=(90,111,124),width=3)
    d.ellipse((255,143,1045,710),outline=(46,69,84),width=3)
    if kind=="REGEN":
        # Particulate filter housing, parallel filtering channels and regeneration flow.
        d.rounded_rectangle((237,345,987,556),radius=55,fill=(73,86,91),outline=(199,199,172),width=10)
        d.rounded_rectangle((391,309,823,584),radius=52,fill=(117,134,128),outline=(217,189,150),width=10)
        d.rounded_rectangle((426,341,789,554),radius=27,fill=(39,65,77),outline=(117,153,164),width=5)
        for j in range(10):
            yy=358+j*19
            for i in range(15):
                xx=445+i*22
                d.rounded_rectangle((xx-7,yy-5,xx+7,yy+5),radius=3,outline=(146,170,168),width=2)
        for cx in [473,602,734]:
            d.arc((cx-50,186,cx+50,305),190,345,fill=(226,147,75),width=9)
            d.line((cx-32,259,cx-5,216),fill=accent,width=5)
        d.line([(236,445),(325,445)],fill=(229,154,93),width=13)
        d.line([(831,445),(982,445)],fill=(83,204,216),width=13)
    elif kind=="EPS-CAN":
        # Wheel assembly and independent electronic power steering controller.
        d.ellipse((280,193,793,693),outline=(192,198,182),width=34)
        d.ellipse((327,240,745,646),outline=(67,119,135),width=10)
        d.polygon([(306,421),(761,420),(643,498),(446,499)],fill=(99,127,127))
        d.polygon([(535,475),(605,475),(650,645),(490,645)],fill=(99,127,127))
        d.ellipse((517,382,627,495),fill=(47,72,87),outline=(224,194,144),width=9)
        d.rounded_rectangle((867,301,1070,499),radius=28,fill=(45,67,78),outline=(154,190,198),width=7)
        d.rounded_rectangle((911,347,1026,454),radius=15,fill=(77,124,137))
        for y in (379,409,437):d.line((927,y,1008,y),fill=(125,202,211),width=5)
        d.line([(774,449),(838,405),(865,405)],fill=accent,width=7,joint="curve")
        d.line([(776,475),(829,467),(857,467)],fill=(78,198,215),width=7,joint="curve")
    elif kind=="SRS-CAN":
        # Read-only status modules, no pyrotechnic firing circuits.
        d.rounded_rectangle((296,271,742,576),radius=42,fill=(76,94,105),outline=(190,201,185),width=10)
        d.rounded_rectangle((343,323,698,526),radius=25,fill=(38,63,76),outline=(113,164,175),width=6)
        for yy in [348,395,446,492]:
            d.line((386,yy,664,yy),fill=(97,158,171),width=7)
        d.ellipse((474,371,564,463),outline=accent,width=8)
        d.rounded_rectangle((862,304,1016,489),radius=37,fill=(123,139,138),outline=(219,204,174),width=8)
        d.line([(896,359),(932,440),(990,357)],fill=(68,98,111),width=18,joint="curve")
        for x in [753,789,826]:d.line((x,414,x+17,414),fill=(226,159,92),width=8)
        d.polygon([(779,370),(816,370),(797,407)],fill=(226,159,92))
    elif kind=="BRAKE-ECU":
        # EBCM controller housing, separate ground rail and power supply ports.
        d.rounded_rectangle((348,247,848,627),radius=49,fill=(99,116,121),outline=(210,200,170),width=10)
        d.rounded_rectangle((400,295,797,573),radius=35,fill=(36,60,73),outline=(134,181,181),width=6)
        for yy in (339,386,436,490,534):d.line((438,yy,755,yy),fill=(103,143,154),width=8)
        for xx in range(463,742,51):d.ellipse((xx-9,313,xx+9,331),fill=(181,197,185))
        d.rounded_rectangle((867,311,1062,489),radius=31,fill=(44,69,83),outline=(152,185,184),width=6)
        for xx in (917,965,1015):d.ellipse((xx-11,377,xx+11,400),fill=accent)
        d.line([(840,357),(877,357)],fill=(80,197,213),width=11)
        d.line([(590,627),(590,689),(470,689)],fill=accent,width=10,joint="curve")
        for w in [455,477,499]:d.line((w,689,477,721),fill=(214,172,106),width=4)
    else:
        # Driver seat and separate side cushion shape, no deployment or wiring instructions.
        d.rounded_rectangle((373,169,708,559),radius=93,fill=(84,108,115),outline=(199,203,185),width=11)
        d.rounded_rectangle((420,220,662,516),radius=59,fill=(47,70,83),outline=(129,165,174),width=7)
        d.rounded_rectangle((299,508,810,663),radius=52,fill=(76,97,110),outline=(207,197,170),width=10)
        d.polygon([(679,306),(811,321),(921,434),(833,558),(697,509)],fill=(170,187,182),outline=(232,215,180))
        d.arc((703,332,924,570),35,145,fill=(230,212,168),width=7)
        d.arc((755,281,1011,569),245,329,fill=accent,width=11)
        d.line([(569,647),(542,719)],fill=(136,159,168),width=18)
    d.text((77,710),"A3TAL.COM",font=font(21,True),fill=(229,189,129))
    d.line((78,744,275,744),fill=(165,134,87),width=3)
    output=io.BytesIO()
    im.save(output,format="WEBP",quality=87,method=5)
    return output.getvalue()
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
    print("All batch 16 featured illustrations processed safely",flush=True)
if __name__=="__main__":main()
