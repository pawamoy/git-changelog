# git\_changelog

git-changelog package.

Automatic Changelog generator using Jinja2 templates.

Modules:

- **`build`** –

  Deprecated. Import from `git_changelog` directly.
- **`cli`** –

  Deprecated. Import from `git_changelog` directly.
- **`commit`** –

  Deprecated. Import from `git_changelog` directly.
- **`providers`** –

  Deprecated. Import from `git_changelog` directly.
- **`templates`** –

  Deprecated. Import from `git_changelog` directly.
- **`versioning`** –

  Deprecated. Import from `git_changelog` directly.

Classes:

- **`AngularConvention`** –

  Angular commit message convention.
- **`BasicConvention`** –

  Basic commit message convention.
- **`Bitbucket`** –

  A parser for the Bitbucket references.
- **`Changelog`** –

  The main changelog class.
- **`Commit`** –

  A class to represent a commit.
- **`CommitConvention`** –

  A base class for a convention of commit messages.
- **`ConventionalCommitConventionV0`** –

  Original Conventional Commit convention, including patch bumps for other commit types.
- **`ConventionalCommitConventionV1`** –

  Conventional Commits 1.0.0, with version bumps only for features, fixes, and breaking changes.
- **`Forgejo`** –

  A parser for the Forgejo references.
- **`GitHub`** –

  A parser for the GitHub references.
- **`GitLab`** –

  A parser for the GitLab references.
- **`LinuxConvention`** –

  Linux commit message convention.
- **`PEP440Bumper`** –

  PEP 440 version bumper.
- **`PEP440Version`** –

  PEP 440 version.
- **`ParsedVersion`** –

  Base class for versioning schemes.
- **`ProviderRefParser`** –

  A base class for specific providers reference parsers.
- **`Ref`** –

  A class to represent a reference and its URL.
- **`RefDef`** –

  A class to store a reference regular expression and URL building string.
- **`RefRe`** –

  An enum helper to store parts of regular expressions for references.
- **`Section`** –

  A list of commits grouped by section\_type.
- **`SemVerBumper`** –

  SemVer version bumper.
- **`SemVerVersion`** –

  SemVer version.
- **`Templates`** –

  Helper to pick a template on the command line.
- **`Version`** –

  A class to represent a changelog version.
- **`VersionBumper`** –

  Base class for version bumpers.

Functions:

- **`build_and_render`** –

  Build a changelog and render it.
- **`bump`** –

  Bump a version. Deprecated, use [`bump_semver`](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.bump_semver> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-attribute\"></code>            <span class=\"doc doc-object-name doc-attribute-name\">bump_semver</span>     <span class=\"doc doc-labels\">       <small class=\"doc doc-label doc-label-module-attribute\"><code>module-attribute</code></small>   </span>") instead.
- **`configure_env`** –

  Configure the Jinja environment.
- **`get_custom_template`** –

  Get a custom template instance.
- **`get_parser`** –

  Return the CLI argument parser.
- **`get_release_notes`** –

  Get release notes from existing changelog.
- **`get_template`** –

  Get a builtin template instance.
- **`get_version`** –

  Return the current `git-changelog` version.
- **`main`** –

  Run the main program.
- **`output_release_notes`** –

  Print release notes from existing changelog.
- **`parse_pep440`** –

  Parse a PEP version.
- **`parse_semver`** –

  Parse a SemVer version.
- **`parse_settings`** –

  Parse arguments and config files to build the final settings set.
- **`parse_version`** –

  Parse a version. Deprecated, use [`bump_semver`](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.parse_semver> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-function\"></code>            <span class=\"doc doc-object-name doc-function-name\">parse_semver</span>") instead.
- **`read_config`** –

  Find config files and initialize settings with the one of highest priority.
- **`render`** –

  Render a changelog.
- **`version_prefix`** –

  Return a version and its optional `v` prefix.

Attributes:

- **`CONVENTIONS`** –

  Available commit message conventions.
- **`ConventionType`** –

  The type of convention used for commits.
- **`ConventionalCommitConvention`** –

  Alias for the original Conventional Commit convention.
- **`DEFAULT_CHANGELOG_FILE`** –

  Default changelog file name.
- **`DEFAULT_CONFIG_FILES`** –

  Default configuration files read by git-changelog.
- **`DEFAULT_MARKER_LINE`** –

  Default marker line for finding insertion points.
- **`DEFAULT_SETTINGS`** (`dict[str, Any]`) –

  Default settings for the CLI.
- **`DEFAULT_VERSIONING`** –

  Default versioning strategy.
- **`DEFAULT_VERSION_REGEX`** –

  Default version regex for finding versions.
- **`JINJA_ENV`** –

  The Jinja environment.
- **`PEP440Strategy`** –

  PEP 440 versioning strategies.
- **`SemVerStrategy`** –

  SemVer versioning strategies.
- **`TEMPLATES_PATH`** –

  The path to the templates directory.
- **`bump_pep440`** –

  Bump a PEP 440 version.
- **`bump_semver`** –

  Bump a SemVer version.

## CONVENTIONS

```
CONVENTIONS = sorted(Changelog.CONVENTION)
```

Available commit message conventions.

## ConventionType

```
ConventionType = (
    str | CommitConvention | type[CommitConvention]
)
```

The type of convention used for commits.

## ConventionalCommitConvention

```
ConventionalCommitConvention = (
    ConventionalCommitConventionV0
)
```

Alias for the original Conventional Commit convention.

## DEFAULT\_CHANGELOG\_FILE

```
DEFAULT_CHANGELOG_FILE = 'CHANGELOG.md'
```

Default changelog file name.

## DEFAULT\_CONFIG\_FILES

```
DEFAULT_CONFIG_FILES = [
    "pyproject.toml",
    ".git-changelog.toml",
    "config/git-changelog.toml",
    ".config/git-changelog.toml",
    str(Path(user_config_dir()) / "git-changelog.toml"),
]
```

Default configuration files read by git-changelog.

## DEFAULT\_MARKER\_LINE

```
DEFAULT_MARKER_LINE = '<!-- insertion marker -->'
```

Default marker line for finding insertion points.

## DEFAULT\_SETTINGS

```
DEFAULT_SETTINGS: dict[str, Any] = {
    "bump": None,
    "bump_latest": None,
    "convention": "basic",
    "filter_commits": None,
    "in_place": False,
    "include_all": False,
    "input": DEFAULT_CHANGELOG_FILE,
    "marker_line": None,
    "omit_empty_versions": False,
    "output": sys.stdout,
    "parse_refs": False,
    "parse_trailers": False,
    "provider": None,
    "remote": None,
    "remote_url": None,
    "release_notes": False,
    "latest_version": False,
    "bumped_version": False,
    "repository": ".",
    "sections": None,
    "template": "keepachangelog",
    "jinja_context": {},
    "version_regex": None,
    "versioning": DEFAULT_VERSIONING,
    "zerover": True,
}
```

Default settings for the CLI.

## DEFAULT\_VERSIONING

```
DEFAULT_VERSIONING = 'semver'
```

Default versioning strategy.

## DEFAULT\_VERSION\_REGEX

```
DEFAULT_VERSION_REGEX = '^## \\[(?P<version>v?[^\\]]+)'
```

Default version regex for finding versions.

## JINJA\_ENV

```
JINJA_ENV = Environment()
```

The Jinja environment.

## PEP440Strategy

```
PEP440Strategy = Literal[
    "epoch",
    "release",
    "major",
    "minor",
    "micro",
    "patch",
    "pre",
    "alpha",
    "beta",
    "candidate",
    "post",
    "dev",
    "major+alpha",
    "major+beta",
    "major+candidate",
    "major+dev",
    "major+alpha+dev",
    "major+beta+dev",
    "major+candidate+dev",
    "minor+alpha",
    "minor+beta",
    "minor+candidate",
    "minor+dev",
    "minor+alpha+dev",
    "minor+beta+dev",
    "minor+candidate+dev",
    "micro+alpha",
    "micro+beta",
    "micro+candidate",
    "micro+dev",
    "micro+alpha+dev",
    "micro+beta+dev",
    "micro+candidate+dev",
    "alpha+dev",
    "beta+dev",
    "candidate+dev",
]
```

PEP 440 versioning strategies.

## SemVerStrategy

```
SemVerStrategy = Literal[
    "major", "minor", "patch", "release"
]
```

SemVer versioning strategies.

## TEMPLATES\_PATH

```
TEMPLATES_PATH = Path(__file__).parent
```

The path to the templates directory.

## bump\_pep440

```
bump_pep440 = PEP440Bumper(PEP440Strategy.__args__)
```

Bump a PEP 440 version.

## bump\_semver

```
bump_semver = SemVerBumper(SemVerStrategy.__args__)
```

Bump a SemVer version.

## AngularConvention

Bases: `CommitConvention`

Angular commit message convention.

Methods:

- **`is_major`** –

  Tell if this commit is worth a major bump.
- **`is_minor`** –

  Tell if this commit is worth a minor bump.
- **`parse_breaking_changes`** –

  Extract breaking change sections, or use the subject of a major commit.
- **`parse_commit`** –

  Parse the commit to extract information.
- **`parse_subject`** –

  Parse the subject of the commit (`<type>[(scope)]: Subject`).

Attributes:

- **`BREAKING_CHANGE_REGEX`** (`Pattern`) –

  The singular, space-separated marker used to extract breaking change descriptions.
- **`BREAK_REGEX`** (`Pattern`) –

  The commit message breaking change regex.
- **`DEFAULT_RENDER`** (`list[str]`) –

  The default sections to render.
- **`SUBJECT_REGEX`** (`Pattern`) –

  The commit message subject regex.
- **`TRAILER_REGEX`** (`Pattern`) –

  The trailer token and value regex, also accepting Conventional Commits reference footers.
- **`TYPES`** (`dict[str, str]`) –

  The commit message types.
- **`TYPE_REGEX`** (`Pattern`) –

  The commit message type regex.

### BREAKING\_CHANGE\_REGEX

```
BREAKING_CHANGE_REGEX: Pattern = re.compile(
    "^BREAKING CHANGE: (?P<description>\\S.*)$",
    re.MULTILINE,
)
```

The singular, space-separated marker used to extract breaking change descriptions.

### BREAK\_REGEX

```
BREAK_REGEX: Pattern = re.compile(
    "^break(s|ing changes?)?[ :].+$",
    re.IGNORECASE | re.MULTILINE,
)
```

The commit message breaking change regex.

### DEFAULT\_RENDER

```
DEFAULT_RENDER: list[str] = [
    TYPES["feat"],
    TYPES["fix"],
    TYPES["revert"],
    TYPES["refactor"],
    TYPES["perf"],
]
```

The default sections to render.

### SUBJECT\_REGEX

```
SUBJECT_REGEX: Pattern = re.compile(
    f"^(?P<type>({'|'.join(TYPES.keys())}))(?:\\((?P<scope>.+)\\))?: (?P<subject>.+)$"
)
```

The commit message subject regex.

### TRAILER\_REGEX

```
TRAILER_REGEX: Pattern = re.compile(
    "^[A-Za-z0-9-]+[ \\t]*(?::(?!//)[^\\r\\n]*| #[^\\r\\n]+)$"
)
```

The trailer token and value regex, also accepting Conventional Commits reference footers.

### TYPES

```
TYPES: dict[str, str] = {
    "build": "Build",
    "chore": "Chore",
    "ci": "Continuous Integration",
    "deps": "Dependencies",
    "doc": "Docs",
    "docs": "Docs",
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance Improvements",
    "ref": "Code Refactoring",
    "refactor": "Code Refactoring",
    "revert": "Reverts",
    "style": "Style",
    "test": "Tests",
    "tests": "Tests",
}
```

The commit message types.

### TYPE\_REGEX

```
TYPE_REGEX: Pattern
```

The commit message type regex.

### is\_major

```
is_major(commit_message: str) -> bool
```

Tell if this commit is worth a major bump.

Parameters:

- #### **`commit_message`**

  (`str`) –

  The commit message.

Returns:

- `bool` –

  Whether it's a major commit.

### is\_minor

```
is_minor(commit_type: str) -> bool
```

Tell if this commit is worth a minor bump.

Parameters:

- #### **`commit_type`**

  (`str`) –

  The commit type.

Returns:

- `bool` –

  Whether it's a minor commit.

### parse\_breaking\_changes

```
parse_breaking_changes(commit: Commit) -> list[str]
```

Extract breaking change sections, or use the subject of a major commit.

Sections end at another breaking change marker or the final Git trailer block. Markdown code fences protect their contents from section delimiters.

### parse\_commit

```
parse_commit(commit: Commit) -> dict[str, str | bool]
```

Parse the commit to extract information.

Parameters:

- #### **`commit`**

  (`Commit`) –

  The commit to parse.

Returns:

- `dict[str, str | bool]` –

  A dictionary containing the parsed data.

### parse\_subject

```
parse_subject(commit_subject: str) -> dict[str, str]
```

Parse the subject of the commit (`<type>[(scope)]: Subject`).

Parameters:

- #### **`commit_subject`**

  (`str`) –

  The commit message subject.

Returns:

- `dict[str, str]` –

  The parsed data.

## BasicConvention

Bases: `CommitConvention`

Basic commit message convention.

Methods:

- **`is_major`** –

  Tell if this commit is worth a major bump.
- **`is_minor`** –

  Tell if this commit is worth a minor bump.
