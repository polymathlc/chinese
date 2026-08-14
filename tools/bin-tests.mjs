// Regression tests for 🗑 THE BIN and the write-safety helper it shares with
// every save. Run with:
//     node tools/bin-tests.mjs            all cases
//     node tools/bin-tests.mjs <name>     one case
//
// It loads the REAL `_firestoreSafeQuestion`, `_binExpiryMs`, `binDaysLeft`,
// `binExpired` and `_binRecord` out of app.js.
//
// Deleting a question is the one action in this app that destroys work, and the
// bin is what makes it survivable — so both of its edges are pinned here:
//
//   • the CALENDAR. A day counted wrong purges somebody's question early, and
//     an unparseable date either purges it instantly or keeps it forever. The
//     purge is a background sweep, so neither leaves a trace on screen.
//   • the RECORD. Restore rebuilds the question out of what was stored, so a
//     field lost on the way in is a question that comes back broken — a week
//     later, with nothing left to compare it against.
//
// `_firestoreSafeQuestion` is here because the bin shares it with saveQuestion:
// Firestore rejects nested arrays, so a table question written without the
// conversion fails to save at all.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');

const slice = (from, to, what) => {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(what + ' not found in app.js — did the banner comment change?');
  return src.slice(a, b);
};

const safe    = slice('function _firestoreSafeQuestion(q)', '\nlet _inflightOps', '_firestoreSafeQuestion');
const table   = slice('function tableDataToFirestore(data)', '\nfunction ', 'tableDataToFirestore');
const binCalc = slice('function _binExpiryMs(rec)', 'async function binLoad', 'the bin date + record block');

const M = new Function(`
  let currentUser = { uid: 'u1', name: 'Zhi Kai Chung' };
  const BIN_DAYS = ${/const BIN_DAYS = (\d+)/.exec(src)[1]};
  ${table}
  ${safe}
  ${binCalc}
  return {
    _firestoreSafeQuestion, _binExpiryMs, binDaysLeft, binExpired, _binRecord, BIN_DAYS,
    setUser(u) { currentUser = u; },
  };
`)();

const DAY = 864e5;
const agoIso = days => new Date(Date.now() - days * DAY).toISOString();

const cases = [];
const test = (name, fn) => cases.push({ name, fn });
const eq = (got, want, what) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    throw new Error((what || 'value') + ': got ' + JSON.stringify(got) + ', wanted ' + JSON.stringify(want));
  }
};
const ok = (cond, what) => { if (!cond) throw new Error(what || 'expected true'); };

// ── the calendar ─────────────────────────────────────────────────────────────

test('a question deleted just now has the FULL week left', () => {
  // Rounded up, or a question deleted at 11pm shows "6 days" a minute later and
  // the bin quietly promises a day less than it says on the dialog.
  eq(M.binDaysLeft({ deletedAt: new Date().toISOString() }), M.BIN_DAYS);
  eq(M.binDaysLeft({ deletedAt: agoIso(0.9) }), M.BIN_DAYS);
});

test('the count comes down one day at a time', () => {
  eq(M.binDaysLeft({ deletedAt: agoIso(1) }), 6);
  eq(M.binDaysLeft({ deletedAt: agoIso(3) }), 4);
  eq(M.binDaysLeft({ deletedAt: agoIso(6.5) }), 1);
});

test('nothing is swept before its seventh day', () => {
  // The one failure that destroys work. Every hour of the last day must hold.
  for (const d of [0, 1, 3, 6, 6.5, 6.9, 6.99]) {
    ok(!M.binExpired({ deletedAt: agoIso(d) }), `expired after only ${d} days`);
    ok(M.binDaysLeft({ deletedAt: agoIso(d) }) > 0, `showed 0 days left after ${d} days`);
  }
});

test('past seven days it is expired, and says 0 left', () => {
  ok(M.binExpired({ deletedAt: agoIso(7.01) }), 'not expired at 7.01 days');
  ok(M.binExpired({ deletedAt: agoIso(30) }), 'not expired at 30 days');
  eq(M.binDaysLeft({ deletedAt: agoIso(7.01) }), 0);
  eq(M.binDaysLeft({ deletedAt: agoIso(90) }), 0);
});

test('a record with no readable date is KEPT, never swept', () => {
  // The two mistakes are not equal. Keeping one too long leaves a row in a
  // dialog with a Delete forever button next to it; sweeping one too early
  // destroys work in a background job, with nothing on screen to show it.
  [undefined, null, {}, { deletedAt: '' }, { deletedAt: 'whenever' }, { deletedAt: {} }].forEach(r => {
    ok(!M.binExpired(r), 'swept a record whose date could not be read: ' + JSON.stringify(r));
    eq(M.binDaysLeft(r), null, 'days left for ' + JSON.stringify(r));
  });
});

test('a NUMBER is not read as a date', () => {
  // Date.parse coerces, and Date.parse('12345') is the YEAR 12345 — so a
  // timestamp stored as a number would have sat in the bin for ten millennia
  // while reading as perfectly healthy. Only an ISO string counts.
  [12345, Date.now(), 0].forEach(n => {
    ok(!M.binExpired({ deletedAt: n }), 'a numeric date was treated as readable: ' + n);
    eq(M.binDaysLeft({ deletedAt: n }), null, 'days left for ' + n);
    eq(M._binExpiryMs({ deletedAt: n }), null, 'expiry for ' + n);
  });
});

