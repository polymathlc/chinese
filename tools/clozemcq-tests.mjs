// Regression tests for 📝 短文填空 — the inline-options cloze (`cm*`). Run with:
//     node tools/clozemcq-tests.mjs            all cases
//     node tools/clozemcq-tests.mjs <name>     one case
//
// It loads the REAL code out of app.js: `_cmParse`, `cmBlanks`, `cmUnanswered`,
// `_cmStart`, `cmAnswerKeyText`, `cmPrintHtml`, `cmSetCorrect`.
//
// Every failure here is silent, and three of them are the same failure the
// passage builder exists to prevent, one step worse:
//
//   • A blank parsed with the wrong correct option marks a whole class against
//     the wrong word, and the question renders and prints perfectly either way.
//   • A blank with NO ticked option must stay untricked. The moment a missing
//     answer is turned into a guess — index 0, say — the paper acquires an
//     answer key that is confidently wrong, and nothing on screen says so.
//   • The printed worksheet must show NO answer. The read-only rendering paints
//     the correct option green, so a print path falling through to it hands the
//     student a worksheet with every answer already marked.
//   • The answer key numbers from the PAPER's own first number (16 in these
//     papers, not 1). A key numbered from 1 against a paper numbered from 16 is
//     a teacher marking question 16 against the answer to question 1.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');

const slice = (from, to, what) => {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(what + ' not found in app.js — did the banner comments change?');
  return src.slice(a, b);
};

// The parse, the key and the print builder — plus the two functions that build
// the student's DROP-DOWN, which is where the choice is now read from and
// therefore where a silently wrong answer would come from.
const cm = slice('const CM_START_DEFAULT =', '// ---- the student\'s passage', 'clozemcq parse')
  + slice('function _cmOptionsHtml(options, picked)', 'function _cmWrapOf(', 'clozemcq dropdown')
  + slice('function cmPrintHtml(block)', '// ---- the editor ---', 'clozemcq print')
  + slice('function cmSetCorrect(id, blankIdx, optIdx)', '\n}\n', 'clozemcq set correct') + '\n}\n';

const preamble = `
function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
// cmSetCorrect edits the editor's live block list and its textarea.
let blocks = [];
const document = { getElementById: () => null };
function cmSyncEditor() {}
`;

const M = await import('data:text/javascript;base64,' + Buffer.from(
  preamble + cm +
  '\nexport { _cmParse, _cmParseBlank, cmBlanks, cmHasBlanks, cmUnanswered, _cmStart, cmIntro, cmPrintHtml, cmAnswerKeyText, cmSetCorrect, _cmOptionsHtml, cmStudentHtml, blocks, CM_START_DEFAULT };'
).toString('base64'));

// ── helpers ──────────────────────────────────────────────────────────────────
const cases = [];
const test = (name, fn) => cases.push({ name, fn });
function ok(v, msg) { if (!v) throw new Error(msg || 'expected truthy, got ' + v); }
function no(v, msg) { if (v) throw new Error(msg || 'expected falsy, got ' + v); }
function eq(a, b, msg) {
  const A = JSON.stringify(a), B = JSON.stringify(b);
  if (A !== B) throw new Error((msg ? msg + ': ' : '') + 'expected ' + B + ', got ' + A);
}
const blk = (text, extra) => Object.assign({ type: 'clozemcq', text }, extra || {});

// The passage from the screenshot, cut to the first two blanks.
const PAPER = '课外活动是学生生活的一部分。教室里还有学生在下棋、画画等。'
  + '[[总算|就算|*不管|尽管]]是体育、艺术，还是团队活动，课外活动的种类非常丰富。'
  + '它们让学生课后的生活变得更[[坚强|*充实|充足|顽强]]和有趣。';

// ── the parse ────────────────────────────────────────────────────────────────

test('options are split on the pipe and the * is the answer', () => {
  const b = M._cmParseBlank('总算|就算|*不管|尽管');
  eq(b.options, ['总算', '就算', '不管', '尽管']);
  eq(b.correct, 2);
});

