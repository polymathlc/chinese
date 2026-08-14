// Can this app reach a collection that is not its own? Run with:
//     node tools/bank-isolation-tests.mjs            all cases
//     node tools/bank-isolation-tests.mjs <name>     one case
//
// Three portals — Science (`polymathlc/cer`), English (`polymathlc/english`)
// and this one — share ONE Firebase project, ONE sign-in and therefore one
// `users/{uid}` tree. The only thing keeping their question banks apart is the
// NAME of each collection, so this harness reads app.js as text and checks the
// shape of every Firestore path in it.
//
// It exists because this failure has already happened once, and it did not look
// like a failure. The English portal's four bank helpers spelled 'questions'
// and 'vetting' inline — the Science app's own names, under the same uid — so
// for three versions the two apps were one bank wearing two front ends. Nothing
// threw. Nothing looked broken. The only symptom was the wrong subject's
// questions on the bank page, which reads as a filter bug.
//
// A shared-name path fails LOUDLY nowhere and quietly everywhere, which is why
// this is a test and not a comment.
import fs from 'fs';

const APP = new URL('../app.js', import.meta.url).pathname;
const RULES = new URL('../firestore.rules', import.meta.url).pathname;
const src = fs.readFileSync(APP, 'utf8');
const rules = fs.readFileSync(RULES, 'utf8');

// ── the declared collection constants ────────────────────────────────────────
const DOC_CONSTS = ['GAPS_DOC'];          // a document name, not a collection
const cols = {};
{
  const re = /^const ([A-Z][A-Z0-9_]*(?:_COL|_DOC))\s*=\s*'([^']+)'/gm;
  let m;
  while ((m = re.exec(src))) if (!DOC_CONSTS.includes(m[1])) cols[m[1]] = m[2];
}

// ── every doc()/collection() call made against db, with its arguments ────────
function dbCalls() {
  const out = [];
  const head = /\b(collection|doc)\(\s*db\s*,/g;
  let h;
  while ((h = head.exec(src))) {
    let i = head.lastIndex, depth = 1, args = '';
    while (i < src.length) {
      const c = src[i];
      if (c === '(') depth++;
      else if (c === ')') { depth--; if (!depth) break; }
      args += c; i++;
    }
    out.push({ kind: h[1], args, line: src.slice(0, h.index).split('\n').length });
  }
  return out;
}
// Split on top-level commas only.
function segs(s) {
  const out = []; let depth = 0, cur = '';
  for (const c of s) {
    if ('([{'.includes(c)) depth++;
    if (')]}'.includes(c)) depth--;
    if (c === ',' && depth === 0) { out.push(cur.trim()); cur = ''; continue; }
    cur += c;
  }
  if (cur.trim()) out.push(cur.trim());
  return out;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const cases = [];
const test = (name, fn) => cases.push({ name, fn });
function ok(v, msg) { if (!v) throw new Error(msg || 'expected truthy'); }
function eq(a, b, msg) {
  const A = JSON.stringify(a), B = JSON.stringify(b);
  if (A !== B) throw new Error((msg ? msg + ': ' : '') + 'expected ' + B + ', got ' + A);
}

// ── 1. the names themselves ──────────────────────────────────────────────────

test('every collection constant carries this app\'s marker', () => {
  const n = Object.keys(cols).length;
  ok(n >= 20, 'only ' + n + ' collection constants found — did the block move?');
  const unmarked = Object.entries(cols).filter(([, v]) => !/Zh$/.test(v) && !/^zh[A-Z]/.test(v));
  eq(unmarked, [], 'these do not end in Zh or start with zh');
});

test('no two constants point at the same collection', () => {
  const seen = {};
  Object.entries(cols).forEach(([k, v]) => { (seen[v] = seen[v] || []).push(k); });
  eq(Object.entries(seen).filter(([, ks]) => ks.length > 1), [], 'duplicated collection names');
});

// ── 2. no literal where a collection goes ────────────────────────────────────

test('every collection in a path comes from a CONSTANT, never a literal', () => {
  // This is the v1.3.0 bug, stated as a rule. Arguments alternate
  // collection, id, collection, id… so every even slot names a collection.
  const bad = [];
  dbCalls().forEach(c => {
    segs(c.args).forEach((p, i) => {
      if (i % 2) return;                                  // a document id
      const lit = /^'([^']*)'$/.exec(p);
      if (!lit || lit[1] === 'users') return;             // 'users' is the shared root
      bad.push('app.js:' + c.line + ' ' + c.kind + '() → ' + JSON.stringify(lit[1]));
    });
  });
  eq(bad, [], 'a collection is named by a literal');
});

test('there are paths to check at all', () => {
  // A guard on the guard: if the scan silently matched nothing, every other
  // case above would pass while checking an empty list.
  ok(dbCalls().length > 100, 'only ' + dbCalls().length + ' db path calls found — the scan is broken');
});

// ── 3. the other two apps' names appear nowhere in a path ────────────────────

