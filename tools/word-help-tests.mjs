// Regression tests for 💬 WORD & GRAMMAR HELP — the popout on a marked
// question's options. Run with:
//     node tools/word-help-tests.mjs            all cases
//     node tools/word-help-tests.mjs <name>     one case
//
// It loads the REAL section out of app.js — `_whHasWords`, `_whClean`,
// `_whNormItems`, `_whPrompt` — and runs it over synthetic option lists and
// synthetic model replies.
//
// This is pinned because the failure it guards against is the quietest one in
// the app. `_whNormItems` decides which OPTION each of the model's answers is
// about. Line them up wrong and the card still opens, still looks right, still
// reads fluently — and tells a child that "reluctantly" cannot be used because
// it is an adjective. Nothing throws, nothing is red, and the student believes
// it, because everything else on the page has been correct all term.
//
// The other half is `_whHasWords`: too loose and a question whose options are
// "(1) (2) (3) (4)" against a diagram gets four ⓘ badges promising a meaning
// there is no word to give.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');
const a = src.indexOf('// ---- what there is to explain, and which option each answer belongs to');
const b = src.indexOf('// ---- the AI call, cached per option list', a);
if (a < 0 || b < 0) throw new Error('word-help section not found in app.js — did the banner comments change?');

// The few things the section leans on from the rest of the module. The two
// caps and `_normMcqChoice` are copied verbatim from app.js; `_questionContext`
// is reduced to the one line these tests need from it.
const preamble = `
const WH_MEANING_MAX = 240;
const WH_WHY_MAX = 400;
function _normMcqChoice(raw) {
  const s = String(raw || '').trim().toUpperCase();
  if (!s) return '';
  const digits = s.match(/\\d+/);
  if (digits) return digits[0];
  const ch = s.charAt(0);
  if (ch >= 'A' && ch <= 'H') return String(ch.charCodeAt(0) - 64);
  return ch;
}
function _questionContext(q) { return String((q && q.title) || ''); }
`;

const M = new Function(preamble + src.slice(a, b) +
  '\nreturn { _whHasWords, _whClean, _whNormItems, _whPrompt };')();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const ok = (cond, what) => { if (!cond) throw new Error(what); };
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};

// ---- builders --------------------------------------------------------------
// The shape buildOpenBody registers in _openMcqStore: "letter" is the option
// NUMBER as a string, and `correct` is already resolved off block.correctId.
const opts = (texts, correct = 0) => texts.map((t, i) => ({
  letter: String(i + 1), text: t, id: 'o' + i, correct: i === correct
}));
const said = (n, meaning, why) => ({ n, meaning, why });

// ── _whHasWords — is there anything here to explain? ────────────────────────

test('an ordinary word list has words', () => {
  ok(M._whHasWords(opts(['reluctant', 'reluctantly', 'reluctance', 'reluctancy'])), 'should have words');
});

test('bare-number options against a diagram have none', () => {
  ok(!M._whHasWords(opts(['(1)', '(2)', '(3)', '(4)'])), 'a numbered option list has no word to define');
});

test('the leading option number is stripped before looking for words', () => {
  // "(1) 24" is a number wearing a number — still nothing to define.
  ok(!M._whHasWords(opts(['(1) 24', '(2) 36', '(3) 48', '(4) 60'])), 'numbers only');
  ok(M._whHasWords(opts(['(1) at', '(2) on', '(3) in', '(4) by'])), 'prepositions are words');
});

test('one wordy option is enough to badge the block', () => {
  ok(M._whHasWords(opts(['(1)', '(2)', '(3)', 'none of the above'])), 'one word list is a word list');
});

test('a single letter is not a word', () => {
  // "a" is a real word, but a one-letter option is far more often a label —
  // the 2-letter floor is what keeps "A / B / C / D" from being badged.
  ok(!M._whHasWords(opts(['A', 'B', 'C', 'D'])), 'option labels are not words');
});

test('a malformed option list never throws', () => {
  [null, undefined, [], [null], [{}], [{ text: null }]].forEach(o => M._whHasWords(o));
});

// ── _whNormItems — WHICH option is each answer about? ───────────────────────

test('answers are placed by their own number, not their position', () => {
  const o = opts(['walk', 'walks', 'walked', 'walking']);
  // The model answered out of order. Placing these positionally would file
  // the explanation of "walked" under "walk".
  const map = M._whNormItems({ options: [said('3', 'past tense of walk', 'the sentence is about today')] }, o);
  eq(Object.keys(map), ['3'], 'only option 3 answered');
  eq(map['3'].meaning, 'past tense of walk');
});

test('"(2)", "2." and "B" all land on option 2', () => {
  const o = opts(['at', 'on', 'in', 'by']);
  eq(Object.keys(M._whNormItems({ options: [said('(2)', 'm', 'w')] }, o)), ['2'], 'parenthesised');
  eq(Object.keys(M._whNormItems({ options: [said('2.', 'm', 'w')] }, o)), ['2'], 'dotted');
  eq(Object.keys(M._whNormItems({ options: [said('B', 'm', 'w')] }, o)), ['2'], 'lettered');
});

test('a number the option list does not have is dropped, never squeezed in', () => {
  const o = opts(['at', 'on', 'in']);
  eq(M._whNormItems({ options: [said('4', 'm', 'w')] }, o), {}, 'option 4 does not exist');
});

test('a repeated number is a duplicate, not a second option — the first wins', () => {
  const o = opts(['at', 'on', 'in', 'by']);
  const map = M._whNormItems({ options: [said('1', 'first', 'w'), said('1', 'second', 'w')] }, o);
  eq(map['1'].meaning, 'first');
  eq(Object.keys(map), ['1'], 'the duplicate did not become another option');
});

