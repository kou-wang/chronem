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

Set `MNEMO_DISTRIBUTION_DATABASE_URL` to a fresh, disposable PostgreSQL database
that the smoke test may migrate and write to.

```bash
repository_root="$PWD"
artifact_dir="$(mktemp -d)"
smoke_dir="$(mktemp -d)"

python -m build --outdir "$artifact_dir"
python -m twine check --strict "$artifact_dir"/*
python scripts/validate_distribution.py "$artifact_dir"

python -m venv "$smoke_dir"
wheel_paths=("$artifact_dir"/*.whl)
"$smoke_dir/bin/python" -m pip install "${wheel_paths[0]}[postgres]"
cp scripts/smoke_installed_wheel.py "$smoke_dir/"
cp scripts/smoke_installed_wheel_postgres.py "$smoke_dir/"
cp examples/deterministic_lifecycle.py "$smoke_dir/"
(
  cd /tmp
  "$smoke_dir/bin/python" "$smoke_dir/smoke_installed_wheel.py"
  "$smoke_dir/bin/python" "$smoke_dir/deterministic_lifecycle.py"
  "$smoke_dir/bin/python" "$smoke_dir/smoke_installed_wheel_postgres.py" \
    --database-url "$MNEMO_DISTRIBUTION_DATABASE_URL" \
    --source-root "$repository_root"
)
```

This proves that the wheel and sdist build, metadata renders cleanly, required
package data is present, and the wheel—not the editable checkout—imports and
runs in a fresh environment. It also proves that packaged migrations initialize
a fresh PostgreSQL database and that an installed repository adapter works. The
manual **Release dry run** GitHub workflow runs the same checks for a selected
ref and uploads the artifacts without publishing.

## Source-distribution contents

Mnemo's sdist intentionally includes source-facing project material useful for
inspection and downstream validation: source code, tests, documentation,
examples, scripts, GitHub automation, and contributor/agent configuration. It
may therefore contain more than the runtime wheel.

The distribution validator rejects local or generated material that is not
intentional source content: environment files, virtual environments, Python and
tool caches, coverage output, nested build/distribution output, common secret
or credential files, private-key formats, and editor/local-machine artifacts.
Required package resources—including all PostgreSQL migration files—must be
present in both the wheel and sdist.

## PostgreSQL migration paths

In a source checkout, `alembic upgrade head` uses the repository's
`alembic.ini`, which points into the packaged PostgreSQL adapter tree. An
installed-wheel user instead runs:

```bash
python -m mnemo.persistence.postgres.migrations \
  --database-url "$MNEMO_DATABASE_URL"
```

or calls `upgrade_postgres_database(database_url)` from
`mnemo.persistence.postgres`. Neither installed-package path reads a
repository-local `alembic.ini`.

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
