from __future__ import annotations

import warnings

from rt_stoppers_contrib import NoImprovementTrialStopper  # noqa: F401

warnings.warn(
    "Please import NoImprovementTrialStopper directly from the rt_stoppers_contrib."
    " This module will be removed in a future release.",
    category=DeprecationWarning,
    stacklevel=2,
)
