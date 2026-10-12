from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_release_workflow_is_manual_and_uses_trusted_publishing() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(
        encoding="utf-8"
    )

    assert "workflow_dispatch:" in workflow
    assert "\n  push:" not in workflow
    assert "\n  pull_request:" not in workflow
    assert "id-token: write" in workflow
    assert "environment:\n      name: pypi" in workflow
    assert "pypa/gh-action-pypi-publish@release/v1" in workflow
    assert "password:" not in workflow
    assert "__token__" not in workflow


def test_release_dry_run_cannot_publish() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release-dry-run.yml").read_text(
        encoding="utf-8"
    )

    assert "workflow_dispatch:" in workflow
    assert "gh-action-pypi-publish" not in workflow
    assert "id-token: write" not in workflow


def test_version_stays_pre_release_and_readme_does_not_claim_pypi_availability() -> None:
    with (ROOT / "pyproject.toml").open("rb") as pyproject:
        version = tomllib.load(pyproject)["project"]["version"]
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert version == "0.1.0"
    assert "Mnemo is not published on PyPI yet" in readme