- **`parse_breaking_changes`** –

  Extract breaking change sections, or use the subject of a major commit.
- **`parse_commit`** –

  Parse the commit to extract information.
- **`parse_type`** –

  Parse the type of the commit given its subject.

Attributes:

- **`BREAKING_CHANGE_REGEX`** (`Pattern`) –

  The singular, space-separated marker used to extract breaking change descriptions.
- **`BREAK_REGEX`** (`Pattern`) –

  The commit message breaking change regex.
- **`DEFAULT_RENDER`** (`list[str]`) –

  The default sections to render.
- **`TRAILER_REGEX`** (`Pattern`) –

  The trailer token and value regex, also accepting Conventional Commits reference footers.
- **`TYPES`** (`dict[str, str]`) –

  The commit message types.
- **`TYPE_REGEX`** (`Pattern`) –

  The commit message type regex.

### BREAKING\_CHANGE\_REGEX

```
BREAKING_CHANGE_REGEX: Pattern = re.compile(
    "^BREAKING CHANGE: (?P<description>\\S.*)$",
    re.MULTILINE,
)
```

The singular, space-separated marker used to extract breaking change descriptions.

### BREAK\_REGEX

```
BREAK_REGEX: Pattern = re.compile(
    "^break(s|ing changes?)?[ :].+$",
    re.IGNORECASE | re.MULTILINE,
)
```

The commit message breaking change regex.

### DEFAULT\_RENDER

```
DEFAULT_RENDER: list[str] = [
    TYPES["add"],
    TYPES["fix"],
    TYPES["change"],
    TYPES["remove"],
]
```

The default sections to render.

### TRAILER\_REGEX

```
TRAILER_REGEX: Pattern = re.compile(
    "^[A-Za-z0-9-]+[ \\t]*(?::(?!//)[^\\r\\n]*| #[^\\r\\n]+)$"
)
```

The trailer token and value regex, also accepting Conventional Commits reference footers.

### TYPES

```
TYPES: dict[str, str] = {
    "add": "Added",
    "fix": "Fixed",
    "change": "Changed",
    "remove": "Removed",
    "merge": "Merged",
    "doc": "Documented",
}
```

The commit message types.

### TYPE\_REGEX

```
TYPE_REGEX: Pattern = re.compile(
    f"^(?P<type>({'|'.join(TYPES.keys())}))", re.IGNORECASE
)
```

The commit message type regex.

### is\_major

```
is_major(commit_message: str) -> bool
```

Tell if this commit is worth a major bump.

Parameters:

- #### **`commit_message`**

  (`str`) –

  The commit message.

Returns:

- `bool` –

  Whether it's a major commit.

### is\_minor

```
is_minor(commit_type: str) -> bool
```

Tell if this commit is worth a minor bump.

Parameters:

- #### **`commit_type`**

  (`str`) –

  The commit type.

Returns:

- `bool` –

  Whether it's a minor commit.

### parse\_breaking\_changes

```
parse_breaking_changes(commit: Commit) -> list[str]
```

Extract breaking change sections, or use the subject of a major commit.

Sections end at another breaking change marker or the final Git trailer block. Markdown code fences protect their contents from section delimiters.

### parse\_commit

```
parse_commit(commit: Commit) -> dict[str, str | bool]
```

Parse the commit to extract information.

Parameters:

- #### **`commit`**

  (`Commit`) –

  The commit to parse.

Returns:

- `dict[str, str | bool]` –

  A dictionary containing the parsed data.

### parse\_type

```
parse_type(commit_subject: str) -> str
```

Parse the type of the commit given its subject.

Parameters:

- #### **`commit_subject`**

  (`str`) –

  The commit message subject.

Returns:

- `str` –

  The commit type.

## Bitbucket

```
Bitbucket(
    namespace: str, project: str, url: str | None = None
)
```

Bases: `ProviderRefParser`

A parser for the Bitbucket references.

Parameters:

- ### **`namespace`**

  (`str`) –

  The Bitbucket namespace.
- ### **`project`**

  (`str`) –

  The Bitbucket project.
- ### **`url`**

  (`str | None`, default: `None` ) –

  The Bitbucket URL.

Methods:

- **`build_ref_url`** –

  Build the URL for a reference type and a dictionary of matched groups.
- **`get_compare_url`** –

  Get the URL for a tag comparison.
- **`get_refs`** –

  Find all references in the given text.
- **`get_tag_url`** –

  Get the URL for a git tag.
- **`parse_refs`** –

  Parse references in the given text.

Attributes:

- **`REF`** (`dict[str, RefDef]`) –

  The reference definitions for the provider.
- **`commit_max_length`** –

  The maximum length of a commit hash.
- **`commit_min_length`** –

  The minimum length of a commit hash.
- **`namespace`** (`str`) –

  The namespace for the provider.
- **`project`** (`str`) –

  The project for the provider.
- **`project_url`** (`str`) –

  The project URL for the provider.
- **`tag_url`** (`str`) –

  The tag URL for the provider.
- **`url`** (`str`) –

  The base URL for the provider.

### REF

```
REF: dict[str, RefDef] = {
    "issues": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?issue\\s*"
            + RefRe.ID.format(symbol="#"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/issues/{ref}",
    ),
    "merge_requests": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?pull request\\s*"
            + RefRe.ID.format(symbol="#"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/pull-request/{ref}",
    ),
    "commits": RefDef(
        regex=re.compile(
            RefRe.BB
            + "(?:{np}@)?{commit}{ba}".format(
                np=RefRe.NP,
                commit=RefRe.COMMIT.format(
                    min=commit_min_length,
                    max=commit_max_length,
                ),
                ba=RefRe.BA,
            ),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/commits/{ref}",
    ),
    "commits_ranges": RefDef(
        regex=re.compile(
            RefRe.BB
            + "(?:{np}@)?{commit_range}".format(
                np=RefRe.NP,
                commit_range=RefRe.COMMIT_RANGE.format(
                    min=commit_min_length,
                    max=commit_max_length,
                ),
            ),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/branches/compare/{ref}#diff",
    ),
    "mentions": RefDef(
        regex=re.compile(
            RefRe.BB + RefRe.MENTION, re.IGNORECASE
        ),
        url_string="{base_url}/{ref}",
    ),
}
```

The reference definitions for the provider.

### commit\_max\_length

```
commit_max_length = 40
```

The maximum length of a commit hash.

### commit\_min\_length

```
commit_min_length = 8
```

The minimum length of a commit hash.

### namespace

```
namespace: str = namespace
```

The namespace for the provider.

### project

```
project: str = project
```

The project for the provider.

### project\_url

```
project_url: str = '{base_url}/{namespace}/{project}'
```

The project URL for the provider.

### tag\_url

```
tag_url: str = (
    "{base_url}/{namespace}/{project}/commits/tag/{ref}"
)
```

The tag URL for the provider.

### url

```
url: str = 'https://bitbucket.org'
```

The base URL for the provider.

### build\_ref\_url

```
build_ref_url(
    ref_type: str, match_dict: dict[str, str]
) -> str
```

Build the URL for a reference type and a dictionary of matched groups.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`match_dict`**

  (`dict[str, str]`) –

  The matched groups.

Returns:

- `str` –

  The built URL.

### get\_compare\_url

```
get_compare_url(base: str, target: str) -> str
```

Get the URL for a tag comparison.

Parameters:

- #### **`base`**

  (`str`) –

  The base tag.
- #### **`target`**

  (`str`) –

  The target tag.

Returns:

- `str` –

  The comparison URL.

### get\_refs

```
get_refs(ref_type: str, text: str) -> list[Ref]
```

Find all references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text in which to search references.

Returns:

- `list[Ref]` –

  A list of references (instances of [Ref](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.Ref> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-class\"></code>            <span class=\"doc doc-object-name doc-class-name\">Ref</span>")).

### get\_tag\_url

```
get_tag_url(tag: str = '') -> str
```

Get the URL for a git tag.

Parameters:

- #### **`tag`**

  (`str`) –

  The git tag.

Returns:

- `str` –

  The tag URL.

### parse\_refs

```
parse_refs(ref_type: str, text: str) -> list[Match]
```

Parse references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text to parse.

Returns:

- `list[Match]` –

  A list of regular expressions matches.

## Changelog

```
Changelog(
    repository: str | Path,
    *,
    provider: ProviderRefParser
    | type[ProviderRefParser]
    | None = None,
    convention: ConventionType | None = None,
    parse_provider_refs: bool = False,
    parse_trailers: bool = False,
    sections: list[str] | None = None,
    bump_latest: bool = False,
    bump: str | None = None,
    zerover: bool = True,
    filter_commits: str | None = None,
    include_all: bool = False,
    versioning: Literal["semver", "pep440"] = "semver",
    remote: str | None = None,
    remote_url: str | None = None,
)
```

The main changelog class.

Parameters:

- ### **`repository`**

  (`str | Path`) –

  The repository (directory) for which to build the changelog.
- ### **`provider`**

  (`ProviderRefParser | type[ProviderRefParser] | None`, default: `None` ) –

  The provider to use (github.com, gitlab.com, etc.).
- ### **`convention`**

  (`ConventionType | None`, default: `None` ) –

  The commit convention to use (angular, etc.).
- ### **`parse_provider_refs`**

  (`bool`, default: `False` ) –

  Whether to parse provider-specific references in the commit messages.
- ### **`parse_trailers`**

  (`bool`, default: `False` ) –

  Whether to parse Git trailers in the commit messages.
- ### **`sections`**

  (`list[str] | None`, default: `None` ) –

  The sections to render (features, bug fixes, etc.).
- ### **`bump_latest`**

  (`bool`, default: `False` ) –

  Deprecated, use `bump="auto"` instead. Whether to try and bump latest version to guess new one.
- ### **`bump`**

  (`str | None`, default: `None` ) –

  Whether to try and bump to a given version.
- ### **`zerover`**

  (`bool`, default: `True` ) –

  Keep major version at zero, even for breaking changes.
- ### **`filter_commits`**

  (`str | None`, default: `None` ) –

  The Git revision-range used to filter commits in git-log (e.g: `v1.0.1..`).
- ### **`include_all`**

  (`bool`, default: `False` ) –

  Whether to include commits without a recognized type.
- ### **`remote`**

  (`str | None`, default: `None` ) –

  Git remote name. Defaults to `GIT_CHANGELOG_REMOTE`, or `origin`.
- ### **`remote_url`**

  (`str | None`, default: `None` ) –

  Repository URL. Defaults to `GIT_CHANGELOG_REMOTE_URL`, or the selected remote's URL.

Methods:

- **`get_log`** –

  Get the `git log` output.
- **`get_remote_url`** –

  Get the git remote URL for the repository.
- **`parse_commits`** –

  Parse the output of 'git log' into a list of commits.
- **`run_git`** –

  Run a git command in the chosen repository.

Attributes:

- **`CONVENTION`** (`dict[str, type[CommitConvention]]`) –

  Available commit message conventions.
- **`FORMAT`** (`str`) –

  Format string for the changelog.
- **`MARKER`** (`str`) –

  Marker for the changelog.
- **`commits`** (`list[Commit]`) –

  The list of parsed commits.
- **`convention`** (`CommitConvention`) –

  The commit convention to use.
- **`filter_commits`** (`str | None`) –

  The Git revision-range used to filter commits in git-log (e.g: `v1.0.1..`).
- **`parse_provider_refs`** (`bool`) –

  Whether to parse provider-specific references in the commit messages.
- **`parse_trailers`** (`bool`) –

  Whether to parse Git trailers in the commit messages.
- **`provider`** –

  The provider to use (github.com, gitlab.com, etc.).
- **`raw_log`** (`str`) –

  The raw Git log output.
- **`remote_url`** (`str`) –

  The remote URL of the repository.
- **`repository`** (`str | Path`) –

  The repository (directory) for which to build the changelog.
- **`sections`** –

  The sections to include in the changelog.
- **`tag_commits`** (`list[Commit]`) –

  The list of tagged commits.
- **`version_bumper`** –

  The version bumper function.
- **`version_parser`** –

  The version parser function.
- **`versions_dict`** –

  The dictionary of versions.
- **`versions_list`** –

  The list of versions.
- **`zerover`** (`bool`) –

  Whether to keep major version at zero, even for breaking changes.

### CONVENTION

```
CONVENTION: dict[str, type[CommitConvention]] = {
    "basic": BasicConvention,
    "angular": AngularConvention,
    "conventional": ConventionalCommitConvention,
    "conventional-v0": ConventionalCommitConventionV0,
    "conventional-v1": ConventionalCommitConventionV1,
    "linux": LinuxConvention,
}
```

Available commit message conventions.

### FORMAT

```
FORMAT: str = (
    "%H%n%an%n%ae%n%ad%n%cn%n%ce%n%cd%n%D%n%P%n%s%n%b%n"
    + MARKER
)
```

Format string for the changelog.

### MARKER

```
MARKER: str = '--GIT-CHANGELOG MARKER--'
```

Marker for the changelog.

### commits

```
commits: list[Commit] = self.parse_commits()
```

The list of parsed commits.

### convention

```
convention: CommitConvention = convention
```

The commit convention to use.

### filter\_commits

```
filter_commits: str | None = filter_commits
```

The Git revision-range used to filter commits in git-log (e.g: `v1.0.1..`).

### parse\_provider\_refs

```
parse_provider_refs: bool = parse_provider_refs
```

