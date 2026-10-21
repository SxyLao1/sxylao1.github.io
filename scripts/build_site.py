"""Build the directory-backed personal site and its portable Moments backup."""
from build_catalog import main as build_catalog
from build_moments import build as build_moments
from build_pages import main as build_pages


if __name__ == "__main__":
    build_catalog()
    moments = build_moments()
    build_pages()
    print(f"Built site with {len(moments['posts'])} Moments posts.")
