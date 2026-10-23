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
const camera=$('#camera'),shadow=$('#floor-shadow'),sceneNote=$('#scene-note'),opening=$('#opening-result'),halo=$('#point-halo'),cue=$('#scroll-cue');
// Inline writes only; this cache never asks the browser to resolve computed layout.
const styles=new WeakMap();
function style(node,key,value){let cache=styles.get(node);if(!cache){cache={};styles.set(node,cache);}if(cache[key]!==value){cache[key]=value;node.style[key]=value;}}
let viewport,pointFrames=[],labelNodes=[],lastProgress=NaN,lastApart=NaN,lastCancel=NaN,artHidden,haloVisible,cueVerdict=false;
const motionQuery=matchMedia('(prefers-reduced-motion: reduce)');
let override=false,progress=0,phase=-1,queued=false,point=1,pointChosen=false,pointScale=1,geometry=[],layouts=[],plotW=0,plotH=0,reduceChapter=0;
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
 object.append(slab);slabs.push(slab);slab.paper=slab.querySelector('.slab-paper');slab.linework=slab.querySelector('.court-linework');
}
const net=document.createElement('div');net.className='court-net';net.innerHTML='<span></span>';object.append(net);$('#net-object').remove();
const marks=new Map(),pointTransforms=new Map(),ledger=$('#point-ledger');
// Equal-size count glyphs. Seams are pictograms, never recorded ball positions.
for(const r of rows){
 const node=document.createElementNS(ns,'g');node.setAttribute('class','point '+(r.winner===2?'dj':'fed'));node.dataset.id=r.id;node.dataset.winner=r.winner;
 const body=document.createElementNS(ns,'circle');body.setAttribute('r','5.5');body.setAttribute('class','ball-body');
 const seam=document.createElementNS(ns,'path');seam.setAttribute('d','M-3.5-3.5Q-1.3 0-3.5 3.5M3.5-3.5Q1.3 0 3.5 3.5');seam.setAttribute('class','ball-seam');if(r.winner===2)seam.setAttribute('transform','rotate(90)');
 node.append(body,seam);ledger.querySelector('#marks').append(node);marks.set(r.id,node);
 const translate=ledger.createSVGTransform(),scale=ledger.createSVGTransform();node.transform.baseVal.appendItem(translate);node.transform.baseVal.appendItem(scale);pointTransforms.set(r.id,{translate,scale});
}
function groups(n){if(n<2)return[1,2,3,4,5].map(s=>({name:'Set '+s,records:rows.filter(r=>r.set===s),filter:'set'+s}));if(n===2)return[{name:'Set two',records:subsets.set2,filter:'set2',accent:true},{name:'Other four sets',records:subsets.other,filter:'other'}];return[{name:'Set two',records:subsets.set2,filter:'set2',accent:true},{name:'Three tiebreaks',records:subsets.tb,filter:'tb'},{name:'Other points in those sets',records:subsets.rest,filter:'rest'}];}
function calculate(n){
 const {mobile,short}=viewport,w=plotW,h=plotH,coords=new Map(),labels=[],gs=groups(n),radius=5.5*pointScale;
 for(let i=0;i<gs.length;i++){
  const g=gs[i],st=stats(g.records),five=n<2,pad=mobile?(five?4:5):16,gap=mobile?4:16;
  let x=0,y=0,width;
  if(five){x=i*w/5;width=w/5-(mobile?4:14);}
  else if(i===0)width=w*(mobile?.35:.28);
  else if(n===2){x=w*(mobile?.43:.36);width=w*(mobile?.57:.64);}
  else if(mobile){x=w*.43;width=w*.57;y=i===1?0:Math.max(h*(short?.385:.40),labels[1].deck.y+labels[1].deck.height+8);}
  else{x=w*(i===1?.36:.71);width=w*.29;}
  const inner=width-pad*2,lane=(inner-gap)/2;
  const header=five?(mobile?(short?124:132):148):(mobile?(i===0?(short?100:122):n===2?144:(short?100:122)):(n===2&&i===1?188:164));
  const columns=p=>Math.max(1,1+Math.floor((lane-radius*2)/p));
  let pitch=mobile?(short?6:7.4):14;
  const minPitch=radius*2+.35,available=h-y-header-radius-2,maxCount=Math.max(st.f,st.d);
  while(pitch>minPitch&&(Math.ceil(maxCount/columns(pitch))-1)*pitch>available)pitch=Math.max(minPitch,pitch-.1);
  const cols=columns(pitch);let bottom=header;
  for(const winner of[1,2])g.records.filter(r=>r.winner===winner).forEach((r,j)=>{
   const py=y+header+Math.floor(j/cols)*pitch;bottom=Math.max(bottom,py-y);
   coords.set(r.id,{x:x+pad+radius+(winner-1)*(lane+gap)+(j%cols)*pitch,y:py});
  });
  const deckHeight=Math.min(h-y,bottom+radius+(mobile?12:24));
  labels.push({...g,...st,x:x+pad,y:y+(mobile?6:10),width:inner,deck:{x,y,width,height:deckHeight}});
 }
 if(n<2){const height=Math.max(...labels.map(g=>g.deck.height));labels.forEach(g=>{g.deck.height=height;});}
 return {coords,labels};
}
function drawLabels(n){
 const holder=$('#group-labels'),focused=holder.contains(document.activeElement)?document.activeElement.dataset.inspectFilter:null;
 holder.replaceChildren();labelNodes=[];
 for(const g of layouts[n].labels){
  const el=document.createElement('div');el.className='group-label'+(g.accent?' accent':'');el.dataset.group=g.filter;el.style.left=g.x+'px';el.style.top=g.y+'px';el.style.width=g.width+'px';
  el.innerHTML=`<button data-inspect-filter="${g.filter}" aria-label="Inspect ${g.name}: ${g.n} points, Federer ${g.f}, Djokovic ${g.d}">${g.name}</button><span class="group-sample">${g.n}/422${n<2?'':' points'}</span><span class="group-margin">${signed(g.f-g.d)}</span><div class="group-counts"><span>F <b>${g.f}</b></span><span>D <b>${g.d}</b></span></div>`;
  holder.append(el);labelNodes.push(el);
 }
 if(focused){const next=holder.querySelector(`[data-inspect-filter="${focused}"]`);(next||$('[data-stop="'+n+'"]')).focus({preventScroll:true});}
}
function setChapter(n){
 if(n===phase)return;phase=n;stage.dataset.phase=n;
 $('#chapter-title').innerHTML=chapters[n].title;$('#chapter-copy').innerHTML=chapters[n].copy;$('#stage-caption').textContent=chapters[n].caption;
 $('#story').classList.toggle('compact',n!==0);
 $$('.chapter-track button').forEach((b,i)=>{if(i===n)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});
 $('#transition-status').textContent=chapters[n].copy.replace(/<[^>]+>/g,' ');
 $('#ledger-desc').textContent=groups(n).map(g=>{const s=stats(g.records);return`${g.name}: ${s.n} of 422, Federer ${s.f}, Djokovic ${s.d}.`;}).join(' ')+' One ball is one recorded point. Green Federer and plum Djokovic stay in labelled lanes. Positions are groups, never shot locations.';
 drawLabels(n===0?1:n);
 const verdict=n===4;if(verdict!==cueVerdict){cue.firstChild.textContent=verdict?'Continue to the verdict ':'Scroll to take it apart ';cueVerdict=verdict;}
}
function paint(){
 queued=false;
 if(!plotW)return;
 // Read scroll position before any writes. Dimensions belong to resize(), never this loop.
 if(!isReduced())progress=clamp((window.scrollY-viewport.top)/viewport.travel);
 else progress=stops[reduceChapter];
 if(progress===lastProgress)return;lastProgress=progress;
 const n=progress<.20?0:progress<.46?1:progress<.73?2:progress<.96?3:4;
 setChapter(n);
 const {w,h,mobile}=viewport;
 const split=smooth((progress-.09)/.23),flat=smooth((progress-.20)/.18),apart=smooth((progress-.43)/.14),cancel=smooth((progress-.71)/.13);
 const sx0=Math.min(w*(mobile?1.03:.69)/850,h*(mobile?.4:.57)/420)*(mobile&&h<650?.7:1),sx1=plotW/850;
 const sx=lerp(sx0,sx1,flat),sy=lerp(sx0,plotH/420,flat);
 const cx=lerp(w*(mobile?.51:.66),viewport.artLeft+plotW/2,flat),cy=lerp(h*(mobile?.60:.62),viewport.artTop+plotH/2,flat);
 style(camera,'transform',`translate3d(${cx-425}px,${cy-210}px,0) scale(${sx},${sy})`);
 style(object,'transform',`rotateX(${lerp(57,0,flat)}deg) rotateZ(${lerp(-25,0,flat)}deg)`);
 // The same group rectangles place labels, records and court fragments.
 // Left-origin transforms remove the old centre-scaling drift.
 let restIndex=0;
 for(let i=0;i<5;i++){
  const selected=i===1,ri=selected?0:restIndex++;
  const first=layouts[1].labels[i].deck,mid=layouts[2].labels[selected?0:1].deck,last=layouts[3].labels[selected?0:ri<2?1:2].deck;
  const rect={};for(const key of['x','y','width','height'])rect[key]=lerp(lerp(first[key],mid[key],apart),last[key],cancel);
  const separated=(i-2)*24*split;
  const tx=lerp(separated,rect.x/plotW*850-i*170,flat),ty=lerp(0,rect.y/plotH*420,flat);
  const scaleX=lerp(1,rect.width/plotW*5,flat),scaleY=lerp(1,rect.height/plotH,flat);
  // At the analytical rest the surfaces lie flush with their exact evidence bounds.
  const z=(selected?24:4)*split*(1-flat);
  style(slabs[i],'transform',`translate3d(${tx}px,${ty}px,${z}px) scale(${scaleX},${scaleY})`);
  style(slabs[i].paper,'opacity',flat);
  style(slabs[i].linework,'opacity',(1-flat)*.88);
 }
 style(net,'opacity',1-smooth((progress-.11)/.15));
 style(shadow,'transform',`translate(20px,40px) rotate(${lerp(-22,0,flat)}deg) scale(${lerp(1,.9,flat)},${lerp(1,.65,flat)})`);style(shadow,'opacity',.24*(1-flat));
 style(sceneNote,'opacity',1-smooth(progress/.15));
 style(opening,'opacity',1-smooth((progress-.12)/.08));style(opening,'pointerEvents',n===0?'auto':'none');
 const visibility=isReduced()?1:smooth((progress-.24)/.12);style(art,'opacity',visibility);
 const hidden=visibility<.5;if(hidden!==artHidden){artHidden=hidden;art.inert=hidden;art.setAttribute('aria-hidden',String(hidden));}
 // Persistent IDs and nodes; skip stationary coordinates, including the held set of 38.
 if(apart!==lastApart||cancel!==lastCancel){
  lastApart=apart;lastCancel=cancel;
  for(const f of pointFrames){
   const held=f.held&&apart===1;
   const x=held?f.mid.x:lerp(lerp(f.first.x,f.mid.x,apart),f.last.x,cancel),y=held?f.mid.y:lerp(lerp(f.first.y,f.mid.y,apart),f.last.y,cancel);
   if(x!==f.position.x||y!==f.position.y){f.position.x=x;f.position.y=y;f.translate.setTranslate(x,y);}
  }
 }
 // Never place an exact count over travelling marks. Set two's stable label stays during the final split.
 const changing=apart>0&&apart<1||cancel>0&&cancel<1;
 for(const el of labelNodes)style(el,'visibility',changing&&!(cancel>0&&el.dataset.group==='set2')?'hidden':'visible');
 updateHalo();
}
function updateHalo(){const p=geometry[point-1];if(!p)return;style(halo,'transform',`translate(${p.x}px,${p.y}px)`);const visible=pointChosen&&progress>.34;if(visible!==haloVisible){haloVisible=visible;halo.setAttribute('visibility',visible?'visible':'hidden');}}
function requestPaint(){if(!queued){queued=true;requestAnimationFrame(paint);}}
function resize(){
 // One read phase per resize/preference change, followed by one write phase.
 const artRect=art.getBoundingClientRect(),stageRect=stage.getBoundingClientRect();plotW=artRect.width;plotH=artRect.height;
 viewport={w:innerWidth,h:stage.clientHeight,mobile:innerWidth<=760,short:innerHeight<740,top:window.scrollY+section.getBoundingClientRect().top,travel:Math.max(1,section.offsetHeight-stage.clientHeight),artLeft:artRect.left-stageRect.left,artTop:artRect.top-stageRect.top};
 pointScale=viewport.mobile?(viewport.short?.45:.55):(viewport.w<=1050?(viewport.short?.59:.7):(viewport.short||viewport.w<=1400?.85:1));
 layouts=[0,1,2,3,4].map(calculate);
 geometry=rows.map(r=>({id:r.id,x:NaN,y:NaN}));
 pointFrames=rows.map((r,i)=>({held:r.set===2,translate:pointTransforms.get(r.id).translate,position:geometry[i],first:layouts[1].coords.get(r.id),mid:layouts[2].coords.get(r.id),last:layouts[3].coords.get(r.id)}));
 for(const {scale} of pointTransforms.values())scale.setScale(pointScale,pointScale);
 ledger.setAttribute('viewBox',`0 0 ${plotW} ${plotH}`);
 lastProgress=lastApart=lastCancel=NaN;phase=-1;paint();
}
function goToStop(n){if(resizeID){clearTimeout(resizeID);resizeID=null;resize();}n=clamp(n,0,4);if(isReduced()){reduceChapter=n;progress=stops[n];paint();return;}const top=viewport.top+stops[n]*viewport.travel;window.scrollTo({top,behavior:'instant'});requestPaint();}
$$('[data-stop]').forEach(b=>b.addEventListener('click',()=>goToStop(+b.dataset.stop)));
function preference(){const within=section.getBoundingClientRect().top<=1&&section.getBoundingClientRect().bottom>0,current=Math.max(0,phase);reduceChapter=current===0&&isReduced()?4:current;document.body.classList.toggle('motion-reduced',isReduced());$('#motion-setting').setAttribute('aria-pressed',String(override));$('#motion-setting').disabled=motionQuery.matches;$('#motion-setting').textContent=motionQuery.matches?'Motion reduced':override?'Full motion':'Reduce motion';resize();if(isReduced()&&within)window.scrollTo({top:0,behavior:'instant'});else if(!isReduced())goToStop(current);}
$('#motion-setting').addEventListener('click',()=>{override=!override;preference();});motionQuery.addEventListener('change',preference);
window.addEventListener('scroll',requestPaint,{passive:true});let resizeID;window.addEventListener('resize',()=>{clearTimeout(resizeID);resizeID=setTimeout(()=>{resizeID=null;resize();},100);});
window.MarginsCourt=Object.freeze({selectPoint:(id,chosen=true)=>{point=id;pointChosen=chosen;updateHalo();}});
window.marginsCourtSnapshot=()=>({phase,progress,reduced:isReduced(),pointScale,positions:geometry.map(p=>({...p})),slabTransforms:slabs.map(n=>getComputedStyle(n).transform),records:rows.map(r=>({...r})),groups:groups(phase).map(g=>({name:g.name,ids:g.records.map(r=>r.id),...stats(g.records)}))});
if(motionQuery.matches)preference();else resize();
})();
