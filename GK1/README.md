# Báo cáo GK1 — Phiên âm âm vị học tiếng Việt

## Yêu cầu đề bài
Viết chương trình phiên âm âm vị học tiếng Việt: nhận vào một chuỗi văn bản tiếng Việt (Unicode), tách thành các âm tiết và ánh xạ từng âm tiết sang dãy âm vị (ký hiệu gần-IPA) kèm thông tin thanh điệu.

Triển khai: xem `GK1/main.py` (kèm test đơn vị trong `GK1/unit_test.py`).

## Đầu vào
- Chuỗi văn bản Unicode có thể chứa:
  - Âm tiết tiếng Việt có dấu (ví dụ: "Trường", "học").
  - Dấu câu/ký tự không phải chữ (ví dụ: , . ! ; - …).
  - Chữ hoa/chữ thường; chương trình không phân biệt hoa/thường khi phiên âm.

Lưu ý:
- Chương trình xử lý theo từng token; token là “từ” hoặc dấu câu (tách bằng regex) để bảo toàn dấu câu trong đầu ra.
- Các âm tiết/chuỗi chữ không thuần Việt (ví dụ tên riêng Latin) vẫn đi qua cùng bộ quy tắc nên kết quả chỉ mang tính xấp xỉ.

## Đầu ra
- Danh sách các bản ghi theo thứ tự token đầu vào:
  - Với token là âm tiết (có chữ cái): một đối tượng gồm:
    - `syllable`: âm tiết gốc (giữ nguyên dấu/chữ hoa thường).
    - `phonemes`: danh sách âm vị theo gần-IPA, theo thứ tự: âm đầu + vần + âm cuối.
    - `tone`: tên thanh điệu: `ngang | sắc | huyền | hỏi | ngã | nặng`.
  - Với token là dấu câu/ký tự khác: một đối tượng dạng `{ "raw": <ký tự> }`.

- Hàm `pretty_print(...)` có thể định dạng danh sách trên thành các dòng dễ đọc, ví dụ:

```
Trường, học!
→
Trường -> /ʈ/ /ɯɤ/ /ŋ/ (huyền)
,
học -> /h/ /ɔ/ /k/ (nặng)
!
```

## Quá trình xử lý
Tóm tắt ngắn gọn, ở mức high level:

1) Tách token, giữ nguyên dấu câu
- Chia văn bản thành các token (chuỗi chữ và dấu câu) để vừa xử lý âm tiết vừa bảo toàn vị trí dấu câu.

2) Xác định thanh điệu và chuẩn hóa chữ
- Từ mỗi token là chữ, tách dấu thanh (sắc, huyền, hỏi, ngã, nặng) để lấy tên thanh; vẫn giữ loại nguyên âm (ă, â, ê, ô, ơ, ư).

3) Chia âm tiết thành 3 phần
- Tách âm đầu, vần (nguyên âm/nhị trùng âm và các bán nguyên âm), và âm cuối bằng một bộ quy tắc chính tả tiếng Việt đơn giản, ưu tiên khớp dài cho các tổ hợp phổ biến (ví dụ: qu, ngh/ng/nh; âm cuối nh/ng/ch).

4) Ánh xạ sang ký hiệu âm vị gần-IPA
- Mỗi phần được chuyển sang ký hiệu âm vị (gần-IPA); khi có `o/u` hoặc `i/y` ở rìa vần, thêm bán nguyên âm tương ứng `/w/` hoặc `/j/`.

5) Tổ hợp kết quả
- Ghép theo thứ tự âm đầu + vần + âm cuối và gắn tên thanh điệu. Token không phải chữ được trả về nguyên dạng.

Lưu ý: Các quy tắc được thiết kế ở mức khái quát để dễ hiểu và có thể điều chỉnh; mã nguồn chọn các biến thể âm vị phổ biến cho tiếng Việt chuẩn.

## Ví dụ minh hoạ
- "Trường" → âm vị: `/ʈ/ /ɯɤ/ /ŋ/`, thanh: `huyền`.
- "quốc" → âm vị: `/k/ /w/ /o/ /k/`, thanh: `sắc`.
- "học" → âm vị: `/h/ /ɔ/ /k/`, thanh: `nặng`.

Các ví dụ trên có thể xác nhận bằng test đơn vị trong `GK1/unit_test.py`.

## Cách chạy nhanh
- Chạy demo tích hợp trong `main.py`:

```cmd
cd "c:\Users\nguyenphong\Downloads\study master\NLP\TranslatePhoneme\GK1"
python main.py
```

- Chạy test đơn vị:

```cmd
cd "c:\Users\nguyenphong\Downloads\study master\NLP\TranslatePhoneme\GK1"
python -m unittest unit_test.py -v
```

## Tài liệu tham khảo
- Nguyễn Tài Cẩn (1995), "Ngữ âm tiếng Việt", NXB Giáo dục.
- Hoàng Phê (chủ biên) (2003), "Từ điển tiếng Việt", Trung tâm Từ điển học, NXB Đà Nẵng.
- Đoàn Thiện Thuật (1999), "Ngữ âm tiếng Việt", NXB Đại học Quốc gia Hà Nội.
- Viện Ngôn ngữ học (2001), "Ngữ pháp tiếng Việt", NXB Khoa học Xã hội.
- Unicode Normalization (NFC/NFD) — Unicode Standard Annex #15: https://unicode.org/reports/tr15/
