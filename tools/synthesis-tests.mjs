// Regression tests for ✍️ SYNTHESIS & TRANSFORMATION. Run with:
//     node tools/synthesis-tests.mjs            all cases
//     node tools/synthesis-tests.mjs <name>     one case
//
// It loads the REAL section out of app.js — the accessors, `syRubric`,
// `_openAnswerText`, `syPrintHtml` — plus the `synthesis` arm of
// `buildBlocksFromAi`.
//
// Two things here fail silently and a class pays for both.
//
// `syRubric` is the ONE place the marker is told what "correct" means. Lose it
// and the AI falls back to comparing the student's wording against the model
// answer — and a sentence transformation has ONE right meaning but many right
// wordings, so a correct rewrite phrased differently is marked wrong. Nothing
// throws; the child simply gets a red border on a right answer.
//
// `_openAnswerText` puts back what the PAPER gave and the student therefore
// never typed: the opening ("This plot of corn"), and the full stop printed at
// the end of the last rule. Without the first the marker is handed a sentence
// fragment — "was grown from scratch by the farmer" — and marks a perfect
// answer as not a sentence; without the second it marks a perfect answer down
// for punctuation nobody asked for.
//
// The answer is written across the paper's RULED LINES — two boxes, one
// sentence — so `_openAnswerEls` is the ONE place that group is resolved.
// Everything that reads, paints, clears or locks an answer goes through it, and
// each of those fails in its own silent way if a rule is missed: a second rule
// still live after the question is finished, a red border on one line and none
// on the next, half a sentence surviving a reset into the next question.
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
  cut('const SY_MARKS_DEFAULT', "// ---- the student's box", 'synthesis core'),
  cut('function syStudentHtml(items', '\n// Moving between the rules', 'student rules'),
  cut('function syLineKey(ev, el)', '\n}\n', 'line keys') + '\n}\n',
  cut('function syPrintHtml(block)', '\n}\n', 'print') + '\n}\n',
  `
function micButtonHtml() { return '<button class="mic-btn"></button>'; }
function _partActionsHtml() { return '<div class="part-actions"></div>'; }
function _adminAnswerToolHtml() { return '<div class="admin-ans-tool"></div>'; }
`,
  // The synthesis arm of the builder, reached through the real function.
  'const SY_LINES_DEFAULT_X = SY_LINES_DEFAULT;',
  cut('function buildBlocksFromAi', '\n// Build a full pending question object', 'builder'),
  `
let _n = 0;
function generateBlockId() { return 'b' + (++_n); }
function stripHtml(c) { return c ? String(c).replace(/<[^>]*>/g, ' ').replace(/\\s+/g, ' ').trim() : ''; }
function _separateOptionLines(t) { return String(t == null ? '' : t); }
function _markedToBlanks(t) { return { content: String(t == null ? '' : t), blanks: {} }; }
function escapeHtml(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function escapeHtmlKeepLines(s) { return escapeHtml(s); }
function qApplyAiParts(b) { return b; }
const QPART_NONE = '-';
function qPartNormalize(v) {
  const t = String(v == null ? '' : v).trim().toLowerCase().replace(/[()\s.]/g, '');
  if (/^[1-9]\d{0,2}$/.test(t)) return t;
  return (t.length === 1 && 'abcdefghjklmnopqrstuvwxyz'.indexOf(t) >= 0) ? t : '';
}
`
].join('\n');

const M = new Function(section +
  '\nreturn { syIsBlock, syGiven, syCue, syAnswer, syStartsWith, syMarks, syLines, syReady,' +
  ' syRubric, _openAnswerText, _openAnswerEls, _openAnswerPaint, _openAnswerClear, _openAnswerLock,' +
  ' syStudentHtml, syLineKey, syPrintHtml, buildBlocksFromAi, SY_MARKS_DEFAULT, SY_LINES_MAX };')();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const ok = (cond, what) => { if (!cond) throw new Error(what); };
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};