test('the expiry is exactly BIN_DAYS after the deletion', () => {
  const at = '2026-08-14T03:48:13.000Z';
  eq(M._binExpiryMs({ deletedAt: at }), Date.parse(at) + M.BIN_DAYS * DAY);
});

// ── the record ───────────────────────────────────────────────────────────────

test('the whole question is stored, not a summary of it', () => {
  const q = { id: 'q1', title: 'Phrasal Verbs with Call', topic: 'Vocabulary',
    category: 'Multiple Choice Question', tags: ['phrasal verbs'], los: ['lo-1'],
    blocks: [{ type: 'mcq', options: [{ text: 'call in' }, { text: 'call on' }] }] };
  const rec = M._binRecord(q, 'bank');
  eq(rec.question, q, 'the stored question');
  eq(rec.id, 'q1');
  eq(rec.from, 'bank');
});

test('a row can be read without unpacking the question', () => {
  const rec = M._binRecord({ id: 'q1', title: 'Phrasal Verbs with Call', topic: 'Vocabulary' }, 'bank');
  eq(rec.title, 'Phrasal Verbs with Call');
  eq(rec.topic, 'Vocabulary');
  ok(rec.deletedAt && !Number.isNaN(Date.parse(rec.deletedAt)), 'deletedAt is a real date');
});

test('who deleted it is recorded, and a missing name is not a crash', () => {
  eq(M._binRecord({ id: 'q1' }, 'bank').deletedByName, 'Zhi Kai Chung');
  M.setUser(null);
  const rec = M._binRecord({ id: 'q1' }, 'bank');
  eq(rec.deletedBy, '');
  eq(rec.deletedByName, '');
  M.setUser({ uid: 'u1', name: 'Zhi Kai Chung' });
});

test('an untitled question still gets a name in the bin', () => {
  // A blank row is one nobody can identify to restore.
  eq(M._binRecord({ id: 'q1' }, 'bank').title, 'Untitled question');
  eq(M._binRecord({ id: 'q1', title: '   ' }, 'bank').title, 'Untitled question');
});

test('a fresh record is not already expired', () => {
  const rec = M._binRecord({ id: 'q1', title: 'x' }, 'bank');
  ok(!M.binExpired(rec), 'a question was binned and immediately expired');
  eq(M.binDaysLeft(rec), M.BIN_DAYS);
});

// ── the write-safety helper (shared with every save) ─────────────────────────

test('a table question is converted — Firestore rejects nested arrays', () => {
  const q = { id: 'q1', blocks: [{ type: 'table', data: [['a', 'b'], ['c', 'd']], colWidths: [80, 120] }] };
  const out = M._firestoreSafeQuestion(q);
  eq(out.blocks[0].data, { 0: { 0: 'a', 1: 'b' }, 1: { 0: 'c', 1: 'd' } }, 'table data');
  eq(out.blocks[0].colWidths, { 0: 80, 1: 120 }, 'colWidths');
});

test('the in-memory question is left exactly as it was', () => {
  // The editor and the bank are still holding this object; converting it in
  // place would break every table on screen.
  const q = { id: 'q1', blocks: [{ type: 'table', data: [['a']], colWidths: [80] }] };
  M._firestoreSafeQuestion(q);
  eq(q.blocks[0].data, [['a']], 'data after conversion');
  eq(q.blocks[0].colWidths, [80], 'colWidths after conversion');
});

test('a question needing nothing is passed straight through', () => {
  const q = { id: 'q1', blocks: [{ type: 'text', content: '<p>hi</p>' }] };
  ok(M._firestoreSafeQuestion(q) === q, 'a question with no tables was needlessly copied');
});

test('an already-converted table is not converted twice', () => {
  const q = { id: 'q1', blocks: [{ type: 'table', data: { 0: { 0: 'a' } }, colWidths: { 0: 80 } }] };
  const out = M._firestoreSafeQuestion(q);
  eq(out.blocks[0].data, { 0: { 0: 'a' } });
  eq(out.blocks[0].colWidths, { 0: 80 });
});

test('a null cell becomes an empty string, never a dropped key', () => {
  const q = { id: 'q1', blocks: [{ type: 'table', data: [['a', null, undefined]] }] };
  eq(M._firestoreSafeQuestion(q).blocks[0].data, { 0: { 0: 'a', 1: '', 2: '' } });
});

test('a hole in colWidths is skipped, not written as null', () => {
  const q = { id: 'q1', blocks: [{ type: 'table', data: [['a']], colWidths: [80, null, 120] }] };
  eq(M._firestoreSafeQuestion(q).blocks[0].colWidths, { 0: 80, 2: 120 });
});

test('a malformed question never throws', () => {
  [null, undefined, {}, { blocks: null }, { blocks: [null] }, { blocks: [{ type: 'table' }] }]
    .forEach(q => M._firestoreSafeQuestion(q));
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
