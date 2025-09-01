# Utilities to handle different versioning schemes such as SemVer and PEP 440.

from __future__ import annotations

from typing import Any, Literal, Protocol

import semver
from packaging import version as packaging_version

SemVerStrategy = Literal[
    "major",
    "minor",
    "patch",
    "release",
]
"""SemVer versioning strategies."""
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
"""PEP 440 versioning strategies."""


_release_kind = {"a": "alpha", "b": "beta", "c": "candidate", "rc": "candidate", "p": "post"}


class ParsedVersion(Protocol):  # noqa: PLW1641
    """Base class for versioning schemes."""

    def __lt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...


class SemVerVersion(semver.Version, ParsedVersion):  # type: ignore[misc]
    """SemVer version."""

    def bump_major(self) -> SemVerVersion:
        return SemVerVersion(*super().bump_major())  # type: ignore[misc]

    def bump_minor(self) -> SemVerVersion:
        return SemVerVersion(*super().bump_minor())  # type: ignore[misc]

    def bump_patch(self) -> SemVerVersion:
        return SemVerVersion(*super().bump_patch())  # type: ignore[misc]

    def bump_release(self) -> SemVerVersion:
        """Bump from a pre-release to the same, regular release.

        Returns:
            The same version, without pre-release or build metadata.
        """
        return SemVerVersion(self.major, self.minor, self.patch)


