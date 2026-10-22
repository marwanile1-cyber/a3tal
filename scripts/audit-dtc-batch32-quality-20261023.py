#!/usr/bin/env python3
"""Read-only QA of the ALREADY-PUBLISHED DTC batch 32. No publishing or edits."""
import html,json,re,time,urllib.parse,urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CODES="P0345 P0742 P0868 U0194 U0422 U0418 C0072 C0071 B1443 B1446".split()
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
    req=urllib.request.Request(url,headers={"User-Agent":"A3talDTCReadOnlyAudit/2026-10-22","Accept":"application/json","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
def count_words(body):
    parser=TextReader();parser.feed(body)
    return len(re.findall(r"\S+",html.unescape(" ".join(parser.parts))))
def main():
    source=json.loads((ROOT/"data/dtc-original-batch-31.json").read_text(encoding="utf-8"))
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
          "canonical":canonical,
          "canonical_matches_permalink":canonical.rstrip("/")==str(post.get("link") or "").rstrip("/"),
          "meta_description_present":bool((seo.get("description") or "").strip()),
          "code_marker_present":f'data-a3tal-batch32="{code}"' in body,
          "temporary_photo":"batch32-temporary-photo" in image or "صورة توضيحية عامة مؤقتة" in body,
          "og_matches_featured":bool(image and image in og),
          "video_embedded":bool(re.search(r"(youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=)|youtu\.be/)",body,re.I)),
          "internal_dtc_links":len(re.findall(r"href=['\"]https?://a3tal\.com/dtc/",body,re.I)),
          "last_modified":post.get("modified")
        }
        results.append(status)
        print("BATCH32_QA "+json.dumps(status,ensure_ascii=False),flush=True)
    report={
     "batch":32,"checked":"2026-10-22","published":len(results),
     "below_1500":sum(x["under_1500"] for x in results),
     "temporary_photos":sum(x["temporary_photo"] for x in results),
     "wrong_og_images":sum(not x["og_matches_featured"] for x in results),
     "without_embedded_video":sum(not x["video_embedded"] for x in results),
     "wrong_canonical":sum(not x["canonical_matches_permalink"] for x in results),
     "missing_meta_description":sum(not x["meta_description_present"] for x in results),
     "missing_updated_diagnostic_chapter":sum(not x["code_marker_present"] for x in results),
     "results":results
    }
    Path("dtc-batch32-live-quality-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("BATCH32_QA_SUMMARY "+json.dumps({k:v for k,v in report.items() if k!="results"},ensure_ascii=False),flush=True)
    if report["wrong_og_images"] or report["wrong_canonical"]:
        raise RuntimeError("Batch32 published editorial/OG verification failed; see the artifact")
if __name__=="__main__":main()
