// Regression tests for 🏆 THE JOURNEY LEADERBOARD.
// Run with:
//     node tools/journey-board-tests.mjs            all cases
//     node tools/journey-board-tests.mjs <name>     one case
//
// It loads the REAL scoring and ranking out of app.js and runs them over
// synthetic board rows. There is MONEY on this board — the top three each win a
// voucher — and every way it can go wrong is silent: the page paints, the
// medals line up, the numbers look plausible, and the wrong child is paid.
//
//  • THE BOARD RANKS ON THE NUMBER OF QUESTIONS ANSWERED RIGHT, and on
//    nothing else. It is the one number a student can count for themselves.
//    Anything else quietly ranked in — accuracy, a weighting, how far the run
//    got — is a board whose order nobody can check.
//  • THE MONTH KEY IS SINGAPORE TIME, and it must agree with the one the game
//    writes (monthKey in journey/index.html). Drift by one hour and a run
//    answered late on the 31st is filed in a month the board is not showing.
//  • RANKING AND PAYING ARE DIFFERENT QUESTIONS. A row ranks on its score; it
//    is only PAYABLE with real work behind it, or a voucher is decided by
//    somebody who answered three questions and happened to get them right.
//  • A TIE MUST BREAK ON SOMETHING VISIBLE. Two students on the same score in
//    an order nobody can explain is a board nobody trusts twice.
//  • THE CHAPTER DECIDES NOTHING. It is climbable by replaying the easy
//    chapters, so it is shown and never ranked on.
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

// The board's pure half — everything up to the first function that touches the
// DOM, so the harness needs no document.
const block = cut('const JB_SUBJECT', '\nfunction jbSetTab', 'board');
const B = new Function(block + `
return { jbScore, jbStats, jbRank, jbPrizeWinners, jbMonthKey, jbMonthLabel,
         JB_PRIZE_TOP, JB_MIN_QUESTIONS, JB_PRIZE_TEXT, JB_SUBJECT };`)();

let pass = 0, fail = 0;
const queue = [];
const section = title => queue.push(async () => console.log(title));
const only = process.argv[2];
function test(name, fn) {
  if (only && !name.includes(only)) return;
  queue.push(async () => {
    try { await fn(); console.log('  ✅ ' + name); pass++; }
    catch (e) { console.log('  ❌ ' + name + '\n     ' + e.message); fail++; }
  });
}
const eq = (a, b, m) => { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error((m || '') + ' expected ' + JSON.stringify(b) + ', got ' + JSON.stringify(a)); };
const ok = (v, m) => { if (!v) throw new Error(m || 'expected truthy'); };

const KEY = B.jbMonthKey();
const row = (uid, c, a, chapter = 1, months = null) => ({
  uid, name: uid, email: uid + '@x', correct: c, answered: a, bestChapter: chapter,
  months: months || { [KEY]: { c, a } }
});

section('\nTHE SCORE — the number of questions answered right, and nothing else');

test('the score IS the questions answered right', () => {
  eq(B.jbScore(40, 40), 40);
  eq(B.jbScore(40, 80), 40, 'the score was weighted by something other than the count');
  eq(B.jbScore(7, 200), 7);
});

test('accuracy does not enter the score at all', () => {
  // The same number right, answered over wildly different amounts, must score
  // the same — otherwise the board is ranked on something a student cannot
  // count for themselves.
  eq(B.jbScore(30, 30), B.jbScore(30, 300));
});

test('doing MORE always ranks higher, however loose', () => {
  ok(B.jbScore(315, 900) > B.jbScore(200, 200), 'more questions right must rank higher');
});

test('nothing answered is nothing scored', () => { eq(B.jbScore(0, 0), 0); eq(B.jbScore(5, 0), 0); });

test('a score can never exceed the questions answered', () => {
  for (const [c, a] of [[10, 10], [7, 10], [1, 50], [99, 100]]) {
    ok(B.jbScore(c, a) <= a, c + '/' + a + ' scored ' + B.jbScore(c, a));
  }
});

test('a nonsense row cannot score more than it answered', () => {
  ok(B.jbScore(500, 10) <= 10, 'a row claiming more right than done must not out-rank the board');
  eq(B.jbScore(-5, 10), 0);
});

section('\nTHE MONTH — which board a run lands on');

test('the month key is SINGAPORE time and shaped YYYY-MM', () => {
  ok(/^\d{4}-\d{2}$/.test(KEY), 'got ' + KEY);
  // 31 Dec 2025, 20:00 UTC is already 1 Jan 2026 in Singapore.
  eq(B.jbMonthKey(new Date('2025-12-31T20:00:00Z')), '2026-01');
  // …and 16:00 UTC on the 31st is still December there.
  eq(B.jbMonthKey(new Date('2025-12-31T15:00:00Z')), '2025-12');
});