class PEP440Version(packaging_version.Version, ParsedVersion):  # type: ignore[misc]
    """PEP 440 version."""

    @classmethod
    def from_parts(
        cls,
        epoch: int | None = None,
        release: tuple[int, ...] | None = None,
        pre: tuple[str, int] | None = None,
        post: int | None = None,
        dev: int | None = None,
    ) -> PEP440Version:
        """Build a version from its parts.

        Parameters:
            epoch: Version's epoch number.
            release: Version's release numbers.
            pre: Version's prerelease kind and number.
            post: Version's post number.
            dev: Version's dev number.

        Returns:
            A PEP 440 version.
        """
        # Since the original class only allows instantiating a version
        # by passing a string, we first create a dummy version "1"
        # and then re-assign its internal `_version` with the real one.
        version = cls("1")
        version._version = packaging_version._Version(
            epoch=epoch or 0,
            release=release or (),
            pre=pre,
            post=None if post is None else ("post", post),
            dev=None if dev is None else ("dev", dev),
            local=None,
        )

        # We also have to update its `_key` attribute.
        # This is a hack and I would prefer that such functionality
        # is exposed directly in the original class.
        version._key = packaging_version._cmpkey(
            version._version.epoch,
            version._version.release,
            version._version.pre,
            version._version.post,
            version._version.dev,
            version._version.local,
        )

        return version

    def bump_epoch(self) -> PEP440Version:
        """Bump epoch.

        Examples:
            >>> PEP440Version("1.0").bump_epoch()
            <Version('1!1.0')>
            >>> PEP440Version("0!1.0").bump_epoch()
            <Version('1!1.0')>
            >>> PEP440Version("1!1.0").bump_epoch()
            <Version('2!1.0')>
            >>> PEP440Version("1.0a2.post3").bump_epoch()
            <Version('2!1.0')>

        Returns:
            Version with bumped epoch, same release, and the right parts reset to 0 or nothing.
        """
        return PEP440Version.from_parts(epoch=self.epoch + 1, release=self.release)

    def bump_release(self, level: int | None = None, *, trim: bool = False) -> PEP440Version:
        """Bump given release level.

        Parameters:
            level: The release level to bump.

                - 0 means major
                - 1 means minor
                - 2 means micro (patch)
                - 3+ don't have names
                - None means move from pre-release to release (unchanged)
            trim: Whether to trim all zeroes on the right after bumping.

        Examples:
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

        Returns:
            Version with same epoch, bumped release level, and the right parts reset to 0 or nothing.
        """
        release = list(self.release)

        # When level is not specified, user wants to bump the version
        # as a "release", going out of alpha/beta/candidate phase.
        # So we simply keep the release part as it is, optionally trimming it.
        if level is None:
            # However if this is a post-release, this is an error:
            # we can't bump from a post-release to the same, regular release.
            if self.post is not None:
                raise ValueError("Cannot bump from post-release to release")
            if trim:
                while release[-1] == 0:
                    release.pop()

        # When level is specified, we bump the specified level.
        # If the given level is higher that the number of release parts,
        # we insert the missing parts as 0.
        else:
            try:
                release[level] += 1
            except IndexError:
                while len(release) < level:
                    release.append(0)
                release.append(1)
            if trim:
                release = release[: level + 1]
            else:
                for index in range(level + 1, len(release)):
                    release[index] = 0

        # We rebuild the version with same epoch, updated release,
        # and pre/post/dev parts dropped.
        return PEP440Version.from_parts(epoch=self.epoch, release=tuple(release))

    def bump_major(self, *, trim: bool = False) -> PEP440Version:
        """Bump major.

        Parameters:
            trim: Whether to trim all zeroes on the right after bumping.

        Examples:
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

        Returns:
            Version with same epoch, bumped major and the right parts reset to 0 or nothing.
        """
        return self.bump_release(level=0, trim=trim)

    def bump_minor(self, *, trim: bool = False) -> PEP440Version:
        """Bump minor.

        Parameters:
            trim: Whether to trim all zeroes on the right after bumping.

        Examples:
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

        Returns:
            Version with same epoch, same major, bumped minor and the right parts reset to 0 or nothing.
        """
        return self.bump_release(level=1, trim=trim)

    def bump_micro(self, *, trim: bool = False) -> PEP440Version:
        """Bump micro.

        Parameters:
            trim: Whether to trim all zeroes on the right after bumping.

        Examples:
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

        Returns:
            Version with same epoch, same major, same minor, bumped micro and the right parts reset to 0 or nothing.
        """
        return self.bump_release(level=2, trim=trim)

    def bump_pre(self, pre: Literal["a", "b", "c", "rc"] | None = None) -> PEP440Version:
        """Bump pre-release.

        Parameters:
            pre: Kind of pre-release to bump.

                - a means alpha
                - b means beta
                - c or rc means (release) candidate

        Examples:
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

            >>> PEP440Version("1").bump_pre("b")
            ValueError: Cannot bump from release to beta pre-release (use `dent_beta`)
            >>> PEP440Version("1a2").bump_pre("b")
            <Version('1b0')>
            >>> PEP440Version("1b2").bump_pre("b")
            <Version('1b3')>
            >>> PEP440Version("1c2").bump_pre("b")
            ValueError: Cannot bump from candidate to beta pre-release (use `dent_beta`)

            >>> PEP440Version("1").bump_pre("c")
            ValueError: Cannot bump from release to candidate pre-release (use `dent_candidate`)
            >>> PEP440Version("1a2").bump_pre("c")
            <Version('1rc0')>
            >>> PEP440Version("1b2").bump_pre("rc")
            <Version('1rc0')>
            >>> PEP440Version("1rc2").bump_pre("c")
            <Version('1rc3')>

        Returns:
            Version with same epoch, same release, bumped pre-release and the right parts reset to 0 or nothing.
        """
        if self.pre is None:
            kind = _release_kind.get(pre, "")  # type: ignore[arg-type]
            raise ValueError(
                f"Cannot bump from release to {kind + ' ' if kind else ''}pre-release (use `dent_{kind or 'pre'}`)",
            )
        current_pre: Literal["a", "b", "c", "rc"]
        current_pre, number = self.pre  # type: ignore[assignment]
        if pre is None:
            pre = current_pre
        if pre == current_pre:
            number += 1
        elif current_pre < pre:
            number = 0
        else:
            raise ValueError(
                f"Cannot bump from {_release_kind.get(current_pre, 'release')} to {_release_kind[pre]} pre-release (use `dent_{_release_kind[pre]}`)",
            )
        return PEP440Version.from_parts(epoch=self.epoch, release=self.release, pre=(pre, number))

    def bump_alpha(self) -> PEP440Version:
        """Bump alpha-release.

        Examples:
            >>> PEP440Version("1").bump_alpha()
            ValueError: Cannot bump from release to alpha pre-release (use `dent_alpha`)
            >>> PEP440Version("1a0").bump_alpha()
            <Version('1a1')>
            >>> PEP440Version("1a0").bump_alpha("a")
            <Version('1a1')>
            >>> PEP440Version("1a0.post0").bump_alpha()
            <Version('1a1')>

        Returns:
            Version with same epoch, same release, bumped alpha pre-release and the right parts reset to 0 or nothing.
        """
        return self.bump_pre("a")

    def bump_beta(self) -> PEP440Version:
        """Bump beta-release.

        Examples:
            >>> PEP440Version("1").bump_beta()
            ValueError: Cannot bump from release to beta pre-release (use `dent_beta`)
            >>> PEP440Version("1b0").bump_beta()
            <Version('1b1')>
            >>> PEP440Version("1b0").bump_beta()
            <Version('1b1')>
            >>> PEP440Version("1b0.post0").bump_beta()
            <Version('1b1')>

        Returns:
            Version with same epoch, same release, bumped beta pre-release and the right parts reset to 0 or nothing.
        """
        return self.bump_pre("b")

    def bump_candidate(self) -> PEP440Version:
        """Bump candidate release.

        Examples:
            >>> PEP440Version("1").bump_candidate()
            ValueError: Cannot bump from release to candidate pre-release (use `dent_candidate`)
            >>> PEP440Version("1c0").bump_candidate()
            <Version('1rc1')>
            >>> PEP440Version("1c0").bump_candidate()
            <Version('1rc1')>
            >>> PEP440Version("1c0.post0").bump_candidate()
            <Version('1rc1')>

        Returns:
            Version with same epoch, same release, bumped candidate pre-release and the right parts reset to 0 or nothing.
        """
        return self.bump_pre("rc")

    def bump_post(self) -> PEP440Version:
        """Bump post-release.

        Examples:
            >>> PEP440Version("1").bump_post()
            <Version('1.post0')>
            >>> PEP440Version("1.post0").bump_post()
            <Version('1.post1')>
            >>> PEP440Version("1a0.post0").bump_post()
            <Version('1a0.post1')>
            >>> PEP440Version("1.post0.dev1").bump_post()
            <Version('1.post1')>

        Returns:
            Version with same epoch, same release, same pre-release, bumped post-release and the right parts reset to 0 or nothing.
        """
        post = 0 if self.post is None else self.post + 1
        return PEP440Version.from_parts(epoch=self.epoch, release=self.release, pre=self.pre, post=post)

    def bump_dev(self) -> PEP440Version:
        """Bump dev-release.

        Examples:
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

        Returns:
            Version with same epoch, same release, same pre-release, same post-release and bumped dev-release.
        """
        if self.dev is None:
            if self.post is not None:
                kind = "p"
            elif self.pre is not None:
                kind = self.pre[0]
            else:
                kind = "z"
            raise ValueError(f"Cannot bump from {_release_kind.get(kind, 'release')} to dev-release (use `dent_dev`)")
        return PEP440Version.from_parts(
            epoch=self.epoch,
            release=self.release,
            pre=self.pre,
            post=self.post,
            dev=self.dev + 1,
        )

    def dent_pre(self, pre: Literal["a", "b", "c", "rc"] | None = None) -> PEP440Version:
        """Dent to pre-release.

        This method dents a release down to an alpha, beta or candidate pre-release.

        Parameters:
            pre: Kind of pre-release to bump.

                - a means alpha
                - b means beta
                - c or rc means (release) candidate

        Examples:
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

        Returns:
            Version with same epoch and release dented to pre-release.
        """
        if self.pre is not None:
            raise ValueError(f"Cannot dent {_release_kind[self.pre[0]]} pre-releases")
        if pre is None:
            pre = "a"
        return PEP440Version.from_parts(epoch=self.epoch, release=self.release, pre=(pre, 0))

    def dent_alpha(self) -> PEP440Version:
        """Dent to alpha-release.

        Examples:
            >>> PEP440Version("1").dent_alpha()
            <Version('1a0')>
            >>> PEP440Version("1a0").dent_alpha()
            ValueError: Cannot dent alpha pre-releases
            >>> PEP440Version("1b0").dent_alpha()
            ValueError: Cannot dent beta pre-releases
            >>> PEP440Version("1rc0").dent_alpha()
            ValueError: Cannot dent candidate pre-releases

        Returns:
            Version with same epoch and release dented to alpha pre-release.
        """
        return self.dent_pre("a")

    def dent_beta(self) -> PEP440Version:
        """Dent to beta-release.

        Examples:
            >>> PEP440Version("1").dent_beta()
            <Version('1b0')>
            >>> PEP440Version("1a0").dent_beta()
            ValueError: Cannot dent alpha pre-releases
            >>> PEP440Version("1b0").dent_beta()
            ValueError: Cannot dent beta pre-releases
            >>> PEP440Version("1rc0").dent_beta()
            ValueError: Cannot dent candidate pre-releases

        Returns:
            Version with same epoch and release dented to beta pre-release.
        """
        return self.dent_pre("b")

    def dent_candidate(self) -> PEP440Version:
        """Dent to candidate release.

        Examples:
            >>> PEP440Version("1").dent_candidate()
            <Version('1rc0')>
            >>> PEP440Version("1a0").dent_candidate()
            ValueError: Cannot dent alpha pre-releases
            >>> PEP440Version("1b0").dent_candidate()
            ValueError: Cannot dent beta pre-releases
            >>> PEP440Version("1rc0").dent_candidate()
            ValueError: Cannot dent candidate pre-releases

        Returns:
            Version with same epoch and release dented to candidate pre-release.
        """
        return self.dent_pre("rc")

    def dent_dev(self) -> PEP440Version:
        """Dent to dev-release.

        Examples:
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

        Returns:
            Version with same epoch and release dented to dev-release.
        """
        if self.dev is not None:
            raise ValueError("Cannot dent dev-releases")
        return PEP440Version.from_parts(epoch=self.epoch, release=self.release, pre=self.pre, post=self.post, dev=0)


