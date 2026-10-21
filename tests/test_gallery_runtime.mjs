import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = await readFile(path.join(repo, 'dist', 'app.js'), 'utf8');

class Element {
  constructor(id = '') { this.id = id; this.style = {}; this.listeners = new Map(); this.hidden = false; this.open = false; this.disabled = false; this.clientWidth = 400; this.clientHeight = 300; }
  addEventListener(type, listener) { this.listeners.set(type, listener); }
  emit(type, event = {}) { this.listeners.get(type)?.({ target: this, preventDefault() { this.defaultPrevented = true; }, ...event }); }
  showModal() { this.open = true; }
  close() { this.open = false; this.emit('close'); }
  setAttribute() {}
  closest() { return null; }
}

function galleryEnvironment() {
  const ids = ['themeToggle', 'lightbox', 'lightboxImage', 'lightboxCaption', 'lightboxCount', 'lightboxClose', 'lightboxPrev', 'lightboxNext', 'lightboxViewport', 'lightboxZoomOut', 'lightboxZoomIn', 'lightboxReset', 'lightboxZoomValue', 'lightboxDownload'];
  const elements = new Map(ids.map((id) => [id, new Element(id)]));
  const documentListeners = new Map();
  const document = {
    body: { dataset: { page: 'album' }, style: {}, classList: { toggle() {}, contains: () => false } },
    querySelector: (selector) => elements.get(selector.slice(1)) || null,
    querySelectorAll: () => [],
    addEventListener: (type, listener) => documentListeners.set(type, listener),
  };
  const context = vm.createContext({
    document, location: { hash: '', href: 'https://test/album.html', search: '' }, history: { replaceState() {} }, URL, URLSearchParams, Intl,
    fetch: () => new Promise(() => {}), localStorage: { getItem: () => null, setItem() {} }, console,
  });
  vm.runInContext(`${source}\nglobalThis.__galleryTest = { openImageGroup, moveLightbox };`, context, { filename: 'dist/app.js' });
  return { elements, documentListeners, api: context.__galleryTest };
}

test('lightbox prefers original, creates a same-origin download, zooms and resets on navigation', () => {
  const { elements, api } = galleryEnvironment();
  const first = { preview: 'images/preview.jpg', original: 'images/original.png', name: 'picture.png' };
  const second = { preview: 'images/second.jpg', name: 'second.jpg' };
  api.openImageGroup([first, second], 0);
  assert.equal(elements.get('lightboxImage').src, first.original);
  assert.equal(elements.get('lightboxImage').draggable, false);
  assert.equal(elements.get('lightboxDownload').href, first.original);
  assert.equal(elements.get('lightboxDownload').download, 'picture.png');
  elements.get('lightboxZoomIn').emit('click');
  assert.equal(elements.get('lightboxZoomValue').textContent, '125%');
  elements.get('lightboxViewport').emit('pointerdown', { pointerId: 1, clientX: 40, clientY: 40 });
  elements.get('lightboxViewport').emit('pointermove', { pointerId: 1, clientX: 80, clientY: 60 });
  assert.match(elements.get('lightboxImage').style.transform, /translate\(40px, 20px\) scale\(1.25\)/);
  api.moveLightbox(1);
  assert.equal(elements.get('lightboxImage').src, second.preview);
  assert.equal(elements.get('lightboxZoomValue').textContent, '100%');
  assert.match(elements.get('lightboxImage').style.transform, /translate\(0px, 0px\) scale\(1\)/);
});

test('lightbox wheel and double-click change scale, while tool keyboard focus does not navigate', () => {
  const { elements, documentListeners, api } = galleryEnvironment();
  api.openImageGroup([{ preview: 'one.jpg', name: 'one.jpg' }, { preview: 'two.jpg', name: 'two.jpg' }], 0);
  elements.get('lightboxViewport').emit('wheel', { deltaY: -1 });
  assert.equal(elements.get('lightboxZoomValue').textContent, '125%');
  elements.get('lightboxViewport').emit('dblclick');
  assert.equal(elements.get('lightboxZoomValue').textContent, '100%');
  const tool = new Element('tool'); tool.closest = (selector) => selector === '.lightbox-tools' ? tool : null;
  documentListeners.get('keydown')({ key: 'ArrowRight', target: tool, preventDefault() {} });
  assert.equal(elements.get('lightboxImage').src, 'one.jpg');
  documentListeners.get('keydown')({ key: 'ArrowRight', target: new Element('outside'), preventDefault() {} });
  assert.equal(elements.get('lightboxImage').src, 'two.jpg');
});

test('pinch scales the image, panning stays inside bounds, and downloads keep the actual extension', () => {
  const { elements, api } = galleryEnvironment();
  api.openImageGroup([{ preview: 'preview.webp', original: 'original.png', name: 'photo.jpg' }], 0);
  assert.equal(elements.get('lightboxDownload').download, 'photo.png');
  const viewport = elements.get('lightboxViewport');
  viewport.emit('pointerdown', { pointerId: 1, clientX: 0, clientY: 0 });
  viewport.emit('pointerdown', { pointerId: 2, clientX: 100, clientY: 0 });
  viewport.emit('pointermove', { pointerId: 2, clientX: 200, clientY: 0 });
  assert.equal(elements.get('lightboxZoomValue').textContent, '200%');
  viewport.emit('pointerup', { pointerId: 2 });
  viewport.emit('pointermove', { pointerId: 1, clientX: 1000, clientY: 1000 });
  assert.match(elements.get('lightboxImage').style.transform, /translate\(200px, 150px\) scale\(2\)/);
  viewport.emit('lostpointercapture', { pointerId: 1 });
  viewport.emit('pointermove', { pointerId: 1, clientX: -1000, clientY: -1000 });
  assert.match(elements.get('lightboxImage').style.transform, /translate\(200px, 150px\) scale\(2\)/);
  elements.get('lightboxReset').emit('click');
  assert.equal(elements.get('lightboxZoomValue').textContent, '100%');
});
