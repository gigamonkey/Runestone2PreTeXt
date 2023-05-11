from pathlib import Path
import sys
import os
import shutil

IMG_EXTS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".pdf",
    ".eps",
    ".tif",
    ".tiff",
    ".bmp",
]


def copy_figs(sourcedir: Path, destdir: Path) -> None:
    """
    Recursively copies figures in sourcedir to external dir, retaining directory structure.
    """
    for f in sourcedir.iterdir():
        if f.suffix.lower() in IMG_EXTS:
            # create the destination directory if it doesn't exist
            destdir.mkdir(parents=True, exist_ok=True)
            print(f"Copying {f} to {destdir}")
            # copy with metadata preservation
            shutil.copy2(f, destdir)


def main(sourcedir: Path, destdir: Path) -> None:
    """
    Traverses sourcedir looking for images and copies them to destdir.
    Preserves relative directory structure.
    """
    for root, _, _ in os.walk(sourcedir):
        root = Path(root)
        copy_figs(root, destdir / root.relative_to(sourcedir))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sourcedir = Path(sys.argv[1])
        destdir = Path(sys.argv[2])
        main(sourcedir, destdir)
    else:
        print(
            """Usage: python copy_figs.py <sourcedir> <destdir>
where <sourcedir> is the rst source directory and <destdir> is the PreTeXt external assets directory.
"""
        )
