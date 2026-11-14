#!/usr/bin/env python3
"""Read-only, low-volume audit of A3tal live site, 14 Nov 2026.
Never edits WordPress/GitHub contents, no authenticated calls.
Sitemap coverage, sitemap fetch errors, sampled HTTP and SEO, caches, images.
Avoid site load: 2 concurrent workers, capped 60 page requests.
"""
import collections,concurrent.futures,json,re,time,random,urllib.parse,xml.etree.ElementTree as ET
from pathlib import Path
import requests
from bs4 import BeautifulSoup
BASE="https://a3tal.com"
USER_AGENT="Mozilla/5.0 (compatible; A3tal-Emergency-ReadOnly-SiteAudit/20261114)"
S=requests.Session(); S.headers.update({"User-Agent":USER_AGENT,"Accept-Encoding":"gzip, deflate","Cache-Control":"no-cache"})
OUT=Path("reports/a3tal-sitewide-emergency-readonly-20261114.json")
OUT.parent.mkdir(parents=True,exist_ok=True)
def get(url,timeout=27):
    for i in range(2):
        start=time.monotonic()
        try:
            r=S.get(url,timeout=timeout,allow_redirects=True)
            latency=time.monotonic()-start
            if r.status_code not in (429,500,502,503,504) or i==1:
                return r,round(latency,3)
        except requests.RequestException as e:
            if i==1:raise
        time.sleep(1.3)

def root_and_sitemaps():
    data={}
    idx,ttfb=get(BASE+"/sitemap_index.xml")
    data["index_status"]=idx.status_code
    data["index_elapsed"]=ttfb
    if idx.status_code!=200:raise RuntimeError("Sitemap index "+str(idx.status_code))
    root=ET.fromstring(idx.content)
    sitemap_urls=[x.text.strip() for x in root.iter() if x.tag.endswith("loc") and x.text]
    data["index_count"]=len(sitemap_urls)
    children={}
    for name in sitemap_urls:
        key=name.split("/")[-1]
        try:
            r,t=get(name,timeout=35)
            entry={"status":r.status_code,"secs":t,"bytes":len(r.content),
                   "content_type":r.headers.get("content-type",""),
                   "sample_urls":[],"all_urls":[]}
            if r.status_code==200:
                tree=ET.fromstring(r.content)
                locs=[x.text.strip() for x in tree.iter() if x.tag.endswith("loc") and x.text]
                entry["count"]=len(locs)
                entry["all_urls"]=locs
            else:entry["error"]="HTTP "+str(r.status_code)
            children[key]=entry
            print("SITEMAP_AUDIT",key,entry.get("status"),entry.get("count"),"s",t,"bytes",len(r.content),flush=True)
        except Exception as exc:
            children[key]={"status":"error","error":str(exc)[:250]}
            print("SITEMAP_AUDIT_ERROR",key,str(exc)[:200],flush=True)
    data["children"]=children
    return data

