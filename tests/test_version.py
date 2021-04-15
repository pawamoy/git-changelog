"""Test version bumping."""

from git_changelog.build import bump


def test_bump():  # noqa: WPS218 (too many assert statements)
    """Test default version bumping."""
    assert bump("0.0.1") == "0.0.2"
    assert bump("0.1.0") == "0.1.1"
    assert bump("0.1.1") == "0.1.2"
    assert bump("1.0.0") == "1.0.1"
    assert bump("1.0.1") == "1.0.2"
    assert bump("1.1.0") == "1.1.1"
    assert bump("1.1.1") == "1.1.2"

    assert bump("v0.0.1") == "v0.0.2"
    assert bump("v0.1.0") == "v0.1.1"
    assert bump("v0.1.1") == "v0.1.2"
    assert bump("v1.0.0") == "v1.0.1"
    assert bump("v1.0.1") == "v1.0.2"
    assert bump("v1.1.0") == "v1.1.1"
    assert bump("v1.1.1") == "v1.1.2"


def test_bump_patch():  # noqa: WPS218 (too many assert statements)
    """Test patch version bumping."""
    assert bump("0.0.1", "patch") == "0.0.2"
    assert bump("0.1.0", "patch") == "0.1.1"
    assert bump("0.1.1", "patch") == "0.1.2"
    assert bump("1.0.0", "patch") == "1.0.1"
    assert bump("1.0.1", "patch") == "1.0.2"
    assert bump("1.1.0", "patch") == "1.1.1"
    assert bump("1.1.1", "patch") == "1.1.2"

    assert bump("v0.0.1", "patch") == "v0.0.2"
    assert bump("v0.1.0", "patch") == "v0.1.1"
    assert bump("v0.1.1", "patch") == "v0.1.2"
    assert bump("v1.0.0", "patch") == "v1.0.1"
    assert bump("v1.0.1", "patch") == "v1.0.2"
    assert bump("v1.1.0", "patch") == "v1.1.1"
    assert bump("v1.1.1", "patch") == "v1.1.2"


def test_bump_minor():  # noqa: WPS218 (too many assert statements)
    """Test minor version bumping."""
    assert bump("0.0.1", "minor") == "0.1.0"
    assert bump("0.1.0", "minor") == "0.2.0"
    assert bump("0.1.1", "minor") == "0.2.0"
    assert bump("1.0.0", "minor") == "1.1.0"
    assert bump("1.0.1", "minor") == "1.1.0"
    assert bump("1.1.0", "minor") == "1.2.0"
    assert bump("1.1.1", "minor") == "1.2.0"

    assert bump("v0.0.1", "minor") == "v0.1.0"
    assert bump("v0.1.0", "minor") == "v0.2.0"
    assert bump("v0.1.1", "minor") == "v0.2.0"
    assert bump("v1.0.0", "minor") == "v1.1.0"
    assert bump("v1.0.1", "minor") == "v1.1.0"
    assert bump("v1.1.0", "minor") == "v1.2.0"
    assert bump("v1.1.1", "minor") == "v1.2.0"


def test_bump_major():  # noqa: WPS218 (too many assert statements)
    """Test major version bumping."""
    assert bump("0.0.1", "major") == "0.1.0"
    assert bump("0.1.0", "major") == "0.2.0"
    assert bump("0.1.1", "major") == "0.2.0"
    assert bump("1.0.0", "major") == "2.0.0"
    assert bump("1.0.1", "major") == "2.0.0"
    assert bump("1.1.0", "major") == "2.0.0"
    assert bump("1.1.1", "major") == "2.0.0"

    assert bump("v0.0.1", "major") == "v0.1.0"
    assert bump("v0.1.0", "major") == "v0.2.0"
    assert bump("v0.1.1", "major") == "v0.2.0"
    assert bump("v1.0.0", "major") == "v2.0.0"
    assert bump("v1.0.1", "major") == "v2.0.0"
    assert bump("v1.1.0", "major") == "v2.0.0"
    assert bump("v1.1.1", "major") == "v2.0.0"
