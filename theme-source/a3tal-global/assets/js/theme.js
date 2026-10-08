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
      let visible=true;
      let frame=0;
      let resetAt=0;
      const speed=42;
      const reducedMotion=window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const measure=()=>{
        const gap=parseFloat(window.getComputedStyle(track).gap)||42;
        resetAt=firstGroup.offsetWidth+gap;
        if(resetAt>0 && -x>=resetAt) x=0;
      };
      const stop=()=>{
        if(frame) cancelAnimationFrame(frame);
        frame=0;
        last=0;
      };
      const start=()=>{
        if(!frame && !paused && visible && !document.hidden && !reducedMotion){
          frame=requestAnimationFrame(step);
        }
      };
      const step=(ts)=>{
        frame=0;
        if(last && resetAt>0){
          x -= speed*(Math.min(40,ts-last)/1000);
          if(-x>=resetAt) x+=resetAt;
          track.style.transform='translate3d('+x+'px,0,0)';
        }
        last=ts;
        start();
      };
      const setPaused=(value)=>{paused=value;if(value)stop();else start();};
      measure();
      if('ResizeObserver' in window){new ResizeObserver(measure).observe(firstGroup);}
      else window.addEventListener('resize',measure,{passive:true});
      if('IntersectionObserver' in window){
        new IntersectionObserver(entries=>{
          visible=Boolean(entries[0] && entries[0].isIntersecting);
          if(visible)start();else stop();
        }).observe(viewport);
      }
      viewport.addEventListener('mouseenter',()=>setPaused(true));
      viewport.addEventListener('mouseleave',()=>setPaused(false));
      viewport.addEventListener('focusin',()=>setPaused(true));
      viewport.addEventListener('focusout',()=>setPaused(false));
      document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();else start();});
      start();
    }
  }
});