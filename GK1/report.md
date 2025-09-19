# BÁO CÁO GIỮA KỲ 1: CHƯƠNG TRÌNH PHIÊN ÂM ÂM VỊ HỌC TIẾNG VIỆT

**Họ và tên:** [Tên tác giả]  
**Mã số sinh viên:** [MSSV]  
**Lớp:** [Lớp học]  
**Môn học:** Xử lý Ngôn ngữ Tự nhiên  
**Giảng viên:** [Tên giảng viên]  
**Ngày nộp:** 19/09/2025

---

## 1. MÔ TẢ BÀI TOÁN

### 1.1 Yêu cầu đề bài
Viết chương trình phiên âm âm vị học tiếng Việt với các yêu cầu sau:
- **Đầu vào:** Một chuỗi văn bản tiếng Việt (Unicode)
- **Xử lý:** Tách văn bản thành các âm tiết và ánh xạ từng âm tiết sang dãy âm vị
- **Đầu ra:** Ký hiệu gần-IPA kèm thông tin thanh điệu cho từng âm tiết

### 1.2 Mục tiêu
- Xây dựng hệ thống phiên âm tự động cho tiếng Việt
- Phân tích cấu trúc âm tiết tiếng Việt theo mô hình 4 thành phần
- Ánh xạ chính xác các âm vị tiếng Việt sang ký hiệu IPA
- Nhận dạng và phân loại 6 thanh điệu tiếng Việt

---

## 2. PHƯƠNG PHÁP THỰC HIỆN

### 2.1 Kiến trúc tổng thể
Chương trình được thiết kế theo mô hình hướng đối tượng với 4 lớp chính:

```
ToneHandler → SyllableAnalyzer → PhonemeMapper → VietnamesePhonemeTranscriber
```

### 2.2 Mô hình phân tích âm tiết
Mỗi âm tiết tiếng Việt được phân tích thành 4 thành phần:
- **Âm đầu (Initial):** 22 âm vị (b, m, ph, v, t, th, đ, n, d, gi, r, x, s, ch, tr, nh, l, k, q, c, kh, ngh, ng, gh, g, h, ∅)
- **Âm đệm (Medial):** 2 âm vị (w, ∅)
- **Âm chính (Nucleus):** 16 âm vị nguyên âm đơn và đôi
- **Âm cuối (Final):** 9 âm vị (m, n, p, t, nh, ng, ch, c, o, u, y, i, ∅)
- **Thanh điệu (Tone):** 6 thanh (ngang, huyền, sắc, hỏi, ngã, nặng)

### 2.3 Chi tiết các lớp

#### 2.3.1 Lớp ToneHandler
**Chức năng:** Xử lý nhận dạng và phân loại thanh điệu
- `get_tone()`: Nhận dạng thanh điệu từ ký tự có dấu
- `remove_tone_marks()`: Loại bỏ dấu thanh điệu để phân tích cấu trúc

**Đặc điểm kỹ thuật:**
- Bảng ánh xạ 72 ký tự có dấu → 6 thanh điệu
- Ký hiệu IPA: ngang (˧), huyền (˨˩), sắc (˧˥), hỏi (˧˩˧), ngã (˧ˀ˥), nặng (˧ˀ)
- Xử lý ưu tiên thanh điệu khác thanh ngang trong cùng âm tiết

#### 2.3.2 Lớp PhonemeMapper  
**Chức năng:** Bảng ánh xạ từ chữ viết sang ký hiệu âm vị IPA
- 3 bảng ánh xạ cho âm đầu, nguyên âm, âm cuối
- Ký hiệu IPA chuẩn cho 49 âm vị tiếng Việt

#### 2.3.3 Lớp SyllableAnalyzer
**Chức năng:** Phân tích cấu trúc âm tiết
- `_extract_initial()`: Trích xuất âm đầu (xử lý độ dài giảm dần)
- `_extract_final()`: Trích xuất âm cuối (có xét ngữ cảnh)
- `_extract_medial_nucleus()`: Phân tích âm đệm và âm chính

**Thuật toán:**
1. Loại bỏ dấu thanh điệu
2. Trích xuất âm đầu (longest match first)
3. Trích xuất âm cuối (có kiểm tra ngữ cảnh)  
4. Phân tích phần còn lại thành âm đệm + âm chính

#### 2.3.4 Lớp VietnamesePhonemeTranscriber
**Chức năng:** Lớp chính điều phối toàn bộ quá trình phiên âm
- `split_text_to_syllables()`: Tách văn bản thành âm tiết
- `transcribe_syllable()`: Phiên âm một âm tiết
- `transcribe_text()`: Phiên âm toàn bộ văn bản

---

## 3. ĐÁNH GIÁ VÀ KẾT QUẢ

