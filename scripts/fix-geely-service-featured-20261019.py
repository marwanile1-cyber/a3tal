#!/usr/bin/env python3
"""Add one clearly labeled, original illustration to the existing Geely service directory page.
Generated art is explanatory, not a photograph of an official branch or a Geely EX2.
Preserve article permalink, content, category, SEO and all other posts.
"""
import base64,io,json,os,re,time,urllib.request,urllib.parse,math
from PIL import Image,ImageDraw,ImageFilter
BASE="https://a3tal.com";API=BASE+"/wp-json/a3tal-direct/v1"
PID=83426;SLUG="geely-egypt-service-centers-hotline-ex2"
FILE="a3tal-geely-service-electrical-inspection-original-20261019.webp"
KEY=os.getenv("A3TAL_API_KEY")
if not KEY:raise RuntimeError("Missing bridge secret")
def request(url,payload=None,auth=False):
    h={"Accept":"application/json","User-Agent":"A3talOriginalMediaReview/1.0","Cache-Control":"no-store"}
    if auth:h.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=None
    if payload is not None:h["Content-Type"]="application/json";data=json.dumps(payload,ensure_ascii=False).encode()
    req=urllib.request.Request(url,data=data,headers=h)
    with urllib.request.urlopen(req,timeout=130) as r:return json.load(r)
def post():
    d=request(BASE+f"/wp-json/wp/v2/posts/{PID}?_fields=id,slug,status,link,featured_media,yoast_head_json")
    if d.get("id")!=PID or d.get("slug")!=SLUG or d.get("status")!="publish":raise RuntimeError("Wrong page identity")
    if d.get("link","").rstrip("/")!=BASE+"/"+SLUG:raise RuntimeError("Unexpected permalink")
    return d
def make_image():
    w,h=1600,900
    im=Image.new("RGB",(w,h),"#e6eef3");pix=im.load()
    for y in range(h):
        for x in range(w):
            yy=y/h;xx=x/w
            glow=24*math.exp(-((xx-.74)**2/(.22**2)+(yy-.17)**2/(.28**2)))
            r=int(min(255,218+13*yy+glow));g=int(min(255,230+11*yy+glow));b=int(min(255,240+7*yy+glow))
            pix[x,y]=(r,g,b)
    d=ImageDraw.Draw(im)
    # Clean, well-lit technical service bay. Deliberately stylized as an original illustration.
    d.polygon([(0,0),(1600,0),(1600,440),(0,355)],fill="#f8fcff")
    for x in (55,360,670,980,1290,1570):
        d.rectangle((x,24,x+30,440),fill="#bdcfd9")
    for x in (90,400,710,1020,1330):
        d.rounded_rectangle((x,88,x+255,315),radius=10,fill="#c6e3ec",outline="#f9ffff",width=13)
        d.line((x+127,95,x+127,310),fill="#f8ffff",width=10)
        d.line((x,208,x+255,208),fill="#f8ffff",width=10)
    d.polygon([(0,445),(1600,470),(1600,900),(0,900)],fill="#a8b4bd")
    for k in range(0,22):
        xx=(k*230)%1800-100
        d.line((xx,700,xx+190,900),fill="#cad3d9",width=3)
    for y in (640,767,867):d.line((0,y,1600,y+10),fill="#e4ebed",width=3)
    # Cabinet and diagnostic station
    d.rounded_rectangle((1118,390,1472,674),radius=12,fill="#183644",outline="#42616c",width=8)
    for y in (468,536,610):d.rounded_rectangle((1160,y,1432,y+39),radius=5,fill="#284f60",outline="#72919d",width=2)
    d.rectangle((1140,400,1452,452),fill="#22566a")
    for k in range(5):d.ellipse((1174+k*55,414,1192+k*55,432),fill="#75bcc3")
    # floor contact shadow
    shadow=Image.new("RGBA",(w,h),(0,0,0,0));sd=ImageDraw.Draw(shadow)
    sd.ellipse((180,700,1210,830),fill=(16,37,46,105))
    shadow=shadow.filter(ImageFilter.GaussianBlur(23));im=Image.alpha_composite(im.convert("RGBA"),shadow);d=ImageDraw.Draw(im)
    # unmistakably generic EV service vehicle, not identifiable as a specific model
    d.polygon([(218,608),(315,522),(467,488),(819,485),(1035,537),(1128,624),(1145,720),(181,720)],fill="#f2f6fa")
    d.line([(218,608),(315,522),(467,488),(819,485),(1035,537),(1128,624)],fill="#506c7a",width=13,joint="curve")
    d.polygon([(422,504),(807,504),(944,562),(330,562)],fill="#36576a")
    d.line((639,505,639,562),fill="#d4e7f1",width=13)
    d.rectangle((197,642,1135,712),fill="#e2edf2")
    d.polygon([(250,637),(390,625),(390,666),(237,674)],fill="#a2e4ef")
    d.polygon([(961,623),(1085,635),(1118,678),(955,656)],fill="#80c0d6")
    d.rounded_rectangle((565,650,845,665),radius=7,fill="#bacbd6")
    for cx in (365,973):
        d.ellipse((cx-92,637,cx+92,827),fill="#253540")
        d.ellipse((cx-60,666,cx+60,800),fill="#9aaebd")
        d.ellipse((cx-32,698,cx+32,766),fill="#354b55")
    # Open hood and visible orange EV-rated diagnostic protection (illustrative, not a wiring diagram)
    d.polygon([(425,466),(771,357),(995,385),(1040,478)],fill="#e0e9ef")
    d.line((425,466,771,357,995,385,1040,478),fill="#516d78",width=11)
    d.rounded_rectangle((735,469,956,531),radius=17,fill="#355366")
    d.arc((723,464,990,581),180,345,fill="#f0952a",width=14)
    d.rounded_rectangle((805,487,939,511),radius=8,fill="#698895")
    # technician standing to the side with tablet
    d.ellipse((1166,272,1253,367),fill="#c58b62")
    d.polygon([(1173,276),(1184,254),(1234,255),(1254,281),(1241,295),(1179,290)],fill="#263d48")
    d.polygon([(1135,365),(1229,350),(1296,399),(1281,599),(1117,606)],fill="#284454")
    d.polygon([(1140,589),(1200,590),(1210,802),(1144,802)],fill="#243e4b")
    d.polygon([(1211,590),(1278,596),(1292,802),(1221,802)],fill="#203744")
    d.line((1153,404,1080,516),fill="#c18c65",width=34)
    d.line((1261,402,1183,500),fill="#c18c65",width=34)
    d.polygon([(1024,470),(1181,475),(1180,584),(1022,575)],fill="#182d3a")
    d.polygon([(1034,484),(1170,487),(1169,560),(1034,551)],fill="#75b6c4")
    for y in (503,521,540):d.line((1050,y,1138,y-3),fill="#d5f4f7",width=4)
    d.line((1084,594,1066,662),fill="#234c59",width=9)
    # subtle workshop safety markings
    d.polygon([(1480,698),(1526,614),(1571,698)],fill="#f6c864",outline="#8b7043",width=6)
    d.line((1526,639,1526,674),fill="#75684e",width=9)
    d.ellipse((1521,683,1530,692),fill="#75684e")
    return im.convert("RGB")
