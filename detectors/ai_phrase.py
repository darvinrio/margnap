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
    # history=43cd0cb7-94ed-4320-a979-527df6f5032b
    ("resilience", 30),
    # history=25cc4c4e-8442-4c93-87eb-26586ac532e0
    ("on one of the most", 6),
    ("blend", 6),
]


def _word_to_pattern(word: str) -> str:
    r"""
    Convert a word to a regex pattern that matches it as a whole word.

    Description:
        Converts each character in word to a regex pattern that matches it as a whole.
        Helps pattern matching "its" in "it's"

    Example:
        "hello" -> "[^\\w]*h[^\\w]*e[^\\w]*l[^\\w]*l[^\\w]*o[^\\w]*"
        "its" -> "[^\\w]*i[^\\w]*t[^\\w]*s[^\\w]*"
    Args:
        word (str): The word to convert.

    Returns:
        str: The regex pattern.
    """
    chars = [re.escape(c) for c in word]
    return r"[^\w]*".join(chars)


def _phrase_to_pattern(phrase: str) -> str:
    r"""
    Convert a phrase to a regex pattern that matches it as a whole word.

    Description:
        Splits the phrase into words, converts each word to a regex pattern,
        and joins them with word boundaries to match the phrase as a whole word.

    Args:
        phrase (str): The phrase to convert.

    Returns:
        str: The regex pattern.
    """
    words = phrase.split()
    return r"\b" + r"(?:\W|_)+".join(_word_to_pattern(w) for w in words) + r"\b"


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
        r"(?:" + "|".join(_phrase_to_pattern(p) for p in phrases) + r")", re.IGNORECASE
    )

    spans = [list(match.span()) for match in pattern.finditer(text)]
    return len(spans), spans
