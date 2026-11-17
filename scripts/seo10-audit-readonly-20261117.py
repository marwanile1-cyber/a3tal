#!/usr/bin/env python3
"""READ ONLY: inspect exact live content/metadata of 10 high-impression existing A3tal posts."""
import os,json,urllib.request,re,html
ids=[80524,81039,80521,80508,81009,80611,79890,80153,79952,80992]
key=os.environ["A3TAL_API_KEY"]
for pid in ids:
 req=urllib.request.Request(f"https://a3tal.com/wp-json/a3tal-direct/v1/post/{pid}",headers={"X-A3tal-Key":key,"Authorization":"Bearer "+key,"Accept":"application/json","User-Agent":"curl/8.5.0","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=100) as x:p=json.load(x)
 s=p["content"]
 hs=[re.sub(r'<[^>]+>','',m.group(1))[:100] for m in re.finditer(r'<h[2-4]\b[^>]*>([\s\S]*?)</h[2-4]>',s,re.I)]
 dates=[re.sub(r'<[^>]+>',' ',s[max(0,m.start()-35):min(len(s),m.end()+80)]).replace('\n',' ') for m in re.finditer(r'(?:202[4-9]|آخر تحديث|مراجعة|سعر|60%)',s,re.I)]
 suspicious=[x[:160] for x in dates if any(k in x for k in ('2024','2025','2026','2027','آخر تحديث','مراجعة','60%'))]
 print(json.dumps({"id":pid,"title":p.get("title"),"slug":p.get("slug"),"last":p.get("modified_gmt"),"len":len(s),"featured":p.get("featured_media"),"h2":hs[:28],"early":re.sub('<[^>]+>',' ',s[:1350]).replace('\n',' ')[:900],"risky_dates":suspicious[:12],"image_count":len(re.findall(r'<img\b',s,re.I)),"link_count":len(re.findall(r'<a\b',s,re.I)),"article_wrappers":len(re.findall(r'<article\b',s,re.I)),"first_html":s[:220]},ensure_ascii=False),flush=True)

 # Targeted legacy content audit: printed CSS and unsupported experience headings
 if pid in (80508,79890,80153,79952):
  for needle in ('60%','تجربتنا','body {','Google News Article Schema'):
   q=s.find(needle)
   if q>=0:print('LEGACY_CONTEXT',pid,needle,repr(s[max(0,q-320):min(len(s),q+1800)]),flush=True)
