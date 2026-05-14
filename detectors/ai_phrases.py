"""
detectors/ai_phrases.py

Detect AI-typical phrases that appear far more often in AI-generated text.

Based on Pangram's list of 40+ overused phrases like:
  - "in today's fast-paced world" (35x)
  - "crucial to note that" (22x)
  - "delve into" (45x)
  - "navigate the tapestry of" (18x)
  - "complex tapestry"
  - "profound connection between"
  - ...and many more

Detection approach:
  Option A (Simplest): Pattern matching against a curated phrase list.
    - Pros: High precision, very easy to maintain, no false positives
    - Cons: Requires maintaining the phrase list

  Option B (Statistical): N-gram frequency analysis.
    - Pros: Can discover new phrases automatically
    - Cons: Much harder, needs baseline corpus, prone to false positives

  Recommendation: Option A. Each phrase is individually known, not a
  statistical pattern. Just do a case-insensitive substring search.

The challenge: You can't regex your way to "delve into" being suspicious
without context. "Delve" itself isn't rare in human writing; the phrase
"is only suspicious in combination with other AI tells."
"""

import re
from dataclasses import dataclass

# Curated list of AI-overused phrases from Pangram's blog.
# Each entry is a regex pattern for flexibility (handles apostrophe variants).
# These are NOT regex — they are literal phrases to match (compiled to regex).
AI_PHRASES = [
    "ability to adapt to",
    "accessible even for those",
    "anyone looking to elevate",
    "become a focal point",
    "become an essential part",
    "blur the line between",
    "can vary depending on the specific",
    "casual night",
    "complex tapestry",
    "engaging narrative",
    "fascinating and complex",
    "feel repetitive",
    "guessing until the final",
    "he was known for",
    "highly recommend for anyone",
    "his ability to perform",
    "i am writing to provide",
    "i ordered their signature",
    "is a compelling read",
    "is a great question",
    "its compact design",
    "known for his ability",
    "let me know if you'd",
    "light on the complex",
    "making it simple to",
    "noticeable lag",
    "offering profound",
    "profound connection between",
    "read for anyone interested",
    "recently had the pleasure",
    "reflection in the polished",
    "steady despite the tremor",
    "testament to human",
    "to adapt to different",
    "to detail and commitment",
    "took a slow sip",
    "weight of unspoken",
    "you for your continued dedication",
    "you or someone you know",
    "you're touching on",
    # Extra high-signal phrases from the examples section
    "in today's fast-paced world",
    "crucial to note that",
    "delve into",
    "navigate the tapestry of",
    "ever-evolving landscape",
    "dive into",
    "in conclusion",
    "it is important to note",
    "on the other hand",
    "last but not least",
    "at the end of the day",
    "in the realm of",
    "play a significant role",
    "in today's world",
    "a testament to",
    "fascinating world",
    "deep dive",
    "cutting edge",
    "game changer",
    "paradigm shift",
    "robust solution",
    "seamless integration",
    "holistic approach",
]


def find_ai_phrases(text: str) -> tuple[int, list[list[int]]]:
    """
    Find AI-typical phrases in the given text.

    Returns:
        (match_count, list_of_spans)
    """
    # Build a single pattern from all phrases.
    # Escape each phrase for safe regex inclusion.
    escaped = [re.escape(p) for p in AI_PHRASES]
    # Sort longest first to avoid partial matches
    escaped.sort(key=len, reverse=True)
    pattern = re.compile("|".join(escaped), re.IGNORECASE)

    spans = [list(m.span()) for m in pattern.finditer(text)]
    return len(spans), spans
