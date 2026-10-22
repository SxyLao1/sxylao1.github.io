'use strict';

const articleId = new URLSearchParams(location.search).get('id') || '';
const articleStatus = document.querySelector('#articleStatus');
const articleView = document.querySelector('#articleView');
const articleContent = document.querySelector('#articleContent');
const searchInput = document.querySelector('#articleSearch');
const searchPanel = document.querySelector('#articleSearchPanel');
let articleData;
let renderVersion = 0;
let retryArticle = null;
let searchVersion = 0;
let searchTimer;
let searchWorker;
let workerUnavailable = false;
let fallbackIndex;
let searchResults = [];
let mathRendererPromise;

const paint = () => new Promise((resolve) => {
  if (typeof requestAnimationFrame === 'function') requestAnimationFrame(() => requestAnimationFrame(resolve));
  else setTimeout(resolve, 0);
});

function spinner(message) {
  return '<span class="reader-spinner" aria-hidden="true"></span><p>' + escapeHtml(message) + '</p>';
}

function setReadingBusy(message) {
  articleStatus.hidden = false;
  articleStatus.classList.add('is-loading');
  articleStatus.setAttribute('role', 'status');
  articleStatus.innerHTML = spinner(message);
  articleView.setAttribute('aria-busy', 'true');
}

function showArticleError(retry) {
  retryArticle = retry;
  articleView.hidden = true;
  articleStatus.hidden = false;
  articleStatus.classList.remove('is-loading');
  articleStatus.setAttribute('role', 'alert');
  articleStatus.innerHTML = '<span class="eyebrow">FROM THE NOTEBOOK</span><h1>笔记暂时没有打开。</h1><p>可以重试，或回到博客继续翻翻。</p><div class="reader-error-actions">' + (retry ? '<button type="button" id="articleRetry">重新加载</button>' : '') + '<a class="text-link" href="blog.html">返回博客 ↗</a></div>';
}

async function readJSON(url) {
  const controller = typeof AbortController === 'function' ? new AbortController() : null;
  const timeout = controller ? setTimeout(() => controller.abort(), 120000) : null;
  try {
    const response = await fetch(url, { cache: 'no-cache', ...(controller ? { signal: controller.signal } : {}) });
    if (!response.ok) throw new Error('Reading resource unavailable');
    return await response.json();
  } finally { if (timeout !== null) clearTimeout(timeout); }
}

async function ensureMathRenderer() {
  if (typeof katex !== 'undefined') return true;
  if (!mathRendererPromise) mathRendererPromise = new Promise((resolve) => {
    const script = document.createElement('script');
    let finished = false;
    const finish = (ready) => {
      if (finished) return;
      finished = true;
      clearTimeout(timeout);
      if (!ready) mathRendererPromise = null;
      resolve(ready);
    };
    const timeout = setTimeout(() => finish(false), 15000);
    script.src = 'vendor/katex/katex.min.js';
    script.onload = () => finish(true);
    script.onerror = () => finish(false);
    document.head.append(script);
  });
  return mathRendererPromise;
}

function fragment() {
  try { return decodeURIComponent(location.hash.slice(1)); } catch { return ''; }
}

async function prepareContent(version) {
  const blocks = [...articleContent.querySelectorAll('pre')];
  for (let start = 0; start < blocks.length; start += 25) {
    for (const block of blocks.slice(start, start + 25)) {
      if (!block.querySelector('code') || block.querySelector('.code-copy')) continue;
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'code-copy';
      button.textContent = '复制';
      button.setAttribute('aria-label', '复制代码');
      block.append(button);
    }
    await paint();
    if (version !== renderVersion) return false;
  }
  const formulas = [...articleContent.querySelectorAll('.math')];
  if (formulas.length && await ensureMathRenderer()) {
    for (let start = 0; start < formulas.length; start += 4) {
      for (const node of formulas.slice(start, start + 4)) {
        try { katex.render(node.textContent, node, { displayMode: node.classList.contains('block'), throwOnError: false, trust: false, maxExpand: 1000 }); }
        catch { /* Keep unsupported formulas as their original LaTeX. */ }
      }
      await paint();
      if (version !== renderVersion) return false;
    }
  }
  return version === renderVersion;
}