Whether to parse provider-specific references in the commit messages.

### parse\_trailers

```
parse_trailers: bool = parse_trailers
```

Whether to parse Git trailers in the commit messages.

### provider

```
provider = provider
```

The provider to use (github.com, gitlab.com, etc.).

### raw\_log

```
raw_log: str = self.get_log()
```

The raw Git log output.

### remote\_url

```
remote_url: str = remote_url
```

The remote URL of the repository.

### repository

```
repository: str | Path = repository
```

The repository (directory) for which to build the changelog.

### sections

```
sections = sections
```

The sections to include in the changelog.

### tag\_commits

```
tag_commits: list[Commit] = [
    commit for commit in self.commits[1:] if commit.tag
]
```

The list of tagged commits.

### version\_bumper

```
version_bumper = version_bumper
```

The version bumper function.

### version\_parser

```
version_parser = version_parser
```

The version parser function.

### versions\_dict

```
versions_dict = v_dict
```

The dictionary of versions.

### versions\_list

```
versions_list = v_list
```

The list of versions.

### zerover

```
zerover: bool = zerover
```

Whether to keep major version at zero, even for breaking changes.

### get\_log

```
get_log() -> str
```

Get the `git log` output.

Returns:

- `str` –

  The output of the `git log` command, with a particular format.

### get\_remote\_url

```
get_remote_url() -> str
```

Get the git remote URL for the repository.

Returns:

- `str` –

  The explicitly configured URL, or the selected Git remote URL.

### parse\_commits

```
parse_commits() -> list[Commit]
```

Parse the output of 'git log' into a list of commits.

The commits build a Git commit graph by referencing their parent commits. Commits are ordered from newest to oldest.

Returns:

- `list[Commit]` –

  The list of commits.

### run\_git

```
run_git(*args: str) -> str
```

Run a git command in the chosen repository.

Parameters:

- #### **`*args`**

  (`str`, default: `()` ) –

  Arguments passed to the git command.

Returns:

- `str` –

  The git command output.

## Commit

```
Commit(
    commit_hash: str,
    author_name: str = "",
    author_email: str = "",
    author_date: str | datetime = "",
    committer_name: str = "",
    committer_email: str = "",
    committer_date: str | datetime = "",
    refs: str = "",
    subject: str = "",
    body: list[str] | None = None,
    url: str = "",
    *,
    parse_trailers: bool = False,
    parent_hashes: str | list[str] = "",
    commits_map: dict[str, Commit] | None = None,
    version_parser: Callable[
        [str], tuple[ParsedVersion, str]
    ]
    | None = None,
)
```

A class to represent a commit.

Parameters:

- ### **`commit_hash`**

  (`str`) –

  The commit hash.
- ### **`author_name`**

  (`str`, default: `''` ) –

  The author name.
- ### **`author_email`**

  (`str`, default: `''` ) –

  The author email.
- ### **`author_date`**

  (`str | datetime`, default: `''` ) –

  The authoring date (datetime, UTC timestamp with optional timezone offset).
- ### **`committer_name`**

  (`str`, default: `''` ) –

  The committer name.
- ### **`committer_email`**

  (`str`, default: `''` ) –

  The committer email.
- ### **`committer_date`**

  (`str | datetime`, default: `''` ) –

  The committing date (datetime, UTC timestamp with optional timezone offset).
- ### **`refs`**

  (`str`, default: `''` ) –

  The commit refs.
- ### **`subject`**

  (`str`, default: `''` ) –

  The commit message subject.
- ### **`body`**

  (`list[str] | None`, default: `None` ) –

  The commit message body.
- ### **`url`**

  (`str`, default: `''` ) –

  The commit URL.
- ### **`parse_trailers`**

  (`bool`, default: `False` ) –

  Whether to parse Git trailers.

Methods:

- **`update_with_convention`** –

  Apply the convention-parsed data to this commit.
- **`update_with_provider`** –

  Apply the provider-parsed data to this commit.

Attributes:

- **`author_date`** (`datetime`) –

  The author date.
- **`author_email`** (`str`) –

  The author email.
- **`author_name`** (`str`) –

  The author name.
- **`body`** (`list[str]`) –

  The commit body.
- **`body_without_trailers`** –

  The commit body without trailers.
- **`breaking_changes`** (`list[str]`) –

  Breaking change descriptions, populated when a convention is applied.
- **`committer_date`** (`datetime`) –

  The committer date.
- **`committer_email`** (`str`) –

  The committer email.
- **`committer_name`** (`str`) –

  The committer name.
- **`convention`** (`dict[str, Any]`) –

  The commit message convention.
- **`hash`** (`str`) –

  The commit hash.
- **`parent_commits`** (`list[Commit]`) –

  Parent commits of this commit.
- **`parent_hashes`** –

  The parent commit hashes.
- **`subject`** (`str`) –

  The commit subject.
- **`tag`** (`str`) –

  The commit tag.
- **`text_refs`** (`dict[str, list[Ref]]`) –

  The commit text references.
- **`trailers`** (`list[tuple[str, str]]`) –

  The commit trailers.
- **`url`** (`str`) –

  The commit URL.
- **`version`** (`str`) –

  The commit version.

### author\_date

```
author_date: datetime = author_date
```

The author date.

### author\_email

```
author_email: str = author_email
```

The author email.

### author\_name

```
author_name: str = author_name
```

The author name.

### body

```
body: list[str] = _clean_body(body) if body else []
```

The commit body.

### body\_without\_trailers

```
body_without_trailers = self.body
```

The commit body without trailers.

### breaking\_changes

```
breaking_changes: list[str] = []
```

Breaking change descriptions, populated when a convention is applied.

### committer\_date

```
committer_date: datetime = committer_date
```

The committer date.

### committer\_email

```
committer_email: str = committer_email
```

The committer email.

### committer\_name

```
committer_name: str = committer_name
```

The committer name.

### convention

```
convention: dict[str, Any] = {}
```

The commit message convention.

### hash

```
hash: str = commit_hash
```

The commit hash.

### parent\_commits

```
parent_commits: list[Commit]
```

Parent commits of this commit.

### parent\_hashes

```
parent_hashes = parent_hashes
```

The parent commit hashes.

### subject

```
subject: str = subject
```

The commit subject.

### tag

```
tag: str = tag
```

The commit tag.

### text\_refs

```
text_refs: dict[str, list[Ref]] = {}
```

The commit text references.

### trailers

```
trailers: list[tuple[str, str]] = _Trailers()
```

The commit trailers.

### url

```
url: str = url
```

The commit URL.

### version

```
version: str = tag
```

The commit version.

### update\_with\_convention

```
update_with_convention(
    convention: CommitConvention,
) -> None
```

Apply the convention-parsed data to this commit.

Parameters:

- #### **`convention`**

  (`CommitConvention`) –

  The convention to use.

### update\_with\_provider

```
update_with_provider(
    provider: ProviderRefParser, parse_refs: bool = True
) -> None
```

Apply the provider-parsed data to this commit.

Parameters:

- #### **`provider`**

  (`ProviderRefParser`) –

  The provider to use.
- #### **`parse_refs`**

  (`bool`, default: `True` ) –

  Whether to parse references for this provider.

## CommitConvention

Bases: `ABC`

A base class for a convention of commit messages.

Methods:

- **`parse_breaking_changes`** –

  Extract breaking change sections, or use the subject of a major commit.
- **`parse_commit`** –

  Parse the commit to extract information.

Attributes:

- **`BREAKING_CHANGE_REGEX`** (`Pattern`) –

  The singular, space-separated marker used to extract breaking change descriptions.
- **`BREAK_REGEX`** (`Pattern`) –

  The commit message breaking change regex.
- **`DEFAULT_RENDER`** (`list[str]`) –

  The sections rendered by default.
- **`TRAILER_REGEX`** (`Pattern`) –

  The trailer token and value regex, also accepting Conventional Commits reference footers.
- **`TYPES`** (`dict[str, str]`) –

  The commit message types.
- **`TYPE_REGEX`** (`Pattern`) –

  The commit message type regex.

### BREAKING\_CHANGE\_REGEX

```
BREAKING_CHANGE_REGEX: Pattern = re.compile(
    "^BREAKING CHANGE: (?P<description>\\S.*)$",
    re.MULTILINE,
)
```

The singular, space-separated marker used to extract breaking change descriptions.

### BREAK\_REGEX

```
BREAK_REGEX: Pattern
```

The commit message breaking change regex.

### DEFAULT\_RENDER

```
DEFAULT_RENDER: list[str]
```

The sections rendered by default.

### TRAILER\_REGEX

```
TRAILER_REGEX: Pattern = re.compile(
    "^[A-Za-z0-9-]+[ \\t]*(?::(?!//)[^\\r\\n]*| #[^\\r\\n]+)$"
)
```

The trailer token and value regex, also accepting Conventional Commits reference footers.

### TYPES

```
TYPES: dict[str, str]
```

The commit message types.

### TYPE\_REGEX

```
TYPE_REGEX: Pattern
```

The commit message type regex.

### parse\_breaking\_changes

```
parse_breaking_changes(commit: Commit) -> list[str]
```

Extract breaking change sections, or use the subject of a major commit.

Sections end at another breaking change marker or the final Git trailer block. Markdown code fences protect their contents from section delimiters.

### parse\_commit

```
parse_commit(commit: Commit) -> dict[str, str | bool]
```

Parse the commit to extract information.

Parameters:

- #### **`commit`**

  (`Commit`) –

  The commit to parse.

Returns:

- `dict[str, str | bool]` –

  A dictionary containing the parsed data.

## ConventionalCommitConventionV0

Bases: `AngularConvention`

Original Conventional Commit convention, including patch bumps for other commit types.

Methods:

- **`is_major`** –

  Tell if this commit is worth a major bump.
- **`is_minor`** –

  Tell if this commit is worth a minor bump.
- **`parse_breaking_changes`** –

  Extract breaking change sections, or use the subject of a major commit.
- **`parse_commit`** –

  Parse the commit to extract information.
- **`parse_subject`** –

  Parse the subject of the commit (`<type>[(scope)]: Subject`).

Attributes:

- **`BREAKING_CHANGE_REGEX`** (`Pattern`) –

  The singular, space-separated marker used to extract breaking change descriptions.
- **`BREAK_REGEX`** (`Pattern`) –

  The commit message breaking change regex.
- **`DEFAULT_RENDER`** (`list[str]`) –

  The default sections to render.
- **`SUBJECT_REGEX`** (`Pattern`) –

  The commit message subject regex.
- **`TRAILER_REGEX`** (`Pattern`) –

  The trailer token and value regex, also accepting Conventional Commits reference footers.
- **`TYPES`** (`dict[str, str]`) –

  The commit message types.
- **`TYPE_REGEX`** (`Pattern`) –

  The commit message type regex.

### BREAKING\_CHANGE\_REGEX

```
BREAKING_CHANGE_REGEX: Pattern = re.compile(
    "^BREAKING CHANGE: (?P<description>\\S.*)$",
    re.MULTILINE,
)
```

The singular, space-separated marker used to extract breaking change descriptions.

### BREAK\_REGEX

```
BREAK_REGEX: Pattern = re.compile(
    "^break(s|ing changes?)?[ :].+$",
    re.IGNORECASE | re.MULTILINE,
)
```

The commit message breaking change regex.

### DEFAULT\_RENDER

```
DEFAULT_RENDER: list[str] = AngularConvention.DEFAULT_RENDER
```

The default sections to render.

### SUBJECT\_REGEX

```
SUBJECT_REGEX: Pattern = re.compile(
    f"^(?P<type>({'|'.join(TYPES.keys())}))(?:\\((?P<scope>.+)\\))?(?P<breaking>!)?: (?P<subject>.+)$"
)
```

The commit message subject regex.

### TRAILER\_REGEX

```
TRAILER_REGEX: Pattern = re.compile(
    "^[A-Za-z0-9-]+[ \\t]*(?::(?!//)[^\\r\\n]*| #[^\\r\\n]+)$"
)
```

The trailer token and value regex, also accepting Conventional Commits reference footers.

### TYPES

```
TYPES: dict[str, str] = AngularConvention.TYPES
```

The commit message types.

### TYPE\_REGEX

```
TYPE_REGEX: Pattern
```

The commit message type regex.

### is\_major

```
is_major(commit_message: str) -> bool
```

Tell if this commit is worth a major bump.

Parameters:

- #### **`commit_message`**

  (`str`) –

  The commit message.

Returns:

- `bool` –

  Whether it's a major commit.

### is\_minor

```
is_minor(commit_type: str) -> bool
```

Tell if this commit is worth a minor bump.

Parameters:

- #### **`commit_type`**

  (`str`) –

  The commit type.

Returns:

- `bool` –

  Whether it's a minor commit.

### parse\_breaking\_changes

```
parse_breaking_changes(commit: Commit) -> list[str]
```

Extract breaking change sections, or use the subject of a major commit.

Sections end at another breaking change marker or the final Git trailer block. Markdown code fences protect their contents from section delimiters.

### parse\_commit

```
parse_commit(commit: Commit) -> dict[str, str | bool]
```

Parse the commit to extract information.

Parameters:

- #### **`commit`**

  (`Commit`) –

  The commit to parse.

Returns:

- `dict[str, str | bool]` –

  A dictionary containing the parsed data.

### parse\_subject

```
parse_subject(commit_subject: str) -> dict[str, str]
```

