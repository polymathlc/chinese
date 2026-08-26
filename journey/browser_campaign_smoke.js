const fs = require('fs');

async function main() {
  const pages = await (await fetch('http://127.0.0.1:9224/json')).json();
  const page = pages.find(item => item.type === 'page' && item.url.endsWith('/index.html'));
  if (!page) throw new Error('Campaign page not found on Edge debugging port 9224');

  const socket = new WebSocket(page.webSocketDebuggerUrl);
  const pending = new Map();
  const browserErrors = [];
  let nextId = 1;

  socket.onmessage = event => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) reject(new Error(message.error.message));
      else resolve(message.result);
    } else if (message.method === 'Runtime.exceptionThrown') {
      browserErrors.push(message.params.exceptionDetails.text);
    } else if (message.method === 'Runtime.consoleAPICalled' && message.params.type === 'error') {
      browserErrors.push(message.params.args.map(arg => arg.value || arg.description || '').join(' '));
    }
  };

  await new Promise((resolve, reject) => {
    socket.onopen = resolve;
    socket.onerror = reject;
  });

  const command = (method, params = {}) => new Promise((resolve, reject) => {
    const id = nextId++;
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
  const evaluate = async expression => {
    const result = await command('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
    return result.result.value;
  };
  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
  const screenshot = async filename => {
    const result = await command('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
    fs.writeFileSync(filename, Buffer.from(result.data, 'base64'));
  };

  await command('Runtime.enable');
  await command('Page.enable');
  await command('Page.reload', { ignoreCache: true });
  await wait(1600);

  await evaluate('startNewRun(); true');
  await wait(700);
  const chapterOne = await evaluate(`({
    chapter: gameState.chamberIndex,
    biome: gameState.campaignBiome,
    title: document.getElementById('chamber-name').innerText,
    weapon: document.getElementById('weapon-style-title').innerText,
    enemies: enemies.map(enemy => enemy.typeKey),
    hp: player.hp
  })`);
  await screenshot('campaign_chapter1_playtest.png');

  const monkeyBoss = await evaluate(`(() => {
    closeAllOverlays(); gameState.isPaused = false; startChamber(5);
    return { dialogue: getComputedStyle(document.getElementById('boss-dialogue-modal')).display, boss: enemies.find(e => e.isBoss)?.typeKey };
  })()`);

  const doctrine = await evaluate(`(() => {
    closeAllOverlays(); gameState.isPaused = false; startChamber(6); skipBossDialogue();
    const choiceVisible = getComputedStyle(document.getElementById('transformation-choice-modal')).display;
    chooseTransformationDoctrine('72');
    return { choiceVisible, selected: gameState.transformationDoctrine, ashes: gameState.ashes };
  })()`);

  const ruyi = await evaluate(`(() => {
    closeAllOverlays(); gameState.isPaused = false; startChamber(18);
    enemies.filter(e => e.isBoss).forEach(e => { e.alive = false; e.isDying = false; });
    checkChamberClear();
    return { acquired: gameState.ruyiAcquired, playerFlag: player.hasRuyiStaff, weapon: document.getElementById('weapon-style-title').innerText };
  })()`);

  const buddha = await evaluate(`(() => {
    closeAllOverlays(); gameState.isPaused = false; startChamber(32); skipBossDialogue();
    const boss = enemies.find(e => e.typeKey === 'campaign_buddha');
    boss.takeDamage(boss.maxHp * 0.51, true, true);
    const result = { imprisoned: gameState.buddhaImprisoned, modal: getComputedStyle(document.getElementById('buddha-modal')).display, hpRatio: boss.hp / boss.maxHp };
    closeBuddhaApprovalCutscene();
    result.nextChapter = gameState.chamberIndex;
    result.tangDialogue = getComputedStyle(document.getElementById('boss-dialogue-modal')).display;
    return result;
  })()`);

  const finale = await evaluate(`(() => {
    closeAllOverlays(); gameState.isPaused = false; startChamber(65);
    return { biome: gameState.campaignBiome, boss: enemies.find(e => e.isBoss)?.typeKey, dialogue: getComputedStyle(document.getElementById('boss-dialogue-modal')).display };
  })()`);
  await wait(300);
  await screenshot('campaign_chapter65_playtest.png');
  await evaluate('skipBossDialogue(); true');
  await wait(500);
  await screenshot('campaign_chapter65_combat_playtest.png');

  console.log(JSON.stringify({ chapterOne, monkeyBoss, doctrine, ruyi, buddha, finale, browserErrors }, null, 2));
  socket.close();
  if (browserErrors.length) process.exitCode = 2;
}

main().catch(error => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
