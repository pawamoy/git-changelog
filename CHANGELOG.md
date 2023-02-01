# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.7.0](https://github.com/pawamoy/git-changelog/releases/tag/0.7.0) - 2023-02-02

<small>[Compare with 0.6.0](https://github.com/pawamoy/git-changelog/compare/0.6.0...0.7.0)</small>

### Features

- Support Git trailers, render them in Keep A Changelog template ([cdf17c0](https://github.com/pawamoy/git-changelog/commit/cdf17c0302d4beaf933e237e2d838a2b8546688d) by Timothée Mazzucotelli).
- Allow disabling parsing of provider-specific references ([cf41a97](https://github.com/pawamoy/git-changelog/commit/cf41a97d3aefabc3d97160e540417fa6d276b25f) by Timothée Mazzucotelli).

### Bug Fixes

- Fix spacing in keepachangelog templates ([cf5117a](https://github.com/pawamoy/git-changelog/commit/cf5117a27fc28503a12bc133c5ed663628b02740) by Timothée Mazzucotelli).
- Don't crash when trying to parse the latest tag as semver ([e90aa2b](https://github.com/pawamoy/git-changelog/commit/e90aa2be1c94fa792f26b82e0db86b10924a8c83) by Timothée Mazzucotelli).
- Keep a Changelog template: don't capitalize commit summary ([87348ed](https://github.com/pawamoy/git-changelog/commit/87348ed1503b043d6bfae2e113c09f7c9c166501) by Timothée Mazzucotelli).
- Keep a Changelog template: respect sections order (don't sort) ([f645e62](https://github.com/pawamoy/git-changelog/commit/f645e62bf49ed61601ba095715f9098b6935ad2f) by Timothée Mazzucotelli).
- Use `importlib.metadata` instead of `pkg_resources` to get current version ([79109d0](https://github.com/pawamoy/git-changelog/commit/79109d0f4e55f821bb8c8299477c7d0693435445) by Timothée Mazzucotelli).

### Code Refactoring

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
