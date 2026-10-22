import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_articles.py"
SPEC = importlib.util.spec_from_file_location("build_articles", SCRIPT)
articles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(articles)


class ArticleBuildTests(unittest.TestCase):
    def make_site(self, markdown="# Visible title\n\n## Section\n\nA paragraph."):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "content" / "posts").mkdir(parents=True)
        (root / "dist" / "data").mkdir(parents=True)
        selection = {"items": [{"path": "Original.md", "slug": "safe-article", "title": "Reader title", "summary": "A reviewed summary.", "category": "Test", "section": "Test section"}]}
        (root / "content" / "notes-selection.json").write_text(json.dumps(selection), encoding="utf-8")
        catalog = {"collections": {"notes": {"items": [{"path": "Original.md", "modifiedAt": "2026-10-22"}]}}}
        (root / "dist" / "data" / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
        (root / "content" / "posts" / "safe-article.md").write_text(markdown, encoding="utf-8", newline="")
        return temporary, root

    def test_renders_original_headings_math_tables_code_and_safe_links(self):
        markdown = r'''# Original title

## Section

### Detail

| Key | Value |
| --- | --- |
| a | b |

```text
C:\private\note.md and [bad](javascript:alert(1)) are documentation examples.
```

Inline $\frac{a}{b}$.

$$
\mathbf{x}
$$

[http](http://example.com) [https](https://example.com) [mail](mailto:test@example.com)

Soft line one
Soft line two

```text
code line one
code line two
```

<script>alert('no')</script>
'''
        temporary, root = self.make_site(markdown)
        with temporary:
            output = articles.build(root)[0]
            self.assertEqual([item["id"] for item in output["toc"]], ["section-1", "section-2", "section-3"])
            self.assertIn('<h1 id="section-1">Original title</h1>', output["html"])
            self.assertIn("<table>", output["html"])
            self.assertIn("C:\\private\\note.md", output["html"])
            self.assertIn('<span class="math inline">\\frac{a}{b}</span>', output["html"])
            self.assertIn('<div class="math block">\n\\mathbf{x}\n</div>', output["html"])
            self.assertIn('href="http://example.com"', output["html"])
            self.assertIn('href="https://example.com"', output["html"])
            self.assertIn('href="mailto:test@example.com"', output["html"])
            self.assertIn('rel="noopener noreferrer"', output["html"])
            self.assertIn("Soft line one<br />\nSoft line two", output["html"])
            self.assertIn("code line one\ncode line two", output["html"])
            self.assertIn("&lt;script&gt;", output["html"])
            published = json.loads((root / "dist" / "data" / "articles" / "safe-article.json").read_text(encoding="utf-8"))
            self.assertTrue(published["sourceOriginal"])
            self.assertEqual(published["modifiedAt"], "2026-10-22")

    def test_large_article_keeps_full_html_all_heading_levels_and_search_index(self):
        parts = ["# Start\n\n## Second\n\n### Third\n\n#### Fourth\n\n##### Fifth\n\n###### Sixth\n\n"]
        for number in range(22):
            parts.append(f"## Section {number}\n\n" + (f"paragraph-{number} " * 900) + "\n\n")
        parts.append("## Last Section\n\n```text\nCODE-FINAL\n```\n\n$$\n\\omega\n$$\n")
        temporary, root = self.make_site("".join(parts))
        with temporary:
            article = articles.build(root)[0]
            self.assertNotIn("chapters", article)
            self.assertEqual([item["level"] for item in article["toc"][:6]], [1, 2, 3, 4, 5, 6])
            self.assertIn("paragraph-0", article["html"])
            self.assertIn("paragraph-21", article["html"])
            search = json.loads((root / "dist" / article["searchUrl"]).read_text(encoding="utf-8"))
            self.assertTrue(any("CODE-FINAL" in item["text"] for item in search["entries"]))
            self.assertTrue(any("\\omega" in item["text"] for item in search["entries"]))
            self.assertTrue(any("Last Section" in item["text"] for item in search["entries"]))
            self.assertTrue(all(len(item["text"]) <= 1600 for item in search["entries"]))

    def test_search_entries_keep_continuous_heading_context(self):
        temporary, root = self.make_site("# First\n\nintro\n\n## Last\n\n```text\nCODE-BLOCK\n```\n\n$$\n\\omega\n$$\n")
        with temporary:
            article = articles.build(root)[0]
            search = json.loads((root / "dist" / article["searchUrl"]).read_text(encoding="utf-8"))
            last_entries = [entry for entry in search["entries"] if "CODE-BLOCK" in entry["text"] or "\\omega" in entry["text"]]
            self.assertTrue(last_entries)
            self.assertTrue(all(entry["headingId"] == "section-2" for entry in last_entries))

    def test_original_crlf_and_actual_unsafe_destinations_are_preserved_or_inert(self):
        source_bytes = b"# Title\r\n\r\n[unsafe](javascript:alert(1)) ![missing](file:///C:/private.png)\r\n"
        temporary, root = self.make_site()
        with temporary:
            source = root / "content" / "posts" / "safe-article.md"
            source.write_bytes(source_bytes)
            output = articles.build(root)[0]
            self.assertIn("unsafe", output["html"])
            self.assertNotIn("javascript:", output["html"])
            self.assertNotIn("file:///", output["html"])
            self.assertIn('class="image-unavailable"', output["html"])
            self.assertEqual((root / "dist" / "articles" / "safe-article.md").read_bytes(), source_bytes)

    def test_missing_relative_links_are_inert_and_selected_markdown_and_heading_links_resolve(self):
        temporary, root = self.make_site("# Heading\n\n[missing](missing.txt) [selected](Original.md) [jump](#heading)")
        with temporary:
            output = articles.build(root)[0]["html"]
            self.assertNotIn('href="missing.txt"', output)
            self.assertIn('href="article.html?id=safe-article"', output)
            self.assertIn('href="#section-1"', output)

    def test_manifest_maps_local_image_and_unmapped_escape_is_inert(self):
        temporary, root = self.make_site("![mapped](C:\\Pictures\\demo.png) ![escape](../private.png)")
        with temporary:
            raw = r"C:\Pictures\demo.png"
            digest = articles.hashlib.sha256(raw.encode("utf-8")).hexdigest()
            asset = root / "dist" / "article-assets" / "safe-article" / "demo.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"image")
            manifest = {"articles": {"safe-article": {digest: "article-assets/safe-article/demo.png"}}}
            (root / "content" / "article-assets.json").write_text(json.dumps(manifest), encoding="utf-8")
            output = articles.build(root)[0]["html"]
            self.assertIn('src="article-assets/safe-article/demo.png"', output)
            self.assertIn('loading="lazy"', output)
            self.assertIn('decoding="async"', output)
            self.assertIn('referrerpolicy="no-referrer"', output)
            self.assertIn('class="image-unavailable"', output)

    def test_missing_or_invalid_selected_posts_fail_before_outputs_change(self):
        temporary, root = self.make_site()
        with temporary:
            target = root / "dist" / "data" / "articles"
            target.mkdir(parents=True)
            previous = target / "safe-article.json"
            previous.write_text('{"old": true}\n', encoding="utf-8")
            selection = json.loads((root / "content" / "notes-selection.json").read_text(encoding="utf-8"))
            selection["items"][0]["slug"] = "INVALID"
            (root / "content" / "notes-selection.json").write_text(json.dumps(selection), encoding="utf-8")
            with self.assertRaises(ValueError):
                articles.build(root)
            self.assertEqual(previous.read_text(encoding="utf-8"), '{"old": true}\n')

            selection["items"][0]["slug"] = "missing-post"
            (root / "content" / "notes-selection.json").write_text(json.dumps(selection), encoding="utf-8")
            with self.assertRaises(ValueError):
                articles.build(root)
            self.assertEqual(previous.read_text(encoding="utf-8"), '{"old": true}\n')


if __name__ == "__main__":
    unittest.main()
