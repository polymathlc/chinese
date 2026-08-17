# CLAUDE.md

Guidance for Claude when working in this repo.

## The app

`index.html` + `app.js` — the **"Chinese Learning Portal"** (the product name in
the sidebar, the `<title>` and the footer). Admin question authoring (block
editor, AI build-from-screenshot, image crop/touch-up, vetting → bank) plus
student practice, worksheets and marking.

**The markup and CSS live in `index.html`; ALL of the application JavaScript
lives in `app.js`**, loaded as `<script type="module" src="app.js">`. They ship
together — `index.html` is useless without `app.js` next to it, so deploy the
directory, never the single file.

This is a fork of the **English portal** (`polymathlc/english`), which is itself
a fork of the Science portal (`polymathlc/cer`) with the game layer removed. See
**The fork** at the bottom for what that means in practice.

There is a **third file**: `pinyin-dict.json`, the input method's dictionary. It
is fetched on first use rather than bundled — see **拼音 input** below. Deploy it
beside the other two.

- Functions referenced from inline `onclick`/`on*` handlers MUST be assigned to
  `window` near the bottom of `app.js` (search `window.navigateTo =`), because
  the module has its own scope.
- `const` declared mid-module is in its temporal dead zone earlier in the file —
  only read such values at call time, not at module-eval time.

## Where the data lives — read this before touching any Firestore path

This app shares a Firebase PROJECT with its two siblings and shares **no data**
with either. Every collection is named once, at the top of `app.js`, and every
path is built from those constants (`QUESTIONS_COL`, `SETTINGS_COL`,
`PROFILES_COL`, `PROGRESS_COL`, …). Nothing else in the file spells a collection
name out — keep it that way.

This app has **two** siblings in that project — the Science portal and the
English portal (`polymathlc/english`) it was forked from — so every name it uses
ends in `Zh` or starts with `zh`.

**That rule is not style, and the English app's v1.3.0 is what it costs to break
it.** Four functions are the only door to the bank — `_qRef` / `_vRef` / `_qCol`
/ `_vCol` — and over there they spelled `'questions'` and `'vetting'` inline: the
Science app's own names, under the same `users/{uid}` tree, in the same project.
So for three versions those two apps were *one bank wearing two front ends*.
Every English question saved landed in the Science bank and every Science
question came back out of it. Nothing threw. Nothing looked broken. The only
symptom was Science questions listed on the English bank page, which reads as a
filter bug. Three things follow:

- **A shared-name path fails LOUDLY nowhere and quietly everywhere.** The
  fail-closed warning below is about names the rules *don't* know; this is the
  opposite and worse — a name the rules know for the *other app*, which works
  perfectly and silently merges two data sets.
- **`mistakes`, `flashcards` and `scheduledQuestions` had the same bug** and are
  `mistakesZh` / `flashcardsZh` / `scheduledQuestionsZh` here. Anything tempted
  to call them "shared with no one" is wrong twice over: both siblings write
  exactly those three names under the same user. `scheduledQuestions` is the
  dangerous one — a question ANOTHER app had queued would be released into
  **this** bank on its release date, linking two subjects a day after somebody
  checked they were separate.
- **There is deliberately NO bank-rescue tool here.** The English portal carries
  a one-time 📦 From Science bank (`_lb*`) because it really did write into the
  Science bank for three versions. This app was forked after that fix and has
  never written outside its own collections, so there is nothing to rescue — and
  the tool is not inert if ported: it scans another app's collections and offers
  to MOVE what it finds into this one, deciding subject against a list of
  ENGLISH topics that shares no entry with a Chinese one. Every question it
  could find belongs to another subject, and every verdict it offered would be
  wrong. `tools/bank-rescue-tests.mjs` went with it.

- **`users/{uid}` — the bare document — is the ONE thing all three portals
  really do share.** One project, one sign-in, one uid, so it is the same
  document in every subject. Nothing here may read or write it. Two things had
  to move for that to be true, and both had already been shipped:
  - **The legacy single-doc migration is gone.** Both siblings carry one: the
    Science app once kept its whole bank as `questionBank` / `vettingList`
    ARRAYS on that document, and the code that migrates them into subcollections
    came across with the fork. Here it is a door into this app's bank from the
    outside — on the teacher's first sign-in it would read a legacy array
    belonging to SCIENCE, write every question in it into `questionsZh` through
    `_qRef`, then blank the arrays so nothing was left to show where they came
    from or to give back. This app has never had a single-doc format, so any
    such array under that uid belongs to another subject. Do not port it back.
  - **The student roster lives at `{SETTINGS_COL}/students`**, not on the shared
    document. Both siblings write `students` and `studentSetupSeen` straight
    onto it, so on the shared document the teacher's Chinese roster and their
    English roster are one array and the last app to save wins.

**A name the Firestore rules do not know about fails closed**: reads come back
empty, writes are denied, and nothing on screen explains why. So a new
collection means a matching block in `firestore.rules`, deployed alongside the
other two apps' rules — never replacing them. `README.md` has the deploy steps.

**`node tools/bank-isolation-tests.mjs` is what holds all of this in place.** It
reads app.js as text and checks the SHAPE of every Firestore path: that each
collection comes from a constant and never a literal, that every constant is
`Zh`-marked, that no sibling's name is used as a collection, that the four bank
doors go through `QUESTIONS_COL` / `VETTING_COL`, that nothing addresses the
bare user document, that the migration has not come back, and that the rules
cover this app's collections and only those. Run it after touching any path.

The bank starts EMPTY, deliberately: `users/{uid}/questionsZh` does not exist
until the first Chinese question is written.

## The subject switcher — four apps, one student (v2.6.0)

`SUBJECT_APPS` / `subject*` (in `app.js`, search `THE SUBJECT SWITCHER`), plus
`#subjectSwitch` and the `.subject-*` CSS in `index.html`. A pill in the
**top-right of every page** naming the subject you are in; click it and the
other three are one tap away.

Polymath teaches four subjects through four separate apps, and they share a
Firebase project and a sign-in and **nothing else** — four banks, four sets of
progress, four topic lists. A student taught three of them had one bookmark per
subject on a school Chromebook, and the subject they never bookmarked is the
one they stopped using.

- **It is a LINK, not a router.** Four `<a href>`s and no JS navigation: each
  app stays reachable at its own URL exactly as before, nothing here redirects
  or gates anything, and middle-click / open-in-new-tab behave the way a
  student expects — which a `location.href =` handler would quietly break.
- **The URLs are RELATIVE (`../cer/`), and that is load-bearing.** The four are
  GitHub Pages project sites — `polymathlc.github.io/{math,english,chinese,cer}`
  — so they are sibling folders on one host, and a relative hop resolves there,
  on a local checkout with the four repos side by side, and on a custom domain
  later, without this file ever naming a host. An absolute
  `https://polymathlc.github.io/…` works perfectly until the centre moves to a
  domain of its own and then sends every student back to the old one.
- **Science lives at `../cer/`** — the repo name, not the subject name. The
  label and the folder differ on purpose; `../science/` is a 404 for the whole
  school at once and reads as a link somebody forgot to finish.
- **`SUBJECT_KEY` says which of the four THIS app is**, and it is the ONE line
  that differs between the repos — everything else in the block is identical in
  all four, so a fix copies straight across. `subjectCurrent()` falls back to
  the first entry, so a `SUBJECT_KEY` naming nothing does not throw: it labels
  this app "Math" and offers a link back to the app you are already in.
- **The menu is built from `SUBJECT_APPS`**, never written out in `index.html`,
  so a subject added to that list appears by editing one line per app.
- **The current subject is shown and marked, never dropped.** A menu that
  silently omits where you already are leaves a student unable to tell which
  app they are looking at. It is a `<div>` rather than an `<a>` — a link back to
  the page you are on reloads the app and loses whatever was half-typed.
- **It is turned on from `configureSidebarForRole`**, the one function every
  signed-in path (admin, employee, student) already goes through, rather than
  from three call sites that could drift. It is hidden until then, or it floats
  over the login card belonging to nobody.
- **`z-index: 150` sits in a deliberate gap**: above the sidebar (100) and every
  sticky `.page-header` (50) so it is always reachable, and below every modal
  (`.confirm-overlay` and friends start at 200) so a dialog covers it rather
  than being covered by it.
- **`.page-header` gives up its right-hand corner** (`padding-right`), because
  that is where every page keeps its action buttons and the switcher floats
  over them. It is fixed to the viewport rather than dropped into a header
  because this app has no global top bar at all — forty-odd pages carry their
  own `.page-header`, and a page added next month would be the one that quietly
  had no switcher on it.
- The CSS is written against the design tokens and nothing else, so the **same
  block is used in all four apps** and each paints it in its own palette. A
  themed copy per app is a copy that drifts.
- Run **`node tools/subject-level-tests.mjs`** after touching any of it.

## Keep the page fast — these are load-bearing, do not undo them

- Fonts are ONE non-blocking request (`media="print" onload="this.media='all'"`).
  Adding another render-blocking `<link rel="stylesheet">` to Google Fonts puts
  first paint back at the mercy of the school's network. Crimson Pro is
  deliberately `media="print"` — it is only used by the printed worksheet cover.
- There is NO icon font. The landing-page icons are inline SVG inside
  `.material-symbols-outlined` spans. Do not reintroduce Material Symbols: the
  variable webfont is 1.1 MB.
- Tailwind is PREBUILT and inlined (search `Tailwind, prebuilt`). Do not put the
  `cdn.tailwindcss.com` Play CDN back — it ships a CSS compiler to the student's
  phone. Regenerate via `docs/tailwind/` instead.
- `<link rel="modulepreload" href="app.js">` in the head is what starts the app
  download early. Keep it, and keep it pointing at the right filename.

## 拼音 input — a Chinese keyboard on an English keyboard

`zhime*` (in `app.js`, search `拼音 INPUT METHOD`). Type pinyin, pick the
character: `xuexi` → 学习. The centre's machines and the students' Chromebooks
have no system IME and cannot have one installed, so without this an author
composes questions somewhere else and pastes them in, and a student cannot
answer a written question at all.

- **ONE listener, on the document, in CAPTURE** — never a binding per field.
  This app builds its DOM continuously, so anything bound per element covers the
  fields that existed when it ran and silently misses every one made afterwards.
  Capture also puts it ahead of the editor's own keydown handlers, which would
  otherwise act on the raw latin letters being composed from.
- **It BUFFERS the keystrokes** rather than letting them land and replacing them
  afterwards. Every field in the block editor saves from its `oninput`, so
  writing latin in and fixing it later leaves half-typed pinyin in the database
  whenever the commit does not happen.
- **It commits through `execCommand('insertText')`** — deprecated, and still the
  only insertion that works in an `<input>`, a `<textarea>` and a
  contenteditable alike, keeps the browser's undo stack, and **fires a real
  `input` event**. The manual fallback dispatches `input` by hand; without it a
  question types perfectly on screen and stores nothing.
- **It is OFF by default** (Ctrl+Space, or the pill) and it has to be: the
  汉语拼音 questions in 语文应用 have pinyin as their OPTIONS — "píng mù",
  "chèn shān" — so a keyboard that could not be turned off would make exactly
  those questions unauthorable. The choice is stored per user.
- **`pinyin-dict.json` is fetched on FIRST USE**, not bundled into `app.js`. It
  is ~720 KB of data for something not needed until a caret is in a field, and
  the loading rules above exist to keep first paint off the school's network.
  It is built by a script from three public datasets (mozillazg/pinyin-data,
  mozillazg/phrase-pinyin-data, fxsjy/jieba); the frequency ordering is what
  makes 的 beat 得 for "de". **jieba's counts come from a NEWS corpus**, which
  rates 病句 at 5 and 近义词 at 6 — below any sane cut — so the vocabulary of
  this subject is seeded explicitly and ranked above the corpus. A word missing
  from the dictionary is a word a teacher simply cannot type.
- **The word list has a SECOND job**: `zhSegment` is the segmenter behind
  `_fbTokenSpans`. Chinese is written without spaces, so the fill-in-the-blank
  and cloze chip rows — which split on `\S+` — saw a whole passage as ONE chip
  that blanked the entire paragraph. It falls back to one chip per character
  until the dictionary arrives, which is why nothing waits on the fetch.
- **`FB_EDGE`, not `\W`, is the punctuation a blank leaves outside itself.**
  Every Chinese character IS `\W`, so the greedy trim ate the whole word and
  课外 blanked to `课外[[]]` — an empty blank, in a passage that still reads
  perfectly in the textarea.
- **`fbToggleToken` splices by OFFSET**, never `toks.join(' ')`. The join threw
  away every newline, and for a 短文填空 the passage *is* the question.
- Run **`node tools/pinyin-ime-tests.mjs`** after touching any of it.

## Every prompt speaks Simplified Chinese

`ZH_PROMPT_RULES` (in `app.js`, just above `askGemini`) is prepended to every
prompt inside the **three** functions that are the only doors to a model:
`askGemini`, `askGeminiVision` and `_widgetAskAI`. Do not add a fourth door, and
do not restate the rules inside a prompt.

Sixty-odd prompts describe their task in English on purpose — they are read and
diffed in English. What they must not each carry is their own copy of the
language rule, because the one that gets missed does not fail: it comes back
fluent, confident and in the wrong language, and every surface downstream
renders it perfectly. Five things it protects, each a silently wrong answer:
**Traditional characters** (學 for 学 looks right to anyone who cannot tell);
**translation on the way in** (a vision call told to "read the question" returns
a fluent English translation of a Chinese paper); **pinyin turned into
characters** (in 语文应用 the pinyin IS the question, and rendering "píng mù" as
屏幕 deletes it while leaving four plausible options); **half-width
punctuation**; and **JSON keys**, which every caller parses by.

It is PREPENDED, never appended — many prompts end with the material they work
on (`"Text:\n" + text`), and a rule bolted on after that reads as more material.

## 画线词语 — the underlined word (v2.1.0)

The paper underlines the word a question is about, and in 汉语拼音 that
underline **is** the question:

