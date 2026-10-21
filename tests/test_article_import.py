import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "import_articles.py"
SPEC = importlib.util.spec_from_file_location("import_articles", SCRIPT)
article_import = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(article_import)


class ArticleImportTests(unittest.TestCase):
    def make_site(self, source_bytes=b"# Title\r\n"):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        notes = root / "notes"
        notes.mkdir()
        (notes / "Original.md").write_bytes(source_bytes)
        (root / "content").mkdir()
        (root / "dist").mkdir()
        (root / "content" / "notes-selection.json").write_text(
            json.dumps({"items": [{"path": "Original.md", "slug": "safe-article"}]}), encoding="utf-8")
        return temporary, root, notes

    def test_copies_original_crlf_bytes_exactly(self):
        source = b"# Title\r\n\r\nText\r\n"
        temporary, root, notes = self.make_site(source)
        with temporary:
            result = article_import.build(root=root, notes_root=notes)
            self.assertEqual(result["articles"], ["safe-article"])
            self.assertEqual((root / "content" / "posts" / "safe-article.md").read_bytes(), source)

    def test_relative_configured_notes_root_is_relative_to_site_root(self):
        temporary, root, notes = self.make_site()
        with temporary:
            (root / ".local").mkdir()
            (root / ".local" / "sources.json").write_text(json.dumps({"notes": "notes"}), encoding="utf-8")
            result = article_import.build(root=root)
            self.assertEqual(result["articles"], ["safe-article"])

    def test_copies_relative_png_and_uses_hashed_source_key(self):
        image = b"not-a-real-png-but-copied-as-bytes"
        markdown = b"![sample](images/demo.png)\n"
        temporary, root, notes = self.make_site(markdown)
        with temporary:
            (notes / "images").mkdir()
            (notes / "images" / "demo.png").write_bytes(image)
            article_import.build(root=root, notes_root=notes)
            source_hash = hashlib.sha256(b"images/demo.png").hexdigest()
            image_hash = hashlib.sha256(image).hexdigest()[:20]
            relative = f"article-assets/safe-article/{image_hash}.png"
            manifest = json.loads((root / "content" / "article-assets.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest, {"articles": {"safe-article": {source_hash: relative}}})
            self.assertEqual((root / "content" / relative).read_bytes(), image)
            self.assertEqual((root / "dist" / relative).read_bytes(), image)
            self.assertNotIn(str(notes), (root / "content" / "article-assets.json").read_text(encoding="utf-8"))

    def test_remote_image_is_ignored_without_network_access(self):
        temporary, root, notes = self.make_site(b"![remote](https://example.invalid/a.png)\n")
        with temporary:
            result = article_import.build(root=root, notes_root=notes)
            self.assertEqual(result["missingImages"], [])
            manifest = json.loads((root / "content" / "article-assets.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest, {"articles": {"safe-article": {}}})

    def test_missing_local_image_is_counted_without_exposing_its_path(self):
        temporary, root, notes = self.make_site(b"![missing](images/not-here.png)\n")
        with temporary:
            result = article_import.build(root=root, notes_root=notes)
            self.assertEqual(result["missingImages"], [{"slug": "safe-article", "count": 1}])

    def test_traversal_is_rejected_before_prior_output_changes(self):
        temporary, root, notes = self.make_site()
        with temporary:
            (root / "content" / "posts").mkdir()
            previous = root / "content" / "posts" / "safe-article.md"
            previous.write_bytes(b"previous output")
            (root / "content" / "notes-selection.json").write_text(
                json.dumps({"items": [{"path": "../escape.md", "slug": "safe-article"}]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                article_import.build(root=root, notes_root=notes)
            self.assertEqual(previous.read_bytes(), b"previous output")


if __name__ == "__main__":
    unittest.main()
