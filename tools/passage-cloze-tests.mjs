// Regression tests for the two comprehension formats. Run with:
//     node tools/passage-cloze-tests.mjs            all cases
//     node tools/passage-cloze-tests.mjs <name>     one case
//
// It loads the REAL code out of app.js:
//   • 📑 the PASSAGE BUILDER's parse — `_pbQStart`, `_pbParse`, `_pbParseKey`,
//     `_pbPassageHtml`
//   • 🔤 the COMPREHENSION CLOZE's bank — `cbBank`, `cbBankMap`, `_cbGrid`,
//     `cbIntro`, `cbAnswerKeyText`
//   • the NUMERIC part labels both of them depend on — `qPartNormalize`
//
// Every failure here is silent. A passage split one line early swallows the
// first option list into the passage and the question loses an answer nobody
// notices until a class sits it. A question number read off a quantity —
// "20,000 animals across 1,000 species" — cuts the passage in half. And a word
// bank that does not contain one of its own answers renders perfectly, prints
// perfectly, and is unanswerable.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');

const slice = (from, to, what) => {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(what + ' not found in app.js — did the banner comments change?');
  return src.slice(a, b);
};

// The numeric-part rules, the passage parse, and the cloze's bank.
const parts = slice('const QPART_NUM_RE =', 'function qPartLabel(', 'numeric part rules')
  // qBlockOpensPart and qPartLabelFirst decide, between them, which block wears
  // the label on screen and on paper.
  + slice('function qBlockOpensPart(b)', '// Does this question use parts at all', 'part openers')
  + slice('function qPartLabelFirst(blocks, block)', '\n}\n', 'label-first') + '\n}\n';
const pb = slice('const PB_QLINE_RE =', '// ---- the dialog ---', 'passage builder parse');
const cb = slice('const CB_LETTERS =', '// ---- the student\'s passage', 'cloze bank')
  // cbAnswerKeyText sits below the DOM half, so it is taken on its own rather
  // than dragging every drag-and-drop listener into a headless harness.
  + slice('// Every blank on the key', '\n}\n', 'cloze answer key') + '\n}\n';

// The handful of things those sections lean on, copied verbatim from app.js.
const preamble = `
const QPART_ASSIGN = 'abcdefghjklmnopqrstuvwxyz';
function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function _fbParse(text) {
  const parts = []; const re = /\\[\\[([\\s\\S]+?)\\]\\]/g; let last = 0, m; text = String(text || '');
  while ((m = re.exec(text))) { if (m.index > last) parts.push({ type: 'text', text: text.slice(last, m.index) }); parts.push({ type: 'blank', answer: (m[1] || '').trim() }); last = m.index + m[0].length; }
  if (last < text.length) parts.push({ type: 'text', text: text.slice(last) });
  return parts;
}
let _blockN = 0;
function generateBlockId() { return 'b' + (++_blockN); }
function createBlock(type) {
  const b = { id: generateBlockId(), type };
  if (type === 'text') b.content = '';
  if (type === 'mcq') { b.options = []; b.correctId = null; }
  return b;
}
`;

const M = new Function(preamble + parts + cb + pb +
  '\nreturn { qPartIsNum, qPartNormalize, qBlockOpensPart, qPartLabelFirst, _pbQStart, _pbParse, _pbParseKey, _pbPassageHtml,'
  + ' pbBuildBlocks, pbPartLetter, pbPartOverflow, _pbRelabelPassage,' +
  ' cbBank, cbBankMap, _cbGrid, cbIntro, cbAnswerKeyText, _cbBlanks, _cbStart, cbHasBlanks, CB_LETTERS };')();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const ok = (cond, what) => { if (!cond) throw new Error(what); };
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};

// ── numeric part labels ─────────────────────────────────────────────────────

test('a number is a part in its own right', () => {
  eq(M.qPartNormalize('16'), '16');
  eq(M.qPartNormalize('(16)'), '16');
  eq(M.qPartNormalize(' 16. '), '16');
  ok(M.qPartIsNum('16'), '16 should read as numeric');
});

