// Does a question the author was told was saved actually exist? Run with:
//     node tools/question-persistence-tests.mjs            all cases
//     node tools/question-persistence-tests.mjs <name>     one case
//
// This harness exists because of the one bug in this app that leaves NOTHING on
// screen to see. Every authoring path grows `questionBank` / `vettingList`,
// redraws the page and says "Question added to bank ✓" before the Firestore
// write resolves — `saveQuestion(q); // async, non-blocking` at a dozen call
// sites — and then throws the result away. So a write that failed left a
// question that was on screen, in the bank, in the count, searchable and
// pickable for a worksheet, and in no database at all. It lasted exactly as
// long as the tab. There was no error, no red card, no gap in the numbering:
// the question was simply not there at the next sign-in.
//
// Three edges are pinned here, and every one of them is silent when wrong:
//
//   • THE ORDER OF A MOVE. Approving out of vetting writes the bank copy and
//     deletes the vetting one. Done in the wrong order — or in no order at all,
//     which is what unawaited writes amount to — a failed write deletes the
//     question from where it was and never writes it where it was going. Auto-
//     Vet ran that pair in a loop over the whole queue, which is how a batch
//     went at once.
//   • `_firestoreSafeQuestion` ON BOTH DOORS. Firestore rejects nested arrays,
//     and a table block holds its cells as array-of-arrays the moment
//     normalizeLoadedQuestion has touched it. saveQuestion converted them;
//     saveVettingQuestion did not, so every already-loaded table question sent
//     to vetting was refused — after the bank copy had been deleted.
//   • THE STASH. A write that fails after all its retries has to leave the
//     question somewhere, or the net is only as good as the connection.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const HTML = new URL('../index.html', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');
const html = fs.readFileSync(HTML, 'utf8');

const slice = (from, to, what) => {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(what + ' not found in app.js — did the banner comment change?');
  return src.slice(a, b);
};

// The function bodies under test, taken from app.js itself.
const safe    = slice('function _firestoreSafeQuestion(q)', '\nlet _inflightOps', '_firestoreSafeQuestion');
const table   = slice('function tableDataToFirestore(data)', '\nfunction ', 'tableDataToFirestore');
const stash   = slice('const UNSAVED_KEY =', '// Write one question doc with auto-retry.', 'the unsaved-question stash');
const blocked = slice('function _bankWriteBlocked()', '\nfunction _adminAnswerToolHtml', '_bankWriteBlocked');

// A localStorage that can be made to fail, because a browser in private mode
// has none and a full one throws on write — and the save path that calls the
// stash must survive both.
function fakeStorage() {
  const map = new Map();
  return {
    full: false,
    getItem(k) { return map.has(k) ? map.get(k) : null; },
    setItem(k, v) { if (this.full) throw new Error('QuotaExceededError'); map.set(k, String(v)); },
    removeItem(k) { map.delete(k); },
    _raw: map,
  };
}

function load() {
  const store = fakeStorage();
  const toasts = [];
  const painted = [];
  const M = new Function(`
    const store = arguments[0], toasts = arguments[1], painted = arguments[2];
    const localStorage = store;
    let currentUser = { uid: 'u1', name: 'Zhi Kai Chung' };
    let adminUid = null;
    let employee = false;
    let questionBank = [], vettingList = [];
    const showToast = (m, k) => toasts.push({ m, k });
    const _canAuthor = () => true;
    const _isEmployee = () => employee;
    const _xtAnnounceQuestion = () => {};
    const updateCounts = () => {};
    const populateTopicFilter = () => {};
    const renderQuestionBank = () => {};
    const renderVettingList = () => {};
    const normalizeLoadedQuestion = q => q;
    const document = { querySelectorAll: () => [], querySelector: () => null };
    // The two real doors are exercised separately (their bodies talk to
    // Firestore). What _unsavedRetryAll needs from them is their CONTRACT:
    // return true only when the write landed, and drop the stash entry when it
    // did. That the real ones honour it is pinned by the source checks below.
    let writeOk = true;
    const saveQuestion = async q => { if (!writeOk) return false; _unsavedDrop(q.id); return true; };
    const saveVettingQuestion = async q => { if (!writeOk) return false; _unsavedDrop(q.id); return true; };
    ${table}
    ${safe}
    ${stash}
    ${blocked}
    return {
      _unsavedKey, _unsavedRead, _unsavedWrite, _unsavedKeep, _unsavedDrop,
      _unsavedCount, _unsavedRetryAll, _unsavedPaint, _bankWriteBlocked,
      UNSAVED_MAX, store, toasts,
      bank: () => questionBank, vetting: () => vettingList,
      setUser(u) { currentUser = u; },
      setEmployee(v, uid) { employee = v; adminUid = uid || null; },
      setWriteOk(v) { writeOk = v; },
    };
  `)(store, toasts, painted);
  return M;
}

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};
const ok = (cond, what) => { if (!cond) throw new Error(what || 'expected true'); };
const q = (id, extra) => Object.assign({ id, title: 'Q' + id, blocks: [] }, extra || {});

