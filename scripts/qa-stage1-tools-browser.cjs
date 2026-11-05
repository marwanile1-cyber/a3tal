'use strict';
const {chromium}=require('/tmp/a3tal-stage1/node_modules/playwright');
const BASE='https://a3tal.com';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for (const width of [390,1440]){
   const ctx=await browser.newContext({viewport:{width,height:850},locale:'ar-EG'});
   const page=await ctx.newPage(),errs=[];
   page.on('pageerror',e=>errs.push(e.message));
   let res=await page.goto(BASE+'/car-tools/?stage1_qa='+width,{waitUntil:'domcontentloaded',timeout:65000});
   if(!res||res.status()!==200)throw Error('Tools HTTP '+(res&&res.status()));
   await page.locator('#a3rt-litres').fill('25');
   await page.locator('#a3rt-distance').fill('320');
   await page.locator('#a3rt-litre-price').fill('20');
   await page.locator('#a3rt-fuel-form button').click();
   let fuel=await page.locator('#a3rt-fuel-result').innerText();
   if(!fuel.includes('لتر/100 كم')||fuel.includes('النتيجة هتظهر'))throw Error('Fuel calculator failed '+fuel);
   await page.locator('#a3rt-fluids').fill('1200');
   await page.locator('#a3rt-parts').fill('300');
   await page.locator('#a3rt-labor').fill('100');
   await page.locator('#a3rt-vat').fill('0');
   await page.locator('#a3rt-extra').fill('0');
   await page.locator('#a3rt-maint-form button').click();
   let total=await page.locator('#a3rt-maint-result').innerText();
   if(!total.includes('جنيه مصري')||total.includes('الإجمالي هيتحسب'))throw Error('Maintenance calc failed '+total);
   let metrics=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
   if(metrics.scroll>metrics.width+4)throw Error('Tools horizontal overflow '+JSON.stringify(metrics));
   if(errs.length)throw Error('Tools JavaScript errors: '+errs.join(' | '));
   console.log('STAGE1_TOOLS_BROWSER_PASS',width,fuel,total,JSON.stringify(metrics));
   await ctx.close();
  }
  const ctx=await browser.newContext({viewport:{width:1440,height:900},locale:'ar-EG'});
  const home=await ctx.newPage();
  await home.goto(BASE+'/?stage1_qa=browser',{waitUntil:'domcontentloaded',timeout:65000});
  for (const suffix of ['car-tools/#fuel-use','car-tools/#maintenance-cost','car-tires-prices-egypt-2026/']){
   if(await home.locator('.a3tal-reference-page .toolgrid a[href*="'+suffix+'"]').count()!==1)throw Error('Homepage tool link missing '+suffix);
  }
  if(await home.locator('.a3tal-reference-page .carcard[href*="kgm-torres-2027-egypt-price-trims-8speed"]').count()!==1)
   throw Error('Homepage KGM model does not open canonical price article');
  const cars=await ctx.newPage();
  await cars.goto(BASE+'/cars/?stage1_qa=browser',{waitUntil:'domcontentloaded',timeout:65000});
  for(const slug of ['kgm-torres-2027-egypt-price-trims-8speed','renault-boreal-2027-egypt-price-trims','jetour-t2-idm-4x4-2027-egypt-price-specs']){
   if(await cars.locator('.cg-car-card a[href*="'+slug+'"]').count()<1)throw Error('Catalogue card missing canonical link '+slug);
  }
  console.log('STAGE1_HOME_AND_MODEL_LINKS_BROWSER_PASS');
  await ctx.close();
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
