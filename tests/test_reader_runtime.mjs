import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [articleSource, workerSource] = await Promise.all([
  readFile(path.join(repo, 'dist', 'article.js'), 'utf8'),
  readFile(path.join(repo, 'dist', 'article-search-worker.js'), 'utf8'),
]);
const tick = () => new Promise((resolve) => setImmediate(resolve));
const deferred = () => { let resolve; const promise = new Promise((done) => { resolve = done; }); return { promise, resolve }; };
const response = (payload, ok = true) => ({ ok, json: async () => payload });

class Element {
  constructor(id = '') {
    this.id = id; this.hidden = false; this.attributes = {}; this.dataset = {}; this.textContent = ''; this.value = ''; this.listeners = new Map(); this._innerHTML = '';
    const values = new Set(); this.classList = { add: (v) => values.add(v), remove: (v) => values.delete(v), contains: (v) => values.has(v) };
  }
  get innerHTML() { return this._innerHTML; }
  set innerHTML(value) { this._innerHTML = String(value); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  removeAttribute(name) { delete this.attributes[name]; }
  addEventListener(type, listener) { this.listeners.set(type, listener); }
  emit(type, event = {}) { this.listeners.get(type)?.({ target: this, preventDefault() {}, ...event }); }
  querySelectorAll() { return []; }
  querySelector() { return null; }
  getBoundingClientRect() { this.laidOut = true; return { width: 720, height: 900 }; }
  focus() { this.focused = true; }
  scrollIntoView() { this.scrolled = true; }
}

function article(slug = 'note') {
  return { slug, title: 'Fixture', category: '安全', summary: '', html: '<h1 id="h1">one</h1><pre><code>const needle = 1;</code></pre><h6 id="tail">tail</h6>', toc: [{ id: 'h1', text: 'One', level: 1 }, { id: 'h2', text: 'Two', level: 2 }, { id: 'h3', text: 'Three', level: 3 }, { id: 'h4', text: 'Four', level: 4 }, { id: 'h5', text: 'Five', level: 5 }, { id: 'tail', text: 'Tail', level: 6 }], searchUrl: `data/articles/${slug}/search.json` };
}

function makeReader({ id = 'note', hash = '', fetchImpl, frames = [] } = {}) {
  const ids = ['articleStatus', 'articleView', 'articleContent', 'articleSearch', 'articleSearchPanel', 'articleTitle', 'articleCategory', 'articleSummary', 'articleMeta', 'articleToc', 'articleDownload', 'articleSearchStatus', 'articleSearchResults', 'articleSearchClear'];
  const elements = new Map(ids.map((name) => [name, new Element(name)]));
  elements.set('tail', new Element('tail'));
  elements.get('articleView').hidden = true; elements.get('articleContent').hidden = true; elements.get('articleSearchPanel').hidden = true;
  const document = { title: '', head: { append() {} }, querySelector(selector) { return selector.startsWith('#') ? elements.get(selector.slice(1)) || null : null; }, querySelectorAll() { return []; }, getElementById(idValue) { return elements.get(idValue) || null; }, addEventListener() {}, createElement: () => new Element() };
  const location = { search: `?id=${id}`, hash, href: `https://test/article.html?id=${id}${hash}` };
  const context = vm.createContext({ document, location, history: { replaceState() {} }, URLSearchParams, URL, fetch: fetchImpl, siteName: 'test', escapeHtml: String, setTimeout: (fn) => { frames.push(fn); return frames.length; }, clearTimeout() {}, requestAnimationFrame: (fn) => { frames.push(fn); return frames.length; }, navigator: { clipboard: { writeText: async () => {} } }, console, AbortController });
  context.window = new Element('window');
  vm.runInContext(articleSource, context, { filename: 'dist/article.js' });
  return { context, elements, frames, flush: async () => { while (frames.length) { frames.shift()(); await tick(); } } };
}

test('reader fetches one complete article, prepares before reveal, and honors a tail fragment', async () => {
  const calls = []; const payload = deferred();
  const env = makeReader({ hash: '#tail', fetchImpl: (url) => { calls.push(url); return payload.promise; } });
  assert.equal(env.elements.get('articleView').hidden, true);
  await env.flush(); assert.deepEqual(calls, ['data/articles/note.json']);
  payload.resolve(response(article())); await tick();
  const stepFrame = async () => { env.frames.shift()(); await tick(); };
  await stepFrame(); await stepFrame();
  assert.equal(env.elements.get('articleView').hidden, false, 'full document enters the layout tree before reveal');
  assert.equal(env.elements.get('articleView').classList.contains('is-preparing'), true, 'loader stays visible during preparation');
  assert.equal(env.elements.get('articleStatus').hidden, false);
  await env.flush();
  assert.equal(env.elements.get('articleView').hidden, false);
  assert.equal(env.elements.get('articleView').classList.contains('is-preparing'), false, 'preparing class is removed only after layout');
  assert.equal(env.elements.get('articleStatus').hidden, true); assert.equal(env.elements.get('articleContent').hidden, false); assert.equal(env.elements.get('articleContent').laidOut, true);
  assert.equal(env.elements.get('tail').scrolled, true, 'tail fragment scrolls only after preparation');
  assert.match(env.elements.get('articleToc').innerHTML, /toc-level-1/); assert.match(env.elements.get('articleToc').innerHTML, /toc-level-6/);
  assert.match(env.elements.get('articleToc').innerHTML, /One<\/a><ol><li class="toc-level-2">/);
  assert.equal(calls.length, 1, 'no chapter or search resource is fetched during article load');
});

test('table of contents and full-text results jump inside the loaded document without fetching it again', async () => {
  const calls = [];
  const env = makeReader({ fetchImpl: async (url) => {
    calls.push(url);
    return response(url.endsWith('/search.json') ? { slug: 'note', entries: [{ headingId: 'tail', text: 'needle in tail' }] } : article());
  } });
  await env.flush();
  const tocLink = { dataset: { heading: 'tail' }, closest: () => tocLink };
  env.elements.get('articleToc').emit('click', { target: tocLink });
  assert.equal(env.elements.get('tail').scrolled, true);
  assert.deepEqual(calls, ['data/articles/note.json']);
  env.elements.get('articleSearch').value = 'needle';
  env.elements.get('articleSearch').emit('input');
  await env.flush();
  assert.match(env.elements.get('articleSearchResults').innerHTML, /needle/);
  const result = { dataset: { searchResult: '0' }, closest: () => result };
  env.elements.get('articleSearchResults').emit('click', { target: result });
  assert.deepEqual(calls, ['data/articles/note.json', 'data/articles/note/search.json']);
  assert.equal(env.elements.get('articleContent').innerHTML, article().html);
});

test('reader shows retry for unavailable data and never fetches an invalid slug', async () => {
  let invalidFetches = 0;
  const invalid = makeReader({ id: '../bad', fetchImpl: () => { invalidFetches += 1; } });
  await invalid.flush(); assert.equal(invalidFetches, 0); assert.equal(invalid.elements.get('articleStatus').hidden, false);
  const unavailable = makeReader({ fetchImpl: async () => response(null, false) });
  await unavailable.flush(); assert.equal(unavailable.elements.get('articleView').hidden, true); assert.match(unavailable.elements.get('articleStatus').innerHTML, /articleRetry/);
});

test('search worker finds full-note tail/code text, caches its index, and suppresses stale queries', async () => {
  const index = deferred(); const posted = []; let fetches = 0; const self = { postMessage: (message) => posted.push(message) };
  const context = vm.createContext({ self, fetch: () => { fetches += 1; return index.promise; } }); vm.runInContext(workerSource, context, { filename: 'dist/article-search-worker.js' });
  const base = { type: 'search', slug: 'note', url: 'data/articles/note/search.json' };
  const old = self.onmessage({ data: { ...base, requestId: 1, query: 'old' } }); const fresh = self.onmessage({ data: { ...base, requestId: 2, query: 'needle' } });
  index.resolve(response({ slug: 'note', entries: [{ headingId: 'tail', text: 'tail has needle' }, { headingId: 'code', text: 'const needle = 1;' }] })); await Promise.all([old, fresh]);
  assert.equal(fetches, 1); assert.equal(posted.length, 1); assert.equal(posted[0].requestId, 2); assert.equal(posted[0].total, 2);
  await self.onmessage({ data: { ...base, requestId: 3, query: 'const' } }); assert.equal(fetches, 1, 'first search index is cached'); assert.equal(posted.at(-1).results[0].headingId, 'code'); assert.equal(Object.hasOwn(posted.at(-1).results[0], 'chapterIndex'), false);
});