// The five questions off the paper.
const Q66 = { type: 'synthesis', given: 'We admire Mr Kwan. He is our local football player.', cue: 'whom', cuePos: 'use', answer: 'Mr Kwan, whom we admire, is our local football player.', marks: 2 };
const Q67 = { type: 'synthesis', given: 'The farmer grew this plot of corn from scratch.', cue: 'This plot of corn', cuePos: 'start', answer: 'This plot of corn was grown from scratch by the farmer.', marks: 2 };
const Q70 = { type: 'synthesis', given: 'Produce the voucher to get your meal.', cue: 'or', cuePos: 'use', answer: 'Produce the voucher or you will not get your meal.', marks: 2 };
// A textarea, as the marking paths see it.
const box = (value, prefix) => ({ value, dataset: prefix ? { prefix } : {} });

// The paper's ruled lines, as the marking paths see them: n inputs sharing one
// data-sy-group inside one .open-answer-section, the FIRST of them carrying the
// printed opening and the printed full stop.
const rules = (values, prefix, after) => {
  const els = [];
  const section = {
    querySelectorAll(sel) {
      const m = /^\[data-sy-group="(.*)"\]$/.exec(sel);
      return m ? els.filter(e => e._g === m[1]) : [];
    }
  };
  values.forEach((v, i) => {
    const e = {
      _g: 'g1', value: v, style: {}, disabled: false, selectionStart: 0, focused: false,
      dataset: i === 0
        ? Object.assign({ suffix: '.' }, prefix ? { prefix } : {}, after ? { after } : {})
        : {},
      getAttribute: a => (a === 'data-sy-group' ? e._g : null),
      closest: s => (s === '.open-answer-section' ? section : null),
      focus() { e.focused = true; },
      setSelectionRange() {}
    };
    els.push(e);
  });
  return els;
};
const key = (k, extra) => Object.assign({ key: k, shiftKey: false, prevented: false, preventDefault() { this.prevented = true; } }, extra || {});

// ── the block itself ────────────────────────────────────────────────────────

test('a block with nothing given is not a question yet', () => {
  ok(!M.syReady({ type: 'synthesis', given: '   ' }), 'an empty given must not render an answer box');
  ok(M.syReady(Q66), 'a real one must');
  ok(!M.syReady({ type: 'text', given: 'x' }), 'only a synthesis block counts');
});

test('the two cue positions are distinguished', () => {
  ok(!M.syStartsWith(Q66), '"whom" is printed at the end of the rule');
  ok(M.syStartsWith(Q67), '"This plot of corn" is the given opening');
  ok(!M.syStartsWith({ type: 'synthesis', cue: 'x' }), 'the default is "use"');
});

test('marks and lines fall back rather than going NaN', () => {
  eq(M.syMarks(Q66), 2);
  [null, undefined, 0, -1, 21, 'x', {}].forEach(v => eq(M.syMarks({ marks: v }), M.SY_MARKS_DEFAULT, 'marks ' + JSON.stringify(v)));
  eq(M.syLines({ lines: 99 }), M.SY_LINES_MAX, 'a runaway line count is capped');
  eq(M.syLines({ lines: 3 }), 3);
});

test('a malformed block never throws', () => {
  [null, undefined, {}, { type: 'synthesis' }, { type: 'synthesis', given: null, cue: null }]
    .forEach(b => { M.syGiven(b); M.syCue(b); M.syAnswer(b); M.syMarks(b); M.syLines(b); M.syReady(b); M.syPrintHtml(b); });
});

// ── _openAnswerText — the opening the paper gave ────────────────────────────

test('the given opening is put back before marking', () => {
  // The box holds only what the student wrote; "This plot of corn" was printed.
  eq(M._openAnswerText(box('was grown from scratch by the farmer.', 'This plot of corn')),
     'This plot of corn was grown from scratch by the farmer.');
});

test('an ordinary answer box is unchanged', () => {
  eq(M._openAnswerText(box('  Mr Kwan, whom we admire, is our local football player.  ')),
     'Mr Kwan, whom we admire, is our local football player.');
});

test('an empty box stays empty — the prefix alone is not an answer', () => {
  // Otherwise an untouched box reads as "This plot of corn", the marker is
  // asked to judge it, and "you did not answer" becomes "that is not a
  // sentence".
  eq(M._openAnswerText(box('', 'This plot of corn')), '');
  eq(M._openAnswerText(box('   ', 'This plot of corn')), '');
});

