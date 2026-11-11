const { chromium } = require('/tmp/a3tal-watch-browser-qa/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const URL = 'https://a3tal.com/jacob-co-watch-offer/';
const OUT = path.resolve('reports/watch-offer');
fs.mkdirSync(OUT, { recursive: true });

(async () => {
 const result = { page: URL, checks: {}, videoSources: [], errors: [] };
 const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
 try {
  for (const [device, viewport] of Object.entries({
   desktop: { width: 1440, height: 900 },
   mobile: { width: 390, height: 844 },
  })) {
   const page = await browser.newPage({ viewport, deviceScaleFactor: 1 });
   page.on('pageerror', err => result.errors.push(device + ': ' + err.message));
   const response = await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 45000 });
   assert.strictEqual(response.status(), 200, device + ' HTTP not 200');
   await page.locator('#watch-title').waitFor({ timeout: 20000 });
   result.checks[device + '_seo_h1'] = (await page.locator('h1').count() === 1) &&
     (await page.locator('h1').innerText()).includes('ساعة جاكوب اند كو هاي كوبي في مصر');
   result.checks[device + '_offer'] = (await page.locator('body').innerText()).includes('24,000') &&
     (await page.locator('body').innerText()).includes('6 قطع فقط');
   result.checks[device + '_videos'] = (await page.locator('video').count()) === 3;
   result.checks[device + '_whatsapp'] = (await page.locator('a[data-watch-whatsapp]').first().getAttribute('href')).includes('wa.me/201025036151');
   await page.waitForFunction(() => { const img = document.querySelector('#jw-current-watch'); return !!img && img.complete && img.naturalWidth >= 650; }, null, { timeout: 25000 }).catch(() => {});
   result.checks[device + '_visible_img'] = await page.locator('#jw-current-watch').evaluate(img=>img.complete && img.naturalWidth >= 650);
   const before = await page.locator('#jw-current-watch').getAttribute('src');
   await page.locator('.jw-variant[data-watch-variant="gold"]').click();
   await page.waitForFunction(old => { const img = document.querySelector('#jw-current-watch'); const btn = document.querySelector('.jw-variant[data-watch-variant="gold"]'); return !!img && img.getAttribute('src') !== old && btn?.getAttribute('aria-pressed') === 'true'; }, before, { timeout: 12000 }).catch(() => {});
   const after = await page.locator('#jw-current-watch').getAttribute('src');
   const aria = await page.locator('.jw-variant[data-watch-variant="gold"]').getAttribute('aria-pressed');
   if (device === 'mobile') {
    const inspect = await page.locator('.jw-variant[data-watch-variant="gold"]').evaluate(el=>{const r=el.getBoundingClientRect(); return {html:el.outerHTML.slice(0,260), rect:{x:r.x,y:r.y,w:r.width,h:r.height},centerElement:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.outerHTML?.slice(0,200),readyState:document.readyState, goldStored:document.querySelector('.jw-gallery-card img:nth-child(1)')?.getAttribute('src')}; });
    await page.locator('.jw-variant[data-watch-variant="gold"]').evaluate(el=>el.click());
    const afterJs = await page.locator('#jw-current-watch').getAttribute('src');
    const ariaJs = await page.locator('.jw-variant[data-watch-variant="gold"]').getAttribute('aria-pressed');
    console.log('MOBILE_VARIANT_DEBUG', JSON.stringify({before,after,aria,afterJs,ariaJs,steelLoaded:result.checks[device + '_visible_img'],inspect}));
   }
   result.checks[device + '_variant_switch'] = before !== after && aria === 'true';
   result.checks[device + '_no_overflow'] = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 5);
   await page.locator('#watch-videos').scrollIntoViewIfNeeded();
   await page.screenshot({ path: path.join(OUT, 'watch-' + device + '.png'), fullPage: true });
   if(device==='desktop'){
    const mp4 = await page.locator('video source').evaluateAll(nodes => nodes.map(n => n.src));
    for(const src of mp4){
      const raw = await page.request.get(src,{timeout:45000,headers:{Range:'bytes=0-4095'}});
      const bytes=await raw.body();
      const valid=(raw.status()===200 || raw.status()===206) && bytes.length>=400 && bytes.toString('ascii',4,8)==='ftyp';
      result.videoSources.push({url:src,status:raw.status(),mime:raw.headers()['content-type'],bytes:bytes.length,valid_mp4:valid});
    }
    const schema=await page.locator('script[type="application/ld+json"]').allTextContents();
    result.checks['schema_product_videos']=schema.some(x=>{
      try{const j=JSON.parse(x); const graph=j['@graph']??[];return graph.some(n=>n['@type']==='Product'&& n.offers.price==='24000') && graph.filter(n=>n['@type']==='VideoObject').length>=3;}catch(e){return false;}
    });
    result.checks['canonical']=await page.locator('link[rel="canonical"]').first().getAttribute('href')===URL;
    result.checks['og_image']=!!(await page.locator('meta[property="og:image"]').first().getAttribute('content')).includes('watch-skeleton-premium-design');
   }
   await page.close();
  }
  result.checks['all_mp4_downloadable'] = result.videoSources.length===3&&result.videoSources.every(v=>v.valid_mp4);
  result.passed = Object.values(result.checks).every(Boolean) && result.errors.length === 0;
  console.log('WATCH_BROWSER_QA',JSON.stringify(result,null,2));
  if(!result.passed) process.exitCode = 1;
 } catch(err){result.errors.push(err.stack||String(err));result.passed=false;process.exitCode=1;}
 finally{
  fs.writeFileSync(path.join(OUT,'browser-qa.json'),JSON.stringify(result,null,2));
  await browser.close();
 }
})().catch(err=>{console.error(err);process.exit(1);});
