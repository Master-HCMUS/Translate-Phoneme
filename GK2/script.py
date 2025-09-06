from collections import Counter

def extract_am_tiet(input_file, output_file):
    counter = Counter()

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split left column (word) and right column (tags)
            parts = line.split("\t")
            word = parts[0].strip()

            am_tiet_list = word.split()

            # Count each âm tiết
            counter.update(am_tiet_list)

    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        for am_tiet, count in counter.most_common():
            f.write(f"{am_tiet}\t{count}\n")

    print("Done!")
    
if __name__ == "__main__":
    extract_am_tiet("VDic_uni.txt", "output.txt")
