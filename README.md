# git-changelog

[![ci](https://github.com/pawamoy/git-changelog/workflows/ci/badge.svg)](https://github.com/pawamoy/git-changelog/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/git-changelog/)
[![pypi version](https://img.shields.io/pypi/v/git-changelog.svg)](https://pypi.org/project/git-changelog/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/git-changelog)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/git-changelog/community)

Automatic Changelog generator using Jinja2 templates. From git logs to change logs.

## Features

- [Jinja2][jinja2] templates!
  You get full control over the rendering.
  Built-in [Keep a Changelog][keep-a-changelog] and [Angular][angular] templates
  (also see [Conventional Changelog][conventional-changelog]).
- Commit styles/conventions parsing.
  Built-in [Angular][angular-style], [Conventional Commit][conventional-commit], [Atom][atom-style] and basic styles.
- Git service/provider agnostic,
  plus references parsing (issues, commits, etc.).
  Built-in [GitHub][github-refs] and [Gitlab][gitlab-refs] support.
- Understands [Semantic Versioning][semantic-versioning]:
  major/minor/patch for versions and commits.
  Guesses next version based on last commits.

- Todo:
    - [Plugin architecture][issue-19],
      to support more commit styles and git services.
    - [Template context injection][issue-17],
      to furthermore customize how your changelog will be rendered.
    - [Easy access to "Breaking Changes"][issue-14] in the templates.
    - [Update changelog in-place][issue-15], paired with
      [commits/dates/versions range limitation ability][issue-16].

[jinja2]:                 http://jinja.pocoo.org/
[keep-a-changelog]:       http://keepachangelog.com/en/1.0.0/
[angular]:                https://github.com/angular/angular/blob/master/CHANGELOG.md
[conventional-changelog]: https://github.com/conventional-changelog/conventional-changelog
[semantic-versioning]:    http://semver.org/spec/v2.0.0.html
[atom-style]:             https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages
[angular-style]:          https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit
[conventional-commit]:    https://www.conventionalcommits.org/en/v1.0.0/
[github-refs]:            https://help.github.com/articles/autolinked-references-and-urls/
[gitlab-refs]:            https://docs.gitlab.com/ce/user/markdown.html#special-gitlab-references

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
python3.7 -m pip install --user pipx
pipx install git-changelog
```

## Usage (command-line)

```
usage: git-changelog [-h] [-o OUTPUT] [-R]
                     [-s {angular,atom,conventional,basic}]
                     [-t {angular,keepachangelog}] [-T] [-v]
                     REPOSITORY

Command line tool for git-changelog Python package.

positional arguments:
  REPOSITORY            The repository path, relative or absolute.

optional arguments:
  -h, --help            Show this help message and exit.
  -o OUTPUT, --output OUTPUT
                        Output to given file. Default: stdout.
  -R, --no-parse-refs   Do not parse provider-specific references in commit
                        messages (issues, PRs, etc.).
  -s {angular,atom,conventional,basic}, --style {angular,atom,conventional,basic}
                        The commit style to match against. Default: basic.
  -t {angular,keepachangelog}, --template {angular,keepachangelog}
                        The Jinja2 template to use. Prefix with "path:" to
                        specify the path to a directory containing a file
                        named "changelog.md".
  -T, --trailers        Parse Git trailers in the commit message. See
                        https://git-scm.com/docs/git-interpret-trailers.
  -v, --version         Show the current version of the program and exit.
```
