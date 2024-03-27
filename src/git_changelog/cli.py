"""Module that contains the command line application."""

# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m git_changelog` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `git_changelog.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `git_changelog.__main__` in `sys.modules`.

from __future__ import annotations

import argparse
import re
import sys
import warnings
from importlib import metadata
from pathlib import Path
from typing import Any, Literal, Pattern, Sequence, TextIO

from appdirs import user_config_dir
from jinja2.exceptions import TemplateNotFound

from git_changelog import debug, templates
from git_changelog.build import Changelog, Version
from git_changelog.commit import (
    AngularConvention,
    BasicConvention,
    CommitConvention,
    ConventionalCommitConvention,
)
from git_changelog.providers import Bitbucket, GitHub, GitLab, ProviderRefParser
from git_changelog.versioning import bump_pep440, bump_semver

# TODO: Remove once support for Python 3.10 is dropped.
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

DEFAULT_VERSIONING = "semver"
DEFAULT_VERSION_REGEX = r"^## \[(?P<version>v?[^\]]+)"
DEFAULT_MARKER_LINE = "<!-- insertion marker -->"
DEFAULT_CHANGELOG_FILE = "CHANGELOG.md"
CONVENTIONS = ("angular", "conventional", "basic")
DEFAULT_CONFIG_FILES = [
    "pyproject.toml",
    ".git-changelog.toml",
    "config/git-changelog.toml",
    ".config/git-changelog.toml",
    str(Path(user_config_dir()) / "git-changelog.toml"),
]
"""Default configuration files read by git-changelog."""

DEFAULT_SETTINGS: dict[str, Any] = {
    "bump": None,
    "bump_latest": None,
    "convention": "basic",
    "filter_commits": None,
    "in_place": False,
    "input": DEFAULT_CHANGELOG_FILE,
    "marker_line": DEFAULT_MARKER_LINE,
    "omit_empty_versions": False,
    "output": sys.stdout,
    "parse_refs": False,
    "parse_trailers": False,
    "provider": None,
    "release_notes": False,
    "repository": ".",
    "sections": None,
    "template": "keepachangelog",
    "jinja_context": {},
    "version_regex": DEFAULT_VERSION_REGEX,
    "versioning": DEFAULT_VERSIONING,
    "zerover": True,
}


class Templates(tuple):  # (subclassing tuple)
    """Helper to pick a template on the command line."""

    def __contains__(self, item: object) -> bool:
        if isinstance(item, str):
            return item.startswith("path:") or super().__contains__(item)
        return False


def get_version() -> str:
    """Return the current `git-changelog` version.

    Returns:
        The current `git-changelog` version.
    """
    try:
        return metadata.version("git-changelog")
    except metadata.PackageNotFoundError:
        return "0.0.0"


def _comma_separated_list(value: str) -> list[str]:
    return value.split(",")


class _ParseDictAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,  # noqa: ARG002
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | Sequence[Any] | None = None,  # noqa: ARG002
    ):
        attribute = getattr(namespace, self.dest)
        if not isinstance(attribute, dict):
            setattr(namespace, self.dest, {})
        if isinstance(values, str):
            key, value = values.split("=", 1)
            getattr(namespace, self.dest)[key] = value


providers: dict[str, type[ProviderRefParser]] = {
    "github": GitHub,
    "gitlab": GitLab,
    "bitbucket": Bitbucket,
}


