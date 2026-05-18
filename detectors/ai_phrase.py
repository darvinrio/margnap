"""
detectors/ai_phrase.py

Detect specific AI phrases
"""

import re

"""
AI Phrase and their frequency multiplier
Frequency multiplier is the number of times its appears in AI text compared to Human text
"""
AI_PHRASES: list[tuple[str, int | None]] = [
    # from https://www.pangram.com/supporting-evidence#sig-ngrams
    ("ability to adapt to", None),
    ("accessible even for those", None),
    ("anyone looking to elevate", None),
    ("become a focal point", None),
    ("become an essential part", None),
    ("blur the line between", None),
    ("can vary depending on the specific", None),
    ("casual night", None),
    ("complex tapestry", None),
    ("engaging narrative", None),
    ("fascinating and complex", None),
    ("feel repetitive", None),
    ("guessing until the final", None),
    ("he was known for", None),
    ("highly recommend for anyone", None),
    ("his ability to perform", None),
    ("i am writing to provide", None),
    ("i ordered their signature", None),
    ("is a compelling read", None),
    ("is a great question", None),
    ("its compact design", None),
    ("known for his ability", None),
    ("let me know if you'd", None),
    ("light on the complex", None),
    ("making it simple to", None),
    ("noticeable lag", None),
    ("offering profound", None),
    ("profound connection between", None),
    ("read for anyone interested", None),
    ("recently had the pleasure", None),
    ("reflection in the polished", None),
    ("steady despite the tremor", None),
    ("testament to human", None),
    ("to adapt to different", None),
    ("to detail and commitment", None),
    ("took a slow sip", None),
    ("weight of unspoken", None),
    ("you for your continued dedication", None),
    ("you or someone you know", None),
    ("you're touching on", None),
    ("today's fast-paced world", 35),
    ("crucial to note that", 22),
    ("delve into", 45),
    ("navigate the tapestry of", 18),
    # history=4754c1cd-a1ec-4368-9426-c382270cbb8c
    ("robust", 5),
    ("profound", 10),
    ("is its ability to", 10),
    ("robust", 5),
    ("invaluable", 7),
    ("is more than just", 7),
]


def _phrase_to_regex(phrase: str) -> str:
    """
    Convert a phrase to a regex pattern that matches it as a whole word.

    Args:
        phrase (str): The phrase to convert.

    Returns:
        str: The regex pattern.
    """
    words = phrase.split()
    return r"\b" + r"(?:\W|_)+".join(re.escape(w) for w in words) + r"\b"


def find_ai_phrases(text: str) -> tuple[int, list[list[int]]]:
    """
    Find AI phrases in the given text.

    Returns a list of [start, end] indices for each AI phrase.

    Args:
        text (str): The text to search for AI phrases.

    Returns:
        tuple[int, list[list[int]]]: A tuple containing
        - the number of matches
        - a list of their spans.
    """
    phrases = [phrase for phrase, _ in AI_PHRASES]

    pattern = re.compile(
        r"(?:" + "|".join(_phrase_to_regex(p) for p in phrases) + r")", re.IGNORECASE
    )

    spans = [list(match.span()) for match in pattern.finditer(text)]
    return len(spans), spans
