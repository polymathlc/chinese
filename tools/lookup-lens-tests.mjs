// Regression tests for 🔍 词语查询 — the look-up lens (`lu*`). Run with:
//     node tools/lookup-lens-tests.mjs            all cases
//     node tools/lookup-lens-tests.mjs <name>     one case
//
// It loads the REAL geometry, voice picking and prompt out of app.js, and
// parses index.html for the three pieces of markup the tool is nothing
// without.
//
// What fails silently here:
//
//   • A drag made right-to-left or bottom-to-top gives a NEGATIVE width, and a
//     rectangle with a negative width matches nothing — the tool reads as
//     broken only for left-handed dragging, which is exactly the half of the
//     testing nobody does.
//   • The crop maths maps the box onto the picture's own pixels. Off by a
//     factor and the model is sent a different part of the diagram and
//     explains a different word, fluently, with nothing on screen amiss.
//   • The card renders fields the prompt has to ask for by name. Rename one on
//     either side and that line is blank forever.
//   • Pinyin WITHOUT TONE MARKS is the wrong answer to "how do I say this",
//     and it looks perfectly fine.
//   • An English voice reading 衬衫 says something confident and wrong.
//   • The markup must be a DIRECT CHILD of <body>. Nested inside any of the
//     app's overlays it inherits display:none and no student ever sees it —
//     which is exactly what happened to the subject switcher in the Maths app
//     for nine minor versions.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const HTML = new URL('../index.html', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');
const html = fs.readFileSync(HTML, 'utf8');

const slice = (from, to, what) => {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(what + ' not found in app.js — did the banner comments change?');
  return src.slice(a, b);
};

const lu = slice('const LU_MIN_DRAG =', '// ---- the selection ---', 'lens constants')
  + slice('function _luRect()', 'function _luDrawBox()', 'lens rect')
  + slice('function _luCropBox(rect, r, natW, natH)', '// The picture under the box', 'lens crop box')
  + slice('const LU_FIELDS =', 'async function luLookUp(', 'lens prompts')
  + slice('function _luVoiceList()', 'function luSpeak(', 'lens voices');

const preamble = 'let currentUser = { uid: "u1" };\nlet _fakeVoices = [];\nconst window = { speechSynthesis: { getVoices: () => _fakeVoices }, SpeechSynthesisUtterance: function () {} };\n';
const M = await import('data:text/javascript;base64,' + Buffer.from(
  preamble + lu +
  '\nfunction __setLu(v) { _lu = v; }'
  + '\nfunction __setVoices(v) { _fakeVoices = v; _luVoices = null; }'
  + '\nexport { _luRect, _luCropBox, _luZhVoice, luCanSpeak, _luTextPrompt, _luImagePrompt, LU_FIELDS,'
  + ' LU_MIN_DRAG, LU_MAX_CHARS, LU_CROP_MAX, LU_SPEAK_RATE, __setLu, __setVoices };'
).toString('base64'));

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
function ok(v, msg) { if (!v) throw new Error(msg || 'expected truthy, got ' + v); }
function eq(a, b, msg) {
  if (JSON.stringify(a) !== JSON.stringify(b)) {
    throw new Error((msg ? msg + ': ' : '') + 'expected ' + JSON.stringify(b) + ', got ' + JSON.stringify(a));
  }
}
const near = (a, b, msg) => { if (Math.abs(a - b) > 0.001) throw new Error((msg || 'value') + ': expected ' + b + ', got ' + a); };

// ── the drag ─────────────────────────────────────────────────────────────────
test('a normal drag gives the box that was drawn', () => {
  M.__setLu({ x0: 100, y0: 50, x1: 220, y1: 90 });
  const r = M._luRect();
  eq([r.left, r.top, r.width, r.height], [100, 50, 120, 40], 'rect');
});

