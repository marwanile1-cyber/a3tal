#!/usr/bin/env python3
"""Read-only editorial QA for DTC batch28. Never publishes or marks photos reviewed."""
import json,re,sys
from pathlib import Path
p=Path("data/dtc-original-batch-28.json")
data=json.loads(p.read_text(encoding="utf-8"))
codes="P0262 P0354 P0620 U0142 U0150 U0153 C0052 C0053 B2103 B2431".split()
items=data.get("items",[])
assert [x.get("code") for x in items]==codes,"Ten approved codes or order changed"
assert data.get("ready_for_auto_publish") is False,"Unsafe: release has not passed photographic/video QA"
assert data.get("release_quality",{}).get("photographic_covers_manually_reviewed") is False
orig=[]
allow_video={"P0262":"KeuXbBVR6uk","P0354":"JYvhzYA_Fe4","P0620":"VkuDmEwTxrM","U0142":"ONWAExsFNeg"}
for item in items:
    code=item["code"]
    assert item.get("source","").startswith("https://"),code+" missing technical reference"
    assert len(item.get("steps",[]))==5 and len(item.get("faqs",[]))==3,code+" missing diagnostic sections"
    assert len(item.get("deep_dive",[]))==4 and len(item.get("decision",[]))==3,code+" missing depth"
    assert all(len(section)==2 and len(section[1].split())>=57 for section in item["deep_dive"]),code+" short deep dive"
    assert len(item.get("symptoms",[]))>=3 and len(item.get("causes",[]))>=3,code+" incomplete"
    assert item.get("scope")==("oem:ford" if code.startswith("B") else "generic"),code+" wrong scope"
    vid=item.get("video")
    if vid: assert code in allow_video and vid.get("id")==allow_video[code],code+" unverified video"
    else: assert len(item.get("no_video_reason",""))>=70,code+" unexplained absent video"
    assert not item.get("featured_media"),code+" unverified photos cannot be marked as published"
    body=" ".join([str(item.get(k,"")) for k in ("summary","how","difference","repair","safety")])
    body+=" "+" ".join(str(v) for key in ("symptoms","causes","steps","faqs","deep_dive","decision") for v in item.get(key,[]))
    count=len(re.findall(r"\S+",re.sub(r"[\[\]\(\)',]"," ",body)))
    assert count>=750,code+" is too thin: "+str(count)
    orig.append((code,count,"video" if vid else "no approved video"))
assert "Gateway E" in items[4]["name"]+items[4]["en"] and "Right" in items[5]["en"]
assert "Signal A" in items[6]["en"] and "Signal B" in items[7]["en"]
print("DTC_BATCH28_EDITORIAL_DRAFTS_VALIDATED")
for x in orig:print(*x)
print("DTC_BATCH28_RELEASE_HOLD: ten standalone photographic WebPs, manual QA, live video embed checks and batch28 publisher are not complete")
