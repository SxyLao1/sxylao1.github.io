'use strict';
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
const fmt = (value) => new Intl.NumberFormat('zh-CN').format(value);
const titleOf = (item) => item.title || item.name.replace(/\.[^.]+$/, '');
const page = document.body.dataset.page;
let catalog;
let noteFolder = 'all';
let galleryMode;
let galleryItems = [];
let lightboxItems = [];
let lightboxIndex = 0;

// Preserve links shared before the original five-page structure was restored.
if (page === 'index') {
  const oldLinks = { '#about': 'about.html', '#notes': 'blog.html', '#blog': 'blog.html', '#gallery': 'album.html', '#album': 'album.html', '#contact': 'join.html', '#join': 'join.html' };
  if (oldLinks[location.hash]) location.replace(oldLinks[location.hash]);
}

function savedTheme() {
  try { return localStorage.getItem('sxylao1-theme') || 'light'; } catch { return 'light'; }
}
function applyTheme(theme) {
  const dark = theme === 'dark';
  document.body.classList.toggle('dark', dark);
  $('#themeToggle').setAttribute('aria-pressed', String(dark));
  $('#themeToggle').setAttribute('aria-label', dark ? '切换浅色主题' : '切换深色主题');
}
applyTheme(savedTheme());
$('#themeToggle').addEventListener('click', () => {
  const next = document.body.classList.contains('dark') ? 'light' : 'dark';
  applyTheme(next);
  try { localStorage.setItem('sxylao1-theme', next); } catch { /* Theme still works when browser storage is unavailable. */ }
});

function renderHome() {
  const items = (catalog.collections.blog?.items || catalog.collections.notes.items).slice(0, 4);
  $('#homePosts').innerHTML = items.map((item, index) => `<a class="home-post" href="blog.html?q=${encodeURIComponent(item.name)}"><span class="post-no">${String(index + 1).padStart(2, '0')}</span><div><h3>${escapeHtml(titleOf(item))}</h3><p>${escapeHtml(item.category || '笔记')} · ${escapeHtml(item.modifiedAt || 'MYNOTE')} · 目录索引</p></div><span class="post-arrow" aria-hidden="true">↗</span></a>`).join('');
}

