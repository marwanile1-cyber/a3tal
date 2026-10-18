#!/usr/bin/env python3
"""Read-only live SEO + contextual linking audit. Never writes to WordPress."""
import collections
import concurrent.futures
import json
import re
import threading
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ORIGIN = "https://a3tal.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; A3talSEOAudit/1.0; +https://a3tal.com/)"}
tls = threading.local()

def session():
    if not hasattr(tls, "s"):
        tls.s = requests.Session()
        tls.s.headers.update(HEADERS)
    return tls.s

def norm(raw):
    p = urllib.parse.urlsplit(urllib.parse.urljoin(ORIGIN, raw))
    if p.netloc.lower() not in ("a3tal.com", "www.a3tal.com"):
        return None
    path = urllib.parse.unquote(p.path or "/").rstrip("/") + "/"
    return ORIGIN + path.lower()

def fetch(url, timeout=20):
    return session().get(url, timeout=timeout, allow_redirects=True)

def sitemap_urls():
    idx = fetch(ORIGIN + "/sitemap_index.xml", 30)
    idx.raise_for_status()
    root = ET.fromstring(idx.content)
    locs = [el.text.strip() for el in root.iter() if el.tag.endswith("}loc") and el.text]
    all_urls, types = {}, collections.defaultdict(list)
    for u in locs:
        r = fetch(u, 30)
        r.raise_for_status()
        xml = ET.fromstring(r.content)
        for el in xml.iter():
            if not el.tag.endswith("}url"): continue
            loc = next((n.text for n in el if n.tag.endswith("}loc")), "")
            if not loc: continue
            key=norm(loc)
            if key: types[u.split("/")[-1]].append(key); all_urls.setdefault(key, loc)
    return all_urls, types

def anchors(el):
    if el is None: return []
    return [norm(a.get("href")) for a in el.select("a[href]") if norm(a.get("href"))]

def inspect(item):
    key, url = item
    try:
        r=fetch(url)
        s=BeautifulSoup(r.content, "html.parser")
        title=s.title.get_text(" ", strip=True) if s.title else ""
        md=s.find("meta",attrs={"name":"description"})
        robots=s.find("meta",attrs={"name":"robots"})
        canonical=s.find("link",rel=lambda x: x and "canonical" in x)
        og=s.find("meta",property="og:image")
        main=s.find("main")
        content=(s.select_one(".g-entry") or s.select_one(".d-entry") or
                 s.select_one(".d-guide-body") or s.select_one(".cg-model-journey") or main)
        page={
            "url":key,"requested":url,"status":r.status_code,"final":norm(r.url),
            "title":title,"description":md.get("content","") if md else "",
            "robots":robots.get("content","") if robots else "",
            "canonical":norm(canonical.get("href")) if canonical else None,
            "h1":[x.get_text(" ",strip=True)[:160] for x in s.select("h1")],
            "og_image":bool(og),"images":len(s.select("main img")),
            "main_links":list(dict.fromkeys(anchors(main))),
            "context_links":list(dict.fromkeys(anchors(content))),
            "all_links":list(dict.fromkeys(anchors(s))),
            "header_links":list(dict.fromkeys(anchors(s.find("header")))),
        }
        return page
    except Exception as e:
        return {"url":key,"requested":url,"status":0,"error":str(e)[:160],
                "main_links":[],"context_links":[],"all_links":[],"header_links":[]}

def kind(u):
    p=urllib.parse.urlsplit(u).path
    for prefix,typ in [("/cars/","cars"),("/dtc/","dtc"),("/service-centers/","centers"),
                       ("/car-showrooms/","showrooms"),("/parts-stores/","vendors"),
                       ("/maintenance-schedules/","maintenance"),("/motorcycles/","moto"),
                       ("/category/","category"),("/my-garage/","garage")]:
        if p.startswith(prefix): return typ
    return "post-or-page"

