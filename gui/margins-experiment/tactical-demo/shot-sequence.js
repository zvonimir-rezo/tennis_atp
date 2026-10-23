/* Persistent source sequence for the three audited pressure moments. */
(() => {
  'use strict';
  const steps=document.querySelector('#stroke-steps');
  let currentPoint=null,selected=0,edges=[],viewportWidth=0,scrollPosition=0;
  function reveal(){
    const edge=edges[selected];if(!edge||!viewportWidth)return;
    const inset=4,max=Math.max(0,edges.at(-1).right+inset-viewportWidth);
    let target=scrollPosition;
    if(edge.left<target+inset)target=edge.left-inset;
    else if(edge.right>target+viewportWidth-inset)target=edge.right-viewportWidth+inset;
    target=Math.max(0,Math.min(max,target));
    if(target!==scrollPosition){scrollPosition=target;steps.scrollTo({left:target,behavior:'instant'});}
  }
  // Measure after layout and on resize; shot input itself reads no geometry.
  const measure=new ResizeObserver(()=>{
    edges=[...steps.children].map(button=>({left:button.offsetLeft,right:button.offsetLeft+button.offsetWidth}));
    viewportWidth=steps.clientWidth;reveal();
  });
  measure.observe(steps);
  steps.addEventListener('scroll',()=>{scrollPosition=steps.scrollLeft;},{passive:true});
  const names={1:'Djokovic',2:'Medvedev'};
  window.shotSequence={
    render({point,shots,index,select}){
      selected=index;
      // Identity persists while moving through a point. Only the selected state changes.
      if(currentPoint!==point){
        currentPoint=point;edges=[];steps.replaceChildren();steps.scrollLeft=0;scrollPosition=0;
        shots.forEach((shot,i)=>{
          const button=document.createElement('button');button.type='button';
          button.dataset.stroke=i;button.dataset.actor=shot.actor;
          const actor=document.createElement('span');actor.className='sequence-actor';actor.textContent=`${i+1} · ${names[shot.actor]}`;
          const type=document.createElement('span');type.className='sequence-shot';
          type.textContent=shot.serve?(shot.approach?'Serve + approach':'First serve'):shot.type+(i===1?' return':'');
          button.dataset.sourceToken=shot.token;
          button.append(actor,type);
          button.setAttribute('aria-label',`Stroke ${i+1}: ${names[shot.actor]}, ${type.textContent.toLowerCase()}`);
          button.addEventListener('click',event=>{select(i,event.detail>0);button.focus({preventScroll:true});});
          steps.append(button);
        });
        measure.unobserve(steps);measure.observe(steps);
      }
      [...steps.children].forEach((button,i)=>{
        button.setAttribute('aria-pressed',String(i===index));
        button.tabIndex=i===index?0:-1;
      });
      // Reveal only as much as necessary. Never scroll the page or queue a tween.
      reveal();
    }
  };
})();
