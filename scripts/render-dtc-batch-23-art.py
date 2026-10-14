#!/usr/bin/env python3
"""Render five original photo-styled automotive component illustrations offline.

Entirely drawn with Pillow; no borrowed photography or OEM-specific wiring
layouts. Each code gets its own subject and scene. Files are reproducible,
1200? No: reviewed batch23 artwork is 1600x900, saved as WebP.
"""
from pathlib import Path
from hashlib import sha256
import io, json, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

OUT = Path("assets/dtc-batch23")
CODES = ["P0119","U0156","U0186","C0036","B1422"]
SUBJECTS = {
    "P0119":"Coolant temperature sensor and engine harness",
    "U0156":"Dashboard information display and data connection",
    "U0186":"Car audio amplifier and signal wiring",
    "C0036":"ABS wheel sensing assembly (conceptual; OEM varies)",
    "B1422":"Automotive A/C compressor and clutch in a Toyota-compatible context",
}
W,H=1600,900
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def f(n,bold=False):
    p=FONT.replace("DejaVuSans.ttf","DejaVuSans-Bold.ttf") if bold else FONT
    return ImageFont.truetype(p,n)

def base(code):
    rng=random.Random(sum(ord(c) for c in code)*317)
    a=Image.new("RGB",(W,H)); d=ImageDraw.Draw(a)
    for y in range(H):
        t=y/H
        d.line((0,y,W,y),fill=(int(12+9*t),int(20+12*t),int(29+14*t)))
    # Soft workshop lights and a reflective bench, not an external photograph.
    glow=Image.new("RGBA",(W,H),(0,0,0,0)); g=ImageDraw.Draw(glow)
    colors={"P0119":(78,169,191),"U0156":(38,165,220),"U0186":(78,160,211),"C0036":(179,158,100),"B1422":(77,193,184)}
    accent=colors[code]
    g.ellipse((60,-300,980,500),fill=(*accent,62))
    g.ellipse((1110,300,1980,1030),fill=(224,161,104,39))
    g.ellipse((250,700,1420,1170),fill=(157,185,185,30))
    glow=glow.filter(ImageFilter.GaussianBlur(150));a=Image.alpha_composite(a.convert("RGBA"),glow)
    d=ImageDraw.Draw(a)
    for x in [70,170,1470,1550]:
        d.line((x,0,x,730),fill=(32,44,51,120),width=11)
    d.polygon([(0,715),(W,690),(W,H),(0,H)],fill=(37,48,54,255))
    for k in range(23):
        y=710+k*10
        d.line((0,y,W,y-10),fill=(55+k//4,64+k//4,68+k//5,140),width=1)
    for i in range(65):
        x=rng.randrange(W);y=rng.randrange(H)
        rad=rng.randrange(1,4)
        d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=(113,139,145,65))
    return a,accent

def shadow(a,box,r=54,alpha=128):
    ov=Image.new("RGBA",(W,H)); d=ImageDraw.Draw(ov)
    d.ellipse(box,fill=(0,0,0,alpha))
    a.alpha_composite(ov.filter(ImageFilter.GaussianBlur(r)))

def metal(d,box,r=30,base_col=(76,91,99),stroke=(172,181,179),width=9):
    x1,y1,x2,y2=box
    d.rounded_rectangle(box,radius=r,fill=(*base_col,255),outline=(*stroke,255),width=width)
    d.rounded_rectangle((x1+16,y1+15,x2-18,y2-16),radius=max(5,r-12),outline=(121,142,148,220),width=3)
    d.line((x1+29,y1+30,x2-39,y1+30),fill=(227,219,187,125),width=5)
    d.line((x1+36,y2-32,x2-42,y2-32),fill=(21,29,35,180),width=7)

def bolt(d,c,r=11):
    x,y=c
    d.ellipse((x-r-4,y-r-4,x+r+4,y+r+4),fill=(35,47,52),outline=(204,203,180),width=3)
    d.ellipse((x-r,y-r,x+r,y+r),fill=(129,144,144),outline=(219,216,188),width=2)
    d.line((x-6,y-4,x+6,y+4),fill=(37,46,54),width=4)

def tube(d,points,clr=(84,102,111),width=38):
    d.line(points,fill=(14,19,22),width=width+18,joint="curve")
    d.line(points,fill=(*clr,255),width=width,joint="curve")
    d.line(points,fill=(168,179,177,180),width=max(2,width//7),joint="curve")

def cable(d,points,clr=(32,37,43),w=19):
    d.line(points,fill=(179,182,166),width=w+7,joint="curve")
    d.line(points,fill=clr,width=w,joint="curve")
    d.line(points,fill=(91,116,126),width=3,joint="curve")

def ring(d,box,width=20):
    d.ellipse(box,fill=(39,49,56,255),outline=(195,201,190,255),width=width)
    x1,y1,x2,y2=box
    d.ellipse((x1+37,y1+37,x2-37,y2-37),fill=(29,42,49),outline=(123,156,160),width=11)
    d.ellipse((x1+82,y1+82,x2-82,y2-82),fill=(106,125,128),outline=(215,207,171),width=9)

def scene_coolant(a,accent):
    d=ImageDraw.Draw(a)
    shadow(a,(280,680,1250,830))
    metal(d,(244,232,1205,739),r=76,base_col=(79,92,94))
    for x in range(310,1160,80):
        d.line((x,276,x+27,650),fill=(44,62,69),width=21)
        d.line((x+11,281,x+38,645),fill=(140,158,153),width=5)
    metal(d,(610,314,1160,606),r=42,base_col=(43,58,64))
    tube(d,[(145,441),(279,447),(442,486),(617,495)],width=82)
    # ECT brass probe at threaded port
    d.ellipse((763,404,1005,641),fill=(46,58,58),outline=(205,195,153),width=10)
    d.polygon([(762,485),(817,432),(937,443),(972,505),(914,559),(797,550)],fill=(198,171,112),outline=(233,211,155))
    for i in range(7):
        y=470+i*12;d.line((796,y,940,y+6),fill=(103,91,65),width=3)
    metal(d,(890,361,1105,459),r=24,base_col=(43,56,66),stroke=(148,173,183))
    for x in (930,959,989,1019):
        d.line((x,377,x,438),fill=(59,106,119),width=7)
    cable(d,[(1080,404),(1190,365),(1346,370),(1485,322)],w=30)
    for pos in [(330,320),(1080,672),(429,659),(648,281)]:bolt(d,pos,12)
    d.arc((710,380,1100,672),202,323,fill=(*accent,255),width=10)

def scene_display(a,accent):
    d=ImageDraw.Draw(a)
    shadow(a,(270,685,1290,825),alpha=160)
    metal(d,(167,213,1400,700),r=64,base_col=(43,54,65),stroke=(153,167,178),width=13)
    metal(d,(272,274,1221,649),r=39,base_col=(24,35,45),stroke=(97,126,150),width=7)
    screen=Image.new("RGBA",(W,H),(0,0,0,0));s=ImageDraw.Draw(screen)
    s.rounded_rectangle((320,307,1172,606),radius=19,fill=(17,47,68,255))
    for yy in range(310,605):
        t=(yy-310)/295
        s.line((323,yy,1167,yy),fill=(int(15+20*t),int(59-10*t),int(79+12*t)),width=1)
    a.alpha_composite(screen);d=ImageDraw.Draw(a)
    d.rounded_rectangle((377,369,602,546),radius=18,outline=(96,169,191),width=4)
    d.ellipse((435,392,556,506),outline=(193,212,197),width=8)
    d.line([(497,450),(550,418)],fill=(*accent,255),width=8)
    for j in range(3):
        y=370+j*72
        d.rounded_rectangle((668,y,1100,y+41),radius=13,fill=(38,75+j*10,92+j*12),outline=(96,164,192),width=3)
        d.rounded_rectangle((691,y+12,880+j*62,y+27),radius=5,fill=(66,166,191))
    for x in [360,1225]:
        for y in [296,410,535,625]:bolt(d,(x,y),9)
    cable(d,[(1374,380),(1460,333),(1555,347)],w=38)
    # Glowing CAN-style communication route, explicitly conceptual
    d.line([(350,600),(619,600),(672,575),(840,575),(945,589),(1175,589)],fill=(*accent,210),width=6)

def scene_amp(a,accent):
    d=ImageDraw.Draw(a)
    shadow(a,(220,700,1430,845),alpha=165)
    metal(d,(188,288,1358,711),r=46,base_col=(54,68,77),stroke=(183,197,198),width=10)
    for k in range(23):
        xx=270+k*44
        d.rounded_rectangle((xx,327,xx+19,675),radius=5,fill=(27,39,47),outline=(115,137,140),width=2)
        d.line((xx+5,344,xx+5,653),fill=(163,173,163),width=4)
    metal(d,(478,369,1031,612),r=34,base_col=(38,49,58))
    d.rounded_rectangle((519,402,982,573),radius=14,fill=(25,37,48),outline=(81,155,181),width=5)
    # heatsink and audio signal section without implying real circuit terminals
    for i in range(9):
        xx=550+i*49
        d.line((xx,438,xx,531),fill=(86,136,150),width=10)
    d.rounded_rectangle((742,423,943,545),radius=13,outline=(*accent,255),width=4)
    for x in [262,351,1230,1283]:
        bolt(d,(x,623),10)
    for j,clr in enumerate([(136,60,53),(31,36,42),(105,151,162)]):
        tube(d,[(1358,424+j*55),(1462,419+j*55),(1570,350+j*88)],clr=clr,width=17)
    for i in range(4):
        d.ellipse((341+i*57,565,372+i*57,596),fill=(145,160,164),outline=(223,210,171),width=4)

def scene_abs(a,accent):
    d=ImageDraw.Draw(a)
    shadow(a,(270,690,1270,830))
    d.ellipse((190,146,849,768),fill=(30,37,40),outline=(120,128,129),width=36)
    d.ellipse((261,218,777,697),outline=(199,201,174),width=33)
    d.ellipse((318,267,733,663),fill=(89,102,108),outline=(219,214,192),width=11)
    for i in range(23):
        th=2*math.pi*i/23
        cx=525+int(172*math.cos(th));cy=466+int(164*math.sin(th))
        d.rounded_rectangle((cx-10,cy-11,cx+10,cy+11),radius=4,fill=(27,40,48),outline=(184,185,166),width=3)
    d.ellipse((454,397,597,540),fill=(54,70,75),outline=(224,209,174),width=13)
    for i in range(5):
        th=2*math.pi*i/5
        bolt(d,(525+int(80*math.cos(th)),470+int(75*math.sin(th))),10)
    metal(d,(834,347,1101,497),r=32,base_col=(101,118,120))
    metal(d,(886,374,1043,453),r=12,base_col=(48,71,83),stroke=(186,203,189))
    cable(d,[(1095,396),(1225,325),(1396,335),(1516,276)],w=27)
    # pulse trace readout, not a wiring plan
    metal(d,(1056,539,1432,719),r=24,base_col=(31,49,60),stroke=(109,154,159))
    points=[(1086,660),(1125,660),(1125,580),(1160,580),(1160,660),(1198,660),(1198,580),(1239,580),(1239,660),(1265,660),(1278,620),(1296,663),(1332,663),(1332,579),(1360,579),(1360,658),(1408,658)]
    d.line(points,fill=(*accent,255),width=7,joint="curve")

def scene_ac(a,accent):
    d=ImageDraw.Draw(a)
    shadow(a,(270,686,1310,826))
    metal(d,(289,268,1271,736),r=56,base_col=(86,96,95),stroke=(197,201,179))
    for i in range(12):
        xx=349+i*72
        d.line((xx,298,xx+21,679),fill=(48,61,69),width=22)
        d.line((xx+12,320,xx+27,673),fill=(179,182,158),width=5)
    # belt pulley and outer compressor clutch, conceptual not OEM-specific
    ring(d,(536,259,1091,770),width=35)
    d.ellipse((625,345,1003,686),fill=(47,65,72),outline=(175,184,174),width=22)
    d.ellipse((701,408,929,622),fill=(123,140,138),outline=(223,204,171),width=13)
    for i in range(6):
        th=2*math.pi*i/6;bolt(d,(817+int(88*math.cos(th)),515+int(80*math.sin(th))),12)
    d.ellipse((771,474,864,557),fill=(42,55,59),outline=(206,190,149),width=11)
    tube(d,[(292,379),(164,345),(73,289)],clr=(145,153,147),width=33)
    tube(d,[(1137,351),(1305,288),(1505,292)],clr=(122,145,150),width=31)
    d.arc((508,229,1131,800),42,177,fill=(*accent,210),width=11)
    for x,y in [(381,336),(1157,336),(407,684),(1185,677)]:bolt(d,(x,y),12)

SCENES={"P0119":scene_coolant,"U0156":scene_display,
        "U0186":scene_amp,"C0036":scene_abs,"B1422":scene_ac}

def image_for(code):
    a,accent=base(code)
    SCENES[code](a,accent)
    d=ImageDraw.Draw(a)
    d.rounded_rectangle((42,38,W-43,H-39),radius=32,outline=(103,127,132,180),width=4)
    d.rounded_rectangle((88,87,318,164),radius=16,fill=(17,31,42,235),outline=(*accent,255),width=4)
    d.text((111,97),code,font=f(45,True),fill=(236,239,226))
    d.text((93,812),"A3TAL.COM  |  ORIGINAL DIAGNOSTIC VISUAL",font=f(20,True),fill=(189,197,187))
    d.line((94,845,510,845),fill=(*accent,230),width=4)
    # Gentle photographic grain; it is original illustrative artwork, not a photo.
    rng=random.Random(131+sum(ord(c) for c in code))
    grains=Image.new("RGBA",(W//4,H//4),(0,0,0,0));gd=ImageDraw.Draw(grains)
    for i in range(13500):
        px=rng.randrange(W//4);py=rng.randrange(H//4)
        gd.point((px,py),fill=(223,230,219,rng.randrange(5,16)))
    grains=grains.resize((W,H),Image.Resampling.BILINEAR)
    a=Image.alpha_composite(a,grains)
    buf=io.BytesIO();a.convert("RGB").save(buf,format="WEBP",quality=79,method=5)
    return buf.getvalue()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    files=[]
    hashes=set()
    for code in CODES:
        raw=image_for(code)
        if not 25_000<len(raw)<500_000:
            raise RuntimeError("Cover exceeds approved WebP size: "+code+" -> "+str(len(raw)))
        dst=OUT/("a3tal-dtc-"+code.lower()+"-exclusive.webp")
        dst.write_bytes(raw)
        h=sha256(raw).hexdigest()
        if h in hashes:raise RuntimeError("Nonunique generated art")
        hashes.add(h)
        files.append({"code":code,"filename":dst.name,"bytes":len(raw),"sha256":h,"description":SUBJECTS[code],"image_type":"original technical illustration"})
        print("RENDERED_ORIGINAL",code,len(raw),dst,flush=True)
    (OUT/"manifest.json").write_text(json.dumps({"batch":23,"source":"Original A3tal Pillow illustration, no borrowed photos, not a factory wiring schematic","files":files},ensure_ascii=False,indent=2))
    print("ORIGINAL_ART_GATE_PASSED",len(files),flush=True)

if __name__=="__main__":
    main()
