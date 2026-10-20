#!/usr/bin/env python3
"""Read-only exhaustive content screening of every published WordPress post on a3tal.com.
Emits per-URL evidence and priority for a subsequent human editorial review.
IMPORTANT: The 0-100 screening index is NOT a manual factual-quality judgment
and MUST NOT be treated as Google's rating or the owner's 80% editing threshold.
Does not publish, edit, noindex, redirect, delete or update anything on WordPress.
"""
from __future__ import annotations
import collections,csv,datetime as dt,gzip,hashlib,html,json,math,os,re,time
from pathlib import Path
from urllib.parse import urlparse,urljoin
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from concurrent.futures import ThreadPoolExecutor,as_completed

SITE="https://a3tal.com"
REPORT=Path("diagnostics/egypt-sitewide-content-20261020")
REPORT.mkdir(parents=True,exist_ok=True)
UA="A3talEgyptSiteWideReadOnlyQualityAudit/20261020 (+GitHubActions)"
WS=re.compile(r"[\u0621-\u064a\u0671-\u06d3][\u0621-\u064a\u064b-\u065f\u0671-\u06d3]*|[A-Za-z][A-Za-z0-9_-]*|\d+(?:[.,]\d+)?")
STRIP={"script","style","noscript","svg","template","iframe","figcaption"}
ARABIC_DIA=["فحص","تشخيص","اختبار","قياس","افحص","يراجع","يراجع","عطل","الأعراض","التسريب","كود","حساس","الضغط","الأكواد","السائل","فتيس","المحرك"]
ARABIC_SAFE=["توقف","بأمان","سلامة","خطر","الحروق","تجنب","لا تفتح","لا تستخدم","فني مؤهل","مختص"]
ARABIC_UNSOURCED=["الأفضل","الأرخص","الأقوى","حصري","مضمون","نهائي"]
OFFICIAL=("toyota.com","hyundai-egypt","kia.com","skoda-egypt","skoda-storyboard",
"mgmotor.com","opel","vauxhall","renault","bmwgroup","nissan.com","honda","geely","chery","jetour","gov.eg","gov.uk","bosch","continental")
EXCLUDE_HOST=("a3tal.com","www.a3tal.com","localhost")
HEADINGS_RE=re.compile(r"^(?:p|u|c|b)\d{4}$",re.I)

def txt_count(s):
    return len(WS.findall(s))
def norm(s):
    s=re.sub(r"\s+"," ",s or "").strip().lower()
    s=re.sub(r"[\u064b-\u065f\u0670\u0640]","",s)
    return s

def request_posts():
    ses=requests.Session();ses.headers.update({"User-Agent":UA,"Accept":"application/json","Cache-Control":"no-cache"})
    all_posts=[];page=1;pages=[]
    while True:
        query={"per_page":100,"page":page,"orderby":"id","order":"asc",
           "_fields":"id,slug,status,link,title,content,excerpt,date,modified,featured_media,categories,author,tags"}
        err=None
        for attempt in range(5):
            try:
                r=ses.get(SITE+"/wp-json/wp/v2/posts",params=query,timeout=80)
                if r.status_code==400 and page>1:return all_posts,pages
                r.raise_for_status()
                dat=r.json()
                if not isinstance(dat,list):raise RuntimeError("WP unexpected response shape")
                break
            except Exception as e:
                err=e
                if attempt==4:raise RuntimeError(f"Page {page} of WordPress REST failed: {err}")
                time.sleep((attempt+1)*5)
        pages.append({"page":page,"records":len(dat),"x_total":r.headers.get("X-WP-Total"),"x_pages":r.headers.get("X-WP-TotalPages")})
        all_posts+=dat
        print("SITEWIDE_WP_PAGE",page,"records",len(dat),"total",len(all_posts),flush=True)
        if not dat or len(dat)<100:break
        page+=1
        if page>100:raise RuntimeError("Too many WP pages; abort to avoid infinite loop")
    ids=[x["id"] for x in all_posts]
    if len(ids)!=len(set(ids)):raise RuntimeError("Duplicate WordPress IDs across REST pages")
    if any(x.get("status")!="publish" for x in all_posts):raise RuntimeError("Unpublished article in inventory")
    return all_posts,pages

