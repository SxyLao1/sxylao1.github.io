"""Build the durable, directory-backed Moments catalogue and recovery archive."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from PIL import Image, ImageOps

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python 3.9+ provides zoneinfo
    ZoneInfo = None


SITE_ROOT = Path(__file__).resolve().parents[1]
MOMENTS_ROOT = SITE_ROOT / "content" / "moments"
DIST = SITE_ROOT / "dist"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def shanghai_timezone():
    if ZoneInfo is not None:
        try:
            return ZoneInfo("Asia/Shanghai")
        except Exception:
            pass
    return timezone(timedelta(hours=8), name="Asia/Shanghai")


SHANGHAI_TZ = shanghai_timezone()


def fail(message: str) -> ValueError:
    return ValueError(f"Invalid Moments content: {message}")


def plain_string(value, field: str, post_id: str, *, allow_newlines: bool = True) -> str:
    if not isinstance(value, str):
        raise fail(f"{post_id}: {field} must be a string")
    if not value.strip():
        raise fail(f"{post_id}: {field} must not be empty")
    allowed = {"\n", "\r", "\t"} if allow_newlines else set()
    if any(ord(char) < 32 and char not in allowed for char in value):
        raise fail(f"{post_id}: {field} contains a control character")
    return value


def load_posts(moments_root: Path):
    if not moments_root.exists():
        return []
    if not moments_root.is_dir():
        raise fail("content/moments must be a directory")

    posts = []
    seen_ids = set()
    for post_dir in sorted(moments_root.iterdir(), key=lambda item: item.name):
        if not post_dir.is_dir():
            raise fail(f"{post_dir.name}: each item must be a post directory")
        if post_dir.is_symlink():
            raise fail(f"{post_dir.name}: post folders must not be symlinks")
        metadata_path = post_dir / "post.json"
        if not metadata_path.is_file():
            raise fail(f"{post_dir.name}: missing post.json")
        try:
            metadata_path.resolve(strict=True).relative_to(post_dir.resolve())
        except (OSError, ValueError) as exc:
            raise fail(f"{post_dir.name}: post.json escapes its post folder") from exc
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise fail(f"{post_dir.name}: unreadable post.json ({exc})") from exc
        if not isinstance(metadata, dict):
            raise fail(f"{post_dir.name}: post.json must contain an object")

        post_id = metadata.get("id")
        if not isinstance(post_id, str) or not post_id or post_id != post_dir.name:
            raise fail(f"{post_dir.name}: id must equal its folder name")
        if post_id in seen_ids:
            raise fail(f"duplicate id {post_id}")
        seen_ids.add(post_id)
        date = metadata.get("date")
        if not isinstance(date, str):
            raise fail(f"{post_id}: date must be an ISO date")
        try:
            if datetime.strptime(date, "%Y-%m-%d").date().isoformat() != date:
                raise ValueError("not canonical")
        except ValueError as exc:
            raise fail(f"{post_id}: date must be ISO YYYY-MM-DD") from exc

        title = plain_string(metadata.get("title"), "title", post_id, allow_newlines=False)
        text = plain_string(metadata.get("text"), "text", post_id)
        tags = metadata.get("tags")
        if not isinstance(tags, list) or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
            raise fail(f"{post_id}: tags must be a list of non-empty strings")
        images = metadata.get("images", [])
        if not isinstance(images, list) or len(images) > 9:
            raise fail(f"{post_id}: images must contain from zero to nine filenames")

        resolved_folder = post_dir.resolve()
        sources = []
        seen_images = set()
        for filename in images:
            if not isinstance(filename, str) or not filename:
                raise fail(f"{post_id}: image names must be strings")
            path = Path(filename)
            if path.is_absolute() or path.parent != Path(".") or filename in {".", ".."}:
                raise fail(f"{post_id}: image must be a relative filename in its post folder")
            if filename in seen_images:
                raise fail(f"{post_id}: duplicate image filename {filename}")
            seen_images.add(filename)
            source = post_dir / path
            try:
                resolved_source = source.resolve(strict=True)
                resolved_source.relative_to(resolved_folder)
            except (OSError, ValueError) as exc:
                raise fail(f"{post_id}: image escapes its post folder: {filename}") from exc
            if not resolved_source.is_file() or resolved_source.suffix.lower() not in IMAGE_EXTENSIONS:
                raise fail(f"{post_id}: unsupported or missing image {filename}")
            sources.append((filename, resolved_source))

        posts.append({"id": post_id, "date": date, "title": title, "text": text, "tags": tags, "sources": sources, "metadata": metadata_path})
    return sorted(posts, key=lambda post: (post["date"], post["id"]), reverse=True)


def source_digest(post_id: str, filename: str, source: Path) -> str:
    digest = hashlib.sha256()
    digest.update(post_id.encode("utf-8"))
    digest.update(b"\0")
    digest.update(filename.encode("utf-8"))
    with source.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def render_image(post_id: str, filename: str, source: Path, target: Path):
    try:
        with Image.open(source) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image.thumbnail((1400, 1000), Image.Resampling.LANCZOS)
            image.save(target, "WEBP", quality=84, method=6)
        with Image.open(target) as rendered:
            return {"src": f"assets/moments/{source_digest(post_id, filename, source)}.webp", "alt": "", "width": rendered.width, "height": rendered.height}
    except Exception as exc:
        raise fail(f"{post_id}: cannot render image {filename} ({exc})") from exc


RECOVERY_README = """# 时光足迹恢复说明

