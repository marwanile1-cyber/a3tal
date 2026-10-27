#!/usr/bin/env python3
"""Read-only QA of the ALREADY-PUBLISHED DTC batch 33. No publishing or edits."""
import html,json,re,time,urllib.parse,urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CODES="P0359 P0360 P0485 P0762 P0763 P0874 U0206 U0207 U0215 U0216".split()
BASE="https://a3tal.com"
class TextReader(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.depth=0
    def handle_starttag(self,tag,attrs):
        if tag in ("script","style"):self.depth+=1
    def handle_endtag(self,tag):
        if tag in ("script","style"):self.depth=max(self.depth-1,0)
    def handle_data(self,data):
        if not self.depth:self.parts.append(data)
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"A3talDTCReadOnlyAudit/2026-10-27","Accept":"application/json","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
def count_words(body):
    parser=TextReader();parser.feed(body)
    return len(re.findall(r"\S+",html.unescape(" ".join(parser.parts))))
def main():
    source=json.loads((ROOT/"data/dtc-original-batch-37.json").read_text(encoding="utf-8"))
    if [x["code"] for x in source["items"]]!=CODES:raise RuntimeError("Batch roster mismatch")
    results=[]
    for item in source["items"]:
        code=item["code"]
        query=urllib.parse.urlencode({"slug":code.lower(),"per_page":2,
        "_fields":"id,slug,status,content,featured_media,yoast_head_json,link,modified"})
        posts=fetch(BASE+"/wp-json/wp/v2/a3tal-dtc?"+query+"&nonce="+str(time.time_ns()))
        if not isinstance(posts,list) or len(posts)!=1 or posts[0].get("slug")!=code.lower():raise RuntimeError("Missing/duplicate "+code)
        post=posts[0]
        if post.get("status")!="publish":raise RuntimeError("Not published "+code)
        body=(post.get("content") or {}).get("rendered","")
        wc=count_words(body) if body else 0
        mid=int(post.get("featured_media") or 0)
        media=fetch(BASE+f"/wp-json/wp/v2/media/{mid}?_fields=id,source_url,mime_type") if mid else {}
        image=media.get("source_url","")
        og=[x.get("url","") for x in (post.get("yoast_head_json") or {}).get("og_image",[]) if isinstance(x,dict)]
        seo=post.get("yoast_head_json") or {}
        canonical=seo.get("canonical") or ""
        status={
          "code":code,"id":post["id"],"url":post.get("link"),
          "words":wc,"source_words":item.get("word_count"),"under_1500":wc<1500,
          "featured_media":mid,"image":image,
          "webp":media.get("mime_type")=="image/webp",
          "robots_index_allowed":"noindex" not in str((seo.get("robots") or {}).get("index") or "index").lower(),
          "canonical":canonical,
          "canonical_matches_permalink":canonical.rstrip("/")==str(post.get("link") or "").rstrip("/"),
          "meta_description_present":bool((seo.get("description") or "").strip()),
          "code_marker_present":(code in body and body.count("<h2")>=10),
          "temporary_photo":"batch37-temporary-photo" in image or "صورة توضيحية عامة مؤقتة" in body,
          "og_matches_featured":bool(image and image in og),
          "video_embedded":bool(re.search(r"(youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=)|youtu\.be/)",body,re.I)),
          "internal_dtc_links":len(re.findall(r"href=['\"]https?://a3tal\.com/dtc/",body,re.I)),
          "last_modified":post.get("modified")
        }
        results.append(status)
        print("BATCH37_QA "+json.dumps(status,ensure_ascii=False),flush=True)
    report={
     "batch":37,"checked":"2026-10-27","published":len(results),
     "below_1500":sum(x["under_1500"] for x in results),
     "temporary_photos":sum(x["temporary_photo"] for x in results),
     "wrong_og_images":sum(not x["og_matches_featured"] for x in results),
     "without_embedded_video":sum(not x["video_embedded"] for x in results),
     "wrong_canonical":sum(not x["canonical_matches_permalink"] for x in results),
     "missing_meta_description":sum(not x["meta_description_present"] for x in results),
     "missing_updated_diagnostic_chapter":sum(not x["code_marker_present"] for x in results),
     "non_webp_images":sum(not x["webp"] for x in results),
     "noindex_pages":sum(not x["robots_index_allowed"] for x in results),
     "missing_internal_links":sum(x["internal_dtc_links"]<1 for x in results),
     "results":results
    }
    Path("dtc-batch37-live-quality-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("BATCH37_QA_SUMMARY "+json.dumps({k:v for k,v in report.items() if k!="results"},ensure_ascii=False),flush=True)
    if (report["below_1500"] or report["wrong_og_images"] or report["wrong_canonical"] or
        report["missing_meta_description"] or report["missing_updated_diagnostic_chapter"] or
        report["non_webp_images"] or report["noindex_pages"] or report["missing_internal_links"]):
        raise RuntimeError("Batch37 published editorial/OG verification failed; see the artifact")
if __name__=="__main__":main()