test('the * never survives into the option the student reads', () => {
  // It is markup. Left in, the correct option is visibly starred on screen and
  // on paper — the answer, printed on the question.
  M._cmParse(PAPER).filter(p => p.type === 'blank').forEach(p =>
    p.options.forEach(o => no(o.includes('*'), 'a * leaked into ' + JSON.stringify(o))));
});

test('a blank with no * has no answer, and is never given one', () => {
  const b = M._cmParseBlank('总算|就算|不管|尽管');
  eq(b.correct, -1, 'an unmarked blank must not resolve to an option');
  eq(M.cmUnanswered(blk('x[[a|b|c|d]]y')), 1);
});

test('only the FIRST * counts', () => {
  // Two asterisks is an authoring slip, and the alternative — taking the last,
  // or refusing the blank entirely — loses the author's first choice silently.
  eq(M._cmParseBlank('*甲|乙|*丙').correct, 0);
});

test('the passage text around the blanks is preserved exactly', () => {
  eq(M._cmParse(PAPER).map(p => p.type === 'blank' ? '' : p.text).join(''),
     PAPER.replace(/\[\[[\s\S]*?\]\]/g, ''));
});

test('a blank needs something to choose between', () => {
  // One option is not a question, and [[]] is an author mid-edit. Neither may
  // reach the student as a live blank or be counted on the key.
  eq(M.cmBlanks(blk('a[[只有一个]]b')).length, 0);
  eq(M.cmBlanks(blk('a[[]]b')).length, 0);
  no(M.cmHasBlanks(blk('a[[]]b')));
});

test('the screenshot passage parses to two answered blanks', () => {
  const bs = M.cmBlanks(blk(PAPER));
  eq(bs.length, 2);
  eq(bs[0].options[bs[0].correct], '不管');
  eq(bs[1].options[bs[1].correct], '充实');
  eq(M.cmUnanswered(blk(PAPER)), 0);
});

test('a block with no blanks is not a cloze', () => {
  no(M.cmHasBlanks(blk('课外活动是学生生活的一部分。')));
  no(M.cmHasBlanks({ type: 'text', text: 'a[[b|c]]d' }), 'the type must still be checked');
});

test('nothing throws on a malformed block', () => {
  [null, undefined, {}, { type: 'clozemcq' }, blk(''), blk(null)].forEach(b => {
    M.cmBlanks(b); M.cmHasBlanks(b); M.cmUnanswered(b); M._cmStart(b); M.cmAnswerKeyText(b);
  });
});

// ── numbering ────────────────────────────────────────────────────────────────

test('numbering starts where the PAPER starts it', () => {
  eq(M._cmStart(blk(PAPER)), M.CM_START_DEFAULT, 'these papers open 短文填空 at 16');
  eq(M._cmStart(blk(PAPER, { startNum: 21 })), 21);
});

test('a nonsense start number falls back rather than printing it', () => {
  [0, -3, 1000, 'x', null, NaN].forEach(v => eq(M._cmStart(blk(PAPER, { startNum: v })), M.CM_START_DEFAULT, 'startNum ' + v));
  eq(M._cmStart(blk(PAPER, { startNum: '21' })), 21, 'a numeric string is a real number');
});

// ── the answer key ───────────────────────────────────────────────────────────

test('the key carries the number, the option NUMBER and the word', () => {
  // The marking scheme answers "16 (3)", so the option's number is part of the
  // answer — the word alone leaves the teacher counting brackets.
  const key = M.cmAnswerKeyText(blk(PAPER));
  ok(key.includes('16. (3) 不管'), key);
  ok(key.includes('17. (2) 充实'), key);
});

test('the key follows a custom start number', () => {
  ok(M.cmAnswerKeyText(blk(PAPER, { startNum: 21 })).startsWith('21. '), 'the key must not number from 1');
});

