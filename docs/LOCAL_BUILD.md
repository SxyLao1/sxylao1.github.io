# 本地构建

需要 Python 3.10 或更高版本，以及本机可读取的图片和笔记目录。原始目录只读；构建只导入白名单中的原始笔记与引用的本地图片，并生成 `dist/`。Markdown 和原图保留来源字节，网页负责排版。

```powershell
New-Item -ItemType Directory -Force .local | Out-Null
Copy-Item content/sources.example.json .local/sources.json
python -m pip install -r requirements.txt
```

编辑 `.local/sources.json`，设置 `funny`、`arknights` 和 `notes` 三个目录。相对路径以仓库根目录为基准；该文件已被 Git 忽略，不能提交。

```powershell
python scripts/build_site.py
python scripts/check_site.py
python -m http.server 8000 --directory dist
```

只更新笔记时，可依次运行 `python scripts/import_articles.py` 和 `python scripts/build_articles.py`。引用的本地图片会复制到 `content/article-assets/` 与 `dist/article-assets/`；找不到的原始图片以缺图提示保留。

只更新个人资料或感悟时，运行 `python scripts/build_pages.py`。修改首页精选范围和顺序后，运行 `python scripts/build_catalog.py`；全文搜索与章节数据由文章构建器一并生成，不需要额外服务。

修改生成器或阅读器后运行对应检查：

```powershell
python -X utf8 -m unittest discover -s tests -v
node --test tests/test_reader_runtime.mjs tests/test_gallery_runtime.mjs
python scripts/check_site.py
```

在浏览器打开 `http://localhost:8000` 预览。确认后检查 `dist/`，只提交本次更新需要的内容与生成后的静态文件。

## Referenced by（导航辅助，非权威）
- ../README.md — 项目入口和发布说明