test('the letters still work and 0 / 1000 do not', () => {
  eq(M.qPartNormalize('a'), 'a');
  eq(M.qPartNormalize('(C)'), 'c');
  eq(M.qPartNormalize('0'), '', 'a part is never zero');
  eq(M.qPartNormalize('1000'), '', 'a paper never numbers past 999');
  eq(M.qPartNormalize('16a'), '', 'not a number and not a letter');
});

test('a multi-letter value is NOT a part', () => {
  // indexOf on a string matches substrings, so "ab" used to come back as a
  // valid part — one no picker can show and no answer key can label.
  eq(M.qPartNormalize('ab'), '');
  eq(M.qPartNormalize('abc'), '');
});

test('the unfiled marker and empties are still nothing', () => {
  ['', null, undefined, '-', 'i', '  '].forEach(v => eq(M.qPartNormalize(v), '', 'value ' + JSON.stringify(v)));
});

// ── 📑 the passage builder ──────────────────────────────────────────────────

const PAPER = `As a student, I find the POSB Smart Buddy programme helpful. __Rolled out__ (16) in 2017,
it is now expanding to all schools in Singapore. With Smart Buddy, making payments in
school has become so __convenient__ (17). I just tap my smartwatch or EZ-Link card.

16   (1) Originated
     (2) Embarked
     (3) Launched
     (4) Founded

17   (1) advanced
     (2) creative
     (3) efficient
     (4) flexible`;

test('the paper splits into a passage and its sub-questions', () => {
  const p = M._pbParse(PAPER);
  eq(p.subs.map(s => s.n), [16, 17]);
  eq(p.subs[0].options, ['Originated', 'Embarked', 'Launched', 'Founded']);
  eq(p.subs[1].options, ['advanced', 'creative', 'efficient', 'flexible']);
  ok(/POSB Smart Buddy/.test(p.passage), 'the passage is kept');
  ok(!/Originated/.test(p.passage), 'an option list leaked into the passage');
});

test('the (16) markers inside the passage are never read as options', () => {
  const p = M._pbParse(PAPER);
  ok(/\(16\)/.test(p.passage), 'the marker must stay in the passage');
  eq(p.subs.length, 2, 'a marker was read as a question');
});

test('a quantity at the start of a line does not cut the passage', () => {
  // "20,000 animals across 1,000 species" opens with what looks like question 20.
  const p = M._pbParse(`Managed by Mandai Wildlife Group, these parks are home to more than
20,000 animals across 1,000 species, of which some are endangered.

16   (1) at
     (2) on`);
  ok(/20,000 animals/.test(p.passage), 'the passage was cut at a quantity');
  eq(p.subs.map(s => s.n), [16]);
});

test('a bare number with no option list under it is not a question', () => {
  const p = M._pbParse('The year was\n1985\nand nothing followed it.');
  eq(p.subs, []);
  ok(/1985/.test(p.passage), 'the number belongs to the passage');
});

test('the question number and its first option may share a line', () => {
  const p = M._pbParse('Some passage.\n16 (1) Originated\n(2) Embarked\n(3) Launched');
  eq(p.subs[0].options, ['Originated', 'Embarked', 'Launched']);
});

test('a wrapped option keeps its tail', () => {
  // An option long enough to wrap arrives as two lines. Dropping the second
  // loses half the answer with nothing looking wrong.
  const p = M._pbParse('Passage.\n16\n(1) a person who is very\nreluctant to help\n(2) short');
  eq(p.subs[0].options, ['a person who is very reluctant to help', 'short']);
});

test('"16 (3) x" is a wrapped line, not a new question', () => {
  eq(M._pbQStart('16 (3) something'), null);
  eq(M._pbQStart('16'), { n: 16, first: null });
  eq(M._pbQStart('16 (1) Originated'), { n: 16, first: 'Originated' });
});

test('a question with fewer than two options is dropped', () => {
  const p = M._pbParse('Passage.\n16\n(1) only one');
  eq(p.subs, [], 'one option is not a multiple-choice question');
});

