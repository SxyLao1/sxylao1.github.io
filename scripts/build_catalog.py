from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from PIL import Image

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


SITE_ROOT = Path(__file__).resolve().parents[1]
DIST = SITE_ROOT / "dist"
DATA = DIST / "data"
PREVIEWS = DIST / "assets" / "previews"
SOURCES_CONFIG = SITE_ROOT / ".local" / "sources.json"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Scan the source locally, but publish only the deliberately reviewed images.
ARK_PREVIEW_NAMES = [
    "4K巫恋.jpg",
    "4K稀音.jpg",
    "4K缪尔赛斯.jpg",
    "4K迷迭香.jpg",
    "Amiya.jpg",
    "Lappland01.jpg",
    "Priestess.png",
    "斯卡蒂壁纸.jpg",
    "日光中的花束.jpg",
    "能天使彩绘.jpg",
    "铃兰是我们的光.jpg",
    "音律联觉特蕾西娅.png",
]

def shanghai_timezone():
    if ZoneInfo is not None:
        try:
            return ZoneInfo("Asia/Shanghai")
        except Exception:
            pass
    return timezone(timedelta(hours=8), name="Asia/Shanghai")


SHANGHAI_TZ = shanghai_timezone()


def load_sources():
    """Load local-only source directories when a catalog rebuild is requested.

    Keep this out of module import so CI can check the committed static site
    without a personal disk layout; rebuilding must fail instead of publishing
    an accidentally empty catalog.
    """
    if not SOURCES_CONFIG.is_file():
        raise FileNotFoundError(
            f"Missing local source configuration: {SOURCES_CONFIG}. "
            "Copy content/sources.example.json to .local/sources.json and set funny, arknights, and notes."
        )
    try:
        config = json.loads(SOURCES_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {SOURCES_CONFIG}: {exc}") from exc
    if not isinstance(config, dict):
        raise ValueError(f"{SOURCES_CONFIG} must be a JSON object")

    sources = {}
    for key in ("funny", "arknights", "notes"):
        value = config.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{SOURCES_CONFIG} requires a non-empty {key!r} directory")
        source = Path(value).expanduser()
        if not source.is_absolute():
            source = SITE_ROOT / source
        source = source.resolve()
        if not source.is_dir():
            raise FileNotFoundError(f"Configured {key!r} directory does not exist or is not a directory: {source}")
        sources[key] = source
    return sources


def local_date(timestamp: float):
    return datetime.fromtimestamp(timestamp, SHANGHAI_TZ).date().isoformat()


def note_category(path: Path):
    source = path.as_posix().lower()
    if "english" in source or "postgratuatewriting" in source:
        return "英语学习"
    if "operationsystem" in source:
        return "系统基础"
    # Match APT as a token: substring matching incorrectly labels "Chapter" as security.
    if re.search(r"(?:^|[/ _-])apt(?:[/ _-]|$)", source):
        return "安全"
    if any(keyword in source for keyword in (
        "安全", "security", "forensic", "penetration", "pwn", "reverse", "sqli", "sqlmap", "nmap",
        "traffic", "ctf", "malware", "web-ctf",
    )):
        return "安全"
    if any(keyword in source for keyword in (
        "开发", "program", "python", "javascript", "typescript", "java", "golang",
        "rust", "c.md", "prompt",
    )):
        return "开发"
    if any(keyword in source for keyword in (
        "学习", "study", "course", "教程", "读书", "reading", "笔记",
    )):
        return "学习"
    return "技术"


def files_under(root: Path):
    if not root.exists():
        return []
    return sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: str(p).lower())


def item(path: Path, root: Path):
    rel = path.relative_to(root).as_posix()
    return {
        "name": path.name,
        "path": rel,
        "extension": path.suffix.lower().lstrip(".") or "file",
        "sizeKb": round(path.stat().st_size / 1024, 1),
    }


def note_item(path: Path, notes_root: Path):
    return {
        **item(path, notes_root),
        "folder": path.parent.relative_to(notes_root).as_posix() if path.parent != notes_root else "根目录",
        "title": path.stem,
        "category": note_category(path.relative_to(notes_root)),
        "modifiedAt": local_date(path.stat().st_mtime),
    }


def selected_notes(note_files, notes_root: Path):
    # Only reviewed entries leave the local notebook. New files must never
    # become visible merely because a recursive scan discovered them.
    selection = json.loads((SITE_ROOT / "content" / "notes-selection.json").read_text(encoding="utf-8"))
    source_paths = {path.relative_to(notes_root).as_posix(): path for path in note_files}
    notes, featured, seen = [], [], set()
    for entry in selection["items"]:
        path = entry["path"]
        if path in seen or path not in source_paths:
            raise ValueError(f"Duplicate or missing selected note: {path}")
        if "english" in path.lower() or "postgratuatewriting" in path.lower():
            raise ValueError("English study material is excluded from the website")
        seen.add(path)
        note = {**note_item(source_paths[path], notes_root), **{key: entry[key] for key in ("title", "summary", "category")}, "folder": entry["section"]}
        slug = entry["slug"]
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"Invalid article slug for selected note: {path}")
        note.update({"slug": slug, "url": f"article.html?id={slug}"})
        if entry.get("status"):
            note["status"] = entry["status"]
        notes.append(note)
        if entry.get("featured"):
            featured.append(note)
    return notes, featured


def source_hash(source: Path):
    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()[:16]


