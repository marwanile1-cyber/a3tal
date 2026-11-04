(function(){
'use strict';
var root=document.querySelector('.g-ency-search');
if(root){
var form=root.querySelector('form'),input=form.querySelector('input[name]'),tabs=root.querySelectorAll('[data-ency-search]');
var routes={
car:{name:'s',url:root.dataset.home,placeholder:'ابحث باسم الماركة أو الموديل',pattern:''},
reference:{name:'q',url:root.dataset.reference,placeholder:'ابحث عن مواصفات موديل مثل MG7',pattern:''},
fault:{name:'code',url:root.dataset.dtc,placeholder:'اكتب كود عطل مثل P0420',pattern:'[PpBbCcUu][0-9a-fA-F]{4}'},
price:{name:'s',url:root.dataset.home,placeholder:'ابحث عن سعر عربية أو مراجعة',pattern:''}
};
Array.prototype.forEach.call(tabs,function(tab){
tab.addEventListener('click',function(){
var route=routes[tab.dataset.encySearch];if(!route)return;
Array.prototype.forEach.call(tabs,function(t){t.setAttribute('aria-selected',String(t===tab));});
form.action=route.url;input.name=route.name;input.placeholder=route.placeholder;input.value='';
if(route.pattern){input.setAttribute('pattern',route.pattern);input.setAttribute('maxlength','8');input.setAttribute('dir','ltr');}
else{input.removeAttribute('pattern');input.removeAttribute('maxlength');input.removeAttribute('dir');}
input.focus();
});
});
}
})();