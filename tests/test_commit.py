"""Tests for the `commit` module."""

from __future__ import annotations

from abc import ABCMeta
from typing import Generator

import pytest

from git_changelog.commit import (
    AngularConvention,
    BasicConvention,
    Commit,
    CommitConvention,
    ConventionalCommitConvention,
)


@pytest.mark.parametrize(
    ("body", "expected_trailers"),
    [
        ("t1: v1\nt2: v2", {"t1": "v1", "t2": "v2"}),  # ok
        ("body\n\nt1: v1\nt2: v2", {"t1": "v1", "t2": "v2"}),  # ok
        ("t1: v1\nt2:v2", {}),  # missing space after colon
        ("t1: v1\nt2: v2\n\nf", {}),  # trailers not last
        ("t1: v1\nt2 v2", {}),  # not all trailers
        (
            "something: else\n\nt1: v1\nt2: v2",
            {"t1": "v1", "t2": "v2"},
        ),  # parse footer only
    ],
)
def test_parsing_trailers(body: str, expected_trailers: dict[str, str]) -> None:
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


@pytest.fixture()
def _reserve_types() -> Generator[None, None, None]:
    """Fixture to preserve the conventional types."""
    original_types: dict[type[CommitConvention], tuple[dict[str, str], list[str]]] = {
        AngularConvention: (dict(AngularConvention.TYPES), list(AngularConvention.MINOR_TYPES)),
        BasicConvention: (dict(BasicConvention.TYPES), list(BasicConvention.MINOR_TYPES)),
        ConventionalCommitConvention: (dict(ConventionalCommitConvention.TYPES),
                                       list(ConventionalCommitConvention.MINOR_TYPES)),
    }

    yield

    AngularConvention.TYPES = dict(original_types[AngularConvention][0])
    BasicConvention.TYPES = dict(original_types[BasicConvention][0])
    ConventionalCommitConvention.TYPES = dict(original_types[ConventionalCommitConvention][0])
    AngularConvention.MINOR_TYPES = list(original_types[AngularConvention][1])
    BasicConvention.MINOR_TYPES = list(original_types[BasicConvention][1])
    ConventionalCommitConvention.MINOR_TYPES = list(original_types[ConventionalCommitConvention][1])


@pytest.mark.usefixtures("_reserve_types")
def test_replace_types() -> None:
    """Test that the TYPES attribute is replaced correctly in various conventions."""
    _new_types = {"n": "Notes", "o": "Other", "d": "Draft"}
    for convention in [AngularConvention, BasicConvention, ConventionalCommitConvention]:
        assert _new_types != convention.TYPES
        convention.replace_types(_new_types)
        assert _new_types == convention.TYPES


@pytest.mark.usefixtures("_reserve_types")
def test_is_minor_works_with_custom_minor_types() -> None:
    """Test that custom minor types are correctly recognized as minor changes."""
    _new_types = {"n": "Notes", "o": "Other", "d": "Draft"}
    _minor_types = "n,o"
    for convention in [AngularConvention, BasicConvention, ConventionalCommitConvention]:
        subject = "n: Added a new feature"
        commit = Commit(
            commit_hash="aaaaaaa",
            subject=subject,
            body=[""],
            author_date="1574340645",
            committer_date="1574340645",
        )
        convention.replace_types(_new_types)
        convention.update_minor_list(_minor_types)
        if not isinstance(convention, ABCMeta):
            conv = convention()
            commit_dict = conv.parse_commit(commit)
            assert not commit_dict["is_major"]
            assert commit_dict["is_minor"]
            assert not commit_dict["is_patch"]
