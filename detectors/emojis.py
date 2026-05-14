"""
detectors/emojis.py

Detect emojis, with emphasis on AI-typical emoji usage patterns.

Pangram's data:
  - Overall emoji use: barely elevated (2x multiplier)
  - But WHICH emojis differ wildly:
    ✅ white heavy check mark: 167x
    2️⃣ keycap two: 129x
    4️⃣ keycap four: 98x
    3️⃣ keycap three: 86x
    ✔️ check mark: 64x
    1️⃣ keycap one: 61x
    🚀 rocket: 26x
    ❌ cross mark: 24x

  - Humans use faces more: 😊 0.6x, ❤️ 0.2x

Detection approach:
  Emoji detection is straightforward via regex.
  The interesting part is CLASSIFICATION — separating AI-typical emojis
  (UI symbols, checkmarks, keycaps, arrows) from human-typical ones (faces, hearts).

  The detection is easy; the signal comes from the DISTRIBUTION of emoji types,
  not just the count.
"""

import re
import unicodedata
import emoji
from dataclasses import dataclass


@dataclass
class EmojiSignal:
    char: str
    name: str
    category: str  # "ai_typical", "human_typical", or "neutral"


def find_emojis(text: str) -> tuple[int, list[list[int]], list[EmojiSignal]]:
    """
    Detect emojis in text, classified by AI/human usage pattern.

    Returns:
        (total_count, list_of_spans, list_of_signals)
        Each signal is (char, unicode_name, category)
    """
    # AI-typical emojis (UI symbols, checkmarks, keycaps, etc.)
    AI_EMOJIS = {
        '✅': 'white heavy check mark',
        '✔️': 'check mark',
        '✖️': 'multiplication x',
        '❌': 'cross mark',
        '❎': 'cross mark button',
        '🚀': 'rocket',
        '💡': 'light bulb',
        '⚠️': 'warning sign',
        'ℹ️': 'information source',
        '📌': 'pushpin',
        '🔗': 'link',
        '🔍': 'magnifying glass',
        '🔑': 'key',
        '📊': 'bar chart',
        '📈': 'chart increasing',
        '📝': 'memo',
        '🎯': 'bullseye',
        '⭐': 'star',
        '✨': 'sparkles',
        '💰': 'money bag',
        '📱': 'mobile phone',
        '💻': 'laptop',
        '🏆': 'trophy',
        '👍': 'thumbs up',
        '👎': 'thumbs down',
    }

    # Human-typical emojis (faces, emotions)
    HUMAN_EMOJIS = {
        '😊': 'smiling face with smiling eyes',
        '❤️': 'red heart',
        '😂': 'tears of joy',
        '😍': 'smiling face with heart eyes',
        '🤔': 'thinking face',
        '😢': 'crying face',
        '😡': 'pouting face',
        '🥳': 'partying face',
        '👋': 'waving hand',
        '🤗': 'hugging face',
        '😎': 'smiling face with sunglasses',
        '🙏': 'folded hands',
        '😅': 'grinning face with sweat',
        '🤦': 'face palm',
        '🫡': 'saluting face',
        '👏': 'clapping hands',
    }

    # Use the `emoji` package for robust detection of emoji sequences (including ZWJ, flags, keycaps).
    # This correctly handles multi-codepoint emoji as single tokens and avoids
    # the overlapping/missing ranges issues of the hand-rolled character class.
    entries: list[tuple[list[int], EmojiSignal]] = []
    for match in emoji.emoji_list(text):
        em = match['emoji']
        span = [match['match_start'], match['match_end']]
        if em in AI_EMOJIS:
            sig = EmojiSignal(em, AI_EMOJIS[em], "ai_typical")
        elif em in HUMAN_EMOJIS:
            sig = EmojiSignal(em, HUMAN_EMOJIS[em], "human_typical")
        else:
            try:
                name = unicodedata.name(em, 'unknown')
            except ValueError:
                name = 'unknown'
            sig = EmojiSignal(em, name, "neutral")
        entries.append((span, sig))

    # Sort by start position to keep spans and signals aligned
    entries.sort(key=lambda x: x[0])
    spans_sorted = [s for s, _ in entries]
    signals_sorted = [sig for _, sig in entries]

    return len(spans_sorted), spans_sorted, signals_sorted
