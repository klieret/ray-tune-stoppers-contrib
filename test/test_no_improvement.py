from __future__ import annotations

from test import StopperTester

import pytest

from rt_stoppers_contrib.no_improvement import NoImprovementStopper

cases = [
    StopperTester(
        stopper=NoImprovementStopper(patience=3, metric="loss", mode="min"),
        metric_results=[1.0, 2.0, 3.0, 4.0],
    ),
    StopperTester(
        stopper=NoImprovementStopper(patience=3, metric="loss", mode="min"),
        metric_results=[1.0, 2.0, 3.0, 0.9],
        doesnt_stop=True,
    ),
    StopperTester(
        stopper=NoImprovementStopper(
            patience=3, metric="loss", mode="min", rel_change_thld=0.1
        ),
        metric_results=[1.0, 1.1, 0.95, 0.92],
    ),
]


@pytest.mark.parametrize("case", cases)
def test_integration(case):
    case.run()
