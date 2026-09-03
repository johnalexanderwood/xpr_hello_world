"""
Pure image-generation logic, kept separate from the GUI code so it
can be unit-tested directly (no display, no Tk, no PyInstaller
involved).
"""
import cv2
import numpy as np


def generate_color_sweep(width: int = 400, height: int = 200) -> np.ndarray:
    """Generate an RGB uint8 numpy array of shape (height, width, 3)
    that sweeps hue across the width at full saturation/value.
    Uses OpenCV for the HSV->BGR colour conversion; returns RGB
    (PIL's expected order), not OpenCV's native BGR.
    """
    hue = (
        np.linspace(0, 179, width, dtype=np.uint8)
        .reshape(1, width)
        .repeat(height, axis=0)
    )
    saturation = np.full((height, width), 255, dtype=np.uint8)
    value = np.full((height, width), 255, dtype=np.uint8)

    hsv = cv2.merge([hue, saturation, value])
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb
