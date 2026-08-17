// Regression tests for 🔗 词语搭配 — the word-collocation match (`wm*`). Run with:
//     node tools/wordmatch-tests.mjs            all cases
//     node tools/wordmatch-tests.mjs <name>     one case
//
// It loads the REAL code out of app.js: the item parser, the bank, the number
// each answer resolves to, the printed page, the answer key and the editor's
// one-click answer setter.
//
// Every failure here is silent — the question renders, prints and marks
// without throwing whichever way it goes:
//
//   • The NUMBER is the answer, and it comes from the word's position in the
//     paper's table. Get the order or the 1-based numbering wrong and every
//     item is keyed to a different word than the one the class is told.
//   • `[[了解]]情况` and `发出[[指令]]` put the bracket at opposite ends. Read
//     the two halves the wrong way round and the paper prints 情况（ ）.
//   • An item the author never keyed must stay unkeyed. The moment a missing
//     answer becomes a guess — the first word of the table, say — the paper
//     acquires an answer key that is confidently wrong.
//   • The bank can never be missing one of its own answers: such a question
//     renders perfectly, prints perfectly and cannot be answered at all.
//   • The printed worksheet must show NO answer. The student rendering is a
//     REVIEW rendering with every number already in its bracket, so a print
//     path falling through to it hands out a completed exercise.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');

const slice = (from, to, what) => {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(what + ' not found in app.js — did the banner comments change?');
  return src.slice(a, b);
};

const wm = slice('const WM_START_DEFAULT =', "// ---- the student's page", 'wordmatch core')
  + slice('function _wmOptionsHtml(bank, picked)', 'function wmStudentHtml(block', 'wordmatch dropdown')
  + slice('function wmStudentHtml(block, containerSel, oidxs)', 'function _wmWrapOf(', 'wordmatch student')
  + slice('function wmPrintHtml(block)', '// ---- the editor ---', 'wordmatch print')
  + slice('function wmSetAnswer(id, itemIdx, bankIdx)', '\n}\n', 'wordmatch set answer') + '\n}\n';

const preamble = `
function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
// wmSetAnswer edits the editor's live block list and its textarea.
let blocks = [];
const document = { getElementById: () => null };
function wmSyncEditor() {}
`;