test('a drag made BACKWARDS still gives a positive box', () => {
  // Right-to-left and bottom-to-top. Without the min/abs this comes back with
  // a negative width, which intersects nothing at all.
  M.__setLu({ x0: 220, y0: 90, x1: 100, y1: 50 });
  const r = M._luRect();
  eq([r.left, r.top, r.width, r.height], [100, 50, 120, 40], 'reversed drag');
  eq([r.right, r.bottom], [220, 90], 'far edges');
});

test('a tap is below the drag floor', () => {
  ok(M.LU_MIN_DRAG >= 6, 'the floor must be big enough that a tap is not a selection');
  M.__setLu({ x0: 100, y0: 50, x1: 103, y1: 52 });
  const r = M._luRect();
  ok(r.width < M.LU_MIN_DRAG && r.height < M.LU_MIN_DRAG, 'a 3px drag should be refused');
});

// ── the crop ─────────────────────────────────────────────────────────────────
const imgRect = { left: 100, top: 100, right: 500, bottom: 400, width: 400, height: 300 };

test('a box inside the picture maps onto its own pixels', () => {
  // The picture is displayed at 400×300 and is really 800×600, so every
  // screen pixel is two of its own.
  const c = M._luCropBox({ left: 200, top: 150, right: 300, bottom: 200 }, imgRect, 800, 600);
  near(c.sx, 200, 'sx'); near(c.sy, 100, 'sy');
  near(c.sw, 200, 'sw'); near(c.sh, 100, 'sh');
});

test('a box drawn half off the picture is clamped to the overlap', () => {
  // Asking for pixels outside the bitmap draws nothing at all, so the crop
  // comes back blank and the model is sent an empty picture.
  const c = M._luCropBox({ left: 0, top: 0, right: 200, bottom: 200 }, imgRect, 800, 600);
  near(c.sx, 0, 'sx clamped'); near(c.sy, 0, 'sy clamped');
  near(c.sw, 200, 'sw is the overlap only'); near(c.sh, 200, 'sh is the overlap only');
});

test('a picture shown at its own size maps 1:1', () => {
  const c = M._luCropBox({ left: 150, top: 120, right: 250, bottom: 180 }, imgRect, 400, 300);
  near(c.sx, 50, 'sx'); near(c.sy, 20, 'sy'); near(c.sw, 100, 'sw'); near(c.sh, 60, 'sh');
});

test('a zero-size overlap still asks for at least one pixel', () => {
  const c = M._luCropBox({ left: 500, top: 400, right: 500, bottom: 400 }, imgRect, 800, 600);
  ok(c.sw >= 1 && c.sh >= 1, 'a canvas cannot be drawn 0 wide: ' + JSON.stringify(c));
});

// ── the prompt ───────────────────────────────────────────────────────────────
test('the prompt asks for TONE MARKS, by example', () => {
  ok(/TONE MARKS/i.test(M.LU_FIELDS), 'tone marks are not demanded');
  ok(M.LU_FIELDS.indexOf('chèn shān') >= 0, 'the example must SHOW the tone marks');
});

test('the prompt asks for every field the card renders', () => {
  // A field the card reads and the prompt never names is a line that is blank
  // for ever, on a card that otherwise looks complete.
  const card = src.slice(src.indexOf('function luOpenCard(state)'), src.indexOf('const ZHIME_DICT_URL'));
  const used = new Set();
  for (const m of card.matchAll(/\bd\.([a-zA-Z]+)/g)) used.add(m[1]);
  ok(used.size >= 5, 'expected the card to render several fields, found ' + [...used]);
  for (const f of used) ok(M.LU_FIELDS.indexOf('"' + f + '"') >= 0, 'the prompt never asks for "' + f + '"');
});

test('the text prompt carries the selection and the image prompt does not pretend to', () => {
  const t = M._luTextPrompt('衬衫');
  ok(t.indexOf('衬衫') >= 0, 'the selected text is missing from the prompt');
  ok(t.indexOf(M.LU_FIELDS) >= 0, 'the text prompt does not carry the field list');
  ok(M._luImagePrompt().indexOf(M.LU_FIELDS) >= 0, 'the image prompt does not carry the field list');
  ok(/Read the Chinese/i.test(M._luImagePrompt()), 'the image prompt must ask it to READ the picture first');
});

