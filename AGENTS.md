# 网站维护约定

资源入口：仓库 `https://github.com/SxyLao1/sxylao1.github.io`；网站 `https://sxylao1.github.io/`；发布目录 `dist/`；工作流 `.github/workflows/pages.yml`。

- `dist/` 是提交到仓库的静态发布内容；GitHub Pages 工作流验证并发布它，不在云端扫描个人磁盘。
- 修改页面结构用 `scripts/build_pages.py`；个人文字用 `content/profile.json`；笔记展示范围用 `content/notes-selection.json`；相册标签用 `content/gallery-tags.json`。
- 本机媒体与笔记路径仅写入忽略的 `.local/sources.json`。不提交本地凭据、整本笔记、内部工作记录或未经选择的资源。
- 笔记目前只展示目录与摘要。新增源文件不会自动进入公开目录；不要绕过白名单发布原文。
- 新增 Arknights 图片前必须逐张查看内容，再修改明确的预览白名单。保留已有标签，避免将人物图用于主页主题。
- 学习计划的状态由真实进展决定，不能因计划文件存在就写成已开始或已完成。
- 足迹保存在 `content/moments/<id>/`；单条配图零至九张。页面不展示话题标签。
- 内容更新后生成对应静态产物，运行 `python scripts/check_site.py`；JavaScript 有修改时运行 `node --check dist/app.js` 和 `node --check dist/moments.js`。修改足迹生成器时运行相应单元测试。
- 修改后检查 Git 差异，只提交所负责的文件。发布需跟踪 GitHub Actions 至终态；失败时读取相关日志，不能以已推送代替已上线。
