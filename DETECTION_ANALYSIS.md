# Pangram Supporting Evidence Detection — Regex/Heuristic Analysis

> Analysis of how easy it is to detect each of Pangram's 9 AI-detection signals using regex or heuristics. Tested against `sample_text.txt` (~1000 words, AI-generated DBT article).

---

## Quick Results

| # | Signal | AI:H Multiplier | Regex? | Difficulty | Detected in Sample |
|---|--------|-----------------|--------|------------|-------------------|
| 1 | Markdown | 12× | ✓ | **Trivial** | 27 (269/10k) |
| 2 | AI Phrases | 12× | ✓ (lookup) | **Easy** | 1 |
| 3 | Em dashes | 10× | ✓ | **Trivial** | 6 (60/10k) |
| 4 | Bullet lists | 9× | ✓ | **Easy** | 7 (70/10k) |
| 5 | Triads | 4× | ✓ | **Moderate** | 10 (100/10k) |
| 6 | Not just X but Y | 3× | ✓ | **Easy** | 0 |
| 7 | Unusual Unicode | 3× | ✓ | **Easy** | 0 |
| 8 | AI-style headers | 2× | ✓ | **Easy** | 0 |
| 9 | Emojis | 2× | ✓ | **Easy** | 0 |

**All 9 signals are detectable via regex/heuristics.** None require machine learning.

---

## Detailed Breakdown

### 1. Markdown (12× multiplier) — TRIVIAL

**Detection:** 4 simple regexes, one per variant.

