/* Journey combat presentation and specialisations. No account/network access. */
(function (root) {
  'use strict';
  const VERSION = 'v1.1.0';
  const ARTS = Object.freeze([
    { id:'rhythm', hero:'wukong', icon:'☀', color:'#fbbf24', en:'Stone-Sun Rhythm', zh:'石心三叠', enDesc:'Land three separate staff attacks within 4 seconds for a solar finisher. Rank 2 splashes nearby foes; rank 3 restores Qi.', zhDesc:'4 秒内三次棍击命中，第三击引爆烈阳。二重波及附近敌人，三重回复真气。' },
    { id:'recall', hero:'wukong', icon:'↩', color:'#fb923c', en:'Returning Comet', zh:'回天彗棍', enDesc:'Catch a staff that hit an enemy to empower your next melee hit for 3 seconds and restore Qi. Higher ranks strengthen the strike.', zhDesc:'收回命中过敌人的飞棒，3 秒内下一次棍击强化并回复真气。升重提高强化伤害。' },
    { id:'clones', hero:'wukong', icon:'🐒', color:'#a3e635', en:'Monkey Constellation', zh:'群猴星阵', enDesc:'Hair clones launch a homing star each second at nearby foes for 6 seconds. Higher ranks add damage; casting refunds Qi.', zhDesc:'分身在 6 秒内每秒发射追踪星芒攻击附近敌人。升重增加星芒伤害，施法返还真气。' },
    { id:'verdict', hero:'erlang', icon:'👁', color:'#67e8f9', en:'Sealbreaker Verdict', zh:'破印天裁', enDesc:'A spear hit consumes a Third Eye brand for bonus damage. Rank 2 chains a bolt; rank 3 restores Qi.', zhDesc:'枪击消耗天眼烙印造成额外伤害。二重引出连锁雷矢，三重回复真气。' },
    { id:'pack', hero:'erlang', icon:'🐕', color:'#c4b5fd', en:'Hound-and-Spear Pact', zh:'犬枪同心', enDesc:'Command the hound, then strike its target within 3 seconds: pin the foe and recover part of a dodge charge.', zhDesc:'指挥哮天犬后，3 秒内枪击同一目标：定住敌人并回复部分闪避次数。' },
    { id:'guard', hero:'erlang', icon:'◇', color:'#93c5fd', en:'Mirror Thunderstep', zh:'雷遁返镜', enDesc:'For 0.35 seconds after dodging, reflect nearby enemy bolts toward foes. Each rank allows another reflection, up to three.', zhDesc:'闪避后 0.35 秒内，将附近敌方飞弹反射向敌人。每重多反射一枚，最多三枚。' }
  ]);
  const rank = (value) => Math.max(0, Math.min(3, Math.floor(Number(value) || 0)));
  function sanitize(saved) {
    const ranks = {};
    for (const art of ARTS) ranks[art.id] = rank(saved?.ranks?.[art.id]);
    ranks.rhythm = Math.max(1, ranks.rhythm); ranks.verdict = Math.max(1, ranks.verdict);
    const equipped = {};
    for (const hero of ['wukong','erlang']) equipped[hero] = ARTS.find(a => a.hero === hero && a.id === saved?.equipped?.[hero] && ranks[a.id])?.id || (hero === 'wukong' ? 'rhythm' : 'verdict');
    return { ranks, equipped };
  }
  function cost(currentRank) { return [12,24,40][rank(currentRank)] ?? Infinity; }
  function purchase(saved, id, merit) {
    const next = sanitize(saved), art = ARTS.find(a => a.id === id), balance = Number(merit);
    if (!art || !Number.isFinite(balance) || balance < cost(next.ranks[id])) return null;
    const spent = cost(next.ranks[id]); next.ranks[id]++; next.equipped[art.hero] = id;
    return { state: next, merit: balance - spent };
  }
  // Earliest swept-circle impact prevents fast bolts tunnelling through a foe.
  function impactTime(x0,y0,x1,y1,cx,cy,radius) {
    const dx=x1-x0, dy=y1-y0, ox=x0-cx, oy=y0-cy, a=dx*dx+dy*dy, c=ox*ox+oy*oy-radius*radius;
    if (c<=0) return 0;
    if (a<=1e-9) return null;
    const b=2*(ox*dx+oy*dy), disc=b*b-4*a*c;
    if (disc<0) return null;
    const t=(-b-Math.sqrt(disc))/(2*a); return t>=0 && t<=1 ? t : null;
  }
  function install(env) {
    const { Player, Projectile, sound }=env;
    let clock=0, paused=true, previousFocus=null, previousPause=true, open=false;
    let state={ rhythm:0, rhythmTimer:0, recall:0, clones:0, cloneTick:0, guard:0, reflections:0, pact:null, pactTimer:0, pactCredit:0 };
    const game=()=>env.game(), hero=()=>game().playableHero;
    const art=()=>ARTS.find(a=>a.id===env.artState().equipped[hero()]) || ARTS[0];
    const level=()=>env.artState().ranks[art().id] || 1;
    const hostiles=()=>env.enemies().filter(e=>e.alive && !e.isAlly && !e.isDying);
    const nearest=(x,y,range,exclude)=>hostiles().filter(e=>e!==exclude && Math.hypot(e.x-x,e.y-y)<=range).sort((a,b)=>Math.hypot(a.x-x,a.y-y)-Math.hypot(b.x-x,b.y-y))[0];
    const label=a=>game().language==='en'?a.en:a.zh;
    const text=(en,zh)=>game().language==='en'?en:zh;
    function reset(){state={rhythm:0,rhythmTimer:0,recall:0,clones:0,cloneTick:0,guard:0,reflections:0,pact:null,pactTimer:0,pactCredit:0};}
    function cue(target=env.player(), name=label(art())) {
      env.cue(target.x,target.y,art().icon,art().color,name);
      motif(art().id);
    }
    function bolt(from,to,damage,color) {
      if (!to) return;
      const angle=Math.atan2(to.y-from.y,to.x-from.x);
      const p=new Projectile(from.x,from.y,Math.cos(angle)*520,Math.sin(angle)*520,damage,color,false);
      p.journeyHoming=to; p.life=1.6; p.radius=6; env.projectiles().push(p);
    }
    function melee(player, enemy, damage, pending) {
      if (paused) return damage;
      const chosen=art().id, r=level();
      if (chosen==='rhythm' && !pending.journeyArtHit) {
        pending.journeyArtHit=true; state.rhythm++; state.rhythmTimer=4;
        if(state.rhythm>=3){
          state.rhythm=0; damage*=1.25+r*.1; cue(enemy);
          if(r>=2) for(const e of hostiles().filter(e=>e!==enemy && Math.hypot(e.x-enemy.x,e.y-enemy.y)<130).slice(0,3)) e.takeDamage(damage*.20,false,true);
          if(r>=3) player.qi=Math.min(player.maxQi,player.qi+6);
        }
      } else if(chosen==='recall' && state.recall>0){state.recall=0;damage*=1.35+r*.15;cue(enemy);}
      else if(chosen==='verdict' && enemy.judgmentMarkTimer>0){
        enemy.judgmentMarkTimer=0;damage*=1.25+r*.1;cue(enemy);
        if(r>=2) bolt(enemy,nearest(enemy.x,enemy.y,250,enemy),damage*.25,art().color);
        if(r>=3) player.qi=Math.min(player.maxQi,player.qi+5);
      } else if(chosen==='pack' && state.pact===enemy && state.pactTimer>0){
        state.pact=null;state.pactTimer=0;
        if(player.dashCharges<player.maxDashCharges){
          state.pactCredit+=.25*r;
          const earned=Math.floor(state.pactCredit);
          player.dashCharges=Math.min(player.maxDashCharges,player.dashCharges+earned);
          state.pactCredit=player.dashCharges>=player.maxDashCharges?0:state.pactCredit-earned;
        } else state.pactCredit=0;
        enemy.applySlow?.(.4,1+r*.3); if(!enemy.isBoss) enemy.applyStun?.(.3+r*.15);cue(enemy);
      }
      return damage;
    }
    const originalReset=Player.prototype.resetForRun;
    Player.prototype.resetForRun=function(...args){reset();return originalReset.apply(this,args);};
    const originalCatch=Player.prototype.onRuyiCatch;
    Player.prototype.onRuyiCatch=function(source){
      const result=originalCatch.call(this,source);
      if(art().id==='recall' && source.hitCount>0){state.recall=3;this.qi=Math.min(this.maxQi,this.qi+3+level()*2);cue();}
      return result;
    };
    const originalCast=Player.prototype.performCast;
    Player.prototype.performCast=function(...args){
      const before=this.qi, wasTransformed=this.isTransformed, result=originalCast.apply(this,args);
      if(art().id==='clones' && !wasTransformed && this.qi<before){state.clones=6;state.cloneTick=.5;this.qi=Math.min(this.maxQi,this.qi+8+level()*2);cue();}
      return result;
    };
    const originalHound=Player.prototype.resolveXiaotianquanCommand;
    Player.prototype.resolveXiaotianquanCommand=function(...args){
      const result=originalHound.apply(this,args);
      if(art().id==='pack' && this.hound?.commandTarget?.alive){state.pact=this.hound.commandTarget;state.pactTimer=3;cue(state.pact);}
      return result;
    };
    const originalDash=Player.prototype.performDash;
    Player.prototype.performDash=function(...args){
      const before=this.isDashing,result=originalDash.apply(this,args);
      if(!before && this.isDashing && art().id==='guard'){state.guard=.35;state.reflections=level();cue();}
      return result;
    };
    const originalSignature=Player.prototype.triggerSignature;
    Player.prototype.triggerSignature=function(...args){
      const before=this.isTransformed||this.isManifested,result=originalSignature.apply(this,args);
      if(!before && (this.isTransformed||this.isManifested)) motif(this.isTransformed?this.activeTransformationForm:'verdict');
      return result;
    };
    Projectile.prototype.update=function(dt){
      if(!this.alive || dt<=0) return;
      if(this.journeyHoming?.alive){const a=Math.atan2(this.journeyHoming.y-this.y,this.journeyHoming.x-this.x),speed=Math.hypot(this.vx,this.vy);this.vx=Math.cos(a)*speed;this.vy=Math.sin(a)*speed;}
      const x0=this.x,y0=this.y;
      this.x+=this.vx*dt;this.y+=this.vy*dt;this.life-=dt;
      this.journeyTrail=(this.journeyTrail||[]);this.journeyTrail.push([x0,y0]);if(this.journeyTrail.length>6)this.journeyTrail.shift();
      const targets=this.isEnemy?[env.player()]:hostiles(); let first=null, earliest=Infinity;
      for(const target of targets){const t=impactTime(x0,y0,this.x,this.y,target.x,target.y,(target.radius||0)+this.radius);if(t!==null && t<earliest){first=target;earliest=t;}}
      if(first){this.x=x0+(this.x-x0)*earliest;this.y=y0+(this.y-y0)*earliest;this.alive=false;first.takeDamage(this.dmg);}
      if(this.life<=0)this.alive=false;
    };
    const oldProjectileDraw=Projectile.prototype.draw;
    Projectile.prototype.draw=function(ctx){
      if(!this.alive)return;
      ctx.save();ctx.strokeStyle=this.color;ctx.lineWidth=this.isEnemy?3:2;ctx.globalAlpha=.6;
      if(!game().reducedMotion && this.journeyTrail?.length){ctx.beginPath();this.journeyTrail.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.lineTo(this.x,this.y);ctx.stroke();}
      ctx.restore();oldProjectileDraw.call(this,ctx);
      ctx.save();ctx.translate(this.x,this.y);ctx.rotate(Math.atan2(this.vy,this.vx));ctx.strokeStyle=this.isEnemy?'#fff1f2':'#ffffff';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(7,0);ctx.lineTo(-3,-4);ctx.lineTo(-1,0);ctx.lineTo(-3,4);ctx.closePath();ctx.stroke();ctx.restore();
    };
    function tick(dt){
      if(paused)return;clock+=dt;
      for(const key of ['rhythmTimer','recall','clones','guard','pactTimer'])state[key]=Math.max(0,state[key]-dt);
      if(!state.rhythmTimer)state.rhythm=0;
      if(state.clones>0 && art().id==='clones'){
        state.cloneTick-=dt;
        if(state.cloneTick<=0){state.cloneTick=1;const clone=env.clones().find(c=>c.alive),target=clone&&nearest(clone.x,clone.y,500);if(target)bolt(clone,target,(20+level()*12)*(env.player().metaDamageMultiplier||1),art().color);}
      }
      if(state.guard>0 && state.reflections>0 && art().id==='guard'){
        const p=env.player();
        for(const shot of env.projectiles()){
          if(state.reflections<=0)break;
          if(!(shot instanceof Projectile)||!shot.alive||!shot.isEnemy||!Number.isFinite(shot.vx)||!Number.isFinite(shot.vy)||Math.hypot(shot.x-p.x,shot.y-p.y)>85)continue;
          const target=nearest(shot.x,shot.y,1000),angle=target?Math.atan2(target.y-shot.y,target.x-shot.x):Math.atan2(-shot.vy,-shot.vx),speed=Math.max(280,Math.hypot(shot.vx,shot.vy));
          shot.isEnemy=false;shot.vx=Math.cos(angle)*speed;shot.vy=Math.sin(angle)*speed;shot.color=art().color;shot.journeyHoming=target;state.reflections--;p.qi=Math.min(p.maxQi,p.qi+2);motif('guard');
        }
      }
    }
    let audioSettings={volume:.55,muted:false};try{Object.assign(audioSettings,JSON.parse(env.storageGet('journeyAudioV1')||'{}'));}catch{}
    sound.volume=Number.isFinite(Number(audioSettings.volume))?Math.max(0,Math.min(1,Number(audioSettings.volume))):.55;sound.muted=!!audioSettings.muted;sound.paused=true;
    const oldInit=sound.init.bind(sound);
    sound.init=function(){oldInit();if(this.ctx&&!this.output){this.output=this.ctx.createGain();this.output.gain.value=paused||this.muted?0:this.volume;this.output.connect(this.ctx.destination);}};
    function syncAudio(){
      sound.paused=paused||document.hidden;
      if(sound.output){sound.output.gain.cancelScheduledValues(sound.ctx.currentTime);if(sound.paused||sound.muted)sound.output.gain.setValueAtTime(0,sound.ctx.currentTime);else sound.output.gain.setTargetAtTime(sound.volume,sound.ctx.currentTime,.025);}
      for(const id of ['title-audio-btn','pause-audio-btn']){const el=document.getElementById(id);if(el){el.textContent=sound.muted?text('🔇 Sound Off','🔇 音效关闭'):text('🔊 Sound On','🔊 音效开启');el.setAttribute('aria-pressed',String(sound.muted));}}
      for(const slider of document.querySelectorAll('.journey-volume input'))slider.value=String(Math.round(sound.volume*100));
      env.storageSet('journeyAudioV1',JSON.stringify({volume:sound.volume,muted:sound.muted}));
    }
    function toggleMute(){sound.muted=!sound.muted;sound.init();syncAudio();}
    let lastMotif=-10;
    function motif(id){
      if(!sound.ctx||sound.muted||paused||document.hidden||sound.volume===0||clock-lastMotif<.12)return;lastMotif=clock;
      const notes={rhythm:[220,440],recall:[392,784],clones:[523,659],verdict:[740,988],pack:[196,294],guard:[880,587],dragon:[294,587],tiger:[147,220],roc:[784,1047],ape:[82,164],tortoise:[174,349]}[id]||[440,660];
      try{notes.forEach((frequency,i)=>{const o=sound.ctx.createOscillator(),g=sound.ctx.createGain(),t=sound.ctx.currentTime+i*.045;o.type=id==='ape'?'triangle':'sine';o.frequency.setValueAtTime(frequency,t);o.frequency.exponentialRampToValueAtTime(frequency*.65,t+.20);g.gain.setValueAtTime(.12,t);g.gain.exponentialRampToValueAtTime(.001,t+.24);o.connect(g);g.connect(sound.output);o.onended=()=>{o.disconnect();g.disconnect();};o.start(t);o.stop(t+.25);});}catch{}
    }
    function setPaused(value){if(paused!==!!value){paused=!!value;syncAudio();}}
    function atmosphere(ctx){
      const b=game().campaignBiome||0,t=game().reducedMotion?0:clock,palettes=[['#84cc16','#d9f99d'],['#38bdf8','#cffafe'],['#f59e0b','#fef3c7'],['#c084fc','#ede9fe'],['#fb7185','#ffe4e6']],[color,light]=palettes[Math.floor(b/3)%palettes.length];
      ctx.save();ctx.globalAlpha=.075;ctx.fillStyle=color;
      for(let i=0;i<4;i++){const x=-1000+i*620+Math.sin(t*.08+i)*45;ctx.beginPath();ctx.moveTo(x,-900);ctx.lineTo(x+170,-900);ctx.lineTo(x+700,900);ctx.lineTo(x+270,900);ctx.closePath();ctx.fill();}
      ctx.globalAlpha=.45;ctx.fillStyle=light;
      for(let i=0;i<(game().reducedMotion?12:26);i++){const x=((i*389+Math.sin(i*17)*100+t*(7+b%5))%2400)-1200,y=((i*277+t*(b%3===1?-9:4)+18000)%1800)-900;ctx.beginPath();ctx.ellipse(x,y,2+(i%3),b%3===1?4:1.8,t*.1+i,0,Math.PI*2);ctx.fill();}
      ctx.restore();
    }
    function aura(ctx){
      const p=env.player();if(!p.isTransformed&&!p.isManifested)return;
      const form=p.isTransformed?p.activeTransformationForm:'eye',colors={dragon:'#38bdf8',tiger:'#f59e0b',roc:'#fbbf24',ape:'#ea580c',tortoise:'#10b981',eye:'#93c5fd'},sides={dragon:3,tiger:3,roc:5,ape:4,tortoise:6,eye:8};
      ctx.save();ctx.translate(p.x,p.y+8);ctx.scale(1,.44);ctx.rotate(game().reducedMotion?0:clock*.18);ctx.strokeStyle=colors[form];ctx.lineWidth=3;ctx.globalAlpha=.6;const n=sides[form]||6,r=form==='ape'?70:54;ctx.beginPath();for(let i=0;i<=n;i++){const a=i/n*Math.PI*2;i?ctx.lineTo(Math.cos(a)*r,Math.sin(a)*r):ctx.moveTo(r,0);}ctx.stroke();ctx.beginPath();ctx.arc(0,0,r+7,0,Math.PI*2);ctx.stroke();ctx.restore();
    }
    const modal=document.createElement('div');modal.id='journey-combat-modal';modal.setAttribute('role','dialog');modal.setAttribute('aria-modal','true');modal.setAttribute('aria-labelledby','journey-art-title');modal.hidden=true;document.body.append(modal);
    function render(){
      const current=env.artState();modal.innerHTML=`<section class="journey-art-sheet"><header><div><small>${text('HERO COMBAT ARTS','英雄战技')} · ${VERSION}</small><h2 id="journey-art-title">${text(hero()==='erlang'?'Erlang · Heaven’s Pursuit':'Wukong · Stone-Sun Mastery',hero()==='erlang'?'二郎 · 巡天封神':'悟空 · 石心斗战')}</h2></div><button type="button" data-close>${text('Return','返回')}</button></header><p>${text('Equip one art. The first branch starts unlocked; learn the others with Merit. Each branch has three ranks with new tactical effects.','装备一种战技。首支免费开启，其他分支消耗功德学习。每支三重，逐步掌握新的战术。')}</p><strong>${text('Merit','功德')}: ${Math.floor(game().ashes)}</strong><div class="journey-art-grid">${ARTS.filter(a=>a.hero===hero()).map(a=>{const r=current.ranks[a.id],equipped=current.equipped[hero()]===a.id;return `<article style="--art-color:${a.color}" class="${equipped?'equipped':''}"><span class="journey-art-icon">${a.icon}</span><h3>${label(a)}</h3><div class="journey-art-ranks" aria-label="${text('Rank','境界')} ${r} / 3">${[1,2,3].map(n=>`<span class="${r>=n?'learned':''}">${n}</span>`).join('<b>→</b>')}</div><p>${game().language==='en'?a.enDesc:a.zhDesc}</p><button type="button" data-equip="${a.id}" ${!r||equipped?'disabled':''}>${equipped?text('Equipped','已装备'):text('Equip','装备')}</button><button type="button" data-invest="${a.id}" ${r===3||game().ashes<cost(r)?'disabled':''}>${r===3?text('Mastered','已圆满'):text(r?'Advance':'Learn',r?'进阶':'学习')+' · '+cost(r)}</button></article>`;}).join('')}</div></section>`;
      modal.querySelector('[data-close]').onclick=close;
      for(const button of modal.querySelectorAll('[data-equip]'))button.onclick=()=>{const next=sanitize(env.artState());next.equipped[hero()]=button.dataset.equip;env.setArtState(next);reset();env.save();render();modal.querySelector('[data-close]').focus();};
      for(const button of modal.querySelectorAll('[data-invest]'))button.onclick=()=>{const bought=purchase(env.artState(),button.dataset.invest,game().ashes);if(!bought)return;game().ashes=bought.merit;env.setArtState(bought.state);reset();env.save();env.refresh();render();modal.querySelector('[data-close]').focus();};
    }
    function show(){previousFocus=document.activeElement;previousPause=game().isPaused;game().isPaused=true;game().mouse.isDown=false;open=true;render();modal.hidden=false;setPaused(true);modal.querySelector('[data-close]').focus();}
    function close(){modal.hidden=true;open=false;game().isPaused=previousPause;previousFocus?.focus();env.refresh();}
    modal.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();close();}else if(e.key==='Tab'){const items=[...modal.querySelectorAll('button:not(:disabled)')],i=items.indexOf(document.activeElement);if(e.shiftKey&&i<=0){e.preventDefault();items.at(-1)?.focus();}else if(!e.shiftKey&&i===items.length-1){e.preventDefault();items[0]?.focus();}}});
    for(const id of ['training-title-btn','pause-audio-btn']){const base=document.getElementById(id);if(base){const button=document.createElement('button');button.type='button';button.className=base.className;button.dataset.journeyArts='';button.textContent=text('✦ Hero Combat Arts','✦ 英雄战技');button.onclick=show;base.after(button);}}
    for(const id of ['title-audio-btn','pause-audio-btn']){const base=document.getElementById(id);if(base){const label=document.createElement('label');label.className='journey-volume';label.innerHTML=`<span>${text('Sound level','音量')}</span><input type="range" min="0" max="100" value="${Math.round(sound.volume*100)}" aria-label="${text('Sound level','音量')}">`;label.querySelector('input').oninput=e=>{sound.volume=Number(e.target.value)/100;sound.init();syncAudio();};base.after(label);}}
    const badge=document.createElement('div');badge.id='journey-art-status';document.querySelector('.player-bars')?.append(badge);
    function hud(){
      const chosen=art(),suffix=chosen.id==='rhythm'?`${state.rhythm}/3`:chosen.id==='recall'?text(state.recall>0?'Strike ready':'Throw → catch → strike',state.recall>0?'棍击已强化':'飞棒 → 收回 → 棍击'):chosen.id==='clones'?text(state.clones>0?'Stars active':'Cast hair clones',state.clones>0?'星阵生效':'施放分身'):chosen.id==='verdict'?text('Eye brand → spear','天眼烙印 → 枪击'):chosen.id==='pack'?text(state.pactTimer>0?'Strike hound target':'Hound → spear',state.pactTimer>0?'枪击哮天犬目标':'哮天犬 → 枪击'):text(state.guard>0?'Reflecting':'Dodge through bolts',state.guard>0?'反射生效':'闪避接近飞弹');
      badge.textContent=`${chosen.icon} ${label(chosen)} ${level()}/3 · ${suffix}`;badge.style.borderColor=chosen.color;
      for(const button of document.querySelectorAll('[data-journey-arts]'))button.textContent=text('✦ Hero Combat Arts','✦ 英雄战技');
    }
    document.addEventListener('visibilitychange',syncAudio);
    syncAudio();hud();
    return {tick,setPaused,atmosphere,aura,melee,toggleMute,hud,show,close,reset,getState:()=>({...state}),isOpen:()=>open};
  }
  root.JourneyCombat=Object.freeze({VERSION,ARTS,sanitize,cost,purchase,impactTime,install});
})(globalThis);
