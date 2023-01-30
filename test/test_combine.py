from __future__ import annotations

from test import StopperTester

from rt_stoppers_contrib.combine import AndStopper
from rt_stoppers_contrib.no_improvement import NoImprovementTrialStopper


def test_combine_stopper_single():
    StopperTester(
        stopper=AndStopper(
            [
                NoImprovementTrialStopper(patience=3, metric="loss"),
            ]
        ),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    )


def test_combine_stopper_clone():
    StopperTester(
        stopper=AndStopper(
            [
                NoImprovementTrialStopper(patience=3, metric="loss"),
                NoImprovementTrialStopper(patience=3, metric="loss"),
            ]
        ),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    )


def test_combine_stopper_mixed():
    StopperTester(
        stopper=AndStopper(
            [
                NoImprovementTrialStopper(patience=1, metric="loss"),
                NoImprovementTrialStopper(patience=3, metric="loss"),
            ]
        ),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    )


def test_combine_stopper_empty():
    StopperTester(
        stopper=AndStopper([]),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    )
