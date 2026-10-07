"""PowerShell-friendly convenience tasks for local development."""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="AgentSec Sandbox development tasks")
    parser.add_argument("task", choices=["doctor", "test", "lint"])
    task = parser.parse_args().task
    commands = {
        "doctor": [sys.executable, "-m", "agentsec.cli", "doctor"],
        "test": [sys.executable, "-m", "pytest"],
        "lint": [sys.executable, "-m", "ruff", "check", "."],
    }
    return subprocess.run(commands[task], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
