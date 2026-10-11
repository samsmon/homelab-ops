#!/usr/bin/env python3
import re
from pathlib import Path

# Load raw list
from analyze_gdrive_list import lines

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~/シャイニーカラーズ')
existing_folders = [p.name for p in BASE.rglob('*') if p.is_dir() and p.name != 'BK']

print("=== CHECKING GDRIVE LIST AGAINST EXISTING SHINY COLORS LIBRARY ===")
present = []
missing = []

for l in lines:
    # clean zip extension and trailing chars
    name = l.replace('.zip', '')
    
    # Extract date tag like [250903] or [180905]
    m_date = re.match(r'\[(\d{6})\]', name)
    
    # Check if any folder in existing_folders matches loosely
    match = False
    for ef in existing_folders:
        # Check by core title
        if m_date:
            d_str = m_date.group(1)
            # 250903 -> 2025.09.03 or similar
            y = "20" + d_str[:2]
            m = d_str[2:4]
            d = d_str[4:6]
            iso_date = f"{y}.{m}.{d}"
            if iso_date in ef:
                # check keywords
                # e.g. WING 04, CANVAS, etc.
                match = True
                break
        # fallback simple title match
        clean_key = re.sub(r'\[.*?\]|\(.*?\)', '', name).strip()
        if clean_key and len(clean_key) > 6 and clean_key in ef:
            match = True
            break

    if match:
        present.append(name)
    else:
        missing.append(name)

print(f"\nAlready Present in Library: {len(present)}")
print(f"Missing / Not Found in Library: {len(missing)}")

if missing:
    print("\n=== LIST OF MISSING RELEASES ===")
    for m in missing:
        print(f" • {m}")
