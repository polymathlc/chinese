// Regression tests for THE BETWEEN-ROUNDS QUESTION GATE in journey/index.html.
// Run with:
//     node tools/journey-quiz-tests.mjs            all cases
//     node tools/journey-quiz-tests.mjs <name>     one case
//
// It loads the REAL filter and the REAL draw out of journey/index.html — the
// game is one 48 MB file, so the harness cuts the two windows it needs rather
// than importing anything — and runs them over synthetic questions.
//
// EVERY FAILURE HERE IS SILENT. The gate opens, the card paints, the student
// answers something, and the run carries on:
//
//  • THE ALLOWLIST IS THE WHOLE FEATURE. Loosen it and a student standing in a
//    doorway with a horde on the other side is handed a comprehension passage,
//    an editing passage or a 200-word cloze — which is exactly the thing this
//    gate was asked never to do. Tighten it past the real bank and the gate
//    silently stops using the teacher's questions at all and quietly runs on
//    its built-in set for ever, with a card that still says where each
//    question came from and a teacher who never looks at it.
//  • AN UNTICKED MCQ MUST NEVER BE SERVED. Guessing which option is right
//    marks a whole class against a word nobody chose, on a card that reads
//    perfectly.
//  • THE ROUND MUST NEVER REPEAT ITSELF, AND MUST NEVER RUN DRY. A 100-chapter
//    run asks 300 questions; a draw that cannot serve past the bank's own size
//    stops asking half way through and the gate turns back into a doorway.
//  • THE BUILT-IN SET IS THE FALLBACK EVERYTHING RESTS ON, so a row with a
//    correct index off the end of its options, or two identical options, is a
//    question that cannot be answered right.
import fs from 'fs';

const GAME = new URL('../journey/index.html', import.meta.url).pathname;
const src = fs.readFileSync(GAME, 'utf8');

const cut = (from, to, what) => {
  const a = src.indexOf(from);
  if (a < 0) throw new Error(what + ': "' + from + '" not found in journey/index.html');
  const b = src.indexOf(to, a + from.length);
  if (b < 0) throw new Error(what + ': end marker "' + to + '" not found');
  return src.slice(a, b);
};

// ---------------------------------------------------------------- the filter
// `plain` is the browser's own tag stripping, which a harness has no DOM for.
// The shim below is a stand-in for it: what these cases pin is the ALLOWLIST —
// which blocks may reach a student — not how a <p> is unwrapped.
const DOM_SHIM = `
const document = {
  createElement: () => ({
    _t: '',
    set innerHTML(v) {
      this._t = String(v)
        .replace(/<[^>]*>/g, ' ')
        .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<').replace(/&gt;/g, '>');
    },
    get textContent() { return this._t; }
  })
};
`;
const filterBlock = cut('    const MAX_STEM', '    // ---- THE ATTEMPT LOG', 'filter');
const raw = new Function(DOM_SHIM + filterBlock + '\nreturn { quizUsable, plain, MAX_STEM, MAX_OPTION, IGNORED_BLOCKS, PASSAGE_TOPIC_RE, PASSAGE_STEM_RE };')();
// A refusal comes back as { no: '<reason>' } so the bank load can report what
// disqualified a bank rather than leaving a teacher to guess. `usable` is the
// question or null; `why` is the reason it was refused.
const F = {
  ...raw,
  usable: q => { const v = raw.quizUsable(q); return (v && v.stem !== undefined) ? v : null; },
  why:    q => { const v = raw.quizUsable(q); return (v && v.no) || ''; }
};

// ---------------------------------------------------------------- the draw
const GAME_SHIM = `
const window = { JourneyBank: null };
const uiText = (zh, en) => en;
`;
const drawBlock = cut('    const JQ_PER_GATE', '    const JQ_STYLE', 'draw');
const bonusBlock = cut('    function jqTakeBonusRanks()', '\n    // A boon or a peach rank', 'bonus');
const G = new Function(GAME_SHIM + drawBlock + bonusBlock + `
return {
  JQ_PER_GATE, JQ_HEAL, JQ_SHOP_GOLD, JQ_HEART_HP, JQ_ASHES, JQ_BUILTIN,
  jqDraw, jqBuiltinQuestion, jqSourceTag, jqTakeBonusRanks,
  setBank(list) { window.JourneyBank = { state: 'ready', questions: list }; },
  noBank() { window.JourneyBank = null; },
  forget() { jqAskedIds = []; },
  asked() { return jqAskedIds.slice(); },
  setBonus(n) { jqBonusRanks = n; }
};`)();

