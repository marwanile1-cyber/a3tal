/* Live desktop/mobile acceptance for A3tal's interactive, deterministic fault triage. */
'use strict';
const {chromium}=require('/tmp/a3tal-fault-browser/node_modules/playwright');
const URL='https://a3tal.com/fault-diagnosis/';
async function open(page,width){
 let problems=[];
 for(let i=1;i<=3;i++){
  const response=await page.goto(URL+'?fd_browser='+width+'-'+i+'-'+Date.now(),{waitUntil:'domcontentloaded',timeout:65000});
  if(!response||response.status()!==200)throw Error('Fault page HTTP '+(response&&response.status()));
  try{await page.locator('#a3fd-app[data-ready="1"]').waitFor({timeout:11000});return;}
  catch(e){problems.push({try:i,title:await page.title(),hasApp:await page.locator('#a3fd-app').count(),ready:await page.locator('#a3fd-app').getAttribute('data-ready').catch(()=>null)});}
 }
 throw Error('Live fault triage script never initialized '+JSON.stringify(problems));
}
async function scenario(page,name){
 await page.locator('#a3fd-symptoms button').filter({hasText:name}).first().click();
 await page.locator('#a3fd-questions fieldset').first().waitFor();
}
async function answer(page,q,value){
 await page.locator('#a3fd-questions input[name="a3fd-q'+q+'"][value="'+value+'"]').check();
}
async function report(page,expectedRisk){
 await page.locator('#a3fd-show:not([disabled])').click();
 await page.locator('#a3fd-report:not([hidden])').waitFor();
 const actual=await page.locator('#a3fd-report .a3fd-risk').getAttribute('class');
 if(!actual.includes('a3fd-risk-'+expectedRisk))throw Error('Expected '+expectedRisk+' but '+actual);
 if((await page.locator('#a3fd-report .a3fd-causes li').count())!==3)throw Error('Causes must remain three prioritised inspections');
 if(!await page.locator('#a3fd-report').innerText().then(s=>s.includes('مافيش مدى سعري مؤكد')))throw Error('Unverified repair price not explained');
}
async function tests(width){
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const ctx=await browser.newContext({viewport:{width,height:900},locale:'ar-EG'});
 const page=await ctx.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 try{
  await open(page,width);
  const num=await page.locator('#a3fd-app').getAttribute('data-scenario-count');
  if(Number(num)<18)throw Error('Fewer than 18 source-reviewed scenarios');
  if(!await page.locator('#a3fd-vehicles button').first().getAttribute('aria-pressed'))throw Error('Vehicle buttons not accessible');
  await scenario(page,'لمبة ضغط الزيت');
  await answer(page,0,0);await answer(page,1,1);
  await report(page,'stop');
  console.log('FAULT_TEST_STOP_OIL',width);
  await page.locator('#a3fd-symptoms button').filter({hasText:'Check Engine'}).first().click();
  await answer(page,0,0);await answer(page,1,1);
  await report(page,'caution');
  await answer(page,0,1);
  await report(page,'stop');
  console.log('FAULT_TEST_DYNAMIC_CHECK_ENGINE',width);
  await page.locator('#a3fd-danger input[value="fuel"]').check();
  await page.locator('#a3fd-symptoms button').filter({hasText:'Check Engine'}).first().click();
  await answer(page,0,0);await answer(page,1,1);
  await report(page,'stop');
  console.log('FAULT_TEST_GLOBAL_DANGER_OVERRIDE',width);
  await page.locator('#a3fd-danger input[value="none"]').check();
  await page.locator('#a3fd-vehicles button').filter({hasText:'موتوسيكل'}).click();
  await page.locator('#a3fd-cats button').filter({hasText:'التشغيل والأداء'}).click();
  await scenario(page,'بيفصل بعد ما يسخن');
  await answer(page,0,1);await answer(page,1,1);
  await report(page,'urgent');
  const refs=await page.locator('#a3fd-report .a3fd-link').evaluateAll(els=>els.map(el=>el.href));
  if(!refs.some(url=>url.includes('motorcycle-blue-smoke-exhaust-oil-burning-diagnosis')))throw Error('Motorcycle source article missing');
  console.log('FAULT_TEST_MOTORCYCLE_LINKS',width);
  const metrics=await page.evaluate(()=>{
   const root=document.getElementById('a3fd');
   return {viewport:innerWidth,pageWidth:document.documentElement.scrollWidth,rootWidth:root.scrollWidth,
    style:!!document.querySelector('#a3fd-inline-style'),
    script:!!document.querySelector('#a3fd-inline-script')};
  });
  if(metrics.pageWidth>metrics.viewport+5 || metrics.rootWidth>metrics.viewport+5)throw Error('Horizontal mobile/desktop overflow '+JSON.stringify(metrics));
  if(!metrics.style || !metrics.script)throw Error('Scoped CSS/JS missing');
  if(errors.length)throw Error('Browser runtime errors: '+errors.join(' | '));
  await page.screenshot({path:'/tmp/a3tal-fault-'+width+'.png',fullPage:true});
  console.log('FAULT_BROWSER_PASS',width,JSON.stringify(metrics));
 }finally{await ctx.close();await browser.close();}
}
(async()=>{for(const width of [390,1440])await tests(width);console.log('A3TAL_FAULT_DIAGNOSER_BOTH_VIEWPORTS_PASS')})().catch(e=>{console.error(e.stack||e);process.exit(1)});
