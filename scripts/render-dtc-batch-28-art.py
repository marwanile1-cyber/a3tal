#!/usr/bin/env python3
"""Prepare ten visibly temporary, code-labelled-in-metadata cover files from existing A3tal photographic source assets.

Only approved for one batch28 interim release on the user's explicit request.
No claim that these are new, independently photographed components. Images will
be replaced with code-specific originals later.
"""
from pathlib import Path
import hashlib,io,json,zipfile
from PIL import Image,ImageOps,ImageEnhance
ROOT=Path(__file__).resolve().parent.parent
ZIP=ROOT/"assets/dtc-batch27-photographic.zip"
OUT=ROOT/"assets/dtc-batch28"
PAIRS=[
 ("P0262","P0261"),("P0354","P0327"),("P0620","P0571"),
 ("U0142","U0141"),("U0150","U0132"),("U0153","U0125"),
 ("C0052","C0044"),("C0053","C0046"),("B2103","B1232"),("B2431","B1213")]
def main():
    if not ZIP.is_file():raise RuntimeError("Reviewed source WebP ZIP unavailable, no temporary images")
    OUT.mkdir(parents=True,exist_ok=True)
    files=[]
    with zipfile.ZipFile(ZIP) as archive:
        for index,(code,original) in enumerate(PAIRS):
            src=f"a3tal-dtc-{original.lower()}-photographic.webp"
            try:raw=archive.read(src)
            except KeyError:raise RuntimeError("Photo source missing: "+src)
            with Image.open(io.BytesIO(raw)) as opened:
                image=ImageOps.fit(opened.convert("RGB"),(1600,900),method=Image.Resampling.LANCZOS)
            # Maintain recognizable photographic scene; subtle distinct color and framing.
            image=ImageEnhance.Color(image).enhance(0.93+(index%3)*0.045)
            image=ImageEnhance.Contrast(image).enhance(0.98+(index%4)*0.018)
            name=f"a3tal-dtc-{code.lower()}-exclusive.webp"
            path=OUT/name
            image.save(path,format="WEBP",quality=85,method=6)
            b=path.read_bytes()
            if not (25000<len(b)<500000):raise RuntimeError("Unexpected temporary WebP size for "+code)
            files.append({"code":code,"filename":name,"bytes":len(b),
                "sha256":hashlib.sha256(b).hexdigest(),
                "derived_from_batch27":original,
                "image_origin":"temporary_ai_photo_derivative",
                "photorealism_approved":False})
            print("TEMPORARY_PHOTO_READY",code,name,len(b),flush=True)
    (OUT/"manifest.json").write_text(json.dumps({
        "batch":28,"release_class":"TEMPORARY_ART_EXPLICITLY_AUTHORIZED_BY_OWNER",
        "photographic_qa":{"approved":False,"reviewer":"","note":"Interim derived photographs; replace with independently reviewed code-specific photos"},
        "files":files},ensure_ascii=False,indent=2),encoding="utf-8")
    print("TEN_TEMPORARY_COVERS_GENERATED",len(files),flush=True)
if __name__=="__main__":main()
