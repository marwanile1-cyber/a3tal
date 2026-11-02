#!/usr/bin/env python3
"""Replace original diagram covers for first Kia reference batch with individual
photo-based covers. Never touches the 5 manually approved image replacements.
Source material: five previously ChatGPT-generated Kia automotive photographs
stored in this repo. Data and links stay unchanged.
"""
import base64
import importlib.util
import json
import os
import re
import time
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"data/car-reference/batch-01-kia-verified-2026-11-02.json").read_text(encoding="utf8"))
spec=importlib.util.spec_from_file_location("premium",ROOT/"scripts/publish-car-reference-batch02-premium.py")
premium=importlib.util.module_from_spec(spec)
spec.loader.exec_module(premium)
BASE="https://a3tal.com"
KEY=os.environ["A3TAL_API_KEY"]
S=requests.Session()
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
REPORT=ROOT/"car-reference-batch01-photo-upgrade-report.json"
DONE=[]
SKIP={("cerato-bd-2023","engine-oil-16-mpi")}
CAR={
  "cerato-bd-2023":("cerato-bd-2023.webp","كيا سيراتو 2023"),
  "seltos-sp2-2023":("seltos-sp2-2023.webp","كيا سيلتوس 2023"),
  "sportage-nq5-2023":("sportage-nq5-2023.webp","كيا سبورتاج NQ5"),
}
CATEGORIES={
  "engine-oil":("زيت المحرك",(39,189,224)),
  "transmission-oil":("زيت ناقل الحركة",(95,157,240)),
  "coolant":("سائل تبريد المحرك",(35,185,188)),
  "fuel":("سعة خزان الوقود",(223,143,87)),
}
def short_metric(value):
    value=str(value)
    match=re.search(r"(\d+(?:[.,]\d+)?)\s*(?:إلى|~|–|-)\s*(\d+(?:[.,]\d+)?)",value)
    if match:return match[1]+"–"+match[2]+" L"
    num=re.search(r"\d+(?:[.,]\d+)?",value)
    if num and "لتر" in value:return num.group(0)+" L"
    if num and "مل" in value:return num.group(0)+" ml"
    # No fake numbers: print the verified published measurement when short.
    if len(value)<=12 and not re.search(r"[\u0600-\u06ff]",value):return value
    return "KIA 2023"

def live(slug):
    r=S.get(BASE+"/wp-json/wp/v2/car-reference-records",params={"slug":slug,"per_page":20},timeout=45)
    r.raise_for_status()
    a=[x for x in r.json() if x.get("slug")==slug and x.get("status")=="publish"]
    if len(a)!=1:raise RuntimeError("Post missing or duplicate "+slug+" count="+str(len(a)))
    return a[0]

def put(path,payload):
    for attempt in range(3):
        r=S.post(BASE+"/wp-json/a3tal-direct/v1"+path,json=payload,headers=HEAD,timeout=160)
        if r.status_code>=500 and attempt<2:
            time.sleep(3*(attempt+1))
            continue
        if not r.ok:raise RuntimeError(f"Bridge HTTP {r.status_code} {r.text[:200]}")
        return r.json()
    raise RuntimeError("POST retries exhausted")

def check(url,filename,image_id):
    for i in range(6):
        r=S.get(url,params={"a3cr_renew_img":str(time.time_ns())},timeout=60)
        html=r.text
        media=live(url.rstrip("/").split("/")[-1])
        if (r.ok and r.url.split("?")[0].rstrip("/")==url.rstrip("/")
            and filename in html
            and re.search(r'<meta[^>]*property=["\x27]og:image["\x27][^>]*content=["\x27][^"\x27]*'+re.escape(filename),html,re.I)
            and "noindex" not in html[:14000].lower()):
            return True
        time.sleep(4)
    raise RuntimeError("Failed HTML/OG/media check "+url)

def main():
    rows=[s for s in DATA["specs"] if (s["model"],s["slug"]) not in SKIP]
    assert len(rows)==25 and len({r["slug"] for r in rows})==25
    limit=max(1,min(25,int(os.getenv("A3CR_IMAGE_LIMIT","25"))))
    print("Image upgrade: ",limit,"of 25 original pages",flush=True)
    try:
        for i,s in enumerate(rows[:limit]):
            slug=s["slug"]
            post=live(slug)
            desired=BASE+"/car-reference/kia/"+s["model"]+"/"+slug+"/"
            if post["link"].rstrip("/")!=desired.rstrip("/"):
                raise RuntimeError("Wrong hierarchy for "+slug)
            category=s["category"]
            label,color=CATEGORIES[category]
            base,car=CAR[s["model"]]
            metric=short_metric(s["facts"][0][1])
            tag="KIA-"+s["model"]+"-"+slug
            name="a3tal-verified-photo-"+slug+".webp"
            # Avoid any publication changes if existing photo is already upgraded.
            if slug in {"engine-oil-20-mpi","engine-oil-16-tgdi","engine-oil-smartstream-16"}:
                DONE.append({"url":desired,"slug":slug,"status":"pilot-already-verified"})
                print("SKIP pilot photo already verified independently",slug,flush=True)
                continue
            existing_html=S.get(desired,timeout=60).text
            if name in existing_html:
                original_id=int(post.get("featured_media") or 0)
                check(desired,name,original_id)
                DONE.append({"url":desired,"slug":slug,"new":original_id,"status":"already-verified"})
                print("SKIP verified existing image",slug,flush=True)
                continue
            premium.DESIGNS[tag]=(base,car,label,metric,
                s["engine"] if all(ord(c)<128 for c in s["engine"]) and len(s["engine"])<=16 else "دليل المالك 2023",
                color,(i%3))
            image=premium.make_art(tag)
            if len(image)<55000:raise RuntimeError("Invalid generated image "+slug)
            media=put("/upload-image-data",{"post_id":post["id"],
                  "filename":name,"title":s["title"],
                  "alt":s["title"]+" - دليل أعطال.كوم",
                  "image_base64":base64.b64encode(image).decode("ascii"),
                  "convert_webp":False})
            new_id=int(media.get("media_id") or 0)
            if not new_id:raise RuntimeError("Upload missing media_id")
            response=put("/set-featured-image",{"post_id":post["id"],"media_id":new_id})
            if int(response.get("featured_media") or 0)!=new_id:
                raise RuntimeError("Featured mismatch for "+slug)
            check(desired,name,new_id)
            DONE.append({"url":desired,"slug":slug,"old":post.get("featured_media"),
                "new":new_id,"image_url":media["url"],"status":"verified"})
            print("PHOTO UPDATED",desired,flush=True)
    finally:
        REPORT.write_text(json.dumps(DONE,ensure_ascii=False,indent=2),encoding="utf8")
    if len(DONE)!=limit:raise RuntimeError("Expected "+str(limit)+" updates, got "+str(len(DONE)))
    print("DONE",len(DONE),"replacement images all verified",flush=True)

if __name__=="__main__":main()
