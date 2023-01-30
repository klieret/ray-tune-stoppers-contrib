from __future__ import annotations

from test import StopperTester

from rt_stoppers_contrib import AndStopper, NoImprovementTrialStopper


def test_combine_stopper_single() -> None:
    StopperTester(
        stopper=AndStopper(
            [
                NoImprovementTrialStopper(patience=3, metric="loss"),
            ]
        ),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    )


def test_combine_stopper_clone() -> None:
    StopperTester(
        stopper=AndStopper(
            [
                NoImprovementTrialStopper(patience=3, metric="loss"),
                NoImprovementTrialStopper(patience=3, metric="loss"),
            ]
        ),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    )


def test_combine_stopper_mixed() -> None:
    StopperTester(
        stopper=AndStopper(
            [
                NoImprovementTrialStopper(patience=1, metric="loss"),
                NoImprovementTrialStopper(patience=3, metric="loss"),
            ]
        ),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    )


def test_combine_stopper_empty() -> None:
    StopperTester(
        stopper=AndStopper([]),
        metric_results=[4.0, 3.0, 2.0, 1.0],
    )
