#!/usr/bin/env python3
"""A3tal Egyptian XML sitemap integrity audit (read only, 2026-11-16).
Fetches live robots, parses sitemap index and all child XMLs, checks every
entry and a deterministic coverage sample from all sitemap categories.
This checks submitted-discoverability/HTML indexability, NOT actual Google indexing.
No WP API key, POST, redirect, WordPress mutation, or Search Console submit.
"""
import collections
import concurrent.futures
import datetime
import json
import re
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit,unquote
import requests
from bs4 import BeautifulSoup
BASE="https://a3tal.com"
UA={"User-Agent":"Mozilla/5.0 (compatible; A3talSitemapReadOnlyAudit/1.0)"}
NS="{http://www.sitemaps.org/schemas/sitemap/0.9}"
RETRY=(429,500,502,503,504)
def utc_now():return datetime.datetime.now(datetime.timezone.utc)
def req(url):
    last=None
    for a in range(3):
        try:
            r=requests.get(url,timeout=(9,28),headers=UA,allow_redirects=True)
            if r.status_code not in RETRY or a==2:return r
            last="retryable_status_"+str(r.status_code)
        except requests.RequestException as exc:
            last=repr(exc)[:220]
        time.sleep(1+a)
    raise RuntimeError(f"Unable to read {url}: {last}")
def locs(root,kind):
    return [x.text.strip() for x in root.findall(".//"+NS+kind+"/"+NS+"loc") if x.text]
def exact_path_key(url):
    parts=urlsplit(url)
    return (parts.scheme.lower(),parts.netloc.lower(),unquote(parts.path or "/").rstrip("/").casefold())
def sample(urls,limit):
    if len(urls)<=limit:return urls
    positions={int(i*(len(urls)-1)/max(1,limit-1)) for i in range(limit)}
    return [urls[i] for i in sorted(positions)]
def meta_check(item):
    src,url=item
    result={"sitemap":src,"url":url,"http_status":0,"final":"","redirect_count":0,
            "canonical":"","robots":"","og":False,"meta_description":False,
            "h1_count":None,"error":None}
    try:
        r=req(url)
        result.update(http_status=r.status_code,final=r.url,redirect_count=len(r.history))
        if r.status_code!=200:return result
        h=BeautifulSoup(r.text,"html.parser")
        can=h.select_one("link[rel=canonical]")
        rob=h.select_one('meta[name="robots"]')
        og=h.select_one('meta[property="og:image"]')
        desc=h.select_one('meta[name="description"]')
        result.update(canonical=can.get("href","") if can else "",
                      robots=rob.get("content","") if rob else "",
                      og=bool(og and og.get("content")),
                      meta_description=bool(desc and desc.get("content","").strip()),
                      h1_count=len(h.select("h1")))
    except Exception as exc:result["error"]=str(exc)[:180]
    return result