test('nothing but a passage parses to no sub-questions', () => {
  const p = M._pbParse('Just a paragraph with no questions at all.');
  eq(p.subs, []);
  eq(p.passage, 'Just a paragraph with no questions at all.');
});

test('an empty or malformed paste never throws', () => {
  [null, undefined, '', '\n\n\n', '   ', '16', '(1) x'].forEach(v => M._pbParse(v));
});

// ── the answer key ──────────────────────────────────────────────────────────

test('a bare run of digits fills the answers positionally', () => {
  const subs = [{ n: 16 }, { n: 17 }, { n: 18 }, { n: 19 }, { n: 20 }];
  eq(M._pbParseKey('3 3 2 2 4', subs), { 16: 3, 17: 3, 18: 2, 19: 2, 20: 4 });
});

test('a paired key is read by question number, not by position', () => {
  const subs = [{ n: 16 }, { n: 17 }, { n: 18 }];
  eq(M._pbParseKey('18-2, 16-3, 17-1', subs), { 16: 3, 17: 1, 18: 2 });
});

test('a pair for a question we do not have is ignored', () => {
  eq(M._pbParseKey('16-3 99-4', [{ n: 16 }]), { 16: 3 });
});

test('an empty key yields nothing rather than a wrong guess', () => {
  eq(M._pbParseKey('', [{ n: 16 }]), {});
  eq(M._pbParseKey(null, [{ n: 16 }]), {});
});

// ── the blocks that come out ────────────────────────────────────────────────

test('the passage becomes one text block and each question its own LETTERED part', () => {
  // The paper's 16 and 17 are that exam paper's numbering, not this question's.
  // A bank question stands on its own, and one opening at part (16) reads as
  // though fifteen parts are missing.
  const p = M._pbParse(PAPER);
  p.subs[0].correct = 2;
  const out = M.pbBuildBlocks(p, 'For each question, choose the word closest in meaning…');
  eq(out.map(b => b.type), ['text', 'text', 'mcq', 'mcq']);
  eq(out[2].part, 'a');
  eq(out[3].part, 'b');
  ok(out[2].correctId === out[2].options[2].id, 'the ticked option is the one marked correct');
});

test('the markers INSIDE the passage are renumbered to match', () => {
  // Letter the questions and leave the passage alone and the student reads
  // "(16)" over the underlined word, then hunts for a question 16 that is now
  // part (a). The marker and its question must always agree.
  const p = M._pbParse(PAPER);
  const out = M.pbBuildBlocks(p, '');
  const passage = out[0].content;
  ok(/\(a\)/.test(passage), 'the first marker did not become (a): ' + passage.slice(0, 160));
  ok(/\(b\)/.test(passage), 'the second marker did not become (b)');
  ok(!/\(16\)/.test(passage) && !/\(17\)/.test(passage), 'a paper number survived in the passage');
});

test('only the parenthesised marker form is renumbered', () => {
  // "(160)" and the 16 in "16 January" are not markers.
  const subs = [{ n: 16 }, { n: 17 }];
  eq(M._pbRelabelPassage('On 16 January, (16) of the (160) cases, see (17).', subs),
     'On 16 January, (a) of the (160) cases, see (b).');
});

test('a passage with no markers is left exactly as it was', () => {
  eq(M._pbRelabelPassage('Nothing to renumber here.', [{ n: 21 }]), 'Nothing to renumber here.');
  eq(M._pbRelabelPassage(null, [{ n: 21 }]), '');
});

test('the letters run a, b, c… and skip i, as the editor does elsewhere', () => {
  eq([0, 1, 2, 7, 8].map(M.pbPartLetter), ['a', 'b', 'c', 'h', 'j']);
});

