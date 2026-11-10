#!/usr/bin/env python3
"""Inspect exact MG RX9 PHEV official gallery native photo dimensions before PSEO publishing."""
import io,hashlib,requests
from PIL import Image
paths=["2026/09/e148a83ac6ddefb0e92e9cebfe131595.webp","2026/08/RX9-Side-1-Photoroom-1.webp","2026/08/MG_RX9-High-Res-57-2_11zon-1.webp","2026/08/MG_RX9-High-Res-69-1-1.webp","2026/06/MG_RX9-High-Res-55-1.webp","2026/06/MG_RX9-High-Res-57-1.webp","2026/06/MG_RX9-High-Res-58-1.webp","2026/06/MG_RX9-High-Res-59-1.webp","2026/06/MG_RX9-High-Res-60-1.webp","2026/06/MG_RX9-High-Res-84-1.webp","2026/06/MG_RX9-High-Res-34-1.webp","2026/06/MG_RX9-High-Res-42-1.webp","2026/06/MG_RX9-High-Res-70-1.webp","2026/06/MG_RX9-High-Res-71-1.webp","2026/06/MG_RX9-High-Res-73-1.webp","2026/06/MG_RX9-High-Res-77-1.webp","2026/06/MG_RX9-High-Res-80-1.webp","2026/06/MG_RX9-High-Res-81-1.webp"]
s=requests.Session()
s.headers.update({"User-Agent":"A3tal-Genuine-Model-Photo-Preflight/1.0"})
for p in paths:
    url="https://www.mgmotor.com.eg/wp-content/uploads/"+p
    try:
        r=s.get(url,timeout=24);r.raise_for_status()
        raw=r.content;im=Image.open(io.BytesIO(raw))
        print("MG_RX9_IMAGE_PROBE",p,im.size,im.mode,len(raw),hashlib.sha256(raw).hexdigest()[:12],flush=True)
    except Exception as e:
        print("MG_RX9_IMAGE_PROBE_ERROR",p,type(e).__name__,str(e)[:160],flush=True)
