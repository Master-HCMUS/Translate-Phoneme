#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests cho chương trình phiên âm âm vị học tiếng Việt
"""

import unittest
import sys
import os

# Thêm đường dẫn để import module main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import (
    ToneHandler, 
    PhonemeMapper, 
    SyllableAnalyzer, 
    VietnamesePhonemeTranscriber
)


class TestToneHandler(unittest.TestCase):
    """Test class cho ToneHandler"""
    
    def setUp(self):
        self.tone_handler = ToneHandler()
    
    def test_get_tone_ngang(self):
        """Test nhận dạng thanh ngang"""
        tone_code, tone_name = self.tone_handler.get_tone("ma")
        self.assertEqual(tone_code, 0)
        self.assertEqual(tone_name, "ngang")
        
        tone_code, tone_name = self.tone_handler.get_tone("con")
        self.assertEqual(tone_code, 0)
        self.assertEqual(tone_name, "ngang")
    
    def test_get_tone_huyen(self):
        """Test nhận dạng thanh huyền"""
        tone_code, tone_name = self.tone_handler.get_tone("mà")
        self.assertEqual(tone_code, 1)
        self.assertEqual(tone_name, "huyền")
        
        tone_code, tone_name = self.tone_handler.get_tone("làm")
        self.assertEqual(tone_code, 1)
        self.assertEqual(tone_name, "huyền")
    
    def test_get_tone_sac(self):
        """Test nhận dạng thanh sắc"""
        tone_code, tone_name = self.tone_handler.get_tone("má")
        self.assertEqual(tone_code, 2)
        self.assertEqual(tone_name, "sắc")
        
        tone_code, tone_name = self.tone_handler.get_tone("tóc")
        self.assertEqual(tone_code, 2)
        self.assertEqual(tone_name, "sắc")
    
    def test_get_tone_hoi(self):
        """Test nhận dạng thanh hỏi"""
        tone_code, tone_name = self.tone_handler.get_tone("mả")
        self.assertEqual(tone_code, 3)
        self.assertEqual(tone_name, "hỏi")
        
        tone_code, tone_name = self.tone_handler.get_tone("tổ")
        self.assertEqual(tone_code, 3)
        self.assertEqual(tone_name, "hỏi")
    
    def test_get_tone_nga(self):
        """Test nhận dạng thanh ngã"""
        tone_code, tone_name = self.tone_handler.get_tone("mã")
        self.assertEqual(tone_code, 4)
        self.assertEqual(tone_name, "ngã")
        
        tone_code, tone_name = self.tone_handler.get_tone("tõm")
        self.assertEqual(tone_code, 4)
        self.assertEqual(tone_name, "ngã")
    
    def test_get_tone_nang(self):
        """Test nhận dạng thanh nặng"""
        tone_code, tone_name = self.tone_handler.get_tone("mạ")
        self.assertEqual(tone_code, 5)
        self.assertEqual(tone_name, "nặng")
        
        tone_code, tone_name = self.tone_handler.get_tone("tọc")
        self.assertEqual(tone_code, 5)
        self.assertEqual(tone_name, "nặng")
    
    def test_remove_tone_marks(self):
        """Test loại bỏ dấu thanh điệu"""
        self.assertEqual(self.tone_handler.remove_tone_marks("mà"), "ma")
        self.assertEqual(self.tone_handler.remove_tone_marks("tóc"), "toc")
        self.assertEqual(self.tone_handler.remove_tone_marks("mẹ"), "me")
        self.assertEqual(self.tone_handler.remove_tone_marks("ông"), "ong")  # ô -> o
        self.assertEqual(self.tone_handler.remove_tone_marks("ượu"), "uơu")  # ự -> u, ơ giữ nguyên, u -> u


class TestSyllableAnalyzer(unittest.TestCase):
    """Test class cho SyllableAnalyzer"""
    
    def setUp(self):
        self.analyzer = SyllableAnalyzer()
    
    def test_extract_initial_simple(self):
        """Test trích xuất âm đầu đơn giản"""
        result = self.analyzer.split_syllable("ma")
        self.assertEqual(result['initial'], 'm')
        
        result = self.analyzer.split_syllable("ba")
        self.assertEqual(result['initial'], 'b')
        
        result = self.analyzer.split_syllable("ta")
        self.assertEqual(result['initial'], 't')
    
    def test_extract_initial_complex(self):
        """Test trích xuất âm đầu phức tạp"""
        result = self.analyzer.split_syllable("pha")
        self.assertEqual(result['initial'], 'ph')
        
        result = self.analyzer.split_syllable("tha")
        self.assertEqual(result['initial'], 'th')
        
        result = self.analyzer.split_syllable("kha")
        self.assertEqual(result['initial'], 'kh')
        
        result = self.analyzer.split_syllable("nga")
        self.assertEqual(result['initial'], 'ng')
        
        result = self.analyzer.split_syllable("cha")
        self.assertEqual(result['initial'], 'ch')
        
        result = self.analyzer.split_syllable("tra")
        self.assertEqual(result['initial'], 'tr')
    
    def test_extract_initial_empty(self):
        """Test trích xuất âm đầu rỗng"""
        result = self.analyzer.split_syllable("an")
        self.assertEqual(result['initial'], '')
        
        result = self.analyzer.split_syllable("eo")
        self.assertEqual(result['initial'], '')
        
        result = self.analyzer.split_syllable("uống")
        self.assertEqual(result['initial'], '')
    
    def test_extract_final_simple(self):
        """Test trích xuất âm cuối đơn giản"""
        result = self.analyzer.split_syllable("man")
        self.assertEqual(result['final'], 'n')
        
        result = self.analyzer.split_syllable("mat")
        self.assertEqual(result['final'], 't')
        
        result = self.analyzer.split_syllable("mam")
        self.assertEqual(result['final'], 'm')
    
    def test_extract_final_complex(self):
        """Test trích xuất âm cuối phức tạp"""
        result = self.analyzer.split_syllable("manh")
        self.assertEqual(result['final'], 'nh')
        
        result = self.analyzer.split_syllable("mang")
        self.assertEqual(result['final'], 'ng')
        
        result = self.analyzer.split_syllable("mach")
        self.assertEqual(result['final'], 'ch')
        
        result = self.analyzer.split_syllable("mac")
        self.assertEqual(result['final'], 'c')
    
    def test_extract_final_empty(self):
        """Test trích xuất âm cuối rỗng"""
        result = self.analyzer.split_syllable("ma")
        self.assertEqual(result['final'], '')
        
        result = self.analyzer.split_syllable("me")
        self.assertEqual(result['final'], '')
        
        result = self.analyzer.split_syllable("mo")
        self.assertEqual(result['final'], '')
    
    def test_extract_nucleus_simple(self):
        """Test trích xuất âm chính đơn giản"""
        result = self.analyzer.split_syllable("ma")
        self.assertEqual(result['nucleus'], 'a')
        
        result = self.analyzer.split_syllable("me")
        self.assertEqual(result['nucleus'], 'e')
        
        result = self.analyzer.split_syllable("mi")
        self.assertEqual(result['nucleus'], 'i')
        
        result = self.analyzer.split_syllable("mo")
        self.assertEqual(result['nucleus'], 'o')
        
        result = self.analyzer.split_syllable("mu")
        self.assertEqual(result['nucleus'], 'u')
    
    def test_tone_recognition(self):
        """Test nhận dạng thanh điệu trong phân tích âm tiết"""
        result = self.analyzer.split_syllable("má")
        self.assertIn("sắc", result['tone'])
        
        result = self.analyzer.split_syllable("mà")
        self.assertIn("huyền", result['tone'])
        
        result = self.analyzer.split_syllable("mả")
        self.assertIn("hỏi", result['tone'])
        
        result = self.analyzer.split_syllable("mã")
        self.assertIn("ngã", result['tone'])
        
        result = self.analyzer.split_syllable("mạ")
        self.assertIn("nặng", result['tone'])


class TestPhonemeMapper(unittest.TestCase):
    """Test class cho PhonemeMapper"""
    
    def setUp(self):
        self.mapper = PhonemeMapper()
    
    def test_initial_consonants_mapping(self):
        """Test ánh xạ âm đầu"""
        self.assertEqual(self.mapper.initial_consonants['b'], '/b-/')
        self.assertEqual(self.mapper.initial_consonants['m'], '/m-/')
        self.assertEqual(self.mapper.initial_consonants['ph'], '/f-/')
        self.assertEqual(self.mapper.initial_consonants['th'], '/tʼ-/')
        self.assertEqual(self.mapper.initial_consonants['đ'], '/d-/')
        self.assertEqual(self.mapper.initial_consonants[''], '/ʔ-/')
    
    def test_vowels_mapping(self):
        """Test ánh xạ nguyên âm"""
        self.assertEqual(self.mapper.vowels['a'], '/-a-/')
        self.assertEqual(self.mapper.vowels['e'], '/-ɛ-/')
        self.assertEqual(self.mapper.vowels['ê'], '/-e-/')
        self.assertEqual(self.mapper.vowels['i'], '/-i-/')
        self.assertEqual(self.mapper.vowels['o'], '/-ɔ-/')
        self.assertEqual(self.mapper.vowels['ô'], '/-o-/')
        self.assertEqual(self.mapper.vowels['u'], '/-u-/')
        self.assertEqual(self.mapper.vowels['ư'], '/-ɯ-/')
        self.assertEqual(self.mapper.vowels['ơ'], '/-ɤ-/')
    
    def test_final_consonants_mapping(self):
        """Test ánh xạ âm cuối"""
        self.assertEqual(self.mapper.final_consonants['m'], '/-m/')
        self.assertEqual(self.mapper.final_consonants['n'], '/-n/')
        self.assertEqual(self.mapper.final_consonants['p'], '/-p/')
        self.assertEqual(self.mapper.final_consonants['t'], '/-t/')
        self.assertEqual(self.mapper.final_consonants['ng'], '/-ŋ/')
        self.assertEqual(self.mapper.final_consonants['nh'], '/-ŋ/')
        self.assertEqual(self.mapper.final_consonants['c'], '/-k/')
        self.assertEqual(self.mapper.final_consonants['ch'], '/-k/')


class TestVietnamesePhonemeTranscriber(unittest.TestCase):
    """Test class cho VietnamesePhonemeTranscriber"""
    
    def setUp(self):
        self.transcriber = VietnamesePhonemeTranscriber()
    
    def test_split_text_to_syllables(self):
        """Test tách văn bản thành âm tiết"""
        syllables = self.transcriber.split_text_to_syllables("xin chào")
        self.assertEqual(syllables, ["xin", "chào"])
        
        syllables = self.transcriber.split_text_to_syllables("tôi là sinh viên")
        self.assertEqual(syllables, ["tôi", "là", "sinh", "viên"])
        
        syllables = self.transcriber.split_text_to_syllables("Việt Nam")
        self.assertEqual(syllables, ["Việt", "Nam"])
    
    def test_transcribe_simple_syllables(self):
        """Test phiên âm các âm tiết đơn giản"""
        # Test âm tiết "ma"
        result = self.transcriber.transcribe_syllable("ma")
        self.assertEqual(result['original'], "ma")
        self.assertEqual(result['phonemes']['initial'], '/m-/')
        self.assertEqual(result['phonemes']['nucleus'], '/-a-/')
        self.assertEqual(result['phonemes']['final'], '/zero/')
        self.assertIn("ngang", result['phonemes']['tone'])
        
        # Test âm tiết "bé"
        result = self.transcriber.transcribe_syllable("bé")
        self.assertEqual(result['original'], "bé")
        self.assertEqual(result['phonemes']['initial'], '/b-/')
        self.assertEqual(result['phonemes']['nucleus'], '/-ɛ-/')
        self.assertEqual(result['phonemes']['final'], '/zero/')
        self.assertIn("sắc", result['phonemes']['tone'])
    
    def test_transcribe_complex_syllables(self):
        """Test phiên âm các âm tiết phức tạp"""
        # Test âm tiết "thành" 
        result = self.transcriber.transcribe_syllable("thành")
        self.assertEqual(result['phonemes']['initial'], '/tʼ-/')
        self.assertEqual(result['phonemes']['final'], '/-ŋ/')
        self.assertIn("huyền", result['phonemes']['tone'])  # thành có dấu huyền
        
        # Test âm tiết "phòng"
        result = self.transcriber.transcribe_syllable("phòng")
        self.assertEqual(result['phonemes']['initial'], '/f-/')
        self.assertEqual(result['phonemes']['final'], '/-ŋ/')
        self.assertIn("huyền", result['phonemes']['tone'])
        
        # Test âm tiết "trường" (dấu huyền)
        result = self.transcriber.transcribe_syllable("trường")
        self.assertEqual(result['phonemes']['initial'], '/ʈ-/')
        self.assertEqual(result['phonemes']['final'], '/-ŋ/')
        self.assertIn("huyền", result['phonemes']['tone'])  # trường có dấu huyền
    
    def test_transcribe_syllables_with_no_initial(self):
        """Test phiên âm các âm tiết không có âm đầu"""
        # Test âm tiết "ăn"
        result = self.transcriber.transcribe_syllable("ăn")
        self.assertEqual(result['phonemes']['initial'], '/ʔ-/')
        self.assertEqual(result['phonemes']['nucleus'], '/-ă-/')
        self.assertEqual(result['phonemes']['final'], '/-n/')
        
        # Test âm tiết "uống" (dấu sắc)
        result = self.transcriber.transcribe_syllable("uống")
        self.assertEqual(result['phonemes']['initial'], '/ʔ-/')
        self.assertEqual(result['phonemes']['final'], '/-ŋ/')
        self.assertIn("sắc", result['phonemes']['tone'])  # uống có dấu sắc
    
    def test_transcribe_text(self):
        """Test phiên âm toàn bộ văn bản"""
        results = self.transcriber.transcribe_text("xin chào")
        self.assertEqual(len(results), 2)
        
        # Kiểm tra âm tiết "xin"
        self.assertEqual(results[0]['original'], "xin")
        self.assertEqual(results[0]['phonemes']['initial'], '/s-/')
        self.assertEqual(results[0]['phonemes']['nucleus'], '/-i-/')
        self.assertEqual(results[0]['phonemes']['final'], '/-n/')
        
        # Kiểm tra âm tiết "chào"
        self.assertEqual(results[1]['original'], "chào")
        self.assertEqual(results[1]['phonemes']['initial'], '/c-/')
        self.assertIn("huyền", results[1]['phonemes']['tone'])
    
    def test_full_transcription_string(self):
        """Test chuỗi phiên âm hoàn chỉnh"""
        result = self.transcriber.transcribe_syllable("xin")
        transcription = result['full_transcription']
        
        # Kiểm tra chuỗi phiên âm có chứa các thành phần chính
        self.assertIn('/s-/', transcription)
        self.assertIn('/-i-/', transcription)
        self.assertIn('/-n/', transcription)
        self.assertIn('ngang', transcription)


class TestSpecialCases(unittest.TestCase):
    """Test các trường hợp đặc biệt"""
    
    def setUp(self):
        self.transcriber = VietnamesePhonemeTranscriber()
    
    def test_qu_combination(self):
        """Test tổ hợp 'qu'"""
        result = self.transcriber.transcribe_syllable("quán")  # quán có dấu sắc
        self.assertEqual(result['phonemes']['initial'], '/k-/')
        self.assertEqual(result['phonemes']['medial'], '/-w-/')
        self.assertIn("sắc", result['phonemes']['tone'])  # quán có dấu sắc
    
    def test_gi_combination(self):
        """Test tổ hợp 'gi'"""
        result = self.transcriber.transcribe_syllable("già")  # già có dấu huyền
        self.assertEqual(result['phonemes']['initial'], '/z-/')
        self.assertIn("huyền", result['phonemes']['tone'])  # già có dấu huyền
    
    def test_ng_nh_distinction(self):
        """Test phân biệt ng và nh"""
        # Test "anh" - âm cuối nh
        result = self.transcriber.transcribe_syllable("anh")
        self.assertEqual(result['phonemes']['final'], '/-ŋ/')
        
        # Test "hang" - âm cuối ng  
        result = self.transcriber.transcribe_syllable("hang")
        self.assertEqual(result['phonemes']['final'], '/-ŋ/')
    
    def test_ch_c_distinction(self):
        """Test phân biệt ch và c"""
        # Test "ách" - âm cuối ch
        result = self.transcriber.transcribe_syllable("ách")
        self.assertEqual(result['phonemes']['final'], '/-k/')
        
        # Test "ác" - âm cuối c
        result = self.transcriber.transcribe_syllable("ác")
        self.assertEqual(result['phonemes']['final'], '/-k/')


def run_tests():
    """Chạy tất cả các test cases"""
    print("=== CHẠY UNIT TESTS CHO CHƯƠNG TRÌNH PHIÊN ÂM ===\n")
    
    # Tạo test suite
    test_suite = unittest.TestSuite()
    
    # Thêm các test classes
    test_classes = [
        TestToneHandler,
        TestSyllableAnalyzer, 
        TestPhonemeMapper,
        TestVietnamesePhonemeTranscriber,
        TestSpecialCases
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Chạy tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Tóm tắt kết quả
    print(f"\n=== KẾT QUẢ TEST ===")
    print(f"Tổng số tests: {result.testsRun}")
    print(f"Thành công: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Thất bại: {len(result.failures)}")
    print(f"Lỗi: {len(result.errors)}")
    
    if result.failures:
        print("\n=== CÁC TEST THẤT BẠI ===")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n=== CÁC LỖI ===")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
