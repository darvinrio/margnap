#!/usr/bin/env python3
"""Deep analysis of what each detector actually matches on the sample text."""

from detectors import (
from pathlib import Path
    find_ai_phrases, find_triads, find_markdown,
    find_bullet_lists, find_em_dashes,
)

with open(Path(__file__).parent / "sample_text.txt") as f:
    text = f.read()

# === AI PHRASES ===
print("=== AI PHRASES DETAIL ===")
count, spans = find_ai_phrases(text)
print(f"Total: {count}")
for span in spans:
    start, end = span
    matched = text[start:end]
    before = text[max(0, start-40):start]
    after = text[end:end+40]
    print(f"  '{matched}'")
    print(f"    before: ...{before.strip()}...")
    print(f"    after: ...{after.strip()}...")

# === TRIADS ===
print("\n=== TRIADS DETAIL ===")
count, spans = find_triads(text)
print(f"Total: {count}")
for i, span in enumerate(spans):
    start, end = span
    matched = text[start:end].strip()
    print(f"  #{i+1} '{matched[:120]}...'")

# === MARKDOWN ===
print("\n=== MARKDOWN DETAIL ===")
total, signals = find_markdown(text)
print(f"Total: {total}")
for variant, sps in signals:
    print(f"\n  {variant}: {len(sps)} matches")
    for s in sps:
        start, end = s
        print(f"    [{start}:{end}] '{text[start:end].strip()[:60]}'")

# === BULLET LISTS ===
print("\n=== BULLET LISTS DETAIL ===")
total, signals = find_bullet_lists(text)
print(f"Total: {total}")
for variant, sps in signals:
    print(f"\n  {variant}: {len(sps)} matches")
    for s in sps:
        start, end = s
        line = text[start:end].strip()
        # Only show first 80 chars
        print(f"    [{start}:{end}] '{line[:80]}'")

# === EM DASHES ===
print("\n=== EM DASHES DETAIL ===")
count, spans = find_em_dashes(text)
print(f"Total: {count}")
for span in spans:
    start, end = span
    context = text[max(0, start-40):end+40]
    print(f"  [{start}:{end}] ...{context.strip()}...")

# === WORD COUNT ===
words = len(text.split())
print(f"\nTotal words: {words}")
print(f"Text length: {len(text)} chars")