// ---------------------------------------------------------------- harness
let pass = 0, fail = 0;
const only = process.argv[2];
// Some cases are async (the gate WAITS, which is the point of it), so every
// case is queued and awaited in order rather than run inline.
const queue = [];
const section = title => queue.push(async () => console.log(title));
function test(name, fn) {
  if (only && !name.includes(only)) return;
  queue.push(async () => {
    try { await fn(); console.log('  ✅ ' + name); pass++; }
    catch (e) { console.log('  ❌ ' + name + '\n     ' + e.message); fail++; }
  });
}
const eq = (a, b, m) => { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error((m || '') + ' expected ' + JSON.stringify(b) + ', got ' + JSON.stringify(a)); };
const ok = (v, m) => { if (!v) throw new Error(m || 'expected truthy'); };

const mcq = (over = {}) => ({
  id: 'm1', type: 'mcq',
  options: [{ id: 'o1', text: 'go' }, { id: 'o2', text: 'goes' }, { id: 'o3', text: 'going' }],
  correctId: 'o2', ...over
});
const shortQ = (over = {}) => ({
  id: 'q1', title: 'Present tense', topic: 'Grammar',
  blocks: [{ id: 't1', type: 'text', content: '<p>She ______ to school every morning.</p>' }, mcq()],
  ...over
});

section('\nTHE ALLOWLIST — what may be asked at a gate');

test('a short wording + one MCQ is usable', () => {
  const q = F.usable(shortQ());
  ok(q, 'a plain short MCQ must be usable');
  eq(q.stem, 'She ______ to school every morning.');
  eq(q.options.length, 3);
  eq(q.correctId, 'o2');
  eq(q.fromBank, true);
});

