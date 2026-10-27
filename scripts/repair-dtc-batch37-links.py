#!/usr/bin/env python3
"""Batch37 read-before-write cleanup: remove only links to nonpublic DTC codes.
Requires 10 live posts with valid featured images and matching Open Graph before any write.
Uses A3tal Direct Bridge revision guarded update-post; never alters slugs, titles or images.
"""
import json,os,re,time,urllib.parse,urllib.request
SITE="https://a3tal.com"
BRIDGE=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
CODES="P0359 P0360 P0485 P0762 P0763 P0874 U0206 U0207 U0215 U0216".split()
LINK_PATTERN=re.compile(r'<a href="https://a3tal\.com/dtc/([pbcu][0-9a-f]{4})/">([PBCU][0-9A-F]{4})</a>')
def log(*v): print("BATCH37_LINK_QA",*v,flush=True)
def req(method,url,data=None,auth=False):
 headers={"User-Agent":"A3tal-Batch37-LinkQA/1.0","Accept":"application/json","Cache-Control":"no-store"}
 if auth:
  if not KEY: raise RuntimeError("Bridge secret unavailable")
  headers["X-A3tal-Key"]=KEY
  headers["Authorization"]="Bearer "+KEY
 raw=json.dumps(data,ensure_ascii=False).encode("utf-8") if data is not None else None
 if raw:headers["Content-Type"]="application/json; charset=utf-8"
 u=urllib.request.Request(url,data=raw,headers=headers,method=method)
 with urllib.request.urlopen(u,timeout=85) as response:return json.load(response)
def public(code):
 args=urllib.parse.urlencode({"slug":code.lower(),"per_page":2,"_fields":"id,slug,status,featured_media,yoast_head_json"})
 rows=req("GET",SITE+"/wp-json/wp/v2/a3tal-dtc?"+args)
 if not isinstance(rows,list):raise RuntimeError("Bad public rest response "+code)
 same=[row for row in rows if row.get("slug")==code.lower() and row.get("status")=="publish"]
 if len(same)>1:raise RuntimeError("Multiple published slugs "+code)
 return same[0] if same else None
def photo(mid):
 return req("GET",SITE+"/wp-json/wp/v2/media/"+str(mid)+"?_fields=id,source_url,mime_type")
def raw_post(pid):
 return req("GET",BRIDGE+"/post/"+str(pid),auth=True)
def update(pid,rev,content):
 return req("POST",BRIDGE+"/update-post",{"id":pid,"content":content,"expected_modified_gmt":rev},True)
def main():
 posts={}
 for code in CODES:
  p=public(code)
  if not p:raise RuntimeError("Cannot patch missing page "+code)
  mid=int(p.get("featured_media") or 0)
  if not mid:raise RuntimeError("Image not yet assigned, defer links patch "+code)
  media=photo(mid)
  source=media.get("source_url","")
  og=[v.get("url") for v in (p.get("yoast_head_json") or {}).get("og_image",[]) if isinstance(v,dict)]
  if not source or source not in og:raise RuntimeError("OG image not verified, defer links patch "+code)
  posts[code]=p
 log("ALL_TEN_POSTS_IMAGES_AND_OG_VERIFIED")
 records={code:raw_post(int(posts[code]["id"])) for code in CODES}
 for code,row in records.items():
  if row.get("type")!="a3_dtc" or row.get("status")!="publish" or row.get("slug")!=code.lower():
   raise RuntimeError("Bridge raw record identity mismatch "+code)
 links=set()
 for row in records.values():
  for _,dest in LINK_PATTERN.findall(row["content"]):links.add(dest)
 print("BATCH37_RELATED_LINKS",",".join(sorted(links)),flush=True)
 existing={}
 for code in sorted(links):
  p=public(code)
  existing[code]=bool(p)
 missing=sorted(code for code in links if not existing[code])
 log("UNPUBLISHED_LINK_DESTINATIONS",",".join(missing) or "none")
 edits=[]
 for code,row in records.items():
  before=row["content"]
  def replacement(match):
   dest=match.group(2)
   return match.group(0) if existing.get(dest,False) else dest
  after=LINK_PATTERN.sub(replacement,before)
  if after!=before:
   edits.append((code,row,after))
   log("LINKS_TO_CORRECT",code,len(before)-len(after))
 # Preflight all readbacks before mutation. Any interrupted POST requires manual
 # read-only reconciliation, not blind replay.
 for code,row,new_content in edits:
  p=public(code)
  if not p or int(p["id"])!=int(row["id"]):raise RuntimeError("Identity drift "+code)
  log("PATCHING",code)
  try:result=update(int(row["id"]),row["modified_gmt"],new_content)
  except Exception as exc:
   recovered=raw_post(int(row["id"]))
   if recovered.get("content")==new_content:
    log("RECOVERED_AMBIGUOUS_UPDATE",code)
    continue
   raise RuntimeError("Unconfirmed edit: stop "+code) from exc
  if result.get("id")!=row["id"] or result.get("content")!=new_content:
   raise RuntimeError("Bridge response mismatch after edit "+code)
  confirm=raw_post(int(row["id"]))
  if confirm.get("content")!=new_content:raise RuntimeError("Content mismatch "+code)
  log("LINKS_CORRECTED",code)
  time.sleep(4)
 for code in CODES:
  row=raw_post(int(posts[code]["id"]))
  for _,dest in LINK_PATTERN.findall(row["content"]):
   if dest in missing:raise RuntimeError("Broken link remains: "+code+" to "+dest)
 log("ALL_TEN_LIVE_ARTICLES_INTERNAL_DTC_LINKS_VERIFIED",len(edits),"edited")
if __name__=="__main__":main()
