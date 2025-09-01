"""Development tasks."""

from __future__ import annotations

import os
import re
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from cProfile import Profile
from importlib.metadata import version as pkgversion
from pathlib import Path
from pstats import SortKey, Stats
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from duty import duty, tools

if TYPE_CHECKING:
    from collections.abc import Iterator

    from duty.context import Context


PY_SRC_PATHS = (Path(_) for _ in ("src", "tests", "duties.py", "scripts"))
PY_SRC_LIST = tuple(str(_) for _ in PY_SRC_PATHS)
PY_SRC = " ".join(PY_SRC_LIST)
CI = os.environ.get("CI", "0") in {"1", "true", "yes", ""}
WINDOWS = os.name == "nt"
PTY = not WINDOWS and not CI
MULTIRUN = os.environ.get("MULTIRUN", "0") == "1"
PY_VERSION = f"{sys.version_info.major}{sys.version_info.minor}"
PY_DEV = "314"


def pyprefix(title: str) -> str:
    if MULTIRUN:
        prefix = f"(python{sys.version_info.major}.{sys.version_info.minor})"
        return f"{prefix:14}{title}"
    return title


@contextmanager
def material_insiders() -> Iterator[bool]:
    if "+insiders" in pkgversion("mkdocs-material"):
        os.environ["MATERIAL_INSIDERS"] = "true"
        try:
            yield True
        finally:
            os.environ.pop("MATERIAL_INSIDERS")
    else:
        yield False


def _get_changelog_version() -> str:
    changelog_version_re = re.compile(r"^## \[(\d+\.\d+\.\d+)\].*$")
    with Path(__file__).parent.joinpath("CHANGELOG.md").open("r", encoding="utf8") as file:
        return next(filter(bool, map(changelog_version_re.match, file))).group(1)  # type: ignore[union-attr]


@duty
def changelog(ctx: Context, bump: str = "") -> None:
    """Update the changelog in-place with latest commits.

    Parameters:
        bump: Bump option passed to git-changelog.
    """
    ctx.run(tools.git_changelog(bump=bump or None), title="Updating changelog")
    ctx.run(tools.yore.check(bump=bump or _get_changelog_version()), title="Checking legacy code")


@duty(pre=["check-quality", "check-types", "check-docs", "check-api"])
def check(ctx: Context) -> None:
    """Check it all!"""


@duty(nofail=PY_VERSION == PY_DEV)
def check_quality(ctx: Context) -> None:
    """Check the code quality."""
    ctx.run(
        tools.ruff.check(*PY_SRC_LIST, config="config/ruff.toml"),
        title=pyprefix("Checking code quality"),
    )


@duty(nofail=PY_VERSION == PY_DEV)
def check_docs(ctx: Context) -> None:
    """Check if the documentation builds correctly."""
    Path("htmlcov").mkdir(parents=True, exist_ok=True)
    Path("htmlcov/index.html").touch(exist_ok=True)
    with material_insiders():
        ctx.run(
            tools.mkdocs.build(strict=True, verbose=True),
            title=pyprefix("Building documentation"),
        )


@duty(nofail=PY_VERSION == PY_DEV)
def check_types(ctx: Context) -> None:
    """Check that the code is correctly typed."""
    os.environ["FORCE_COLOR"] = "1"
    ctx.run(
        tools.mypy(*PY_SRC_LIST, config_file="config/mypy.ini"),
        title=pyprefix("Type-checking"),
    )


@duty(nofail=PY_VERSION == PY_DEV)
def check_api(ctx: Context, *cli_args: str) -> None:
    """Check for API breaking changes."""
    ctx.run(
        tools.griffe.check("git_changelog", search=["src"], color=True).add_args(*cli_args),
        title="Checking for API breaking changes",
        nofail=True,
    )


