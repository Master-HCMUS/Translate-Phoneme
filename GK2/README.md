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

## Notes
- All scripts assume UTF-8 encoding.
- Adjust file paths in scripts if you change the folder structure.
- `blacklist.txt` (optional) can be used to filter out unwanted syllables.
- `rimes.txt` should contain all valid rimes (one per line, canonical form).

## Contact
For questions or contributions, please contact the project maintainer.
