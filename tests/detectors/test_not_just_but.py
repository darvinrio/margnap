"""
test/detectors/test_not_just_but.py

Tests for the detectors/not_just_but.py.
"""

import pytest

from detectors.not_just_but import find_not_but_also


@pytest.mark.parametrize(
    "text, output",
    [
        pytest.param("", (0, []), id="empty"),
        pytest.param("not just but", (1, [[0, 12]])),
        pytest.param("not just but also", (1, [[0, 12]])),
    ],
)
def test_find_not_but_also(text: str, output: tuple[int, list[list[int]]]) -> None:
    """
    Test find_not_but_also function

    Verifies that the function correctly identifies Not just X but Y
    """
    assert find_not_but_also(text) == output
