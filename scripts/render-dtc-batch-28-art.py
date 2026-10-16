#!/usr/bin/env python3
"""Unpack ONLY pre-reviewed standalone batch28 1600x900 WebP photos.
No Pillow drawings, no fallback covers, no invented photographic provenance.
Input: assets/dtc-batch28-photographic.zip with 10 code-specific WebPs and manifest.
"""
import hashlib,io,json,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
PACK=ROOT/"assets/dtc-batch28-photographic.zip"
OUT=ROOT/"assets/dtc-batch28"
CODES="P0262 P0354 P0620 U0142 U0150 U0153 C0052 C0053 B2103 B2431".split()
def main():
    if not PACK.is_file():raise RuntimeError("No batch28 reviewed 10-photo ZIP; do not publish or synthesize a fallback")
    with zipfile.ZipFile(PACK) as z:
        entries=z.namelist()
        if len(entries)!=11 or len(set(entries))!=11 or "manifest.json" not in entries:
            raise RuntimeError("Expected exactly ten WebP images and reviewed manifest")
        m=json.loads(z.read("manifest.json"))
        qa=m.get("photographic_qa",{})
        if m.get("batch")!=28 or qa.get("approved") is not True or not qa.get("reviewer"):
            raise RuntimeError("Photographic provenance has not been independently approved")
        files=m.get("files",[])
        if len(files)!=10 or [x.get("code") for x in files]!=CODES:raise RuntimeError("Image roster mismatch")
        digests=set();approved={}
        for row in files:
            code=row["code"];name=f"a3tal-dtc-{code.lower()}-exclusive.webp"
            if row.get("filename")!=name or row.get("photorealism_approved") is not True:
                raise RuntimeError("Unapproved image or unexpected image name "+code)
            if row.get("image_origin") not in ("original_photo","original_ai_photorealistic"):
                raise RuntimeError("No verified photo provenance "+code)
            raw=z.read(name)
            if not 25000<len(raw)<500000 or len(raw)!=row.get("bytes"):raise RuntimeError("Unexpected bytes "+code)
            digest=hashlib.sha256(raw).hexdigest()
            if digest!=row.get("sha256") or digest in digests:raise RuntimeError("Image changed or duplicated "+code)
            digests.add(digest)
            with Image.open(io.BytesIO(raw)) as im:
                if im.format!="WEBP" or im.size!=(1600,900):raise RuntimeError("Wrong WebP dimensions "+code)
                im.verify()
            approved[name]=raw
        OUT.mkdir(parents=True,exist_ok=True)
        for name,raw in approved.items(): (OUT/name).write_bytes(raw)
        (OUT/"manifest.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
    print("TEN_REVIEWED_BATCH28_PHOTOGRAPHS_VERIFIED",len(approved))
if __name__=="__main__":main()