def main():
    before=post()
    if before.get("featured_media"):
        print("GEELY_ALREADY_HAS_FEATURED",before["featured_media"],flush=True);return
    q=urllib.parse.urlencode({"search":"a3tal-geely-service-electrical-inspection-original-20261019","per_page":20,"_fields":"id,source_url"})
    previous=request(BASE+"/wp-json/wp/v2/media?"+q)
    exact=[x for x in previous if FILE in x.get("source_url","")]
    if len(exact)>1:raise RuntimeError("Ambiguous prior upload")
    if exact:media_id=int(exact[0]["id"])
    else:
        pic=make_image();out=io.BytesIO();pic.save(out,"WEBP",quality=87,method=6)
        raw=out.getvalue()
        if not 24_000<len(raw)<600_000:raise RuntimeError("Unreasonable image bytes "+str(len(raw)))
        payload={"post_id":PID,"filename":FILE,
          "title":"رسم إرشادي أصلي لورشة فحص السيارات الكهربائية",
          "alt":"تصميم توضيحي حصري لفني يفحص سيارة كهربائية بجهاز تشخيص داخل ورشة، وليست صورة فعلية لمركز جيلي",
          "image_base64":base64.b64encode(raw).decode(),"convert_webp":False}
        try:
            uploaded=request(API+"/upload-image-data",payload,auth=True)
        except Exception:
            rows=request(BASE+"/wp-json/wp/v2/media?"+q)
            exact=[x for x in rows if FILE in x.get("source_url","")]
            if len(exact)!=1:raise RuntimeError("Image write ambiguous: do not retry")
            media_id=int(exact[0]["id"])
        else:media_id=int(uploaded["media_id"])
    fresh=post()
    if fresh.get("featured_media"):
        if int(fresh["featured_media"])==media_id:print("ALREADY_SET_IMAGE",media_id);return
        raise RuntimeError("Someone else set featured image; leave unchanged")
    result=request(API+"/set-featured-image",{"post_id":PID,"media_id":media_id},auth=True)
    after=post()
    if int(after.get("featured_media") or 0)!=media_id:raise RuntimeError("Featured image update not confirmed")
    image_urls=[x.get("url","") for x in after.get("yoast_head_json",{}).get("og_image",[]) if isinstance(x,dict)]
    if not any(FILE in u for u in image_urls):raise RuntimeError("Featured set, but og:image not yet confirmed")
    print("GEELY_ORIGINAL_FEATURED_AND_OG_VERIFIED",BASE+"/"+SLUG+"/","media",media_id,flush=True)
if __name__=="__main__":main()