def intent(title,slug):
    t=title.lower()+" "+slug.lower()
    if HEADINGS_RE.search(slug.split("/")[-1]) or re.search(r"fault.codes|dtc.dictionary|dtc/|أكواد|كود عطل",t):return "اكواد وتشخيص"
    if re.search(r"service.center|مراكز الصيانة|مركز صيانة|الخط الساخن|مراكز الخدمة",t):return "مراكز وخدمة"
    if re.search(r"سعر|أسعار|price|prices|pricing|تسعير",t):return "أسعار ومقارنات"
    if re.search(r"أعطال|مشاكل|مشكلات|problems|diagnos|صيانة|repair|تسريب|تقطيع|تبريد|الفتيس|عيوب",t):return "أعطال وإصلاح"
    if re.search(r"مواصفات|specs|review|تجربة|مقارنة|vs-|دليل",t):return "مواصفات ومراجعات"
    return "مقالات عامة وأخبار"

def parse_post(p):
    raw=(p.get("content") or {}).get("rendered") or ""
    soup=BeautifulSoup(raw,"html.parser")
    for t in soup.find_all(STRIP):t.decompose()
    text=soup.get_text(" ",strip=True)
    words=txt_count(text)
    title=BeautifulSoup((p.get("title") or {}).get("rendered",""),"html.parser").get_text(" ",strip=True)
    headings=[norm(h.get_text(" ",strip=True)) for h in soup.select("h2,h3,h4") if h.get_text(" ",strip=True)]
    head2=[norm(h.get_text(" ",strip=True)) for h in soup.select("h2") if h.get_text(" ",strip=True)]
    para=[norm(x.get_text(" ",strip=True)) for x in soup.select("p,li") if txt_count(x.get_text(" ",strip=True))>=25]
    images=soup.select("img")
    links=soup.select("a[href]")
    internal=[];external=[];off=[]
    for link in links:
        link_url=urljoin(p.get("link") or SITE,link.get("href","").strip())
        parsed=urlparse(link_url)
        if parsed.scheme not in ("http","https"):continue
        host=(parsed.hostname or "").lower()
        if host in EXCLUDE_HOST:
            internal.append(link_url.split("?")[0].rstrip("/")+"/")
        else:
            external.append(link_url)
            if any(v in host for v in OFFICIAL):off.append(link_url)
    normtext=norm(text)
    snippets=[k for k in ARABIC_DIA if k in normtext]
    safe=[k for k in ARABIC_SAFE if k in normtext]
    unique_h=len(set(headings))
    dup_heading_count=len(headings)-unique_h
    long_p=sum(txt_count(t)>145 for t in para)
    has_list=bool(soup.select("ul li,ol li"))
    has_table=bool(soup.select("table"))
    has_video=bool(soup.select("iframe[src*=youtube],iframe[src*=vimeo],video")) or "youtube.com" in raw or "youtu.be" in raw
    type_=intent(title,p["slug"])
    result={
        "id":p["id"],"slug":p["slug"],"title":title,"url":p.get("link") or SITE+"/"+p["slug"]+"/",
        "intent":type_,"modified":p.get("modified",""),"published":p.get("date",""),
        "words":words,"h2":len(head2),"h3":len(soup.select("h3")),"unique_headings":unique_h,"repeated_headings":dup_heading_count,
        "paragraphs_over_145_words":long_p,"tables":len(soup.select("table")),"has_list":has_list,
        "inline_images":len(images),"images_missing_alt":sum(not x.get("alt","").strip() for x in images),
        "has_featured":bool(p.get("featured_media")),"has_video":has_video,
        "links_internal":len(internal),"links_external":len(external),"links_official":len(off),
        "distinct_external_hosts":len(set((urlparse(u).hostname or "").lower() for u in external)),
        "body_text_sha256":hashlib.sha256(normtext.encode()).hexdigest(),
        "factual_source_note":"Automatic inventory only: citations and official domains do not prove factual correctness.",
        "_text":normtext,"_paragraphs":para,"_internal_urls":internal,"_external_urls":external,
        "_diag_terms":len(set(snippets)),"_safety_terms":len(set(safe)),
    }
    return result

