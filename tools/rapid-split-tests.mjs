// Regression tests for HOW MANY QUESTIONS A PAGE HOLDS. Run with:
//     node tools/rapid-split-tests.mjs            all cases
//     node tools/rapid-split-tests.mjs <name>     one case
//
// It loads the REAL `_aiQuestionPayloads` out of app.js, plus the build prompt
// and the numbering stripper that guards it, and checks the rules the model is
// given.
//
// A 语文应用 page of 1, 2, 3, 4, 5 holds FIVE questions, not one question with
// five parts. They share no passage, a student is served one at a time and each
// is marked on its own — so ⚡ Rapid add must put five rows in vetting. 短文填空
// and 阅读理解 are the opposite case: one passage its questions cannot be read
// without, and still ONE question with lettered parts.
//
// `_aiQuestionPayloads` is the ONE place that decision is read out of a build
// reply, and every way it can go wrong is silent:
//
//  • Return one payload for a five-question page and four questions are thrown
//    away, with a single row in vetting that looks perfectly fine.
//  • Return five for a 短文填空 and the passage is torn off its blanks, leaving
//    five that cannot be answered.
//  • Drop the inherited topic/category and every question after the first lands
//    in vetting untopiced, for an author to open and fix by hand.
//  • Return NOTHING for a reply in the old single-question shape and Rapid add
//    stops working altogether for every ordinary screenshot.
//
// The numbering stripper is here for the same reason: a 华文 paper prints "2、"
// and "（2）", and a stripper that knows only "44." leaves the paper's number at
// the head of every one of the five questions it just separated.
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
  cut('function _aiQuestionPayloads(parsed)', 'function buildQuestionFromAi', 'payload split'),
  cut('function _aiBuildQuestionPrompt(isPdf, imageCount, levelHint)', '\n// The lettered-parts rules', 'build prompt'),
  cut('function _partsPromptRules()', '\n// The rectangle-selection', 'parts rules'),
  cut('const EP_LEAD_NUM_RE =', '\n// A bare number needs a separator', 'question numbering'),
  cut('function qPartWalkPlain(html)', '\n// How many line-starts', 'html walk'),
  `
function currentTopics() { return ['汉语拼音 Hanyu Pinyin', '短文填空 Cloze Passage', '阅读理解 Comprehension']; }
// ⚡ Rapid add's "Level for this batch" narrows the topic list the prompt
// offers — a level is read off the TOPIC here, so that is the only lever.
function currentTopicsByLevel() { return { P3: ['汉语拼音 Hanyu Pinyin'], P4: [], P5: ['短文填空 Cloze Passage'], P6: ['阅读理解 Comprehension'] }; }
function _genPreamble() { return ''; }
function _aiTagsPromptLine() { return ''; }
function _rectangleRules() { return ''; }
const SCAN_READING_NOTE = '';
`
].join('\n');

const M = new Function(section + '\nreturn { _aiQuestionPayloads, _aiBuildQuestionPrompt, _epStripLeadNumber, EP_LEAD_NUM_RE };')();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const ok = (cond, what) => { if (!cond) throw new Error(what); };
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};

const syn = (given, cue) => ({ type: 'synthesis', given, cue, cuePos: 'use', answer: 'x', marks: 2 });

// The page off the paper: five 改写句子 questions sharing nothing at all.
const PAGE = {
  questions: [
    { title: '因为……所以', topic: '汉语拼音 Hanyu Pinyin', category: 'Explanation', tags: ['改写句子'], questionType: 'open', blocks: [syn('他很努力。他的成绩进步得很快。', '因为……所以')] },
    { title: '虽然……但是', blocks: [syn('妹妹年纪小。她很懂事。', '虽然……但是')] },
    { title: '一边……一边', blocks: [syn('爸爸在看电视。爸爸在吃水果。', '一边……一边')] },
    { title: '不但……而且', blocks: [syn('这家餐馆的食物好吃。价钱也便宜。', '不但……而且')] },
    { title: '只要……就', blocks: [syn('你多加练习。你的华文会进步。', '只要……就')] }
  ],
  topic: '汉语拼音 Hanyu Pinyin', category: 'Explanation', tags: ['改写句子', '句子重组']
};

// ── the split ───────────────────────────────────────────────────────────────

test('a page of five numbered questions becomes FIVE questions', () => {
  // The whole point: five rows in vetting, not one question with five parts.
  const out = M._aiQuestionPayloads(PAGE);
  eq(out.length, 5, 'four questions were thrown away');
  eq(out.map(p => p.title), ['因为……所以', '虽然……但是', '一边……一边', '不但……而且', '只要……就']);
  eq(out[0].blocks.length, 1, 'each carries only its own blocks');
});

