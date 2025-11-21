# git-changelog

Automatic Changelog generator using Jinja2 templates. From git logs to change logs.

## Features

- [Jinja2](http://jinja.pocoo.org/) templates! You get full control over the rendering. Built-in [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and [Angular](https://github.com/angular/angular/blob/master/CHANGELOG.md) templates (also see [Conventional Changelog](https://github.com/conventional-changelog/conventional-changelog)).

- Commit styles/conventions parsing. Built-in [Angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit), [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) and basic conventions.

- Git service/provider agnostic, plus references parsing (issues, commits, etc.). Built-in [GitHub](https://help.github.com/articles/autolinked-references-and-urls/), [Gitlab](https://docs.gitlab.com/ce/user/markdown.html#special-gitlab-references) and [Bitbucket](https://support.atlassian.com/bitbucket-cloud/docs/markup-comments) support.

- Understands [SemVer](http://semver.org/spec/v2.0.0.html) and [PEP 440](https://peps.python.org/pep-0440/) versioning schemes. Guesses next version based on last commits.

- Parses [Git trailers](https://git-scm.com/docs/git-interpret-trailers), allowing to reference issues, PRs, etc., in your commit messages in a clean, provider-agnostic way.

- Template context injection, to furthermore customize how your changelog will be rendered.

- Todo:

  - [Plugin architecture](https://github.com/pawamoy/git-changelog/issues/19), to support more commit conventions and git services.
  - [Easy access to "Breaking Changes"](https://github.com/pawamoy/git-changelog/issues/14) in the templates.

## Installation

```
pip install git-changelog
```

With [`uv`](https://docs.astral.sh/uv/):

```
uv tool install git-changelog
```

## Usage

Simply run `git-changelog` in your repository to output a changelog on standard output. To show the different options and their descriptions, use `git-changelog -h`.

- See [Quick usage](http://pawamoy.github.io/git-changelog/usage/#quick-usage) for some command line examples.
- See [Configuration](https://pawamoy.github.io/git-changelog/usage/#configuration-files) to learn how to configure *git-changelog* for your project.
- See the [CLI reference](https://pawamoy.github.io/git-changelog/cli) and the [API reference](https://pawamoy.github.io/git-changelog/reference) for more information.

## Alternatives

- [git-cliff](https://github.com/orhun/git-cliff): A highly customizable Changelog Generator that follows Conventional Commit specifications.

## Sponsors
