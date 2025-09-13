#!/usr/bin/env python3
# -*- coding: utf-8 -*-

VDIC_FILE = "data/VDic_uni.txt"
DIFF_EXPECTED_FILE = "test/groundtruth_only_syllables.txt"
OUTPUT_FILE = "output/groundtruth_not_in_vdic.txt"

def load_vdic_words(path):
    words = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            word, _ = line.split("\t", 1)
            for syll in word.split():
                words.add(syll.lower())
    return words

def load_list(path):
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

def main():
    vdic_words = load_vdic_words(VDIC_FILE)
    diff_expected = load_list(DIFF_EXPECTED_FILE)

    not_in_vdic = sorted(diff_expected - vdic_words)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for w in not_in_vdic:
            out.write(w + "\n")

    print(f"Found {len(not_in_vdic)} syllables in {DIFF_EXPECTED_FILE} but not in {VDIC_FILE}")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