test('an unnumbered reply of exactly one entry per option falls back to order', () => {
  const o = opts(['at', 'on', 'in', 'by']);
  const map = M._whNormItems({
    options: [
      { meaning: 'one', why: 'w' }, { meaning: 'two', why: 'w' },
      { meaning: 'three', why: 'w' }, { meaning: 'four', why: 'w' }
    ]
  }, o);
  eq(map['1'].meaning, 'one');
  eq(map['4'].meaning, 'four');
});

test('an unnumbered PARTIAL reply is dropped rather than guessed at', () => {
  // Three answers for four options. The third might be about option 3 or
  // option 4 and there is no way to tell, so none of them is placed.
  const o = opts(['at', 'on', 'in', 'by']);
  eq(M._whNormItems({ options: [{ meaning: 'a' }, { meaning: 'b' }, { meaning: 'c' }] }, o), {});
});

test('one numbered entry disables the positional fallback for the rest', () => {
  // A half-numbered reply must not have its unnumbered entries lined up by
  // position — the numbered one has already shifted everything along.
  const o = opts(['at', 'on', 'in', 'by']);
  const map = M._whNormItems({
    options: [said('3', 'about in', 'w'), { meaning: 'unnumbered' }, { meaning: 'also unnumbered' }, { meaning: 'and this' }]
  }, o);
  eq(Object.keys(map), ['3']);
  eq(map['3'].meaning, 'about in');
});

test('a bare array is read the same as {options:[…]}', () => {
  const o = opts(['at', 'on']);
  eq(Object.keys(M._whNormItems([said('2', 'm', 'w')], o)), ['2']);
});

test('"items" and "explanations" are accepted as the array key too', () => {
  const o = opts(['at', 'on']);
  eq(Object.keys(M._whNormItems({ items: [said('1', 'm', 'w')] }, o)), ['1']);
  eq(Object.keys(M._whNormItems({ explanations: [said('1', 'm', 'w')] }, o)), ['1']);
});

test('an entry with neither field is dropped, not stored empty', () => {
  const o = opts(['at', 'on']);
  eq(M._whNormItems({ options: [{ n: '1', meaning: '', why: '  ' }] }, o), {},
    'an empty answer is no answer');
});

test('a malformed reply never throws and yields nothing', () => {
  const o = opts(['at', 'on']);
  [null, undefined, {}, { options: null }, { options: 'nope' }, [null], ['string'], [42]]
    .forEach(r => eq(M._whNormItems(r, o), {}, 'reply ' + JSON.stringify(r)));
});

// ── _whClean — what actually reaches the card ───────────────────────────────

test('whitespace is collapsed and both fields are capped', () => {
  const it = M._whClean({ meaning: '  a   long\n  gap ', why: 'x'.repeat(600) });
  eq(it.meaning, 'a long gap');
  eq(it.why.length, 400, 'why capped at WH_WHY_MAX');
});

test('"fit" and "reason" stand in for "why", "means" for "meaning"', () => {
  eq(M._whClean({ means: 'quickly', fit: 'it is an adverb' }), { meaning: 'quickly', why: 'it is an adverb' });
  eq(M._whClean({ reason: 'wrong tense' }), { meaning: '', why: 'wrong tense' });
});

test('a meaning with no "why" is still worth showing', () => {
  eq(M._whClean({ meaning: 'unwilling' }), { meaning: 'unwilling', why: '' });
});

test('a non-object is null, never a half-built item', () => {
  [null, undefined, 'text', 42, []].forEach(v => ok(M._whClean(v) === null || Array.isArray(v), 'clean ' + v));
});

// ── _whPrompt — the model is told what it needs and nothing it should guess ──

test('the prompt prints every option, numbered, and names the correct one', () => {
  const p = M._whPrompt({ title: 'Choose the best word.' }, { options: opts(['at', 'on', 'in', 'by'], 2) });
  ok(p.includes('(1) at') && p.includes('(4) by'), 'every option printed');
  ok(p.includes('Option (3) is the correct one.'), 'the correct option is named');
  ok(p.includes('Choose the best word.'), 'the question travels with it');
});

test('a question with no correct option ticked says so rather than lying', () => {
  const p = M._whPrompt(null, { options: opts(['at', 'on']).map(o => ({ ...o, correct: false })) });
  ok(/No option is recorded as correct/.test(p), 'the authoring gap is stated, not invented over');
});

test('a blank option is printed as (blank), not as an empty line', () => {
  const p = M._whPrompt(null, { options: opts(['at', '   ']) });
  ok(p.includes('(2) (blank)'), 'a blank option keeps its number');
});

test('the prompt asks for the two fields the card renders', () => {
  const p = M._whPrompt(null, { options: opts(['at', 'on']) });
  ok(p.includes('"meaning"') && p.includes('"why"'), 'both fields requested');
  ok(p.includes('CANNOT be used in this sentence'), 'the grammar half is asked for explicitly');
});

test('a malformed block never throws', () => {
  [null, undefined, {}, { options: null }, { options: [] }].forEach(m => M._whPrompt(null, m));
});

// ── runner ───────────────────────────────────────────────────────────────────

const only = process.argv[2];
let passed = 0, failed = 0;
for (const c of cases) {
  if (only && c.name !== only) continue;
  try { c.fn(); console.log('  ok   ' + c.name); passed++; }
  catch (err) { console.log('  FAIL ' + c.name + '\n         ' + err.message); failed++; }
}
console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