> 弟弟不小心把果汁洒在自己的<u>衬衫</u>上，哭着喊妈妈帮他换。
> （1）cēn sān （2）cèn sān （3）chēn shān （4）chèn shān

Transcribe that sentence flat and the question still reads perfectly, still
prints perfectly, and no longer says which of a dozen words the four spellings
belong to. Every option becomes a plausible answer to a question nobody can
answer — and nothing on any screen looks wrong. It is the same class of failure
as pinyin rendered into characters, which is why the rule sits beside that one.

- **The model is told once, in `_partsPromptRules()`** — the ONE fragment all
  five build prompts carry — so 🤖 Build from screenshot, ⚡ Rapid add, 📄 Exam
  Paper, the bulk PDF import and 🔁 Regenerate copy gained it together. It says
  in as many words that `<u>…</u>` **survives the "plain text only, no markdown"
  line** four of those prompts end with; without that the model resolves the
  contradiction by dropping the tag, which is the bug arriving through its
  own fix.
- **`_aiUnderline` is the ONE place an underline becomes markup**, called from
  `buildBlocksFromAi`'s text branch — the function every AI authoring path goes
  through. Three forms arrive and leave as one: `<u>…</u>`, the `__word__` a
  model reaching for markdown writes (the same marker a pasted passage carries
  into `_pbPassageHtml`), and the `&lt;u&gt;` a model escapes on the way through
  JSON. An **unbalanced tag is dropped**, never repaired: an opener with no
  closer underlines the rest of the question, which reads as a broken app.
- **`escapeHtmlKeepLines` keeps `<u>` and nothing else.** That function is what
  BOTH print builders send a text block through, and it stripped every tag — so
  the underline showed on screen and vanished on paper, the one surface nobody
  checks until the class is sitting in front of it. The tag crosses the escape
  on two control characters, which are stripped from the input first so nothing
  an author typed can pose as the marker.
- The editor's **U button** writes the same `<u>`, and the text block stores
  `innerHTML`, so an author can add or remove one by hand and it round-trips.
- Run **`node tools/underline-tests.mjs`** after touching any of it.

## Learner progress

`progress` (in `app.js`, search `LEARNER PROGRESS`) is the plain record of work
done: questions marked, how many were right, the fractional marks total and the
day streak. My Report, the student Home screen, the teacher's Usage dashboard
and Ai-nstein all read it. It replaced the RPG hero doc the Science app used.

- **`progressOnMarked(q, score, total, opts)` is the ONE hook** every marking
  path calls, through `recordCerPerformance`. Do not add a second.
- Stored at `users/{uid}/{SETTINGS_COL}/progress`, mirrored to `PROGRESS_COL`
  so a teacher — who cannot read another account's settings tree — can see the
  class. That mirror carries **counts only**: never answers, never the mark on a
  particular question.
- **`correct` is a valid lower bound on `creditSum`.** Every question in the
  binary count scored ≥ 0.95, so an honestly accumulated `creditSum` can never
  sit below `0.95 × correct`; `progressHydrate` seeds it from the binary count
  when it is lower, and `progressPublish` takes the higher of the two. Without
  that, a counter added later reads every earlier question as WRONG for the rest
  of the account's life. Any future counter added beside an older one needs the
  same treatment.
- Writes coalesce (600 ms) and the class mirror publishes at 1500 ms — a photo
  answer marks every part at once and would otherwise be one write per part.

## Learning gaps and the daily retry credits