Parse the subject of the commit (`<type>[(scope)]: Subject`).

Parameters:

- #### **`commit_subject`**

  (`str`) –

  The commit message subject.

Returns:

- `dict[str, str]` –

  The parsed data.

## ConventionalCommitConventionV1

Bases: `ConventionalCommitConventionV0`

Conventional Commits 1.0.0, with version bumps only for features, fixes, and breaking changes.

Methods:

- **`is_major`** –

  Tell whether the message contains an uppercase breaking change footer.
- **`is_minor`** –

  Tell if this commit is worth a minor bump.
- **`is_patch`** –

  Tell whether the parsed commit type warrants a patch bump.
- **`parse_breaking_changes`** –

  Extract breaking change sections, or use the subject of a major commit.
- **`parse_commit`** –

  Parse the commit and select its highest applicable version bump.
- **`parse_subject`** –

  Parse a Conventional Commits subject and map known types to section titles.

Attributes:

- **`BREAKING_CHANGE_REGEX`** (`Pattern`) –

  The singular, space-separated marker used to extract breaking change descriptions.
- **`BREAK_REGEX`** (`Pattern`) –

  The case-sensitive breaking change footer regex.
- **`DEFAULT_RENDER`** (`list[str]`) –

  The default sections to render.
- **`FOOTER_REGEX`** (`Pattern`) –

  The footer token and separator regex.
- **`SUBJECT_REGEX`** (`Pattern`) –

  The commit subject regex, including custom types and case-insensitive matching.
- **`TRAILER_REGEX`** (`Pattern`) –

  The trailer token and value regex, also accepting Conventional Commits reference footers.
- **`TYPES`** (`dict[str, str]`) –

  The commit message types.
- **`TYPE_REGEX`** (`Pattern`) –

  The commit message type regex.

### BREAKING\_CHANGE\_REGEX

```
BREAKING_CHANGE_REGEX: Pattern = re.compile(
    "^BREAKING CHANGE: (?P<description>\\S.*)$",
    re.MULTILINE,
)
```

The singular, space-separated marker used to extract breaking change descriptions.

### BREAK\_REGEX

```
BREAK_REGEX: Pattern = (
    CommitConvention.BREAKING_CHANGE_REGEX
)
```

The case-sensitive breaking change footer regex.

### DEFAULT\_RENDER

```
DEFAULT_RENDER: list[str] = AngularConvention.DEFAULT_RENDER
```

The default sections to render.

### FOOTER\_REGEX

```
FOOTER_REGEX: Pattern = re.compile(
    "^(?:BREAKING CHANGE|[\\w-]+)(?:: | #).+$"
)
```

The footer token and separator regex.

### SUBJECT\_REGEX

```
SUBJECT_REGEX: Pattern = re.compile(
    "^(?P<type>[^\\s():!]+)(?:\\((?P<scope>[^()\\r\\n]+)\\))?(?P<breaking>!)?: (?P<subject>\\S.*)$",
    re.IGNORECASE,
)
```

The commit subject regex, including custom types and case-insensitive matching.

### TRAILER\_REGEX

```
TRAILER_REGEX: Pattern = re.compile(
    "^[A-Za-z0-9-]+[ \\t]*(?::(?!//)[^\\r\\n]*| #[^\\r\\n]+)$"
)
```

The trailer token and value regex, also accepting Conventional Commits reference footers.

### TYPES

```
TYPES: dict[str, str] = AngularConvention.TYPES
```

The commit message types.

### TYPE\_REGEX

```
TYPE_REGEX: Pattern
```

The commit message type regex.

### is\_major

```
is_major(commit_message: str) -> bool
```

Tell whether the message contains an uppercase breaking change footer.

### is\_minor

```
is_minor(commit_type: str) -> bool
```

Tell if this commit is worth a minor bump.

Parameters:

- #### **`commit_type`**

  (`str`) –

  The commit type.

Returns:

- `bool` –

  Whether it's a minor commit.

### is\_patch

```
is_patch(commit_type: str) -> bool
```

Tell whether the parsed commit type warrants a patch bump.

### parse\_breaking\_changes

```
parse_breaking_changes(commit: Commit) -> list[str]
```

Extract breaking change sections, or use the subject of a major commit.

Sections end at another breaking change marker or the final Git trailer block. Markdown code fences protect their contents from section delimiters.

### parse\_commit

```
parse_commit(commit: Commit) -> dict[str, str | bool]
```

Parse the commit and select its highest applicable version bump.

### parse\_subject

```
parse_subject(commit_subject: str) -> dict[str, str]
```

Parse a Conventional Commits subject and map known types to section titles.

## Forgejo

```
Forgejo(
    namespace: str, project: str, url: str | None = None
)
```

Bases: `ProviderRefParser`

A parser for the Forgejo references.

Parameters:

- ### **`namespace`**

  (`str`) –

  The Bitbucket namespace.
- ### **`project`**

  (`str`) –

  The Bitbucket project.
- ### **`url`**

  (`str | None`, default: `None` ) –

  The Bitbucket URL.

Methods:

- **`build_ref_url`** –

  Build the URL for a reference type and a dictionary of matched groups.
- **`get_compare_url`** –

  Get the URL for a tag comparison.
- **`get_refs`** –

  Find all references in the given text.
- **`get_tag_url`** –

  Get the URL for a git tag.
- **`parse_refs`** –

  Parse references in the given text.

Attributes:

- **`REF`** (`dict[str, RefDef]`) –

  The reference definitions for the provider.
- **`commit_max_length`** –

  The maximum length of a commit hash.
- **`commit_min_length`** –

  The minimum length of a commit hash.
- **`namespace`** (`str`) –

  The namespace for the provider.
- **`project`** (`str`) –

  The project for the provider.
- **`project_url`** (`str`) –

  The project URL for the provider.
- **`tag_url`** (`str`) –

  The tag URL for the provider.
- **`url`** (`str`) –

  The base URL for the provider.

### REF

```
REF: dict[str, RefDef] = {
    "issues": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ID.format(symbol="#"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/issues/{ref}",
    ),
    "merge_requests": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ID.format(symbol="#"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/pulls/{ref}",
    ),
    "commits": RefDef(
        regex=re.compile(
            RefRe.BB
            + "(?:{np}@)?{commit}{ba}".format(
                np=RefRe.NP,
                commit=RefRe.COMMIT.format(
                    min=commit_min_length,
                    max=commit_max_length,
                ),
                ba=RefRe.BA,
            ),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/commit/{ref}",
    ),
    "commits_ranges": RefDef(
        regex=re.compile(
            RefRe.BB
            + "(?:{np}@)?{commit_range}".format(
                np=RefRe.NP,
                commit_range=RefRe.COMMIT_RANGE.format(
                    min=commit_min_length,
                    max=commit_max_length,
                ),
            ),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/compare/{ref}",
    ),
    "mentions": RefDef(
        regex=re.compile(
            RefRe.BB + RefRe.MENTION, re.IGNORECASE
        ),
        url_string="{base_url}/{ref}",
    ),
}
```

The reference definitions for the provider.

### commit\_max\_length

```
commit_max_length = 40
```

The maximum length of a commit hash.

### commit\_min\_length

```
commit_min_length = 8
```

The minimum length of a commit hash.

### namespace

```
namespace: str = namespace
```

The namespace for the provider.

### project

```
project: str = project
```

The project for the provider.

### project\_url

```
project_url: str = '{base_url}/{namespace}/{project}'
```

The project URL for the provider.

### tag\_url

```
tag_url: str = (
    "{base_url}/{namespace}/{project}/src/tag/{ref}"
)
```

The tag URL for the provider.

### url

```
url: str = 'https://codeberg.org'
```

The base URL for the provider.

### build\_ref\_url

```
build_ref_url(
    ref_type: str, match_dict: dict[str, str]
) -> str
```

Build the URL for a reference type and a dictionary of matched groups.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`match_dict`**

  (`dict[str, str]`) –

  The matched groups.

Returns:

- `str` –

  The built URL.

### get\_compare\_url

```
get_compare_url(base: str, target: str) -> str
```

Get the URL for a tag comparison.

Parameters:

- #### **`base`**

  (`str`) –

  The base tag.
- #### **`target`**

  (`str`) –

  The target tag.

Returns:

- `str` –

  The comparison URL.

### get\_refs

```
get_refs(ref_type: str, text: str) -> list[Ref]
```

Find all references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text in which to search references.

Returns:

- `list[Ref]` –

  A list of references (instances of [Ref](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.Ref> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-class\"></code>            <span class=\"doc doc-object-name doc-class-name\">Ref</span>")).

### get\_tag\_url

```
get_tag_url(tag: str = '') -> str
```

Get the URL for a git tag.

Parameters:

- #### **`tag`**

  (`str`) –

  The git tag.

Returns:

- `str` –

  The tag URL.

### parse\_refs

```
parse_refs(ref_type: str, text: str) -> list[Match]
```

Parse references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text to parse.

Returns:

- `list[Match]` –

  A list of regular expressions matches.

## GitHub

```
GitHub(
    namespace: str, project: str, url: str | None = None
)
```

Bases: `ProviderRefParser`

A parser for the GitHub references.

Parameters:

- ### **`namespace`**

  (`str`) –

  The Bitbucket namespace.
- ### **`project`**

  (`str`) –

  The Bitbucket project.
- ### **`url`**

  (`str | None`, default: `None` ) –

  The Bitbucket URL.

Methods:

- **`build_ref_url`** –

  Build the URL for a reference type and a dictionary of matched groups.
- **`get_compare_url`** –

  Get the URL for a tag comparison.
- **`get_refs`** –

  Find all references in the given text.
- **`get_tag_url`** –

  Get the URL for a git tag.
- **`parse_refs`** –

  Parse references in the given text.

Attributes:

- **`REF`** (`dict[str, RefDef]`) –

  The reference definitions for the provider.
- **`commit_max_length`** –

  The maximum length of a commit hash.
- **`commit_min_length`** –

  The minimum length of a commit hash.
- **`namespace`** (`str`) –

  The namespace for the provider.
- **`project`** (`str`) –

  The project for the provider.
- **`project_url`** (`str`) –

  The project URL for the provider.
- **`tag_url`** (`str`) –

  The tag URL for the provider.
- **`url`** (`str`) –

  The base URL for the provider.

### REF

```
REF: dict[str, RefDef] = {
    "issues": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ID.format(symbol="#"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/issues/{ref}",
    ),
    "commits": RefDef(
        regex=re.compile(
            RefRe.BB
            + "(?:{np}@)?{commit}{ba}".format(
                np=RefRe.NP,
                commit=RefRe.COMMIT.format(
                    min=commit_min_length,
                    max=commit_max_length,
                ),
                ba=RefRe.BA,
            ),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/commit/{ref}",
    ),
    "commits_ranges": RefDef(
        regex=re.compile(
            RefRe.BB
            + "(?:{np}@)?{commit_range}".format(
                np=RefRe.NP,
                commit_range=RefRe.COMMIT_RANGE.format(
                    min=commit_min_length,
                    max=commit_max_length,
                ),
            ),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/compare/{ref}",
    ),
    "mentions": RefDef(
        regex=re.compile(
            RefRe.BB + RefRe.MENTION, re.IGNORECASE
        ),
        url_string="{base_url}/{ref}",
    ),
}
```

The reference definitions for the provider.

### commit\_max\_length

```
commit_max_length = 40
```

The maximum length of a commit hash.

### commit\_min\_length

```
commit_min_length = 8
```

The minimum length of a commit hash.

### namespace

```
namespace: str = namespace
```

The namespace for the provider.

### project

```
project: str = project
```

The project for the provider.

### project\_url

```
project_url: str = '{base_url}/{namespace}/{project}'
```

The project URL for the provider.

### tag\_url

```
tag_url: str = (
    "{base_url}/{namespace}/{project}/releases/tag/{ref}"
)
```

The tag URL for the provider.

### url

```
url: str = 'https://github.com'
```

The base URL for the provider.

### build\_ref\_url

```
build_ref_url(
    ref_type: str, match_dict: dict[str, str]
) -> str
```

Build the URL for a reference type and a dictionary of matched groups.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`match_dict`**

  (`dict[str, str]`) –

  The matched groups.

Returns:

- `str` –

  The built URL.

### get\_compare\_url

```
get_compare_url(base: str, target: str) -> str
```

Get the URL for a tag comparison.

Parameters:

- #### **`base`**

  (`str`) –

  The base tag.
- #### **`target`**

  (`str`) –

  The target tag.

Returns:

- `str` –

  The comparison URL.

### get\_refs

```
get_refs(ref_type: str, text: str) -> list[Ref]
```

Find all references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text in which to search references.

Returns:

- `list[Ref]` –

  A list of references (instances of [Ref](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.Ref> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-class\"></code>            <span class=\"doc doc-object-name doc-class-name\">Ref</span>")).

### get\_tag\_url

```
get_tag_url(tag: str = '') -> str
```

Get the URL for a git tag.

Parameters:

- #### **`tag`**

  (`str`) –

  The git tag.

Returns:

- `str` –

  The tag URL.

### parse\_refs

```
parse_refs(ref_type: str, text: str) -> list[Match]
```

Parse references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text to parse.

Returns:

- `list[Match]` –

  A list of regular expressions matches.

## GitLab

```
GitLab(
    namespace: str, project: str, url: str | None = None
)
```

Bases: `ProviderRefParser`

