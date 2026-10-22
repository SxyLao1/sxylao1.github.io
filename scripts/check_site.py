"""Validate the committed static GitHub Pages artifact without local source media."""

from __future__ import annotations

import json
import html
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CONTENT = ROOT / "content"
EXPECTED_PAGES = ("index.html", "about.html", "blog.html", "album.html", "join.html", "article.html", "thoughts.html")
SITES_METADATA_DIR = ".openai"
SITES_IDENTITY_PREFIXES = ("appgprj_", "appgver_", "appgdep_")
FORBIDDEN_NOTE_TERMS = ("english", "postgratuatewriting", "temporal")
TEXT_EXTENSIONS = {".css", ".html", ".js", ".json", ".svg", ".txt", ".xml", ".md"}
DRIVE_PATH_PATTERN = re.compile(r"(?<![A-Za-z0-9+.-])[A-Za-z]:[\\/]")


class SiteError(ValueError):
    """A committed deployment artifact is incomplete or does not match its source metadata."""


def fail(message: str) -> None:
    raise SiteError(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON {path.relative_to(ROOT)}: {exc}")


class ReferenceCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append((name, value))


def local_references(page: Path) -> list[str]:
    parser = ReferenceCollector()
    try:
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeDecodeError) as exc:
        fail(f"cannot parse {page.relative_to(DIST)}: {exc}")
    return [value for _, value in parser.references]


def check_html_references() -> None:
    dist_root = DIST.resolve()
    for page in sorted(DIST.rglob("*.html")):
        for reference in local_references(page):
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc or reference.startswith("//"):
                continue
            if not parsed.path:
                continue
            if parsed.path.startswith("/"):
                fail(f"{page.relative_to(DIST)} uses root-relative local reference: {reference}")
            target = (page.parent / unquote(parsed.path)).resolve(strict=False)
            try:
                target.relative_to(dist_root)
            except ValueError:
                fail(f"{page.relative_to(DIST)} reference escapes dist: {reference}")
            if not target.is_file():
                fail(f"{page.relative_to(DIST)} reference is missing: {reference}")


def webp_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 16 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        fail(f"not a WebP preview: {path.relative_to(DIST)}")
    offset = 12
    while offset + 8 <= len(data):
        chunk_type = data[offset:offset + 4]
        chunk_size = int.from_bytes(data[offset + 4:offset + 8], "little")
        payload = offset + 8
        end = payload + chunk_size
        if end > len(data):
            fail(f"truncated WebP preview: {path.relative_to(DIST)}")
        chunk = data[payload:end]
        if chunk_type == b"VP8X" and len(chunk) >= 10:
            return (
                int.from_bytes(chunk[4:7], "little") + 1,
                int.from_bytes(chunk[7:10], "little") + 1,
            )
        if chunk_type == b"VP8 " and len(chunk) >= 10 and chunk[3:6] == b"\x9d\x01\x2a":
            return (
                int.from_bytes(chunk[6:8], "little") & 0x3FFF,
                int.from_bytes(chunk[8:10], "little") & 0x3FFF,
            )
        if chunk_type == b"VP8L" and len(chunk) >= 5 and chunk[0] == 0x2F:
            bits = int.from_bytes(chunk[1:5], "little")
            return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        offset = end + (chunk_size % 2)
    fail(f"WebP preview has no dimensions: {path.relative_to(DIST)}")