`lgState` (in `app.js`, search `LEARNING GAPS`) is the list of what one student
does not understand yet — **named** weaknesses ("past perfect tense", "the word
'reluctant'"), not topics. The mistake log records what went wrong on a
particular question; this is the same evidence read as a list that outlives the
question. Stored at `users/{uid}/{SETTINGS_COL}/{GAPS_DOC}`, and **not mirrored
to the class collection**: a list of what a child cannot do is not a class
statistic.

- **`lgNoteFromParts` is the ONE hook**, and it is called from inside
  `fcNoteMistakes` — the function every marking path already funnels its wrong
  answers through. Do not add a second; a surface added later is covered free.
- The list does three jobs and it is the **same list** for all three: it is shown
  to the student, it **picks** the bank questions they are served
  (`lgBankQuestionsFor`), and it **briefs the AI** when the bank has nothing left
  (`lgBuildQuestion`, which goes through `buildBlocksFromAi` like every other AI
  authoring path). A generated question is **never saved** — the bank is the
  teacher's, and nothing unvetted belongs in it.
- **The AI names the gap; the question's own tags are the fallback.** With the AI
  off or the call failed, `_lgFallbackItems` files the mistake under the
  question's tags or topic. The list must never simply stop filling. But an
  **empty `items` array is a real answer** — the model is told to return one when
  a slip shows no misunderstanding — so it is not overridden by the fallback.
- **A gap is closed by the student, not the clock**: `LG_CLEAR_WINS` right in a
  row (`lgNoteWin`, called from `recordCerPerformance` at the same ≥0.95
  threshold `progressOnMarked` uses). One wrong answer **re-opens** it.
- **Credits are `REGEN_DAILY_CREDITS` (30) a day, reset by calendar day**, spent
  BEFORE the AI call so two quick taps cannot buy two questions for one credit,
  and **refunded when the call fails**. `_lgRollCredits` must run on load or a
  stale `dayKey` hands out one allowance and never another.
- `_lgHostId` is the ONE place a gap key becomes an element id, and it is
  injective on purpose — a bare strip of non-alphanumerics lets two gaps share a
  host, and the second one's button then does nothing at all.
- Run **`node tools/learning-gap-tests.mjs`** after touching any of it: a
  mis-keyed gap, a credit that misses the rollover and a gap that cannot re-open
  are all silent.

Topic lists carry **no P3–P6 headings** — not the bank filter, the authoring
`<select>`, the manage dialog or the student topic grid. A Chinese topic is not
owned by a year the way a Science one is. The level each topic is filed under is
still live (it gates what a student may be served); it is simply not announced.

**The topics are the sections of a 华文 paper**, bilingual and Chinese-first
(`'汉语拼音 Hanyu Pinyin'`, `'短文填空 Cloze Passage'`): the questions and the
students are Chinese, the authoring UI around the dropdown is English, and a
teacher filing a question should not have to translate a section heading in
their head to find it. Four structures must agree, or the failure is silent —
`topicLevelMap`, `topicsByLevel`, `topicEmojis` and `SYLLABUS_LO_TOPICS`. A topic
missing from `topicEmojis` draws a blank badge on the student grid; one whose
level disagrees between the first two is served to the wrong years. The fork
left the SCIENCE emoji map behind, so every topic drew a blank badge in the
English app too.

## The two comprehension formats — one passage, many questions

Both arrived in v1.6.0 and both exist because the block editor could not express
a **passage with its own sub-questions as ONE bank question**.

### Sub-questions are LETTERED — (a) (b) (c) — whatever the paper called them

**Every automatic path letters them** (v1.8.0): the passage builder, and the AI
read of a screenshot set. The paper's 16, 17, 18 / 21, 22, 23 are *that exam
paper's* numbering, not this question's — a bank question stands on its own, and
one that opens at part (21) reads as though twenty parts are missing.

- **The markers INSIDE the passage are renumbered to match**
  (`_pbRelabelPassage`). The paper prints "(16)" against the underlined word
  question 16 asks about; letter the questions and leave the passage alone and
  the student reads "(16)" over the word, then hunts for a question 16 that is
  now part (a). Only the **parenthesised whole number** is rewritten, so "(160)"
  and the 16 in "16 January" survive. The AI prompt asks for the same rewrite on
  any passage text it transcribes.
- **Past the alphabet a sub-question is DROPPED and the author is told**
  (`pbPartOverflow`). It is never given an empty part: `qPartMap` inherits
  forward, so an unlabelled sub-question is filed under the previous one and two
  option lists share a heading.
- `pbPartLetter(i)` is the one place an index becomes a letter.

### Parts may still be NUMBERS

`qPartNormalize` accepts **1–999** as well as a letter. Nothing automatic
produces one any more — the parts bar's **Number from** box is the deliberate
manual escape hatch, for an author who does want the paper's numbering.

- **Detection is deliberately NOT extended.** `qPartDetect` still matches
  letters only — a number at the start of a line is a question number, a
  quantity or a year far more often than it is a part. Assigning is a decision;
  detecting is a guess, which is why `QPART_ASSIGN` was already longer than
  `QPART_LETTERS`.
- The letter branch now requires **length 1**: `indexOf` on a *string* matches
  substrings, so `'ab'` used to come back as a valid part — one no picker could
  show and no key could label.
- `autoNumberParts(startAt)` takes an optional start; the parts bar's **Number
  from** box feeds it, and blank falls back to the letters.
- **`QPART_OPENER_TYPES` is `['text', 'mcq']`.** An MCQ joins because these
  papers have no text block to hang the part on — the sub-question is nothing
  but its four options. Both print paths and `buildOpenBody` print the label for
  an MCQ that opens a part, which is what makes that safe (the original
  text-only rule existed so a part could never be labelled on the key with
  nothing marking it on the paper).

### 📑 The passage builder (`pb*`)

Paste the passage and the questions as they are on the paper; out comes one text
block for the passage plus, per sub-question, its wording and its MCQ — each
sub-question opening its own lettered part. Both shapes a 华文 paper sets are
read: a question that is nothing but a number and its four choices, and a
阅读理解 question that carries its own wording.

- **The parse is deterministic — there is no AI in it.** A wrong guess here is
  not a wrong answer, it is four options quietly filed under the wrong number.
- A question opens on a **bare** number at the start of a line; an option number
  is **parenthesised and single-digit**. That one rule is what stops the "(16)"
  markers inside the passage reading as options, and stops "20,000 animals
  across 1,000 species" reading as question 20. **`_pbQStart` refuses anything
  `PB_OPT_RE` matches**, and the parse tests options FIRST — otherwise
  "（1）作者的父亲赚的钱不多。" opens question 1 with the option as its wording,
  and every option list becomes four questions.
- **阅读理解 questions carry their own WORDING** (v2.3.0) — "Q21 为什么作者的
  父亲没时间管他？" — and the number **announces itself**: `Q21`, `第21题`,
  `21.`, `21、`, `（21）`. That announcement is what lets the wording form exist
  at all; a bare number followed by text stays prose, or the quantity rule above
  is undone. A `Q` needs no other proof and splits the passage on its own,
  because a 阅读理解 question's wording often wraps before its options begin.
- **Everything is half- OR full-width.** A 华文 paper prints `（1）`, not `(1)`,
  and `ZH_PROMPT_RULES` asks every model to keep the paper's punctuation exactly
  as printed — so an ASCII-only parser reads a whole 阅读理解 as one long
  passage with no questions in it, and the builder says "Nothing to add yet",
  which reads as a paste that failed. `_pbNum` is the one place a full-width
  digit becomes a number.
- A line that is neither **continues what came last** — an option long enough to
  wrap, or the question's own wording, which runs to two lines often enough that
  dropping the tail would lose half the question with nothing looking wrong.
- **The WORDING opens the part and the options inherit it.** `pbBuildBlocks`
  gives the MCQ a part only when there is no wording block above it: a part
  opened twice files the wording under (a) and the options under (a) again, and
  the key prints two (a) rows. `qPartLabelFirst` is what stops the paper reading
  "(a) 为什么… (a) （1）作者的父亲…".
- **An unticked sub-question is saved with no correct option.** Guessing one
  marks every class that ever sits it against the wrong word.

### Reading a passage set off SCREENSHOTS (v1.7.0)

The multi-screenshot build and the `box_2d` auto-crop both already existed —
`aiBuildFromScreenshot` reads N images as ONE question and
`_autoFillDiagramsFromBoxes` crops each AI-drawn rectangle out of its own page.
The one thing missing was a way for the model to say **"these four options are
question 21 of the passage"**, so a comprehension page came back as eight
option lists in a row with nothing telling them apart.

- **`buildBlocksFromAi` honours an explicit `"part"`** on any AI block, through
  `qPartNormalize` — so `"b"` and `"21"` both work, though the prompt now asks
  for letters — with `QPART_NONE` preserved. It is stamped on the FIRST block that entry produced, because
  `qPartMap` inherits forward. This is the ONE function every AI authoring path
  goes through, so all of them gained it at once.
- **`qLiftPartMarkers` already skipped a block that opens a part**, which is
  what stops the typed-marker pass overwriting the model's numbering.
- **The rules live in `_partsPromptRules()`**, the fragment all four build
  prompts carry — do not restate them in a prompt. They tell the model to
  LETTER the sub-questions in order and to rewrite any "(16)" marker in the
  passage text to the matching letter.
- **`qPartLabelFirst(blocks, block)` decides who prints the label.** A numbered
  question is usually a text block (the wording) and an MCQ (the options) both
  filed under (21); labelled twice the paper reads "(21) What does… (21) (1)
  humans", which looks like a printing fault. `buildOpenBody` and both print
  builders ask the same function, so screen and paper cannot disagree.
- **The token budget scales with the pages** (`4096 + 3000 × extra`, capped at
  16384). Running out does not fail — it TRUNCATES, and `_repairAIJson` then
  hands back a valid-looking question missing its last few sub-questions.
  `_aiJsonRepaired` is set when a reply had to be repaired, and the build warns
  the author instead of letting the tail go quietly.
- **A sub-question the model could not answer is built with NO tick.** It works
  the answers out from the passage rather than reading a marking scheme, so the
  completion toast says how many need checking. Never turn a missing
  `correctIndex` into a guess.
- Run **`node tools/ai-parts-tests.mjs`** after touching any of it.

### 🔤 The comprehension cloze (`cb*`, block type `clozebank`)

One passage, numbered blanks, and a bank of words lettered (A)–(Q) above it.
The student drags a word into a blank and it is struck off.

- It is **`fillblank`'s sibling, not a variant**. A fill-in-the-blank is marked
  on what the student *wrote*, so it goes to the AI for synonyms and spelling.
  Here the student picks from a closed list, so the mark is exact, instant and
  free — an AI pass could only turn a right answer wrong.
- **The answers ARE the bank**: `cbBank` derives the list from the blanks plus
  the author's distractors, so a bank missing one of its own answers cannot be
  authored. It renders perfectly, prints perfectly and is unanswerable.
- `[[word]]` is **the same markup `fillblank` uses**, parsed by the same
  `_fbParse`. `_fbChipsHtml` takes the toggle to call, because hardcoding
  `fbToggleToken` made every cloze chip a no-op that looked like a working one.
- **`CB_LETTERS` skips I and O** — a handwritten (I) is a 1 and a handwritten
  (O) is a 0. The paper says so in as many words, and `cbIntro` generates that
  sentence from the passage so it cannot drift from it.
- **Struck-off is a RENDER of the placements** (`_cbUsed`), never a second list;
  a flag kept beside them is one drag away from disagreeing with the passage.
  The tapped-and-waiting word lives on the element, not in a map keyed by block
  id — the same block can be on screen in two surfaces at once.
- A **used word is still draggable**, and dropping it MOVES it. Refusing the
  drag would make the only way to correct blank 26 a tap to release and a second
  drag to place.
- **The bank is read DOWN the columns**, as the paper sets it, and the cells are
  sized from the columns actually filled (`_cbCols`).
- Both print builders carry an **explicit `case 'clozebank'`** for exactly the
  reason `fillblank` does, one step worse: falling through to the student
  rendering prints a draggable word bank over a passage of drop targets.
- Run **`node tools/passage-cloze-tests.mjs`** after touching any of it.

### 📝 短文填空 — the inline-options cloze (`cm*`, block type `clozemcq`)

The second section of a 华文 paper: ONE passage with numbered blanks, and each
blank prints its **own** four choices in brackets right where the blank is.

> …教室里还有学生在下棋、画画等。 16 （1 总算　2 就算　3 不管　4 尽管）是体育、
> 艺术，还是团队活动，课外活动的种类非常丰富。

**It is not `clozebank` with different styling**, and that is why it is its own
type. `clozebank` has ONE bank shared by every blank, lettered (A)–(Q) above the
passage and struck off as used — choosing for blank 26 changes what is left for
blank 30, and that coupling *is* the question. Here the blanks are INDEPENDENT,
and the options are position-bearing: the paper numbers them (1)(2)(3)(4) and
the marking scheme answers "16 (3)", so the NUMBER is part of the answer.
Forcing one onto the other would mean a single bank of twenty options with
nothing saying which four belong to which blank.

- **The options live IN the passage**, in the same `[[ ]]` markup every other
  blank in this app uses: `[[总算|就算|*不管|尽管]]`. One syntax, and the options
  cannot drift from the blank they belong to because they are stored nowhere
  else.
- **The `*` is the answer, and an unticked blank is saved with NO answer.** It
  is never inferred from position — an exam paper's correct option is not
  usually (1) — and `cmUnanswered` is what tells the author. The same rule holds
  on the AI path: a missing `correctIndex` stays missing.
- **The author never types the `*`.** `cmSetCorrect` rewrites one blank in
  place; clicking the current answer again clears it, so an author who ticked
  the wrong option can get back to "not set" rather than being made to leave
  some answer behind.
- Marking is **exact, instant and free**, for `clozebank`'s reason: the student
  picks from a closed list, so an AI pass could only turn a right answer wrong.
- **Each blank registers its own ITEM**, exactly as `fillblank` and `clozebank`
  do, so the score, the mistake log, the learning-gap list and
  `_checkAllPartsMarked` all cover it without knowing what it is. Do NOT add a
  second marking path.
- **Both print builders carry an explicit `case 'clozemcq'`** — one step worse
  than `fillblank`'s reason: the read-only rendering paints the correct option
  green, so falling through to it prints a worksheet with every answer circled.
- **On SCREEN each blank is a DROP-DOWN** (`.cm-pick`, v2.3.0); on PAPER the
  four choices still print inline in their brackets, exactly as the paper sets
  them. They differ on purpose: five blanks × four choices is eighty characters
  of options threaded through the prose, and on a phone the sentence the student
  is supposed to be reading for meaning disappears into it. `cmPrintHtml` is
  untouched.
  - **`_cmOptionsHtml` is the ONE place a blank's list is built**, and every
    option keeps the PAPER's number — `（3）不管` — because the marking scheme
    answers "16 (3)" and a list of bare words leaves the student unable to check
    their work against a key.
  - **The empty choice is `value="-1"`, never `""`.** `Number('')` is 0, which
    is option (1): an unanswered blank would be marked against a word the
    student never picked.
  - **The choice is READ OFF the `<select>`** (`_cmPicked`), never kept in a map
    beside it — a parallel list of picks is one change away from disagreeing
    with the passage on screen.
  - **Marking DISABLES the selects.** A `<select>` ignores the `cm-locked`
    class, so without that the student can still change an answer after the
    passage has been scored.
  - `appearance:auto` on `.cm-pick` is **not optional** — Tailwind's preflight
    sets it to `none`, which takes the arrow off and leaves something that does
    not read as a control (the same trap as a bare checkbox).
  - The correct word is shown **at the blank it belongs to** (`.cm-ans`), not
    only in the list under the passage: five blanks down, a student reading
    "16 (3) 解决" at the bottom has to count blanks back up to find which one it
    was.
- Run **`node tools/clozemcq-tests.mjs`** after touching any of it.

### 🔗 词语搭配 — the word-collocation match (`wm*`, block type `wordmatch`) — v2.12.0

The third section of the paper: a boxed, NUMBERED table of words, then a run of
short items each with a bracket to write a number in.

    1 负责　2 照顾　3 了解 / 4 弟妹　5 指令　6 国旗
    Q7 （　）情况   Q8 （　）值日   Q9 发出（　）   Q10 挥动（　）

**It is neither of the two clozes**, and the differences are why it is its own
type. `clozebank` has one bank for one PASSAGE and strikes a word off once
used, because what is left over is part of the question; here the items are
independent one-line phrases with no passage, and the paper prints MORE words
than items — six for four — so two are meant to be left standing. `clozemcq`
gives each blank its own four options; here every item chooses from the SAME
table, which is what makes it a matching exercise. And in both of those the
student supplies a WORD, while this paper says in as many words 把代表它的号码
填写在括号里 — the answer is the NUMBER.

- **The answer lives IN the item, in the same `[[ ]]` markup every other blank
  in this app uses, and it marks WHERE THE BRACKET GOES as well as what belongs
  in it.** `[[了解]]情况` prints （　）情况 and `发出[[指令]]` prints 发出（　）.
  That is not decoration: the bracket comes before the word in half of these
  items and after it in the other half, and a format that could only put it at
  one end could not set the paper.
- **The NUMBER is derived from the word's position in the table and is never
  stored**, exactly as an MCQ's option label is. An answer stored as "3" points
  at a different word the moment the author fixes a typo in the table.
- **The table can never be missing one of its own answers.** `wmBank` appends
  any answer the author's table does not contain — the rule `cbBank` is built
  on, because such a question renders perfectly, prints perfectly and cannot be
  answered. It is also REPORTED (`wmProblems`), since on a paper it means the
  table was transcribed wrong.
- **An item with an empty `[[]]` is saved with NO answer and is never marked.**
  Never infer one; a guess marks every class that ever sits it against the
  wrong word. The AI arm obeys the same rule — a model that could not work an
  item out leaves `answer` out rather than naming the first word of the table.
- **A used word is NOT struck off the other items' lists**, unlike the word-bank
  cloze. Nothing on the paper forbids using a word twice, and removing it would
  both make a legitimate repeat unauthorable and hand the student an
  elimination the paper does not give them.
- **Each item registers its own ITEM**, exactly as the two clozes do, so the
  score, the mistake log, the learning-gap list and `_checkAllPartsMarked` all
  count a 词语搭配 without knowing what one is. Do NOT add a second marking path.
- Marking is **exact, instant and free** — the student picks from a closed list,
  so an AI pass could only turn a right answer wrong.
- **On SCREEN each bracket is a DROP-DOWN** carrying the paper's number as well
  as the word (`（3）了解`), for 短文填空's reasons: this is answered on a school
  phone, a typed number is a number that can be typed wrong, and the marking
  scheme answers "7（3）". The empty choice is **`value="-1"`, never `""`** —
  `Number('')` is 0, which is option (1), so an unanswered item would be marked
  against a word nobody picked. `appearance:auto` on `.wm-pick` is not optional
  (Tailwind's preflight strips the arrow off it).
- **The table is read ACROSS** — 1 2 3 on the first row, 4 5 6 on the second —
  as this paper sets it. The 🔤 cloze bank reads DOWN its columns, because that
  is how ITS paper sets that one; they are not the same table.
- **Both print builders carry an explicit `case 'wordmatch'`**, for `fillblank`'s
  reason and one step worse: the student rendering is a REVIEW rendering with
  every answer's number already in its bracket, so falling through to it prints
  the whole exercise filled in.
- The rule the model reads lives in **`_partsPromptRules()`** with the other
  section types, so ⚡ Rapid add, 🤖 Build from screenshot, the paper import,
  📄 Exam Paper and 🔁 Regenerate all read the section. It returns the table and
  the items as DATA (`before` / `after` / `answer`) rather than the `[[ ]]`
  markup inline, for `clozemcq`'s reason — and it is **never asked for the
  number**, because a model that miscounts the table would key every item to
  the wrong word while looking perfectly right.
- Run **`node tools/wordmatch-tests.mjs`** after touching any of it.

## How many questions is a page? (v2.1.0)

A 语文应用 page of **1, 2, 3, 4, 5** holds FIVE questions, not one question with
five parts. ⚡ Rapid add puts five rows in vetting.

**`_aiQuestionPayloads(parsed)` is the ONE place a build reply becomes the list
of questions it describes**, and every path that reads one asks it. Both shapes
work: the old single-question object, and the `questions` array the prompt now
asks for.

- **The rule is the shared stimulus, not the numbering.** Numbered questions
  that share nothing are SEPARATE; a 阅读理解 passage, poster or infographic
  followed by numbered questions is still ONE question with lettered parts,
  because those questions cannot be read without it, and a 短文填空 is ONE
  question however many blanks run through it. The prompt gives the model the
  test in one line: *if you deleted every other question on the page, would this
  one still make complete sense?*
- **The paper's number is only the signal.** It is never kept — no `part`, and
  not in any block's text. `_epStripNumbering` runs as a guard on a
  multi-question page. **Its regexes had to learn full-width numbering**:
  `ZH_PROMPT_RULES` asks for the paper's punctuation exactly as printed, so a
  华文 paper's questions arrive as `2、`, `２．` and `（2）`, and a stripper that
  knew only `44.` and `(44)` read every Chinese paper as unnumbered. A BARE
  leading number is still deliberately left alone in both widths, because
  refusing it is what stops "50毫升的水" losing its 50.
- **An entry INHERITS the title / topic / category / tags it does not repeat.**
  A model told to write them per entry writes them once at the top and stops,
  and a question landing in vetting untopiced is one an author must open by hand.
- **The block type is chosen PER question** — the prompt names `synthesis`,
  `mcq` and `clozemcq` — so two questions on one page can be different types.
- **An empty or unusable `questions` array falls back to the whole reply**, and
  a reply with no usable blocks at all returns `[]` — Rapid add turns that into
  a visible red card rather than a blank question.
- **Each question is saved as it is built**, not batched at the end: a failure on
  question 4 must not lose the three that already read perfectly. Each crops
  from its OWN entry's rectangles, or five questions share the first one's
  pictures.
- **The whole-screenshot B&W backup is single-question only.** On a page of five
  it would give every one of them the same whole-page picture, which is worse
  than no picture at all.
- 🤖 **Build from screenshot loads the FIRST and says so** — the editor holds one
  question, and silently building one of five with nothing on screen to say the
  other four existed is how they get lost. It hands **that entry**, never the
  whole reply, to `_autoFillDiagramsFromBoxes`: given the reply, a page that came
  back as a `questions` array has no `blocks` of its own and the pictures quietly
  stop being cropped.
- The rapid budget is **8192 tokens**, because running out does not fail — it
  TRUNCATES, and `_repairAIJson` hands back a valid-looking reply missing its
  last questions. `_aiJsonRepaired` is what warns the author instead.
- Run **`node tools/rapid-split-tests.mjs`** after touching any of it.

### ⚡ Rapid add on a PHONE (v2.5.0)

The pad was a paste target and nothing else, so on a phone it was **a box that
could not be filled**: no Ctrl/⌘+V, nothing on the clipboard to paste, nothing
to drag. The camera and the gallery are the way in there.

- **`(pointer: coarse)` is the whole gate**, in the CSS (`.rapid-desk` /
  `.rapid-touch`) and in `_rapidTouch()` for the JS half. On a mouse the pad is
  the box it always was — same wording, same paste, same drop — and a
  touchscreen laptop driven by a trackpad reports a FINE pointer, so it keeps
  the paste pad too.
- **Both routes end at `startRapidJob`**, the ONE queue entry point, so a photo
  is read, cropped and filed exactly as a pasted screenshot is. Do not give the
  phone its own pipeline.
- **The picker's `value` is cleared BEFORE the files are queued.** An `<input
  type=file>` still holding last time's file fires no `change` for the same
  photo picked twice, so the second tap does nothing at all — a button that
  looks like it works and does not.
- **An oversized photo is SHRUNK, not refused** (`_rapidPrepFile`,
  `RAPID_PHOTO_MAX_SIDE`). A 12 MP camera photo is several times the size guard,
  so the guard alone refused the phone route for being the phone route. It only
  touches an image over `RAPID_SHRINK_OVER` (4 MB) — a pasted screenshot never
  reaches that and comes through byte-for-byte — and it re-encodes as **JPEG,
  never PNG**, or a photograph comes out bigger than it went in.
- **The size check runs AFTER the shrink**, and a failure there files the same
  red card a failed read does (`_failRapidJob`, which `processRapidJob`'s own
  catch now calls too). A screenshot that vanished silently reads as one that
  worked.

### 📚 The level a BATCH is filed at (v2.6.0)

`rapidLevel` / `setRapidLevel` / `_rapidApplyLevel` / `_rapidLevelOptions`, and
the `#rapidLevelWrap` picker above the pad. An author working through a pile of
screenshots is nearly always working through ONE year's paper, and the AI was
choosing the topic — and therefore the level — one screenshot at a time with no
idea which paper it came from. Saying "these are all P5" once is both less work
and more accurate than correcting forty questions in vetting afterwards.

- **A LEVEL IS NOT A FIELD ON A QUESTION HERE**, and that is the whole design.
  It is read off the TOPIC (`getTopicLevel`), and every surface that cares — the
  bank filter, the student-level gate, the topic grid — reads it that way. So
  stamping `q.level` would write a field nothing in this app looks at, and the
  question would still be served at whatever level its topic belongs to.
  Choosing a level instead **narrows the topics the AI may pick from** to that
  level's, and the level follows from the topic exactly as it always has.
- **`_aiBuildQuestionPrompt` takes the level as a third argument** and blank —
  every other caller, including 🤖 Build from screenshot — leaves the prompt
  byte-for-byte what it was: the whole topic list, chosen from freely.
- **A level whose topics have all been removed falls back to the full list.**
  An empty "choose from EXACTLY this list" leaves the model nothing to choose
  from and it invents a topic instead.
- **`_rapidApplyLevel` is the guard for a reply that ignored the list**, and it
  is what makes the promise true. An off-level or unknown topic is snapped into
  the level and the question is marked **`topicConfidence: 'low'`** — an
  existing signal that already draws the "⚠ check topic" badge in vetting. The
  author asked for a level and gets it; the one thing that had to be guessed —
  WHICH topic within it — is flagged for the glance it deserves.
- **A SECONDARY topic counts too.** `qLevelNum` takes the MAX over both, so a
  `topic2` from a higher level puts the question above the level the author
  chose while the primary topic looks perfectly right.
- **The level is captured in `startRapidJob`, synchronously, as the file is
  queued** — never read inside the job. `_rapidPrepFile` re-encodes a phone
  photo, which takes real time, and the pad stays open the whole while: an
  author who queues a P3 paper and switches the picker for the next one must
  not have the first paper land at P4 because its prep finished second. It is
  carried on the job (and shown on its vetting card) and applied to **every**
  question the page held — a page of five is five questions at that level.
- **It lives in `sessionStorage`**, which is the honest lifetime: a batch is one
  sitting, so it survives a reload mid-pile and is back to "Any level" in a new
  tab or tomorrow. A level that persisted for a week would be the one an author
  set last Tuesday and never noticed again, filing a P3 paper as P5.
- **The options are generated from `TOPIC_LEVELS`**, never typed into
  `index.html`: a level added to the topics and missing from the picker is a
  level nobody can file at.
- The chosen level is **named back in the toast and the status line**. Filing at
  a level and never confirming it is how a whole pile ends up at the wrong one.
- Run **`node tools/subject-level-tests.mjs`** after touching any of it.

## 阅读理解问答 — a passage answered IN WRITING (v2.2.0)

The B组 of the paper: one 短文, then Q34–Q40 answered in sentences, each with a
ruled box and its own marks — *（2分）*, *（4分）*, 7题22分. No options anywhere.

It needed **no new block type**. It is a passage question like any other: the
passage in text blocks with no part, then per question a `text` block carrying
its letter and a `plainanswer` block carrying the same letter and the model
answer. What it needed was the three things that were missing around it —
**marks**, **a way to answer by hand**, and **a whole script of photos**.

### 分 — the marks the paper gives each answer

- **`qaMarks(block)` is the ONE place a block's allocation is read**, and
  **`qaWeight` is the ONE place it becomes a score**. `qaMarks` returns 0 for
  "not set"; `qaWeight(0)` is **1**. That default is the whole compatibility
  story: every question authored before 分 existed is scored exactly as it
  always was, one point a part.
- A verdict is worth `w` / `w/2` / `0`, so a 4分 question outweighs a 1分 one and
  the question is out of the paper's 22 rather than out of 7. **Both marking
  paths weight identically** — `markOpenAnswersIn` and `markQuestionPart` — or
  the score would change with the button the student happened to press.
- `_openTotalWeight` reads the denominator from the ITEM store, never from the
  results, so the total does not grow as parts are marked.
- **Marks are taken on a `plainanswer` only.** A Claim/Evidence/Reasoning block
  renders THREE items, so an allocation stamped on it would be charged three
  times and a 2分 question would be out of 6.
- The marker is TOLD the marks (`marks=4` on the item line) — a 4分 answer wants
  the reasons as well as the point, and without it the model marks to its own
  idea of full. The label prints on the paper too (`qaPrintMarksHtml`), from the
  same function, so screen and paper cannot disagree.

### Three ways to answer, one marker

- **Typed** — the 拼音 keyboard, as before. The box is sized from the marks: a
  4分 answer gets a paragraph's worth of rows, a 1分 answer a phrase's.
- **✍️ Handwritten on screen (`hw*`)** — a pad under every open answer, for a
  stylus on an iPad. The ink is an ANSWER, not an annotation: the diagram pads
  (`_annot*`) compare a drawing to a model drawing, this is handwriting the
  marker READS. Strokes live **on the element**, never in a map keyed by index —
  the same question can be on screen in two surfaces at once. `touch-action:none`
  is load-bearing: without it the first stroke scrolls the page instead of
  drawing. The listeners are ONE delegated set, because this app builds its DOM
  continuously and anything bound per pad misses every pad made afterwards.
- **📸 Photographed — several pages at once.** `_openPhoto[containerSel]` is a
  **LIST** (`_openPhotoList` is the one place it is read as one), because an
  answer script runs to two or three sides and a one-photo route made the
  student mark the page in instalments. They go in ONE call.

- **`_openAnswerMedia` is the ONE place the images going to a marking call are
  assembled and described**, and both marking paths ask it. The order is fixed —
  pages first, then one image per pad with ink — and the note names each image
  BY NUMBER. Let the note and the array drift apart and item (a) is marked
  against item (d)'s handwriting: a wrong mark, delivered fluently, with nothing
  on screen amiss. Marking ONE part sends only THAT part's ink; a multiple-choice
  part gets the pages and no pads at all.
- **The marker returns what it READ** and it is shown back to the student and
  recorded as their answer. Without it a photographed script reaches the mistake
  log and the learning-gap list as a blank, and a misreading is invisible.
- The pads **lock and clear with the typed answers** (`hwLockIn` / `hwClearIn`),
  or ink left through a reset is last attempt's answer waiting to be marked again.
- Run **`node tools/written-answer-tests.mjs`** after touching any of it.

## ✍️ Synthesis & transformation (`sy*`, block type `synthesis`)

Its Chinese equivalent is 改写句子 / 句子重组, and the block is unchanged: one or
two sentences, a word or a pair of connectives the student must use, and ONE
rewritten sentence meaning exactly the same thing.
*"他很努力。他的成绩进步得很快。" + "因为……所以"*.

**It is marked by the AI as one whole sentence, and that is the design
constraint.** There is no marking a rewrite in pieces — the meaning lives in the
arrangement, so a clause correct on its own can still be the wrong answer, and a
sentence differing from the model answer word for word can still be right. The
student writes ONE sentence and the marker receives ONE string.

### On screen it is the PAPER: ruled lines, not a box (v1.9.1)

The paper gives this question two ruled lines with the word provided printed at
one end of the first, and the student writes one sentence across both. That is
what the screen shows: `syLines(block)` clickable rules, the cue printed where
the paper prints it, the closing full stop at the end of the last rule — and
**no square marks box**, which on paper is where a teacher writes a mark and on
screen is furniture.

- **Several boxes, still ONE answer.** `_openAnswerEls(el)` is the ONE place the
  group of rules is resolved, and everything that reads, paints, clears or locks
  an answer asks it. Each of those fails in its own silent way if a rule is
  missed: half a sentence surviving a reset into the next question, a red border
  on rule one and none on rule two, and worst — a second rule still typeable
  after the question has been marked and scored.
- A box with no `data-sy-group` **answers for itself**, which is every other
  question type in the app. They see no change at all.
- Only the **FIRST rule** is the registered `.open-answer` and carries
  `data-oidx`. Two would register one answer twice and mark the student on half
  a sentence, twice over.
- `syLineKey` walks the rules — Enter and ↓ forward, ↑ and Backspace-on-empty
  back, never Tab, and never into a locked rule.

- **It hangs off the EXISTING open-answer plumbing rather than growing its own.**
  It renders an `.open-answer` inside an `.open-answer-section` and registers one
  item in `items`, exactly as `_openSection` does, so every marking path, the
  score, the mistake log, the photo-of-your-page route and `_checkAllPartsMarked`
  cover it without knowing it exists. **Do not add a second marking path.**
- **`syRubric` is the ONE place the marker is told what "correct" means**, and it
  travels on `item.rubric` into both marking prompts. Without it the model falls
  back to comparing wording against the model answer and fails every valid
  rewrite phrased differently — which is most of them. Both prompts say a rubric
  OVERRIDES the default "compare by meaning" instruction for that item.
- **`_openAnswerText(el)` is the ONE place an answer is read**, and both marking
  paths call it. It reads the page in the order the page reads, putting back the
  three things that are PRINTED and therefore never typed. Each one missing marks
  a perfect rewrite wrong in its own way:
  - the given **opening** ("This plot of corn ______"), or the marker gets a
    fragment and says it is not a sentence;
  - the word provided printed **BETWEEN the rules** ("… because of its" / "… or"),
    or the marker reads the two rules run together, cannot find the word the
    question required, and says the connector is missing — the whole question,
    answered correctly, marked wrong (v1.9.2);
  - the closing **full stop**, or it marks a perfect answer down for punctuation
    nobody asked for.

  Each goes back **only where the student has not already written it**
  (`_syAlreadyTyped`): a student may reasonably type the whole sentence on one
  rule, word provided and all, and doubling it — "…进步得很快。因为" — is
  the same wrong answer from the other direction. An empty set of rules stays
  empty: printed words alone are never an answer.
- **`cueHere` in `syStudentHtml` decides BOTH the span the student reads and the
  `data-after` the marker reads.** Two expressions could disagree, and that
  disagreement is invisible — the page shows the connector, the marker never
  sees it. Same reason `qPartLabelFirst` is asked by screen and paper alike.
- **`syStudentHtml` refuses a block with nothing given**, exactly as
  `syPrintHtml` does — an item is a markable answer, and one with no question
  behind it is a mark the student can never earn.
- `cuePos` is `'use'` (printed at the end of the rule, the sentence must contain
  it) or `'start'` (the given opening). Only `'start'` writes a `data-prefix`.
- **`QPART_OPENER_TYPES` gained `'synthesis'`** — the block carries its own
  question wording, so labelling it is honest on the printed page.
- **Both print builders carry an explicit `case 'synthesis'`**, for `fillblank`'s
  reason: the read-only rendering shows the model answer, which on a worksheet
  is the whole question given away.
- The PRINTED page **keeps its marks box** (`print-sy-box`). Screen and paper
  differ here on purpose: paper is marked with a pen.
- Run **`node tools/synthesis-tests.mjs`** after touching any of it.

## Word & grammar help on a marked question's options

`wh*` (in `app.js`, search `WORD & GRAMMAR HELP`). Once a multiple-choice
question has been **marked**, every option becomes hoverable — tap the ⓘ on a
touch screen — and the card says two things: what the word or phrase **means**,
and why that word **does or does not work in this sentence** (the tense, the
preposition, the part of speech, the partner word).

The second half is the point of it. `_genAndShowExplanation` writes an A.I.
Explanation only when the question has an OPEN part (`hasOpen`), so before this
an MCQ-only question — which is most of 语文应用 — ended at a red border
and a green one and told the student nothing about the difference.

- **`_mcqPaintResult` is the ONE painter**, and `whArm` is called from it and
  nowhere else. All three marking paths (`markOpenAnswersIn`, and both branches
  of `markQuestionPart`) carried their own copy of the colouring loop, which is
  exactly how this would have ended up armed on two surfaces out of three.
- **It must never arm before marking.** Hover the four options on an unanswered
  question and the one that "fits" is the one to tick. `resetOpenAnswersIn`
  disarms for the same reason, and the gate is the **`wh-on` class checked in
  `_whOpen`** — not unbinding the listeners, which cannot be done without a
  handle on every closure, and which is why a reset used to leave a question
  that still answered a hover.
- **ONE call covers the WHOLE option list**, through `askGeminiCached` (this is
  its first caller) so the prompt hash is the cache key: the prompt carries the
  question, every option and which is correct, so an edited question can never
  be served the old wording's answers. A failed call **removes** that key — the
  raw reply is already in `sessionStorage`, and if it was the PARSE that failed,
  leaving it makes every retry for the rest of the session fail instantly.
- **An answer is placed against an option by the option's OWN number.** This is
  the one thing here that fails silently: an explanation under the wrong option
  reads perfectly and teaches a child the opposite of the truth. `_whNormItems`
  falls back to positional order **only** when the model numbered nothing at all
  AND returned exactly one entry per option; a partial unnumbered list is
  dropped rather than guessed at.
- **An option with no words gets no badge** (`_whHasWords`). A question whose
  choices read "(1) (2) (3) (4)" against a diagram — the shape ✅ Check
  Questions exists to encourage — has nothing to define.
- Run **`node tools/word-help-tests.mjs`** after touching any of it.

## Printing

- **Printed / PDF worksheet answer boxes** are sized from the MODEL ANSWER by
  `printAnswerLines(block, text)`: `PRINT_ANSWER_LINES` (2) is the floor, a
  one-number / ≤4-word answer (`PRINT_SHORT_CHARS`) gets 1 line, longer answers
  scale at `PRINT_LINE_CHARS` (52) characters a ruled line with a
  `PRINT_HAND_ALLOWANCE` (×1.15) for handwriting, capped at `PRINT_LINES_MAX`.
  Each Claim / Evidence / Reasoning box is sized from ITS OWN field. The answer
  block's "Printed lines" field (`block.printLines`) overrides the estimate;
  blank means Auto. The box `min-height` in the print CSS is one line + padding
  (32pt) — do not raise it. Both print paths — `doPrintWorksheetOpen` and the
  saved-worksheet builder — must stay in step.

- **On-screen picture width** is capped by `IMG_AUTO_MAX_PCT` (70%) inside
  `imgSizeStyle` — the ONE function every rendered picture goes through. It is a
  `max-width` CAP, never a `width`: setting `width:70%` would stretch a small
  inset UP to 70% of the column. A picture the author sized by hand
  (`block.scale`) keeps that size.

- **Printed picture heights** — `.print-question-page img` caps at **92mm**, with
  `print-img-sm` (60mm) / `print-img-lg` (140mm) / `print-img-full` (170mm)
  chosen per picture by the image block's "Print size" control. A question whose
  SINGLE picture is paired with ≤3-character MCQ options is upgraded to Large
  automatically (`imgQuestionNeedsBig`). Do NOT go back to one flat 170mm cap.

- **`.print-text-block img` must not set `max-height`.** That selector has the
  SAME specificity (0,1,1) as the `.print-question-page img` 92mm cap while
  sitting later in the file, so a `max-height` there wins and makes
  `print-img-lg` *smaller* than Auto. The ladder must read 60 / 92 / 140 / 170mm.

- **The print planner must MEASURE, never assume.** `_printPlanIn` lays every
  page out in a print-CSS iframe; a page needing fit-to-page shrinking goes
  through `_printVerifiedZoom`, which re-measures with the zoom applied and steps
  down until the page really fits, falling back to a flowing
  (`print-page-tall`) page at the zoom floor. The page box is a fixed height with
  `overflow: visible`, so any un-verified overestimate paints over the NEXT sheet.
  Five things keep the measurement honest — none optional:
  - **Pictures must reserve their box before they load.** An `<img>` that has not
    decoded occupies ~22px, not the ~350px it prints at, and the planner's iframe
    RE-FETCHES every picture. `_printLearnImgDims` / `_printStampImgDims` stamp
    `width`/`height` onto every printed `<img>`. If anything is still unsized,
    `_printPlanPages` refuses to plan and takes `_printFlowFallback`, which is
    denser but can never overlap. **Never emit a printed `<img>` without dimensions.**
  - **`usable` must reserve the page number.** `.print-page-number` is stamped on
    AFTER planning, so `usable = PRINT_PAGE_PX − numH − PRINT_FIT_SAFETY`.
    `budget` derives from the same ceiling, so the packer and the verifier cannot
    drift apart.
  - **A page promoted to tall must promote its CHUNKS too.** `_printPlanIn`
    writes `cls.tallFlags[idx]` and adds `.print-chunk-tall` for the whole group,
    because a chunk that cannot break on an over-sheet page overflows.
  - **The measuring iframe must get the real fonts.** Both font `<link>`s are
    `media="print"` and the iframe is a SCREEN medium, so copying them verbatim
    measures every stem in fallback metrics. `_printFontLinksHtml` forces
    `media="all"` on the COPIES. Never copy `link.outerHTML` directly.
  - **No box may be taller than a sheet.** `PRINT_LINES_MANUAL_MAX` (24) caps the
    author's override; `_wsBlockLines` / `WS_BLOCK_LINES_MAX` (30) cap the raw
    pixel heights `openLines` / `workingSpace` write.

- **Fill-in-the-blank must print BLANK.** `renderImportedBlockStudent`'s
  `fillblank` branch is `_fbReadonlyHtml`, a REVIEW rendering with the answers in
  the slots. Both print builders carry an explicit `case 'fillblank'` using
  `_fbPrintHtml` and push `_fbAnswerKeyText` onto the key. Do not delete either.

- **EVERY question gets an answer on the printed key** (`_pushBlockAnswerKey` /
  `_qFallbackKeySection` / `_akQuestionSections`). Most answers live in an
  `answer` / `plainanswer` box; the rest do not, and were silently dropped — an
  **MCQ**'s correct option, an **`answerLine`**'s answer, a 🔑 **`answerKey`**
  block. A key that omits a question prints perfectly and looks tidy, so the
  teacher only finds out in front of the class.
  - **`answerKeyExtras` gates EXPLANATIONS ONLY.** An answer is never optional;
    an explanation is teaching commentary and stays behind the flag.
  - **`_pushBlockAnswerKey(sections, block, part)` is the ONE pusher both print
    paths call.** Adding an answer-bearing block type means adding a case there,
    not in two switches.
  - **A question with nothing still gets a ROW** — the explanation stands in
    (labelled *Explanation*), and failing that "No answer recorded for this
    question", because a gap in the numbering reads as a printing fault. The
    placeholder is substituted at RENDER time and is deliberately not what
    `hasAny` counts: a bank with no model answers must still print no key sheet.
  - Run **`node tools/answer-key-tests.mjs`** after touching any of it.

## Question parts — (a) (b) (c)

Parts live on `block.part`. A block carrying a part OPENS it and every block
after it INHERITS until the next opener. Read it with `qPartMap(blocks)` /
`qBlockOpensPart(b)` / `qHasParts(blocks)` — never write a second walker.

- **`block.part === QPART_NONE` (`'-'`) files a block under NO part** — how a
  note about the WHOLE question sits among the parts without lying about what it
  explains. It unfiles **that block only** and deliberately does NOT close the
  part. `qPartUnfiled(b)` is the predicate.
- **An explanation explains the question printed directly above it**, and that is
  enforced for EVERY authoring path:
  - **`qApplyAiParts(blocks)` runs inside `buildBlocksFromAi`** — the one
    function every AI authoring path goes through — in this order:
    `qSplitPartBlocks` → `qLiftPartMarkers` → `qScopeExplanations`. The guards
    keep it safe: splitting needs `<br>` to be the only markup
    (`QPART_ONLY_BR_RE` — the cut is a source offset), lowercase consecutive
    letters, and no `mcq` block; lifting inside an MCQ is allowed only on the
    FIRST text block, because every other lettered line is an option.
  - **The AI buttons write for ONE part.** `aiGenerateBlockExplanation` and
    `aiGenerateBlockAnswer` scope their prompt to the part the box sits in,
    marked `>>>` by `_aiPartScopeLine`, with the other parts as labelled
    background they are told not to write.
  - **Every build prompt carries `_partsPromptRules()`** — keep the four prompts
    pointing at that one fragment rather than restating the rules.
- `qPartDetect` matches a single letter **a–h** at the very start, parenthesised
  or not, closed by `)` or `.`. It stops at `h` on purpose (`i` collided with the
  roman sub-part `(i)`), and a bare `X.` must be LOWERCASE (`E. coli` is prose).
  **`QPART_ASSIGN` is a separate, longer alphabet** for what the editor may
  ASSIGN — detection has to be conservative about unvetted text, an admin
  numbering by hand is not guessing.
- `autoNumberParts` must never write an EMPTY part: `qPartMap` inherits forward,
  so an unlabelled opener is filed under the PREVIOUS part and two answers share
  one heading — the very bug parts exist to prevent.
- **Apply re-resolves each question by id** and checks the block still holds the
  scanned text, then saves a COPY and only commits to `questionBank` on success:
  between scan and apply a question can be edited or deleted.

### The label is drawn from the BLOCK, so it must not also be in the TEXT (v2.8.1)

`qStripOwnPartMarker` / `qPartBodyHtml` / `_qPartOwnMarker` (in `app.js`, search
`THE LABEL IS DRAWN FROM THE BLOCK`).

A block that opens part (a) already wears its label — the chip in the editor,
the tag beside the question on screen, the marker in the margin on paper. When
the SAME marker is also typed at the front of its content the question reads
**"(a) (a) 文中形容…"** on every surface at once.

- **It came in from the AI paths.** The model is asked to letter the
  sub-questions and answers by BOTH stamping `"part":"a"` and writing "(a)"
  into the wording — and `qLiftPartMarkers`, whose whole job is to move a typed
  marker into the field, opened with `if (qBlockOpensPart(b)) return;`. The one
  case it could not fix was the one case that needed fixing.
- **It is handled at BOTH ends, and both are needed.**
  `qStripOwnPartMarker` takes it out of the BLOCK (from `qLiftPartMarkers`, from
  `setBlockPart` when an author labels one by hand, and on `editQuestion` so a
  question tidies itself the moment somebody opens it), and **`qPartBodyHtml`
  takes it out at RENDER** — the bank is already full of questions written the
  other way and nobody will open them one at a time. The render side never
  touches the block, so an author still sees exactly what is stored.
- **The marker must name the block's OWN part.** A block labelled (b) whose
  text opens "(a)" is two people disagreeing about which question this is, and
  that is for a human to look at — not something to tidy away silently.
- **`_qPartOwnMarkerRe` accepts FULL-WIDTH brackets and `QPART_MARKER_RE`
  deliberately does not.** That regex has to find a part in text nobody has
  labelled, where being wrong files a question under the wrong letter; here the
  block already says it is part (a), so a leading `（a）` can only be the same
  label twice. It also drops the `(?=\s|$)` guard **for the bracketed forms
  only**: a 华文 paper writes `（a）文中形容……` with the character hard against
  the bracket, so demanding whitespace there matched none of them. The two BARE
  forms keep it, or `a.` would eat the front of any sentence opening with a
  lone letter.
- **Two markers in one box is refused**, the same guard the Doctor's scan and
  `autoNumberParts` use: that is several parts written into one box, or an
  options list, and neither is fixed by removing the first.
- A **NUMBERED** part is left alone — detection is letters only, on purpose.
- `qPartDetect` now takes an optional regex; its default is byte-for-byte
  `QPART_MARKER_RE`, so nothing else about detection moved.
- Run **`node tools/part-marker-tests.mjs`** after touching any of it.

## Clearing the vetting list — deleting several at once (v2.7.0)

`_vetSelected` / `_vetVisibleQuestions` / `_vetDeleteMany` (in `app.js`, search
`DELETING SEVERAL VETTING QUESTIONS AT ONCE`), plus the tick box on every
vetting card, the `#vetBulkBar` above the grid and **🗑 Delete all** beside
✨ AI Auto-Vet All.

The vetting list is where a whole BAD BATCH lands — forty screenshots off the
wrong paper, an import run twice, a set the model made a mess of. Clearing that
one card at a time is forty confirm dialogs, which is why it gets left instead,
and a vetting list nobody clears is one nobody reads either.

- **"All" means every card the author can SEE.** `_vetVisibleQuestions` is the
  ONE place that set is worked out — filtered by the search box, newest first —
  and the cards, the tick-all box, 🗑 Delete selected and 🗑 Delete all all read
  it. Deleting questions hidden behind a filter is the one outcome nobody could
  have predicted from the button they pressed, so the confirm **says which of
  the two it is doing** and how many are being spared.
- **The deletes are AWAITED, one document at a time** (`deleteVettingDocAwait`,
  the awaited twin of the fire-and-forget `deleteVettingDoc`). A batch has to be
  able to report that four of forty would not go, and a question leaves
  `vettingList` only once its document really went — the same order every other
  move in this app uses. A list that has dropped a question the database still
  holds looks perfectly right until the next sign-in.
- **The selection is PRUNED on every render** (`_vetPruneSelection`). A ticked
  question approved into the bank, edited away or auto-vetted out is not a thing
  to delete; doing it in the renderer rather than in each of those paths is what
  covers a path added later. "3 selected" outliving the cards it counted is how
  the wrong question gets deleted.
- **The ticks live in a `Set` of ids, never as a flag on the question.** Those
  objects are replaced wholesale by re-reads and cross-tab syncs, which would
  silently drop the tick.
- **`.vet-pick` must set `appearance: auto`** — Tailwind's preflight sets it to
  `none`, which leaves an invisible white square exactly where the control the
  author is looking for should be. The usual trap.
- A ticked card's outline **outranks** the duplicate / just-added one while it is
  ticked and gives it back when unticked: both are inline styles, so one has to
  win outright rather than being layered.
- **This delete is FINAL — it does not go through the 🗑 bin.** It is the same
  `deleteVettingDoc` the single card's 🗑 has always used, and the confirm says
  so in as many words. A vetting draft that should be kept is approved into the
  bank, where deleting *is* a move to the bin.
- Run **`node tools/vetting-bulk-delete-tests.mjs`** after touching any of it.

## "You may already have this one" — the duplicate warning (v2.8.0)

`findDuplicateCandidate` / `checkEditorDuplicate` / `dupWatchKick` /
`_dupGateSave` (in `app.js`, search `THE DUPLICATE WATCH`), plus the
`#dupWarnBanner` at the top of the question editor and the 🟡 badge on a
vetting card.

The matcher itself is old: a token-overlap (Jaccard) score over the title, the
body and the MCQ options, past `DUP_MIN_SCORE` (0.7). What was missing was
everywhere it was not being asked.

- **It used to be raised from ONE place — straight after 🤖 Build from
  screenshot.** So a question TYPED into the block editor, pasted, built by the
  passage builder, or opened and reworked was checked against nothing at all,
  and the only duplicate warning in the app was a badge on a Rapid add card.
  The bank fills up with the same question twice and nothing anywhere says so.
- **The banner is LIVE.** `dupWatchKick` re-checks as the author works, so the
  warning is on screen while there is still something to do about it. The
  listener is **ONE delegated pair on `#page-create`**, for the reason the 拼音
  IME's is: this app builds the editor's DOM continuously, so anything bound
  per element covers the fields that existed when it ran and silently misses
  every one made afterwards. **`renderBlocks` kicks it too** — a builder writing
  blocks programmatically fires no `input` event at all.
- **The SAVE asks as well, and that is the backstop.** A banner sits at the top
  of a long editor and the Save button is at the bottom, so `_dupGateSave` is on
  all three editor saves — ✅ Add to vetting, 💾 Save, and Save straight to the
  bank. It is a **PROMPT, never a block**: only the author can tell a real
  duplicate from two questions that merely share a stem, so "Save anyway" is
  always there.
- **The gate is a PASS-THROUGH, never a second write path.** Each save function
  keeps its body in a `*Confirmed` twin, so answering "Save anyway" ends at the
  same door — and therefore the same ordering guarantees — as before.
  `tools/question-persistence-tests.mjs` pins that.
- **The VETTING LIST is searched as well as the bank**, and the result says
  which (`_dupWhereLabel`). The commonest duplicate of all is the same
  screenshot read twice in one sitting, and BOTH copies are then in vetting,
  where a bank-only search sees neither — nothing was flagged, and the pair was
  approved into the bank one after the other.
- **`_dupStillThere` is the ONE place a suspected twin is checked for existence**,
  and it reads both lists. The vetting card used to ask `questionBank` alone, so
  a twin that is itself still in vetting made the badge vanish.
- **The banner's 👁 button ASKS before it leaves** (`dupOpenOriginal`). The
  banner is on screen while the author is mid-compose, so loading the twin
  replaces the draft they are looking at; hovering the same button previews a
  BANK twin without leaving at all, which is the answer most of the time. The
  vetting card's copy of the button needs no guard — nothing is being typed
  there — which is what the third argument to `_dupSeeOriginalBtn` selects.
- **The hover preview is attached only for a BANK twin.** `ppBankHoverHtml`
  reads `questionBank` and nothing else, so a vetting original would open an
  empty card that reads as a broken preview.
- Run **`node tools/duplicate-warning-tests.mjs`** after touching any of it.

### ⇄ Side by side — the comparison the warning was missing (vv2.10.0)

`dupCompare` / `_dupFindQuestion` / `_dupCompareSide` / `_dupDiffHtml`
(search `SIDE BY SIDE`), plus the `#dupCompareOverlay` in `index.html`.

The banner said *"this looks 90% like Sharing a Sum of Money"* and offered
exactly ONE button: **open** that question. Which replaces the draft — so the
only way to answer the question the banner asks (*are these two the same?*) was
to throw away the thing being compared, go and look, and then build it again
from memory. Nobody does that, so the warning got clicked past, which makes it
a warning that costs attention and buys nothing.

The two questions now go up **next to each other**: what is being written on the
left, what is already filed on the right.

- **Both sides go through the SAME renderer** — `renderQuestionBodyPreviewHtml`,
  split out of `renderQuestionPreviewHtml` so it takes the question OBJECT
  rather than an id, because the left-hand column is a draft that has never been
  saved and has no id to look up. A second renderer written for this view would
  be free to drift, and a comparison whose two halves are drawn by different
  code can flatter one of them.
- **Nothing is written and nothing is replaced by opening it.** It is a read.
  The one destructive action — loading the original into the editor — lives in
  the overlay's foot, still behind `dupOpenOriginal`'s confirm, and is now
  reached only by somebody who has actually seen what they are about to lose. It
  is **hidden** when the left-hand side is a saved question (a vetting card),
  because there is no draft to lose there.
- **`mineId` names the LEFT-hand question.** A vetting card passes its own id;
  the editor banner passes nothing, and the draft is read from
  `_dupEditorQuestion()`. That third argument to `_dupSeeOriginalBtn` used to be
  a boolean `guard` — same position, different meaning, so check both call sites
  if you change it.
- **It says what differs IN WORDS** (`_dupDiffHtml`, through the matcher's own
  `_dupTokenSet`). Two near-identical questions are near-identical to LOOK at,
  which is the whole problem: the eye slides straight over the one changed
  number. The words appearing on one side only are the fastest honest answer to
  "so what did they change?", and a diff computed on any other footing would
  contradict the percentage printed above it. When both lists are empty it says
  *word for word the same*, which is the strongest thing it can tell an author.
- Run **`node tools/duplicate-warning-tests.mjs`** after touching any of it —
  the direction of the difference strip is the silent one: reversed, the two
  lists read perfectly and tell the author the opposite of the truth.

### The matcher had never fired in this app at all (v2.10.0)

`_dupTokenSet` / `_dupCjkBigrams` / `_DUP_CJK_RUN_RE`.

`_docNorm` keeps only `[a-z0-9]`, so a 华文 question normalised to an EMPTY
STRING, `target.size < 3` refused it, and `findDuplicateCandidate` returned null
every single time. The banner, the vetting badge, the save prompt and now the
side-by-side comparison all hang off that one function — so the whole feature
was decoration here, and nothing threw or looked wrong.

- **Two kinds of token, and both are needed.** Latin words keep the `length > 2`
  rule they always had (a romanised name, a number, an English title). Chinese
  is written without spaces, so it is tokenised as character **BIGRAMS** —
  学习 / 习成 / 成绩.
- **Bigrams, not characters and not words.** Single characters are far too
  common (的 and 是 would make any two questions look alike), and whole words
  would need `zhSegment`, whose dictionary is FETCHED and may not have arrived
  when the matcher runs.
- The harness cuts from `const _DUP_CJK_RUN_RE`, not from `_dupTokenSet`: the
  tokeniser calls the helper, so a cut starting at the tokeniser loads a matcher
  that throws on its first question.
- Four cases pin it from both directions — an identical 华文 pair must be
  flagged, two different questions on one topic must NOT be, a question must not
  match itself, and a mixed English/Chinese question must count both halves.

## Authoring surfaces that must not be merged

- **📄 Exam Paper** (`ep*`) takes a whole paper the way a teacher has one:
  question screenshots ONE AT A TIME, the marking scheme SEPARATELY, and the
  paper's own answers slotted in by **question number**.
  - **Nothing is written until Send.** The paper sits in `_epShots` /
    `_epKeyShots` in memory; `_epCommit` is the only writer and it goes through
    `saveQuestion` / `saveVettingQuestion` like every other path.
  - **Screenshots are read as a RUN, never one question per screenshot.**
    `_epRunBuild` sends `EP_BATCH` (4) at a time as multiple images in ONE
    `askGeminiVision` call. Reading is always a read of the WHOLE set — adding or
    removing a screenshot sets `_epDirty` and asks for a re-read.
  - **The paper's question number never reaches the question**
    (`_epStripNumbering`). `EP_LEAD_NUM_RE` ends in `(?!\d)` or "2.5 kg of ice"
    opens with what looks like question 2; a bare leading number needs a `.`/`)`
    after it, so "50 ml of water was added" survives.
  - **The link between a question and its answer is `_epNumKey(number)`**, which
    collapses `Q12 (b)`, `12b` and `12(B)` to one key. Every unmatched question
    gets a per-row `<select>` in the ③ Match table.
  - **A question with parts is matched PART BY PART** — the paper numbers ONE
    question while the scheme answers (a), (b), (c) separately. `_epApplyAnswer`
    places each answer **inside that part's own run of blocks**, never on top of
    the next part's. A question matched on only SOME parts is **partial** and
    both the ③ table and the Send dialog say so.

- **🖊️ Mark Paper** (`mp*`) is the exam-paper builder read backwards: the same
  paper once a student has WRITTEN on it.
  - **It is not Snap & Mark.** Snap & Mark is the STUDENT's tool — one photo, one
    question, matched against a question that must already be in the bank. A
    marked script is thirty questions the bank has never seen, so the questions
    here are read off the paper itself.
  - **The answer key has three sources, best first, and every row says which**:
    🔑 the paper's own marking scheme, 📚 a bank question that is plainly the
    same (`_mpBankMatch`, a cheap token overlap with `MP_BANK_MIN_SIM` at 0.62
    because a wrong match marks the student against the wrong question), then 🤖
    the model's own answer. A teacher checking a mark has to know which.
  - **Reading and marking are separate passes.** `_mpReadScript` sends
    `MP_READ_BATCH` (3) pages in one vision call and is told to transcribe, never
    to mark; `_mpMarkAll` then marks from the transcription in text-only calls.
  - **Nothing is written anywhere.** A marked script is a child's work; it lives
    in memory and leaves through `mpPrintReport` / `mpCopyReport`.
  - Guards: an unmarked question defaults to 1 (MCQ) / 2 (written); `awarded` is
    clamped to `[0, marks]`; a `correct` verdict earns FULL marks; a blank answer
    can never be correct; a batch whose AI call FAILED renders `unmarked` with a
    note rather than a silent zero.

- **✅ Check Questions** (`cq*`) serves the newest questions back one at a time
  for a second pair of eyes. It is not the Question Doctor: the Doctor is a
  whole-bank audit read as a LIST, this is a QUEUE worked newest-first.
  - **The headline check**: a question whose TABLE OR DIAGRAM already sets out
    the four choices, with the options underneath repeating them in words. Those
    should read just **(1) (2) (3) (4)**.
  - **Two layers find it, and neither can do the job alone.** Structurally it is
    decidable only when the choices are in a `table` block. The same question
    with a **picture** is invisible to any text check, so the AI pass attaches the
    diagrams (`_cqMedia` → `askGeminiVision`). **Do not "optimise" that down to
    `askGemini`** — without the images the check cannot be made.
  - **The one-tap fix must never be a guess.** `_cqMcqFixable` gates it on a real
    option list that is not already numbered; the button blanks the wording of
    all four options, so offering it on a question whose choices are NOT in the
    picture destroys the question while looking tidy. The picture-only case
    raises a low-severity nudge with **no fix button**.
  - **`q.checked` lives on the QUESTION, not per user**, and is written with a
    **quiet** save — reading a question is housekeeping, not authoring. It is
    deliberately absent from `EDITOR_OWNED_QUESTION_FIELDS`.
  - Run **`node tools/check-questions-tests.mjs`** after touching any of it.

## 🗑 The bin — deleting a question is a move, not a delete

A question is somebody's work: a screenshot cropped, an answer written, a
diagram touched up. So every real deletion in the app is a **move**
(`questionsZh` → `binZh`, `binQuestion`), restorable in one tap for `BIN_DAYS`
(7), after which the next sign-in sweeps it for good.

- **`binQuestion(id)` is the ONE deletion path** — the bank card's 🗑, the
  Question Doctor's, and ✅ Check Questions' all go through it. `deleteQuestionDoc`
  is the raw hard-delete and stays that way, because two of its three call sites
  are **moves to vetting**, not deletions; binning there would leave a copy in
  the bin of a question that is still very much alive.
- **Copy → read the copy back → delete the original**, the same order as the
  legacy bank rescue. If the copy cannot be verified the question stays in the
  bank; if the *original* cannot be deleted the bin copy is rolled back, because
  a question in both places is worse than a question that refused to delete.
- **A binned question is OUT of `questionsZh`.** It is not a flag on a live
  question — no practice mode, worksheet, search or student can reach it. A
  saved worksheet that referenced it draws its "no longer in the bank" row, and
  restoring puts it back.
- **`binExpired` KEEPS a record whose date it cannot read**, and that asymmetry
  is deliberate: keeping one too long leaves a row in a dialog with a *Delete
  forever* button beside it, while sweeping one too early destroys work in a
  background job with nothing on screen to show it happened. `_binExpiryMs`
  accepts **only an ISO string** for the same reason — `Date.parse` coerces, and
  `Date.parse(12345)` is the *year 12345*, so a numeric timestamp would read as
  perfectly healthy and sit in the bin for ten millennia.
- **The purge is client-side** — there is no server — so it runs when an author
  next opens the app, not on the stroke of the seventh day. `binDaysLeft` is
  therefore what the bin PROMISES (never *less* than 7 days), not a countdown.
- **The confirm dialog is on the bank and the Doctor, and deliberately NOT in
  Check Questions.** That queue is worked at speed with one big button and an
  ↩ Undo in view at all times; a dense list of small 🗑 icons is a different
  risk. `cqUndo` covers the deletion *and* the last ✓, newest first.
- `_firestoreSafeQuestion` is shared with `saveQuestion` — Firestore rejects
  nested arrays, so a table question written to the bin without it fails to save
  at all. Run **`node tools/bin-tests.mjs`** after touching any of it.

## A question is saved when Firestore says so (v2.4.0)

The bin above is careful because deleting is the one action that destroys work.
It wasn't: **a question could disappear without anyone deleting anything**, and
that is what this section is about.

Every authoring path grows `questionBank` / `vettingList`, redraws the page and
says "Question added to bank ✓" **before** the write resolves, then throws the
result away — `saveQuestion(q); // async, non-blocking` at a dozen call sites.
So a write that failed left a question on screen, in the bank, in the count,
searchable and pickable for a worksheet, and in **no database**. It lasted
exactly as long as the tab. Nothing looked wrong at any point; the question was
simply not there at the next sign-in.

- **`saveQuestion` and `saveVettingQuestion` are the two doors, and they must
  stay identical in shape.** Both now build their payload with
  `_firestoreSafeQuestion`, both return TRUE only when Firestore took it, and
  both take `opts.quiet` / `opts.noStash`. `saveVettingQuestion` had **neither**
  the conversion nor a return value, and the missing conversion alone destroyed
  one whole class of question: Firestore rejects nested arrays, a table block
  holds array-of-arrays the moment `normalizeLoadedQuestion` has touched it, so
  every already-loaded table question sent back to vetting was refused — after
  the bank copy had been deleted. 🚩 Move to vetting, on a question a student
  flagged, is the path that did it.
- **A move goes through `moveVettingToBank` / `moveBankToVetting`, and nothing
  else.** Both follow `binQuestion`'s order: write the destination, WAIT for it,
  and only then delete the source. Five paths used to do it by hand and all five
  in the losing order — `saveQuestion(q); deleteVettingDoc(id);`, a write nobody
  waited for beside a delete that happened regardless. **Auto-Vet ran that pair
  in a loop over the whole queue**, which is how a batch went at once. Do not add
  a third mover.
- **A failed move stashes NOTHING** (`noStash`). There is nothing to rescue —
  the question is still whole in the collection it was moving out of — and a
  copy kept on the device would write a SECOND one on the next sign-in, beside
  the row it never left. The ordering fix would have become a duplicating one.
- **A failed write is kept on the device and retried** (`_unsaved*`,
  `zhUnsavedQuestions` in localStorage, retried by `unsavedInit` on every
  authoring sign-in). The net is INSIDE the two doors, not at the dozen call
  sites, so an authoring surface added later is covered without knowing it
  exists. Keyed **per uid** — a stash replayed under the wrong account writes one
  author's questions into another's bank. `quiet` writes are excluded: the usage
  backfill and the auto-tagger re-write questions already in the bank, and a
  queue of those would push the author's real losses off the end of it.
- **The stash is shown** (`.unsaved-banner`, on the Bank and Vetting pages). A
  stash nobody is told about only trades a question that vanished for a question
  sitting in localStorage that nobody knows to retry.
- **An employee may not write while `adminUid` is null** (`_bankWriteBlocked`).
  `_bankOwnerUid` falls back to their OWN uid, and a question written there is
  one nobody ever sees again — not the teacher, not a student, and not the
  employee, who gets the teacher's bank back the moment the pointer resolves.
- Run **`node tools/question-persistence-tests.mjs`** after touching any of it.

## Image touch-up & the transform session

- **Touch up & label** (`_annotXform*`) is ONE session shared by Resize (F),
  Rotate (R) and Skew (K): the selected pixels are lifted onto their own layer
  and nothing is committed until Apply, so 30° and back to 0° leaves the pixels
  as sharp as they started. The transform is **scale → skew → rotate**, and
  `_annotXformMapper` and `_annotXformDrawInto` must apply it in that order or
  the handles drift off the picture they are drawn on.
  - Resize drags the eight handles round the box: the corner OPPOSITE the one
    being dragged is the anchor, so the maths runs in the **M-frame**
    (`_annotXformMFrame`), where the new factor is just
    `(pointer − anchor) / handle-span`. Only the axes a handle actually DRIVES
    get a vote when "keep shape" is on, and `_annotXformRecentre` puts the pivot
    back in the middle after every resize or move.
  - A pointer arrives in CANVAS coordinates and the transform lives in the
    pre-offset frame, so anything comparing the two goes through
    `_annotXformUnoffset` or a grown canvas breaks the hit test.
- **The brush cursor is a RING at the real size of the mark**
  (`ANNOT_RING_TOOLS` / `_annotUpdateBrushRing`). The tools that take no size
  show no ring, and `_annotUpdateBrushRing` only touches `canvas.style.cursor`
  for a tool that IS in `ANNOT_RING_TOOLS`, or it fights the resize handles'
  own cursors. The ring lives in the STAGE, never on the canvas (which is scaled
  and panned underneath it). `_annotSyncControls` is the ONE place every route to
  the size lands, so the "12 px" badge flashes from there.
- **A picture can be PASTED straight in** (`_annotPasteHandler`). Ctrl+V drops it
  on the canvas scaled to fit (`ANNOT_PASTE_FIT`, 90%) and opens the transform
  box with **Resize already in hand**.
  - It is its **own transform scope, `paste`** — the pixels do not come off the
    canvas, so Cancel leaves no trace.
  - **`_annotXformIsIdentity` must return false for a paste**, or a picture
    dropped at 100% and 0° is read as "nothing to do" and silently thrown away.
    That is the one bug this scope can produce, and it looks exactly like the
    paste never happened.
  - The handler is bound in **capture**, because the exam paper builder, Mark
    Paper and the contenteditable guard all listen for `paste` underneath.
- **`_annotPaintCompose` sets the composite mode for a WHOLE stroke** and
  `_annotUp` puts it back; `_annotSetTool` resets it too — a canvas stranded in
  `destination-out` erases everything drawn afterwards.
- **Annotation answers** — an annotation pad carries its own answer on the block:
  `answerImg` is a screenshot of the diagram WITH the correct annotations,
  `answerKey` the same in words. All three consumers read the BLOCK, not the
  question: `annotShowAnswer`, `annotAiCheck` (which sends the screenshot as a
  SECOND picture so the AI compares two diagrams), and `_pushAnnotAnswerKey`.

## Roles

**admin / employee / student.** `EMPLOYEE_EMAILS` names accounts hired to WRITE
QUESTIONS: they get exactly `EMPLOYEE_PAGES` and nothing else. Two rules keep it
default-deny — `configureSidebarForRole('employee')` hides every `.nav-item` and
shows back only those pages, and `navigateTo` rewrites any other page to `create`
(hiding nav items alone would leave a bookmark walking straight in). **Anything
that switches a nav item on after sign-in must ask `_navAllowed(page)` first.**

Gate authoring on **`_canAuthor()`** (admin OR employee), never by widening
`_isAdmin()`. An employee has **no bank of their own**: `_bankOwnerUid()` points
`_qCol`/`_vCol` at the teacher's subtree, so `_resolveBankOwner()` must run (and
`adminUid` be set) before anything reads or writes. Employees must never write
the bank pointer — that is what students resolve the bank from. An employee must
be created with their REAL email; the dialog refuses an address not already on
`EMPLOYEE_EMAILS`. The `role` written to the profile is descriptive only — the
live role is decided at sign-in.

## Work sessions and concurrent tabs

- **The clock is two timestamps, never a counter.** `_wkElapsed` =
  `(endedAt || pausedAt || now) − startedAt − pausedMs`, so a minimised tab, a
  throttled `setInterval` or a sleeping laptop cost nothing. Do not "fix" it by
  accumulating ticks — that is the exact bug this shape prevents.
- `lastSeen` is a 60-second heartbeat meaning *the tab was demonstrably open at
  this moment*, and it is where an abandoned session is closed. Hours when
  nobody was at the keyboard are not hours worked.
- **Questions are logged from `saveQuestion` / `saveVettingQuestion`** — the two
  functions every committed question goes through. `opts.quiet` writes are
  excluded and `_wkSuppress` guards the automatic paths. **Both flags are read at
  CALL time into a local `wkLog`, before the `await`.**
- **One session covers ALL the author's windows, and every write MERGES.**
  `_wkMerge` must stay **idempotent**: items union by question id, `savesByTab`
  counts per tab, `pauseSetAt` decides whose pause is current, any `endedAt`
  wins. `uniq` is DERIVED from the merged list, never incremented.
- `xtInit()` opens a **BroadcastChannel**, falling back to a `localStorage` key.
  Messages are **hints, never data**: a tab is told an id changed and re-reads
  that document, so two tabs cannot talk each other into a state the database
  does not have. `_xtFlushQuestions` debounces (500 ms), **reads first and
  applies after**, and a read that FAILS changes nothing.
- `_xtTabId()` lives in **`sessionStorage`** — per-tab, kept across a reload.
  That is exactly what the exam paper draft needs; don't move it to localStorage.
- **The exam paper draft is mirrored to IndexedDB** (`_epDraft*`) so an unsent
  paper survives a reload. Three records per draft — `epmeta:` (a few numbers, so
  a scan never pulls another window's 90 MB of screenshots into memory),
  `epwork:` and `epshot:` (rewritten only when `_epShotsSig()` changes). Keyed by
  **tab**, never by user.

## Learning objectives

Filed from BOTH ends: from the objective's end (the 🎯 page writes
`loData.map[loId]`) and from the question's end (the editor's 🎯 field writes
`q.los`). **`loQuestions(id)` reads both and dedupes** — that is what makes them
one system. `loDetachQuestion` clears both ends, or the question reappears on the
next render.

