#!/usr/bin/env python3
"""Propose contextual links only between already-indexable, topical article pairs.

Input: read-only complete sitemap crawl report. Outputs a reviewable JSON
before anything may be deployed. Avoids broad price/car/brand-only similarity.
"""
import collections
import json
import math
import re
import unicodedata
from urllib.parse import unquote, urlsplit
from pathlib import Path

raw = json.loads(Path("old-audit/seo-audit-report.json").read_text())
pages = [p for p in raw["pages"] if p.get("status")==200 and p["url"].startswith("https://a3tal.com/") and urlsplit(p["url"]).path.count("/") == 2 and "/category/" not in p["url"] and "/dtc/" not in p["url"]]
page_set = {p["url"] for p in pages}
stop = {
"أعطال","اعطال","للسيارات","السيارات","السيارة","سيارة","العربية","الموتور","مصر","المصري","المصرية",
"فى","في","عن","على","من","إلى","الى","مع","حتى","قبل","بعد","عند","أو","و","كل","هل","ما","كيف","متى","ايه","إيه",
"دليل","كامل","شامل","للتشخيص","التشخيص","تشخيص","الأسباب","اسباب","أسباب","الحلول","حلول","شرح","خطوات","أعراض","اعراض","سبب",
"المميزات","العيوب","مشاكل","مشكلة","الأعطال","طريقة","الفرق","أنواع","والأسعار","السعر","الاسعار","أسعار","سعر",
"صيانه","صيانة","الصيانة","والمواصفات","المواصفات","مواصفات","ومميزات","الفحص","فحص","الكتالوج",
"ومتطلبات","جديد","الجديد","وكيف","تعمل","يعمل","اخطر","اهم","أهم","الكاملة","الحقيقي","الصحيح","الصحيحة","لدى","لدي",
"خدمة","متاح","علامات","بالفيديو","حل","مراجعة","شراء","تحديث","بدون","معنى","على",
"أوتوماتيك","اوتوماتيك","automatic","2025","2026","2027","a3tal","com","guide","egypt","price","specs","review",
"and","the","with","for","how","to","when","fix","causes","symptoms","problems","diagnosis","car","cars",
"engine","motor","egyptian","new","2024","system","fault","faults","faulty","change","vs","types","which",
}
def text_tokens(s):
    s=unicodedata.normalize("NFKC",s.lower())
    s=re.sub(r"[\u064b-\u065f\u0670\u0640]","",s)
    s=s.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ى","ي")
    s=re.sub(r"(?:\s*[-|]\s*(?:أعطال|اعطال).*)$", "", s)
    tokens=re.findall(r"[\w]+",s,flags=re.U)
    return frozenset(t for t in tokens if len(t)>2 and t not in stop and not t.isdigit() and not re.fullmatch(r"20\d\d",t))
post_tokens={p["url"]:text_tokens(p.get("title","")) for p in pages}
freq=collections.Counter(w for tt in post_tokens.values() for w in tt)
n=len(pages)
def sim(x,y):
    common=post_tokens[x]&post_tokens[y]
    if len(common)<2:return 0,[]
    # Penalize price-year generic vocabulary and brand-only pairs
    weights={w:math.log(1+(n/(1+freq[w]))) for w in common}
    wsum=sum(weights.values())
    rarities=[w for w in common if freq[w]<int(n*.15)]
    if len(rarities)<2: return 0,[]
    numerator=wsum
    den=math.sqrt((sum(math.log(1+n/(1+freq[t])) for t in post_tokens[x]))*
                  (sum(math.log(1+n/(1+freq[t])) for t in post_tokens[y])))
    return numerator/max(den,1), sorted(common)
titled={p["url"]:p.get("title","").split("|")[0].strip() for p in pages}
out=[]
for page in pages:
    url=page["url"]
    if any(link in page_set and link!=url for link in page.get("context_links",[])):continue
    if len(post_tokens[url])<2:continue
    arr=[]
    for target in pages:
        v=target["url"]
        if url==v or v in page.get("main_links",[]) or len(post_tokens[v])<2:continue
        score, tokens=sim(url,v)
        if score>=0.46:
            arr.append((round(score,3),v,tokens))
    arr.sort(reverse=True)
    if not arr:continue
    # Pick 1-2 strongly aligned, but avoid two same title slugs
    chosen=[]
    for score,v,tokens in arr:
        if len(chosen)>=2:break
        if any(v in c["url"] or c["url"] in v for c in chosen):continue
        chosen.append({"url":v,"title":titled[v],"score":score,"shared":tokens})
    if chosen:out.append({"source":url,"title":titled[url],"targets":chosen})
print("SUGGESTED_CONTEXT_LINKS",json.dumps({"pages":len(pages),"proposed_sources":len(out),"sample":out[:75]},ensure_ascii=False),flush=True)
Path("context-links-reviewed-candidates.json").write_text(json.dumps({"count":len(out),"pairs":out},ensure_ascii=False,indent=2))
