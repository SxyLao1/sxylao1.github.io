# 网站维护状态

## 2026-10-23 恢复纸墨主题

- 撤回本轮实验室风格，恢复纸墨配色、原首页插图和页面排版。
- 保留整篇笔记加载、全文搜索、相册缩放拖拽下载、CONTACT 联系入口及单行寄语。

## 阅读与相册体验更新

- 博客保留 20 篇原始 Markdown，新增 Forensics、Reverse 与 Web-CTF；首页精选按 Penetration、Pwn、8086 汇编、Forensics、Reverse、Web-CTF 排列。
- 大笔记一次载入完整原文，读取和排版完成前显示加载状态，完成后展示全文。目录保留原文标题 1–6，全文搜索涵盖代码；网页按原文换行，原始 Markdown 下载保持字节不变。
- 关于页保留最近两篇感悟的摘录，全文迁入独立页面，并提供全部随想索引。
- 相册预览支持缩放、拖拽查看和下载已审核原图；照片墙仍使用轻量预览。联系导航改为 CONTACT。
- 发布验证覆盖原稿与下载一致性、全文与搜索数据、个人文字、图片白名单、足迹备份及阅读器交互。
- 整篇阅读修正见 [PR #6](https://github.com/SxyLao1/sxylao1.github.io/pull/6)，[Pages 检查与部署成功](https://github.com/SxyLao1/sxylao1.github.io/actions/runs/39758111598)。线上全文、搜索索引与原文下载均与提交产物一致，旧分章资源已退役。首页寄语为愿此行，终抵群星。
- 浏览器自动化连接超时，真实浏览器视觉与触屏手势尚未实测。

## 2026-10-22 前序发布

以下记录中的分节阅读与上下节跳转属于前序方案，已修正为整篇一次加载与全文展示，仅保留为历史记录。

- 前序相册与内容结构变更见 [PR #4](https://github.com/SxyLao1/sxylao1.github.io/pull/4)，[当时的 Pages 部署成功](https://github.com/SxyLao1/sxylao1.github.io/actions/runs/39653662781)，当时线上产物核对一致。

- 页面结构：首页、关于、博客、相册、联系；纸墨主题与深浅色切换。
- 内容：17 篇原始 Markdown 笔记（含 Penetration、8086 汇编与 Pwn）、27 张图库预览、一条文字足迹；三份学习计划均为“还没开始”。
- 文章：博客与首页链接进入阅读页，提供章节目录、表格、代码复制及 Markdown 下载；只导入选定原文，原始目录只读；本地插图随文章发布。
- 关于页：书单按单书列出并加入《非暴力沟通》，去掉游戏厂商括号和《雾山五行》的外链；移除首页旧站引用署名与联系页邀请句。
- 个人标识：显示名使用 `𝒮𝓍𝓎ℒ𝒶ℴ𝓁`；网站图标、博客头像与足迹头像统一采用指定的 Hacker 图片，源图为 `content/site-icon.jpg`。
- 关于页新增“从求解，到观察”，记录面对不确定性、允许绕路与自我宽恕的想法。
- 首页精选：Penetration、8086 汇编、Pwn 和样本初步分析。
- 托管：GitHub Pages，网站 https://sxylao1.github.io/ ，静态产物为 `dist/`。
- 首次发布提交：`20e579922f746d1e012cb5230637ab3cd657775a`；[部署运行成功](https://github.com/SxyLao1/sxylao1.github.io/actions/runs/39641809314)。
- 本次发布：原文阅读与个人内容更新已合并至 `6392db8c937d52452eb540d668aaa03468c9bdf8`；[Pages 部署成功](https://github.com/SxyLao1/sxylao1.github.io/actions/runs/39646998910)，变更见 [PR #2](https://github.com/SxyLao1/sxylao1.github.io/pull/2)。
- 线上核对：六个页面、17 篇正文与原文下载、头像及本地插图样例可无认证访问，内容与提交产物一致；图库为 4/11/12，足迹备份保持一致。
- 后续维护：更新内容并生成 `dist/`，验证后推送 `main`；GitHub Actions 自动发布。文档更新不会触发重复部署。

## Referenced by（导航辅助，非权威）
- README.md — 项目当前状态
