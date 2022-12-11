from __future__ import annotations

from ray import tune

from rt_stoppers_contrib.no_improvement import NoImprovementStopper


class StopperTester:
    def __init__(self, stopper: tune.Stopper, metric_results: list[float]):
        """

        Args:
            stopper: Metric must be set to 'loss'
            metric_results:
        """
        self._stopper = stopper
        self._metric_results = metric_results

    def run(self):
        last_epoch = len(self._metric_results)
        for epoch, result in enumerate(self._metric_results, start=1):
            ret = self._stopper(0, {"loss": result})
            if epoch < last_epoch:
                assert not ret
            else:
                assert ret


def test_integration():
    StopperTester(
        stopper=NoImprovementStopper(patience=3, metric="loss", mode="min"),
        metric_results=[1.0, 2.0, 3.0, 4.0],
    ).run()
