// Exercise the real settings migration, request bodies and provider dispatch.
// Run: node tools/model-defaults-tests.mjs
import assert from 'node:assert/strict';
import fs from 'node:fs';

const src = fs.readFileSync(new URL('../app.js', import.meta.url), 'utf8');
const html = fs.readFileSync(new URL('../index.html', import.meta.url), 'utf8');
function section(start, end) {
  const a = src.indexOf(start), b = src.indexOf(end, a);
  assert.ok(a >= 0 && b > a, `missing source section: ${start}`);
  return src.slice(a, b);
}
const settingsBlock = section('const AI_ENGINE_STORE =', '/* =====================================================================\n   ⚙️ THREE ROUTES');
function settings(initial = {}, unavailable = false) {
  return new Function('initial', 'unavailable', `
    const saved = new Map(Object.entries(initial)), requests = [];
    const localStorage = {
      getItem(k) { if (unavailable) throw new Error('storage unavailable'); return saved.get(k) || null; },
      setItem(k, v) { if (unavailable) throw new Error('storage unavailable'); saved.set(k, String(v)); },
      removeItem(k) { saved.delete(k); }
    };
    async function fetch(url, options) {
      requests.push({ url, ...options, body: JSON.parse(options.body) });
      return { ok: true, json: async () => ({ choices: [{ message: { content: '中文回答' } }] }) };
    }
    ${settingsBlock}
    return { saved, requests, getAiEngine, getOpenAiModel, askOpenAI, openAiReasoningEffort, store: AI_ENGINE_STORE };
  `)(initial, unavailable);
}

let count = 0;
function check(label, fn) { fn(); count++; console.log('  ok  ' + label); }
const fresh = settings();
check('new devices use OpenAI and GPT 6.1 Sol', () => {
  assert.equal(fresh.getAiEngine(), 'openai'); assert.equal(fresh.getOpenAiModel(), 'gpt-6.1-sol');
});
for (const old of ['gpt-6-astra', 'gpt-5.6-sol']) {
  check(`the saved ${old} default migrates`, () => {
    const s = settings({ zh_ai_engine: 'gemini', zh_openai_model: old, zh_openai_model_gen: 'astra' });
    assert.equal(s.getAiEngine(), 'openai'); assert.equal(s.getOpenAiModel(), 'gpt-6.1-sol');
  });
}
check('a marked manual engine and model survive migration', () => {
  const s = settings({ zh_ai_engine: 'gemini', zh_ai_engine_choice: 'manual', zh_openai_model: 'gpt-6-astra', zh_openai_model_choice: 'manual' });
  assert.equal(s.getAiEngine(), 'gemini'); assert.equal(s.getOpenAiModel(), 'gpt-6-astra');
});
check('a deliberate older model selected after migration survives reload', () => {
  const s = settings({ zh_openai_model_gen: 'sol61', zh_openai_model: 'gpt-6-astra' });
  assert.equal(s.getOpenAiModel(), 'gpt-6-astra');
});
check('storage failures still use the new defaults', () => {
  const s = settings({}, true); assert.equal(s.getAiEngine(), 'openai'); assert.equal(s.getOpenAiModel(), 'gpt-6.1-sol');
});

const media = [{ mimeType: 'image/png', data: 'picture-bytes' }, { mimeType: 'application/pdf', data: 'pdf-bytes' }];
await fresh.askOpenAI('Read the paper', media, { json: true, temperature: 0.2, maxOutputTokens: 2048, reasoningEffort: 'none' });
check('browser vision keeps image/PDF input and compatible reasoning fields', () => {
  const b = fresh.requests.at(-1).body;
  assert.equal(b.model, 'gpt-6.1-sol'); assert.equal(b.reasoning_effort, 'low');
  assert.equal(b.max_completion_tokens, 6144); assert.equal(b.response_format.type, 'json_object');
  assert.equal(b.messages[0].content[1].image_url.url, 'data:image/png;base64,picture-bytes');
  assert.equal(b.messages[0].content[2].file.file_data, 'data:application/pdf;base64,pdf-bytes');
  assert.match(b.messages[0].content.at(-1).text, /JSON/);
  for (const field of ['temperature', 'top_p', 'logprobs']) assert.ok(!(field in b));
});
await fresh.askOpenAI('Build a widget', null, { maxOutputTokens: 32768, reasoningEffort: 'high', exactOutputBudget: true });
check('explicit widget budgets retain their requested ceiling and effort', () => {
  assert.equal(fresh.requests.at(-1).body.reasoning_effort, 'high');
  assert.equal(fresh.requests.at(-1).body.max_completion_tokens, 32768);
});

