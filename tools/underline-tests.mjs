// Regression tests for 画线词语 — THE UNDERLINED WORD. Run with:
//     node tools/underline-tests.mjs            all cases
//     node tools/underline-tests.mjs <name>     one case
//
// It loads the REAL `_aiUnderline`, `_separateOptionLines`,
// `escapeHtmlKeepLines` and the shared prompt fragment out of app.js.
//
// 汉语拼音 is what this protects. The paper underlines the word the question is
// about — 弟弟不小心把果汁洒在自己的<u>衬衫</u>上 — and the four options are
// nothing but that word's pinyin: cēn sān / cèn sān / chēn shān / chèn shān.
//
// Every failure here is silent, and each one produces a question that reads
// perfectly and cannot be answered:
//
//  • The prompt not asking for the underline: the sentence is transcribed
//    flat, and the question no longer says which of a dozen words the four
//    spellings belong to.
//  • _aiUnderline not accepting the markdown a model reaches for: __衬衫__ is
//    stored and printed literally, underscores and all.
//  • escapeHtmlKeepLines stripping <u>: the screen shows the underline and the
//    PRINTED worksheet does not — the one surface nobody checks before class.
//  • An unbalanced tag: an opener with no closer underlines the whole of the
//    rest of the question, which reads as a fault in the app.
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
  cut('function _separateOptionLines(text)', '\n// 画线词语', 'option lines'),
  cut('function _aiUnderline(text)', '\n// The "tags" instruction', 'underline'),
  // _keepParagraphGaps is what keeps the author's blank lines; cut in rather
  // than re-written, so this harness cannot drift from the real one.
  cut('function _keepParagraphGaps(lines) {', '\nfunction escapeHtmlKeepLines', 'para gaps'),
  cut('function escapeHtmlKeepLines(content)', '\n// A repeated message stacks', 'escape keeping lines'),
  cut('function _partsPromptRules()', '\n// The rectangle-selection', 'parts rules'),
  `
// The DOM-based escapeHtml, without the DOM.
function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
`
].join('\n');

const M = new Function(section + '\nreturn { _aiUnderline, _separateOptionLines, escapeHtmlKeepLines, _partsPromptRules };')();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const ok = (cond, what) => { if (!cond) throw new Error(what); };
const eq = (got, want, what) => {
  if (got !== want) throw new Error((what || 'value') + ':\n         got    ' + JSON.stringify(got) + '\n         wanted ' + JSON.stringify(want));
};

const SENTENCE = '弟弟不小心把果汁洒在自己的<u>衬衫</u>上，哭着喊妈妈帮他换。';

// ── what the model is told ──────────────────────────────────────────────────

test('every build prompt is told to keep the underline', () => {
  // The rule lives in the ONE fragment all five build prompts carry, so it
  // cannot be added to Build-from-screenshot and missed by Rapid add.
  const r = M._partsPromptRules();
  ok(/画线词语/.test(r), 'the rule is missing from the shared fragment');
  ok(/<u>…<\/u>/.test(r), 'the model is never shown the markup to use');
  ok(/汉语拼音/.test(r), 'the reason — the options ARE the pinyin — is not given');
});

test('the underline rule overrides "plain text only"', () => {
  // Four of the five prompts end with "Use plain text only, no markdown", and
  // a model resolving that contradiction drops the tag — which is the whole
  // failure, arriving through the fix for it.
  const r = M._partsPromptRules();
  ok(/plain text only/i.test(r) && /does not remove it/i.test(r),
    'nothing tells the model the "plain text only" rule does not cancel <u>');
});

// ── the normaliser ──────────────────────────────────────────────────────────

test('a tag the model wrote is kept as it is', () => {
  eq(M._aiUnderline(SENTENCE), SENTENCE);
});

test('the markdown a model reaches for becomes a tag', () => {
  // __word__ is the same marker a pasted passage carries (_pbPassageHtml), so
  // both doors into the app agree on what an underline looks like.
  eq(M._aiUnderline('弟弟把果汁洒在__衬衫__上。'), '弟弟把果汁洒在<u>衬衫</u>上。');
});

