#!/usr/bin/env python3
"""Non-negotiable editorial acceptance gate for a3tal.com/Egypt.

The 1500-word count applies to *article body text*, not headings from the
website, sidebar/navigation, alt text, CSS, scripts, HTML attributes or schema.
Images/tables/videos may enhance an article but never replace 1500 real words.

This script is a pre-publish guard; it does not silently noindex, unpublish,
truncate or change the canonical URL of older posts awaiting rehabilitation.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

MINIMUM_WORDS = 1500
# Count real text words, including Arabic, Latin and ordinary numeric technical
# codes, rather than HTML tags, images, URLs and metadata.
WORD_RE = re.compile(r"[\u0621-\u064a\u0671-\u06d3][\u0621-\u064a\u064b-\u065f\u0671-\u06d3]*|[A-Za-z][A-Za-z0-9_-]*|\d+(?:[.,]\d+)?")
EXCLUDE = {"script", "style", "noscript", "svg", "template", "iframe", "figcaption"}
class BodyText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ignore = 0
        self.parts = []
    def handle_starttag(self, name, attrs):
        if name in EXCLUDE:
            self.ignore += 1
    def handle_endtag(self, name):
        if name in EXCLUDE and self.ignore:
            self.ignore -= 1
    def handle_data(self, data):
        if not self.ignore:
            self.parts.append(data)
    def handle_entityref(self, name):
        if not self.ignore:
            self.parts.append(html.unescape("&"+name+";"))
def count_editorial_words(body_html):
    parser = BodyText()
    parser.feed(body_html or "")
    parser.close()
    return len(WORD_RE.findall(" ".join(parser.parts)))
def require_minimum(body_html, slug, minimum=MINIMUM_WORDS):
    count=count_editorial_words(body_html)
    if count<minimum:
        raise ValueError(
            f"EDITORIAL_REJECTED {slug}: {count} body words; at least "
            f"{minimum} required, missing {minimum-count}. "
            "No publish/acceptance permitted. Expand with distinctive "
            "diagnosis, verified sources, useful steps and factual tables, "
            "not padding or repeated text."
        )
    return count
def validate_manifest(path):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    items=data.get("articles",data.get("items",[]))
    if not items: raise ValueError("Empty or invalid editorial manifest")
    seen=set()
    for article in items:
        slug=article["slug"]
        if slug in seen:raise ValueError("Duplicate URL slug "+slug)
        seen.add(slug)
        require_minimum(article.get("content") or article.get("html",""),slug)
        print("EDITORIAL_1500_PASS",slug,flush=True)
    print("EDITORIAL_MANIFEST_1500_PASS",path,len(items),flush=True)
if __name__=="__main__":
    if len(sys.argv)<2:raise SystemExit("Usage: python3 scripts/editorial_minimum_words.py PATH_TO_MANIFEST.json")
    for p in sys.argv[1:]:validate_manifest(p)
