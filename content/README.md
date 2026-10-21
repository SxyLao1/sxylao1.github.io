# 内容目录

`moments/` 是时光足迹的持久来源。每条足迹使用一个独立目录：

```text
content/moments/<id>/
  post.json
  photo-1.jpg
  photo-2.png
```

`post.json` 必须包含与目录名相同的 `id`、ISO 日期 `date`、`title`、纯文本 `text`、字符串数组 `tags`，以及可选的 `images` 文件名数组。每条可放零到九张图片；图片必须放在同一条目的目录中。

添加或修改内容后运行：

```powershell
python scripts/build_moments.py
```

它会生成 `dist/data/moments.json`、用于页面展示的 `dist/assets/moments/` 图片，以及可直接下载和恢复的 `dist/data/moments-backup.zip`。发布时同时发布这些 `dist/` 输出。请持续备份 `content/moments/` 这一来源目录；网站没有在线编辑器。