- Nothing is written until the question is saved; `los` is in
  `EDITOR_OWNED_QUESTION_FIELDS` or `carryOverQuestionMeta` restores an objective
  the author just removed.
- **`var editorLos`, not `let`** — the block sits near the END of the module and
  `navigateTo('create')`'s reset can reach `loEditorSet` before it is evaluated.
- **`qLos(q)` drops an unknown objective at READ time, and only once the list has
  LOADED** — otherwise a question opened before the list arrives comes back from
  the editor stripped of every objective it had, and is saved that way.
- Run **`node tools/objective-tag-tests.mjs`** after touching any of it: every
  failure here is silent.

## Saved worksheets

A saved worksheet is nothing but an ORDERED list of bank ids (`ws.questionIds`),
so the editor (`wse*`) edits that list and everything else follows.

- It **never touches the question bank** — it only adds and removes references.
  Editing the question ITSELF is the quick-edit drawer (`wsQuickEdit`).
- **Every change persists as it is made** (`_wsPersistWorksheet`): a list of ids
  is a tiny write, and an edit the teacher believes is saved and is not is far
  worse than a chatty connection.
- Removing must also drop the id from `wsManualBreaks` / `wsMergeUp` — those
  overrides are keyed by question id.
- The **whole-paper editor** renders each question through **`buildOpenBody`**,
  the same renderer every student surface uses, so the preview cannot drift. Each
  row needs its OWN container selector — buildOpenBody keys its answer stores by
  selector, and the same selector twice clobbers the first question's answers.

