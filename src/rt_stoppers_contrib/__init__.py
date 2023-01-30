from __future__ import annotations

import collections
from math import isnan
from typing import Any, DefaultDict, TypeVar

from ray import tune

try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version  # type: ignore


__version__ = version("rt_stoppers_contrib")


_T = TypeVar("_T")


def _get_quantity_for_epoch(
    values: dict[int, _T] | _T, epoch: int, fallback: _T | None = None
) -> _T:
    """Get quantity that is defined for lower limits of epochs

    Args:
        values:
        epoch:
        fallback:

    Returns:

    """
    if not isinstance(values, dict):
        return values
    relevant_epoch = max([k for k in values if k <= epoch], default=-1)
    if relevant_epoch < 0:
        if fallback is not None:
            return fallback
        raise ValueError(f"No value for epoch {epoch} found.")
    return values[relevant_epoch]


class NoImprovementTrialStopper(tune.Stopper):
    def __init__(
        self,
        metric: str,
        *,
        rel_change_thld: float | dict[int, float] = 0.01,
        mode: str = "max",
        patience: int | dict[int, int] = 6,
        grace_period: int = 4,
    ):
        """Stopper that stops trial if at no iteration within ``num_results`` a better
        result than the current best one is observed.

        This can be useful if your metric shows instabilities/oscillations and thus
        does not converge in a way that would make the
        ``tune.stopper.TrialPlateauStopper`` stop.

        Args:
            metric:
            rel_change_thld: Relative change threshold to be considered for improvement.
                Any change that is less than that is considered no improvement. If set
                to 0, any change is considered an improvement.
                Can also be set to a dictionary epoch -> threshold (the first epoch
                has the index 0).
            mode: "max" or "min"
            patience: Number of iterations without improvement after which to stop.
                If 1, stop after the first iteration without improvement.
                Can also be set to a dictionary epoch -> patience (the first epoch
                has the index 0).
            grace_period: Number of iterations to wait before considering stopping
        """
        self._metric = metric
        self._rel_change_thld = rel_change_thld
        self._comparison_mode = mode

        if isinstance(patience, dict):
            min_patience = min(patience.values())
        else:
            min_patience = patience
        if min_patience < 1:
            raise ValueError("Patience must be at least 1.")
        self._patience = patience
        self._grace_period = grace_period
        self._best: DefaultDict[Any, None | float] = collections.defaultdict(
            lambda: None
        )
        self._stagnant: DefaultDict[Any, int] = collections.defaultdict(int)
        self._epoch: DefaultDict[Any, int] = collections.defaultdict(int)

    def _better_than(self, a: float, b: float, epoch: int) -> bool:
        """Is result a better than result b?"""
        try:
            ratio = a / b
        except ZeroDivisionError:
            ratio = None
        if ratio is None:
            return False
        rc_thld = _get_quantity_for_epoch(self._rel_change_thld, epoch)
        if self._comparison_mode == "max" and ratio > 1 + rc_thld:
            return True
        if self._comparison_mode == "min" and ratio < 1 - rc_thld:
            return True
        return False

    def __call__(self, trial_id: Any, result: dict[str, Any]) -> bool:
        self._epoch[trial_id] += 1
        epoch = self._epoch[trial_id]
        if self._best[trial_id] is None:
            self._best[trial_id] = result[self._metric]
            return False
        best_result = self._best[trial_id]
        assert best_result is not None  # for mypy
        if self._better_than(result[self._metric], best_result, epoch):
            self._best[trial_id] = result[self._metric]
            self._stagnant[trial_id] = 0
            return False
        self._stagnant[trial_id] += 1
        if self._epoch[trial_id] < self._grace_period:
            return False
        if self._stagnant[trial_id] >= _get_quantity_for_epoch(self._patience, epoch):
            return True
        return False

    def stop_all(self) -> bool:
        return False


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
        return _get_quantity_for_epoch(self._thresholds, epoch, fallback=float("nan"))

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


class AndStopper(tune.Stopper):
    def __init__(self, stoppers: list[tune.Stopper]):
        """Trigger stopping option only if all stoppers agree."""
        self._stoppers = stoppers

    def __call__(self, trial_id: Any, result: dict[str, Any]) -> bool:
        return all([stopper(trial_id, result) for stopper in self._stoppers])

    def stop_all(self) -> bool:
        return all([stopper.stop_all() for stopper in self._stoppers])
