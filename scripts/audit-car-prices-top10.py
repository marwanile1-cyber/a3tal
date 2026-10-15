#!/usr/bin/env python3
"""Read-only QA of ten published /cars/ entities using public WordPress REST and
the authenticated Direct Bridge (post_meta reads only).
Never mutates content or invents prices. Writes report artifact + job summary.
"""
import importlib.util
import json
import os
import time
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

spec=importlib.util.spec_from_file_location("a3tal_release","scripts/deploy-dtc-library.py")
release=importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)
BASE="https://a3tal.com"
REQUIRED=[
 "_a3_year","_a3_price_min","_a3_price_max","_a3_currency",
 "_a3_engine_cc","_a3_power_hp","_a3_torque_nm",
 "_a3_transmission","_a3_fuel","_a3_drivetrain",
 "_a3_source_url","_a3_source_checked_at","_a3_related_post_ids"
]
FIELDS="_fields=id,slug,link,title,featured_media"
def public(url):
    req=Request(url,headers={"User-Agent":"A3tal-Car-QA/1.0","Accept":"application/json","Cache-Control":"no-cache"})
    # Origin may return 522 briefly while the production bridge changes theme files.
    # Reads are safe to retry, writes remain strictly disabled.
    for attempt in range(4):
        try:
            with urlopen(req,timeout=45) as res:return json.load(res)
        except HTTPError as error:
            if error.code not in (429,500,502,503,504,520,522,524) or attempt == 3:raise
            print("CAR_AUDIT_PUBLIC_TRANSIENT",error.code,"retry",attempt+1,flush=True)
        except (URLError,TimeoutError) as error:
            if attempt == 3:raise
            print("CAR_AUDIT_PUBLIC_TRANSPORT_RETRY",attempt+1,flush=True)
        time.sleep(25*(attempt+1))
def clean(meta,k):
    raw=meta.get(k,[])
    if isinstance(raw,list):v=raw[0] if raw else ""
    else:v=raw
    if isinstance(v,(list,dict)):return ""
    return str(v).strip()
def main():
    entries=public(BASE+"/wp-json/wp/v2/a3tal-cars?per_page=10&"+FIELDS)
    if len(entries)!=10:raise RuntimeError("Expected ten published car entities")
    bridge=release.Bridge()
    rows=[]
    for entry in entries:
        entity_id=int(entry["id"])
        data=bridge.request({"op":"post_meta","post_id":entity_id})
        if not isinstance(data,dict):raise RuntimeError("Unexpected metadata type for "+str(entity_id))
        fields={k:clean(data,k) for k in REQUIRED}
        price_ok=(fields["_a3_price_min"] not in ("","0") or fields["_a3_price_max"] not in ("","0"))
        checked=fields["_a3_source_checked_at"]
        try:datetime.strptime(checked,"%Y-%m-%d");checked_valid=True
        except ValueError:checked_valid=False
        url=fields["_a3_source_url"]
        source_valid=url.startswith("https://") or url.startswith("http://")
        needs=[k for k in REQUIRED if not fields[k] or (k=="_a3_price_max" and not price_ok)]
        title=entry["title"]["rendered"]
        row={
          "id":entity_id,"title":title,"slug":entry["slug"],"link":entry["link"],
          "featured_media":int(entry.get("featured_media") or 0),
          "year":fields["_a3_year"],"price_min":fields["_a3_price_min"],
          "price_max":fields["_a3_price_max"],"currency":fields["_a3_currency"],
          "last_checked":checked,"source_url":url,
          "source_url_present":source_valid,"checked_date_valid":checked_valid,
          "related_post_ids":fields["_a3_related_post_ids"],
          "missing_fields":needs,"fields":fields
        }
        rows.append(row)
        print("CAR_AUDIT",entity_id,entry["slug"],"missing="+",".join(needs) if needs else "complete",
              "featured="+str(row["featured_media"]),"source="+str(source_valid),
              "date="+str(checked_valid),flush=True)
    report={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"count":len(rows),"cars":rows}
    folder=Path("car-price-audit-output");folder.mkdir(exist_ok=True)
    (folder/"top-10-existing-cars.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    lines=["# A3TAL: ten existing models, read-only data audit","",
           "Live WordPress post meta. No price modifications or new slugs. Data presence is not independent price verification.","",
           "| Model | Image | Price | Official source | Review date | Missing fields |","|---|---|---|---|---|---|"]
    for row in rows:
        lines.append("| "+str(row["id"])+" "+row["slug"]+" | "+("Yes" if row["featured_media"] else "NO")+" | "+("Yes" if row["price_min"] else "NO")+" | "+("Yes" if row["source_url_present"] else "NO")+" | "+("Yes" if row["checked_date_valid"] else "NO")+" | "+str(len(row["missing_fields"]))+" |")
    lines+=["","## Next edits","Only fill missing fields from verified official sources and existing articles. Preserve original URLs."]
    Path("car-price-audit-output/README.md").write_text("\n".join(lines),encoding="utf-8")
    summary=os.getenv("GITHUB_STEP_SUMMARY")
    if summary:Path(summary).open("a",encoding="utf-8").write("\n".join(lines)+"\n")
    print("CAR_AUDIT_COMPLETE",len(rows),"records; verified without WordPress writes",flush=True)
if __name__=="__main__":main()
