import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../journey/combat-arts.js',import.meta.url),'utf8');
const context=vm.createContext({});vm.runInContext(source,context);const rules=context.JourneyCombat;
const plain=v=>JSON.parse(JSON.stringify(v));
test('old saves receive one usable art for each hero without losing learned ranks',()=>{
 const old=rules.sanitize();assert.equal(old.ranks.rhythm,1);assert.equal(old.ranks.verdict,1);
 const next=rules.sanitize({ranks:{recall:2,guard:900,clones:-3},equipped:{wukong:'recall',erlang:'rhythm'}});
 assert.equal(next.ranks.recall,2);assert.equal(next.ranks.guard,3);assert.equal(next.ranks.clones,0);assert.equal(next.equipped.wukong,'recall');assert.equal(next.equipped.erlang,'verdict');
});
test('all six branches are reachable at explicit costs and cap at three ranks',()=>{
 for(const art of rules.ARTS){let state=rules.sanitize(),balance=1000;const initial=state.ranks[art.id];for(let r=initial;r<3;r++){const result=rules.purchase(state,art.id,balance);assert.equal(balance-result.merit,rules.cost(r));assert.equal(result.state.ranks[art.id],r+1);assert.equal(result.state.equipped[art.hero],art.id);state=result.state;balance=result.merit;}assert.equal(rules.purchase(state,art.id,balance),null);}
});
test('unaffordable and malformed purchases cannot spend currency or mutate saves',()=>{
 const state=rules.sanitize(),before=plain(state);for(const amount of [-1,0,11,NaN,Infinity])assert.equal(rules.purchase(state,'recall',amount),null);
 assert.equal(rules.purchase(state,'unknown',100),null);assert.deepEqual(plain(state),before);
});
test('equipping cannot cross hero boundaries or equip an unlearned art',()=>{
 const state=rules.sanitize({ranks:{recall:0,pack:2},equipped:{wukong:'pack',erlang:'clones'}});assert.equal(state.equipped.wukong,'rhythm');assert.equal(state.equipped.erlang,'verdict');
});
test('swept collision catches fast projectiles and returns the first contact',()=>{
 assert.equal(rules.impactTime(0,0,200,0,100,0,10),.45);
 assert.equal(rules.impactTime(0,0,200,0,100,30,10),null);
 assert.equal(rules.impactTime(0,0,0,0,0,0,10),0);
 assert.equal(rules.impactTime(0,0,0,0,30,0,10),null);
 assert.equal(rules.impactTime(0,0,10,0,30,0,10),null);
 assert.equal(rules.impactTime(0,0,200,0,100,10,10),.5);
 assert.ok(rules.impactTime(0,0,200,0,30,0,10)<rules.impactTime(0,0,200,0,100,0,10));
});
test('every main production script still parses with the original embedded assets',()=>{
 const html=fs.readFileSync(new URL('../journey/index.html',import.meta.url),'utf8');
 const main=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('class Player'));
 assert.ok(main);new vm.Script(main);
 assert.ok(main.includes('journeyCombat.melee(this, enemy, finalDmg, pending)'));
 assert.ok(main.includes('combatArts: combatArtsState'));
 const sound=main.slice(main.indexOf('class SoundEngine'),main.indexOf('const sound = new SoundEngine'));
 assert.equal((sound.match(/if \(!this.ctx \|\| this.muted \|\| this.paused \|\| this.volume === 0\) return;/g)||[]).length,13);
 assert.equal((sound.match(/connect\(this.output \|\| this.ctx.destination\)/g)||[]).length,12);
});
