# 本地构建

需要 Python 3.10 或更高版本，以及本机可读取的图片和笔记目录。原始目录只读；构建只会把已审核的预览和笔记目录写入 `dist/`。

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

在浏览器打开 `http://localhost:8000` 预览。确认后检查 `dist/`，只提交本次更新需要的内容与生成后的静态文件。

## Referenced by（导航辅助，非权威）
- ../README.md — 项目入口和发布说明
