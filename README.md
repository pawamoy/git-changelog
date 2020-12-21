# git-changelog

[![ci](https://github.com/pawamoy/git-changelog/workflows/ci/badge.svg)](https://github.com/pawamoy/git-changelog/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/git-changelog/)
[![pypi version](https://img.shields.io/pypi/v/git-changelog.svg)](https://pypi.org/project/git-changelog/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/git-changelog/community)

Automatic Changelog generator using Jinja2 templates. From git logs to change logs.

## Features

- [Jinja2][jinja2] templates!
  You get full control over the rendering.
  Built-in [Keep a Changelog][keep-a-changelog] and [Angular][angular] templates
  (also see [Conventional Changelog][conventional-changelog]).
- Commit styles/conventions parsing.
  Built-in [Angular][angular-style], [Atom][atom-style] and basic styles.
- Git service/provider agnostic,
  plus references parsing (issues, commits, etc.).
  Built-in [GitHub][github-refs] and [Gitlab][gitlab-refs] support.
- Understands [Semantic Versioning][semantic-versioning]:
  major/minor/patch for versions and commits.
  Guesses next version based on last commits.

- Todo:
  - [Plugin architecture][issue-7],
    to support more commit styles and git services.
  - [Template context injection][issue-4],
    to furthermore customize how your changelog will be rendered.
  - [Easy access to "Breaking Changes"][issue-1] in the templates.
  - [Update changelog in-place][issue-2], paired with
    [commits/dates/versions range limitation ability][issue-3].

[jinja2]:                 http://jinja.pocoo.org/
[keep-a-changelog]:       http://keepachangelog.com/en/1.0.0/
[angular]:                https://github.com/angular/angular/blob/master/CHANGELOG.md
[conventional-changelog]: https://github.com/conventional-changelog/conventional-changelog
[semantic-versioning]:    http://semver.org/spec/v2.0.0.html
[atom-style]:             https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages
[angular-style]:          https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit
[github-refs]:            https://help.github.com/articles/autolinked-references-and-urls/
[gitlab-refs]:            https://docs.gitlab.com/ce/user/markdown.html#special-gitlab-references

[issue-1]: https://gitlab.com/pawamoy/git-changelog/issues/1
[issue-2]: https://gitlab.com/pawamoy/git-changelog/issues/2
[issue-3]: https://gitlab.com/pawamoy/git-changelog/issues/3
[issue-4]: https://gitlab.com/pawamoy/git-changelog/issues/4
[issue-5]: https://gitlab.com/pawamoy/git-changelog/issues/5
[issue-6]: https://gitlab.com/pawamoy/git-changelog/issues/6
[issue-7]: https://gitlab.com/pawamoy/git-changelog/issues/7

## Requirements

git-changelog requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.12

# make it available globally
pyenv global system 3.6.12
```
</details>

## Installation

With `pip`:
```bash
python3.6 -m pip install git-changelog
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.6 -m pip install --user pipx

pipx install --python python3.6 git-changelog
```

## Usage (command-line)

```
usage: git-changelog [-h] [-o OUTPUT] [-s {angular,atom,basic}]
                     [-t {angular,keepachangelog}] [-v]
                     REPOSITORY

Command line tool for git-changelog Python package.

positional arguments:
  REPOSITORY            The repository path, relative or absolute.

optional arguments:
  -h, --help            Show this help message and exit.
  -o OUTPUT, --output OUTPUT
                        Output to given file. Default: stdout.
  -s {angular,atom,basic}, --style {angular,atom,basic}
                        The commit style to match against.
  -t {angular,keepachangelog}, --template {angular,keepachangelog}
                        The Jinja2 template to use. Prefix with "path:" to
                        specify the path to a directory containing a file
                        named "changelog.md".
  -v, --version         Show the current version of the program and exit.

```
