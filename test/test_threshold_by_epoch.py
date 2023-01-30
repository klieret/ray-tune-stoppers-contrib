from __future__ import annotations

from copy import deepcopy
from test import StopperTester

import pytest

from rt_stoppers_contrib import ThresholdTrialStopper


def get_reversed_experiment(st: StopperTester) -> StopperTester:
    """Changes signs of metric results and sets mode to min instead of max
    (and vice-versa)
    """
    stopper = deepcopy(st._stopper)
    stopper._thresholds = {k: -v for k, v in stopper._thresholds.items()}
    stopper._comparison_mode = "min" if stopper._comparison_mode == "max" else "max"
    return StopperTester(
        stopper=stopper,
        metric_results=[-m for m in st._metric_results],
        doesnt_stop=st._doesnt_stop,
    )


_cases = [
    StopperTester(
        ThresholdTrialStopper("loss", None),
        [1.0, 2.0, 3.0, 4.0],
        doesnt_stop=True,
    ),
    StopperTester(
        ThresholdTrialStopper("loss", {2: 3}),
        [
            1.0,
            2.0,
        ],
    ),
]
cases = [c for c in _cases]
cases.extend([get_reversed_experiment(c) for c in _cases])


@pytest.mark.parametrize("case", cases)
def test_integration(case: StopperTester) -> None:
    case.run()


def test_invalid_mode() -> None:
    stopper = ThresholdTrialStopper("loss", {1: 1}, mode="invalid")
    with pytest.raises(ValueError, match="Invalid mode"):
        stopper(0, {"loss": 1.0})
