"""Render the original HOME / ABOUT / BLOG / ALBUM / CONTACT structure as static pages."""
from pathlib import Path
from shutil import copyfile
from about_content import render_about
from reflection_content import load_reflections, render_thoughts_index, render_thought

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DISPLAY_NAME = "𝒮𝓍𝓎ℒ𝒶ℴ𝓁"
PAGES = {"index": ("首页", "HOME"), "about": ("关于", "ABOUT"), "blog": ("博客", "BLOG"), "album": ("相册", "ALBUM"), "join": ("联系", "CONTACT")}


def header(page):
    links = "".join(f'<a href="{key}.html" {"aria-current=\"page\"" if key == page else ""}><span>{en}</span>{cn}</a>' for key, (cn, en) in PAGES.items())
    return f'''<header class="site-header"><div class="wrap header-inner">
      <a class="brand" href="index.html" aria-label="SxyLao1 首页">{DISPLAY_NAME}<span class="brand-period">.</span><small>MY PROFILE</small></a>
      <nav class="main-nav" aria-label="主导航">{links}</nav>
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="切换深色主题" aria-pressed="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></svg></button>
    </div></header>'''


FOOTER = f'''<footer class="site-footer wrap"><a class="footer-brand" href="index.html">{DISPLAY_NAME}.</a><p>Cease to struggle and you cease to live.</p><a href="#top" class="back-top">回到顶部 ↑</a><small>© 2022–2026 · 文字、图像与一些未完成的想法</small></footer>'''


def page_head(index, english, title, description):
    return f'<div class="page-head wrap"><p class="eyebrow">{index} / {english}</p><h1>{title}<span class="accent">.</span></h1><p class="page-description">{description}</p></div>'


HOME = '''<section class="home-hero wrap">
  <div class="hero-copy"><p class="eyebrow"><span class="short-line"></span>A LITTLE CORNER OF THE INTERNET</p>
    <p class="hero-name">你好，我是 𝒮𝓍𝓎ℒ𝒶ℴ𝓁。</p><h1>Cease to struggle,<br>and you cease<br>to <em>live.</em></h1>
    <p class="hero-description">一个计算机爱好者的自留地。<br>写下所学，存下喜欢，慢慢向前。</p>
    <a class="text-link" href="blog.html">翻翻我的笔记 <span>↗</span></a>
    <div class="hero-bottom"><span>TECHNOLOGY · NOTES · LIFE</span><span>SCROLL TO EXPLORE ↓</span></div>
  </div>
  <div class="hero-art"><img src="assets/quiet-hours.svg" alt="安静的窗边：远山、阳光和几本书" width="840" height="1000"><span class="art-caption">A WINDOW, A FEW BOOKS, SOME TIME.</span><span class="art-number">01 — HOME</span></div>
</section>
<section class="home-entries wrap" aria-label="网站入口">
  <a class="entry" href="about.html"><span class="entry-top">01 / ABOUT <span>↗</span></span><h2>关于我</h2><p>普通人，计算机爱好者，<br>还在人生的长跑路上。</p></a>
  <a class="entry" href="blog.html"><span class="entry-top">02 / BLOG <span>↗</span></span><h2>博客与笔记</h2><p>安全、技术和学习，<br>给思考留一个位置。</p></a>
  <a class="entry" href="album.html"><span class="entry-top">03 / ALBUM <span>↗</span></span><h2>我的相册</h2><p>喜欢的画面，偶然的灵感，<br>在照片墙上慢慢看。</p></a>
  <a class="entry" href="join.html"><span class="entry-top">04 / CONTACT <span>↗</span></span><h2>打个招呼</h2><p>在代码、文字和共同<br>感兴趣的事情里遇见。</p></a>
</section>
<section class="section wrap"><div class="section-heading"><div><p class="eyebrow">FROM THE NOTEBOOK</p><h2>笔记的几页</h2></div><a class="text-link" href="blog.html">全部笔记 <span>↗</span></a></div><div class="home-posts" id="homePosts"><p class="loading">正在整理目录…</p></div></section>
<section class="home-signoff wrap"><span class="eyebrow">A NOTE TO MYSELF</span><p>愿此行，终抵群星。</p></section>'''

ABOUT = page_head("01", "ABOUT", "关于我", "计算机爱好者，二次元与文字的爱好者，也在认真认识自己。") + render_about()

