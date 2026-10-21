'use strict';
let momentsData;

function selectAlbumView(view, updateUrl = true) {
  const moments = view === 'moments';
  document.querySelector('#photosPanel').hidden = moments;
  document.querySelector('#momentsPanel').hidden = !moments;
  document.querySelectorAll('.album-view-button').forEach((button) => {
    const selected = button.dataset.view === (moments ? 'moments' : 'photos');
    button.classList.toggle('active', selected);
    button.setAttribute('aria-selected', String(selected));
    button.tabIndex = selected ? 0 : -1;
  });
  if (!moments && catalog) renderGallery();
  if (updateUrl) {
    const url = new URL(location.href);
    if (moments) url.searchParams.set('view', 'moments');
    else url.searchParams.delete('view');
    url.hash = '';
    history.replaceState(null, '', url);
  }
}

function renderMoments(data) {
  momentsData = data;
  const posts = data.posts;
  document.querySelector('#momentsCount').textContent = `${posts.length} 条足迹${posts.length ? ` · 从 ${posts[posts.length - 1].date} 开始` : ''}`;
  document.querySelector('#momentsFeed').innerHTML = posts.map((post, postIndex) => {
    const [year, month, day] = post.date.split('-');
    const text = post.text.split(/\n\s*\n/).filter(Boolean).map((part) => `<p>${escapeHtml(part).replaceAll('\n', '<br>')}</p>`).join('');
    const images = post.images || [];
    return `<article class="moment-card" id="moment-${escapeHtml(post.id)}"><time class="moment-date" datetime="${escapeHtml(post.date)}"><strong>${escapeHtml(day)}</strong><span>${escapeHtml(month)} 月</span><small>${escapeHtml(year)}</small></time><div class="moment-content"><div class="moment-author"><img class="moment-avatar" src="favicon.jpg?v=20261022-hacker" alt="" width="29" height="29"><span>${siteName}</span></div><h2>${escapeHtml(post.title)}</h2><div class="moment-text">${text}</div>${images.length ? `<div class="moment-images" data-count="${images.length}">${images.map((image, imageIndex) => `<button type="button" class="moment-image" data-post="${postIndex}" data-image="${imageIndex}" aria-label="放大足迹图片 ${imageIndex + 1}：${escapeHtml(image.alt || post.title)}"><img src="${escapeHtml(image.src)}" alt="${escapeHtml(image.alt || post.title)}" width="${image.width}" height="${image.height}" loading="lazy"></button>`).join('')}</div>` : ''}</div></article>`;
  }).join('') || '<p class="moments-error">第一条足迹，留给接下来想记住的那一天。</p>';
  document.querySelectorAll('.moment-image').forEach((button) => button.addEventListener('click', () => {
    const post = momentsData.posts[Number(button.dataset.post)];
    openImageGroup(post.images.map((image) => ({ preview: image.src, title: image.alt || post.title, name: image.alt || post.title })), Number(button.dataset.image));
  }));
}

const viewButtons = [...document.querySelectorAll('.album-view-button')];
viewButtons.forEach((button, index) => {
  button.addEventListener('click', () => selectAlbumView(button.dataset.view));
  button.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? viewButtons.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + viewButtons.length) % viewButtons.length;
    viewButtons[next].focus();
    viewButtons[next].click();
  });
});
selectAlbumView(new URLSearchParams(location.search).get('view') === 'moments' || location.hash === '#moments' ? 'moments' : 'photos', false);
fetch('data/moments.json', { cache: 'no-cache' })
  .then((response) => { if (!response.ok) throw new Error('Moments unavailable'); return response.json(); })
  .then(renderMoments)
  .catch(() => {
    document.querySelector('#momentsCount').textContent = '暂时无法读取足迹';
    document.querySelector('#momentsFeed').innerHTML = '<p class="moments-error">足迹暂时没有加载成功，请刷新页面再试一次。</p>';
  });
