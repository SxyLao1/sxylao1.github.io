# SxyLao1 的个人网站

一个计算机爱好者的自留地：写下所学，存下喜欢，慢慢向前。

网站：**https://sxylao1.github.io/**

使用 HTML、CSS 和 JavaScript 构建，发布到 GitHub Pages。浏览网站不需要运行 Python、数据库或自己的服务器。

## 页面与内容

- 首页：个人介绍和精选笔记入口。
- 关于：修己、游戏动漫与阅读偏好、学习计划、桌面折腾。
- 博客：精选笔记的目录与摘要，按安全分析、计算机基础和学习计划分类。
- 相册：图片收藏和按日期记录的时光足迹，支持零至九张配图与原始内容备份。
- 联系：GitHub、CSDN 与 Bilibili 入口。

`content/profile.json` 保存关于页文字；`content/notes-selection.json` 是笔记展示白名单；`content/gallery-tags.json` 定义图片标签。新增足迹的格式见 [内容目录说明](content/README.md)。

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

## 发布

将修改后的内容和生成的 `dist/` 一起提交并推送到 `main`。GitHub Actions 会验证页面、目录、图片与足迹备份，再将 `dist/` 发布到 GitHub Pages。云端发布不读取本机媒体目录。

发布状态见仓库的 Actions；工作流为 `.github/workflows/pages.yml`。维护状态见 [WORKLOG.md](WORKLOG.md)。

原主页设计致谢：HZR / Bilibili-hzr。收藏图片的相关权利归各自原作者。
