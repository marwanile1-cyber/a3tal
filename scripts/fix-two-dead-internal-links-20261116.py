#!/usr/bin/env python3
"""Fix ONLY two independently verified dead context links. Safe exact-match patch.
A3tal: GitHub Actions + A3tal Direct Bridge; no WPWriter.
Preserve all content bytes except two verified href values. No new posts,
redirections, snippets, titles, prices, images, dates, or canonical changes.
"""
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

SITE = "https://a3tal.com"
BRIDGE = SITE + "/wp-json/a3tal-direct/v1"
KEY = os.environ.get("A3TAL_API_KEY", "")
ROWS = [
  {
    "slug": "car-battery-heat-saudi-summer-voltage-test-before-replace",
    "broken": "https://a3tal.com/car-battery-drains-when-parked-diagnosis/",
    "replacement": "https://a3tal.com/car-battery-parasitic-draw-diagnosis/",
    "anchor_text": "دليل أعطال عن تفريغ البطارية",
  },
  {
    "slug": "serpentine-belt-squealing-vs-timing-belt-replacement",
    "broken": "https://a3tal.com/صيانة-دورية-للسيارة/",
    "replacement": "https://a3tal.com/maintenance-schedules/",
    "anchor_text": "دليل الصيانة الدورية في أعطال",
  },
]
HEADERS={"User-Agent":"A3tal-CoreUpdate-TwoBrokenLinks-20261116/1.0",
         "Accept":"application/json","Cache-Control":"no-store"}
def request_url(url,data=None,secure=False):
    headers=dict(HEADERS)
    if secure:
        if not KEY:raise RuntimeError("Missing A3tal Direct Bridge key")
        headers["X-A3tal-Key"]=KEY
        headers["Authorization"]="Bearer "+KEY
    body=json.dumps(data,ensure_ascii=False).encode("utf-8") if data is not None else None
    if body is not None: headers["Content-Type"]="application/json; charset=utf-8"
    max_attempts=3 if body is None else 1
    for attempt in range(max_attempts):
        try:
            req=urllib.request.Request(url,headers=headers,data=body,
                  method="POST" if body is not None else "GET")
            with urllib.request.urlopen(req,timeout=85) as resp:
                out=resp.read()
                try:return json.loads(out)
                except (ValueError,UnicodeDecodeError):return out
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError):
            if attempt+1>=max_attempts:raise
            time.sleep(3*(attempt+1))
def post_from_slug(slug):
    q=urllib.parse.urlencode({"slug":slug,"_fields":"id,slug,status,modified_gmt,link,featured_media,title,yoast_head_json"})
    rows=request_url(SITE+"/wp-json/wp/v2/posts?"+q)
    if not isinstance(rows,list) or len(rows)!=1 or rows[0].get("slug")!=slug or rows[0].get("status")!="publish":
        raise RuntimeError("Unable to uniquely identify public published post "+slug)
    return rows[0]
def bridge_post(pid):
    return request_url(BRIDGE+"/post/"+str(pid),secure=True)
def key(url):
    p=urllib.parse.urlsplit(html.unescape(url))
    return (p.scheme.lower(),p.netloc.lower(),urllib.parse.unquote(p.path).rstrip("/").casefold())