class _DebugInfo(argparse.Action):
    def __init__(self, nargs: int | str | None = 0, **kwargs: Any) -> None:
        super().__init__(nargs=nargs, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        debug.print_debug_info()
        sys.exit(0)


def get_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="git-changelog",
        description=re.sub(
            r"\n *",
            "\n",
            f"""
            Automatic Changelog generator using Jinja2 templates.

            This tool parses your commit messages to extract useful data
            that is then rendered using Jinja2 templates, for example to
            a changelog file formatted in Markdown.

            Each Git tag will be treated as a version of your project.
            Each version contains a set of commits, and will be an entry
            in your changelog. Commits in each version will be grouped
            by sections, depending on the commit convention you follow.

            ### Conventions

            {BasicConvention._format_sections_help()}
            {AngularConvention._format_sections_help()}
            {ConventionalCommitConvention._format_sections_help()}
            """,
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "repository",
        metavar="REPOSITORY",
        nargs="?",
        help="The repository path, relative or absolute. Default: current working directory.",
    )

    parser.add_argument(
        "--config-file",
        metavar="PATH",
        nargs="*",
        help="Configuration file(s).",
    )

    parser.add_argument(
        "-b",
        "--bump-latest",
        action="store_true",
        dest="bump_latest",
        help="Deprecated, use --bump=auto instead. "
        "Guess the new latest version by bumping the previous one based on the set of unreleased commits. "
        "For example, if a commit contains breaking changes, bump the major number (or the minor number for 0.x versions). "
        "Else if there are new features, bump the minor number. Else just bump the patch number. "
        "Default: unset (false).",
    )
    parser.add_argument(
        "-B",
        "--bump",
        action="store",
        dest="bump",
        metavar="VERSION",
        help="Specify the bump from latest version for the set of unreleased commits. "
        "Can be one of `auto`, `major`, `minor`, `patch` or a valid SemVer version (eg. 1.2.3). "
        "For both SemVer and PEP 440 versioning schemes (see -n), `auto` will bump the major number "
        "if a commit contains breaking changes (or the minor number for 0.x versions, see -Z), "
        "else the minor number if there are new features, else the patch number. "
        "Default: unset (false).",
    )
    parser.add_argument(
        "-n",
        "--versioning",
        action="store",
        dest="versioning",
        metavar="SCHEME",
        help="Versioning scheme to use when bumping and comparing versions. "
        "The selected scheme will impact the values accepted by the `--bump` option. "
        "Supported: `pep440`, `semver`. PEP 440 provides the following bump strategies: `auto`, "
        f"`{'`, `'.join(part for part in bump_pep440.strategies if '+' not in part)}`. "
        "Values `auto`, `major`, `minor`, `micro` can be suffixed with one of `+alpha`, `+beta`, `+candidate`, "
        "and/or `+dev`. Values `alpha`, `beta` and `candidate` can be suffixed with `+dev`. "
        "Examples: `auto+alpha`, `major+beta+dev`, `micro+dev`, `candidate+dev`, etc.. "
        "SemVer provides the following bump strategies: `auto`, "
        f"`{'`, `'.join(bump_semver.strategies)}`. "
        "See the docs for more information. Default: unset (`semver`).",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )
    parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        dest="in_place",
        help="Insert new entries (versions missing from changelog) in-place. "
        "An output file must be specified. With custom templates, "
        "you can pass two additional arguments: `--version-regex` and `--marker-line`. "
        "When writing in-place, an `in_place` variable "
        "will be injected in the Jinja context, "
        "allowing to adapt the generated contents "
        "(for example to skip changelog headers or footers). Default: unset (false).",
    )
    parser.add_argument(
        "-g",
        "--version-regex",
        action="store",
        metavar="REGEX",
        dest="version_regex",
        help="A regular expression to match versions in the existing changelog "
        "(used to find the latest release) when writing in-place. "
        "The regular expression must be a Python regex with a `version` named group. "
        f"Default: `{DEFAULT_VERSION_REGEX}`.",
    )

    parser.add_argument(
        "-m",
        "--marker-line",
        action="store",
        metavar="MARKER",
        dest="marker_line",
        help="A marker line at which to insert new entries "
        "(versions missing from changelog). "
        "If two marker lines are present in the changelog, "
        "the contents between those two lines will be overwritten "
        "(useful to update an 'Unreleased' entry for example). "
        f"Default: `{DEFAULT_MARKER_LINE}`.",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        metavar="FILE",
        dest="output",
        help="Output to given file. Default: standard output.",
    )
    parser.add_argument(
        "-p",
        "--provider",
        metavar="PROVIDER",
        dest="provider",
        choices=providers.keys(),
        help="Explicitly specify the repository provider. Default: unset.",
    )
    parser.add_argument(
        "-r",
        "--parse-refs",
        action="store_true",
        dest="parse_refs",
        help="Parse provider-specific references in commit messages (GitHub/GitLab/Bitbucket "
        "issues, PRs, etc.). Default: unset (false).",
    )
    parser.add_argument(
        "-R",
        "--release-notes",
        action="store_true",
        dest="release_notes",
        help="Output release notes to stdout based on the last entry in the changelog. Default: unset (false).",
    )
    parser.add_argument(
        "-I",
        "--input",
        metavar="FILE",
        dest="input",
        help=f"Read from given file when creating release notes. Default: `{DEFAULT_CHANGELOG_FILE}`.",
    )
    parser.add_argument(
        "-c",
        "--convention",
        "--commit-style",
        "--style",
        metavar="CONVENTION",
        choices=CONVENTIONS,
        dest="convention",
        help=f"The commit convention to match against. Default: `{DEFAULT_SETTINGS['convention']}`.",
    )
    parser.add_argument(
        "-s",
        "--sections",
        action="store",
        type=_comma_separated_list,
        metavar="SECTIONS",
        dest="sections",
        help="A comma-separated list of sections to render. "
        "See the available sections for each supported convention in the description. "
        "Default: unset (None).",
    )
    parser.add_argument(
        "-t",
        "--template",
        choices=Templates(("angular", "keepachangelog")),
        metavar="TEMPLATE",
        dest="template",
        help="The Jinja2 template to use. Prefix it with `path:` to specify the path "
        "to a Jinja templated file. "
        f"Default: `{DEFAULT_SETTINGS['template']}`.",
    )
    parser.add_argument(
        "-T",
        "--trailers",
        "--git-trailers",
        action="store_true",
        dest="parse_trailers",
        help="Parse Git trailers in the commit message. "
        "See https://git-scm.com/docs/git-interpret-trailers. Default: unset (false).",
    )
    parser.add_argument(
        "-E",
        "--omit-empty-versions",
        action="store_true",
        dest="omit_empty_versions",
        help="Omit empty versions from the output. Default: unset (false).",
    )
    parser.add_argument(
        "-Z",
        "--no-zerover",
        action="store_false",
        dest="zerover",
        help="By default, breaking changes on a 0.x don't bump the major version, maintaining it at 0. "
        "With this option, a breaking change will bump a 0.x version to 1.0.",
    )
    parser.add_argument(
        "-F",
        "--filter-commits",
        action="store",
        metavar="RANGE",
        dest="filter_commits",
        help="The Git revision-range filter to use (e.g. `v1.2.0..`). Default: no filter.",
    )
    parser.add_argument(
        "-j",
        "--jinja-context",
        action=_ParseDictAction,
        metavar="KEY=VALUE",
        dest="jinja_context",
        help="Pass additional key/value pairs to the template. Option can be used multiple times. "
        "The key/value pairs are accessible as 'jinja_context' in the template.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {debug.get_version()}",
        help="Show the current version of the program and exit.",
    )
    parser.add_argument("--debug-info", action=_DebugInfo, help="Print debug information.")

    return parser