def version_prefix(version: str) -> tuple[str, str]:
    """Return a version and its optional `v` prefix.

    Arguments:
        version: The full version.

    Returns:
        version: The version without its prefix.
        prefix: The version prefix.
    """
    prefix = ""
    if version[0] == "v":
        prefix = "v"
        version = version[1:]
    return version, prefix


def parse_semver(version: str) -> tuple[SemVerVersion, str]:
    """Parse a SemVer version.

    Returns:
        A semver version instance with useful methods.
    """
    version, prefix = version_prefix(version)
    return SemVerVersion.parse(version), prefix


def parse_pep440(version: str) -> tuple[PEP440Version, str]:
    """Parse a PEP version.

    Returns:
        A PEP 440 version instance with useful methods.
    """
    version, prefix = version_prefix(version)
    return PEP440Version(version), prefix


class VersionBumper:
    """Base class for version bumpers."""

    initial: str

    def __init__(self, strategies: tuple[str, ...]) -> None:
        """Initialize the bumper.

        Parameters:
            strategies: The supported bumping strategies.
        """
        self.strategies = strategies

    def __call__(self, version: str, strategy: str = ..., **kwargs: Any) -> str:
        """Bump a version.

        Parameters:
            version: The version to bump.
            strategy: The bumping strategy.
            **kwargs: Additional bumper-specific arguments.

        Returns:
            The bumped version.
        """
        raise NotImplementedError


