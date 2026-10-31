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
    const cases=[['home','/'],['p0420','/p0420-catalyst-efficiency-bank-1/'],['directory','/service-centers/']];
    for (const [name,path] of cases) {
      // Isolate pages from delayed third-party navigations left by the prior page.
      const page=await context.newPage();
      let response;
      try {
        response=await page.goto('https://a3tal.com'+path,{waitUntil:'domcontentloaded',timeout:90000});
      } catch (error) {
        const state={page:name,viewport:width,url:page.url(),error:String(error),body:(await page.locator('body').innerText().catch(()=>''))?.slice(0,800)};
        await fs.writeFile(`${out}/navigation-error-${name}-${width}.json`,JSON.stringify(state,null,2));
        await page.screenshot({path:`${out}/navigation-error-${name}-${width}.png`}).catch(()=>{});
        throw error;
      }
      if (response.status()!==200) throw new Error(`${name} HTTP ${response.status()}`);
      await page.locator('h1').waitFor();
      await page.evaluate(()=>document.fonts.ready);
      const metrics=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,h1Count:document.querySelectorAll('h1').length,release:document.body.classList.contains('a3tal-ux-20261031')}));
      if (metrics.documentWidth>metrics.width+1) throw new Error(`Horizontal overflow ${name} ${width}: ${metrics.documentWidth}`);
      if (metrics.h1Count!==1 || !metrics.release) throw new Error(`Missing semantic heading or release marker: ${name}`);
      if (name==='home' && width===1440) {
        const size=await page.locator('#g-v3-main-title').evaluate(el=>parseFloat(getComputedStyle(el).fontSize));
        if (size>43) throw new Error('New homepage typography not applied');
      }
      if (name==='p0420') {
        if (!await page.locator('.d-quick-answer').isVisible()) throw new Error('Quick answer not visible');
        if (!await page.locator('.d-guide .d-dtc-featured img').count()) throw new Error('Assigned cover missing from article');
        const quick=await page.locator('.d-quick-answer').boundingBox();
        if (width<768 && quick.y>800) throw new Error('Quick answer is too far below the mobile opening');
      }
      await page.screenshot({path:`${out}/${name}-${width}.png`,fullPage:false});
      results.push({page:name,viewport:width,...metrics});
      console.log('BROWSER_LAYOUT_PASS',name,width,JSON.stringify(metrics));
      await page.close();
    }
    if (width===390) {
      const page=await context.newPage();
      await page.goto('https://a3tal.com/',{waitUntil:'domcontentloaded'});
      const navigations=[];
      page.on('framenavigated',frame=>{if(frame===page.mainFrame())navigations.push(frame.url());});
      // Tap the field as a mobile visitor does before typing; LiteSpeed starts
      // deferred interactive scripts on the first pointer or keyboard event.
      await page.locator('#g-v3-site-search').click();
      await page.locator('#g-v3-site-search').pressSequentially('P0420');
      try {
        await Promise.all([page.waitForURL(url=>url.searchParams.get('s')==='P0420',{waitUntil:'domcontentloaded',timeout:30000}),page.locator('.g-v3-search button').click()]);
      } catch (error) {
        const state=await page.evaluate(()=>({url:location.href,forms:[...document.querySelectorAll('form')].map(form=>({action:form.action,method:form.method,fields:[...form.querySelectorAll('input')].map(input=>({name:input.name,value:input.value}))}))}));
        await fs.writeFile(`${out}/search-error.json`,JSON.stringify({error:String(error),navigations,...state},null,2));
        await page.screenshot({path:`${out}/search-error.png`,fullPage:false});
        throw error;
      }
      const first=page.locator('.si-primary-grid .g-card-media').first();
      if ((await first.getAttribute('href'))!=='https://a3tal.com/p0420-catalyst-efficiency-bank-1/') throw new Error('Wrong primary code search result');
      if (await page.locator('#si-results a[href="https://a3tal.com/dtc/p0420/"]').count()) throw new Error('Mirrored result remains');
      await page.screenshot({path:`${out}/search-390.png`,fullPage:false});
      console.log('BROWSER_SEARCH_FORM_PASS');
      await page.close();
    }
    await context.close();
  }
  await fs.writeFile(`${out}/browser-layout.json`,JSON.stringify({adCreativesBlockedForLayout:true,results},null,2));
} finally { await browser.close(); }