test('no Science or English collection name is used as a collection', () => {
  const FOREIGN = new Set([
    'questions', 'vetting', 'scheduledQuestions', 'mistakes', 'flashcards', 'bin',
    'settings', 'worksheets', 'teachingNotes', 'stats', 'workSessions',
    'questionsEn', 'vettingEn', 'binEn', 'settingsEn', 'teachingNotesEn', 'statsEn',
    'worksheetsEn', 'workSessionsEn', 'mistakesEn', 'flashcardsEn', 'scheduledQuestionsEn',
    'enUserProfiles', 'enConfig', 'enProgress', 'enQuestionAttempts', 'enFlaggedQuestions',
    'enCommunity', 'enEncounterQuests', 'enMessages', 'enLoginEvents', 'enWorkSessions',
    'userProfiles', 'cerConfig', 'cerProgress', 'cerQuestionAttempts',
  ]);
  // Checked as a VALUE of a constant and as a literal in a path — not as bare
  // text, because 'vetting' is also a page name and 'mistakes' a field value.
  const asConst = Object.entries(cols).filter(([, v]) => FOREIGN.has(v));
  eq(asConst, [], 'a constant points at another app\'s collection');

  const inPath = [];
  dbCalls().forEach(c => segs(c.args).forEach((p, i) => {
    const lit = /^'([^']*)'$/.exec(p);
    if (i % 2 === 0 && lit && FOREIGN.has(lit[1])) inPath.push('app.js:' + c.line + ' ' + lit[1]);
  }));
  eq(inPath, [], 'another app\'s collection is named in a path');
});

// ── 4. the four doors to the bank ────────────────────────────────────────────

test('_qRef / _vRef / _qCol / _vCol all go through the constant', () => {
  ['_qRef', '_vRef', '_qCol', '_vCol'].forEach(fn => {
    const hit = new RegExp('function ' + fn + '\\([^)]*\\)\\s*\\{[^}]*\\}').exec(src);
    ok(hit, fn + ' not found');
    ok(/QUESTIONS_COL|VETTING_COL/.test(hit[0]), fn + ' does not use the constant');
    ok(!/'(questions|vetting)/.test(hit[0]), fn + ' spells a collection inline');
  });
});

// ── 5. the shared document ───────────────────────────────────────────────────

test('nothing writes to the bare users/{uid} document', () => {
  // `users/{uid}` is the ONE document all three portals share — same project,
  // same sign-in, same uid. Both siblings write `students` and
  // `studentSetupSeen` straight onto it, so a roster saved there is the same
  // roster in every subject and the last app to save wins.
  const bad = [];
  dbCalls().forEach(c => {
    const p = segs(c.args);
    if (c.kind === 'doc' && p.length === 2 && /^'users'$/.test(p[0])) {
      bad.push('app.js:' + c.line + ' doc(db, ' + p.join(', ') + ')');
    }
  });
  eq(bad, [], 'the shared user document is addressed directly');
});

test('there is no legacy single-doc migration', () => {
  // Ported from either sibling, it reads `questionBank` / `vettingList` arrays
  // off the SHARED user document and writes each question into this app's bank
  // through _qRef — a Chinese bank filled with another subject's questions, in
  // one silent pass, on the teacher's first sign-in. This app has never had a
  // single-doc format, so any such array under that uid belongs elsewhere.
  ok(!/old\.questionBank|old\.vettingList/.test(src), 'the legacy migration is back');
  ok(!/Migrating from legacy single-doc/.test(src), 'the legacy migration is back');
});

// ── 6. the rules ─────────────────────────────────────────────────────────────

const ruled = new Set();
{
  const re = /match \/(?:\{database\}\/documents\/)?([A-Za-z0-9_]+)\//g;
  let r;
  while ((r = re.exec(rules))) ruled.add(r[1]);
}

test('every collection this app uses has a Firestore rule', () => {
  // A name the rules do not know fails CLOSED: reads come back empty, writes
  // are denied, and nothing on screen explains why.
  const missing = Object.entries(cols).filter(([, v]) => !ruled.has(v)).map(([k, v]) => k + ' (' + v + ')');
  eq(missing, [], 'no rule — the page will be silently blank');
});

test('the rules grant nothing outside this app', () => {
  const mine = new Set(Object.values(cols));
  const stray = [...ruled].filter(n => n !== 'users' && n !== 'databases' && !mine.has(n));
  eq(stray, [], 'the rules name a collection this app does not use');
});

test('the rules never name a sibling\'s collection', () => {
  ['questionsEn', 'vettingEn', 'enConfig', 'enUserProfiles'].forEach(n =>
    ok(!ruled.has(n), 'the rules grant access to ' + n));
  // The plain Science names must not appear either — granting them here would
  // widen the Science app's own rules from this file.
  ['questions', 'vetting', 'scheduledQuestions'].forEach(n =>
    ok(!ruled.has(n), 'the rules grant access to the Science app\'s ' + n));
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
