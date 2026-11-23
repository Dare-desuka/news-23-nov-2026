"""Copy the entry image to the grader's output directory.

Standard library only: this program runs with no network and nothing
installed, so it just copies entry.png (which ships in this repository)
to /output/entry.png. The image itself is drawn by gen_image.py.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(OUT, "entry.png"))


if __name__ == "__main__":
    main()
