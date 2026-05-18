"""
detectors/triad.py

Detect triads (e.g. "apple, banana and orange")
"""

import re


def find_triads(text: str) -> tuple[int, list[list[int]]]:
    """
    Finds triads (e.g. "apple, banana and orange") in the given text.

    Args:
        text (str): The text to search for triads.

    Returns:
        tuple[int, list[list[int]]]: A tuple containing
        - the number of matches
        - a list of their spans.
    """
    pattern = re.compile(
        r"\b([a-zA-Z]+)\b\s*,\s+([a-zA-Z]+)\b\s*(?:and|,)\s+([a-zA-Z]+)\b",
        re.IGNORECASE,
    )

    spans = [list(match.span()) for match in pattern.finditer(text)]
    return len(spans), spans