A parser for the GitLab references.

Parameters:

- ### **`namespace`**

  (`str`) –

  The Bitbucket namespace.
- ### **`project`**

  (`str`) –

  The Bitbucket project.
- ### **`url`**

  (`str | None`, default: `None` ) –

  The Bitbucket URL.

Methods:

- **`build_ref_url`** –

  Build the URL for a reference type and a dictionary of matched groups.
- **`get_compare_url`** –

  Get the URL for a tag comparison.
- **`get_refs`** –

  Find all references in the given text.
- **`get_tag_url`** –

  Get the URL for a git tag.
- **`parse_refs`** –

  Parse references in the given text.

Attributes:

- **`REF`** (`dict[str, RefDef]`) –

  The reference definitions for the provider.
- **`commit_max_length`** –

  The maximum length of a commit hash.
- **`commit_min_length`** –

  The minimum length of a commit hash.
- **`namespace`** (`str`) –

  The namespace for the provider.
- **`project`** (`str`) –

  The project for the provider.
- **`project_url`** (`str`) –

  The project URL for the provider.
- **`tag_url`** (`str`) –

  The tag URL for the provider.
- **`url`** (`str`) –

  The base URL for the provider.

### REF

```
REF: dict[str, RefDef] = {
    "issues": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ID.format(symbol="#"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/issues/{ref}",
    ),
    "merge_requests": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ID.format(symbol="!"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/merge_requests/{ref}",
    ),
    "snippets": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ID.format(symbol="\\$"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/snippets/{ref}",
    ),
    "labels_ids": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ID.format(symbol="~"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
    ),
    "labels_one_word": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ONE_WORD.format(symbol="~"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
    ),
    "labels_multi_word": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.MULTI_WORD.format(symbol="~"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
    ),
    "milestones_ids": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ID.format(symbol="%"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/milestones/{ref}",
    ),
    "milestones_one_word": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.ONE_WORD.format(symbol="%"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/milestones",
    ),
    "milestones_multi_word": RefDef(
        regex=re.compile(
            RefRe.BB
            + RefRe.NP
            + "?"
            + RefRe.MULTI_WORD.format(symbol="%"),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/milestones",
    ),
    "commits": RefDef(
        regex=re.compile(
            RefRe.BB
            + "(?:{np}@)?{commit}{ba}".format(
                np=RefRe.NP,
                commit=RefRe.COMMIT.format(
                    min=commit_min_length,
                    max=commit_max_length,
                ),
                ba=RefRe.BA,
            ),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/commit/{ref}",
    ),
    "commits_ranges": RefDef(
        regex=re.compile(
            RefRe.BB
            + "(?:{np}@)?{commit_range}".format(
                np=RefRe.NP,
                commit_range=RefRe.COMMIT_RANGE.format(
                    min=commit_min_length,
                    max=commit_max_length,
                ),
            ),
            re.IGNORECASE,
        ),
        url_string="{base_url}/{namespace}/{project}/compare/{ref}",
    ),
    "mentions": RefDef(
        regex=re.compile(
            RefRe.BB + RefRe.MENTION, re.IGNORECASE
        ),
        url_string="{base_url}/{ref}",
    ),
}
```

The reference definitions for the provider.

### commit\_max\_length

```
commit_max_length = 40
```

The maximum length of a commit hash.

### commit\_min\_length

```
commit_min_length = 8
```

The minimum length of a commit hash.

### namespace

```
namespace: str = namespace
```

The namespace for the provider.

### project

```
project: str = project
```

The project for the provider.

### project\_url

```
project_url: str = '{base_url}/{namespace}/{project}'
```

The project URL for the provider.

### tag\_url

```
tag_url: str = "{base_url}/{namespace}/{project}/tags/{ref}"
```

The tag URL for the provider.

### url

```
url: str = 'https://gitlab.com'
```

The base URL for the provider.

### build\_ref\_url

```
build_ref_url(
    ref_type: str, match_dict: dict[str, str]
) -> str
```

Build the URL for a reference type and a dictionary of matched groups.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`match_dict`**

  (`dict[str, str]`) –

  The matched groups.

Returns:

- `str` –

  The built URL.

### get\_compare\_url

```
get_compare_url(base: str, target: str) -> str
```

Get the URL for a tag comparison.

Parameters:

- #### **`base`**

  (`str`) –

  The base tag.
- #### **`target`**

  (`str`) –

  The target tag.

Returns:

- `str` –

  The comparison URL.

### get\_refs

```
get_refs(ref_type: str, text: str) -> list[Ref]
```

Find all references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text in which to search references.

Returns:

- `list[Ref]` –

  A list of references (instances of [Ref](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.Ref> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-class\"></code>            <span class=\"doc doc-object-name doc-class-name\">Ref</span>")).

### get\_tag\_url

```
get_tag_url(tag: str = '') -> str
```

Get the URL for a git tag.

Parameters:

- #### **`tag`**

  (`str`) –

  The git tag.

Returns:

- `str` –

  The tag URL.

### parse\_refs

```
parse_refs(ref_type: str, text: str) -> list[Match]
```

Parse references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text to parse.

Returns:

- `list[Match]` –

  A list of regular expressions matches.

## LinuxConvention

Bases: `BasicConvention`

Linux commit message convention.

Methods:

- **`is_major`** –

  Tell if this commit is worth a major bump.
- **`is_minor`** –

  Tell if this commit is worth a minor bump.
- **`parse_breaking_changes`** –

  Extract breaking change sections, or use the subject of a major commit.
- **`parse_commit`** –

  Parse the commit to extract information.
- **`parse_type`** –

  Parse the type of the commit given its subject.

Attributes:

- **`BREAKING_CHANGE_REGEX`** (`Pattern`) –

  The singular, space-separated marker used to extract breaking change descriptions.
- **`BREAK_REGEX`** (`Pattern`) –

  The commit message breaking change regex.
- **`DEFAULT_RENDER`** (`list[str]`) –

  The default sections to render.
- **`TRAILER_REGEX`** (`Pattern`) –

  The trailer token and value regex, also accepting Conventional Commits reference footers.
- **`TYPES`** (`dict[str, str]`) –

  The commit message types.
- **`TYPE_REGEX`** (`Pattern`) –

  The commit message type regex.

### BREAKING\_CHANGE\_REGEX

```
BREAKING_CHANGE_REGEX: Pattern = re.compile(
    "^BREAKING CHANGE: (?P<description>\\S.*)$",
    re.MULTILINE,
)
```

The singular, space-separated marker used to extract breaking change descriptions.

### BREAK\_REGEX

```
BREAK_REGEX: Pattern = re.compile(
    "^break(s|ing changes?)?[ :].+$",
    re.IGNORECASE | re.MULTILINE,
)
```

The commit message breaking change regex.

### DEFAULT\_RENDER

```
DEFAULT_RENDER: list[str] = [
    TYPES["add"],
    TYPES["fix"],
    TYPES["change"],
    TYPES["remove"],
]
```

The default sections to render.

### TRAILER\_REGEX

```
TRAILER_REGEX: Pattern = re.compile(
    "^[A-Za-z0-9-]+[ \\t]*(?::(?!//)[^\\r\\n]*| #[^\\r\\n]+)$"
)
```

The trailer token and value regex, also accepting Conventional Commits reference footers.

### TYPES

```
TYPES: dict[str, str] = {
    "add": "Added",
    "fix": "Fixed",
    "change": "Changed",
    "remove": "Removed",
    "merge": "Merged",
    "doc": "Documented",
}
```

The commit message types.

### TYPE\_REGEX

```
TYPE_REGEX: Pattern = re.compile(
    f"^(?P<type>({'|'.join(TYPES.keys())}))", re.IGNORECASE
)
```

The commit message type regex.

### is\_major

```
is_major(commit_message: str) -> bool
```

Tell if this commit is worth a major bump.

Parameters:

- #### **`commit_message`**

  (`str`) –

  The commit message.

Returns:

- `bool` –

  Whether it's a major commit.

### is\_minor

```
is_minor(commit_type: str) -> bool
```

Tell if this commit is worth a minor bump.

Parameters:

- #### **`commit_type`**

  (`str`) –

  The commit type.

Returns:

- `bool` –

  Whether it's a minor commit.

### parse\_breaking\_changes

```
parse_breaking_changes(commit: Commit) -> list[str]
```

Extract breaking change sections, or use the subject of a major commit.

Sections end at another breaking change marker or the final Git trailer block. Markdown code fences protect their contents from section delimiters.

### parse\_commit

```
parse_commit(commit: Commit) -> dict[str, str | bool]
```

Parse the commit to extract information.

Parameters:

- #### **`commit`**

  (`Commit`) –

  The commit to parse.

Returns:

- `dict[str, str | bool]` –

  A dictionary containing the parsed data.

### parse\_type

```
parse_type(commit_subject: str) -> str
```

Parse the type of the commit given its subject.

Parameters:

- #### **`commit_subject`**

  (`str`) –

  The commit message subject.

Returns:

- `str` –

  The commit type.

## PEP440Bumper

```
PEP440Bumper(strategies: tuple[str, ...])
```

Bases: `VersionBumper`

PEP 440 version bumper.

Parameters:

- ### **`strategies`**

  (`tuple[str, ...]`) –

  The supported bumping strategies.

Methods:

- **`__call__`** –

  Bump a PEP 440 version.

Attributes:

- **`initial`** (`str`) –

  The initial version.
- **`strategies`** –

  The supported bumping strategies.

### initial

```
initial: str = '0.0.0'
```

The initial version.

### strategies

```
strategies = strategies
```

The supported bumping strategies.

### \_\_call\_\_

```
__call__(
    version: str,
    strategy: PEP440Strategy = "micro",
    *,
    zerover: bool = False,
    trim: bool = False,
) -> str
```

Bump a PEP 440 version.

Parameters:

- #### **`version`**

  (`str`) –

  The version to bump.
- #### **`strategy`**

  (`PEP440Strategy`, default: `'micro'` ) –

  The part of the version to bump.
- #### **`zerover`**

  (`bool`, default: `False` ) –

  Keep major version at zero, even for breaking changes.
- #### **`trim`**

  (`bool`, default: `False` ) –

  Whether to trim all zeroes on the right after bumping.

Returns:

- `str` –

  The bumped version.

## PEP440Version

Bases: `Version`, `ParsedVersion`

PEP 440 version.

Methods:

- **`__eq__`** –

  Implement `==` comparison.
- **`__ge__`** –

  Implement `>=` comparison.
- **`__gt__`** –

  Implement `>` comparison.
- **`__le__`** –

  Implement `<=` comparison.
- **`__lt__`** –

  Implement `<` comparison.
- **`__ne__`** –

  Implement `!=` comparison.
- **`bump_alpha`** –

  Bump alpha-release.
- **`bump_beta`** –

  Bump beta-release.
- **`bump_candidate`** –

  Bump candidate release.
- **`bump_dev`** –

  Bump dev-release.
- **`bump_epoch`** –

  Bump epoch.
- **`bump_major`** –

  Bump major.
- **`bump_micro`** –

  Bump micro.
- **`bump_minor`** –

  Bump minor.
- **`bump_post`** –

  Bump post-release.
- **`bump_pre`** –

  Bump pre-release.
- **`bump_release`** –

  Bump given release level.
- **`dent_alpha`** –

  Dent to alpha-release.
- **`dent_beta`** –

  Dent to beta-release.
- **`dent_candidate`** –

  Dent to candidate release.
- **`dent_dev`** –

  Dent to dev-release.
- **`dent_pre`** –

  Dent to pre-release.
- **`from_parts`** –

  Build a version from its parts.

### \_\_eq\_\_

```
__eq__(other: object) -> bool
```

Implement `==` comparison.

### \_\_ge\_\_

```
__ge__(other: object) -> bool
```

Implement `>=` comparison.

### \_\_gt\_\_

```
__gt__(other: object) -> bool
```

Implement `>` comparison.

### \_\_le\_\_

```
__le__(other: object) -> bool
```

Implement `<=` comparison.

### \_\_lt\_\_

```
__lt__(other: object) -> bool
```

Implement `<` comparison.

### \_\_ne\_\_

```
__ne__(other: object) -> bool
```

Implement `!=` comparison.

### bump\_alpha

```
bump_alpha() -> PEP440Version
```

Bump alpha-release.

Examples:

```
>>> PEP440Version("1").bump_alpha()
ValueError: Cannot bump from release to alpha pre-release (use `dent_alpha`)
>>> PEP440Version("1a0").bump_alpha()
<Version('1a1')>
>>> PEP440Version("1a0").bump_alpha("a")
<Version('1a1')>
>>> PEP440Version("1a0.post0").bump_alpha()
<Version('1a1')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, same release, bumped alpha pre-release and the right parts reset to 0 or nothing.

### bump\_beta

```
bump_beta() -> PEP440Version
```

Bump beta-release.

Examples:

```
>>> PEP440Version("1").bump_beta()
ValueError: Cannot bump from release to beta pre-release (use `dent_beta`)
>>> PEP440Version("1b0").bump_beta()
<Version('1b1')>
>>> PEP440Version("1b0").bump_beta()
<Version('1b1')>
>>> PEP440Version("1b0.post0").bump_beta()
<Version('1b1')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, same release, bumped beta pre-release and the right parts reset to 0 or nothing.

### bump\_candidate

```
bump_candidate() -> PEP440Version
```

