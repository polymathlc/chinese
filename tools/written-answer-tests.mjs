// Regression tests for 阅读理解问答 — a passage answered IN WRITING. Run with:
//     node tools/written-answer-tests.mjs            all cases
//     node tools/written-answer-tests.mjs <name>     one case
//
// It loads the REAL `qaMarks` / `qaWeight` / `_openTotalWeight`,
// `_openPhotoList`, `_openAnswerMedia` and the shared prompt fragment out of
// app.js, with a small stand-in DOM for the handwriting pads.
//
// Three things here fail silently, and all three end in a mark the student
// cannot argue with because nothing on screen looks wrong:
//
//  • THE IMAGE ORDER. The marker is handed N images and a note saying what each
//    one is BY NUMBER. Let the note and the array drift apart and item (a) is
//    marked against item (d)'s handwriting — a wrong mark, delivered fluently.
//  • THE WEIGHT. A 4分 question is worth four times a 1分 one, and a question
//    with no marks at all is worth 1 — every question authored before 分
//    existed. Get the default wrong and the whole bank scores 0 out of 0.
//  • THE PROMPT. A page of ruled answer boxes read as multiple choice comes
//    back as four invented options per question: a comprehension paper turned
//    into an answerable-looking quiz that tests nothing the paper asked.
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

const section = [
  cut('const QA_MARKS_MAX =', 'function _openSection(', 'marks helpers'),
  cut('function _hwCanvas(containerSel, oidx)', '// The canvas is sized in CSS', 'pad lookup'),
  cut('function hwHasInk(containerSel, oidx)', 'function hwLockIn(', 'ink export'),
  cut('const _openPhoto = {};', 'function openPhotoBarHtml(', 'photo store'),
  cut('function _openAnswerMedia(containerSel, opts = {})', '\nfunction renderOpenPracticeBody', 'marking media'),
  cut('function _setPartResult(containerSel', '// Once a part is marked', 'part results'),
  cut('function _partsPromptRules()', '\n// The rectangle-selection', 'prompt rules'),
  `
function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
const _openItemsStore = {}, _openMcqStore = {}, _openPartResults = {};
// A stand-in for the handwriting pads on screen: one registry, queried the same
// way the real DOM is, so the ORDER _openAnswerMedia walks them in is the order
// under test.
const _pads = {};   // containerSel -> [ { oidx, ink } ]
const document = {
  querySelectorAll(sel) {
    const m = /^(\\S+) \\.hw-pad$/.exec(sel);
    if (!m) return [];
    return (_pads[m[1]] || []).map(p => ({ getAttribute: k => (k === 'data-hw-canvas' ? p.oidx : null) }));
  },
  querySelector(sel) {
    const m = /^(\\S+) \\.hw-pad\\[data-hw-canvas="([^"]+)"\\]$/.exec(sel);
    if (!m) return null;
    const pad = (_pads[m[1]] || []).find(p => p.oidx === m[2]);
    if (!pad) return null;
    return {
      _hwStrokes: pad.ink ? [[{ x: 1, y: 1 }]] : [],
      toDataURL: () => 'data:image/png;base64,' + pad.ink
    };
  }
};
`
].join('\n');

const M = new Function(section +
  '\nreturn { qaMarks, qaWeight, qaMarksLabel, qaPrintMarksHtml, _openPhotoList, _openAnswerMedia, _openTotalWeight, _setPartResult, _partsPromptRules, _openPhoto, _openItemsStore, _openMcqStore, _openPartResults, _pads };')();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const ok = (cond, what) => { if (!cond) throw new Error(what); };
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};
const CS = '#practiceContainer';
const reset = () => {
  M._openPhoto[CS] = [];
  M._pads[CS] = [];
  M._openItemsStore[CS] = [];
  M._openMcqStore[CS] = [];
  M._openPartResults[CS] = {};
};
const page = n => ({ dataUrl: 'data:image/jpeg;base64,p' + n, mimeType: 'image/jpeg', data: 'p' + n, name: 'page' + n });

