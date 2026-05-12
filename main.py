"""main.py"""

from detectors import find_em_dashes, find_not_but_also, find_triads


def main() -> None:
    """main function"""
    with open("sample_text.txt") as f:
        text = f.read()

    em_dash_count, _ = find_em_dashes(text)
    not_but_count, _ = find_not_but_also(text)
    triad_count, _ = find_triads(text)

    print(f"Number of em dashes: {em_dash_count}")
    print(f"Number of not just but also: {not_but_count}")
    print(f"Number of triads: {triad_count}")


if __name__ == "__main__":
    main()
