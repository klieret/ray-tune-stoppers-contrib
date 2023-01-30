from __future__ import annotations

from ray import tune


class StopperTester:
    def __init__(
        self,
        stopper: tune.Stopper,
        metric_results: list[float],
        doesnt_stop: bool = False,
    ):
        """

        Args:
            stopper: Metric must be set to 'loss'
            metric_results:
            doesnt_stop: Don't check if it stops
        """
        self._stopper = stopper
        self._metric_results = metric_results
        self._doesnt_stop = doesnt_stop

    def run(self) -> None:
        last_epoch = len(self._metric_results)
        for epoch, result in enumerate(self._metric_results, start=1):
            ret = self._stopper(0, {"loss": result})
            assert not self._stopper.stop_all()
            if epoch < last_epoch:
                assert not ret, "Should not have stopped yet"
            else:
                if self._doesnt_stop:
                    assert not ret, "Should not have stopped at all"
                else:
                    assert ret, "Should have stopped after last metric result"