for (const type of ['clozebank', 'clozeopen', 'clozemcq', 'editpassage', 'wordmatch', 'synthesis',
                    'fillblank', 'plainanswer', 'answer', 'table', 'openLines', 'workingSpace']) {
  test('a ' + type + ' block is refused', () => {
    ok(!F.usable(shortQ({
      blocks: [{ id: 't1', type: 'text', content: '<p>Read the passage.</p>' }, { id: 'p1', type }, mcq()]
    })), type + ' reached a student standing in a doorway');
    eq(F.why(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>x</p>' }, { id: 'p1', type }, mcq()] })), type,
       'the refusal must NAME the block, or a teacher cannot tell why their bank is not being used');
  });
}

// The block types the portal itself hides inside a question a student is
// answering. Refusing a question for carrying one of these is what kept most
// of a real bank out of the gate: the portal's AI writes an explanation onto
// very nearly every question it builds.
for (const type of ['explanation', 'widget', 'answerKey', 'pageBreak', 'video', 'commonMistake', 'studentAnswer']) {
  test('a ' + type + ' block does NOT disqualify an otherwise short question', () => {
    const q = F.usable(shortQ({
      blocks: [{ id: 't1', type: 'text', content: '<p>She ______ to school.</p>' }, mcq(), { id: 'x1', type }]
    }));
    ok(q, 'a question carrying a ' + type + ' block is still an ordinary short MCQ');
    eq(q.stem, 'She ______ to school.');
  });
}

test('the ignored list is the portal\'s own "hidden inside the question" set', () => {
  ['explanation', 'widget', 'answerKey', 'pageBreak'].forEach(t =>
    ok(F.IGNORED_BLOCKS.includes(t), t + ' fell off the ignored list'));
});

test('a passage set — several MCQs in one question — is refused', () => {
  const q = shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>Read the passage below.</p>' }, mcq(), mcq({ id: 'm2' })] });
  ok(!F.usable(q), 'a comprehension set is exactly what must not be asked here');
  eq(F.why(q), 'passage-set');
});

test('a question with NO mcq at all is refused', () => {
  ok(!F.usable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>Explain why.</p>' }] })));
});

test('a question with lettered parts is refused', () => {
  const q = shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>(a) Which word fits?</p>', part: 'a' }, mcq()] });
  ok(!F.usable(q), 'a stem that only makes sense beside its other parts');
  eq(F.why(q), 'has-parts');
});

test('an UNTICKED mcq is refused — the gate never guesses which is right', () => {
  const q = shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>Q</p>' }, mcq({ correctId: null })] });
  ok(!F.usable(q));
  eq(F.why(q), 'unticked');
});

test('a correctId naming no option is refused', () => {
  ok(!F.usable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>Q</p>' }, mcq({ correctId: 'nope' })] })));
});

test('a stem longer than the cap is refused', () => {
  const long = 'word '.repeat(80);
  ok(!F.usable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>' + long + '</p>' }, mcq()] })));
});

test('a stem exactly at the cap is still usable', () => {
  const at = 'a'.repeat(F.MAX_STEM);
  ok(F.usable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>' + at + '</p>' }, mcq()] })));
});

test('an option longer than the cap is refused', () => {
  ok(!F.usable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Q</p>' },
             mcq({ options: [{ id: 'o1', text: 'a'.repeat(F.MAX_OPTION + 1) }, { id: 'o2', text: 'b' }], correctId: 'o2' })]
  })));
});

test('a question with ONE picture keeps it, so the figure reaches the card', () => {
  const fromBlock = F.usable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Look at the picture and choose.</p>' },
             { id: 'i1', type: 'image', url: 'https://example.test/fig.png' }, mcq()]
  }));
  ok(fromBlock, 'an image block must not disqualify a short question');
  eq(fromBlock.picture, 'https://example.test/fig.png');

  const pasted = F.usable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Look <img src="https://example.test/in.png"> and choose.</p>' }, mcq()]
  }));
  ok(pasted, 'a picture pasted into the wording must not disqualify it either');
  eq(pasted.picture, 'https://example.test/in.png');
});

test('a question with SEVERAL pictures is refused — that is a figure study', () => {
  ok(!F.usable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Compare them.</p>' },
             { id: 'i1', type: 'image', url: 'a.png' }, { id: 'i2', type: 'image', url: 'b.png' }, mcq()]
  })));
  eq(F.why(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Compare.</p>' },
             { id: 'i1', type: 'image', url: 'a.png' }, { id: 'i2', type: 'image', url: 'b.png' }, mcq()]
  })), 'many-pictures');
});

test('a picture with no wording at all is still a question', () => {
  const q = F.usable({ id: 'q', blocks: [{ id: 'i1', type: 'image', url: 'fig.png' }, mcq()] });
  ok(q, 'the figure IS the question on a diagram MCQ');
  eq(q.picture, 'fig.png');
});

test('an annotation question is refused', () => {
  ok(!F.usable(shortQ({ annotation: true })));
});

test('a question with fewer than two options is refused', () => {
  ok(!F.usable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Q</p>' }, mcq({ options: [{ id: 'o1', text: 'only' }], correctId: 'o1' })]
  })));
});

test('no wording AND no picture is refused', () => {
  ok(!F.usable({ id: 'q', blocks: [mcq()] }), 'four options and nothing asking anything');
  eq(F.why({ id: 'q', blocks: [mcq()] }), 'no-wording');
});

test('an empty / malformed question is refused rather than thrown on', () => {
  ok(!F.usable(null));
  ok(!F.usable({}));
  ok(!F.usable({ blocks: [] }));
  ok(!F.usable({ blocks: 'not an array' }));
});

test('the wording comes back as PLAIN text, markup gone', () => {
  const q = F.usable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Choose the <strong>correct</strong> word.</p>' }, mcq()]
  }));
  ok(!/[<>]/.test(q.stem), 'markup reached the card: ' + q.stem);
});

section('\nNO COMPREHENSION QUESTIONS — the passage is never on the card');

