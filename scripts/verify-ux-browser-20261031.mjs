import fs from 'node:fs/promises';
import { chromium } from 'playwright';
const out = process.env.A3TAL_QA_OUTPUT;
if (!out) throw new Error('QA output directory required');
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({headless:true, executablePath:process.env.A3TAL_QA_CHROME || undefined});
const results=[];
try {
  for (const width of [320,390,1440]) {
    const context=await browser.newContext({viewport:{width,height:width<768?900:1000},deviceScaleFactor:1,userAgent:'A3tal-UX-Layout-QA/20261031'});
    // Keep variable third-party advertising creatives out of layout screenshots.
    await context.route(/googlesyndication|doubleclick|adservice|googleads|admaster/,route=>route.abort());
    const page=await context.newPage();
    const cases=[['home','/'],['p0420','/p0420-catalyst-efficiency-bank-1/'],['directory','/service-centers/']];
    for (const [name,path] of cases) {
      const response=await page.goto('https://a3tal.com'+path+'?a3tal_ux_browser='+Date.now(),{waitUntil:'domcontentloaded',timeout:90000});
      if (response.status()!==200) throw new Error(`${name} HTTP ${response.status()}`);
      await page.locator('h1').waitFor();
      await page.evaluate(()=>document.fonts.ready);
      const metrics=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,h1Count:document.querySelectorAll('h1').length,css:!!document.querySelector('link[href*="ux-improvements-20261031.css"]')}));
      if (metrics.documentWidth>metrics.width+1) throw new Error(`Horizontal overflow ${name} ${width}: ${metrics.documentWidth}`);
      if (metrics.h1Count!==1 || !metrics.css) throw new Error(`Missing semantic heading or stylesheet: ${name}`);
      if (name==='p0420') {
        if (!await page.locator('.d-quick-answer').isVisible()) throw new Error('Quick answer not visible');
        if (!await page.locator('.d-guide .d-dtc-featured img').count()) throw new Error('Assigned cover missing from article');
        const quick=await page.locator('.d-quick-answer').boundingBox();
        if (width<768 && quick.y>800) throw new Error('Quick answer is too far below the mobile opening');
      }
      await page.screenshot({path:`${out}/${name}-${width}.png`,fullPage:false});
      results.push({page:name,viewport:width,...metrics});
      console.log('BROWSER_LAYOUT_PASS',name,width,JSON.stringify(metrics));
    }
    if (width===390) {
      await page.goto('https://a3tal.com/?a3tal_ux_search='+Date.now(),{waitUntil:'domcontentloaded'});
      await page.locator('#g-v3-site-search').fill('P0420');
      await Promise.all([page.waitForURL(url=>url.searchParams.get('s')==='P0420'),page.locator('.g-v3-search button').click()]);
      const first=page.locator('.si-primary-grid .g-card-media').first();
      if ((await first.getAttribute('href'))!=='https://a3tal.com/p0420-catalyst-efficiency-bank-1/') throw new Error('Wrong primary code search result');
      if (await page.locator('#si-results a[href="https://a3tal.com/dtc/p0420/"]').count()) throw new Error('Mirrored result remains');
      await page.screenshot({path:`${out}/search-390.png`,fullPage:false});
      console.log('BROWSER_SEARCH_FORM_PASS');
    }
    await context.close();
  }
  await fs.writeFile(`${out}/browser-layout.json`,JSON.stringify({adCreativesBlockedForLayout:true,results},null,2));
} finally { await browser.close(); }
