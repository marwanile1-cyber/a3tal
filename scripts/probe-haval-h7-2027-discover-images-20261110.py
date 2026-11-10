#!/usr/bin/env python3
import io,requests,hashlib
from PIL import Image
urls=["https://greatwall.eg/media/images/Haval_H7_car_img_2026-05-12_153240.143306.png","https://greatwall.eg/media/car360images/h7_black.png","https://greatwall.eg/media/extDesignImages/h7_black_edition_exterior_.jpg","https://greatwall.eg/media/extDesignImages/h7_black_edition_exterior_1.jpg","https://greatwall.eg/media/car-performance-images/performance_black_edition_H7.jpg","https://greatwall.eg/media/car-performance-mobile-images/performance_black_edition_H71.jpg"]
for u in urls:
 try:
  r=requests.get(u,timeout=28,headers={"User-Agent":"Mozilla/5.0 (compatible; A3talImageQA/1.0)"});r.raise_for_status()
  b=r.content;im=Image.open(io.BytesIO(b))
  print("HAVAL_H7_OFFICIAL_PHOTO_QA",u,im.size,im.mode,len(b),hashlib.sha256(b).hexdigest()[:14],flush=True)
 except Exception as e:print("HAVAL_H7_OFFICIAL_PHOTO_FAILED",u,type(e).__name__,str(e)[:140],flush=True)
