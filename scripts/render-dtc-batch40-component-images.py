#!/usr/bin/env python3
"""Original, explanatory Arabic 1600x900 WebP art for DTC40.
One component-specific vector illustration per code, with exact code and diagnostic name.
No external photographs or assets. A diagram never claims to prove a component faulty.
"""
import sys,math,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
DATA={
"P0070":("عطل دائرة حساس","حرارة الهواء الخارجي","ambient","افحص الحساس والفيشة"),
"P0093":("تسريب كبير بمنظومة","ضغط وتغذية الوقود","fuel","تحقق من التسريب بأمان"),
"P0222":("إشارة منخفضة لحساس","البوابة أو الدعسة B","throttle","فحص الجهد المرجعي والإشارة"),
"P0299":("ضغط التيربو أقل","من القيمة المطلوبة","turbo","افحص الخراطيم والتحكم"),
"P0507":("ارتفاع دوران المحرك","أثناء السلانسيه","idle","افحص بوابة الهواء والتسريب"),
"P0520":("عطل دائرة حساس","ضغط زيت المحرك","oil","تحقق من الضغط الحقيقي أولًا"),
"P0562":("جهد كهرباء السيارة","أقل من المطلوب","charge","افحص البطارية والدينامو"),
"P0710":("عطل دائرة حساس","حرارة زيت الفتيس","atf","فحص حرارة وموصل الفتيس"),
"P0741":("ضعف أداء قفل","محول عزم الفتيس","torque","فحص TCC والزيت والانزلاق"),
"P0444":("دائرة صمام تبخير","الوقود مفتوحة","evap","افحص صمام Purge والفيشة")
}
COLORS={"ambient":(75,219,236),"fuel":(248,169,94),"throttle":(79,198,223),"turbo":(249,177,83),"idle":(95,220,213),"oil":(244,185,75),"charge":(94,194,239),"atf":(138,199,239),"torque":(242,179,89),"evap":(94,232,188)}
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
 if kind=="ambient":
  # Compact outside-air thermistor with grille and two-pin connector.
  d.rounded_rectangle((255,245,574,613),radius=42,fill=(39,56,70,255),outline=(215,235,239,255),width=9)
  d.rounded_rectangle((325,173,502,287),radius=20,fill=(19,38,50,255),outline=(*C,255),width=7)
  for k in range(5):stroke(d,(295,334+k*48,533,334+k*48),(142,177,185,255),10)
  for k in range(4):stroke(d,(317+k*59,316,317+k*59,545),(97,142,156,230),6)
  d.ellipse((365,382,466,493),fill=(13,34,45,255),outline=(*C,250),width=8)
  d.ellipse((406,412,425,443),fill=(248,184,93,255))
  stroke(d,(620,377,745,321),(*C,220),9)
  d.text((142,199),"AMBIENT TEMP",font=font(29),fill=(*C,255))
 elif kind=="fuel":
  # Common-rail pressure manifold and fuel feed fitting; diagram, not live leak.
  d.rounded_rectangle((153,335,702,459),radius=38,fill=(106,127,140,255),outline=(216,234,239,255),width=10)
  for k in range(4):
   x=230+k*133
   d.rounded_rectangle((x,449,x+39,639),radius=12,fill=(45,73,90,255),outline=(205,218,221,255),width=6)
   bolt(x+19,481,12)
  d.rounded_rectangle((332,251,486,330),radius=19,fill=(19,45,62,255),outline=(*C,255),width=7)
  stroke(d,(700,391,788,392),(229,211,181,255),45)
  poly(d,[(777,337),(826,363),(824,415),(776,446)],(94,110,120,255))
  d.arc((719,244,824,343),start=35,end=284,fill=(*C,235),width=8)
  d.text((144,215),"FUEL RAIL",font=font(29),fill=(*C,255))
 elif kind in ("throttle","idle"):
  # Physical throttle housing with motor and butterfly plate, not a generic MAF.
  d.ellipse((220,248,662,666),fill=(107,126,138,255),outline=(223,234,236,255),width=18)
  d.ellipse((291,315,591,597),fill=(15,34,47,255),outline=(181,203,212,255),width=14)
  poly(d,[(301,454),(571,371),(596,453),(309,535)],(117,143,154,255),width=7)
  d.ellipse((393,398,490,496),fill=(44,66,80,255),outline=(*C,255),width=8)
  d.rounded_rectangle((599,365,807,568),radius=31,fill=(27,47,60,255),outline=(*C,255),width=9)
  for x,y in [(241,295),(633,291),(273,619),(628,624)]:bolt(x,y)
  d.text((135,192),"THROTTLE BODY",font=font(28),fill=(*C,255))
  if kind=="throttle":d.text((643,581),"TPS B",font=font(27),fill=(*C,255))
  else:
   stroke(d,(674,253,725,183,788,254),(243,183,77,240),9)
   d.text((693,188),"RPM",font=font(29),fill=(253,185,86,255))
 elif kind=="turbo":
  # Compressor snail and actuator including intake/outlet compressor ducts.
  d.ellipse((191,268,671,684),fill=(124,147,157,255),outline=(225,236,235,255),width=16)
  d.ellipse((279,339,563,600),fill=(15,40,55,255),outline=(194,218,221,255),width=11)
  for i in range(8):
   a=2*math.pi*i/8;x=419+math.cos(a)*92;y=467+math.sin(a)*92
   poly(d,[(417,467),(int(x),int(y)),(int(419+math.cos(a+.4)*108),int(467+math.sin(a+.4)*108))],(103,176,194,255),width=2)
  d.ellipse((396,441,439,485),fill=(*C,255))
  tube([(647,373),(739,374),(790,321)],(116,153,169,255),width=64)
  d.rounded_rectangle((629,618,789,683),radius=19,fill=(24,46,60,255),outline=(*C,255),width=6)
  stroke(d,(663,618,572,577),(215,232,230,240),9)
  d.text((136,204),"TURBO BOOST",font=font(30),fill=(*C,255))
 elif kind=="oil":
  # Pressure sender threaded into engine oil gallery; wiring pin.
  d.rounded_rectangle((258,243,577,459),radius=47,fill=(94,116,127,255),outline=(223,234,236,255),width=11)
  d.rounded_rectangle((335,159,507,279),radius=24,fill=(20,46,63,255),outline=(*C,255),width=8)
  poly(d,[(303,454),(531,454),(558,520),(529,577),(304,577),(273,520)],(139,159,163,255))
  d.rounded_rectangle((354,570,478,687),radius=11,fill=(172,182,176,255),outline=(238,237,217,255),width=6)
  for y in range(591,678,15):stroke(d,(355,y,475,y),(98,110,111,255),4)
  d.ellipse((375,302,464,393),fill=(17,42,58,255),outline=(*C,255),width=7)
  d.text((134,207),"OIL PRESSURE",font=font(29),fill=(*C,255))
 elif kind=="charge":
  # Automotive alternator with pulley and adjacent battery.
  d.ellipse((122,242,581,689),fill=(81,107,124,255),outline=(221,232,239,255),width=13)
  d.ellipse((215,320,488,591),fill=(13,38,57,255),outline=(*C,255),width=8)
  for k in range(12):
   a=2*math.pi*k/12
   x1=352+math.cos(a)*53;y1=455+math.sin(a)*53
   x2=352+math.cos(a)*126;y2=455+math.sin(a)*126
   stroke(d,(x1,y1,x2,y2),(159,192,203,255),15)
  d.ellipse((294,394,411,511),fill=(53,80,98,255),outline=(230,238,239,255),width=11)
  d.rounded_rectangle((606,353,829,631),radius=18,fill=(31,55,72,255),outline=(216,235,240,255),width=9)
  d.rectangle((645,321,683,357),fill=(*C,255))
  d.rectangle((749,321,788,357),fill=(*C,255))
  d.text((639,380),"+",font=font(50),fill=(250,211,125,255))
  d.text((730,381),"-",font=font(50),fill=(230,237,239,255))
  d.text((132,194),"CHARGING SYSTEM",font=font(25),fill=(*C,255))
 elif kind=="atf":
  # Transmission fluid thermistor probe mounted at valve body.
  d.rounded_rectangle((146,278,714,646),radius=48,fill=(65,87,105,255),outline=(192,219,230,255),width=14)
  for k in range(5):
   y=335+k*60
   stroke(d,(194,y,654,y),(114,155,171,255),12)
  d.rounded_rectangle((350,189,480,482),radius=23,fill=(23,46,62,255),outline=(*C,255),width=8)
  d.rounded_rectangle((372,402,460,549),radius=21,fill=(170,185,184,255),outline=(238,239,232,255),width=8)
  d.ellipse((388,497,445,563),fill=(*C,235))
  d.text((126,214),"ATF TEMP SENSOR",font=font(26),fill=(*C,255))
 elif kind=="torque":
  # Clutch pack within a torque converter circular housing.
  d.ellipse((190,200,700,718),fill=(82,110,127,255),outline=(226,231,233,255),width=15)
  d.ellipse((248,263,643,659),fill=(22,43,56,255),outline=(186,211,219,255),width=13)
  for i in range(9):
   a=2*math.pi*i/9
   xx=444+math.cos(a)*133;yy=461+math.sin(a)*133
   d.ellipse((xx-29,yy-29,xx+29,yy+29),fill=(129,158,166,255),outline=(*C,255),width=4)
  d.ellipse((356,374,533,552),fill=(108,129,138,255),outline=(229,236,233,255),width=11)
  d.ellipse((410,430,477,495),fill=(18,44,57,255),outline=(*C,255),width=9)
  d.text((115,177),"TORQUE CONVERTER",font=font(26),fill=(*C,255))
 elif kind=="evap":
  # Vacuum purge valve with hose nipples and electrical connector.
  d.rounded_rectangle((235,328,613,563),radius=59,fill=(34,62,75,255),outline=(212,229,237,255),width=9)
  d.rounded_rectangle((121,384,244,501),radius=19,fill=(73,108,119,255),outline=(191,218,219,255),width=7)
  d.rounded_rectangle((603,374,816,515),radius=22,fill=(65,94,103,255),outline=(197,223,223,255),width=7)
  d.rounded_rectangle((345,227,515,341),radius=25,fill=(16,37,51,255),outline=(*C,255),width=8)
  for x in range(365,496,28):stroke(d,(x,254,x,305),(168,206,212,255),5)
  d.text((123,203),"EVAP PURGE VALVE",font=font(26),fill=(*C,255))
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
 out=Path("assets/dtc-batch40");out.mkdir(parents=True,exist_ok=True)
 path=out/("a3tal-dtc-"+code.lower()+"-exclusive-ar.webp")
 im.save(path,"WEBP",quality=86,method=6)
 with Image.open(path) as ck:
  assert ck.format=="WEBP" and ck.size==(1600,900)
 print("DTC40_IMAGE_RENDERED",code,str(path),"bytes",path.stat().st_size,"SHA256",hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
 return path
if __name__=="__main__":
 if len(sys.argv)!=2 or sys.argv[1] not in DATA:raise SystemExit("Specify one supported code")
 diag(sys.argv[1])
