// Regression tests for the "part" field the AI sets on a block. Run with:
//     node tools/ai-parts-tests.mjs            all cases
//     node tools/ai-parts-tests.mjs <name>     one case
//
// It loads the REAL `buildBlocksFromAi` out of app.js and feeds it the JSON a
// model returns for a comprehension page — a passage, then the questions on it.
//
// This is pinned because `buildBlocksFromAi` is the ONE function every AI
// authoring path goes through (Build from screenshot, Rapid add, the bulk PDF
// import, the exam paper builder, the learning-gap generator), and the "part"
// field is the only way the model can say "these four options are part (a) of
// the passage". Drop it and the failure is completely silent: eight option
// lists render in a row with nothing telling them apart, the answer key prints
// all eight under one heading, and every screen still looks right.
//
// The parts are LETTERED (a) (b) (c), not given the paper's own 21, 22, 23:
// those numbers belong to that exam paper and a bank question stands on its
// own. A number is still accepted, because the parts bar's "Number from" box
// lets an author set one by hand.
//
// The other direction matters too. `qLiftPartMarkers` runs immediately after,
// hunting typed "(a)" markers — it must leave a block that already carries a
// part alone, or the model's lettering is overwritten by whatever the text
// happens to start with.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');

const cut = (from, to, what) => {
  const a = src.indexOf(from);
  if (a < 0) throw new Error(what + ': "' + from + '" not found in app.js');
  const b = src.indexOf(to, a + from.length);
  if (b < 0) throw new Error(what + ': end marker not found');
  return src.slice(a, b);
};

// The real thing: the builder, and the whole part pipeline it ends with.
const section = [
  'const QPART_ASSIGN = ' + /const QPART_ASSIGN = ('[a-z]*')/.exec(src)[1] + ';',
  'const QPART_LETTERS = ' + /const QPART_LETTERS = ('[a-z]*')/.exec(src)[1] + ';',
  'const QPART_MARKER_RE = ' + /const QPART_MARKER_RE = (\/.*\/);/.exec(src)[1] + ';',
  // qPartWalkPlain … qPartDetect sit ABOVE the numeric-part constants, so the
  // marker slice has to stop where they start or both slices declare them.
  cut('function qPartWalkPlain', 'const QPART_NUM_RE', 'marker detection'),
  cut('const QPART_NUM_RE', '// The part each block belongs to', 'numeric parts + normalize'),
  cut('function qPartMap(blocks)', 'function qPartUnfileLoneExplanation', 'part map'),
  cut('function qPartUnfileLoneExplanation', 'function qApplyAiParts', 'ai part helpers'),
  cut('function qApplyAiParts', '// Should THIS block print the part label', 'apply + qPartOf'),
  cut('function qBlockOpensPart(b)', '// Does this question use parts at all', 'openers'),
  cut('function buildBlocksFromAi', '\n// Build a full pending question object', 'builder'),
  // The handful of leaf helpers the builder leans on, reduced to their contract.
  `
let _n = 0;
function generateBlockId() { return 'b' + (++_n); }
function stripHtml(c) { return c ? String(c).replace(/<[^>]*>/g, ' ').replace(/\\s+/g, ' ').trim() : ''; }
function _separateOptionLines(t) { return String(t == null ? '' : t); }
function _markedToBlanks(t) { return { content: String(t == null ? '' : t), blanks: {} }; }
function escapeHtml(s) { return String(s == null ? '' : s); }
`
].join('\n');

const M = new Function(section +
  '\nreturn { buildBlocksFromAi, qPartMap, qPartOf, qBlockOpensPart, qPartNormalize };')();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const ok = (cond, what) => { if (!cond) throw new Error(what); };
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};

const mcq = (part, opts, correctIndex) => {
  const b = { type: 'mcq', options: opts || ['a', 'b', 'c', 'd'] };
  if (part != null) b.part = part;
  if (correctIndex != null) b.correctIndex = correctIndex;
  return b;
};
const build = blocks => M.buildBlocksFromAi({ blocks }).blocks;
const partsOf = bs => bs.map(b => M.qBlockOpensPart(b));

// ── the shape a comprehension page comes back as ────────────────────────────

// One passage, one poster picture, then the four questions that follow it —
// exactly what the model is asked to return for a page of "Myths of lice" plus
// Q21 onwards. The paper numbers them 21 to 24; the model is told to LETTER
// them (a) (b) (c) (d), because those numbers belong to that exam paper and a
// bank question stands on its own.
const PAGE = [
  { type: 'text', text: 'For each question, four options are given.' },
  { type: 'image', page: 1, box_2d: [40, 30, 900, 970] },
  { type: 'text', part: 'a', text: 'What does the word "Troublemakers" in the title refer to?' },
  mcq('a', ['humans', 'head lice', 'parasites', 'infestations'], 1),
  { type: 'text', part: 'b', text: 'This article is an extract from ______.' },
  mcq('b', ['a daily newspaper', 'a medical journal', 'a magazine for parents', 'a school magazine'], 2),
  mcq('c', ['one', 'two', 'three', 'four']),
  mcq('d', ['one', 'two', 'three', 'four'], 3)
];

