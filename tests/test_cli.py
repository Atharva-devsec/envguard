import subprocess
import sys

from envguard import __version__


def test_version_command() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "envguard", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == f"envguard {__version__}"
    assert result.stderr == ""
