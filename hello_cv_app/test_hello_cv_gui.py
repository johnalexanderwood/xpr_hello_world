"""
Smoke test for the built hello_xpr_cv executable (OpenCV + GUI
variant).

Unlike the console hello-world test, this does NOT check stdout —
--windowed/GUI builds don't reliably expose it on Windows. Instead
this confirms the exe launches, generates and displays the image,
survives its own auto-close timer (passed via --autoclose-ms), and
exits cleanly (return code 0) within a generous timeout.

This does NOT prove anything about what actually renders on
screen — look at a downloaded build at least once. It also won't
catch subtle OpenCV/PyInstaller packaging gaps that only manifest
as visibly wrong output rather than a crash (e.g. a channel-order
mixup) — this only proves it ran, not that it looked right.
"""
import subprocess
import sys

AUTOCLOSE_MS = 1500
TIMEOUT_SECONDS = 15


def main():
    if len(sys.argv) != 2:
        print("Usage: test_hello_cv_gui.py <path-to-exe>")
        sys.exit(1)

    exe_path = sys.argv[1]

    try:
        result = subprocess.run(
            [exe_path, f"--autoclose-ms={AUTOCLOSE_MS}"],
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"FAIL: exe did not exit within {TIMEOUT_SECONDS}s "
              f"(did the autoclose timer fire? did it hang on an error dialog?)")
        sys.exit(1)
    except Exception as exc:
        print(f"FAIL: could not run exe: {exc}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAIL: exe exited with code {result.returncode}")
        sys.exit(1)

    print("PASS: exe launched, generated the image, and exited cleanly")
    sys.exit(0)


if __name__ == "__main__":
    main()
