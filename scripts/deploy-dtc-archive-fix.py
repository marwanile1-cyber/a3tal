#!/usr/bin/env python3
"""Scoped /dtc/ release with encrypted rollback snapshot handled by GitHub Actions.

Only four DTC archive files are considered. No arbitrary WP posts or other
template files are changed. The original live bytes and SHA256 are captured
before any write, then the source SHA and live SHA are checked again.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("a3tal_dtc_release", "scripts/deploy-dtc-library.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)

THEME = Path("theme-source/a3tal-global")
FILES = (
    "dtc-live-search.css",
    "assets/js/dtc-live-search.js",
    "dtc-library-support.php",
    "dtc-library-archive.php",
)


def sha(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def prepare(api, state_dir):
    info = api.request({"op": "site_info"})
    if info.get("active_theme") != "a3tal-global":
        raise RuntimeError("Active WordPress theme is not a3tal-global")
    funcs = api.read("functions.php")
    if "A3TAL-DTC-LIBRARY:START" not in funcs["content"]:
        raise RuntimeError("Independent DTC library is not active; abort")
    originals = {}
    sources = {}
    for name in FILES:
        source = THEME / name
        text = source.read_text(encoding="utf-8")
        if name.endswith(".php"):
            release.lint(source)
        sources[name] = text
        originals[name] = api.read(name, missing=True)
    state = {
        "commit": release.source_commit(),
        "originals": originals,
        "sources": sources,
        "functions_sha256": funcs["sha256"],
    }
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "snapshot.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    print("PREFLIGHT OK: original live files captured for protected backup", flush=True)


def deploy(api, state_dir):
    state = json.loads((state_dir / "snapshot.json").read_text(encoding="utf-8"))
    if state["commit"] != release.source_commit():
        raise RuntimeError("Source commit changed between preflight and deployment")
    if api.read("functions.php")["sha256"] != state["functions_sha256"]:
        raise RuntimeError("Live DTC entrypoint changed after snapshot")
    for name in FILES:
        source = (THEME / name).read_text(encoding="utf-8")
        if source != state["sources"][name]:
            raise RuntimeError("Checked-out source differs from prepared snapshot: " + name)
        previous = state["originals"][name]
        current = api.read(name, missing=previous is None)
        if (previous is None) != (current is None):
            raise RuntimeError("A file was independently created or deleted: " + name)
        if current and current["sha256"] != previous["sha256"]:
            raise RuntimeError("Live file changed after snapshot: " + name)
        if current and current["sha256"] == sha(source):
            print("UNCHANGED VERIFIED:", name, flush=True)
            continue
        api.write(name, source, current["sha256"] if current else None)
    if api.read("functions.php")["sha256"] != state["functions_sha256"]:
        raise RuntimeError("Unexpected functions.php modification")
    try:
        api.flush()
    except RuntimeError as error:
        print("Cache flush was unavailable, independent page verification required: " + str(error), flush=True)
    for name in FILES:
        actual = api.read(name)
        if actual["sha256"] != sha(state["sources"][name]):
            raise RuntimeError("Post-write checksum mismatch: " + name)
    print("DEPLOYMENT VERIFIED: four DTC archive file checksums match", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "deploy"])
    parser.add_argument("--state-dir", type=Path, required=True)
    args = parser.parse_args()
    api = release.Bridge()
    if args.phase == "prepare":
        prepare(api, args.state_dir)
    else:
        deploy(api, args.state_dir)


if __name__ == "__main__":
    main()
