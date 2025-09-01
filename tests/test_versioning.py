"""Test version bumping."""

from __future__ import annotations

import pytest

from git_changelog._internal.versioning import (
    PEP440Strategy,
    PEP440Version,
    SemVerStrategy,
    bump_pep440,
    bump_semver,
    version_prefix,
)


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        ("1", ("1", "")),
        ("v1", ("1", "v")),
        ("va", ("a", "v")),
        ("x1", ("x1", "")),
    ],
)
def test_version_prefix(version: str, expected: tuple[str, str]) -> None:
    """Test splitting version and `v` prefix.

    Parameters:
        version: The version to split.
        bumped: The expected version and prefix.
    """
    assert expected == version_prefix(version)


@pytest.mark.parametrize(
    ("part", "version", "bumped"),
    [
        ("major", "0.0.1", "1.0.0"),
        ("major", "0.1.0", "1.0.0"),
        ("major", "0.1.1", "1.0.0"),
        ("major", "1.0.0", "2.0.0"),
        ("major", "1.0.1", "2.0.0"),
        ("major", "1.1.0", "2.0.0"),
        ("major", "1.1.1", "2.0.0"),
        ("minor", "0.0.1", "0.1.0"),
        ("minor", "0.1.0", "0.2.0"),
        ("minor", "0.1.1", "0.2.0"),
        ("minor", "1.0.0", "1.1.0"),
        ("minor", "1.0.1", "1.1.0"),
        ("minor", "1.1.0", "1.2.0"),
        ("minor", "1.1.1", "1.2.0"),
        ("patch", "0.0.1", "0.0.2"),
        ("patch", "0.1.0", "0.1.1"),
        ("patch", "0.1.1", "0.1.2"),
        ("patch", "1.0.0", "1.0.1"),
        ("patch", "1.0.1", "1.0.2"),
        ("patch", "1.1.0", "1.1.1"),
        ("patch", "1.1.1", "1.1.2"),
        ("release", "1.1.1", "1.1.1"),
        ("release", "1.1.1-alpha", "1.1.1"),
        ("release", "1.1.1-alpha+build", "1.1.1"),
    ],
)
def test_semver_bump_patch(part: SemVerStrategy, version: str, bumped: str) -> None:
    """Test default and patch version bumping.

    Parameters:
        part: The version part to bump.
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump_semver(version, part, zerover=False) == bumped


@pytest.mark.parametrize(
    ("version", "bumped"),
    [
        ("0.0.1", "0.1.0"),
        ("0.1.0", "0.2.0"),
        ("0.1.1", "0.2.0"),
        ("1.0.0", "2.0.0"),
        ("1.0.1", "2.0.0"),
        ("1.1.0", "2.0.0"),
        ("1.1.1", "2.0.0"),
    ],
)
def test_semver_bump_major_zerover(version: str, bumped: str) -> None:
    """Test major version bumping with zerover.

    Parameters:
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump_semver(version, "major", zerover=True) == bumped


