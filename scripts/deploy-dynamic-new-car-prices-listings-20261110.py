#!/usr/bin/env python3
"""Repair A3tal homepage and /cars price panels systematically, never one manual story.
Two theme files only, GitHub + A3tal Direct Bridge, preflight exact live blob
lease, encrypted backup before any write, verified readback, public H7 QA.
"""
import argparse, hashlib, json, importlib.util, time, urllib.request
from pathlib import Path
spec=importlib.util.spec_from_file_location('a3bridge','scripts/deploy-dtc-library.py')
bridge=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)
T=Path('theme-source/a3tal-global')
FILES={
 'home-reference-20261104.php':'2e3a510aeaf2ccfe59dfe7ed0bab32eb4e255090',
 'car-price-guide.php':'fe596ada83a378f275533dd3a520e7bbebe247e8'
}
H7='haval-h7-hybrid-2027-egypt-price-ultra-black/'
PAGE_URLS=['https://a3tal.com/','https://a3tal.com/cars/']

def gitblob(v):
    raw=v.encode('utf-8')
    return hashlib.sha1(('blob '+str(len(raw))+'\0').encode('utf-8')+raw).hexdigest()

def prepare(api,where):
    info=api.request({'op':'site_info'})
    if info.get('active_theme')!='a3tal-global' or info.get('parent_theme')!='a3tal-global':
        raise RuntimeError('Active theme was changed; no mutation allowed')
    previous={};target={}
    for name,old_blob in FILES.items():
        desired=(T/name).read_text('utf-8')
        bridge.lint(T/name)
        old=api.read(name)
        if old is None:raise RuntimeError('Live theme file unexpectedly absent: '+name)
        prev=gitblob(old['content'])
        cur=bridge.digest(desired)
        if prev!=old_blob and prev!=gitblob(desired):
            raise RuntimeError('CONFLICT: live '+name+' differs from reviewed source; stop rather than overwrite unrelated changes; current blob='+prev)
        if name.startswith('home') and ("$home_latest_price_posts = new WP_Query" not in desired or "'cat'=>374" not in desired):
            raise RuntimeError('Home new post query is absent')
        if name.startswith('car-price') and ('cg-latest-price-articles' not in desired or 'cg_price_updates->posts' not in desired):
            raise RuntimeError('Cars page new post grid is absent')
        previous[name]=old
        target[name]=desired
        print('PRICES_DYNAMIC_PREFLIGHT',name,'live_blob',prev,'target_sha',cur,flush=True)
    where.mkdir(parents=True,exist_ok=True)
    (where/'snapshot.json').write_text(json.dumps({'originals':previous,'target':target,'source_commit':bridge.source_commit()},ensure_ascii=False),encoding='utf-8')
    print('SAFE_BACKUP_CAPTURED_BEFORE_ANY_LIVE_THEME_WRITE',flush=True)

def deploy(api,where):
    state=json.loads((where/'snapshot.json').read_text('utf-8'))
    if state['source_commit']!=bridge.source_commit():raise RuntimeError('Source commit changed between backup and deploy')
    for name in FILES:
        current=api.read(name)
        old=state['originals'][name]
        desired=state['target'][name]
        if current['sha256']!=old['sha256'] and current['sha256']!=bridge.digest(desired):
            raise RuntimeError('CONFLICT: live file changed after backup, no overwrite '+name)
        if current['sha256']==bridge.digest(desired):
            print('PRICES_DYNAMIC_ALREADY_DEPLOYED',name,flush=True)
            continue
        if (T/name).read_text('utf-8')!=desired:raise RuntimeError('Source file changed on runner: '+name)
        api.write(name,desired,current['sha256'])
    api.flush()
    for name in FILES:
        actual=api.read(name)
        if actual['sha256']!=bridge.digest(state['target'][name]):
            raise RuntimeError('Live theme readback mismatch '+name)
        print('PRICES_DYNAMIC_LIVE_FILE_VERIFIED',name,flush=True)
    print('PRICES_DYNAMIC_BOTH_THEME_FILES_DEPLOYED',flush=True)

def public_check():
    headers={'User-Agent':'Mozilla/5.0 (A3tal price-archive-link-validation)','Cache-Control':'no-cache'}
    for page in PAGE_URLS:
        last=''
        for attempt in range(6):
            url=page+('?a3tal_price_fix=20261110' if '?' not in page else '&a3tal_price_fix=20261110')
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=50) as f:html=f.read(2_000_000).decode('utf-8','replace')
            if H7 in html and ('cg-latest-price-articles' in html if '/cars/' in page else 'a3egy-price-grid' in html):
                print('LATEST_H7_PRICE_LINK_VISIBLE_LIVE',page,flush=True)
                break
            last='H7 missing in HTML for '+page+' (bytes '+str(len(html))+')'
            time.sleep(9)
        else:raise RuntimeError(last)
    print('H7_PRICE_POST_NOW_VISIBLE_HOME_AND_CARS_NO_MANUAL_RECORD',flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('phase',choices=('prepare','deploy','qa'))
    p.add_argument('--state-dir',type=Path,default=Path('/tmp/a3tal-price-fix'))
    args=p.parse_args()
    if args.phase=='qa':public_check();return
    api=bridge.Bridge()
    if args.phase=='prepare':prepare(api,args.state_dir)
    else:deploy(api,args.state_dir)

if __name__=='__main__':main()
