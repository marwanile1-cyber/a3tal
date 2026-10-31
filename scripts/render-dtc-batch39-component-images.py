#!/usr/bin/env python3
"""Original, explanatory Arabic 1600x900 WebP art for DTC39.
One component-specific vector illustration per code, with exact code and diagnostic name.
No external photographs or assets. A diagram never claims to prove a component faulty.
"""
import sys,math,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
DATA={
"P0171":("خليط وقود فقير","البنك الأول B1","intake","الهواء الزائد أو ضغط الوقود"),
"P0301":("اختلال احتراق","الأسطوانة الأولى","ignition","كويل وبوجيه الأسطوانة 1"),
"P0442":("تسريب صغير بنظام EVAP","منظومة أبخرة الوقود","evap_small","افحص الغطاء والخراطيم"),
"P0128":("حرارة المحرك أقل","من نطاق الثرموستات","thermostat","افحص الثرموستات وحساس ECT"),
"P0455":("تسريب كبير بنظام EVAP","منظومة أبخرة الوقود","evap_large","افحص الغطاء والخرطوم"),
"P0400":("خلل تدفق غازات EGR","نظام إعادة التدوير","egr","فحص الصمام ومسار التدفق"),
"P0136":("عطل دائرة حساس الأكسجين","الحساس الخلفي B1S2","o2","فحص إشارة الحساس الخلفي"),
"P0101":("خلل نطاق حساس الهواء","MAF Range / Performance","maf","افحص السحب وبيانات MAF"),
"P0016":("خلل توافق الكرنك والكامة","Cam / Crank Correlation","timing","راجع التوقيت وإشارات الحساسات")
}
COLORS={"intake":(52,213,237),"ignition":(243,179,65),"evap_small":(87,228,177),
"evap_large":(243,132,85),"thermostat":(67,191,244),"egr":(180,217,108),
"o2":(68,203,229),"maf":(88,203,227),"timing":(237,181,83)}
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,b=True):return ImageFont.truetype(BOLD if b else REG,size)
def stroke(d,coords,fill,width=3):d.line(coords,fill=fill,width=width,joint="curve")
def poly(d,vertices,color,outline=(225,233,238,255),width=5):
 d.polygon(vertices,fill=color)
 d.line(vertices+[vertices[0]],fill=outline,width=width,joint="curve")
