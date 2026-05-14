"""
detectors/bullet_lists.py

Detect bullet/numbered lists used to organize information systematically.

Pangram's data:
  - Human: 3 per 10k words (9x multiplier)
  - AI: 28 per 10k words

Detection approach:
  Regex is straightforward for this. The key is detecting LISTS specifically,
  not just random dashes or numbers. AI tends to use lists even where prose
  would read more naturally (e.g., "apples, oranges, and bananas" → 3 bullet items).

  Patterns to match:
  1. -, *, +, • followed by space and text at line start
  2. Numbered lists: 1., 2., etc. at line start
  3. Multi-item sequences: 3+ list items in close proximity

  The "multiplier" signal comes from density: >3 list markers in a short
  passage is already suspicious.
"""

import re
from dataclasses import dataclass


@dataclass
class ListSignal:
    variant: str  # "bullets" or "numbered"
    spans: list[list[int]]


def find_bullet_lists(text: str) -> tuple[int, list[tuple[str, list[list[int]]]]]:
    """
    Detect bullet/numbered lists in text.

    Returns:
        (total_match_count, list_of_signals) where each signal is
        (variant, list_of_spans)
    """
    signals: dict[str, list[list[int]]] = {}

    # Unordered list markers: -, *, +, • followed by whitespace and content
    unordered = re.finditer(
        r'^[\s]*[-*+•]\s+\S.*$', text, re.MULTILINE
    )
    spans = [list(m.span()) for m in unordered]
    if spans:
        signals['unordered'] = spans

    # Numbered list markers: digit(s). followed by whitespace and content
    numbered = re.finditer(
        r'^[\s]*\d+\.\s+\S.*$', text, re.MULTILINE
    )
    spans = [list(m.span()) for m in numbered]
    if spans:
        signals['numbered'] = spans

    total = sum(len(v) for v in signals.values())
    signal_list = [(name, spans) for name, spans in signals.items()]
    return total, signal_list