```python
import re

BOLD = re.compile(r'\*\*(.+?)\*\*')       # 43× multiplier
HEADER = re.compile(r'^#{1,6}\s+', re.M)  # 23× multiplier
INLINE_CODE = re.compile(r'`([^`]+)`')    # 5× multiplier
ITALIC = re.compile(r'(?<!\*)\*(\w[\w\s\w]*?\w)\*(?!\*)')  # 2× multiplier
```

**Precision:** Perfect. Each pattern is unambiguous — `**text**` is markdown, nothing else.

**Signal source:** Density, not presence. AI writes ~90/10k words with markdown vs ~8/10k for humans.

**Verdict:** One of the easiest to detect. The regexes are 4 lines of code.

---

### 2. AI Phrases (12× multiplier) — EASY

**Detection:** Curated list lookup, not a regex pattern.

```python
AI_PHRASES = [
    "delve into",
    "in today's fast-paced world",
    "crucial to note that",
    "navigate the tapestry of",
    "complex tapestry",
    "profound connection between",
    # ... ~60 phrases total
]

# Build alternation pattern, longest first
import re
escaped = [re.escape(p) for p in AI_PHRASES]
escaped.sort(key=len, reverse=True)
pattern = re.compile("|".join(escaped), re.IGNORECASE)
```

**Precision:** High but not perfect. False positives occur when the phrase appears in non-AI context (e.g., quoting AI text, common tech vocabulary like "paradigm shift").

**The hard part:** You can't derive this list from regex alone. You need a curated vocabulary of known AI-overused phrases. This is the one signal where having the data matters more than the detection method.

**Verdict:** Easy to implement IF you have the phrase list. Hard if you don't. The detection itself is just string matching.

---

### 3. Em Dashes (10× multiplier) — TRIVIAL

**Detection:** Single character match.

```python
import re
EM_DASH = re.compile(r'\u2014')  # —
```

That's it. One regex line. Zero false positives.

**Precision:** Perfect. The em dash (—) is a single Unicode character. There is no ambiguity.

**Signal source:** Density. AI writes ~17-45/10k words with em dashes vs ~2-5/10k for humans.

**Verdict:** The easiest signal to detect. One character, one regex, perfect precision.

---

### 4. Bullet Lists (9× multiplier) — EASY

**Detection:** Line-start regex patterns.

```python
import re

# Unordered lists: -, *, +, • followed by whitespace
UNORDERED = re.compile(r'^[\s]*[-*+•]\s+\S.*$', re.MULTILINE)

# Numbered lists: digits. followed by whitespace
NUMBERED = re.compile(r'^[\s]*\d+\.\s+\S.*$', re.MULTILINE)
```

**Precision:** Moderate. Matches any list, not just "unnatural" AI lists. The signal comes from density and context (lists where prose would read more naturally).

**Signal source:** AI writes ~28/10k bullet items vs ~3/10k for humans. The key is detecting the list format, then assessing whether a list is appropriate for the context.

**Verdict:** Easy to detect. The hard part is contextual judgment — whether a list is "unnatural" requires comparing the list against surrounding prose.

---

### 5. Triads (4× multiplier) — MODERATE

**Detection:** Regex matching "X, Y and Z" pattern.

```python
import re
TRIAAD = re.compile(
    r"\b([^,\n]+?),\s+([^,\n]+?)\s+and\s+([^,\n.!?]+)\b",
    re.IGNORECASE
)
```

**Precision:** Low. This regex matches ANY three-item grammatical construct, not just rhetorical triads. In testing, it returned 10 matches in a ~1000-word text, many of which are mundane (e.g., "SQL, Jinja and YAML" — a tech list, not a rhetorical device).

**The problem:** The "rule of three" is a grammatically universal pattern, not an AI-specific one. Humans use it constantly: "salt, pepper, and oil". The regex cannot distinguish between a rhetorical triad and a natural three-item list.

**To improve precision:** Would require NLP — parse the sentence structure, identify if the three items are rhetorically parallel (not just syntactically parallel). This is beyond regex.

**Verdict:** Detectable but noisy. The regex finds all three-item lists; a human or classifier would be needed to judge which are "rhetorical triads" vs "natural lists".

---

### 6. "Not just X but Y" (3× multiplier) — EASY

**Detection:** Regex with greedy matching.

```python
import re
NOT_BUT = re.compile(
    r"not\s+.*?but\s+(?:also\s+)?.*?(?=[.!?]|$)",
    re.IGNORECASE | re.DOTALL
)
```

**Precision:** Moderate. The regex is greedy and may match across sentences. A more restrictive version would help.

**The problem:** The "not X but Y" construction appears in normal English: "It's not just a tool, it's a solution." The regex matches this perfectly, but it also matches false positives where "not" and "but" appear in different contexts.

**Verdict:** Easy to regex, but precision is limited by the ubiquity of the construction in normal English. The signal is one of many — no single instance is definitive.

---

### 7. Unusual Unicode (3× multiplier) — EASY

**Detection:** Character set match.

```python
import re

UNUSUAL_CHARS = {
    '\u2500': 'box drawings light horizontal',  # ─
    '\u2248': 'almost equal to',                # ≈
    '\u26A0': 'warning sign',                   # ⚠
    '\u2192': 'rightwards arrow',               # →
    # ... ~80 characters
}

for char in UNUSUAL_CHARS:
    re.finditer(re.escape(char), text)
```

**Precision:** Perfect. Each character is uniquely identifiable. Box-drawing characters (─), mathematical symbols (≈), arrow glyphs (→), and decorative characters (⚠) are virtually never typed by humans on standard keyboards.

**Signal source:** High-multiplier characters like ─ (940×) and ≈ (241×) are extremely rare in normal human text.

**Verdict:** Easy to detect. The challenge is maintaining an exhaustive list of unusual Unicode characters.

---

### 8. AI-style Headers (2× multiplier) — EASY

**Detection:** Pattern match for conversational openings.

```python
import re

AI_HEADERS = [
    r'^(?:Certainly|Of\s+course|Sure|Sure\s+thing|Happy\s+to\s+help)',
    r'^Here\'(?:s|s)\s+(?:a|an)\s+(?:breakdown|overview|summary)',
    r"I?\s+can\s+help\s+you\s+with\s+that",
    r"^Thank\s+you\s+for\s+(?:asking|your\s+(?:question|query))",
    r"^No\s+problem!",
    r"^You\s+got\s+it!",
]

combined = '|'.join(AI_HEADERS)
pattern = re.compile(combined, re.IGNORECASE | re.MULTILINE)
```

**Precision:** High for chatbot/dialogue output. Zero relevance for articles, blog posts, or formal documents.

**Signal source:** These are conversational openings typical of chatbot responses, not standalone documents.

**Verdict:** Easy to regex, but only applicable to conversational text. Irrelevant for formal documents.

---

### 9. Emojis (2× multiplier) — EASY

**Detection:** Unicode range regex + classification.

```python
import re
import unicodedata

# Unicode emoji ranges
EMOJI = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    # ... etc
]

# Classify: AI-typical vs human-typical
AI_EMOJIS = {
    '✅': 'white heavy check mark (167×)',
    '🚀': 'rocket (26×)',
    '⚠️': 'warning sign',
    # ... UI-coded glyphs
}

HUMAN_EMOJIS = {
    '😊': 'smiling face (0.6×)',
    '❤️': 'red heart (0.2×)',
    # ... faces and emotions
}
```

**Precision:** Moderate. Counting emojis is trivial. The signal is in the DISTRIBUTION — which emojis, not how many.

**Signal source:** Overall emoji count barely differs between AI and human text (2×). But AI overuses UI symbols (✅ 167×, 🔢 keycaps 61-129×) while humans use faces (😊 0.6×, ❤️ 0.2×).

**Verdict:** Easy to count. The nuanced signal (which emojis) requires classification, not just detection.

---

## Summary Table

| Signal | Regex? | Lines of Code | Precision | Key Insight |
|--------|--------|--------------|-----------|-------------|
| Em dashes | Yes | 1 | Perfect | Single character |
| Markdown | Yes | 4 | Perfect | Density is the signal |
| Unusual Unicode | Yes | ~80 chars | Perfect | Character set lookup |
| AI Phrases | List lookup | ~60 entries | High (with list) | Need curated vocabulary |
| Bullet lists | Yes | 2 | Moderate | Context matters |
| Emojis | Yes | ~50 lines | Moderate | Distribution matters |
| AI headers | Yes | ~7 patterns | High (chat only) | N/A for articles |
| Not just X but Y | Yes | 1 | Moderate | Greedy regex |
| Triads | Yes | 1 | Low | Too many false positives |

## Bottom Line

**All 9 signals are detectable via regex or simple heuristics.** The difficulty ranges from trivial (em dashes: 1 character, 1 regex line) to moderate (triads: regex catches everything, including non-rhetorical three-item lists).

**The hardest part is not the regex — it's defining what "counts":**
- For density-based signals (markdown, em dashes, bullet lists), you need baseline human vs AI rates to determine thresholds
- For pattern-based signals (triads, not-just-but), you need to distinguish rhetorical devices from natural grammar
- For phrase-based signals (AI phrases), you need a curated vocabulary

**No single signal is definitive.** Pangram's approach is to combine all signals into a single score. That's the key insight: individual regex hits are noisy, but the combination of multiple signals provides meaningful confidence.

---

## Project Structure

```
margnap/
├── detectors/
│   ├── __init__.py          # Exports all 9 detectors
│   ├── em_dash.py           # ✓ existing: em dashes
│   ├── not_just_but.py      # ✓ existing: not just but also
│   ├── triad.py             # ✓ existing: triads
│   ├── markdown.py          # ✓ new: markdown variants
│   ├── ai_phrases.py        # ✓ new: AI phrase list
│   ├── bullet_lists.py      # ✓ new: bullet/numbered lists
│   ├── unusual_unicode.py   # ✓ new: unusual Unicode chars
│   ├── ai_headers.py        # ✓ new: AI conversational openings
│   └── emojis.py            # ✓ new: emoji detection + classification
├── main.py                  # Runs all 9 detectors
├── sample_text.txt          # AI-generated DBT article (~1000 words)
├── analyze_all.py           # Full analysis script
└── analyze_matches.py       # Detailed match inspection
```

## Running the Analysis

```bash
cd margnap
uv sync
uv run python main.py          # Run all detectors
uv run python analyze_all.py   # Full analysis with verdicts
uv run python analyze_matches.py  # Inspect each match in context
```
