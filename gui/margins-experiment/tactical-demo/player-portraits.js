/* Editorial identity art. Hitter emphasis comes only from the current shot actor. */
(() => {
  'use strict';
  const art=document.querySelector('.rivalry-art'),strip=document.querySelector('#hitter-strip');
  const pieces=[...art.querySelectorAll('.portrait-piece')], people=[...strip.querySelectorAll('.hitter')];
  const system=matchMedia('(prefers-reduced-motion: reduce)');
  const ease=getComputedStyle(document.documentElement).getPropertyValue('--ease-out').trim();
  let input='pointer', entered=false, pending=false, actor=1;
  const running=new Set();
  const reduced=()=>system.matches||document.body.classList.contains('motion-reduced');
  function settle(){for(const animation of running)animation.cancel();running.clear();strip.dataset.motion='instant';}
  document.addEventListener('keydown',()=>{input='keyboard';settle();},{capture:true});
  document.addEventListener('pointerdown',()=>{input='pointer';},{capture:true,passive:true});
  function enter(){
    if(entered||pending)return;
    pending=true;
    Promise.allSettled(pieces.map(p=>p.querySelector('img').decode())).then(()=>{
      pending=false;
      const box=art.getBoundingClientRect();
      if(entered||box.bottom<=0||box.top>=innerHeight)return;
      entered=true;art.dataset.entered='true';
      if(input==='keyboard')return;
      const gentle=reduced();
      pieces.forEach((piece,i)=>{
        const from=gentle?{opacity:0}:{opacity:0,transform:`translateY(24px) rotate(${i===0?-2:2}deg) scale(1.025)`};
        const to=gentle?{opacity:1}:{opacity:1,transform:'translateY(0) rotate(0deg) scale(1)'};
        const animation=piece.animate([from,to],{duration:gentle?100:240,delay:gentle?0:i*40,easing:ease,fill:'backwards'});
        running.add(animation);animation.finished.catch(()=>{}).finally(()=>running.delete(animation));
      });
    });
  }
  const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting))enter();},{threshold:.15});
  art.dataset.motionReady='true';
  observer.observe(art);
  const preference=()=>{if(reduced())settle();};
  system.addEventListener('change',preference);
  new MutationObserver(preference).observe(document.body,{attributes:true,attributeFilter:['class']});
  window.playerPortraits={
    setHitter(next,pointer=false){
      if(next!==1&&next!==2)return;
      actor=next;
      strip.dataset.motion=pointer?(reduced()?'gentle':'pointer'):'instant';
      strip.dataset.actor=String(actor);strip.setAttribute('aria-label',`Recorded hitter: ${actor===1?'Djokovic':'Medvedev'}`);
      for(const person of people){const active=+person.dataset.player===actor;person.classList.toggle('is-hitter',active);person.querySelector('.hitter-status').setAttribute('aria-hidden',String(!active));}
    },
    snapshot(){return {actor,entered,pending,input,reduced:reduced(),running:running.size,motion:strip.dataset.motion};}
  };
})();