test('the order on the page is the order they are added', () => {
  const out = M._aiQuestionPayloads(PAGE);
  eq(out[0].blocks[0].cue, '因为……所以');
  eq(out[4].blocks[0].cue, '只要……就');
});

test('an entry INHERITS the topic and category it did not repeat', () => {
  // A model told to write these per entry writes them once at the top and then
  // stops. Without the inheritance every question after the first lands in
  // vetting untopiced, for an author to open and fix by hand.
  const out = M._aiQuestionPayloads(PAGE);
  out.forEach((p, i) => {
    eq(p.topic, '汉语拼音 Hanyu Pinyin', 'entry ' + i + ' lost its topic');
    eq(p.category, 'Explanation', 'entry ' + i + ' lost its category');
  });
  eq(out[1].tags, ['改写句子', '句子重组'], 'and its tags');
});

test('an entry that DID carry its own keeps them', () => {
  const out = M._aiQuestionPayloads(PAGE);
  eq(out[0].tags, ['改写句子'], 'its own tags must win over the page default');
  const own = M._aiQuestionPayloads({ topic: '汉语拼音 Hanyu Pinyin', questions: [{ topic: '阅读理解 Comprehension', blocks: [1] }] });
  eq(own[0].topic, '阅读理解 Comprehension');
});

// ── the shapes that must NOT split ──────────────────────────────────────────

test('the old single-question shape still returns exactly one', () => {
  // Every ordinary screenshot comes back like this. Return nothing here and
  // Rapid add stops working altogether.
  const one = { title: '衬衫的拼音', topic: '汉语拼音 Hanyu Pinyin', blocks: [syn('a', 'b')] };
  eq(M._aiQuestionPayloads(one).length, 1);
  eq(M._aiQuestionPayloads(one)[0].title, '衬衫的拼音');
});

test('a page holding ONE question returns one, not zero', () => {
  eq(M._aiQuestionPayloads({ questions: [{ title: '单题', blocks: [syn('a', 'b')] }] }).length, 1);
});

test('a 阅读理解 passage stays ONE question with its parts', () => {
  // The opposite failure: torn apart, the sub-questions cannot be answered
  // because the passage they are about is attached to only the first of them.
  const passage = {
    title: '小贩中心', questionType: 'passage',
    blocks: [
      { type: 'text', text: '一篇关于小贩中心的短文。' },
      { type: 'mcq', part: 'a', options: ['1', '2'], correctIndex: 0 },
      { type: 'mcq', part: 'b', options: ['1', '2'], correctIndex: 1 }
    ]
  };
  const out = M._aiQuestionPayloads(passage);
  eq(out.length, 1, 'the passage was torn off its sub-questions');
  eq(out[0].blocks.length, 3, 'and every part must stay with it');
});

test('a 短文填空 stays ONE question, however many blanks it has', () => {
  // One clozemcq block IS the whole section. Split per blank and each blank
  // loses the passage that decides which word belongs in it.
  const cloze = {
    questions: [{
      title: '短文填空', topic: '短文填空 Cloze Passage',
      blocks: [{ type: 'clozemcq', startNum: 16, passage: '课外活动是学生生活的一部分。{{}}是体育、艺术……', blanks: [{ options: ['总算', '就算', '不管', '尽管'], correctIndex: 2 }] }]
    }]
  };
  const out = M._aiQuestionPayloads(cloze);
  eq(out.length, 1, 'the passage was split into one question per blank');
  eq(out[0].blocks[0].type, 'clozemcq');
});

// ── replies that are broken in some way ─────────────────────────────────────

test('an empty questions array falls back to the reply itself', () => {
  // A page that produced blocks must produce a question.
  const out = M._aiQuestionPayloads({ questions: [], title: '备用', blocks: [syn('a', 'b')] });
  eq(out.length, 1);
  eq(out[0].title, '备用');
});

test('entries with no blocks are dropped, not built as empty questions', () => {
  const out = M._aiQuestionPayloads({
    questions: [{ title: '真题', blocks: [syn('a', 'b')] }, { title: '空的', blocks: [] }, { title: '没有' }, null, 'nonsense']
  });
  eq(out.length, 1, 'an entry with nothing in it is not a question');
  eq(out[0].title, '真题');
});