test('a tag escaped on the way through JSON is put back', () => {
  eq(M._aiUnderline('这件&lt;u&gt;衬衫&lt;/u&gt;很好看。'), '这件<u>衬衫</u>很好看。');
});

test('sloppy spacing and capitals in the tag still count', () => {
  eq(M._aiUnderline('这件< U >衬衫</ u >很好看。'), '这件<u>衬衫</u>很好看。');
});

test('an unbalanced tag is dropped, never left open', () => {
  // An opener with no closer underlines every word after it, including the
  // options — which looks like a broken app, not like the paper.
  eq(M._aiUnderline('弟弟把果汁洒在<u>衬衫上。'), '弟弟把果汁洒在衬衫上。');
  eq(M._aiUnderline('弟弟把果汁洒在衬衫</u>上。'), '弟弟把果汁洒在衬衫上。');
});

test('ordinary text is left completely alone', () => {
  eq(M._aiUnderline('弟弟不小心把果汁洒在自己的衬衫上。'), '弟弟不小心把果汁洒在自己的衬衫上。');
  eq(M._aiUnderline(''), '');
  eq(M._aiUnderline(null), '');
});

test('two underlined words in one sentence both survive', () => {
  eq(M._aiUnderline('__屏幕__和__衬衫__的拼音。'), '<u>屏幕</u>和<u>衬衫</u>的拼音。');
});

test('the option-line split runs before it and does not fight it', () => {
  // buildBlocksFromAi wires them in this order. The label splitter inserts
  // <br> before each option; the underline must come through untouched.
  const out = M._aiUnderline(M._separateOptionLines('弟弟把果汁洒在__衬衫__上。\n(1) cēn sān\n(2) chèn shān'));
  ok(out.indexOf('<u>衬衫</u>') >= 0, 'the underline was lost in the split: ' + out);
  ok(out.indexOf('<br>(2) chèn shān') >= 0, 'the options no longer split onto their own lines: ' + out);
});

test('buildBlocksFromAi is the ONE place it is wired in', () => {
  // A text block that skipped it would be the same bug back, on one path.
  ok(src.indexOf('_aiUnderline(_separateOptionLines(stripBrackets(b.text || b.content)))') >= 0,
    'the AI text block no longer runs through _aiUnderline');
});

// ── the printed page ────────────────────────────────────────────────────────

test('the PRINTED worksheet keeps the underline', () => {
  // This is the surface that fails last and worst: the screen shows the
  // underline, the printout does not, and nobody finds out until the class is
  // sitting in front of the paper.
  eq(M.escapeHtmlKeepLines(SENTENCE), '弟弟不小心把果汁洒在自己的<u>衬衫</u>上，哭着喊妈妈帮他换。');
});

test('every other tag is still stripped', () => {
  eq(M.escapeHtmlKeepLines('这件<strong>衬衫</strong>很好看。'), '这件衬衫很好看。');
  eq(M.escapeHtmlKeepLines('<script>alert(1)</script>安全'), 'alert(1)安全');
});

test('line breaks still become <br>, with the underline intact', () => {
  eq(M.escapeHtmlKeepLines('弟弟把果汁洒在<u>衬衫</u>上。<br>(1) cēn sān<br>(2) chèn shān'),
    '弟弟把果汁洒在<u>衬衫</u>上。<br>(1) cēn sān<br>(2) chèn shān');
});

test('an unbalanced tag prints as plain text, not as an open underline', () => {
  eq(M.escapeHtmlKeepLines('弟弟把果汁洒在<u>衬衫上。'), '弟弟把果汁洒在衬衫上。');
});

test('nothing in the text can pose as the marker', () => {
  // <u> is carried across the escape on two control characters. One already in
  // the content is dropped, or it would come out the other side as live markup.
  eq(M.escapeHtmlKeepLines('弟弟\u0001衬衬\u0002上。'), '弟弟衬衬上。');
  eq(M.escapeHtmlKeepLines('5 < 7'), '5 &lt; 7');
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