test('past the alphabet a sub-question is DROPPED, never given an empty part', () => {
  // qPartMap inherits forward, so an unlabelled sub-question is filed under the
  // previous one and two option lists share a heading.
  const subs = Array.from({ length: 30 }, (_, i) => ({ n: i + 1, options: ['a', 'b'], correct: -1 }));
  const out = M.pbBuildBlocks({ passage: 'P', subs }, '');
  const mcqs = out.filter(b => b.type === 'mcq');
  eq(mcqs.length, 25, 'the alphabet holds 25 parts');
  ok(mcqs.every(b => b.part), 'a sub-question was written with an empty part');
  eq(M.pbPartOverflow(subs), 5, 'the overflow must be reported, not swallowed');
});

test('an unticked sub-question is saved with NO correct option', () => {
  // Guessing one puts a tick against an option nobody chose, and every class
  // that ever sits the question is marked against the wrong word.
  const p = M._pbParse(PAPER);
  const out = M.pbBuildBlocks(p, '');
  eq(out[2].correctId, null);
});

test('__underscores__ underline, and the passage is escaped', () => {
  eq(M._pbPassageHtml('__Rolled out__ (16)'), '<u>Rolled out</u> (16)');
  ok(M._pbPassageHtml('a < b & c').indexOf('&lt;') >= 0, 'the passage must be escaped');
  eq(M._pbPassageHtml('one\ntwo'), 'one<br>two');
});

// ── 🔤 the comprehension cloze ──────────────────────────────────────────────

const cloze = (text, extras) => ({
  id: 'c1', type: 'clozebank', text, extras: extras || [], startNum: 26, once: true, sortBank: true
});

test('every answer is in the bank, automatically', () => {
  const b = cloze('Managed [[by]] Mandai, home [[to]] more [[than]] 20,000 animals.', ['since']);
  const bank = M.cbBank(b);
  ['by', 'to', 'than', 'since'].forEach(w => ok(bank.indexOf(w) >= 0, 'bank is missing ' + w));
});

test('the bank is sorted, so its order gives nothing away', () => {
  const b = cloze('[[will]] [[and]] [[over]]', ['can']);
  eq(M.cbBank(b), ['and', 'can', 'over', 'will']);
});

test('a duplicate word appears once', () => {
  const b = cloze('[[the]] cat sat on [[the]] mat', ['the', 'The']);
  eq(M.cbBank(b), ['the']);
});

test('the bank letters skip I and O', () => {
  eq(M.CB_LETTERS.indexOf('I'), -1, 'I must be omitted');
  eq(M.CB_LETTERS.indexOf('O'), -1, 'O must be omitted');
  eq(M.CB_LETTERS.slice(0, 9), 'ABCDEFGHJ');
});

test('letter → word and word → letter agree', () => {
  const b = cloze('[[and]] [[by]] [[is]]');
  const m = M.cbBankMap(b);
  eq(m.bank, ['and', 'by', 'is']);
  eq(m.byLetter.A, 'and');
  eq(m.byWord['is'], 'C');
});

test('the bank grid is read DOWN the columns, as the paper sets it', () => {
  const b = cloze('', []);
  b.extras = ['and', 'are', 'as', 'by', 'can', 'for', 'is', 'or', 'over', 'since', 'so', 'than', 'that', 'then', 'will'];
  const grid = M._cbGrid(M.cbBank(b));
  eq(grid.length, 3, 'fifteen words over five columns is three rows');
  eq(grid[0].map(c => c.word), ['and', 'by', 'is', 'since', 'that']);
  eq(grid[0].map(c => c.letter), ['A', 'D', 'G', 'K', 'N'], 'the paper letters exactly these');
  eq(grid[2].map(c => c.word), ['as', 'for', 'over', 'than', 'will']);
});

test('the instruction is generated from the passage and cannot drift from it', () => {
  const b = cloze('[[a]] [[b]] [[c]] [[d]] [[e]] [[f]] [[g]] [[h]] [[i]] [[j]]');
  const intro = M.cbIntro(b);
  ok(/10 blanks, numbered 26 to 35/.test(intro), 'wrong range: ' + intro);
  ok(/\(I\) and \(O\) have been omitted/.test(intro), 'the omitted letters must be stated');
});

