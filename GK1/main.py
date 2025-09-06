# -*- coding: utf-8 -*-
import re
import unicodedata
from typing import List, Dict, Tuple, Optional

# =========================
# 1) Cấu hình âm vị mặc định
# =========================

PHONEME_CHOICES = {
    # Các phụ âm đầu có nhiều lựa chọn — lấy lựa chọn đầu tiên trong bảng bạn đưa
    "kh": "/χ/",      # có thể đổi thành "/x/" hoặc "/kʰ/"
    "th": "/tʰ/",     # có thể đổi thành "/t’/" (ở đây chọn /tʰ/)
    "tr": "/ʈ/",      # có thể đổi thành "/ʈ͡ʂ/"
    "ch": "/c/",      # có thể đổi thành "/t/" (cho âm đầu); với âm cuối 'ch' ta cũng dùng /c/
    "d_or_gi": "/z/",
    "o_or_u_as_w": "/w/",
    "i_or_y_as_j": "/j/",
    "o_letter": "/ɔ/",
    "u_letter": "/u/",
    "i_letter": "/i/",
    "y_letter": "/i/",  # 'y' = /i/ khi là nguyên âm
    "o_hat": "/o/",     # ô
    "o_horn": "/ɤ/",    # ơ
    "u_horn": "/ɯ/",    # ư
    "a_breve": "/ă/",   # ă
    "a_circ": "/ɤ̆/",   # â (chọn /ɤ̆/ thay vì /ə̆/)
    "e_letter": "/ε/",
    "e_hat": "/e/",
    "a_letter": "/a/",
    # Diphthongs (chọn dạng đầu)
    "ie": "/ie/",       # hoặc /iə/
    "uo": "/uo/",       # hoặc /uə/
    "ɯɤ": "/ɯɤ/",      # hoặc /ɯə/ hoặc /ɨə/
}

# Map phụ âm đầu (ưu tiên khớp dài nhất)
INITIAL_MULTI = [
    ("ngh", "/ŋ/"),
    ("gh",  "/ɣ/"),
    ("ng",  "/ŋ/"),
    ("nh",  "/ɲ/"),
    ("kh",  PHONEME_CHOICES["kh"]),
    ("th",  PHONEME_CHOICES["th"]),
    ("tr",  PHONEME_CHOICES["tr"]),
    ("ph",  "/f/"),
    ("ch",  PHONEME_CHOICES["ch"]),
    ("gi",  PHONEME_CHOICES["d_or_gi"]),
    ("qu",  None),  # xử lý đặc biệt: /k/ + /w/
]

INITIAL_SINGLE = {
    "b": "/b/",
    "c": "/k/",
    "k": "/k/",
    "q": "/k/",   # nếu đơn lẻ (hiếm), còn "qu" xử lý riêng
    "đ": "/d/",
    "g": "/ɣ/",
    "h": "/h/",
    "l": "/l/",
    "m": "/m/",
    "n": "/n/",
    "p": "/p/",
    "r": "/ʐ/",
    "s": "/ʂ/",
    "t": "/t/",
    "v": "/v/",
    "x": "/s/",
    "d": PHONEME_CHOICES["d_or_gi"],  # d → /z/
}

# Âm cuối (ưu tiên chuỗi 2 ký tự trước)
CODA_MULTI = {
    "nh": "/ɲ/",
    "ng": "/ŋ/",
    "ch": "/c/",
}
CODA_SINGLE = {
    "c": "/k/",
    "m": "/m/",
    "n": "/n/",
    "p": "/p/",
    "t": "/t/",
}

# Diphthong (vần lõi)
DIPHTHONGS = {
    # iê ~ ia ~ yê
    "iê": PHONEME_CHOICES["ie"],
    "ia": PHONEME_CHOICES["ie"],
    "yê": PHONEME_CHOICES["ie"],

    # uô ~ ua
    "uô": PHONEME_CHOICES["uo"],
    "ua": PHONEME_CHOICES["uo"],

    # ươ ~ ưa
    "ươ": PHONEME_CHOICES["ɯɤ"],
    "ưa": PHONEME_CHOICES["ɯɤ"],
}

# Nguyên âm đơn
MONO_VOWELS = {
    "a": PHONEME_CHOICES["a_letter"],
    "ă": PHONEME_CHOICES["a_breve"],
    "â": PHONEME_CHOICES["a_circ"],
    "e": PHONEME_CHOICES["e_letter"],
    "ê": PHONEME_CHOICES["e_hat"],
    "i": PHONEME_CHOICES["i_letter"],
    "y": PHONEME_CHOICES["y_letter"],
    "o": PHONEME_CHOICES["o_letter"],
    "ô": PHONEME_CHOICES["o_hat"],
    "ơ": PHONEME_CHOICES["o_horn"],
    "u": PHONEME_CHOICES["u_letter"],
    "ư": PHONEME_CHOICES["u_horn"],
}

