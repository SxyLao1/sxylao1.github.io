"""Render the About body from the author-maintained profile source."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "content" / "profile.json"


def _text(value: object) -> str:
    return html.escape(str(value), quote=True)


def _items(values: list[str]) -> str:
    return "".join(f"<li>{_text(value)}</li>" for value in values)


def render_about() -> str:
    """Return the About page body without the shared page header or footer."""
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    identity = profile["identity"]
    interests = profile["interests"]
    selection = json.loads((ROOT / "content" / "notes-selection.json").read_text(encoding="utf-8"))
    article_slugs = {Path(note["path"]).name: note["slug"] for note in selection["items"]}

    reflection = "".join(f"<p>{_text(paragraph)}</p>" for paragraph in profile["reflection"])
    acceptance = profile["acceptance"]
    acceptance_prose = "".join(f"<p>{_text(paragraph)}</p>" for paragraph in acceptance["paragraphs"])
    plans = "".join(
        "<li class=\"profile-plan\">"
        f"<a class=\"text-link\" href=\"article.html?id={quote(article_slugs[plan['name']])}\">{_text(plan.get('title', plan['name']))}<span>↗</span></a>"
        f"<p>{_text(plan['description'])}</p><small>{_text(plan['status'])}</small></li>"
        for plan in profile["learningPlans"]
    )

    title = "<br>".join(_text(line) for line in identity["title"].splitlines())
    return f'''<section class="profile-hero wrap">
  <div><p class="eyebrow">{_text(identity['eyebrow'])}</p><h2>{title}</h2></div>
  <p class="profile-lead">{_text(identity['intro'])}</p>
</section>
<nav class="profile-outline wrap" aria-label="关于我目录"><a href="#self-cultivation">修己</a><a href="#acceptance">与自己和解</a><a href="#interests">兴趣</a><a href="#learning">学习计划</a><a href="#desktop">桌面折腾</a></nav>
<section class="profile-story wrap" id="self-cultivation">
  <div class="profile-aside"><p class="eyebrow">A CURRENT VIEW</p><span>01</span></div>
  <div class="profile-prose"><h2>修己，是我理解的成长。</h2>{reflection}</div>
</section>
<section class="profile-story wrap" id="acceptance">
  <div class="profile-aside"><p class="eyebrow">LEARNING TO BE AT EASE</p><span>02</span></div>
  <div class="profile-prose"><h2>{_text(acceptance['title'])}</h2>{acceptance_prose}</div>
</section>
<section class="profile-interests wrap" id="interests">
  <div class="profile-section-title"><p class="eyebrow">THINGS I LOVE</p><h2>喜欢的事，慢慢收集。</h2></div>
  <div class="profile-interest-grid">
    <article><h3>游戏</h3><ul>{_items(interests['games'])}</ul></article>
    <article><h3>日漫</h3><ul>{_items(interests['animeJapan'])}</ul></article>
    <article><h3>国漫</h3><ul>{_items(interests['animeChina'])}</ul></article>
    <article><h3>书</h3><ul>{_items(interests['books'])}</ul></article>
  </div>
</section>
<section class="profile-learning wrap" id="learning">
  <div class="profile-section-title"><p class="eyebrow">NOT STARTED YET</p><h2>想学的方向，还在起点。</h2><p>计划已经写下，还没有真正开始。把方向留在这里，也提醒自己：下一步，是从一件能做的小事开始。</p></div>
  <ol>{plans}</ol>
</section>
<section class="profile-desktop wrap" id="desktop">
  <p class="eyebrow">A DESKTOP MADE MINE</p><h2>也会把 Windows 桌面<br>调成顺手的样子。</h2><p>{_text(profile['desktop'])}</p>
</section>
<section class="profile-history wrap">
  <div><p class="eyebrow">ABOUT THIS WEBSITE</p><h2>从旧主页，继续往前。</h2></div>
  <div><p>{_text(profile['siteHistory'])}</p><small>{_text(profile['attribution'])}</small></div>
</section>'''


if __name__ == "__main__":
    print(render_about())
