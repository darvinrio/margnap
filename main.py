"""main.py"""

from detectors import find_ai_phrases, find_em_dashes, find_not_but_also, find_triads


def main() -> None:
    """main function"""
    with open("sample_text.txt") as f:
        text = f.read()

    em_dash_count, _ = find_em_dashes(text)
    not_but_count, _ = find_not_but_also(text)
    triad_count, triad_list = find_triads(text)
    ai_phrase_count, ai_phrase_list = find_ai_phrases(text)

    print(f"Number of em dashes: {em_dash_count}")
    print(f"Number of not just but also: {not_but_count}")
    print(f"Number of triads: {triad_count}")
    print(f"Number of AI phrases: {ai_phrase_count}")

    # print(f"Triad list: {triad_list}")
    # print traids
    for triad in triad_list:
        print(text[triad[0] : triad[1]])

    # print(f"AI phrase list: {ai_phrase_list}")
    # print AI phrases
    for ai_phrase in ai_phrase_list:
        print(text[ai_phrase[0] : ai_phrase[1]])


if __name__ == "__main__":
    main()