// ── the stash: what a failed write leaves behind ─────────────────────────────

test('a failed write is kept, and comes back with its question intact', () => {
  const M = load();
  M._unsavedKeep(q('q1', { title: '汉语拼音 1', topic: '汉语拼音 Hanyu Pinyin' }), 'bank');
  const list = M._unsavedRead();
  eq(list.length, 1);
  eq(list[0].q.id, 'q1');
  eq(list[0].q.title, '汉语拼音 1');
  eq(list[0].where, 'bank');
});

test('vetting and bank are remembered apart', () => {
  // They go back to different collections. A vetting question replayed into the
  // bank would be approved by the recovery, unread by anybody.
  const M = load();
  M._unsavedKeep(q('q1'), 'bank');
  M._unsavedKeep(q('q2'), 'vetting');
  const where = M._unsavedRead().map(r => r.q.id + ':' + r.where).sort();
  eq(where, ['q1:bank', 'q2:vetting']);
});

test('an unknown destination is filed as bank, never left undefined', () => {
  const M = load();
  M._unsavedKeep(q('q1'), 'somewhere-else');
  eq(M._unsavedRead()[0].where, 'bank');
});

test('the SAME question failing twice is one entry, not two', () => {
  // A retry that fails again must not grow the stash a copy at a time — left
  // unchecked that is how the cap silently pushes out the real losses.
  const M = load();
  M._unsavedKeep(q('q1', { title: 'first go' }), 'bank');
  M._unsavedKeep(q('q1', { title: 'second go' }), 'bank');
  eq(M._unsavedCount(), 1);
  eq(M._unsavedRead()[0].q.title, 'second go', 'the newer attempt wins');
});

test('the stash is capped, newest kept', () => {
  const M = load();
  for (let i = 0; i < M.UNSAVED_MAX + 10; i++) M._unsavedKeep(q('q' + i), 'bank');
  eq(M._unsavedCount(), M.UNSAVED_MAX);
  eq(M._unsavedRead()[0].q.id, 'q' + (M.UNSAVED_MAX + 9), 'newest first');
});

test('a table question is stashed Firestore-SAFE', () => {
  // The whole point of the stash is to write the question later. Stored with
  // the nested arrays a loaded table carries, every retry would be refused for
  // the same reason the first write was.
  const M = load();
  M._unsavedKeep({ id: 'q1', blocks: [{ type: 'table', data: [['a', 'b'], ['c', 'd']], colWidths: [80, null] }] }, 'bank');
  const b = M._unsavedRead()[0].q.blocks[0];
  eq(b.data, { 0: { 0: 'a', 1: 'b' }, 1: { 0: 'c', 1: 'd' } });
  eq(b.colWidths, { 0: 80 });
});

test('the stash is keyed per ACCOUNT', () => {
  // Two teachers share a centre laptop. A stash replayed under the wrong uid
  // writes one author's questions into the other's bank — the same silent
  // cross-contamination the collection names exist to prevent, arriving
  // through localStorage instead.
  const M = load();
  M._unsavedKeep(q('q1'), 'bank');
  M.setUser({ uid: 'u2' });
  eq(M._unsavedCount(), 0, 'the other account sees none of it');
  M._unsavedKeep(q('q2'), 'bank');
  eq(M._unsavedRead()[0].q.id, 'q2');
  M.setUser({ uid: 'u1' });
  eq(M._unsavedRead()[0].q.id, 'q1', 'and the first account still has its own');
});

