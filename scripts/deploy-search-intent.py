#!/usr/bin/env python3
"""Scoped, reversible A3tal whole-site search UX release.
Preflight reads active theme originals, stores encrypted rollback in Actions,
writes CSS before WordPress search.php, then verifies live bytes. No permalink,
content, DB, taxonomy, canonical, robots or main search query modifications.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('a3tal_bridge', 'scripts/deploy-dtc-library.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
SOURCE=Path('theme-source/a3tal-global')
FILES=('search-intent.css','search.php')

def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def prepare(api, folder):
    info=api.request({'op':'site_info'})
    if info.get('active_theme')!='a3tal-global':
        raise RuntimeError('Expected a3tal-global active theme; not safe to deploy')
    originals,sources={},{}
    for name in FILES:
        content=(SOURCE/name).read_text(encoding='utf-8')
        if name.endswith('.php'):
            base.lint(SOURCE/name)
        existing=api.read(name,missing=True)
        # The repository did not contain these new files. Never overwrite
        # untracked production customization by guessing it is disposable.
        if existing is not None and existing['sha256']!=sha(content):
            raise RuntimeError('Untracked live '+name+' exists with independent content; abort')
        originals[name]=existing
        sources[name]=content
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'snapshot.json').write_text(json.dumps({
        'commit':base.source_commit(),'originals':originals,'sources':sources,
    },ensure_ascii=False),encoding='utf-8')
    print('SEARCH_INTENT_PREPARED originals captured and version pinned',flush=True)

def deploy(api,folder):
    state=json.loads((folder/'snapshot.json').read_text(encoding='utf-8'))
    if state['commit']!=base.source_commit():
        raise RuntimeError('Source commit changed since preflight')
    for name in FILES:
        source=state['sources'][name]
        if (SOURCE/name).read_text(encoding='utf-8')!=source:
            raise RuntimeError('Source changed after backup: '+name)
        original=state['originals'][name]
        current=api.read(name,missing=original is None)
        if bool(current)!=bool(original) or (current and current['sha256']!=original['sha256']):
            raise RuntimeError('Concurrent live edit: '+name)
        if current and current['sha256']==sha(source):
            print('SEARCH_INTENT_UNCHANGED',name,flush=True)
        else:
            api.write(name,source,current['sha256'] if current else None)
            print('SEARCH_INTENT_WRITTEN',name,flush=True)
    try:
        api.flush()
    except RuntimeError as exc:
        print('SEARCH_INTENT_CACHE_FLUSH_WARNING',str(exc),flush=True)
    for name in FILES:
        actual=api.read(name)
        if actual['sha256']!=sha(state['sources'][name]):
            raise RuntimeError('Live bytes differed from reviewed source: '+name)
        print('SEARCH_INTENT_VERIFIED',name,flush=True)

def rollback(api,folder):
    target=folder/'snapshot.json'
    if not target.exists():
        return
    state=json.loads(target.read_text(encoding='utf-8'))
    original=state['originals']['search.php']
    current=api.read('search.php',missing=True)
    if not current:
        print('SEARCH_INTENT_ROLLBACK_NOT_NEEDED',flush=True)
        return
    if original and current['sha256']==original['sha256']:
        print('SEARCH_INTENT_ALREADY_ORIGINAL',flush=True)
        return
    if current['sha256']!=sha(state['sources']['search.php']):
        raise RuntimeError('Someone independently edited live search.php; stop rollback')
    # Search.php did not exist before this release: mimic WordPress default
    # search fallback by requiring the original index.php.
    fallback=original['content'] if original else "<?php require get_template_directory().'/index.php'; ?>\n"
    api.write('search.php',fallback,current['sha256'])
    if api.read('search.php')['sha256']!=sha(fallback):
        raise RuntimeError('Could not restore the safe original search behavior')
    print('SEARCH_INTENT_ROLLBACK_RESTORED',flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('phase',choices=('prepare','deploy','rollback'))
    p.add_argument('--state-dir',required=True,type=Path)
    args=p.parse_args()
    api=base.Bridge()
    if args.phase=='prepare':
        prepare(api,args.state_dir)
    elif args.phase=='deploy':
        deploy(api,args.state_dir)
    else:
        rollback(api,args.state_dir)

if __name__=='__main__':
    main()
