"""Deploy the scoped DTC experience through the existing authenticated bridge.

prepare saves live bytes before mutation; GitHub encrypts and uploads that backup
before deploy. Never send credentials to public URLs or log response bodies.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = 'https://a3tal.com'
THEME = Path('theme-source/a3tal-global')
REMOTE = 'themes/a3tal-global/'
FILES = [
    'dtc-library.css', 'assets/js/dtc-library.js', 'header-dtc.php',
    'footer-dtc.php', 'dtc-library-archive.php', 'dtc-library-single.php',
    'dtc-discussions.php', 'dtc-library-support.php',
]
BLOCK = """/* A3TAL-DTC-LIBRARY:START */
if (is_file(get_template_directory() . '/dtc-library-support.php')) {
    require_once get_template_directory() . '/dtc-library-support.php';
}
/* A3TAL-DTC-LIBRARY:END */"""


def digest(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


class Bridge:
    def __init__(self):
        self.key = os.environ.get('A3TAL_API_KEY', '')
        if not self.key:
            raise RuntimeError('Missing configured repository bridge secret')

    def request(self, data, write=False, missing=False):
        url = BASE + '/wp-json/a3tal-direct/v1/admin'
        headers = {'X-A3tal-Key': self.key, 'Authorization': 'Bearer ' + self.key,
                   'Accept': 'application/json', 'User-Agent': 'A3tal-DTC-Deploy/1.0',
                   'Cache-Control': 'no-cache, no-store'}
        body = None
        if write:
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        else:
            # Negative file lookups can be cached by the hosting layer. Every
            # authenticated source read must see the current filesystem bytes.
            params = dict(data, _a3tal_dtc_read=str(time.time_ns()))
            url += '?' + urllib.parse.urlencode(params)
        # Reads may retry transient transport failures; mutations never replay.
        for attempt in range(1 if write else 2):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, body, headers), timeout=30 if write else 20) as response:
                    result = json.load(response)
                if not result.get('ok') or 'result' not in result:
                    raise RuntimeError('Bridge returned an invalid success envelope')
                return result['result']
            except urllib.error.HTTPError as error:
                try:
                    payload = json.loads(error.read().decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    payload = {}
                if missing and error.code == 404:
                    if payload.get('code') == 'a3tal_file_missing':
                        return None
                code = payload.get('code', '')
                suffix = ': ' + code if isinstance(code, str) and re.fullmatch('[a-z][a-z0-9_]{0,70}', code) else ''
                raise RuntimeError(f"Bridge {data['op']} rejected (HTTP {error.code}){suffix}") from None
            except (TimeoutError, urllib.error.URLError, json.JSONDecodeError):
                if write or attempt == 1:
                    raise RuntimeError(f"Bridge {data['op']} transport error") from None
                time.sleep(2)

    def read(self, name, missing=False):
        result = self.request({'op': 'file_read', 'path': REMOTE + name}, missing=missing)
        if result is not None and digest(result['content']) != result['sha256']:
            raise RuntimeError('Live source bytes do not match reported checksum: ' + name)
        return result

    def write(self, name, content, expected=None):
        data = {'op': 'file_write', 'path': REMOTE + name, 'content': content,
                'confirm': True, 'dangerous': True}
        if expected:
            data['expected_sha256'] = expected
        # If the response is lost, readback determines whether the write happened.
        mutation_error = None
        try:
            self.request(data, write=True)
        except RuntimeError as error:
            mutation_error = error
        try:
            actual = self.read(name)
        except RuntimeError:
            if mutation_error:
                raise mutation_error
            raise
        if actual['sha256'] != digest(content):
            raise mutation_error or RuntimeError('Readback checksum mismatch: ' + name)
        print('Verified live file:', name)

    def flush(self):
        self.request({'op': 'cache_flush'}, write=True)


def lint(path):
    subprocess.run(['php', '-l', str(path)], check=True, stdout=subprocess.DEVNULL)


def source_commit():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()


def compose(original, mode):
    if 'A3TAL-DTC-LIBRARY:START' in original:
        if original.count(BLOCK) != 1:
            raise RuntimeError('Live activation block differs from the reviewed block')
        return original if mode == 'deploy' else original.replace(BLOCK, '', 1)
    if mode == 'deactivate':
        return original
    if original.rstrip().endswith('?>'):
        raise RuntimeError('Unexpected PHP closing tag; review live functions before activation')
    return original + '\n\n' + BLOCK + '\n'


def prepare(bridge, folder, mode):
    info = bridge.request({'op': 'site_info'})
    if info['active_theme'] != 'a3tal-global' or info['parent_theme'] != 'a3tal-global':
        raise RuntimeError('The reviewed theme is no longer the active theme')
    originals = {'functions.php': bridge.read('functions.php')}
    sources = {}
    if mode == 'deploy':
        for name in FILES:
            path = THEME / name
            sources[name] = path.read_text(encoding='utf-8')
            if name.endswith('.php'):
                lint(path)
            originals[name] = bridge.read(name, missing=True)
    target = compose(originals['functions.php']['content'], mode)
    if mode == 'deploy' and BLOCK in originals['functions.php']['content']:
        changed = any(not originals[name] or originals[name]['sha256'] != digest(content)
                      for name, content in sources.items())
        if changed:
            raise RuntimeError('Deactivate the library through workflow mode before updating active source files')
    folder.mkdir(parents=True, exist_ok=True)
    candidate = folder / 'functions-candidate.php'
    candidate.write_bytes(target.encode('utf-8'))
    lint(candidate)
    snapshot = {'commit': source_commit(), 'mode': mode,
                'originals': originals, 'sources': sources, 'functions': target}
    (folder / 'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False), encoding='utf-8')
    print('Prepared and linted exact live activation bytes; originals ready for encrypted backup')


def unchanged(bridge, name, original):
    current = bridge.read(name, missing=original is None)
    if (current is None) != (original is None) or (current and current['sha256'] != original['sha256']):
        raise RuntimeError('Live file changed after backup; stop and prepare again: ' + name)
    return current


def public_get(path):
    # Verification queries deliberately bypass cached pre-deployment responses.
    sep = '&' if '?' in path else '?'
    url = BASE + path + sep + 'a3tal_dtc_verify=' + str(time.time_ns())
    with urllib.request.urlopen(urllib.request.Request(url, headers={'Cache-Control': 'no-cache'}), timeout=20) as response:
        return response.read().decode('utf-8')


def verify(mode):
    archive = public_get('/dtc/')
    if mode == 'deploy':
        assert 'd-hero' in archive and 'dtc-codes' in archive, 'Archive template is not active'
        detail = public_get('/dtc/p0172/')
        assert 'data-post-id=' in detail and 'd-detail-hero' in detail, 'Detail/discussion template missing'
        guide = public_get('/p0172-system-too-rich-bank1-diagnosis/')
        assert 'd-detail-hero' in guide and 'data-post-id=' in guide, 'Existing guide integration missing'
        search = public_get('/dtc/?code=%20p0172%20')
        assert 'P0172' in search and search.count('class="d-code-card"') == 1, 'Code search failed'
        no_match = public_get('/dtc/?code=P9999')
        assert 'لا يوجد شرح منشور مطابق' in no_match, 'Empty search handling failed'
        assert 'noindex' in search, 'Search variants must not become indexable'
    else:
        assert 'class="d-hero"' not in archive, 'Feature did not deactivate'
    home = public_get('/')
    assert 'a3g-dtc-library' not in home and '<html' in home, 'Homepage scope changed'
    print('Verified archive, existing links, search, discussions and unaffected homepage')


def deploy(bridge, folder):
    state = json.loads((folder / 'snapshot.json').read_text(encoding='utf-8'))
    if state['commit'] != source_commit():
        raise RuntimeError('Prepared source commit changed')
    mode, originals = state['mode'], state['originals']
    unchanged(bridge, 'functions.php', originals['functions.php'])
    uploaded = []
    activated = False
    try:
        for name, content in state['sources'].items():
            if (THEME / name).read_text(encoding='utf-8') != content:
                raise RuntimeError('Source changed after preflight: ' + name)
            current = unchanged(bridge, name, originals[name])
            if current and current['sha256'] == digest(content):
                continue
            uploaded.append(name)
            bridge.write(name, content, current['sha256'] if current else None)
        fresh = unchanged(bridge, 'functions.php', originals['functions.php'])
        lint(folder / 'functions-candidate.php')
        if fresh['sha256'] != digest(state['functions']):
            activated = True
            bridge.write('functions.php', state['functions'], fresh['sha256'])
        bridge.flush()
        verify(mode)
        bridge.request({'op': 'site_info'})
        (folder / 'result.json').write_text(json.dumps({'ok': True, 'mode': mode, 'commit': state['commit']}))
    except Exception:
        print('Deployment failed; restoring conflict-checked original files')
        if activated:
            live = bridge.read('functions.php')
            if live['sha256'] == digest(state['functions']):
                bridge.write('functions.php', originals['functions.php']['content'], live['sha256'])
            elif live['sha256'] != originals['functions.php']['sha256']:
                raise RuntimeError('Rollback stopped: functions.php has another editor’s changes') from None
        rollback_conflicts = []
        for name in reversed(uploaded):
            original = originals[name]
            if original:
                live = bridge.read(name)
                if live['sha256'] == digest(state['sources'][name]):
                    bridge.write(name, original['content'], live['sha256'])
                elif live['sha256'] != original['sha256']:
                    rollback_conflicts.append(name)
                if not rollback_conflicts and bridge.read(name)['sha256'] != original['sha256']:
                    rollback_conflicts.append(name)
        bridge.flush()
        if rollback_conflicts:
            raise RuntimeError('Rollback incomplete; concurrent changes in: ' + ', '.join(rollback_conflicts)) from None
        print('Original activation and existing source restored; newly uploaded files remain inactive')
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'deploy'])
    parser.add_argument('--state-dir', type=Path, required=True)
    parser.add_argument('--mode', choices=['deploy', 'deactivate'], default='deploy')
    args = parser.parse_args()
    api = Bridge()
    if args.phase == 'prepare':
        prepare(api, args.state_dir, args.mode)
    else:
        deploy(api, args.state_dir)