// A comprehension MCQ passes every block test: one text block, one MCQ, no
// parts. Its passage is somewhere else, so what reaches a student is
// "According to the passage, why did…" with nothing to answer it from. This
// is the leak the user reported, and it is refused twice over — by what the
// question is FILED as, and by what it SAYS.

for (const topic of [
  'Comprehension MCQ', 'Comprehension: Inference', 'Comprehension (Open-ended)',
  'Comprehension Cloze', 'Vocabulary Cloze', 'Grammar Cloze', 'Visual Text Comprehension',
  'Listening Comprehension', 'Oral: Reading Aloud',
  '阅读理解（选择题） Comprehension MCQ', '阅读理解（问答题） Comprehension Open-ended',
  '短文填空 Cloze Passage', '听力理解 Listening Comprehension', '口试：朗读 Oral: Reading Aloud'
]) {
  test('a question filed under "' + topic + '" is refused', () => {
    const q = shortQ({ topic });
    ok(!F.usable(q), 'a comprehension question reached a student mid-battle');
    eq(F.why(q), 'comprehension-topic');
  });
}

test('the SECOND topic field is read too', () => {
  eq(F.why(shortQ({ topic: 'Grammar', topic2: 'Comprehension: Inference' })), 'comprehension-topic');
});

test('a TITLE off a comprehension paper is read too', () => {
  eq(F.why(shortQ({ topic: 'Grammar', title: 'Comprehension Passage 2 — Q17' })), 'comprehension-topic');
});

test('a tag is read too', () => {
  eq(F.why(shortQ({ topic: 'Grammar', tags: ['past-paper', '阅读理解'] })), 'comprehension-topic');
});

for (const topic of [
  'Grammar', 'Vocabulary', 'Punctuation and Spelling', 'Synthesis and Transformation',
  'Editing for Spelling and Grammar',
  '汉语拼音 Hanyu Pinyin', '词语运用 Vocabulary in Use', '成语与谚语 Idioms & Proverbs',
  '关联词 Connectives', '完成句子 Sentence Completion', '病句修改 Correcting Sentences',
  '量词与搭配 Measure Words & Collocation', '标点符号 Punctuation'
]) {
  test('a question filed under "' + topic + '" is still asked', () => {
    ok(F.usable(shortQ({ topic })), 'the gate just lost a whole topic of perfectly good questions');
  });
}

for (const stem of [
  'According to the passage, why was the boy late?',
  'In the passage, what does the word "reluctant" mean?',
  'What does the author suggest in paragraph 3?',
  'From the extract, how did the writer feel?',
  'Which word best describes the narrator?',
  'Read line 4. What is the effect?',
  '文中的“衬衫”指的是什么？',
  '根据短文，作者为什么没有时间？',
  '本文主要讲述了什么？',
  '第二段中的“它”指的是谁？',
  '作者的父亲做什么工作？'
]) {
  test('a stem that points at a passage is refused: "' + stem.slice(0, 34) + '…"', () => {
    const q = shortQ({ topic: 'Grammar', blocks: [{ id: 't1', type: 'text', content: '<p>' + stem + '</p>' }, mcq()] });
    ok(!F.usable(q), 'the passage it points at is not on the card');
    eq(F.why(q), 'needs-a-passage');
  });
}

for (const stem of [
  'She ______ to school every morning.',
  'Which word is a noun?',
  'Choose the correct connective: He was tired, ______ he kept running.',
  '“开心”的近义词是：',
  '下列哪个词语的写法是正确的？',
  '一（　）书',
  '“衬衫”的汉语拼音是：'
]) {
  test('an ordinary one-line question is still asked: "' + stem.slice(0, 30) + '…"', () => {
    ok(F.usable(shortQ({ topic: 'Grammar', blocks: [{ id: 't1', type: 'text', content: '<p>' + stem + '</p>' }, mcq()] })),
       'the passage rule ate an ordinary question');
  });
}

test('an OPTION may say "the author" — only the stem is checked', () => {
  ok(F.usable(shortQ({
    topic: 'Vocabulary',
    blocks: [{ id: 't1', type: 'text', content: '<p>Who wrote the book?</p>' },
             mcq({ options: [{ id: 'o1', text: 'the author' }, { id: 'o2', text: 'the printer' }], correctId: 'o1' })]
  })), 'a perfectly ordinary answer was read as a passage reference');
});

