import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [articleSource, workerSource] = await Promise.all([
  readFile(path.join(repo, 'dist/article.js'), 'utf8'),
  readFile(path.join(repo, 'dist/article-search-worker.js'), 'utf8'),
]);

const tick = () => new Promise((resolve) => setImmediate(resolve));
const deferred = () => { let resolve; const promise = new Promise((done) => { resolve = done; }); return { promise, resolve }; };
const response = (payload, ok = true) => ({ ok, json: async () => payload });

class Element {
  constructor(id = '') {
    this.id = id; this.hidden = false; this.attributes = {}; this.dataset = {}; this.children = [];
    this.className = ''; this.textContent = ''; this.value = ''; this.disabled = false; this.listeners = new Map();
    this.classList = { contains: () => false }; this._innerHTML = '';
  }
  get innerHTML() { return this._innerHTML; }
  set innerHTML(value) { this._innerHTML = String(value); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  removeAttribute(name) { delete this.attributes[name]; }
  addEventListener(type, listener) { this.listeners.set(type, listener); }
  emit(type, target = this) { this.listeners.get(type)?.({ target, preventDefault() {} }); }
  querySelectorAll() { return []; }
  querySelector() { return null; }
  append() {}
  focus() { this.focused = true; }
  scrollIntoView() { this.scrolled = true; }
}

function makeReader({ id = 'note', hash = '', fetchImpl, frames = [] } = {}) {
  const ids = ['articleStatus', 'articleView', 'articleContent', 'articleSearch', 'articleSearchPanel', 'chapterLoading', 'articleTitle', 'articleCategory', 'articleSummary', 'articleMeta', 'articleToc', 'chapterSelect', 'articleDownload', 'chapterControls', 'chapterPrev', 'chapterNext', 'chapterPosition', 'chapterBottom', 'chapterPrevBottom', 'chapterNextBottom', 'chapterBottomPosition', 'articleSearchStatus', 'articleSearchResults', 'articleSearchClear'];
  const elements = new Map(ids.map((name) => [name, new Element(name)]));
  elements.get('articleView').hidden = true;
  elements.get('articleContent').hidden = true;
  elements.get('chapterLoading').hidden = true;
  elements.get('articleSearchPanel').hidden = true;
  const document = {
    title: '',
    querySelector(selector) { return selector.startsWith('#') ? elements.get(selector.slice(1)) || null : null; },
    querySelectorAll(selector) { return selector === '#articleToc a' ? elements.get('articleToc').children : []; },
    getElementById(name) { return elements.get(name) || null; },
    addEventListener() {},
    createElement: () => new Element(),
  };
  const location = { search: `?id=${id}`, hash, href: `https://test/article.html?id=${id}${hash}` };
  const context = vm.createContext({
    document, location, history: { replaceState() {} }, URLSearchParams, URL, fetch: fetchImpl,
    siteName: 'test', escapeHtml: (value) => String(value), setTimeout: (fn) => { frames.push(fn); return frames.length; }, clearTimeout() {},
    requestAnimationFrame: (fn) => { frames.push(fn); return frames.length; }, navigator: { clipboard: { writeText: async () => {} } }, console,
  });
  context.window = new Element('window');
  vm.runInContext(articleSource, context, { filename: 'dist/article.js' });
  return { context, elements, frames, flush: async () => { while (frames.length) { frames.shift()(); await tick(); } } };
}

function metadata(slug = 'note') {
  return { slug, title: 'Fixture', category: '安全', summary: '', toc: [{ id: 'first', text: 'First', level: 2, chapterIndex: 0 }, { id: 'last', text: 'Last', level: 2, chapterIndex: 1 }], html: '', chapters: [{ id: 'chapter-1', title: 'One', url: `data/articles/${slug}/chapter-1.json`, headingIds: ['first'] }, { id: 'chapter-2', title: 'Two', url: `data/articles/${slug}/chapter-2.json`, headingIds: ['last'] }], searchUrl: `data/articles/${slug}/search.json` };
}

test('chapter reader fetches metadata then only selected chapter, and exposes after layout', async () => {
  const calls = []; const meta = deferred(); const chapter = deferred();
  const env = makeReader({ fetchImpl: (url) => { calls.push(url); return url.endsWith('.json') && !url.includes('chapter-') ? meta.promise : chapter.promise; } });
  assert.equal(env.elements.get('articleView').hidden, true, 'view remains hidden during initial paint');
  await env.flush();
  assert.deepEqual(calls, ['data/articles/note.json']);
  meta.resolve(response(metadata())); await tick(); await env.flush();
  assert.deepEqual(calls, ['data/articles/note.json', 'data/articles/note/chapter-1.json']);
  assert.equal(env.elements.get('articleView').hidden, true, 'chapter content is still gated while fetching/layout runs');
  chapter.resolve(response({ slug: 'note', chapterId: 'chapter-1', html: '<h2 id="first">first</h2>' })); await tick(); await env.flush();
  assert.equal(env.elements.get('articleView').hidden, false);
  assert.equal(env.elements.get('articleContent').hidden, false);
  assert.equal(env.elements.get('chapterLoading').hidden, true);
  assert.equal(calls.includes('data/articles/note/search.json'), false, 'search index stays lazy');
  assert.equal(calls.includes('data/articles/note/chapter-2.json'), false, 'other chapters stay lazy');
});

test('fragment and controls request the correct chapter; stale chapter response cannot win', async () => {
  const calls = []; const pending = new Map();
  const env = makeReader({ hash: '#last', fetchImpl: (url) => { calls.push(url); const item = deferred(); pending.set(url, item); return item.promise; } });
  await env.flush(); pending.get('data/articles/note.json').resolve(response(metadata())); await tick(); await env.flush();
  assert.deepEqual(calls, ['data/articles/note.json', 'data/articles/note/chapter-2.json'], 'last heading starts at its chapter');
  env.context.location.hash = '#first';
  env.context.window.emit('hashchange');
  await tick(); await env.flush();
  assert.ok(calls.includes('data/articles/note/chapter-1.json'));
  pending.get('data/articles/note/chapter-2.json').resolve(response({ slug: 'note', chapterId: 'chapter-2', html: 'STALE' })); await tick(); await env.flush();
  assert.notEqual(env.elements.get('articleContent').innerHTML, 'STALE', 'late response from prior chapter is ignored');
  pending.get('data/articles/note/chapter-1.json').resolve(response({ slug: 'note', chapterId: 'chapter-1', html: 'ONE' })); await tick(); await env.flush();
  assert.equal(env.elements.get('articleContent').innerHTML, 'ONE');
});

test('bottom chapter navigation is lazy and chapter-id fragments reach unheaded chapters', async () => {
  const calls = []; const pending = new Map();
  const env = makeReader({ fetchImpl: (url) => { calls.push(url); const item = deferred(); pending.set(url, item); return item.promise; } });
  await env.flush();
  pending.get('data/articles/note.json').resolve(response(metadata())); await tick(); await env.flush();
  pending.get('data/articles/note/chapter-1.json').resolve(response({ slug: 'note', chapterId: 'chapter-1', html: 'ONE' })); await tick(); await env.flush();
  assert.equal(env.elements.get('chapterPrevBottom').disabled, true, 'first chapter has no previous chapter');
  assert.equal(env.elements.get('chapterNextBottom').disabled, false, 'first chapter can advance');
  env.elements.get('chapterNextBottom').emit('click'); await tick(); await env.flush();
  assert.equal(calls.at(-1), 'data/articles/note/chapter-2.json', 'bottom next fetches only the target chapter');

  const directCalls = []; const directPending = new Map();
  const direct = makeReader({ hash: '#chapter-2', fetchImpl: (url) => { directCalls.push(url); const item = deferred(); directPending.set(url, item); return item.promise; } });
  await direct.flush();
  directPending.get('data/articles/note.json').resolve(response(metadata())); await tick(); await direct.flush();
  assert.deepEqual(directCalls, ['data/articles/note.json', 'data/articles/note/chapter-2.json'], 'chapter id fragment loads an unheaded chapter directly');
});

test('invalid slug does not fetch and unavailable metadata offers a retry action', async () => {
  let fetches = 0;
  const invalid = makeReader({ id: '../bad', fetchImpl: () => { fetches += 1; } });
  await invalid.flush();
  assert.equal(fetches, 0);
  assert.equal(invalid.elements.get('articleStatus').hidden, false);
  const unavailable = makeReader({ fetchImpl: async () => response(null, false) });
  await unavailable.flush();
  assert.equal(unavailable.elements.get('articleStatus').hidden, false);
  assert.match(unavailable.elements.get('articleStatus').innerHTML, /articleRetry/);
});

test('search worker uses one cached index, finds tail and code entries, and suppresses old queries', async () => {
  const index = deferred(); const posted = []; let fetches = 0;
  const self = { postMessage: (message) => posted.push(message) };
  const context = vm.createContext({ self, fetch: () => { fetches += 1; return index.promise; } });
  vm.runInContext(workerSource, context, { filename: 'dist/article-search-worker.js' });
  const base = { type: 'search', slug: 'note', url: 'data/articles/note/search.json' };
  const old = self.onmessage({ data: { ...base, requestId: 1, query: 'old' } });
  const fresh = self.onmessage({ data: { ...base, requestId: 2, query: 'needle' } });
  index.resolve(response({ slug: 'note', entries: [{ chapterIndex: 1, headingId: 'last', text: 'tail has needle' }, { chapterIndex: 1, headingId: 'code', text: 'const needle = 1;' }] }));
  await Promise.all([old, fresh]);
  assert.equal(fetches, 1);
  assert.equal(posted.length, 1);
  assert.equal(posted[0].requestId, 2);
  assert.equal(posted[0].total, 2);
  await self.onmessage({ data: { ...base, requestId: 3, query: 'const' } });
  assert.equal(fetches, 1, 'cached index is reused');
  assert.equal(posted.at(-1).results[0].headingId, 'code');
});
