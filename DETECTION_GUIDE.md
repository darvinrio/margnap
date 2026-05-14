# Pangram Supporting Evidence — How to Detect Each Signal

Practical guide for implementing all 9 AI detection signals from Pangram's Supporting Evidence suite. Each section covers: **what the signal is**, **how to detect it**, **code example**, and **limitations**.

---

## Signal 1: Markdown (12× multiplier)

**What it is:** Markdown formatting (`**bold**`, `## Header`, `` `code` ``, `*italic*`) inserted into plain text contexts where humans rarely use it (Google Docs, email, forums).

**Detection method:** Regex — straightforward for each variant.

### Implementation

```python
import re

# Bold: **text**
BOLD = re.compile(r'\*\*(.+?)\*\*')

# Headers: # at start of line
HEADER = re.compile(r'^#{1,6}\s+', re.MULTILINE)

# Inline code: `code`
INLINE_CODE = re.compile(r'`([^`]+)`')

# Italic: single *text* (avoiding * that's part of **)
ITALIC = re.compile(r'(?<!\*)\*(?!\*)(\w[\w\s\w]*?\w)(?<!\w)\*(?!\*)')
```

### Usage

```python
def count_markdown(text):
    counts = {}
    for variant, pattern in [('bold', BOLD), ('header', HEADER),
                              ('inline_code', INLINE_CODE), ('italic', ITALIC)]:
        counts[variant] = len(pattern.findall(text))
    return counts
```

### Results on sample text (~1000 words)
- Bold: 13 (human avg: 2/10k → AI avg: 65/10k → **43×**)
- Header: 11 (human avg: 0.5/10k → AI avg: 11/10k → **23×**)
- Inline code: 3 (human avg: 0.2/10k → AI avg: 0.8/10k → **5×**)
- Italic: 0 (human avg: 5/10k → AI avg: 13/10k → **2×**)

### Verdict: **Trivial with regex.** 4 simple patterns, perfect precision.

---

## Signal 2: AI Phrases (12× multiplier)

**What it is:** Word patterns that appear far more often in AI-generated text. Examples:
- "delve into" (45×)
- "in today's fast-paced world" (35×)
- "crucial to note that" (22×)
- "navigate the tapestry of" (18×)

**Detection method:** Not regex pattern matching — use a curated phrase list. Regex is NOT the right approach because the signal is lexical (specific words), not structural.

### Implementation

```python
import re

# Curated list of AI-overused phrases (from Pangram's research)
AI_PHRASES = [
    "delve into",
    "in today's fast-paced world",
    "crucial to note that",
    "navigate the tapestry of",
    "ever-evolving landscape",
    "complex tapestry",
    "profound connection between",
    "testament to human",
    "highly recommend for anyone",
    "blurring the lines between",
    "fascinating and complex",
    "dive into",
    "play a significant role",
    "robust solution",
    # ... add more from Pangram's list (40+ phrases)
]

# Build alternation pattern, sorted longest-first to avoid partial matches
escaped_phrases = [re.escape(p) for p in AI_PHRASES]
escaped_phrases.sort(key=len, reverse=True)
pattern = re.compile("|".join(escaped_phrases), re.IGNORECASE)
```

### Usage

```python
def find_ai_phrases(text):
    matches = []
    for m in pattern.finditer(text):
        matches.append({
            'phrase': m.group(0),
            'start': m.start(),
            'end': m.end(),
            'context': text[max(0,m.start()-30):m.end()+30]
        })
    return matches
```

### Results on sample text
- Matched: "Paradigm Shift" (false positive — used in a tech article header, not as an AI cliché)
- This is the main risk: AI phrases like "paradigm shift", "game changer" have entered general tech vocabulary

### Verdict: **Not regex pattern matching — use phrase lookup.** The detection is simple string matching, but the challenge is curating the phrase list. You can't derive this from regex alone.

---

## Signal 3: Em Dashes (10× multiplier)

**What it is:** Overuse of em dashes (—) where human writers typically use commas, colons, or parentheses.

**Detection method:** Simple regex for the single em dash character.

### Implementation

```python
import re

# Em dash is U+2014 — a single Unicode character
EM_DASH = re.compile(r'\u2014')
```

### Usage

```python
def count_em_dashes(text):
    return len(EM_DASH.findall(text))

# Results on sample (~1000 words): 6 em dashes
# Human avg: 5/10k → AI avg: 17-45/10k → 3-9× multiplier
```

### Verdict: **Trivial with regex.** One character, one regex line, zero false positives.

---

## Signal 4: Bullet Lists (9× multiplier)

**What it is:** AI models prefer bullet-point lists where a human would write a simple sentence. Example:

> AI: "You make amylase in:
> - Salivary glands
> - Pancreas"
>
> Human: "Amylase is made in your salivary glands and pancreas."

**Detection method:** Regex for list markers at line starts.

### Implementation

```python
import re

# Unordered list markers: -, *, +, • at line start
UNORDERED_LIST = re.compile(r'^[\s]*[-*+•]\s+\S.*$', re.MULTILINE)

# Numbered list markers: digits. at line start
NUMBERED_LIST = re.compile(r'^[\s]*\d+\.\s+\S.*$', re.MULTILINE)
```

### Usage

```python
def count_bullet_lists(text):
    unordered = len(UNORDERED_LIST.findall(text))
    numbered = len(NUMBERED_LIST.findall(text))
    return {
        'unordered': unordered,
        'numbered': numbered,
        'total': unordered + numbered
    }

# Results on sample (~1000 words): 5 unordered + 2 numbered = 7
# Human avg: 3/10k → AI avg: 28/10k → 9× multiplier
```

### Limitations
- Matches ANY list, not just "unnatural" AI lists
- Signal is in the **density** and **context**: are lists being used where prose would read more naturally?
- Full contextual analysis requires comparing list structure against surrounding sentences

### Verdict: **Easy with regex.** Detection is straightforward; contextual judgment requires more analysis.

---

## Signal 5: Triads (4× multiplier)

**What it is:** AI overuses the "rule of three" rhetorical pattern: "past, present, and future" or "blood, sweat, and tears."

**Detection method:** Regex for three-item patterns separated by commas and "and".

### Implementation

```python
import re

# Pattern: X, Y and Z (three comma-separated items ending with "and")
TRIAAD = re.compile(
    r"\b([^,\n]+?),\s+([^,\n]+?)\s+and\s+([^,\n.!?]+)\b",
    re.IGNORECASE
)
```

### Usage

```python
def find_triads(text):
    matches = []
    for m in TRIAAD.finditer(text):
        matches.append({
            'full_match': m.group(0),
            'item1': m.group(1),
            'item2': m.group(2),
            'item3': m.group(3)
        })
    return matches
```

### Results on sample (~1000 words): 10 matches

### ⚠️ Major Limitation
This regex matches **ANY** three-item construct, not just rhetorical triads. In testing, it matched:
- "reliable, and actionable insights is arguably" → This is NOT a triad, it's just "A, and B is C"
- "Redshift, etc.). Its fundamental mission" → Also not a triad

The problem: The regex is too greedy. It catches grammatical patterns that happen to contain two commas and the word "and", not just actual rhetorical triads like "love, loss, and identity."

### Verdict: **Possible with regex but LOW precision.** The regex finds all three-item patterns, not just rhetorical ones. To improve precision would require NLP (parsing sentence structure to check if items are parallel/rhetorical vs just grammatical).

---

## Signal 6: "Not just X but Y" (3× multiplier)

**What it is:** AI overuses the "not just A, but B" contrast pattern. Example:
> "It's not just a tool — it's a framework."

**Detection method:** Regex with greedy matching between "not" and "but".

### Implementation

```python
import re

# Pattern: "not" ... some text ... "but (also)"
NOT_BUT_PATTERN = re.compile(
    r"not\s+\S.*?but\s+(?:also\s+)?\S.*?(?=[.!?]|$)",
    re.IGNORECASE | re.DOTALL
)
```

### Usage

```python
def find_not_just_but(text):
    matches = []
    for m in NOT_BUT_PATTERN.finditer(text):
        matches.append(m.group(0))
    return matches
```

### Limitations
- The regex is greedy and may match across sentence boundaries
- The "not ... but" construction appears in normal English frequently
- Example of false positive: "It's not a replacement for a warehouse; rather, it is..." → doesn't match "but" so OK, but other patterns might

### Verdict: **Easy with regex, but moderate precision.** The signal is one of many — a single instance is never definitive. Works best when combined with other signals.

---

## Signal 7: Unusual Unicode (3× multiplier)

**What it is:** Decorative/unnatural Unicode characters that don't appear on standard keyboards. Used in humanized text to bypass detectors, or by AI for formatting.

**Detection method:** Character set match against known unusual characters.

### Implementation

```python
import re

# Set of unusual Unicode characters (key ones with high multipliers)
UNUSUAL_CHARS = {
    '\u2500': 'box drawings light horizontal ─ (940×)',
    '\u2248': 'almost equal to ≈ (241×)',
    '\u26A0': 'warning sign ⚠ (57×)',
    '\u2192': 'rightwards arrow → (48×)',
    '\u2190': 'leftwards arrow ←',
    '\u2191': 'upwards arrow ↑',
    '\u2193': 'downwards arrow ↓',
    '\u2194': 'left right arrow ↔',
    '\u2264': 'less-than or equal to ≤',
    '\u2265': 'greater-than or equal to ≥',
    '\u25cf': 'black circle ●',
    '\u25cb': 'white circle ○',
    '\u2713': 'check mark ✓',
    '\u2714': 'heavy check mark ✔',
    '\u2716': 'multiplication ✖',
    '\u2717': 'heavy multiplication ✗',
    '\u2764': 'heavy black heart ❤',
    '\u3013': 'geta mark ︓',
}

def find_unusual_unicode(text):
    results = []
    for char, description in UNUSUAL_CHARS.items():
        for m in re.finditer(re.escape(char), text):
            results.append({
                'char': char,
                'description': description,
                'position': m.start()
            })
    return results
```

### Results on sample (~1000 words): 0 (no unusual Unicode present)

### Verdict: **Easy with regex.** Simple character class matching. Perfect precision (each character is uniquely identifiable). The signal is more relevant for "humanized" text where users try to bypass detectors.

---

## Signal 8: AI-style Headers (2× multiplier)

**What it is:** Overly helpful conversational openings common in AI output:
- "Certainly! Here's..."
- "Of course! I'd be happy to..."
- "Sure thing! Here's a breakdown..."
- "Great question! Here's..."

**Detection method:** Pattern match for conversational openings.

### Implementation

```python
import re

AI_HEADER_PATTERNS = [
    r'^(?:Certainly|Of\s+course|Sure|Sure\s+thing|Happy\s+to\s+help|Great\s+question|Absolutely|I\'d\s+be\s+happy\s+to|I\'m\s+happy\s+to|Let\s+me\s+help\s+you)\b.*?(?::|—|-)',
    r"^Here\'(?:s|s)\s+(?:a|an)\s+(?:breakdown|overview|summary|list|explanation|answer|response)",
    r"I?\s+can\s+help\s+you\s+with\s+that",
    r"Thank\s+you\s+for\s+(?:asking|your\s+(?:question|query|interest))",
    r"^No\s+problem!",
    r"^You\s+got\s+it!",
]

combined = '|'.join(AI_HEADER_PATTERNS)
AI_HEADER_REGEX = re.compile(combined, re.IGNORECASE | re.MULTILINE)
```

### Usage

```python
def find_ai_headers(text):
    matches = []
    for m in AI_HEADER_REGEX.finditer(text):
        matches.append({
            'matched_text': m.group(0),
            'start': m.start(),
            'end': m.end()
        })
    return matches
```

### Limitations
- Only relevant for **conversational/chatbot output**, not articles, essays, or formal documents
- The sample DBT article has 0 matches because it's not a chat response

### Verdict: **Easy with regex, but narrow scope.** Only applies to conversational text. Useless for blog posts, documentation, or essays.

---

## Signal 9: Emojis (2× multiplier)

**What it is:** AI uses emojis differently than humans. While overall emoji frequency is similar, the **types** of emojis differ wildly:

| Emoji | Type | Multiplier |
|-------|------|------------|
| ✅ | Checkmark (UI) | 167× |
| 2️⃣ | Keycap two | 129× |
| 🚀 | Rocket | 26× |
| 😊 | Smile (human) | 0.6× |
| ❤️ | Heart (human) | 0.2× |

**Detection method:** Unicode range regex + emoji classification.

### Implementation

```python
import re
import unicodedata

# Unicode emoji ranges (covers most common emoji)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # enclosed characters
    "\U00002600-\U000026FF"  # misc symbols
    "\U00002700-\U000027BF"  # dingbats (additional)
    "\U00002300-\U000023FF"  # misc technical
    "]+",
    re.UNICODE
)

# Classification dictionaries
AI_TYPICAL_EMOJIS = {
    '✅': 'white heavy check mark',
    '✔️': 'check mark',
    '🚀': 'rocket',
    '💡': 'light bulb',
    '⚠️': 'warning sign',
    '📌': 'pushpin',
    '🔗': 'link',
    '🔍': 'magnifying glass',
    '✨': 'sparkles',
    '⭐': 'star',
    '👍': 'thumbs up',
    '❌': 'cross mark',
}

HUMAN_TYPICAL_EMOJIS = {
    '😊': 'smiling face',
    '❤️': 'red heart',
    '😂': 'tears of joy',
    '😍': 'heart eyes',
    '🤔': 'thinking face',
    '👋': 'waving hand',
}

def classify_emoji(emoji_char):
    if emoji_char in AI_TYPICAL_EMOJIS:
        return 'ai_typical'
    elif emoji_char in HUMAN_TYPICAL_EMOJIS:
        return 'human_typical'
    else:
        try:
            name = unicodedata.name(emoji_char, 'unknown')
        except ValueError:
            name = 'unknown'
        return 'neutral'
```

### Usage

```python
def find_emojis(text):
    results = {
        'total': 0,
        'ai_typical': [],
        'human_typical': [],
        'neutral': [],
    }
    
    for m in EMOJI_PATTERN.finditer(text):
        emoji = m.group(0)
        category = classify_emoji(emoji)
        results['total'] += 1
        results[category].append({
            'emoji': emoji,
            'name': unicodedata.name(emoji, 'unknown'),
            'position': m.start()
        })
    
    return results
```

### Results on sample (~1000 words): 0 emojis

### Limitations
- The `EMOJI_PATTERN` regex doesn't cover all emoji (especially newer ones)
- Full emoji detection requires the `emoji` Python package (`pip install emoji`)
- The key signal is **type distribution**, not count. AI uses UI symbols (✅, 🔢) while humans use faces (😊, ❤️)

### Verdict: **Easy with regex, but incomplete coverage.** A regex covers most common emojis. For full coverage, use the `emoji` Python package. The signal is in distribution, not count.

---

## Complete Detection Summary

```
Signal                Regex?     Difficulty   Precision
───────────────────── ─────────  ──────────── ────────────
Markdown              ✓          Trivial      Perfect
AI Phrases            ✓ (lookup) Easy         High*
Em Dashes             ✓          Trivial      Perfect
Bullet Lists          ✓          Easy         Moderate
Triads                ✓          Moderate     Low
Not Just X But Y      ✓          Easy         Moderate
Unusual Unicode       ✓          Easy         Perfect
AI Headers            ✓          Easy         High**
Emojis                ✓          Easy         Moderate
```

\* AI Phrases: requires curated phrase list, not pure regex pattern
\*\* AI Headers: only applies to conversational text, not documents

## Key Takeaways

1. **All 9 signals are detectable via regex or simple string matching.** None require machine learning.

2. **Three categories of difficulty:**
   - **Trivial:** Em dashes (1 character), Markdown (4 variants), Unusual Unicode (character set)
   - **Easy:** AI Phrases (list lookup), Bullet Lists, Not Just X But Y, Emojis, AI Headers
   - **Moderate:** Triads (regex catches too many false positives)

3. **The hardest part isn't the regex — it's defining what "counts":**
   - Density-based signals need human vs AI baselines
   - Pattern-based signals need to distinguish rhetorical from grammatical patterns
   - Phrase-based signals need curated vocabulary

4. **No single signal is definitive.** The signal comes from combining all 9 into a weighted score.