test('a missing element or dataset never throws', () => {
  eq(M._openAnswerText(null), '');
  eq(M._openAnswerText({ value: 'x' }), 'x');
  eq(M._openAnswerText({}), '');
});

// ── the ruled lines are ONE answer ──────────────────────────────────────────

test('a sentence written across two rules reaches the marker as one sentence', () => {
  // The whole design constraint of this question type: there is no marking a
  // rewrite in pieces, so two boxes must arrive as one string.
  const r = rules(['Mr Kwan, whom we admire,', 'is our local football player']);
  eq(M._openAnswerText(r[0]), 'Mr Kwan, whom we admire, is our local football player.');
});

test('the full stop the paper prints is put back — and never doubled', () => {
  eq(M._openAnswerText(rules(['He ran home', 'because he was late'])[0]), 'He ran home because he was late.');
  eq(M._openAnswerText(rules(['He ran home because he was late.', ''])[0]), 'He ran home because he was late.');
  eq(M._openAnswerText(rules(['Did he go home?', ''])[0]), 'Did he go home?', 'a question mark already ends the sentence');
  eq(M._openAnswerText(rules(['He shouted, "Go home!"', ''])[0]), 'He shouted, "Go home!"', 'a closing quote still counts as ended');
});

test('the given opening still comes back, now in front of the rules', () => {
  const r = rules(['was grown from scratch', 'by the farmer'], 'This plot of corn');
  eq(M._openAnswerText(r[0]), 'This plot of corn was grown from scratch by the farmer.');
});

// ── the word printed BETWEEN the rules ──────────────────────────────────────
// The page prints it at the end of the first rule, so the student writes around
// it and never types it. Left out, the marker reads the two rules run together,
// cannot find the word the question required, and marks a right answer wrong
// for a connector the student can see on the page.

test('the word printed between the rules is put back where the page prints it', () => {
  const r = rules(['The children in the neighbourhood love playing with the cat', 'friendliness'], null, 'because of its');
  eq(M._openAnswerText(r[0]),
     'The children in the neighbourhood love playing with the cat because of its friendliness.');
});

test('it is put back for a one-word connector too', () => {
  eq(M._openAnswerText(rules(['Produce the voucher', 'you will not get your meal'], null, 'or')[0]),
     'Produce the voucher or you will not get your meal.');
  eq(M._openAnswerText(rules(['Mr Kwan,', 'we admire, is our local football player'], null, 'whom')[0]),
     'Mr Kwan, whom we admire, is our local football player.');
});

test('a word the student typed THEMSELVES is never doubled', () => {
  // The same wrong answer from the other direction: a student may reasonably
  // write the whole sentence on one rule, word provided and all, and
  // "…is our local football player whom." fails every rubric there is.
  eq(M._openAnswerText(rules(['Mr Kwan, whom we admire, is our local football player', ''], null, 'whom')[0]),
     'Mr Kwan, whom we admire, is our local football player.');
  eq(M._openAnswerText(rules(['Produce the voucher', 'or you will not get your meal'], null, 'or')[0]),
     'Produce the voucher or you will not get your meal.');
  eq(M._openAnswerText(rules(['Mark was late because of his', 'indecision'], null, 'because of his')[0]),
     'Mark was late because of his indecision.');
});

test('a retyped opening is not doubled either', () => {
  eq(M._openAnswerText(rules(['This plot of corn was grown from scratch by the farmer', ''], 'This plot of corn')[0]),
     'This plot of corn was grown from scratch by the farmer.');
});

test('the connector still goes in when only the second rule is written', () => {
  // Blank rule, "because of its", "friendliness" — that is what the page says.
  eq(M._openAnswerText(rules(['', 'friendliness'], null, 'because of its')[0]),
     'because of its friendliness.');
});

test('a connector hiding INSIDE another word does not count as typed', () => {
  // "for" contains "or". Read as already typed, the word the question required
  // never reaches the marker at all.
  eq(M._openAnswerText(rules(['Produce the vouchers for your meal', ''], null, 'or')[0]),
     'Produce the vouchers for your meal or.');
});

