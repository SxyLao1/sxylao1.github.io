"""Compile the reviewed Markdown articles into safe static reader payloads."""
from __future__ import annotations

import html
import json
import math
import os
import re
import tempfile
import hashlib
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin


ROOT = Path(__file__).resolve().parents[1]
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DRIVE_PATH_PATTERN = re.compile(r"(?<![A-Za-z0-9+.-])[A-Za-z]:[\\/]")


def fail(message: str) -> ValueError:
    return ValueError(f"Invalid article content: {message}")


def load_json(path: Path, label: str):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise fail(f"cannot read {label}: {exc}") from exc
    if not isinstance(data, dict):
        raise fail(f"{label} must contain an object")
    return data


def safe_relative_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise fail(f"{label} must be a non-empty string")
    normalized = value.replace("\\", "/")
    path = Path(normalized)
    if path.is_absolute() or DRIVE_PATH_PATTERN.search(value) or any(part == ".." for part in path.parts):
        raise fail(f"{label} must be a relative path inside the reviewed source")
    return normalized


def article_markdown(selection: dict, site_root: Path) -> tuple[str, bytes, Path]:
    slug = selection["slug"]
    source = site_root / "content" / "posts" / f"{slug}.md"
    try:
        source.resolve(strict=True).relative_to((site_root / "content" / "posts").resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise fail(f"{slug}: article source escapes content/posts") from exc
    if not source.is_file():
        raise fail(f"{slug}: missing content/posts/{slug}.md")
    try:
        markdown_bytes = source.read_bytes()
        markdown = markdown_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise fail(f"{slug}: Markdown must be UTF-8") from exc
    return markdown, markdown_bytes, source


def url_kind(value: str, *, target_dir: Path, dist: Path, image: bool) -> str:
    """Classify a rendered destination without inspecting or following it."""
    candidate = html.unescape(unquote(value)).strip()
    if not candidate or any(ord(char) < 32 for char in candidate):
        return "unsafe"
    parsed = urlsplit(candidate)
    if parsed.scheme:
        scheme = parsed.scheme.lower()
        if scheme in {"http", "https"} and parsed.netloc:
            return "external"
        if not image and scheme == "mailto" and parsed.path:
            return "mailto"
        return "unsafe"
    if parsed.netloc or candidate.startswith("//"):
        return "unsafe"
    if parsed.path:
        target = (target_dir / unquote(parsed.path)).resolve(strict=False)
        try:
            target.relative_to(dist.resolve())
        except ValueError as exc:
            return "unsafe"
        if not target.is_file():
            return "missing"
    return "relative"


def make_markdown_renderer(target_dir: Path, dist: Path) -> MarkdownIt:
    renderer = MarkdownIt("commonmark", {"html": False, "linkify": False}).enable(["table", "strikethrough"])
    # Parse all explicit Markdown links so unsafe destinations can display their
    # label as inert text instead of leaving source syntax in the reader.
    renderer.validateLink = lambda value: True

    def render_math(tex: str, options: dict) -> str:
        escaped = html.escape(tex)
        if options.get("display_mode"):
            return f'<div class="math block">{escaped}</div>'
        return f'<span class="math inline">{escaped}</span>'

    renderer.use(dollarmath_plugin, renderer=render_math)

    def link_open(tokens, index, options, env):
        token = tokens[index]
        href = token.attrGet("href") or ""
        if (token.meta or {}).get("inert"):
            return ""
        kind = url_kind(href, target_dir=target_dir, dist=dist, image=False)
        if kind in {"external", "mailto"}:
            token.attrSet("rel", "noopener noreferrer")
        if kind == "external":
            token.attrSet("target", "_blank")
        return self_render(tokens, index, options, env)

    # Capture the standard rules before replacing them.
    self_render = renderer.renderer.rules.get("link_open", renderer.renderer.renderToken)
    renderer.renderer.rules["link_open"] = link_open
    self_render_image = renderer.renderer.rules.get("image")

    def safe_image(tokens, index, options, env):
        token = tokens[index]
        src = token.attrGet("src") or ""
        if (token.meta or {}).get("inert"):
            alt = token.content or token.attrGet("title") or "原文图片暂缺"
            return f'<span class="image-unavailable">{html.escape(alt)}</span>'
        kind = url_kind(src, target_dir=target_dir, dist=dist, image=True)
        if kind not in {"external", "relative"}:
            return f'<span class="image-unavailable">{html.escape(token.content or "原文图片暂缺")}</span>'
        token.attrSet("loading", "lazy")
        token.attrSet("decoding", "async")
        token.attrSet("referrerpolicy", "no-referrer")
        return self_render_image(tokens, index, options, env)

    renderer.renderer.rules["image"] = safe_image
    return renderer


def inline_text(renderer: MarkdownIt, token) -> str:
    rendered = renderer.renderInline(token.content)
    return html.unescape(re.sub(r"<[^>]*>", "", rendered)).strip()


def image_manifest(site_root: Path, slug: str) -> dict[str, str]:
    manifest_path = site_root / "content" / "article-assets.json"
    if not manifest_path.is_file():
        return {}
    manifest = load_json(manifest_path, "content/article-assets.json")
    articles = manifest.get("articles", {})
    mapping = articles.get(slug, {}) if isinstance(articles, dict) else {}
    if not isinstance(mapping, dict):
        return {}
    return {key: value for key, value in mapping.items() if isinstance(key, str) and isinstance(value, str)}


def heading_alias(text: str, used: dict[str, int]) -> str:
    base = re.sub(r"[^\w\-\u4e00-\u9fff ]", "", text.casefold()).strip()
    base = re.sub(r"[\s-]+", "-", base) or "section"
    count = used.get(base, 0)
    used[base] = count + 1
    return base if count == 0 else f"{base}-{count}"


def prepare_inline_tokens(tokens, renderer: MarkdownIt, *, asset_map: dict[str, str], article_urls: dict[str, str], anchor_ids: dict[str, str], target_dir: Path, dist: Path) -> None:
    for token in tokens:
        if token.type != "inline" or not token.children:
            continue
        link_stack = []
        for child in token.children:
            if child.type == "link_open":
                href = child.attrGet("href") or ""
                parsed = urlsplit(href)
                mapped_article = False
                if not parsed.path and parsed.fragment in anchor_ids:
                    child.attrSet("href", f"#{anchor_ids[parsed.fragment]}")
                elif parsed.path.lower().endswith(".md"):
                    replacement = article_urls.get(Path(unquote(parsed.path)).name.casefold())
                    if replacement:
                        child.attrSet("href", replacement + (f"#{parsed.fragment}" if parsed.fragment else ""))
                        mapped_article = True
                safe = mapped_article or url_kind(child.attrGet("href") or "", target_dir=target_dir, dist=dist, image=False) in {"external", "mailto", "relative"}
                child.meta = {"inert": not safe}
                link_stack.append(not safe)
            elif child.type == "link_close":
                child.meta = {"inert": link_stack.pop() if link_stack else True}
            elif child.type == "image":
                source = child.attrGet("src") or ""
                candidates = (source, unquote(source))
                mapped = next((asset_map.get(hashlib.sha256(value.encode("utf-8")).hexdigest()) for value in candidates if asset_map.get(hashlib.sha256(value.encode("utf-8")).hexdigest())), None)
                if mapped is not None:
                    child.attrSet("src", mapped)
                kind = url_kind(child.attrGet("src") or "", target_dir=target_dir, dist=dist, image=True)
                child.meta = {"inert": kind not in {"external", "relative"}}


def render_article(markdown: str, *, slug: str, site_root: Path, dist: Path, article_urls: dict[str, str]) -> tuple[str, list[dict], int]:
    # Article HTML is inserted into dist/article.html, so relative references
    # resolve from the published site root. Markdown downloads stay in articles/.
    target_dir = dist
    renderer = make_markdown_renderer(target_dir, dist)
    tokens = renderer.parse(markdown)
    toc = []
    anchor_ids = {}
    used_aliases = {}
    heading_number = 0
    filtered = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.type == "heading_open":
            level = int(token.tag[1:])
            heading_number += 1
            heading_id = f"section-{heading_number}"
            token.attrSet("id", heading_id)
            if level in (1, 2, 3) and index + 1 < len(tokens) and tokens[index + 1].type == "inline":
                text = inline_text(renderer, tokens[index + 1])
                toc.append({"id": heading_id, "text": text, "level": level})
                anchor_ids[heading_alias(text, used_aliases)] = heading_id
        filtered.append(token)
        index += 1
    prepare_inline_tokens(filtered, renderer, asset_map=image_manifest(site_root, slug), article_urls=article_urls, anchor_ids=anchor_ids, target_dir=target_dir, dist=dist)
    html_output = renderer.renderer.render(filtered, renderer.options, {})
    word_count = len(re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]", markdown))
    return html_output, toc, max(1, math.ceil(word_count / 200))


def selected_articles(site_root: Path):
    selection = load_json(site_root / "content" / "notes-selection.json", "content/notes-selection.json")
    items = selection.get("items")
    if not isinstance(items, list):
        raise fail("content/notes-selection.json requires an items list")
    seen_slugs = set()
    validated = []
    for entry in items:
        if not isinstance(entry, dict):
            raise fail("selection items must be objects")
        slug = entry.get("slug")
        if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug) or slug in seen_slugs:
            raise fail(f"invalid or duplicate article slug: {slug!r}")
        seen_slugs.add(slug)
        path = safe_relative_path(entry.get("path"), f"{slug}: path")
        required = ("title", "summary", "category", "section")
        if any(not isinstance(entry.get(field), str) or not entry[field].strip() for field in required):
            raise fail(f"{slug}: title, summary, category, and section must be non-empty strings")
        if "status" in entry and (not isinstance(entry["status"], str) or not entry["status"].strip()):
            raise fail(f"{slug}: status must be a non-empty string when present")
        validated.append({**entry, "path": path})
    return validated