test('the key the board reads is the key the GAME writes', () => {
  // The game carries its own copy — it is a separate page and cannot import
  // this one — so the two are checked against each other here.
  const game = fs.readFileSync(new URL('../journey/index.html', import.meta.url).pathname, 'utf8');
  const m = /function monthKey\(\)\s*\{([\s\S]*?)\n    \}/.exec(game);
  ok(m, 'the game has no monthKey() — the board would be filed under nothing');
  const gameKey = new Function('return function monthKey() {' + m[1] + '}')();
  eq(gameKey(), KEY, 'the game and the board disagree about what month it is');
});

test('a month nobody played reads as zero, not as a missing row', () => {
  eq(B.jbStats(row('a', 9, 10, 3, {}), 'month', KEY), { correct: 0, answered: 0 });
});

test('the all-time board reads the running totals, not one month', () => {
  const r = row('a', 5, 6, 2, { '2020-01': { c: 5, a: 6 } });
  eq(B.jbStats(r, 'all', KEY), { correct: 5, answered: 6 });
  eq(B.jbStats(r, 'month', KEY), { correct: 0, answered: 0 });
});

section('\nTHE RANKING');

test('the board is ordered by questions right', () => {
  const ranked = B.jbRank([row('low', 10, 40), row('high', 30, 30), row('mid', 20, 25)], 'month', KEY);
  eq(ranked.map(e => e.row.uid), ['high', 'mid', 'low']);
});

test('MORE RIGHT WINS, even at lower accuracy', () => {
  const ranked = B.jbRank([row('careful', 40, 40), row('busy', 60, 200)], 'month', KEY);
  eq(ranked[0].row.uid, 'busy', 'the board stopped ranking on the number answered right');
});

test('a student who has answered nothing is not on the board', () => {
  eq(B.jbRank([row('none', 0, 0)], 'month', KEY).length, 0, 'an empty row took a place on a board with a prize');
});

test('a tie on the count breaks on ACCURACY, then chapter', () => {
  const a = B.jbRank([row('loose', 16, 32), row('tight', 16, 20)], 'month', KEY);
  eq(a[0].row.uid, 'tight', 'level on answers, the more accurate one goes first');
  const b = B.jbRank([row('shallow', 16, 20, 2), row('deep', 16, 20, 40)], 'month', KEY);
  eq(b[0].row.uid, 'deep', 'level on both, the further run goes first');
  eq(b.length, 2, 'a tie dropped a row');
});

test('THE CHAPTER DECIDES NOTHING', () => {
  const ranked = B.jbRank([row('deep', 5, 20, 99), row('accurate', 20, 20, 1)], 'month', KEY);
  eq(ranked[0].row.uid, 'accurate', 'the board was won by replaying chapters instead of answering');
});

test('every row carries the numbers the board prints beside it', () => {
  const e = B.jbRank([row('a', 9, 12, 4)], 'month', KEY)[0];
  eq(e.correct, 9); eq(e.answered, 12); eq(e.chapter, 4);
  eq(Math.round(e.acc * 100), 75);
  eq(e.score, e.correct, 'the ranking number is not the count printed on the row');
});

section('\nTHE PRIZE — who the voucher actually pays');

test('the top three win it', () => {
  const ranked = B.jbRank(['a', 'b', 'c', 'd', 'e'].map((u, i) => row(u, 50 - i * 5, 50)), 'month', KEY);
  const winners = B.jbPrizeWinners(ranked);
  eq(winners.length, 3);
  eq(winners.map(w => w.row.uid), ['a', 'b', 'c']);
});

test('the prize is a $10 voucher for the top 3', () => {
  eq(B.JB_PRIZE_TOP, 3);
  ok(/\$10/.test(B.JB_PRIZE_TEXT), 'the prize text no longer says $10: ' + B.JB_PRIZE_TEXT);
});

test('a tiny perfect run is on the board and is NOT payable', () => {
  // 9 right leads a board where nobody else has more, and is still not
  // payable: a voucher decided on nine questions is decided on luck.
  const ranked = B.jbRank([row('lucky', 9, 9), row('quiet', 8, 8)], 'month', KEY);
  eq(ranked[0].row.uid, 'lucky');
  eq(B.jbPrizeWinners(ranked).map(w => w.row.uid), [],
     'ranking and PAYING are different questions, and only one of them has money on it');
});

