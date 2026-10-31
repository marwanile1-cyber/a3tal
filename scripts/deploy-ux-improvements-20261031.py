#!/usr/bin/env python3
"""Deploy reviewed theme UX changes through A3tal Direct Bridge with SHA guards."""
import hashlib,json,os,re,subprocess,time,urllib.request,urllib.parse,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'theme-source/a3tal-global'
BACKUP=ROOT/'theme-patches/ux-20261031-baseline'
OUT=ROOT/'reports/ux-20261031'
OUT.mkdir(parents=True,exist_ok=True)
SITE='https://a3tal.com'
API=SITE+'/wp-json/a3tal-direct/v1'
KEY=os.environ['A3TAL_API_KEY']
NEW=['ux-improvements-20261031.php','ux-improvements-20261031.css','assets/js/ux-improvements-20261031.js']
EXISTING=['functions.php','header.php','header-dtc.php','footer-dtc.php','search.php','front-page.php','platform-archive-directory.php','dtc-library-single.php']
def digest(text):return hashlib.sha256(text.encode('utf8')).hexdigest()
def request(url,payload=None,auth=True,optional=False):
    headers={'User-Agent':'A3tal-Guarded-UX/20261031','Cache-Control':'no-cache,no-store','Accept':'application/json' if auth else 'text/html'}
    if auth:headers.update({'X-A3tal-Key':KEY,'Authorization':'Bearer '+KEY})
    raw=json.dumps(payload,ensure_ascii=False).encode('utf8') if payload is not None else None
    if raw is not None:headers['Content-Type']='application/json; charset=utf-8'
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers=headers,data=raw,method='POST' if raw is not None else 'GET')
            with urllib.request.urlopen(req,timeout=100) as r:body=r.read().decode('utf8','replace')
            return json.loads(body) if auth else body
        except urllib.error.HTTPError as error:
            if optional and error.code==404:return None
            if error.code in [429,500,502,503,504] and attempt<2:time.sleep(3);continue
            raise RuntimeError('Request failed with HTTP '+str(error.code)) from None
        except (TimeoutError,urllib.error.URLError):
            if attempt<2:time.sleep(3);continue
            raise RuntimeError('Request connection failed') from None
def read_file(name,optional=False):
    query=urllib.parse.urlencode({'op':'file_read','path':'themes/a3tal-global/'+name,'ux_nonce':time.time_ns()})
    result=request(API+'/admin?'+query,optional=optional)
    if result is None:return None
    if not result.get('ok'):raise RuntimeError('Bridge file read not confirmed')
    info=result['result']
    if digest(info['content'])!=info['sha256']:raise RuntimeError('Inconsistent live digest: '+name)
    return info
def write_file(name,content,expected):
    result=request(API+'/admin',{'op':'file_write','path':'themes/a3tal-global/'+name,'content':content,'expected_sha256':expected,'confirm':True,'dangerous':True})
    if not result.get('ok') or result.get('result',{}).get('sha256')!=digest(content):raise RuntimeError('Write not confirmed: '+name)
    after=read_file(name)
    if after['content']!=content:raise RuntimeError('Read-back differs: '+name)
def public(path):return request(SITE+path+('&' if '?' in path else '?')+'a3tal_ux_check='+str(time.time_ns()),auth=False)
def canonical(html):
    match=re.search(r'<link\b(?=[^>]*\brel=[\"\x27]canonical[\"\x27])[^>]*\bhref=[\"\x27]([^\"\x27]+)',html,re.I)
    return match.group(1) if match else ''
def robots(html):
    match=re.search(r'<meta\b(?=[^>]*\bname=[\"\x27]robots[\"\x27])[^>]*\bcontent=[\"\x27]([^\"\x27]+)',html,re.I)
    return match.group(1) if match else ''