// ── 分: what the paper gives each answer ────────────────────────────────────

test('marks are the paper\'s own allocation, within sane bounds', () => {
  eq(M.qaMarks({ marks: 2 }), 2);
  eq(M.qaMarks({ marks: '4' }), 4, 'a number typed into the field arrives as a string');
  eq(M.qaMarks({ marks: 2.6 }), 3, 'rounded, never stored as a fraction of a mark');
  eq(M.qaMarks({ marks: 0 }), 0, '0 means not set');
  eq(M.qaMarks({ marks: -3 }), 0);
  eq(M.qaMarks({ marks: 999 }), 0, 'past the cap it is a typo, not an allocation');
  eq(M.qaMarks({}), 0);
  eq(M.qaMarks(null), 0);
});

test('a question with NO marks is still worth one point', () => {
  // Every question authored before 分 existed. Get this wrong and the whole
  // bank is suddenly scored out of zero.
  eq(M.qaWeight(0), 1);
  eq(M.qaWeight(undefined), 1);
  eq(M.qaWeight(null), 1);
  eq(M.qaWeight(4), 4);
});

test('the label is the paper\'s, in full-width brackets', () => {
  eq(M.qaMarksLabel(2), '（2分）');
  eq(M.qaMarksLabel(0), '');
  ok(M.qaPrintMarksHtml({ marks: 3 }).indexOf('（3分）') >= 0, 'the printed paper drops the marks');
  eq(M.qaPrintMarksHtml({}), '', 'a question with no marks prints exactly as it always did');
});

test('the question is out of the PAPER\'s total', () => {
  reset();
  // Q34–Q40 of the paper in the screenshot: 2+2+2+4+4+4+4 = 22分.
  M._openItemsStore[CS] = [2, 2, 2, 4, 4, 4, 4].map(m => ({ marks: m }));
  eq(M._openTotalWeight(CS), 22);
});

test('an unmarked question is still out of the number of parts', () => {
  reset();
  M._openItemsStore[CS] = [{}, {}, {}];
  M._openMcqStore[CS] = [{ blockId: 'x' }, { blockId: 'y' }];
  eq(M._openTotalWeight(CS), 5, 'three answers and two MCQs is out of 5, as it always was');
});

test('a part result carries what it was out of', () => {
  reset();
  M._setPartResult(CS, 'open:0', 'correct', 4, 'model', 'student', 4);
  M._setPartResult(CS, 'mcq:b1', 'correct', 1, 'x', 'y');
  eq(M._openPartResults[CS]['open:0'].w, 4);
  eq(M._openPartResults[CS]['mcq:b1'].w, 1, 'a part with no weight is worth one');
});

// ── the answer script: several photos, and handwriting ──────────────────────

test('the photo store reads as a LIST however it was written', () => {
  reset();
  eq(M._openPhotoList(CS), []);
  M._openPhoto[CS] = [page(1), page(2), page(3)];
  eq(M._openPhotoList(CS).length, 3, 'three pages of a 阅读理解 script');
  // Snap & Mark hands ONE photo straight in; it must read the same way.
  M._openPhoto[CS] = page(9);
  eq(M._openPhotoList(CS).length, 1);
  M._openPhoto[CS] = [page(1), { dataUrl: 'x' }, null];
  eq(M._openPhotoList(CS).length, 1, 'a half-read file is not a page');
});

test('every page goes to the marker, in the order they were added', () => {
  reset();
  M._openPhoto[CS] = [page(1), page(2), page(3)];
  const shot = M._openAnswerMedia(CS);
  eq(shot.media.map(m => m.data), ['p1', 'p2', 'p3'], 'a page was dropped or reordered');
  eq(shot.pageCount, 3);
  ok(/Image 1: page 1/.test(shot.note) && /Image 3: page 3/.test(shot.note), shot.note);
});

