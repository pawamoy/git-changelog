# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [2.4.0](https://github.com/pawamoy/git-changelog/releases/tag/2.4.0) - 2023-11-04

<small>[Compare with 2.3.2](https://github.com/pawamoy/git-changelog/compare/2.3.2...2.4.0)</small>

### Features

- Add option to enable/disable "zerover" behavior ([7d0c259](https://github.com/pawamoy/git-changelog/commit/7d0c259f2ec4c5666d15a3616de8765f52fb282c) by Mark Minakov). [Issue #57](https://github.com/pawamoy/git-changelog/issues/57), [PR #58](https://github.com/pawamoy/git-changelog/pull/58), Co-authored-by: Timothée Mazzucotelli <pawamoy@pm.me>
- Add `-F,--filter-commits` to filter by revision-range ([e016965](https://github.com/pawamoy/git-changelog/commit/e0169654c917497ce88966fca1baf47d0a4586f7) by Pedro Brochado). [Issue #63](https://github.com/pawamoy/git-changelog/issues/63), [Issue #16](https://github.com/pawamoy/git-changelog/issues/16), [PR #64](https://github.com/pawamoy/git-changelog/pull/64), Co-authored-by: Timothée Mazzucotelli <pawamoy@pm.me>

### Bug Fixes

- Always output release notes to stdout ([1e44bca](https://github.com/pawamoy/git-changelog/commit/1e44bcaf82da9c5be4e853bf504fcd8faae06a3d) by Timothée Mazzucotelli). [Issue #65](https://github.com/pawamoy/git-changelog/issues/65)

## [2.3.2](https://github.com/pawamoy/git-changelog/releases/tag/2.3.2) - 2023-10-25

<small>[Compare with 2.3.1](https://github.com/pawamoy/git-changelog/compare/2.3.1...2.3.2)</small>

### Dependencies

- Use tomli instead of toml on Python less than 3.11 ([37f7cf1](https://github.com/pawamoy/git-changelog/commit/37f7cf1766944223e5ad2bc51fe7f48539aa1729) by Timothée Mazzucotelli).

## [2.3.1](https://github.com/pawamoy/git-changelog/releases/tag/2.3.1) - 2023-10-10

<small>[Compare with 2.3.0](https://github.com/pawamoy/git-changelog/compare/2.3.0...2.3.1)</small>

### Bug Fixes

- Remove any credentials from remote URLs, not just GitHub tokens ([5d07e91](https://github.com/pawamoy/git-changelog/commit/5d07e91c0ce1a8d21ace984ed1481f72da78b175) by Timothée Mazzucotelli). [Issue #61](https://github.com/pawamoy/git-changelog/issues/61)

## [2.3.0](https://github.com/pawamoy/git-changelog/releases/tag/2.3.0) - 2023-10-08

<small>[Compare with 2.2.0](https://github.com/pawamoy/git-changelog/compare/2.2.0...2.3.0)</small>

### Deprecations

- CLI argument `--bump-latest` and API parameter `bump_latest`
    are deprecated in favor of `--bump=auto` and `bump="auto"`
    argument and parameter, respectively.
    See ["Understand the relationship with SemVer"](usage.md#understand-the-relationship-with-semver).

### Features

- Add configuration files ([b527ccf](https://github.com/pawamoy/git-changelog/commit/b527ccf0939a1186254eb3b7003768c9594d0e63) by Oscar Esteban). [Issue #54](https://github.com/pawamoy/git-changelog/issues/54), [PR #55](https://github.com/pawamoy/git-changelog/pull/55), Co-authored-by: Timothée Mazzucotelli <pawamoy@pm.me>
- Add bump option (CLI, library) allowing to specify an exact version to bump to, as well as `auto`, `major`, `minor` or `patch` ([2c0dbb8](https://github.com/pawamoy/git-changelog/commit/2c0dbb84ab4dc7d24f301bbc8a1c25358eca5c36) by Théo Goudout). [Issue #38](https://github.com/pawamoy/git-changelog/issues/38), [PR #41](https://github.com/pawamoy/git-changelog/pull/41), Co-authored-by: Timothée Mazzucotelli <pawamoy@pm.me>
- Add provider CLI option ([908531b](https://github.com/pawamoy/git-changelog/commit/908531b514c92cc0a37b352330450fc070a28821) by Théo Goudout). [Issue #37](https://github.com/pawamoy/git-changelog/issues/37), [PR #40](https://github.com/pawamoy/git-changelog/pull/40), Co-authored-by: Timothée Mazzucotelli <pawamoy@pm.me>

## [2.2.0](https://github.com/pawamoy/git-changelog/releases/tag/2.2.0) - 2023-08-17

<small>[Compare with 2.1.0](https://github.com/pawamoy/git-changelog/compare/2.1.0...2.2.0)</small>

### Features

- Add option to omit empty versions from output ([b91f777](https://github.com/pawamoy/git-changelog/commit/b91f7775317feb79ebd2214c3e3c5e5251449d4d) by Sven Axelsson). [PR #52](https://github.com/pawamoy/git-changelog/pull/52)

### Code Refactoring

- Remove broken Atom commit convention ([2f33180](https://github.com/pawamoy/git-changelog/commit/2f331801134a2519a1d3704a02061b1f297e0f09) by Timothée Mazzucotelli).

## [2.1.0](https://github.com/pawamoy/git-changelog/releases/tag/2.1.0) - 2023-08-04

<small>[Compare with 2.0.0](https://github.com/pawamoy/git-changelog/compare/2.0.0...2.1.0)</small>

### Features

- Add Bitbucket provider ([5d793e5](https://github.com/pawamoy/git-changelog/commit/5d793e540be4fe5a648742c285c0762c111537ee) by Sven Axelsson).

### Code Refactoring

- Stop using deprecated `datetime.utcfromtimestamp` (Python 3.12) ([1f3ed5d](https://github.com/pawamoy/git-changelog/commit/1f3ed5da94e2a7c8938645977e6a7a0ffde7f713) by Sven Axelsson).

## [2.0.0](https://github.com/pawamoy/git-changelog/releases/tag/2.0.0) - 2023-07-03

<small>[Compare with 1.0.1](https://github.com/pawamoy/git-changelog/compare/1.0.1...2.0.0)</small>

### Breaking Changes

- Drop support for Python 3.7

### Features

- Add option to output release notes ([483745a](https://github.com/pawamoy/git-changelog/commit/483745a62078891682df6affd29e6cbfd7fdbe9e) by Timothée Mazzucotelli). [Issue #49](https://github.com/pawamoy/git-changelog/issues/49)

### Bug Fixes

- Remove GitHub tokens from remote URL ([187e26e](https://github.com/pawamoy/git-changelog/commit/187e26e8f1001c86d99689f5f15713a66d3f99ed) by Timothée Mazzucotelli). [Issue #50](https://github.com/pawamoy/git-changelog/issues/50)

### Code Refactoring

- Show default for every CLI option ([f015830](https://github.com/pawamoy/git-changelog/commit/f0158308a2196373c708b42271373f538ba6f53f) by Timothée Mazzucotelli).
- Remove Python 3.7 related code ([3295812](https://github.com/pawamoy/git-changelog/commit/32958129189e5c11573246f20e6900246da09997) by Timothée Mazzucotelli).

## [1.0.1](https://github.com/pawamoy/git-changelog/releases/tag/1.0.1) - 2023-05-10

<small>[Compare with 1.0.0](https://github.com/pawamoy/git-changelog/compare/1.0.0...1.0.1)</small>

### Bug Fixes

- Check if the latest version tag is already part of the changelog ([1fad8a8](https://github.com/pawamoy/git-changelog/commit/1fad8a82b2b6b79e6c989e0f236cc6d11d701ae6) by Kevin Squire).
- Include `v` prefix in default version regular expression ([a50d6a2](https://github.com/pawamoy/git-changelog/commit/a50d6a2b05ea699302b44705e994d84e30d6f489) by Kevin Squire).

## [1.0.0](https://github.com/pawamoy/git-changelog/releases/tag/1.0.0) - 2023-02-04

<small>[Compare with 0.6.0](https://github.com/pawamoy/git-changelog/compare/0.6.0...1.0.0)</small>

### Breaking changes

This version brings a lot of new features, so I took this opportunity
to break things, allowing to clean things up, and to bump to version 1.0.0.

- New version is not automatically guessed anymore (by bumping latest version).
    Enable it again with the `--bump-latest` CLI option.
- Provider-specific references are not parsed by default anymore.
    Parse them again with the `--parse-refs` CLI option.
- The commit convention cannot be passed with the `-s` CLI option anymore.
    This option is now used for declaring sections. Use `-c` instead.
    See [usage](https://pawamoy.github.io/git-changelog/usage/).
- Rename Python objects by replacing occurrences of "style" by "convention" everywhere.

### Features

Lots of new features! Usage is documented here: https://pawamoy.github.io/git-changelog/usage/.

- Support updating changelog in-place ([18029cd](https://github.com/pawamoy/git-changelog/commit/18029cd4982fd350d966bfd40dfda1c2a7c8ba78) by Timothée Mazzucotelli). [Issue #15](https://github.com/pawamoy/git-changelog/issues/15)
- Better handle single, initial versions ([4c6ecf5](https://github.com/pawamoy/git-changelog/commit/4c6ecf582d17b7efe1266f402adbeee8ce7dc0a4) by Timothée Mazzucotelli).
- Use current directory by default ([d50d0b1](https://github.com/pawamoy/git-changelog/commit/d50d0b18b2e7f3319542231b3882377c9850e373) by Timothée Mazzucotelli).
- Allow choosing whether to guess new version by bumping latest ([85c04fd](https://github.com/pawamoy/git-changelog/commit/85c04fd0e4eac883c032d3ef5c9c8d86035d1636) by Timothée Mazzucotelli).
- Support Git trailers, render them in Keep A Changelog template ([cdf17c0](https://github.com/pawamoy/git-changelog/commit/cdf17c0302d4beaf933e237e2d838a2b8546688d) by Timothée Mazzucotelli).
- Disable parsing of provider-specific references by default, allow enabling it ([cf41a97](https://github.com/pawamoy/git-changelog/commit/cf41a97d3aefabc3d97160e540417fa6d276b25f) by Timothée Mazzucotelli).

### Bug Fixes

- Clean up body to fix parsing trailers ([1183c25](https://github.com/pawamoy/git-changelog/commit/1183c259c9b16eea2043a930f7ff775e058c9733) by Timothée Mazzucotelli).
- Fix building commit body ([f76bf32](https://github.com/pawamoy/git-changelog/commit/f76bf3205ab4e696ec9907e95517817e6c04af70) by Timothée Mazzucotelli).
- Fix spacing in keepachangelog templates ([cf5117a](https://github.com/pawamoy/git-changelog/commit/cf5117a27fc28503a12bc133c5ed663628b02740) by Timothée Mazzucotelli).
- Don't crash when trying to parse the latest tag as semver ([e90aa2b](https://github.com/pawamoy/git-changelog/commit/e90aa2be1c94fa792f26b82e0db86b10924a8c83) by Timothée Mazzucotelli).
- Keep a Changelog template: don't capitalize commit summary ([87348ed](https://github.com/pawamoy/git-changelog/commit/87348ed1503b043d6bfae2e113c09f7c9c166501) by Timothée Mazzucotelli).
- Keep a Changelog template: respect sections order (don't sort) ([f645e62](https://github.com/pawamoy/git-changelog/commit/f645e62bf49ed61601ba095715f9098b6935ad2f) by Timothée Mazzucotelli).
- Use `importlib.metadata` instead of `pkg_resources` to get current version ([79109d0](https://github.com/pawamoy/git-changelog/commit/79109d0f4e55f821bb8c8299477c7d0693435445) by Timothée Mazzucotelli).

### Code Refactoring

- Allow passing sections with `-s` CLI option (removed from commit convention option) ([a1ae778](https://github.com/pawamoy/git-changelog/commit/a1ae778322d53ecd90ffd2e7e7a085482597855d) by Timothée Mazzucotelli).
- Rename 'style' to 'convention' everywhere ([c454481](https://github.com/pawamoy/git-changelog/commit/c4544816349cfa44644416abd1fa852ed861d779) by Timothée Mazzucotelli).
- Rename `inplace` variable to `in_place` ([7a271ef](https://github.com/pawamoy/git-changelog/commit/7a271ef7d2f889c852685fbba68e1738240c4df6) by Timothée Mazzucotelli).
- Refactor CLI: all flags default to false ([9616bdd](https://github.com/pawamoy/git-changelog/commit/9616bddcf154f2088f34e431f2887614c6a46960) by Timothée Mazzucotelli).
- Refactor CLI for better library usage ([43ec5d1](https://github.com/pawamoy/git-changelog/commit/43ec5d1ce4bbe4fe60d31948365609e5e2111045) by Timothée Mazzucotelli).
- Make changelog methods private ([0b4bbc0](https://github.com/pawamoy/git-changelog/commit/0b4bbc03292fadca4b22e3835718f7165c8e76e0) by Timothée Mazzucotelli).
- Expose `Changelog` and `Commit` from `git_changelog` ([d3dca05](https://github.com/pawamoy/git-changelog/commit/d3dca0582cb64ffe04f42cddfbca0a7e9a8e2fc3) by Timothée Mazzucotelli).
- Detect more commit types (Karma/Angular), rework section titles ([f751736](https://github.com/pawamoy/git-changelog/commit/f75173681bbdd22b7da1928f2e5369018bf56313) by Timothée Mazzucotelli).
- Allow passing datetimes, UTC timestamps as strings, or nothing when creating commit ([34460ab](https://github.com/pawamoy/git-changelog/commit/34460ab79b95754343874701d8287064b8280402) by Timothée Mazzucotelli).
- Build body before instantiating commit ([37de53f](https://github.com/pawamoy/git-changelog/commit/37de53f022a2cfd9f2b9a4f50e56bd1c0cb1c580) by Timothée Mazzucotelli).

## [0.6.0](https://github.com/pawamoy/git-changelog/releases/tag/0.6.0) - 2022-10-26

<small>[Compare with 0.5.0](https://github.com/pawamoy/git-changelog/compare/0.5.0...0.6.0)</small>

### Features

- Add GIT_CHANGELOG_REMOTE variable ([9b9b3fc](https://github.com/pawamoy/git-changelog/commit/9b9b3fc172be4909b47e2bf97d74e6ec68fab882) by Lukáš Zapletal). [PR #35](https://github.com/pawamoy/git-changelog/issues/35)

## [0.5.0](https://github.com/pawamoy/git-changelog/releases/tag/0.5.0) - 2021-11-14

<small>[Compare with 0.4.2](https://github.com/pawamoy/git-changelog/compare/0.4.2...0.5.0)</small>

### Dependencies

- Accept Jinja2 3.x ([9ef3259](https://github.com/pawamoy/git-changelog/commit/9ef3259bd9bce7a654c4e35c731619df37adaa21) by Timothée Mazzucotelli).

### Features

- Allow to choose conventional style from CLI ([aafa779](https://github.com/pawamoy/git-changelog/commit/aafa7793ec02af8b443576262af4e244901787dc) by Ivan Gonzalez). [PR #32](https://github.com/pawamoy/git-changelog/pull/32)
- Add ConventionalCommit commit type ([3becce8](https://github.com/pawamoy/git-changelog/commit/3becce8d344a3985905b0af916e9bcc426760426) by Kevin Squire). [PR #30](https://github.com/pawamoy/git-changelog/pull/30)

### Bug Fixes

- Properly bump semver version ([ecc7dd4](https://github.com/pawamoy/git-changelog/commit/ecc7dd430719c90b289acf7f29adb0b82e193fa8) by Kevin Squire). References: [#31](https://github.com/pawamoy/git-changelog/issues/31)
- Fix typo in keepachangelog template ([fa9b434](https://github.com/pawamoy/git-changelog/commit/fa9b4349c1a954a3029e5b35ac306a22fc08babe) by Alexander Schleifer). [PR #28](https://github.com/pawamoy/git-changelog/pull/28)

### Code Refactoring

- Use semver to bump version more reliably ([b68a565](https://github.com/pawamoy/git-changelog/commit/b68a565fce51f8d0e94f0f67c98dea30e421dd8f) by Timothée Mazzucotelli).

## [0.4.2](https://github.com/pawamoy/git-changelog/releases/tag/0.4.2) - 2021-01-06

<small>[Compare with 0.4.1](https://github.com/pawamoy/git-changelog/compare/0.4.1...0.4.2)</small>

### Bug Fixes

- Handle prerelease tags better ([4bcc451](https://github.com/pawamoy/git-changelog/commit/4bcc451059bf2e7763a4033b09894a438270b8db) by Timothée Mazzucotelli).

## [0.4.1](https://github.com/pawamoy/git-changelog/releases/tag/0.4.1) - 2020-12-21

<small>[Compare with 0.4.0](https://github.com/pawamoy/git-changelog/compare/0.4.0...0.4.1)</small>

### Bug Fixes

- Fix wrong version being printed ([0ec050f](https://github.com/pawamoy/git-changelog/commit/0ec050f513f8524dc3c65734fbda64c47c42fdbc) by Timothée Mazzucotelli).

## [0.4.0](https://github.com/pawamoy/git-changelog/releases/tag/0.4.0) - 2020-05-21

<small>[Compare with 0.3.0](https://github.com/pawamoy/git-changelog/compare/0.3.0...0.4.0)</small>

### Bug Fixes

- Use actual url for references ([46a8790](https://github.com/pawamoy/git-changelog/commit/46a87907eaa4bdf48c9c5e581cd0a9877145f262) by Timothée Mazzucotelli).
- Use style subject if possible ([7f2c3ad](https://github.com/pawamoy/git-changelog/commit/7f2c3ad43bd9c3cd22e725529b8178663d26e905) by Timothée Mazzucotelli).
- Correctly handle nested subgroups for gitlab repos ([8ca990b](https://github.com/pawamoy/git-changelog/commit/8ca990b8b3a49ca4d21efb30b9888efaa506eead) by Timothée Mazzucotelli).
- Fix bumping versions starting with "v" ([44e7644](https://github.com/pawamoy/git-changelog/commit/44e7644477b1cfe0c0aced748ce1c21af0cf8aca) by Timothée Mazzucotelli).

### Code Refactoring

- Move styles into new commit module to avoid cyclic dependencies ([d90bd15](https://github.com/pawamoy/git-changelog/commit/d90bd154ae13666ddca08682a1f2f0dae3e30852) by Timothée Mazzucotelli).

### Features

- Improve changelog rendering ([e9dd3f4](https://github.com/pawamoy/git-changelog/commit/e9dd3f42b3bc30816dafbfce39c489521d44f994) by Timothée Mazzucotelli).
    - Use today's date for current version
    - Move "compare" link below the heading (better table of contents in documentation)
    - Improve "compare" links to handle first and current version
    - Use selected commit types to render sections
- Add default commit types to render variable ([173392a](https://github.com/pawamoy/git-changelog/commit/173392a60a15ae888fe400ca94f35a37a9a90d85) by Timothée Mazzucotelli).
- Always use today's date for unreleased version ([1c34fa8](https://github.com/pawamoy/git-changelog/commit/1c34fa86ff3f875e63fa9f8390c6a8324e37e3d4) by Timothée Mazzucotelli).

## [0.3.0](https://github.com/pawamoy/git-changelog/releases/tag/0.3.0) - 2020-03-31

<small>[Compare with 0.2.0](https://github.com/pawamoy/git-changelog/compare/0.2.0...0.3.0)</small>

### Bug Fixes

- Fix `is_minor` method for version ([6d08978](https://github.com/pawamoy/git-changelog/commit/6d089785f692d4a21349c9eaa117641a481ba398) by Loïc Viennois).
- Fix `parse_refs` method for `ProviderRefParser` ([dc51589](https://github.com/pawamoy/git-changelog/commit/dc515898fef7dd47cde749c7dd690f607f5cf10c) by Loïc Viennois).
- Correctly detect major version, for both angular style and basic style ([7385e19](https://github.com/pawamoy/git-changelog/commit/7385e1952848e79a18a599119debf4bd75a2ecb7) by Loïc Viennois).

### Code Refactoring

- Add type hints to all classes and methods ([95276ef](https://github.com/pawamoy/git-changelog/commit/95276ef0b600575813ecaca30b582c2067f6439c) by Loïc Viennois).

### Features

- Update template `keepachangelog` ([ce76ed6](https://github.com/pawamoy/git-changelog/commit/ce76ed6bb8d92eb4b44513cf1cac9d34a5ef658f)) by RainChen:
    - Capitalize commit subject
    - Show author name for each commit
    - Sort commits by date
    - Unique commit subjects

## [0.2.0](https://github.com/pawamoy/git-changelog/releases/tag/0.2.0) - 2019-11-24

<small>[Compare with 0.1.1](https://github.com/pawamoy/git-changelog/compare/0.1.1...0.2.0)</small>

Drop support for Python < 3.6.

Use [poetry](https://github.com/sdispater/poetry) to manage the project!

### Fixed

- Fix detection of feature (is_minor) for angular style ([4fbf0ee](https://github.com/pawamoy/git-changelog/commit/4fbf0ee4ae582c1925e80b885bb4da42b69ecc09)).

## [0.1.1](https://github.com/pawamoy/git-changelog/tags/0.1.1) - 2018-06-27

<small>[Compare with 0.1.0](https://github.com/pawamoy/git-changelog/compare/0.1.0...0.1.1)</small>

### Fixed

- Fix build with MANIFEST.in, add license file ([013fb69](https://github.com/pawamoy/git-changelog/commit/013fb691826924d6f71b4159a8fa650e40324db3)).

### Misc

- Improve readability ([5e590f6](https://github.com/pawamoy/git-changelog/commit/5e590f6ac62b23e608a507e08123efba3b0f7e0d)).

## [0.1.0](https://github.com/pawamoy/git-changelog/tags/0.1.0) - 2018-06-27

<small>[Compare with first commit](https://github.com/pawamoy/git-changelog/compare/83845fe8d7deb85a2e093fe68a4b6a48b6d8e446...0.1.0)</small>


### Added
- Add github/github regexes ([584fd73](https://github.com/pawamoy/git-changelog/commit/584fd73ec88ac51abbf8555d8f78b7144529e6b3)).


### Fixed
- Fix patch bump ([8470e69](https://github.com/pawamoy/git-changelog/commit/8470e695128d9892296acdd31c404d85add68983)).
- Fix refs parsing ([8c77cb7](https://github.com/pawamoy/git-changelog/commit/8c77cb736971473837384a8238c3c53886d77c75)).

### Misc

- Continue packaging (#6) ([a29af2c](https://github.com/pawamoy/git-changelog/commit/a29af2cf990edf950b55a46ebea164ab068c9aec)).
- Finish packaging (#6) ([e92b492](https://github.com/pawamoy/git-changelog/commit/e92b4923a60d561c38150331dac9cd2e3ba6c130)).
- Implement reference parsing ([a9b4a89](https://github.com/pawamoy/git-changelog/commit/a9b4a89cd2737056166feb7a46da971549f1ffed)).
- Improve angular template, improve style/refs system ([5b87d48](https://github.com/pawamoy/git-changelog/commit/5b87d48acdf3aa0f5cc2731f48e372c4065d9f9b)).
- Initial commit ([83845fe](https://github.com/pawamoy/git-changelog/commit/83845fe8d7deb85a2e093fe68a4b6a48b6d8e446)).
- Package code (#6) ([1219eaf](https://github.com/pawamoy/git-changelog/commit/1219eafd02521f6f6ab942a02b7a7aee3d664143)).
- Update changelog for version 0.1.0 ([14edcaf](https://github.com/pawamoy/git-changelog/commit/14edcaf078d02c42abf1692664c620c509df88a0)).
- Update changelog for version 0.1.0 ([610633d](https://github.com/pawamoy/git-changelog/commit/610633da8a569e7f2966f1675a30aca651563e0b)).
- Update changelog for version 0.1.0 ([2eaaa2e](https://github.com/pawamoy/git-changelog/commit/2eaaa2e76fc35d111517ecd0a15daf65e705723c)).
- Work in progress ([27a60e8](https://github.com/pawamoy/git-changelog/commit/27a60e80e9a8308b88942311184346b1bfa4b0a8)).
