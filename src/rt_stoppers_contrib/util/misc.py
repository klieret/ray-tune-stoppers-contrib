from __future__ import annotations

from typing import TypeVar

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
