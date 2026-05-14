"""
detectors/unusual_unicode.py

Detect unusual Unicode characters that may indicate humanization attempts
or AI formatting habits.

Pangram's data:
  - Human: 28 per 10k words
  - AI: 71 per 10k words
  - Multiplier: 3x

Top offenders (by multiplier):
  - ─ (U+2500) box drawings light horizontal: 940x
  - ≈ (U+2248) almost equal to: 241x
  - ⚠ (U+26A0) warning sign: 57x
  - → (U+2192) rightwards arrow: 48x

Detection approach:
  Simple regex / character class matching. Very easy.
  The characters themselves are rare in normal human typing.
"""

import re


def find_unusual_unicode(text: str) -> tuple[int, list[list[int]], list[tuple[str, str]]]:
    """
    Detect unusual Unicode characters in text.

    Returns:
        (total_count, list_of_spans, list_of_char_names)
        char_names: [(matched_char, name), ...] for reference
    """
    # Set of unusual Unicode characters that appear at high multiplier
    # These are characters you can't type from a standard keyboard
    UNUSUAL_CHARS = {
        '\u2500': 'box drawings light horizontal',      # ─
        '\u2501': 'box drawings light double',           # ━
        '\u2502': 'box drawings light vertical',         # │
        '\u250c': 'box drawings light down and right',   # ┌
        '\u2510': 'box drawings light down and left',    # ┐
        '\u2514': 'box drawings light up and right',     # └
        '\u2518': 'box drawings light up and left',      # ┘
        '\u253c': 'box drawings light vertical and horizontal', # ┼
        '\u2248': 'almost equal to',                     # ≈
        '\u2264': 'less-than or equal to',               # ≤
        '\u2265': 'greater-than or equal to',            # ≥
        '\u2190': 'leftwards arrow',                     # ←
        '\u2191': 'upwards arrow',                       # ↑
        '\u2192': 'rightwards arrow',                    # →
        '\u2193': 'downwards arrow',                     # ↓
        '\u2194': 'left right arrow',                    # ↔
        '\u2196': 'north west arrow',                    # ↖
        '\u2197': 'north east arrow',                    # ↗
        '\u2198': 'south east arrow',                    # ↘
        '\u2199': 'south west arrow',                    # ↙
        '\u21b5': 'downwards arrow with corner left to right', # ↵
        '\u2318': 'place of interest sign',              # ⌘
        '\u25cb': 'white circle',                        # ○
        '\u25cf': 'black circle',                        # ●
        '\u25e6': 'white bullet',                        # ◦
        '\u25aa': 'black small square',                  # ▪
        '\u25ab': 'white small square',                  # ▫
        '\u25b6': 'black right-pointing triangle',       # ▶
        '\u25c0': 'black left-pointing triangle',        # ◀
        '\u25b8': 'black right-pointing pointer',        # ▸
        '\u25be': 'black down-pointing triangle',        # ▾
        '\u25c4': 'black left-pointing pointer',         # ◄
        '\u25ba': 'black right-pointing pointer',        # ►
        '\u2605': 'black star',                          # ★
        '\u2606': 'white star',                          # ☆
        '\u2665': 'black heart suit',                    # ♥
        '\u2666': 'diamond suit',                        # ♦
        '\u26a0': 'warning sign',                        # ⚠
        '\u2713': 'check mark',                          # ✓
        '\u2714': 'heavy check mark',                    # ✔
        '\u2716': 'multiplication x',                    # ✖
        '\u2717': 'heavy multiplication x',              # ✗
        '\u271c': 'ballot x',                            # ✜
        '\u2720': 'cross mark',                          # ✠
        '\u2736': 'white trident contour',               # ❶
        '\u2740': 'easy key',                            # ❀
        '\u2757': 'exclamation mark',                    # ‼
        '\u2763': 'heavy heart exclamation',             # ❣
        '\u2764': 'heavy black heart',                   # ❤
        '\u2776': 'dotted circle',                       # ❶
        '\u2777': 'dotted circle',                       # ❷
        '\u2981': 'z notation spot',                     # ⦁
        '\u3008': 'left angle bracket',                  # 〈
        '\u3009': 'right angle bracket',                 # 〉
        '\u3013': 'geta mark',                           # ︓
        '\uff01': 'fullwidth exclamation mark',          # ！
        '\uff02': 'fullwidth double quotation mark',     # ＂
        '\uff03': 'fullwidth number sign',               # ＃
        '\uff04': 'fullwidth dollar sign',               # ＄
        '\uff05': 'fullwidth percent sign',              # ％
        '\uff06': 'fullwidth ampersand',                 # ＆
        '\uff07': 'fullwidth apostrophe',                # ＇
        '\uff08': 'fullwidth left parenthesis',          # （
        '\uff09': 'fullwidth right parenthesis',         # ）
        '\uff0a': 'fullwidth asterisk',                  # ＊
        '\uff0b': 'fullwidth plus sign',                 # ＋
        '\uff0c': 'fullwidth comma',                     # ，
        '\uff0d': 'fullwidth hyphen-minus',              # －
        '\uff0e': 'fullwidth full stop',                 # ．
        '\uff0f': 'fullwidth solidus',                   # ／
        '\uff1a': 'fullwidth colon',                     # ：
        '\uff1b': 'fullwidth semicolon',                 # ；
        '\uff1c': 'fullwidth less-than sign',            # ＜
        '\uff1d': 'fullwidth equals sign',               # ＝
        '\uff1e': 'fullwidth greater-than sign',         # ＞
        '\uff1f': 'fullwidth question mark',             # ？
        '\uff20': 'fullwidth commercial at',             # ＠
        '\uff3b': 'fullwidth left square bracket',       # ［
        '\uff3c': 'fullwidth reverse solidus',           # ＼
        '\uff3d': 'fullwidth right square bracket',      # ］
        '\uff3e': 'fullwidth circumflex accent',         # ＾
        '\uff3f': 'fullwidth low line',                  # ＿
        '\uff40': 'fullwidth grave accent',              # ｀
        '\uff5b': 'fullwidth left curly bracket',        # ［
        '\uff5c': 'fullwidth vertical line',             # ｜
        '\uff5d': 'fullwidth right curly bracket',       # ］
        '\uff5e': 'fullwidth tilted double hyphen',      # ～
    }

    spans = []
    matched = []
    for char, name in UNUSUAL_CHARS.items():
        for m in re.finditer(re.escape(char), text):
            spans.append(list(m.span()))
            matched.append((char, name))

    return len(spans), sorted(spans), matched