test('a blank with no answer says so on the key', () => {
  // Never a number. "16. (1)" against a blank nobody ticked is an answer key
  // that is confidently wrong.
  const key = M.cmAnswerKeyText(blk('a[[甲|乙|丙|丁]]b'));
  ok(key.includes('not set'), key);
  no(/\(\d\)/.test(key), 'an option number was invented: ' + key);
});

test('a block with no blanks contributes no key at all', () => {
  eq(M.cmAnswerKeyText(blk('课外活动是学生生活的一部分。')), '');
});

// ── the printed worksheet ────────────────────────────────────────────────────

test('the printed page gives NOTHING away', () => {
  const html = M.cmPrintHtml(blk(PAPER));
  ok(html.includes('不管'), 'the option itself must still print');
  no(html.includes('*'), 'the answer marker printed: ' + html);
  no(/class="[^"]*\bon\b/.test(html), 'the correct option is highlighted on the worksheet');
  no(html.includes('is-right'), 'a marked-up answer reached the paper');
});

test('the printed page numbers each blank and prints all four options', () => {
  const html = M.cmPrintHtml(blk(PAPER));
  ok(html.includes('<b>16</b>'), 'blank 16 is not numbered: ' + html);
  ok(html.includes('<b>17</b>'), 'blank 17 is not numbered');
  ['总算', '就算', '不管', '尽管'].forEach((o, i) =>
    ok(html.includes((i + 1) + ' ' + o), 'option ' + (i + 1) + ' ' + o + ' missing from the paper'));
});

test('the printed page carries the instruction line', () => {
  ok(M.cmPrintHtml(blk(PAPER)).includes('根据短文'), 'the 短文填空 instruction is missing');
  ok(M.cmPrintHtml(blk(PAPER, { intro: '自定说明。' })).includes('自定说明。'), "the author's own instruction is ignored");
});

test('the printed passage is escaped', () => {
  ok(M.cmPrintHtml(blk('<b>x</b>[[甲|乙]]')).includes('&lt;b&gt;'), 'raw HTML reached the printed page');
});

// ── ticking the answer in the editor ─────────────────────────────────────────

function setCorrect(text, blankIdx, optIdx) {
  M.blocks.length = 0;
  M.blocks.push({ id: 'b1', type: 'clozemcq', text });
  M.cmSetCorrect('b1', blankIdx, optIdx);
  return M.blocks[0].text;
}

test('ticking an option writes the * on the RIGHT blank', () => {
  const t = 'a[[甲|乙|丙|丁]]b[[戊|己|庚|辛]]c';
  eq(setCorrect(t, 1, 2), 'a[[甲|乙|丙|丁]]b[[戊|己|*庚|辛]]c');
  eq(setCorrect(t, 0, 3), 'a[[甲|乙|丙|*丁]]b[[戊|己|庚|辛]]c');
});

test('ticking moves the answer rather than adding a second', () => {
  eq(setCorrect('a[[甲|*乙|丙]]b', 0, 2), 'a[[甲|乙|*丙]]b');
});

test('ticking the current answer again clears it', () => {
  // An author who ticked the wrong option must be able to get back to "not
  // set", or the question keeps an answer nobody stands behind.
  eq(setCorrect('a[[甲|*乙|丙]]b', 0, 1), 'a[[甲|乙|丙]]b');
  eq(M.cmUnanswered(blk('a[[甲|乙|丙]]b')), 1);
});

test('ticking leaves the passage around the blank untouched', () => {
  const t = '课外活动。\n\n它们让学生的生活变得更[[坚强|充实|充足|顽强]]和有趣。';
  const out = setCorrect(t, 0, 1);
  eq(out.replace(/\*/g, ''), t, 'the passage changed beyond the marker');
  eq((out.match(/\n/g) || []).length, 2, 'paragraph breaks were lost');
});