BLOG = page_head("02", "BLOG", "博客与笔记", "安全分析与计算机基础，一些值得留下的笔记，也留着还在起点的学习计划。") + '''
<section class="blog-layout wrap"><aside class="blog-sidebar"><div class="sidebar-profile"><img class="profile-avatar" src="favicon.jpg?v=20261022-hacker" alt="个人头像" width="62" height="62"><h2>𝒮𝓍𝓎ℒ𝒶ℴ𝓁</h2><p>写下所学，也留下问题。</p><a class="text-link" href="https://blog.csdn.net/SxyLao1" target="_blank" rel="noreferrer">CSDN 博客 ↗</a></div><div class="sidebar-section"><p class="eyebrow">CATEGORIES / 目录</p><div id="folderRail" class="folder-rail"></div></div></aside>
<div class="blog-content"><div class="blog-tools"><label class="search-box"><span aria-hidden="true">⌕</span><input id="noteSearch" type="search" placeholder="搜索文章或目录" aria-label="搜索文章或目录"><kbd>/</kbd></label><select id="noteSort" aria-label="文章排序"><option value="name">按标题</option><option value="date">最近修改</option></select></div><div class="list-heading"><span id="listTitle">全部笔记</span><span id="noteResultCount" aria-live="polite"></span></div><div id="notesList" class="article-list"><p class="loading">正在加载文章目录…</p></div><p class="directory-note">整理自个人笔记。点击文章即可阅读全文，也可以下载 Markdown。</p></div></section>'''

ALBUM = page_head("03", "ALBUM", "相册与足迹", "喜欢的画面，走过的时间，都在这里慢慢留下。") + '''
<div class="album-view-nav wrap" role="tablist" aria-label="相册视图"><button type="button" id="photosTab" class="album-view-button active" role="tab" aria-controls="photosPanel" aria-selected="true" data-view="photos">图片收藏 <span>COLLECTION</span></button><button type="button" id="momentsTab" class="album-view-button" role="tab" aria-controls="momentsPanel" aria-selected="false" data-view="moments">时光足迹 <span>MOMENTS</span></button></div>
<section class="album-section wrap" id="photosPanel" role="tabpanel" aria-labelledby="photosTab"><div class="album-toolbar"><div class="gallery-switcher" id="galleryTags" role="tablist" aria-label="图片标签"></div><span class="album-hint" id="galleryCount" aria-live="polite"></span></div><p class="gallery-description" id="galleryDescription"></p><div class="photo-wall" id="galleryGrid"><p class="loading">正在展开照片墙…</p></div><p class="album-bottom">收藏的图像，各有各的故事。<span>点击预览 · 滚轮缩放 · 拖拽移动 · 可下载原图</span></p></section>
<section class="moments-section wrap" id="momentsPanel" role="tabpanel" aria-labelledby="momentsTab" hidden><div class="moments-layout"><aside class="moments-intro"><span class="eyebrow">A TRACE OF MY DAYS</span><h2>给日常，<br>留一个地址。</h2><p>一段文字，几张图片。<br>把此刻留给未来的自己。</p><p class="moments-count" id="momentsCount">正在整理足迹…</p><a class="moment-backup text-link" href="data/moments-backup.zip" download="SxyLao1-时光足迹备份.zip">下载足迹备份 <span>↓</span></a></aside><div class="moments-feed" id="momentsFeed" aria-live="polite"><p class="loading">正在翻开时间…</p></div></div></section>
<dialog class="lightbox" id="lightbox" aria-label="图片预览"><button class="lightbox-close" id="lightboxClose" aria-label="关闭预览" type="button">×</button><button class="lightbox-prev" id="lightboxPrev" aria-label="上一张" type="button">←</button><div class="lightbox-content"><div class="lightbox-viewport" id="lightboxViewport"><img id="lightboxImage" alt="" draggable="false"></div><div class="lightbox-tools" aria-label="图片工具"><button id="lightboxZoomOut" type="button" aria-label="缩小图片">−</button><output id="lightboxZoomValue" aria-label="缩放比例">100%</output><button id="lightboxZoomIn" type="button" aria-label="放大图片">＋</button><button id="lightboxReset" type="button">适应窗口</button><a id="lightboxDownload" download>下载原图 ↓</a></div><div class="lightbox-caption"><p id="lightboxCaption"></p><span id="lightboxCount"></span></div></div><button class="lightbox-next" id="lightboxNext" aria-label="下一张" type="button">→</button></dialog>'''

