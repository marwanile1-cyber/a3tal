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
    'سو ايست':'soueast','ديبال':'changan deepal'
  };
  root.querySelectorAll('.cg-brand[data-brand-name]').forEach(function(card){
    var name=(card.getAttribute('data-brand-name')||'').trim();
    var key=aliases[name]||name.toLocaleLowerCase('en-US');
    if(key==='mercedes')key='mercedes-benz';
    if(key==='xpeng')key='xpeng';
    var data=library[key];
    if(typeof data!=='string'||data.indexOf('data:image/')!==0)return;
    var symbol=card.querySelector('.cg-brand-icon');
    if(!symbol)return;
    var icon=document.createElement('img');
    icon.src=data;
    icon.alt='';
    icon.loading='lazy';
    icon.decoding='async';
    icon.onerror=function(){icon.remove()};
    symbol.replaceChildren(icon);
  });
  var search=root.querySelector('#cg-car-search');
  var other=root.querySelector('#cg-filters input[name="s"]');
  if(search&&other){
    search.addEventListener('input',function(){other.value=search.value});
    other.addEventListener('input',function(){search.value=other.value});
  }
})();
