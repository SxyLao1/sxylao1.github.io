import importlib
import json
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
about = importlib.import_module("about_content")
reflections = importlib.import_module("reflection_content")


class Identifiers(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        self.ids.extend(value for key, value in attrs if key == "id")


class ReflectionTests(unittest.TestCase):
    def test_more_reflections_keep_about_compact_and_all_full_text_reachable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "content" / "reflections").mkdir(parents=True)
            for name in ("profile.json", "notes-selection.json"):
                (root / "content" / name).write_bytes((ROOT / "content" / name).read_bytes())
            for index in range(4):
                entry = {"slug": f"reflection-{index}", "title": f"Thought {index}", "publishedAt": f"2026-10-{20 + index}", "excerpt": f"Short excerpt {index}", "paragraphs": [f"Complete separate paragraph {index} <script>text only</script>"]}
                (root / "content" / "reflections" / f"{index}.json").write_text(json.dumps(entry), encoding="utf-8")
            entries = reflections.load_reflections(root)
            with patch.object(about, "ROOT", root), patch.object(about, "PROFILE_PATH", root / "content" / "profile.json"):
                body = about.render_about()
            self.assertEqual(body.count('class="profile-reflection-card"'), 2)
            self.assertIn("thought-reflection-3.html", body)
            self.assertIn("thought-reflection-2.html", body)
            self.assertNotIn("Complete separate paragraph", body)
            self.assertIn('href="#reflections"', body)
            identifiers = Identifiers()
            identifiers.feed(body)
            self.assertEqual(len(identifiers.ids), len(set(identifiers.ids)))
            index = reflections.render_thoughts_index(entries)
            for entry in entries:
                detail = reflections.render_thought(entry)
                self.assertIn(f"thought-{entry['slug']}.html", index)
                self.assertEqual(detail.count("<h1>"), 1)
                self.assertIn("&lt;script&gt;text only&lt;/script&gt;", detail)
                self.assertNotIn("<script>", detail)

    def test_invalid_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / "content" / "reflections"
            directory.mkdir(parents=True)
            (directory / "bad.json").write_text('{"slug":"../escape"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                reflections.load_reflections(root)


if __name__ == "__main__":
    unittest.main()