test('NO BUILT-IN QUESTION trips either rule', () => {
  // The built-in set is the fallback everything rests on. If the passage rules
  // ate half of it the gate would quietly run short on the very days the bank
  // cannot be read.
  G.JQ_BUILTIN.forEach((row, i) => {
    ok(!F.PASSAGE_STEM_RE.test(row[0]), 'built-in row ' + i + ' reads as a passage question: ' + row[0]);
  });
});

section('\nTHE DRAW — which questions a round is built from');

const bankOf = n => Array.from({ length: n }, (_, i) => ({
  id: 'bank' + i, title: 't', stem: 'stem ' + i, fromBank: true,
  options: [{ id: 'a', text: 'a' }, { id: 'b', text: 'b' }], correctId: 'a'
}));

test('a full bank fills the whole round from the bank', () => {
  G.forget(); G.setBank(bankOf(20));
  const round = G.jqDraw(3);
  eq(round.length, 3);
  ok(round.every(q => q.fromBank), 'the teacher\'s own questions must win');
});

test('a short bank is TOPPED UP from the built-in set, never left short', () => {
  G.forget(); G.setBank(bankOf(1));
  const round = G.jqDraw(3);
  eq(round.length, 3, 'a round must always be three questions');
  eq(round.filter(q => q.fromBank).length, 1);
  eq(round.filter(q => !q.fromBank).length, 2);
});

test('no bank at all still fills the round from the built-in set', () => {
  G.forget(); G.noBank();
  const round = G.jqDraw(3);
  eq(round.length, 3);
  ok(round.every(q => !q.fromBank));
});

test('an empty bank falls through to the built-in set', () => {
  G.forget(); G.setBank([]);
  eq(G.jqDraw(3).length, 3);
});

test('a round never asks the same question twice', () => {
  G.forget(); G.setBank(bankOf(40));
  for (let i = 0; i < 30; i++) {
    const ids = G.jqDraw(3).map(q => q.id);
    eq(new Set(ids).size, 3, 'round ' + i + ' repeated a question: ' + ids);
  }
});

test('a long run keeps asking after every question has been seen once', () => {
  G.forget(); G.setBank(bankOf(4));
  for (let i = 0; i < 100; i++) eq(G.jqDraw(3).length, 3, 'the gate ran dry at round ' + i);
});

test('fresh questions are preferred over ones already asked', () => {
  G.forget(); G.setBank(bankOf(6));
  const first = G.jqDraw(3).map(q => q.id);
  const second = G.jqDraw(3).map(q => q.id);
  eq(first.filter(id => second.includes(id)).length, 0, 'the second round re-asked a fresh bank');
});

test('the asked list is capped, so a 100-chapter run cannot grow it for ever', () => {
  G.forget(); G.setBank(bankOf(500));
  for (let i = 0; i < 200; i++) G.jqDraw(3);
  ok(G.asked().length <= 400, 'asked list grew to ' + G.asked().length);
});

test('a card SAYS which of the two a question came from', () => {
  const bank = G.jqSourceTag({ fromBank: true });
  const own = G.jqSourceTag({ fromBank: false });
  ok(bank !== own, 'a student told these are their teacher\'s questions when they are not');
  ok(/bank/i.test(bank) && /practice/i.test(own));
});

section('\nTHE WAIT — the gate holds for the teacher’s bank before it asks its own');