class PEP440Bumper(VersionBumper):
    """PEP 440 version bumper."""

    initial: str = "0.0.0"

    def __call__(  # type: ignore[override]
        self,
        version: str,
        strategy: PEP440Strategy = "micro",
        *,
        zerover: bool = False,
        trim: bool = False,
    ) -> str:
        """Bump a PEP 440 version.

        Arguments:
            version: The version to bump.
            strategy: The part of the version to bump.
            zerover: Keep major version at zero, even for breaking changes.
            trim: Whether to trim all zeroes on the right after bumping.

        Returns:
            The bumped version.
        """
        pep440_version, prefix = parse_pep440(version)

        # Split into main part and pre/dev markers
        # (+alpha, +beta, +candidate, +dev).
        main_part, *predev = strategy.split("+")

        # Bump main part.
        if main_part == "epoch":
            pep440_version = pep440_version.bump_epoch()
        elif main_part == "release":
            pep440_version = pep440_version.bump_release(trim=trim)
        elif main_part == "major":
            # If major version is 0 and zerover is active, only bump minor.
            if pep440_version.major == 0 and zerover:
                pep440_version = pep440_version.bump_minor(trim=trim)
            else:
                pep440_version = pep440_version.bump_major(trim=trim)
        elif main_part == "minor":
            pep440_version = pep440_version.bump_minor(trim=trim)
        elif main_part in ("micro", "patch"):
            pep440_version = pep440_version.bump_micro(trim=trim)
        elif main_part == "pre":
            pep440_version = pep440_version.bump_pre()
        elif main_part == "alpha":
            pep440_version = pep440_version.bump_alpha()
        elif main_part == "beta":
            pep440_version = pep440_version.bump_beta()
        elif main_part == "candidate":
            pep440_version = pep440_version.bump_candidate()
        elif main_part == "post":
            pep440_version = pep440_version.bump_post()
        elif main_part == "dev":
            pep440_version = pep440_version.bump_dev()
        else:
            raise ValueError(f"Invalid strategy {main_part}, use one of {', '.join(self.strategies)}")

        # Dent to pre-release (+alpha, +beta, +candidate).
        if "alpha" in predev:
            pep440_version = pep440_version.dent_alpha()
        elif "beta" in predev:
            pep440_version = pep440_version.dent_beta()
        elif "candidate" in predev:
            pep440_version = pep440_version.dent_candidate()

        # Dent to dev-release (+dev).
        if "dev" in predev:
            pep440_version = pep440_version.dent_dev()

        # Return new version with preserved prefix.
        return prefix + str(pep440_version)


