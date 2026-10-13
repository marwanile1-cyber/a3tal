/* A3TAL Global Garage, progressive browser. No fabricated DTC-to-model mapping. */
(function(){
'use strict';
var root=document.querySelector('[data-gg-garage]');if(!root)return;
/* Origin describes marque heritage, not assembly plant or present corporate ownership.
   Keep historic marques as discoverable names; editorially verify updates before expansion. */
var sources={
jp:[
'Toyota|تويوتا|toyota','Lexus|لكزس|lexus','Nissan|نيسان|nissan','Infiniti|إنفينيتي|infiniti','Honda|هوندا|honda','Acura|أكيورا|acura','Mazda|مازدا|mazda','Mitsubishi|ميتسوبيشي|mitsubishi','Suzuki|سوزوكي|suzuki','Subaru|سوبارو|subaru','Isuzu|إيسوزو|isuzu','Daihatsu|دايهاتسو|daihatsu','Hino|هينو|hino','Mitsuoka|ميتسوؤكا|','UD Trucks|يو دي تراكس|'
],
kr:[
'Hyundai|هيونداي|hyundai','Kia|كيا|kia','Genesis|جينيسيس|genesis','KGM|كي جي إم|','SsangYong|سانج يونج|ssangyong','Daewoo|دايو|daewoo','Renault Korea|رينو كوريا|','Asia Motors|آسيا موتورز|'
],
cn:[
'BYD|بي واي دي|byd','Geely|جيلي|geely','Chery|شيري|chery','Changan|شانجان|changan','Great Wall|جريت وول|greatwall','Haval|هافال|haval','Tank|تانك|','Ora|أورا|','Wey|واي|','Jetour|جيتور|','Exeed|إكسيد|','Omoda|أومودا|','Jaecoo|جايكو|','JAC|جاك|jac','GAC|جي إيه سي|gac','Trumpchi|ترامبشي|','Aion|أيون|','MG|إم جي|mg','Roewe|رووي|','Maxus|ماكسوس|','IM Motors|آي إم موتورز|','Nio|نيو|nio','XPeng|إكس بنج|xpeng','Li Auto|لي أوتو|','Leapmotor|ليب موتور|','Zeekr|زيكر|zeekr','Lynk & Co|لينك آند كو|lynkco','Hongqi|هونشي|hongqi','FAW|فاو|faw','Bestune|بيستون|','Dongfeng|دونج فينج|dongfeng','Voyah|فويا|','Forthing|فورثينج|','BAIC|بايك|baicmotor','Arcfox|أركفوكس|','Beijing|بكين|','DFSK|دي إف إس كيه|','Seres|سيريس|','AITO|آيتو|','Wuling|وولينج|wuling','Baojun|باوجون|','Changan Deepal|ديبال|','Avatr|أفاتر|','Xiaomi Auto|شاومي أوتو|xiaomi','Denza|دينزا|','Yangwang|يانج وانج|','Fangchengbao|فانج تشينج باو|'
],
in:[
'Tata|تاتا|tata','Mahindra|ماهيندرا|mahindra','Maruti Suzuki|ماروتي سوزوكي|marutisuzuki','Force Motors|فورس موتورز|','Ashok Leyland|أشوك ليلاند|','Hindustan Motors|هندوستان موتورز|','Bajaj Auto|باجاج|bajaj','Eicher|أيشر|eicher','Premier|بريميير|'
],
eu:[
'Mercedes-Benz|مرسيدس بنز|mercedesbenz','BMW|بي إم دبليو|bmw','Audi|أودي|audi','Volkswagen|فولكس فاجن|volkswagen','Porsche|بورشه|porsche','Opel|أوبل|opel','Smart|سمارت|smart','Maybach|مايباخ|','Mini|ميني|mini','Rolls-Royce|رولز رويس|rollsroyce','Bentley|بنتلي|bentley','Jaguar|جاكوار|jaguar','Land Rover|لاند روفر|landrover','Range Rover|رينج روفر|','Aston Martin|أستون مارتن|astonmartin','McLaren|ماكلارين|mclaren','Lotus|لوتس|lotus','MG Rover|إم جي روفر|','Vauxhall|فوكسهول|vauxhall','Peugeot|بيجو|peugeot','Citroën|سيتروين|citroen','Renault|رينو|renault','DS Automobiles|دي إس|dsautomobiles','Alpine|ألبين|alpine','Bugatti|بوجاتي|bugatti','Fiat|فيات|fiat','Alfa Romeo|ألفا روميو|alfaromeo','Ferrari|فيراري|ferrari','Lamborghini|لامبورجيني|lamborghini','Maserati|مازيراتي|maserati','Lancia|لانسيا|lancia','Abarth|أبارث|abarth','Pagani|باجاني|pagani','Skoda|سكودا|skoda','SEAT|سيات|seat','Cupra|كوبرا|cupra','Dacia|داسيا|dacia','Volvo|فولفو|volvo','Polestar|بولستار|polestar','Saab|ساب|saab','Koenigsegg|كونيجسيج|koenigsegg','Iveco|إيفيكو|iveco','Scania|سكانيا|scania','MAN|مان|man','Rimac|ريماك|rimac','KTM|كي تي إم|ktm'
],
us:[
'Ford|فورد|ford','Lincoln|لينكولن|lincoln','Chevrolet|شيفروليه|chevrolet','Cadillac|كاديلاك|cadillac','GMC|جي إم سي|gmc','Buick|بويك|buick','Chrysler|كرايسلر|chrysler','Jeep|جيب|jeep','Dodge|دودج|dodge','Ram|رام|ram','Tesla|تسلا|tesla','Rivian|ريفيان|rivian','Lucid|لوسيد|lucid','Hummer|هامر|hummer','Pontiac|بونتياك|pontiac','Saturn|ساترن|saturn','Mercury|ميركوري|mercury','Oldsmobile|أولدزموبيل|','Plymouth|بليموث|','Fisker|فيسكر|fisker','SSC|إس إس سي|'
],
other:[
'Proton|بروتون|proton','Perodua|بيرودوا|perodua','VinFast|فينفاست|vinfast','Togg|توج|','Iran Khodro|إيران خودرو|','SAIPA|سايبا|','Lada|لادا|lada','UAZ|واز|','GAZ|جاز|','Moskvich|موسكفيتش|','Holden|هولدن|holden','HSV|إتش إس في|','W Motors|دبليو موتورز|','Praga|براجا|'
]
};
var models={
'Toyota':'Corolla|كامري|Camry|Yaris|RAV4|Land Cruiser|Hilux|Prius|C-HR|Fortuner|Avanza',
'Nissan':'Sunny|Sentra|Altima|Maxima|Qashqai|Juke|X-Trail|Patrol|Navara',
'Honda':'Civic|Accord|City|CR-V|HR-V|Jazz|Pilot',
'Mazda':'Mazda 2|Mazda 3|Mazda 6|CX-3|CX-5|CX-30|CX-60|MX-5',
'Mitsubishi':'Lancer|Pajero|Outlander|Eclipse Cross|ASX|Xpander|Attrage|L200',
'Suzuki':'Alto|Swift|Dzire|Ciaz|Baleno|Vitara|Jimny|S-Presso',
'Subaru':'Impreza|Legacy|Forester|Outback|XV|WRX|BRZ',
'Hyundai':'Elantra|Accent|Sonata|Tucson|Santa Fe|Creta|i10|i20|Ioniq 5|Ioniq 6',
'Kia':'Sportage|Cerato|Rio|Picanto|Seltos|Sorento|Carnival|K5|EV6|EV9',
'Genesis':'G70|G80|G90|GV60|GV70|GV80',
'Chevrolet':'Aveo|Optra|Cruze|Captiva|Equinox|Tahoe|Silverado|Camaro|Malibu',
'Ford':'Focus|Fiesta|Fusion|Escape|Explorer|Mustang|F-150|Ranger|Bronco',
'Jeep':'Wrangler|Compass|Cherokee|Grand Cherokee|Renegade',
'Mercedes-Benz':'A-Class|C-Class|E-Class|S-Class|GLA|GLC|GLE|G-Class',
'BMW':'1 Series|3 Series|5 Series|7 Series|X1|X3|X5|X6|i4',
'Audi':'A3|A4|A6|A8|Q3|Q5|Q7|Q8|e-tron',
'Volkswagen':'Golf|Polo|Passat|Tiguan|Touareg|Jetta|T-Roc|ID.4',
'Opel':'Astra|Corsa|Insignia|Mokka|Crossland|Grandland|Vectra',
'Peugeot':'208|301|308|408|2008|3008|5008|508',
'Renault':'Logan|Sandero|Duster|Megane|Clio|Captur|Kadjar|Austral',
'Skoda':'Octavia|Fabia|Superb|Karoq|Kodiaq|Kamiq',
'Fiat':'500|Panda|Tipo|Punto|Doblo|500X',
'Volvo':'S60|S90|XC40|XC60|XC90|EX30',
'BYD':'F3|Dolphin|Atto 3|Seal|Song Plus|Han|Seagull',
'Chery':'Arrizo 5|Arrizo 6|Tiggo 3|Tiggo 4|Tiggo 7|Tiggo 8',
'Geely':'Emgrand|Coolray|Starray|Monjaro|Galaxy EX2|Geometry C',
'GAC':'GS3|GS4|GS8|Emzoom|Empow|Aion Y',
'Jetour':'X70|X70 Plus|X90|Dashing|T2',
'MG':'MG5|MG6|ZS|HS|RX5|MG4|One',
'JAC':'JS2|JS3|JS4|JS6|J7',
'Changan':'Alsvin|Eado|CS35|CS55|CS75|UNI-T|UNI-K',
'Haval':'H6|Jolion|H9|Dargo',
'Tata':'Nexon|Punch|Harrier|Safari|Tiago|Altroz',
'Mahindra':'Scorpio|XUV700|Thar|Bolero|XUV300',
'Proton':'Saga|Persona|X50|X70|S70',
'Lada':'Granta|Vesta|Niva|Largus',
'Tesla':'Model 3|Model Y|Model S|Model X|Cybertruck',
'Porsche':'911|Cayenne|Macan|Panamera|Taycan',
'Land Rover':'Defender|Discovery|Freelander',
'Jaguar':'XE|XF|F-Pace|E-Pace',
'Cadillac':'Escalade|XT4|XT5|CT5',
'Lincoln':'Navigator|Corsair|Aviator',
'GMC':'Sierra|Yukon|Terrain|Acadia'
};
var list=[];Object.keys(sources).forEach(function(origin){sources[origin].forEach(function(raw){var p=raw.split('|');list.push({en:p[0],ar:p[1],icon:p[2]||'',origin:origin});});});
var region='all',selected=null,selectedModel='',expanded=false;
var brandsWrap=document.getElementById('gg-brands'),modelsWrap=document.getElementById('gg-models'),empty=document.getElementById('gg-brands-empty');
var search=document.getElementById('gg-find'),counter=document.getElementById('gg-brand-count'),desc=document.getElementById('gg-model-desc');
function normalize(value){return String(value||'').toLowerCase().normalize('NFKD').replace(/[\u064b-\u065f\u0670]/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').replace(/[\u0300-\u036f]/g,'').trim();}
function node(tag,cls,content){var e=document.createElement(tag);if(cls)e.className=cls;if(content!=null)e.textContent=content;return e;}
function save(){try{localStorage.setItem('a3tal_gg_v1',JSON.stringify({brand:selected?selected.en:'',model:selectedModel}));}catch(e){}}
function setOrigin(value){region=value;selected=null;selectedModel='';expanded=false;document.querySelectorAll('[data-origin]').forEach(function(b){var active=b.dataset.origin===region;b.classList.toggle('is-active',active);b.setAttribute('aria-pressed',active?'true':'false');});drawBrands();drawModels();}
function drawBrands(){
  var needle=normalize(search.value), matches=list.filter(function(b){return (region==='all'||region===b.origin)&&(!needle||normalize(b.en).includes(needle)||normalize(b.ar).includes(needle)||(models[b.en]||'').toLowerCase().includes(needle));});
  var shown=matches;
  if(!needle&&region==='all'&&!expanded)shown=matches.slice(0,24);
  brandsWrap.replaceChildren();
  shown.forEach(function(brand){
    var b=node('button','gg-brand'+(selected&&selected.en===brand.en?' is-selected':''));b.type='button';b.setAttribute('aria-pressed',selected&&selected.en===brand.en?'true':'false');
    var symbol=node('span','gg-logo');
    var verifiedLogo=(window.a3talGarageBrandLogos||{})[brand.en];
    if(verifiedLogo){
      var img=document.createElement('img');
      img.src=verifiedLogo;img.alt='شعار '+brand.ar;
      img.width=88;img.height=62;img.loading='lazy';img.decoding='async';
      img.onerror=function(){img.remove();symbol.classList.add('gg-logo-wordmark');symbol.textContent=brand.en;};
      symbol.appendChild(img);
    }else{
      // Transparent and honest fallback: never present initials as a fake brand mark.
      symbol.classList.add('gg-logo-wordmark');symbol.textContent=brand.en;
    }
    var ar=node('strong','',brand.ar),en=node('small','',brand.en);b.append(symbol,ar,en);
    b.addEventListener('click',function(){selected=brand;selectedModel='';save();drawBrands();drawModels();document.getElementById('gg-models').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'nearest'});});
    brandsWrap.appendChild(b);
  });
  if(!needle&&region==='all'&&!expanded&&matches.length>shown.length){
    var more=node('button','gg-more','عرض جميع الماركات ('+matches.length+')');more.type='button';more.addEventListener('click',function(){expanded=true;drawBrands();});brandsWrap.appendChild(more);
  }
  counter.textContent=matches.length+' ماركة في هذا العرض';
  empty.hidden=matches.length>0;
}
var ggData={cars:[],guides:[]};
try{var rawGG=document.getElementById('a3tal-gg-data');if(rawGG)ggData=JSON.parse(rawGG.textContent);}catch(e){}
function selectVehicleRecord(brand,model){
  var nBrand=normalize(brand.en),nAr=normalize(brand.ar),nModel=normalize(model);
  if(!nModel)return null;
  return (ggData.cars||[]).find(function(car){
    var title=normalize(car.title),carBrand=normalize(car.brand);
    var compatibleBrand=carBrand===nBrand||carBrand===nAr||title.includes(nBrand)||title.includes(nAr);
    return compatibleBrand&&title.includes(nModel);
  })||null;
}
function drawDiagnostics(){
  var panel=document.getElementById('gg-diagnostics');if(!panel)return;
  var grid=document.getElementById('gg-diagnostics-grid');grid.replaceChildren();
  if(!selected){panel.hidden=true;return;}
  panel.hidden=false;
  var car=selectedModel?selectVehicleRecord(selected,selectedModel):null;
  var verified=car&&Array.isArray(car.verified_codes)?car.verified_codes:[];
  var guides=Array.isArray(ggData.guides)?ggData.guides:[];
  var generic=guides.filter(function(x){return /^P[0-9][0-9A-F]{3}$/.test(x.code);});
  var rows=[];
  verified.forEach(function(code){var found=guides.find(function(item){return item.code===code;});if(found)rows.push({data:found,verified:true});});
  // Start with the five newly reviewed guides, then continue with existing code pages.
  var preferred=['P0137','P0138','P0192','P0193','P0449'];
  preferred.forEach(function(code){var data=generic.find(function(x){return x.code===code;});if(data&&!rows.some(function(x){return x.data.code===code;}))rows.push({data:data,verified:false});});
  generic.slice().reverse().forEach(function(data){if(rows.length>=15)return;if(!rows.some(function(x){return x.data.code===data.code;}))rows.push({data:data,verified:false});});
  var d=document.getElementById('gg-diagnostics-description');
  d.textContent=verified.length?'توجد روابط فنية خاصة بهذا الموديل في القسم الأول. باقي الأكواد شروحات عامة وليس تشخيصًا لحالة عربيتك.':(selectedModel?'أدلة أكواد OBD العامة لتبدأ منها بعد قراءة كود عربيتك. لم نتحقق بعد من أعطال خاصة لهذا الجيل والمحرك.':'ابدأ بشروحات الأكواد العامة المتاحة لهذه الفئة من السيارات المزودة بنظام OBD-II. اختَر موديلًا عندما تتوفر بياناته، ولا تعتبر الكود عطلًا شائعًا لهذه الماركة.');
  if(car){var anchor=document.getElementById('gg-search-model');anchor.href=car.url;anchor.textContent='صفحة السيارة الموجودة على أعطال ←';}
  if(!rows.length){grid.appendChild(node('div','gg-placeholder','الأدلة قيد الإضافة. استخدم البحث بكود العطل في المكتبة.'));return;}
  rows.slice(0,15).forEach(function(row){var a=node('a','gg-diagnostic-card');a.href=row.data.url;a.append(node('b','',row.data.code),node('span','',row.data.title),node('small','',row.verified?'مطابق بمصدر فني':'شرح كود عام'));grid.appendChild(a);});
}
function drawModels(){
  modelsWrap.replaceChildren();drawDiagnostics();var selectedBox=document.getElementById('gg-selected');selectedBox.hidden=true;
  if(!selected){desc.textContent='اختَر الماركة أولاً لعرض موديلاتها المتاحة.';modelsWrap.appendChild(node('div','gg-placeholder','اختَر ماركة من البطاقات بالأعلى.'));return;}
  var data=models[selected.en]||'';
  // Published vehicle cards take priority over illustrative model names.
  // This exposes genuinely available pages even when the sample model list is incomplete.
  var published=(ggData.cars||[]).filter(function(car){
    return normalize(car.brand)===normalize(selected.en)||normalize(car.brand)===normalize(selected.ar);
  });
  var declared=data?data.split('|'):[];
  published.forEach(function(car){
    var exists=declared.some(function(m){return normalize(car.title).includes(normalize(m));});
    if(!exists)declared.unshift(car.title);
  });
  data=declared.join('|');
  desc.textContent=selected.ar+' · '+(data?'موديلات استرشادية متاحة للتصفح':'جارٍ استكمال بيانات الموديلات الموثقة');
  if(!data){modelsWrap.appendChild(node('div','gg-placeholder','العلامة متاحة في الدليل العالمي، لكن قائمة الموديلات لم تكتمل بعد. استخدم البحث العام للعثور على الأدلة المنشورة.'));selectedBox.hidden=false;document.getElementById('gg-selected-name').textContent=selected.ar;document.getElementById('gg-search-model').href='/?s='+encodeURIComponent(selected.ar);return;}
  data.split('|').forEach(function(model){
    var b=node('button','gg-model'+(selectedModel===model?' is-selected':''));b.type='button';b.setAttribute('aria-pressed',selectedModel===model?'true':'false');
    b.append(node('span','gg-model-car','◈'),node('strong','',model),node('small','',''));
    b.querySelector('small').textContent=selected.en;
    b.addEventListener('click',function(){selectedModel=model;save();drawModels();});
    modelsWrap.appendChild(b);
  });
  selectedBox.hidden=false;
  document.getElementById('gg-selected-name').textContent=selected.ar+(selectedModel?' · '+selectedModel:'');
  document.getElementById('gg-search-model').href='/?s='+encodeURIComponent(selected.en+(selectedModel?' '+selectedModel:''));
  drawDiagnostics();
}
root.querySelectorAll('[data-origin]').forEach(function(b){b.addEventListener('click',function(){search.value='';setOrigin(b.dataset.origin);});});
root.querySelector('[data-gg-reset]').addEventListener('click',function(){search.value='';setOrigin('all');save();});
search.addEventListener('input',function(){expanded=false;drawBrands();});
try{var old=JSON.parse(localStorage.getItem('a3tal_gg_v1')||'{}');if(old.brand){selected=list.find(function(b){return b.en===old.brand;})||null;selectedModel=selected&&models[selected.en]&&models[selected.en].split('|').includes(old.model)?old.model:'';}}catch(e){}
drawBrands();drawModels();
})();