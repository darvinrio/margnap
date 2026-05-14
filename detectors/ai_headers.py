"""
detectors/ai_headers.py

Detect AI-style headers and introductions that are overly helpful.

Pangram's data:
  - Human: 1 per 10k words
  - AI: 2 per 10k words
  - Multiplier: 2x

Examples of AI-style headers:
  - "Certainly! Here's..."
  - "Of course! I'd be happy to..."
  - "Sure thing! Here's a breakdown..."
  - "Happy to help! Here are..."
  - "Great question! Here's..."
  - "Absolutely! Let me break this down..."
  - "I'd be happy to explain..."
  - "Sure! Here are..."

Detection approach:
  Simple pattern matching. These are formulaic conversational openings
  that chatbot models use as preamble before delivering content.
  Very easy to detect via regex — just match the conversational
  opener patterns followed by a colon or dash and content.
"""

import re


def find_ai_headers(text: str) -> tuple[int, list[list[int]], list[str]]:
    """
    Detect AI-style headers/introductions in text.

    Returns:
        (match_count, list_of_spans, list_of_matched_text)
    """
    # Patterns for AI conversational openings
    # These are typically at the START of a response, followed by a colon/dash
    AI_HEADER_PATTERNS = [
        r'^(?:Certainly|Of\s+course|Sure|Sure\s+thing|Happy\s+to\s+help|Great\s+question|Absolutely|I\'d\s+be\s+happy\s+to|I\'m\s+happy\s+to|Let\s+me\s+help\s+you|I\'d\s+be\s+glad\s+to|It\'s\s+my\s+pleasure)\b.*?(?::|—|-)',
        r"^Here\'(?:s|s)\s+(?:a|an)\s+(?:breakdown|overview|summary|list|explanation|answer|response)",
        r"I?\s+can\s+help\s+you\s+with\s+that\s*(?:by\s+(?:providing|explaining|showing))?.*?[:—-]",
        r"To\s+(?:answer|explain|describe|summarize)\s+(?:your\s+)?question\s*(?:about)?\s*,?\s*(?:I?\s+will|here|let|\b(?:be|start|go))",
        r"Thank\s+you\s+for\s+(?:asking|your\s+(?:question|query|interest)).*?[:—-]",
        r"No\s+problem!\s*(?:here|I?|let).*?[:—-]",
        r"You\s+got\s+it!\s*(?:here|I?|let).*?[:—-]",
    ]

    combined_pattern = '|'.join(AI_HEADER_PATTERNS)
    regex = re.compile(combined_pattern, re.IGNORECASE | re.MULTILINE)

    matches = []
    matched_texts = []
    for m in regex.finditer(text):
        matches.append(list(m.span()))
        matched_texts.append(m.group(0))

    return len(matches), matches, matched_texts