def check_catalog() -> None:
    catalog = load_json(DIST / "data" / "catalog.json")
    config = load_json(CONTENT / "notes-selection.json")
    expected_notes = [entry["path"] for entry in config["items"]]
    notes = catalog.get("collections", {}).get("notes", {}).get("items")
    if not isinstance(notes, list):
        fail("catalog is missing collections.notes.items")
    actual_notes = [entry.get("path") for entry in notes if isinstance(entry, dict)]
    if actual_notes != expected_notes or len(actual_notes) != len(notes):
        fail("catalog note paths do not exactly match content/notes-selection.json")
    for path in actual_notes:
        if not isinstance(path, str) or any(term in path.lower() for term in FORBIDDEN_NOTE_TERMS):
            fail(f"catalog includes excluded note path: {path}")
    featured = catalog.get("collections", {}).get("blog", {}).get("items", [])
    expected_featured = sorted((item for item in config["items"] if item.get("featured")), key=lambda item: item.get("featuredRank", 999))
    if [item.get("slug") for item in featured] != [item["slug"] for item in expected_featured]:
        fail("home featured articles do not match the selected reading list")

    gallery_config = load_json(CONTENT / "gallery-tags.json")
    gallery = catalog.get("gallery")
    if not isinstance(gallery, dict) or not isinstance(gallery.get("items"), list) or not isinstance(gallery.get("tags"), list):
        fail("catalog is missing gallery items or tags")
    tag_ids = [tag.get("id") for tag in gallery_config.get("tags", []) if isinstance(tag, dict)]
    if gallery.get("defaultTag") != gallery_config.get("defaultTag") or len(tag_ids) != len(set(tag_ids)):
        fail("gallery tag configuration is invalid or does not match catalog")

    expected_items: dict[tuple[str, str], dict] = {}
    collections = catalog.get("collections", {})
    for bucket in ("funny", "arknights"):
        collection = collections.get(bucket, {})
        for item in collection.get("items", []):
            if not isinstance(item, dict) or not item.get("preview"):
                continue
            source_path = item.get("path")
            if not isinstance(source_path, str):
                fail(f"{bucket} has an item without a path")
            tags = gallery_config.get("assignments", {}).get(bucket, {}).get(
                source_path, gallery_config.get("defaults", {}).get(bucket)
            )
            if not isinstance(tags, list) or not tags:
                fail(f"gallery configuration has no tags for {bucket}/{source_path}")
            expected_items[(bucket, source_path)] = {**item, "tags": tags}

    actual_items: dict[tuple[str, str], dict] = {}
    for item in gallery["items"]:
        if not isinstance(item, dict):
            fail("gallery includes a non-object item")
        key = (item.get("bucket"), item.get("path"))
        if not all(isinstance(part, str) for part in key) or key in actual_items:
            fail("gallery items must have unique bucket/path pairs")
        actual_items[key] = item
    if set(actual_items) != set(expected_items):
        fail("gallery items do not match previewable catalog items")

    counts = {tag_id: 0 for tag_id in tag_ids}
    for key, expected in expected_items.items():
        actual = actual_items[key]
        for field in ("preview", "previewWidth", "previewHeight", "original"):
            if actual.get(field) != expected.get(field):
                fail(f"gallery {key[0]}/{key[1]} has inconsistent {field}")
        tags = actual.get("tags")
        if tags != expected["tags"] or any(tag not in counts for tag in tags):
            fail(f"gallery {key[0]}/{key[1]} has inconsistent tags")
        preview = DIST / actual["preview"]
        if not preview.is_file():
            fail(f"gallery preview is missing: {actual['preview']}")
        if webp_dimensions(preview) != (actual["previewWidth"], actual["previewHeight"]):
            fail(f"gallery preview dimensions do not match metadata: {actual['preview']}")
        original_url = actual.get("original")
        if not isinstance(original_url, str):
            fail(f"gallery original is missing: {key[0]}/{key[1]}")
        original = (DIST / original_url).resolve()
        original_root = (DIST / "assets" / "originals" / key[0]).resolve()
        if not original.is_relative_to(original_root) or not original.is_file():
            fail(f"gallery original must be a published file in its bucket: {original_url}")
        for tag in tags:
            counts[tag] += 1
    catalog_counts = {tag.get("id"): tag.get("count") for tag in gallery["tags"] if isinstance(tag, dict)}
    if catalog_counts != counts:
        fail("gallery tag counts do not match gallery items")
    expected_originals = {item["original"] for item in actual_items.values()}
    published_originals = {path.relative_to(DIST).as_posix() for path in (DIST / "assets" / "originals").rglob("*") if path.is_file()}
    if published_originals != expected_originals:
        fail("published gallery originals must exactly match reviewed gallery items")


