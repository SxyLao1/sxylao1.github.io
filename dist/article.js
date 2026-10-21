'use strict';

const articleId = new URLSearchParams(location.search).get('id') || '';
const articleStatus = document.querySelector('#articleStatus');
const articleView = document.querySelector('#articleView');

function showArticleError() {
  document.title = `笔记暂未找到 · ${siteName}`;
  articleView.hidden = true;
  articleStatus.hidden = false;
  articleStatus.setAttribute('role', 'alert');
  articleStatus.innerHTML = '<span class="eyebrow">FROM THE NOTEBOOK</span><h1>这篇笔记暂时没有找到。</h1><p>从博客列表选一篇继续读，或稍后刷新再试。</p><a class="text-link" href="blog.html">返回博客 <span>↗</span></a>';
}

function addCodeCopyButtons() {
  document.querySelectorAll('#articleContent pre').forEach((block) => {
    const code = block.querySelector('code');
    if (!code) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'code-copy';
    button.textContent = '复制';
    button.setAttribute('aria-label', '复制代码');
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = '已复制';
      } catch {
        button.textContent = '请手动选择复制';
      }
      setTimeout(() => { button.textContent = '复制'; }, 1800);
    });
    block.append(button);
  });
}

async function loadArticle() {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(articleId)) {
    showArticleError();
    return;
  }
  try {
    const response = await fetch(`data/articles/${articleId}.json`, { cache: 'no-cache' });
    if (!response.ok) throw new Error('Article unavailable');
    const data = await response.json();
    if (data.slug !== articleId || typeof data.html !== 'string' || !Array.isArray(data.toc)) throw new Error('Invalid article');
    document.title = `${data.title} · ${siteName}`;
    document.querySelector('#articleTitle').textContent = data.title;
    document.querySelector('#articleCategory').textContent = data.category || 'FROM THE NOTEBOOK';
    document.querySelector('#articleSummary').textContent = data.summary || '';
    document.querySelector('#articleMeta').textContent = [data.modifiedAt, `${data.readingMinutes || 1} 分钟阅读`, data.status].filter(Boolean).join(' · ');
    // HTML is produced only by the Markdown compiler with raw HTML disabled.
    document.querySelector('#articleContent').innerHTML = data.html;
    document.querySelector('#articleToc').innerHTML = data.toc.length ? `<ol>${data.toc.map((entry) => `<li class="toc-level-${[1, 2, 3].includes(entry.level) ? entry.level : 2}"><a href="#${encodeURIComponent(entry.id)}">${escapeHtml(entry.text)}</a></li>`).join('')}</ol>` : '<a href="#articleTitle">文章开头</a>';
    const download = document.querySelector('#articleDownload');
    const markdownUrl = `articles/${articleId}.md`;
    download.href = markdownUrl;
    download.setAttribute('download', `${articleId}.md`);
    addCodeCopyButtons();
    if (typeof katex !== 'undefined') {
      document.querySelectorAll('#articleContent .math').forEach((node) => {
        try {
          katex.render(node.textContent, node, { displayMode: node.classList.contains('block'), throwOnError: false, trust: false, maxExpand: 1000 });
        } catch { /* Unsupported formulas remain readable as original LaTeX. */ }
      });
    }
    articleStatus.hidden = true;
    articleView.hidden = false;
    if (location.hash) {
      try { document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView(); } catch { /* Invalid fragments leave the article at its opening. */ }
    }
  } catch {
    showArticleError();
  }
}

loadArticle();