def _latest(lines: list[str], regex: Pattern) -> str | None:
    for line in lines:
        match = regex.search(line)
        if match:
            return match.groupdict()["version"]
    return None


def _unreleased(versions: list[Version], last_release: str) -> list[Version]:
    for index, version in enumerate(versions):
        if version.tag == last_release:
            return versions[:index]
    return versions


def read_config(
    config_file: Sequence[str | Path] | str | Path | None = DEFAULT_CONFIG_FILES,
) -> dict:
    """Find config files and initialize settings with the one of highest priority.

    Parameters:
        config_file: A path or list of paths to configuration file(s); or `None` to
            disable config file settings. Default: a list of paths given by
            [`git_changelog.cli.DEFAULT_CONFIG_FILES`][].

    Returns:
        A settings dictionary. Default settings if no config file is found or `config_file` is `None`.

    """
    project_config = DEFAULT_SETTINGS.copy()
    if config_file is None:  # Unset config file
        return project_config

    for filename in config_file if isinstance(config_file, (list, tuple)) else [config_file]:
        _path = Path(filename)

        if not _path.exists():
            continue

        with _path.open("rb") as file:
            new_settings = tomllib.load(file)
        if _path.name == "pyproject.toml":
            new_settings = new_settings.get("tool", {}).get("git-changelog", {}) or new_settings.get(
                "tool.git-changelog",
                {},
            )

            if not new_settings:  # pyproject.toml did not have a git-changelog section
                continue

        # Settings can have hyphens like in the CLI
        new_settings = {key.replace("-", "_"): value for key, value in new_settings.items()}

        # TODO: remove at some point
        if "bump_latest" in new_settings:
            _opt_value = new_settings["bump_latest"]
            _suggestion = (
                "remove it from the config file" if not _opt_value else "set `bump = 'auto'` in the config file instead"
            )
            warnings.warn(
                f"`bump-latest = {str(_opt_value).lower()}` option found "
                f"in config file ({_path.absolute()}). This option will be removed in the future. "
                f"To achieve the same result, please {_suggestion}.",
                FutureWarning,
                stacklevel=1,
            )

        # Massage found values to meet expectations
        # Parse sections
        if "sections" in new_settings:
            # Remove "sections" from dict, only restore if the list is valid
            sections = new_settings.pop("sections", None)
            if isinstance(sections, str):
                sections = sections.split(",")

            sections = [s.strip() for s in sections if isinstance(s, str) and s.strip()]

            if sections:  # toml doesn't store null/nil
                new_settings["sections"] = sections

        project_config.update(new_settings)
        break

    return project_config