const kimiBlock = section('const KIMI_API_BASE =', 'function _aiRun(');
const kimi = new Function(`
  const AI_ENGINE_STORE = { kimiKey: 'key', kimiModel: 'model' };
  let model = 'kimi-k3';
  const requests = [];
  const localStorage = { getItem(k) { return k === 'model' ? model : 'test-key'; } };
  async function fetch(url, options) {
    requests.push({ url, body: JSON.parse(options.body) });
    return { ok: true, json: async () => ({ choices: [{ message: { content: 'Kimi response' } }] }) };
  }
  ${kimiBlock}
  return { askKimiDirect, requests, setModel(value) { model = value; } };
`)();
await kimi.askKimiDirect('Read an image', media.slice(0, 1), { maxOutputTokens: 4096, temperature: 0.2, reasoningEffort: 'medium' });
check('Kimi K3 browser requests use its documented schema', () => {
  const b = kimi.requests.at(-1).body;
  assert.equal(b.model, 'kimi-k3'); assert.equal(b.max_completion_tokens, 4096);
  assert.equal(b.reasoning_effort, 'high');
  assert.equal(b.messages[0].content[1].image_url.url, 'data:image/png;base64,picture-bytes');
  for (const field of ['temperature', 'top_p', 'thinking', 'max_tokens']) assert.ok(!(field in b));
});
await kimi.askKimiDirect('Build a widget', null, { maxOutputTokens: 65536, temperature: 0.4, reasoningEffort: 'xhigh' });
check('Kimi K3 maps xhigh thinking to its supported max effort', () => assert.equal(kimi.requests.at(-1).body.reasoning_effort, 'max'));
kimi.setModel('moonshot-v1-8k');
await kimi.askKimiDirect('Text task', null, { maxOutputTokens: 2048, temperature: 0.3, reasoningEffort: 'high' });
check('deliberately selected older Moonshot models keep compatible requests', () => {
  const b = kimi.requests.at(-1).body;
  assert.equal(b.max_tokens, 2048); assert.equal(b.temperature, 0.3);
  assert.ok(!('max_completion_tokens' in b)); assert.ok(!('reasoning_effort' in b));
});