@duty
def docs(ctx: Context, *cli_args: str, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Serve the documentation (localhost:8000).

    Parameters:
        host: The host to serve the docs from.
        port: The port to serve the docs on.
    """
    with material_insiders():
        ctx.run(
            tools.mkdocs.serve(dev_addr=f"{host}:{port}").add_args(*cli_args),
            title="Serving documentation",
            capture=False,
        )


@duty
def docs_deploy(ctx: Context) -> None:
    """Deploy the documentation to GitHub pages."""
    os.environ["DEPLOY"] = "true"
    with material_insiders() as insiders:
        if not insiders:
            ctx.run(lambda: False, title="Not deploying docs without Material for MkDocs Insiders!")
        ctx.run(tools.mkdocs.gh_deploy(), title="Deploying documentation")


@duty
def format(ctx: Context) -> None:
    """Run formatting tools on the code."""
    ctx.run(
        tools.ruff.check(*PY_SRC_LIST, config="config/ruff.toml", fix_only=True, exit_zero=True),
        title="Auto-fixing code",
    )
    ctx.run(tools.ruff.format(*PY_SRC_LIST, config="config/ruff.toml"), title="Formatting code")


@duty
def build(ctx: Context) -> None:
    """Build source and wheel distributions."""
    ctx.run(
        tools.build(),
        title="Building source and wheel distributions",
        pty=PTY,
    )


@duty
def publish(ctx: Context) -> None:
    """Publish source and wheel distributions to PyPI."""
    if not Path("dist").exists():
        ctx.run("false", title="No distribution files found")
    dists = [str(dist) for dist in Path("dist").iterdir()]
    ctx.run(
        tools.twine.upload(*dists, skip_existing=True),
        title="Publishing source and wheel distributions to PyPI",
        pty=PTY,
    )


@duty(post=["build", "publish", "docs-deploy"])
def release(ctx: Context, version: str = "") -> None:
    """Release a new Python package.

    Parameters:
        version: The new version number to use.
    """
    if not (version := (version or input("> Version to release: ")).strip()):
        ctx.run("false", title="A version must be provided")
    ctx.run("git add pyproject.toml CHANGELOG.md", title="Staging files", pty=PTY)
    ctx.run(["git", "commit", "-m", f"chore: Prepare release {version}"], title="Committing changes", pty=PTY)
    ctx.run(f"git tag {version}", title="Tagging commit", pty=PTY)
    ctx.run("git push", title="Pushing commits", pty=False)
    ctx.run("git push --tags", title="Pushing tags", pty=False)


@duty(silent=True, aliases=["cov"])
def coverage(ctx: Context) -> None:
    """Report coverage as text and HTML."""
    ctx.run(tools.coverage.combine(), nofail=True)
    ctx.run(tools.coverage.report(rcfile="config/coverage.ini"), capture=False)
    ctx.run(tools.coverage.html(rcfile="config/coverage.ini"))


@duty(nofail=PY_VERSION == PY_DEV)
def test(ctx: Context, *cli_args: str, match: str = "") -> None:  # noqa: PT028
    """Run the test suite.

    Parameters:
        match: A pytest expression to filter selected tests.
    """
    os.environ["COVERAGE_FILE"] = f".coverage.{PY_VERSION}"
    ctx.run(
        tools.pytest(
            "tests",
            config_file="config/pytest.ini",
            select=match,
            color="yes",
        ).add_args("-n", "auto", *cli_args),
        title=pyprefix("Running tests"),
    )


@duty
def profile(ctx: Context, merge: int = 15) -> None:
    """Profile the parsing and grouping of commits.

    Parameters:
        merge: Number of times to merge a branch in the temporary repository.
    """
    # Do not import those from the top level,
    # as it prevents the pytest-cov plugin for marking
    # lines executed at import time as covered.
    from git_changelog import Changelog  # noqa: PLC0415
    from git_changelog.commit import AngularConvention  # noqa: PLC0415

    try:
        from tests.helpers import GitRepo  # noqa: PLC0415
    except ModuleNotFoundError:
        import sys  # noqa: PLC0415

        sys.path.insert(0, str(Path(__file__).parent))
        from tests.helpers import GitRepo  # noqa: PLC0415

    def merge_branches(repo: GitRepo, branch: str = "feat", times: int = 15) -> None:
        for _ in range(times):
            repo.branch(branch)
            repo.checkout(branch)
            repo.commit(f"feat: {branch}")
            repo.checkout("main")
            repo.merge(branch)
            repo.git("branch", "-d", branch)

    with TemporaryDirectory() as tmp_dir:
        repo = GitRepo(Path(tmp_dir) / "repo")
        ctx.run(merge_branches, args=(repo, "feat", merge), title="Creating temporary repository")

        with Profile() as profile:
            Changelog(repo.path, convention=AngularConvention)
        Stats(profile).strip_dirs().sort_stats(SortKey.TIME).print_stats()
