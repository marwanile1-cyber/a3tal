#!/usr/bin/env python3
"""Surgically replace ONLY the verified original homepage price-section/query.
Live home differs from GitHub's full file: preserve every unrelated live byte.
Secure A3tal Direct Bridge CAS write; encrypt original BEFORE changing anything.
"""
import argparse, json, hashlib, importlib.util, urllib.request, time
from pathlib import Path
spec=importlib.util.spec_from_file_location('a3tal_bridge','scripts/deploy-dtc-library.py')
b=importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
NAME='home-reference-20261104.php'
P=Path('data/repairs/auto-new-car-prices-home-section-20261110.json')
H7='haval-h7-hybrid-2027-egypt-price-ultra-black/'
URLS=['https://a3tal.com/','https://a3tal.com/cars/']

def transform(content,patch):
    old=patch['legacy_section'];new=patch['fixed_section']
    oldq=patch['legacy_query'];newq=patch['fixed_query']
    if new in content and newq in content:
        print('HOME_PRICE_SECTION_ALREADY_UPDATED',flush=True)
        return content
    if content.count(old)!=1 or content.count(oldq)!=1:
        print('LIVE_HOME_PRICE_SECTION_CONFLICT',
              'oldSection',content.count(old),'oldQuery',content.count(oldq),
              'newSection',content.count(new),'newQuery',content.count(newq),flush=True)
        raise RuntimeError('Live price section differs from reviewed original, refusing destructive replacement')
    target=content.replace(oldq,newq,1).replace(old,new,1)
    if target.count(new)!=1 or target.count(newq)!=1 or old in target:
        raise RuntimeError('Scoped price replacement verification failed')
    # The only allowed difference is exactly the two reviewed substitutions.
    restored=target.replace(new,old,1).replace(newq,oldq,1)
    if restored!=content:raise RuntimeError('Unrelated live page bytes changed')
    return target

def prepare(api,folder):
    info=api.request({'op':'site_info'})
    if info.get('active_theme')!='a3tal-global':raise RuntimeError('Unexpected active theme')
    patch=json.loads(P.read_text('utf-8'))
    live=api.read(NAME)
    if not live:raise RuntimeError('Live home file is missing')
    dest=transform(live['content'],patch)
    # Assert the existing cars archive already received its own scoped price-card fix.
    catalog=api.read('car-price-guide.php')
    if 'id="cg-latest-price-articles"' not in catalog['content']:
        raise RuntimeError('Car-price guide latest-editorial block not deployed yet')
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'snapshot.json').write_text(json.dumps({
        'original':live,'desired':dest,'previous_sha':live['sha256'],
        'desired_sha':b.digest(dest),'source_commit':b.source_commit()
    },ensure_ascii=False),encoding='utf-8')
    print('SCOPED_PRICE_SECTION_PREPARED',len(live['content']),len(dest),'unchanged_rest_of_live_home',flush=True)

def deploy(api,folder):
    state=json.loads((folder/'snapshot.json').read_text('utf-8'))
    if state['source_commit']!=b.source_commit():raise RuntimeError('GitHub source commit changed')
    live=api.read(NAME)
    if live['sha256']==state['desired_sha']:
        print('HOME_PRICE_SECTION_VERIFIED_NOOP',flush=True)
    else:
        if live['sha256']!=state['previous_sha']:
            raise RuntimeError('Live home changed after backup; no overwrite')
        api.write(NAME,state['desired'],state['previous_sha'])
    api.flush()
    after=api.read(NAME)
    if after['sha256']!=state['desired_sha']:
        raise RuntimeError('Home repair readback hash mismatch')
    print('SCOPED_AUTO_PRICE_HOME_DEPLOYED_AND_HASH_VERIFIED',flush=True)

def qa():
    h={'User-Agent':'Mozilla/5.0 (A3tal HTML section link QA)','Cache-Control':'no-store'}
    for url in URLS:
        good=False
        for attempt in range(6):
            u=url+('?a3tal_cars_fix=20261110' if '?' not in url else '&a3tal_cars_fix=20261110')
            req=urllib.request.Request(u,headers=h)
            with urllib.request.urlopen(req,timeout=45) as f:s=f.read(3_000_000).decode('utf-8','replace')
            if '/cars/' in url:
                a=s.find('id="cg-latest-price-articles"')
                e=s.find('id="cg-popular"',a)
            else:
                a=s.find('class="a3egy-price-grid"')
                e=s.find('class="a3egy-market-quick"',a)
            scope=s[a:e] if a>=0 and e>a else ''
            good=H7 in scope and 'a3tal-haval-h7-2027-cover' in scope
            print('PRICE_SECTION_RAW_HTML_CHECK',url,
                  'marker_found',a>=0,'section_length',len(scope),
                  'h7_link',H7 in scope,'h7_photo','a3tal-haval-h7-2027-cover' in scope,flush=True)
            if good:break
            time.sleep(6)
        if not good:raise RuntimeError('Haval H7 featured price card absent inside actual requested section: '+url)
    print('H7_LIVE_VISIBLE_IN_HOMEPAGE_AND_CARS_MAIN_GRID_WITH_REAL_PHOTO',flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('phase',choices=('prepare','deploy','qa'))
    p.add_argument('--state-dir',type=Path,default=Path('/tmp/a3tal-home-price'))
    args=p.parse_args()
    if args.phase=='qa':qa();return
    api=b.Bridge()
    if args.phase=='prepare':prepare(api,args.state_dir)
    else:deploy(api,args.state_dir)

if __name__=='__main__':main()