Bump candidate release.

Examples:

```
>>> PEP440Version("1").bump_candidate()
ValueError: Cannot bump from release to candidate pre-release (use `dent_candidate`)
>>> PEP440Version("1c0").bump_candidate()
<Version('1rc1')>
>>> PEP440Version("1c0").bump_candidate()
<Version('1rc1')>
>>> PEP440Version("1c0.post0").bump_candidate()
<Version('1rc1')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, same release, bumped candidate pre-release and the right parts reset to 0 or nothing.

### bump\_dev

```
bump_dev() -> PEP440Version
```

Bump dev-release.

Examples:

```
>>> PEP440Version("1").bump_dev()
ValueError: Cannot bump from release to dev-release (use `dent_dev`)
>>> PEP440Version("1a0").bump_dev()
ValueError: Cannot bump from alpha to dev-release (use `dent_dev`)
>>> PEP440Version("1b1").bump_dev()
ValueError: Cannot bump from beta to dev-release (use `dent_dev`)
>>> PEP440Version("1rc2").bump_dev()
ValueError: Cannot bump from candidate to dev-release (use `dent_dev`)
>>> PEP440Version("1.post0").bump_dev()
ValueError: Cannot bump from post to dev-release (use `dent_dev`)
>>> PEP440Version("1a0.dev1").bump_dev()
<Version('1a0.dev2')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, same release, same pre-release, same post-release and bumped dev-release.

### bump\_epoch

```
bump_epoch() -> PEP440Version
```

Bump epoch.

Examples:

```
>>> PEP440Version("1.0").bump_epoch()
<Version('1!1.0')>
>>> PEP440Version("0!1.0").bump_epoch()
<Version('1!1.0')>
>>> PEP440Version("1!1.0").bump_epoch()
<Version('2!1.0')>
>>> PEP440Version("1.0a2.post3").bump_epoch()
<Version('2!1.0')>
```

Returns:

- `PEP440Version` –

  Version with bumped epoch, same release, and the right parts reset to 0 or nothing.

### bump\_major

```
bump_major(*, trim: bool = False) -> PEP440Version
```

Bump major.

Parameters:

- #### **`trim`**

  (`bool`, default: `False` ) –

  Whether to trim all zeroes on the right after bumping.

Examples:

```
>>> PEP440Version("1").bump_major()
<Version('2')>
>>> PEP440Version("1.1").bump_major()
<Version('2.0')>
>>> PEP440Version("1.1.1").bump_major()
<Version('2.0.0')>
>>> PEP440Version("1.1.1").bump_major(trim=True)
<Version('2')>
>>> PEP440Version("1a2.post3").bump_major()
<Version('2')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, bumped major and the right parts reset to 0 or nothing.

### bump\_micro

```
bump_micro(*, trim: bool = False) -> PEP440Version
```

Bump micro.

Parameters:

- #### **`trim`**

  (`bool`, default: `False` ) –

  Whether to trim all zeroes on the right after bumping.

Examples:

```
>>> PEP440Version("1").bump_micro()
<Version('1.0.1')>
>>> PEP440Version("1.1").bump_micro()
<Version('1.1.1')>
>>> PEP440Version("1.1.1").bump_micro()
<Version('1.1.2')>
>>> PEP440Version("1.1.1").bump_micro()
<Version('1.1.2')>
>>> PEP440Version("1.1.1.1").bump_micro()
<Version('1.1.2.0')>
>>> PEP440Version("1.1.1.1").bump_micro(trim=True)
<Version('1.1.2')>
>>> PEP440Version("1a2.post3").bump_micro()
<Version('1.0.1')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, same major, same minor, bumped micro and the right parts reset to 0 or nothing.

### bump\_minor

```
bump_minor(*, trim: bool = False) -> PEP440Version
```

Bump minor.

Parameters:

- #### **`trim`**

  (`bool`, default: `False` ) –

  Whether to trim all zeroes on the right after bumping.

Examples:

```
>>> PEP440Version("1").bump_minor()
<Version('1.1')>
>>> PEP440Version("1.1").bump_minor()
<Version('1.2')>
>>> PEP440Version("1.1.1").bump_minor()
<Version('1.2.0')>
>>> PEP440Version("1.1.1").bump_minor(trim=True)
<Version('1.2')>
>>> PEP440Version("1a2.post3").bump_minor()
<Version('1.1')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, same major, bumped minor and the right parts reset to 0 or nothing.

### bump\_post

```
bump_post() -> PEP440Version
```

Bump post-release.

Examples:

```
>>> PEP440Version("1").bump_post()
<Version('1.post0')>
>>> PEP440Version("1.post0").bump_post()
<Version('1.post1')>
>>> PEP440Version("1a0.post0").bump_post()
<Version('1a0.post1')>
>>> PEP440Version("1.post0.dev1").bump_post()
<Version('1.post1')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, same release, same pre-release, bumped post-release and the right parts reset to 0 or nothing.

### bump\_pre

```
bump_pre(
    pre: Literal["a", "b", "rc"] | None = None,
) -> PEP440Version
```

Bump pre-release.

Parameters:

- #### **`pre`**

  (`Literal['a', 'b', 'rc'] | None`, default: `None` ) –

  Kind of pre-release to bump.

  - a means alpha
  - b means beta
  - c or rc means (release) candidate

Examples:

```
>>> PEP440Version("1").bump_pre()
ValueError: Cannot bump from release to alpha pre-release (use `dent_pre`)
>>> PEP440Version("1a0").bump_pre()
<Version('1a1')>
>>> PEP440Version("1a0").bump_pre("a")
<Version('1a1')>
>>> PEP440Version("1a0.post0").bump_pre()
<Version('1a1')>
>>> PEP440Version("1b2").bump_pre("a")
ValueError: Cannot bump from beta to alpha pre-release (use `dent_alpha`)
>>> PEP440Version("1c2").bump_pre("a")
ValueError: Cannot bump from candidate to alpha pre-release (use `dent_alpha`)
```

```
>>> PEP440Version("1").bump_pre("b")
ValueError: Cannot bump from release to beta pre-release (use `dent_beta`)
>>> PEP440Version("1a2").bump_pre("b")
<Version('1b0')>
>>> PEP440Version("1b2").bump_pre("b")
<Version('1b3')>
>>> PEP440Version("1c2").bump_pre("b")
ValueError: Cannot bump from candidate to beta pre-release (use `dent_beta`)
```

```
>>> PEP440Version("1").bump_pre("c")
ValueError: Cannot bump from release to candidate pre-release (use `dent_candidate`)
>>> PEP440Version("1a2").bump_pre("c")
<Version('1rc0')>
>>> PEP440Version("1b2").bump_pre("rc")
<Version('1rc0')>
>>> PEP440Version("1rc2").bump_pre("c")
<Version('1rc3')>
```

Returns:

- `PEP440Version` –

  Version with same epoch, same release, bumped pre-release and the right parts reset to 0 or nothing.

### bump\_release

```
bump_release(
    level: int | None = None, *, trim: bool = False
) -> PEP440Version
```

Bump given release level.

Parameters:

- #### **`level`**

  (`int | None`, default: `None` ) –

  The release level to bump.

  - 0 means major
  - 1 means minor
  - 2 means micro (patch)
  - 3+ don't have names
  - None means move from pre-release to release (unchanged)
- #### **`trim`**

  (`bool`, default: `False` ) –

  Whether to trim all zeroes on the right after bumping.

Examples:

```
>>> PEP440Version("1").bump_release(0)
<Version('2')>
>>> PEP440Version("1.1").bump_release(0)
<Version('2.0')>
>>> PEP440Version("1.1.1").bump_release(0)
<Version('2.0.0')>
>>> PEP440Version("1.1.1").bump_release(0, trim=True)
<Version('2')>
>>> PEP440Version("1a2.post3").bump_release(0)
<Version('2')>
```

```
>>> PEP440Version("1").bump_release(1)
<Version('1.1')>
>>> PEP440Version("1.1").bump_release(1)
<Version('1.2')>
>>> PEP440Version("1.1.1").bump_release(1)
<Version('1.2.0')>
>>> PEP440Version("1.1.1").bump_release(1, trim=True)
<Version('1.2')>
>>> PEP440Version("1a2.post3").bump_release(1)
<Version('1.1')>
```

```
>>> PEP440Version("1a0").bump_release()
<Version('1')>
>>> PEP440Version("1b1").bump_release()
<Version('1')>
>>> PEP440Version("1rc2").bump_release()
<Version('1')>
>>> PEP440Version("1a2.dev0").bump_release()
<Version('1')>
>>> PEP440Version("1post0").bump_release()
ValueError: Cannot bump from post-release to release
```

Returns:

- `PEP440Version` –

  Version with same epoch, bumped release level, and the right parts reset to 0 or nothing.

### dent\_alpha

```
dent_alpha() -> PEP440Version
```

Dent to alpha-release.

Examples:

```
>>> PEP440Version("1").dent_alpha()
<Version('1a0')>
>>> PEP440Version("1a0").dent_alpha()
ValueError: Cannot dent alpha pre-releases
>>> PEP440Version("1b0").dent_alpha()
ValueError: Cannot dent beta pre-releases
>>> PEP440Version("1rc0").dent_alpha()
ValueError: Cannot dent candidate pre-releases
```

Returns:

- `PEP440Version` –

  Version with same epoch and release dented to alpha pre-release.

### dent\_beta

```
dent_beta() -> PEP440Version
```

Dent to beta-release.

Examples:

```
>>> PEP440Version("1").dent_beta()
<Version('1b0')>
>>> PEP440Version("1a0").dent_beta()
ValueError: Cannot dent alpha pre-releases
>>> PEP440Version("1b0").dent_beta()
ValueError: Cannot dent beta pre-releases
>>> PEP440Version("1rc0").dent_beta()
ValueError: Cannot dent candidate pre-releases
```

Returns:

- `PEP440Version` –

  Version with same epoch and release dented to beta pre-release.

### dent\_candidate

```
dent_candidate() -> PEP440Version
```

Dent to candidate release.

Examples:

```
>>> PEP440Version("1").dent_candidate()
<Version('1rc0')>
>>> PEP440Version("1a0").dent_candidate()
ValueError: Cannot dent alpha pre-releases
>>> PEP440Version("1b0").dent_candidate()
ValueError: Cannot dent beta pre-releases
>>> PEP440Version("1rc0").dent_candidate()
ValueError: Cannot dent candidate pre-releases
```

Returns:

- `PEP440Version` –

  Version with same epoch and release dented to candidate pre-release.

### dent\_dev

```
dent_dev() -> PEP440Version
```

Dent to dev-release.

Examples:

```
>>> PEP440Version("1").dent_dev()
<Version('1.dev0')>
>>> PEP440Version("1a0").dent_dev()
<Version('1a0.dev0')>
>>> PEP440Version("1b1").dent_dev()
<Version('1b1.dev0')>
>>> PEP440Version("1c2").dent_dev()
<Version('1rc2.dev0')>
>>> PEP440Version("1.post0").dent_dev()
<Version('1.post0.dev0')>
>>> PEP440Version("1a0.dev1").dent_dev()
ValueError: Cannot dent dev-releases
```

Returns:

- `PEP440Version` –

  Version with same epoch and release dented to dev-release.

### dent\_pre

```
dent_pre(
    pre: Literal["a", "b", "rc"] | None = None,
) -> PEP440Version
```

Dent to pre-release.

This method dents a release down to an alpha, beta or candidate pre-release.

Parameters:

- #### **`pre`**

  (`Literal['a', 'b', 'rc'] | None`, default: `None` ) –

  Kind of pre-release to bump.

  - a means alpha
  - b means beta
  - c or rc means (release) candidate

Examples:

```
>>> PEP440Version("1").dent_pre()
<Version('1a0')>
>>> PEP440Version("1").dent_pre("a")
<Version('1a0')>
>>> PEP440Version("1a0").dent_pre("a")
ValueError: Cannot dent alpha pre-releases
>>> PEP440Version("1").dent_pre("b")
<Version('1b0')>
>>> PEP440Version("1b0").dent_pre("b")
ValueError: Cannot dent beta pre-releases
>>> PEP440Version("1").dent_pre("c")
<Version('1rc0')>
>>> PEP440Version("1").dent_pre("rc")
<Version('1rc0')>
>>> PEP440Version("1rc0").dent_pre("c")
ValueError: Cannot dent candidate pre-releases
```

Returns:

- `PEP440Version` –

  Version with same epoch and release dented to pre-release.

### from\_parts

```
from_parts(
    epoch: int | None = None,
    release: tuple[int, ...] | None = None,
    pre: tuple[Literal["a", "b", "rc"], int] | None = None,
    post: int | None = None,
    dev: int | None = None,
) -> PEP440Version
```

Build a version from its parts.

Parameters:

- #### **`epoch`**

  (`int | None`, default: `None` ) –

  Version's epoch number.
- #### **`release`**

  (`tuple[int, ...] | None`, default: `None` ) –

  Version's release numbers.
- #### **`pre`**

  (`tuple[Literal['a', 'b', 'rc'], int] | None`, default: `None` ) –

  Version's prerelease kind and number.
- #### **`post`**

  (`int | None`, default: `None` ) –

  Version's post number.
- #### **`dev`**

  (`int | None`, default: `None` ) –

  Version's dev number.

Returns:

- `PEP440Version` –

  A PEP 440 version.

## ParsedVersion

