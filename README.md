# Windows build pipeline — hello world proof of concept

This is the smallest possible version of the pipeline: build a
Windows .exe from a Python script via GitHub Actions, on a real
Windows runner, with an automated check that the exe actually
works — with no Windows machine of your own required.

## What's here

- `hello_app/hello.py` — trivial script, prints ~`Hello, xpr!`
- `hello_app/test_hello.py` — runs a given exe and checks the
  output matches. Used as the CI smoke test; also runnable locally
  against any exe you build by hand.
- `.github/workflows/build-windows.yml` — GitHub Actions workflow:
  checks out the repo on `windows-latest`, installs PyInstaller,
  builds `hello_xpr.exe`, runs the smoke test against it, and
  (if it passes) uploads the exe as a downloadable build artifact.

## How to try it

1. Create a new GitHub repo (or a new branch in an existing one)
   and copy this whole folder structure into it — `hello_app/`,
   `.github/workflows/build-windows.yml`, and this README all at
   the repo root.
2. Commit and push to `main`.
3. Open the repo on GitHub → **Actions** tab. You should see
   "Build Windows Exe" running (it triggers automatically on push
   to `main`, or you can trigger it manually via
   **Run workflow** thanks to `workflow_dispatch`).
4. Once it finishes (a couple of minutes), open the completed run →
   scroll to **Artifacts** → download `hello_xpr-windows-exe`.
   That's a zip containing the real Windows .exe, built on a real
   Windows machine, that you never touched.
5. If you *do* have a Windows machine handy at some point, unzip it
   and double-click — or run `hello_xpr.exe` from a terminal —
   and confirm you see `Hello, xpr!` printed. The CI smoke test
   already checked this automatically, but seeing it yourself once
   is worth doing.

## What this proves (and doesn't)

Proves:
- You can go from Python source to a working Windows .exe with zero
  local Windows access.
- The build can be automatically verified (not just "it compiled",
  but "it actually runs and does the right thing") before you ever
  download it.
- The whole thing is repeatable — every push rebuilds and re-tests.

Doesn't yet prove:
- That OpenCV / ttkbootstrap / your real dependencies package
  cleanly this way (they usually do, but numpy/OpenCV wheels and
  ttkbootstrap's Tk dependency are exactly the kind of thing that
  can surprise you — worth doing as the *next* increment, not
  skipping to the full xpr codebase).
- That the resulting exe runs cleanly on a machine that isn't the
  CI runner (different Windows versions, missing VC++ redistributables,
  antivirus flagging an unsigned exe, etc.) — that's what the
  friendly-tester step in week 4 is for.
- GUI behaviour — this smoke test only checks stdout from a
  console script. A ttkbootstrap window can't be "clicked" by CI in
  this simple setup; the honest test there is still a human
  launching it.

## Suggested next increment

Same pattern, slightly bigger: a minimal ttkbootstrap window (just
one label, no real xpr logic) built the same way, with the smoke
test relaxed to "the exe launches and exits 0 within N seconds"
rather than checking stdout, since a GUI app won't print anything by
default. That will surface any Tk-specific packaging issues early,
still with almost no real code at stake.
