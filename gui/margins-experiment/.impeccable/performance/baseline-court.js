/* Margins: one symbolic court, five sets, 422 persistent records.
   Scroll is a direct, reversible playhead. No inferred shot positions or clock. */
(() => {
'use strict';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],ns='http://www.w3.org/2000/svg';
const rows=window.MARGINS_RECORDS.map(raw=>({id:+raw.Pt,winner:+raw.PtWinner,set:1+(+raw.Set1)+(+raw.Set2),tb:+raw.Gm1===+raw.Gm2&&+raw.Gm1===((+raw.Set1)+(+raw.Set2)===4?12:6)}));
const subsets={all:rows,set2:rows.filter(r=>r.set===2),other:rows.filter(r=>r.set!==2),tb:rows.filter(r=>r.tb),rest:rows.filter(r=>r.set!==2&&!r.tb)};
const stats=a=>({n:a.length,f:a.filter(r=>r.winner===1).length,d:a.filter(r=>r.winner===2).length});
const signed=n=>n>0?'+'+n:n<0?'−'+Math.abs(n):'0';
const clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,n)),lerp=(a,b,t)=>a+(b-a)*t;
const smooth=t=>{t=clamp(t);return t*t*(3-2*t);};
const section=$('#sequence'),stage=$('#theatre'),scene=$('#scene'),object=$('#court-object'),art=$('#evidence-art');
const motionQuery=matchMedia('(prefers-reduced-motion: reduce)');
let override=false,progress=0,phase=-1,queued=false,point=1,geometry=[],layouts=[],plotW=0,plotH=0,reduceChapter=0;
const isReduced=()=>motionQuery.matches||override;
const stops=[0,.38,.61,.86,1];
const chapters=[
 {title:'The anatomy<br>of <em>almost.</em>',copy:'Federer won fourteen more points.<br>Djokovic won Wimbledon.',caption:'An illustrated court. A real point record.'},
 {title:'Five sets.<br><em>Uneven ground.</em>',copy:'Federer’s point margins: −5, +14, +1, +5, −1. The advantage was not spread evenly.',caption:'Five equal court sections name sets. Their area does not encode point totals.'},
 {title:'All fourteen.<br><em>In one set.</em>',copy:'Set two holds the entire net surplus. The other four sets, taken together, were 192–192.',caption:'Set two stays present: IDs 88–125. A partition, not a match without that set.'},
 {title:'Even.<br><em>Not uniform.</em>',copy:'Hold set two fixed. In the other four sets, −9 in tiebreaks and +9 outside them cancel.',caption:'Other four sets: (12 − 21) + (180 − 171) = −9 + 9 = 0.'},
 {title:'Real.<br><em>Concentrated.</em>',copy:'The full-match total is true. Alone, it does not establish sustained dominance.',caption:'Set two counted. More games, too: Federer 36 / Djokovic 32. No claim about deservedness.'}
];
const slabs=[];
const courtLines='<rect x="65" y="45" width="720" height="330"/><path d="M65 87h720M65 333h720M280 87v246M570 87v246M280 210h290M425 45v330M61 210h8M781 210h8"/>';
for(let i=0;i<5;i++){
 const slab=document.createElement('div');slab.className='court-slab';slab.dataset.set=i+1;slab.style.left=(i*20)+'%';
 slab.innerHTML=`<div class="slab-back"></div><div class="slab-front"></div><div class="slab-side"></div><div class="slab-top" style="background-position:${-i*170}px 0"><svg class="court-linework" style="left:${-i*100}%" viewBox="0 0 850 420" aria-hidden="true">${courtLines}</svg><div class="slab-paper"></div></div>`;
 object.append(slab);slabs.push(slab);
}
const net=document.createElement('div');net.className='court-net';net.innerHTML='<span></span>';object.append(net);$('#net-object').remove();
const marks=new Map();
for(const r of rows){const node=document.createElementNS(ns,r.winner===1?'circle':'rect');if(r.winner===1)node.setAttribute('r','2.65');else{const side=Math.sqrt(Math.PI*2.65*2.65);node.setAttribute('x',-side/2);node.setAttribute('y',-side/2);node.setAttribute('width',side);node.setAttribute('height',side);}node.setAttribute('class','point '+(r.winner===2?'dj':'fed'));node.dataset.id=r.id;node.dataset.winner=r.winner;$('#marks').append(node);marks.set(r.id,node);}
function groups(n){if(n<2)return[1,2,3,4,5].map(s=>({name:'Set '+s,records:rows.filter(r=>r.set===s),filter:'set'+s}));if(n===2)return[{name:'Set two',records:subsets.set2,filter:'set2',accent:true},{name:'Other four sets',records:subsets.other,filter:'other'}];return[{name:'Set two',records:subsets.set2,filter:'set2',accent:true},{name:'Three tiebreaks',records:subsets.tb,filter:'tb'},{name:'Other points in those sets',records:subsets.rest,filter:'rest'}];}
function calculate(n){
 const mobile=innerWidth<=760,short=mobile&&innerHeight<740,w=plotW,h=plotH,coords=new Map(),labels=[],gs=groups(n);
 for(let i=0;i<gs.length;i++){
  const g=gs[i],st=stats(g.records);let x,y,width;
  if(n<2){width=w/5-(mobile?6:22);x=i*w/5;y=0;}
  else if(n===2){x=i===0?0:w*.34;width=i===0?w*.27:w*.64;y=0;}
  else {x=i===0?0:i===1?w*.34:w*.69;width=i===0?w*.27:w*.29;y=0;}
  // On phone, the objection stacks the two complementary groups beside the held set.
  if(mobile&&n>=3){if(i===0)width=w*.35;else{x=w*.43;width=w*.55;y=i===1?0:h*(short?.415:.45);}}
  if(mobile&&n===2&&i===0)width=w*.35;
  if(mobile&&n===2&&i===1){x=w*.43;width=w*.55;}
  const header=n<2?(short?148:160):(mobile?(short?(i===0?114:n===2?136:90):140):175);
  const lane=(width-(mobile?7:16))/2,pitch=n<2?(mobile?(short?4.8:4.9):7.3):(mobile?5.3:7.7),cols=Math.max(1,Math.floor((lane-5)/pitch));
  for(const winner of[1,2])g.records.filter(r=>r.winner===winner).forEach((r,j)=>coords.set(r.id,{x:x+4+(winner-1)*(lane+(mobile?7:16))+(j%cols)*pitch,y:y+header+Math.floor(j/cols)*pitch}));
  labels.push({...g,...st,x,y,width});
 }
 return {coords,labels};
}
function drawLabels(n){
 const holder=$('#group-labels'),focused=holder.contains(document.activeElement)?document.activeElement.dataset.inspectFilter:null;
 holder.replaceChildren();
 for(const g of layouts[n].labels){
  const el=document.createElement('div');el.className='group-label'+(g.accent?' accent':'');el.dataset.group=g.filter;el.style.left=g.x+'px';el.style.top=g.y+'px';el.style.width=g.width+'px';
  el.innerHTML=`<button data-inspect-filter="${g.filter}" aria-label="Inspect ${g.name}: ${g.n} points, Federer ${g.f}, Djokovic ${g.d}">${g.name}</button><span class="group-sample">${g.n}/422 points</span><span class="group-margin">${signed(g.f-g.d)}</span><div class="group-counts"><span>F <b>${g.f}</b></span><span>D <b>${g.d}</b></span></div>`;
  holder.append(el);
 }
 if(focused){const next=holder.querySelector(`[data-inspect-filter="${focused}"]`);(next||$('[data-stop="'+n+'"]')).focus({preventScroll:true});}
}
function setChapter(n){
 if(n===phase)return;phase=n;stage.dataset.phase=n;
 $('#chapter-title').innerHTML=chapters[n].title;$('#chapter-copy').innerHTML=chapters[n].copy;$('#stage-caption').textContent=chapters[n].caption;
 $('#story').classList.toggle('compact',n!==0);
 $$('.chapter-track button').forEach((b,i)=>{if(i===n)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});
 $('#transition-status').textContent=chapters[n].copy.replace(/<[^>]+>/g,' ');
 $('#ledger-desc').textContent=groups(n).map(g=>{const s=stats(g.records);return`${g.name}: ${s.n} of 422, Federer ${s.f}, Djokovic ${s.d}.`;}).join(' ')+' Positions are groups, never shot locations.';
 drawLabels(n===0?1:n);
}
function paint(){
 queued=false;
 if(!plotW)return;
 if(!isReduced()){const rect=section.getBoundingClientRect();progress=clamp(-rect.top/(section.offsetHeight-stage.clientHeight));}
 else progress=stops[reduceChapter];
 const n=progress<.20?0:progress<.46?1:progress<.73?2:progress<.96?3:4;
 setChapter(n);
 const w=innerWidth,h=stage.clientHeight,mobile=w<=760;
 const split=smooth((progress-.09)/.23),flat=smooth((progress-.20)/.25),apart=smooth((progress-.43)/.14),cancel=smooth((progress-.71)/.13);
 const sx0=Math.min(w*(mobile?1.03:.69)/850,h*(mobile?.4:.57)/420)*(mobile&&h<650?.7:1),sx1=plotW/850;
 const sx=lerp(sx0,sx1,flat),sy=lerp(sx0,plotH/420,flat);
 const cx=lerp(w*(mobile?.51:.66),w*.5,flat),cy=lerp(h*(mobile?.60:.62),art.offsetTop+plotH/2,flat);
 $('#camera').style.transform=`translate3d(${cx-425}px,${cy-210}px,0) scale(${sx},${sy})`;
 object.style.transform=`rotateX(${lerp(57,0,flat)}deg) rotateZ(${lerp(-25,0,flat)}deg)`;
 let restIndex=0;
 for(let i=0;i<5;i++){
  const selected=i===1,ri=selected?0:restIndex++;
  const separated=(i-2)*24*split;
  const targetX=selected?-170:(mobile?365.5+ri*116.875:289+ri*134)-i*170;
  const x=lerp(separated,targetX,apart);
  const tx=selected?x:lerp(x,(mobile?365.5:ri<2?289:586)+(ri%2)*7-i*170,cancel);
  const targetScale=selected?(mobile?1.75:1.34):(mobile?.65:.76);
  const scaleX=lerp(1,selected?targetScale:lerp(targetScale,mobile?2.75:1.44,cancel),apart);
  let y=selected?0:(ri%2)*6*cancel,z=lerp(selected?24:4,selected?12:(ri%2)*4,apart)*split;
  if(mobile&&!selected&&cancel){y=ri<2?0:420*(innerHeight<740?.415:.45);}
  slabs[i].style.transform=`translate3d(${tx}px,${y}px,${z}px) scale(${scaleX},${mobile&&!selected?lerp(1,ri<2?.4:.55,cancel):1})`;
  const paper=slabs[i].querySelector('.slab-paper');paper.style.opacity=flat*(selected?.89:.97);
  slabs[i].querySelector('.court-linework').style.opacity=(1-flat)*.88;
 }
 net.style.opacity=1-smooth((progress-.11)/.15);
 const shadow=$('#floor-shadow');shadow.style.transform=`translate(20px,40px) rotate(${lerp(-22,0,flat)}deg) scale(${lerp(1,.9,flat)},${lerp(1,.65,flat)})`;shadow.style.opacity=lerp(.24,.13,flat);
 $('#scene-note').style.opacity=1-smooth(progress/.15);
 $('#opening-result').style.opacity=1-smooth((progress-.12)/.08);$('#opening-result').style.pointerEvents=n===0?'auto':'none';
 const visibility=isReduced()?1:smooth((progress-.24)/.12);art.style.opacity=visibility;art.inert=visibility<.5;art.setAttribute('aria-hidden',String(visibility<.5));
 const a=layouts[1].coords,b=layouts[2].coords,c=layouts[3].coords;
 geometry=rows.map(r=>{const first=a.get(r.id),mid=b.get(r.id),last=c.get(r.id);return{id:r.id,x:lerp(lerp(first.x,mid.x,apart),last.x,cancel),y:lerp(lerp(first.y,mid.y,apart),last.y,cancel)};});
 for(const p of geometry)marks.get(p.id).style.transform=`translate(${p.x}px,${p.y}px)${mobile?' scale(.8)':''}`;
 // Never place an exact count over travelling marks. Set two's stable label stays during the final split.
 const changing=apart>0&&apart<1||cancel>0&&cancel<1;
 for(const el of $$('#group-labels .group-label'))el.style.visibility=changing&&!(cancel>0&&el.dataset.group==='set2')?'hidden':'visible';
 $('#scroll-cue').innerHTML=n===4?'Continue to the verdict <span aria-hidden="true">↓</span>':'Scroll to take it apart <span aria-hidden="true">↓</span>';
 updateHalo();
}
function updateHalo(){const p=geometry.find(p=>p.id===point);if(!p)return;const halo=$('#point-halo');halo.style.transform=`translate(${p.x}px,${p.y}px)`;halo.setAttribute('visibility',progress>.34?'visible':'hidden');}
function requestPaint(){if(!queued){queued=true;requestAnimationFrame(paint);}}
function resize(){plotW=art.clientWidth;plotH=art.clientHeight;$('#point-ledger').setAttribute('viewBox',`0 0 ${plotW} ${plotH}`);layouts=[0,1,2,3,4].map(calculate);phase=-1;paint();}
function goToStop(n){n=clamp(n,0,4);if(isReduced()){reduceChapter=n;progress=stops[n];paint();return;}const top=window.scrollY+section.getBoundingClientRect().top+stops[n]*(section.offsetHeight-stage.clientHeight);window.scrollTo({top,behavior:'instant'});requestPaint();}
$$('[data-stop]').forEach(b=>b.addEventListener('click',()=>goToStop(+b.dataset.stop)));
function preference(){const within=section.getBoundingClientRect().top<=1&&section.getBoundingClientRect().bottom>0,current=Math.max(0,phase);reduceChapter=current===0&&isReduced()?4:current;document.body.classList.toggle('motion-reduced',isReduced());$('#motion-setting').setAttribute('aria-pressed',String(override));$('#motion-setting').disabled=motionQuery.matches;$('#motion-setting').textContent=motionQuery.matches?'Motion reduced':override?'Full motion':'Reduce motion';resize();if(isReduced()&&within)window.scrollTo({top:0,behavior:'instant'});else if(!isReduced())goToStop(current);}
$('#motion-setting').addEventListener('click',()=>{override=!override;preference();});motionQuery.addEventListener('change',preference);
window.addEventListener('scroll',requestPaint,{passive:true});let resizeID;window.addEventListener('resize',()=>{clearTimeout(resizeID);resizeID=setTimeout(resize,100);});
window.MarginsCourt=Object.freeze({selectPoint:id=>{point=id;updateHalo();}});
window.marginsCourtSnapshot=()=>({phase,progress,reduced:isReduced(),positions:geometry.map(p=>({...p})),slabTransforms:slabs.map(n=>getComputedStyle(n).transform),records:rows.map(r=>({...r})),groups:groups(phase).map(g=>({name:g.name,ids:g.records.map(r=>r.id),...stats(g.records)}))});
if(motionQuery.matches)preference();else resize();
})();
