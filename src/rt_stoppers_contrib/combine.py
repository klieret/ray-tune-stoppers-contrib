from __future__ import annotations

from typing import Any

from ray import tune


class AndStopper(tune.Stopper):
    def __init__(self, stoppers: list[tune.Stopper]):
        """Trigger stopping option only if all stoppers agree."""
        self._stoppers = stoppers

    def __call__(self, trial_id: Any, result: dict[str, Any]) -> bool:
        return all([stopper(trial_id, result) for stopper in self._stoppers])

    def stop_all(self) -> bool:
        return all([stopper.stop_all() for stopper in self._stoppers])
