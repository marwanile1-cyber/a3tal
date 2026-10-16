// Browser-level regression checks, screenshots and layout health for A3tal /cars/.
// Read-only. Does not modify WordPress, payment accounts or indexed content.
'use strict';
const fs=require('fs');
const path=require('path');
const {chromium}=require('/tmp/a3tal-visual/node_modules/playwright');
const BASE='https://a3tal.com';
const DIR='car-visual-qa-output';
fs.mkdirSync(DIR,{recursive:true});
const summary=[];
const transient=new Set([429,500,502,503,504,520,522,524]);
async function getWithRetry(page,url,tag){
  let last=null;
  for(let n=0;n<4;n++){
    const sep=url.indexOf('?')<0?'?':'&';
    const target=url+sep+'qa_retry='+n;
    try{
      const response=await page.goto(target,{waitUntil:'domcontentloaded',timeout:65000});
      if(response&&response.status()===200){
        if(n) console.log('ORIGIN_RETRY_RECOVERED',tag,'attempt',n+1);
        return response;
      }
      last='status '+(response?response.status():'no-response');
      if(response&&!transient.has(response.status()))break;
    }catch(error){
      last=String(error.message||error).slice(0,240);
    }
    console.log('ORIGIN_TRANSIENT_RETRY',tag,'attempt',n+1,last);
    if(n<3)await new Promise(resolve=>setTimeout(resolve,2500*(n+1)));
  }
  throw Error('Origin unavailable after bounded retries: '+tag+' '+last);
}

async function screenshotAndTest(browser,w,h,name) {
  const ctx=await browser.newContext({viewport:{width:w,height:h},deviceScaleFactor:1,locale:'ar-EG',colorScheme:'light'});
  const page=await ctx.newPage();
  const errors=[];
  page.on('pageerror',e=>errors.push(String(e.message||e)));
  const response=await getWithRetry(page,BASE+'/cars/?qa_viewport='+w,name);
  if(!response || response.status()!==200)throw Error(name+' status '+(response&&response.status()));
  await page.waitForSelector('.cg-car-card',{timeout:30000});
  await page.waitForTimeout(1700);
  const metrics=await page.evaluate(()=>{
    const by=(s)=>document.querySelectorAll(s);
    const rect=(s)=>{const a=document.querySelector(s);if(!a)return null;const r=a.getBoundingClientRect();return {x:Math.round(r.x),width:Math.round(r.width),height:Math.round(r.height)};};
    return {
      innerWidth:innerWidth,scrollWidth:document.documentElement.scrollWidth,
      cards:by('.cg-car-card').length,brands:by('.cg-brand').length,
      brandLogos:by('.cg-brand-icon img').length,
      heroImages:by('.cg-hero-photo img').length,
      loadedCardImages:[...by('.cg-car-photo img')].filter(x=>x.complete&&x.naturalWidth>0).length,
      title:document.title,hero:rect('.cg-hero'),brand:rect('.cg-brands'),filter:rect('.cg-filter'),
      cssLoaded:!![...document.styleSheets].find(s=>String(s.href||'').includes('car-price-guide.css'))
    };
  });
  if(metrics.scrollWidth>metrics.innerWidth+3)throw Error(name+' horizontal overflow '+JSON.stringify(metrics));
  if(metrics.cards<6||metrics.brands<8||metrics.heroImages===0||!metrics.cssLoaded)throw Error(name+' missing guide components '+JSON.stringify(metrics));
  if(errors.length)throw Error(name+' JS errors '+errors.join(' | '));
  await page.screenshot({path:path.join(DIR,name+'.png'),fullPage:true});
  summary.push({name,status:response.status(),metrics});
  console.log('VISUAL_QA_PASS',name,JSON.stringify(metrics));
  await ctx.close();
}
async function filters(browser){
  const ctx=await browser.newContext({viewport:{width:390,height:844}});
  const page=await ctx.newPage();
  for(const [url,expected] of [
    ['/cars/?car_year=2027','K4'],
    ['/cars/?brand=kia&car_year=2027','K4'],
    ['/cars/?car_search=Kia&car_year=2027&brand=kia','Seltos'],
  ]){
    const response=await getWithRetry(page,BASE+url,'filter '+url);
    if(!response||response.status()!==200)throw Error('Bad filter response '+url+' '+(response&&response.status()));
    await page.waitForSelector('.cg-car-card',{timeout:30000});
    if(!await page.locator('.cg-car-card').first().innerText().then(x=>x.includes(expected)).catch(()=>false)){
      if(!await page.locator('.cg-guide').innerText().then(x=>x.includes(expected)))throw Error('Filter missing expected car '+url);
    }
    const robots=await page.locator('meta[name="robots"]').first().getAttribute('content');
    if(!robots||!robots.includes('noindex'))throw Error('Query filter should be noindex '+url+' got '+robots);
    summary.push({filter:url,status:response.status(),robots});
    console.log('FILTER_QA_PASS',url);
  }
  await ctx.close();
}
async function verifyTrimTables(browser){
  const context=await browser.newContext({viewport:{width:390,height:844},locale:'ar-EG'});
  const page=await context.newPage();
  for(const [slug,names,prices] of [
    ['skoda-octavia-2027-egypt',['Loft','Lounge','Suite'],[1825000,2050000,2250000]],
    ['mazda-3-2027-egypt',['Highline سيدان','Highline هاتشباك'],[1609000,1619000]],
    ['suzuki-alto-2027-egypt',['مانيوال'],[535000]],
    ['jac-js2-2027-egypt',['Smart'],[775000]]
  ]){
    const res=await getWithRetry(page,BASE+'/cars/'+slug+'/','trim '+slug);
    if(!res||res.status()!==200)throw Error('Car URL changed or failed '+slug);
    const region=page.locator('#trims.cg-trim-panel');
    await region.waitFor({timeout:20000});
    const txt=await region.innerText();
    for(const name of names)if(!txt.includes(name))throw Error('Missing verified trim '+slug+' '+name);
    const shown=await page.locator('#trims tbody tr .cg-trim-price').allInnerTexts();
    const normalized=shown.map(t=>Number(t.replace(/[\u0660-\u0669\u06f0-\u06f9]/g,c=>{
      const code=c.charCodeAt(0);return String(code>=0x06f0?code-0x06f0:code-0x0660);
    }).replace(/[^0-9]/g,'')));
    if(JSON.stringify(normalized)!==JSON.stringify(prices))
      throw Error('Trim prices not exact for '+slug+' '+JSON.stringify(normalized));
    const headers=await page.locator('#trims .cg-trim-table thead th').count();
    if(headers!==3)throw Error('Invalid trim table structure '+slug);
    const scroll=await page.evaluate(()=>{
      const el=document.querySelector('.cg-trim-scroller');
      return !!el&&el.clientWidth<=innerWidth&&el.scrollWidth>=el.clientWidth;
    });
    if(!scroll)throw Error('Mobile trim scroller misconfigured '+slug);
    summary.push({trim:slug,status:res.status(),rows:await page.locator('#trims tbody tr').count()});
    console.log('TRIMS_QA_PASS',slug);
  }
  await context.close();
}

(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  await screenshotAndTest(browser,390,844,'mobile-390');
  await screenshotAndTest(browser,768,920,'tablet-768');
  await screenshotAndTest(browser,1440,900,'desktop-1440');
  await filters(browser);
  await verifyTrimTables(browser);
  fs.writeFileSync(path.join(DIR,'report.json'),JSON.stringify(summary,null,2));
  console.log('CAR_VISUAL_AND_FILTER_QA_COMPLETE',summary.length);
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
