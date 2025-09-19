#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chương trình phiên âm âm vị học tiếng Việt
Chuyển đổi văn bản tiếng Việt thành ký hiệu âm vị (gần-IPA) kèm thanh điệu
"""

import re
import unicodedata
from typing import List, Tuple, Dict, Optional


class ToneHandler:
    """Xử lý nhận dạng và phân loại thanh điệu tiếng Việt"""
    
    def __init__(self):
        # Bảng ánh xạ từ ký tự có dấu sang thanh điệu
        self.tone_marks = {
            # Thanh ngang (0) - không dấu
            'a': 0, 'ă': 0, 'â': 0, 'e': 0, 'ê': 0, 'i': 0, 'o': 0, 'ô': 0, 'ơ': 0, 'u': 0, 'ư': 0, 'y': 0,
            
            # Thanh huyền (1)
            'à': 1, 'ằ': 1, 'ầ': 1, 'è': 1, 'ề': 1, 'ì': 1, 'ò': 1, 'ồ': 1, 'ờ': 1, 'ù': 1, 'ừ': 1, 'ỳ': 1,
            
            # Thanh sắc (2)
            'á': 2, 'ắ': 2, 'ấ': 2, 'é': 2, 'ế': 2, 'í': 2, 'ó': 2, 'ố': 2, 'ớ': 2, 'ú': 2, 'ứ': 2, 'ý': 2,
            
            # Thanh hỏi (3)
            'ả': 3, 'ẳ': 3, 'ẩ': 3, 'ẻ': 3, 'ể': 3, 'ỉ': 3, 'ỏ': 3, 'ổ': 3, 'ở': 3, 'ủ': 3, 'ử': 3, 'ỷ': 3,
            
            # Thanh ngã (4)
            'ã': 4, 'ẵ': 4, 'ẫ': 4, 'ẽ': 4, 'ễ': 4, 'ĩ': 4, 'õ': 4, 'ỗ': 4, 'ỡ': 4, 'ũ': 4, 'ữ': 4, 'ỹ': 4,
            
            # Thanh nặng (5)
            'ạ': 5, 'ặ': 5, 'ậ': 5, 'ẹ': 5, 'ệ': 5, 'ị': 5, 'ọ': 5, 'ộ': 5, 'ợ': 5, 'ụ': 5, 'ự': 5, 'ỵ': 5
        }
        
        # Tên thanh điệu
        self.tone_names = ['ngang', 'huyền', 'sắc', 'hỏi', 'ngã', 'nặng']
        
        # Ký hiệu thanh điệu theo chuẩn IPA
        self.tone_symbols = ['˧', '˨˩', '˧˥', '˧˩˧', '˧ˀ˥', '˧ˀ']
    
    def get_tone(self, syllable: str) -> Tuple[int, str]:
        """
        Xác định thanh điệu của âm tiết
        
        Args:
            syllable: Âm tiết tiếng Việt
            
        Returns:
            Tuple của (mã thanh điệu, tên thanh điệu)
        """
        # Tìm tất cả thanh điệu trong âm tiết và chọn thanh điệu khác thanh ngang đầu tiên
        tones_found = []
        for char in syllable.lower():
            if char in self.tone_marks:
                tone_code = self.tone_marks[char]
                tones_found.append(tone_code)
        
        # Nếu có thanh điệu khác thanh ngang (0), ưu tiên thanh điệu đó
        for tone_code in tones_found:
            if tone_code != 0:
                return tone_code, self.tone_names[tone_code]
        
        # Nếu chỉ có thanh ngang hoặc không có thanh điệu nào
        return 0, self.tone_names[0]  # Mặc định thanh ngang
    
    def remove_tone_marks(self, text: str) -> str:
        """
        Loại bỏ dấu thanh điệu khỏi văn bản, giữ lại ký tự gốc
        
        Args:
            text: Văn bản có dấu thanh điệu
            
        Returns:
            Văn bản không dấu thanh điệu
        """
        # Bảng chuyển đổi từ ký tự có dấu sang không dấu
        accent_map = {
            # Nguyên âm a
            'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
            'ằ': 'ă', 'ắ': 'ă', 'ẳ': 'ă', 'ẵ': 'ă', 'ặ': 'ă',
            'ầ': 'â', 'ấ': 'â', 'ẩ': 'â', 'ẫ': 'â', 'ậ': 'â',
            
            # Nguyên âm e
            'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
            'ề': 'ê', 'ế': 'ê', 'ể': 'ê', 'ễ': 'ê', 'ệ': 'ê',
            
            # Nguyên âm i
            'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
            
            # Nguyên âm o
            'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
            'ô': 'o',  # thêm ô không dấu 
            'ồ': 'ô', 'ố': 'ô', 'ổ': 'ô', 'ỗ': 'ô', 'ộ': 'ô',
            'ờ': 'ơ', 'ớ': 'ơ', 'ở': 'ơ', 'ỡ': 'ơ', 'ợ': 'ơ',
            
            # Nguyên âm u
            'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
            'ừ': 'ư', 'ứ': 'ư', 'ử': 'ư', 'ữ': 'ư', 'ự': 'ư',
            
            # Thêm xử lý cho nguyên âm đôi
            'ư': 'u',  # ư không dấu -> u
            'ơ': 'o',  # ơ không dấu -> o
            
            # Nguyên âm y
            'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
        }
        
        result = ''
        for char in text:
            result += accent_map.get(char, char)
        
        return result


class PhonemeMapper:
    """Bảng ánh xạ từ chữ viết tiếng Việt sang ký hiệu âm vị IPA"""
    
    def __init__(self):
        # Hệ thống âm đầu (22 âm vị)
        self.initial_consonants = {
            'b': '/b-/',
            'm': '/m-/',
            'ph': '/f-/',
            'v': '/v-/',
            't': '/t-/',
            'th': '/tʼ-/',
            'đ': '/d-/',
            'n': '/n-/',
            'd': '/z-/',     # trường hợp d không phải đ
            'gi': '/z-/',    # gi phát âm như z
            'r': '/ʐ-/',
            'x': '/s-/',
            's': '/ʂ-/',
            'ch': '/c-/',
            'tr': '/ʈ-/',
            'nh': '/ɲ-/',
            'l': '/l-/',
            'k': '/k-/',
            'q': '/k-/',     # qu phát âm như k + w
            'c': '/k-/',
            'kh': '/χ-/',
            'ngh': '/ŋ-/',   # trước i, e, ê
            'ng': '/ŋ-/',    # trường hợp còn lại
            'gh': '/ɣ-/',    # trước i, e, ê  
            'g': '/ɣ-/',     # trường hợp còn lại
            'h': '/h-/',
            '': '/ʔ-/'       # âm đầu rỗng (thanh quản bế)
        }
        
        # Hệ thống âm đệm (2 âm vị)
        self.medial_consonants = {
            'w': '/-w-/',    # âm đệm u/o
            '': '/zero/'     # không có âm đệm
        }
        
        # Hệ thống âm chính (16 âm vị)
        self.vowels = {
            'i': '/-i-/',
            'y': '/-i-/',     # trong một số trường hợp
            'ê': '/-e-/',
            'e': '/-ɛ-/',
            'ư': '/-ɯ-/',
            'ơ': '/-ɤ-/',
            'a': '/-a-/',     # hoặc /-ă-/, /-ɛ̈-/ tùy ngữ cảnh
            'ă': '/-ă-/',
            'â': '/-ɤ̈-/',
            'u': '/-u-/',
            'ô': '/-o-/',
            'o': '/-ɔ-/',     # hoặc /-ɔ̈-/ tùy ngữ cảnh
            'iê': '/-ie-/',   # nguyên âm đôi
            'ia': '/-ie-/',
            'yê': '/-ie-/',
            'ya': '/-ie-/',
            'ươ': '/-ɯɤ-/',   # nguyên âm đôi
            'ưa': '/-ɯɤ-/',
            'uô': '/-uo-/',   # nguyên âm đôi
            'ua': '/-uo-/'
        }
        
        # Hệ thống âm cuối (9 âm vị)
        self.final_consonants = {
            'm': '/-m/',
            'n': '/-n/',
            'p': '/-p/',
            't': '/-t/',
            'nh': '/-ŋ/',     # sau i, e, anh
            'ng': '/-ŋ/',     # trường hợp còn lại
            'ch': '/-k/',     # sau i, e, ach
            'c': '/-k/',      # trường hợp còn lại
            'o': '/-w/',      # âm cuối o sau a, e
            'u': '/-w/',      # âm cuối u
            'y': '/-j/',      # âm cuối y sau ă, â
            'i': '/-j/',      # âm cuối i
            '': '/zero/'      # không có âm cuối
        }


class SyllableAnalyzer:
    """Phân tích âm tiết tiếng Việt thành các thành phần âm vị"""
    
    def __init__(self):
        self.tone_handler = ToneHandler()
        self.phoneme_mapper = PhonemeMapper()
    
    def split_syllable(self, syllable: str) -> Dict[str, str]:
        """
        Tách âm tiết thành các thành phần: âm đầu, âm đệm, âm chính, âm cuối
        
        Args:
            syllable: Âm tiết tiếng Việt
            
        Returns:
            Dictionary chứa các thành phần âm vị
        """
        # Loại bỏ dấu thanh điệu để phân tích cấu trúc
        clean_syllable = self.tone_handler.remove_tone_marks(syllable.lower())
        
        result = {
            'initial': '',
            'medial': '',
            'nucleus': '',
            'final': '',
            'tone': '',
            'original': syllable
        }
        
        # Xác định thanh điệu
        tone_code, tone_name = self.tone_handler.get_tone(syllable)
        result['tone'] = f"{tone_name} ({self.tone_handler.tone_symbols[tone_code]})"
        
        # Phân tích âm đầu
        initial = self._extract_initial(clean_syllable)
        result['initial'] = initial
        remaining = clean_syllable[len(initial):] if initial else clean_syllable
        
        # Phân tích âm cuối
        final = self._extract_final(remaining)
        result['final'] = final
        remaining = remaining[:-len(final)] if final else remaining
        
        # Phân tích âm đệm và âm chính
        medial, nucleus = self._extract_medial_nucleus(remaining, initial)
        result['medial'] = medial
        result['nucleus'] = nucleus
        
        return result
    
    def _extract_initial(self, syllable: str) -> str:
        """Trích xuất âm đầu từ âm tiết"""
        # Danh sách âm đầu theo thứ tự độ dài giảm dần để tránh nhầm lẫn
        initials = ['ngh', 'ng', 'gh', 'kh', 'th', 'ph', 'tr', 'ch', 'nh', 'gi', 'qu',
                   'b', 'm', 'v', 't', 'đ', 'n', 'd', 'r', 'x', 's', 'l', 'k', 'c', 'g', 'h']
        
        for initial in initials:
            if syllable.startswith(initial):
                # Xử lý trường hợp đặc biệt cho k, q, c
                if initial == 'qu':
                    return 'qu'
                elif initial == 'k' and len(syllable) > 1:
                    next_vowel = syllable[1:2]
                    if next_vowel in ['i', 'e', 'ê']:
                        return 'k'
                elif initial == 'c' and len(syllable) > 1:
                    next_vowel = syllable[1:2]
                    if next_vowel not in ['h']:  # không phải ch
                        return 'c'
                elif initial == 'g' and len(syllable) > 1:
                    if syllable[1:2] not in ['h', 'i']:  # không phải gh hoặc gi
                        return 'g'
                elif initial == 'd' and len(syllable) > 1:
                    if syllable[1:2] != 'đ':  # không phải đ
                        return 'd'
                else:
                    return initial
        
        return ''  # Không có âm đầu (âm đầu rỗng)
    
    def _extract_final(self, syllable: str) -> str:
        """Trích xuất âm cuối từ âm tiết"""
        finals = ['nh', 'ng', 'ch', 'c', 'p', 't', 'm', 'n', 'u', 'o', 'i', 'y']
        
        for final in finals:
            if syllable.endswith(final) and len(syllable) > 1:
                # Kiểm tra ngữ cảnh cho nh/ng và ch/c
                if final == 'nh':
                    # nh sau i, e, anh
                    vowel_part = syllable[:-2]
                    if vowel_part.endswith(('i', 'e')) or 'a' in vowel_part:
                        return 'nh'
                elif final == 'ch':
                    # ch sau i, e, ach
                    vowel_part = syllable[:-2]
                    if vowel_part.endswith(('i', 'e')) or 'a' in vowel_part:
                        return 'ch'
                elif final in ['ng', 'c', 'p', 't', 'm', 'n']:
                    return final
                elif final in ['u', 'o', 'i', 'y']:
                    # Chỉ coi u, o, i, y là âm cuối khi có nguyên âm khác phía trước
                    vowel_part = syllable[:-1]
                    if len(vowel_part) > 0 and any(v in vowel_part for v in ['a', 'e', 'ê', 'ă', 'â', 'ơ', 'ô', 'ư']):
                        return final
        
        return ''  # Không có âm cuối
    
    def _extract_medial_nucleus(self, remaining: str, initial: str) -> Tuple[str, str]:
        """Trích xuất âm đệm và âm chính"""
        medial = ''
        nucleus = remaining
        
        # Xử lý âm đệm u/o
        if initial == 'qu':
            medial = 'u'  # qu có âm đệm u
            nucleus = remaining
        elif remaining.startswith(('uo', 'ua', 'uô')):
            medial = 'u'
            nucleus = remaining[1:]
        elif remaining.startswith(('ươ', 'ưa')):
            medial = ''  # không có âm đệm riêng
            nucleus = remaining
        elif remaining.startswith('oa') or remaining.startswith('oe'):
            medial = 'o'
            nucleus = remaining[1:]
        
        # Nhận dạng nguyên âm đôi
        if nucleus.startswith(('iê', 'ia', 'yê', 'ya')):
            nucleus = nucleus[:2] if len(nucleus) >= 2 else nucleus
        elif nucleus.startswith(('ươ', 'ưa', 'uô', 'ua')):
            nucleus = nucleus[:2] if len(nucleus) >= 2 else nucleus
        
        return medial, nucleus


class VietnamesePhonemeTranscriber:
    """Lớp chính thực hiện phiên âm tiếng Việt sang ký hiệu âm vị"""
    
    def __init__(self):
        self.syllable_analyzer = SyllableAnalyzer()
        self.phoneme_mapper = PhonemeMapper()
    
    def split_text_to_syllables(self, text: str) -> List[str]:
        """
        Tách văn bản thành các âm tiết
        
        Args:
            text: Văn bản tiếng Việt
            
        Returns:
            Danh sách các âm tiết
        """
        # Xóa dấu câu và ký tự đặc biệt, giữ lại khoảng trắng
        cleaned_text = re.sub(r'[^\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]', '', text)
        
        # Tách thành từ
        words = cleaned_text.split()
        
        syllables = []
        for word in words:
            # Mỗi từ trong tiếng Việt có thể là một hoặc nhiều âm tiết
            # Với đơn giản hóa, mỗi từ được coi là một âm tiết
            if word.strip():
                syllables.append(word.strip())
        
        return syllables
    
    def transcribe_syllable(self, syllable: str) -> Dict[str, str]:
        """
        Phiên âm một âm tiết sang ký hiệu âm vị
        
        Args:
            syllable: Âm tiết tiếng Việt
            
        Returns:
            Dictionary chứa thông tin phiên âm
        """
        # Phân tích âm tiết
        components = self.syllable_analyzer.split_syllable(syllable)
        
        # Ánh xạ sang ký hiệu âm vị
        phoneme_transcription = {
            'original': syllable,
            'components': components,
            'phonemes': {
                'initial': self._map_initial(components['initial']),
                'medial': self._map_medial(components['medial']),
                'nucleus': self._map_nucleus(components['nucleus']),
                'final': self._map_final(components['final'], components['nucleus']),
                'tone': components['tone']
            }
        }
        
        # Tạo chuỗi phiên âm hoàn chỉnh
        phoneme_string = ''
        phoneme_string += phoneme_transcription['phonemes']['initial']
        if phoneme_transcription['phonemes']['medial'] != '/zero/':
            phoneme_string += phoneme_transcription['phonemes']['medial']
        phoneme_string += phoneme_transcription['phonemes']['nucleus']
        if phoneme_transcription['phonemes']['final'] != '/zero/':
            phoneme_string += phoneme_transcription['phonemes']['final']
        phoneme_string += ' ' + components['tone']
        
        phoneme_transcription['full_transcription'] = phoneme_string
        
        return phoneme_transcription
    
    def _map_initial(self, initial: str) -> str:
        """Ánh xạ âm đầu sang ký hiệu âm vị"""
        if initial == '':
            return self.phoneme_mapper.initial_consonants['']
        elif initial == 'qu':
            return self.phoneme_mapper.initial_consonants['q']
        elif initial in self.phoneme_mapper.initial_consonants:
            return self.phoneme_mapper.initial_consonants[initial]
        else:
            return f"/{initial}-/"  # Fallback
    
    def _map_medial(self, medial: str) -> str:
        """Ánh xạ âm đệm sang ký hiệu âm vị"""
        if medial == '' or medial == 'zero':
            return self.phoneme_mapper.medial_consonants['']
        elif medial in ['u', 'o']:
            return self.phoneme_mapper.medial_consonants['w']
        else:
            return self.phoneme_mapper.medial_consonants['']
    
    def _map_nucleus(self, nucleus: str) -> str:
        """Ánh xạ âm chính sang ký hiệu âm vị"""
        if nucleus in self.phoneme_mapper.vowels:
            return self.phoneme_mapper.vowels[nucleus]
        else:
            # Xử lý các trường hợp đặc biệt
            if nucleus in ['a']:
                return '/-a-/'
            elif nucleus in ['o']:
                return '/-ɔ-/'
            else:
                return f"/-{nucleus}-/"  # Fallback
    
    def _map_final(self, final: str, nucleus: str) -> str:
        """Ánh xạ âm cuối sang ký hiệu âm vị (có xét ngữ cảnh âm chính)"""
        if final == '':
            return self.phoneme_mapper.final_consonants['']
        elif final in self.phoneme_mapper.final_consonants:
            return self.phoneme_mapper.final_consonants[final]
        else:
            return f"/-{final}/"  # Fallback
    
    def transcribe_text(self, text: str) -> List[Dict[str, str]]:
        """
        Phiên âm toàn bộ văn bản
        
        Args:
            text: Văn bản tiếng Việt
            
        Returns:
            Danh sách kết quả phiên âm cho từng âm tiết
        """
        syllables = self.split_text_to_syllables(text)
        results = []
        
        for syllable in syllables:
            transcription = self.transcribe_syllable(syllable)
            results.append(transcription)
        
        return results


def main():
    """Hàm main để test chương trình"""
    transcriber = VietnamesePhonemeTranscriber()
    
    print("=== CHƯƠNG TRÌNH PHIÊN ÂM ÂM VỊ HỌC TIẾNG VIỆT ===")
    print("Nhập văn bản tiếng Việt để phiên âm (Enter để thoát):")
    
    while True:
        text = input("\n> ").strip()
        if not text:
            break
        
        print(f"\nPhiên âm cho: '{text}'")
        print("-" * 60)
        
        results = transcriber.transcribe_text(text)
        
        for i, result in enumerate(results, 1):
            print(f"\nÂm tiết {i}: {result['original']}")
            print(f"  - Thành phần:")
            print(f"    + Âm đầu: '{result['components']['initial']}' → {result['phonemes']['initial']}")
            print(f"    + Âm đệm: '{result['components']['medial']}' → {result['phonemes']['medial']}")
            print(f"    + Âm chính: '{result['components']['nucleus']}' → {result['phonemes']['nucleus']}")
            print(f"    + Âm cuối: '{result['components']['final']}' → {result['phonemes']['final']}")
            print(f"    + Thanh điệu: {result['phonemes']['tone']}")
            print(f"  - Phiên âm: {result['full_transcription']}")


if __name__ == "__main__":
    main()