test('a printed word is matched however the student spaced it', () => {
  eq(M._openAnswerText(rules(['Mark was late because of   his', 'indecision'], null, 'because of his')[0]),
     'Mark was late because of his indecision.');
});

test('printed words are never an answer on their own', () => {
  // Untouched rules must stay blank however much the page prints around them,
  // or "you did not answer" is marked as "that is not a sentence".
  eq(M._openAnswerText(rules(['', ''], 'This plot of corn', 'because of its')[0]), '');
  eq(M._openAnswerText(rules(['  ', ' '], null, 'or')[0]), '');
});

test('a printed word with regex characters in it never throws', () => {
  ['(or)', 'a.b', 'it\'s', '[x]', '*', '\\'].forEach(cue => {
    ok(typeof M._openAnswerText(rules(['He ran', 'home'], null, cue)[0]) === 'string', 'cue ' + cue);
  });
});

test('untouched rules are still no answer at all', () => {
  // Otherwise an untouched question is marked as "This plot of corn." — a
  // fragment the marker judges, so "you did not answer" becomes "wrong".
  eq(M._openAnswerText(rules(['', ''], 'This plot of corn')[0]), '');
  eq(M._openAnswerText(rules(['   ', ''])[0]), '');
});

test('a blank rule in the middle does not leave a hole in the sentence', () => {
  eq(M._openAnswerText(rules(['He ran home', '  ', 'because he was late'])[0]),
     'He ran home because he was late.');
});

test('painting, clearing and locking reach EVERY rule, not just the first', () => {
  // Each of these is silent on its own: a red border on rule one and none on
  // rule two, half a sentence surviving into the next question, and — the worst
  // — a second rule still typeable after the question has been marked.
  const r = rules(['one', 'two']);
  M._openAnswerPaint(r[0], 'red');
  eq(r.map(x => x.style.borderColor), ['red', 'red'], 'the verdict must colour the whole answer');
  M._openAnswerLock(r[0], true);
  eq(r.map(x => x.disabled), [true, true], 'a finished question must lock every rule');
  M._openAnswerClear(r[0]);
  eq(r.map(x => x.value), ['', ''], 'another go must clear every rule');
  eq(r.map(x => x.disabled), [false, false], 'and unlock every rule');
});

test('an ordinary answer box is not a group and is left alone', () => {
  const b = box('x');
  eq(M._openAnswerEls(b).length, 1, 'every other question type must see no change');
  eq(M._openAnswerEls(null), []);
});

// ── the rules on screen ─────────────────────────────────────────────────────

const student = (b) => M.syStudentHtml([], b, '#c', '(a)');

test('the word provided sits at the END of the first rule, as the paper prints it', () => {
  const h = student(Q66);
  ok(h.indexOf('sy-line') < h.indexOf('whom'), '"whom" must follow the rule it is printed after');
  ok(/sy-cue-end/.test(h), 'the cue is printed beside the rule, never typed into it');
  ok(!/data-prefix/.test(h), 'a "use" cue is not the opening of the answer');
});

test('the word printed between the rules is ALSO handed to the marker', () => {
  // The span the student reads and the data-after the marker reads come from
  // one decision. Disagreeing is invisible: the page shows the connector, the
  // marker never sees it, and a right answer is marked wrong for missing it.
  ok(/data-after="whom"/.test(student(Q66)), 'the printed word must travel to the marker');
  ok(!/data-after/.test(student(Q67)), 'a given OPENING is a prefix, not a word printed between rules');
});

test('a given OPENING sits in front of the first rule and is put back to mark', () => {
  const h = student(Q67);
  ok(h.indexOf('This plot of corn') < h.indexOf('<input'), 'the opening precedes the rule');
  ok(/data-prefix="This plot of corn"/.test(h), 'without this the marker is handed a fragment');
});

test('the printed word is on the rule it is printed AFTER, and only that one', () => {
  const h = student(Object.assign({}, Q66, { lines: 3 }));
  eq((h.match(/data-after=/g) || []).length, 1, 'the connector belongs at one junction, not every rule');
});

