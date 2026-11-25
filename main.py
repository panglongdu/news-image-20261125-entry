"""make.fun news-image-20261125 entry.

Writes the day's-news summary image to the output directory.
The image beside this file (entry.png, 1024x1024, drawn by build_image.py
from the headlines of 25 November 2026) is the entry; this program copies
it to <output>/entry.png, where <output> is MAKEFUN_OUTPUT_DIR when set
and /output otherwise.
"""
import os
import shutil
from pathlib import Path

src = Path(__file__).with_name("entry.png")
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, out_dir / "entry.png")
print(f"wrote {out_dir / 'entry.png'}")
