/* Car prices directory: progressive enhancement only, native GET filters work without JavaScript. */
(function(){
  'use strict';
  var root=document.querySelector('.cg-guide');
  if(!root) return;
  var library=window.a3talPriceBrandLogos||{};
  var aliases={
    'كيا':'kia','تويوتا':'toyota','هيونداي':'hyundai','نيسان':'nissan',
    'شيفروليه':'chevrolet','شيري':'chery','جيلي':'geely','سوزوكي':'suzuki',
    'مازدا':'mazda','هافال':'haval','بيجو':'peugeot','فولكس فاجن':'volkswagen',
    'مرسيدس':'mercedes-benz','سكودا':'skoda','بي ام دبليو':'bmw',
    'اوبل':'opel','رينو':'renault','جيتور':'jetour','جاك':'jac','ام جي':'mg',
    'سو ايست':'soueast','ديبال':'deepal'
  };
  root.querySelectorAll('.cg-brand[data-brand-name]').forEach(function(card){
    var name=(card.getAttribute('data-brand-name')||'').trim();
    var key=aliases[name]||name.toLocaleLowerCase('en-US');
    if(key==='mercedes')key='mercedes-benz';
    if(key==='xpeng')key='xpeng';
    var data=library[key];
    if(typeof data!=='string')return;
    var internal=data.indexOf('data:image/')===0;
    var external=(key==='forthing'&&data==='https://cdn.globalso.com/forthingmotor/new-logo-proportionss1.png')||
      (key==='soueast'&&data==='https://commons.wikimedia.org/wiki/Special:FilePath/Soueast_Logo.png');
    if(!internal&&!external)return;
    var symbol=card.querySelector('.cg-brand-icon');
    if(!symbol)return;
    var icon=document.createElement('img');
    icon.src=data;
    icon.alt='';
    icon.loading='lazy';
    icon.decoding='async';
    icon.onerror=function(){symbol.replaceChildren(document.createTextNode(name.substring(0,2)))};
    symbol.replaceChildren(icon);
  });
  var search=root.querySelector('#cg-car-search');
  var other=root.querySelector('#cg-filters input[name="car_search"]');
  if(search&&other){
    search.addEventListener('input',function(){other.value=search.value});
    other.addEventListener('input',function(){search.value=other.value});
  }
})();
