#!/usr/bin/env python3
"""Hand the built news image to the grader.

The grader sets MAKEFUN_OUTPUT_DIR to the directory it wants the
image in; when that variable is missing we fall back to /output.
We create the directory when it is not there yet, then copy
entry.png (which sits next to this file) into it.
"""
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(BASE_DIR, "entry.png")

target = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
if not os.path.isfile(IMAGE):
    raise SystemExit("entry.png not found next to main.py; run build_image.py first")
os.makedirs(target, exist_ok=True)
shutil.copyfile(IMAGE, os.path.join(target, "entry.png"))
print("entry.png written to", target)