def test_semver_bump_unknown_part() -> None:
    """Bump unknown part of a SemVer version."""
    with pytest.raises(ValueError, match="Invalid strategy unknown"):
        bump_semver("1.0.0", "unknown")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("part", "version", "bumped"),
    [
        ("epoch", "0!1.0", "1!1.0"),
        ("epoch", "1!1.0", "2!1.0"),
        ("epoch", "2!1.0a0.dev1", "3!1.0"),
        ("release", "1.0a0", "1.0"),
        ("release", "1.0.1b1", "1.0.1"),
        ("release", "2.1rc2", "2.1"),
        ("release", "1.dev0", "1"),
        ("major", "0.0.1", "1.0.0"),
        ("major", "0.1.0", "1.0.0"),
        ("major", "0.1.1", "1.0.0"),
        ("major", "1.0.0", "2.0.0"),
        ("major", "1.0.1", "2.0.0"),
        ("major", "1.1.0", "2.0.0"),
        ("major", "1.1.1", "2.0.0"),
        ("major", "1", "2"),
        ("major", "1.1", "2.0"),
        ("major", "1.1.1.1", "2.0.0.0"),
        ("major", "1a2.post3", "2"),
        ("minor", "0.0.1", "0.1.0"),
        ("minor", "0.1.0", "0.2.0"),
        ("minor", "0.1.1", "0.2.0"),
        ("minor", "1.0.0", "1.1.0"),
        ("minor", "1.0.1", "1.1.0"),
        ("minor", "1.1.0", "1.2.0"),
        ("minor", "1.1.1", "1.2.0"),
        ("minor", "1", "1.1"),
        ("minor", "1.1", "1.2"),
        ("minor", "1.1.1.1", "1.2.0.0"),
        ("minor", "1a2.post3", "1.1"),
        ("micro", "0.0.1", "0.0.2"),
        ("micro", "0.1.0", "0.1.1"),
        ("micro", "0.1.1", "0.1.2"),
        ("micro", "1.0.0", "1.0.1"),
        ("micro", "1.0.1", "1.0.2"),
        ("micro", "1.1.0", "1.1.1"),
        ("micro", "1.1.1", "1.1.2"),
        ("micro", "1", "1.0.1"),
        ("micro", "1.1", "1.1.1"),
        ("micro", "1.1.1.1", "1.1.2.0"),
        ("micro", "1a2.post3", "1.0.1"),
        ("pre", "1a0", "1a1"),
        ("pre", "1b1", "1b2"),
        ("pre", "1c2", "1rc3"),
        ("pre", "1.0a2.post3", "1.0a3"),
        ("alpha", "1a0", "1a1"),
        ("alpha", "1.1a99", "1.1a100"),
        ("beta", "1a0", "1b0"),
        ("beta", "1.1a99", "1.1b0"),
        ("beta", "1b0", "1b1"),
        ("beta", "1.1b1", "1.1b2"),
        ("candidate", "1a0", "1rc0"),
        ("candidate", "1.1a99", "1.1rc0"),
        ("candidate", "1b0", "1rc0"),
        ("candidate", "1.1b1", "1.1rc0"),
        ("candidate", "1c0", "1rc1"),
        ("candidate", "1.1rc1", "1.1rc2"),
        ("post", "1", "1.post0"),
        ("post", "1.post0", "1.post1"),
        ("post", "1.0a2.post3", "1.0a2.post4"),
        ("dev", "1.dev0", "1.dev1"),
        ("dev", "1.post0.dev1", "1.post0.dev2"),
        ("dev", "1.0a2.post3.dev2", "1.0a2.post3.dev3"),
        ("major+alpha", "1", "2a0"),
        ("major+alpha", "1a0", "2a0"),
        ("major+alpha", "1b0.dev0", "2a0"),
        ("major+beta", "1", "2b0"),
        ("major+beta", "1a0", "2b0"),
        ("major+candidate", "1", "2rc0"),
        ("major+candidate", "1a0", "2rc0"),
        ("major+dev", "1", "2.dev0"),
        ("major+dev", "1a0.post0", "2.dev0"),
        ("major+alpha+dev", "1", "2a0.dev0"),
        ("major+alpha+dev", "1a1.dev1", "2a0.dev0"),
        ("major+beta+dev", "1", "2b0.dev0"),
        ("major+beta+dev", "1a1.dev1", "2b0.dev0"),
        ("major+candidate+dev", "1", "2rc0.dev0"),
        ("major+candidate+dev", "1a1.dev1", "2rc0.dev0"),
        ("minor+alpha", "1", "1.1a0"),
        ("minor+alpha", "1a0", "1.1a0"),
        ("minor+alpha", "1b0.dev0", "1.1a0"),
        ("minor+beta", "1", "1.1b0"),
        ("minor+beta", "1a0", "1.1b0"),
        ("minor+candidate", "1", "1.1rc0"),
        ("minor+candidate", "1a0", "1.1rc0"),
        ("minor+dev", "1", "1.1.dev0"),
        ("minor+dev", "1a0.post0", "1.1.dev0"),
        ("minor+alpha+dev", "1", "1.1a0.dev0"),
        ("minor+alpha+dev", "1a1.dev1", "1.1a0.dev0"),
        ("minor+beta+dev", "1", "1.1b0.dev0"),
        ("minor+beta+dev", "1a1.dev1", "1.1b0.dev0"),
        ("minor+candidate+dev", "1", "1.1rc0.dev0"),
        ("minor+candidate+dev", "1a1.dev1", "1.1rc0.dev0"),
        ("micro+alpha", "1", "1.0.1a0"),
        ("micro+alpha", "1a0", "1.0.1a0"),
        ("micro+alpha", "1b0.dev0", "1.0.1a0"),
        ("micro+beta", "1", "1.0.1b0"),
        ("micro+beta", "1a0", "1.0.1b0"),
        ("micro+candidate", "1", "1.0.1rc0"),
        ("micro+candidate", "1a0", "1.0.1rc0"),
        ("micro+dev", "1", "1.0.1.dev0"),
        ("micro+dev", "1a0.post0", "1.0.1.dev0"),
        ("micro+alpha+dev", "1", "1.0.1a0.dev0"),
        ("micro+alpha+dev", "1a1.dev1", "1.0.1a0.dev0"),
        ("micro+beta+dev", "1", "1.0.1b0.dev0"),
        ("micro+beta+dev", "1a1.dev1", "1.0.1b0.dev0"),
        ("micro+candidate+dev", "1", "1.0.1rc0.dev0"),
        ("micro+candidate+dev", "1a1.dev1", "1.0.1rc0.dev0"),
        ("alpha+dev", "1a0", "1a1.dev0"),
        ("beta+dev", "1a0", "1b0.dev0"),
        ("beta+dev", "1b0", "1b1.dev0"),
        ("candidate+dev", "1a0", "1rc0.dev0"),
        ("candidate+dev", "1b0", "1rc0.dev0"),
        ("candidate+dev", "1rc0", "1rc1.dev0"),
    ],
)
def test_pep440_bump(part: PEP440Strategy, version: str, bumped: str) -> None:
    """Test PEP 440 version bumping.

    Parameters:
        part: The version part to bump.
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump_pep440(version, part, zerover=False) == bumped


@pytest.mark.parametrize(
    ("version", "bumped"),
    [
        ("0.0.1", "0.1.0"),
        ("0.1.0", "0.2.0"),
        ("0.1.1", "0.2.0"),
        ("1.0.0", "2.0.0"),
        ("1.0.1", "2.0.0"),
        ("1.1.0", "2.0.0"),
        ("1.1.1", "2.0.0"),
        ("1", "2"),
        ("1.1", "2.0"),
        ("1a2.post3", "2"),
    ],
)
def test_pep440_bump_major_zerover(version: str, bumped: str) -> None:
    """Test major version bumping with zerover.

    Parameters:
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump_pep440(version, "major", zerover=True) == bumped


