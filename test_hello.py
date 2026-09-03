"""
Smoke test for the built hello_xpr executable.

Run as: python test_hello.py <path-to-exe>

Exits 0 and prints PASS if the exe runs and produces the expected
output. Exits 1 and prints FAIL otherwise, so this can be used
directly as a CI step that fails the build on a bad exe.
"""
import subprocess
import sys

EXPECTED = ""Hello World, this is an experiment!"


def main():
    if len(sys.argv) != 2:
        print("Usage: test_hello.py <path-to-exe>")
        sys.exit(1)

    exe_path = sys.argv[1]

    try:
        result = subprocess.run(
            [exe_path],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:
        print(f"FAIL: could not run exe: {exc}")
        sys.exit(1)

    if EXPECTED not in result.stdout:
        print(f"FAIL: expected '{EXPECTED}' in stdout, got: {result.stdout!r}")
        print(f"stderr was: {result.stderr!r}")
        sys.exit(1)

    print("PASS: exe produced expected output")
    sys.exit(0)


if __name__ == "__main__":
    main()
