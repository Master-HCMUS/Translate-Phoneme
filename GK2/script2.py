#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sinh tất cả rimes có dấu từ rimes.txt (không dấu).
Output:
    - rimes_with_tones.txt
"""

import unicodedata

RIMES_FILE = "rimes.txt"
OUTPUT_FILE = "rimes_with_tones.txt"

# 6 thanh điệu (unicode combining)
TONES = {
    "ngang": "",
    "sắc": "\u0301",
    "huyền": "\u0300",
    "hỏi": "\u0309",
    "ngã": "\u0303",
    "nặng": "\u0323",
}

# Nguyên âm VN
VOWELS = set("aăâeêioôơuưy")

def add_tone_to_vowel(v, tone):
    if tone == "":
        return v
    return unicodedata.normalize("NFC", v + tone)

def apply_tone(rime, tone):
    """Đặt dấu vào nguyên âm cuối trong rime"""
    for i in reversed(range(len(rime))):
        if rime[i] in VOWELS:
            return rime[:i] + add_tone_to_vowel(rime[i], tone) + rime[i+1:]
    return rime

def main():
    rimes = []
    with open(RIMES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            r = line.strip()
            if r:
                rimes.append(r)

    out = []
    for r in rimes:
        for tone, mark in TONES.items():
            out.append(apply_tone(r, mark))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in out:
            f.write(r + "\n")

    print(f"Đã sinh {len(out)} rimes có dấu từ {len(rimes)} rimes gốc.")
    print(f"Kết quả lưu vào {OUTPUT_FILE}")
    print("Ví dụ 20 rime đầu:")
    for r in out[:20]:
        print(r)

if __name__ == "__main__":
    main()
