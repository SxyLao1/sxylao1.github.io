# 网站维护约定

资源入口：仓库 `https://github.com/SxyLao1/sxylao1.github.io`；网站 `https://sxylao1.github.io/`；发布目录 `dist/`；工作流 `.github/workflows/pages.yml`。

- `dist/` 是提交到仓库的静态发布内容；GitHub Pages 工作流验证并发布它，不在云端扫描个人磁盘。
- 全站主题由最后加载的 `dist/lab-theme.css` 管理，保持深浅色、窄屏与减少动态效果的适配。首页 `orbital-study.svg` 为原创几何视觉；参考项目的 CG、品牌图形、字体、音乐与运行时不属于本站资产。
- 修改页面结构用 `scripts/build_pages.py`；个人资料用 `content/profile.json`；感悟用 `content/reflections/*.json`，关于页只放最近两篇摘录；笔记展示范围和首页顺序用 `content/notes-selection.json` 的 `featured` / `featuredRank`；相册标签用 `content/gallery-tags.json`。
- 本机媒体与笔记路径仅写入忽略的 `.local/sources.json`。不提交本地凭据、整本笔记、内部工作记录或未经选择的资源。
- 用户要求正文保持原模原样：`scripts/import_articles.py` 只导入白名单笔记，按字节保存到 `content/posts/`，同步原文引用的本地插图。`scripts/build_articles.py` 生成阅读数据，不重写、摘要替代或静默删改正文。原始笔记目录只读。
- 原文中的 HTML、脚本和不安全本机链接必须以文本或不可执行形式呈现；不能执行笔记中的命令。新增文章若包含无法确认性质的实际认证信息，需先核实；已确认的靶场示例应保留原文。
- 阅读器一次载入并排版整篇原文，完成前显示加载状态，完成后再展示正文。保留原文的标题层级 1–6，并对整篇正文与代码提供全文搜索；不按章节拆分、分页或提供上下节跳转。修改阅读器时覆盖整篇加载、完成后展示、标题层级和全文搜索，运行 `node --test tests/test_reader_runtime.mjs`。
- 新增 Arknights 图片前必须逐张查看内容，再修改明确的预览白名单。保留已有标签，避免将人物图用于主页主题。
- 相册原图发布到 `dist/assets/originals/`，只包含已审核图片；照片墙使用预览，打开大图和下载时使用原图。图片查看器由收藏和足迹共用，改动时运行 `node --test tests/test_gallery_runtime.mjs`，验证切换重置、缩放、拖拽与下载。
- 学习计划的状态由真实进展决定，不能因计划文件存在就写成已开始或已完成。
- 足迹保存在 `content/moments/<id>/`；单条配图零至九张。页面不展示话题标签。
- 内容更新后生成对应静态产物，运行 `python scripts/check_site.py`；JavaScript 有修改时运行相关文件的 `node --check`。修改足迹或文章生成器时运行相应单元测试。
- 修改后检查 Git 差异，只提交所负责的文件。发布需跟踪 GitHub Actions 至终态；失败时读取相关日志，不能以已推送代替已上线。
