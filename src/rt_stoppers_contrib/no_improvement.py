from __future__ import annotations

import collections
from typing import Any, DefaultDict

from ray import tune


class NoImprovementStopper(tune.Stopper):
    def __init__(
        self,
        metric: str,
        *,
        rel_change_thld=0.01,
        mode: str = "max",
        patience=6,
        grace_period=4,
    ):
        """Stopper that stops if at no iteration within ``num_results`` a better
        result than the current best one is observed.

        Args:
            metric:
            rel_change_thld: Relative change threshold to be considered for improvement.
                Any change that is less than that is considered no improvement. If set
                to 0, any change is considered an improvement.
            mode: "max" or "min"
            patience: Number of iterations without improvement after which to stop.
                If 1, stop after the first iteration without improvement.
            grace_period: Number of iterations to wait before considering stopping
        """
        self.metric = metric
        self.rel_change_thld = rel_change_thld
        self.mode = mode
        if patience < 1:
            raise ValueError("Patience must be at least 1.")
        self.patience = patience
        self.grace_period = grace_period
        self._best: DefaultDict[Any, None | float] = collections.defaultdict(
            lambda: None
        )
        self._stagnant: DefaultDict[Any, int] = collections.defaultdict(int)
        self._epoch: DefaultDict[Any, int] = collections.defaultdict(int)

    def _better_than(self, a: float, b: float) -> bool:
        """Is result a better than result b?"""
        try:
            ratio = a / b
        except ZeroDivisionError:
            ratio = None
        if ratio is None:
            return False
        if self.mode == "max" and ratio > 1 + self.rel_change_thld:
            return True
        if self.mode == "min" and ratio < 1 - self.rel_change_thld:
            return True
        return False

    def __call__(self, trial_id, result) -> bool:
        self._epoch[trial_id] += 1
        if self._best[trial_id] is None:
            self._best[trial_id] = result[self.metric]
            return False
        best_result = self._best[trial_id]
        assert best_result is not None  # for mypy
        if self._better_than(result[self.metric], best_result):
            self._best[trial_id] = result[self.metric]
            self._stagnant[trial_id] = 0
            return False
        self._stagnant[trial_id] += 1
        if self._epoch[trial_id] < self.grace_period:
            return False
        if self._stagnant[trial_id] >= self.patience:
            return True
        return False

    def stop_all(self):
        return False