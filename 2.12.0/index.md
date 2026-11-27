# git-changelog

[![ci](<https://github.com/pawamoy/git-changelog/workflows/ci/badge.svg>)](<https://github.com/pawamoy/git-changelog/actions?query=workflow%3Aci>) [![documentation](<https://img.shields.io/badge/docs-zensical-FF9100.svg?style=flat>)](<https://pawamoy.github.io/git-changelog/>) [![pypi version](<https://img.shields.io/pypi/v/git-changelog.svg>)](<https://pypi.org/project/git-changelog/>)

Automatic Changelog generator using Jinja2 templates. From git logs to change logs.

## Features

- [Jinja2](<http://jinja.pocoo.org/>) templates! You get full control over the rendering. Built-in [Keep a Changelog](<http://keepachangelog.com/en/1.0.0/>) and [Angular](<https://github.com/angular/angular/blob/master/CHANGELOG.md>) templates (also see [Conventional Changelog](<https://github.com/conventional-changelog/conventional-changelog>)).
- Commit styles/conventions parsing. Built-in [Angular](<https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit>), [Conventional Commit](<https://www.conventionalcommits.org/en/v1.0.0/>) and basic conventions.
- Git service/provider agnostic, plus references parsing (issues, commits, etc.). Built-in [GitHub](<https://help.github.com/articles/autolinked-references-and-urls/>), [Gitlab](<https://docs.gitlab.com/ce/user/markdown.html#special-gitlab-references>) and [Bitbucket](<https://support.atlassian.com/bitbucket-cloud/docs/markup-comments>) support.
- Understands [SemVer](<http://semver.org/spec/v2.0.0.html>) and [PEP 440](<https://peps.python.org/pep-0440/>) versioning schemes. Guesses next version based on last commits.
- Parses [Git trailers](<https://git-scm.com/docs/git-interpret-trailers>), allowing to reference issues, PRs, etc., in your commit messages in a clean, provider-agnostic way.
- Template context injection, to furthermore customize how your changelog will be rendered.
- Todo:

  - [Plugin architecture](<https://github.com/pawamoy/git-changelog/issues/19>), to support more commit conventions and git services.
  - [Easy access to "Breaking Changes"](<https://github.com/pawamoy/git-changelog/issues/14>) in the templates.

## Installation

```
pip install git-changelog
```

With [`uv`](<https://docs.astral.sh/uv/>):

```
uv tool install git-changelog
```

## Usage

Simply run `git-changelog` in your repository to output a changelog on standard output. To show the different options and their descriptions, use `git-changelog -h`.

- See [Quick usage](<http://pawamoy.github.io/git-changelog/usage/#quick-usage>) for some command line examples.
- See [Configuration](<https://pawamoy.github.io/git-changelog/usage/#configuration-files>) to learn how to configure *git-changelog* for your project.
- See the [CLI reference](<https://pawamoy.github.io/git-changelog/cli>) and the [API reference](<https://pawamoy.github.io/git-changelog/reference>) for more information.

## Alternatives

- [git-cliff](<https://github.com/orhun/git-cliff>): A highly customizable Changelog Generator that follows Conventional Commit specifications.

## Sponsors

**Bronze sponsors**

[![Nixtla](<https://www.nixtla.io/img/logo/full-black.svg>)](<https://www.nixtla.io/>)

---

[![ofek](<https://avatars.githubusercontent.com/u/9677399?u=386c330f212ce467ce7119d9615c75d0e9b9f1ce&amp;v=4>)](<https://github.com/ofek>) [![samuelcolvin](<https://avatars.githubusercontent.com/u/4039449?u=42eb3b833047c8c4b4f647a031eaef148c16d93f&amp;v=4>)](<https://github.com/samuelcolvin>) [![tlambert03](<https://avatars.githubusercontent.com/u/1609449?u=922abf0524b47739b37095e553c99488814b05db&amp;v=4>)](<https://github.com/tlambert03>) [![ssbarnea](<https://avatars.githubusercontent.com/u/102495?u=c7bd9ddf127785286fc939dd18cb02db0a453bce&amp;v=4>)](<https://github.com/ssbarnea>) [![femtomc](<https://avatars.githubusercontent.com/u/34410036?u=f13a71daf2a9f0d2da189beaa94250daa629e2d8&amp;v=4>)](<https://github.com/femtomc>) [![FastAPI](<https://raw.githubusercontent.com/tiangolo/fastapi/master/docs/en/docs/img/logo-margin/logo-teal.png>)](<https://fastapi.tiangolo.com/>) [![cmarqu](<https://avatars.githubusercontent.com/u/360986?v=4>)](<https://github.com/cmarqu>) [![kolenaIO](<https://avatars.githubusercontent.com/u/77010818?v=4>)](<https://github.com/kolenaIO>) [![ramnes](<https://avatars.githubusercontent.com/u/835072?u=3fca03c3ba0051e2eb652b1def2188a94d1e1dc2&amp;v=4>)](<https://github.com/ramnes>) [![machow](<https://avatars.githubusercontent.com/u/2574498?u=c41e3d2f758a05102d8075e38d67b9c17d4189d7&amp;v=4>)](<https://github.com/machow>) [![BenHammersley](<https://avatars.githubusercontent.com/u/99436?u=4499a7b507541045222ee28ae122dbe3c8d08ab5&amp;v=4>)](<https://github.com/BenHammersley>) [![trevorWieland](<https://avatars.githubusercontent.com/u/28811461?u=74cc0e3756c1d4e3d66b5c396e1d131ea8a10472&amp;v=4>)](<https://github.com/trevorWieland>) [![MarcoGorelli](<https://avatars.githubusercontent.com/u/33491632?u=7de3a749cac76a60baca9777baf71d043a4f884d&amp;v=4>)](<https://github.com/MarcoGorelli>) [![analog-cbarber](<https://avatars.githubusercontent.com/u/7408243?u=fe0e7bf2882d1c9c901a341c2502e1518466527a&amp;v=4>)](<https://github.com/analog-cbarber>) [![OdinManiac](<https://avatars.githubusercontent.com/u/22727172?u=36ab20970f7f52ae8e7eb67b7fcf491fee01ac22&amp;v=4>)](<https://github.com/OdinManiac>) [![rstudio-sponsorship](<https://avatars.githubusercontent.com/u/58949051?u=0c471515dd18111be30dfb7669ed5e778970959b&amp;v=4>)](<https://github.com/rstudio-sponsorship>) [![schlich](<https://avatars.githubusercontent.com/u/21191435?u=6f1240adb68f21614d809ae52d66509f46b1e877&amp;v=4>)](<https://github.com/schlich>) [![butterlyn](<https://avatars.githubusercontent.com/u/53323535?v=4>)](<https://github.com/butterlyn>) [![livingbio](<https://avatars.githubusercontent.com/u/10329983?v=4>)](<https://github.com/livingbio>) [![NemetschekAllplan](<https://avatars.githubusercontent.com/u/912034?v=4>)](<https://github.com/NemetschekAllplan>) [![EricJayHartman](<https://avatars.githubusercontent.com/u/9259499?u=7e58cc7ec0cd3e85b27aec33656aa0f6612706dd&amp;v=4>)](<https://github.com/EricJayHartman>) [![15r10nk](<https://avatars.githubusercontent.com/u/44680962?u=f04826446ff165742efa81e314bd03bf1724d50e&amp;v=4>)](<https://github.com/15r10nk>) [![activeloopai](<https://avatars.githubusercontent.com/u/34816118?v=4>)](<https://github.com/activeloopai>) [![roboflow](<https://avatars.githubusercontent.com/u/53104118?v=4>)](<https://github.com/roboflow>) [![RapidataAI](<https://avatars.githubusercontent.com/u/104209891?v=4>)](<https://github.com/RapidataAI>) [![rodolphebarbanneau](<https://avatars.githubusercontent.com/u/46493454?u=6c405452a40c231cdf0b68e97544e07ee956a733&amp;v=4>)](<https://github.com/rodolphebarbanneau>) [![theSymbolSyndicate](<https://avatars.githubusercontent.com/u/111542255?v=4>)](<https://github.com/theSymbolSyndicate>) [![blakeNaccarato](<https://avatars.githubusercontent.com/u/20692450?u=bb919218be30cfa994514f4cf39bb2f7cf952df4&amp;v=4>)](<https://github.com/blakeNaccarato>) [![ChargeStorm](<https://avatars.githubusercontent.com/u/26000165?v=4>)](<https://github.com/ChargeStorm>) [![Cusp-AI](<https://avatars.githubusercontent.com/u/178170649?v=4>)](<https://github.com/Cusp-AI>)

*And 4 more private sponsor(s).*