const routesBlock = section('const AI_DOWN_MS =', 'function aiRouteReport(');
const efforts = section('const WIDGET_EFFORTS =', 'let _widgetBusy =');
const widget = section('async function _widgetAskAI(', '// Pull the HTML document');
const vision = section('async function _askGeminiVisionRaw(', '// Convert text with');
const text = section('async function _askGeminiRaw(', '// Was the LAST');
function router({ failOpenAI = false, failGemini = false, emptyGemini = false, shared = {} } = {}) {
  return new Function('flags', `
    const calls = [], payloads = [];
    const console = { warn() {} }, document = { getElementById: () => null }, window = {};
    const AI_THINK_MIN = 'low', AI_ENGINE_STORE = { kimiKey: 'k', kimiModel: 'm' }, app = {}, db = {}, CONFIG_COL = 'zhConfig';
    const localStorage = { getItem: () => '', setItem() {}, removeItem() {} };
    function getAiEngine() { return 'openai'; }
    function getOpenAiKey() { return ''; }
    function getOpenAiModel() { return 'gpt-6.1-sol'; }
    function openAiReasoningEffort(v) { return ['low', 'medium', 'high', 'xhigh', 'max'].includes(v) ? v : 'low'; }
    function getFunctions() { return {}; }
    function httpsCallable(_f, name) { return async payload => {
      calls.push(name); payloads.push(payload);
      if (name === 'askOpenAi' && flags.failOpenAI) throw new Error('OpenAI quota');
      return { data: { text: name === 'askOpenAi' ? 'Sol response' : 'Kimi response' } };
    }; }
    async function askOpenAI() { throw new Error('no local key'); }
    const geminiModel = { async generateContent(payload) {
      calls.push('gemini'); payloads.push(payload);
      if (flags.failGemini) throw new Error('Gemini quota');
      return { response: { text: () => flags.emptyGemini ? '' : 'Gemini response' } };
    } };
    function doc() { return {}; }
    async function getDoc() { return { exists: () => true, data: () => flags.shared }; }
    function onSnapshot() { return () => {}; }
    function renderAiEngineStatus() {}
    function _zhPrompt(p) { return 'CHINESE RULES\\n' + p; }
    ${routesBlock}
    ${efforts}
    ${widget}
    ${vision}
    ${text}
    return { calls, payloads, aiEngineOrder, aiSharedPreference, aiEngineLoadShared, _askGeminiRaw, _askGeminiVisionRaw, _widgetAskAI, get last() { return aiLastCall; } };
  `)({ failOpenAI, failGemini, emptyGemini, shared });
}
const primary = router();
check('fresh server-first order has both backup providers', () => assert.deepEqual(primary.aiEngineOrder(), ['openai', 'gemini', 'kimi']));
await primary._askGeminiRaw('Text task', {});
await primary._askGeminiVisionRaw('Read photo', media, { json: true });
check('text and vision dispatch to GPT 6.1 Sol on the server', () => {
  assert.deepEqual(primary.calls, ['askOpenAi', 'askOpenAi']);
  assert.equal(primary.payloads[1].model, 'gpt-6.1-sol');
  assert.deepEqual(primary.payloads[1].media, media);
});
const secondary = router({ failOpenAI: true });
assert.equal(await secondary._askGeminiVisionRaw('Read photo', media, {}), 'Gemini response');
check('OpenAI failure reaches Gemini with the same media', () => {
  assert.deepEqual(secondary.calls, ['askOpenAi', 'gemini']);
  assert.deepEqual(secondary.payloads[1].contents[0].parts.slice(1).map(p => p.inlineData), media);
  assert.equal(secondary.last.engine, 'gemini'); assert.equal(secondary.last.fellBack, true);
});
const tertiary = router({ failOpenAI: true, failGemini: true });
assert.equal(await tertiary._askGeminiVisionRaw('Read photo', media.slice(0, 1), {}), 'Kimi response');
check('two provider failures reach Kimi with image data intact', () => {
  assert.deepEqual(tertiary.calls, ['askOpenAi', 'gemini', 'askKimi']);
  assert.deepEqual(tertiary.payloads[2].media, media.slice(0, 1));
});
const empty = router({ failOpenAI: true, emptyGemini: true });
assert.equal(await empty._askGeminiRaw('Text task', {}), 'Kimi response');
check('empty Gemini output triggers the final backup', () => assert.equal(empty.last.engine, 'kimi'));
check('untouched shared defaults migrate while recorded choices remain', () => {
  assert.equal(primary.aiSharedPreference({}), 'openai');
  assert.equal(primary.aiSharedPreference({ aiEngine: 'gemini' }), 'openai');
  assert.equal(primary.aiSharedPreference({ aiEngine: 'gemini', aiEngineBy: 'teacher@example.com' }), 'gemini');
  assert.equal(primary.aiSharedPreference({ aiEngine: 'kimi' }), 'kimi');
});
const shared = router({ shared: { aiEngine: 'gemini', aiEngineAt: '2026-09-01' } });
await shared.aiEngineLoadShared(true);
check('the actual shared load follows deliberate administrator overrides', () => assert.equal(shared.aiEngineOrder()[0], 'gemini'));
const thinking = router();
await thinking._widgetAskAI('auto', 'high', 'Build learning widget');
check('widgets use the server without a browser key and preserve thinking depth', () => {
  assert.deepEqual(thinking.calls, ['askOpenAi']);
  assert.equal(thinking.payloads[0].reasoningEffort, 'high');
  assert.equal(thinking.payloads[0].exactOutputBudget, true);
  assert.equal(thinking.payloads[0].maxOutputTokens, 32768);
  assert.match(thinking.payloads[0].prompt, /^CHINESE RULES/);
});
const widgetBackup = router({ failOpenAI: true, failGemini: true });
assert.equal(await widgetBackup._widgetAskAI('auto', 'pro', 'Build learning widget'), 'Kimi response');
check('thinking widgets reach Kimi after both primary providers fail', () => {
  assert.deepEqual(widgetBackup.calls, ['askOpenAi', 'gemini', 'askKimi']);
  assert.equal(widgetBackup.payloads[0].reasoningEffort, 'max');
  assert.equal(widgetBackup.payloads[1].generationConfig.thinkingConfig.thinkingLevel, 'high');
  assert.equal(widgetBackup.payloads[2].reasoningEffort, 'max');
});
check('the chooser and new widgets expose the defaults without demanding local keys', () => {
  assert.match(html, /value="gpt-6\.1-sol" selected/);
  assert.match(html, /value="openai" checked/);
  assert.match(src, /block\.engine = 'auto'/);
  const editor = section('function renderWidgetBlockEditor(', 'function _widgetQuestionContext(');
  assert.doesNotMatch(editor, /hasKey|add key in AI Engine/);
});
console.log(`\n${count} model-default checks passed`);
