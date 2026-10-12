"""Require an intentional version tag that matches package and changelog versions."""

from __future__ import annotations

import argparse
import re
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def validate(tag: str) -> None:
    with (ROOT / "pyproject.toml").open("rb") as pyproject:
        version = str(tomllib.load(pyproject)["project"]["version"])
    expected_tag = f"v{version}"
    if tag != expected_tag:
        raise ValueError(
            f"release tag must match package version: expected {expected_tag}, got {tag}"
        )

    tags_at_head = subprocess.run(
        ["git", "tag", "--points-at", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if tag not in tags_at_head:
        raise ValueError(f"{tag} does not point at the checked-out release commit")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    release_heading = rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$"
    if re.search(release_heading, changelog, re.M) is None:
        raise ValueError(f"CHANGELOG.md needs a dated [{version}] release section")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag")
    args = parser.parse_args()
    validate(args.tag)
    print(f"validated release tag: {args.tag}")


if __name__ == "__main__":
    main()
