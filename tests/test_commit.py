"""Tests for the `commit` module."""

from __future__ import annotations

import pytest

from git_changelog import Commit


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
        assert not commit.trailers.keys()  # type: ignore[attr-defined]
    with pytest.warns(DeprecationWarning, match="Trailers are now a list of 2-tuples."):
        assert not commit.trailers.values()  # type: ignore[attr-defined]
    with pytest.warns(DeprecationWarning, match="Trailers are now a list of 2-tuples."):
        assert not commit.trailers.items()  # type: ignore[attr-defined]
    with pytest.warns(DeprecationWarning, match="Trailers are now a list of 2-tuples."):
        assert not commit.trailers.get("key")  # type: ignore[attr-defined]
    with (
        pytest.warns(
            DeprecationWarning,
            match="Getting a trailer with a string key will stop being supported in version 3. Instead, use an integer index, or iterate.",
        ),
        pytest.raises(KeyError),
    ):
        assert not commit.trailers["key"]  # type: ignore[call-overload]
