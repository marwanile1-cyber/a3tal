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
  const response=await page.goto('https://a3tal.com/?a3tal_reference_browser='+Date.now(),{waitUntil:'domcontentloaded',timeout:90000});
  if(!response||response.status()>=400)throw Error(label+' navigation HTTP '+response?.status());
  await page.waitForSelector('.a3tal-reference-page .hero',{timeout:15000});
  await page.waitForTimeout(2200);
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
  if(info.h1!==1||info.failedImages.length||!info.specLink||!info.hasCarousel||info.totalImages<20)throw Error(label+' failed UI assertions '+JSON.stringify(info));
  if(label==='mobile' && info.overflow>3)throw Error('Mobile horizontal overflow '+info.overflow);
  if(label==='desktop' && !info.heroBackground.includes('a3tal-ref-20261104-hero-desktop.webp'))throw Error('Desktop exact hero absent');
  if(label==='mobile' && !info.heroBackground.includes('a3tal-ref-20261104-hero-desktop.webp')){/* mobile uses separate scene */}
  await page.screenshot({path:dir+'/'+label+'-first-screen.png',fullPage:false,animations:'disabled'});
  await page.screenshot({path:dir+'/'+label+'-full.png',fullPage:true,animations:'disabled'});
  // Mode buttons are intentionally hidden below 720px; test their interaction on desktop.
  if(label==='desktop'){
    await page.locator('[data-mode="code"]').click();
    const input=page.locator('#query');
    if(await input.getAttribute('name')!=='code')throw Error('Desktop DTC search mode failed');
    if(await page.locator('#searchForm').getAttribute('action')!=='https://a3tal.com/dtc/')throw Error('Desktop DTC action failed');
    await page.locator('[data-mode="spec"]').click();
    if(await input.getAttribute('name')!=='q')throw Error('Desktop technical reference search mode failed');
    if(await page.locator('#searchForm').getAttribute('action')!=='https://a3tal.com/car-reference/')throw Error('Desktop reference search action failed');
  }
  const heroFile=label==='desktop'?'a3tal-ref-20261104-hero-desktop.webp':'a3tal-ref-20261104-hero-mobile.webp';
  if(label==='mobile'){
    const mobileHero=await page.locator('.hero-mobile-scene').evaluate(x=>getComputedStyle(x).backgroundImage);
    if(!mobileHero.includes(heroFile))throw Error('Mobile hero background is missing');
    if(!(await page.locator('.search-modes').isHidden()))throw Error('Mobile search controls unexpectedly visible outside reference layout');
    await page.locator('#menuToggle').click();
    if(!(await page.locator('.a3r-site-header .desktop-nav').isVisible()))throw Error('Mobile navigation failed to open');
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