Bases: `Protocol`

Base class for versioning schemes.

Methods:

- **`__eq__`** –

  Implement `==` comparison.
- **`__ge__`** –

  Implement `>=` comparison.
- **`__gt__`** –

  Implement `>` comparison.
- **`__le__`** –

  Implement `<=` comparison.
- **`__lt__`** –

  Implement `<` comparison.
- **`__ne__`** –

  Implement `!=` comparison.

### \_\_eq\_\_

```
__eq__(other: object) -> bool
```

Implement `==` comparison.

### \_\_ge\_\_

```
__ge__(other: object) -> bool
```

Implement `>=` comparison.

### \_\_gt\_\_

```
__gt__(other: object) -> bool
```

Implement `>` comparison.

### \_\_le\_\_

```
__le__(other: object) -> bool
```

Implement `<=` comparison.

### \_\_lt\_\_

```
__lt__(other: object) -> bool
```

Implement `<` comparison.

### \_\_ne\_\_

```
__ne__(other: object) -> bool
```

Implement `!=` comparison.

## ProviderRefParser

```
ProviderRefParser(
    namespace: str, project: str, url: str | None = None
)
```

Bases: `ABC`

A base class for specific providers reference parsers.

Parameters:

- ### **`namespace`**

  (`str`) –

  The Bitbucket namespace.
- ### **`project`**

  (`str`) –

  The Bitbucket project.
- ### **`url`**

  (`str | None`, default: `None` ) –

  The Bitbucket URL.

Methods:

- **`build_ref_url`** –

  Build the URL for a reference type and a dictionary of matched groups.
- **`get_compare_url`** –

  Get the URL for a tag comparison.
- **`get_refs`** –

  Find all references in the given text.
- **`get_tag_url`** –

  Get the URL for a git tag.
- **`parse_refs`** –

  Parse references in the given text.

Attributes:

- **`REF`** (`dict[str, RefDef]`) –

  The reference definitions for the provider.
- **`namespace`** (`str`) –

  The namespace for the provider.
- **`project`** (`str`) –

  The project for the provider.
- **`url`** (`str`) –

  The URL for the provider.

### REF

```
REF: dict[str, RefDef] = {}
```

The reference definitions for the provider.

### namespace

```
namespace: str = namespace
```

The namespace for the provider.

### project

```
project: str = project
```

The project for the provider.

### url

```
url: str = url or self.url
```

The URL for the provider.

### build\_ref\_url

```
build_ref_url(
    ref_type: str, match_dict: dict[str, str]
) -> str
```

Build the URL for a reference type and a dictionary of matched groups.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`match_dict`**

  (`dict[str, str]`) –

  The matched groups.

Returns:

- `str` –

  The built URL.

### get\_compare\_url

```
get_compare_url(base: str, target: str) -> str
```

Get the URL for a tag comparison.

Parameters:

- #### **`base`**

  (`str`) –

  The base tag.
- #### **`target`**

  (`str`) –

  The target tag.

Returns:

- `str` –

  The comparison URL.

### get\_refs

```
get_refs(ref_type: str, text: str) -> list[Ref]
```

Find all references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text in which to search references.

Returns:

- `list[Ref]` –

  A list of references (instances of [Ref](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.Ref> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-class\"></code>            <span class=\"doc doc-object-name doc-class-name\">Ref</span>")).

### get\_tag\_url

```
get_tag_url(tag: str) -> str
```

Get the URL for a git tag.

Parameters:

- #### **`tag`**

  (`str`) –

  The git tag.

Returns:

- `str` –

  The tag URL.

### parse\_refs

```
parse_refs(ref_type: str, text: str) -> list[Match]
```

Parse references in the given text.

Parameters:

- #### **`ref_type`**

  (`str`) –

  The reference type.
- #### **`text`**

  (`str`) –

  The text to parse.

Returns:

- `list[Match]` –

  A list of regular expressions matches.

## Ref

```
Ref(ref: str, url: str)
```

A class to represent a reference and its URL.

Parameters:

- ### **`ref`**

  (`str`) –

  The reference text.
- ### **`url`**

  (`str`) –

  The reference URL.

Attributes:

- **`ref`** (`str`) –

  The reference text.
- **`url`** (`str`) –

  The reference URL.

### ref

```
ref: str = ref
```

The reference text.

### url

```
url: str = url
```

The reference URL.

## RefDef

```
RefDef(regex: Pattern, url_string: str)
```

A class to store a reference regular expression and URL building string.

Parameters:

- ### **`regex`**

  (`Pattern`) –

  The regular expression to match the reference.
- ### **`url_string`**

  (`str`) –

  The URL string to format using matched groups.

Attributes:

- **`regex`** –

  The regular expression to match the reference.
- **`url_string`** –

  The URL string to format using matched groups.

### regex

```
regex = regex
```

The regular expression to match the reference.

### url\_string

```
url_string = url_string
```

The URL string to format using matched groups.

## RefRe

An enum helper to store parts of regular expressions for references.

Attributes:

- **`BA`** –

  Blank after the reference.
- **`BB`** –

  Blank before the reference.
- **`COMMIT`** –

  Commit hash.
- **`COMMIT_RANGE`** –

  Commit range.
- **`ID`** –

  Issue or pull request ID.
- **`MENTION`** –

  Mention.
- **`MULTI_WORD`** –

  Multi word reference.
- **`NP`** –

  Namespace and project.
- **`ONE_WORD`** –

  One word reference.

### BA

```
BA = '(?:[\\s,]|$)'
```

Blank after the reference.

### BB

```
BB = '(?:^|[\\s,])'
```

Blank before the reference.

### COMMIT

```
COMMIT = '(?P<ref>[0-9a-f]{{{min},{max}}})'
```

Commit hash.

### COMMIT\_RANGE

```
COMMIT_RANGE = "(?P<ref>[0-9a-f]{{{min},{max}}}\\.\\.\\.[0-9a-f]{{{min},{max}}})"
```

Commit range.

### ID

```
ID = '{symbol}(?P<ref>[1-9]\\d*)'
```

Issue or pull request ID.

### MENTION

```
MENTION = '@(?P<ref>\\w[-\\w]*)'
```

Mention.

### MULTI\_WORD

```
MULTI_WORD = '{symbol}(?P<ref>"\\w[- \\w]*")'
```

Multi word reference.

### NP

```
NP = '(?:(?P<namespace>[-\\w]+)/)?(?P<project>[-\\w]+)'
```

Namespace and project.

### ONE\_WORD

```
ONE_WORD = '{symbol}(?P<ref>\\w*[-a-z_ ][-\\w]*)'
```

One word reference.

## Section

```
Section(
    section_type: str = "",
    commits: list[Commit] | None = None,
)
```

A list of commits grouped by section\_type.

Parameters:

- ### **`section_type`**

  (`str`, default: `''` ) –

  The section section\_type.
- ### **`commits`**

  (`list[Commit] | None`, default: `None` ) –

  The list of commits.

Attributes:

- **`commits`** (`list[Commit]`) –

  The list of commits.
- **`type`** (`str`) –

  The section type.

### commits

```
commits: list[Commit] = commits or []
```

The list of commits.

### type

```
type: str = section_type
```

The section type.

## SemVerBumper

```
SemVerBumper(strategies: tuple[str, ...])
```

Bases: `VersionBumper`

SemVer version bumper.

Parameters:

- ### **`strategies`**

  (`tuple[str, ...]`) –

  The supported bumping strategies.

Methods:

- **`__call__`** –

  Bump a SemVer version.

Attributes:

- **`initial`** (`str`) –

  The initial version.
- **`strategies`** –

  The supported bumping strategies.

### initial

```
initial: str = '0.0.0'
```

The initial version.

### strategies

```
strategies = strategies
```

The supported bumping strategies.

### \_\_call\_\_

```
__call__(
    version: str,
    strategy: SemVerStrategy = "patch",
    *,
    zerover: bool = True,
) -> str
```

Bump a SemVer version.

Parameters:

- #### **`version`**

  (`str`) –

  The version to bump.
- #### **`strategy`**

  (`SemVerStrategy`, default: `'patch'` ) –

  The bumping strategy to use.
- #### **`zerover`**

  (`bool`, default: `True` ) –

  Keep major version at zero, even for breaking changes.

Returns:

- `str` –

  The bumped version.

## SemVerVersion

Bases: `Version`, `ParsedVersion`

SemVer version.

Methods:

- **`__eq__`** –

  Implement `==` comparison.
- **`__ge__`** –

  Implement `>=` comparison.
- **`__gt__`** –

  Implement `>` comparison.
- **`__le__`** –

  Implement `<=` comparison.
- **`__lt__`** –

  Implement `<` comparison.
- **`__ne__`** –

  Implement `!=` comparison.
- **`bump_major`** –

  Bump the major version.
- **`bump_minor`** –

  Bump the minor version.
- **`bump_patch`** –

  Bump the patch version.
- **`bump_release`** –

  Bump from a pre-release to the same, regular release.

### \_\_eq\_\_

```
__eq__(other: object) -> bool
```

Implement `==` comparison.

### \_\_ge\_\_

```
__ge__(other: object) -> bool
```

Implement `>=` comparison.

### \_\_gt\_\_

```
__gt__(other: object) -> bool
```

Implement `>` comparison.

### \_\_le\_\_

```
__le__(other: object) -> bool
```

Implement `<=` comparison.

### \_\_lt\_\_

```
__lt__(other: object) -> bool
```

Implement `<` comparison.

### \_\_ne\_\_

```
__ne__(other: object) -> bool
```

Implement `!=` comparison.

### bump\_major

```
bump_major() -> SemVerVersion
```

Bump the major version.

### bump\_minor

```
bump_minor() -> SemVerVersion
```

Bump the minor version.

### bump\_patch

```
bump_patch() -> SemVerVersion
```

Bump the patch version.

### bump\_release

```
bump_release() -> SemVerVersion
```

Bump from a pre-release to the same, regular release.

Returns:

- `SemVerVersion` –

  The same version, without pre-release or build metadata.

## Templates

Bases: `tuple`

Helper to pick a template on the command line.

Methods:

- **`__contains__`** –

  Check if the template is in the list.

### \_\_contains\_\_

```
__contains__(item: object) -> bool
```

Check if the template is in the list.

## Version

```
Version(
    tag: str = "",
    date: date | datetime | None = None,
    sections: list[Section] | None = None,
    commits: list[Commit] | None = None,
    url: str = "",
    compare_url: str = "",
    *,
    version_parser: Callable[
        [str], tuple[SemVerVersion | PEP440Version, str]
    ]
    | None = None,
)
```

A class to represent a changelog version.

Parameters:

- ### **`tag`**

  (`str`, default: `''` ) –

  The version tag.
- ### **`date`**

  (`date | datetime | None`, default: `None` ) –

  The version date.
- ### **`sections`**

  (`list[Section] | None`, default: `None` ) –

  The version sections.
- ### **`commits`**

  (`list[Commit] | None`, default: `None` ) –

  The version commits.
- ### **`url`**

  (`str`, default: `''` ) –

  The version URL.
- ### **`compare_url`**

  (`str`, default: `''` ) –

  The version 'compare' URL.
- ### **`version_parser`**

  (`Callable[[str], tuple[SemVerVersion | PEP440Version, str]] | None`, default: `None` ) –

  The version parser. By default, try SemVer, then PEP 440.

Methods:

- **`add_commit`** –

  Register the given commit and add it to the relevant section based on its message convention.

Attributes:

- **`breaking_changes`** (`list[str]`) –

  Return breaking change descriptions from all commits in this version.
- **`commits`** (`list[Commit]`) –

  The version commits.
- **`compare_url`** (`str`) –

  The version 'compare' URL.
- **`date`** (`date | None`) –

  The version date.
- **`is_major`** (`bool`) –

  Tell if the release has zero minor and patch components.
- **`is_minor`** (`bool`) –

  Tell if the release has a nonzero minor and zero patch components.
- **`next_version`** (`Version | None`) –

  The next version.
- **`planned_tag`** (`str | None`) –

  The planned version tag.
- **`previous_version`** (`Version | None`) –

  The previous version.
- **`sections_dict`** (`dict[str, Section]`) –

  The version sections (dict).
- **`sections_list`** (`list[Section]`) –

  The version sections (list).
- **`tag`** –

  The version tag.
- **`timestamp`** (`datetime | None`) –

  The version timestamp.
- **`typed_sections`** (`list[Section]`) –

  The typed sections.
- **`untyped_section`** (`Section | None`) –

  Untyped section if any.
- **`url`** (`str`) –

  The version URL.

### breaking\_changes

```
breaking_changes: list[str]
```

Return breaking change descriptions from all commits in this version.

### commits

```
commits: list[Commit] = commits or []
```

The version commits.

### compare\_url

```
compare_url: str = compare_url
```

The version 'compare' URL.

### date

```
date: date | None
```

The version date.

### is\_major

```
is_major: bool
```

Tell if the release has zero minor and patch components.

Use the planned tag for an unreleased version with a planned release. Ignore prerelease and build metadata when classifying the release. Return false for empty or invalid tags.

Returns:

- `bool` –

  Whether this version is major.

### is\_minor

```
is_minor: bool
```

Tell if the release has a nonzero minor and zero patch components.

Use the planned tag for an unreleased version with a planned release. Ignore prerelease and build metadata when classifying the release. Return false for empty or invalid tags.

Returns:

