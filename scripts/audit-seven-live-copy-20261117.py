#!/usr/bin/env python3
"""Read-only quality and stale-date audit of the seven revised Egypt articles."""
import os,json,re,html,urllib.request,urllib.error,time
IDS=[79964,80401,79,80669,80266,80534,80056]
API="https://a3tal.com/wp-json/a3tal-direct/v1"
KEY=os.getenv("A3TAL_API_KEY","")
if not KEY: raise RuntimeError("Missing Direct Bridge key")
def get(pid):
    req=urllib.request.Request(f"{API}/post/{pid}",headers={"X-A3tal-Key":KEY,"Authorization":"Bearer "+KEY,"Cache-Control":"no-cache","Accept":"application/json","User-Agent":"curl/8.5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=100) as r:return json.load(r)
        except urllib.error.HTTPError as exc:
            if attempt==2:raise
            print("RETRY_BRIDGE_READ",pid,exc.code,flush=True)
            time.sleep(4+attempt*3)
def norm(s):
    s=html.unescape(re.sub(r'<[^>]+>',' ',s))
    return re.sub(r'\s+',' ',s).strip()
for pid in IDS:
    p=get(pid);content=p.get("content") or ""
    print("\n==== DOCUMENT",pid,p.get("link"),"DATE",p.get("modified_gmt"),"SIZE",len(content),"====",flush=True)
    print("TITLE",p.get("title"),"STATUS",p.get("status"),"FEATURED",p.get("featured_media"),flush=True)
    print("HTML_ANCHORS",len(re.findall(r'<a\b',content,re.I)),"IMAGES",len(re.findall(r'<img\b',content,re.I)),"H2",len(re.findall(r'<h2\b',content,re.I)),flush=True)
    for k,m in enumerate(re.finditer(r'(?:آخر\s+(?:تحديث|مراجعة)|تحديث\s+(?:رسمي|البيانات|الأرقام)|آخر\s+فحص|مراجعة\s+(?:الأسعار|الأرقام|البيانات)|سبتمبر|أكتوبر|أغسطس|نوفمبر|ديسمبر|2027|سعر\s+(?:الكاوتش|الفردة))',content,re.I)):
        # Print surrounding sentence or HTML paragraph near match, deduplicate long repetitions
        st=max(0,m.start()-120);en=min(len(content),m.end()+150)
        snippet=norm(content[st:en])
        print("DATED_CONTEXT",k,snippet[:320],flush=True)
        if k>=80:break
    for match in re.finditer(r'<!--([\s\S]*?)-->',content):
        val=norm(match.group(1))
        if "SEO" in val or "2027" in val or "مقترح" in val or "التحديث" in val:
            print("EDITORIAL_COMMENT",val[:500],flush=True)
    if pid==80056:
        print("CLUTCH_OPENING",repr(content[:1600]),flush=True)
        print("CLUTCH_CSS_MATCH",bool(re.search(r'body\s*\{[^<]*font-family',content,re.I)),flush=True)
    print("QA_COMPLETED",pid,flush=True)