class SemVerBumper(VersionBumper):
    """SemVer version bumper."""

    initial: str = "0.0.0"

    def __call__(  # type: ignore[override]
        self,
        version: str,
        strategy: SemVerStrategy = "patch",
        *,
        zerover: bool = True,
    ) -> str:
        """Bump a SemVer version.

        Arguments:
            version: The version to bump.
            part: The part of the version to bump.
            zerover: Keep major version at zero, even for breaking changes.

        Returns:
            The bumped version.
        """
        semver_version, prefix = parse_semver(version)
        if strategy == "major":
            if semver_version.major == 0 and zerover:
                semver_version = semver_version.bump_minor()
            else:
                semver_version = semver_version.bump_major()
        elif strategy == "minor":
            semver_version = semver_version.bump_minor()
        elif strategy == "patch":
            semver_version = semver_version.bump_patch()
        elif strategy == "release":
            semver_version = semver_version.bump_release()
        else:
            raise ValueError(f"Invalid strategy {strategy}, use one of {', '.join(self.strategies)}")
        return prefix + str(semver_version)


bump_pep440 = PEP440Bumper(PEP440Strategy.__args__)  # type: ignore[attr-defined]
"""Bump a PEP 440 version."""
bump_semver = SemVerBumper(SemVerStrategy.__args__)  # type: ignore[attr-defined]
"""Bump a SemVer version."""