- `bool` –

  Whether this version is minor.

### next\_version

```
next_version: Version | None = None
```

The next version.

### planned\_tag

```
planned_tag: str | None = None
```

The planned version tag.

### previous\_version

```
previous_version: Version | None = None
```

The previous version.

### sections\_dict

```
sections_dict: dict[str, Section] = {
    section.type: section for section in self.sections_list
}
```

The version sections (dict).

### sections\_list

```
sections_list: list[Section] = sections or []
```

The version sections (list).

### tag

```
tag = tag
```

The version tag.

### timestamp

```
timestamp: datetime | None
```

The version timestamp.

### typed\_sections

```
typed_sections: list[Section]
```

The typed sections.

### untyped\_section

```
untyped_section: Section | None
```

Untyped section if any.

### url

```
url: str = url
```

The version URL.

### add\_commit

```
add_commit(commit: Commit) -> None
```

Register the given commit and add it to the relevant section based on its message convention.

Parameters:

- #### **`commit`**

  (`Commit`) –

  The git commit.

## VersionBumper

```
VersionBumper(strategies: tuple[str, ...])
```

Base class for version bumpers.

Parameters:

- ### **`strategies`**

  (`tuple[str, ...]`) –

  The supported bumping strategies.

Methods:

- **`__call__`** –

  Bump a version.

Attributes:

- **`initial`** (`str`) –

  The initial version.
- **`strategies`** –

  The supported bumping strategies.

### initial

```
initial: str
```

The initial version.

### strategies

```
strategies = strategies
```

The supported bumping strategies.

### \_\_call\_\_

```
__call__(version: str, strategy: str, **kwargs: Any) -> str
```

Bump a version.

Parameters:

- #### **`version`**

  (`str`) –

  The version to bump.
- #### **`strategy`**

  (`str`) –

  The bumping strategy.
- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Additional bumper-specific arguments.

Returns:

- `str` –

  The bumped version.

## build\_and\_render

```
build_and_render(
    repository: str,
    template: str,
    convention: str | CommitConvention,
    parse_refs: bool = False,
    parse_trailers: bool = False,
    sections: list[str] | None = None,
    in_place: bool = False,
    output: str | TextIO | None = None,
    version_regex: str | None = None,
    marker_line: str | None = None,
    bump_latest: bool = False,
    omit_empty_versions: bool = False,
    provider: str | None = None,
    bump: str | None = None,
    zerover: bool = True,
    filter_commits: str | None = None,
    jinja_context: dict[str, Any] | None = None,
    versioning: Literal["pep440", "semver"] = "semver",
    include_all: bool = False,
    remote: str | None = None,
    remote_url: str | None = None,
    **kwargs: Any,
) -> tuple[Changelog, str]
```

Build a changelog and render it.

This function returns the changelog instance and the rendered contents, but also updates the specified output file (side-effect) or writes to stdout.

Parameters:

- ### **`repository`**

  (`str`) –

  Path to a local repository.
- ### **`template`**

  (`str`) –

  Name of a builtin template, or path to a custom template (prefixed with `path:`).
- ### **`convention`**

  (`str | CommitConvention`) –

  Name of a commit message style/convention.
- ### **`parse_refs`**

  (`bool`, default: `False` ) –

  Whether to parse provider-specific references (GitHub/GitLab issues, PRs, etc.).
- ### **`parse_trailers`**

  (`bool`, default: `False` ) –

  Whether to parse Git trailers.
- ### **`sections`**

  (`list[str] | None`, default: `None` ) –

  Sections to render (features, bug fixes, etc.).
- ### **`in_place`**

  (`bool`, default: `False` ) –

  Whether to update the changelog in-place.
- ### **`output`**

  (`str | TextIO | None`, default: `None` ) –

  Output/changelog file.
- ### **`version_regex`**

  (`str | None`, default: `None` ) –

  Regular expression to match versions in an existing changelog file.
- ### **`marker_line`**

  (`str | None`, default: `None` ) –

  Marker line used to insert contents in an existing changelog.
- ### **`bump_latest`**

  (`bool`, default: `False` ) –

  Deprecated, use --bump=auto instead. Whether to try and bump the latest version to guess the new one.
- ### **`omit_empty_versions`**

  (`bool`, default: `False` ) –

  Whether to omit empty versions from the output.
- ### **`provider`**

  (`str | None`, default: `None` ) –

  Provider class used by this repository.
- ### **`bump`**

  (`str | None`, default: `None` ) –

  Whether to try and bump to a given version.
- ### **`zerover`**

  (`bool`, default: `True` ) –

  Keep major version at zero, even for breaking changes.
- ### **`filter_commits`**

  (`str | None`, default: `None` ) –

  The Git revision-range used to filter commits in git-log.
- ### **`include_all`**

  (`bool`, default: `False` ) –

  Whether to include commits without a recognized type.
- ### **`jinja_context`**

  (`dict[str, Any] | None`, default: `None` ) –

  Key/value pairs passed to the Jinja template.
- ### **`versioning`**

  (`Literal['pep440', 'semver']`, default: `'semver'` ) –

  Versioning scheme to use when grouping commits and bumping versions.
- ### **`remote`**

  (`str | None`, default: `None` ) –

  Git remote name used for changelog links.
- ### **`remote_url`**

  (`str | None`, default: `None` ) –

  Repository URL used for changelog links, overriding the remote name.
- ### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Swallowing kwargs to allow passing all settings at once.

Raises:

- `ValueError` –

  When some arguments are incompatible or missing.

Returns:

- `tuple[Changelog, str]` –

  The built changelog and the rendered contents.

## bump

```
bump(
    version: str,
    part: Literal["major", "minor", "patch"] = "patch",
    *,
    zerover: bool = True,
) -> str
```

Bump a version. Deprecated, use [`bump_semver`](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.bump_semver> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-attribute\"></code>            <span class=\"doc doc-object-name doc-attribute-name\">bump_semver</span>     <span class=\"doc doc-labels\">       <small class=\"doc doc-label doc-label-module-attribute\"><code>module-attribute</code></small>   </span>") instead.

Parameters:

- ### **`version`**

  (`str`) –

  The version to bump.
- ### **`part`**

  (`Literal['major', 'minor', 'patch']`, default: `'patch'` ) –

  The part of the version to bump (major, minor, or patch).
- ### **`zerover`**

  (`bool`, default: `True` ) –

  Keep major version at zero, even for breaking changes.

Returns:

- `str` –

  The bumped version.

## configure\_env

```
configure_env(env: Environment) -> None
```

Configure the Jinja environment.

Parameters:

- ### **`env`**

  (`Environment`) –

  The environment to configure.

## get\_custom\_template

```
get_custom_template(path: str | Path) -> Template
```

Get a custom template instance.

Parameters:

- ### **`path`**

  (`str | Path`) –

  Path to the custom template.

Returns:

- `Template` –

  The Jinja template.

## get\_parser

```
get_parser() -> ArgumentParser
```

Return the CLI argument parser.

Returns:

- `ArgumentParser` –

  An argparse parser.

## get\_release\_notes

```
get_release_notes(
    input_file: str | Path = "CHANGELOG.md",
    version_regex: str = DEFAULT_VERSION_REGEX,
    marker_line: str = DEFAULT_MARKER_LINE,
) -> str
```

Get release notes from existing changelog.

This will return the latest entry in the changelog.

Parameters:

- ### **`input_file`**

  (`str | Path`, default: `'CHANGELOG.md'` ) –

  The changelog to read from.
- ### **`version_regex`**

  (`str`, default: `DEFAULT_VERSION_REGEX` ) –

  A regular expression to match version entries.
- ### **`marker_line`**

  (`str`, default: `DEFAULT_MARKER_LINE` ) –

  The insertion marker line in the changelog.

Returns:

- `str` –

  The latest changelog entry.

## get\_template

```
get_template(name: str) -> Template
```

Get a builtin template instance.

Parameters:

- ### **`name`**

  (`str`) –

  The template name.

Returns:

- `Template` –

  The Jinja template.

## get\_version

```
get_version() -> str
```

Return the current `git-changelog` version.

Returns:

- `str` –

  The current `git-changelog` version.

## main

```
main(args: list[str] | None = None) -> int
```

Run the main program.

This function is executed when you type `git-changelog` or `python -m git_changelog`.

Parameters:

- ### **`args`**

  (`list[str] | None`, default: `None` ) –

  Arguments passed from the command line.

Returns:

- `int` –

  An exit code.

## output\_release\_notes

```
output_release_notes(
    input_file: str = "CHANGELOG.md",
    version_regex: str | None = None,
    marker_line: str | None = None,
    output_file: str | TextIO | None = None,
) -> None
```

Print release notes from existing changelog.

This will print the latest entry in the changelog.

Parameters:

- ### **`input_file`**

  (`str`, default: `'CHANGELOG.md'` ) –

  The changelog to read from.
- ### **`version_regex`**

  (`str | None`, default: `None` ) –

  A regular expression to match version entries.
- ### **`marker_line`**

  (`str | None`, default: `None` ) –

  The insertion marker line in the changelog.
- ### **`output_file`**

  (`str | TextIO | None`, default: `None` ) –

  Where to print/write the release notes.

## parse\_pep440

```
parse_pep440(version: str) -> tuple[PEP440Version, str]
```

Parse a PEP version.

Returns:

- `tuple[PEP440Version, str]` –

  A PEP 440 version instance with useful methods.

## parse\_semver

```
parse_semver(version: str) -> tuple[SemVerVersion, str]
```

Parse a SemVer version.

Returns:

- `tuple[SemVerVersion, str]` –

  A semver version instance with useful methods.

## parse\_settings

```
parse_settings(args: list[str] | None = None) -> dict
```

Parse arguments and config files to build the final settings set.

Parameters:

- ### **`args`**

  (`list[str] | None`, default: `None` ) –

  Arguments passed from the command line.

Returns:

- `dict` –

  A dictionary with the final settings.

## parse\_version

```
parse_version(version: str) -> tuple[SemVerVersion, str]
```

Parse a version. Deprecated, use [`bump_semver`](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.parse_semver> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-function\"></code>            <span class=\"doc doc-object-name doc-function-name\">parse_semver</span>") instead.

Parameters:

- ### **`version`**

  (`str`) –

  The version to parse.

Returns:

- **`semver_version`** ( `SemVerVersion` ) –

  The semantic version.
- **`prefix`** ( `str` ) –

  The version prefix.

## read\_config

```
read_config(
    config_file: Sequence[str | Path]
    | str
    | Path
    | None = DEFAULT_CONFIG_FILES,
) -> dict
```

Find config files and initialize settings with the one of highest priority.

Parameters:

- ### **`config_file`**

  (`Sequence[str | Path] | str | Path | None`, default: `DEFAULT_CONFIG_FILES` ) –

  A path or list of paths to configuration file(s); or `None` to disable config file settings. Default: a list of paths given by [`git_changelog.DEFAULT_CONFIG_FILES`](<https://pawamoy.github.io/git-changelog/2.12.0/reference/api/index.md#git_changelog.DEFAULT_CONFIG_FILES> "<code class=\"doc-symbol doc-symbol-heading doc-symbol-attribute\"></code>            <span class=\"doc doc-object-name doc-attribute-name\">DEFAULT_CONFIG_FILES</span>     <span class=\"doc doc-labels\">       <small class=\"doc doc-label doc-label-module-attribute\"><code>module-attribute</code></small>   </span>").

Returns:

- `dict` –

  A settings dictionary. Default settings if no config file is found or `config_file` is `None`.

## render

```
render(
    changelog: Changelog,
    template: str,
    in_place: bool = False,
    output: str | TextIO | None = None,
    version_regex: str | None = None,
    marker_line: str | None = None,
    bump_latest: bool = False,
    bump: str | None = None,
    jinja_context: dict[str, Any] | None = None,
) -> str
```

Render a changelog.

This function updates the specified output file (side-effect) or writes to stdout.

Parameters:

- ### **`changelog`**

  (`Changelog`) –

  The changelog to render.
- ### **`template`**

  (`str`) –

  Name of a builtin template, or path to a custom template (prefixed with `path:`).
- ### **`in_place`**

  (`bool`, default: `False` ) –

  Whether to update the changelog in-place.
- ### **`output`**

  (`str | TextIO | None`, default: `None` ) –

  Output/changelog file.
- ### **`version_regex`**

  (`str | None`, default: `None` ) –

  Regular expression to match versions in an existing changelog file.
- ### **`marker_line`**

  (`str | None`, default: `None` ) –

  Marker line used to insert contents in an existing changelog.
- ### **`bump_latest`**

  (`bool`, default: `False` ) –

  Deprecated, use --bump=auto instead. Whether to try and bump the latest version to guess the new one.
- ### **`bump`**

  (`str | None`, default: `None` ) –

  Whether to try and bump to a given version.
- ### **`jinja_context`**

  (`dict[str, Any] | None`, default: `None` ) –

  Key/value pairs passed to the Jinja template.

Raises:

- `ValueError` –

  When some arguments are incompatible or missing.

Returns:

- `str` –

  The rendered changelog.

## version\_prefix

```
version_prefix(version: str) -> tuple[str, str]
```

Return a version and its optional `v` prefix.

Parameters:

- ### **`version`**

  (`str`) –

  The full version.

Returns:

- **`version`** ( `str` ) –

  The version without its prefix.
- **`prefix`** ( `str` ) –

  The version prefix.