test('the last rule ends in the full stop the paper prints', () => {
  ok(/sy-stop/.test(student(Q66)), 'the closing full stop is missing');
  ok(/data-suffix="\."/.test(student(Q66)), 'and it must be put back before marking');
});

test('every rule is drawn, and ONLY the first is the registered answer', () => {
  // Two data-oidx would register one answer twice and mark the student on half
  // a sentence, twice over.
  const h = student(Object.assign({}, Q66, { lines: 3 }));
  eq((h.match(/data-sy-group=/g) || []).length, 3, 'a rule was dropped');
  eq((h.match(/data-oidx=/g) || []).length, 1, 'exactly one rule is the answer element');
  eq((h.match(/class="open-answer sy-line"/g) || []).length, 1);
});

test('the question registers exactly ONE item, marked by the rubric', () => {
  const items = [];
  M.syStudentHtml(items, Q66, '#c', '(a)');
  eq(items.length, 1, 'a rewrite is marked as one whole sentence, so it is one item');
  eq(items[0].model, Q66.answer);
  ok(/AS ONE WHOLE SENTENCE/.test(items[0].rubric), 'the rubric must travel with the item');
});

test('the square marks box is not drawn on screen', () => {
  // It is where a teacher WRITES a mark on paper; there is nothing to write on
  // here, and the screen is not a marking sheet.
  const h = student(Q66);
  ok(!/print-sy-box|sy-marks|sy-cue-chip/.test(h), 'the paper-only furniture is on screen: ' + h);
});

test('a block with nothing given draws no rules at all', () => {
  eq(M.syStudentHtml([], { type: 'synthesis', given: '' }, '#c', ''), '');
});

// ── moving between the rules ────────────────────────────────────────────────

test('Enter carries on down to the next rule', () => {
  const r = rules(['He ran home', '']);
  const ev = key('Enter');
  M.syLineKey(ev, r[0]);
  ok(r[1].focused, 'Enter must move to the next rule');
  ok(ev.prevented, 'and never submit the surrounding form');
});

test('Enter on the LAST rule stays put', () => {
  const r = rules(['a', 'b']);
  M.syLineKey(key('Enter'), r[1]);
  ok(!r[0].focused, 'it must not wrap back round to the first rule');
});

test('Backspace goes back only from an EMPTY rule', () => {
  const r = rules(['He ran home', '']);
  M.syLineKey(key('Backspace'), r[1]);
  ok(r[0].focused, 'an empty rule hands the caret back');

  const r2 = rules(['He ran home', 'because']);
  M.syLineKey(key('Backspace'), r2[1]);
  ok(!r2[0].focused, 'a rule with writing on it deletes a letter instead');
});

test('a locked rule is never focused', () => {
  // The question is finished; Enter must not walk the caret into a dead box.
  const r = rules(['a', '']);
  r[1].disabled = true;
  M.syLineKey(key('Enter'), r[0]);
  ok(!r[1].focused, 'a finished question must not hand the caret on');
});

test('an ordinary key is left entirely alone', () => {
  const r = rules(['a', '']);
  const ev = key('x');
  M.syLineKey(ev, r[0]);
  ok(!ev.prevented && !r[1].focused, 'typing must just type');
  M.syLineKey(key('Enter'), null);   // never throws
  M.syLineKey(null, r[0]);
});

// ── syRubric — what the marker is actually told ─────────────────────────────

test('the rubric says to mark the sentence AS A WHOLE', () => {
  const r = M.syRubric(Q66);
  ok(/AS ONE WHOLE SENTENCE/i.test(r), 'the whole-sentence instruction is missing: ' + r);
  ok(/never phrase by phrase/i.test(r), 'phrase-by-phrase must be ruled out');
});

test('the rubric protects a correct rewrite that is worded differently', () => {
  // The single most likely way this question type marks a class unfairly.
  const r = M.syRubric(Q66);
  ok(/[Dd]ifferent wording from the model answer is FINE/.test(r), 'wording latitude is missing: ' + r);
  ok(/more than one correct rewrite/i.test(r), 'the marker must be told there are several right answers');
});

