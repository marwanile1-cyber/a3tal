#!/usr/bin/env python3
"""Deploy only A3tal /cars/ price guide using the existing Direct Bridge.
Read-and-hash preflight, encrypted rollback in Actions, immutable sources,
CSS/JS/template first, archive wrapper LAST. Does not mutate WordPress content.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('a3tal_bridge', 'scripts/deploy-dtc-library.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

THEME = Path('theme-source/a3tal-global')
FILES = (
    'car-price-guide.css',
    'car-price-brand-logos.js',
    'car-price-guide.js',
    'car-price-guide.php',
    'archive-a3_car.php',  # only activation change: legacy endpoint /cars/ intact
)
ORIGINAL_WRAPPER = "<?php $a3g_vehicle_type='a3_car'; require get_template_directory().'/platform-archive-vehicle.php'; ?>"

def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def prepare(api, folder):
    info = api.request({'op':'site_info'})
    if info.get('active_theme') != 'a3tal-global' or info.get('parent_theme') != 'a3tal-global':
        raise RuntimeError('Active theme differs from reviewed a3tal-global')
    originals, sources = {}, {}
    for name in FILES:
        src = (THEME / name).read_text(encoding='utf-8')
        if name.endswith('.php'):
            base.lint(THEME / name)
        sources[name] = src
        originals[name] = api.read(name, missing=True)
    wrapper = originals['archive-a3_car.php']
    if not wrapper or wrapper['content'].strip() not in (ORIGINAL_WRAPPER, sources['archive-a3_car.php'].strip()):
        raise RuntimeError('Live cars archive was changed independently: stop for human review')
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'snapshot.json').write_text(json.dumps({
        'commit':base.source_commit(),
        'originals':originals,'sources':sources,
        'active_theme':info['active_theme'],
    },ensure_ascii=False),encoding='utf-8')
    print('CAR_GUIDE_PREPARED original live bytes saved for encrypted rollback',flush=True)

def deploy(api,folder):
    state=json.loads((folder/'snapshot.json').read_text(encoding='utf-8'))
    if state['commit'] != base.source_commit():
        raise RuntimeError('Source commit differs from reviewed prepared snapshot')
    for name in FILES:
        original = state['originals'][name]
        content = state['sources'][name]
        if (THEME / name).read_text(encoding='utf-8') != content:
            raise RuntimeError('Source changed since preflight: '+name)
        current = api.read(name,missing=original is None)
        if (current is None) != (original is None) or (current and current['sha256'] != original['sha256']):
            raise RuntimeError('Live file drifted after backup: '+name)
        if current and current['sha256']==sha(content):
            print('CAR_GUIDE_UNCHANGED',name,flush=True)
            continue
        api.write(name,content,current['sha256'] if current else None)
    api.flush()
    for name in FILES:
        actual=api.read(name)
        if actual['sha256'] != sha(state['sources'][name]):
            raise RuntimeError('Live hash mismatch: '+name)
    print('CAR_GUIDE_DEPLOY_VERIFIED exact five source files read back correctly',flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('phase',choices=('prepare','deploy'))
    p.add_argument('--state-dir',required=True,type=Path)
    a=p.parse_args()
    api=base.Bridge()
    if a.phase=='prepare':
        prepare(api,a.state_dir)
    else:
        deploy(api,a.state_dir)

if __name__=='__main__':
    main()
