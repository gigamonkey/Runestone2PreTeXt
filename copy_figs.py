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
    Copies figures from sourcedir to destdir, creating any necessary subdirectories.
    Figures defined as files with extensions in IMG_EXTS, case insensitive.
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
    Walks through the sourcedir and copies any figures to the destdir, preserving directory structure.
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
