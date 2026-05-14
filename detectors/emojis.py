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
        '📊': 'chart increasing',
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

    # Emoji regex pattern: matches emoji sequences including variation selectors
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001f926-\U0001f937"  # new symbols
        "\U0001F192-\U0001F251"  # supplemental symbols
        "\U0001F600-\U0001F64F"  # more emoticons
        "\U0001F680-\U0001F6FF"  # transport
        "\U00002600-\U000026FF"  # misc symbols
        "\U0000FE00"  # variation selectors
        "\U0000FE0F"  # variation selector-16
        "\U0000200D"  # zero-width joiner
        "\U0000231A-\U0000231B"  # watch, hourglass
        "\U000023E9-\U000023F3"  # other symbols
        "\U000023F8-\U000023FA"  # more symbols
        "\U000025AA-\U000025AB"  # small squares
        "\U000025B6"  # triangle
        "\U000025C0"  # triangle left
        "\U000025BA-\U000025BB"  # triangles right
        "\U000025FC-\U000025FE"  # squares
        "\U00002611"  # ballot box
        "\U00002614-\U00002615"  # umbrella
        "\U00002648-\U00002653"  # zodiac
        "\U0000267F"  # wheelchair
        "\U00002693"  # anchor
        "\U000026A1"  # lightning
        "\U000026AA-\U000026AB"  # circles
        "\U000026BD-\U000026BE"  # sports
        "\U000026C4-\U000026C5"  # snowman
        "\U000026CE"  # Ophiuchus
        "\U000026D4"  # no entry
        "\U000026EA"  # church
        "\U000026F2-\U000026F3"  # camping, ferry
        "\U000026F5"  # sailboat
        "\U000026FA"  # tent
        "\U000026FD"  # fuel pump
        "\U00002700"  # open hands
        "\U00002705"  # checkmark
        "\U00002708-\U0000270D"  # pens
        "\U0000270F"  # pencil
        "\U00002712"  # black nib
        "\U00002714"  # checkmark
        "\U00002716"  # x
        "\U0000271D"  # bottom right
        "\U00002721"  # star
        "\U00002728"  # sparkle
        "\U00002733-\U00002734"  # eight spoked
        "\U00002744"  # snowflake
        "\U00002747"  # sparkles
        "\U0000274C"  # cross
        "\U0000274E"  # multiplication
        "\U00002753-\U00002755"  # question
        "\U00002757"  # exclamation
        "\U00002763-\U00002764"  # hearts
        "\U00002795-\U00002797"  # plus/minus
        "\U000027A1"  # arrow
        "\U000027B0"  # curly loop
        "\U000027BF"  # voice
        "\U00002934-\U00002935"  # arrows
        "\U00002B05-\U00002B07"  # arrows
        "\U00002B1B-\U00002B1C"  # squares
        "\U00002B50"  # star
        "\U00002B55"  # circle
        "\U00003030"  # wavy dash
        "\U0000303D"  # part alternation
        "\U00003297"  # circled ideograph
        "\U00003299"  # circled ideograph
        "]",
        re.UNICODE,
    )

    spans = []
    signals = []
    for m in emoji_pattern.finditer(text):
        emoji = m.group(0)
        spans.append(list(m.span()))

        # Classify the emoji
        if emoji in AI_EMOJIS:
            signals.append(EmojiSignal(emoji, AI_EMOJIS[emoji], "ai_typical"))
        elif emoji in HUMAN_EMOJIS:
            signals.append(EmojiSignal(emoji, HUMAN_EMOJIS[emoji], "human_typical"))
        else:
            # Try to get unicode name
            try:
                name = unicodedata.name(emoji, 'unknown')
            except ValueError:
                name = 'unknown'
            signals.append(EmojiSignal(emoji, name, "neutral"))

    return len(spans), sorted(spans), signals
