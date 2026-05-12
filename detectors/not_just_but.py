"""
not_just_but.py

Detect "not ... but also ..."
"""

import re


def find_not_but_also(text: str) -> tuple[int, list[list[int]]]:
    """
    Find instances of "not  ... but also ..." in the given text.

    Args:
        text (str): The input text to search for "not ... but also ..." instances.

    Returns:
        tuple[int, list[list[int]]]: A tuple containing
        - the number of matches
        - a list of their spans.
    """
    pattern = re.compile(
        r"not\s+\s+.*?(?:,\s*)?but\s+also\s+.*?(?=[.!?]|$)", re.IGNORECASE | re.DOTALL
    )

    spans = [list(match.span()) for match in pattern.finditer(text)]
    return len(spans), spans
