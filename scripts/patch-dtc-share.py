#!/usr/bin/env python3
"""Safely update the single DTC share permalink line in the active WP theme.

GitHub encrypts the original bytes in its workflow before the deploy phase.
No other template, URL, content or database record is changed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://a3tal.com"
URL = BASE + "/wp-json/a3tal-direct/v1/admin"
REMOTE = "themes/a3tal-global/dtc-library-single.php"
SOURCE = Path("theme-source/a3tal-global/dtc-library-single.php")
OLD = "  $dtc_share_url = get_permalink($dtc_content_id);"
NEW = "  $dtc_share_url = get_permalink($dtc_id);"


def sha(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class Bridge:
    def __init__(self):
        self.key = os.environ.get("A3TAL_API_KEY", "")
        if not self.key:
            raise RuntimeError("Missing A3tal bridge key")
        self.last = 0

    def request(self, operation, body, write=False):
        payload = dict(body, op=operation)
        headers = {
            "X-A3tal-Key": self.key, "Authorization": "Bearer " + self.key,
            "Content-Type": "application/json", "Accept": "application/json",
            "Cache-Control": "no-cache", "User-Agent": "A3tal-Verified-Scoped-Patch/1.0",
        }
        for attempt in range(4 if not write else 1):
            time.sleep(max(0, 18 - (time.monotonic() - self.last)))
            self.last = time.monotonic()
            req = urllib.request.Request(URL, json.dumps(payload, ensure_ascii=False).encode(), headers)
            try:
                with urllib.request.urlopen(req, timeout=45) as res:
                    response = json.load(res)
                if not response.get("ok") or not isinstance(response.get("result"), dict):
                    raise RuntimeError("Bridge returned an invalid response")
                return response["result"]
            except urllib.error.HTTPError as exc:
                if not write and attempt < 3 and exc.code in (429, 502, 503, 504, 520, 522, 524):
                    print("Temporary Bridge read error, waiting before retry: HTTP", exc.code, flush=True)
                    time.sleep(60 * (attempt + 1))
                    continue
                raise RuntimeError("Bridge rejected operation: HTTP " + str(exc.code)) from None
            except (TimeoutError, urllib.error.URLError):
                if not write and attempt < 3:
                    time.sleep(45 * (attempt + 1))
                    continue
                raise RuntimeError("Bridge transport interruption") from None

    def read(self):
        result = self.request("file_read", {"path": REMOTE})
        if sha(result["content"]) != result["sha256"]:
            raise RuntimeError("Inconsistent live file checksum")
        return result

    def write(self, text, expected):
        try:
            self.request("file_write", {
                "path": REMOTE, "content": text, "expected_sha256": expected,
                "confirm": True, "dangerous": True,
            }, write=True)
        except RuntimeError:
            # A lost response is not proof of a failed mutation; check readback.
            pass
        live = self.read()
        if live["sha256"] != sha(text):
            raise RuntimeError("Scoped share change not verified; inspect live file before retrying")
        return live


def main(phase, folder):
    api = Bridge()
    folder.mkdir(parents=True, exist_ok=True)
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(NEW) != 1 or OLD in source:
        raise RuntimeError("Reviewed source line not in expected state")
    if phase == "prepare":
        live = api.read()
        if live["content"] == source:
            print("Share permalink patch already active and verified", flush=True)
            original = live
            changed = False
        else:
            if live["content"].count(OLD) != 1 or NEW in live["content"]:
                raise RuntimeError("Live template differs from reviewed original, refusing update")
            candidate = live["content"].replace(OLD, NEW, 1)
            if candidate != source:
                raise RuntimeError("Live template and GitHub source differ beyond scoped change")
            original = live
            changed = True
        (folder / "original.json").write_text(json.dumps({
            "live": original, "source_sha": sha(source), "needs_update": changed,
        }), encoding="utf-8")
        print("Preflight complete; original bytes ready for encrypted backup", flush=True)
        return

    state = json.loads((folder / "original.json").read_text(encoding="utf-8"))
    if sha(source) != state["source_sha"]:
        raise RuntimeError("Reviewed source changed since backup")
    live = api.read()
    if live["sha256"] == sha(source):
        print("Share permalink patch already live", flush=True)
    else:
        if not state["needs_update"] or live["sha256"] != state["live"]["sha256"]:
            raise RuntimeError("Concurrent update detected; refusing to overwrite")
        api.write(source, live["sha256"])
        print("Verified only DTC detail share target updated in live template", flush=True)
    live = api.read()
    if live["sha256"] != sha(source):
        raise RuntimeError("Final checksum mismatch")
    print("SUCCESS: source and production share template checksums match", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "deploy"))
    parser.add_argument("--state-dir", type=Path, required=True)
    args = parser.parse_args()
    main(args.phase, args.state_dir)
