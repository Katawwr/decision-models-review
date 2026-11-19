"""Clone the three source repositories into data/ at their pinned commits."""

from __future__ import annotations

import subprocess
from pathlib import Path

from paths import DATA, PINS


def fetch(name: str, pin: dict, destination: Path) -> str:
    if not destination.exists():
        subprocess.run(["git", "clone", "-q", pin["url"], str(destination)], check=True)
    subprocess.run(["git", "-C", str(destination), "fetch", "-q", "origin", pin["commit"]], check=False)
    subprocess.run(["git", "-C", str(destination), "checkout", "-q", "--detach", pin["commit"]], check=True)
    head = subprocess.run(["git", "-C", str(destination), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    if head != pin["commit"]:
        raise SystemExit(f"{name}: HEAD is {head}, expected {pin['commit']}")
    return head


if __name__ == "__main__":
    for repo_name, repo_pin in PINS.items():
        print(f"{repo_name} at {fetch(repo_name, repo_pin, DATA / repo_name)}")
