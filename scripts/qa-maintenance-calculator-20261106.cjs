/* Read-only browser QA for the source-backed A3tal maintenance scheduler. */
'use strict';
const { chromium } = require('/tmp/a3tal-maint-browser/node_modules/playwright');
const BASE='https://a3tal.com';
async function pageOk(page,url,label){
  const res=await page.goto(url,{waitUntil:'domcontentloaded',timeout:65000});
  if(!res||res.status()!==200)throw Error(label+' bad HTTP '+(res&&res.status()));
}
async function verifyAt(browser,width,model){
  const ctx=await browser.newContext({viewport:{width,height:860},locale:'ar-EG',deviceScaleFactor:1});
  const page=await ctx.newPage(),errs=[];
  page.on('pageerror',e=>errs.push(e.message));
  await pageOk(page,BASE+'/maintenance-schedules/?vehicle_entity='+model+'&maintenance_qa='+width,'maintenance');
  await page.locator('#a3ms-calculator').waitFor({timeout:18000});
  if(await page.locator('.a3ms-item').count()<5)throw Error('Missing real schedule items '+width);
  await page.locator('#a3ms-current-km').fill('57000');
  await page.locator('#a3ms-calc-button').click();
  await page.waitForTimeout(600);
  const state=await page.evaluate(()=>({hidden:document.querySelector('#a3ms-summary').hidden,
    text:document.querySelector('#a3ms-summary').textContent,
    inlineScript:!!document.querySelector('#a3ms-inline-script'),
    inlineStyle:!!document.querySelector('#a3ms-inline-style')}));
  if(state.hidden || !state.text.includes('نتائج الحساب'))throw Error('No actual calculation '+width+' '+JSON.stringify(state)+' page errors='+errs.join(' | '));
  const oil=page.locator('.a3ms-item').filter({hasText:'تغيير زيت المحرك الدوري'}).first();
  if(await oil.count()!==1)throw Error('Source-backed oil service missing '+width);
  await oil.locator('.a3ms-last-km').fill('47000');
  await page.locator('#a3ms-calc-button').click();
  if(!await oil.evaluate(n=>n.classList.contains('a3ms-due')))throw Error('Verified due interval not calculated '+width);
  await oil.locator('.a3ms-last-km').fill('50000');
  await page.locator('#a3ms-calc-button').click();
  if(!await oil.evaluate(n=>n.classList.contains('a3ms-later')))throw Error('Future schedule not recalculated '+width);
  await page.locator('#a3ms-usage').selectOption('severe');
  await page.locator('#a3ms-calc-button').click();
  if(!(await oil.locator('.a3ms-result').innerText()).includes('لا توجد فترة استخدام شاق موثقة'))throw Error('Severe mode must not invent source intervals '+width);
  await oil.locator('.a3ms-last-km').fill('58000');
  await page.locator('#a3ms-calc-button').click();
  if(!(await oil.locator('.a3ms-status').innerText()).includes('راجع الإدخال'))throw Error('Bad odometer input not blocked '+width);
  const metrics=await page.evaluate(()=>({w:innerWidth,scroll:document.documentElement.scrollWidth,cardPadding:getComputedStyle(document.querySelector('.a3ms-card')).paddingTop}));
  if(metrics.scroll>metrics.w+3)throw Error('Mobile/desktop horizontal overflow '+JSON.stringify(metrics));
  if(!metrics.cardPadding || parseFloat(metrics.cardPadding)<10)throw Error('Maintenance styling did not apply '+width);
  if(errs.length)throw Error('JavaScript errors '+errs.join(' | '));
  console.log('MAINTENANCE_BROWSER_PASS',width,'items',await page.locator('.a3ms-item').count(),JSON.stringify(metrics));
  await ctx.close();
}
(async()=>{
  const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  try{
    const ctx=await browser.newContext({viewport:{width:390,height:850},locale:'ar-EG'});
    const page=await ctx.newPage();
    await pageOk(page,BASE+'/maintenance-schedules/?maintenance_qa=overview','overview');
    const opts=await page.locator('.g-maintenance-select select[name="vehicle_entity"] option').evaluateAll(a=>a.map(e=>e.value).filter(Boolean));
    if(opts.length<1)throw Error('No reviewed maintenance models found');
    if(await page.locator('.g-maintenance-demo-ring').count())console.warn('MAINTENANCE_DEFAULT_ARCHIVE_EDGE_CACHE_STALE: model-specific calculations are tested separately');
    console.log('MAINTENANCE_AVAILABLE_MODEL_COUNT',opts.length);
    await ctx.close();
    for(const width of [390,1440])await verifyAt(browser,width,opts[0]);
    const missing=await browser.newPage();
    await pageOk(missing,BASE+'/maintenance-schedules/?vehicle_entity=85276&maintenance_qa=missing','missing model');
    if(await missing.locator('#a3ms-calculator').count())throw Error('Non-covered car wrongly displays schedule');
    console.log('MAINTENANCE_MISSING_MODEL_HONEST_EMPTY_PASS');
    await missing.close();
  }finally{await browser.close();}
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
