#!/usr/bin/env python3
import re

from analyze_gdrive_list import lines

print("=== CHECKING OFFICIAL SERIES COMPLETENESS IN GDRIVE LIST ===\n")

def check_series(name, expected_nums, pattern):
    found = {}
    for l in lines:
        m = re.search(pattern, l)
        if m:
            num = int(m.group(1))
            found[num] = l
    
    missing = [n for n in expected_nums if n not in found]
    print(f"[{name}]")
    print(f"  Total expected: {len(expected_nums)}")
    print(f"  Found in list : {len(found)} -> {sorted(found.keys())}")
    if missing:
        print(f"  MISSING from GDrive list: {missing}")
    else:
        print(f"  STATUS: COMPLETE! (All {len(expected_nums)} present)")
    print()

# 1. BRILLI@NT WING (01..05)
check_series("BRILLI@NT WING", range(1, 6), r"BRILLI@NT WING 0?(\d+)")

# 2. FR@GMENT WING (01..06)
check_series("FR@GMENT WING", range(1, 7), r"FR@GMENT WING 0?(\d+)")

# 3. GR@DATE WING (01..07)
check_series("GR@DATE WING", range(1, 8), r"GR@DATE WING 0?(\d+)")

# 4. L@YERED WING (01..08)
check_series("L@YERED WING", range(1, 9), r"L@YERED WING 0?(\d+)")

# 5. PANOR@MA WING (01..08)
check_series("PANOR@MA WING", range(1, 9), r"PANOR@MA WING 0?(\d+)")

# 6. CANVAS (01..08)
check_series("CANVAS", range(1, 9), r"CANVAS[”\"]\s*0?(\d+)")

# 7. ECHOES (01..09)
check_series("ECHOES", range(1, 10), r"ECHOES 0?(\d+)")

# 8. 円環 -Halo around- (01..04)
check_series("円環 -Halo around-", range(1, 5), r"Halo around[”\"]\s*0?(\d+)")

# 9. Synthe-Side (01..03)
check_series("Synthe-Side", range(1, 4), r"Synthe-Side 0?(\d+)")

# 10. COLORFUL FE@THERS (Stella, Luna, Sol, SHHis, CoMETIK)
feathers = [l for l in lines if 'COLORFUL FE@THERS' in l]
print("[COLORFUL FE@THERS]")
print(f"  Found {len(feathers)} items:")
for f in feathers:
    print(f"   - {f}")
print()
