#!/usr/bin/env python3
"""Repair stale Yoast og:image on A3tal car reference pages after featured image replacement.
Revision guarded, PHP-linted Bridge file write; no edits to articles or featured IDs.
"""
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
import requests

BASE="https://a3tal.com"
ADMIN=BASE+"/wp-json/a3tal-direct/v1/admin"
FILE="plugins/a3tal-car-reference/a3tal-car-reference.php"
KEY=os.environ["A3TAL_API_KEY"]
session=requests.Session()
HEAD={"X-A3tal-Key":KEY,"Content-Type":"application/json"}
MARKER="A3CR_CURRENT_FEATURED_OG_FIX_20261102"
PAGES={
  "https://a3tal.com/car-reference/kia/":"kia.webp",
  "https://a3tal.com/car-reference/kia/cerato-bd-2023/":"cerato-bd-2023.webp",
  "https://a3tal.com/car-reference/kia/seltos-sp2-2023/":"seltos-sp2-2023.webp",
  "https://a3tal.com/car-reference/kia/sportage-nq5-2023/":"sportage-nq5-2023.webp",
  "https://a3tal.com/car-reference/kia/cerato-bd-2023/engine-oil-16-mpi/":"cerato-engine-oil-16-mpi.webp",
}
OUTPUT=Path("a3tal-kia-og-image-check.json")

def admin_get(op,**kwargs):
    r=session.get(ADMIN,params={"op":op,**kwargs},headers=HEAD,timeout=90)
    r.raise_for_status()
    j=r.json()
    if not j.get("ok"):raise RuntimeError("Admin GET error "+str(j.get("code")))
    return j.get("result")

def admin_post(op,**kwargs):
    r=session.post(ADMIN,json={"op":op,**kwargs},headers=HEAD,timeout=130)
    r.raise_for_status()
    j=r.json()
    if not j.get("ok"):raise RuntimeError("Admin POST error "+str(j.get("code")))
    return j.get("result")

def patch(code):
    if MARKER in code:return code
    old="add_filter('wpseo_metadesc',[__CLASS__,'seo_description']);"
    new=(old+
      "\n        add_filter('wpseo_opengraph_image',[__CLASS__,'featured_og_image'],999);"+
      "\n        add_filter('wpseo_twitter_image',[__CLASS__,'featured_og_image'],999);"+
      "\n        add_filter('wpseo_opengraph_image_width',[__CLASS__,'featured_og_width'],999);"+
      "\n        add_filter('wpseo_opengraph_image_height',[__CLASS__,'featured_og_height'],999);")
    if code.count(old)!=1:raise RuntimeError("Expected single SEO bootstrap insertion point")
    snippet="""
    // A3CR_CURRENT_FEATURED_OG_FIX_20261102
    public static function featured_og_image($existing) {
        if (!is_singular(self::TYPE)) return $existing;
        $post_id = get_queried_object_id();
        $attachment_id = $post_id ? get_post_thumbnail_id($post_id) : 0;
        $image_url = $attachment_id ? wp_get_attachment_image_url($attachment_id, 'full') : false;
        return $image_url ?: $existing;
    }
    public static function featured_og_width($existing) {
        if (!is_singular(self::TYPE)) return $existing;
        $id = get_post_thumbnail_id(get_queried_object_id());
        $size = $id ? wp_get_attachment_metadata($id) : [];
        return !empty($size['width']) ? (int) $size['width'] : $existing;
    }
    public static function featured_og_height($existing) {
        if (!is_singular(self::TYPE)) return $existing;
        $id = get_post_thumbnail_id(get_queried_object_id());
        $size = $id ? wp_get_attachment_metadata($id) : [];
        return !empty($size['height']) ? (int) $size['height'] : $existing;
    }
"""
    anchor="    public static function schema(){"
    if code.count(anchor)!=1:raise RuntimeError("Expected single schema() declaration")
    return code.replace(old,new,1).replace(anchor,snippet+"\n"+anchor,1)

def verify():
    out=[]
    for url,name in PAGES.items():
        expected="a3tal-kia-2026-new-"+name
        ok=False
        for k in range(7):
            try:
                r=session.get(url,params={"verify_og_fix":str(time.time_ns())},timeout=45,headers={"Cache-Control":"no-cache"})
                r.raise_for_status()
                match=re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)',r.text,re.I)
                img=match.group(1) if match else ""
                if expected in img:
                    ok=True
                    break
            except requests.RequestException:
                img=""
            time.sleep(5)
        out.append({"url":url,"expected_image":expected,"og_image":img,"ok":ok})
        print("OG CHECK",("PASS" if ok else "FAILED"),url,flush=True)
    OUTPUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    if not all(x["ok"] for x in out):
        raise RuntimeError("Some OG images are still stale. Inspect report, do not claim full success.")

def main():
    live=admin_get("file_read",path=FILE)
    old=str(live.get("content",""))
    sha=str(live.get("sha256",""))
    assert old.startswith("<?php") and len(sha)==64
    new=patch(old)
    if new!=old:
        with tempfile.NamedTemporaryFile(mode="w",suffix=".php",encoding="utf-8",delete=False) as fp:
            fp.write(new)
            tmp=fp.name
        subprocess.run(["php","-l",tmp],check=True)
        Path("/tmp/a3cr-og-original.php").write_text(old,encoding="utf-8")
        subprocess.run(["openssl","enc","-aes-256-cbc","-salt","-pbkdf2","-iter","200000",
                        "-pass","env:A3TAL_API_KEY","-in","/tmp/a3cr-og-original.php",
                        "-out","/tmp/a3cr-og-backup.enc"],check=True)
        changed=admin_post("file_write",path=FILE,content=new,expected_sha256=sha,confirm=True,dangerous=True)
        if changed.get("sha256")!=hashlib.sha256(new.encode("utf-8")).hexdigest():
            raise RuntimeError("Live bridge file SHA mismatch")
        print("Deployed conflict-checked PHP override",changed.get("bytes"),flush=True)
        admin_post("cache_flush")
    else:
        print("OG image patch already installed",flush=True)
    verify()

if __name__=="__main__":main()
