import json,re,urllib.request
root="https://a3tal.com"
def read(url):
    req=urllib.request.Request(url,headers={"User-Agent":"A3tal-DTC-OG-Inspector/1.0","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=40) as f:return f.read().decode("utf-8")
for code in ["p0137","p0192","p0105"]:
    try:
        x=json.loads(read(root+"/wp-json/wp/v2/a3tal-dtc?slug="+code+"&_fields=id,slug,featured_media,yoast_head_json"))
        if not x:print(code,"POST ABSENT");continue
        z=x[0]
        imgs=z.get("yoast_head_json",{}).get("og_image",[])
        media=z.get("featured_media")
        u=""
        if media:
            m=json.loads(read(root+"/wp-json/wp/v2/media/"+str(media)+"?_fields=id,source_url"))
            u=m.get("source_url")
        print("OG_INSPECT",json.dumps({"code":code,"post":z.get("id"),"featured":media,"featured_url":u,"og_image":imgs,"yoast_keys":list(z.get("yoast_head_json",{}).keys())[:12]},ensure_ascii=False),flush=True)
    except Exception as e:print("INSPECT_ERROR",code,str(type(e).__name__),str(e)[:180],flush=True)
