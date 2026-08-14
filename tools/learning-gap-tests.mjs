// Regression tests for the 🎯 LEARNING GAPS list and the daily retry credits.
// Run with:
//     node tools/learning-gap-tests.mjs            all cases
//     node tools/learning-gap-tests.mjs <name>     one case
//
// It loads the REAL `lgHydrate` / `lgRecord` / `lgNoteWin` / credit accounting
// out of app.js, so a change to any of them is caught here rather than on a
// child's phone.
//
// Everything this file pins fails SILENTLY in the app. A gap keyed two ways
// splits its own evidence and never gathers enough to be ranked; a credit
// counter that misses the day rollover hands out 30 credits once and never
// again; a gap that cannot be re-opened tells a student they have mastered
// something they just got wrong. Nothing throws in any of those cases.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');

const slice = (from, to, what) => {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(what + ' not found in app.js — did the banner comment change?');
  return src.slice(a, b);
};

// Everything from the store's constants down to the end of the read helpers:
// hydrate, record, prune, win, and the credit accounting.
const store = slice("const GAPS_DOC = 'learningGaps'", '// ---- job 2: feeding the student', 'the learning-gap store');

const M = new Function(`
  ${'let currentUser = { uid: "u1", role: "student" }, db = null;'}
  let questionBank = [];
  let _now = Date.parse('2026-08-14T09:00:00Z');
  let _today = '2026-08-14';
  const FC_HALFLIFE_DAYS = 14;
  function progressToday() { return _today; }
  function stripHtmlToText(s) { return String(s == null ? '' : s).replace(/<[^>]*>/g, ''); }
  function qTagList(q) { return (q && Array.isArray(q.tags)) ? q.tags.filter(Boolean) : []; }
  function setDoc() { return Promise.resolve(); }
  function doc() { return {}; }
  function showToast() {}
  const window = { __aiReady: () => false };
  function askGemini() { return Promise.reject(new Error('no ai in tests')); }
  function _parseAIJson() { return null; }
  function _docQParts(q) { return { text: (q && q.text) || '' }; }
  function lgPaintCredits() {}
  const SETTINGS_COL = 'settingsZh';
  ${store}
  return {
    LG_CLEAR_WINS, LG_MAX, LG_EVIDENCE_KEEP, REGEN_DAILY_CREDITS, LG_NEW_PER_ATTEMPT,
    lgHydrate, lgGapKey, lgRecord, lgNoteWin, lgActiveGaps, lgClearedGaps, lgAllGaps,
    lgCreditsLeft, lgSpendCredit, lgRefundCredit, lgKindFromTopic, lgKindOf,
    lgNoteFromParts, _lgFallbackItems,
    reset(saved, day) { _today = day || '2026-08-14'; lgState = lgHydrate(saved || null); _lgRollCredits(); },
    state() { return lgState; },
    setDay(d) { _today = d; },
    setBank(b) { questionBank = b; },
  };
`)();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};
const ok = (cond, what) => { if (!cond) throw new Error(what || 'expected true'); };

const Q = { id: 'q1', title: 'A question', topic: 'Grammar', tags: ['past perfect tense'] };

// ---- keying ----------------------------------------------------------------
// The same weakness written two ways is the bug that quietly halves every gap's
// evidence, so the key has to survive case, spacing and punctuation.

test('one weakness written three ways is ONE gap', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: 'Past Perfect Tense' }], Q, []);
  M.lgRecord([{ kind: 'grammar', label: 'past perfect tense' }], Q, []);
  M.lgRecord([{ kind: 'grammar', label: 'past-perfect  tense!' }], Q, []);
  eq(M.lgAllGaps().length, 1, 'gap count');
  eq(M.lgAllGaps()[0].misses, 3, 'misses accumulated on the one record');
});

test('the same words under a different kind are a different gap', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: 'tense' }], Q, []);
  M.lgRecord([{ kind: 'vocabulary', label: 'tense' }], Q, []);
  eq(M.lgAllGaps().length, 2, 'grammar and vocabulary are not the same list');
});

test('an unknown kind is filed, not dropped', () => {
  M.reset();
  M.lgRecord([{ kind: 'nonsense', label: 'something' }], Q, []);
  eq(M.lgAllGaps().length, 1, 'still recorded');
  eq(M.lgAllGaps()[0].kind, 'grammar', 'falls back to a real kind');
});

test('a gap with no label is refused', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: '   ' }, { kind: 'grammar', label: '' }], Q, []);
  eq(M.lgAllGaps().length, 0, 'nothing filed under a blank name');
});

