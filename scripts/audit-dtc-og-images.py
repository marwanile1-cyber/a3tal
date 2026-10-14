#!/usr/bin/env python3
"""Fail-closed, read-only WordPress check: featured art, Yoast og:image, visible article image.
This tool never mutates WordPress.
"""
import argparse,json,re,time,urllib.request,urllib.error,urllib.parse
BASE="https://a3tal.com"
BATCHES={"07":["P0137","P0138","P0192","P0193","P0449"],"08":["P0105","P0140","P0190","P0205","P0481"],
         "09":["P0012","P0206","P0452","P0506","P0706"],"10":["P0017","P0116","P0139","P0234","P0453"],"11":["P0217","P0463","U0155","C0035","B0001"],"12":["P0380","P0530","U0073","C0040","B0010"],"13":["P2002","U0109","U0126","C0050","B0028"],"14":["P0243","U0102","U0129","C0045","B0081"],"15":["P0421","U0415","C0110","C0161","B0051"],"16":["P2459","U0131","U0151","C0550","B0020"],"17":["P06DD","U0103","U0164","C0265","B0090"],"18":["P2101","U0128","U0184","C0561","B0070"],"19":["P0544","U0104","U0111","C0299","B0095"],"20":["P0691","U023A","C0051","C0800","B1325"],"21":["P0523","U0106","U0159","C0236","B0094"],"22":["P2563","U0107","C1241","C0237","B1421"],"23":["P0119","U0156","U0186","C0036","B1422"],"24":["P0237","P0451","P0765","U0122","U0401","U0167","C0037","C0041","B1318","B0092"],"14":["P0243","U0102","U0129","C0045","B0081"]}
def read(url):
    headers={"User-Agent":"Mozilla/5.0 (compatible; A3tal-Image-Integrity/1.0)","Accept":"application/json,text/html;q=0.9,*/*;q=0.5","Cache-Control":"no-cache"}
    for n in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as res:return res.read().decode("utf-8")
        except urllib.error.HTTPError as err:
            if err.code not in (429,500,502,503,504,520,522,524) or n==2:raise
        except (TimeoutError,urllib.error.URLError):
            if n==2:raise
        time.sleep(25*(n+1))
def inspect(code):
    uri=BASE+"/wp-json/wp/v2/a3tal-dtc?slug="+code.lower()+"&_fields=id,slug,featured_media,yoast_head_json"
    body=json.loads(read(uri))
    selected=[p for p in body if p.get("slug")==code.lower()]
    if len(selected)!=1:raise RuntimeError("Missing or duplicate published code: "+code)
    post=selected[0]
    media_id=int(post.get("featured_media") or 0)
    if not media_id:raise RuntimeError("Missing featured_media for "+code)
    media=json.loads(read(BASE+"/wp-json/wp/v2/media/"+str(media_id)+"?_fields=id,source_url,mime_type"))
    if not str(media.get("mime_type","")).startswith("image/"):
        raise RuntimeError("Featured media is not an image: "+code)
    original=media.get("source_url","")
    if not original:raise RuntimeError("Missing featured image source URL for "+code)
    images=post.get("yoast_head_json",{}).get("og_image",[])
    og=[i.get("url","") for i in images if isinstance(i,dict)]
    # Account for original vs regenerated crop variants of the same attachment.
    artstem=original.rsplit("/",1)[-1].split(".",1)[0]
    cleanstem=re.sub(r"-[0-9]+x[0-9]+$","",artstem)
    if not any(cleanstem in link for link in og):
        raise RuntimeError("og:image is not the featured art for "+code)
    html=read(BASE+"/dtc/"+code.lower()+"/?a3tal_media_audit=1")
    if "d-dtc-featured" not in html or ("<img" not in html and "wp-post-image" not in html):
        raise RuntimeError("Featured illustration is not visible inside single template for "+code)
    print("ART_AND_OG_VERIFIED",code,media_id,original,flush=True)
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--batch",required=True,choices=sorted(BATCHES))
    args=parser.parse_args()
    for code in BATCHES[args.batch]:
        inspect(code)
    print("ALL",len(BATCHES[args.batch]),"FEATURED_IMAGES_AND_OG_PASSED",args.batch,flush=True)
if __name__=="__main__":main()
