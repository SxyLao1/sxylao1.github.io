'use strict';

let indexPromise;
let activeRequest = 0;

async function loadIndex(url) {
  const controller = typeof AbortController === 'function' ? new AbortController() : null;
  const timeout = controller ? setTimeout(() => controller.abort(), 30000) : null;
  try {
    const response = await fetch(url, { cache: 'no-cache', ...(controller ? { signal: controller.signal } : {}) });
    if (!response.ok) throw new Error('Index unavailable');
    return await response.json();
  } finally { if (timeout !== null) clearTimeout(timeout); }
}

self.onmessage = async ({ data }) => {
  if (data.type !== 'search' || typeof data.query !== 'string') return;
  activeRequest = data.requestId;
  const query = data.query.trim().slice(0, 80).toLowerCase();
  if (!query) return;
  try {
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(data.slug) || data.url !== `data/articles/${data.slug}/search.json`) throw new Error('Invalid index path');
    if (!indexPromise) indexPromise = loadIndex(data.url);
    const index = await indexPromise;
    if (index.slug !== data.slug || !Array.isArray(index.entries)) throw new Error('Invalid index');
    if (activeRequest !== data.requestId) return;
    const results = [];
    let total = 0;
    for (const entry of index.entries) {
      const at = entry.text.toLowerCase().indexOf(query);
      if (at < 0) continue;
      total += 1;
      if (results.length < 60) results.push({ headingId: entry.headingId, snippet: entry.text.slice(Math.max(0, at - 65), at + query.length + 105) });
    }
    self.postMessage({ type: 'results', requestId: data.requestId, total, results });
  } catch {
    indexPromise = null;
    if (activeRequest === data.requestId) self.postMessage({ type: 'error', requestId: data.requestId });
  }
};
