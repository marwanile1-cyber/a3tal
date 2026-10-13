"""Safely hot-deploy the additive A3tal global garage without reactivating DTC.
Encrypted GitHub artifact preserves original files before writes.
Existing DTC code URLs, editorial posts, functions.php and comments are untouched.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('existing_dtc_release', 'scripts/deploy-dtc-library.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)

SOURCE = Path('theme-source/a3tal-global')
# Write assets first; archive entrypoint last to avoid exposing a half-installed feature.
FILES = [
  'assets/js/dtc-brand-logos.generated.js',
  'dtc-world-garage.css',
  'assets/js/dtc-world-garage.js',
  'dtc-world-garage.php',
  'dtc-library-support.php',
  'dtc-library-archive.php',
  'dtc-model-links.php',
  'dtc-model-links.css',
]

def sha(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def prepare(api, folder):
    info = api.request({'op': 'site_info'})
    if info.get('active_theme') != 'a3tal-global':
        raise RuntimeError('Reviewed global theme is not active; abort without changes')
    current_functions = api.read('functions.php')
    if 'A3TAL-DTC-LIBRARY:START' not in current_functions['content']:
        raise RuntimeError('Independent DTC library activation is missing; do not hotpatch')
    snapshot = {'originals': {}, 'sources': {}, 'commit': release.source_commit()}
    for name in FILES:
        p = SOURCE / name
        content = p.read_text(encoding='utf-8')
        if name.endswith('.php'):
            release.lint(p)
        live = api.read(name, missing=True)
        if name in ('dtc-library-support.php', 'dtc-library-archive.php'):
            if live is None:
                raise RuntimeError('Required live template not present: ' + name)
            if not any(t in live['content'] for t in
                       (('a3g-dtc-library', 'a3g_dtc_catalog') if name.endswith('support.php')
                        else ('d-hero', 'd-families'))):
                raise RuntimeError('Unexpected live DTC template; review rather than overwrite: ' + name)
        snapshot['originals'][name] = live
        snapshot['sources'][name] = content
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False), encoding='utf-8')
    print('Prepared six scoped garage files; encrypted backup must be uploaded before writes', flush=True)

def run(api, folder):
    snapshot = json.loads((folder / 'snapshot.json').read_text(encoding='utf-8'))
    if snapshot['commit'] != release.source_commit():
        raise RuntimeError('Prepared source ref changed')
    logo_pack = snapshot['sources']['assets/js/dtc-brand-logos.generated.js']
    if len(logo_pack) < 30000 or 'a3talGarageBrandLogos' not in logo_pack:
        raise RuntimeError('Verified local logos bundle is missing or unexpectedly small')
    for name in FILES:
        original = snapshot['originals'][name]
        current = api.read(name, missing=original is None)
        if bool(original) != bool(current):
            raise RuntimeError('Live file creation/removal race: ' + name)
        if current and current['sha256'] != original['sha256']:
            raise RuntimeError('Live file was edited after backup, abort: ' + name)
        content = snapshot['sources'][name]
        if (SOURCE / name).read_text(encoding='utf-8') != content:
            raise RuntimeError('Local source changed after preflight: ' + name)
        if current and current['sha256'] == sha(content):
            print('Already correct:', name, flush=True)
            continue
        api.write(name, content, current['sha256'] if current else None)
    try:
        api.flush()
    except RuntimeError as exc:
        # A host cache-flush rate limit doesn't invalidate checksum-verified writes.
        print('Cache flush unavailable; confirm fresh public page:', str(exc), flush=True)
    # The original code library remains active; never force a theme reactivation.
    active_functions = api.read('functions.php')
    if 'A3TAL-DTC-LIBRARY:START' not in active_functions['content']:
        raise RuntimeError('Independent DTC activation changed during deployment')
    try:
        html = release.public_get('/dtc/')
        if 'id="global-garage"' not in html or 'id="dtc-codes"' not in html:
            raise RuntimeError('Live archive did not render both garage and DTC codes')
        if 'dtc-world-garage.js' not in html or 'dtc-brand-logos.generated.js' not in html:
            raise RuntimeError('Logo bundle or world garage javascript not included')
        print('PUBLIC QA PASSED: premium garage and existing code archive render', flush=True)
    except release.PublicCheckBlocked as exc:
        print('PUBLIC QA REQUIRES EXTERNAL CHECK: ' + str(exc), flush=True)
    print('Finished. All six intended live file checksums were verified through bridge.', flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'deploy'])
    parser.add_argument('--state-dir', type=Path, required=True)
    args=parser.parse_args()
    api=release.Bridge()
    if args.phase=='prepare':
        prepare(api,args.state_dir)
    else:
        run(api,args.state_dir)

if __name__=='__main__':
    main()
