#!/usr/bin/env python3
"""
Final analysis: How easy is it to detect each Pangram signal via regex/heuristics?
Tests against sample_text.txt (~1003 words, AI-generated DBT article).
"""

from detectors import (
from pathlib import Path
    find_em_dashes,
    find_not_but_also,
    find_triads,
    find_markdown,
    find_ai_phrases,
    find_bullet_lists,
    find_unusual_unicode,
    find_ai_headers,
    find_emojis,
)

with open(Path(__file__).parent / "sample_text.txt") as f:
    text = f.read()

words = len(text.split())

print("=" * 80)
print("PANGRAM SUPPORTING EVIDENCE — Regex/Heuristic Detection Analysis")
print("=" * 80)
print(f"Sample: {words} words")
print()

results = []

# 1. Em dashes (10×)
count, spans = find_em_dashes(text)
results.append({
    "signal": "Em dashes",
    "multiplier": "10×",
    "detected": count,
    "per_10k": (count / words) * 10000,
    "method": "Regex: \\u2014",
    "difficulty": "TRIVIAL",
    "precision": "Perfect — em dash is a single Unicode character, no false positives possible",
    "notes": "The sample has 6 em dashes in 1003 words. The regex is one line.",
})

# 2. Not just X but Y (3×)
count, spans = find_not_but_also(text)
results.append({
    "signal": "\"Not just X but Y\"",
    "multiplier": "3×",
    "detected": count,
    "per_10k": (count / words) * 10000,
    "method": "Regex: `not.*?but also` (with wildcards)",
    "difficulty": "EASY",
    "precision": "Good — but the regex `not\\s+.*?but also` is greedy and may over-match across sentences",
    "notes": "0 in sample. The sample has \"not a replacement for; rather, it is\" which doesn't match the pattern. The existing regex has a bug: `not\\s+\\s+` (double \\s+).",
})

# 3. Triads (4×)
count, spans = find_triads(text)
results.append({
    "signal": "Triads",
    "multiplier": "4×",
    "detected": count,
    "per_10k": (count / words) * 10000,
    "method": "Regex: `X, Y and Z` (three items separated by comma+and)",
    "difficulty": "MODERATE",
    "precision": "LOW — matches ANY three-item list, not just rhetorical triads. Returns 10 for a ~1000 word text, many are mundane lists like \"SQL, Jinja and YAML\" or \"Python-based engine. It compiles the project and runs the transformation graph\" (which shouldn't match at all — the regex is too greedy).",
    "notes": "The sample text is AI-generated, so it has many natural triads. The regex `([^,\\n]+?),\\s+([^,\\n]+?)\\s+and\\s+([^,\\n.!?]+)\\b` is far too broad. It catches grammatical patterns that are not the 'rule of three' rhetorical device.",
})

# 4. Markdown (12×)
total, signals = find_markdown(text)
results.append({
    "signal": "Markdown",
    "multiplier": "12×",
    "detected": total,
    "per_10k": (total / words) * 10000,
    "method": "Regex: \\*\\*text\\*, #header, `code`, *italic*",
    "difficulty": "EASY",
    "precision": "HIGH — each variant is a distinct regex. Bold (**), headers (#), inline code (`), italic (*) are each trivially detectable.",
    "notes": f"Bold: 13, Headers: 11, Inline code: 3. The density (269 per 10k) is the key signal, not presence. Humans write ~8/10k, AI writes ~90/10k.",
})

# 5. AI Phrases (12×)
count, spans = find_ai_phrases(text)
results.append({
    "signal": "AI Phrases",
    "multiplier": "12×",
    "detected": count,
    "per_10k": (count / words) * 10000,
    "method": "Pattern match against curated phrase list (~60 phrases)",
    "difficulty": "EASY (if you have the list), HARD (if you don't)",
    "precision": "HIGH — each phrase is individually verifiable",
    "notes": f"Matched 'Paradigm Shift' in 'The Paradigm Shift: Software Engineering for Data'. This is actually from the sample's own content (it's a section header about DBT's paradigm shift — not an AI phrase, but matches because 'paradigm shift' is a common AI phrase). False positive risk is real with substring matching.",
})

# 6. Bullet lists (9×)
total, signals = find_bullet_lists(text)
results.append({
    "signal": "Bullet lists",
    "multiplier": "9×",
    "detected": total,
    "per_10k": (total / words) * 10000,
    "method": "Regex: line starts with [-*+] or digit.+ followed by content",
    "difficulty": "EASY",
    "precision": "MODERATE — matches any list, not just AI-typical ones. The signal is in the DENSITY and CONTEXT (lists where prose would be more natural).",
    "notes": f"5 unordered, 2 numbered. The regex is straightforward: `^[-*+•]\\s+` and `^\\d+\\.\\s+`.",
})

