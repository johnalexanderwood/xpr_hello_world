"""
Fast unit test of the pure image-generation logic — no display, no
GUI, no PyInstaller involved. Run directly with:
    python test_colorsweep.py
"""
import numpy as np

from colorsweep import generate_color_sweep


def main():
    width, height = 400, 200
    img = generate_color_sweep(width, height)

    assert img.shape == (height, width, 3), f"unexpected shape: {img.shape}"
    assert img.dtype == np.uint8, f"unexpected dtype: {img.dtype}"

    left = img[height // 2, 0]
    mid = img[height // 2, width // 3]
    right = img[height // 2, width - 1]

    assert not np.array_equal(left, mid), "expected colour to vary across the sweep"
    assert not np.array_equal(mid, right), "expected colour to vary across the sweep"

    print(f"PASS: sweep image is {img.shape}, dtype {img.dtype}, colour varies across width")


if __name__ == "__main__":
    main()
