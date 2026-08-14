// Regression tests for the 拼音 input method and the Chinese-aware tokenizer.
// Run with:
//     node tools/pinyin-ime-tests.mjs            all cases
//     node tools/pinyin-ime-tests.mjs <name>     one case
//
// It loads the REAL code out of app.js — `zhSegment`, `zhimeCandidates`,
// `_fbTokenSpans`, `fbToggleToken`'s splice and `FB_EDGE` — and the REAL
// dictionary out of pinyin-dict.json.
//
// Everything here fails silently in the app:
//
//   • A candidate list in the wrong ORDER is not an error, it is the wrong
//     character typed into a question and saved. "chengyu" offering 称王 before
//     成语 produces a question about a king.
//   • The tokenizer is worse. Chinese has no spaces, so splitting on \S+ makes
//     a whole passage ONE chip: the author clicks a word and blanks the entire
//     paragraph, and the textarea still looks fine. Splitting per character
//     instead files 充实 as two separate blanks.
//   • \W as the punctuation edge is the subtlest of the three. Every Chinese
//     character IS \W, so the greedy trim eats the whole word and 课外 blanks
//     to "课外[[]]" — an empty blank in a passage that reads perfectly.
//   • A toggle that rebuilds the text by joining tokens drops every newline in
//     the passage. For 短文填空 the passage IS the question, several paragraphs
//     of it, and one click flattens the lot onto a single line.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const DICT = new URL('../pinyin-dict.json', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');

const slice = (from, to, what) => {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(what + ' not found in app.js — did the banner comments change?');
  return src.slice(a, b);
};

// The candidate lookup and the segmenter, verbatim.
const ime = slice('const ZH_CJK_RE =', '// ---- the fields it may type into', 'segmenter + candidates');
// The tokenizer and the blank/un-blank splice.
const tok = slice('// The punctuation a blank leaves OUTSIDE its brackets', '// Parse into ordered segments', 'tokenizer')
          + slice('function fbToggleToken(id, idx)', '\n}\n', 'toggle') + '\n}\n';

const preamble = `
const _zhimeDictRaw = ${fs.readFileSync(DICT, 'utf8')};
let _zhimeDict = _zhimeDictRaw;
let _zhimeKeys = Object.keys(_zhimeDict.words).sort();
let _zhimeWordSet = new Set();
Object.keys(_zhimeDict.words).forEach(k => String(_zhimeDict.words[k]).split(' ').forEach(w => { if (w) _zhimeWordSet.add(w); }));
const ZHIME_PAGE = 9;
// fbToggleToken reaches for the editor's block list, its textarea and the chip
// redraw; none exists in a headless harness, so each is stubbed to the minimum
// it touches. What is under test is the SPLICE, not the redraw.
let blocks = [];
const document = { getElementById: () => null };
function fbSyncChips() {}
`;

const M = await import('data:text/javascript;base64,' + Buffer.from(
  preamble + ime + tok +
  '\nexport { zhSegment, zhimeCandidates, _fbTokenSpans, _fbSplitTokens, fbToggleToken, FB_EDGE, zhIsCJK, zhHasCJK, blocks };'
).toString('base64'));

// ── helpers ──────────────────────────────────────────────────────────────────
const cases = [];
const test = (name, fn) => cases.push({ name, fn });
function ok(v, msg) { if (!v) throw new Error(msg || 'expected truthy, got ' + v); }
function eq(a, b, msg) {
  const A = JSON.stringify(a), B = JSON.stringify(b);
  if (A !== B) throw new Error((msg ? msg + ': ' : '') + 'expected ' + B + ', got ' + A);
}
// The candidate list, as the bar would show it.
const cands = s => M.zhimeCandidates(s);
const firstOf = s => cands(s)[0];

// ── the dictionary itself ────────────────────────────────────────────────────

test('the dictionary ships with the app', () => {
  ok(fs.existsSync(DICT), 'pinyin-dict.json is missing — the keyboard cannot load without it');
});

test('every syllable the chars table names is a real pinyin syllable', () => {
  // A stray key here is a candidate list nobody can ever reach.
  const bad = Object.keys(M ? {} : {});
  const dict = JSON.parse(fs.readFileSync(DICT, 'utf8'));
  const odd = Object.keys(dict.chars).filter(k => !/^[a-z]{1,6}$/.test(k));
  eq(odd, [], 'non-alphabetic syllable keys');
  ok(Object.keys(dict.chars).length > 380, 'far too few syllables: ' + Object.keys(dict.chars).length);
});

