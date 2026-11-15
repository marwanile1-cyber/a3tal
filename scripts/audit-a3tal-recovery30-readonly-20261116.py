#!/usr/bin/env python3
"""SEO emergency triage for 30 GSC-prioritized a3tal.com Egypt pages.
READ ONLY: GET published pages; no WP/GitHub writes and no indexing requests.
Counts current structural evidence; historic 3-month GSC metrics are NOT a
Nov 12-13 page-level loss comparison. Avoid ranking claims from this audit.
"""
import collections
import concurrent.futures
import datetime
import difflib
import json
import re
import time
import unicodedata
from urllib.parse import urlsplit, unquote
import requests
from bs4 import BeautifulSoup

BASE="https://a3tal.com/"
URL_PATHS=[
"ghabbour-auto-maintenance-booking-numbers-branches/",
"دليلك-الشامل-أفضل-مراكز-خدمة-غبور-أوتو/",
"حجز-صيانة-هيونداي-في-مصر-كل-المراكز-وأر/",
"الدليل-الشامل-أرقام-مراكز-خدمة-المنصو/",
"mansour-chevrolet-maintenance-booking-numbers-branches/",
"soueast-egypt-service-centers-locations-hotline/",
"skoda-egypt-service-centers-locations/",
"مراكز-خدمة-جيتور-المعتمدة-في-مصر/",
"jetour-t2-maintenance-schedule-egypt/",
"jetour-t2-maintenance-schedule-spare-parts/",
"toyota-corolla-maintenance-prices-guide-2026/",
"toyota-corolla-maintenance-spare-parts-guide/",
"mg-5-maintenance-prices-guide-2026/",
"mg5-spare-parts-prices-egypt/",
"changan-spare-parts-prices-egypt/",
"gac-empow-maintenance-schedule/",
"jaecoo-egypt-agent-service-centers-maintenance-2026/",
"رجة-في-السيارة-على-سرعة-80-أو-100-أو-120/",
"car-tires-prices-egypt-2026/",
"traffic-fines-prices-radars-egypt-2026/",
"5-علامات-تؤكد-تلف-أسطوانة-الدبرياج-الكل/",
"pcv-valve-failure-symptoms-oil-consumption/",
"bad-starter-motor-symptoms-repair-guide/",
"dtc-p0342-chevrolet/",
"كود-p0011-سيارات-هيونداي/",
"toyota-egypt-maintenance-booking-guide/",
"renault-egypt-maintenance-booking-centers-locations/",
"what-to-do-when-check-engine-light-is-on/",
"byd-f3-price-egypt/",
"p0335-crankshaft-position-sensor/"
]
assert len(URL_PATHS)==30 and len(set(URL_PATHS))==30
GROUPS=[
("جيتور T2",9,10),
("كورولا",11,12),
("غبور",1,2),
("منصور",4,5),
("MG5 صيانة وقطع غيار",13,14)
]
HEADERS={"User-Agent":"Mozilla/5.0 (compatible; A3talEmergencyRecoveryReadOnly/1.0; +https://a3tal.com/)"}
BLOCKED={"script","style","aside","footer","header","nav","form","noscript"}
def normalized(url):
    p=urlsplit(url)
    return unquote(p.path).strip("/").casefold()
def text_of(node):
    shadow=BeautifulSoup(str(node),"html.parser")
    for tag in shadow.find_all(list(BLOCKED)):
        tag.decompose()
    return " ".join(shadow.stripped_strings)