def parse_settings(args: list[str] | None = None) -> dict:
    """Parse arguments and config files to build the final settings set.

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        A dictionary with the final settings.
    """
    parser = get_parser()
    opts = vars(parser.parse_args(args=args))

    # Determine which arguments were explicitly set with the CLI
    sentinel = object()
    sentinel_ns = argparse.Namespace(**{key: sentinel for key in opts})
    explicit_opts_dict = {
        key: opts.get(key, None)
        for key, value in vars(parser.parse_args(namespace=sentinel_ns, args=args)).items()
        if value is not sentinel
    }

    config_file = explicit_opts_dict.pop("config_file", DEFAULT_CONFIG_FILES)
    if str(config_file).strip().lower() in ("no", "none", "off", "false", "0", ""):
        config_file = None
    elif str(config_file).strip().lower() in ("yes", "default", "on", "true", "1"):
        config_file = DEFAULT_CONFIG_FILES

    jinja_context = explicit_opts_dict.pop("jinja_context", {})

    settings = read_config(config_file)

    # CLI arguments override the config file settings
    settings.update(explicit_opts_dict)

    # Merge jinja context, CLI values override config file values.
    settings["jinja_context"].update(jinja_context)

    # TODO: remove at some point
    if "bump_latest" in explicit_opts_dict:
        warnings.warn("`--bump-latest` is deprecated in favor of `--bump=auto`", FutureWarning, stacklevel=1)

    return settings


