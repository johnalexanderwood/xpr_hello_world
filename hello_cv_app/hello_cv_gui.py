"""
ttkbootstrap window that displays an OpenCV/Numpy-generated image.
Proves out the OpenCV -> Numpy -> PIL -> ImageTk -> ttk Label path
through the same PyInstaller/GitHub Actions pipeline as
hello_gui.py.

Same legacy-resampling-constant monkeypatch as hello_gui.py — see
that file for details on why it's here.
"""
import sys

from PIL import Image, ImageTk

_LEGACY_RESAMPLING_ALIASES = {
    "NEAREST": "NEAREST",
    "LANCZOS": "LANCZOS",
    "BILINEAR": "BILINEAR",
    "BICUBIC": "BICUBIC",
    "BOX": "BOX",
    "HAMMING": "HAMMING",
    "ANTIALIAS": "LANCZOS",
    "CUBIC": "BICUBIC",
    "LINEAR": "BILINEAR",
}
for _old_name, _resampling_name in _LEGACY_RESAMPLING_ALIASES.items():
    if not hasattr(Image, _old_name):
        setattr(Image, _old_name, getattr(Image.Resampling, _resampling_name))

import ttkbootstrap as tb  # noqa: E402

from colorsweep import generate_color_sweep  # noqa: E402


def parse_autoclose_ms(argv):
    for arg in argv[1:]:
        if arg.startswith("--autoclose-ms="):
            try:
                return int(arg.split("=", 1)[1])
            except ValueError:
                return None
    return None


def main():
    app = tb.Window(themename="flatly")
    app.title("xpr hello (OpenCV + GUI)")

    rgb_array = generate_color_sweep(width=400, height=200)
    pil_image = Image.fromarray(rgb_array)
    tk_image = ImageTk.PhotoImage(pil_image)

    label = tb.Label(app, image=tk_image)
    label.image = tk_image  # keep a reference - Tk won't hold one for you
    label.pack(padx=10, pady=10)

    caption = tb.Label(app, text="OpenCV colour sweep, rendered via Tk")
    caption.pack(pady=(0, 10))

    autoclose_ms = parse_autoclose_ms(sys.argv)
    if autoclose_ms is not None:
        app.after(autoclose_ms, app.destroy)

    app.mainloop()


if __name__ == "__main__":
    main()
