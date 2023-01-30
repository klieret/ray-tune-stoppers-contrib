from __future__ import annotations

import math

import pytest

from rt_stoppers_contrib.util.misc import _get_quantity_for_epoch


def test_get_quantity() -> None:
    assert _get_quantity_for_epoch(0.5, 1) == 0.5
    assert _get_quantity_for_epoch({0: 0.5}, 1) == 0.5
    assert _get_quantity_for_epoch({0: 0.5}, 3) == 0.5
    assert math.isnan(_get_quantity_for_epoch({10: 0.5}, 3, fallback=float("nan")))
    assert math.isnan(_get_quantity_for_epoch({}, 3, fallback=float("nan")))
    with pytest.raises(ValueError):
        _get_quantity_for_epoch({10: 0.5}, 3)
    with pytest.raises(ValueError):
        _get_quantity_for_epoch({}, 3)
