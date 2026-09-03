# Xpr Windows build pipeline — hello world proof of concept

This is the smallest possible version of the pipeline: build a
Windows .exe from a Python script via GitHub Actions, on a real
Windows runner, with an automated check that the exe actually
works — with no Windows machine of your own required.

Two variants are proven out here:

- **Console app** (`hello_app/`) — plain script, printed output.
- **GUI app** (`hello_gui_app/`) — a real ttkbootstrap window,
  packaged the same way. This is the one closer to actual Xpr.

## What's here

- `hello_app/hello.py` / `hello_app/test_hello.py` — console
  hello-world and its smoke test (checks stdout).
- `hello_gui_app/hello_gui.py` — a minimal ttkbootstrap window.
  Takes an optional `--autoclose-ms=<n>` flag so it can close
  itself automatically under CI; without it, it just stays open
  for a human to look at.
- `hello_gui_app/test_hello_gui.py` — GUI smoke test. Doesn't
  check stdout (unreliable for `--windowed` Windows builds) —
  instead confirms the exe launches and exits cleanly within a
  timeout, using the autoclose flag.
- `.github/workflows/build-windows.yml` — two parallel jobs,
  `build-console` and `build-gui`, each building, smoke-testing,
  and uploading its own exe as a build artifact.

## How to try it

1. Copy this whole folder structure into a repo, preserving paths
   exactly — `hello_app/`, `hello_gui_app/`, and
   `.github/workflows/build-windows.yml` all at the repo root.
   (If uploading via the GitHub web UI, use **Add file → Create
   new file** and type the full path including slashes — drag-and-
   drop uploads can flatten folder structure.)
2. Commit and push to `main`.
3. Check the **Actions** tab — "Build Windows Exe" should appear
   and run both jobs.
4. Download each exe from the run's **Artifacts** section, or set
   up a GitHub **Release** for a permanent, no-login-required
   download link to send to a tester.

## Real packaging issues found (and fixed) building this

Two genuine PyInstaller/ttkbootstrap issues turned up while
building the GUI variant — both fixed and now baked into the
workflow above:

1. **Missing ttkbootstrap asset files.** PyInstaller doesn't
   automatically bundle non-Python files a package ships (icon
   fonts, in this case). Without `--collect-data ttkbootstrap`,
   the exe builds fine but crashes on launch with
   `FileNotFoundError: .../ttkbootstrap/assets/icons/bootstrap.ttf`.
2. **Missing PIL hidden import.** `PIL.ImageTk` locates
   `PIL._tkinter_finder` dynamically at runtime, which PyInstaller's
   static analysis doesn't catch. Without
   `--hidden-import PIL._tkinter_finder`, the exe crashes on first
   themed-icon render with `ModuleNotFoundError`.

Both are now in the `build-gui` job's PyInstaller command.

## On the resize-constant (NEAREST/LINEAR) issue

This is a real, documented ttkbootstrap/Pillow compatibility bug:
Pillow 10+ removed old-style resize filter names
(`Image.CUBIC`, `Image.LINEAR`, `Image.ANTIALIAS`) in favour of
`Image.Resampling.*`, but some ttkbootstrap widget code still calls
the old names — see
https://github.com/israel-dryer/ttkbootstrap/issues/472. A
defensive monkeypatch is included at the top of `hello_gui.py`
(restores the old names as aliases before ttkbootstrap is
imported), matching what you remembered needing before.

Tested directly here: a plain `Window` + `Label`, as in this
hello-world, does **not** actually trigger the bug — it's specific
to certain widgets (the `Meter` widget, per the upstream issue).
So the patch isn't proven necessary for this minimal case, but it's
cheap insurance and worth keeping once real Xpr widgets are
added, since you won't want to rediscover this mid-deadline.

## What this proves (and doesn't)

Proves:
- Console AND GUI (Tk + ttkbootstrap + Pillow) apps can go from
  Python source to a working Windows .exe with zero local Windows
  access, via a repeatable, automatically-verified CI pipeline.
- Two real packaging gaps specific to this dependency stack are now
  known and fixed, before any real Xpr code is at stake.

Doesn't yet prove:
- That the resulting exe runs cleanly on a machine that isn't the
  CI runner (different Windows versions, missing VC++ redistributables,
  antivirus flagging an unsigned exe, etc.) — that's what a
  friendly-tester step before the real release is for.
- Anything about what's actually on screen — the smoke test checks
  launch/exit behaviour, not visual correctness. Look at it yourself
  at least once via a downloaded artifact.
- Behaviour with the real dependency set (OpenCV, larger images,
  your actual plugin architecture) — this is still a near-empty app.

## Suggested next increment

Bring in OpenCV alongside ttkbootstrap in the same pattern — a
window that loads and displays one modestly-sized image. OpenCV has
its own PyInstaller quirks (missing DLLs, `--collect-all cv2` is
often needed) worth surfacing now rather than later.