const M = await import('data:text/javascript;base64,' + Buffer.from(
  preamble + wm +
  '\nexport { _wmParseItem, wmItems, wmHasItems, _wmSplitBank, wmBank, wmAnswerNum, wmUnanswered,'
  + ' _wmStart, wmIntro, wmProblems, _wmGrid, _wmOptionsHtml, wmStudentHtml, wmPrintHtml,'
  + ' wmAnswerKeyText, wmSetAnswer, blocks, WM_START_DEFAULT, WM_COLS };'
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

// The section from the screenshot, whole: six words, four items, numbered from 7.
const BANK = '负责\n照顾\n了解\n弟妹\n指令\n国旗';
const TEXT = '[[了解]]情况\n[[负责]]值日\n发出[[指令]]\n挥动[[国旗]]';
const paper = (extra) => Object.assign({ type: 'wordmatch', id: 'b1', text: TEXT, bank: BANK, startNum: 7 }, extra || {});

// ── the two shapes of item ───────────────────────────────────────────────────
test('the bracket comes BEFORE the word in one item and after it in the next', () => {
  const items = M.wmItems(paper());
  eq(items.length, 4, 'four items');
  eq([items[0].before, items[0].answer, items[0].after], ['', '了解', '情况'], '（　）情况');
  eq([items[2].before, items[2].answer, items[2].after], ['发出', '指令', ''], '发出（　）');
});

test('an item with nothing either side of the bracket is not a question', () => {
  // An author mid-edit. Counting it would put an unanswerable row on the paper.
  eq(M.wmItems({ type: 'wordmatch', text: '[[了解]]情况\n[[]]\n\n[[负责]]值日' }).length, 2, 'two real items');
});

test('a line with no bracket at all is dropped', () => {
  eq(M.wmItems({ type: 'wordmatch', text: '这是说明文字\n[[了解]]情况' }).length, 1, 'one item');
});

// ── the table and the numbers ────────────────────────────────────────────────
test('the table keeps the PAPER\'S order, and the numbers follow it', () => {
  const bank = M.wmBank(paper());
  eq(bank, ['负责', '照顾', '了解', '弟妹', '指令', '国旗'], 'paper order');
  eq(M.wmAnswerNum(bank, '了解'), 3, 'Q7 is (3)');
  eq(M.wmAnswerNum(bank, '负责'), 1, 'Q8 is (1)');
  eq(M.wmAnswerNum(bank, '指令'), 5, 'Q9 is (5)');
  eq(M.wmAnswerNum(bank, '国旗'), 6, 'Q10 is (6)');
});

test('the numbering is 1-based, and an unknown word is 0', () => {
  // 0 is what everything downstream reads as "no answer"; returning 0-based
  // indexes here would key every first word as unanswered.
  eq(M.wmAnswerNum(['负责', '照顾'], '负责'), 1, 'first word is 1');
  eq(M.wmAnswerNum(['负责', '照顾'], '毛病'), 0, 'unknown is 0');
});

test('the table is read ACROSS, as this paper sets it', () => {
  const rows = M._wmGrid(['负责', '照顾', '了解', '弟妹', '指令', '国旗']);
  eq(rows.length, 2, 'two rows');
  eq(rows[0].map(c => c.n + c.word), ['1负责', '2照顾', '3了解'], 'first row');
  eq(rows[1].map(c => c.n + c.word), ['4弟妹', '5指令', '6国旗'], 'second row');
});

test('the table accepts the AI\'s array and the author\'s typing alike', () => {
  eq(M._wmSplitBank(['负责', '照顾']), ['负责', '照顾'], 'array');
  eq(M._wmSplitBank('负责、照顾，了解\n弟妹'), ['负责', '照顾', '了解', '弟妹'], 'punctuation and lines');
});

// ── the rule that makes a question answerable ────────────────────────────────
test('an answer the table is missing is ADDED to it, never dropped', () => {
  // A bank without its own answer renders perfectly, prints perfectly and
  // cannot be answered — the same rule the word-bank cloze is built on.
  const b = { type: 'wordmatch', text: '[[了解]]情况\n[[负责]]值日', bank: '负责\n照顾' };
  const bank = M.wmBank(b);
  ok(bank.indexOf('了解') >= 0, 'the answer is missing from the bank: ' + bank.join());
  ok(M.wmAnswerNum(bank, '了解') > 0, 'and so has no number');
});

test('…and the author is told, because it means the table was mistranscribed', () => {
  const probs = M.wmProblems({ type: 'wordmatch', text: '[[了解]]情况', bank: '负责\n照顾' });
  ok(probs.join(' ').indexOf('了解') >= 0, 'not reported: ' + probs.join(' | '));
});

test('a duplicated word in the table is only numbered once', () => {
  eq(M.wmBank({ type: 'wordmatch', text: '', bank: '负责\n负责\n照顾' }), ['负责', '照顾'], 'deduped');
});

// ── an unset answer stays unset ──────────────────────────────────────────────
test('an item with an empty bracket is never given a guessed answer', () => {
  const b = { type: 'wordmatch', text: '[[]]情况\n[[负责]]值日', bank: BANK, startNum: 7 };
  eq(M.wmUnanswered(b), 1, 'one unanswered');
  eq(M.wmAnswerNum(M.wmBank(b), M.wmItems(b)[0].answer), 0, 'no number for it');
  ok(M.wmAnswerKeyText(b).indexOf('7. — not set') >= 0, 'the key must say so: ' + M.wmAnswerKeyText(b));
});

// ── the printed page ─────────────────────────────────────────────────────────
test('the printed sheet gives NOTHING away', () => {
  const html = M.wmPrintHtml(paper());
  for (const w of ['了解', '负责', '指令', '国旗']) {
    // Every word is in the printed TABLE, so it must appear — what must not is
    // a number sitting in a bracket.
    ok(html.indexOf(w) >= 0, 'the table lost ' + w);
  }
  ok(html.indexOf('（3）') < 0 && html.indexOf('(3)') < 0, 'an answer number is printed on the worksheet');
  ok(/（(?:&nbsp;)+）/.test(html), 'no empty bracket to write in: ' + html);
});

test('the printed items keep the paper\'s numbering and both bracket positions', () => {
  const html = M.wmPrintHtml(paper());
  ok(html.indexOf('<b>7</b>') >= 0 && html.indexOf('<b>10</b>') >= 0, 'items are numbered 7–10');
  const q9 = html.slice(html.indexOf('<b>9</b>'), html.indexOf('<b>10</b>'));
  ok(q9.indexOf('发出') < q9.indexOf('print-wm-bracket'), '发出（　）printed the wrong way round');
});

test('a block with no items prints nothing at all', () => {
  eq(M.wmPrintHtml({ type: 'wordmatch', text: '', bank: BANK }), '', 'empty block');
});

// ── the answer key ───────────────────────────────────────────────────────────
test('the key numbers from the PAPER\'s first number and names the whole phrase', () => {
  const key = M.wmAnswerKeyText(paper());
  ok(key.indexOf('7. （3）了解情况') >= 0, 'Q7 wrong: ' + key);
  ok(key.indexOf('9. （5）发出指令') >= 0, 'Q9 wrong: ' + key);
  ok(key.indexOf('10. （6）挥动国旗') >= 0, 'Q10 wrong: ' + key);
  ok(key.indexOf('1. ') !== 0, 'the key must not renumber from 1: ' + key);
});

// ── the student's page ───────────────────────────────────────────────────────
test('every bracket offers the WHOLE table, numbered', () => {
  const html = M._wmOptionsHtml(['负责', '照顾', '了解'], -1);
  ok(html.indexOf('（1）负责') >= 0 && html.indexOf('（3）了解') >= 0, 'options: ' + html);
});

test('the empty choice is -1, never an empty string', () => {
  // Number('') is 0, which is option (1): an unanswered item would be marked
  // against a word the student never picked. Same trap as 短文填空's.
  ok(M._wmOptionsHtml(['负责'], -1).indexOf('<option value="-1">') >= 0, 'empty choice must be -1');
});

test('a used word is NOT removed from the other items\' lists', () => {
  // Nothing on the paper forbids using a word twice, and removing it would
  // hand the student an elimination the paper does not give them.
  const html = M.wmStudentHtml(paper(), '#x', [0, 1, 2, 3]);
  eq((html.match(/（3）了解/g) || []).length, 4, 'every item should still offer 了解');
});

test('the student page shows no answers and no ticks', () => {
  const html = M.wmStudentHtml(paper(), '#x', [0, 1, 2, 3]);
  no(/selected/.test(html), 'an option is pre-selected: the answer is given away');
});

// ── the instruction line ─────────────────────────────────────────────────────
test('the generated instruction names the table\'s real range', () => {
  ok(M.wmIntro(paper()).indexOf('1–6') >= 0, 'range wrong: ' + M.wmIntro(paper()));
  const five = M.wmIntro({ type: 'wordmatch', text: '[[了解]]情况', bank: '负责\n照顾\n了解\n弟妹\n指令' });
  ok(five.indexOf('1–5') >= 0, 'the range must follow the table: ' + five);
});

test('an author\'s own instruction is left alone', () => {
  eq(M.wmIntro(paper({ intro: '选出适当的词语。' })), '选出适当的词语。', 'typed intro');
});

// ── the editor's one-click answer ────────────────────────────────────────────
test('clicking a word sets that item\'s answer, and clicking it again clears it', () => {
  const b = { id: 'b1', type: 'wordmatch', text: '[[]]情况\n发出[[]]', bank: BANK };
  M.blocks.length = 0; M.blocks.push(b);
  M.wmSetAnswer('b1', 0, 2);                       // 3 了解
  eq(M.wmItems(b)[0].answer, '了解', 'set');
  eq(M.wmItems(b)[1].answer, '', 'the other item must not move');
  M.wmSetAnswer('b1', 0, 2);
  eq(M.wmItems(b)[0].answer, '', 'clicking the same word again clears it');
});

test('setting an answer keeps what is printed either side of the bracket', () => {
  const b = { id: 'b1', type: 'wordmatch', text: '发出[[]]', bank: BANK };
  M.blocks.length = 0; M.blocks.push(b);
  M.wmSetAnswer('b1', 0, 4);                       // 5 指令
  eq(b.text, '发出[[指令]]', 'the phrase was rebuilt wrong: ' + b.text);
});

// ── the wiring ───────────────────────────────────────────────────────────────
test('BOTH print builders carry an explicit case for wordmatch', () => {
  // Falling through to the student rendering prints a REVIEW rendering — the
  // whole exercise already filled in.
  const builders = ['function doPrintWorksheetOpen', 'function buildWorksheetHtml'];
  for (const fn of builders) {
    const a = src.indexOf(fn);
    ok(a >= 0, fn + ' not found');
    const b = src.indexOf('\nfunction ', a + 10);
    const body = src.slice(a, b < 0 ? src.length : b);
    ok(body.indexOf("case 'wordmatch':") >= 0, fn + " has no explicit `case 'wordmatch'`");
    ok(body.indexOf('wmPrintHtml(block)') >= 0, fn + ' does not print through wmPrintHtml');
    ok(body.indexOf('wmAnswerKeyText(block)') >= 0, fn + ' does not put the answers on the key');
  }
});

test('the editor handlers are exported to window', () => {
  // The module has its own scope, so an inline onclick with no window
  // assignment is a control that throws ReferenceError and looks dead.
  for (const f of ['wmSetAnswer', 'wmInsertItem', 'wmCheck', 'wmClearAll', 'wmSyncEditor']) {
    ok(src.indexOf('window.' + f + ' = ' + f + ';') >= 0, f + ' is not on window');
  }
});

test('the block type is offered, styled and understood', () => {
  const html = fs.readFileSync(new URL('../index.html', import.meta.url).pathname, 'utf8');
  ok(html.indexOf("addBlock('wordmatch')") >= 0, 'no 词语搭配 button in the add-block menu');
  ok(html.indexOf('.wm-pick {') >= 0, 'no screen CSS for the drop-down');
  ok(html.indexOf('.print-wm-bank {') >= 0, 'no print CSS for the table');
  ok(/\.wm-pick\s*{[^}]*appearance:\s*auto/.test(html),
    'the drop-down needs appearance:auto — Tailwind preflight strips the arrow off it');
  ok(src.indexOf("t === 'wordmatch'") >= 0, 'buildBlocksFromAi cannot build one from a screenshot');
  ok(src.indexOf('"type":"wordmatch"') >= 0, 'no prompt rule teaching the AI to read the section');
});

// ── run ──────────────────────────────────────────────────────────────────────
const only = process.argv[2];
let pass = 0, fail = 0;
for (const c of cases) {
  if (only && c.name.indexOf(only) < 0) continue;
  try { c.fn(); pass++; console.log('  ok   ' + c.name); }
  catch (e) { fail++; console.log('  FAIL ' + c.name + '\n       ' + e.message); }
}
console.log((fail ? '❌ ' : '✅ ') + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
