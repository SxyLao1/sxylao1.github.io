import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_moments.py"
SPEC = importlib.util.spec_from_file_location("build_moments", SCRIPT)
moments = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(moments)


class MomentsBuildTests(unittest.TestCase):
    def make_site(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "content" / "moments").mkdir(parents=True)
        return temporary, root

    def write_post(self, root, post_id, date, image_count=0):
        folder = root / "content" / "moments" / post_id
        folder.mkdir()
        images = []
        for index in range(image_count):
            filename = f"photo-{index}.png"
            Image.new("RGB", (20 + index, 10), color=(index, 0, 0)).save(folder / filename)
            images.append(filename)
        (folder / "post.json").write_text(json.dumps({
            "id": post_id, "date": date, "title": post_id, "text": "A plain text entry.",
            "tags": ["test"], "images": images,
        }), encoding="utf-8")
        return folder

    def test_zero_one_and_nine_photos_are_catalogued_and_dates_descend(self):
        temporary, root = self.make_site()
        with temporary:
            self.write_post(root, "zero", "2026-01-01", 0)
            self.write_post(root, "nine", "2026-03-01", 9)
            self.write_post(root, "one", "2026-02-01", 1)
            result = moments.build(root, generated_at="2026-10-22")

            self.assertEqual([post["id"] for post in result["posts"]], ["nine", "one", "zero"])
            self.assertEqual([len(post["images"]) for post in result["posts"]], [9, 1, 0])
            self.assertEqual(len({image["src"] for post in result["posts"] for image in post["images"]}), 10)
            self.assertTrue((root / "dist" / "data" / "moments-backup.zip").is_file())

    def test_traversal_and_more_than_nine_images_are_rejected_before_catalogue_replacement(self):
        temporary, root = self.make_site()
        with temporary:
            data_dir = root / "dist" / "data"
            data_dir.mkdir(parents=True)
            catalogue = data_dir / "moments.json"
            catalogue.write_text('{"old": true}\n', encoding="utf-8")
            folder = self.write_post(root, "bad", "2026-01-01", 1)
            metadata = json.loads((folder / "post.json").read_text(encoding="utf-8"))
            metadata["images"] = ["../outside.png"]
            (folder / "post.json").write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaises(ValueError):
                moments.build(root, generated_at="2026-10-22")
            self.assertEqual(catalogue.read_text(encoding="utf-8"), '{"old": true}\n')

            metadata["images"] = [f"photo-{index}.png" for index in range(10)]
            (folder / "post.json").write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaises(ValueError):
                moments.build(root, generated_at="2026-10-22")
            self.assertEqual(catalogue.read_text(encoding="utf-8"), '{"old": true}\n')


if __name__ == "__main__":
    unittest.main()
