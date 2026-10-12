# Releasing Mnemo

Mnemo is not currently published on PyPI. This document defines the pre-1.0
policy and the steps maintainers will use for an intentional public release.

## Versioning policy

Mnemo uses Semantic Versioning with a manual version in `pyproject.toml` and a
matching `vMAJOR.MINOR.PATCH` Git tag.

Before `1.0.0`:

- `0.MINOR.0` may introduce backward-incompatible public API or semantic changes;
- `0.MINOR.PATCH` is for backward-compatible fixes, documentation, packaging,
  and internal improvements;
- breaking changes require explicit Issue scope and should include migration
  guidance or deprecation where practical;
- versions are never bumped automatically by CI.

Every release moves relevant `CHANGELOG.md` entries from `Unreleased` into a
dated `## [VERSION] - YYYY-MM-DD` section. The package version, changelog
version, and Git tag must match.

## Local release dry run

From a clean checkout with `.[dev]` installed:

```bash
repository_root="$PWD"
artifact_dir="$(mktemp -d)"
smoke_dir="$(mktemp -d)"

python -m build --outdir "$artifact_dir"
python -m twine check --strict "$artifact_dir"/*
python scripts/validate_distribution.py "$artifact_dir"

python -m venv "$smoke_dir"
"$smoke_dir/bin/python" -m pip install "$artifact_dir"/*.whl
(
  cd /tmp
  "$smoke_dir/bin/python" "$repository_root/scripts/smoke_installed_wheel.py"
  "$smoke_dir/bin/python" "$repository_root/examples/deterministic_lifecycle.py"
)
```

This proves that the wheel and sdist build, metadata renders cleanly, required
package data is present, and the wheel—not the editable checkout—imports and
runs in a fresh environment. The manual **Release dry run** GitHub workflow runs
the same checks for a selected ref and uploads the artifacts without publishing.

## One-time trusted-publishing setup

Publishing uses PyPI's GitHub Actions trusted publisher and short-lived OIDC
credentials. No PyPI token or password belongs in repository secrets or files.
Before the first release, a maintainer must:

1. Create or reserve the `mnemo-memory` project on PyPI, or configure a pending
   trusted publisher for that project name.
2. Configure the publisher for owner `kou-wang`, repository `mnemo-memory`,
   workflow `release.yml`, and GitHub environment `pypi`.
3. Create the `pypi` environment in repository settings and add required
   reviewers and tag protection appropriate to the project.
4. Confirm the repository permits the workflow's `id-token: write` permission.

These are repository/account-side controls; merging the workflow does not
configure PyPI and does not publish a package.

## Maintainer release checklist

1. Confirm `main` is green on Python 3.11 and 3.12, including PostgreSQL and the
   deterministic evaluation gate.
2. Choose the version deliberately. Update `project.version` in `pyproject.toml`
   and create the matching dated changelog section; do not change versions only
   to make automation pass.
3. Open and merge a reviewed release-preparation PR.
4. Run the **Release dry run** workflow on the exact merged commit and inspect
   its wheel and sdist artifacts.
5. Create and push an annotated `vMAJOR.MINOR.PATCH` tag pointing at that commit.
6. Run **Release Python distribution** with that tag and `publish` disabled.
   Inspect the second clean build before continuing.
7. After the PyPI trusted publisher and `pypi` environment are configured, rerun
   the release workflow with the same tag and `publish` enabled. Environment
   protection should require explicit maintainer approval.
8. Verify the published project page and install the exact released version in
   a new environment. Then create release notes from the dated changelog entry.

The release workflow has no `push` or `pull_request` trigger. Ordinary commits,
PRs, and tags cannot invoke its publish job.
