#!/usr/bin/env python3
"""Safely replace factually unsafe MG7 maintenance guide with independently
reviewed Egypt-specific official-source encyclopedia. The bridge saves a
WordPress backup. Abort on concurrent edit, wrong URL, missing cover/SEO meta.
"""
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SITE="https://a3tal.com"
REST=SITE+"/wp-json/a3tal-direct/v1"
PID=80480
EXPECTED_SLUG="صيانة-mg-7-في-مصر"
EXPECTED_MODIFIED="2026-10-01T23:21:41+00:00"
CONTENT_PATH=Path("data/repairs/egypt-mg7-service-official-facts-20261020.html")
EXPECTED_FEATURED=80481
NEW_TITLE="صيانة MG 7 في مصر: جدول الفحص وفتيس Wet DCT والزيوت والمراكز"
KEY=os.environ.get("A3TAL_API_KEY")
if not KEY: raise SystemExit("Missing private bridge authentication")

def call(path,body=None,auth=True):
    headers={"Accept":"application/json","User-Agent":"A3tal-OfficialMG7-Editorial-Quality/1.0",
             "Cache-Control":"no-store"}
    if auth:headers.update({"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY})
    data=None
    if body is not None:
        data=json.dumps(body,ensure_ascii=False).encode("utf-8")
        headers["Content-Type"]="application/json"
    req=urllib.request.Request(REST+path if path.startswith("/") else path,data=data,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=110) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        print("BRIDGE_HTTP_ERROR",exc.code,flush=True)
        raise

def identity(post):
    if (int(post.get("id",0))!=PID or post.get("type")!="post" or
        post.get("status")!="publish" or
        urllib.parse.unquote(post.get("slug",""))!=EXPECTED_SLUG or
        not post.get("link","").startswith(SITE+"/")):
        raise RuntimeError("Post ID, type, status or slug mismatch; refusing any write")

def word_count(body):
    return len(re.findall(r"[\u0621-\u064a\u0671-\u06d3A-Za-z0-9]+", re.sub(r"<[^>]*>"," ",body)))

def main():
    content=CONTENT_PATH.read_text("utf-8").strip()
    if word_count(content)<1500:raise RuntimeError("Encyclopedic minimum absent")
    if "<h1" in content.lower():raise RuntimeError("Duplicate H1 forbidden")
    markers=["7-speed Wet DCT","المصادر المرجعية","المواصفة","16424","المحرك بارد","خطوات"]
    for marker in markers:
        if marker not in content:raise RuntimeError("Required editorial component missing")
    for source in ("https://www.mgmotor.com.eg/model/mg7/",
                   "https://www.mgmotor.com.eg/faqs/?lang=ar",
                   "https://www.mgmotor.com.eg/locations-showrooms/?lang=ar"):
        if source not in content:raise RuntimeError("Missing manufacturer reference: "+source)
    original=call("/post/"+str(PID))
    identity(original)
    if original["modified_gmt"]!=EXPECTED_MODIFIED:
        raise RuntimeError("WordPress changed after reviewed revision: abort")
    if int(original.get("featured_media") or 0)!=EXPECTED_FEATURED:
        raise RuntimeError("Featured image changed after review: abort")
    old=(original.get("content") or "")
    if not all(x in old for x in ("5W-30","10,000","92","60,000")):
        raise RuntimeError("Reviewed unsafe baseline differs: abort")
    fields={
        "id":PID, "expected_modified_gmt":EXPECTED_MODIFIED,
        "title":NEW_TITLE, "content":content,
        "excerpt":"دليل MG 7 في مصر المبني على مواصفات MG الرسمية: 1.5 تيربو و7 سرعات Wet DCT، وفحوصات الزيت والفتيس والتبريد والفرامل، وكيف تحصل على جدول الصيانة الصحيح من الوكيل.",
        "meta":{
            "_yoast_wpseo_focuskw":"صيانة MG 7 في مصر",
            "_yoast_wpseo_title":"صيانة MG 7 في مصر: جدول الفحص وفتيس DCT والزيوت",
            "_yoast_wpseo_metadesc":"دليل صيانة MG 7 في مصر بالمصادر الرسمية: فتيس Wet DCT، فحص المحرك والسوائل والفرامل، ومواعيد الوكيل الصحيحة دون جداول تغيير تخمينية."
        }
    }
    updated=call("/update-post",fields)
    identity(updated)
    if int(updated.get("featured_media") or 0)!=EXPECTED_FEATURED:
        raise RuntimeError("Featured image changed, check production")
    if len(updated.get("content") or "")<14000:
        raise RuntimeError("Unexpected truncated updated post content")
    live=call(SITE+"/wp-json/wp/v2/posts/"+str(PID)+"?_fields=id,slug,status,link,featured_media,content,yoast_head_json",auth=False)
    if int(live.get("id") or 0)!=PID or live.get("status")!="publish":
        raise RuntimeError("Live publication status mismatch")
    if urllib.parse.unquote(live["slug"])!=EXPECTED_SLUG:
        raise RuntimeError("Live slug changed")
    if int(live.get("featured_media") or 0)!=EXPECTED_FEATURED:
        raise RuntimeError("Live featured media changed")
    rendered=(live.get("content") or {}).get("rendered","")
    count=word_count(rendered)
    if count<1500 or "7 Speed Wet Dual Clutch" not in rendered or "16424" not in rendered:
        raise RuntimeError("Content QA failed: body below threshold or missing critical checks")
    yoast=live.get("yoast_head_json") or {}
    if "index" not in (yoast.get("robots") or {}).get("index","index"):
        raise RuntimeError("Unexpected new noindex")
    print("MG7_OFFICIAL_SERVICE_REPAIR_VERIFIED",PID,"WORDS",count,"FEATURED",EXPECTED_FEATURED,
          "SLUG_PRESERVED","TRUE",flush=True)

if __name__=="__main__":
    main()