test('a signed-out stash never lands in a real account', () => {
  const M = load();
  M.setUser(null);
  ok(M._unsavedKey().endsWith(':anon'), 'no uid means the anon key, not a bare one');
});

test('dropping removes that question and leaves the rest', () => {
  const M = load();
  M._unsavedKeep(q('q1'), 'bank');
  M._unsavedKeep(q('q2'), 'bank');
  M._unsavedDrop('q1');
  eq(M._unsavedRead().map(r => r.q.id), ['q2']);
});

test('an id given as a number still drops the entry it names', () => {
  // Question ids are strings everywhere, but nothing enforces it at this door.
  const M = load();
  M._unsavedKeep(q(12), 'bank');
  M._unsavedDrop('12');
  eq(M._unsavedCount(), 0);
});

test('a question with no id is never stashed', () => {
  // It could not be written back — there would be nothing to write it to.
  const M = load();
  M._unsavedKeep({ title: 'no id' }, 'bank');
  M._unsavedKeep(null, 'bank');
  eq(M._unsavedCount(), 0);
});

test('a full or missing localStorage never throws', () => {
  // The stash is called from inside the save path. Throwing here would take
  // down the write it is trying to rescue — the one thing worse than no net.
  const M = load();
  M.store.full = true;
  const warn = console.warn;
  console.warn = () => {};   // the quota warning IS the expected behaviour here
  try { M._unsavedKeep(q('q1'), 'bank'); } finally { console.warn = warn; }
  eq(M._unsavedCount(), 0, 'nothing kept, but nothing thrown either');
});

test('a corrupted stash reads as empty rather than throwing', () => {
  const M = load();
  M.store.setItem(M._unsavedKey(), 'not json{{');
  eq(M._unsavedRead(), []);
  M.store.setItem(M._unsavedKey(), '{"not":"an array"}');
  eq(M._unsavedRead(), []);
  M.store.setItem(M._unsavedKey(), '[null,{"no":"q"},{"q":{"id":"q1"},"where":"bank"}]');
  eq(M._unsavedRead().length, 1, 'the readable entry survives its broken neighbours');
});

// ── the retry ────────────────────────────────────────────────────────────────

test('a recovered question is dropped from the stash and put on screen', async () => {
  const M = load();
  M._unsavedKeep(q('q1'), 'bank');
  M._unsavedKeep(q('q2'), 'vetting');
  const r = await M._unsavedRetryAll();
  eq(r, { ok: 2, left: 0 });
  eq(M._unsavedCount(), 0);
  eq(M.bank().map(x => x.id), ['q1']);
  eq(M.vetting().map(x => x.id), ['q2']);
});

test('a retry that fails again keeps the question', () => {
  // The one thing the stash must never do is lose the question it is holding.
  const M = load();
  M._unsavedKeep(q('q1'), 'bank');
  M.setWriteOk(false);
  return M._unsavedRetryAll().then(r => {
    eq(r, { ok: 0, left: 1 });
    eq(M._unsavedRead()[0].q.id, 'q1');
  });
});

test('a recovered question is not duplicated into a list that already has it', () => {
  // The bank load and the retry both run at sign-in, in that order.
  const M = load();
  M._unsavedKeep(q('q1'), 'bank');
  M.bank().push(q('q1'));
  return M._unsavedRetryAll().then(() => eq(M.bank().length, 1));
});

test('retrying an empty stash does nothing at all', async () => {
  const M = load();
  eq(await M._unsavedRetryAll(), { ok: 0, left: 0 });
});

// ── an employee with no bank pointer ─────────────────────────────────────────

