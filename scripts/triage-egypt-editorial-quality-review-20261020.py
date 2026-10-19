#!/usr/bin/env python3
"""Read-only priority queue for MANUAL editorial quality reviews on a3tal.com.

IMPORTANT: This is NOT a quality score. Automated fields are used only to
choose which posts a human editor should evaluate next. Never publish or
rewrite based on word count, missing images, link counts or this queue alone.
A <=80/100 editorial decision must be made by reviewing the actual article.
"""
import collections,json,os,re,time,urllib.parse
from pathlib import Path
import requests
from bs4 import BeautifulSoup
BASE="https://a3tal.com"
API=BASE+"/wp-json/wp/v2/posts"
OUT=Path("diagnostics")
OUT.mkdir(exist_ok=True)
SESSION=requests.Session()
SESSION.headers.update({"User-Agent":"A3tal-ReadOnly-Editorial-Quality-Review/2.0","Accept":"application/json"})
def fetch(page):
    params={"per_page":100,"page":page,"_fields":"id,slug,link,status,modified,title,content,featured_media,categories"}
    last=None
    for n in range(6):
        try:
            r=SESSION.get(API,params=params,timeout=60)
            if r.status_code==400 and page>1:return []
            if r.status_code in (403,429,500,502,503,504):
                last=f"HTTP {r.status_code} for page {page}";time.sleep(min(4*(n+1),16));continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            last=str(e);time.sleep(min(4*(n+1),16))
    raise RuntimeError("WordPress content inventory incomplete: "+str(last))
def text_of(value):
    return BeautifulSoup(value or "", "html.parser").get_text(" ",strip=True)
def analyze(p):
    soup=BeautifulSoup((p.get("content") or {}).get("rendered",""),"html.parser")
    for el in soup.select("script,style,noscript,svg"):el.decompose()
    body=soup.get_text(" ",strip=True)
    words=re.findall(r"[\u0600-\u06ffa-zA-Z0-9]+",body)
    headings=[re.sub(r"\s+"," ",x.get_text(" ",strip=True)).lower() for x in soup.select("h2,h3")]
    unique_h=len(set(headings))
    links=[str(a.get("href") or "") for a in soup.select("a[href]")]
    internals=[x for x in links if x.startswith(BASE)]
    externals=[x for x in links if x.startswith("http") and "a3tal.com" not in x]
    images=len(soup.select("img"))
    videos=len(soup.select("iframe[src*=youtube],iframe[src*=vimeo],video"))
    tables=len(soup.select("table"))
    has_oem=any(any(d in s for d in ("mgmotor.com.eg","toyota.com.eg","hyundai.com","kia.com","vauxhall.co.uk","renault.com","nissan","chery","volkswagen","ford.com")) for s in externals)
    flags=[]
    # Review triage flags are NOT individual reasons to change or lengthen a post.
    if len(words)<350:flags.append("very_short_body_review_priority")
    elif len(words)<700:flags.append("short_body_review_priority")
    if not headings:flags.append("missing_body_headings")
    if len(headings)>=6 and unique_h<len(headings)-2:flags.append("repeated_headings")
    if images==0:flags.append("no_inline_explanatory_media")
    if not internals:flags.append("no_stored_internal_context_links")
    if not externals:flags.append("no_inline_external_documentation")
    if len(externals)>0 and not has_oem:flags.append("external_citations_need_primary_source_review")
    if tables==0 and len(words)<1000:flags.append("no_short_diagnostic_table")
    if not p.get("featured_media"):flags.append("missing_featured_media")
    title=text_of((p.get("title") or {}).get("rendered"))
    review_priority=(4 if len(words)<350 else 2 if len(words)<700 else 0) + sum(1 for x in flags if x not in ("short_body_review_priority","very_short_body_review_priority"))
    return {
        "id":p["id"],"slug":p["slug"],"url":p["link"],"title":title,
        "body_words":len(words),"headings":len(headings),"distinct_headings":unique_h,
        "inline_images":images,"inline_videos":videos,"tables":tables,
        "internal_links":len(internals),"external_links":len(externals),
        "oem_reference_signal":has_oem,"featured_media":bool(p.get("featured_media")),
        "modified":p.get("modified"),"review_signals":flags,
        "review_queue_priority_not_quality_score":review_priority,
        "editorial_score":None,"editorial_decision":"unreviewed"
    }
def main():
    all_items=[];page=1
    while True:
        chunk=fetch(page)
        if not chunk:break
        for post in chunk:
            if post.get("status")=="publish":all_items.append(analyze(post))
        print("INVENTORY_PAGE",page,"COUNT",len(all_items),flush=True)
        if len(chunk)<100:break
        page+=1
        if page>60:raise RuntimeError("Suspicious endless pagination")
    if len(all_items)<500:raise RuntimeError("Incomplete Egypt post inventory, refusing report "+str(len(all_items)))
    all_items.sort(key=lambda a:(-a["review_queue_priority_not_quality_score"],a["body_words"]))
    summary={
        "published_normal_posts":len(all_items),
        "manual_quality_reviews_completed_this_job":0,
        "number_scored_80_or_below_this_job":None,
        "under_1500_words_for_context_only":sum(x["body_words"]<1500 for x in all_items),
        "no_inline_images_for_context_only":sum(x["inline_images"]==0 for x in all_items),
        "no_inline_external_documentation_for_context_only":sum(x["external_links"]==0 for x in all_items),
        "missing_featured":sum(not x["featured_media"] for x in all_items),
        "audit_scoring_note":"No automatic quality verdict. A sub-1500 post may be excellent. Only manual <=80 editorial review authorizes a rewrite.",
        "manual_review_rubric":"25 factual accuracy/safety;25 diagnostic usefulness;15 intent;10 original model-specific value;10 structure/UX;10 visuals;5 useful verified linking."
    }
    print("CONTENT_REVIEW_QUEUE_SUMMARY",json.dumps(summary,ensure_ascii=False),flush=True)
    for x in all_items[:35]:
        print("MANUAL_REVIEW_CANDIDATE",json.dumps({
            k:x[k] for k in ("id","slug","body_words","review_queue_priority_not_quality_score","review_signals")
        },ensure_ascii=False),flush=True)
    output={"summary":summary,"queue":all_items}
    (OUT/"a3tal-egypt-manual-quality-review-queue.json").write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding="utf-8")
    (OUT/"a3tal-egypt-manual-quality-review-top100.md").write_text(
       "# Egypt editorial review priority queue (not quality scores)\n\n"
       +"Only repair after a documented manual score of 80/100 or less. No length-only edits.\n\n"
       +"| Priority | URL | Words | Review signs |\n|---:|---|---:|---|\n"
       +"\n".join(f"| {x['review_queue_priority_not_quality_score']} | {x['url']} | {x['body_words']} | {', '.join(x['review_signals'])} |" for x in all_items[:100]),encoding="utf-8")
if __name__=="__main__":main()