CONTACT = page_head("04", "CONTACT", "打个招呼", "欢迎聊聊代码、文字，以及共同感兴趣的事情。") + '''
<section class="join-layout wrap"><div class="join-statement"><p class="eyebrow">LET'S KEEP IN TOUCH</p><h2>一个问题，<br>也可以是<br><em>对话的开始。</em></h2><p>可以从 GitHub 上的项目开始，也可以从博客里的一篇文章开始。</p></div><div class="contact-links"><a href="https://github.com/SxyLao1" target="_blank" rel="noreferrer"><span class="contact-index">01</span><div><small>CODE & PROJECTS</small><h3>GitHub</h3><p>@SxyLao1</p></div><span class="contact-arrow">↗</span></a><a href="https://blog.csdn.net/SxyLao1" target="_blank" rel="noreferrer"><span class="contact-index">02</span><div><small>ARTICLES & NOTES</small><h3>CSDN</h3><p>@SxyLao1</p></div><span class="contact-arrow">↗</span></a><a href="https://space.bilibili.com/389562675" target="_blank" rel="noreferrer"><span class="contact-index">03</span><div><small>ELSEWHERE</small><h3>Bilibili</h3><p>在另一个角落</p></div><span class="contact-arrow">↗</span></a></div></section>'''


ARTICLE = '''<div class="reader-wrap wrap">
<a class="text-link reader-back" href="blog.html">← 返回博客</a>
<div id="articleStatus" class="reader-status is-loading" role="status" aria-live="polite"><span class="reader-spinner" aria-hidden="true"></span><p>正在读取完整笔记…</p></div>
<div id="articleView" hidden aria-busy="true">
  <header class="reader-heading"><p class="eyebrow" id="articleCategory"></p><h1 id="articleTitle"></h1><p class="reader-summary" id="articleSummary"></p><div class="reader-meta"><span id="articleMeta"></span><a id="articleDownload" href="blog.html" download>下载原始 Markdown ↓</a></div></header>
  <section class="reader-search" aria-label="笔记内搜索">
    <div class="reader-search-field"><label for="articleSearch">全文搜索</label><input id="articleSearch" type="search" maxlength="80" placeholder="搜索整篇笔记与代码…" autocomplete="off"><kbd>Ctrl K</kbd><button id="articleSearchClear" type="button">清空</button></div>
    <div id="articleSearchPanel" class="reader-search-panel" hidden><p id="articleSearchStatus" role="status" aria-live="polite"></p><div id="articleSearchResults"></div></div>
  </section>
  <div class="reading-layout">
    <aside class="reader-toc" aria-label="文章目录"><p class="eyebrow">CONTENTS / 目录</p><nav id="articleToc"></nav></aside>
    <div class="reader-main">
      <article class="markdown-body" id="articleContent"></article>
    </div>
  </div>
  <div class="reader-end"><span class="eyebrow">FROM THE NOTEBOOK</span><p>写下所学，也留下问题。</p><a class="text-link" href="blog.html">继续翻翻笔记 <span>↗</span></a></div>
</div></div>'''


def main():
    copyfile(ROOT / "content" / "site-icon.jpg", DIST / "favicon.jpg")
    reflections = load_reflections()
    bodies = {"index": HOME, "about": ABOUT, "blog": BLOG, "album": ALBUM, "join": CONTACT, "article": ARTICLE, "thoughts": render_thoughts_index(reflections)}
    thought_titles = {}
    for entry in reflections:
        key = f"thought-{entry['slug']}"
        bodies[key] = render_thought(entry)
        thought_titles[key] = entry['title']
    for page, body in bodies.items():
        label = thought_titles.get(page) or ("一些随想" if page == "thoughts" else "笔记" if page == "article" else PAGES.get(page, ("个人主页",))[0])
        title = f"{DISPLAY_NAME} · 个人主页" if page == "index" else f"{label} · {DISPLAY_NAME}"
        extra = ''
        if page == 'about' or page.startswith('thought'):
            extra = '<link rel="stylesheet" href="about.css?v=20261022-fullnote">'
        elif page == 'album':
            extra = '<link rel="stylesheet" href="album.css?v=20261022-fullnote"><script src="moments.js?v=20261022-fullnote" defer></script>'
        elif page == 'article':
            extra = '<link rel="stylesheet" href="article.css?v=20261022-fullnote"><link rel="stylesheet" href="vendor/katex/katex.min.css"><script src="article.js?v=20261022-fullnote" defer></script>'
        html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="SxyLao1 的个人主页：博客、笔记与图像收藏。"><meta name="color-scheme" content="light dark"><title>{title}</title><link rel="icon" href="favicon.jpg?v=20261022-hacker" type="image/jpeg"><link rel="stylesheet" href="styles.css?v=20261022-quote"><script src="app.js?v=20261022-fullnote" defer></script>{extra}</head>
<body id="top" data-page="{page}"><a class="skip-link" href="#main">跳到主要内容</a>{header('blog' if page == 'article' else 'about' if page.startswith('thought') else page)}<main id="main">{body}</main>{FOOTER}</body></html>'''
        (DIST / f"{page}.html").write_text(html, encoding="utf-8")
    print(f"Rendered {len(bodies)} pages, including {len(reflections)} thoughts.")


if __name__ == "__main__":
    main()