test('an employee may not write until the teacher\'s bank has resolved', () => {
  // _bankOwnerUid falls back to the employee's OWN uid while adminUid is null,
  // and a question written there is one nobody ever sees again — not the
  // teacher, not a student, and not the employee, who gets the teacher's bank
  // back the moment the pointer resolves.
  const M = load();
  M.setEmployee(true, null);
  ok(M._bankWriteBlocked(), 'blocked while the pointer is unresolved');
  ok(M.toasts.length, 'and the author is told why');
  M.setEmployee(true, 'admin-uid');
  ok(!M._bankWriteBlocked(), 'allowed once it has resolved');
});

test('an admin is never blocked', () => {
  const M = load();
  M.setEmployee(false, null);
  ok(!M._bankWriteBlocked());
});

// ── the shape of app.js: what cannot be evaluated here ───────────────────────

// One function's source, by name.
function body(name) {
  const decl = new RegExp('(?:^|\\n)(?:async )?function ' + name + '\\s*\\(');
  const m = decl.exec(src);
  if (!m) throw new Error(name + ' not found in app.js');
  const from = m.index + (m[0].startsWith('\n') ? 1 : 0);
  // Walk braces from the header's opening brace to its match.
  let i = src.indexOf('{', from), depth = 0;
  for (let j = i; j < src.length; j++) {
    if (src[j] === '{') depth++;
    else if (src[j] === '}') { depth--; if (!depth) return src.slice(from, j + 1); }
  }
  throw new Error(name + ' has no closing brace');
}

test('BOTH save doors go through _firestoreSafeQuestion', () => {
  // saveVettingQuestion did not, and that alone destroyed every already-loaded
  // table question sent back to vetting: Firestore rejects nested arrays, so
  // the write was refused three times over — after the bank copy was deleted.
  ['saveQuestion', 'saveVettingQuestion'].forEach(fn => {
    ok(/_firestoreSafeQuestion\(q\)/.test(body(fn)), fn + ' must build its payload with _firestoreSafeQuestion');
    ok(!/setDoc\(_[qv]Ref\(q\.id\),\s*q\)/.test(body(fn)), fn + ' must never write the raw question');
  });
});

test('BOTH save doors report whether the write landed', () => {
  ['saveQuestion', 'saveVettingQuestion'].forEach(fn => {
    const b = body(fn);
    ok(/return done\(true\)/.test(b), fn + ' must return true only on a real write');
    ok(/return done\(false\)/.test(b), fn + ' must return false when it gave up');
  });
});

test('BOTH save doors stash on failure and drop on success', () => {
  ['saveQuestion', 'saveVettingQuestion'].forEach(fn => {
    const b = body(fn);
    const wrote = b.indexOf('await setDoc(');
    const caught = b.indexOf('} catch (err) {');
    const drop = b.indexOf('_unsavedDrop(q.id)');
    ok(drop > wrote && drop < caught, fn + ': the drop belongs between the write landing and the catch');
    // The keep may appear more than once — the door also refuses to write at
    // all when the bank owner is unresolved — so the one that matters is the
    // one inside the catch.
    ok(b.indexOf('_unsavedKeep(q,', caught) > caught, fn + ' must keep the question when it gives up');
  });
});

test('a move WRITES the destination before deleting the source', () => {
  // The order is the whole fix. Reversed — or unordered, which is what an
  // unawaited write amounts to — a failed write deletes the question from
  // where it was and never writes it where it was going.
  [['moveVettingToBank', '_vRef'], ['moveBankToVetting', '_qRef']].forEach(([fn, srcRef]) => {
    const b = body(fn);
    const wrote = Math.max(b.indexOf('await saveQuestion(q'), b.indexOf('await saveVettingQuestion(q'));
    const deleted = b.indexOf('deleteDoc(' + srcRef);
    ok(wrote > 0, fn + ' must await its destination write');
    ok(deleted > wrote, fn + ' must delete the source only after the write');
    ok(/if \(!ok\)/.test(b), fn + ' must return early when the write did not land');
  });
});

