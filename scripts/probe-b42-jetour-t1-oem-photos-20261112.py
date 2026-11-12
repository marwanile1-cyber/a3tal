#!/usr/bin/env python3
import hashlib,io,requests
from PIL import Image
names=["7_1.jpg","7_2.jpg","4-1.jpg","4-2.jpg","4-4.jpg","5-2.jpg","5-3.jpg","5-4.jpg","Silver-car.png","White-car.png","Gold-car.png","Black-car.png"]
base="https://jetouregypt.com/models/T1/new_assets/images/carModel/t1/"
extra=[
"https://jetouregypt.com/img/cars/T1.png",
"https://jetouregypt.com/img/cars/T1-Black1.png",
"https://jetouregypt.com/models/T1/new_assets/images/carModel/t1/4-1_m.jpg",
"https://jetouregypt.com/models/T1/new_assets/images/carModel/t1/4-2_m.jpg",
"https://jetouregypt.com/models/T1/new_assets/images/carModel/t1/4-4_m.jpg",
"https://jetouregypt.com/models/T1/new_assets/images/carModel/t1/5-2_m.jpg",
"https://jetouregypt.com/models/T1/new_assets/images/carModel/t1/5-3_m.jpg",
"https://jetouregypt.com/models/T1/new_assets/images/carModel/t1/5-4_m.jpg"]
for name in names+extra:
 try:
  r=requests.get(name if name.startswith("https://") else base+name,timeout=30);r.raise_for_status()
  b=r.content;im=Image.open(io.BytesIO(b))
  print("JETOUR_T1_PHOTO_PROBE",name,im.size,im.mode,len(b),hashlib.sha256(b).hexdigest()[:14],flush=True)
 except Exception as exc:
  print("JETOUR_T1_PHOTO_FAILED",name,type(exc).__name__,str(exc)[:150],flush=True)
