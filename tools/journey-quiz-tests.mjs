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
const F = new Function(DOM_SHIM + filterBlock + '\nreturn { quizUsable, plain, MAX_STEM, MAX_OPTION };')();

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
function test(name, fn) {
  if (only && !name.includes(only)) return;
  try { fn(); console.log('  ✅ ' + name); pass++; }
  catch (e) { console.log('  ❌ ' + name + '\n     ' + e.message); fail++; }
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

console.log('\nTHE ALLOWLIST — what may be asked at a gate');

test('a short wording + one MCQ is usable', () => {
  const q = F.quizUsable(shortQ());
  ok(q, 'a plain short MCQ must be usable');
  eq(q.stem, 'She ______ to school every morning.');
  eq(q.options.length, 3);
  eq(q.correctId, 'o2');
  eq(q.fromBank, true);
});

for (const type of ['clozebank', 'clozeopen', 'clozemcq', 'editpassage', 'wordmatch', 'synthesis',
                    'fillblank', 'plainanswer', 'answer', 'table', 'image', 'openLines', 'workingSpace']) {
  test('a ' + type + ' block is refused', () => {
    ok(!F.quizUsable(shortQ({
      blocks: [{ id: 't1', type: 'text', content: '<p>Read the passage.</p>' }, { id: 'p1', type }, mcq()]
    })), type + ' reached a student standing in a doorway');
  });
}

test('a passage set — several MCQs in one question — is refused', () => {
  ok(!F.quizUsable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Read the passage below.</p>' }, mcq(), mcq({ id: 'm2' })]
  })), 'a comprehension set is exactly what must not be asked here');
});

test('a question with NO mcq at all is refused', () => {
  ok(!F.quizUsable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>Explain why.</p>' }] })));
});

test('a question with lettered parts is refused', () => {
  ok(!F.quizUsable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>(a) Which word fits?</p>', part: 'a' }, mcq()]
  })), 'a stem that only makes sense beside its other parts');
});

test('an UNTICKED mcq is refused — the gate never guesses which is right', () => {
  ok(!F.quizUsable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>Q</p>' }, mcq({ correctId: null })] })));
});

test('a correctId naming no option is refused', () => {
  ok(!F.quizUsable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>Q</p>' }, mcq({ correctId: 'nope' })] })));
});

test('a stem longer than the cap is refused', () => {
  const long = 'word '.repeat(80);
  ok(!F.quizUsable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>' + long + '</p>' }, mcq()] })));
});

test('a stem exactly at the cap is still usable', () => {
  const at = 'a'.repeat(F.MAX_STEM);
  ok(F.quizUsable(shortQ({ blocks: [{ id: 't1', type: 'text', content: '<p>' + at + '</p>' }, mcq()] })));
});

test('an option longer than the cap is refused', () => {
  ok(!F.quizUsable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Q</p>' },
             mcq({ options: [{ id: 'o1', text: 'a'.repeat(F.MAX_OPTION + 1) }, { id: 'o2', text: 'b' }], correctId: 'o2' })]
  })));
});

test('a question carrying a picture is refused — the card cannot show one', () => {
  ok(!F.quizUsable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Look at the diagram <img src="x.png"> and choose.</p>' }, mcq()]
  })));
});

test('an annotation question is refused', () => {
  ok(!F.quizUsable(shortQ({ annotation: true })));
});

test('a question with fewer than two options is refused', () => {
  ok(!F.quizUsable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Q</p>' }, mcq({ options: [{ id: 'o1', text: 'only' }], correctId: 'o1' })]
  })));
});

test('a question with no wording at all is refused', () => {
  ok(!F.quizUsable({ id: 'q', blocks: [mcq()] }), 'four options and nothing asking anything');
});

test('an empty / malformed question is refused rather than thrown on', () => {
  ok(!F.quizUsable(null));
  ok(!F.quizUsable({}));
  ok(!F.quizUsable({ blocks: [] }));
  ok(!F.quizUsable({ blocks: 'not an array' }));
});

test('the wording comes back as PLAIN text, markup gone', () => {
  const q = F.quizUsable(shortQ({
    blocks: [{ id: 't1', type: 'text', content: '<p>Choose the <strong>correct</strong> word.</p>' }, mcq()]
  }));
  ok(!/[<>]/.test(q.stem), 'markup reached the card: ' + q.stem);
});

console.log('\nTHE DRAW — which questions a round is built from');

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

console.log('\nTHE BUILT-IN SET — the fallback everything rests on');

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

console.log('\nTHE TIER — what answering well is worth');

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

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