def check_moments() -> None:
    generated = load_json(DIST / "data" / "moments.json")
    posts = generated.get("posts")
    if not isinstance(posts, list):
        fail("moments catalog has no posts list")
    generated_by_id = {post.get("id"): post for post in posts if isinstance(post, dict)}
    if len(generated_by_id) != len(posts):
        fail("moments catalog has missing or duplicate post IDs")
    source_root = CONTENT / "moments"
    source_posts = sorted(path for path in source_root.iterdir() if path.is_dir())
    if set(generated_by_id) != {path.name for path in source_posts}:
        fail("generated moments do not exactly match source post folders")

    backup = DIST / "data" / "moments-backup.zip"
    if not backup.is_file():
        fail("moments backup ZIP is missing")
    try:
        with zipfile.ZipFile(backup) as archive:
            for folder in source_posts:
                source_metadata = folder / "post.json"
                source = load_json(source_metadata)
                generated_post = generated_by_id[folder.name]
                for field in ("id", "date", "title", "text"):
                    if generated_post.get(field) != source.get(field):
                        fail(f"generated moment {folder.name} does not match source {field}")
                images = source.get("images", [])
                rendered_images = generated_post.get("images", [])
                if not isinstance(images, list) or not isinstance(rendered_images, list) or len(images) > 9 or len(rendered_images) != len(images):
                    fail(f"moment {folder.name} must have matching zero to nine images")
                for image in rendered_images:
                    if not isinstance(image, dict) or not isinstance(image.get("src"), str):
                        fail(f"moment {folder.name} has invalid generated image metadata")
                    if not (DIST / image["src"]).is_file():
                        fail(f"moment {folder.name} generated image is missing: {image['src']}")
                member = f"content/moments/{folder.name}/post.json"
                try:
                    archived = archive.read(member)
                except KeyError:
                    fail(f"moments backup lacks {member}")
                if archived != source_metadata.read_bytes():
                    fail(f"moments backup metadata differs from {member}")
    except zipfile.BadZipFile as exc:
        fail(f"moments backup ZIP is invalid: {exc}")


def check_dist_safety() -> None:
    for path in DIST.rglob("*"):
        relative = path.relative_to(DIST)
        if SITES_METADATA_DIR in relative.parts:
            fail(f"dist contains Sites hosting metadata: {relative.as_posix()}")
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                fail(f"public text file is not UTF-8: {relative.as_posix()} ({exc})")
            is_original_article = relative.parts[:1] == ("articles",) or relative.parts[:2] == ("data", "articles")
            if DRIVE_PATH_PATTERN.search(text) and not is_original_article:
                fail(f"public text file exposes an absolute drive path: {relative.as_posix()}")
            if any(marker in text for marker in SITES_IDENTITY_PREFIXES):
                fail(f"public text file exposes a Sites platform identity: {relative.as_posix()}")


class ArticleMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.append((dict(attrs).get("id"), int(tag[1:])))
        if tag in {"script", "style", "iframe", "object", "embed", "form", "svg"}:
            fail(f"article includes active HTML tag: {tag}")
        for key, value in attrs:
            if key.lower().startswith("on"):
                fail("article includes an HTML event handler")
            if key == "id":
                if value in self.ids:
                    fail(f"article has a duplicate heading ID: {value}")
                self.ids.add(value)
            if key in {"href", "src"}:
                self.links.append(value or '')


