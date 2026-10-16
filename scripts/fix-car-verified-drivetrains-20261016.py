#!/usr/bin/env python3
"""One-time evidence-backed and non-destructive car metadata repair.
Only two existing a3_car IDs, only an *empty* _a3_drivetrain key.
Do not touch prices, timestamps, text, images, links or car taxonomy.
Sources reviewed October 16 2026:
Mazda3: https://www.shift-eg.com/news/local-news/details/27051/
JAC JS2: https://www.busines24.com/413464
"""
import importlib.util
import json
import urllib.request

spec=importlib.util.spec_from_file_location("a3tal_bridge","scripts/deploy-dtc-library.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PATCHES=[
    {"id":83532,"slug":"mazda-3-2027-egypt","value":"FWD","source":"https://www.shift-eg.com/news/local-news/details/27051/"},
    {"id":83425,"slug":"jac-js2-2027-egypt","value":"FWD","source":"https://www.busines24.com/413464"},
]

def value(raw):
    if isinstance(raw,list):
        return str(raw[0] if raw else "").strip()
    return str(raw if raw is not None else "").strip()

def main():
    api=module.Bridge()
    state=api.request({"op":"site_info"})
    if state.get("active_theme")!="a3tal-global":
        raise RuntimeError("Active theme mismatch, abort metadata update")
    for patch in PATCHES:
        target=patch["id"]
        url=f"https://a3tal.com/wp-json/wp/v2/a3tal-cars/{target}?_fields=id,slug,status"
        req=urllib.request.Request(url,headers={"User-Agent":"A3tal-Car-Spec-Repair/1.0","Accept":"application/json"})
        with urllib.request.urlopen(req,timeout=45) as res:
            item=json.load(res)
        if item.get("slug")!=patch["slug"] or int(item.get("id",0))!=target:
            raise RuntimeError("Live car identity mismatch, abort: "+str(target))
        pre=api.request({"op":"post_meta","post_id":target,"key":"_a3_drivetrain"})
        before=value(pre.get("_a3_drivetrain"))
        if before==patch["value"]:
            print("CAR_SPEC_ALREADY_FIXED",patch["slug"],flush=True)
            continue
        if before not in ("","None"):
            raise RuntimeError("Non-empty drivetrain already present; refuse overwrite: "+patch["slug"])
        print("CAR_SPEC_SOURCE_VERIFIED",patch["slug"],patch["source"],flush=True)
        error=None
        try:
            api.request({"op":"post_meta_set","post_id":target,
                         "meta":{"_a3_drivetrain":patch["value"]},"confirm":True,"dangerous":True},write=True)
        except RuntimeError as e:
            error=e
        post=api.request({"op":"post_meta","post_id":target,"key":"_a3_drivetrain"})
        actual=value(post.get("_a3_drivetrain"))
        if actual!=patch["value"]:
            raise RuntimeError("Write not confirmed for "+patch["slug"]+"; "+str(error))
        print("CAR_SPEC_PATCH_CONFIRMED",patch["slug"],actual,flush=True)
    print("CAR_SPEC_VERIFIED_BATCH_DONE",len(PATCHES),flush=True)

if __name__=="__main__":
    main()