def prepare_duplicates(rows):
    vec=TfidfVectorizer(analyzer="char",ngram_range=(3,5),min_df=2,max_df=.88,
        max_features=80000,sublinear_tf=True,dtype="float32")
    corpus=[r["_text"][:22000] for r in rows]
    matrix=vec.fit_transform(corpus)
    sims=cosine_similarity(matrix,dense_output=True)
    for i in range(len(rows)):sims[i,i]=0
    dup_pairs=[]
    for i,r in enumerate(rows):
        j=int(sims[i].argmax())
        r["closest_similarity"]=round(float(sims[i,j]),4)
        r["closest_url"]=rows[j]["url"]
        r["near_duplicate_candidate"]=bool(sims[i,j]>=.85 and min(r["words"],rows[j]["words"])>=400)
        for k in range(i+1,len(rows)):
            if sims[i,k]>=.82 and min(r["words"],rows[k]["words"])>=300:
                dup_pairs.append({"url_a":r["url"],"url_b":rows[k]["url"],
                    "similarity":round(float(sims[i,k]),4),
                    "words_a":r["words"],"words_b":rows[k]["words"]})
    return sorted(dup_pairs,key=lambda x:-x["similarity"])

def repeat_paras(rows):
    index=collections.defaultdict(set)
    for i,r in enumerate(rows):
        for p in set(r["_paragraphs"]):
            if txt_count(p)>=35:index[hashlib.sha256(p.encode()).hexdigest()].add(i)
    for i,r in enumerate(rows):
        repeats=0
        for p in set(r["_paragraphs"]):
            if txt_count(p)>=35 and len(index[hashlib.sha256(p.encode()).hexdigest()])>=2:repeats+=1
        r["shared_long_paragraphs"]=repeats
    return sum(len(ix)>=2 for ix in index.values())

