---
hide:
- navigation
---

# Usage

*git-changelog* parses your commit messages to extract useful data
that is then rendered using Jinja2 templates, for example to
a changelog file formatted in Markdown.

Each Git tag will be treated as a version of your project.
Each version contains a set of commits, and will be an entry
in your changelog. Commits in each version will be grouped
by sections, depending on the commit coonvention you follow.

## Quick usage

Print the changelog on standard output,
using the basic convention for commit messages
and the Angular template:

```bash
git-changelog -c basic -t angular
```

Update a changelog in-place, overwriting and updating the "Unreleased" section,
using the Angular commit message convention and the Keep A Changelog template (default):

```bash
git-changelog -io CHANGELOG.md -c angular
```

Same thing, but now you're ready to tag so you tell *git-changelog*
to guess the new version by bumping the latest version
based on the semantics of your commits:

```bash
git-changelog -B auto -io CHANGELOG.md -c angular
```

Same thing, but also parse Git trailers
and choose the sections to render, and their order
(author's favorite!):

```bash
git-changelog -B auto -Tio CHANGELOG.md -c angular -s build,deps,fix,feat,refactor
```

Generate a changelog using a custom template,
and parsing provider-specific references (GitHub/GitLab/Bitbucket):

```bash
git-changelog -rt path:./templates/changelog.md.jinja
```

Generate a changelog using a specific provider (GitHub/GitLab/BitBucket):

```bash
git-changelog --provider github
```

Author's favorite, from Python:

```python
from git_changelog.cli import build_and_render

build_and_render(
    repository=".",
    output="CHANGELOG.md",
    convention="angular",
    provider="github",
    template="keepachangelog",
    parse_trailers=True,
    parse_refs=False,
    sections=("build", "deps", "feat", "fix", "refactor"),
    versioning="pep440",
    bump="auto",
    in_place=True,
)
```

The following sections explain in more details all the features of *git-changelog*.

## Configuration files

[(--config-file)](cli.md#config_file)

Project-wise, permanent configuration of *git-changelog* is possible.
By default, *git-changelog* will search for the existence a suitable configuration
in the `pyproject.toml` file or otherwise, the following configuration files 
in this particular order:

- `.git-changelog.toml`
- `config/git-changelog.toml`
- `.config/git-changelog.toml`
- `<current-user-config-path>/git-changelog.toml`

In the last case (`<current-user-config-path>/git-changelog.toml`), the `<current-user-config-path>`
is platform-dependent and will be automatically inferred from your settings.
In Unix systems, this will typically point at `$HOME/.config/git-changelog.toml`.
The use of a configuration file can be disabled or overridden with the `--config-file`
option.
To disable the configuration file, pass `no`, `none`, `false`, `off`, `0` or empty string (`''`):

```bash
git-changelog --config-file no
```

To override the configuration file, pass the path to the new file:

```bash
git-changelog --config-file $HOME/.custom-git-changelog-config
```

The configuration file must be written in TOML language, and may take values
for most of the command line options:

```toml
bump = "auto"
convention = "basic"
in-place = false
filter-commits = "0.5.0.."
marker-line = "<!-- insertion marker -->"
output = "output.log"
parse-refs = false
parse-trailers = false
provider = "gitlab"
repository = "."
sections = ["fix", "maint"]
template = "angular"
version-regex = "^## \\\\[(?P<version>v?[^\\\\]]+)"
versioning = "semver"
zerover = true
```

In the case of configuring *git-changelog* within `pyproject.toml`, these
settings must be found in the appropriate section:

```toml
[tool.git-changelog]
bump = "minor"
convention = "conventional"
in-place = false
filter-commits = "0.5.0.."
marker-line = "<!-- insertion marker -->"
output = "output.log"
parse-refs = false
parse-trailers = false
provider = "gitlab"
repository = "."
sections = "fix,maint"
template = "keepachangelog"
version-regex = "^## \\\\[(?P<version>v?[^\\\\]]+)"
versioning = "semver"
zerover = true
```

## Output a changelog

[(--output)](cli.md#output)

To output a changelog for the current repository (current directory),
simply run:

```bash
git-changelog
```

To output a changelog for another repository (directory),
pass the path to that repository:

```bash
git-changelog /path/to/my/repo
```

By default, *git-changelog* will parse commit messages
as if they use the "basic" convention, and render a
[Keep A Changelog][keepachangelog]-formatted changelog
writing to the standard output.

To write to a file instead, use the `-o` or `--output` CLI option:

```bash
git-changelog --output CHANGELOG.md
```

## Choose the commit message convention

[(--convention)](cli.md#convention)

Different conventions, or styles, are supported by *git-changelog*.
To select a different convention than the default one (basic, see below),
use the `-c` or `--convention` CLI option:

```bash
git-changelog --convention angular
```

### Basic convention

The basic convention, as the name implies, is very simple.
If a commit message summary (the first line of the message)
with a particular word/prefix (case-insensitive),
it is added to the corresponding section:

Type     | Section
---------|-----------
`add`    | Added
`fix`    | Fixed
`change` | Changed
`remove` | Removed
`merge`  | Merged
`doc`    | Documented

### Angular/Karma convention

The Angular/Karma convention initiated the [Conventional Commit specification][conventional-commit].
It expects the following format for commit messages:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

The types and corresponding sections *git-changelog* recognizes are:

Type         | Section
-------------|-------------------------
`build`      | Build
`chore`      | Chore
`ci`         | Continuous Integration
`deps`       | Dependencies
`doc(s)`     | Docs
`feat`       | Features
`fix`        | Bug Fixes
`perf`       | Performance Improvements
`ref(actor)` | Code Refactoring
`revert`     | Reverts
`style`      | Style
`test(s)`    | Tests

Breaking changes are detected by searching for `^break(s|ing changes?)?[ :]`
in the commit message body.

### Conventional Commit convention

The [Conventional Commit specification][conventional-commit] originates
from the Angular commit message convention. It's basically the same thing,
but only the `feat` and `fix` types are specified, and the rest is up to you.
In *git-changelog* though, it is equivalent to the Angular convention,
with an additional thing: it detects breaking changes when `!`
appears right before the colon in the message summary
(for example: `refactor!: Stuff`).

## Choose the sections to render

[(--sections)](cli.md#sections)

Each commit message convention has a default set of sections
that will be rendered in the output. The other sections will be ignored.
To override this, you can provide a list of sections to render to *git-changelog*
with the `-s` or `--sections` CLI option:

```bash
# with the basic convention
git-changelog --sections add,fix,remove,doc

# with the angular/karma/conventionalcommit convention
git-changelog --sections build,deps,feat,fix,refactor
```

See the previous paragraphs to get the list of available sections
for each commit message convetions.

## Choose a changelog template

[(--template)](cli.md#template)

*git-changelog* provides two built-in templates: `keepachangelog` and `angular`.
Both are very similar, they just differ with the formatting a bit.
We stronly recommend the `keepachangelog` format.

Use the `-t`, `--template` option to specify the template to use:

```bash
git-changelog --template keepachangelog
```

You can also write and use your own changelog templates.
Templates are single files written using the [Jinja][jinja] templating engine.
You can get inspiration from
[the source of our built-in templates][builtin-templates].

Prefix the value passed to the `--template` option with `path:` to use a custom template:

```bash
git-changelog --template path:mytemplate.md
```

### Writing a changelog template

To write your own changelog template,
we recommend using our [keepachangelog built-in template][keepachangelog-template]
as a starting point.

From there, simply modify the different Jinja macros:

- `render_commit()`, which accepts a [Commit][git_changelog.build.Commit] object
- `render_section()`, which accepts a [Section][git_changelog.build.Section] object
- `render_version()`, which accepts a [Version][git_changelog.build.Version] object

Then, also update the template at the end, to change the changelog's header
or add a changelog footer for example.

The variables available in the template are `changelog`,
which is a [Changelog][git_changelog.build.Changelog] instance,
and `in_place`, which is a boolean, and tells whether the changelog
is being updated in-place.

> QUESTION: **How to get spacing right?**
> Although spacing (line jumps) is not super important in Markdown contents
> (it won't change HTML output), it is best if you get spacing right,
> as it makes prettier changelog files, and will reduce the noise
> in diffs when you commit an update to your changelog.
>
> To manage spacing (in Jinja terms, [control whitespace][control-whitespace])
> Jinja allows to "eat" spaces on the left or right of an expression,
> by adding a dash after/before the percent sign: `{%-` and `-%}`.
> However, spacing is not always easy to get right with Jinja,
> so here are two tips that we find helpful:
>
> - **To collapse content up**, eat spaces on the **left**, and add new lines
>     at the **top** of the Jinja block:
>
>     ```django
>     Some text.
>     {%- if some_condition %}
>
>     Some content.
>     {%- endif %}
>     ```
>
>     If the condition is true, there will be exactly one blank line
>     between "Some text" and "Some content". If not, there won't be
>     extreanous trailing blank lines :+1:
>
> - **To collapse content down**, eat spaces on the **right**, and add new lines
>     at the **bottom** of the Jinja block:
>
>     ```django
>     {% if some_condition -%}
>     Some content.
>
>     {% endif -%}
>     Some text.
>     ```
>
>     If the condition is true, there will be exactly one blank line
>     between "Some content" and "Some text". If not, there won't be
>     extreanous leading blank lines :+1:

### Extra Jinja context

[(--jinja-context)](cli.md#jinja_context)

Your custom changelog templates can support user-provided extra Jinja context.
This extra context is available in the `jinja_context` variable, which is a dictionary,
and is passed by users with the `-j`, `--jinja-context` CLI option
or with the `jinja_context` configuration option.

For example, you could let users specify their own changelog footer
by adding this at the end of your template:

```django
{% if jinja_context.footer %}
{{ jinja_context.footer }}
{% endif %}
```

Then users would be able to provide their own footer with the CLI option:

```bash
git-changelog -t path:changelog.md -j footer="Copyright 2024 My Company"
```

...or with the configuration option:

```toml
template = "path:changelog.md"

[jinja_context]
footer = "Copyright 2024 My Company"
```

## Filter commits

[(--filter-commits)](cli.md#filter_commits)

Sometimes it may be useful to use a limited set of commits, for example, if your
project has migrated to SemVer recently and you want to ignore old non-conventional commits.

This is possible through the option `-F`, `--filter-commits`, which takes a
*revision-range* to select the commits that will be used in the changelog.
This option will pass the [revision-range](https://git-scm.com/docs/git-log#
Documentation/git-log.txt-ltrevision-rangegt) to `git log`, so it will follow 
the rules defined by Git.

For example, to use commits from tag `0.5.0` up to latest:

```bash
git-changelog --filter-commits "0.5.0.."
```

Or using the commit hash:

```bash
git-changelog --filter-commits "2c0dbb8.."
```

## Understand the relationship with SemVer

[(--bump)](cli.md#bump)<br>
[(--versioning)](cli.md#versioning)<br>
[(--zerover)](cli.md#zerover)

*Although git-changelog supports several [versioning schemes](#choose-a-versioning-scheme),
SemVer plays a particular role when managing versions.*

[SemVer][semver], or Semantic Versioning, helps users of tools and libraries
understand the impact of version changes. To quote SemVer itself:

> Given a version number MAJOR.MINOR.PATCH, increment the:
>
> 1. MAJOR version when you make incompatible API changes
> 2. MINOR version when you add functionality in a backwards compatible manner
> 3. PATCH version when you make backwards compatible bug fixes

Thanks to the SemVer specification and the commit message conventions,
*git-changelog* is able to guess the new version your project is supposed
to take given a set of untagged commits (commits more recent than the latest tag).
An "Added" (basic convention) or "feat" (Angular/Karma/ConventionalCommit) commit
will bump the MINOR part of the latest tag. Other types will bump the PATCH part.
Commits containing breaking changes will bump the MAJOR part, unless MAJOR is 0,
in which case they'll only bump the MINOR part.

To tell *git-changelog* to try and guess the new version, use the `--bump=auto` CLI option:

```bash
git-changelog --bump auto
```

You can also specify a version to bump to directly:

```bash
git-changelog --bump 2.3.1
```

Or which part of the version to bump, resetting
numbers on its right to 0:

```bash
git-changelog --bump major  # 1.2.3 -> 2.0.0
git-changelog --bump minor  # 1.2.3 -> 1.3.0
git-changelog --bump patch  # 1.2.3 -> 1.2.4
```

As different schemes have different bumping strategies,
the selected scheme will affect the `--bump` option.
See [PEP 440 strategies](#pep-440) and [SemVer strategies](#semver).

### ZeroVer

Note that by default, "ZeroVer" mode is activated,
which means that a breaking change will only bump the major version
if the major version is already at `1` or more,
otherwise it will bump the minor version.

While this behavior is described in SemVer's specification,
the "ZeroVer" name comes from the satyrical
[ZeroVer (or zer0ver, 0ver) versioning scheme](https://0ver.org/).

When you are ready to bump to 1.0.0,
just pass this version as value, or use the `-Z`, `--no-zerover` flag.

Let say we are at version `0.1.0`, and unreleased commits
contain breaking changes:

```bash
git-changelog --bump auto      # 0.2.0
git-changelog --bump auto -Z   # 1.0.0
git-changelog --bump major     # 0.2.0
git-changelog --bump major -Z  # 1.0.0
```

If we are already at version `1.0.0`, and unreleased commits
contain breaking changes again:

```bash
git-changelog --bump auto      # 2.0.0
git-changelog --bump auto -Z   # 2.0.0, same
git-changelog --bump major     # 2.0.0
git-changelog --bump major -Z  # 2.0.0, same
```

If you use *git-changelog* in CI, to update your changelog automatically,
it is recommended to use a configuration file instead of the CLI option.
On a fresh project, start by setting `zerover = true` in one of the supported
[configuration files](#configuration-files). Then, once you are ready
to bump to v1, set `zerover = false` and commit it as a breaking change.
Once v1 is released, the setting has no use anymore, and you can remove it
from your configuration file.

## Choose a versioning scheme

[(--bump)](cli.md#bump)<br>
[(--versioning)](cli.md#versioning)<br>
[(--zerover)](cli.md#zerover)

*git-changelog* currently supports the following versioning schemes:

- `pep440`, see [PEP 440][pep440]
- `semver`, see [SemVer][semver]

Versioning schemes are useful to *git-changelog* when grouping commits
from your Git history into versions, and when bumping versions.

To choose a specific scheme, use the `-n`, `--versioning` CLI option:

```bash
git-changelog -n pep440
```

For backward compatibility reasons, it uses the SemVer scheme by default.

As different schemes have different bumping strategies,
the selected scheme will affect the `--bump` option.

### PEP 440

The bumping strategies supported by the PEP 440 scheme
are described in the table below.
Bumping a specific part of the version will remove or reset the parts
on its right to 0.

Strategy              | Example               | Description
--------------------- | --------------------- | -----------
`auto`                | -                     | Guess which of major, minor or micro to bump<br>thanks to the Git history and commit message conventions.
`epoch`               | `1!1` → `2!1`         | Bump [epoch][pep440-epoch], keeping [final release][pep440-release] only.
`release`             | `1rc2` → `1`          | Bump version to a [final release][pep440-release].
`major`               | `1.1` → `2.0`         | Bump major version.
`minor`               | `1.1.1` → `1.2.0`     | Bump minor version.
`micro` (or `patch`)  | `1.1.1.1` → `1.1.2.0` | Bump micro version.
`pre`                 | `1a0` → `1a1`         | Bump current [pre-release][pep440-pre] (alpha `a`, beta `b` or release candidate `rc`).
`alpha`               | `1a0` → `1a1`         | Bump current alpha pre-release.
`beta`                | `1b0` → `1b1`         | Bump current beta pre-release.
`candidate`           | `1rc0` → `1rc1`       | Bump current candidate pre-release.
`post`                | `1` → `1.post0`       | Bump to a [post-release][pep440-post].
`dev`                 | `1.dev0` → `1.dev1`   | Bump current [dev-release][pep440-dev].
`auto+alpha`          | -                     | Guess major/minor/micro bump, and set it to alpha pre-release.
`auto+beta`           | -                     | Guess major/minor/micro bump, and set it to beta pre-release.
`auto+candidate`      | -                     | Guess major/minor/micro bump, and set it to candidate pre-release.
`auto+dev`            | -                     | Guess major/minor/micro bump, and set it to dev-release.
`auto+alpha+dev`      | -                     | Guess major/minor/micro bump, and set it to alpha pre-release and dev-release.
`auto+beta+dev`       | -                     | Guess major/minor/micro bump, and set it to beta pre-release and dev-release.
`auto+candidate+dev`  | -                     | Guess major/minor/micro bump, and set it to candidate pre-release and dev-release.
`major+alpha`         | `1` → `2a0`           | Bump major version and set it to alpha pre-release.
`major+beta`          | `1` → `2b0`           | Bump major version and set it to beta pre-release.
`major+candidate`     | `1` → `2rc0`          | Bump major version and set it to candidate pre-release.
`major+dev`           | `1` → `2.dev0`        | Bump major version and set it to dev-release.
`major+alpha+dev`     | `1` → `2a0.dev0`      | Bump major version and set it to alpha pre-release and dev-release.
`major+beta+dev`      | `1` → `2b0.dev0`      | Bump major version and set it to beta pre-release and dev-release.
`major+candidate+dev` | `1` → `2rc0.dev0`     | Bump major version and set it to candidate pre-release and dev-release.
`minor+alpha`         | `1` → `1.1a0`         | Bump minor version and set it to alpha pre-release.
`minor+beta`          | `1` → `1.1b0`         | Bump minor version and set it to beta pre-release.
`minor+candidate`     | `1` → `1.1rc0`        | Bump minor version and set it to candidate pre-release.
`minor+dev`           | `1` → `1.1.dev0`      | Bump minor version and set it to dev-release.
`minor+alpha+dev`     | `1` → `1.1a0.dev0`    | Bump minor version and set it to alpha pre-release and dev-release.
`minor+beta+dev`      | `1` → `1.1b0.dev0`    | Bump minor version and set it to beta pre-release and dev-release.
`minor+candidate+dev` | `1` → `1.1rc0.dev0`   | Bump minor version and set it to candidate pre-release and dev-release.
`micro+alpha`         | `1` → `1.0.1a0`       | Bump micro version and set it to alpha pre-release.
`micro+beta`          | `1` → `1.0.1b0`       | Bump micro version and set it to beta pre-release.
`micro+candidate`     | `1` → `1.0.1rc0`      | Bump micro version and set it to candidate pre-release.
`micro+dev`           | `1` → `1.0.1.dev0`    | Bump micro version and set it to dev-release.
`micro+alpha+dev`     | `1` → `1.0.1a0.dev0`  | Bump micro version and set it to alpha pre-release and dev-release.
`micro+beta+dev`      | `1` → `1.0.1b0.dev0`  | Bump micro version and set it to beta pre-release and dev-release.
`micro+candidate+dev` | `1` → `1.0.1rc0.dev0` | Bump micro version and set it to candidate pre-release and dev-release.
`alpha+dev`           | `1a0` → `1a1.dev0`    | Bump current alpha pre-release and set it to a dev-release.
`beta+dev`            | `1b0` → `1b1.dev0`    | Bump current beta pre-release and set it to a dev-release.
`candidate+dev`       | `1rc0` → `1rc1.dev0`  | Bump current candidate pre-release and set it to a dev-release.

Try it out:

```pyodide install="git-changelog"
from git_changelog.versioning import bump_pep440

# "auto" strategies are not directly supported by this function
print(bump_pep440("1.2.3", "minor+alpha"))
```

The `v` prefix will be preserved when bumping a version: `v1` -> `v2`.

The bumping strategies for PEP 440 try to make the most sense,
allowing you to bump in a semantic way and preventing version downgrade mistakes.
Specifically, it is not possible:

- to bump from a final release version to a pre-release or a dev-release version
- to bump from a pre-release version to a lower pre-release version or a dev-version
- more generally, to bump from any version to any lower version

If you need to "bump" to a version that is lower than the latest released one,
you must explicitely pass the version to the `--bump` option:

```bash
# latest release is 1.1
git-changelog --bump 1.0
```

### SemVer

The bumping strategies supported by the SemVer scheme
are described in the table below.
Bumping a specific part of the version will remove or reset the parts
on its right to 0.

Strategy              | Example               | Description
--------------------- | --------------------- | -----------
`auto`                | -                     | Guess which of major, minor or patch to bump<br>thanks to the Git history and commit message conventions.
`major`               | `1.1.1` → `2.0.0`     | Bump major version.
`minor`               | `1.1.1` → `1.2.0`     | Bump minor version.
`patch`               | `1.1.1` → `1.1.2`     | Bump micro version.
`release`             | `1.1.1-a2` → `1.1.1`  | Bump version to a final release (remove pre-release and build metadata).

Try it out:

```pyodide install="git-changelog"
from git_changelog.versioning import bump_semver

# the "auto" strategy is not directly supported by this function
print(bump_semver("1.2.3", "minor"))
```

The `v` prefix will be preserved when bumping a version: `v1.0.0` -> `v2.0.0`.

The bumping strategies for SemVer will prevent you from bumping from any version to a lower one.
It does not support bump pre-release metadata or build metadata
because these are not standardized.

If you need to "bump" to a version that is lower than the latest released one,
or to add pre-release or build metadata,
you must explicitely pass the version to the `--bump` option:

```bash
# downgrade
git-changelog --bump 1.1.0

# add pre-release metadata
git-changelog --bump 2.0.0-alpha1
```

## Parse additional information in commit messages

*git-changelog* is able to parse the body of commit messages
to find additional information.

### Provider-specific references

[(--parse-refs)](cli.md#parse_refs)<br>
[(--provider)](cli.md#provider)

*git-changelog* will detect when you are using GitHub, GitLab or Bitbucket
by checking the `origin` remote configured in your local clone
(or the remote indicated by the value of the `GIT_CHANGELOG_REMOTE` environment variable).

Detecting the provider allows *git-changelog* to build URLs to specific commits and tags.
But it also allows it to parse text references understood by these providers
in the commit messages. For example: #18 (issue) or a78bcf2e (commit hash).
These references are then available when rendering the changelog template,
allowing to add links to issues, pull requests, users, etc.

Example of a commit message with GitLab references:

```text
fix: Fix atrocious bug

Fixes issue #14.
Follow-up of MR !7.
Part of milestone %2.
```

To enable provider-specific reference parsing, use the `-r` or `--parse-refs` CLI option:

```bash
git-changelog --parse-refs
```

Provider-references are a bit limited, difficult to parse and favor vendor lock-in,
so for these reasons we do not recommend them. Instead, we recommend using Git trailers.

### Git trailers

[(--trailers)](cli.md#parse_trailers)

Git has an [`interpret-trailers`][git-trailers] command
that allows to add or parse trailers line to commit messages.
Trailers line are located in the footer of commit message:
there must be a blank line between the body and the first trailer.
Each trailer is a line of the form `token: value`, for example
`Co-authored-by: Timothée Mazzucotelli <pawamoy@pm.me>`.

The tokens are specified not to allow whitespace in them,
but *git-changelog* takes the liberty to lift up this limitation
for convenience. It means you can write `Issue 18: https://...`
instead of `Issue-18: https://...`. The first colon + space (`: `)
delimitate the token and value.

Example of a commit message with Git trailers:

```text
fix: Fix atrocious bug

Fixes issue #14: https://github.com/super/repo/issues/14
Follow-up of PR #7: https://github.com/super/repo/pull/7
Part of epic #5: https://agile-software.com/super/project/epics/5
```

As you can see, compared to provider-specific references,
trailers are written out explicitly, so it's a bit more work,
but this ensures your changelog can be rendered correctly *anywhere*,
not just on GitHub, GitLab or Bitbucket, and without pre/post-processing.

Trailers are rendered in the Keep A Changelog template.
If the value is an URL, a link is created with the token as title.
If not, the trailer is written as is.

Example of how the previous trailers are rendered:

```md exec="1" source="material-block"
- Fix atrocious bug ([aafa779](https://github.com/super/repo/commit/aafa7793ec02a) by John Doe).
    [Fixes issue #14](https://github.com/super/repo/issues/14),
    [Follow-up of PR #7](https://github.com/super/repo/pull/7),
    [Part of epic #5](https://agile-software.com/super/project/epics/5)
```

To enable Git trailers parsing, use the `-T` or `--trailers` CLI option:

```bash
git-changelog --trailers
```

## Update changelog in place

[(--in-place)](cli.md#in_place)<br>
[(--marker-line)](cli.md#marker_line)<br>
[(--version-regex)](cli.md#version_regex)

Writing the whole generated changelog to a file is nice,
but sometimes you need to tweak the entries in your changelog
and you don't want to overwrite these slight modifications
each time your regenerate your changelog.

For this reason, *git-changelog* is able to update a changelog file in-place.
It means that it will only insert new entries at the top of the changelog,
without modifying existing ones.

To update a changelog in-place, use the `-i` or `--in-place` CLI option:

```bash
git-changelog --output CHANGELOG.md --in-place
```

To achieve this, *git-changelog* searches for versions (entries)
already written to the changelog with a regular expression.
The verions that are not found in the changelog will be added at the top.
To know where to add them exactly, we search for a marker line in the changelog.
This marker line is an HTML comment: it is not visible when the changelog
is displayed in web pages.

To support in-place updates in a custom template, you have two choices:

1. format versions in your template so they match the default regular expression,
    and use the default marker line(s) to tell *git-changelog* where
    to insert new entries. Here are these default values:

    ```python
    DEFAULT_VERSION_REGEX = r"^## \[(?P<version>v?[^\]]+)"
    DEFAULT_MARKER_LINE = "<!-- insertion marker -->"
    ```

2. provide a custom regular expression and marker line,
    to match the contents of your custom template,
    with the `-g` or `--version-regex`, and `-m` or `--marker-line` CLI options:

    ```bash
    git-changelog --output CHANGELOG.md --in-place \
        --version-regex '<a href="[^"]+">(?P<version>[^<]+)' \
        --marker-line '<!-- new entries will be injected here -->'
    ```

When only one marker line is found in the template,
new entries are inserted at this line exactly, overwriting it
(but the marker is added again by the new entries themselves).

When two marker lines are found, new entries are applied between
those two lines, overwriting the previous contents.
This is useful when you don't tell *git-changelog* to bump the latest version:
you will have an "Unreleased" section that is overwritten and updated
each time you update your changelog in-place.

## Output release notes

[(--input)](cli.md#input)<br>
[(--release-notes)](cli.md#release_notes)

Some platforms allow to announce releases with additional "release notes".
*git-changelog* can help generating release notes too, by simply
reading your existing changelog and printing the latest entry.
So if you just pushed a tag with an updated changelog,
you can use *git-changelog* in Continuous Integration/Deployment
to create a release (specific to your platform, e.g. GitHub)
with the latest changelog entry as release notes.

For example, on GitHub, with the [softprops/action-gh-release][] action:

```yaml
name: github_release

on: push

jobs:
  github_release:
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
    - name: Install git-changelog
      run: pip install git-changelog
    - name: Prepare release notes
      run: git-changelog --release-notes > release-notes.md
    - name: Create GitHub release
      uses: softprops/action-gh-release@v1
      with:
        body_path: release-notes.md
```

By default *git-changelog* will try to read release notes
from a file named `CHANGELOG.md`. Use the `-i`, `--input`
option to specify another file to read from.
Other options can be used to help *git-changelog* retrieving
the latest entry from your changelog: `--version-regex`
and `--marker-line`.

[keepachangelog]: https://keepachangelog.com/en/1.0.0/
[conventional-commit]: https://www.conventionalcommits.org/en/v1.0.0-beta.4/
[jinja]: https://jinja.palletsprojects.com/en/3.1.x/
[semver]: https://semver.org/
[git-trailers]: https://git-scm.com/docs/git-interpret-trailers
[softprops/action-gh-release]: https://github.com/softprops/action-gh-release
[keepachangelog-template]: https://github.com/pawamoy/git-changelog/tree/main/src/git_changelog/templates/keepachangelog.md
[builtin-templates]: https://github.com/pawamoy/git-changelog/tree/main/src/git_changelog/templates
[control-whitespace]: https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control
[pep440]: https://peps.python.org/pep-0440/
[pep440-epoch]: https://peps.python.org/pep-0440/#version-epochs
[pep440-pre]: https://peps.python.org/pep-0440/#pre-releases
[pep440-post]: https://peps.python.org/pep-0440/#post-releases
[pep440-dev]: https://peps.python.org/pep-0440/#developmental-releases
[pep440-release]: https://peps.python.org/pep-0440/#final-releases
