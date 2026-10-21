"""Load and render the small, data-backed collection of personal reflections."""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
REQUIRED_FIELDS = ("slug", "title", "publishedAt", "excerpt", "paragraphs")


def fail(message: str) -> ValueError:
    return ValueError(f"Invalid reflection content: {message}")


def _text(value: str) -> str:
    return html.escape(value, quote=True)


def _entry(path: Path) -> dict:
    try:
        entry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise fail(f"cannot read {path.name}: {exc}") from exc
    if not isinstance(entry, dict):
        raise fail(f"{path.name} must contain an object")
    missing = [field for field in REQUIRED_FIELDS if field not in entry]
    if missing:
        raise fail(f"{path.name} is missing: {', '.join(missing)}")
    slug = entry["slug"]
    if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
        raise fail(f"{path.name} has an invalid slug")
    for field in ("title", "publishedAt", "excerpt"):
        if not isinstance(entry[field], str) or not entry[field].strip():
            raise fail(f"{slug}: {field} must be a non-empty string")
    try:
        dt.date.fromisoformat(entry["publishedAt"])
    except ValueError as exc:
        raise fail(f"{slug}: publishedAt must use YYYY-MM-DD") from exc
    if not isinstance(entry["paragraphs"], list) or not entry["paragraphs"]:
        raise fail(f"{slug}: paragraphs must be a non-empty list")
    if any(not isinstance(paragraph, str) or not paragraph.strip() for paragraph in entry["paragraphs"]):
        raise fail(f"{slug}: paragraphs must contain non-empty strings")
    if "order" in entry and (not isinstance(entry["order"], int) or isinstance(entry["order"], bool)):
        raise fail(f"{slug}: order must be an integer when present")
    return entry


def load_reflections(root: Path = ROOT) -> list[dict]:
    """Return validated reflections, newest first and explicit order second."""
    directory = Path(root) / "content" / "reflections"
    if not directory.is_dir():
        raise fail("content/reflections directory is missing")
    entries = [_entry(path) for path in directory.glob("*.json")]
    slugs = [entry["slug"] for entry in entries]
    if len(slugs) != len(set(slugs)):
        raise fail("reflection slugs must be unique")
    return sorted(entries, key=lambda entry: (entry["publishedAt"], -entry.get("order", 0), entry["slug"]), reverse=True)


def _card(entry: dict) -> str:
    return f'''<article class="thought-card" id="{_text(entry['slug'])}">
  <p class="eyebrow">收录于 {_text(entry['publishedAt'])}</p>
  <h3>{_text(entry['title'])}</h3>
  <p>{_text(entry['excerpt'])}</p>
  <a class="profile-inline-link" href="thought-{_text(entry['slug'])}.html">读全文 <span>↗</span></a>
</article>'''


def render_thoughts_index(entries: list[dict] | None = None) -> str:
    """Return the all-reflections page body without shared chrome."""
    if entries is None:
        entries = load_reflections()
    cards = "".join(_card(entry) for entry in entries)
    return f'''<section class="thoughts-hero wrap">
  <p class="eyebrow">REFLECTIONS</p><h1>随想，慢慢写。</h1>
  <p>把一时想明白的事留在这里，也允许它在以后被重新理解。</p>
</section>
<section class="thoughts-list wrap">{cards}</section>'''


def render_thought(entry: dict) -> str:
    """Return one reflection body without shared chrome."""
    paragraphs = "".join(f"<p>{_text(paragraph)}</p>" for paragraph in entry["paragraphs"])
    return f'''<article class="thought-detail wrap">
  <a class="profile-inline-link" href="thoughts.html">← 全部随想</a>
  <header><p class="eyebrow">收录于 {_text(entry['publishedAt'])}</p><h1>{_text(entry['title'])}</h1></header>
  <div class="thought-detail-prose">{paragraphs}</div>
</article>'''