test('word entries are SPACE separated, never run together', () => {
  // "什么" and "甚么" concatenated are four characters that no split() can take
  // apart again, and the bar would offer one four-character nonsense candidate.
  const dict = JSON.parse(fs.readFileSync(DICT, 'utf8'));
  const list = String(dict.words['shenme'] || '').split(' ');
  ok(list.length >= 2, 'shenme should hold more than one word, got ' + JSON.stringify(dict.words['shenme']));
  list.forEach(w => ok(w.length <= 4, 'suspiciously long candidate: ' + w));
});

// ── candidates ───────────────────────────────────────────────────────────────

test('a whole word beats its first character', () => {
  eq(firstOf('xuexi'), '学习');
  eq(firstOf('laoshi'), '老师');
  eq(firstOf('xuesheng'), '学生');
});

test('the vocabulary of THIS subject is typable', () => {
  // A general news corpus rates these far too low to survive the frequency cut
  // — 病句 scores 5 — and they are what a 华文 teacher types all day.
  const want = {
    chengyu: '成语', guanlianci: '关联词', duanwen: '短文', kewai: '课外',
    yuedu: '阅读', lijie: '理解', pinyin: '拼音', ciyu: '词语', bingju: '病句',
    biaodian: '标点', liangci: '量词', zuowen: '作文', langdu: '朗读',
  };
  for (const [key, word] of Object.entries(want)) {
    ok(cands(key).includes(word), key + ' cannot type ' + word + ' — got ' + JSON.stringify(cands(key).slice(0, 5)));
  }
});

test('a primary reading outranks an exotic one', () => {
  // 王 carries a rare third reading "yù", which makes 称王 a real spelling of
  // "chengyu" — and a commoner word in a news corpus than 成语. On frequency
  // alone a teacher typing the word for "idiom" is offered 称王 first.
  eq(firstOf('chengyu'), '成语');
});

test('the words from the screenshot are all typable', () => {
  const words = ['屏幕', '衬衫', '检查', '位置', '熟悉', '勤奋', '榜样', '摇晃',
                 '姿态', '取代', '幻想', '充实', '锻炼', '配合', '避免', '课外'];
  const keys = ['pingmu', 'chenshan', 'jiancha', 'weizhi', 'shuxi', 'qinfen', 'bangyang', 'yaohuang',
                'zitai', 'qudai', 'huanxiang', 'chongshi', 'duanlian', 'peihe', 'bimian', 'kewai'];
  words.forEach((w, i) => ok(cands(keys[i]).includes(w), keys[i] + ' cannot type ' + w));
});

test('a single syllable offers characters, commonest first', () => {
  eq(cands('de')[0], '的');
  eq(cands('wo')[0], '我');
  ok(cands('xue').includes('学'), 'xue must offer 学');
  ok(cands('xue').includes('雪'), 'xue must offer 雪');
});

test('ü is typed as v, the way an IME expects', () => {
  ok(cands('lv').includes('绿'), 'lv must offer 绿');
  ok(cands('nv').includes('女'), 'nv must offer 女');
});

test('a half-typed word still offers something', () => {
  // Mid-word the bar must never go empty — an empty bar reads as "this
  // keyboard is broken", and the student stops typing.
  ok(cands('xuex').length > 0, 'xuex went empty');
  ok(cands('xuexi').length > 0);
  ok(cands('x').length > 0, 'a single letter went empty');
});

test('nonsense returns nothing rather than guessing', () => {
  eq(cands(''), []);
  eq(cands('qqqqzzz'), []);
});

test('candidates never repeat', () => {
  for (const k of ['de', 'shi', 'xuexi', 'laoshi', 'zhongguo', 'yi']) {
    const c = cands(k);
    eq(c.length, new Set(c).size, 'duplicate candidate for ' + k);
  }
});

// ── the segmenter ────────────────────────────────────────────────────────────

test('a passage segments into words, not characters', () => {
  eq(M.zhSegment('学生生活'), ['学生', '生活']);
  eq(M.zhSegment('参加比赛'), ['参加', '比赛']);
});

test('the longest real word wins', () => {
  // Greedy longest-match, which is what makes 课外活动 one chip rather than
  // 课外 + 活动. That is the right way round: an author who wants the two
  // halves blanked separately can wrap them by hand in [[ ]], while a chip row
  // that has already split a word gives no way to blank the whole of it.
  eq(M.zhSegment('课外活动'), ['课外活动']);
  eq(M.zhSegment('课外活动是学生生活'), ['课外活动', '是', '学生', '生活']);
});

test('segmenting is lossless', () => {
  // Whatever it splits into has to join back to exactly what went in, or the
  // chip row and the textarea disagree about what the passage says.
  const s = '课外活动是学生生活的一部分。每当下课铃声响起，校园里便热闹起来。';
  eq(M.zhSegment(s).join(''), s);
});