此压缩包保存每条足迹的原始 `post.json` 和该条目选中的原始图片。

恢复或迁移时，将 `content/moments/` 整体解压回站点源码的同名目录，再运行：

```powershell
python scripts/build_moments.py
```

生成的 `dist/data/moments.json`、`dist/data/moments-backup.zip` 与 `dist/assets/moments/` 可随静态站点一同发布。请另外备份本压缩包和源码中的 `content/moments/`。
"""


def build_backup(posts, stage_zip: Path):
    with zipfile.ZipFile(stage_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("README-RECOVERY.md", RECOVERY_README)
        for post in posts:
            folder = Path("content") / "moments" / post["id"]
            archive.write(post["metadata"], (folder / "post.json").as_posix())
            for filename, source in post["sources"]:
                archive.write(source, (folder / filename).as_posix())


def atomic_replace(source: Path, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    os.replace(source, target)


def build(site_root: Path = SITE_ROOT, generated_at: str | None = None):
    """Validate all posts before replacing the catalogue, then build site outputs."""
    site_root = Path(site_root)
    moments_root = site_root / "content" / "moments"
    posts = load_posts(moments_root)
    date = generated_at or datetime.now(SHANGHAI_TZ).date().isoformat()
    try:
        if datetime.strptime(date, "%Y-%m-%d").date().isoformat() != date:
            raise ValueError("not canonical")
    except ValueError as exc:
        raise ValueError("generated_at must be ISO YYYY-MM-DD") from exc

    dist = site_root / "dist"
    data_dir = dist / "data"
    assets_dir = dist / "assets" / "moments"
    # Stage beside the final catalogue so os.replace stays on the same volume.
    # This avoids a cross-volume move while keeping the old JSON untouched until
    # all source data, resized images, and the backup ZIP are ready.
    data_dir.mkdir(parents=True, exist_ok=True)
    stage_files = []
    try:
        catalogue_posts = []
        outputs = set()
        for post in posts:
            images = []
            for filename, source in post["sources"]:
                with tempfile.NamedTemporaryFile(prefix=".moments-", suffix=".webp", dir=data_dir, delete=False) as handle:
                    stage_image = Path(handle.name)
                stage_files.append(stage_image)
                image = render_image(post["id"], filename, source, stage_image)
                images.append(image)
            if any(image["src"] in outputs for image in images):
                raise fail(f"{post['id']}: duplicate generated image output")
            outputs.update(image["src"] for image in images)
            catalogue_posts.append({key: post[key] for key in ("id", "date", "title", "text", "tags")} | {"images": images})
        catalogue = {"schemaVersion": 1, "generatedAt": date, "posts": catalogue_posts}
        with tempfile.NamedTemporaryFile(prefix=".moments-", suffix=".json", dir=data_dir, delete=False) as handle:
            stage_json = Path(handle.name)
        stage_files.append(stage_json)
        stage_json.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with tempfile.NamedTemporaryFile(prefix=".moments-", suffix=".zip", dir=data_dir, delete=False) as handle:
            stage_zip = Path(handle.name)
        stage_files.append(stage_zip)
        build_backup(posts, stage_zip)

        assets_dir.mkdir(parents=True, exist_ok=True)
        try:
            assets_dir.resolve(strict=True).relative_to((dist / "assets").resolve(strict=True))
        except (OSError, ValueError) as exc:
            raise RuntimeError("Moments asset directory escapes dist/assets") from exc
        for staged_image, image in zip(stage_files[:sum(len(post["sources"]) for post in posts)], (image for post in catalogue_posts for image in post["images"])):
            atomic_replace(staged_image, assets_dir / Path(image["src"]).name)
        atomic_replace(stage_json, data_dir / "moments.json")
        atomic_replace(stage_zip, data_dir / "moments-backup.zip")
        active_names = {Path(image["src"]).name for post in catalogue_posts for image in post["images"]}
        for generated in assets_dir.glob("*.webp"):
            if generated.name not in active_names:
                generated.unlink()
        return catalogue
    finally:
        for staged in stage_files:
            staged.unlink(missing_ok=True)


if __name__ == "__main__":
    result = build()
    print(f"Built {len(result['posts'])} Moments posts.")