test('a half-written blank is skipped, not counted', () => {
  // [[]] is not a blank, so the SECOND real blank is index 1 — if the empty one
  // were counted the tick would land on the wrong question entirely.
  eq(setCorrect('a[[]]b[[甲|乙]]c[[丙|丁]]d', 1, 1), 'a[[]]b[[甲|乙]]c[[丙|*丁]]d');
});

test('ticking out of range changes nothing', () => {
  const t = 'a[[甲|乙|丙]]b';
  eq(setCorrect(t, 9, 0), t);
});

// ── the student's DROP-DOWN ──────────────────────────────────────────────────
// The choice is read straight off the <select>, so what the option VALUES are
// is what the answer is. Every failure here marks a right answer wrong while
// the passage on screen looks perfectly normal.

test('every option keeps the PAPER\'s number', () => {
  // The marking scheme answers "16 (3)", so the number is half the answer: a
  // list showing only the words leaves the student unable to check their work.
  const h = M._cmOptionsHtml(['总算', '就算', '不管', '尽管'], -1);
  ok(h.indexOf('（1）总算') > 0, h);
  ok(h.indexOf('（3）不管') > 0, h);
  eq((h.match(/<option/g) || []).length, 5, 'four choices and the empty one');
});

test('the empty choice is -1, never 0', () => {
  // Number('') is 0, which is option (1). An unanswered blank read as "(1)"
  // marks the student against a word they never picked.
  const h = M._cmOptionsHtml(['甲', '乙'], -1);
  ok(/<option value="-1">—<\/option>/.test(h), h);
  ok(h.indexOf('selected') < 0, 'nothing is chosen until the student chooses');
});

test('a blank that already holds a choice keeps it', () => {
  const h = M._cmOptionsHtml(['甲', '乙', '丙'], 2);
  ok(/<option value="2" selected>（3）丙<\/option>/.test(h), h);
  eq((h.match(/selected/g) || []).length, 1, 'exactly one option can be chosen');
});

test('the passage renders one drop-down per blank, numbered from the paper', () => {
  const html = M.cmStudentHtml({ id: 'b1', text: '课外活动[[总算|就算|*不管|尽管]]是体育[[甲|*乙]]艺术。', startNum: 16 }, '#c', [0, 1]);
  eq((html.match(/class="cm-pick"/g) || []).length, 2, 'a blank lost its drop-down');
  ok(/data-cm-b="0"/.test(html) && /data-cm-b="1"/.test(html), 'the blanks are not keyed by index');
  ok(html.indexOf('>16</b>') > 0 && html.indexOf('>17</b>') > 0, 'the paper numbers from 16, not from 1');
});

test('the drop-down never gives the answer away', () => {
  // The author's tick is a `*` in the markup. Leak it into the list and every
  // blank prints its own answer.
  const html = M.cmStudentHtml({ id: 'b1', text: 'a[[总算|就算|*不管|尽管]]b', startNum: 16 }, '#c', [0]);
  ok(html.indexOf('*') < 0, 'the asterisk reached the student');
  ok(html.indexOf('selected') < 0, 'the correct option arrived pre-selected');
  ok(html.indexOf('（3）不管') > 0, 'and the option itself must still be offered');
});

test('a blank with fewer than two choices is not a blank', () => {
  const html = M.cmStudentHtml({ id: 'b1', text: 'a[[单]]b[[甲|乙]]c', startNum: 16 }, '#c', [0]);
  eq((html.match(/class="cm-pick"/g) || []).length, 1, 'a one-word bracket is not a question');
});

test('the drop-down is wired to the app\'s ONE change listener', () => {
  // This app builds its DOM continuously, so the pick is read by a delegated
  // listener on the document. Lose that wiring and every blank still renders,
  // still opens, still lets a word be chosen — and nothing is ever recorded.
  ok(/addEventListener\('change'[\s\S]{0,240}closest\('\.cm-pick'\)[\s\S]{0,120}cmPicked\(/.test(src),
    'nothing calls cmPicked when a blank changes');
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