# 7. Unusual Unicode (3×)
count, spans, char_names = find_unusual_unicode(text)
results.append({
    "signal": "Unusual Unicode",
    "multiplier": "3×",
    "detected": count,
    "per_10k": (count / words) * 10000,
    "method": "Character class match against known unusual Unicode chars",
    "difficulty": "EASY",
    "precision": "HIGH — each character is individually identifiable",
    "notes": "0 in sample. This signal is more relevant for 'humanized' text (where users try to bypass detectors by adding decorative Unicode). Top offenders: ─ (940×), ≈ (241×), ⚠ (57×), → (48×).",
})

# 8. AI-style headers (2×)
count, spans, matched = find_ai_headers(text)
results.append({
    "signal": "AI-style headers",
    "multiplier": "2×",
    "detected": count,
    "per_10k": (count / words) * 10000,
    "method": "Pattern match for conversational openings: 'Certainly!', 'Here's a breakdown', etc.",
    "difficulty": "MODERATE",
    "precision": "HIGH for conversational text, N/A for articles/essays",
    "notes": "0 in sample. This signal is primarily relevant for chatbot/dialogue output, not formal documents. The sample is an article, not a chat response.",
})

# 9. Emojis (2×)
count, spans, emojis = find_emojis(text)
results.append({
    "signal": "Emojis",
    "multiplier": "2×",
    "detected": count,
    "per_10k": (count / words) * 10000,
    "method": "Unicode range regex for emoji characters + classification",
    "difficulty": "EASY",
    "precision": "MODERATE — counting emojis is easy, but the signal is in the DISTRIBUTION (which emojis, not how many)",
    "notes": "0 in sample. The AI-typical emojis are: ✅ (167×), 2️⃣ (129×), 🚀 (26×), etc. Human-typical: 😊 (0.6×), ❤️ (0.2×). Overall emoji count barely differs (2×), but WHICH emojis differ wildly.",
})

# Print summary table
print(f"{'Signal':<22} {'Multiplier':<12} {'Detected':<10} {'Per 10k':<10} {'Difficulty':<12}")
print("-" * 80)
for r in results:
    print(f"{r['signal']:<22} {r['multiplier']:<12} {r['detected']:<10} {r['per_10k']:<10.1f} {r['difficulty']:<12}")

print()
print("=" * 80)
print("SUMMARY: Detection Difficulty Assessment")
print("=" * 80)
print()

for r in results:
    print(f"\n### {r['signal']} ({r['multiplier']})")
    print(f"  Method:     {r['method']}")
    print(f"  Difficulty: {r['difficulty']}")
    print(f"  Precision:  {r['precision']}")
    print(f"  Found:      {r['detected']} instances in {words} words ({r['per_10k']:.1f}/10k)")
    print(f"  Notes:      {r['notes']}")

print()
print("=" * 80)
print("CONCLUSIONS")
print("=" * 80)
print("""
1. TRIVIALLY EASY (regex-based, high precision):
   - Em dashes: Single Unicode character. One regex line. Zero false positives.
   - Unusual Unicode: Character class. One regex. Zero false positives.
   - Markdown: 4 variants, each trivially regex-able. Precision is perfect;
     the signal is density, not presence.

2. EASY (regex-based, good precision):
   - AI Phrases: Curated phrase list. Each phrase is a simple substring match.
     Risk: false positives when the phrase appears in non-AI context (e.g.
     quoting AI text, using common tech phrases).
   - Bullet lists: Line-start regex. Easy. Signal is density + context.
   - Emojis: Unicode range regex. Easy. Signal is type distribution, not count.
   - AI headers: Pattern match for conversational openings. Easy for chat
     output; irrelevant for articles/docs.

3. MODERATE (regex-based, lower precision):
   - Triads: The "X, Y and Z" pattern is grammatically ubiquitous. The regex
     catches ANY three-item construct, not just rhetorical triads. To improve
     precision would require NLP (parse the sentence structure and check if
     the three items are rhetorically parallel).
   - Not just X but Y: Similar issue — the "not ... but" pattern appears in
     normal English. The regex is overly greedy across sentences.

4. NOT POSSIBLE VIA REGEX alone:
   - None of the 9 signals are truly impossible via regex. However, some need
     contextual understanding to be precise. For example, detecting whether
     a list is "unnatural" (signal: bullet lists) requires comparing the list
     against the surrounding prose. Similarly, AI phrases need a curated list.

BOTTOM LINE:
All 9 signals are detectable via regex/heuristics. The easiest are those
based on single Unicode characters (em dashes, unusual Unicode). The hardest
are those based on rhetorical patterns (triads, not-just-but) where the
same surface pattern appears in normal human writing. The key insight from
Pangram is that no single signal is definitive — it's the COMBINATION of
signals that matters.
""")
