# SxyLao1 的个人网站

一个计算机爱好者的自留地：写下所学，存下喜欢，慢慢向前。

网站：**https://sxylao1.github.io/**

使用 HTML、CSS 和 JavaScript 构建，发布到 GitHub Pages。浏览网站不需要运行 Python、数据库或自己的服务器。

## 页面与内容

- 首页：个人介绍和精选笔记入口。
- 关于：个人概况、游戏动漫与阅读偏好、学习计划、桌面折腾；感悟显示摘录并链接独立全文。
- 博客：20 篇原始笔记，支持分节加载、全文搜索、章节目录、公式、表格、代码复制和 Markdown 下载。
- 相册：图片收藏和按日期记录的时光足迹，支持缩放、拖拽查看与下载，足迹可放零至九张配图并备份原始内容。
- 联系：GitHub、CSDN 与 Bilibili 入口。

`content/profile.json` 保存个人资料；`content/reflections/` 保存独立感悟；`content/notes-selection.json` 是笔记展示白名单，`featuredRank` 控制首页精选顺序；`content/posts/` 保存所选笔记的原始 Markdown 快照；`content/article-assets/` 保存原文引用的本地插图；`content/gallery-tags.json` 定义图片标签。新增感悟与足迹的格式见 [内容目录说明](content/README.md)。

## 本地维护

需要 Python 3.10 或更新版本。安装依赖：

```sh
python -m pip install -r requirements.txt
```

媒体和笔记的来源目录放在被忽略的 `.local/sources.json`。配置方法见 [本地构建说明](docs/LOCAL_BUILD.md)。原始文件只读，未选入的笔记和图片不会自动发布。

```sh
python scripts/build_site.py
python scripts/check_site.py
python -m http.server 4177 --bind 127.0.0.1 --directory dist
```

然后打开 `http://127.0.0.1:4177/`。只修改关于页时，可以单独运行 `python scripts/build_pages.py`；只更新足迹时，运行 `python scripts/build_moments.py`。

更新已有笔记后，运行 `python scripts/import_articles.py` 重新导入原文与本地插图，再运行 `python scripts/build_articles.py`。原始 Markdown 按字节保留，网页仅做阅读排版。选取范围由白名单控制，不会自动公开整个笔记库；原文中的代码和 HTML 只作为内容呈现。

大笔记由构建器按完整的 Markdown 块拆成章节，阅读时只打开当前一节；全文搜索索引在首次搜索时加载，并在后台检索所有章节与代码。正文按原文换行展示，代码块的缩进和换行保持原样。

## 发布

将修改后的内容和生成的 `dist/` 一起提交并推送到 `main`。GitHub Actions 会验证页面、目录、图片与足迹备份，再将 `dist/` 发布到 GitHub Pages。云端发布不读取本机媒体目录。

发布状态见仓库的 Actions；工作流为 `.github/workflows/pages.yml`。维护状态见 [WORKLOG.md](WORKLOG.md)。

原主页设计致谢：HZR / Bilibili-hzr。收藏图片的相关权利归各自原作者。

网站图标源文件为 `content/site-icon.jpg`，构建时自动同步为 `dist/favicon.jpg`。
