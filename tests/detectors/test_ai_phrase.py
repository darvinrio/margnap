"""
test/detectors/test_ai_phrase.py

Test cases for the ai_phrase detector.
"""

import pytest

from detectors.ai_phrase import find_ai_phrases


@pytest.mark.parametrize(
    "text, output",
    [
        pytest.param("", (0, []), id="empty"),
        pytest.param(
            "is its ability to",
            (1, [[0, 17]]),
            id="single_phrase",
        ),
        pytest.param(
            "is it's ability to",
            (1, [[0, 18]]),
            id="single_phrase_with_apostrophe",
        ),
        pytest.param(
            "is its Ability to",
            (1, [[0, 17]]),
            id="single_phrase_with_case",
        ),
        pytest.param(
            "is it's Ability to",
            (1, [[0, 18]]),
            id="single_phrase_with_case_and_apostrophe",
        ),
    ],
)
def test_find_ai_phrases(text: str, output: tuple[int, list[list[int]]]) -> None:
    """
    Test the find_ai_phrases function.

    Verifies that the function correctly identifies AI phrases in the given text.
    """
    spans = find_ai_phrases(text)
    assert spans == output
