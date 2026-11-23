#!/usr/bin/env python3
"""Copy the generated front page into the grader's output folder.

Standard library only: nothing to install, nothing to import beyond
shutil and os. The entry image lives next to this file; the grader
reads it from /output/entry.png.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
TARGET = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    print("Wrote", TARGET)


if __name__ == "__main__":
    main()
