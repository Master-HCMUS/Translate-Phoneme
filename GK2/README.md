# Vietnamese Syllable Extraction & Comparison Toolkit

## Project Structure

```
GK2/
  data/
    blacklist.txt                # List of syllables to exclude
    groundtruth_syllables.txt    # Reference/ground truth syllable list
    rimes.txt                    # List of valid rimes
    VDic_uni.txt                 # Source dictionary (word\ttags)
  output/
    output_syllables.txt         # Extracted/filtered syllables from VDic_uni.txt
    syllable_report.txt          # Extraction report
    groundtruth_not_in_vdic.txt  # Syllables in groundtruth but not in VDic_uni.txt
  test/
    output_only_syllables.txt        # Syllables in output but not in groundtruth
    groundtruth_only_syllables.txt   # Syllables in groundtruth but not in output
  extract_syllables.py           # Main script: extract syllables from VDic_uni.txt
  compare_syllables.py           # Compare output and groundtruth syllables
  groundtruth_not_in_vdic_script.py # Find groundtruth syllables not in VDic_uni.txt
```

## Usage

1. **Extract syllables:**
   ```
   python extract_syllables.py
   ```
   - Output: `output/output_syllables.txt`, `output/syllable_report.txt`

2. **Compare with ground truth:**
   ```
   python compare_syllables.py
   ```
   - Output: `test/output_only_syllables.txt`, `test/groundtruth_only_syllables.txt`

3. **Find groundtruth syllables not in VDic_uni.txt:**
   ```
   python groundtruth_not_in_vdic_script.py
   ```
   - Output: `output/groundtruth_not_in_vdic.txt`


## Ground Truth Source & Explanation

- The ground truth syllable list is sourced from [Dự án S - Âm tiết tiếng Việt](https://s.ngonngu.net/syllables/), which currently records **6,845** valid Vietnamese syllables (as of 2025).
- In this toolkit, the script only keeps syllables that are present in both the ground truth and your `VDic_uni.txt` dictionary. For example, your report may show only **6,661** syllables kept, which is fewer than the ground truth. This is because the remaining syllables (e.g., 184 syllables) are not found in your `VDic_uni.txt` file.
- The difference may be due to `VDic_uni.txt` being outdated or missing some newly added/rare syllables. You can update or expand this file to improve coverage.
- Example of newly added syllables (not in old dictionaries): quềnh, nhày, ụn, nhệu, nhễu, oăng, ngổng, ướn, khuềnh, khoàng, ...

## Notes
- All scripts assume UTF-8 encoding.
- Adjust file paths in scripts if you change the folder structure.
- `blacklist.txt` (optional) can be used to filter out unwanted syllables.
- `rimes.txt` should contain all valid rimes (one per line, canonical form).