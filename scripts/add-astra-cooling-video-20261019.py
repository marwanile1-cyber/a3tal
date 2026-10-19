#!/usr/bin/env python3
"""Embed an independently produced Astra J 1.4 cooling-system diagnostic demonstration.
Do not imply it is an official Opel video or applies to every Astra J powertrain.
"""
import os,json,urllib.request,re,time
BASE="https://a3tal.com";API=BASE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY")
if not KEY:raise RuntimeError("Missing bridge key")
PID=80842
SLUG="opel-astra-j-cooling-system-leaks-thermostat"
TAG="a3tal-astra-j-coolant-diagnostic-video-20261019"
SECTION=(
  '<section class="a3tal-explainer-video" data-a3tal-video="'+TAG+'" style="margin:28px 0">'
  '<h2>فيديو عملي لتشخيص تسريب دورة تبريد أوبل أسترا J</h2>'
  '<p>يوضح المقطع التالي مثالًا من ورشة مستقلة لفحص وإصلاح تسريب تبريد على '
  'أوبل/فوكسهول أسترا J بمحرك 1.4 تيربو، ولا يمثل فيديو رسميًا من أوبل. '
  'قد تختلف أماكن القطع وكود المحرك والطرق المناسبة باختلاف سنة السيارة وتجهيزها. '
  'يُشاهد بغرض فهم مسار التشخيص، لا لاعتماد أرقام الضغط أو فتح القربة والمحرك ساخنًا.</p>'
  '<div style="position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:12px;background:#0d2536">'
  '<iframe loading="lazy" width="1280" height="720"'
  ' src="https://www.youtube-nocookie.com/embed/iVyWj_yhyY0"'
  ' title="فيديو توضيحي مستقل لفحص تسريب تبريد أوبل أسترا J 1.4 تيربو"'
  ' referrerpolicy="strict-origin-when-cross-origin"'
  ' allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"'
  ' allowfullscreen style="width:100%;height:100%;border:0;display:block"></iframe></div>'
  '<p><small>مصدر الفيديو: <a href="https://www.youtube.com/watch?v=iVyWj_yhyY0"'
  ' target="_blank" rel="nofollow noopener noreferrer">Mustang Motors، أكتوبر 2019، تشخيص أسترا J بمحرك LUJ/A14NET</a>.</small></p>'
  '</section>'
)
def req(endpoint,payload=None):
    h={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,
       "Accept":"application/json","Cache-Control":"no-store","User-Agent":"A3tal-Video-QA/1.0"}
    data=None
    if payload is not None:data=json.dumps(payload,ensure_ascii=False).encode();h["Content-Type"]="application/json"
    with urllib.request.urlopen(urllib.request.Request(API+endpoint,data=data,headers=h),timeout=90) as r:return json.load(r)
def live_verify():
    h={"User-Agent":"Mozilla/5.0 (A3tal-Video-QA/1.0)","Cache-Control":"no-store"}
    for i in range(3):
        if i:time.sleep(5)
        with urllib.request.urlopen(urllib.request.Request(BASE+"/"+SLUG+"/?videoqa="+str(int(time.time())),headers=h),timeout=60) as r:s=r.read().decode("utf-8","replace")
        if TAG in s and "youtube-nocookie.com/embed/iVyWj_yhyY0" in s:
            if "a3tal-original-diagnostic-flow-80842-20261019" not in s:raise RuntimeError("Original visual lost")
            print("ASTRA_IN_ARTICLE_VIDEO_VISIBLE",BASE+"/"+SLUG+"/",flush=True);return
    raise RuntimeError("Cannot verify public iframe embed; WordPress may sanitize it")
def main():
    p=req("/post/"+str(PID))
    assert p["status"]=="publish" and p["slug"]==SLUG and p.get("featured_media")
    content=p["content"]
    if TAG in content:live_verify();print("ALREADY_EMBEDDED");return
    if "A3TAL-QA-ASTRA-COOLING-20261019" not in content:raise RuntimeError("Reviewed technical guide missing")
    if "a3tal-original-diagnostic-flow-80842-20261019" not in content:raise RuntimeError("Article diagram missing")
    matches=list(re.finditer(r'<h2\b[^>]*>\s*الخلاصة\s*</h2>',content,re.I))
    if len(matches)!=1:raise RuntimeError("Unexpected conclusion placement")
    point=matches[0].start()
    content=content[:point]+SECTION+content[point:]
    before=p["modified_gmt"]
    recheck=req("/post/"+str(PID))
    if recheck["modified_gmt"]!=before or recheck["content"]!=p["content"]:raise RuntimeError("Concurrent edit")
    try:req("/update-post",{"id":PID,"content":content,"expected_modified_gmt":before})
    except Exception as error:
        if TAG not in req("/post/"+str(PID)).get("content",""):raise RuntimeError("Write outcome uncertain, do not retry") from error
    updated=req("/post/"+str(PID))
    if TAG not in updated.get("content","") or updated.get("featured_media")!=p.get("featured_media"):raise RuntimeError("Video or featured verification failed")
    live_verify()
if __name__=="__main__":main()