## Versioning convention — applies to EVERY change

1. **Bump the version.** In `app.js`, update `const APP_VERSION = 'vX.Y.Z'`.
   Patch bump for fixes, minor bump for new features.
2. **Keep it visible.** It renders in the sidebar footer for admins only
   (`#appVersionBadge`, class `admin-only`).
3. **Report it.** When summarising an update in chat, always state the new
   version number (e.g. "Shipped in **v1.0.3**").

The point: the user checks the version shown in the sidebar against the number
reported in chat, to know whether the deploy actually went through.

## Design convention — breathing space

- Give elements room to breathe: generous, consistent padding inside
  cards/banners, clear vertical spacing between title → description → meta →
  buttons, comfortable line-height. Never cram content edge-to-edge.
- Cards/banners are rounded rectangles constrained to a sensible max-width (not
  full page width) and centred.
- When the user says something is "too big/thick/messy", the fix is usually
  *more* whitespace and a tighter width, not shrinking fonts until it's cramped.
- Keep the spacing scale consistent so every surface feels like one design system.

## 📊 The Student Usage Tracker (v2.11.0)

`USAGE_MODES` / `usageMode` / `_sut` / `sutRender` / `sutVisible` / `sutByMode` /
`sutExportCsv` (in `app.js`, search `THE STUDENT USAGE TRACKER`), plus the
`#studentDetailOverlay` and the `.sut-*` CSS in `index.html`. Opened by clicking
a student anywhere on the Usage page. **All four portals carry the same block —
keep them in step**; only `ATTEMPTS_COL` and the mode table differ.

