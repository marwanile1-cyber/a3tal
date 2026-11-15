#!/usr/bin/env python3
"""Read-only GSC-priority URL/sitemap consistency check for a3tal Egypt.
This is NOT the Google Search Console Page Indexing report. Checks visibility
in XML, live redirects, meta robots, canonical and lastmod for 32 prior
prioritized source URLs (30 distinct live destination URLs).
"""
import collections
import datetime
import importlib.util
import json
import os
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

BASE="https://a3tal.com"
AGENT={"User-Agent":"Mozilla/5.0 (compatible; A3talPriorityIndexabilityReadOnly/1.0)"}
NS="{http://www.sitemaps.org/schemas/sitemap/0.9}"
def get(url):
    r=requests.get(url,headers=AGENT,timeout=(8,32),allow_redirects=True)
    r.raise_for_status()
    return r
def key(url):
    p=urlsplit(url)
    return p.scheme.lower(),p.netloc.lower(),unquote(p.path).casefold().rstrip("/")
def targets_from_repo():
    spec=importlib.util.spec_from_file_location("prior_audit","scripts/audit-a3tal-recovery30-readonly-20261116.py")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [BASE+"/"+p for p in mod.URL_PATHS]
def read_live(url):
    try:
        r=get(url)
        soup=BeautifulSoup(r.text,"html.parser")
        c=soup.select_one("link[rel=canonical]")
        m=soup.select_one('meta[name="robots"]')
        return {"requested":url,"status":r.status_code,"final":r.url,
                "redirect_count":len(r.history),"redirect_chain":[v.status_code for v in r.history],
                "canonical":c.get("href","") if c else "",
                "robots":m.get("content","") if m else "",
                "x_robots":r.headers.get("x-robots-tag","")}
    except Exception as e:
        return {"requested":url,"status":0,"error":str(e)[:200]}
def main():
    idx=get(BASE+"/sitemap_index.xml")
    root=ET.fromstring(idx.content)
    sitemap_names=[n.text.strip() for n in root.findall(".//"+NS+"sitemap/"+NS+"loc") if n.text]
    sitemap_records=[]
    for url in sitemap_names:
        xml=ET.fromstring(get(url).content)
        name=url.rsplit("/",1)[-1]
        for e in xml.findall(NS+"url"):
            loc=e.findtext(NS+"loc")
            lastmod=e.findtext(NS+"lastmod")
            if loc:sitemap_records.append({"url":loc.strip(),"in":name,"lastmod":lastmod})
    bykey=collections.defaultdict(list)
    for r in sitemap_records:bykey[key(r["url"])].append(r)
    targets=targets_from_repo()
    checks=[read_live(u) for u in targets]
    for r in checks:
        r["source_in_sitemap"]=bykey.get(key(r["requested"]),[])
        if r["status"]==200:
            r["destination_in_sitemap"]=bykey.get(key(r["final"]),[])
            r["canonical_in_sitemap"]=bykey.get(key(r["canonical"]),[]) if r["canonical"] else []
            flags=[]
            if not r["destination_in_sitemap"]:flags.append("FINAL_URL_MISSING_FROM_SITEMAP")
            if not r["canonical_in_sitemap"]:flags.append("CANONICAL_MISSING_FROM_SITEMAP")
            if key(r["canonical"])!=key(r["final"]):flags.append("CANONICAL_DIFFERS_FROM_FINAL")
            if "noindex" in (r["robots"]+" "+r["x_robots"]).lower():flags.append("NOINDEX")
            if r["redirect_count"] and r["source_in_sitemap"]:flags.append("REDIRECT_SOURCE_IN_SITEMAP")
            if r["redirect_count"] and not r["source_in_sitemap"]:flags.append("EXPECTED_REDIRECT_OMITTED_FROM_SITEMAP")
            r["flags"]=flags
        else:r["flags"]=["UNAVAILABLE"]
    finals={key(r["final"]) for r in checks if r["status"]==200}
    issues=[r for r in checks if any(f not in ("EXPECTED_REDIRECT_OMITTED_FROM_SITEMAP",) for f in r["flags"])]
    report={
        "generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "mode":"read_only_no_gsc_api",
        "limitation":"External indexability checks do not reveal Google Indexed/Not indexed Page Indexing coverage.",
        "source_urls":len(targets),
        "unique_final_urls":len(finals),
        "sitemap_index_children":len(sitemap_names),
        "sitemap_entries":len(sitemap_records),
        "sitemap_unique_urls":len({key(x["url"]) for x in sitemap_records}),
        "source_in_sitemap":sum(bool(x["source_in_sitemap"]) for x in checks),
        "destination_in_sitemap":sum(bool(x.get("destination_in_sitemap")) for x in checks),
        "canonical_in_sitemap":sum(bool(x.get("canonical_in_sitemap")) for x in checks),
        "redirected_sources":sum(x.get("redirect_count",0)>0 for x in checks),
        "redirected_sources_listed":sum(x.get("redirect_count",0)>0 and bool(x["source_in_sitemap"]) for x in checks),
        "http_errors":sum(x["status"]!=200 for x in checks),
        "noindex":sum("NOINDEX" in x["flags"] for x in checks),
        "unexpected_issues_count":len(issues),
        "unexpected_issues":issues[:30],
        "checks":checks
    }
    with open("a3tal-priority-indexability-readonly-20261116.json","w",encoding="utf8") as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
    print("A3TAL_GSC_TOP_SITEMAP_SUMMARY",json.dumps({k:v for k,v in report.items() if k not in ("checks","unexpected_issues")},ensure_ascii=False),flush=True)
    print("A3TAL_GSC_TOP_SITEMAP_ISSUES",json.dumps(issues[:15],ensure_ascii=False),flush=True)
    print("A3TAL_GSC_TOP_SITEMAP_REDIRECTS",json.dumps([{"source":r["requested"],"dest":r["final"],"source_in_sitemap":bool(r["source_in_sitemap"])} for r in checks if r.get("redirect_count")],ensure_ascii=False),flush=True)
if __name__=="__main__":main()
