import re
from collections import Counter

def is_foreign(word, tags):
    """
    Nhận diện từ mượn dựa trên nhãn và chính tả
    """
    # Loại theo POS tag (Np = proper noun)
    if "Np" in tags.split(","):
        return True
    # Loại nếu có gạch nối
    if "-" in word:
        return True
    # Loại nếu có chữ cái ngoại lai (không thuộc bảng chữ cái Việt)
    if re.search(r"[jfzw]", word.lower()):
        return True
    # Loại theo một số pattern vay mượn phổ biến
    foreign_patterns = ["axit", "ben", "in$", "ic$", "id$", "um$"]
    for pat in foreign_patterns:
        if re.search(pat, word.lower()):
            return True
    return False

def is_noise(word):
    """
    Bỏ qua các ký hiệu không phải từ
    """
    noise_symbols = {
        ".", "...", "\"", "'", "-", "?", ":", ";", "!", "?isName?", "?isDigit?"
    }
    return word in noise_symbols

def extract_am_tiet(input_file, output_file, summary_file):
    counter = Counter()

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) < 2:
                continue
            word = parts[0].strip()
            tags = parts[-1].strip()

            # Bỏ qua noise
            if is_noise(word):
                continue

            # Loại bỏ từ mượn
            if is_foreign(word, tags):
                continue

            # Tách âm tiết (chỉ split theo khoảng trắng)
            am_tiet_list = word.split()

            counter.update(am_tiet_list)

    # Xuất danh sách âm tiết
    with open(output_file, "w", encoding="utf-8") as f:
        for am_tiet, count in counter.most_common():
            f.write(f"{am_tiet}\t{count}\n")

    # Xuất summary
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"Số lượng âm tiết khác nhau: {len(counter)}\n")
        f.write(f"Tổng số lần xuất hiện: {sum(counter.values())}\n")

    print("✅ Hoàn tất xử lý!")

if __name__ == "__main__":
    # Đổi đường dẫn file input/output theo máy local của bạn
    extract_am_tiet("VDic_uni.txt", "output.txt", "summary.txt")