@pytest.mark.parametrize(
    ("part", "version"),
    [
        ("pre", "1"),
        ("pre", "1.0"),
        ("pre", "1.0.post0"),
        ("pre", "1.0.dev0"),
        ("release", "1.post0"),
        ("release", "1.post0.dev0"),
        ("alpha", "1b0"),
        ("alpha", "1rc0"),
        ("beta", "1rc0"),
        ("dev", "1"),
        ("dev", "1a0"),
        ("dev", "1.post0"),
    ],
)
def test_pep440_bump_error(part: PEP440Strategy, version: str) -> None:
    """Test bumping errors.

    Parameters:
        part: The version part to bump.
        version: The base version.
    """
    with pytest.raises(ValueError, match="Cannot bump"):
        bump_pep440(version, part)


def test_pep440_bump_unknown_part() -> None:
    """Bump unknown part of a PEP 440 version."""
    with pytest.raises(ValueError, match="Invalid strategy unknown"):
        bump_pep440("1", "unknown")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("part", "version", "bumped"),
    [
        ("release", "1.0", "1"),
        ("release", "1.0a0", "1"),
        ("major", "1.0", "2"),
        ("major", "1.0a0", "2"),
        ("minor", "1.0", "1.1"),
        ("minor", "1.0.0a0", "1.1"),
        ("micro", "1.0.0.0", "1.0.1"),
        ("micro", "1.0.0.0a0", "1.0.1"),
    ],
)
def test_pep440_bump_trim(part: PEP440Strategy, version: str, bumped: str) -> None:
    """Test PEP 440 version bumping and trimming.

    Parameters:
        part: The version part to bump.
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump_pep440(version, part, trim=True) == bumped


@pytest.mark.parametrize(
    ("part", "version", "dented"),
    [
        ("pre", "1", "1a0"),
        ("pre", "1.0", "1.0a0"),
        ("alpha", "1", "1a0"),
        ("alpha", "1.0", "1.0a0"),
        ("beta", "1", "1b0"),
        ("beta", "1.0", "1.0b0"),
        ("candidate", "1", "1rc0"),
        ("candidate", "1.0", "1.0rc0"),
        ("dev", "1", "1.dev0"),
        ("dev", "1.0", "1.0.dev0"),
    ],
)
def test_pep440_dent(part: PEP440Strategy, version: str, dented: str) -> None:
    """Test denting versions.

    Parameters:
        part: The version part to dent.
        version: The base version.
        dented: The expected, dented version.
    """
    assert str(getattr(PEP440Version(version), f"dent_{part}")()) == dented


@pytest.mark.parametrize(
    ("part", "version"),
    [
        ("pre", "1a0"),
        ("pre", "1b0"),
        ("pre", "1rc0"),
        ("alpha", "1a0"),
        ("alpha", "1b0"),
        ("alpha", "1rc0"),
        ("beta", "1a0"),
        ("beta", "1b0"),
        ("beta", "1rc0"),
        ("candidate", "1a0"),
        ("candidate", "1b0"),
        ("candidate", "1rc0"),
        ("dev", "1.dev0"),
    ],
)
def test_pep440_dent_error(part: PEP440Strategy, version: str) -> None:
    """Test denting errors.

    Parameters:
        part: The version part to bump.
        version: The base version.
    """
    with pytest.raises(ValueError, match="Cannot dent"):
        getattr(PEP440Version(version), f"dent_{part}")()
