document.addEventListener('DOMContentLoaded',function(){
 const b=document.querySelector('.ap-menu-btn'),m=document.querySelector('.ap-mobile-menu');
 if(b&&m)b.addEventListener('click',function(){const o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false')});
 document.querySelectorAll('.ap-entry table').forEach(function(t){if(t.parentElement&&t.parentElement.classList.contains('ap-table-wrap'))return;const w=document.createElement('div');w.className='ap-table-wrap';t.parentNode.insertBefore(w,t);w.appendChild(t)});
});
