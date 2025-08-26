# -*- coding: utf-8 -*-
import unittest

from main import (
    detone_keep_quality,
    parse_initial,
    parse_coda,
    try_match_diphthong,
    parse_rhyme,
    transcribe_syllable,
    split_tokens,
    is_candidate_syllable,
    transcribe_text,
    pretty_print,
)


class TestDetone(unittest.TestCase):
    def test_detone_keeps_quality_and_extracts_tone(self):
        # học -> hoc, tone nặng
        detoned, tone = detone_keep_quality("học")
        self.assertEqual(detoned, "hoc")
        self.assertEqual(tone, "nặng")

    def test_detone_removes_tilde(self):
        # ngã -> nga, tone ngã
        detoned, tone = detone_keep_quality("ngã")
        self.assertEqual(detoned, "nga")
        self.assertEqual(tone, "ngã")


class TestInitialAndCoda(unittest.TestCase):
    def test_parse_initial_simple(self):
        ph, rest = parse_initial("hoc")
        self.assertEqual(ph, ["/h/"])
        self.assertEqual(rest, "oc")

    def test_parse_initial_qu(self):
        ph, rest = parse_initial("quoc")
        self.assertEqual(ph, ["/k/", "/w/"])
        self.assertEqual(rest, "oc")

    def test_parse_initial_tr_case_insensitive(self):
        ph, rest = parse_initial("Truong")
        self.assertEqual(ph, ["/ʈ/"])
        self.assertEqual(rest, "uong")

    def test_parse_coda_multi(self):
        rest, ph = parse_coda("anh")
        self.assertEqual(rest, "a")
        self.assertEqual(ph, ["/ɲ/"])

    def test_parse_coda_single(self):
        rest, ph = parse_coda("oc")
        self.assertEqual(rest, "o")
        self.assertEqual(ph, ["/k/"])


class TestDiphthongAndRhyme(unittest.TestCase):
    def test_try_match_diphthong(self):
        self.assertEqual(try_match_diphthong("iêp"), "/ie/")
        self.assertEqual(try_match_diphthong("uôc"), "/uo/")
        self.assertEqual(try_match_diphthong("ươm"), "/ɯɤ/")

    def test_parse_rhyme_with_onset_glide(self):
        # 'oa' -> /w/ + /a/
        self.assertEqual(parse_rhyme("oa"), ["/w/", "/a/"])

    def test_parse_rhyme_diphthong(self):
        # 'iê' -> /ie/
        self.assertEqual(parse_rhyme("iê"), ["/ie/"])

    def test_parse_rhyme_trailing_glide(self):
        # 'uoi' -> /w/ + /ɔ/ + /j/
        self.assertEqual(parse_rhyme("uoi"), ["/w/", "/ɔ/", "/j/"])

    def test_parse_rhyme_uo_with_tone_variants(self):
        # 'ươ' -> /ɯɤ/
        self.assertEqual(parse_rhyme("ươ"), ["/ɯɤ/"])


class TestTranscribeSyllable(unittest.TestCase):
    def test_transcribe_syllable_truong(self):
        res = transcribe_syllable("Trường")
        self.assertEqual(res["syllable"], "Trường")
        self.assertEqual(res["tone"], "huyền")
        self.assertEqual(res["phonemes"], ["/ʈ/", "/ɯɤ/", "/ŋ/"])

    def test_transcribe_syllable_quoc(self):
        res = transcribe_syllable("quốc")
        self.assertEqual(res["tone"], "sắc")
        # qu -> /k/ /w/, 'ô' -> /o/, 'c' -> /k/
        self.assertEqual(res["phonemes"], ["/k/", "/w/", "/o/", "/k/"])

    def test_transcribe_syllable_hoc(self):
        res = transcribe_syllable("học")
        self.assertEqual(res["tone"], "nặng")
        self.assertEqual(res["phonemes"], ["/h/", "/ɔ/", "/k/"])


class TestTextHelpers(unittest.TestCase):
    def test_split_tokens(self):
        s = "Trường, học!"
        self.assertEqual(split_tokens(s), ["Trường", ",", "học", "!"])

    def test_is_candidate_syllable(self):
        self.assertTrue(is_candidate_syllable("abc"))
        self.assertTrue(is_candidate_syllable("Đ"))
        self.assertFalse(is_candidate_syllable("!!!"))
        self.assertFalse(is_candidate_syllable("123"))

    def test_transcribe_text_and_pretty_print(self):
        s = "Trường, học!"
        items = transcribe_text(s)
        # 4 tokens: word, comma, word, exclam
        self.assertEqual(len(items), 4)
        self.assertIn("syllable", items[0])
        self.assertIn("raw", items[1])
        self.assertIn("syllable", items[2])
        self.assertIn("raw", items[3])
        # Pretty print should include tone text
        pp = pretty_print(items)
        self.assertIn("Trường ->", pp)
        self.assertIn("(huyền)", pp)


if __name__ == "__main__":
    unittest.main()