test('a reply with nothing usable at all returns nothing', () => {
  // Rapid add turns this into a visible red card rather than a blank question.
  eq(M._aiQuestionPayloads({ questions: [] }), []);
  eq(M._aiQuestionPayloads({ questions: [{}] }), []);
  eq(M._aiQuestionPayloads(null), []);
  eq(M._aiQuestionPayloads('a string'), []);
  eq(M._aiQuestionPayloads(undefined), []);
});

test('questions that is not an array is ignored, not crashed on', () => {
  const out = M._aiQuestionPayloads({ questions: 'five', title: '还在', blocks: [syn('a', 'b')] });
  eq(out.length, 1);
  eq(out[0].title, '还在');
});

// ── what the model is actually told ─────────────────────────────────────────

test('the prompt asks how many questions the page holds, FIRST', () => {
  const p = M._aiBuildQuestionPrompt(false, 1);
  ok(/HOW MANY QUESTIONS/i.test(p), 'the count decision is missing from the prompt');
  ok(/SEPARATE questions/.test(p), p.slice(0, 200));
  ok(/Never merge them into one question with parts/i.test(p), 'nothing stops it clumping them into parts');
});

test('the prompt still protects the passage case', () => {
  const p = M._aiBuildQuestionPrompt(false, 1);
  ok(/is ONE question, however many numbers it carries/i.test(p), 'a passage must not be split: ' + p.slice(0, 400));
  ok(/letter its sub-questions/i.test(p), 'and its sub-questions are still lettered');
  ok(/短文填空 — ONE passage with numbered blanks/.test(p), '短文填空 must not be split per blank either');
});

test('the prompt says the paper\'s NUMBER is only a signal, never kept', () => {
  const p = M._aiBuildQuestionPrompt(false, 1);
  ok(/QUESTION NUMBER IS ONLY THE SIGNAL/i.test(p), 'nothing tells it to drop the number');
  ok(/no "part" field/i.test(p), 'the number must not become a part');
  ok(/（2）/.test(p), 'the full-width numbering a 华文 paper actually prints is not named');
});

test('the prompt asks for the block type to be chosen PER question', () => {
  const p = M._aiBuildQuestionPrompt(false, 1);
  ok(/decided per question and not once for the page/i.test(p), 'the type is decided once for the page: ' + p.slice(0, 300));
  ['synthesis', 'mcq', 'clozemcq'].forEach(t =>
    ok(p.indexOf('"' + t + '"') >= 0, 'the model is never told about "' + t + '"'));
});

test('the prompt asks for the questions ARRAY', () => {
  const p = M._aiBuildQuestionPrompt(false, 1);
  ok(/"questions":\[/.test(p), 'the array shape is missing');
  ok(/ONE question returns an array of ONE entry/i.test(p), 'a single question has to be expressible too');
});

// ── the guard: the paper's number never reaches the question ────────────────

test('the numbering stripper knows the forms a 华文 paper prints', () => {
  // ZH_PROMPT_RULES asks for the paper's punctuation exactly as printed, so
  // full-width is the normal case here, not the exotic one.
  const strip = s => M._epStripLeadNumber(s);
  eq(strip('2、弟弟不小心把果汁洒在自己的衬衫上。'), '弟弟不小心把果汁洒在自己的衬衫上。', 'the 顿号 form');
  eq(strip('（2）弟弟不小心把果汁洒在自己的衬衫上。'), '弟弟不小心把果汁洒在自己的衬衫上。', 'full-width brackets');
  eq(strip('2．弟弟不小心把果汁洒在自己的衬衫上。'), '弟弟不小心把果汁洒在自己的衬衫上。', 'the full-width full stop');
  eq(strip('61. Something in English.'), 'Something in English.', 'and the half-width form still works');
});

test('a number that is part of the question survives', () => {
  // The (?!digit) guard, in both widths: a quantity at the head of a sentence
  // is not a question number, and cutting it changes what the question asks.
  eq(M._epStripLeadNumber('2.5公斤的冰块放进水里。'), null, '"2.5公斤" was read as question 2');
  eq(M._epStripLeadNumber('50毫升的水加进杯子里。'), null, 'a bare number needs a separator after it');
  eq(M._epStripLeadNumber('２．５公斤的冰块。'), null, 'the same number written full-width');
});

test('the underline survives the numbering strip', () => {
  // The strip walks the markup rather than a plain-text offset, so the <u> the
  // 汉语拼音 question depends on is not sliced in half by it.
  eq(M._epStripLeadNumber('2、弟弟把果汁洒在<u>衬衫</u>上。'), '弟弟把果汁洒在<u>衬衫</u>上。');
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