// `jqWaitForBank` is the fix for the bug this whole feature had: the first
// chamber is cleared long before four CDN imports, a sign-in and a whole bank
// read have finished, so a gate that drew the instant it was touched served
// the BUILT-IN set every time and the teacher's questions were never asked.
const waitBlock = cut('    const JQ_BANK_WAIT', '    function jqRenderWaiting', 'wait');
function waiter(bank) {
  const calls = { began: 0, waiting: 0 };
  const env = new Function('bank', 'calls', `
    const window = { JourneyBank: bank, setTimeout, clearTimeout };
    let jqBusy = false, jqSession = null, jqShadow = {};
    const beginRewardSelectionPause = () => {};
    const jqCloseCard = () => {};
    const jqGrantGate = () => {};
    const jqBindKeys = () => {};
    const jqRenderQuestion = () => {};
    const jqDraw = () => [{ id: 'x' }];
    const jqRenderWaiting = () => { calls.waiting++; };
    const jqRenderSignIn = () => {};
    const jqEl = () => ({ appendChild(){}, });
    const jqSetText = () => {};
    const uiText = (zh, en) => en;
    const document = { getElementById: () => ({ style: {} }) };
    ` + waitBlock.replace('function jqBegin(gate) {', 'function jqBegin(gate) { calls.began++; return;') + `
    return { jqWaitForBank, JQ_BANK_WAIT };
  `)(bank, calls);
  return { env, calls };
}

test('a bank still loading is WAITED for — the gate does not draw yet', async () => {
  let settle;
  const bank = { state: 'loading', ready: new Promise(r => { settle = r; }) };
  const { env, calls } = waiter(bank);
  env.jqWaitForBank({});
  eq(calls.began, 0, 'the gate drew before the bank had landed — the exact bug');
  eq(calls.waiting, 1, 'and it said nothing while it waited');
  settle();
  await new Promise(r => setTimeout(r, 5));
  eq(calls.began, 1, 'the gate never opened once the bank landed');
});

test('a bank that is already ready draws at once, with no waiting card', async () => {
  const { env, calls } = waiter({ state: 'ready', ready: Promise.resolve() });
  env.jqWaitForBank({});
  eq(calls.began, 1);
  eq(calls.waiting, 0, 'a pointless "fetching…" flash on every gate of a hundred');
});

test('a bank that never settles still opens the gate — it is bounded', () => {
  ok(Number.isFinite(waiter({ state: 'loading', ready: new Promise(() => {}) }).env.JQ_BANK_WAIT),
     'a gate that can never open is worse than one asking its own questions');
  ok(waiter({ state: 'loading', ready: new Promise(() => {}) }).env.JQ_BANK_WAIT <= 20000,
     'a student cannot stand in a doorway for that long');
});

test('a REJECTED bank promise still opens the gate', async () => {
  const bank = { state: 'loading', ready: Promise.reject(new Error('nope')) };
  bank.ready.catch(() => {});
  const { env, calls } = waiter(bank);
  env.jqWaitForBank({});
  await new Promise(r => setTimeout(r, 5));
  eq(calls.began, 1, 'a failed bank read left the run frozen on an empty card');
});

test('no bank object at all still opens the gate', () => {
  const { env, calls } = waiter(null);
  env.jqWaitForBank({});
  eq(calls.began, 1);
});

test('the promise the gate waits on is SETTLED on every terminal state', () => {
  ok(/BANK\.ready = new Promise/.test(src), 'the gate has nothing to wait on');
  const settles = (src.match(/announce\(\); done\(\);/g) || []).length;
  ok(settles >= 3, 'only ' + settles + ' terminal states settle it — a gate waits ' +
     'the full timeout on every single chamber for the rest of the run');
});

section('\nWHAT REACHES THE LEADERBOARD');

// `jqPublishRound` is the only thing that writes a row to the board, and the
// board has a voucher on it. Its one rule is that the BUILT-IN questions do not
// count: two dozen questions a student meets over and over would turn a board
// meant to measure work into one that measures how long a tab was left open.
const pubBlock = cut('    function jqPublishRound', '    const JQ_TIERS', 'publish');
function publisher() {
  const sent = [];
  const env = new Function('sent', `
    const gameState = { chamberIndex: 7 };
    const window = { JourneyBank: { publishBoard: v => sent.push(v) } };
    ${pubBlock}
    return jqPublishRound;
  `)(sent);
  return { publish: env, sent };
}
const session = (rows, results) => ({ questions: rows, results });

test('a round of bank questions is published, with the chapter', () => {
  const { publish, sent } = publisher();
  publish(session([{ id: 'a', fromBank: true }, { id: 'b', fromBank: true }, { id: 'c', fromBank: true }],
                  [true, false, true]));
  eq(sent, [{ correct: 2, answered: 3, chapter: 7 }]);
});

