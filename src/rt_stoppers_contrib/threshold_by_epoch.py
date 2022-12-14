from __future__ import annotations

import collections
from math import isnan
from typing import Any, DefaultDict

from ray import tune


class ThresholdTrialStopper(tune.Stopper):
    def __init__(
        self, metric: str, thresholds: None | dict[int, float], *, mode: str = "max"
    ):
        """Stopper that stops a trial if results at a certain epoch fall above/below
        a certain threshold.

        Args:
            metric: The metric to check
            thresholds: Thresholds as a mapping of epoch to threshold. The first epoch
                (the first time the stopper is checked) is numbered 1.
            mode: "max" or "min"
        """
        self._metric = metric
        if thresholds is None:
            thresholds = {}
        self._thresholds: dict[int, float] = thresholds
        self._comparison_mode = mode
        self._epoch: DefaultDict[Any, int] = collections.defaultdict(int)

    def _get_threshold(self, epoch: int) -> float:
        """Get threshold for epoch. NaN is returned if no threshold is
        defined.
        """
        relevant_epoch = max([k for k in self._thresholds if k <= epoch], default=-1)
        if relevant_epoch < 0:
            return float("nan")
        assert relevant_epoch in self._thresholds
        return self._thresholds[relevant_epoch]

    def _better_than(self, a: float, b: float) -> bool:
        """Is a better than b based on the comparison mode?"""
        if self._comparison_mode == "max":
            return a > b
        elif self._comparison_mode == "min":
            return a < b
        else:
            raise ValueError(f"Invalid mode {self._comparison_mode}")

    def __call__(self, trial_id: Any, result: dict[str, Any]) -> bool:
        self._epoch[trial_id] += 1
        threshold = self._get_threshold(self._epoch[trial_id])
        if isnan(threshold):
            return False
        return not self._better_than(result[self._metric], threshold)

    def stop_all(self) -> bool:
        return False
