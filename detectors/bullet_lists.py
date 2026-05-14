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


def _consecutive_lines(spans: list[list[int]], text: str, min_consecutive: int = 2) -> list[list[int]]:
    """Filter spans to keep only those belonging to runs of ≥min_consecutive consecutive lines."""
    if not spans:
        return []

    # Compute line number for each span (0-based)
    spans_with_lines = [(span, text[: span[0]].count('\n')) for span in spans]
    # Sort by line number
    spans_with_lines.sort(key=lambda x: x[1])

    filtered: list[list[int]] = []
    current_group: list[list[int]] = []
    prev_line: int | None = None

    for span, line in spans_with_lines:
        if prev_line is not None and line == prev_line + 1:
            current_group.append(span)
        else:
            if len(current_group) >= min_consecutive:
                filtered.extend(current_group)
            current_group = [span]
        prev_line = line

    if len(current_group) >= min_consecutive:
        filtered.extend(current_group)

    return filtered


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
    # Filter: require at least 2 consecutive list-marker lines to reduce false positives
    spans = _consecutive_lines(spans, text, min_consecutive=2)
    if spans:
        signals['unordered'] = spans

    # Numbered list markers: digit(s). followed by whitespace and content
    numbered = re.finditer(
        r'^[\s]*\d+\.\s+\S.*$', text, re.MULTILINE
    )
    spans = [list(m.span()) for m in numbered]
    spans = _consecutive_lines(spans, text, min_consecutive=2)
    if spans:
        signals['numbered'] = spans

    total = sum(len(v) for v in signals.values())
    signal_list = [(name, spans) for name, spans in signals.items()]
    return total, signal_list
