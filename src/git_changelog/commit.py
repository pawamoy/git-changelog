"""Deprecated. Import from `git_changelog` directly."""

# YORE: Bump 3: Remove file.

import warnings
from typing import Any

from git_changelog._internal import commit


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `git_changelog.commit` is deprecated. Import from `git_changelog` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(commit, name)
