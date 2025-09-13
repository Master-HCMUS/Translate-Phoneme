#!/usr/bin/env python3
# -*- coding: utf-8 -*-

EXPECTED_FILE = "data/groundtruth_syllables.txt"
OTHER_FILE = "output/output_syllables.txt"
OUTPUT_FILE = "test/output_only_syllables.txt"

def load_words(path):
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}

def main():
    expected = load_words(EXPECTED_FILE)
    other = load_words(OTHER_FILE)


    diff = sorted(other - expected)
    diff_expected = sorted(expected - other)


    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for w in diff:
            if not any(ch.isupper() for ch in w):
                out.write(w + "\n")

    with open("test/groundtruth_only_syllables.txt", "w", encoding="utf-8") as out:
        for w in diff_expected:
            if not any(ch.isupper() for ch in w):
                out.write(w + "\n")

    print(f"Found {len(diff)} syllables in {OTHER_FILE} but not in {EXPECTED_FILE}")
    print(f"Saved to {OUTPUT_FILE}")
    print(f"Found {len(diff_expected)} syllables in {EXPECTED_FILE} but not in {OTHER_FILE}")
    print(f"Saved to test/groundtruth_only_syllables.txt")

if __name__ == "__main__":
    main()