Every question one student has completed, the result they got, and the **mode**
they did it in. The attempt log was always being written; what was missing was a
way to READ it. The old drill-in listed the rows and nothing else, so a teacher
looking at four hundred attempts could not answer either of the two questions
they actually have — *what has this child been doing?* and *how are they getting
on in it?* A list that can only be scrolled is a list nobody reads.

- **`USAGE_MODES` is the ONE place a raw mode string becomes words.** The log
  stores `quickpractice-open`, `snapmark-open`, `gap-generated` — internal names,
  not English. The chip, the breakdown, the filter dropdown and the CSV all read
  that map, so they cannot drift apart. A mode with **no entry still shows**, as
  its own raw string in the `other` group, rather than being dropped or folded
  into "Unknown": an unlabelled mode is a missing label, but a question dropped
  out of the log because nobody wrote a label for its mode is a **missing
  question**, and two unlabelled modes merged into one row is a breakdown that
  lies.
- **A GENERATED question needs its label more than any other row.** A
  learning-gap retry is never saved to the bank, so `sutQuestionMeta` can never
  resolve a title for it — without `gap-generated` / `retry-generated` in the
  table, a teacher reads a row called "Question a7f3…" and has no idea what the
  child did.
- **The breakdown BY MODE is the headline, not the log.** "43 in Quick Practice
  at 71%, 12 gap retries at 50%" is what a teacher opened this for; the
  row-by-row log is the evidence underneath it. Practice modes sort ahead of
  everything else, so the real schoolwork is read before the AI's stand-ins for
  it, even when there are more of those.
