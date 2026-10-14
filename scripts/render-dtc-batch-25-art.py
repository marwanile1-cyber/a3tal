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

OUT = Path("assets/dtc-batch25")
CODES = ["P0221","P0641","P0732","U0001","U0402","U0416","C0038","C0039","B1600","B1601"]
SUBJECTS = {
  "P0221": "Accelerator pedal electronic throttle B position sensor and connector",
  "P0641": "Five volt electronic sensor reference circuit diagnostic modules",
  "P0732": "Automatic gearbox second-gear clutch and hydraulic valve block",
  "U0001": "High speed CAN bus wiring and connected electronic ECUs",
  "U0402": "Transmission computer CAN bus and invalid network frames",
  "U0416": "Electronic stability control VDC controller and sensor network",
  "C0038": "Left rear ABS wheel speed sensor power supply and harness",
  "C0039": "Right rear ABS magnetic tone wheel and encoder target",
  "B1600": "Ford PATS key reader transceiver and security module",
  "B1601": "Ford PATS unprogrammed transponder key and authentication module"
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
    colors={"P0221":[222,171,104],"P0641":[82,192,215],"P0732":[196,169,109],"U0001":[90,172,208],"U0402":[94,166,222],"U0416":[83,192,211],"C0038":[214,163,111],"C0039":[98,178,198],"B1600":[217,178,102],"B1601":[92,186,191]}
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


def scene_turbo(a,accent):
    d=ImageDraw.Draw(a);shadow(a,(210,665,1330,825))
    tube(d,[(180,550),(346,514),(486,462)],width=102)
    d.ellipse((355,222,1030,779),fill=(58,77,85),outline=(194,183,151),width=32)
    d.ellipse((457,311,922,684),fill=(31,49,62),outline=(125,158,170),width=17)
    for i in range(10):
        th=i*math.tau/10
        d.polygon([(683,498),(683+int(158*math.cos(th)),498+int(155*math.sin(th))),(683+int(84*math.cos(th+.42)),498+int(87*math.sin(th+.42)))],fill=(144,165,168),outline=(221,199,156))
    d.ellipse((651,463,716,529),fill=(*accent,255),outline=(235,220,187),width=6)
    tube(d,[(996,412),(1147,365),(1360,369)],width=83)
    metal(d,(1090,411,1425,590),r=36,base_col=(44,63,73),stroke=(196,206,190))
    d.rounded_rectangle((1141,452,1371,554),radius=21,fill=(37,58,73),outline=(*accent,255),width=6)
    cable(d,[(1279,412),(1375,266),(1502,272)],w=24)
    d.line([(1087,532),(979,560),(908,548)],fill=(*accent,255),width=12)
def scene_evap(a,accent):
    d=ImageDraw.Draw(a);shadow(a,(170,690,1420,844))
    metal(d,(260,285,1170,681),r=90,base_col=(58,76,79),stroke=(168,186,184),width=15)
    for k in range(9):
        x=341+k*92;d.line((x,324,x+48,635),fill=(40,53,62),width=21)
    metal(d,(1230,366,1463,600),r=31,base_col=(80,95,100))
    for x in range(1250,1433,39):
        d.line((x,400,x,562),fill=(48,65,70),width=12)
    tube(d,[(1088,338),(1185,305),(1353,309)],clr=(111,143,148),width=21)
    metal(d,(559,170,873,352),r=30,base_col=(42,61,72),stroke=(191,202,177))
    d.ellipse((647,209,789,314),fill=(39,61,72),outline=(*accent,255),width=9)
    cable(d,[(720,170),(827,117),(997,131),(1091,90)],w=20)
    d.line([(721,314),(720,405),(738,472)],fill=(*accent,255),width=15)
    for xy in [(353,335),(1065,350),(338,615),(1081,615)]:bolt(d,xy,11)
def scene_shift(a,accent):
    d=ImageDraw.Draw(a);shadow(a,(200,696,1390,845))
    metal(d,(220,232,1368,745),r=67,base_col=(77,89,89),stroke=(209,199,166),width=15)
    for i in range(4):
        x=320+i*253
        metal(d,(x,342,x+198,598),r=33,base_col=(46,65,74),stroke=(159,170,164))
        d.ellipse((x+35,376,x+158,500),fill=(30,44,53),outline=(*accent,255) if i==3 else (126,151,160),width=9)
        d.ellipse((x+75,410,x+120,456),fill=(145,157,149),outline=(222,201,163),width=6)
        d.line((x+110,598,x+110,656),fill=(*accent,255) if i==3 else (102,124,131),width=14)
    for j in range(5):
        y=290+j*85; d.line((284,y,1325,y),fill=(47,62,68),width=3)
    cable(d,[(1283,284),(1428,176),(1534,177)],w=30)
    d.rounded_rectangle((1105,613,1331,699),radius=15,fill=(45,66,75),outline=(*accent,255),width=6)
def scene_vdc(a,accent):
    d=ImageDraw.Draw(a);shadow(a,(200,694,1350,848))
    metal(d,(502,260,1102,674),r=49,base_col=(67,83,91),stroke=(200,207,177),width=15)
    d.rounded_rectangle((558,324,1037,602),radius=30,fill=(27,48,62),outline=(*accent,255),width=9)
    for y in [370,422,474,526]:
        for x in [620,715,810,905]:
            d.ellipse((x-13,y-13,x+13,y+13),fill=(105,173,193),outline=(212,206,175),width=3)
    for x in [303,1245]:
        for y in [282,593]:
            d.ellipse((x-93,y-88,x+93,y+88),fill=(26,37,47),outline=(187,194,182),width=21)
            d.ellipse((x-40,y-38,x+40,y+38),fill=(92,111,118),outline=(223,213,174),width=7)
    for p in [[(408,281),(520,365)],[(408,592),(516,544)],[(1093,356),(1146,286)],[(1096,544),(1156,596)]]:
        d.line(p,fill=(*accent,255),width=11)
    cable(d,[(755,261),(865,171),(1033,163)],w=22)
def scene_invalid(a,accent):
    scene_display(a,accent);d=ImageDraw.Draw(a)
    metal(d,(1054,111,1484,304),r=26,base_col=(56,73,84),stroke=(194,201,184))
    for k in range(7):
        x=1121+k*48;d.line((x,153,x,262),fill=(52,126,158),width=9)
    d.line([(1050,203),(956,232),(909,307)],fill=(*accent,255),width=10)
def scene_key(a,accent):
    d=ImageDraw.Draw(a);shadow(a,(160,692,1380,843))
    d.ellipse((298,251,817,727),fill=(49,69,83),outline=(206,197,171),width=30)
    d.ellipse((383,333,729,648),fill=(25,41,53),outline=(116,177,188),width=13)
    d.ellipse((480,414,635,573),fill=(128,159,163),outline=(*accent,255),width=13)
    d.rounded_rectangle((567,440,1291,560),radius=39,fill=(160,171,155),outline=(216,205,171),width=12)
    d.polygon([(1110,450),(1129,405),(1186,406),(1208,449)],fill=(167,179,161))
    d.polygon([(1192,540),(1210,606),(1260,603),(1272,546)],fill=(166,180,165))
    metal(d,(915,183,1381,342),r=35,base_col=(45,64,79),stroke=(165,202,192))
    for i in range(7):
        d.line((988+i*48,222,988+i*48,304),fill=(*accent,255),width=9)
    d.arc((742,307,1016,612),270,72,fill=(*accent,255),width=12)
def scene_abs_front(a,accent):
    scene_abs(a,accent);d=ImageDraw.Draw(a)
    tube(d,[(157,126),(228,230),(310,315)],clr=(103,135,144),width=36)
    tube(d,[(805,669),(957,742),(1180,740)],clr=(93,118,133),width=23)
    d.line([(695,336),(832,227),(1153,211)],fill=(*accent,255),width=12)
def scene_battery(a,accent):
    d=ImageDraw.Draw(a);shadow(a,(195,692,1360,839))
    metal(d,(233,275,918,700),r=51,base_col=(78,93,101),stroke=(199,203,176),width=13)
    for x in [348,742]:
        d.rounded_rectangle((x-36,234,x+39,285),radius=11,fill=(175,176,159),outline=(227,214,170),width=6)
    d.line((353,352,353,463),fill=(*accent,255),width=22);d.line((304,405,402,405),fill=(*accent,255),width=22)
    d.line((695,408,790,408),fill=(114,192,202),width=20)
    metal(d,(1071,292,1443,631),r=37,base_col=(45,63,77),stroke=(176,203,192))
    for y in range(347,590,51):
        d.line((1122,y,1400,y),fill=(89,146,164),width=10)
    tube(d,[(351,232),(420,131),(1137,132),(1150,292)],clr=(185,133,82),width=20)
    tube(d,[(744,233),(891,229),(928,661),(1168,665)],clr=(88,158,169),width=17)
def scene_seat(a,accent):
    d=ImageDraw.Draw(a);shadow(a,(216,696,1370,839))
    d.rounded_rectangle((369,159,810,544),radius=108,fill=(64,83,91),outline=(189,196,178),width=18)
    d.rounded_rectangle((441,210,744,502),radius=79,fill=(41,60,72),outline=(110,158,166),width=8)
    d.rounded_rectangle((464,497,1118,695),radius=90,fill=(75,93,98),outline=(205,203,173),width=18)
    for x in range(532,1058,72):
        d.line((x,553,x-16,662),fill=(48,70,77),width=8)
    metal(d,(988,324,1393,487),r=25,base_col=(48,68,80),stroke=(168,204,195))
    for i in range(5):
        x=1035+i*64;d.ellipse((x,369,x+24,394),fill=(*accent,255))
    cable(d,[(1158,490),(1135,556),(1123,692),(843,716)],w=25)
    d.line([(736,542),(792,472),(997,412)],fill=(*accent,255),width=9)

SCENES={
"P0221":scene_seat,"P0641":scene_battery,"P0732":scene_shift,
"U0001":scene_display,"U0402":scene_invalid,"U0416":scene_vdc,
"C0038":scene_abs,"C0039":scene_abs_front,"B1600":scene_key,"B1601":scene_key
}

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
    (OUT/"manifest.json").write_text(json.dumps({"batch":25,"source":"Original A3tal Pillow illustration, no borrowed photos, not a factory wiring schematic","files":files},ensure_ascii=False,indent=2))
    print("ORIGINAL_ART_GATE_PASSED",len(files),flush=True)

if __name__=="__main__":
    main()
