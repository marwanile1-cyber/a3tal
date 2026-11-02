#!/usr/bin/env python3
"""Safely refresh the existing MAGE EV article (ID 82712), never create a duplicate."""
import json, os, re, urllib.request, urllib.error
from pathlib import Path
from html.parser import HTMLParser

SITE="https://a3tal.com"
API=SITE+"/wp-json/a3tal-direct/v1"
KEY=os.environ.get("A3TAL_API_KEY", "")
POST_ID=82712
SLUG="dongfeng-mage-ev-egypt-price-specs"
EXPECTED="2026-09-30T23:23:58+00:00"
URL=SITE+"/"+SLUG+"/"
FILE=Path("data/editorial/dongfeng-mage-ev-update-20261102.html")
TITLE="سعر دونج فينج MAGE EV موديل 2027 في مصر.. المواصفات وموعد الطرح"
META_TITLE="سعر دونج فينج MAGE EV 2027 في مصر والمواصفات | أعطال.كوم"
DESCRIPTION="سعر دونج فينج MAGE EV موديل 2027 في مصر وموعد طرحها بعد بدء تجميعها محليًا. المواصفات الكاملة: بطارية 50.82 كيلووات، مدى 445 كم، الشحن والضمان."
EXCERPT="سعر دونج فينج MAGE EV 2027 لم يُعلن رسميًا بعد. تعرف على موعد طرح SUV الكهربائية المجمعة محليًا ومواصفات البطارية والمدى والشحن والضمان."

def request(path,method="GET",data=None,auth=False):
    head={"User-Agent":"A3tal-Editorial-MAGE-EV-20261102","Accept":"application/json","Cache-Control":"no-cache,no-store"}
    if auth:
        if not KEY: raise RuntimeError("A3TAL_API_KEY missing")
        head["X-A3tal-Key"]=KEY
    payload=None if data is None else json.dumps(data,ensure_ascii=False).encode("utf8")
    if payload is not None:head["Content-Type"]="application/json; charset=utf-8"
    req=urllib.request.Request((API if auth else SITE)+path,method=method,headers=head,data=payload)
    with urllib.request.urlopen(req,timeout=140) as f:return json.load(f)

class Metadata(HTMLParser):
    def __init__(self):super().__init__();self.meta={};self.canonical=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="meta" and (a.get("property") or a.get("name")):
            self.meta[a.get("property") or a.get("name")]=a.get("content","")
        if tag=="link" and a.get("rel")=="canonical":self.canonical.append(a.get("href"))

def main():
    body=FILE.read_text(encoding="utf8").strip()
    if len(body)<10000 or body.count("<h2>")<9 or body.count("<table")<3:
        raise RuntimeError("Reviewed article completeness check failed")
    if not all(t in body for t in ("31 أكتوبر 2026","الربع الأول من 2027","لم يُعلن","50.82","445","300 ألف","82712") if t!="82712"):
        raise RuntimeError("Critical verified facts missing")
    live=request("/wp-json/wp/v2/posts?slug="+SLUG+"&_fields=id,slug,link,status,featured_media")
    if len(live)!=1 or live[0]["id"]!=POST_ID:
        raise RuntimeError("Canonical ownership / duplicate slug check failed")
    if live[0]["status"]!="publish" or live[0]["featured_media"]!=82714:
        raise RuntimeError("Expected featured image or status changed")
    current=request("/post/"+str(POST_ID),auth=True)
    if current["id"]!=POST_ID or current["slug"]!=SLUG or current["status"]!="publish" or current["type"]!="post":
        raise RuntimeError("Bridge returned wrong post")
    if current.get("featured_media")!=82714:
        raise RuntimeError("Expected featured photo assignment changed")
    if current.get("modified_gmt")!=EXPECTED:
        if current.get("title")==TITLE and "31 أكتوبر 2026" in current.get("content","") and "الربع الأول من 2027" in current.get("content",""):
            print("ALREADY_UPDATED",URL,"featured",current["featured_media"],flush=True)
            return
        raise RuntimeError("Existing post changed since reviewed; no overwrite: "+str(current.get("modified_gmt")))
    payload={
        "id":POST_ID,"expected_modified_gmt":EXPECTED,"slug":SLUG,"status":"publish",
        "title":TITLE,"content":body,"excerpt":EXCERPT,
        "meta":{
           "_yoast_wpseo_title":META_TITLE,
           "_yoast_wpseo_metadesc":DESCRIPTION,
           "_yoast_wpseo_focuskw":"سعر دونج فينج MAGE EV 2027",
           "_yoast_wpseo_canonical":URL,
           "_yoast_wpseo_opengraph-title":TITLE,
           "_yoast_wpseo_opengraph-description":DESCRIPTION,
           "_yoast_wpseo_twitter-title":TITLE,
           "_yoast_wpseo_twitter-description":DESCRIPTION
        }
    }
    result=request("/update-post",method="POST",data=payload,auth=True)
    if result.get("id")!=POST_ID or result.get("slug")!=SLUG or result.get("status")!="publish":
        raise RuntimeError("Bridge did not confirm canonical update")
    if result.get("featured_media")!=82714 or "الربع الأول من 2027" not in result.get("content",""):
        raise RuntimeError("Updated article is incomplete or featured image missing")
    check=request("/wp-json/wp/v2/posts/"+str(POST_ID)+"?_fields=id,slug,status,link,featured_media,content,yoast_head_json")
    if check.get("id")!=POST_ID or check.get("status")!="publish" or check.get("link")!=URL or check.get("featured_media")!=82714:
        raise RuntimeError("Public REST article verification failed")
    if "31 أكتوبر 2026" not in check.get("content",{}).get("rendered",""):
        raise RuntimeError("Public WordPress content not updated")
    try:
        p=urllib.request.Request(URL,headers={"User-Agent":"A3tal-Editorial-Verification/2026"})
        with urllib.request.urlopen(p,timeout=45) as f: source=f.read(3_000_000).decode("utf8","replace")
        parser=Metadata();parser.feed(source)
        if URL not in parser.canonical:
            raise RuntimeError("Canonical link mismatch")
        if "dongfeng-mage-ev-front-accurate-1600" not in parser.meta.get("og:image",""):
            raise RuntimeError("Open Graph featured image mismatch")
        if 'max-image-preview:large' not in source:
            raise RuntimeError("Discover image-preview header missing")
        print("OG_IMAGE_CONFIRMED",parser.meta.get("og:image"),flush=True)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as err:
        print("PUBLIC_HTML_VERIFICATION_RETRY_REQUIRED",type(err).__name__,flush=True)
    print("ARTICLE_REFRESHED",POST_ID,URL,"featured",check["featured_media"],"words",len(re.findall(r"[\u0621-\u064a]+",re.sub("<[^>]+>"," ",body))),flush=True)

if __name__=="__main__":main()