- **It renders from state.** `_sut` holds the attempts and the filters and
  `sutRender()` paints the whole overlay from them, so changing a filter never
  re-reads Firestore. `closeStudentDetail` clears `_sut.uid`, which is also what
  makes a reply from a superseded load harmless.
- **`sutVisible()` is the ONE place the window is decided**, and the count, the
  table, the breakdown and the CSV all read it. A CSV holding more rows than the
  table it came from is a teacher sending a parent a report of work in a mode
  they had filtered away.
- **The verdict threshold is the app-wide ≥0.95** that `progressOnMarked` and
  `lgNoteWin` already use, and `sutCredit` is FRACTIONAL — a half-marks open
  answer is **part right**, its own verdict, never rounded into a pass or a fail.
- **The title and topic are resolved from the BANK at read time**
  (`sutQuestionMeta`), not trusted from the attempt: an edited question would
  otherwise wear its old title in the log forever. A question **deleted since**
  is marked *removed from the bank* and keeps its row — the work was still done.
- It reads `ATTEMPTS_COL`, never a spelled-out collection name — see **Where the
  data lives**. It is otherwise **READ-ONLY**: nothing in the block writes
  anything anywhere.
- Run **`node tools/usage-tracker-tests.mjs`** after touching any of it.

## The clone stamp shows what it is about to stamp (vv2.9.0)

`_annotClonePeekSrc` / `_annotUpdateClonePeek` / `ANNOT_PEEK_MIN` and the
`#annotClonePeek` canvas inside `#annotBrushRing` (search `The clone stamp's
live preview`).

The source pin says where the copy comes FROM and the brush ring says how big
the mark will be. Neither says what the mark will BE, so lining a stamp up
meant clicking and then looking at what landed — and undoing it when it was
half a letter out. **The ring is now filled with the patch that would be
stamped this instant**: a lens on the source, carried under the pointer, at the
same zoom as everything else.

