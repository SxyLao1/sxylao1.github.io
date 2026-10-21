"""Create a portable GitHub Pages ZIP from the generated ``dist`` directory."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import zipfile


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DEFAULT_OUTPUT = OUTPUTS_DIR / "github-pages-ready-20261022.zip"
EXCLUDED_PARTS = {".git", ".openai", ".staged", ".qa", "outputs"}
PACKAGE_README = """# Signal Archive GitHub Pages package

This ZIP contains only the generated static site from `dist/` plus `.nojekyll`.

Extract its contents into the root of the GitHub repository that will publish the
site. In GitHub repository Settings > Pages, select Deploy from a branch, then
choose the `main` branch and `/(root)` folder.

The site uses relative `.html` links, so it works for both a user or organization
site (`<username>.github.io`) and a project site (`<username>.github.io/<project>`).
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="ZIP output path under outputs/ (default: %(default)s)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the export without creating a ZIP",
    )
    return parser.parse_args()


def output_path(path: Path) -> Path:
    candidate = path if path.is_absolute() else PROJECT_ROOT / path
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(OUTPUTS_DIR.resolve())
    except ValueError as exc:
        raise ValueError("--output must be inside the project's outputs/ directory") from exc
    if resolved.suffix.lower() != ".zip":
        raise ValueError("--output must name a .zip file")
    return resolved


def dist_files() -> list[Path]:
    if not DIST_DIR.is_dir():
        raise FileNotFoundError(f"generated site directory is missing: {DIST_DIR}")

    root = DIST_DIR.resolve()
    files: list[Path] = []

    def visit(directory: Path) -> None:
        for entry in sorted(directory.iterdir(), key=lambda item: item.name):
            relative = entry.relative_to(DIST_DIR)
            if entry.name in EXCLUDED_PARTS or any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if entry.is_symlink():
                print(f"Skipping symlink: {relative}", file=sys.stderr)
                continue
            resolved = entry.resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                print(f"Skipping escaped entry: {relative}", file=sys.stderr)
                continue
            if entry.is_dir():
                visit(entry)
            elif entry.is_file():
                files.append(entry)

    visit(DIST_DIR)
    if not files:
        raise ValueError("generated site directory is empty")
    index = DIST_DIR / "index.html"
    if index.is_symlink() or not index.is_file() or index not in files:
        raise FileNotFoundError("generated site is missing dist/index.html")
    return files


def main() -> None:
    args = parse_args()
    target = output_path(args.output)
    files = dist_files()
    names = [file.relative_to(DIST_DIR).as_posix() for file in files]
    print(f"Validated {len(names)} files from dist/ for {target}")
    if args.dry_run:
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source, archive_name in zip(files, names, strict=True):
            archive.write(source, archive_name)
        archive.writestr(".nojekyll", "")
        archive.writestr("README.md", PACKAGE_README)
    print(f"Wrote {target}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
