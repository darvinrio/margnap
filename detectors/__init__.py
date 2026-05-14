"""
__init__.py

All 9 Pangram Supporting Evidence detectors:
  1. em_dash.py           - Em dash overuse (10x)
  2. not_just_but.py      - "not just X but Y" pattern (3x)
  3. triad.py             - Rule of three triads (4x)
  4. markdown.py          - Markdown in plain text (12x)
  5. ai_phrases.py        - AI-overused phrases (12x)
  6. bullet_lists.py      - Bullet list overuse (9x)
  7. unusual_unicode.py   - Unusual Unicode chars (3x)
  8. ai_headers.py        - AI-style headers/intros (2x)
  9. emojis.py            - AI-typical emoji distribution (2x)
"""

from .em_dash import find_em_dashes
from .not_just_but import find_not_but_also
from .triad import find_triads
from .markdown import find_markdown
from .ai_phrases import find_ai_phrases
from .bullet_lists import find_bullet_lists
from .unusual_unicode import find_unusual_unicode
from .ai_headers import find_ai_headers
from .emojis import find_emojis

__all__ = [
    "find_em_dashes",
    "find_not_but_also",
    "find_triads",
    "find_markdown",
    "find_ai_phrases",
    "find_bullet_lists",
    "find_unusual_unicode",
    "find_ai_headers",
    "find_emojis",
]