def main():
    started=utc_now()
    index_r=req(BASE+"/sitemap_index.xml")
    if index_r.status_code!=200:raise RuntimeError("INDEX_NOT_200 "+str(index_r.status_code))
    try:index=ET.fromstring(index_r.content)
    except Exception as exc:raise RuntimeError("INDEX_INVALID_XML") from exc
    if index.tag!=NS+"sitemapindex":
        raise RuntimeError("Yoast sitemap index not valid sitemapindex root: "+index.tag)
    children=locs(index,"sitemap")
    print("SITEMAP_INDEX",len(children),"HTTP",index_r.status_code,"CHILDREN",json.dumps(children,ensure_ascii=False),flush=True)
    rows=[];all_urls=[];entries=[];bad_files=[];dates=[]
    for child in children:
        r=req(child)
        record={"file":child,"http":r.status_code,"redirects":len(r.history),"urls":0,"errors":[]}
        if r.status_code!=200:
            record["errors"].append("NON_200");bad_files.append(record);rows.append(record);continue
        try:xml=ET.fromstring(r.content)
        except Exception as exc:
            record["errors"].append("INVALID_XML "+str(exc)[:100]);bad_files.append(record);rows.append(record);continue
        if xml.tag!=NS+"urlset":
            record["errors"].append("NOT_URLSET_ROOT");bad_files.append(record);rows.append(record);continue
        page_urls=locs(xml,"url")
        record["urls"]=len(page_urls)
        record["max_size_bytes"]=len(r.content)
        if len(page_urls)>50000 or len(r.content)>52428800:record["errors"].append("SITEMAP_PROTOCOL_LIMIT")
        loc_nodes=xml.findall(NS+"url")
        for node in loc_nodes:
            loc=node.find(NS+"loc")
            if loc is None or not (loc.text or "").strip():continue
            u=loc.text.strip()
            lastmod=node.find(NS+"lastmod")
            recordline={"sitemap":child.rsplit("/",1)[-1],"url":u}
            if lastmod is not None and (lastmod.text or "").strip():
                v=lastmod.text.strip()
                recordline["lastmod"]=v
                try:
                    dt=datetime.datetime.fromisoformat(v.replace("Z","+00:00"))
                    if dt.tzinfo is None:dt=dt.replace(tzinfo=datetime.timezone.utc)
                    if dt>started+datetime.timedelta(days=1):
                        recordline.setdefault("issues",[]).append("FUTURE_LASTMOD")
                    dates.append(dt)
                except ValueError:recordline.setdefault("issues",[]).append("BAD_LASTMOD")
            parsed=urlsplit(u)
            if (parsed.scheme,parsed.netloc)!=("https","a3tal.com"):
                recordline.setdefault("issues",[]).append("WRONG_PROTOCOL_OR_HOST")
            if parsed.fragment:recordline.setdefault("issues",[]).append("HAS_FRAGMENT")
            if parsed.query:recordline.setdefault("issues",[]).append("HAS_QUERY")
            if "/ksa/" in parsed.path:recordline.setdefault("issues",[]).append("HAS_KSA_PATH")
            if "//" in parsed.path:recordline.setdefault("issues",[]).append("DOUBLE_SLASH_PATH")
            entries.append(recordline)
        rows.append(record)
        all_urls.extend((record["file"],u) for u in page_urls)
        print("SITEMAP_CHILD",record["file"].rsplit("/",1)[-1],record["http"],record["urls"],flush=True)
    counts=collections.Counter(e["url"] for e in entries)
    exact_duplicates=[{"url":k,"count":n} for k,n in counts.items() if n>1]
    normalized=collections.defaultdict(set)
    for e in entries:normalized[exact_path_key(e["url"])].add(e["url"])
    variants=[list(v) for v in normalized.values() if len(v)>1]
    flagged=[e for e in entries if e.get("issues")]
    robots=req(BASE+"/robots.txt")
    robots_content=robots.text if robots.status_code==200 else ""
    robot_sitemap_lines=[s.strip() for s in robots_content.splitlines() if re.match(r"^\s*Sitemap:",s,re.I)]
    disallows=[s.strip() for s in robots_content.splitlines() if s.strip().lower().startswith("disallow:")]
    aliases={}
    for path in ["/sitemap.xml","/wp-sitemap.xml","/sitemap_index.xml"]:
        try:
            r=req(BASE+path)
            aliases[path]={"status":r.status_code,"redirects":len(r.history),"final_url":r.url}
        except Exception as exc:aliases[path]={"error":str(exc)[:120]}
    # Sampling is proportional but with a 4-page minimum, and broad checks for biggest categories.
    category_limits={"post-sitemap.xml":45,"a3_dtc-sitemap.xml":18,"a3_car_ref-sitemap.xml":38}
    samples=[]
    for row in rows:
        if row["errors"]:continue
        urls=[u for k,u in all_urls if k==row["file"]]
        lim=category_limits.get(row["file"].rsplit("/",1)[-1],min(10,len(urls)))
        samples.extend((row["file"].rsplit("/",1)[-1],u) for u in sample(urls,lim))
    # Force-check exact known redirects from prior posts if present in sitemap.
    watch=["/jetour-t2-maintenance-schedule-spare-parts/","/toyota-corolla-maintenance-spare-parts-guide/"]
    watch_in_sitemap=[e["url"] for e in entries if urlsplit(e["url"]).path in watch]
    sample_seen={u for k,u in samples}
    for u in watch_in_sitemap:
        if u not in sample_seen:samples.append(("known-redirect-watch",u))
    examined=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for x in pool.map(meta_check,samples):
            examined.append(x)
    issue_rows=[]
    for x in examined:
        issues=[]
        if x["error"]:issues.append("FETCH_ERROR")
        if x["http_status"]!=200:issues.append("NOT_200")
        if x["redirect_count"]:issues.append("REDIRECT")
        if re.search(r"\bnoindex\b",x["robots"],re.I):issues.append("NOINDEX")
        if not x["canonical"]:issues.append("MISSING_CANONICAL")
        elif exact_path_key(x["canonical"])!=exact_path_key(x["url"]):issues.append("DIFFERENT_CANONICAL")
        if not x["og"]:issues.append("MISSING_OG")
        if not x["meta_description"]:issues.append("MISSING_META_DESCRIPTION")
        if x["h1_count"]!=1:issues.append("H1_NOT_ONE")
        if issues:issue_rows.append({**x,"issues":issues})
    summary={
        "date_utc":utc_now().isoformat(),"read_only":True,
        "sitemap_index":{"url":BASE+"/sitemap_index.xml","status":index_r.status_code,"child_count":len(children)},
        "children":rows,"total_entries":len(entries),"unique_exact_url_count":len(counts),
        "unique_normalized_url_count":len(normalized),"duplicate_exact_urls":exact_duplicates[:100],
        "normalized_variants":variants[:100],
        "url_entries_issues":flagged[:120],"url_entries_issues_count":len(flagged),
        "robots":{"status":robots.status_code,"declared_sitemaps":robot_sitemap_lines,"disallows":disallows[:60]},
        "sitemap_aliases":aliases,"known_redirects_listed":watch_in_sitemap,
        "sample_checked":len(examined),"sample_http_statuses":dict(collections.Counter(x["http_status"] for x in examined)),
        "sample_issues_count":len(issue_rows),"sample_issues":issue_rows[:100],
        "samples":examined
    }
    with open("a3tal-sitemap-live-audit-20261116.json","w",encoding="utf-8") as f:json.dump(summary,f,ensure_ascii=False,indent=2)
    simple={k:summary[k] for k in ["total_entries","unique_exact_url_count","unique_normalized_url_count","url_entries_issues_count","sample_checked","sample_http_statuses","sample_issues_count","known_redirects_listed"]}
    print("A3TAL_SITEMAP_AUDIT_SUMMARY",json.dumps(simple,ensure_ascii=False),flush=True)
    print("A3TAL_SITEMAP_ROBOTS",json.dumps(summary["robots"],ensure_ascii=False),flush=True)
    print("A3TAL_SITEMAP_ALIASES",json.dumps(summary["sitemap_aliases"],ensure_ascii=False),flush=True)
    print("A3TAL_SITEMAP_SAMPLE_ISSUES",json.dumps(issue_rows[:50],ensure_ascii=False),flush=True)
    print("A3TAL_SITEMAP_URL_ENTRY_ISSUES",json.dumps(flagged[:50],ensure_ascii=False),flush=True)
    print("A3TAL_SITEMAP_READONLY_DONE",flush=True)
if __name__=="__main__":main()