def sample_urls(data):
    # Include critical pages and a balanced, deterministic spot-check of 11 sitemaps.
    wanted=[BASE+"/",BASE+"/cars/",BASE+"/car-reference/",BASE+"/dtc/",
       BASE+"/ksa/",BASE+"/robots.txt",
       BASE+"/car-reference/jetour/t1-15t-7dct-egypt-2026/",
       BASE+"/opel-corsa-2027-egypt-price-topline-after-increase/",
       BASE+"/car-reference/kia/cerato-bd-2023/engine-oil-16-mpi/"]
    limits={"post-sitemap.xml":9,"page-sitemap.xml":4,"a3_car-sitemap.xml":4,
      "a3_motorcycle-sitemap.xml":3,"a3_dtc-sitemap.xml":8,
      "a3_service_center-sitemap.xml":3,"a3_showroom-sitemap.xml":3,
      "a3_parts_vendor-sitemap.xml":3,"a3_maintenance_plan-sitemap.xml":4,
      "a3_car_ref-sitemap.xml":10,"category-sitemap.xml":5}
    for name,entry in data["children"].items():
        links=entry.get("all_urls") or []
        if not links:continue
        target=limits.get(name,3)
        choices=[links[0],links[-1],links[len(links)//2]]
        seed=random.Random(1492+len(name)+len(links))
        choices+=seed.sample(links,min(max(0,target-3),len(links)))
        for u in choices:wanted.append(u)
    result=list(dict.fromkeys(wanted))
    return result[:69]

def inspect(u):
    if u.endswith("robots.txt"):
        try:
            r,seconds=get(u)
            return {"url":u,"status":r.status_code,"seconds":seconds,"body":r.text[:2000],
                    "robots_block_all":bool(re.search(r"(?m)^Disallow:\s*/\s*$",r.text))}
        except Exception as exc:return {"url":u,"status":"error","error":str(exc)[:200]}
    try:
        r,seconds=get(u)
        doc=BeautifulSoup(r.text,"html.parser")
        canonical=doc.find("link",rel="canonical")
        if canonical is None:
            canonical=doc.select_one('link[rel~="canonical"]')
        md=doc.select_one('meta[name="description"]')
        robots=doc.select_one('meta[name="robots"]')
        og=doc.select_one('meta[property="og:image"]')
        titles=doc.select("title")
        h1=doc.select("h1")
        main=doc.select_one("main") or doc.body
        main_text=main.get_text(" ",strip=True) if main else ""
        img=doc.select("img")
        scripts=doc.select("script[src]")
        css=doc.select('link[rel="stylesheet"]')
        htmlbytes=len(r.content)
        a={"url":u,"final_url":r.url,"status":r.status_code,"redirects":len(r.history),
            "seconds":seconds,"html_bytes":htmlbytes,"cache_control":r.headers.get("cache-control"),
            "cf_cache_status":r.headers.get("cf-cache-status"),
            "litespeed_cache":r.headers.get("x-litespeed-cache"),
            "x_robots":r.headers.get("x-robots-tag"),
            "server":r.headers.get("server"),
            "title":titles[0].get_text(" ",strip=True)[:150] if titles else None,
            "title_count":len(titles),
            "meta":md.get("content","")[:200] if md else None,
            "h1_count":len(h1),"h1":[x.get_text(" ",strip=True)[:140] for x in h1[:4]],
            "canonical":canonical.get("href") if canonical else None,
            "robots":robots.get("content") if robots else None,
            "og_image":og.get("content") if og else None,
            "images":len(img),"images_missing_alt":sum(not x.has_attr("alt") for x in img),
            "scripts":len(scripts),"stylesheets":len(css),
            "estimated_words":len(main_text.split()),"schema_blocks":len(doc.select('script[type="application/ld+json"]'))}
        a["canonical_self"]=bool(a["canonical"] and urllib.parse.urlsplit(a["canonical"]).path.rstrip("/") == urllib.parse.urlsplit(r.url).path.rstrip("/") and urllib.parse.urlsplit(a["canonical"]).hostname in ("www.a3tal.com","a3tal.com"))
        return a
    except Exception as exc:
        return {"url":u,"status":"error","error":str(exc)[:220]}

def summarize(a,checks):
    ok=[x for x in checks if x["status"]==200 and not x["url"].endswith("robots.txt")]
    return {
        "audited_at_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
        "sampled_urls":len(checks),
        "sitemap_url_total":sum(z.get("count",0) for z in a["children"].values()),
        "sitemap_issues":{k:v for k,v in a["children"].items() if v.get("status")!=200},
        "status_counts":dict(collections.Counter(str(x.get("status")) for x in checks)),
        "http_errors":[x for x in checks if x["status"] not in (200,301,302)],
        "redirects":[{"url":x["url"],"final":x.get("final_url")} for x in checks if x.get("redirects")],
        "canonical_mismatch":[{"url":x["url"],"canonical":x.get("canonical")} for x in ok if not x.get("canonical_self")],
        "noindex":[x["url"] for x in ok if "noindex" in (x.get("robots") or "").lower() or "noindex" in (x.get("x_robots") or "").lower()],
        "no_h1":[x["url"] for x in ok if x.get("h1_count")==0],
        "multiple_h1":[{"url":x["url"],"h1":x.get("h1")} for x in ok if x.get("h1_count",0)>1],
        "missing_titles":[x["url"] for x in ok if not x.get("title")],
        "missing_descriptions":[x["url"] for x in ok if not x.get("meta")],
        "thin_sample_under_200_words":[{"url":x["url"],"words":x.get("estimated_words")} for x in ok if x.get("estimated_words",0)<200],
        "slow_over_3s":[{"url":x["url"],"secs":x.get("seconds")} for x in ok if x.get("seconds",0)>3],
        "max_seconds":max((x.get("seconds",0) for x in ok),default=None),
        "median_seconds":round(sorted(x["seconds"] for x in ok)[len(ok)//2],3) if ok else None,
        "max_html_bytes":max((x.get("html_bytes",0) for x in ok),default=None),
        "largest_html":[{"url":x["url"],"bytes":x.get("html_bytes"),"images":x.get("images"),
             "scripts":x.get("scripts")} for x in sorted(ok,key=lambda x:-x.get("html_bytes",0))[:10]],
        "no_og":[x["url"] for x in ok if not x.get("og_image")],
        "no_schema":[x["url"] for x in ok if x.get("schema_blocks")==0]
    }

def main():
    a=root_and_sitemaps()
    list_urls=sample_urls(a)
    print("BEGIN_LOW_LOAD_SAMPLE",len(list_urls),flush=True)
    # Two workers only, to protect a site experiencing a suspected performance problem.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        inspected=list(ex.map(inspect,list_urls))
    summary=summarize(a,inspected)
    a["children"]={k:{key:val for key,val in z.items() if key!="all_urls"} for k,z in a["children"].items()}
    report={"sitemaps":a,"summary":summary,"sample":inspected}
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
    for name,v in summary.items():
        if name in ("canonical_mismatch","noindex","http_errors","slow_over_3s","thin_sample_under_200_words","multiple_h1","sitemap_issues"):
            print("AUDIT_FINDING",name,json.dumps(v,ensure_ascii=False)[:7500],flush=True)
        else:
            print("AUDIT_SUMMARY",name,json.dumps(v,ensure_ascii=False)[:1800],flush=True)
if __name__=="__main__":main()
