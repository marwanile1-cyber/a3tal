document.addEventListener('DOMContentLoaded',()=> {
  const b=document.querySelector('.g-menu-toggle');
  const m=document.querySelector('.g-mobile-menu');
  if(b&&m){
    b.addEventListener('click',()=>{
      const open=m.classList.toggle('is-open');
      b.setAttribute('aria-expanded',open?'true':'false');
    });
  }

  document.querySelectorAll('.g-entry table').forEach(t=>{
    if(!t.parentElement.classList.contains('g-table-wrap')){
      const w=document.createElement('div');
      w.className='g-table-wrap';
      t.parentNode.insertBefore(w,t);
      w.appendChild(t);
    }
  });

  const viewport=document.querySelector('[data-a3tal-news-ticker]');
  if(viewport){
    const track=viewport.querySelector('.g-newsbar-track');
    const firstGroup=viewport.querySelector('.g-newsbar-group');
    if(track&&firstGroup){
      let x=0;
      let last=0;
      let paused=false;
      const speed=42;

      const step=(ts)=>{
        if(!last) last=ts;
        const dt=Math.min(40,ts-last);
        last=ts;
        if(!paused){
          x -= speed*(dt/1000);
          const resetAt=firstGroup.offsetWidth + 42;
          if(resetAt>0 && -x>=resetAt) x += resetAt;
          track.style.transform='translate3d('+x+'px,0,0)';
        }
        requestAnimationFrame(step);
      };

      viewport.addEventListener('mouseenter',()=>paused=true);
      viewport.addEventListener('mouseleave',()=>paused=false);
      viewport.addEventListener('focusin',()=>paused=true);
      viewport.addEventListener('focusout',()=>paused=false);
      requestAnimationFrame(step);
    }
  }
});