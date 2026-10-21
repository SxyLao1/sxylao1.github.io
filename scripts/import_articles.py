"""Import selected original notes and their local raster image assets.

The manifest deliberately indexes images by SHA-256 of the exact Markdown
``src`` value.  Keeping the original path out of published JSON prevents a
local drive layout from becoming part of the site payload.  Consumers parse
the same Markdown token and hash its source value to find a portable asset.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DRIVE_PATH_PATTERN = re.compile(r"^[A-Za-z]:[\\/]")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def fail(message: str) -> ValueError:
    return ValueError(f"Invalid original article import: {message}")


def load_json(path: Path, label: str) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise fail(f"cannot read {label}: {exc}") from exc
    if not isinstance(data, dict):
        raise fail(f"{label} must contain an object")
    return data


def selected_articles(site_root: Path) -> list[dict[str, str]]:
    selection = load_json(site_root / "content" / "notes-selection.json", "content/notes-selection.json")
    items = selection.get("items")
    if not isinstance(items, list):
        raise fail("content/notes-selection.json requires an items list")
    selected = []
    seen_slugs = set()
    for entry in items:
        if not isinstance(entry, dict):
            raise fail("selection items must be objects")
        slug, source_path = entry.get("slug"), entry.get("path")
        if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug) or slug in seen_slugs:
            raise fail(f"invalid or duplicate article slug: {slug!r}")
        if not isinstance(source_path, str) or not source_path.strip():
            raise fail(f"{slug}: path must be a non-empty string")
        normalized = source_path.replace("\\", "/")
        path = Path(normalized)
        if path.is_absolute() or DRIVE_PATH_PATTERN.match(normalized) or any(part == ".." for part in path.parts):
            raise fail(f"{slug}: path must be a relative path inside notes")
        seen_slugs.add(slug)
        selected.append({"slug": slug, "path": normalized})
    return selected


def configured_notes_root(site_root: Path) -> Path:
    sources = load_json(site_root / ".local" / "sources.json", ".local/sources.json")
    configured = sources.get("notes")
    if not isinstance(configured, str) or not configured.strip():
        raise fail(".local/sources.json requires a non-empty notes path")
    configured_path = Path(configured)
    return configured_path if configured_path.is_absolute() else site_root / configured_path


def within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def image_sources(markdown: str) -> list[str]:
    parser = MarkdownIt("commonmark", {"html": False, "linkify": False})
    sources = []
    for token in parser.parse(markdown):
        if token.type != "inline" or not token.children:
            continue
        for child in token.children:
            if child.type == "image":
                sources.append(child.attrGet("src") or "")
    return sources


def local_image(raw_source: str, note_parent: Path, notes_root: Path) -> tuple[Path | None, bool]:
    """Return a local raster image and whether a local reference was missing."""
    parsed = urlsplit(raw_source)
    if parsed.netloc or (parsed.scheme and not DRIVE_PATH_PATTERN.match(raw_source)):
        return None, False
    # urlsplit treats ``C:/...`` as scheme ``c``; retain the original drive
    # form so explicitly referenced Windows paths can still be containment
    # checked against the configured notes root.
    raw_path = raw_source.split("#", 1)[0].split("?", 1)[0]
    path_text = raw_path if DRIVE_PATH_PATTERN.match(raw_path) else parsed.path
    source_path = Path(unquote(path_text))
    candidate = source_path if source_path.is_absolute() or DRIVE_PATH_PATTERN.match(path_text) else note_parent / source_path
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        return None, True
    if not resolved.is_file() or not within(resolved, notes_root):
        return None, True
    if resolved.suffix.lower() not in IMAGE_SUFFIXES:
        return None, True
    return resolved, False


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(root: Path = ROOT, notes_root: Path | None = None) -> dict:
    """Validate all selected sources, then copy their exact bytes and assets."""
    site_root = Path(root)
    selected = selected_articles(site_root)
    notes = Path(notes_root) if notes_root is not None else configured_notes_root(site_root)
    try:
        notes = notes.resolve(strict=True)
    except OSError as exc:
        raise fail(f"notes root is unavailable: {notes}") from exc
    if not notes.is_dir():
        raise fail("notes root must be a directory")

    articles: list[tuple[str, bytes]] = []
    assets: dict[str, Path] = {}
    manifest_articles: dict[str, dict[str, str]] = {}
    missing_counts: dict[str, int] = {}
    for entry in selected:
        source = notes / entry["path"]
        try:
            source = source.resolve(strict=True)
            source.relative_to(notes)
        except (OSError, ValueError) as exc:
            raise fail(f"{entry['slug']}: source escapes notes root") from exc
        if not source.is_file():
            raise fail(f"{entry['slug']}: source Markdown is missing")
        try:
            markdown_bytes = source.read_bytes()
            markdown = markdown_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise fail(f"{entry['slug']}: Markdown must be UTF-8") from exc
        articles.append((entry["slug"], markdown_bytes))
        mapping: dict[str, str] = {}
        for raw_source in image_sources(markdown):
            image, missing = local_image(raw_source, source.parent, notes)
            if image is None:
                # Remote destinations are intentionally untouched. Only a local
                # path that cannot safely become a portable raster is reported.
                if missing:
                    missing_counts[entry["slug"]] = missing_counts.get(entry["slug"], 0) + 1
                continue
            content_hash = file_hash(image)
            destination = f"article-assets/{entry['slug']}/{content_hash[:20]}{image.suffix.lower()}"
            mapping[hashlib.sha256(raw_source.encode("utf-8")).hexdigest()] = destination
            assets[destination] = image
        manifest_articles[entry["slug"]] = mapping

    manifest = {"articles": manifest_articles}
    result = {
        "articles": [slug for slug, _ in articles],
        "missingImages": [{"slug": slug, "count": count} for slug, count in missing_counts.items()],
    }
    # Every input and binary payload has been read before this point, so a bad
    # selection cannot replace a prior generated output with a partial import.
    with tempfile.TemporaryDirectory(prefix=".article-import-", dir=site_root) as staging_name:
        staging = Path(staging_name)
        staged: list[tuple[Path, Path]] = []
        for slug, markdown_bytes in articles:
            staged_file = staging / "posts" / f"{slug}.md"
            staged_file.parent.mkdir(parents=True, exist_ok=True)
            staged_file.write_bytes(markdown_bytes)
            staged.append((staged_file, site_root / "content" / "posts" / f"{slug}.md"))
        for relative_target, image in assets.items():
            for base in (site_root / "content", site_root / "dist"):
                staged_file = staging / ("content" if base.name == "content" else "dist") / relative_target
                staged_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(image, staged_file)
                staged.append((staged_file, base / relative_target))
        staged_manifest = staging / "article-assets.json"
        staged_manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        staged.append((staged_manifest, site_root / "content" / "article-assets.json"))
        for staged_file, target in staged:
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged_file, target)
    return result


def main() -> None:
    result = build()
    print(f"Imported {len(result['articles'])} original articles.")


if __name__ == "__main__":
    main()