VOWEL_CHARS = set("aăâeêioôơuưy")

# Tone marks (NFD combining)
TONE_MAP = {
    "\u0301": "sắc",   # acute
    "\u0300": "huyền", # grave
    "\u0309": "hỏi",   # hook above
    "\u0303": "ngã",   # tilde
    "\u0323": "nặng",  # dot below
}
TONE_DEFAULT = "ngang"

PUNCT_SPLIT = re.compile(r"(\w+|[^\w\s]+)", re.UNICODE)

# =========================
# 2) Utility: bỏ dấu thanh nhưng giữ chất lượng nguyên âm
# =========================

def detone_keep_quality(s: str) -> Tuple[str, str]:
    """
    Bỏ dấu thanh (sắc/huyền/hỏi/ngã/nặng) nhưng giữ ă, â, ê, ô, ơ, ư.
    Trả về (chuỗi đã bỏ thanh, tone_name).
    Nếu có nhiều dấu thanh (không chuẩn), ưu tiên dấu gặp cuối.

    VD: input "học" -> "hoc", "nặng"
    """
    tone = TONE_DEFAULT
    out = []
    for ch in unicodedata.normalize("NFD", s):
        if ch in TONE_MAP:
            tone = TONE_MAP[ch]
            continue
        out.append(ch)
    detoned = unicodedata.normalize("NFC", "".join(out))
    return detoned, tone

# =========================
# 3) Phân tích 1 âm tiết
# =========================

def parse_initial(s: str) -> Tuple[List[str], str]:
    """
    Tách âm đầu theo bảng. Trả về ([phonemes], rest_str).
    VD: input "hoc" -> (["/h/", "oc"], "")
    """
    s_lower = s.lower()

    for pref, ph in INITIAL_MULTI:
        if s_lower.startswith(pref):
            if pref == "qu":
                # qu → /k/ + /w/
                return ["/k/", PHONEME_CHOICES["o_or_u_as_w"]], s[len(pref):]
            return [ph], s[len(pref):]

    if s_lower and s_lower[0] in INITIAL_SINGLE:
        return [INITIAL_SINGLE[s_lower[0]]], s[1:]

    return [], s  # không có âm đầu

def parse_coda(s: str) -> Tuple[str, List[str]]:
    """
    Tách âm cuối. Trả về (rest, [phonemes]).
    VD: input "oc" -> ("o", ["/k/"])
    """
    s_lower = s.lower()
    # ưu tiên 2 ký tự
    for suf, ph in CODA_MULTI.items():
        if s_lower.endswith(suf):
            return s[:-len(suf)], [ph]
    if s_lower and s_lower[-1] in CODA_SINGLE:
        return s[:-1], [CODA_SINGLE[s_lower[-1]]]
    return s, []

def try_match_diphthong(core: str) -> Optional[str]:
    """Nếu core bắt đầu bằng 1 diphthong trong bảng, trả về phoneme, ngược lại None."""
    core_lower = core.lower()
    # ưu tiên chuỗi 2-3 ký tự dài hơn
    for pat in sorted(DIPHTHONGS.keys(), key=len, reverse=True):
        if core_lower.startswith(pat):
            return DIPHTHONGS[pat]
    return None