test('the rubric names the word the sentence must use', () => {
  ok(/"whom"/.test(M.syRubric(Q66)), 'the cue must be quoted into the rubric');
  ok(/"or"/.test(M.syRubric(Q70)));
});

test('a given OPENING is described as an opening, not just a word to include', () => {
  const r = M.syRubric(Q67);
  ok(/as its opening/i.test(r), 'the opening requirement is missing: ' + r);
  ok(!/as its opening/i.test(M.syRubric(Q66)), '"whom" is not an opening');
});

test('the three verdicts are each given a meaning', () => {
  const r = M.syRubric(Q66);
  ok(/"correct"/.test(r) && /"partial"/.test(r) && /"incorrect"/.test(r), 'a verdict was left undefined: ' + r);
  ok(/meaning changes/i.test(r), 'a changed meaning must be incorrect');
});

test('a question with no word provided still gets a usable rubric', () => {
  const r = M.syRubric({ type: 'synthesis', given: 'He ran. He was tired.' });
  ok(/AS ONE WHOLE SENTENCE/i.test(r));
  ok(!/uses ""/.test(r), 'an empty cue must not be quoted in');
});

// ── the printed page ────────────────────────────────────────────────────────

test('the word provided prints at the END of the rule when it is a "use" cue', () => {
  const h = M.syPrintHtml(Q66);
  ok(h.indexOf('print-sy-rule') < h.indexOf('whom'), '"whom" should follow the rule, as the paper prints it');
});

test('a given OPENING prints at the START of the rule', () => {
  const h = M.syPrintHtml(Q67);
  ok(h.indexOf('This plot of corn') < h.indexOf('print-sy-rule'), 'the opening should precede the rule');
});

test('the printed page never shows the model answer', () => {
  // The trap fillblank fell into: the read-only rendering prints the answer,
  // which on a worksheet is the whole question given away.
  const h = M.syPrintHtml(Q67);
  ok(h.indexOf('was grown from scratch by the farmer') < 0, 'the answer is printed on the question page');
  ok(M.syPrintHtml(Q66).indexOf('whom we admire') < 0);
});

test('the marks box and the right number of rules are drawn', () => {
  const h = M.syPrintHtml(Object.assign({}, Q66, { lines: 3 }));
  ok(/print-sy-box/.test(h), 'the marks box is missing');
  eq((h.match(/class="print-sy-line"/g) || []).length, 3);
});

test('a block with nothing given prints nothing at all', () => {
  eq(M.syPrintHtml({ type: 'synthesis', given: '', cue: 'whom' }), '');
});

// ── read off a screenshot ───────────────────────────────────────────────────

const build = blocks => M.buildBlocksFromAi({ blocks }).blocks;

test('the AI can build one, with its part', () => {
  const bs = build([{
    type: 'synthesis', part: 'a',
    given: 'We admire Mr Kwan. He is our local football player.',
    cue: 'whom', cuePos: 'use',
    answer: 'Mr Kwan, whom we admire, is our local football player.', marks: 2
  }]);
  eq(bs.length, 1);
  eq(bs[0].type, 'synthesis');
  eq(bs[0].given, 'We admire Mr Kwan. He is our local football player.');
  eq(bs[0].cue, 'whom');
  eq(bs[0].cuePos, 'use');
  eq(bs[0].marks, 2);
});

test('cuePos falls back to "use" for anything that is not "start"', () => {
  eq(build([{ type: 'synthesis', given: 'g', cuePos: 'START' }])[0].cuePos, 'start');
  eq(build([{ type: 'synthesis', given: 'g', cuePos: 'end' }])[0].cuePos, 'use');
  eq(build([{ type: 'synthesis', given: 'g' }])[0].cuePos, 'use');
});

test('a synthesis entry with nothing given builds nothing', () => {
  eq(build([{ type: 'synthesis', cue: 'whom' }]).length, 0, 'an empty question must not reach the bank');
});

test('a nonsense marks value from the AI falls back', () => {
  eq(build([{ type: 'synthesis', given: 'g', marks: 'lots' }])[0].marks, M.SY_MARKS_DEFAULT);
  eq(build([{ type: 'synthesis', given: 'g', marks: 99 }])[0].marks, M.SY_MARKS_DEFAULT);
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
