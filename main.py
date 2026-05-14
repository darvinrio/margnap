"""main.py

Test all 9 Pangram Supporting Evidence detectors against sample_text.txt.
"""

from detectors import (
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


def run_all_detectors() -> tuple[str, dict]:
    """Run all detectors and return results."""
    with open("sample_text.txt") as f:
        text = f.read()

    results = {}

    # 1. Em dashes
    count, spans = find_em_dashes(text)
    results["em_dashes"] = {"count": count, "spans": spans}

    # 2. Not just X but Y
    count, spans = find_not_but_also(text)
    results["not_just_but"] = {"count": count, "spans": spans}

    # 3. Triads
    count, spans = find_triads(text)
    results["triads"] = {"count": count, "spans": spans}

    # 4. Markdown
    total, signals = find_markdown(text)
    results["markdown"] = {"total": total, "signals": signals}

    # 5. AI Phrases
    count, spans = find_ai_phrases(text)
    results["ai_phrases"] = {"count": count, "spans": spans}

    # 6. Bullet lists
    total, signals = find_bullet_lists(text)
    results["bullet_lists"] = {"total": total, "signals": signals}

    # 7. Unusual Unicode
    count, spans, char_names = find_unusual_unicode(text)
    results["unusual_unicode"] = {"count": count, "spans": spans, "char_names": char_names}

    # 8. AI headers
    count, spans, matched = find_ai_headers(text)
    results["ai_headers"] = {"count": count, "spans": spans, "matched": matched}

    # 9. Emojis
    count, spans, emojis = find_emojis(text)
    results["emojis"] = {
        "count": count,
        "spans": spans,
        "emojis": emojis,
    }

    return text, results


def print_results(text: str, results: dict) -> None:
    """Pretty-print all detection results."""
    word_count = len(text.split())
    print("=== Pangram Supporting Evidence Detection ===")
    print(f"Text length: {len(text)} chars, ~{word_count} words\n")

    for name, data in results.items():
        print(f"--- {name.upper().replace('_', ' ')} ---")
        if "count" in data:
            print(f"  Matches: {data['count']}")
            if "spans" in data:
                for span in data["spans"][:5]:  # Show first 5
                    start, end = span
                    context = text[max(0, start-20):end+20].strip()
                    context = context.replace("\n", "\\n")
                    print(f"    [{start}:{end}] ...{context}...")
            if "char_names" in data and data["char_names"]:
                print("  Characters found:")
                for ch, name in data["char_names"][:5]:
                    print(f"    U+{ord(ch):04X} ({ch}) = {name}")
        elif "total" in data:
            print(f"  Total matches: {data['total']}")
            if "signals" in data:
                for variant, spans in data["signals"]:
                    print(f"    {variant}: {len(spans)} matches")
                    if spans:
                        for span in spans[:3]:
                            start, end = span
                            context = text[max(0, start-10):end+10].strip()
                            context = context.replace("\n", "\\n")
                            print(f"      [{start}:{end}] ...{context}...")
        if "matched" in data and data["matched"]:
            for m in data["matched"][:3]:
                print(f"    Matched: {repr(m[:80])}")
        if "emojis" in data and data["emojis"]:
            for sig in data["emojis"][:5]:
                print(f"    {sig.char} = {sig.name} ({sig.category})")

        # Calculate per 10k words
        per_10k = 0
        if word_count > 0:
            if "count" in data:
                per_10k = (data["count"] / word_count) * 10000
            elif "total" in data:
                per_10k = (data["total"] / word_count) * 10000
        print(f"  Rate: {per_10k:.1f} per 10k words\n")


if __name__ == "__main__":
    text, results = run_all_detectors()
    print_results(text, results)
