#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filter v7.3: tách từ nhiều âm tiết -> âm tiết đơn, bỏ âm tiết viết hoa
"""

import os, unicodedata
from collections import OrderedDict, defaultdict

VOWEL_MAP = {
    "a":"a","á":"a","à":"a","ả":"a","ã":"a","ạ":"a",
    "ă":"ă","ắ":"ă","ằ":"ă","ẳ":"ă","ẵ":"ă","ặ":"ă",
    "â":"â","ấ":"â","ầ":"â","ẩ":"â","ẫ":"â","ậ":"â",
    "e":"e","é":"e","è":"e","ẻ":"e","ẽ":"e","ẹ":"e",
    "ê":"ê","ế":"ê","ề":"ê","ể":"ê","ễ":"ê","ệ":"ê",
    "i":"i","í":"i","ì":"i","ỉ":"i","ĩ":"i","ị":"i",
    "o":"o","ó":"o","ò":"o","ỏ":"o","õ":"o","ọ":"o",
    "ô":"ô","ố":"ô","ồ":"ô","ổ":"ô","ỗ":"ô","ộ":"ô",
    "ơ":"ơ","ớ":"ơ","ờ":"ơ","ở":"ơ","ỡ":"ơ","ợ":"ơ",
    "u":"u","ú":"u","ù":"u","ủ":"u","ũ":"u","ụ":"u",
    "ư":"ư","ứ":"ư","ừ":"ư","ử":"ư","ữ":"ư","ự":"ư",
    "y":"y","ý":"y","ỳ":"y","ỷ":"y","ỹ":"y","ỵ":"y",
}

def normalize_rime_no_tone(rime: str) -> str:
    return "".join(VOWEL_MAP.get(ch, ch) for ch in rime)


INPUT_FILE = "data/VDic_uni.txt"
OUTPUT_FILE = "output/output_syllables.txt"
RIMES_FILE = "data/rimes.txt"
BLACKLIST_FILE = "data/blacklist.txt"
def load_blacklist():
    bl = set()
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if w:
                    bl.add(w)
    return bl

ONSETS = [
    "ngh","ng","nh","gh","gi","kh","ph","th","tr","ch",
    "qu","b","c","d","đ","g","h","k","l","m","n","p","q",
    "r","s","t","v","x"
]
ONSETS = sorted(list(set(ONSETS)), key=lambda s: -len(s))
VOWELS = set("aăâeêioôơuưy")

def load_rimes():
    rset = set()
    with open(RIMES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            r = line.strip()
            if r:
                r_nfc = unicodedata.normalize('NFC', r)
                rset.add(r_nfc)
    return rset

def try_split_onset_rime(word: str, rimes_set):
    lw = word.lower()
    for onset in ONSETS:
        if lw.startswith(onset):
            rime = lw[len(onset):]
            if not rime: continue
            rime_norm = normalize_rime_no_tone(rime)
            if rime_norm in rimes_set:
                return onset, rime_norm
    rime_norm = normalize_rime_no_tone(lw)
    if rime_norm in rimes_set:
        return "", rime_norm
    return None, None

def main():
    if not os.path.exists(INPUT_FILE):
        print("Không tìm thấy file:", INPUT_FILE)
        return


    rimes = load_rimes()
    blacklist = load_blacklist()
    found = OrderedDict()
    stats = defaultdict(int)
    examples = defaultdict(list)
    EX_MAX = 30

    total = 0
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or "\t" not in line:
                continue
            total += 1
            word = line.split("\t", 1)[0]

            for syll in word.split():
                lw = syll.lower()

                if lw in blacklist:
                    stats['blacklist'] += 1
                    if len(examples['blacklist']) < EX_MAX: examples['blacklist'].append(syll)
                    continue

                if "-" in syll:
                    stats['compound'] += 1
                    if len(examples['compound']) < EX_MAX: examples['compound'].append(syll)
                    continue

                if not any(ch in VOWELS or ch in VOWEL_MAP for ch in lw):
                    stats['no_vowel'] += 1
                    if len(examples['no_vowel']) < EX_MAX: examples['no_vowel'].append(syll)
                    continue

                onset, rime = try_split_onset_rime(syll, rimes)
                if onset is None:
                    stats['rime_not_matched'] += 1
                    if len(examples['rime_not_matched']) < EX_MAX: examples['rime_not_matched'].append(syll)
                    continue

                if lw not in found:
                    found[lw] = (onset, rime)
                    stats['kept'] += 1
                    if len(examples['kept']) < EX_MAX: examples['kept'].append(syll)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for w in found.keys():
            out.write(w + "\n")


    kept = stats['kept']
    skipped = total - kept
    report_lines = []
    report_lines.append("===== REPORT =====")
    report_lines.append(f"Total lines (with tab) read: {total}")
    report_lines.append(f"Kept (syllables): {kept}")
    report_lines.append(f"Skipped: {skipped}")
    report_lines.append("")
    report_lines.append("Breakdown:")
    for k in ['blacklist','compound','no_vowel','rime_not_matched']:
        report_lines.append(f"  {k:15s}: {stats.get(k,0)}")
    report_lines.append("")
    report_lines.append("Examples:")
    for k,v in examples.items():
        report_lines.append(f"  {k}: {', '.join(v)}")
    report_lines.append("")
    report_lines.append(f"Result saved to: {OUTPUT_FILE}")

    # Print to console
    for line in report_lines:
        print(line)

    # Write to file
    with open("output/syllable_report.txt", "w", encoding="utf-8") as rep:
        for line in report_lines:
            rep.write(line + "\n")

if __name__ == "__main__":
    main()