test('a row that ranks above the winners is not silently dropped from the board', () => {
  const ranked = B.jbRank([row('lucky', 9, 9), row('worker', 30, 60)], 'month', KEY);
  eq(ranked.length, 2, 'an ineligible row must still be SHOWN — it is a real student');
});

test('the eligibility floor is a real amount of work and is stated', () => {
  ok(B.JB_MIN_QUESTIONS >= 5, 'the floor is only ' + B.JB_MIN_QUESTIONS + ' questions');
  ok(B.JB_MIN_QUESTIONS <= 50, 'a floor nobody reaches pays nobody');
});

test('fewer than three eligible pays fewer than three, never a filler', () => {
  const ranked = B.jbRank([row('one', 20, 20), row('tiny', 2, 2)], 'month', KEY);
  eq(B.jbPrizeWinners(ranked).map(w => w.row.uid), ['one']);
});

test('the winners are a PREFIX of the board — never out of order', () => {
  const ranked = B.jbRank(['a', 'b', 'c', 'd'].map((u, i) => row(u, 40 - i, 40)), 'month', KEY);
  const winners = B.jbPrizeWinners(ranked).map(w => w.row.uid);
  eq(winners, ranked.slice(0, winners.length).map(e => e.row.uid),
     'a badge on a row the board does not put at the top reads as a mistake');
});

section('\nTHE PAGE — what the board actually prints');

// `jbPaint` is where the ranking becomes the thing a student and a teacher
// LOOK at, so it is rendered here against a DOM stub. The portal's own app.js
// cannot be loaded in a harness (it imports Firebase at the top), so the paint
// is cut out and given only what it reaches for.
const paintBlock = cut('function jbPaint()', '\n// =====', 'paint');
function paint(rows, tab, meUid) {
  let html = '';
  const env = new Function('rows', 'tab', 'meUid', 'sink', `
    ${block}
    const escapeHtml = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const currentUser = meUid ? { uid: meUid } : null;
    const document = { getElementById: id => id === 'jbContainer' ? { set innerHTML(v) { sink(v); } } : null };
    _jbRows = rows; _jbTab = tab;
    ${paintBlock}
    jbPaint();
  `);
  env(rows, tab, meUid, v => { html = v; });
  return html;
}

const BOARD = [
  row('u1', 48, 52, 41), row('u2', 44, 50, 63), row('u3', 30, 34, 22),
  row('u4', 61, 140, 88), row('u5', 4, 4, 5)
];

test('the prize line says WHO wins and WHAT, in words a student can check', () => {
  const html = paint(BOARD, 'month', 'u3');
  ok(/\$10/.test(html), 'the board never names the prize');
  ok(/Top 3/i.test(html), 'the board never says how many win it');
  ok(/number of questions answered right/i.test(html),
     'the board never says what it ranks on — a ranking nobody can check is one nobody trusts');
});

test('a voucher badge goes on the top three and on nobody else', () => {
  const html = paint(BOARD, 'month', 'u3');
  const badges = (html.match(/jb-badge/g) || []).length;
  eq(badges, 3, 'the voucher was offered to ' + badges + ' students');
  const winners = (html.match(/class="jb-win[^"]*"/g) || []).length;
  eq(winners, 3);
});

test('an ineligible row is still SHOWN — it is a real student', () => {
  const html = paint(BOARD, 'month', 'u3');
  ok(html.includes('u5'), 'a student who played was left off the board entirely');
});

test('the signed-in student is marked, and told where they are', () => {
  const html = paint(BOARD, 'month', 'u3');
  ok(/jb-me/.test(html), 'a board of thirty names with your own not marked is unreadable');
  ok(/You are <b>#\d+<\/b>/.test(html), 'the board never says where you are');
});

test('a student not on the board is told how to get on it', () => {
  const html = paint(BOARD, 'month', 'nobody');
  ok(/not on this board yet/i.test(html), 'a blank where your row should be explains nothing');
});

test('an empty board explains itself instead of printing a bare table', () => {
  const html = paint([], 'month', 'u3');
  ok(/Nobody on the board yet/i.test(html));
  ok(/journey\/index\.html/.test(html), 'and it points at the game');
});

test('the all-time tab drops the prize claim', () => {
  const html = paint(BOARD, 'all', 'u3');
  ok(!/jb-badge/.test(html), 'a voucher badge on the all-time board pays the wrong month');
  ok(/monthly board/i.test(html), 'and it says where the prize is actually paid');
});

test('a name is ESCAPED — it is a student-supplied display name', () => {
  const html = paint([row('<img src=x onerror=alert(1)>', 20, 20)], 'month', 'x');
  ok(!/<img src=x/.test(html), 'a display name reached the page as markup');
  ok(/&lt;img/.test(html));
});

for (const run of queue) await run();

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
