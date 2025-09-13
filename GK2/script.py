#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filter v7: kiểm tra bằng danh sách VỄN (rime) hợp lệ
- INPUT: VDic_uni.txt (hardcoded)
- Optional: blacklist.txt (1 từ / dòng, lowercase)
- Optional: rimes.txt (1 rime / dòng, canonical no-tone but KEEP ăâêôơư)
- OUTPUT: syllables.txt (mỗi dòng 1 âm tiết)
- Report: số lượng giữ/loại + phân loại nguyên nhân
Notes:
- Script cố gắng tách onset (âm đầu) bằng danh sách onset chuẩn, phần còn lại là rime.
- Rime được chuẩn hóa (loại dấu thanh) rồi so với tập RIMES.
- Nếu bạn muốn đạt con số tham khảo ~6835, cần 1 file rimes.txt đầy đủ (tập vần chuẩn).
"""


import os
from collections import OrderedDict, defaultdict

# Bản đồ nguyên âm có dấu -> nguyên âm chuẩn
VOWEL_MAP = {
    # a
    "a":"a","á":"a","à":"a","ả":"a","ã":"a","ạ":"a",
    # ă
    "ă":"ă","ắ":"ă","ằ":"ă","ẳ":"ă","ẵ":"ă","ặ":"ă",
    # â
    "â":"â","ấ":"â","ầ":"â","ẩ":"â","ẫ":"â","ậ":"â",
    # e
    "e":"e","é":"e","è":"e","ẻ":"e","ẽ":"e","ẹ":"e",
    # ê
    "ê":"ê","ế":"ê","ề":"ê","ể":"ê","ễ":"ê","ệ":"ê",
    # i
    "i":"i","í":"i","ì":"i","ỉ":"i","ĩ":"i","ị":"i",
    # o
    "o":"o","ó":"o","ò":"o","ỏ":"o","õ":"o","ọ":"o",
    # ô
    "ô":"ô","ố":"ô","ồ":"ô","ổ":"ô","ỗ":"ô","ộ":"ô",
    # ơ
    "ơ":"ơ","ớ":"ơ","ờ":"ơ","ở":"ơ","ỡ":"ơ","ợ":"ơ",
    # u
    "u":"u","ú":"u","ù":"u","ủ":"u","ũ":"u","ụ":"u",
    # ư
    "ư":"ư","ứ":"ư","ừ":"ư","ử":"ư","ữ":"ư","ự":"ư",
    # y
    "y":"y","ý":"y","ỳ":"y","ỷ":"y","ỹ":"y","ỵ":"y",
}

def normalize_rime_no_tone(rime: str) -> str:
    """Chuẩn hóa rime: bỏ dấu thanh, quy về nguyên âm cơ bản"""
    return "".join(VOWEL_MAP.get(ch, ch) for ch in rime)

INPUT_FILE = "VDic_uni.txt"
OUTPUT_FILE = "syllables.txt"
BLACKLIST_FILE = "blacklist.txt"
RIMES_FILE = "rimes.txt"

# Onsets (âm đầu) phổ biến trong tiếng Việt (ưu tiên các onset dài trước)
ONSETS = [
    "ngh","ng","nh","gh","gi","kh","ng","ph","th","tr","ch","gh",
    "qu","b","c","d","đ","g","h","k","l","m","n","p","q","r","s","t","v","x","y"
]
# sắp xếp theo độ dài giảm dần để match longest-first
ONSETS = sorted(list(set(ONSETS)), key=lambda s: -len(s))

# Vietnamese vowel letters (canonical) — lowercase
VOWELS = set("aăâeêioôơuưy")

# Tags which indicate loan/foreign/prop-names in source (heuristic)
DISALLOWED_TAGS = {"Np", "E", "X"}

def load_blacklist():
    bl = set()
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if w: bl.add(w)
    return bl

def load_rimes():
    rset = set()
    with open(RIMES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            r = line.strip()
            if r: rset.add(r)
    return rset

def is_all_letters(word: str) -> bool:
    return all(ch.isalpha() for ch in word)

def try_split_onset_rime(word: str, rimes_set):
    lw = word.lower()
    for onset in sorted(ONSETS, key=lambda s: -len(s)):
        if lw.startswith(onset):
            rime = lw[len(onset):]
            if not rime: continue
            rime_norm = normalize_rime_no_tone(rime)
            if rime_norm in rimes_set:
                return onset, rime_norm
    # thử onset rỗng
    rime_norm = normalize_rime_no_tone(lw)
    if rime_norm in rimes_set:
        return "", rime_norm
    return None, None

def main():
    if not os.path.exists(INPUT_FILE):
        print("Không tìm thấy file:", INPUT_FILE)
        return

    blacklist = load_blacklist()
    rimes = load_rimes()

    found = OrderedDict()
    stats = defaultdict(int)
    examples = defaultdict(list)
    EX_MAX = 100

    total = 0
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or "\t" not in line:
                continue
            total += 1
            word, tags = line.split("\t", 1)
            word = word.strip()
            tags = tags.strip()
            lw = word.lower()

            # blacklist
            if lw in blacklist:
                stats['blacklist'] += 1
                if len(examples['blacklist']) < EX_MAX: examples['blacklist'].append(word)
                continue

            # spaces or hyphen -> composite/multi-syllable
            if "-" in word:
                stats['compound'] += 1
                if len(examples['compound']) < EX_MAX: examples['compound'].append(word)
                continue

            # tags indicating foreign/proper noun
            if any(tag in tags for tag in DISALLOWED_TAGS):
                stats['disallowed_tag'] += 1
                if len(examples['disallowed_tag']) < EX_MAX: examples['disallowed_tag'].append(word)
                continue

            # # must be letters only
            # if not is_all_letters(word):
            #     stats['invalid_chars'] += 1
            #     if len(examples['invalid_chars']) < EX_MAX: examples['invalid_chars'].append(word)
            #     continue

            # must contain at least one vietnamese vowel letter (loose)
            if not any(ch in VOWELS or ch in "áàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵêăâôơư" for ch in lw):
                stats['no_vowel'] += 1
                if len(examples['no_vowel']) < EX_MAX: examples['no_vowel'].append(word)
                continue

            # try to split onset + rime and check rime membership
            onset, rime = try_split_onset_rime(word, rimes)
            if onset is None:
                stats['rime_not_matched'] += 1
                if len(examples['rime_not_matched']) < EX_MAX: examples['rime_not_matched'].append(word)
                continue

            # passed: keep the original word
            if word not in found:
                found[word] = (onset, rime)
                stats['kept'] += 1
                if len(examples['kept']) < EX_MAX: examples['kept'].append(word)

    # write output (plain syllable list)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for w in found.keys():
            out.write(w + "\n")

    # report
    kept = stats['kept']
    skipped = total - kept
    print("===== REPORT =====")
    print("Total lines (with tab) read:", total)
    print("Kept (syllables):", kept)
    print("Skipped:", skipped)
    print()
    print("Breakdown by reason (counts):")
    for r in ['blacklist','compound','disallowed_tag','invalid_chars','no_vowel','rime_not_matched']:
        print(f"  {r:15s}: {stats.get(r,0)}")
    print()
    print("Examples per category (<=10 each):")
    for k, exs in examples.items():
        print(f"  {k} ({len(exs)}): {', '.join(exs)}")
    print()
    print("RESULT saved to:", OUTPUT_FILE)
    print()
    print("Notes:")
    print(" - If you want to reach ~6835 syllables, provide a comprehensive rimes.txt (one rime per line, canonicalized -- no tone marks, keep ăâêôơư).")
    print(" - You can also expand ONSETS if needed.")
    print(" - This script preserves original diacritics in output; matching uses canonicalized rimes (tone removed).")

if __name__ == "__main__":
    main()