def diag(code):
 line1,line2,kind,foot=DATA[code]
 C=COLORS[kind];W,H=1600,900
 im=Image.new("RGB",(W,H));px=im.load()
 for y in range(H):
  for x in range(W):
   pulse=max(0,1-((x-430)**2/(850**2)+(y-450)**2/(720**2))**.5)
   px[x,y]=(int(6+8*pulse),int(20+24*pulse),int(34+35*pulse))
 d=ImageDraw.Draw(im,"RGBA")
 for x in range(60,1600,90):d.line((x,0,x,900),fill=(64,158,183,19),width=1)
 for y in range(0,900,90):d.line((0,y,1600,y),fill=(64,158,183,19),width=1)
 d.rounded_rectangle((36,85,876,805),radius=37,fill=(10,36,53,225),outline=(*C,160),width=4)
 d.ellipse((130,705,800,797),fill=(0,0,0,105))
 d.rounded_rectangle((904,88,1559,798),radius=29,fill=(3,17,31,247),outline=(*C,230),width=4)
 d.rounded_rectangle((935,125,1525,318),radius=20,fill=(11,46,68,255),outline=(*C,215),width=3)
 d.text((1496,144),code,font=font(144),fill=(244,251,254,255),anchor="ra")
 d.rounded_rectangle((1068,340,1507,356),radius=7,fill=(*C,255))
 d.text((1495,420),line1,font=font(43),fill=(251,196,98,255),anchor="ra",direction="rtl")
 d.text((1495,497),line2,font=font(38),fill=(244,251,253,255),anchor="ra",direction="rtl")
 d.rounded_rectangle((939,634,1515,728),radius=15,fill=(16,50,65,253))
 d.text((1479,665),foot,font=font(27),fill=(204,235,243,255),anchor="ra",direction="rtl")
 d.text((1485,754),"أعطال.كوم",font=font(23),fill=(*C,255),anchor="ra",direction="rtl")
 def bolt(x,y,r=18):
  d.ellipse((x-r,y-r,x+r,y+r),fill=(64,80,92,255),outline=(224,234,238,255),width=5)
  d.ellipse((x-5,y-5,x+5,y+5),fill=(17,31,42,255))
 def hole(x,y):
  d.ellipse((x-10,y-10,x+10,y+10),fill=(6,16,26,255),outline=(142,163,166,255),width=3)
 def tube(points,color=(103,136,146,255),width=65):
  stroke(d,points,(13,23,31,255),width+19)
  stroke(d,points,color,width)
  stroke(d,points,(201,222,226,164),max(3,width//12))
 if kind=="intake":
  # Corrugated intake / MAF housing; tiny leak marker.
  tube([(88,434),(292,434),(374,410),(666,410)],width=130)
  d.rounded_rectangle((356,302,562,530),radius=30,fill=(35,52,59,255),outline=(200,219,224,255),width=7)
  d.rectangle((398,330,506,495),fill=(46,84,92,255))
  for x in range(401,507,14):stroke(d,(x,336,x,490),(159,199,208,245),3)
  poly(d,[(590,337),(633,310),(651,381),(601,409)],(43,75,89,255))
  bolt(377,354);bolt(544,478)
  for i in range(7):stroke(d,(678+i*14,377,701+i*14,361),(*C,180),5)
  d.ellipse((678,381,746,445),outline=(243,173,72,255),width=10)
  d.text((154,226),"MAF / AIR INTAKE",font=font(25),fill=(*C,255))
 elif kind=="ignition":
  # Tall coil-on-plug and spark plug, number one cylinder.
  d.rounded_rectangle((292,180,488,461),radius=35,fill=(29,41,51,255),outline=(152,183,195,255),width=8)
  d.rounded_rectangle((323,230,456,410),radius=17,fill=(38,67,81,255))
  d.rounded_rectangle((340,440,439,669),radius=25,fill=(83,91,92,255),outline=(219,220,211,255),width=7)
  for y in range(475,611,13):stroke(d,(330,y,453,y),(210,204,188,200),3)
  poly(d,[(332,671),(371,708),(410,672),(408,626),(340,626)],(158,173,168,255))
  d.polygon([(305,165),(481,165),(474,215),(314,216)],fill=(23,42,53,255))
  stroke(d,(435,170,558,142,624,184),(12,20,26,255),36)
  bolt(306,208);bolt(475,207)
  d.ellipse((572,388,695,511),fill=(11,37,53,255),outline=(*C,255),width=8)
  d.text((632,397),"1",font=font(72),fill=(255,244,211,255),anchor="ma")
 elif kind in ("evap_small","evap_large"):
  d.rounded_rectangle((147,346,653,695),radius=49,fill=(37,77,84,255),outline=(165,209,218,255),width=9)
  d.rectangle((300,265,480,354),fill=(61,84,95,255),outline=(177,206,213,255),width=8)
  d.ellipse((271,207,511,294),fill=(48,61,71,255),outline=(220,233,234,255),width=8)
  for k in range(8):stroke(d,(305+k*23,212,305+k*23,262),(152,169,177,255),5)
  tube([(654,501),(758,502),(801,450)],(97,134,141,255),width=34)
  bolt(235,400);bolt(586,632)
  n=4 if kind=="evap_small" else 12
  for i in range(n):
   x=742+(i%3)*18;y=320-(i//3)*19
   d.ellipse((x-5,y-5,x+5,y+5),fill=(*C,200))
  d.arc((668,290,829,485),start=205,end=318,fill=(255,179,82,240),width=10)
  d.text((107,223),"EVAP",font=font(37),fill=(*C,255))
 elif kind=="thermostat":
  d.ellipse((225,228,646,646),fill=(52,80,92,255),outline=(209,224,229,255),width=15)
  d.ellipse((289,281,587,585),fill=(11,34,43,255),outline=(184,197,201,255),width=13)
  d.ellipse((333,332,542,534),fill=(152,169,171,255),outline=(227,229,223,255),width=8)
  for i in range(8):
   x=358+i*21
   stroke(d,(x,440,x+14,440-30*(-1)**i),(103,116,120,255),12)
  poly(d,[(366,368),(506,368),(530,427),(508,481),(365,481),(343,423)],(154,173,165,255))
  for x,y in [(255,274),(607,285),(286,585),(586,590)]:bolt(x,y)
  tube([(210,557),(105,624)],(84,131,159,255),width=40)
  d.text((118,200),"THERMOSTAT",font=font(29),fill=(*C,255))
 elif kind=="egr":
  d.ellipse((209,313,674,667),fill=(75,101,113,255),outline=(210,228,229,255),width=14)
  d.ellipse((318,396,566,581),fill=(10,23,34,255),outline=(166,188,193,255),width=8)
  d.rounded_rectangle((318,168,571,343),radius=29,fill=(42,56,63,255),outline=(201,219,222,255),width=10)
  d.rounded_rectangle((365,113,526,189),radius=18,fill=(17,42,58,255),outline=(150,204,219,255),width=7)
  tube([(661,520),(811,525)],(130,157,151,255),width=73)
  for x,y in [(246,376),(631,379),(275,615),(627,612)]:bolt(x,y)
  stroke(d,(362,487,527,488),(*C,160),12)
  d.text((132,221),"EGR VALVE",font=font(28),fill=(*C,255))
 elif kind=="o2":
  tube([(652,358),(775,300),(800,198)],(48,65,75,255),width=35)
  d.rounded_rectangle((285,359,660,480),radius=40,fill=(132,154,161,255),outline=(221,230,232,255),width=9)
  poly(d,[(357,322),(450,321),(494,410),(455,526),(357,527),(321,412)],(148,165,164,255))
  d.rounded_rectangle((150,372,294,468),radius=36,fill=(164,178,179,255),outline=(236,237,229,255),width=9)
  for x in [177,218,261]:
   for y in [398,446]:hole(x,y)
  for x in range(503,600,14):stroke(d,(x,350,x-19,487),(233,228,207,190),4)
  d.rounded_rectangle((708,154,853,259),radius=18,fill=(18,31,40,255),outline=(128,158,173,255),width=8)
  d.text((131,258),"O2 SENSOR B1S2",font=font(25),fill=(*C,255))
 elif kind=="maf":
  tube([(135,427),(735,426)],(61,88,94,255),width=154)
  d.rounded_rectangle((312,304,591,550),radius=40,fill=(42,67,74,255),outline=(208,228,230,255),width=10)
  for y in range(342,517,24):stroke(d,(342,y,560,y),(141,178,180,255),5)
  for x in range(345,564,24):stroke(d,(x,339,x,517),(141,178,180,255),5)
  d.rounded_rectangle((393,176,502,313),radius=20,fill=(28,44,56,255),outline=(158,199,211,255),width=8)
  d.rounded_rectangle((413,196,482,254),radius=10,fill=(10,21,34,255))
  d.line((687,299,813,299),fill=(*C,220),width=8)
  poly(d,[(810,279),(851,300),(812,321)],(*C,255))
  d.text((131,219),"MAF SENSOR",font=font(30),fill=(*C,255))
 elif kind=="timing":
  def gear(cx,cy,R):
   for i in range(18):
    a=2*math.pi*i/18
    xx=cx+math.cos(a)*R;yy=cy+math.sin(a)*R
    d.ellipse((xx-19,yy-19,xx+19,yy+19),fill=(132,149,154,255))
   d.ellipse((cx-R+13,cy-R+13,cx+R-13,cy+R-13),fill=(107,125,135,255),outline=(225,230,231,255),width=10)
   d.ellipse((cx-55,cy-55,cx+55,cy+55),fill=(12,32,45,255),outline=(*C,255),width=8)
   bolt(cx,cy,23)
  gear(310,372,133);gear(671,552,100)
  stroke(d,(314,237,682,450),(210,176,99,255),17)
  stroke(d,(322,498,660,670),(210,176,99,255),17)
  for x,y in [(390,269),(476,303),(571,358),(390,537),(490,585),(580,628)]:
   d.rounded_rectangle((x-15,y-10,x+15,y+10),radius=3,fill=(239,207,128,255))
  d.text((143,194),"CAM / CRANK",font=font(29),fill=(*C,255))
 # Visual disclaimer in the bottom margin.
 d.text((60,845),"رسم أصلي توضيحي: افحص الدائرة والمنظومة قبل تغيير القطعة",font=font(21,False),fill=(165,188,197,255),direction="rtl")
 out=Path("assets/dtc-batch39");out.mkdir(parents=True,exist_ok=True)
 path=out/("a3tal-dtc-"+code.lower()+"-exclusive-ar.webp")
 im.save(path,"WEBP",quality=86,method=6)
 with Image.open(path) as ck:
  assert ck.format=="WEBP" and ck.size==(1600,900)
 print("DTC39_IMAGE_RENDERED",code,str(path),"bytes",path.stat().st_size,"SHA256",hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
 return path
if __name__=="__main__":
 if len(sys.argv)!=2 or sys.argv[1] not in DATA:raise SystemExit("Specify one supported code")
 diag(sys.argv[1])