test('a whole sentence is answered with ONE word, and the card says which', () => {
  // Otherwise the student is told about a word they did not pick and has no
  // way of knowing that is what happened.
  ok(/least likely to know/i.test(M.LU_FIELDS), 'no rule for a multi-word selection');
  ok(/the student is shown this field/i.test(M.LU_FIELDS), 'the "word" field must be the one shown back');
});

test('the selection is capped before it is sent', () => {
  ok(M.LU_MAX_CHARS > 0 && M.LU_MAX_CHARS <= 300, 'LU_MAX_CHARS should bound a selection, got ' + M.LU_MAX_CHARS);
  ok(src.indexOf('.slice(0, LU_MAX_CHARS)') >= 0, '_luTextIn does not apply the cap');
});

// ── 🔊 ───────────────────────────────────────────────────────────────────────
test('a Chinese voice is chosen over the others', () => {
  M.__setVoices([{ lang: 'en-US', name: 'Alex' }, { lang: 'zh-CN', name: 'Ting' }, { lang: 'ja-JP', name: 'Kyoko' }]);
  eq(M._luZhVoice().name, 'Ting', 'wrong voice');
});

test('zh-HK and zh-TW count as Chinese voices', () => {
  M.__setVoices([{ lang: 'en-GB', name: 'Daniel' }, { lang: 'zh-HK', name: 'Sinji' }]);
  ok(M._luZhVoice(), 'a zh-* voice was not recognised');
});

test('with voices but NO Chinese one, the button is refused', () => {
  // An English voice reading 衬衫 is confident nonsense — worse than silence.
  M.__setVoices([{ lang: 'en-US', name: 'Alex' }]);
  eq(M._luZhVoice(), null, 'picked a non-Chinese voice');
  eq(M.luCanSpeak(), false, 'the speaker must be disabled');
});

test('an EMPTY voice list is "not loaded yet", not "no voice"', () => {
  // Safari and Chrome hand back nothing until the voices load; a button hidden
  // on that empty list never comes back.
  M.__setVoices([]);
  eq(M.luCanSpeak(), true, 'an empty list must not disable the button');
});

test('speaking cancels whatever is already speaking, and is slowed down', () => {
  const fn = src.slice(src.indexOf('function luSpeak('), src.indexOf('function _luSyncSpeakBtns('));
  ok(fn.indexOf('speechSynthesis.cancel()') >= 0, 'two voices can overlap');
  ok(fn.indexOf('u.rate = LU_SPEAK_RATE') >= 0, 'the rate is not applied');
  ok(M.LU_SPEAK_RATE < 1, 'this is being learned, not skimmed: ' + M.LU_SPEAK_RATE);
  ok(fn.indexOf("'zh-CN'") >= 0, 'no Chinese fallback language on the utterance');
});

// ── it is a READ ─────────────────────────────────────────────────────────────
test('nothing in the lens writes anything anywhere', () => {
  const block = src.slice(src.indexOf('// 🔍 词语查询'), src.indexOf("const ZHIME_DICT_URL"));
  for (const bad of ['setDoc(', 'updateDoc(', 'addDoc(', 'deleteDoc(', 'saveQuestion(', 'progressOnMarked(', '_setPartResult(']) {
    ok(block.indexOf(bad) < 0, 'the lens calls ' + bad + ' — looking a word up must never cost a mark or a credit');
  }
});

test('the look-up is cached on the prompt', () => {
  const fn = src.slice(src.indexOf('async function luLookUp('), src.indexOf('// ---- 🔊'));
  ok(fn.indexOf('askGeminiCached(') >= 0, 'the word a whole class looks up should be fetched once');
  ok(fn.indexOf('_luBusy') >= 0, 'no in-flight guard');
});