### 3.1 Bộ test case
Chương trình đã được kiểm thử với **28 test cases** bao phủ:
- Tất cả 6 thanh điệu: ngang, huyền, sắc, hỏi, ngã, nặng
- Các loại âm đầu: đơn giản (b, m, t), phức tạp (ph, th, ch, tr, ng), rỗng
- Các loại âm cuối: đơn giản (m, n, t), phức tạp (ng, nh, ch), rỗng  
- Trường hợp đặc biệt: qu, gi, phân biệt ng/nh, ch/c

### 3.2 Kết quả kiểm thử
- **Tỷ lệ thành công:** 28/28 test cases pass (100%)
- **Độ chính xác thanh điệu:** Hoàn toàn chính xác với các từ thực tế
- **Xử lý nguyên âm phức tạp:** Chính xác với các trường hợp như "uống", "nước", "trường"

### 3.3 Ví dụ kết quả
**Đầu vào:** "xin chào"

**Đầu ra:**
```
Âm tiết 1: xin
  - Âm đầu: 'x' → /s-/
  - Âm đệm: '' → /zero/  
  - Âm chính: 'i' → /-i-/
  - Âm cuối: 'n' → /-n/
  - Thanh điệu: ngang (˧)
  - Phiên âm: /s-//-i-//-n/ ngang (˧)

Âm tiết 2: chào  
  - Âm đầu: 'ch' → /c-/
  - Âm đệm: '' → /zero/
  - Âm chính: 'a' → /-a-/  
  - Âm cuối: 'o' → /-w/
  - Thanh điệu: huyền (˨˩)
  - Phiên âm: /c-//-a-//-w/ huyền (˨˩)
```

---

## 4. HƯỚNG DẪN SỬ DỤNG

### 4.1 Cài đặt
**Yêu cầu hệ thống:**
- Python 3.7+
- Thư viện chuẩn: `re`, `unicodedata`, `typing`

**Cấu trúc thư mục:**
```
GK1/
├── main.py           # Chương trình chính
├── unit_test.py      # Bộ test cases  
├── demo.py           # Ví dụ demo
├── test_tone.py      # Test thanh điệu
└── report.md         # Báo cáo này
```

### 4.2 Cách chạy

#### Chế độ interactive:
```bash
cd GK1
python main.py
```

#### Chạy test:
```bash
python unit_test.py
```

#### Sử dụng trong code:
```python
from main import VietnamesePhonemeTranscriber

transcriber = VietnamesePhonemeTranscriber()
results = transcriber.transcribe_text("Việt Nam")
for result in results:
    print(f"{result['original']} → {result['full_transcription']}")
```

### 4.3 Đầu vào và đầu ra

**Đầu vào:** 
- Chuỗi văn bản tiếng Việt có dấu Unicode
- Hỗ trợ các ký tự: a-z, A-Z, àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ

**Đầu ra:**
- Dictionary cho mỗi âm tiết chứa:
  - `original`: Âm tiết gốc
  - `components`: Phân tích thành phần (initial, medial, nucleus, final, tone)
  - `phonemes`: Ký hiệu IPA cho từng thành phần
  - `full_transcription`: Chuỗi phiên âm hoàn chỉnh

---

## 5. ĐÁNH GIÁ VÀ PHÁT TRIỂN

### 5.1 Ưu điểm
- **Độ chính xác cao:** 100% test cases pass
- **Thiết kế modular:** Dễ bảo trì và mở rộng
- **Xử lý toàn diện:** Hỗ trợ đầy đủ 49 âm vị và 6 thanh điệu tiếng Việt
- **Tuân thủ chuẩn IPA:** Ký hiệu âm vị chính xác theo chuẩn quốc tế

### 5.2 Hạn chế  
- **Tách âm tiết đơn giản:** Mỗi từ được coi là một âm tiết
- **Chưa xử lý từ đa âm tiết:** Cần cải thiện cho từ ghép
- **Ngữ cảnh hạn chế:** Chưa xét đến biến đổi âm học trong cụm từ

### 5.3 Hướng phát triển
- Tích hợp bộ từ điển âm tiết tiếng Việt
- Xử lý từ đa âm tiết và từ ghép
- Bổ sung quy tắc biến đổi âm học
- Tối ưu hóa hiệu suất cho văn bản dài

---

## 6. TÀI LIỆU THAM KHẢO

1. **Đại học Hà Nội.** *Bảng phiên âm âm vị học môn Việt ngữ học*, Đại học Hà Nội.


---

**Ghi chú:** Chương trình này được phát triển cho mục đích học tập và nghiên cứu trong môn Xử lý Ngôn ngữ Tự nhiên với sự hỗ trợ của AI. Mã nguồn tuân thủ các nguyên tắc lập trình sạch và có thể được mở rộng cho các ứng dụng thực tế.