test('every question after the passage keeps its letter, in order', () => {
  const bs = build(PAGE);
  const mcqs = bs.filter(b => b.type === 'mcq');
  eq(mcqs.map(b => b.part), ['a', 'b', 'c', 'd']);
});

test('a NUMBER is still honoured, for a question numbered by hand', () => {
  // The automatic paths all letter now, but the parts bar's "Number from" box
  // is a deliberate manual escape hatch and qPartNormalize still takes 1-999.
  const bs = build([mcq('21'), mcq('22')]);
  eq(bs.map(b => b.part), ['21', '22']);
});

test('the shared instruction and the poster stay OUTSIDE the parts', () => {
  const bs = build(PAGE);
  eq(M.qBlockOpensPart(bs[0]), '', 'the instruction line must open no part');
  eq(M.qBlockOpensPart(bs[1]), '', 'the poster must open no part');
});

test("a question's wording and its options land under the same part", () => {
  const bs = build(PAGE);
  const map = M.qPartMap(bs);
  const wording = bs.find(b => b.type === 'text' && /Troublemakers/.test(b.content));
  const opts = bs.filter(b => b.type === 'mcq')[0];
  eq(M.qPartOf(map, wording), 'a');
  eq(M.qPartOf(map, opts), 'a');
});

test('nothing before the first part is filed under one', () => {
  const map = M.qPartMap(build(PAGE));
  const bs = build(PAGE);
  eq(M.qPartOf(M.qPartMap(bs), bs[0]), '');
  eq(M.qPartOf(M.qPartMap(bs), bs[1]), '');
});

test('an unanswered sub-question is built with NO correct option', () => {
  const bs = build(PAGE);
  const q23 = bs.filter(b => b.type === 'mcq')[2];
  eq(q23.correctId, null, 'the model omitted correctIndex — that must not become a guess');
  const q21 = bs.filter(b => b.type === 'mcq')[0];
  ok(q21.correctId === q21.options[1].id, 'correctIndex 1 must tick the second option');
});

// ── the part must survive the typed-marker pass that runs straight after ────

test('a lettered part still works the same way', () => {
  const bs = build([
    { type: 'text', part: 'a', text: 'First bit' },
    { type: 'plainanswer', text: 'one' },
    { type: 'text', part: 'b', text: 'Second bit' },
    { type: 'plainanswer', text: 'two' }
  ]);
  eq(partsOf(bs), ['a', '', 'b', '']);
});

test('a declared part is NOT overwritten by a marker typed in the text', () => {
  // qLiftPartMarkers hunts a leading marker and would file this under (a),
  // throwing away the letter the model was asked for.
  const bs = build([{ type: 'text', part: 'c', text: '(a) What does the word mean?' }]);
  eq(M.qBlockOpensPart(bs[0]), 'c');
  const bn = build([{ type: 'text', part: '21', text: '(a) What does the word mean?' }]);
  eq(M.qBlockOpensPart(bn[0]), '21');
});

test('a typed marker still works when the model declares no part', () => {
  const bs = build([
    { type: 'text', text: '(a) First bit' },
    { type: 'plainanswer', text: 'one' },
    { type: 'text', text: '(b) Second bit' },
    { type: 'plainanswer', text: 'two' }
  ]);
  eq(partsOf(bs), ['a', '', 'b', '']);
});

test('"(21)" and "21" are both read as part 21', () => {
  eq(M.qBlockOpensPart(build([mcq('(21)')])[0]), '21');
  eq(M.qBlockOpensPart(build([mcq(' 21. ')])[0]), '21');
});

test('a part the app cannot name is dropped, not stored raw', () => {
  // "Section B" is not a part. Kept, it would render as a label nothing else
  // in the app can group by.
  ['Section B', '0', '1000', 'ab', '', null].forEach(v => {
    eq(M.qBlockOpensPart(build([mcq(v)])[0]), '', 'part ' + JSON.stringify(v));
  });
});

test('the unfiled marker survives, so a whole-question note stays unfiled', () => {
  const bs = build([
    { type: 'text', part: 'a', text: 'The first question' },
    mcq('a'),
    { type: 'explanation', part: '-', text: 'A note about the whole passage.' }
  ]);
  const ex = bs.find(b => b.type === 'explanation');
  eq(ex.part, '-', 'QPART_NONE must not be normalised away');
});

test('only the first block of an entry is stamped, never every one', () => {
  // qPartMap inherits forward, so labelling both would open the same part twice.
  const bs = build([{ type: 'answer', part: 'b', claim: 'c', evidence: 'e', reasoning: 'r' }]);
  eq(bs.filter(b => M.qBlockOpensPart(b) === 'b').length, 1);
});

test('a page with no parts at all is unchanged', () => {
  const bs = build([
    { type: 'text', text: 'A plain question.' },
    mcq(null, ['a', 'b'], 0)
  ]);
  eq(partsOf(bs), ['', '']);
});

test('malformed AI output never throws', () => {
  [{}, { blocks: null }, { blocks: [] }, { blocks: [null] }, { blocks: [{ type: 'mcq', part: {} }] },
   { blocks: [{ type: 'mcq', options: null }] }].forEach(d => M.buildBlocksFromAi(d));
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
