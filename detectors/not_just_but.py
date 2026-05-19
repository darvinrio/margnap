"""
not_just_but.py

Detect "not ... but also ..."
"""

import re

"""Defines the gap placeholder and its regex pattern for use in templates."""
GAP = "..."
GAP_REGEX = r".*?"

TEMPLATES = [
    ["that's not", GAP, "that's", GAP],
    ["not", GAP, "but", GAP],
]


def template_to_regex(parts: list[str]) -> str:
    """
    Convert a template to a regex pattern that matches it as a whole word.

    Args:
        parts (list[str]): The template parts to convert.

    Returns:
        str: The regex pattern that matches the template as a whole word.
    """
    out = []
    for part in parts:
        if part == GAP:
            out.append(GAP_REGEX)
        else:
            out.append(re.escape(part).replace(r"\ ", r"\s+"))
    return "".join(out)


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
        "|".join(f"(?:{template_to_regex(t)})" for t in TEMPLATES),
        re.IGNORECASE | re.DOTALL,
    )

    spans = [list(match.span()) for match in pattern.finditer(text)]
    return len(spans), spans