function markQuery(query, headingId) {
  if (!query || typeof document.createTreeWalker !== 'function') return;
  for (const mark of articleContent.querySelectorAll('mark.reader-hit')) mark.replaceWith(document.createTextNode(mark.textContent));
  articleContent.normalize();
  const heading = headingId ? document.getElementById(headingId) : null;
  const walker = document.createTreeWalker(articleContent, NodeFilter.SHOW_TEXT);
  if (heading) walker.currentNode = heading;
  const nodes = [];
  let node;
  while ((node = walker.nextNode())) {
    const nextHeading = node.parentElement?.closest('h1,h2,h3,h4,h5,h6');
    if (heading && nextHeading && nextHeading !== heading) break;
    if (!node.parentElement?.closest('button,.math,.katex,mark') && node.textContent.toLowerCase().includes(query.toLowerCase())) nodes.push(node);
    if (nodes.length >= 120) break;
  }
  let count = 0;
  for (const textNode of nodes) {
    const text = textNode.textContent;
    const lower = text.toLowerCase();
    const part = document.createDocumentFragment();
    let from = 0;
    let at;
    while (count < 120 && (at = lower.indexOf(query.toLowerCase(), from)) !== -1) {
      part.append(document.createTextNode(text.slice(from, at)));
      const mark = document.createElement('mark');
      mark.className = 'reader-hit';
      mark.textContent = text.slice(at, at + query.length);
      part.append(mark);
      from = at + query.length;
      count += 1;
    }
    part.append(document.createTextNode(text.slice(from)));
    textNode.replaceWith(part);
    if (count >= 120) break;
  }
  const marks = [...articleContent.querySelectorAll('mark.reader-hit')];
  const selected = marks[0];
  selected?.scrollIntoView({ block: 'center' });
}