test('the note NUMBERS every image, and the numbers match the array', () => {
  // The one that fails silently: the marker reads item (a) against item (d)'s
  // handwriting and marks it wrong, fluently, with nothing on screen amiss.
  reset();
  M._openPhoto[CS] = [page(1)];
  M._openItemsStore[CS] = [{ label: '(a) Answer' }, { label: '(b) Answer' }, { label: '(c) Answer' }];
  M._pads[CS] = [{ oidx: '0', ink: 'inkA' }, { oidx: '1', ink: '' }, { oidx: '2', ink: 'inkC' }];
  const shot = M._openAnswerMedia(CS);
  eq(shot.media.map(m => m.data), ['p1', 'inkA', 'inkC'], 'an empty pad must not take an image number');
  eq(shot.inkCount, 2);
  ok(/Image 2: the student's HANDWRITTEN answer for item 0 \[\(a\) Answer\]/.test(shot.note), shot.note);
  ok(/Image 3: the student's HANDWRITTEN answer for item 2 \[\(c\) Answer\]/.test(shot.note), shot.note);
  ok(shot.note.indexOf('item 1') < 0, 'a pad with no ink was described to the marker anyway');
});

test('marking ONE part sends only THAT part\'s handwriting', () => {
  // Another part's ink is another part's answer. Sent along, it is the wrong
  // answer marked against this question.
  reset();
  M._openItemsStore[CS] = [{ label: '(a) Answer' }, { label: '(b) Answer' }];
  M._pads[CS] = [{ oidx: '0', ink: 'inkA' }, { oidx: '1', ink: 'inkB' }];
  const shot = M._openAnswerMedia(CS, { oidx: '1' });
  eq(shot.media.map(m => m.data), ['inkB']);
  ok(/item 1/.test(shot.note) && shot.note.indexOf('item 0') < 0, shot.note);
});

test('a multiple-choice part gets the pages and no pads at all', () => {
  reset();
  M._openPhoto[CS] = [page(1)];
  M._openItemsStore[CS] = [{ label: '(a) Answer' }];
  M._pads[CS] = [{ oidx: '0', ink: 'inkA' }];
  const shot = M._openAnswerMedia(CS, { inks: false });
  eq(shot.media.map(m => m.data), ['p1'], 'an option is circled on the paper, not written on a pad');
  eq(shot.inkCount, 0);
});

test('nothing attached is nothing sent — and no note', () => {
  reset();
  const shot = M._openAnswerMedia(CS);
  eq(shot.media, []);
  eq(shot.note, '');
  eq(shot.pageCount, 0);
});

test('the note tells the marker to ignore handwriting quality', () => {
  // A P3 hand marked down for neatness is a wrong mark on a right answer.
  reset();
  M._openPhoto[CS] = [page(1)];
  const shot = M._openAnswerMedia(CS);
  ok(/Ignore handwriting quality/i.test(shot.note), shot.note);
  ok(/left blank/i.test(shot.note), 'an item answered nowhere must be marked, not skipped');
});

// ── what the model is told when it reads the paper ──────────────────────────

test('the prompt describes 阅读理解问答 as a WRITTEN-answer passage', () => {
  const r = M._partsPromptRules();
  ok(/阅读理解问答/.test(r), 'the format is missing from the shared fragment');
  ok(/plainanswer/.test(r), 'nothing says the answer block to use');
  ok(/Transcribe the WHOLE passage/i.test(r), 'the passage itself could be dropped');
});

test('the prompt forbids inventing options for a written question', () => {
  const r = M._partsPromptRules();
  ok(/Do NOT turn a written-answer question into an "mcq" block/i.test(r),
    'a page of ruled boxes can still come back as four invented options');
});

test('the prompt asks for the paper\'s marks on every answer', () => {
  const r = M._partsPromptRules();
  ok(/"marks"/.test(r), 'the marks are never asked for');
  ok(/（2分）/.test(r), 'the model is not shown what the allocation looks like on the paper');
  ok(/TOTAL/.test(r), 'a question printing （1分）and （3分）must arrive as 4');
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