def check_articles() -> None:
    selection = load_json(CONTENT / "notes-selection.json")["items"]
    notes = load_json(DIST / "data" / "catalog.json")["collections"]["notes"]["items"]
    expected = {entry["slug"]: entry for entry in selection}
    if len(expected) != len(selection):
        fail("article slugs must be unique")
    for note in notes:
        slug = note.get("slug")
        if slug not in expected or note.get("url") != f"article.html?id={slug}":
            fail("note entry does not link to its published article")
    for slug, entry in expected.items():
        article = load_json(DIST / "data" / "articles" / f"{slug}.json")
        source = CONTENT / "posts" / f"{slug}.md"
        published = DIST / "articles" / f"{slug}.md"
        if not source.is_file() or not published.is_file() or source.read_bytes() != published.read_bytes():
            fail(f"published Markdown differs from its reviewed source: {slug}")
        if article.get("slug") != slug or article.get("title") != entry["title"]:
            fail(f"missing or inconsistent rendered article: {slug}")
        if not article.get("sourceOriginal"):
            fail(f"article must be rendered from its original Markdown: {slug}")
        if article.get("markdownUrl") != f"articles/{slug}.md":
            fail(f"article has an invalid Markdown download URL: {slug}")
        if "chapters" in article:
            fail(f"article must be a single complete document: {slug}")
        markup = ArticleMarkup()
        if not article.get("html", '').strip():
            fail(f"article has no complete rendered body: {slug}")
        markup.feed(article["html"])
        toc = article.get("toc", [])
        if [(heading.get("id"), heading.get("level")) for heading in toc] != markup.headings:
            fail(f"table of contents must retain every heading's level and source order: {slug}")
        for heading in article.get("toc", []):
            if heading.get("id") not in markup.ids or not heading.get("text") or heading.get("level") not in range(1, 7):
                fail(f"article has a broken table of contents: {slug}")
        search_url = f"data/articles/{slug}/search.json"
        if article.get("searchUrl") != search_url:
            fail(f"article has no full-text index: {slug}")
        search = load_json(DIST / search_url)
        if search.get("slug") != slug or not isinstance(search.get("entries"), list) or not search["entries"]:
            fail(f"article full-text index is empty: {slug}")
        for hit in search["entries"]:
            if not isinstance(hit.get("text"), str) or not 0 < len(hit["text"]) <= 1600:
                fail(f"article search entry is invalid: {slug}")
            if hit.get("headingId") and hit["headingId"] not in markup.ids:
                fail(f"article search entry has no reachable heading: {slug}")
        for link in markup.links:
            parsed = urlsplit(link)
            if parsed.scheme and parsed.scheme.lower() not in {"http", "https", "mailto"}:
                fail(f"article has an unsafe URL: {slug}")
            if not parsed.scheme and not parsed.netloc and parsed.path:
                target = (DIST / unquote(parsed.path)).resolve()
                if not target.is_relative_to(DIST.resolve()) or not target.is_file():
                    fail(f"article has a broken local resource: {slug}")
        if entry.get("status") and article.get("status") != entry["status"]:
            fail(f"article has an inconsistent learning status: {slug}")
    if list((DIST / "data" / "articles").glob("*/chapter-*.json")):
        fail("retired chapter payloads must not remain in the publication")
    asset_manifest = load_json(CONTENT / "article-assets.json")["articles"]
    for assets in asset_manifest.values():
        for url in assets.values():
            relative = Path(url)
            if relative.parts[:1] != ("article-assets",) or ".." in relative.parts:
                fail("article asset must remain in its public assets folder")
            source_asset = CONTENT / relative
            published_asset = DIST / relative
            if not source_asset.is_file() or not published_asset.is_file() or source_asset.read_bytes() != published_asset.read_bytes():
                fail(f"article image does not match its original source: {url}")


def check_reflections() -> None:
    entries = [load_json(path) for path in (CONTENT / "reflections").glob("*.json")]
    about = (DIST / "about.html").read_text(encoding="utf-8")
    index = (DIST / "thoughts.html").read_text(encoding="utf-8")
    for entry in entries:
        page = DIST / f"thought-{entry['slug']}.html"
        if not page.is_file():
            fail(f"reflection has no reading page: {entry['slug']}")
        body = page.read_text(encoding="utf-8")
        if page.name not in index:
            fail(f"reflection index is missing an entry: {entry['slug']}")
        for paragraph in entry["paragraphs"]:
            encoded = html.escape(paragraph, quote=True)
            if encoded not in body or encoded in about:
                fail(f"reflection must retain full text separately from About: {entry['slug']}")


def main() -> None:
    if not DIST.is_dir():
        fail("dist directory is missing")
    missing = [page for page in EXPECTED_PAGES if not (DIST / page).is_file()]
    if missing:
        fail(f"missing expected HTML pages: {', '.join(missing)}")
    if (CONTENT / "site-icon.jpg").read_bytes() != (DIST / "favicon.jpg").read_bytes():
        fail("published site icon does not match the selected avatar")
    for page in DIST.glob("*.html"):
        if "<span>JOIN</span>" in page.read_text(encoding="utf-8"):
            fail(f"contact navigation still uses JOIN: {page.name}")
    check_dist_safety()
    check_html_references()
    check_catalog()
    check_moments()
    check_articles()
    check_reflections()
    print("Site artifact checks passed.")


if __name__ == "__main__":
    try:
        main()
    except SiteError as exc:
        print(f"Site check failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
