from __future__ import annotations

import warnings

from rt_stoppers_contrib import ThresholdTrialStopper  # noqa: F401

warnings.warn(
    "Please import ThresholdTrialStopper directly from the rt_stoppers_contrib. "
    "This module will be removed in a future release.",
    category=DeprecationWarning,
    stacklevel=2,
)