def screen(r):
    w=r["words"];kind=r["intent"]
    # Transparent evidence index, NOT an authoritative quality score.
    depth=min(17,round(17*min(w,1500)/1500)) + min(5,r["h2"]) + min(3,r["h3"]//2)
    app=min(15,r["_diag_terms"]*2) if kind in ("أعطال وإصلاح","اكواد وتشخيص") else min(15,r["_diag_terms"]*2+int(r["has_list"])*3)
    app+=min(5,r["_safety_terms"]*2) if kind in ("أعطال وإصلاح","اكواد وتشخيص") else int(r["has_list"])*3
    app+=3*int(r["tables"]>0)+2*int(r["has_list"])
    app=min(25,app)
    evidence=min(8,r["links_official"]*4)+min(8,r["links_external"]*2)+4*int(r["links_external"]>0 and r["distinct_external_hosts"]>1)
    evidence=min(20,evidence)
    ux=min(6,r["inline_images"]*3)+int(r["has_video"])*2+2*int(r["has_featured"])+int(r["has_list"])*2+int(r["tables"]>0)*2
    ux+=2 if r["inline_images"] and r["images_missing_alt"]==0 else 0
    ux=min(15,ux)
    nav=min(10,3*min(r["links_internal"],3)+int(r["links_external"]>0))
    uniqueness=5
    if r["closest_similarity"]>=.90:uniqueness=0
    elif r["closest_similarity"]>=.85:uniqueness=2
    elif r["shared_long_paragraphs"]>=2:uniqueness=2
    elif r["shared_long_paragraphs"]:uniqueness=4
    index=sum((depth,app,evidence,ux,nav,uniqueness))
    flags=[]
    if w<1500:flags.append("أقل من سياسة 1500 كلمة")
    if w<600:flags.append("شرح شديد الاختصار")
    if r["h2"]<3:flags.append("عناوين فرعية غير كافية")
    if r["links_official"]==0:flags.append("لا مراجع رسمية مرتبطة داخل المتن")
    if not r["links_external"]:flags.append("دون مصادر خارجية داخل المتن")
    if not r["inline_images"]:flags.append("لا صور داخل المتن")
    if not r["has_featured"]:flags.append("الصورة البارزة مفقودة")
    if not r["links_internal"]:flags.append("لا روابط داخلية داخل المتن")
    if r["near_duplicate_candidate"]:flags.append("تشابه نصي مرتفع يحتاج تحقق من النية والتكرار")
    if r["shared_long_paragraphs"]>=2:flags.append("فقرات طويلة منسوخة في مقالات أخرى")
    if r["repeated_headings"]>=2:flags.append("عناوين فرعية مكررة داخل المقال")
    if r["images_missing_alt"]>=2:flags.append("نصوص بديلة ناقصة لصور")
    if kind in ("أسعار ومقارنات","مقالات عامة وأخبار") and r.get("modified","")[:4] and r["modified"][:4]<"2026":
        flags.append("محتوى أسعار/أخبار قديم: يلزم فحص التاريخ والحقائق")
    if kind in ("أعطال وإصلاح","اكواد وتشخيص") and r["_diag_terms"]<5:
        flags.append("خطوات التشخيص العملي محدودة")
    # Screening only. Do not use 80 as permission to edit.
    r["screening_index_0_100"]=int(index)
    r["screening_band"]="أولوية مراجعة مرتفعة" if index<55 else ("مراجعة تحريرية مطلوبة" if index<80 else "مؤشرات بنيوية جيدة: يلزم تحقق الحقائق")
    r["flags"]=flags
    # Conservative manual priority primarily based on evidence, not length only.
    severity=(int(r["near_duplicate_candidate"])*18+min(35,max(0,1500-w)//50)
      + (14 if kind in ("أعطال وإصلاح","اكواد وتشخيص") and r["_diag_terms"]<5 else 0)
      + (12 if not r["links_external"] else 0)
      + (10 if not r["links_internal"] else 0)
      + (8 if not r["inline_images"] else 0)
      + (9 if r["shared_long_paragraphs"]>=2 else 0)
      + (8 if not r["has_featured"] else 0))
    r["review_priority_0_100"]=min(100,int(severity))
    return r

def run():
    raw,pages=request_posts()
    rows=[parse_post(p) for p in raw]
    pairs=prepare_duplicates(rows)
    rep=repeat_paras(rows)
    rows=[screen(r) for r in rows]
    output_cols=[
       "review_priority_0_100","screening_band","screening_index_0_100",
       "id","url","slug","title","intent","words","h2","h3","tables",
       "has_list","inline_images","images_missing_alt","has_featured","has_video",
       "links_internal","links_external","links_official","distinct_external_hosts",
       "closest_similarity","closest_url","near_duplicate_candidate","shared_long_paragraphs",
       "published","modified","flags"
    ]
    rows.sort(key=lambda r:(-r["review_priority_0_100"],r["screening_index_0_100"],r["slug"]))
    def safe(r):return {k:("; ".join(r[k]) if k=="flags" else r.get(k,"")) for k in output_cols}
    with open(REPORT/"all_articles_screening.csv","w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=output_cols);w.writeheader();w.writerows(safe(r) for r in rows)
    (REPORT/"all_articles_screening.json").write_text(json.dumps([safe(r) for r in rows],ensure_ascii=False,indent=2),encoding="utf-8")
    with open(REPORT/"near_duplicate_candidates.csv","w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["url_a","url_b","similarity","words_a","words_b"]);w.writeheader();w.writerows(pairs)
    # Compact full normalized text kept in Actions artifact only for follow-on editorial checks,
    # not committed to the repository or deployed to production.
    with gzip.open(REPORT/"source_article_text_for_review.json.gz","wt",encoding="utf-8") as f:
        json.dump([{"id":r["id"],"url":r["url"],"title":r["title"],"text":r["_text"]} for r in rows],f,ensure_ascii=False)
    counter=collections.Counter(r["intent"] for r in rows)
    bands=collections.Counter(r["screening_band"] for r in rows)
    summary={
      "as_of_utc":dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
      "scope":"All currently published standard WordPress posts returned by public a3tal.com REST /wp/v2/posts. Custom post types and pages NOT included.",
      "count":len(rows),"rest_pages":pages,"by_intent":dict(counter),"screening_bands":dict(bands),
      "under_600":sum(r["words"]<600 for r in rows),
      "under_1000":sum(r["words"]<1000 for r in rows),
      "under_1500":sum(r["words"]<1500 for r in rows),
      "over_or_equal_1500":sum(r["words"]>=1500 for r in rows),
      "zero_inline_images":sum(r["inline_images"]==0 for r in rows),
      "missing_featured":sum(not r["has_featured"] for r in rows),
      "zero_internal_links":sum(not r["links_internal"] for r in rows),
      "zero_external_sources":sum(not r["links_external"] for r in rows),
      "zero_official_links":sum(not r["links_official"] for r in rows),
      "repeat_long_paragraph_signatures":rep,
      "near_duplicate_candidates_85pct_articles":sum(r["near_duplicate_candidate"] for r in rows),
      "near_duplicate_pairs_82pct":len(pairs),
      "score_warning":"Automated 0-100 screening_index is NOT a true 80%-quality grade. Do not auto-edit from it. Factual accuracy, source recency, original reporting, intent-match and real photo/video authenticity require independent editorial validation.",
      "no_content_edits":True,
      "top_review_priorities":[{k:r[k] for k in ("id","url","title","intent","words","screening_index_0_100","review_priority_0_100","flags")} for r in rows[:35]],
      "strong_screening_examples":[{k:r[k] for k in ("url","words","screening_index_0_100")} for r in sorted(rows,key=lambda r:-r["screening_index_0_100"])[:12]],
    }
    (REPORT/"executive_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    md=[
      "# فحص محتوى جميع المقالات المنشورة - أعطال مصر",
      "",
      "تاريخ الفحص (UTC): "+summary["as_of_utc"],
      "",
      "**مهم:** مؤشر الفحص الآلي (0-100) لتحديد أولوية المراجعة التحريرية، وليس تقييم جودة نهائيًا. لا يعني تجاوز 80 أن الحقائق كلها سليمة، ولا يسمح انخفاضه بتعديل المقال دون مراجعة بشرية.",
      "",
      "لم يتم تعديل أو نشر أو إخفاء أي مقال أثناء الفحص.",
      "",
      "| المؤشر | العدد |","|---|---:|",
      *[f"| {k} | {summary[k]} |" for k in ("count","under_600","under_1000","under_1500","over_or_equal_1500","zero_inline_images","missing_featured","zero_internal_links","zero_external_sources","zero_official_links","near_duplicate_candidates_85pct_articles","near_duplicate_pairs_82pct")],
      "",
      "## توزيع مؤشرات الفرز","",
      *[f"- {k}: {v}" for k,v in bands.items()],
      "",
      "## المقالات الأكثر حاجة إلى مراجعة تحريرية",
      "",
      "| الرابط | كلمات | مؤشر فرز | أولوية | أبرز إشارات النقص |",
      "|---|---:|---:|---:|---|",
      *[f"| [{r['slug']}]({r['url']}) | {r['words']} | {r['screening_index_0_100']} | {r['review_priority_0_100']} | {'، '.join(r['flags'][:3])} |" for r in rows[:35]],
      "",
      "## ملفات التفاصيل",
      "",
      "- all_articles_screening.csv: قياسات ومؤشرات جميع المقالات، مصنفة حسب أولوية الفحص.",
      "- all_articles_screening.json: البيانات نفسها بصيغة قابلة للتحليل.",
      "- near_duplicate_candidates.csv: أزواج تشابه نصي تستلزم مراجعة نية البحث قبل أي دمج أو Redirect.",
      "- source_article_text_for_review.json.gz: نصوص جميع المقالات لمراجعة موضوعية لاحقة.",
      "",
      "## حدود الاستنتاج",
      "",
      "- الروابط والمراجع تم جردها داخل نص المقال، **ولم يتم إثبات أن كل رابط يعمل** أو أن المصدر يثبت صحة كل معلومة.",
      "- التشابه النصي لا يثبت سرقة أو تكرار نية البحث؛ يجب فتح كل زوج.",
      "- 1500 كلمة معيار نشر حدده صاحب الموقع لكنه ليس شهادة بأن المقال دقيق أو مفيد.",
      "- صور الترويسة والوسائط الديناميكية قد تظهر في الواجهة حتى إن لم تظهر في REST body.",
      "- التقرير يغطي نوع post المنشور فقط؛ لا يغطي custom post types أو الصفحات الثابتة.",
      "",
    ]
    (REPORT/"REPORT_AR.md").write_text("\n".join(md),encoding="utf-8")
    print("SITEWIDE_AUDIT_EXEC_SUMMARY",json.dumps({k:v for k,v in summary.items() if k not in ("rest_pages","top_review_priorities","strong_screening_examples")},ensure_ascii=False),flush=True)
    print("SITEWIDE_REVIEW_TOP_35",json.dumps(summary["top_review_priorities"],ensure_ascii=False),flush=True)
    print("SITEWIDE_AUDIT_FINISHED",len(rows),"No WP writes",flush=True)
    if len(rows)<400:raise RuntimeError("Suspiciously few posts for a site expected to have 570+ published; abort accepted status")
if __name__=="__main__":run()
