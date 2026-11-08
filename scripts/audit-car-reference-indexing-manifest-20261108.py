#!/usr/bin/env python3
"""Audit full car-reference sitemap, produce CSV for manual GSC/Bing indexing tracking.
Read only. Never claim Google indexing because a sitemap is submitted.
"""
import csv,json,os,re,time,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
import requests

BASE="https://a3tal.com"
SITEMAP=BASE+"/a3_car_ref-sitemap.xml"
ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"data/car-reference/a3tal-car-reference-indexing-manifest-live.csv"
REPORT=ROOT/"data/car-reference/a3tal-car-reference-indexing-audit-live.json"
session=requests.Session()
session.headers.update({"User-Agent":"A3tal-PSEO-Sitemap-ReadOnly-Audit/1.0"})
def get(url, timeout=60):
    err=None
    for i in range(4):
        try:
            r=session.get(url,timeout=timeout,headers={"Cache-Control":"no-cache"},params=({"audit":str(int(time.time()))} if i and "xml" not in url else {}))
            r.raise_for_status()
            return r
        except Exception as e:
            err=e
            if i<3:time.sleep(3*(i+1))
    raise RuntimeError("Cannot fetch "+url+" "+repr(err))

health=get(BASE+"/wp-json/a3tal-car-reference/v1/health").json()
assert health.get("ok") and health.get("drafts")==0
robots=get(BASE+"/robots.txt").text
assert "Disallow: /car-reference/" not in robots
assert "Sitemap:" in robots
sitemap=get(SITEMAP).text
assert "<urlset" in sitemap,("Not a urlset",sitemap[:600])
tree=ET.fromstring(sitemap)
ns={"sm":"http://www.sitemaps.org/schemas/sitemap/0.9"}
nodes=tree.findall("sm:url",ns)
if not nodes:nodes=tree.findall("url")
entries=[]
for item in nodes:
    loc=item.find("sm:loc",ns) or item.find("loc")
    # ElementTree has false-y elements; use explicit None check.
    loc=item.find("sm:loc",ns)
    if loc is None:loc=item.find("loc")
    last=item.find("sm:lastmod",ns)
    if last is None:last=item.find("lastmod")
    if loc is None or not loc.text:continue
    url=loc.text.strip()
    assert urlparse(url).hostname=="a3tal.com"
    entries.append((url,last.text.strip() if last is not None and last.text else ""))
assert len(entries)==len(set(url for url,_ in entries)),"Duplicate sitemap URLs"
published=health["published"]
car=[(u,lm) for u,lm in entries if "/car-reference/" in u and u.rstrip("/")!=BASE+"/car-reference"]
assert len(car)>=published-1,("Sitemap missing many published pages",len(car),published)
index=get(BASE+"/sitemap_index.xml").text
sitemap_linked=SITEMAP in index or "a3_car_ref-sitemap.xml" in index
assert sitemap_linked,"Main Yoast sitemap index is NOT linking to a3_car_ref-sitemap.xml"
# Representative spot checks across 313+ URLs, no heavy 300-request crawl.
sample=[entries[i][0] for i in sorted(set([0,len(entries)//4,len(entries)//2,3*len(entries)//4,len(entries)-1]))]
sample+= [u for u,_ in entries if "/car-reference/kia/ev5-longrange-egypt/" in u][:2]
samples=[]
for u in list(dict.fromkeys(sample)):
    html=get(u,timeout=70).text
    canonical=re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)',html,re.I) or re.search(r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical',html,re.I)
    assert canonical and canonical.group(1).rstrip("/")==u.rstrip("/"),("Canonical mismatch",u)
    robotsmatch=re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']+)',html,re.I)
    indexable=not(robotsmatch and "noindex" in robotsmatch.group(1).lower())
    assert indexable,("Sitemap contains a noindex page",u)
    samples.append({"url":u,"canonical":canonical.group(1),"robots":robotsmatch.group(1) if robotsmatch else "absent"})
CSV.parent.mkdir(parents=True,exist_ok=True)
with CSV.open("w",newline="",encoding="utf-8-sig") as f:
    wr=csv.writer(f)
    wr.writerow(["URL","lastmod","status","google_indexed","note"])
    for u,lm in entries:wr.writerow([u,lm,"in_sitemap","UNKNOWN - needs Search Console inspection",""])
report={"verified_at_utc":__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),"site":BASE,"published":published,"sitemap":SITEMAP,"sitemap_in_main_index":sitemap_linked,"sitemap_urls":len(entries),"reference_urls":len(car),"sample_checks":samples,"google_indexed":"UNKNOWN - sitemap inclusion is NOT indexing","robots_has_sitemap":True,"csv":str(CSV.relative_to(ROOT))}
REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
print("PSEO_INDEXING_SITEMAP_QA_PASS",json.dumps({k:report[k] for k in ("published","sitemap_urls","reference_urls","sitemap_in_main_index")},ensure_ascii=False))
for u,lm in entries:print("SITEMAP_URL\t"+u+"\t"+lm)
