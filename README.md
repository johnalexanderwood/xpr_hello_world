# Xpr Windows build pipeline — hello world proof of concept

Smallest-possible pipeline: build a Windows .exe from Python via
GitHub Actions, on a real Windows runner, with an automated check
that the exe actually works — no Windows machine of your own
required. Three increasingly-realistic variants, each its own job:

- **`build-console`** (`hello_app/`) — plain script, printed output.
- **`build-gui`** (`hello_gui_app/`) — a ttkbootstrap window.
- **`build-cv-gui`** (`hello_cv_app/`) — OpenCV generates an image
  (a hue sweep), converted through Numpy -> PIL -> ImageTk and
  displayed in a ttkbootstrap Label. This is the closest one yet to
  actual Xpr's load-image-and-draw-on-it shape.

## What's here

- `hello_app/` — console hello-world + its smoke test.
- `hello_gui_app/` — minimal ttkbootstrap window + smoke test.
- `hello_cv_app/`:
  - `colorsweep.py` — pure OpenCV/Numpy image generation, kept
    separate from any GUI code so it's independently unit-testable.
  - `test_colorsweep.py` — fast unit test of that logic (shape,
    dtype, that colour actually varies). No display needed — this
    runs in CI even before the exe is built.
  - `hello_cv_gui.py` — the window: generates the sweep, converts
    it to a Tk-displayable image, shows it in a Label.
  - `test_hello_cv_gui.py` — same launches-and-exits-cleanly smoke
    test pattern as the plain GUI app.
- `.github/workflows/build-windows.yml` — three parallel jobs, each
  building, testing, and uploading its own exe.

## How to try it

1. Copy the whole structure into a repo, preserving paths exactly.
   (Web UI uploads can flatten folders — use **Add file → Create
   new file** and type full paths with slashes if so.)
2. Commit and push to `main`.
3. Check **Actions** — all three jobs should run.
4. Download exes from **Artifacts**, or set up a **Release** for a
   permanent link to send a tester.

## Real packaging issues found (and fixed) building this

1. **Missing ttkbootstrap asset files.** PyInstaller doesn't
   auto-bundle non-Python package files (icon fonts). Fixed with
   `--collect-data ttkbootstrap`.
2. **Missing PIL hidden import.** `PIL.ImageTk` finds
   `PIL._tkinter_finder` dynamically at runtime, invisible to
   PyInstaller's static analysis. Fixed with
   `--hidden-import PIL._tkinter_finder`.
3. **OpenCV** — used `opencv-python-headless` rather than
   `opencv-python`, since nothing here uses cv2's own GUI/imshow
   functions, and headless avoids bundling Qt/GTK dependencies
   PyInstaller would otherwise have to package for no benefit.
   Locally (Linux), the `build-cv-gui` job's PyInstaller command
   needed no extra flags beyond what `build-gui` already had — but
   this was NOT tested on Windows locally (no Windows machine), and
   OpenCV's Windows packaging has its own known quirks (missing
   VC++ runtime DLLs, sometimes needing `--collect-all cv2`). The
   real test is whichever CI run you trigger next — watch that job's
   log even if the other two look fine.

## On the resize-constant (NEAREST/LINEAR) issue

Real, documented ttkbootstrap/Pillow bug: Pillow 10+ removed
old-style names (`Image.CUBIC`, `Image.LINEAR`, `Image.ANTIALIAS`)
in favour of `Image.Resampling.*`; some ttkbootstrap widgets still
call the old names.
See: https://github.com/israel-dryer/ttkbootstrap/issues/472
A defensive monkeypatch sits at the top of both `hello_gui.py` and
`hello_cv_gui.py` (restores old names as aliases before ttkbootstrap
is imported). Tested directly: a plain `Window`+`Label` does not
trigger it — it's specific to certain widgets (`Meter`, per the
upstream issue) — so it's not proven necessary yet, but it's cheap
insurance for when real Xpr widgets are added.

## What this proves (and doesn't)

Proves:
- Console, plain-GUI, and OpenCV+GUI apps can all go from Python
  source to a working Windows .exe with zero local Windows access.
- The core Xpr dependency stack (Tk, ttkbootstrap, Pillow,
  OpenCV, Numpy) can be packaged together, with known gaps already
  fixed.
- Pure logic (image generation) is tested separately from the GUI
  shell, which is the pattern worth carrying into real Xpr —
  most things should be unit-testable without a display; only the
  thin GUI wrapper needs the "launches and exits cleanly" style of
  smoke test.

Doesn't yet prove:
- Behaviour on a real Windows machine that isn't the CI runner
  (different Windows versions, missing redistributables, antivirus
  flagging an unsigned exe) — needs a friendly-tester pass before
  the real release.
- Anything about large images (this is a 400x200 test pattern, not
  32k x 4k) — memory behaviour at real Xpr scale is still
  untested through this pipeline.
- Anything about the real plugin architecture, `.drw` save/load, or
  actual geological imagery — this remains a deliberately trivial
  stand-in for all of that.

## Suggested next increment

Load a real (moderately large, e.g. a few thousand pixels wide)
image file bundled with the exe or opened via a file dialog, rather
than a generated 400x200 pattern — this starts testing actual
memory/performance behaviour and file-dialog packaging (Tk's native
file dialogs can have their own PyInstaller wrinkles on Windows).