// ── the markup ───────────────────────────────────────────────────────────────
// Depth 0 means a direct child of <body>. Nested in one of the app's overlays
// the tool inherits display:none and is invisible for ever, with nothing on
// screen to hint at it — the exact bug that hid the Maths subject switcher.
// Read as MARKUP: scripts, styles and comments come out first, because the
// module is inside <body> and holds thousands of `<div` in its template
// strings. Lifted from the Maths app's harness, where this exact check exists
// because the failure really shipped there.
const VOID = new Set(['area','base','br','col','embed','hr','img','input',
                      'link','meta','param','source','track','wbr']);
function ancestorsOf(id) {
  const clean = html
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '');
  const from = clean.search(/<body\b/i);
  ok(from >= 0, 'no <body> in index.html');
  const stack = [];
  const tag = /<(\/?)([a-zA-Z][\w-]*)((?:"[^"]*"|'[^']*'|[^>])*?)(\/?)>/g;
  tag.lastIndex = from;
  let m;
  while ((m = tag.exec(clean))) {
    const [, close, name, attrs, selfShut] = m;
    const lower = name.toLowerCase();
    if (lower === 'body' && close) break;
    if (!close && new RegExp('\\bid\\s*=\\s*["\']' + id + '["\']').test(attrs)) {
      return stack.filter(t => t.tag !== 'body').map(t => t.label);
    }
    if (VOID.has(lower) || selfShut) continue;
    if (close) {
      for (let i = stack.length - 1; i >= 0; i--) if (stack[i].tag === lower) { stack.length = i; break; }
    } else {
      const idm = attrs.match(/\bid\s*=\s*["\']([^"\']+)["\']/);
      stack.push({ tag: lower, label: idm ? '#' + idm[1] : lower });
    }
  }
  return null;
}
test('the button, the picking layer and the card are direct children of <body>', () => {
  for (const id of ['luFab', 'luOverlay', 'luCard']) {
    const anc = ancestorsOf(id);
    ok(anc !== null, 'no element with id="' + id + '" in index.html');
    eq(anc, [], '#' + id + ' is nested inside <' + (anc || []).join('> <') +
                '> — an ancestor that is display:none hides it whatever luShow() sets');
  }
});

test('the picking layer is above the whole app, including the IME bar', () => {
  const z = (sel) => {
    const at = html.indexOf(sel);
    const chunk = html.slice(at, at + 700);
    const m = /z-index:\s*(\d+)/.exec(chunk);
    return m ? Number(m[1]) : -1;
  };
  const overlay = z('.lu-overlay {');
  ok(overlay > 100000, 'the picking layer must sit over every app overlay and the IME bar, got ' + overlay);
  ok(z('.lu-card {') > overlay, 'the card must be above the layer it replaces');
});

test('the picking layer takes the drag, not the page scroll', () => {
  const at = html.indexOf('.lu-overlay {');
  ok(/touch-action:\s*none/.test(html.slice(at, at + 700)),
    'without touch-action:none the first drag on a phone scrolls the page');
});

test('none of it prints', () => {
  ok(/@media print \{ \.lu-fab, \.lu-overlay, \.lu-card \{ display: none !important; \} \}/.test(html),
    'the lens would print as furniture on a worksheet');
});

test('the inline handlers are on window', () => {
  for (const f of ['luStart', 'luSpeak', 'luCloseCard', 'luCancel']) {
    ok(src.indexOf('window.' + f + ' = ' + f + ';') >= 0, f + ' is not on window — the button throws and looks dead');
  }
});

test('it is turned on from the one place every signed-in path goes through', () => {
  const fn = src.slice(src.indexOf('function configureSidebarForRole('), src.indexOf('function configureSidebarForRole(') + 2500);
  ok(fn.indexOf('luShow()') >= 0, 'the lens is never shown');
  ok(fn.indexOf('_luBindPicker()') >= 0, 'the picker is never bound');
  ok(src.indexOf('function luAvailable() { return !!currentUser; }') >= 0, 'the lens must be hidden before sign-in');
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
