"""
detectors/em_dash.py

Detect em dashes.
"""

import re


def find_em_dashes(text: str) -> tuple[int, list[list[int]]]:
    """
    Find instances of em dashes in the given text.

    Args:
        text (str): The input text to search for em dashes.

    Returns:
        tuple[int, list[list[int]]]: A tuple containing
        - the number of matches
        - a list of their spans.
    """
    pattern = re.compile(r"\u2014")

    spans = [list(match.span()) for match in pattern.finditer(text)]
    return len(spans), spans
