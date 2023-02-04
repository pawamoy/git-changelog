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
git-changelog -bio CHANGELOG.md -c angular
```

Same thing, but also parse Git trailers
and choose the sections to render, and their order
(author's favorite!):

```bash
git-changelog -Tbio CHANGELOG.md -c angular -s build,deps,fix,feat,refactor
```

Generate a changelog using a custom template,
and parsing provider-specific references (GitHub/GitLab):

```bash
git-changelog -rt path:./templates/changelog.md.jinja 
```

Author's favorite, from Python:

```python
from git_changelog.cli import build_and_render

build_and_render(
    repository=".",
    output="CHANGELOG.md",
    convention="angular",
    template="keepachangelog",
    parse_trailers=True,
    parse_refs=False,
    sections=("build", "deps", "feat", "fix", "refactor"),
    bump_latest=True,
    in_place=True,
)
```

The following sections explain in more details all the features of *git-changelog*.

## Output a changelog

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

Different conventions, or styles, are supported by *git-changelog*.
To select a different convention than the default one (basic, see below),
use the `-c` or `--convention` CLI option:

```
git-changelog --convention angular
```

### Basic convention

The basic convention, as the name implies, is very simple.
If a commit message summary (the first line of the message)
with a particular word/prefix (case-insensitive),
it is added to the corresponding section:

Type    | Section
------- | -------
`add`     | Added
`fix`     | Fixed
`change`  | Changed
`remove`  | Removed
`merge`   | Merged
`doc`     | Documented

### Angular/Karma convention

The Angular/Karma convention initiated the [Conventional Commit specification][conventional-commit].
It expects the following format for commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

The types and corresponding sections *git-changelog* recognizes are:

Type          | Section
------------- | -------
`build`       | Build
`chore`       | Chore
`ci`          | Continuous Integration
`deps`        | Dependencies
`doc(s)`      | Docs
`feat`        | Features
`fix`         | Bug Fixes
`perf`        | Performance Improvements
`ref(actor)`  | Code Refactoring
`revert`      | Reverts
`style`       | Style
`test(s)`     | Tests

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

*git-changelog* provides two built-in templates: `keepachangelog` and `angular`.
Both are very similar, they just differ with the formatting a bit.
We stronly recommend the `keepachangelog` format.

You can also write and use your own changelog templates.
Templates are single files written using the [Jinja][jinja] templating engine.
You can get inspiration from
[the source of our built-in templates](https://github.com/pawamoy/git-changelog/tree/master/src/git_changelog/templates).

## Understand the relationship with SemVer

[Semver](semver), or Semantic Versioning, helps users of tools and libraries
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

To tell *git-changelog* to try and guess the new version, use the `-b` or `--bump-latest` CLI option:

```bash
git-changelog --bump
```

## Parse additional information in commit messages

*git-changelog* is able to parse the body of commit messages
to find additional information.

### Provider-specific references

*git-changelog* will detect when you are using GitHub or GitLab
by checking the `origin` remote configured in your local clone
(or the remote indicated by the value of the `GIT_CHANGELOG_REMOTE` environment variable).

Detecting the provider allows *git-changelog* to build URLs to specific commits and tags.
But it also allows it to parse text references understood by these providers
in the commit messages. For example: #18 (issue) or a78bcf2e (commit hash).
These references are then available when rendering the changelog template,
allowing to add links to issues, pull requests, users, etc.

Example of a commit message with GitLab references:

```
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

```
fix: Fix atrocious bug

Fixes issue #14: https://github.com/super/repo/issues/14
Follow-up of PR #7: https://github.com/super/repo/pull/7
Part of epic #5: https://agile-software.com/super/project/epics/5
```

As you can see, compared to provider-specific references,
trailers are written out explicitely, so it's a bit more work,
but this ensures your changelog can be rendered correctly *anywhere*,
not just on GitHub or GitLab, and without pre/post-processing.

Trailers are rendered in the Keep A Changelog template.
If the value is an URL, a link is created with the token as title.
If not, the trailer is written as is.

Example of how the previous trailers are rendered:

```md exec="1" source="material-block"
- Fix atrocious bug ([aafa779](https://github.com/super/repo/commit/aafa7793ec02a) by John Doe).
    [Fixes issue #14](https://github.com/super/repo/issues/14),
    [Follow-up of PR #7](https://github.com/super/repo/pull/7),
    [Part of epic #5](https://agile-software.com/super/project/epics/5),
```

To enable Git trailers parsing, use the `-T` or `--parse-trailers` CLI option:

```bash
git-changelog --parse-trailers
```

## Update changelog in place

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
    DEFAULT_VERSION_REGEX = r"^## \[v?(?P<version>[^\]]+)"
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

[keepachangelog]: https://keepachangelog.com/en/1.0.0/
[conventional-commit]: https://www.conventionalcommits.org/en/v1.0.0-beta.4/
[jinja]: https://jinja.palletsprojects.com/en/3.1.x/
[semver]: https://semver.org/
[git-trailers]: https://git-scm.com/docs/git-interpret-trailers