def build_and_render(
    repository: str,
    template: str,
    convention: str | CommitConvention,
    parse_refs: bool = False,  # noqa: FBT001,FBT002
    parse_trailers: bool = False,  # noqa: FBT001,FBT002
    sections: list[str] | None = None,
    in_place: bool = False,  # noqa: FBT001,FBT002
    output: str | TextIO | None = None,
    version_regex: str = DEFAULT_VERSION_REGEX,
    marker_line: str = DEFAULT_MARKER_LINE,
    bump_latest: bool = False,  # noqa: FBT001,FBT002
    omit_empty_versions: bool = False,  # noqa: FBT001,FBT002
    provider: str | None = None,
    bump: str | None = None,
    zerover: bool = True,  # noqa: FBT001,FBT002
    filter_commits: str | None = None,
    jinja_context: dict[str, Any] | None = None,
    versioning: Literal["pep440", "semver"] = "semver",
) -> tuple[Changelog, str]:
    """Build a changelog and render it.

    This function returns the changelog instance and the rendered contents,
    but also updates the specified output file (side-effect) or writes to stdout.

    Parameters:
        repository: Path to a local repository.
        template: Name of a builtin template, or path to a custom template (prefixed with `path:`).
        convention: Name of a commit message style/convention.
        parse_refs: Whether to parse provider-specific references (GitHub/GitLab issues, PRs, etc.).
        parse_trailers: Whether to parse Git trailers.
        sections: Sections to render (features, bug fixes, etc.).
        in_place: Whether to update the changelog in-place.
        output: Output/changelog file.
        version_regex: Regular expression to match versions in an existing changelog file.
        marker_line: Marker line used to insert contents in an existing changelog.
        bump_latest: Deprecated, use --bump=auto instead.
            Whether to try and bump the latest version to guess the new one.
        omit_empty_versions: Whether to omit empty versions from the output.
        provider: Provider class used by this repository.
        bump: Whether to try and bump to a given version.
        zerover: Keep major version at zero, even for breaking changes.
        filter_commits: The Git revision-range used to filter commits in git-log.
        jinja_context: Key/value pairs passed to the Jinja template.
        versioning: Versioning scheme to use when grouping commits and bumping versions.

    Raises:
        ValueError: When some arguments are incompatible or missing.

    Returns:
        The built changelog and the rendered contents.
    """
    # get template
    if template.startswith("path:"):
        path = template.replace("path:", "", 1)
        try:
            jinja_template = templates.get_custom_template(path)
        except TemplateNotFound as error:
            raise ValueError(f"No such file: {path}") from error
    else:
        jinja_template = templates.get_template(template)

    if output is None:
        output = sys.stdout

    # handle misconfiguration early
    if in_place and output is sys.stdout:
        raise ValueError("Cannot write in-place to stdout")

    # get provider
    provider_class = providers[provider] if provider else None

    # TODO: remove at some point
    if bump_latest:
        warnings.warn("`bump_latest=True` is deprecated in favor of `bump='auto'`", DeprecationWarning, stacklevel=1)
        if bump is None:
            bump = "auto"

    # build data
    changelog = Changelog(
        repository,
        provider=provider_class,
        convention=convention,
        parse_provider_refs=parse_refs,
        parse_trailers=parse_trailers,
        sections=sections,
        bump=bump,
        zerover=zerover,
        filter_commits=filter_commits,
        versioning=versioning,
    )

    # remove empty versions from changelog data
    if omit_empty_versions:
        section_set = set(changelog.sections)
        empty_versions = [
            version for version in changelog.versions_list if section_set.isdisjoint(version.sections_dict.keys())
        ]
        for version in empty_versions:
            changelog.versions_list.remove(version)
            changelog.versions_dict.pop(version.tag)

    # render new entries in-place
    if in_place:
        # read current changelog lines
        with open(output) as changelog_file:  # type: ignore[arg-type]
            lines = changelog_file.read().splitlines()

        # prepare version regex and marker line
        if template in {"angular", "keepachangelog"}:
            version_regex = DEFAULT_VERSION_REGEX
            marker_line = DEFAULT_MARKER_LINE

        # only keep new entries (missing from changelog)
        last_released = _latest(lines, re.compile(version_regex))
        if last_released:
            # check if the latest version is already in the changelog
            if last_released in [
                changelog.versions_list[0].tag,
                changelog.versions_list[0].planned_tag,
            ]:
                raise ValueError(f"Version {last_released} already in changelog")
            changelog.versions_list = _unreleased(
                changelog.versions_list,
                last_released,
            )

        # render new entries
        rendered = (
            jinja_template.render(
                changelog=changelog,
                jinja_context=jinja_context,
                in_place=True,
            ).rstrip("\n")
            + "\n"
        )

        # find marker line(s) in current changelog
        marker = lines.index(marker_line)
        try:
            marker2 = lines[marker + 1 :].index(marker_line)
        except ValueError:
            # apply new entries at marker line
            lines[marker] = rendered
        else:
            # apply new entries between marker lines
            lines[marker : marker + marker2 + 2] = [rendered]

        # write back updated changelog lines
        with open(output, "w") as changelog_file:  # type: ignore[arg-type]
            changelog_file.write("\n".join(lines).rstrip("\n") + "\n")

    # overwrite output file
    else:
        rendered = jinja_template.render(changelog=changelog, jinja_context=jinja_context)

        # write result in specified output
        if output is sys.stdout:
            sys.stdout.write(rendered)
        else:
            with open(output, "w") as stream:  # type: ignore[arg-type]
                stream.write(rendered)

    return changelog, rendered