def read_page(index,path):
    url=BASE+path
    result={"n":index,"requested_url":url,"canonical":"","final_url":"","status":None,
            "redirect_count":None,"title":"","meta_description":"","robots":"","og_image":"",
            "h1":[],"h2":[],"body_chars":0,"paragraphs":0,"article_links_internal":[],
            "links_to_prioritized":[],"external_sources":[],"inline_images":0,
            "toc_fragment_links":0,"flags":[],"evidence":[],"error":None}
    response=None
    for try_number in range(2):
        try:
            response=requests.get(url,timeout=(8,23),allow_redirects=True,headers=HEADERS)
            if response.status_code in (429,500,502,503,504) and try_number==0:
                time.sleep(2);continue
            break
        except Exception as ex:
            result["error"]=type(ex).__name__+": "+str(ex)[:140]
            if try_number==0:time.sleep(1)
    if response is None:
        result["flags"].append("FETCH_FAILED")
        return result
    result["status"]=response.status_code
    result["final_url"]=response.url
    result["redirect_count"]=len(response.history)
    if response.status_code!=200:
        result["flags"].append("NON_200")
        return result
    soup=BeautifulSoup(response.text,"html.parser")
    canonical=soup.select_one('link[rel="canonical"]')
    result["canonical"]=canonical.get("href","") if canonical else ""
    metarobots=soup.select_one('meta[name="robots"]')
    result["robots"]=metarobots.get("content","") if metarobots else ""
    ogimg=soup.select_one('meta[property="og:image"]')
    result["og_image"]=ogimg.get("content","") if ogimg else ""
    desc=soup.select_one('meta[name="description"]')
    result["meta_description"]=desc.get("content","") if desc else ""
    title=soup.select_one("title")
    result["title"]=title.get_text(" ",strip=True) if title else ""
    result["h1"]=[t.get_text(" ",strip=True) for t in soup.select("h1")][:5]
    body=(soup.select_one("article .entry-content") or soup.select_one("article .post-content")
          or soup.select_one(".entry-content") or soup.select_one("article")
          or soup.select_one("main") or soup.body)
    if body is None:result["flags"].append("NO_ARTICLE");return result
    result["h2"]=[x.get_text(" ",strip=True)[:120] for x in body.select("h2")][:28]
    result["paragraphs"]=len(body.select("p"))
    result["inline_images"]=len(body.select("img"))
    article_text=text_of(body)
    result["body_chars"]=len(article_text)
    result["intro"]=article_text[:520]
    result["_sample"]=article_text[:16000]
    links=[]
    source_links=[]
    for a in body.select('a[href]'):
        href=a.get("href","")
        if href.startswith(("#","mailto:","tel:")):continue
        try:
            p=urlsplit(href)
            if p.netloc.endswith("a3tal.com") or href.startswith("/"):
                links.append(href)
            elif p.scheme in ("http","https"):
                source_links.append(href)
        except Exception:pass
    keys=set(normalized(u) for u in links)
    result["article_links_internal"]=links[:60]
    result["links_to_prioritized"]=[n for n,p in enumerate(URL_PATHS,1)
                                     if n!=index and normalized(BASE+p) in keys]
    result["external_sources"]=source_links[:15]
    result["toc_fragment_links"]=len([a for a in soup.select('a[href^="#a3-section"]')])
    if result["canonical"] and normalized(result["canonical"])!=normalized(response.url):
        result["flags"].append("CANONICAL_MISMATCH")
    if not result["canonical"]:result["flags"].append("NO_CANONICAL")
    if "noindex" in result["robots"].lower():result["flags"].append("NOINDEX")
    if not result["og_image"]:result["flags"].append("MISSING_OG_IMAGE")
    if len(result["h1"])!=1:result["flags"].append("H1_NOT_ONE")
    if not result["meta_description"]:result["flags"].append("MISSING_DESCRIPTION")
    if result["body_chars"]<1500:result["flags"].append("SHORT_MAIN_CONTENT")
    if not source_links:result["flags"].append("NO_EXTERNAL_SOURCES_IN_ARTICLE")
    if not links:result["flags"].append("NO_INTERNAL_LINKS_IN_ARTICLE")
    if result["redirect_count"]:result["flags"].append("REDIRECTED_SOURCE")
    for pattern,label in [
       (r"(?:20\s*[-–]\s*30\s*%|20\s*إلى\s*30\s*%)", "PERCENT_SERVICE_INTERVAL"),
       (r"(?:4\s*(?:لترات|لتر).{0,85}(?:CVT|فتيس)|(?:CVT|فتيس).{0,85}4\s*(?:لترات|لتر))","FIXED_CVT_QUANTITY"),
       (r"(?:العملاء.*واقعية|تقييمات.*واقعية)", "UNATTRIBUTED_REVIEWS")
    ]:
        for match in list(re.finditer(pattern,article_text,re.I))[:2]:
            result["evidence"].append({"type":label,"excerpt":article_text[max(0,match.start()-110):match.end()+130]})
            if label not in result["flags"]:result["flags"].append(label)
    return result
