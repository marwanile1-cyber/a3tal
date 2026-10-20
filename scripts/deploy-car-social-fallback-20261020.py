#!/usr/bin/env python3
"""Guarded production append for exact car OG fallback.
Read and write the same live WordPress theme path via POST /admin to avoid
cross-edge GET/POST checksum inconsistency. Never override concurrent edits.
"""
import importlib.util
from pathlib import Path
import subprocess
import tempfile

spec=importlib.util.spec_from_file_location("bridge","scripts/deploy-dtc-library.py")
bridge=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

MARKER="A3TAL-CAR-SOCIAL-FEATURED-FALLBACK-20261020"
NAME="functions.php"

def main():
    source=Path("theme-source/a3tal-global/functions.php").read_text(encoding="utf-8")
    start=source.rfind("\n/**\n * "+MARKER)
    if start < 0:
        raise RuntimeError("Reviewed source marker not found; no write")
    patch=source[start:].rstrip()+"\n"
    client=bridge.Bridge()
    status=client.request({"op":"site_info"})
    if status.get("active_theme")!="a3tal-global":
        raise RuntimeError("Active theme mismatch; no write")
    before=client.read(NAME)
    if before is None or not before.get("sha256") or not isinstance(before.get("content"),str):
        raise RuntimeError("No trustworthy live source readback")
    current=before["content"]
    if MARKER in current:
        print("CAR_SOCIAL_IMAGE_PATCH_ALREADY_PRESENT",flush=True)
        return
    if current.rstrip().endswith("?>"):
        raise RuntimeError("Unsafe closing PHP tag in production functions file")
    target=current.rstrip()+"\n"+patch
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",suffix=".php") as handle:
        handle.write(target)
        handle.flush()
        subprocess.run(["php","-l",handle.name],check=True,stdout=subprocess.DEVNULL)
    # Bridge.write performs a SHA-guarded write, then a fresh read-back check.
    client.write(NAME,target,expected=before["sha256"])
    check=client.read(NAME)
    if MARKER not in check["content"] or check["sha256"]!=bridge.digest(target):
        raise RuntimeError("Live source integrity check failed")
    client.flush()
    print("CAR_SOCIAL_IMAGE_PATCH_VERIFIED",check["sha256"],flush=True)

if __name__=="__main__":
    main()
