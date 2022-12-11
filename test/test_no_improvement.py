from __future__ import annotations

from copy import deepcopy
from test import StopperTester

import pytest

from rt_stoppers_contrib.no_improvement import NoImprovementStopper


def get_reversed_experiment(st: StopperTester):
    """Flips the order of metric results and sets mode to min instead of max
    (and vice-versa)
    """
    stopper = deepcopy(st._stopper)
    stopper.mode = "min" if stopper.mode == "max" else "max"
    return StopperTester(
        stopper=stopper,
        metric_results=list(reversed(st._metric_results)),
        doesnt_stop=st._doesnt_stop,
    )


_cases = [
    StopperTester(
        stopper=NoImprovementStopper(patience=3, metric="loss"),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    ),
    StopperTester(
        stopper=NoImprovementStopper(patience=3, metric="loss"),
        metric_results=[0.9, 3.0, 2.0, 1.0],
        doesnt_stop=True,
    ),
    StopperTester(
        stopper=NoImprovementStopper(
            patience=3, metric="loss", mode="min", rel_change_thld=0.1
        ),
        metric_results=[0.92, 0.95, 1.1, 1.0],
    ),
]
cases = [c for c in _cases]
cases.extend([get_reversed_experiment(c) for c in _cases])


@pytest.mark.parametrize("case", cases)
def test_integration(case):
    case.run()


def test_invalid_patience():
    with pytest.raises(ValueError, match="Patience must be at least 1."):
        NoImprovementStopper(metric="loss", patience=0)