function selectFolder(path) {
  noteFolder = path;
  $$('.folder-button').forEach((button) => {
    const active = button.dataset.folder === path;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  renderNotes();
}
function renderFolders() {
  const notes = catalog.collections.notes;
  $('#folderRail').innerHTML = `<button class="folder-button active" data-folder="all" aria-pressed="true"><span>全部笔记</span><span>${fmt(notes.count)}</span></button>` + notes.folders.map((folder) => `<button class="folder-button" data-folder="${escapeHtml(folder.path)}" aria-pressed="false"><span>${escapeHtml(folder.name)}</span><span>${fmt(folder.markdownCount)}</span></button>`).join('');
  $$('.folder-button').forEach((button) => button.addEventListener('click', () => selectFolder(button.dataset.folder)));
}
function renderNotes() {
  const query = $('#noteSearch').value.trim().toLowerCase();
  const filtered = catalog.collections.notes.items.filter((item) => {
    const matchesFolder = noteFolder === 'all' || item.folder === noteFolder || item.path.startsWith(`${noteFolder}/`);
    const searchText = `${titleOf(item)} ${item.name} ${item.path} ${item.category || ''} ${item.summary || ''}`.toLowerCase();
    return matchesFolder && (!query || searchText.includes(query));
  });
  if ($('#noteSort').value === 'date') filtered.sort((a, b) => String(b.modifiedAt).localeCompare(String(a.modifiedAt)) || a.name.localeCompare(b.name, 'zh-CN'));
  else filtered.sort((a, b) => titleOf(a).localeCompare(titleOf(b), 'zh-CN'));
  $('#listTitle').textContent = query ? `搜索：${$('#noteSearch').value.trim()}` : noteFolder === 'all' ? '全部笔记' : noteFolder;
  $('#noteResultCount').textContent = `${fmt(filtered.length)} 篇`;
  $('#notesList').innerHTML = filtered.map((item, index) => `<article class="article-row"><span class="post-no">${String(index + 1).padStart(2, '0')}</span><div><h2>${escapeHtml(titleOf(item))}</h2>${item.summary ? `<p class="article-summary">${escapeHtml(item.summary)}</p>` : ''}<p>${escapeHtml(item.category || '笔记')}<span aria-hidden="true"> · </span>${escapeHtml(item.folder)}${item.modifiedAt ? `<span aria-hidden="true"> · </span>${escapeHtml(item.modifiedAt)}` : ''}${item.status ? `<span aria-hidden="true"> · </span>${escapeHtml(item.status)}` : ''}</p></div><span class="article-type">MD / 目录</span></article>`).join('') || '<div class="empty-state"><strong>还没有找到这篇笔记</strong><p>换个关键词，或选择“全部笔记”再看看。</p></div>';
}
function setupBlog() {
  renderFolders();
  const query = new URLSearchParams(location.search).get('q');
  if (query) $('#noteSearch').value = query;
  renderNotes();
  $('#noteSearch').addEventListener('input', renderNotes);
  $('#noteSort').addEventListener('change', renderNotes);
  document.addEventListener('keydown', (event) => {
    if (event.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
      event.preventDefault(); $('#noteSearch').focus();
    }
  });
}

function renderGalleryTags() {
  const tags = catalog.gallery.tags;
  $('#galleryTags').innerHTML = tags.map((tag) => `<button class="switch" type="button" data-gallery="${escapeHtml(tag.id)}" role="tab" aria-selected="false">${escapeHtml(tag.label)} <span>${fmt(tag.count)}</span></button>`).join('');
  $$('#galleryTags .switch').forEach((button) => button.addEventListener('click', () => {
    galleryMode = button.dataset.gallery;
    renderGallery();
    const url = new URL(location.href);
    url.searchParams.set('tag', galleryMode);
    history.replaceState(null, '', url);
  }));
}
function renderGallery() {
  const gallery = catalog.gallery;
  const tag = gallery.tags.find((entry) => entry.id === galleryMode) || gallery.tags.find((entry) => entry.id === gallery.defaultTag);
  galleryMode = tag.id;
  galleryItems = gallery.items.filter((item) => item.tags.includes(galleryMode));
  $('#galleryDescription').textContent = tag.description;
  $('#galleryCount').textContent = `${fmt(galleryItems.length)} 张图片`;
  $$('#galleryTags .switch').forEach((button) => {
    const active = button.dataset.gallery === galleryMode;
    button.classList.toggle('active', active);
    button.setAttribute('aria-selected', String(active));
    button.tabIndex = active ? 0 : -1;
  });
  $('#galleryGrid').innerHTML = galleryItems.map((item, index) => `<button class="photo-tile" type="button" data-index="${index}" aria-label="放大图片：${escapeHtml(titleOf(item))}"><img loading="${index < 8 ? 'eager' : 'lazy'}" src="${escapeHtml(item.preview)}" alt="${escapeHtml(titleOf(item))}" ${item.previewWidth && item.previewHeight ? `width="${item.previewWidth}" height="${item.previewHeight}"` : ''}><span class="photo-label">${escapeHtml(titleOf(item))}<br>${escapeHtml(tag.label)}</span></button>`).join('') || '<p class="empty-state">这个标签下还没有图片。</p>';
  $$('.photo-tile').forEach((button) => button.addEventListener('click', () => openLightbox(Number(button.dataset.index))));
}
function openImageGroup(items, index) {
  openLightbox(index, items);
}
function updateLightbox() {
  const item = lightboxItems[lightboxIndex];
  $('#lightboxImage').src = item.preview;
  $('#lightboxImage').alt = titleOf(item);
  $('#lightboxCaption').textContent = titleOf(item);
  $('#lightboxCount').textContent = `${lightboxIndex + 1} / ${lightboxItems.length}`;
}
function openLightbox(index, items = galleryItems) {
  if (!items.length) return;
  lightboxItems = items;
  lightboxIndex = index;
  updateLightbox();
  $('#lightbox').showModal();
  document.body.style.overflow = 'hidden';
}
function moveLightbox(delta) {
  lightboxIndex = (lightboxIndex + delta + lightboxItems.length) % lightboxItems.length;
  updateLightbox();
}
function setupAlbum() {
  const requestedTag = new URLSearchParams(location.search).get('tag');
  galleryMode = catalog.gallery.tags.some((tag) => tag.id === requestedTag) ? requestedTag : catalog.gallery.defaultTag;
  renderGalleryTags();
  renderGallery();
  const tabs = $$('#galleryTags .switch');
  tabs.forEach((tab, index) => tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
    tabs[next].focus(); tabs[next].click();
  }));
}

function setupLightbox() {
  $('#lightboxClose').addEventListener('click', () => $('#lightbox').close());
  $('#lightboxPrev').addEventListener('click', () => moveLightbox(-1));
  $('#lightboxNext').addEventListener('click', () => moveLightbox(1));
  $('#lightbox').addEventListener('click', (event) => {
    if (event.target === $('#lightbox')) $('#lightbox').close();
  });
  $('#lightbox').addEventListener('close', () => { document.body.style.overflow = ''; });
  document.addEventListener('keydown', (event) => {
    if (!$('#lightbox').open) return;
    if (event.key === 'ArrowLeft') { event.preventDefault(); moveLightbox(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); moveLightbox(1); }
  });
}
if (page === 'album') setupLightbox();

if (['index', 'blog', 'album'].includes(page)) {
  fetch('data/catalog.json', { cache: 'no-cache' })
    .then((response) => { if (!response.ok) throw new Error('Catalogue unavailable'); return response.json(); })
    .then((data) => {
      catalog = data;
      if (page === 'index') renderHome();
      if (page === 'blog') setupBlog();
      if (page === 'album') setupAlbum();
    })
    .catch(() => {
      const target = $('#homePosts') || $('#notesList') || $('#galleryGrid');
      if (target) target.innerHTML = '<div class="empty-state"><strong>目录暂时没有加载成功</strong><p>请刷新页面再试一次。</p></div>';
    });
}
