import { chromium } from 'playwright';
import { mkdirSync, existsSync, writeFileSync } from 'node:fs';
const dir='reports/a3tal-home-reference-v5/screenshots';
mkdirSync(dir,{recursive:true});
const opts={headless:true,args:['--no-sandbox','--disable-dev-shm-usage']};
if(existsSync('/usr/bin/google-chrome'))opts.executablePath='/usr/bin/google-chrome';
const browser=await chromium.launch(opts);
let reports=[];
try{
 for(const [label,width,height] of [['desktop',1440,900],['mobile',390,844]]){
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1,locale:'ar-EG'});
  page.on('pageerror',e=>console.log('PAGE_JS_ERROR',label,e.message));
  page.on('requestfailed',r=>{if(r.url().includes('home-reference-20261104'))console.log('REFERENCE_ASSET_REQUEST_FAILED',label,r.url(),r.failure()?.errorText);});
  const response=await page.goto('https://a3tal.com/?a3tal_reference_browser='+Date.now(),{waitUntil:'domcontentloaded',timeout:90000});
  if(!response||response.status()>=400)throw Error(label+' navigation HTTP '+response?.status());
  await page.waitForSelector('.a3tal-reference-page .hero',{timeout:15000});
  // WordPress page-cache and edge nodes can briefly serve the previous release
  // after a verified bridge write. Re-fetch before treating a stale view as a
  // permanent UI regression; retain all assertions against the public page.
  for(let attempt=0;attempt<7;attempt++){
    const live=await page.evaluate(()=>({
      h1:document.querySelector('.a3tal-reference-page h1')?.innerText||'',
      hubs:document.querySelectorAll('.a3tal-hub-tiles .hub-card').length
    }));
    if(live.h1.includes('للسيارات في مصر') && live.hubs===6)break;
    if(attempt===6)throw Error(label+' latest release not visible after repeated uncached requests '+JSON.stringify(live));
    console.log('PUBLIC_CACHE_RETRY',label,attempt+1,JSON.stringify(live));
    await page.waitForTimeout(3500);
    await page.goto('https://a3tal.com/?a3tal_reference_browser_retry='+Date.now()+'_'+attempt,{waitUntil:'domcontentloaded',timeout:90000});
    await page.waitForSelector('.a3tal-reference-page .hero',{timeout:15000});
  }
  await page.waitForTimeout(2200);
  const redundant=await page.locator('.a3r-home-directory, .g-home-dtc-zone, .g-home-cars-section, .g-home-os-section, .g-home-moto-section, .g-v3-mobile-dock').count();
  if(redundant!==0)throw Error(label+' legacy homepage sections or duplicate mobile dock are still rendered: '+redundant);
  if(await page.getByText('استكشف باقي موسوعة أعطال',{exact:true}).count())throw Error(label+' duplicate legacy directory still rendered');
  if(await page.locator('main.a3r-production-home > .a3tal-reference-page').count()!==1)throw Error(label+' expected precisely one V5 homepage interface');
  if(await page.locator('.a3tal-reference-page .dock').count()!==1)throw Error(label+' expected precisely one V5 mobile navigation dock');
  const hubs=await page.locator('.a3tal-hub-tiles .hub-card').count();
  if(hubs!==6)throw Error(label+' expected six compact PSEO navigation cards; got '+hubs);
  for(const path of ['/car-reference/','/dtc/','/motorcycles/','/parts/','/maintenance-schedules/','/service-centers/']){
    const card=page.locator('.a3tal-hub-tiles .hub-card[href="https://a3tal.com'+path+'"]');
    if(await card.count()!==1 || !(await card.isVisible()))throw Error(label+' missing visible PSEO hub '+path);
  }
  const heroText=await page.locator('.a3tal-reference-page .hero h1').innerText();
  if(!heroText.includes('للسيارات في مصر'))throw Error(label+' homepage H1 does not describe the Egyptian automotive portal');
  const metrics=await page.evaluate(()=>{
    const rect=selector=>{const el=document.querySelector(selector);if(!el)return null;const r=el.getBoundingClientRect();const st=getComputedStyle(el);return {top:Math.round(r.top),bottom:Math.round(r.bottom),height:Math.round(r.height),paddingTop:st.paddingTop,marginTop:st.marginTop};};
    return {header:rect('.a3r-site-header'),main:rect('main'),hero:rect('.a3tal-reference-page .hero'),h1:rect('.a3tal-reference-page .hero h1'),heroCopy:rect('.a3tal-reference-page .hero-copy'),scrollWidth:document.documentElement.scrollWidth,viewport:innerWidth};
  });
  console.log('LAYOUT_METRICS',label,JSON.stringify(metrics));
  const info=await page.evaluate(()=>{
    const img=[...document.querySelectorAll('.a3tal-reference-page img')];
    return {
      h1:document.querySelectorAll('h1').length,
      title:document.querySelector('h1')?.textContent?.trim()||'',
      totalImages:img.length,
      failedImages:img.filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.src).slice(0,10),
      overflow:document.documentElement.scrollWidth-window.innerWidth,
      heroBackground:getComputedStyle(document.querySelector('.hero'),'::before').backgroundImage,
      logo:document.querySelector('.topbar .logo')?.currentSrc||'',
      specLink:[...document.querySelectorAll('a')].some(a=>a.href==='https://a3tal.com/car-reference/'),
      hasCarousel:!!document.querySelector('.car-grid'),
      mobileDock:getComputedStyle(document.querySelector('.dock')).display,
    };
  });
  if(info.h1!==1||info.failedImages.length||!info.specLink||!info.hasCarousel||info.totalImages<16)throw Error(label+' failed UI assertions '+JSON.stringify(info));
  if(label==='mobile' && info.overflow>3)throw Error('Mobile horizontal overflow '+info.overflow);
  const cardLayout=await page.locator('.a3tal-hub-tiles').evaluate(el=>({
    columns:getComputedStyle(el).gridTemplateColumns.split(' ').length,
    clipped:[...el.querySelectorAll('.hub-card')].filter(c=>c.scrollWidth>c.clientWidth+2).length,
  }));
  if(cardLayout.clipped)throw Error(label+' unreadable or clipped navigation card');
  if(label==='mobile' && cardLayout.columns!==3)throw Error('Mobile PSEO navigation must have three compact columns');
  if(label==='desktop' && !info.heroBackground.includes('a3tal-ref-20261104-hero-desktop.webp'))throw Error('Desktop exact hero absent');
  if(label==='mobile' && !info.heroBackground.includes('a3tal-ref-20261104-hero-desktop.webp')){/* mobile uses separate scene */}
  // Load actual below-the-fold thumbnails before a full-page screenshot.
  // A screenshot of native loading=lazy images without scrolling shows false gray blanks.
  await page.evaluate(async()=>{
    const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
    const max=document.documentElement.scrollHeight;
    for(let y=0;y<max;y+=Math.max(350,Math.floor(window.innerHeight*.9))){
      window.scrollTo(0,y);
      await delay(90);
    }
    await delay(1100);
    document.documentElement.style.scrollBehavior='auto';window.scrollTo({top:0,behavior:'instant'});
    await delay(400);
  });
  const legacyImages=await page.evaluate(()=>[...document.querySelectorAll('.g-home img')].filter(x=>x.getBoundingClientRect().width>0).map(x=>({src:x.currentSrc||x.src,ok:x.complete&&x.naturalWidth>0})));
  const legacyBroken=legacyImages.filter(x=>!x.ok);
  if(legacyBroken.length)console.log('LEGACY_IMAGE_AUDIT',label,'broken',legacyBroken.slice(0,12));
  console.log('LAZY_IMAGE_SCROLL_AUDIT',label,'total',legacyImages.length,'loaded',legacyImages.length-legacyBroken.length);
  await page.screenshot({path:dir+'/'+label+'-first-screen.png',fullPage:false,animations:'disabled'});
  await page.screenshot({path:dir+'/'+label+'-full.png',fullPage:true,animations:'disabled'});
  // Mode buttons are intentionally hidden below 720px; test their interaction on desktop.
  if(label==='desktop'){
    console.log('SEARCH_MODE_BEFORE',JSON.stringify(await page.evaluate(()=>({scripts:[...document.scripts].filter(x=>x.src.includes('home-reference-20261104')).map(x=>({src:x.src,async:x.async,defer:x.defer,type:x.type})), inputName:document.querySelector('#query')?.name,readyState:document.readyState}))));
    await page.locator('[data-mode="code"]').click();
    console.log('SEARCH_MODE_AFTER',JSON.stringify(await page.evaluate(()=>({inputName:document.querySelector('#query')?.name,modeActive:document.querySelector('[data-mode="code"]')?.classList.contains('active')}))));
    const input=page.locator('#query');
    if(await input.getAttribute('name')!=='code')throw Error('Desktop DTC search mode failed');
    if(await page.locator('#searchForm').getAttribute('action')!=='https://a3tal.com/dtc/')throw Error('Desktop DTC action failed');
    await page.locator('[data-mode="spec"]').click();
    if(await input.getAttribute('name')!=='q')throw Error('Desktop technical reference search mode failed');
    if(await page.locator('#searchForm').getAttribute('action')!=='https://a3tal.com/car-reference/')throw Error('Desktop reference search action failed');
  }
  const heroFile='a3tal-ref-20261104-hero-desktop.webp'; // shared clean scene has no baked-in copy
  if(label==='mobile'){
    const mobileHero=await page.locator('.hero-mobile-scene').evaluate(x=>getComputedStyle(x).backgroundImage);
    if(!mobileHero.includes(heroFile))throw Error('Mobile hero background is missing');
    if(!(await page.locator('.search-modes').isVisible()))throw Error('Mobile search controls unexpectedly hidden');
    await page.locator('#menuToggle').click();
    if(!(await page.locator('.a3r-site-header .desktop-nav').isVisible()))throw Error('Mobile navigation failed to open');
    if(!(await page.locator('.g-mobile-bottom').isHidden()))throw Error('Duplicate legacy mobile navigation still visible');
    if(!(await page.locator('.a3tal-reference-page .dock').isVisible()))throw Error('Reference mobile dock missing');
    if(!(await page.locator('.search-modes').isVisible()))throw Error('Search modes unavailable on mobile');
  }
  const heroLoaded=await page.evaluate(async filename=>{
    const probe=new Image();
    probe.src='https://a3tal.com/wp-content/uploads/2026/11/'+filename;
    try{await probe.decode();return probe.naturalWidth>0;}catch{return false;}
  },heroFile);
  if(!heroLoaded)throw Error(label+' hero image failed to decode '+heroFile);
  reports.push({device:label,...info});
  console.log('BROWSER_VERIFIED',label,'images',info.totalImages,'overflow',info.overflow,'H1',info.h1);
  await page.close();
 }
 writeFileSync('reports/a3tal-home-reference-v5/browser-check.json',JSON.stringify(reports,null,2));
}finally{await browser.close();}
