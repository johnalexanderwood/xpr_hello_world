"""
Minimal ttkbootstrap window, packaged the same way as hello.py, to
prove out GUI packaging (Tk + ttkbootstrap + Pillow) through the
same GitHub Actions -> PyInstaller pipeline.

Includes a defensive monkeypatch for a known ttkbootstrap/Pillow
compatibility issue: Pillow 10+ removed several old-style resize
filter constants (Image.CUBIC, Image.LINEAR, Image.ANTIALIAS, and
in some versions Image.NEAREST/BILINEAR/BICUBIC as top-level names)
in favour of Image.Resampling.*, but some ttkbootstrap widget code
still references the old names directly, causing an AttributeError
at runtime (typically on first paint / theme change, not at
import time, so it can slip past casual testing). This patches the
old names back onto PIL.Image as aliases before ttkbootstrap is
imported, so it works regardless of which Pillow/ttkbootstrap
versions land together on the CI build machine.
See: https://github.com/israel-dryer/ttkbootstrap/issues/472
"""
import sys

from PIL import Image

_LEGACY_RESAMPLING_ALIASES = {
    "NEAREST": "NEAREST",
    "LANCZOS": "LANCZOS",
    "BILINEAR": "BILINEAR",
    "BICUBIC": "BICUBIC",
    "BOX": "BOX",
    "HAMMING": "HAMMING",
    "ANTIALIAS": "LANCZOS",  # old alias, no direct 1:1 equivalent
    "CUBIC": "BICUBIC",      # old alias
    "LINEAR": "BILINEAR",    # old alias
}

for _old_name, _resampling_name in _LEGACY_RESAMPLING_ALIASES.items():
    if not hasattr(Image, _old_name):
        setattr(Image, _old_name, getattr(Image.Resampling, _resampling_name))

import ttkbootstrap as tb  # noqa: E402  (must come after the patch above)


def parse_autoclose_ms(argv):
    """Look for --autoclose-ms=<int> in argv. Returns None if absent
    or malformed, meaning: stay open normally for a human to look at."""
    for arg in argv[1:]:
        if arg.startswith("--autoclose-ms="):
            try:
                return int(arg.split("=", 1)[1])
            except ValueError:
                return None
    return None


def main():
    app = tb.Window(themename="flatly")
    app.title("xpr hello (GUI)")
    app.geometry("320x160")

    label = tb.Label(app, text="Hello, xpr!", font=("Segoe UI", 16))
    label.pack(expand=True)

    autoclose_ms = parse_autoclose_ms(sys.argv)
    if autoclose_ms is not None:
        app.after(autoclose_ms, app.destroy)

    app.mainloop()


if __name__ == "__main__":
    main()
