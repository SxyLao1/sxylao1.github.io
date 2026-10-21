'use strict';

const articleId = new URLSearchParams(location.search).get('id') || '';
const articleStatus = document.querySelector('#articleStatus');
const articleView = document.querySelector('#articleView');
const articleContent = document.querySelector('#articleContent');
const searchInput = document.querySelector('#articleSearch');
const searchPanel = document.querySelector('#articleSearchPanel');
let articleData;
let currentChapter = -1;
let renderVersion = 0;
let retryArticle = null;
let searchVersion = 0;
let searchTimer;
let searchWorker;
let workerUnavailable = false;
let fallbackIndex;
let searchResults = [];
const chapterCache = new Map();
let mathRendererPromise;

const paint = () => new Promise((resolve) => {
  if (typeof requestAnimationFrame === 'function') requestAnimationFrame(() => requestAnimationFrame(resolve));
  else setTimeout(resolve, 0);
});

function spinner(message) {
  return '<span class="reader-spinner" aria-hidden="true"></span><p>' + escapeHtml(message) + '</p>';
}

function setReadingBusy(message) {
  const target = articleView.hidden ? articleStatus : document.querySelector('#chapterLoading');
  target.hidden = false;
  target.setAttribute('role', 'status');
  target.innerHTML = spinner(message);
  articleContent.hidden = true;
  articleView.setAttribute('aria-busy', 'true');
}

function showArticleError(retry) {
  retryArticle = retry;
  articleView.hidden = true;
  articleStatus.hidden = false;
  articleStatus.setAttribute('role', 'alert');
  articleStatus.innerHTML = '<span class="eyebrow">FROM THE NOTEBOOK</span><h1>笔记暂时没有打开。</h1><p>可以重试，或回到博客继续翻翻。</p><div class="reader-error-actions">' + (retry ? '<button type="button" id="articleRetry">重新加载</button>' : '') + '<a class="text-link" href="blog.html">返回博客 ↗</a></div>';
}

async function readJSON(url) {
  const controller = typeof AbortController === 'function' ? new AbortController() : null;
  const timeout = controller ? setTimeout(() => controller.abort(), 30000) : null;
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

function chapterForHeading(id) {
  if (!articleData?.chapters?.length) return 0;
  const index = articleData.chapters.findIndex((chapter) => chapter.id === id || chapter.headingIds.includes(id));
  return index < 0 ? 0 : index;
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
  const walker = document.createTreeWalker(articleContent, NodeFilter.SHOW_TEXT);
  const nodes = [];
  let node;
  while ((node = walker.nextNode())) {
    if (!node.parentElement?.closest('button,.math,.katex,mark') && node.textContent.toLowerCase().includes(query.toLowerCase())) nodes.push(node);
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
  const heading = headingId ? document.getElementById(headingId) : null;
  const marks = [...articleContent.querySelectorAll('mark.reader-hit')];
  const selected = marks.find((mark) => !heading || heading.contains(mark) || (heading.compareDocumentPosition(mark) & 4)) || marks[0];
  selected?.scrollIntoView({ block: 'center' });
}

function updateChapterControls(index, headingId) {
  const chapters = articleData.chapters || [];
  document.querySelector('#chapterControls').hidden = !chapters.length;
  const bottom = document.querySelector('#chapterBottom');
  if (bottom) bottom.hidden = !chapters.length;
  if (!chapters.length) return;
  document.querySelector('#chapterSelect').value = String(index);
  document.querySelector('#chapterPrev').disabled = index === 0;
  document.querySelector('#chapterNext').disabled = index === chapters.length - 1;
  document.querySelector('#chapterPosition').textContent = '第 ' + (index + 1) + ' / ' + chapters.length + ' 节';
  const bottomPrev = document.querySelector('#chapterPrevBottom');
  const bottomNext = document.querySelector('#chapterNextBottom');
  const bottomPosition = document.querySelector('#chapterBottomPosition');
  if (bottomPrev) bottomPrev.disabled = index === 0;
  if (bottomNext) bottomNext.disabled = index === chapters.length - 1;
  if (bottomPosition) bottomPosition.textContent = '第 ' + (index + 1) + ' / ' + chapters.length + ' 节';
  const selectedHeading = chapters[index].headingIds.includes(headingId) ? headingId : chapters[index].headingIds[0];
  document.querySelectorAll('#articleToc a').forEach((link) => {
    if (link.dataset.heading === selectedHeading) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}

async function displayChapter(index, { headingId = '', share = false, query = '' } = {}) {
  const version = ++renderVersion;
  try {
    const chapters = articleData.chapters || [];
    if (chapters.length && (!Number.isInteger(index) || index < 0 || index >= chapters.length)) throw new Error('Unknown chapter');
    setReadingBusy(chapters.length ? '正在打开这一节…' : '正在准备笔记…');
    await paint();
    let html = articleData.html;
    if (chapters.length) {
      const chapter = chapters[index];
      if (!new RegExp('^data/articles/' + articleId + '/chapter-\\d+\\.json$').test(chapter.url)) throw new Error('Invalid chapter path');
      if (!chapterCache.has(chapter.id)) {
        const payload = await readJSON(chapter.url);
        if (payload.slug !== articleId || payload.chapterId !== chapter.id || typeof payload.html !== 'string') throw new Error('Invalid chapter');
        chapterCache.set(chapter.id, payload.html);
      }
      html = chapterCache.get(chapter.id);
    }
    if (version !== renderVersion) return;
    setReadingBusy('正在排版文字与公式…');
    await paint();
    if (version !== renderVersion) return;
    // Only the current, build-time compiled chapter enters the DOM.
    articleContent.innerHTML = html;
    if (!await prepareContent(version)) return;
    currentChapter = index;
    updateChapterControls(index, headingId);
    articleStatus.hidden = true;
    document.querySelector('#chapterLoading').hidden = true;
    articleContent.hidden = false;
    articleView.hidden = false;
    articleView.setAttribute('aria-busy', 'false');
    const shareId = headingId || chapters[index]?.id || '';
    if (share && shareId) history.replaceState(null, '', '?id=' + articleId + '#' + encodeURIComponent(shareId));
    await paint();
    if (version !== renderVersion) return;
    if (headingId) (document.getElementById(headingId) || document.querySelector('#chapterControls')).scrollIntoView({ block: 'start' });
    else if (index > 0) document.querySelector('#chapterControls').scrollIntoView({ block: 'start' });
    markQuery(query, headingId);
  } catch {
    if (version === renderVersion) showArticleError(() => displayChapter(index, { headingId, share, query }));
  }
}

function moveChapter(index) {
  const headingId = articleData.chapters[index]?.headingIds[0] || articleData.chapters[index]?.id || '';
  return displayChapter(index, { headingId, share: true });
}

async function loadArticle() {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(articleId)) { showArticleError(null); return; }
  try {
    setReadingBusy('正在读取笔记…');
    await paint();
    const data = await readJSON('data/articles/' + articleId + '.json');
    if (data.slug !== articleId || typeof data.html !== 'string' || !Array.isArray(data.toc) || (data.chapters && !Array.isArray(data.chapters))) throw new Error('Invalid article');
    articleData = data;
    document.title = data.title + ' · ' + siteName;
    document.querySelector('#articleTitle').textContent = data.title;
    document.querySelector('#articleCategory').textContent = data.category || 'FROM THE NOTEBOOK';
    document.querySelector('#articleSummary').textContent = data.summary || '';
    document.querySelector('#articleMeta').textContent = [data.modifiedAt, (data.readingMinutes || 1) + ' 分钟阅读', data.status].filter(Boolean).join(' · ');
    document.querySelector('#articleToc').innerHTML = data.toc.length ? '<ol>' + data.toc.map((entry) => '<li class="toc-level-' + ([1, 2, 3].includes(entry.level) ? entry.level : 2) + '"><a href="#' + encodeURIComponent(entry.id) + '" data-heading="' + escapeHtml(entry.id) + '" data-chapter="' + (entry.chapterIndex || 0) + '">' + escapeHtml(entry.text) + '</a></li>').join('') + '</ol>' : '<a href="#articleTitle">文章开头</a>';
    document.querySelector('#chapterSelect').innerHTML = (data.chapters || []).map((chapter, index) => '<option value="' + index + '">' + (index + 1) + '. ' + escapeHtml(chapter.title) + '</option>').join('');
    const download = document.querySelector('#articleDownload');
    download.href = 'articles/' + articleId + '.md';
    download.setAttribute('download', articleId + '.md');
    const id = fragment();
    await displayChapter(chapterForHeading(id), { headingId: id });
  } catch { showArticleError(loadArticle); }
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
    const title = heading?.text || articleData.chapters?.[result.chapterIndex]?.title || articleData.title;
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
        if (results.length < 60) results.push({ chapterIndex: entry.chapterIndex, headingId: entry.headingId, snippet: entry.text.slice(Math.max(0, at - 65), at + query.length + 105) });
      }
      await paint();
    }
    acceptSearchResults({ requestId, total, results, type: 'results' });
  } catch { acceptSearchResults({ requestId, type: 'error' }); }
}

function runSearch(requestId, query) {
  if (!articleData?.searchUrl || articleData.searchUrl !== 'data/articles/' + articleId + '/search.json') return;
  showSearchResults('正在检索全部章节与代码…');
  document.querySelector('#articleSearchResults').innerHTML = '';
  if (!workerUnavailable && typeof Worker !== 'undefined') {
    try {
      if (!searchWorker) {
        searchWorker = new Worker('article-search-worker.js?v=20261022-experience');
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
document.querySelector('#chapterPrev').addEventListener('click', () => moveChapter(currentChapter - 1));
document.querySelector('#chapterNext').addEventListener('click', () => moveChapter(currentChapter + 1));
document.querySelector('#chapterPrevBottom')?.addEventListener('click', () => moveChapter(currentChapter - 1));
document.querySelector('#chapterNextBottom')?.addEventListener('click', () => moveChapter(currentChapter + 1));
document.querySelector('#chapterSelect').addEventListener('change', (event) => moveChapter(Number(event.target.value)));
document.querySelector('#articleToc').addEventListener('click', (event) => {
  const link = event.target.closest('a[data-heading]');
  if (!link) return;
  event.preventDefault();
  displayChapter(Number(link.dataset.chapter), { headingId: link.dataset.heading, share: true });
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
  showSearchResults('准备检索全部章节…');
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
  displayChapter(result.chapterIndex, { headingId: result.headingId, share: true, query: searchInput.value.trim() });
});
document.addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); searchInput.focus(); }
  if (event.key === 'Escape') searchPanel.hidden = true;
});
window.addEventListener('hashchange', () => {
  if (!articleData) return;
  const id = fragment();
  const next = chapterForHeading(id);
  if (next !== currentChapter) displayChapter(next, { headingId: id });
  else document.getElementById(id)?.scrollIntoView({ block: 'start' });
});

loadArticle();
