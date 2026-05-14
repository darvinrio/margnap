"""
detectors/markdown.py

Detect markdown formatting inserted into plain text contexts.

Signals:
  - Bold (**text**): 43x multiplier
  - Headers (#): 23x multiplier
  - Inline code (`code`): 5x multiplier
  - Italic (*text*): 2x multiplier

Detection approach: Simple regex. Very easy.
The key insight is not just presence but density - AI writes ~90/10k words
with markdown vs ~8/10k for humans.
"""

import re
from dataclasses import dataclass


@dataclass
class MarkdownSignal:
    variant: str
    count: int


def find_markdown(text: str) -> tuple[int, list[tuple[str, list[list[int]]]]]:
    """
    Detect markdown formatting in text.

    Returns:
        (total_count, list_of_signals) where each signal is
        (variant_name, list_of_spans)
    """
    signals: dict[str, list[list[int]]] = {}

    # Bold: **text**
    bold = re.finditer(r'\*\*(.+?)\*\*', text)
    spans = [list(m.span()) for m in bold]
    if spans:
        signals['bold'] = spans

    # Headers: # at start of line (but not markdown table headers or # in URLs)
    headers = re.finditer(r'^#{1,6}\s+', text, re.MULTILINE)
    spans = [list(m.span()) for m in headers]
    if spans:
        signals['header'] = spans

    # Inline code: `code`
    inline_code = re.finditer(r'`([^`]+)`', text)
    spans = [list(m.span()) for m in inline_code]
    if spans:
        signals['inline_code'] = spans

    # Italic: single *text* (but not inside **bold**)
    italic = re.finditer(r'(?<!\*)\*(?!\*)(\w[\w\s\w]*?\w)(?<!\w)\*(?!\*)', text)
    spans = [list(m.span()) for m in italic]
    if spans:
        signals['italic'] = spans

    total = sum(len(v) for v in signals.values())
    signal_list = [(name, spans) for name, spans in signals.items()]
    return total, signal_list