def catalog_modified_dates(site_root: Path) -> dict[str, str]:
    catalog_path = site_root / "dist" / "data" / "catalog.json"
    if not catalog_path.is_file():
        return {}
    catalog = load_json(catalog_path, "dist/data/catalog.json")
    notes = catalog.get("collections", {}).get("notes", {}).get("items", [])
    if not isinstance(notes, list):
        return {}
    return {item["path"]: item["modifiedAt"] for item in notes if isinstance(item, dict)
            and isinstance(item.get("path"), str) and isinstance(item.get("modifiedAt"), str)}


def build(root: Path = ROOT):
    """Validate every selected Markdown source, then replace its generated outputs."""
    site_root = Path(root)
    dist = site_root / "dist"
    selected = selected_articles(site_root)
    article_urls = {Path(item["path"]).name.casefold(): f"article.html?id={item['slug']}" for item in selected}
    modified_dates = catalog_modified_dates(site_root)
    rendered = []
    for selection in selected:
        markdown, markdown_bytes, _ = article_markdown(selection, site_root)
        body, toc, minutes = render_article(markdown, slug=selection["slug"], site_root=site_root, dist=dist, article_urls=article_urls)
        article = {
            "slug": selection["slug"], "title": selection["title"], "summary": selection["summary"],
            "category": selection["category"], "html": body, "toc": toc,
            "readingMinutes": minutes, "markdownUrl": f"articles/{selection['slug']}.md", "sourceOriginal": True,
        }
        if selection["path"] in modified_dates:
            article["modifiedAt"] = modified_dates[selection["path"]]
        if "status" in selection:
            article["status"] = selection["status"]
        rendered.append((selection["slug"], markdown_bytes, article))

    data_dir = dist / "data" / "articles"
    markdown_dir = dist / "articles"
    data_dir.mkdir(parents=True, exist_ok=True)
    markdown_dir.mkdir(parents=True, exist_ok=True)
    staged = []
    try:
        for slug, markdown_bytes, article in rendered:
            with tempfile.NamedTemporaryFile(prefix=".article-", suffix=".json", dir=data_dir, delete=False, mode="w", encoding="utf-8", newline="") as handle:
                handle.write(json.dumps(article, ensure_ascii=False, indent=2) + "\n")
                staged.append((Path(handle.name), data_dir / f"{slug}.json"))
            with tempfile.NamedTemporaryFile(prefix=".article-", suffix=".md", dir=markdown_dir, delete=False, mode="wb") as handle:
                handle.write(markdown_bytes)
                staged.append((Path(handle.name), markdown_dir / f"{slug}.md"))
        for source, target in staged:
            os.replace(source, target)
        return [article for _, _, article in rendered]
    finally:
        for source, _ in staged:
            source.unlink(missing_ok=True)


def main():
    articles = build()
    print(f"Built {len(articles)} articles.")


if __name__ == "__main__":
    main()
