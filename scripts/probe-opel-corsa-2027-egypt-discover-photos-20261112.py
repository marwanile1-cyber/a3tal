#!/usr/bin/env python3
import requests,io,hashlib
from PIL import Image
urls=["https://www.opelegypt.net/content/dam/opel/egypt/vehicles/corsa/corsa-my21/my25/banner-image-corsa-D.png?imwidth=1920","https://www.opelegypt.net/en/cars/new-corsa/overview-features/_jcr_content/pageContent/grid_builder_v2_8506/col1/grid_builder_v2_copy/col1/tiled_gallery/item_1686921267926.coreimg.jpeg/1690195058917/opel-corsa-ice-exterior-roof-16x9-cosol23-e01-003.jpeg","https://www.opelegypt.net/en/cars/new-corsa/overview-features/_jcr_content/pageContent/grid_builder_v2_8506/col1/grid_builder_v2_copy/col1/tiled_gallery/item_1686919445177.coreimg.jpeg/1710682157421/cosol23-e01-007-edit-copy.jpeg","https://www.opelegypt.net/content/dam/opel/egypt/vehicles/corsa/corsa-my21/my25/Car-Side-Image.png?imwidth=1920","https://www.opelegypt.net/content/dam/opel/egypt/vehicles/corsa/corsa-my21/my25/Red.png"]
urls.extend(["https://ellaithy.com.eg/wp-content/uploads/2026/11/1794376474_361_90456_opelcorsa2027toplineplusexterior.webp","https://www.almansour.com.eg/assets/media/NewCorsa.jpg","https://www.almansour.com.eg/assets/media/NewCorsa2.jpg","https://www.almansour.com.eg/assets/media/NewCorsa3.jpg","https://www.almansour.com.eg/assets/media/NewCorsa4.jpg"])
for u in urls:
 try:
  r=requests.get(u,timeout=28,headers={"User-Agent":"Mozilla/5.0","Accept":"image/avif,image/webp,image/apng,image/*,*/*;q=0.8"});r.raise_for_status()
  data=r.content;img=Image.open(io.BytesIO(data))
  print("CORSA_OFFICIAL_IMAGE",u,"NATIVE",img.size,"MODE",img.mode,"BYTES",len(data),"SHA",hashlib.sha256(data).hexdigest()[:16],flush=True)
 except Exception as e:print("CORSA_IMAGE_ERROR",u,str(e)[:140],flush=True)
