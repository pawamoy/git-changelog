"""Tests for the `commit` module."""

import pytest

from git_changelog.commit import Commit


@pytest.mark.parametrize(
    ("body", "expected_trailers"),
    [
        ("t1: v1\nt2: v2", {"t1": "v1", "t2": "v2"}),  # ok
        ("body\n\nt1: v1\nt2: v2", {"t1": "v1", "t2": "v2"}),  # ok
        ("t1: v1\nt2:v2", {}),  # missing space after colon
        ("t1: v1\nt2: v2\n\nf", {}),  # trailers not last
        ("t1: v1\nt2 v2", {}),  # not all trailers
        ("something: else\n\nt1: v1\nt2: v2", {"t1": "v1", "t2": "v2"}),  # parse footer only
    ],
)
def test_parsing_trailers(body, expected_trailers):
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