def main():
    all_urls, types=sitemap_urls()
    urls=set(all_urls)
    print("SITEMAP_COUNTS",json.dumps({k:len(v) for k,v in types.items()},ensure_ascii=False),flush=True)
    t0=time.time()
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        for i, p in enumerate(ex.map(inspect,all_urls.items()),1):
            results.append(p)
            if i%75==0: print("AUDIT_PROGRESS",i,len(all_urls),round(time.time()-t0,1),flush=True)
    rows={x["url"]:x for x in results}
    statuses=collections.Counter(x["status"] for x in results)
    sitemap_noindex=[{"url":x["url"],"robots":x.get("robots")} for x in results if re.search(r"\bnoindex\b",x.get("robots",""),re.I)]
    missing_canonical=[x["url"] for x in results if x["status"]==200 and not x.get("canonical") and "noindex" not in x.get("robots","")]
    mismatched_canonical=[{"url":x["url"],"canonical":x.get("canonical")} for x in results if x.get("canonical") and x["canonical"]!=x["url"]]
    missing_meta=[x["url"] for x in results if x["status"]==200 and not x.get("description")]
    h1_problems=[{"url":x["url"],"h1":x.get("h1")} for x in results if x["status"]==200 and len(x.get("h1",[]))!=1]
    missing_og=[x["url"] for x in results if x["status"]==200 and not x.get("og_image")]
    titles=collections.defaultdict(list)
    for p in results:
        if p.get("title"): titles[unicodedata.normalize("NFKC",p["title"]).casefold().strip()].append(p["url"])
    duplicate_titles=[v for v in titles.values() if len(v)>1]
    inbound=collections.Counter()
    inbound_context=collections.Counter()
    edges=collections.Counter()
    no_context=[]
    sitewide=collections.Counter()
    missing_targets=collections.Counter()
    missing_target_sources=collections.defaultdict(list)
    for x in results:
        u=x["url"];k=kind(u)
        for dest in set(x.get("header_links",[])):sitewide[dest]+=1
        for dest in set(x["main_links"]):
            if dest!=u and dest in urls:inbound[dest]+=1;edges[(k,kind(dest))]+=1
            elif dest not in urls and dest!=u:
                missing_targets[dest]+=1
                if len(missing_target_sources[dest])<4:missing_target_sources[dest].append(u)
        for dest in set(x["context_links"]):
            if dest!=u and dest in urls:inbound_context[dest]+=1
        if k=="post-or-page" and x["status"]==200 and len([y for y in x["context_links"] if y!=u and y in urls and kind(y)=="post-or-page"])==0:
            no_context.append(u)
    isolated=[u for u in urls if inbound[u]==0]
    weak=[u for u in urls if inbound[u]<=1 and kind(u)=="post-or-page"]
    article_total=sum(kind(u)=="post-or-page" for u in urls)
    result={
        "at":"2026-10-18","origin":ORIGIN,"elapsed_sec":round(time.time()-t0,1),
        "sitemap_counts":{k:len(v) for k,v in types.items()},"unique_sitemap_urls":len(urls),
        "status_counts":dict(statuses),
        "http_failures":[{"url":x["url"],"status":x["status"],"error":x.get("error")} for x in results if x["status"]!=200],
        "sitemap_noindex":sitemap_noindex,"mismatched_canonical":mismatched_canonical,
        "missing_canonical":missing_canonical,"missing_meta":missing_meta,
        "h1_problems":h1_problems,"missing_og":missing_og,"duplicate_titles":duplicate_titles,
        "zero_main_inbound":isolated,"weak_article_inbound":weak,
        "no_contextual_article_links":no_context,
        "link_graph_by_section":[{"source":k[0],"dest":k[1],"total":v} for k,v in edges.most_common()],
        "sections":{typ:{"pages":sum(kind(u)==typ for u in urls),
             "noindex_in_sitemap":sum(kind(x["url"])==typ for x in sitemap_noindex),
             "zero_inbound":sum(kind(u)==typ for u in isolated),
             "avg_main_inbound":round(sum(inbound[u] for u in urls if kind(u)==typ)/max(1,sum(kind(u)==typ for u in urls)),2)}
           for typ in sorted(set(kind(u) for u in urls))},
        "sitewide_top_links":sitewide.most_common(25),
        "non_sitemap_link_destinations":[{"url":u,"source_count":n,"sources":missing_target_sources[u]} for u,n in missing_targets.most_common(80)],
        "sample_noindex":sitemap_noindex[:60],"sample_isolated":isolated[:60],
        "sample_no_context":no_context[:60],"sample_weak":weak[:60],
        "sample_missing_meta":missing_meta[:35],"sample_h1":h1_problems[:35],
        "pages":results
    }
    p=Path("seo-audit-report.json")
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    short={k:v for k,v in result.items() if k not in ("pages","zero_main_inbound","weak_article_inbound","no_contextual_article_links","missing_canonical","missing_meta","h1_problems","missing_og","sitemap_noindex","mismatched_canonical","duplicate_titles")}
    short.update({"sitemap_noindex_count":len(sitemap_noindex),"mismatched_canonical_count":len(mismatched_canonical),"missing_canonical_count":len(missing_canonical),"missing_meta_count":len(missing_meta),"h1_problem_count":len(h1_problems),"missing_og_count":len(missing_og),"duplicate_title_clusters":len(duplicate_titles),"zero_main_inbound_count":len(isolated),"weak_article_inbound_count":len(weak),"no_context_article_count":len(no_context),"article_total":article_total})
    print("SEO_AUDIT_SUMMARY",json.dumps(short,ensure_ascii=False),flush=True)
    print("SEO_AUDIT_EXAMPLES",json.dumps({"noindex":sitemap_noindex[:35],"mismatched_canonical":mismatched_canonical[:15],"http_failures":result["http_failures"][:35],"duplicate_titles":duplicate_titles[:20],"zero_inbound":isolated[:30],"no_context_article_links":no_context[:30]},ensure_ascii=False),flush=True)
    print("REPORT_SAVED",p.resolve(),flush=True)

if __name__=="__main__":
    main()
