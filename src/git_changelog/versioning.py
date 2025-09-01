"""Deprecated. Import from `git_changelog` directly."""

# YORE: Bump 3: Remove file.

import warnings
from typing import Any

from git_changelog._internal import versioning


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `git_changelog.versioning` is deprecated. Import from `git_changelog` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(versioning, name)