def get_release_notes(
    input_file: str | Path = "CHANGELOG.md",
    version_regex: str = DEFAULT_VERSION_REGEX,
    marker_line: str = DEFAULT_MARKER_LINE,
) -> str:
    """Get release notes from existing changelog.

    This will return the latest entry in the changelog.

    Parameters:
        input_file: The changelog to read from.
        version_regex: A regular expression to match version entries.
        marker_line: The insertion marker line in the changelog.

    Returns:
        The latest changelog entry.
    """
    release_notes = []
    found_marker = False
    found_version = False
    with open(input_file) as changelog:
        for line in changelog:
            line = line.strip()  # noqa: PLW2901
            if not found_marker:
                if line == marker_line:
                    found_marker = True
                continue
            if re.search(version_regex, line):
                if found_version:
                    break
                found_version = True
            release_notes.append(line)
    result = "\n".join(release_notes).strip()
    if result.endswith(marker_line):
        result = result[: -len(marker_line)].strip()
    return result


def output_release_notes(
    input_file: str = "CHANGELOG.md",
    version_regex: str = DEFAULT_VERSION_REGEX,
    marker_line: str = DEFAULT_MARKER_LINE,
    output_file: str | TextIO | None = None,
) -> None:
    """Print release notes from existing changelog.

    This will print the latest entry in the changelog.

    Parameters:
        input_file: The changelog to read from.
        version_regex: A regular expression to match version entries.
        marker_line: The insertion marker line in the changelog.
        output_file: Where to print/write the release notes.
    """
    output_file = output_file or sys.stdout
    release_notes = get_release_notes(input_file, version_regex, marker_line)
    try:
        output_file.write(release_notes)  # type: ignore[union-attr]
    except AttributeError:
        with open(output_file, "w") as file:  # type: ignore[arg-type]
            file.write(release_notes)


def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `git-changelog` or `python -m git_changelog`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    settings = parse_settings(args)

    if settings.pop("release_notes"):
        output_release_notes(
            input_file=settings["input"],
            version_regex=settings["version_regex"],
            marker_line=settings["marker_line"],
            output_file=None,  # force writing to stdout
        )
        return 0

    # --input is not necessary anymore
    settings.pop("input", None)
    try:
        build_and_render(**settings)
    except ValueError as error:
        print(f"git-changelog: {error}", file=sys.stderr)
        return 1

    return 0