def parse_rhyme(core: str) -> List[str]:
    """
    Phân tích vần (bán nguyên âm + nguyên âm đôi/đơn + bán nguyên âm).
    Quy tắc:
      - Ưu tiên 3 diphthong: iê/ia/yê; uô/ua; ươ/ưa.
      - Bán nguyên âm đầu: 'o'/'u' trước nguyên âm chính → /w/
      - Bán nguyên âm cuối: 'i'/'y' → /j/; 'o'/'u' → /w/
      - Nếu không khớp đặc biệt: map từng nguyên âm đơn còn lại.
    """
    phonemes: List[str] = []
    rest = core

    # Bán nguyên âm đầu (o/u → /w/) nếu còn ≥2 ký tự và ký tự sau là nguyên âm
    if len(rest) >= 2 and rest[0].lower() in ("o", "u") and rest[1].lower() in VOWEL_CHARS:
        phonemes.append(PHONEME_CHOICES["o_or_u_as_w"])
        rest = rest[1:]

    # Diphthong
    diph = try_match_diphthong(rest)
    if diph:
        phonemes.append(diph)
        rest = rest[2:] if len(rest) >= 2 else ""
        # Trường hợp 'iê'/'yê' dài 2 ký tự, 'uô' cũng 2, 'ươ' cũng 2.
        # Với 'ia'/'ua'/'ưa' cũng 2. (Nếu muốn an toàn tuyệt đối, có thể
        # tính chính xác độ dài theo pattern, nhưng 2 là đủ ở đây.)
    else:
        # Không phải diphthong: map nguyên âm đơn (có thể 1-2 ký tự do ê/ô/ơ/ư/â/ă)
        if not rest:
            return phonemes
        # Nếu còn ≥2 ký tự và ký tự đầu là nguyên âm hợp lệ (kể cả ê/ô/ơ/ư/â/ă)
        # ta map ký tự đầu tiên là âm chính
        ch0 = rest[0]
        ph = MONO_VOWELS.get(ch0.lower())
        if ph:
            phonemes.append(ph)
            rest = rest[1:]
        else:
            # Nếu gặp chữ không phải nguyên âm đơn hợp lệ (ví dụ trường hợp ngoại lệ),
            # ta thử map từng ký tự nguyên âm có thể nhận diện, bỏ qua ký tự lạ.
            consumed = False
            for i, c in enumerate(rest):
                ph_i = MONO_VOWELS.get(c.lower())
                if ph_i:
                    phonemes.append(ph_i)
                    rest = rest[i+1:]
                    consumed = True
                    break
            if not consumed:
                # không tìm thấy nguyên âm → giữ nguyên (fallback)
                rest = ""

    # Bán nguyên âm cuối: ưu tiên i/y → /j/, sau đó o/u → /w/
    if rest:
        last = rest[-1].lower()
        if last in ("i", "y"):
            phonemes.append(PHONEME_CHOICES["i_or_y_as_j"])
            rest = rest[:-1]
        elif last in ("o", "u"):
            phonemes.append(PHONEME_CHOICES["o_or_u_as_w"])
            rest = rest[:-1]

    # Nếu vẫn còn ký tự nguyên âm chưa tiêu thụ (trường hợp hiếm), map tiếp
    while rest:
        c = rest[0]
        ph = MONO_VOWELS.get(c.lower())
        if ph:
            phonemes.append(ph)
        # Ký tự không nhận diện thì bỏ qua
        rest = rest[1:]

    return phonemes

def transcribe_syllable(syl: str) -> Dict[str, object]:
    """
    Phiên âm 1 âm tiết. VD: "tường" -> Trả về:
      {
        "syllable": <âm tiết gốc>,
        "phonemes": ["/ʈ/", "/ɯɤ/", "/ŋ/"],
        "tone": "huyền" | "sắc" | "ngang" | ...
      }
    """
    original = syl
    # Bỏ dấu thanh, giữ ă â ê ô ơ ư
    detoned, tone = detone_keep_quality(syl)

    # tách âm đầu
    onset_ph, rest1 = parse_initial(detoned)

    # tách âm cuối
    core, coda_ph = parse_coda(rest1)

    # vần
    rhyme_ph = parse_rhyme(core)

    phonemes = onset_ph + rhyme_ph + coda_ph
    # lọc rỗng
    phonemes = [p for p in phonemes if p]

    return {
        "syllable": original,
        "phonemes": phonemes,
        "tone": tone
    }

# =========================
# 4) Phiên âm toàn văn bản
# =========================

def split_tokens(text: str) -> List[str]:
    """
    Cắt thành token giữ dấu câu. Ví dụ: "Trường, học!" -> ["Trường", ",", "học", "!"]
    """
    parts = PUNCT_SPLIT.findall(text)
    # Gộp khoảng trắng đơn giản bằng cách thêm khi in
    return [p for p in parts if p and not p.isspace()]

def is_candidate_syllable(tok: str) -> bool:
    # Heuristic: nếu có ký tự chữ cái tiếng Việt/Latin
    return any(ch.isalpha() for ch in tok)

def transcribe_text(text: str) -> List[Dict[str, object]]:
    """
    Phiên âm toàn văn bản: mỗi âm tiết (token chữ) → 1 bản ghi.
    Dấu câu/khác sẽ được trả lại như mục 'raw' (không phiên âm).
    """
    tokens = split_tokens(text)
    result = []
    for t in tokens:
        if is_candidate_syllable(t):
            result.append(transcribe_syllable(t))
        else:
            result.append({"raw": t})
    return result

def pretty_print(items: List[Dict[str, object]]) -> str:
    """
    In đẹp: mỗi âm tiết -> "âm_tiết: /.../ /.../ (/tone)"
    Giữ nguyên dấu câu.
    """
    out = []
    for it in items:
        if "raw" in it:
            out.append(it["raw"])
        else:
            syl = it["syllable"]
            ph = " ".join(it["phonemes"])
            tone = it["tone"]
            out.append(f"{syl} -> {ph} ({tone})")
    return "\n".join(out)

# =========================
# 5) Demo & test nhanh
# =========================

if __name__ == "__main__":
    samples = [
        "Trường đại học Bách Khoa",
        "khoa học dữ liệu",
        "nghiên cứu trí tuệ nhân tạo",
        "Quốc gia giàu đẹp!",
        "học, hành; chăm-chỉ.",
        "Alexander Rhodes"
    ]
    for s in samples:
        print("====", s)
        items = transcribe_text(s)
        print(pretty_print(items))
        print()