test('BUILT-IN questions never reach the board', () => {
  const { publish, sent } = publisher();
  publish(session([{ id: 'a', fromBank: false }, { id: 'b', fromBank: false }, { id: 'c', fromBank: false }],
                  [true, true, true]));
  eq(sent, [], 'a perfect round of the game’s own questions was published as work');
});

test('a mixed round publishes only its bank half', () => {
  const { publish, sent } = publisher();
  publish(session([{ id: 'a', fromBank: true }, { id: 'b', fromBank: false }, { id: 'c', fromBank: true }],
                  [true, true, false]));
  eq(sent, [{ correct: 1, answered: 2, chapter: 7 }]);
});

test('a question left UNANSWERED is not published as wrong', () => {
  const { publish, sent } = publisher();
  const s = session([{ id: 'a', fromBank: true }, { id: 'b', fromBank: true }, { id: 'c', fromBank: true }], []);
  s.results[0] = true;   // only the first was reached
  publish(s);
  eq(sent, [{ correct: 1, answered: 1, chapter: 7 }], 'a round closed early counted questions nobody saw');
});

test('a round is published ONCE, however often the summary repaints', () => {
  const { publish, sent } = publisher();
  const s = session([{ id: 'a', fromBank: true }], [true]);
  publish(s); publish(s); publish(s);
  eq(sent.length, 1, 'a repaint paid the board ' + sent.length + ' times');
});

section('\nTHE BUILT-IN SET — the fallback everything rests on');

test('every built-in row is answerable', () => {
  G.JQ_BUILTIN.forEach((row, i) => {
    const [stem, options, correct] = row;
    ok(typeof stem === 'string' && stem.trim(), 'row ' + i + ' has no wording');
    ok(Array.isArray(options) && options.length >= 2, 'row ' + i + ' has fewer than two options');
    ok(Number.isInteger(correct) && correct >= 0 && correct < options.length,
       'row ' + i + ' points at option ' + correct + ' of ' + options.length);
  });
});

test('no built-in row offers the same option twice', () => {
  G.JQ_BUILTIN.forEach((row, i) => {
    eq(new Set(row[1]).size, row[1].length, 'row ' + i + ' (' + row[0] + ') has a duplicate option');
  });
});

test('every built-in question is SHORT — none is a comprehension passage', () => {
  G.JQ_BUILTIN.forEach((row, i) => {
    ok(row[0].length <= F.MAX_STEM, 'row ' + i + ' is ' + row[0].length + ' characters');
    row[1].forEach(o => ok(o.length <= F.MAX_OPTION, 'row ' + i + ' has a ' + o.length + '-character option'));
  });
});

test('there are enough built-in questions to fill a round several times over', () => {
  ok(G.JQ_BUILTIN.length >= 3 * 4, 'only ' + G.JQ_BUILTIN.length + ' built-in questions');
});

test('a built-in row becomes a question of the same shape a bank one has', () => {
  const q = G.jqBuiltinQuestion(G.JQ_BUILTIN[0], 0);
  ok(q.id && q.stem && q.options.length && q.correctId);
  eq(q.fromBank, false);
  ok(q.options.some(o => o.id === q.correctId), 'the built-in answer names no option');
});

section('\nTHE TIER — what answering well is worth');

test('the tier is taken ONCE, so a later shop peach is a purchase not a prize', () => {
  G.setBonus(3);
  eq(G.jqTakeBonusRanks(), 3);
  eq(G.jqTakeBonusRanks(), 0, 'the gate paid its bonus twice');
});

test('the round asks three questions and each right one heals ten', () => {
  eq(G.JQ_PER_GATE, 3);
  eq(G.JQ_HEAL, 10);
});

test('every plain gate pays MORE for a right answer, never less', () => {
  ok(G.JQ_SHOP_GOLD > 0 && G.JQ_HEART_HP > 0 && G.JQ_ASHES > 0,
     'a tier worth nothing is a question worth nothing');
});

for (const run of queue) await run();

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
