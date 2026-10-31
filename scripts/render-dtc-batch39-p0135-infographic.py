#!/usr/bin/env python3
"""Create one original Arabic Google Images-first P0135 technical illustration.
No reused source photos and no external image dependencies.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, features
from pathlib import Path
from math import sin, cos, pi
import hashlib, json, io, os
W,H=1600,900
OUT=Path("assets/dtc-batch39")
OUT.mkdir(parents=True,exist_ok=True)
TARGET=OUT/"a3tal-dtc-p0135-original-ar.webp"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
assert os.path.isfile(FONT), "Arabic font unavailable"
def f(n,bold=True):return ImageFont.truetype(FONT if bold else REG,n)
bg=Image.new("RGB",(W,H))
pix=bg.load()
for y in range(H):
 for x in range(W):
  glow=max(0,1-((x-450)**2/(850**2)+(y-450)**2/(700**2))**.5)
  pix[x,y]=(int(5+8*glow+y*.004),int(17+21*glow+y*.004),int(31+33*glow+y*.005))
d=ImageDraw.Draw(bg,"RGBA")
# Subtle engineering grid.
for x in range(0,W,80):d.line((x,0,x,H),fill=(80,158,183,13),width=1)
for y in range(0,H,80):d.line((0,y,W,y),fill=(80,158,183,13),width=1)
# Sensor presentation platform.
d.rounded_rectangle((36,79,866,805),radius=40,fill=(8,35,52,188),outline=(30,184,214,115),width=3)
d.ellipse((106,700,815,820),fill=(0,0,0,105))
# Multi-layer realistic sensor visual, from tip to harness at right.
# Outline/surface of metallic oxygen-sensor element at angle.
layer=Image.new("RGBA",(920,530),(0,0,0,0));s=ImageDraw.Draw(layer,"RGBA")
# Cable bend and strain relief behind sensor.
s.arc((522,108,935,455),start=189,end=306,fill=(4,8,14,255),width=54)
s.arc((522,111,938,450),start=189,end=306,fill=(24,42,55,255),width=27)
for t in range(21):
 x=680+t*9
 y=160+int(21*sin(t/5))
 s.line((x,y,x+5,y+12),fill=(95,116,124,130),width=3)
# Connector and protective black cover, diagonal right.
s.rounded_rectangle((714,165,861,295),radius=22,fill=(14,25,31,255),outline=(89,113,125,255),width=7)
s.rounded_rectangle((794,180,880,279),radius=15,fill=(20,35,43,255),outline=(83,115,129,255),width=5)
s.rounded_rectangle((818,203,870,260),radius=8,fill=(4,10,17,255))
for i in range(3):
 s.rectangle((827+i*13,219,835+i*13,236),fill=(170,176,158,255))
# Cylindrical oxygen sensor body (left tip at x=70).
s.rounded_rectangle((89,205,625,338),radius=43,fill=(83,96,103,255),outline=(198,215,220,255),width=6)
for j in range(115):
 y=209+j
 k=int(55+125*max(0,sin((j/114)*pi)))
 s.line((175,y,610,y),fill=(k,k+5,k+8,232),width=1)
# Flat metal ring and hex washer.
s.rectangle((356,177,405,361),fill=(142,153,157,255),outline=(222,228,228,255),width=4)
s.polygon([(405,189),(480,189),(516,257),(481,344),(405,344),(367,257)],fill=(125,144,150,255),outline=(220,230,234,255),width=8)
s.polygon([(415,207),(473,207),(497,257),(471,327),(415,327),(385,257)],fill=(76,89,95,255))
for i in range(9):
 x=203+i*16
 s.line((x,199,x-24,343),fill=(216,222,214,150),width=4)
# Steel sensing tip with vent perforations.
s.rounded_rectangle((48,225,200,321),radius=39,fill=(156,168,171,255),outline=(227,235,231,255),width=6)
for i in range(3):
 for j in range(2):
  cx=79+i*39;cy=249+j*44
  s.ellipse((cx-7,cy-7,cx+7,cy+7),fill=(35,44,48,255),outline=(89,100,100,255),width=2)
# Brown heat discoloration bands, not a diagnosis of sensor failure.
s.rectangle((180,214,196,335),fill=(143,111,79,84))
s.rectangle((608,214,626,329),fill=(30,43,50,220))
sensor=layer.rotate(13,resample=Image.Resampling.BICUBIC,expand=True)
bg.paste(sensor,(6,205),sensor)
d=ImageDraw.Draw(bg,"RGBA")
# Thin technical callout lines/labels.
d.line((270,260,350,165,535,165),fill=(36,211,238,230),width=4)
d.ellipse((261,250,277,266),fill=(35,214,239,255))
d.text((547,143),"O2 / HO2S",font=f(29),fill=(179,233,246,255))
d.line((620,640,720,717,816,717),fill=(242,177,62,205),width=4)
d.text((814,728),"HEATER CIRCUIT",font=f(22),fill=(244,193,90,255),anchor="ra")
# Main right-side title plate, exact code and fault.
d.rounded_rectangle((885,91,1552,801),radius=31,fill=(3,17,31,230),outline=(21,212,229,215),width=4)
d.rounded_rectangle((919,123,1515,317),radius=20,fill=(10,44,68,255),outline=(41,211,228,240),width=3)
d.text((1484,151),"P0135",font=f(147),fill=(239,250,255,255),anchor="ra")
d.rounded_rectangle((1035,334,1496,351),radius=7,fill=(247,168,48,255))
d.text((1492,403),"خلل دائرة سخان",font=f(47),fill=(255,196,91,255),anchor="ra",direction="rtl")
d.text((1492,484),"حساس الأكسجين",font=f(48),fill=(249,252,253,255),anchor="ra",direction="rtl")
d.text((1492,555),"الأمامي B1S1",font=f(39),fill=(110,220,238,255),anchor="ra",direction="rtl")
d.rounded_rectangle((922,641,1513,731),radius=14,fill=(21,49,64,255))
d.text((1483,666),"افحص الفيوز والفيشة قبل التغيير",font=f(27),fill=(226,239,246,255),anchor="ra",direction="rtl")
d.text((1468,761),"أعطال.كوم",font=f(22),fill=(121,187,202,255),anchor="ra",direction="rtl")
d.text((55,844),"رسم فني توضيحي لشكل الحساس — الكود لا يثبت تلف القطعة وحدها",font=f(21,False),fill=(174,197,210,255),direction="rtl")
bg.save(TARGET,"WEBP",quality=86,method=6)
with Image.open(TARGET) as im:
 assert im.size==(1600,900) and im.format=="WEBP"
print("DTC39_ORIGINAL_IMAGE_OK",TARGET,TARGET.stat().st_size,"SHA256",hashlib.sha256(TARGET.read_bytes()).hexdigest(),flush=True)
