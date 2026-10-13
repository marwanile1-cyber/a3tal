"""Build verified, locally served A3TAL marque image pack from two pinned logo archives.
Source logos remain property/trademarks of original rightsholders; identification only.
No remote image URLs or browser-side CDN dependencies.
"""
import argparse
import base64
import io
import json
import re
import unicodedata
from pathlib import Path
from PIL import Image, ImageOps
import cairosvg

SOURCE_COMMIT = "3f0929e70e0a9a2a502063edc4b3e5c0146cba74"
ALIASES = {
  "Mercedes-Benz":"mercedes-benz", "DS Automobiles":"ds", "KGM":"kgm",
  "Changan Deepal":"deepal", "Maruti Suzuki":"maruti", "Xiaomi Auto":"xiaomi",
  "BAIC":"baic",
  "Renault Korea":"renault", "W Motors":"w-motors", "Great Wall":"great-wall",
  "SsangYong":"ssangyong", "AITO":"aito"
}
FALLBACK_ALIASES = {
  "UD Trucks":"ud", "GAC":"gac-group", "Lynk & Co":"lynk-and-co",
  "Range Rover":"range-rover", "MG Rover":"mg-rover",
}
def slug(text):
    v=unicodedata.normalize("NFKD",text.lower()).encode("ascii","ignore").decode()
    return re.sub(r"(^-|-$)","",re.sub(r"[^a-z0-9]+","-",v))
def brands_from_source(text):
    section=text.split("var models=",1)[0]
    return list(dict.fromkeys(re.findall(r"'([^'|\n]+)\|[^'|\n]+\|[^'\n]*'",section)))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--logo-repo",required=True,type=Path)
    p.add_argument("--fallback-dir",type=Path)
    p.add_argument("--input",default="theme-source/a3tal-global/assets/js/dtc-world-garage.js",type=Path)
    p.add_argument("--output",default="theme-source/a3tal-global/assets/js/dtc-brand-logos.generated.js",type=Path)
    args=p.parse_args()
    names=brands_from_source(args.input.read_text(encoding="utf-8"))
    logos={}; missing=[]; errors=[]
    for name in names:
        stem=ALIASES.get(name,slug(name))
        src=None
        for ext in (".svg",".png"):
            test=args.logo_repo/(stem+"-logo"+ext)
            if test.exists():src=test;break
        if not src and args.fallback_dir:
            fallback_stem=FALLBACK_ALIASES.get(name,slug(name))
            extra=args.fallback_dir/(fallback_stem+".png")
            if extra.exists():src=extra
        if not src:
            missing.append(name);continue
        try:
            if src.suffix==".svg":
                # Rasterize to exclude SVG scripts, external resources and remote dependencies.
                pixels=cairosvg.svg2png(bytestring=src.read_bytes(),output_width=360)
                im=Image.open(io.BytesIO(pixels))
            else:im=Image.open(src)
            im=im.convert("RGBA")
            # Preserve transparency, original color and aspect ratio; never redraw trademarks.
            im.thumbnail((216,136),Image.Resampling.LANCZOS)
            if not im.width or not im.height:raise ValueError("empty dimensions")
            bio=io.BytesIO();im.save(bio,format="WEBP",quality=88,method=5)
            logos[name]="data:image/webp;base64,"+base64.b64encode(bio.getvalue()).decode("ascii")
        except Exception as exc:
            errors.append(f"{name} ({src.name}): {type(exc).__name__}: {exc}")
            missing.append(name)
    if len(logos)<115:raise RuntimeError(f"Insufficient valid brand art: {len(logos)}. Fail closed. Errors: {errors}")
    for required in ("Kia","Hyundai","Toyota","Nissan","BMW","Mercedes-Benz","Chevrolet","Chery","BYD","Mitsubishi"):
        if required not in logos:raise RuntimeError("Missing crucial logo: "+required)
    result=("/* A3TAL trademark identification graphics; from vehiclespecs/brand-logos pinned "+SOURCE_COMMIT+" + car-logos-dataset pinned bb2d661f; no affiliation. */\n"
            +"window.a3talGarageBrandLogos = Object.freeze("+json.dumps(logos,ensure_ascii=False,separators=(",",":"))+");\n")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(result,encoding="utf-8")
    if len(result.encode("utf-8")) > 1_900_000:
        raise RuntimeError("Logo bundle exceeds safe bridge payload threshold")
    print(f"Validated {len(logos)} local logos for {len(names)} listed marques; {len(missing)} explicit wordmark fallbacks")
    print("Unmatched marques: "+", ".join(missing))
    if errors: print("Unrenderable sources: "+"; ".join(errors))
    print("Bundle size:",len(result.encode("utf-8")),"bytes")

if __name__=="__main__":
    main()