// ---- clearing --------------------------------------------------------------
// A gap that cannot re-open is the dangerous one: it tells a child they have
// mastered something they have just got wrong again.

test('LG_CLEAR_WINS right in a row clears a gap — and no fewer', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: 'past perfect tense' }], Q, []);
  for (let i = 1; i < M.LG_CLEAR_WINS; i++) {
    M.lgNoteWin(Q);
    eq(M.lgActiveGaps().length, 1, 'still open after ' + i + ' win(s)');
  }
  M.lgNoteWin(Q);
  eq(M.lgActiveGaps().length, 0, 'closed on the last win');
  eq(M.lgClearedGaps().length, 1, 'and shows under Cleared');
});

test('a fresh miss RE-OPENS a cleared gap and resets the run', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: 'past perfect tense' }], Q, []);
  for (let i = 0; i < M.LG_CLEAR_WINS; i++) M.lgNoteWin(Q);
  eq(M.lgClearedGaps().length, 1, 'cleared first');
  M.lgRecord([{ kind: 'grammar', label: 'past perfect tense' }], Q, []);
  eq(M.lgActiveGaps().length, 1, 're-opened');
  eq(M.lgClearedGaps().length, 0, 'no longer cleared');
  eq(M.lgActiveGaps()[0].streak, 0, 'the run towards Cleared starts again');
});

test('a win on an UNRELATED question moves nothing', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: 'past perfect tense' }], Q, []);
  M.lgNoteWin({ id: 'other', topic: 'Vocabulary', tags: ['synonyms'] });
  eq(M.lgActiveGaps()[0].streak, 0, 'streak untouched');
});

test('a win counts when the question is TAGGED with the gap, not just linked by id', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: 'past perfect tense' }], { id: 'seed', topic: 'Grammar' }, []);
  M.lgNoteWin({ id: 'never-seen', topic: 'Grammar', tags: ['Past Perfect Tense'] });
  eq(M.lgActiveGaps()[0].streak, 1, 'matched on the tag');
});

// ---- evidence and bounds ---------------------------------------------------

test('the newest evidence leads and the list stays bounded', () => {
  M.reset();
  for (let i = 0; i < M.LG_EVIDENCE_KEEP + 3; i++) {
    M.lgRecord([{ kind: 'grammar', label: 'past perfect tense' }], Q,
      [{ wrote: 'answer ' + i, should: 'the model' }]);
  }
  const g = M.lgAllGaps()[0];
  eq(g.evidence.length, M.LG_EVIDENCE_KEEP, 'capped');
  eq(g.evidence[0].wrote, 'answer ' + (M.LG_EVIDENCE_KEEP + 2), 'newest first');
});

test('a blank answer is recorded as one, not dropped', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: 'past perfect tense' }], Q, [{ wrote: '', should: 'the model' }]);
  eq(M.lgAllGaps()[0].evidence[0].wrote, '(left blank)', 'blank is evidence too');
});

test('one wrong question opens at most LG_NEW_PER_ATTEMPT gaps', () => {
  M.reset();
  M.lgRecord([
    { kind: 'grammar', label: 'a' }, { kind: 'grammar', label: 'b' },
    { kind: 'grammar', label: 'c' }, { kind: 'grammar', label: 'd' },
  ], Q, []);
  eq(M.lgAllGaps().length, M.LG_NEW_PER_ATTEMPT, 'capped per attempt');
});

test('the list is pruned to LG_MAX, and cleared gaps go first', () => {
  M.reset();
  for (let i = 0; i < M.LG_MAX + 5; i++) M.lgRecord([{ kind: 'grammar', label: 'gap ' + i }], Q, []);
  ok(M.lgAllGaps().length <= M.LG_MAX, 'bounded: ' + M.lgAllGaps().length);
});

// ---- ranking ---------------------------------------------------------------

test('the gap missed most often leads', () => {
  M.reset();
  M.lgRecord([{ kind: 'grammar', label: 'rare' }], Q, []);
  for (let i = 0; i < 5; i++) M.lgRecord([{ kind: 'grammar', label: 'common' }], Q, []);
  eq(M.lgActiveGaps()[0].label, 'common', 'worst first');
});

// ---- the daily credits -----------------------------------------------------
// The rollover is the silent one: a counter that misses it hands out the
// allowance once and never again.

test('a fresh account starts with the full allowance', () => {
  M.reset();
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS, 'full');
});

