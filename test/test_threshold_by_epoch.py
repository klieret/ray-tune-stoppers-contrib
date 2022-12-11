from __future__ import annotations

from test import StopperTester

import pytest

from rt_stoppers_contrib.threshold_by_epoch import ThresholdByEpochStopper

_cases = [
    StopperTester(
        ThresholdByEpochStopper("loss", None),
        [1.0, 2.0, 3.0, 4.0],
        doesnt_stop=True,
    ),
    StopperTester(
        ThresholdByEpochStopper("loss", {2: 3}),
        [
            1.0,
            2.0,
        ],
    ),
]
cases = [c for c in _cases]


@pytest.mark.parametrize("case", cases)
def test_integration(case):
    case.run()