- **It lives INSIDE the ring**, so it is positioned, sized and hidden by exactly
  the code that already does all three for the ring. `_annotUpdateBrushRing` is
  still the ONE place either of them moves.
- **The source point is different before and during a stroke, and getting that
  backwards is the silent failure.** Before the first dab there is no offset, so
  starting the drag here is what would put the source POINT under the pointer —
  the preview is centred on `cloneSrc`. Mid-stroke the offset was locked in at
  pointer-down, so it is `(pointer in image px) − cloneOff`, which drifts away
  from the mark at the speed of the hand if it is computed the other way round.
- **`_annot.ptr` is in STAGE coordinates and the source is in IMAGE pixels**, so
  zoom and pan come off first. Read it raw and the preview is right only at 100%
  with no panning — which is how the editor opens, and therefore how anyone
  would check it by hand.
- **Mid-stroke it reads `cloneSnap`, not the live canvas** — the stamp reads the
  frozen snapshot, so dragging back over ground already covered would otherwise
  preview the copy instead of the source, and the two diverge exactly where it
  matters.
- The backing store is the brush in **image** pixels, so the preview is
  pixel-for-pixel what the dab puts down however far the view is zoomed; under
  `ANNOT_PEEK_MIN` (14) screen px there is nothing to see in the ring and it is
  not drawn. The ring goes white-on-black while it is previewing — a black
  hairline over arbitrary artwork is the one thing that disappears.
- Run **`node tools/clone-preview-tests.mjs`** after touching any of it.

## ✨ Regenerate — say what you want and the AI redraws it (vv2.9.0)

`annotAiRegen` / `_annotAiBarInit` / `_annotAiSyncScope` / `_annotSelBox` /
`ANNOT_AI_KEEP` (search `REGENERATE`), plus the `#annotAiBar` under the
selection bar in the Touch up editor.

AI content-aware fill answers exactly ONE question — *take this out* — with a
prompt nobody can change. Everything else an author actually wants of a picture
("rub out the pencil marks", "make the arrow red", "redraw this beaker
cleanly", "put the missing axis label back") had **no door at all**. This is
that door: a line to type in, and the same image model behind it.

- **TWO SCOPES, and the difference between them is the whole safety story.**
  With an area SELECTED only that area may change: the model is shown the
  picture with the area **RINGED rather than blanked** — "make the arrow red"
  needs the arrow still visible, which is exactly what content-aware fill's
  magenta blanking destroys — and the reply is composited back through
  `_annotWithSelClip`, so a model that quietly rewrote the whole page cannot
  touch one pixel outside the selection. With NOTHING selected the whole picture
  is redrawn, which is the honest reading of "no area chosen".
- **The bar NAMES the scope it is about to use** (`_annotAiSyncScope`, kicked
  from `_annotSelSyncBar`), because those two are very different things to press
  a button on.
- **The magenta marker is drawn just OUTSIDE the selection**, so it never covers
  the content the instruction is about — and anything of it that survives into
  the reply is outside the clip and therefore cannot be composited back.
- **It is ONE history step either way**, so ↶ Undo puts the original back. That
  is what makes an experimental prompt cheap enough to actually experiment with.
- The whole-picture branch **clears the canvas and draws**, never a `'copy'`
  composite: a canvas stranded in a composite mode erases everything drawn
  afterwards (the same trap `_annotResetCompose` exists for).
- `_annotAiBarInit` runs on every open, so **last picture's instruction is never
  left sitting in the box** one Enter away from being run on this one.

## House rules
- After touching **the Student Usage Tracker** (`USAGE_MODES`, `usageMode`,
  `sutCredit`, `sutVerdict`, `sutQuestionMeta`, `sutVisible`, `sutByMode`,
  `sutExportCsv`), run `node tools/usage-tracker-tests.mjs`. Every failure here
  is silent and a teacher acts on it: a mode that falls out of the log is a
  child's work made invisible, a verdict threshold that drifts from the app-wide
  0.95 makes the tracker and the progress counters disagree about the same
  answer with nothing to say which is lying, and an export that reads a
  different window from the table it came from sends a parent a report of work
  in a mode the teacher had filtered away.
- After touching **the clone stamp's live preview** (`_annotClonePeekSrc`,
  `_annotUpdateClonePeek`, `ANNOT_PEEK_MIN`, `_annotUpdateBrushRing`), run
  `node tools/clone-preview-tests.mjs`. A preview that does not appear is
  obvious the first time anyone picks the tool; a preview centred on the WRONG
  source point looks exactly like a working one and aims every stamp a little
  way off — which is worse than the pin-and-guess it replaced.

- After editing `app.js`, validate it:
  `cp app.js /tmp/c.mjs && node --check /tmp/c.mjs` (the `.mjs` copy makes Node
  parse it as a module, so `import` at the top is accepted).
- **The Gemini model is `AI_MODEL` and its thinking floor is `AI_THINK_MIN`, and
  the two move TOGETHER** (v1.2.0). Every model has its own thinking scale, and a
  level it does not know is a **400 INVALID_ARGUMENT on every AI call in the
  app** — not a degraded answer, no answer at all. `gemini-3.7-flash` takes
  `low` / `medium` / `high` and **dropped the `"minimal"` 3.6 accepted**, exactly
  as 3.x had already dropped 2.x's numeric `thinkingBudget`. So the floor is a
  named constant used at every call site rather than a string typed out in three
  places, and swapping the model means checking its scale first. The Science app
  (`polymathlc/cer`) carries the same pair — keep the two in step.
- Run the twenty-two harnesses after touching what they cover — every failure
  they catch is **silent**, with nothing thrown and nothing wrong on screen:
  - `node tools/answer-key-tests.mjs`
  - `node tools/check-questions-tests.mjs`
  - `node tools/part-marker-tests.mjs` — the doubled part marker. Both
    directions are silent: too timid and every AI-built sub-question prints its
    letter twice ("(a) (a) 文中形容…"), too eager and it eats the front of the
    question — "（见图一）文中形容…" opens with a bracket and is prose, and a
    block labelled (b) whose text opens "(a)" is a disagreement somebody should
    see rather than have tidied away.
  - `node tools/duplicate-warning-tests.mjs` — the duplicate warning. It fails
    silently in both directions and the app works perfectly either way: too
    tight and it never fires (a question re-read off the same paper is never
    worded byte-for-byte the same), too loose and it fires on every save, which
    makes it a warning nobody reads and lets the real duplicate through behind
    it. It also pins that the VETTING list is searched — the commonest
    duplicate of all is the same screenshot read twice in one sitting, and both
    copies are then in vetting where a bank-only search sees neither.
  - `node tools/vetting-bulk-delete-tests.mjs` — clearing the vetting list.
    This is the most destructive button in the app and every way it can go
    wrong is silent: 🗑 Delete all reading `vettingList` instead of the
    VISIBLE set destroys the questions the author had filtered away and never
    saw, and a question dropped from the list on a delete the database refused
    leaves a page that looks tidy and a question that is back at the next
    sign-in.
  - `node tools/usage-tracker-tests.mjs`
  - `node tools/objective-tag-tests.mjs`
  - `node tools/learning-gap-tests.mjs`
  - `node tools/question-persistence-tests.mjs` — whether a question the author
    was told was saved actually exists. The order of a move (write the
    destination, wait, then delete the source), `_firestoreSafeQuestion` on both
    save doors, and the stash that holds a failed write until it can be retried.
    This is the one failure with nothing on screen to see at all: the question
    is in the bank, in the count and in the search until the tab closes, and
    gone at the next sign-in with no error ever shown.
  - `node tools/bin-tests.mjs` — the bin's calendar and stored record, plus the
    `_firestoreSafeQuestion` helper every save shares. A day counted wrong
    purges somebody's question early, in a background sweep, with nothing on
    screen; a field lost on the way in is a question that comes back broken a
    week later with nothing left to compare it against.
  - `node tools/bank-isolation-tests.mjs` — that this app cannot reach another
    subject's question bank. Three portals share one project and one uid, and
    the only thing keeping their banks apart is the NAME of each collection, so
    this checks the shape of every path in the file. It is a test rather than a
    comment because the failure it guards has already happened once and did not
    look like a failure: the wrong subject's questions on the bank page, which
    reads as a filter bug.
  - `node tools/pinyin-ime-tests.mjs` — the input method's candidate ORDER, the
    word segmenter, and the Chinese-aware blank tokenizer. A candidate list in
    the wrong order is the wrong character typed into a question and saved. A
    tokenizer that splits on whitespace makes a whole Chinese passage ONE chip,
    so clicking a word blanks the entire paragraph; `\\W` as the punctuation
    edge eats the word instead and leaves `课外[[]]` — an empty blank in a
    passage that reads perfectly.
  - `node tools/wordmatch-tests.mjs` — 词语搭配: which NUMBER each item is
    keyed to, which end of the item the bracket is printed at, and that an
    unkeyed item stays unkeyed. The number comes from the word's position in
    the paper's table, so an order or an off-by-one read wrong keys every item
    to a different word than the class is told — on a page that renders,
    prints and marks without a murmur. It also pins the two silent structural
    ones: a table missing one of its own answers (a question that cannot be
    answered at all) and a print path falling through to the student
    rendering, which hands out the exercise already filled in.
  - `node tools/clozemcq-tests.mjs` — 短文填空: which option each blank is keyed
    to, that an unticked blank is never given an invented answer, that the
    printed worksheet gives none of them away, and that the key numbers from the
    PAPER's first number (16) rather than from 1. Also the student's drop-down —
    an empty choice worth `""` reads as option (1) and marks an unanswered blank
    against a word nobody picked, and a drop-down nothing listens to renders,
    opens and records nothing at all.
  - `node tools/word-help-tests.mjs` — which OPTION each of the model's answers
    is about. Line them up wrong and the popout still opens, still looks right
    and still reads fluently, while telling a child that "reluctantly" cannot be
    used because it is an adjective.
  - `node tools/synthesis-tests.mjs` — the rubric the sentence-rewrite marker
    is given, and the printed opening being put back before marking. Lose the
    rubric and a correct rewrite worded differently from the model answer is
    marked wrong; lose the prefix and the marker judges a fragment.
  - `node tools/ai-parts-tests.mjs` — the `"part"` the AI puts on a block, and
    that the typed-marker pass leaves it alone. Drop it and a comprehension page
    is eight option lists in a row with nothing telling them apart, on a screen
    that still looks right.
  - `node tools/passage-cloze-tests.mjs` — the passage builder's parse, the
    cloze's word bank, and the part lettering both rest on. A passage split
    one line early swallows the first option list; a question number read off a
    quantity cuts the passage in half; a full-width `（1）` read as a question
    turns every option list into four questions; a bank that does not contain
    one of its own answers renders and prints perfectly and is unanswerable.
  - `node tools/rapid-split-tests.mjs` — how many questions a page holds, and
    the full-width numbering strip that guards it. Split a 短文填空 and its
    blanks lose the passage they are about; fail to split a 语文应用 page of
    five and four questions are silently thrown away, leaving one row in vetting
    that looks perfectly fine.
  - `node tools/written-answer-tests.mjs` — 阅读理解问答: what each question is
    worth, and WHICH IMAGE the marker is told is whose. The image order and the
    note that numbers it must agree, or one part is marked against another
    part's handwriting — a wrong mark, delivered fluently. A weight defaulting
    to anything but 1 scores the whole existing bank out of zero.
  - `node tools/underline-tests.mjs` — 画线词语. The paper underlines the word a
    汉语拼音 question is about and the four options are that word's pinyin, so
    an underline lost in transcription — or kept on screen and stripped by the
    print builder — leaves a question that reads perfectly and cannot be
    answered, with four plausible options and no word attached to them.
  - `node tools/subject-level-tests.mjs` — the subject switcher's four links and
    ⚡ Rapid add's batch level. A url pointing at the wrong folder does not
    error, it loads the WRONG subject's app, and `../science/` is a 404 for the
    whole school (the folder is `cer`). An absolute url is the same failure
    delayed until the centre moves domain. And the batch level has no field to
    check itself against — a level is read off the TOPIC here, so if the
    narrowing stops working the picker still says "filed at P5", the toast
    still says "at P5", and forty questions land wherever the AI's topic put
    them.

### Two CSS traps in `index.html`

- **`.confirm-dialog` is declared LATE** and sets `max-width: 400px`, `padding`
  and `text-align: center`. A new dialog variant that only adds a second class
  earlier in the file silently loses all three. Use `.confirm-dialog.your-variant`
  (both classes) for anything that clashes.
- **Tailwind's preflight sets `appearance: none` on form controls**, so a bare
  `<input type="radio">`/`checkbox` renders as an invisible white box. Set
  `appearance: auto` (plus `-webkit-`) on any you add, or draw your own.
- **A `<button>` does not inherit `color`** the way a div does — it falls back to
  the browser's own button text. Any card-shaped button must set
  `color: var(--text)` itself, or its child text is invisible on a dark surface.

## The fork

This repo was created from `polymathlc/english`, which was itself created from
`polymathlc/cer` by removing the game layer:
the RPG hero, the dungeon, the arcade, the Realm of Embers trading-card game,
Ember Duel / Siege / Legends, Science Strike, the game leaderboards, points,
packs, prizes and game credits — about 20,000 lines of `app.js` and 1,200 CSS
rules. What replaced the hero doc is the small **Learner progress** store above.

Do not port the games back. A fix copied across from either sibling needs three
things checked every time, because all three are silent when wrong:

1. **Collection names.** All three apps live in one Firebase project under the
   same `users/{uid}` tree. See **Where the data lives** — a path pasted from
   the English repo writes Chinese questions into the English bank and works
   perfectly while doing it.
2. **Topics.** A different `topicLevelMap` / `SYLLABUS_LO_TOPICS`, sharing no
   entry with either sibling's.
3. **Language.** Anything with a prompt in it — the AI rules live in
   `ZH_PROMPT_RULES`, and a prompt copied across arrives asking for English.

The **Textbooks** page is also absent: it embedded a file of Science content with
no Chinese equivalent.
