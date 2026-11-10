#!/usr/bin/env python3
"""Probe exact official Jetour Egypt X90 Plus manufacturer photo native dimensions."""
import io,hashlib,requests
from PIL import Image
names=["bannerDesc.jpg","1.jpg","2.jpg","3.jpg","car1.jpg","car2.jpg","car3.jpg","car4.jpg","car5.jpg","slidertwo1.jpg","slidertwo2.jpg","slidertwo3.jpg","slidertwo4.jpg","slidertwo5.jpg","technology2.jpg","technology3.jpg"]
base="https://jetouregypt.com/models/x90-plus-1-6t/new_assets/images/"
for name in names:
    try:
        r=requests.get(base+name,timeout=24);r.raise_for_status()
        raw=r.content;im=Image.open(io.BytesIO(raw))
        print("JETOUR_X90_IMAGE_PROBE",name,im.size,im.mode,len(raw),hashlib.sha256(raw).hexdigest()[:14],flush=True)
    except Exception as e:
        print("JETOUR_X90_IMAGE_ERROR",name,type(e).__name__,str(e)[:120],flush=True)