test('a FAILED move stashes nothing', () => {
  // There is nothing to rescue: the question is still whole in the collection
  // it was moving out of. Stash it as well and the next sign-in writes a SECOND
  // copy into the destination, beside the row it never left — the ordering fix
  // turned into a duplicating one.
  ['moveVettingToBank', 'moveBankToVetting'].forEach(fn => {
    ok(/noStash: true/.test(body(fn)), fn + ' must pass noStash to its save door');
  });
  // And the doors have to honour it, in both the refusal and the give-up path.
  ['saveQuestion', 'saveVettingQuestion'].forEach(fn => {
    const keeps = body(fn).match(/_unsavedKeep\(q,/g) || [];
    const guarded = body(fn).match(/if \(!\(opts && opts\.noStash\)\) _unsavedKeep\(q,/g) || [];
    eq(guarded.length, keeps.length, fn + ': every _unsavedKeep must be behind the noStash check');
  });
});

test('every path that moves a question uses one of the two doors', () => {
  // Five of them did it by hand, all five in the losing order. A sixth added
  // later must not reinvent it — which is what this case is for.
  const movers = {
    approveVetting: 'moveVettingToBank',
    _runAutoVet: 'moveVettingToBank',
    saveEditToBank: 'moveVettingToBank',
    moveEditToVetting: 'moveBankToVetting',
    flagMoveToVetting: 'moveBankToVetting',
  };
  Object.entries(movers).forEach(([fn, door]) => {
    const b = body(fn);
    ok(b.indexOf('await ' + door) >= 0, fn + ' must move through ' + door);
    ok(!/\n\s*deleteVettingDoc\(/.test(b), fn + ' must not delete a vetting doc by hand');
    ok(!/\n\s*deleteQuestionDoc\(/.test(b), fn + ' must not delete a bank doc by hand');
  });
});

test('no mover deletes a document itself, or fires a vetting write nobody waits for', () => {
  // The exact shape of the original bug: a write nobody waits for, and a
  // deletion that happens regardless of what it did.
  //
  // A plain `saveQuestion(q);` is still allowed here — saveEditToBank uses one
  // for an ordinary bank edit, which deletes nothing and has the stash behind
  // it. What may never come back is a raw deleteDoc beside it.
  ['approveVetting', '_runAutoVet', 'saveEditToBank', 'moveEditToVetting', 'flagMoveToVetting'].forEach(fn => {
    const b = body(fn);
    ok(!/\bdeleteDoc\(/.test(b), fn + ' must not delete a document itself — the move doors do that, in order');
    ok(!/(?<!await )\bsaveVettingQuestion\(/.test(b),
      fn + ' must await saveVettingQuestion — its result decides whether the source may go');
  });
});

test('the stash is retried on every authoring sign-in', () => {
  // Admin and employee alike. A net only one of the two roles gets is a net the
  // other's questions fall through.
  const enter = body('enterApp');
  eq((enter.match(/unsavedInit\(\)/g) || []).length, 2, 'unsavedInit must run on both authoring branches');
});

test('the banner has somewhere to paint, on both pages', () => {
  // _unsavedPaint fills every .unsaved-banner. With no host element the stash
  // still works and nobody is ever told it is holding anything.
  eq((html.match(/class="unsaved-banner"/g) || []).length, 2, 'one on the bank page, one on vetting');
  ok(/\.unsaved-banner\s*\{/.test(html), 'and it must be styled, or it paints as unstyled text');
  ok(/window\.unsavedRetryNow\s*=/.test(src), 'the banner button is an inline onclick — it needs the window export');
});

test('the stash name is Zh-marked like every other stored name', () => {
  const m = /const UNSAVED_KEY = '([^']+)'/.exec(src);
  ok(m, 'UNSAVED_KEY must be a named constant');
  // Same rule the collection names follow: ends in `Zh` or starts with `zh`.
  ok(/Zh$|^zh/.test(m[1]), 'a key shared with two sibling portals on one domain must say which app it belongs to');
});

// ── runner ───────────────────────────────────────────────────────────────────

const only = process.argv[2];
let passed = 0, failed = 0;
for (const c of cases) {
  if (only && c.name !== only) continue;
  try { await c.fn(); console.log('  ok   ' + c.name); passed++; }
  catch (err) { console.log('  FAIL ' + c.name + '\n         ' + err.message); failed++; }
}
console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