def check_public():
    evidence=[]
    home=public('/')
    assert 'ux-improvements-20261031.css' in home and 'ux-improvements-20261031.js' in home,'Assets not visible'
    assert home.find('g-home-dtc-zone')<home.find('g-home-cars-section'),'Code search not promoted'
    assert 'مقالات جديدة تنضاف تلقائيًا' not in home,'Internal editorial copy remains'
    assert canonical(home)==SITE+'/','Homepage canonical changed'
    image=re.search(r'<meta\b(?=[^>]*property=[\"\x27]og:image[\"\x27])[^>]*content=[\"\x27]([^\"\x27]+)',home,re.I)
    assert image and 'icon.png' not in image.group(1),'Homepage still uses the site icon'
    evidence.append({'page':SITE+'/','checks':['code search promoted','assets','canonical','sharing image']})
    for path in ['/p0420-catalyst-efficiency-bank-1/','/dtc-p0342-chevrolet/','/dtc/p0136/','/dtc/p0400/']:
        html=public(path)
        assert 'd-quick-answer' in html,'Quick answer absent: '+path
        assert 'class="d-dtc-featured"' in html and 'wp-post-image' in html,'Visible cover absent: '+path
        assert html.find('شرح الكود وخطوات التشخيص')<html.find('class="d-dtc-featured"'),'Cover is outside the article'
        assert 'd-author-meta' in html,'Author and date absent: '+path
        assert len(re.findall(r'<h1\b',html,re.I))==1,'H1 count changed: '+path
        assert canonical(html)==SITE+path,'Canonical changed: '+path
        assert robots(html)==baseline_seo[path]['robots'],'Robots policy changed: '+path
        assert html.find('class="d-entry"')<html.find('class="d-share"'),'Sharing precedes the answer'
        evidence.append({'page':SITE+path,'checks':['cover inside article','quick answer','author','canonical','indexability','sharing order']})
    helper=public('/dtc/p0420/')
    assert re.search(r'content=[\"\x27]noindex,\s*follow',helper,re.I),'Mirror noindex policy changed'
    search=public('/?s=P0420')
    section=search.split('id="si-results"',1)[1]
    assert '/dtc/p0420/' not in section,'Duplicate mirror remains in search results'
    match=re.search(r'class="g-card-media"[^>]*href=[\"\x27]([^\"\x27]+)',section)
    assert match and match.group(1)==SITE+'/p0420-catalyst-efficiency-bank-1/','Exact code original is not first'
    assert 'data-google-vignette="false"' in section,'Navigation opt-out absent'
    evidence.append({'page':SITE+'/?s=P0420','checks':['single original result','global exact-code ordering','navigation opt-out']})
    directory=public('/service-centers/')
    brands=re.search(r'<select name="brand">(.*?)</select>',directory,re.S).group(1)
    kia=re.search(r'<option value="([^\"]+)"[^>]*>\s*(?:Kia|كيا)\s*</option>',brands,re.I)
    assert kia,'Kia guide option missing from brand filter'
    filtered=public('/service-centers/?brand='+urllib.parse.quote(kia.group(1)))
    guides=filtered.split('id="service-guides-heading"',1)[1]
    assert 'كيا' in guides and 'g-legacy-card' in guides,'Kia filter has no matching published guide'
    assert 'data-a3tal-action="call"' in directory and 'data-a3tal-action="map"' in directory,'Directory contact actions absent'
    evidence.append({'page':SITE+'/service-centers/','checks':['guide brand filter','matching Kia guides','call and map actions']})
    (OUT/'public-verification.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf8')
    for item in evidence:print('PUBLIC_UX_VERIFIED',item['page'],','.join(item['checks']),flush=True)
    return evidence

# Preflight every file before the first mutation, and lint executable PHP.
before={}
for name in EXISTING:
    live=read_file(name)
    baseline=(BACKUP/name).read_text('utf8')
    desired=(SOURCE/name).read_text('utf8')
    if live['content'] not in [baseline,desired]:raise RuntimeError('Concurrent live change; no writes: '+name)
    before[name]=live
for name in NEW:
    live=read_file(name,optional=True)
    desired=(SOURCE/name).read_text('utf8')
    if live and live['content']!=desired:raise RuntimeError('New path already contains other code: '+name)
    before[name]=live
for name in NEW+EXISTING:
    if name.endswith('.php'):subprocess.run(['php','-l',str(SOURCE/name)],check=True)
print('ALL_LIVE_SHA_GUARDS_AND_PHP_LINT_PASSED',flush=True)
baseline_seo={}
for path in ['/p0420-catalyst-efficiency-bank-1/','/dtc-p0342-chevrolet/','/dtc/p0136/','/dtc/p0400/']:
    html=public(path)
    baseline_seo[path]={'canonical':canonical(html),'robots':robots(html)}
(OUT/'seo-baseline.json').write_text(json.dumps(baseline_seo,ensure_ascii=False,indent=2),encoding='utf8')
applied=[]
try:
    for name in NEW+EXISTING:
        desired=(SOURCE/name).read_text('utf8')
        if before[name] and before[name]['content']==desired:
            print('ALREADY_DEPLOYED',name,flush=True);continue
        expected=before[name]['sha256'] if before[name] else digest('')
        write_file(name,desired,expected)
        applied.append(name)
        print('DEPLOYED_AND_READ_BACK',name,digest(desired),flush=True)
        time.sleep(1)
    result=request(API+'/admin',{'op':'cache_flush','confirm':True,'dangerous':True})
    if not result.get('ok'):raise RuntimeError('Cache purge not confirmed')
    check_public()
except Exception:
    for name in reversed(applied):
        if before[name] is None:continue
        try:
            write_file(name,before[name]['content'],digest((SOURCE/name).read_text('utf8')))
            print('ROLLED_BACK',name,flush=True)
        except Exception:print('ROLLBACK_CONFLICT_REQUIRES_REVIEW',name,flush=True)
    try:request(API+'/admin',{'op':'cache_flush','confirm':True,'dangerous':True})
    except Exception:pass
    raise
print('A3TAL_UX_DEPLOYMENT_AND_PUBLIC_VERIFICATION_COMPLETE',flush=True)