def target_check(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (A3talInternalLinkReadOnly/1.0)"})
    with urllib.request.urlopen(req,timeout=40) as r:
        if r.status!=200 or r.url.rstrip("/")!=url.rstrip("/"):
            raise RuntimeError("Replacement target not HTTP 200 at intended URL: "+url)
        soup=BeautifulSoup(r.read().decode("utf8","replace"),"html.parser")
        canonical=soup.select_one("link[rel=canonical]")
        robots=soup.select_one('meta[name="robots"]')
        c=canonical.get("href","") if canonical else ""
        v=robots.get("content","") if robots else ""
        if key(c)!=key(url) or "noindex" in v.lower():
            raise RuntimeError("Replacement target unindexable or unexpected canonical: "+url)
        return soup.title.get_text(" ",strip=True) if soup.title else ""
HREF=re.compile(r'(?P<attr>\bhref\s*=\s*)(?P<q>["\'])(?P<url>[^"\']+)(?P=q)',re.I)
def patch_link_only(raw,row):
    records=[]
    def replace(match):
        current=html.unescape(match.group("url"))
        if key(current)!=key(row["broken"]):return match.group(0)
        records.append(current)
        return match.group("attr")+match.group("q")+row["replacement"]+match.group("q")
    new=HREF.sub(replace,raw)
    if len(records)==0 and row["replacement"] in raw:
        return None,"already-fixed"
    if len(records)!=1:
        raise RuntimeError("Expected exactly one old href for "+row["slug"]+", found "+str(len(records)))
    # Refuse other changes; replacing new URL back with original in the exact position restores original content.
    back=new.replace(row["replacement"],records[0])
    if back!=raw or row["replacement"] not in new:
        raise RuntimeError("Non-href markup change detected")
    if len(re.findall(r"<img\b",new,re.I))!=len(re.findall(r"<img\b",raw,re.I)):
        raise RuntimeError("Inline media count changed")
    for label in ("<h2","<h3","<table","<figure"):
        if new.lower().count(label)!=raw.lower().count(label):
            raise RuntimeError("Structural HTML changed: "+label)
    return new,"patch"
def seo_snapshot(public):
    seo=public.get("yoast_head_json") or {}
    og=seo.get("og_image") or []
    return {
      "canonical":seo.get("canonical"),
      "description":seo.get("description"),
      "title":seo.get("title"),
      "robots_index":(seo.get("robots") or {}).get("index"),
      "og_image":og[0].get("url") if og else None,
    }
def preflight():
    pending=[]
    for row in ROWS:
        t=target_check(row["replacement"])
        public=post_from_slug(row["slug"])
        pid=public["id"]
        live=bridge_post(pid)
        if (live.get("id"),live.get("slug"),live.get("status"),live.get("type"))!=(pid,row["slug"],"publish","post"):
            raise RuntimeError("Post identity/status mismatch: "+row["slug"])
        if int(live.get("featured_media") or 0)!=int(public.get("featured_media") or 0):
            raise RuntimeError("Featured image inconsistency: "+row["slug"])
        if not isinstance(live.get("content"),str) or len(live["content"])<1300:
            raise RuntimeError("Unexpectedly short original article: "+row["slug"])
        if row["anchor_text"] not in html.unescape(re.sub("<[^>]+>","",live["content"])):
            raise RuntimeError("Original contextual anchor no longer present: "+row["slug"])
        new,state=patch_link_only(live["content"],row)
        if state=="already-fixed":
            print("LINK_ALREADY_REPAIRED",row["slug"],row["replacement"],flush=True)
            continue
        s=seo_snapshot(public)
        if s["canonical"]!=SITE+"/"+row["slug"]+"/" or s["robots_index"]=="noindex" or not s["og_image"]:
            raise RuntimeError("Source SEO baseline unexpectedly changed: "+row["slug"])
        pending.append({"row":row,"before":live,"public":public,"new":new,"target_title":t})
        print("LINK_PREFLIGHT_OK",row["slug"],"id",pid,"content_length",len(live["content"]),
              "target",row["replacement"],"target_title",t[:95],flush=True)
    return pending
def apply():
    rows=preflight()
    print("ALL_LINK_PREFLIGHTS_PASSED",len(rows),flush=True)
    for entry in rows:
        row=entry["row"]; before=entry["before"]; bp=entry["public"]
        current=bridge_post(before["id"])
        if current.get("modified_gmt")!=before.get("modified_gmt") or current.get("content")!=before["content"]:
            raise RuntimeError("Concurrent content edit; refuse to overwrite: "+row["slug"])
        payload={"id":before["id"],"slug":row["slug"],
                 "expected_modified_gmt":before["modified_gmt"],
                 "title":before["title"],"content":entry["new"]}
        try:
            response=request_url(BRIDGE+"/update-post",payload,secure=True)
            if isinstance(response,dict) and (response.get("error") or response.get("ok") is False):
                raise RuntimeError("Bridge rejected safe href update: "+str(response)[:140])
        except Exception as ex:
            check=bridge_post(before["id"])
            if check.get("content")!=entry["new"]:
                raise RuntimeError("Write failed/unconfirmed; will never blindly retry "+row["slug"]) from ex
            print("LINK_WRITE_TIMEOUT_RECOVERED",row["slug"],flush=True)
        final=bridge_post(before["id"])
        p=post_from_slug(row["slug"])
        if final.get("content")!=entry["new"] or final.get("featured_media")!=before.get("featured_media"):
            raise RuntimeError("Bridge content or featured image verification failed: "+row["slug"])
        if (final.get("slug"),final.get("status"),final.get("title"))!=(
            row["slug"],"publish",before["title"]):
            raise RuntimeError("URL/title/status unexpectedly changed")
        if seo_snapshot(p)!=seo_snapshot(bp):
            raise RuntimeError("Yoast metadata/canonical/OG changed unexpectedly")
        if row["replacement"] not in final["content"]:
            raise RuntimeError("New working link missing")
        if any(key(html.unescape(m.group("url")))==key(row["broken"]) for m in HREF.finditer(final["content"])):
            raise RuntimeError("Old broken link survived")
        print("LINK_FIXED_LIVE_VERIFIED",row["slug"],"post_id",before["id"],
              "target",row["replacement"],"featured_image",before.get("featured_media"),flush=True)
    print("A3TAL_TWO_BROKEN_LINKS_DONE",len(rows),flush=True)
if __name__=="__main__":apply()