def words(s):
    return set(w for w in re.findall(r"[\w\u0600-\u06ff]{4,}",s.lower())
               if w not in {"السيارة","الصيانة","جدول","للسيارة","المحرك","الفتيس","مصر","الاسعار","الموقع","الماركة","الصيانات"})
def main():
    print("RECOVERY30_START",datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        fs=[ex.submit(read_page,i+1,p) for i,p in enumerate(URL_PATHS)]
        for f in concurrent.futures.as_completed(fs):
            v=f.result()
            results.append(v)
            print("RECOVERY30_PAGE",json.dumps({"n":v["n"],"status":v["status"],
                "redirects":v["redirect_count"],"flags":v["flags"],
                "body_chars":v["body_chars"],"selected_links":v["links_to_prioritized"]},ensure_ascii=False),flush=True)
    results.sort(key=lambda x:x["n"])
    pair_summary=[]
    for name,a,b in GROUPS:
        x,y=results[a-1],results[b-1]
        if not x.get("_sample") or not y.get("_sample"):
            pair_summary.append({"cluster":name,"pages":[a,b],"error":"Insufficient content to compare"})
            continue
        sim=round(len(words(x["_sample"]) & words(y["_sample"]))/
             max(1,len(words(x["_sample"]) | words(y["_sample"])),3)
        ha=words(" ".join(x["h2"]));hb=words(" ".join(y["h2"]))
        hsim=round(len(ha&hb)/max(1,len(ha|hb)),3)
        linked=a in y["links_to_prioritized"] or b in x["links_to_prioritized"]
        pair_summary.append({"cluster":name,"pages":[a,b],
          "content_token_jaccard":sim,"heading_token_jaccard":hsim,
          "linked_between_pages":linked,
          "url_a_links_b":b in x["links_to_prioritized"],
          "url_b_links_a":a in y["links_to_prioritized"],
          "note":"Similarity is a triage cue, NEVER proof of cannibalization or authorization for 301."})
    for r in results:r.pop("_sample",None)
    count=lambda flag:sum(flag in r["flags"] for r in results)
    summary={"target_count":30,"inspected":len(results),
             "http_200":sum(r["status"]==200 for r in results),
             "fetch_failure":count("FETCH_FAILED"),
             "non_200":count("NON_200"),
             "canonical_mismatch":count("CANONICAL_MISMATCH"),
             "noindex":count("NOINDEX"),
             "missing_meta":count("MISSING_DESCRIPTION"),
             "missing_og":count("MISSING_OG_IMAGE"),
             "missing_external_sources":count("NO_EXTERNAL_SOURCES_IN_ARTICLE"),
             "without_links_to_any_other_selected":sum(not r["links_to_prioritized"] for r in results),
             "tricky_fixed_cvt":count("FIXED_CVT_QUANTITY"),
             "service_interval_percent":count("PERCENT_SERVICE_INTERVAL"),
             "uncited_reviews":count("UNATTRIBUTED_REVIEWS")}
    out={"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "site":"https://a3tal.com/","mode":"strictly_read_only",
         "gsc_context":"30 target pages selected from GSC 14 Aug-13 Nov 2026, metrics are NOT page-level Nov update losses",
         "summary":summary,"pairs":pair_summary,"pages":results}
    with open("a3tal-recovery30-live-readonly.json","w",encoding="utf-8") as o:
        json.dump(out,o,ensure_ascii=False,indent=2)
    print("RECOVERY30_SUMMARY",json.dumps(summary,ensure_ascii=False),flush=True)
    print("RECOVERY30_PAIRS",json.dumps(pair_summary,ensure_ascii=False),flush=True)
    print("RECOVERY30_ARTIFACT a3tal-recovery30-live-readonly.json",flush=True)
    # Fail only on systemic inability to inspect, not because of naturally present SEO issues.
    if summary["http_200"]<24:
        raise SystemExit("Too many inaccessible pages for representative triage; rerun read-only later.")
if __name__=="__main__":main()
