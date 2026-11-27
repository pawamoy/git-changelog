"""Tests for the `commit` module."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from git_changelog import (
    AngularConvention,
    BasicConvention,
    Commit,
    ConventionalCommitConventionV0,
    ConventionalCommitConventionV1,
    LinuxConvention,
)


@pytest.mark.parametrize(
    "convention",
    [
        BasicConvention,
        AngularConvention,
        ConventionalCommitConventionV0,
        ConventionalCommitConventionV1,
        LinuxConvention,
    ],
)
@pytest.mark.parametrize("parse_trailers", [False, True])
def test_breaking_change_sections(convention: type[BasicConvention | AngularConvention], parse_trailers: bool) -> None:
    """Read multiple paragraphs and keep horizontal rules as description text."""
    description = ["Rename the API.", "", "Use `new()` instead of `old()`.", "", "---", "", "Then restart."]
    commit = Commit(
        "aaaaaaa",
        subject="feat: Change the API",
        body=[f"BREAKING CHANGE: {description[0]}", *description[1:], "", "Refs: #14"],
        parse_trailers=parse_trailers,
    )

    commit.update_with_convention(convention())

    assert commit.convention["is_major"]
    assert commit.breaking_changes == ["\n".join(description)]


@pytest.mark.parametrize("parse_trailers", [False, True])
@pytest.mark.parametrize("convention", [AngularConvention, ConventionalCommitConventionV1])
def test_multiple_breaking_changes(convention: type[AngularConvention], parse_trailers: bool) -> None:
    """Keep each section separate and exclude other footers with either trailer setting."""
    commit = Commit(
        "aaaaaaa",
        subject="feat: Change the API",
        body=[
            "Explain the feature.",
            "",
            "BREAKING CHANGE: Rename the API.",
            "Use the new name.",
            "",
            "BREAKING CHANGE: Remove the old option.",
            "",
            "Refs #14",
            "Signed-off-by: Someone",
        ],
        parse_trailers=parse_trailers,
    )

    commit.update_with_convention(convention())

    assert commit.breaking_changes == ["Rename the API.\nUse the new name.", "Remove the old option."]


def test_breaking_change_code_blocks() -> None:
    """Keep code, paragraph spacing, and delimiters inside fenced examples."""
    description = [
        "Use this configuration:",
        "",
        "```yaml",
        "option: value",
        "---",
        "BREAKING CHANGE: This is example code.",
        "```",
        "",
        "Then restart.",
    ]
    commit = Commit(
        "aaaaaaa",
        subject="feat: Change configuration",
        body=[f"BREAKING CHANGE: {description[0]}", *description[1:], "", "Refs: #14"],
    )

    commit.update_with_convention(ConventionalCommitConventionV1())

    assert commit.breaking_changes == ["\n".join(description)]


@pytest.mark.parametrize("convention", [ConventionalCommitConventionV0, ConventionalCommitConventionV1])
@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ([], ["Remove the API"]),
        (["Use the replacement.", "", "Migration details."], ["Remove the API"]),
        (["BREAKING CHANGE: Use the replacement."], ["Use the replacement."]),
    ],
)
def test_breaking_subject_fallback(convention: type[AngularConvention], body: list[str], expected: list[str]) -> None:
    """Use the subject when a breaking prefix has no explicit breaking change section."""
    commit = Commit("aaaaaaa", subject="refactor(api)!: Remove the API", body=body)

    commit.update_with_convention(convention())

    assert commit.breaking_changes == expected


def test_breaking_subject_fallback_without_trailers() -> None:
    """Use the subject even when the body contains migration details and trailers."""
    commit = Commit(
        "aaaaaaa", subject="fix!: Remove the API", body=["Migration details.", "", "Refs: #14"], parse_trailers=True
    )

    commit.update_with_convention(ConventionalCommitConventionV1())

    assert commit.breaking_changes == ["Remove the API"]


def test_conventional_v1_breaking_change_descriptions() -> None:
    """Read the singular marker and its continuation lines."""
    commit = Commit(
        "aaaaaaa",
        subject="custom: Change the API",
        body=["BREAKING CHANGE: Rename the API.", "Migration details.", "", "Refs #14"],
    )

    commit.update_with_convention(ConventionalCommitConventionV1())

    assert commit.breaking_changes == ["Rename the API.\nMigration details."]


@pytest.mark.parametrize("parse_trailers", [False, True])
@pytest.mark.parametrize("separator", ["", " ", "\t"])
def test_breaking_change_trailer_block(parse_trailers: bool, separator: str) -> None:
    """Keep colon-bearing prose, and exclude a final trailer block with folded values."""
    description = ["Rename the API.", "Note: Use the replacement.", "", "Restart after upgrading."]
    commit = Commit(
        "aaaaaaa",
        subject="feat: Change the API",
        body=[
            f"BREAKING CHANGE: {description[0]}",
            *description[1:],
            separator,
            "Refs: #14",
            "Signed-off-by: Someone",
            "  <someone@example.com>",
        ],
        parse_trailers=parse_trailers,
    )

    commit.update_with_convention(ConventionalCommitConventionV1())

    assert commit.breaking_changes == ["\n".join(description)]


def test_breaking_change_without_separate_trailer_block() -> None:
    """A trailer-shaped line without a blank separator remains description text."""
    commit = Commit("aaaaaaa", subject="feat: Change the API", body=["BREAKING CHANGE: Rename the API.", "Refs: #14"])

    commit.update_with_convention(ConventionalCommitConventionV1())

    assert commit.breaking_changes == ["Rename the API.\nRefs: #14"]


@pytest.mark.parametrize(
    "paragraph", [["https://example.com/migration"], ["Note: Use the replacement.", "Then restart."]]
)
def test_breaking_change_final_paragraph(paragraph: list[str]) -> None:
    """A final URL or prose paragraph remains part of the breaking change description."""
    commit = Commit(
        "aaaaaaa", subject="feat: Change the API", body=["BREAKING CHANGE: Rename the API.", "", *paragraph]
    )

    commit.update_with_convention(ConventionalCommitConventionV1())

    assert commit.breaking_changes == ["Rename the API.\n\n" + "\n".join(paragraph)]


@pytest.mark.parametrize(
    "body",
    [
        ["breaking change: Rename the API."],
        ["BREAKING CHANGES: Rename the API."],
        ["BREAKING-CHANGE: Rename the API."],
        ["Break: Rename the API."],
        ["Breaks: Rename the API."],
        ["BREAKING CHANGE:", "Rename the API."],
        ["Some prose.", "BREAKING CHANGE: Still prose."],
        ["An ordinary change."],
    ],
)
def test_nonbreaking_commits_have_no_breaking_changes(body: list[str]) -> None:
    """Do not extract descriptions from markers rejected by the selected convention."""
    commit = Commit("aaaaaaa", subject="custom: Change behavior", body=body)

    assert commit.breaking_changes == []

    commit.update_with_convention(ConventionalCommitConventionV1())

    assert commit.breaking_changes == []


@pytest.mark.parametrize("marker", ["BREAKING CHANGES", "BREAKING-CHANGE", "breaking change", "Break", "Breaks"])
def test_breaking_prefix_with_unrecognized_marker(marker: str) -> None:
    """Rejected marker spellings do not replace the subject fallback."""
    commit = Commit("aaaaaaa", subject="feat!: Replace the API", body=[f"{marker}: Rename the API."])

    commit.update_with_convention(ConventionalCommitConventionV1())

    assert commit.breaking_changes == ["Replace the API"]


@pytest.mark.parametrize(
    ("body", "expected_trailers"),
    [
        ("t1: v1\nt2: v2", [("t1", "v1"), ("t2", "v2")]),  # ok
        ("body\n\nt1: v1\nt2: v2", [("t1", "v1"), ("t2", "v2")]),  # ok
        ("t1: v1\nt2:v2", []),  # missing space after colon
        ("t1: v1\nt2: v2\n\nf", []),  # trailers not last
        ("t1: v1\nt2 v2", []),  # not all trailers
        (
            "something: else\n\nt1: v1\nt2: v2",
            [("t1", "v1"), ("t2", "v2")],
        ),  # parse footer only
        ("t1: v1\nt1: v2", [("t1", "v1"), ("t1", "v2")]),  # multiple identical trailers
    ],
)
def test_parsing_trailers(body: str, expected_trailers: list[tuple[str, str]]) -> None:
    """Assert trailers are parsed correctly.

    Parameters:
        body: A commit message body.
        expected_trailers: The trailers we expect to be parsed.
    """
    commit = Commit(
        commit_hash="aaaaaaaa",
        subject="Summary",
        body=body.split("\n"),
        parse_trailers=True,
    )
    assert commit.trailers == expected_trailers


# YORE: Bump 3: Remove block.
def test_trailers_emit_deprecation_warnings() -> None:
    """Trailers used as a dictionary emit deprecation warnings."""
    commit = Commit(
        commit_hash="aaaaaaaa",
        subject="Summary",
        parse_trailers=True,
    )
    with pytest.warns(DeprecationWarning, match="Trailers are now a list of 2-tuples."):
        assert not commit.trailers.keys()  # ty:ignore[missing-attribute]
    with pytest.warns(DeprecationWarning, match="Trailers are now a list of 2-tuples."):
        assert not commit.trailers.values()  # ty:ignore[missing-attribute]
    with pytest.warns(DeprecationWarning, match="Trailers are now a list of 2-tuples."):
        assert not commit.trailers.items()  # ty:ignore[missing-attribute]
    with pytest.warns(DeprecationWarning, match="Trailers are now a list of 2-tuples."):
        assert not commit.trailers.get("key")  # ty:ignore[missing-attribute]
    with (
        pytest.warns(
            DeprecationWarning,
            match="Getting a trailer with a string key will stop being supported in version 3. Instead, use an integer index, or iterate.",
        ),
        pytest.raises(KeyError),
    ):
        assert not commit.trailers["key"]  # ty:ignore[invalid-argument-type]


def test_tzinfo() -> None:
    """Keep timezone info from commit."""
    commit = Commit(
        commit_hash="aaaaaaaa",
        subject="Summary",
        parse_trailers=True,
        author_date="1772727280 -0500",  # 2026-03-05 11:13:27 -0500
        committer_date="1772830826 -0500",  # 2026-03-06 16:00:26 -0500
    )
    tz = timezone(timedelta(days=-1, seconds=68400))
    assert commit.author_date == datetime(2026, 3, 5, 11, 14, 40, tzinfo=tz)
    assert commit.committer_date == datetime(2026, 3, 6, 16, 0, 26, tzinfo=tz)
