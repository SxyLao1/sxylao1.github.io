'use strict';
const siteName = '𝒮𝓍𝓎ℒ𝒶ℴ𝓁';
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
let lightboxZoom = 1;
let lightboxPan = { x: 0, y: 0 };
const lightboxPointers = new Map();
let pinchDistance = 0;
let pinchZoom = 1;
const LIGHTBOX_MAX_ZOOM = 5;

// Preserve links shared before the original five-page structure was restored.
if (page === 'index') {
  const oldLinks = { '#about': 'about.html', '#notes': 'blog.html', '#blog': 'blog.html', '#gallery': 'album.html', '#album': 'album.html', '#contact': 'join.html', '#join': 'join.html' };
  if (oldLinks[location.hash]) location.replace(oldLinks[location.hash]);
}
if (page === 'about') {
  const reflections = { '#self-cultivation': 'thought-self-cultivation.html', '#acceptance': 'thought-from-solving-to-observing.html' };
  if (reflections[location.hash]) location.replace(reflections[location.hash]);
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
  const items = catalog.collections.blog?.items || catalog.collections.notes.items.slice(0, 6);
  $('#homePosts').innerHTML = items.map((item, index) => `<a class="home-post" href="${escapeHtml(item.url || 'blog.html')}"><span class="post-no">${String(index + 1).padStart(2, '0')}</span><div><h3>${escapeHtml(titleOf(item))}</h3><p>${escapeHtml(item.category || '笔记')} · ${escapeHtml(item.modifiedAt || 'MYNOTE')} · 阅读全文</p></div><span class="post-arrow" aria-hidden="true">↗</span></a>`).join('');
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
  $('#notesList').innerHTML = filtered.map((item, index) => `<a class="article-row" href="${escapeHtml(item.url || 'blog.html')}" aria-label="阅读：${escapeHtml(titleOf(item))}"><span class="post-no">${String(index + 1).padStart(2, '0')}</span><div><h2>${escapeHtml(titleOf(item))}</h2>${item.summary ? `<p class="article-summary">${escapeHtml(item.summary)}</p>` : ''}<p>${escapeHtml(item.folder || item.category || '笔记')}${item.modifiedAt ? `<span aria-hidden="true"> · </span>${escapeHtml(item.modifiedAt)}` : ''}${item.status ? `<span aria-hidden="true"> · </span>${escapeHtml(item.status)}` : ''}</p></div><span class="article-type">阅读全文 ↗</span></a>`).join('') || '<div class="empty-state"><strong>还没有找到这篇笔记</strong><p>换个关键词，或选择“全部笔记”再看看。</p></div>';
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
function lightboxSource(item) {
  return item.original || item.preview;
}
function lightboxFileName(item) {
  const source = lightboxSource(item).split('?')[0];
  const sourceName = source.slice(source.lastIndexOf('/') + 1) || 'image';
  const extension = sourceName.match(/\.[^.]+$/)?.[0] || '';
  const name = (item.name || sourceName).replace(/[\\/:*?"<>|]/g, '_');
  return name.replace(/\.(?:jpe?g|png|webp|gif|avif)$/i, '') + extension;
}
function clampLightboxPan() {
  const viewport = $('#lightboxViewport');
  if (!viewport || lightboxZoom <= 1) { lightboxPan = { x: 0, y: 0 }; return; }
  const image = $('#lightboxImage');
  const width = image.offsetWidth || viewport.clientWidth;
  const height = image.offsetHeight || viewport.clientHeight;
  const maxX = Math.max(0, (width * lightboxZoom - viewport.clientWidth) / 2);
  const maxY = Math.max(0, (height * lightboxZoom - viewport.clientHeight) / 2);
  lightboxPan.x = Math.max(-maxX, Math.min(maxX, lightboxPan.x));
  lightboxPan.y = Math.max(-maxY, Math.min(maxY, lightboxPan.y));
}
function paintLightboxTransform() {
  const image = $('#lightboxImage');
  if (!image) return;
  clampLightboxPan();
  image.style.transform = `translate(${lightboxPan.x}px, ${lightboxPan.y}px) scale(${lightboxZoom})`;
  image.style.cursor = lightboxZoom > 1 ? 'grab' : 'zoom-in';
  const value = $('#lightboxZoomValue');
  if (value) value.textContent = `${Math.round(lightboxZoom * 100)}%`;
  const zoomOut = $('#lightboxZoomOut');
  if (zoomOut) zoomOut.disabled = lightboxZoom <= 1;
  const zoomIn = $('#lightboxZoomIn');
  if (zoomIn) zoomIn.disabled = lightboxZoom >= LIGHTBOX_MAX_ZOOM;
}
function setLightboxZoom(zoom) {
  lightboxZoom = Math.max(1, Math.min(LIGHTBOX_MAX_ZOOM, zoom));
  paintLightboxTransform();
}
function resetLightboxView() {
  lightboxZoom = 1;
  lightboxPan = { x: 0, y: 0 };
  lightboxPointers.clear();
  pinchDistance = 0;
  paintLightboxTransform();
}
function updateLightbox() {
  const item = lightboxItems[lightboxIndex];
  const image = $('#lightboxImage');
  image.src = lightboxSource(item);
  image.draggable = false;
  $('#lightboxImage').alt = titleOf(item);
  $('#lightboxCaption').textContent = titleOf(item);
  $('#lightboxCount').textContent = `${lightboxIndex + 1} / ${lightboxItems.length}`;
  const download = $('#lightboxDownload');
  if (download) { download.href = lightboxSource(item); download.download = lightboxFileName(item); }
  resetLightboxView();
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
  $('#lightboxZoomOut')?.addEventListener('click', () => setLightboxZoom(lightboxZoom - 0.25));
  $('#lightboxZoomIn')?.addEventListener('click', () => setLightboxZoom(lightboxZoom + 0.25));
  $('#lightboxReset')?.addEventListener('click', resetLightboxView);
  const viewport = $('#lightboxViewport');
  const pointerDistance = () => {
    const points = [...lightboxPointers.values()];
    return points.length < 2 ? 0 : Math.hypot(points[0].x - points[1].x, points[0].y - points[1].y);
  };
  viewport?.addEventListener('wheel', (event) => {
    event.preventDefault();
    setLightboxZoom(lightboxZoom + (event.deltaY < 0 ? 0.25 : -0.25));
  }, { passive: false });
  viewport?.addEventListener('dblclick', () => setLightboxZoom(lightboxZoom > 1 ? 1 : 2));
  viewport?.addEventListener('pointerdown', (event) => {
    if (event.pointerType === 'mouse' && event.button !== 0) return;
    lightboxPointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    viewport.setPointerCapture?.(event.pointerId);
    if (lightboxPointers.size === 2) { pinchDistance = pointerDistance(); pinchZoom = lightboxZoom; }
  });
  viewport?.addEventListener('pointermove', (event) => {
    const previous = lightboxPointers.get(event.pointerId);
    if (!previous) return;
    const next = { x: event.clientX, y: event.clientY };
    lightboxPointers.set(event.pointerId, next);
    if (lightboxPointers.size === 1 && lightboxZoom > 1) {
      lightboxPan.x += next.x - previous.x; lightboxPan.y += next.y - previous.y; paintLightboxTransform();
    } else if (lightboxPointers.size === 2 && pinchDistance) {
      setLightboxZoom(pinchZoom * pointerDistance() / pinchDistance);
    }
    event.preventDefault();
  });
  const endPointer = (event) => { lightboxPointers.delete(event.pointerId); if (lightboxPointers.size < 2) pinchDistance = 0; };
  viewport?.addEventListener('pointerup', endPointer);
  viewport?.addEventListener('pointercancel', endPointer);
  viewport?.addEventListener('lostpointercapture', endPointer);
  $('#lightbox').addEventListener('click', (event) => {
    if (event.target === $('#lightbox')) $('#lightbox').close();
  });
  $('#lightbox').addEventListener('close', () => { document.body.style.overflow = ''; resetLightboxView(); });
  document.addEventListener('keydown', (event) => {
    if (!$('#lightbox').open) return;
    if (event.target?.closest?.('.lightbox-tools')) return;
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