test('spending draws down, and never below zero', () => {
  M.reset();
  for (let i = 0; i < M.REGEN_DAILY_CREDITS; i++) ok(M.lgSpendCredit(), 'credit ' + i + ' granted');
  eq(M.lgCreditsLeft(), 0, 'spent out');
  eq(M.lgSpendCredit(), false, 'the next one is refused');
  eq(M.lgCreditsLeft(), 0, 'still zero, never negative');
});

test('a new day restores the whole allowance', () => {
  M.reset();
  for (let i = 0; i < 10; i++) M.lgSpendCredit();
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS - 10, 'drawn down today');
  M.setDay('2026-08-15');
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS, 'refilled tomorrow');
});

test('a refund gives the credit back, and cannot mint new ones', () => {
  M.reset();
  M.lgSpendCredit();
  M.lgRefundCredit();
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS, 'back to full');
  M.lgRefundCredit();
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS, 'a refund with nothing spent adds nothing');
});

test("yesterday's spend does not follow the student into today", () => {
  M.reset({ credits: { dayKey: '2026-08-13', used: 30 } }, '2026-08-14');
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS, 'stale day is rolled over on load');
});

// ---- hydrate ---------------------------------------------------------------
// A half-written document must never take the page down.

test('a malformed document hydrates to an empty, usable list', () => {
  M.reset({ gaps: { bad: null, worse: 42, ugly: { kind: 'grammar' } }, credits: 'nonsense' });
  eq(M.lgAllGaps().length, 0, 'nothing usable survived');
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS, 'credits still work');
});

test('a saved gap comes back with every field it needs', () => {
  M.reset({
    gaps: { 'grammar:past perfect tense': { kind: 'grammar', label: 'past perfect tense', misses: 4 } },
    credits: { dayKey: '2026-08-14', used: 2 },
  });
  const g = M.lgAllGaps()[0];
  eq(g.misses, 4, 'misses kept');
  eq(g.qIds, [], 'missing arrays rebuilt');
  eq(g.evidence, [], 'missing evidence rebuilt');
  eq(g.cleared, false, 'missing flag rebuilt');
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS - 2, 'used count kept');
});

test('a hand-edited negative used-count cannot mint credits', () => {
  M.reset({ credits: { dayKey: '2026-08-14', used: -500 } });
  eq(M.lgCreditsLeft(), M.REGEN_DAILY_CREDITS, 'clamped to the allowance');
});

// ---- the fallback ----------------------------------------------------------
// With the AI off, the list must still fill from the question's own labelling.

test('with no AI, a mistake still lands on the list from the question tags', () => {
  M.reset();
  M.lgNoteFromParts(Q, [{ expected: 'had gone', student: 'has went' }], 'test');
  eq(M.lgAllGaps().length, 1, 'recorded from the fallback');
  eq(M.lgAllGaps()[0].label, 'past perfect tense', 'named by the tag');
});

test('an untagged question falls back to its topic', () => {
  M.reset();
  M.lgNoteFromParts({ id: 'q9', topic: 'Vocabulary Cloze' }, [{ expected: 'a', student: 'b' }], 'test');
  eq(M.lgAllGaps()[0].label, 'Vocabulary Cloze', 'named by the topic');
  eq(M.lgAllGaps()[0].kind, 'vocabulary', 'and filed under the right kind');
});

test('a question with no wrong parts records nothing', () => {
  M.reset();
  M.lgNoteFromParts(Q, [], 'test');
  eq(M.lgAllGaps().length, 0, 'no evidence, no gap');
});

test('topics map to the kind a teacher would expect', () => {
  eq(M.lgKindFromTopic('Vocabulary Cloze'), 'vocabulary', 'vocabulary cloze');
  eq(M.lgKindFromTopic('Grammar Cloze'), 'grammar', 'grammar cloze');
  eq(M.lgKindFromTopic('Continuous Writing'), 'writing', 'writing');
  eq(M.lgKindFromTopic('Comprehension: Inference'), 'comprehension', 'comprehension by keyword');
  eq(M.lgKindFromTopic('Something New'), 'grammar', 'unknown topic still lands somewhere real');
});

// ---- run -------------------------------------------------------------------
const only = process.argv[2];
let pass = 0, fail = 0;
for (const c of cases) {
  if (only && c.name.indexOf(only) < 0) continue;
  try { c.fn(); pass++; console.log('  ok   ' + c.name); }
  catch (e) { fail++; console.log('  FAIL ' + c.name + '\n         ' + e.message); }
}
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