def make_preview(source: Path, bucket: str):
    target_dir = PREVIEWS / bucket
    target_dir.mkdir(parents=True, exist_ok=True)
    try:
        target = target_dir / f"{source_hash(source)}.webp"
        with Image.open(source) as image:
            image = image.convert("RGB")
            image.thumbnail((1400, 1000), Image.Resampling.LANCZOS)
            image.save(target, "WEBP", quality=84, method=6)
        with Image.open(target) as preview:
            return {
                "preview": target.relative_to(DIST).as_posix(),
                "previewWidth": preview.width,
                "previewHeight": preview.height,
            }
    except Exception:
        return None


def gallery_catalog(collections):
    config = json.loads((SITE_ROOT / "content" / "gallery-tags.json").read_text(encoding="utf-8"))
    tag_ids = [tag["id"] for tag in config["tags"]]
    if len(tag_ids) != len(set(tag_ids)) or config["defaultTag"] not in tag_ids:
        raise ValueError("Gallery tag IDs must be unique and include the default tag")
    entries = []
    for bucket in ("funny", "arknights"):
        for image in collections[bucket]["items"]:
            if not image.get("preview"):
                continue
            tags = config.get("assignments", {}).get(bucket, {}).get(image["path"], config["defaults"][bucket])
            if not tags or any(tag not in tag_ids for tag in tags):
                raise ValueError(f"Unknown or empty gallery tags for {bucket}/{image['path']}")
            entries.append({**image, "bucket": bucket, "tags": list(dict.fromkeys(tags))})
    return {
        "defaultTag": config["defaultTag"],
        "tags": [{**tag, "count": sum(tag["id"] in image["tags"] for image in entries)} for tag in config["tags"]],
        "items": entries,
    }


def main():
    sources = load_sources()
    funny_root = sources["funny"]
    ark_root = sources["arknights"]
    notes_root = sources["notes"]
    DATA.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)

    funny = files_under(funny_root)
    arknights = files_under(ark_root)
    note_files = [p for p in files_under(notes_root) if p.suffix.lower() == ".md"]

    funny_items = [item(p, funny_root) for p in funny]
    arknights_items = [item(p, ark_root) for p in arknights]
    notes_items, blog_items = selected_notes(note_files, notes_root)
    folders = [{"name": section, "path": section, "markdownCount": sum(note["folder"] == section for note in notes_items)} for section in dict.fromkeys(note["folder"] for note in notes_items)]

    funny_previews = []
    for path in funny:
        if path.suffix.lower() in IMAGE_EXTS:
            preview = make_preview(path, "funny")
            if preview:
                funny_previews.append({"path": path.relative_to(funny_root).as_posix(), **preview})

    # 原始目录只读，发布数据只保留明确挑过的预览。
    ark_by_name = {p.name: p for p in arknights if p.suffix.lower() in IMAGE_EXTS}
    ark_visuals = [ark_by_name[name] for name in ARK_PREVIEW_NAMES if name in ark_by_name]
    arknights_previews = []
    for path in ark_visuals:
        preview = make_preview(path, "arknights")
        if preview:
            arknights_previews.append({"path": path.relative_to(ark_root).as_posix(), **preview})

    preview_map = {
        "funny": {x["path"]: x for x in funny_previews},
        "arknights": {x["path"]: x for x in arknights_previews},
    }
    # Purge only generated site previews. Unreviewed or retired assets must not
    # remain addressable in the next publication; original directories are read-only.
    for bucket, previews in (("funny", funny_previews), ("arknights", arknights_previews)):
        active = {x["preview"] for x in previews}
        for generated in (PREVIEWS / bucket).glob("*.webp"):
            if generated.resolve().is_relative_to(PREVIEWS.resolve()) and generated.relative_to(DIST).as_posix() not in active:
                generated.unlink()
    for x in funny_items:
        if x["path"] in preview_map["funny"]:
            x.update(preview_map["funny"][x["path"]])
    for x in arknights_items:
        if x["path"] in preview_map["arknights"]:
            x.update(preview_map["arknights"][x["path"]])
    arknights_items = [image for image in arknights_items if image.get("preview")]

    catalog = {
        "generatedAt": datetime.now(SHANGHAI_TZ).date().isoformat(),
        "profile": {
            "eyebrow": "SXYLAO1 · PERSONAL WEBSITE",
            "headline": "SXYLAO1 的个人网站",
            "intro": "记录安全工作、阅读和笔记，也放一些想保存的图片。",
            "pillars": ["安全工作", "阅读笔记", "图像收藏", "个人记录"],
        },
        "collections": {
            "funny": {
                "title": "Funny / 梗与偶发灵感",
                "description": "一些不必解释太多的图，负责给系统降噪。",
                "count": len(funny_items),
                "items": funny_items,
            },
            "arknights": {
                "title": "Arknights / 角色档案",
                "description": "偏好、构图与角色记忆的私人展柜。",
                "count": len(arknights_items),
                "items": arknights_items,
            },
            "notes": {
                "title": "MyNote / 精选笔记目录",
                "description": "从个人笔记里选出的技术目录与学习计划。",
                "count": len(notes_items),
                "folderCount": len(folders),
                "folders": folders,
                "items": notes_items,
            },
            "blog": {
                "title": "Blog / 文章索引",
                "description": "从安全分析、检测工程到长期积累的学习笔记。",
                "count": len(blog_items),
                "items": blog_items,
            },
        },
    }
    catalog["gallery"] = gallery_catalog(catalog["collections"])
    (DATA / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "funny": len(funny_items),
        "arknights": len(arknights_items),
        "sourceNotes": len(note_files),
        "selectedNotes": len(notes_items),
        "folders": len(folders),
        "previews": len(funny_previews) + len(arknights_previews),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
