document.addEventListener('DOMContentLoaded',function(){
  const menuBtn=document.querySelector('.a3-menu-toggle');
  const mobileMenu=document.querySelector('.a3-mobile-menu');
  if(menuBtn&&mobileMenu){
    menuBtn.addEventListener('click',function(){
      const open=mobileMenu.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded',open?'true':'false');
    });
  }
  const modal=document.getElementById('a3-car-modal');
  const openers=document.querySelectorAll('.a3-open-car');
  const closeBtn=document.getElementById('a3-close-car');
  const saveBtn=document.getElementById('a3-save-car');
  const title=document.getElementById('a3-car-title');
  const subtitle=document.getElementById('a3-car-subtitle');
  function openModal(e){if(e)e.preventDefault();if(modal){modal.classList.add('open');modal.setAttribute('aria-hidden','false');}}
  function closeModal(){if(modal){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');}}
  openers.forEach(function(el){el.addEventListener('click',openModal);});
  if(closeBtn)closeBtn.addEventListener('click',closeModal);
  if(modal)modal.addEventListener('click',function(e){if(e.target===modal)closeModal();});
  function loadCar(){
    try{
      const car=JSON.parse(localStorage.getItem('a3talCar')||'null');
      if(car&&title){
        const main=[car.make,car.model,car.year].filter(Boolean).join(' ');
        title.textContent='عربيتي: '+(main||'تم الاختيار');
        if(subtitle)subtitle.textContent=[car.engine].filter(Boolean).join(' · ')||'محفوظة على هذا الجهاز';
        ['make','model','year','engine'].forEach(function(k){const el=document.getElementById('a3-car-'+k);if(el)el.value=car[k]||'';});
      }
    }catch(e){}
  }
  if(saveBtn)saveBtn.addEventListener('click',function(){
    const car={};
    ['make','model','year','engine'].forEach(function(k){const el=document.getElementById('a3-car-'+k);car[k]=el?el.value.trim():'';});
    localStorage.setItem('a3talCar',JSON.stringify(car));
    loadCar();closeModal();
  });
  loadCar();
});
