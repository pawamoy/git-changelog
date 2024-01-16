# git-changelog

[![ci](https://github.com/pawamoy/git-changelog/workflows/ci/badge.svg)](https://github.com/pawamoy/git-changelog/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/git-changelog/)
[![pypi version](https://img.shields.io/pypi/v/git-changelog.svg)](https://pypi.org/project/git-changelog/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/git-changelog)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#git-changelog:gitter.im)

Automatic Changelog generator using Jinja2 templates. From git logs to change logs.

## Features

- [Jinja2][jinja2] templates!
  You get full control over the rendering.
  Built-in [Keep a Changelog][keep-a-changelog] and [Angular][angular] templates
  (also see [Conventional Changelog][conventional-changelog]).
- Commit styles/conventions parsing.
  Built-in [Angular][angular-convention], [Conventional Commit][conventional-commit] and basic conventions.
- Git service/provider agnostic,
  plus references parsing (issues, commits, etc.).
  Built-in [GitHub][github-refs], [Gitlab][gitlab-refs] and [Bitbucket][bitbucket-refs] support.
- Understands [Semantic Versioning][semantic-versioning]:
  major/minor/patch for versions and commits.
  Guesses next version based on last commits.
- Parses [Git trailers][git-trailers], allowing to reference
  issues, PRs, etc., in your commit messages
  in a clean, provider-agnostic way.

- Todo:
    - [Plugin architecture][issue-19],
      to support more commit conventions and git services.
    - [Template context injection][issue-17],
      to furthermore customize how your changelog will be rendered.
    - [Easy access to "Breaking Changes"][issue-14] in the templates.
    - [Commits/dates/versions range limitation ability][issue-16].

[jinja2]:                 http://jinja.pocoo.org/
[keep-a-changelog]:       http://keepachangelog.com/en/1.0.0/
[angular]:                https://github.com/angular/angular/blob/master/CHANGELOG.md
[conventional-changelog]: https://github.com/conventional-changelog/conventional-changelog
[semantic-versioning]:    http://semver.org/spec/v2.0.0.html
[angular-convention]:     https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit
[conventional-commit]:    https://www.conventionalcommits.org/en/v1.0.0/
[github-refs]:            https://help.github.com/articles/autolinked-references-and-urls/
[gitlab-refs]:            https://docs.gitlab.com/ce/user/markdown.html#special-gitlab-references
[bitbucket-refs]:         https://support.atlassian.com/bitbucket-cloud/docs/markup-comments
[git-trailers]:           https://git-scm.com/docs/git-interpret-trailers

[issue-14]: https://github.com/pawamoy/git-changelog/issues/14
[issue-15]: https://github.com/pawamoy/git-changelog/issues/15
[issue-16]: https://github.com/pawamoy/git-changelog/issues/16
[issue-17]: https://github.com/pawamoy/git-changelog/issues/17
[issue-19]: https://github.com/pawamoy/git-changelog/issues/19

## Installation

With `pip`:

```bash
pip install git-changelog
```

With [`pipx`](https://github.com/pipxproject/pipx):

```bash
python3.8 -m pip install --user pipx
pipx install git-changelog
```

## Usage

```
git-changelog [--config-file [PATH ...]] [-b] [-B VERSION] [-h] [-i]
              [-g VERSION_REGEX] [-m MARKER_LINE] [-o OUTPUT]
              [-p {github,gitlab,bitbucket}] [-r] [-R] [-I INPUT]
              [-c {angular,conventional,basic}] [-s SECTIONS]
              [-t {angular,keepachangelog}] [-T] [-E] [-Z] [-F FILTER_COMMITS]
              [-V] [--debug-info]
              [REPOSITORY]
```

Simply run `git-changelog` in your repository to output a changelog on standard output.
To show the different options and their descriptions, use `git-changelog -h`.

- See [Quick usage](http://pawamoy.github.io/git-changelog/usage/#quick-usage)
  for some command line examples.
- See [Configuration](https://pawamoy.github.io/git-changelog/usage/#configuration-files)
  to learn how to configure *git-changelog* for your project.
- See the [CLI reference](https://pawamoy.github.io/git-changelog/cli)
  and the [API reference](https://pawamoy.github.io/git-changelog/reference) for more information.