test("an author's own instruction is kept", () => {
  const b = cloze('[[a]] [[b]]');
  b.intro = 'My own wording.';
  eq(M.cbIntro(b), 'My own wording.');
});

test('the answer key gives the number, the letter and the word', () => {
  const b = cloze('Managed [[by]] Mandai, home [[to]] more [[than]] 20,000.');
  // bank sorted: by(A) than(B) to(C)
  eq(M.cbAnswerKeyText(b), '26. (A) by   27. (C) to   28. (B) than');
});

test('the numbering follows startNum', () => {
  const b = cloze('[[x]] [[y]]');
  b.startNum = 31;
  ok(M.cbAnswerKeyText(b).indexOf('31. ') === 0, 'first blank should be 31');
  eq(M._cbStart(b), 31);
});

test('a nonsense startNum falls back to 26 rather than numbering from NaN', () => {
  [null, undefined, 0, 1000, 'x'].forEach(v => {
    const b = cloze('[[x]]'); b.startNum = v;
    eq(M._cbStart(b), 26, 'startNum ' + JSON.stringify(v));
  });
});

test('a passage with no blanked word is not a cloze', () => {
  ok(!M.cbHasBlanks(cloze('Nothing is blanked here.')), 'no blanks means no question');
  ok(M.cbHasBlanks(cloze('One [[word]] is.')), 'one blank is a question');
  ok(!M.cbHasBlanks({ type: 'text', text: 'a [[b]] c' }), 'only a clozebank block counts');
});

test('a bank longer than the alphabet is cut, never wrapped onto a used letter', () => {
  const b = cloze('[[a]]');
  b.extras = Array.from({ length: 40 }, (_, i) => 'w' + String(i).padStart(2, '0'));
  eq(M.cbBank(b).length, M.CB_LETTERS.length);
});

test('a malformed cloze never throws', () => {
  [null, undefined, {}, { type: 'clozebank' }, { type: 'clozebank', text: null, extras: null }]
    .forEach(b => { M.cbBank(b); M.cbBankMap(b); M.cbIntro(b); M.cbAnswerKeyText(b); M._cbStart(b); });
});

// ── which block wears the part label ────────────────────────────────────────

test('an MCQ can open a part, so a numbered sub-question needs no empty text block', () => {
  eq(M.qBlockOpensPart({ type: 'mcq', part: '21' }), '21');
  eq(M.qBlockOpensPart({ type: 'image', part: '21' }), '21');
  eq(M.qBlockOpensPart({ type: 'mcq' }), '');
});

test('a lone MCQ prints its own part label', () => {
  const mcq = { type: 'mcq', part: '21' };
  const bs = [{ type: 'text' }, mcq];
  ok(M.qPartLabelFirst(bs, mcq), 'nothing above it opened (21)');
});

test('a wording block and its MCQ under one part label it ONCE', () => {
  // The comprehension shape: the question's wording is a text block and its
  // options an MCQ, both filed under (21). Labelled twice the paper reads
  // "(21) What does…  (21) (1) humans", which looks like a printing fault.
  const txt = { type: 'text', part: '21', content: 'What does the word mean?' };
  const mcq = { type: 'mcq', part: '21' };
  const bs = [{ type: 'text' }, txt, mcq];
  ok(M.qPartLabelFirst(bs, txt), 'the wording prints the label');
  ok(!M.qPartLabelFirst(bs, mcq), 'the MCQ must not repeat it');
});

test('each numbered question still gets its own label', () => {
  const a = { type: 'mcq', part: '21' }, b = { type: 'mcq', part: '22' };
  const bs = [{ type: 'text' }, a, b];
  ok(M.qPartLabelFirst(bs, a), '(21) missing');
  ok(M.qPartLabelFirst(bs, b), '(22) missing');
});

test('a block with no part never prints a label', () => {
  const b = { type: 'mcq' };
  ok(!M.qPartLabelFirst([b], b));
});

test('a malformed block list never throws', () => {
  [null, undefined, [], [null]].forEach(bs => M.qPartLabelFirst(bs, { type: 'mcq', part: '21' }));
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
