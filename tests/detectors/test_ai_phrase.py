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
            "The most profound impact of DBT is its ability to impose software engineering best practices onto the data workflow",  # noqa: E501
            (2, [[9, 17], [32, 49]]),
            id="single_phrase",
        ),
        pytest.param(
            "The most profound impact of DBT is it's ability to impose software engineering best practices onto the data workflow",  # noqa: E501
            (2, [[9, 17], [32, 50]]),
            id="single_phrase_with_apostrophe",
        ),
        pytest.param(
            "The most profound impact of DBT is its Ability to impose software engineering best practices onto the data workflow",  # noqa: E501
            (2, [[9, 17], [32, 49]]),
            id="single_phrase_with_case",
        ),
        pytest.param(
            "The most profound impact of DBT is it's Ability to impose software engineering best practices onto the data workflow",  # noqa: E501
            (2, [[9, 17], [32, 50]]),
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
