/* Three audited point records only. Categories, never tracking coordinates. */
(() => {
  'use strict';
  const $=s=>document.querySelector(s), ns='http://www.w3.org/2000/svg';
  const tokens={
    150:['6+','f3','z38','b3','z29*'],
    154:['6','f39','b38','b29','f29','f29','b38','b28','f18','f39','b39','b37','y1n@'],
    155:['4+','f39w#']
  };
  const names={1:'Djokovic',2:'Medvedev'}, types={f:'Forehand',b:'Backhand',z:'Backhand volley',y:'Backhand drop shot'};
  const endingLabels={150:'Second volley →',154:'Drop shot →',155:'Missed return →'};
  const cases=new Map();
  for(const [id,list] of Object.entries(tokens)){
    const source=window.TACTICAL_DATA.records.find(r=>+r.Pt===+id);
    // Fail closed if the audited shot string, server or pre-point score changes.
    if(!source||source.Svr!=='1'||source.Pts!==({150:'40-AD',154:'AD-40',155:'40-40'})[id]||source['2nd']||list.join('')!==source['1st'].replace(/^c+/,''))continue;
    const shots=list.map((token,i)=>({token,actor:i%2===0?1:2,type:i===0?'First serve':types[token[0]],direction:+token[i===0?0:1],serve:i===0,approach:token.includes('+'),depth:i===1&&!/[@#]/.test(token)&&/[789]/.test(token)?+token.match(/[789]/)[0]:null,error:/[@#]/.test(token)?token.includes('n')?'net':'wide':null,outcome:token.endsWith('*')?'winner':token.endsWith('@')?'unforced error':token.endsWith('#')?'forced error':null}));
    cases.set(+id,{source,shots,let:source['1st'].startsWith('c'),side:+id===155?'deuce':'ad'});
  }
  let point=null, index=0;
  const remembered=new Map();
  function rect(group,attrs,className){const el=document.createElementNS(ns,'rect');for(const [key,value] of Object.entries(attrs))el.setAttribute(key,value);el.setAttribute('class',className);group.append(el);}
  function band(receiver,direction){
    // Three labelled categories OUTSIDE the baseline, not landing lanes.
    // Djokovic's schematic end is left; both players are right-handed.
    const slot=direction===2?1:receiver===1?(direction===3?0:2):(direction===1?0:2);
    return {x:receiver===1?40:568,y:90+slot*(170/3),width:12,height:170/3-4};
  }
  function render(pointer=false){
    const c=cases.get(point);if(!c)return;
    const shot=c.shots[index],receiver=shot.actor===1?2:1,regions=$('#shot-regions'),direction=$('#shot-direction');
    regions.replaceChildren();direction.replaceChildren();
    const facts=[];
    if(shot.serve){
      // An in serve establishes the receiving service box; no landing point is chosen.
      const y=c.side==='ad'?175:90;
      rect(regions,{x:310,y,width:132.5,height:85},'recorded-region serve-region');
      facts.push(`${c.side==='ad'?'Ad':'Deuce'}-court serve ${shot.direction===6?'down the T':'out wide'}.`);
      if(shot.approach)facts.push('Serve-and-volley approach coded.');
    }else{
      for(const d of [1,2,3])rect(direction,band(receiver,d),d===shot.direction?'direction-category is-current':'direction-category');
      const destination=shot.direction===2?'the middle':`${names[receiver]}’s ${shot.direction===1?'forehand':'backhand'} side`;
      facts.push(`${shot.error?'Intended baseline direction':'Baseline direction'}: ${destination}.`);
      if(shot.depth){
        const offset=shot.depth===7?113.5:shot.depth===8?56.75:0;
        const extent=shot.depth===7?132.5:56.75;
        rect(regions,{x:receiver===1?64+offset:556-offset-extent,y:90,width:extent,height:170},'recorded-region depth-region');
        facts.push(shot.depth===9?'Return depth: nearer the baseline than the service line.':shot.depth===8?'Return depth: nearer the service line than the baseline.':'Return depth: inside the service boxes.');
      }
      if(shot.error==='net')rect(regions,{x:305,y:61.5,width:10,height:227},'net-error-region');
      if(shot.outcome)facts.push(shot.outcome==='winner'?'Winner.':`${shot.error==='net'?'Into the net':'Missed wide'} · charted ${shot.outcome}.`);
    }
    $('#shot-title').textContent=`${names[shot.actor]} · ${shot.type.toLowerCase()}${index===1?' return':''}`;
    $('#shot-detail').textContent=facts.join(' ');
    $('#shot-token').textContent=shot.token;
    $('#shot-let').hidden=!(c.let&&index===0);
    $('#shot-position').textContent=`Stroke ${index+1} of ${c.shots.length}`;
    $('#shot-court-title').textContent=`Point ${point}, stroke ${index+1}: ${$('#shot-title').textContent}. ${facts.join(' ')}`;
    $('#shot-court-desc').textContent='Schematic court ends: Djokovic left, Medvedev right. A band outside a baseline marks a direction category, not a landing location. Any shaded return-depth region spans the full court width; it does not combine with the direction band into a bounce estimate. The diagram contains no measured ball or player locations.';
    $('#shot-view').dataset.actor=shot.actor;
    window.playerPortraits?.setHitter(shot.actor,pointer);
    $('#shot-view').dataset.stroke=index;
    $('#shot-view').dataset.error=shot.error||'';
    window.shotSequence.render({point,shots:c.shots,index,select(next,pointer){index=next;render(pointer);}});
    remembered.set(point,index);
    $('#shot-previous').disabled=index===0;$('#shot-next').disabled=index===c.shots.length-1;
    $('#shot-ending').textContent=endingLabels[point];$('#shot-ending').disabled=index===c.shots.length-1;
  }
  function step(delta,event){const c=cases.get(point);if(!c)return;const trigger=document.activeElement;index=Math.max(0,Math.min(c.shots.length-1,index+delta));render(event.detail>0);if(trigger?.disabled)$('#stroke-steps').children[index].focus({preventScroll:true});}
  $('#shot-previous').addEventListener('click',event=>step(-1,event));$('#shot-next').addEventListener('click',event=>step(1,event));
  $('#shot-ending').addEventListener('click',event=>{index=cases.get(point).shots.length-1;render(event.detail>0);$('#stroke-steps').children[index].focus({preventScroll:true});});
  $('#stroke-steps').addEventListener('keydown',event=>{
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();
    if(event.key==='Home')index=0;else if(event.key==='End')index=cases.get(point).shots.length-1;else index=Math.max(0,Math.min(cases.get(point).shots.length-1,index+(event.key==='ArrowRight'?1:-1)));
    render();$('#stroke-steps').children[index].focus({preventScroll:true});
  });
  window.pressureView={
    select(id,context={}){
      const source=window.TACTICAL_DATA.records.find(r=>+r.Pt===id),available=cases.has(id);
      point=id;index=remembered.get(id)||0;
      $('#shot-content').hidden=!available;$('#shot-unavailable').hidden=available;
      $('#shot-ending').hidden=!available;
      $('#shot-view-title').textContent=`Source point ${id} · ${available?'recorded shots':'point record'}`;
      if(available){render();return;}
      delete $('#shot-view').dataset.actor;delete $('#shot-view').dataset.stroke;delete $('#shot-view').dataset.error;
      $('#unavailable-kind').textContent=context.type||'Recorded point';
      $('#unavailable-outcome').textContent=source?`${names[+source.PtWinner]} wins.`:'Record unavailable.';
      $('#unavailable-description').textContent=context.description||'';
      $('#unavailable-first').textContent=source?.['1st']||'(empty)';
      $('#unavailable-second').textContent=source?.['2nd']||'(empty)';
    },
    snapshot(){const c=cases.get(point);return {point,index,source:c?.source['1st'],shots:c?.shots,visible:!$('#shot-content').hidden};}
  };
})();