function jumpToHeading(headingId, { share = false, query = '' } = {}) {
  const heading = headingId ? document.getElementById(headingId) : document.querySelector('#articleTitle');
  heading?.scrollIntoView({ block: 'start' });
  document.querySelectorAll('#articleToc a').forEach((link) => {
    if (link.dataset.heading === headingId) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  if (share && headingId) history.replaceState(null, '', '?id=' + articleId + '#' + encodeURIComponent(headingId));
  markQuery(query, headingId);
}

function renderTableOfContents(toc) {
  const roots = [];
  const stack = [];
  for (const entry of toc) {
    const node = { ...entry, children: [] };
    while (stack.length && stack[stack.length - 1].level >= node.level) stack.pop();
    (stack.length ? stack[stack.length - 1].children : roots).push(node);
    stack.push(node);
  }
  const list = (nodes) => '<ol>' + nodes.map((node) => '<li class="toc-level-' + node.level + '"><a href="#' + encodeURIComponent(node.id) + '" data-heading="' + escapeHtml(node.id) + '">' + escapeHtml(node.text) + '</a>' + (node.children.length ? list(node.children) : '') + '</li>').join('') + '</ol>';
  return roots.length ? list(roots) : '<a href="#articleTitle">文章开头</a>';
}

async function loadArticle() {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(articleId)) { showArticleError(null); return; }
  const version = ++renderVersion;
  try {
    articleView.hidden = true;
    setReadingBusy('正在读取完整笔记…');
    await paint();
    const data = await readJSON('data/articles/' + articleId + '.json');
    if (version !== renderVersion) return;
    if (data.slug !== articleId || typeof data.html !== 'string' || !data.html.trim() || !Array.isArray(data.toc) || data.toc.some((entry) => !Number.isInteger(entry.level) || entry.level < 1 || entry.level > 6)) throw new Error('Invalid article');
    articleData = data;
    document.title = data.title + ' · ' + siteName;
    document.querySelector('#articleTitle').textContent = data.title;
    document.querySelector('#articleCategory').textContent = data.category || 'FROM THE NOTEBOOK';
    document.querySelector('#articleSummary').textContent = data.summary || '';
    document.querySelector('#articleMeta').textContent = [data.modifiedAt, (data.readingMinutes || 1) + ' 分钟阅读', data.status].filter(Boolean).join(' · ');
    document.querySelector('#articleToc').innerHTML = renderTableOfContents(data.toc);
    const download = document.querySelector('#articleDownload');
    download.href = 'articles/' + articleId + '.md';
    download.setAttribute('download', articleId + '.md');
    setReadingBusy('正在排版全文、代码与公式…');
    await paint();
    if (version !== renderVersion) return;
    // Lay out the complete document behind the loader before revealing it.
    articleView.classList.add('is-preparing');
    articleContent.innerHTML = data.html;
    articleContent.hidden = false;
    articleView.hidden = false;
    if (!await prepareContent(version)) return;
    articleContent.getBoundingClientRect();
    jumpToHeading(fragment());
    await paint();
    if (version !== renderVersion) return;
    articleView.classList.remove('is-preparing');
    articleView.setAttribute('aria-busy', 'false');
    articleStatus.hidden = true;
    articleStatus.classList.remove('is-loading');
  } catch { if (version === renderVersion) showArticleError(loadArticle); }
}

function snippetHTML(text, query) {
  const at = text.toLowerCase().indexOf(query.toLowerCase());
  if (at < 0) return escapeHtml(text);
  return escapeHtml(text.slice(0, at)) + '<mark>' + escapeHtml(text.slice(at, at + query.length)) + '</mark>' + escapeHtml(text.slice(at + query.length));
}

function showSearchResults(message) {
  searchPanel.hidden = false;
  document.querySelector('#articleSearchStatus').textContent = message;
}

function acceptSearchResults(data) {
  if (data.requestId !== searchVersion) return;
  if (data.type === 'error') { showSearchResults('全文索引暂时没有加载成功，请重新输入试试。'); return; }
  searchResults = data.results;
  const query = searchInput.value.trim();
  showSearchResults(data.total ? '找到 ' + data.total + ' 个匹配片段' + (data.total > data.results.length ? '，显示前 ' + data.results.length + ' 个' : '') : '没有找到匹配内容。');
  document.querySelector('#articleSearchResults').innerHTML = data.results.map((result, index) => {
    const heading = articleData.toc.find((entry) => entry.id === result.headingId);
    const title = heading?.text || articleData.title;
    return '<button type="button" class="reader-search-result" data-search-result="' + index + '"><strong>' + escapeHtml(title) + '</strong><span>' + snippetHTML(result.snippet, query) + '</span></button>';
  }).join('');
}

async function fallbackSearch(requestId, query) {
  if (!query || requestId !== searchVersion) return;
  try {
    if (!fallbackIndex) fallbackIndex = await readJSON(articleData.searchUrl);
    if (fallbackIndex.slug !== articleId || !Array.isArray(fallbackIndex.entries)) throw new Error('Invalid search index');
    const results = [];
    let total = 0;
    for (let start = 0; start < fallbackIndex.entries.length; start += 80) {
      if (requestId !== searchVersion) return;
      for (const entry of fallbackIndex.entries.slice(start, start + 80)) {
        const at = entry.text.toLowerCase().indexOf(query.toLowerCase());
        if (at < 0) continue;
        total += 1;
        if (results.length < 60) results.push({ headingId: entry.headingId, snippet: entry.text.slice(Math.max(0, at - 65), at + query.length + 105) });
      }
      await paint();
    }
    acceptSearchResults({ requestId, total, results, type: 'results' });
  } catch { acceptSearchResults({ requestId, type: 'error' }); }
}

function runSearch(requestId, query) {
  if (!articleData?.searchUrl || articleData.searchUrl !== 'data/articles/' + articleId + '/search.json') return;
  showSearchResults('正在检索整篇笔记与代码…');
  document.querySelector('#articleSearchResults').innerHTML = '';
  if (!workerUnavailable && typeof Worker !== 'undefined') {
    try {
      if (!searchWorker) {
        searchWorker = new Worker('article-search-worker.js?v=20261022-fullnote');
        searchWorker.onmessage = (event) => acceptSearchResults(event.data);
        searchWorker.onerror = () => {
          workerUnavailable = true;
          searchWorker.terminate();
          searchWorker = null;
          fallbackSearch(searchVersion, searchInput.value.trim());
        };
      }
      searchWorker.postMessage({ type: 'search', requestId, slug: articleId, url: articleData.searchUrl, query });
      return;
    } catch { workerUnavailable = true; }
  }
  fallbackSearch(requestId, query);
}

articleStatus.addEventListener('click', (event) => { if (event.target.closest('#articleRetry')) retryArticle?.(); });
document.querySelector('#articleToc').addEventListener('click', (event) => {
  const link = event.target.closest('a[data-heading]');
  if (!link) return;
  event.preventDefault();
  jumpToHeading(link.dataset.heading, { share: true });
});
articleContent.addEventListener('click', async (event) => {
  const button = event.target.closest('.code-copy');
  if (!button) return;
  try { await navigator.clipboard.writeText(button.parentElement.querySelector('code').textContent); button.textContent = '已复制'; }
  catch { button.textContent = '请手动选择复制'; }
  setTimeout(() => { button.textContent = '复制'; }, 1800);
});
searchInput.addEventListener('input', () => {
  const requestId = ++searchVersion;
  clearTimeout(searchTimer);
  const query = searchInput.value.trim().slice(0, 80);
  searchResults = [];
  document.querySelector('#articleSearchResults').innerHTML = '';
  if (!query) { searchResults = []; searchPanel.hidden = true; return; }
  showSearchResults('准备检索整篇笔记…');
  searchTimer = setTimeout(() => runSearch(requestId, query), 220);
});
searchInput.addEventListener('focus', () => { if (searchResults.length && searchInput.value.trim()) searchPanel.hidden = false; });
document.querySelector('#articleSearchClear').addEventListener('click', () => {
  searchVersion += 1;
  clearTimeout(searchTimer);
  searchInput.value = '';
  searchResults = [];
  searchPanel.hidden = true;
  searchInput.focus();
});
document.querySelector('#articleSearchResults').addEventListener('click', (event) => {
  const button = event.target.closest('[data-search-result]');
  if (!button) return;
  const result = searchResults[Number(button.dataset.searchResult)];
  if (!result) return;
  searchPanel.hidden = true;
  jumpToHeading(result.headingId, { share: true, query: searchInput.value.trim() });
});
document.addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); searchInput.focus(); }
  if (event.key === 'Escape') searchPanel.hidden = true;
});
window.addEventListener('hashchange', () => {
  if (!articleData) return;
  if (!articleView.hidden && !articleView.classList.contains('is-preparing')) jumpToHeading(fragment());
});

loadArticle();
