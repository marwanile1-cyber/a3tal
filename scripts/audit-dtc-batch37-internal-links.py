#!/usr/bin/env python3
"""Read-only production check: no broken internal DTC links after batch37 patch."""
import json,re,urllib.parse,urllib.request
from html.parser import HTMLParser
CODES="P0359 P0360 P0485 P0762 P0763 P0874 U0206 U0207 U0215 U0216".split()
SITE="https://a3tal.com"
class Plain(HTMLParser):
 def __init__(self):super().__init__();self.data=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ("style","script"):self.skip+=1
 def handle_endtag(self,t):
  if t in ("style","script"):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.data.append(d)
def get(code,fields="id,slug,status,content,featured_media,yoast_head_json,link"):
 query=urllib.parse.urlencode({"slug":code.lower(),"per_page":3,"_fields":fields})
 req=urllib.request.Request(SITE+"/wp-json/wp/v2/a3tal-dtc?"+query,headers={"User-Agent":"a3tal-batch37-crosslink-qa","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=60)as f:return json.load(f)
def main():
 posts={}
 for code in CODES:
  p=get(code)
  if len(p)!=1 or p[0]["slug"]!=code.lower() or p[0]["status"]!="publish":raise RuntimeError("Code not published "+code)
  v=p[0];body=v["content"]["rendered"];parser=Plain();parser.feed(body);words=len(" ".join(parser.data).split())
  if words<1500:raise RuntimeError("Article below threshold "+code+":"+str(words))
  posts[code]=v
  print("ARTICLE_VALID",code,words,flush=True)
 linked=set()
 for code,p in posts.items():
  for d in re.findall(r'https://a3tal\.com/dtc/([pbcu][0-9a-f]{4})/?',p["content"]["rendered"]):linked.add(d.upper())
 ok={}
 for code in sorted(linked):
  live=get(code,"id,slug,status")
  ok[code]=len(live)==1 and live[0].get("status")=="publish" and live[0].get("slug")==code.lower()
  print("CROSSLINK",code,"LIVE" if ok[code] else "404",flush=True)
 bad=[c for c in ok if not ok[c]]
 summary={"batch":37,"articles":len(posts),"linked_destinations":len(linked),"broken_destinations":bad}
 print("BATCH37_FINAL_LINK_SUMMARY",json.dumps(summary),flush=True)
 if bad:raise RuntimeError("Broken DTC internal links after repair: "+str(bad))
if __name__=="__main__":main()