test('an unknown character is its own token', () => {
  eq(M.zhSegment('龘').join(''), '龘');
});

// ── the tokenizer ────────────────────────────────────────────────────────────

const spans = t => M._fbTokenSpans(t);
const spanText = t => spans(t).map(s => s.text);

test('a Chinese passage is many chips, not one', () => {
  // The bug this file exists for: \S+ over Chinese yields ONE token, so the
  // single chip on screen blanks the whole paragraph.
  const t = '课外活动是学生生活的一部分';
  ok(spanText(t).length > 3, 'got ' + spanText(t).length + ' chips: ' + JSON.stringify(spanText(t)));
});

test('English still splits on whitespace', () => {
  eq(spanText('Metal is a good conductor'), ['Metal', 'is', 'a', 'good', 'conductor']);
});

test('a [[blank]] stays one atomic chip', () => {
  eq(spanText('弟弟把果汁洒在[[衬衫]]上'), spanText('弟弟把果汁洒在[[衬衫]]上'));
  ok(spanText('弟弟把果汁洒在[[衬衫]]上').includes('[[衬衫]]'), 'the blank was split up');
  ok(spanText('a [[conductor]] of heat').includes('[[conductor]]'));
});

test('every span points at the text it came from', () => {
  // The splice in fbToggleToken is by offset, so a span whose start/end do not
  // match its own text rewrites the wrong part of the passage.
  const t = '课外活动是学生生活的一部分。\n\n每当下课铃声响起。';
  spans(t).forEach(s => eq(t.slice(s.start, s.end), s.text, 'span offsets drifted'));
});

test('spans are in order and never overlap', () => {
  const t = '课外活动是学生[[生活]]的一部分。';
  let last = 0;
  spans(t).forEach(s => { ok(s.start >= last, 'overlapping spans'); last = s.end; });
});

// ── blanking ─────────────────────────────────────────────────────────────────

// fbToggleToken works on the shared `blocks` array.
function toggle(text, idx) {
  M.blocks.length = 0;
  M.blocks.push({ id: 'b1', type: 'clozebank', text });
  M.fbToggleToken('b1', idx);
  return M.blocks[0].text;
}

test('blanking a Chinese word wraps the WORD', () => {
  // With \W as the edge this produced "课外[[]]" — an empty blank, on a passage
  // that still reads perfectly in the textarea. The word is the whole chip,
  // whatever its length.
  eq(toggle('学生生活', 0), '[[学生]]生活');
  eq(toggle('学生生活', 1), '学生[[生活]]');
  eq(toggle('课外活动', 0), '[[课外活动]]');
});

test('blanking leaves full-width punctuation outside', () => {
  const t = '生活变得更充实。';
  const i = spanText(t).indexOf('充实');
  ok(i >= 0, 'expected 充实 as its own chip, got ' + JSON.stringify(spanText(t)));
  ok(toggle(t, i).includes('[[充实]]'), 'got ' + toggle(t, i));
  ok(!toggle(t, i).includes('[[充实。]]'), 'the full stop was swallowed into the blank');
});

test('blanking leaves ASCII punctuation outside, as it always did', () => {
  eq(toggle('a good conductor.', 2), 'a good [[conductor]].');
});

test('clicking a blank again un-blanks it', () => {
  const once = toggle('学生生活', 0);
  eq(once, '[[学生]]生活');
  const i = spanText(once).indexOf('[[学生]]');
  ok(i >= 0, 'the blank is not its own chip: ' + JSON.stringify(spanText(once)));
  eq(toggle(once, i), '学生生活');
});

test('a toggle keeps every paragraph break in the passage', () => {
  // toks.join(' ') flattened a multi-paragraph 短文 onto one line, and the
  // passage IS the question.
  const t = '课外活动是学生生活的一部分。\n\n参加课外活动的好处很多。\n\n其次，也能培养团队精神。';
  const out = toggle(t, 0);
  eq((out.match(/\n/g) || []).length, (t.match(/\n/g) || []).length, 'newlines were lost');
  eq(out.replace(/\[\[|\]\]/g, ''), t, 'the passage changed beyond the blank');
});

test('a toggle changes nothing but the token clicked', () => {
  const t = '弟弟不小心把果汁洒在自己的衬衫上，哭着喊妈妈帮他换。';
  const i = spanText(t).indexOf('衬衫');
  ok(i >= 0, 'expected 衬衫 as a chip: ' + JSON.stringify(spanText(t)));
  eq(toggle(t, i).replace(/\[\[|\]\]/g, ''), t);
});

test('a click past the end of the list does nothing', () => {
  eq(toggle('课外活动', 99), '课外活动');
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
